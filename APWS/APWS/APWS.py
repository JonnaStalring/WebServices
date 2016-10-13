from flask import Flask, url_for
from flask import abort
from flask import request
from flask import make_response
from flask import jsonify
from flask import json
import logging
import string
import time
import imp
import os
import sys
import urllib


APMODELCODEPATH = "/disk1/jonsta/dev/Chemics/APWS/APWS/APEndpoints"
SCRATCHDIR = "/tmp/Chemics"

# Instansiate the WS
app = Flask(__name__)


@app.route('/')
def index():
    """Hello world method"""
    return "Hello, World! APWS is up and running!"


@app.route('/api/help', methods = ['GET'])
def help():
    """Print available functions and their documentation."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)


def getSinglePred(endpoint, ID, smiles, project = "dummyProject", series = "dummySeries"):

    # Import the endpoint specific module
    path = os.path.join(APMODELCODEPATH, endpoint)
    moduleName = "predict"+endpoint
    fid, pathname, description = imp.find_module(moduleName, [path])
    endpointModule = imp.load_module(moduleName, fid, pathname, description)

    # Call the endpoint specific method
    prediction, confidence, status = getattr(endpointModule, "predict"+endpoint)(ID, smiles, project, series, APMODELCODEPATH)
    fid.close()
    return prediction, confidence, status


def getBatchPred(molList, jobID):
   
    endpoint = "AllAPendpoints"

    # Import the endpoint specific module
    path = os.path.join(APMODELCODEPATH, endpoint)
    moduleName = "predict"+endpoint
    fid, pathname, description = imp.find_module(moduleName, [path])
    endpointModule = imp.load_module(moduleName, fid, pathname, description)

    # Call the endpoint specific method
    molList, status = getattr(endpointModule, "predict"+endpoint)(molList, jobID, APMODELCODEPATH)
    fid.close()
    return molList, status



@app.route('/prediction/<endpoint>/<ID>/<path:smiles>/<project>/<series>')
def prediction(endpoint, ID, smiles, project, series):
    """
    Get prediction of endpoint for a single molecule. 
    ID - molecular identifier
    smiles - assumed to be a url encoded proper smiles string
    project - should be an established project name in MVDB or a dummy string if a non-project specific prediction is requested
    series - should be an integer or a dummy string is the prediction is not series specific
    """

    smiles = urllib.unquote(str(smiles))
    # Predict
    prediction, confidence, status = getSinglePred(endpoint, ID, smiles, project, series)
    if prediction and prediction != "None":
        smiles = urllib.quote(str(smiles))
        JSONobj = jsonify(ID=ID, smiles=smiles, project=project, series=series, prediction=prediction, confidence=confidence)
        return make_response(JSONobj, 200)
    elif status == "ADMET Predictor License busy":
        app.logger.error('License busy, no prediction for: '+endpoint+ " in project and series "+project+" "+series)
        return make_response(jsonify({"error": "ADMET Predictor License busy"}), 200)
    else:
        app.logger.error(' No model available for endpoint: '+endpoint+ " in project and series "+project+" "+series)
        return make_response(jsonify({"error": "ADMET Predictor unable to predict. Please check the smiles."}), 200)


@app.route('/batchPredictions/<jobID>', methods = ['POST'])
def batchPredictions(jobID):

    """ Only for AllAPendpoints"""

    molList = request.json
    molList, status = getBatchPred(molList, jobID)
    if status != "Finished":
        app.logger.error('Status: '+str(status))
    try:
        JSONobj = jsonify(batchResults = molList)
        #JSONobj = jsonify(molList)
        return make_response(JSONobj, 200)
    except:
        app.logger.error(' Error making JSON object from batch prediction')
        return make_response(jsonify({"error": "ERROR IN RESULTS FORMAT"}), 200)


#@app.route('/cancelBatchPredictions/<jobID>',  methods = ['GET'])
@app.route('/cancelBatchPredictions/<jobID>')
def cancelBatchPredictions(jobID):

    try:
        # Get pid from file
        fid = open(os.path.join(SCRATCHDIR, jobID+".txt"))
        pidAP = string.strip(fid.readline())
        fid.close()
        print "Killing process with pid ", pidAP
        os.system("kill -9 "+pidAP)
        return  make_response("Killed", 200)
    except:
        app.logger.error('Unable to kill the ADMET Predictor process')
        return make_response(jsonify({"error": "ERROR KILLING AP JOB"}), 200)



if __name__ == '__main__':

    # Reading arguments: port(number), debugMode(True/False), threaded(True/False) 
    # Last 2 arg true only for production mode
    port = int(sys.argv[1])
    debugMode = eval(sys.argv[2])
    threadMode = eval(sys.argv[3])

    print "Starting the WS on port: ", port
    if debugMode:
        print "Running in debug and not production mode"
    if threadMode:
        print "Running threaded. OBS only for production mode (2nd arg False)."  
    
    # Setting the mode
    app.debug = debugMode

    print "*********** Starting the application ******************"
    app.run(host='0.0.0.0', port=port, threaded=threadMode)
   
