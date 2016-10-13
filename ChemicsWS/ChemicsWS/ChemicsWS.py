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
import copy
import sys
from rdkit import Chem
import urllib
import requests
from rq import Queue
from rq import cancel_job
from rq.job import Job
from RQworkerChemics import conn
import CONFIG
import commands


# Instansiate the WS
print "***************** Starting the web service *******************"
app = Flask(__name__)

# Instansiate the queue
RQqueue = Queue(connection=conn)


@app.route('/')
def index():
    returnStr = "Hello, World! Chemics is up and running! Please use the route api/doc for information about the API of Chemics."
    return returnStr

@app.route('/api/doc', methods = ['GET'])
def doc():
    from flask import send_file
    fileName = CONFIG.CHEMICSROOTPATH+"ChemicsWS/ChemicsWS/templates/ChemicsAPI.pdf"
    fid = open(fileName, 'rb') 
    return send_file(fid, mimetype="pdf")


@app.route('/api/help', methods = ['GET'])
def help():
    """Print available functions and their documentation."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)


@app.route('/ChemicsVersion')
def ChemicsVersion():
     """
     Read from file which has to be manually updated at every tagging
     """
     fid = open(CONFIG.CHEMICSROOTPATH+"ChemicsWS/ChemicsWS/tag.txt")
     tag = string.strip(fid.readline())
     fid.close()
     return tag
# No repo in prod environment
#def ChemicsVersion():
#    status, output = commands.getstatusoutput("git tag")
#    outList = string.split(output, "\n")
#    nTags = len(outList)
#    lastTag = outList[nTags-1]
#    status, tagMessage = commands.getstatusoutput("git show "+lastTag)
#    return tagMessage


@app.route('/endpoints')
def endpoints():
    """ Returns a JSON object with all exposed endpoints.  """
    try:
        endpoints = os.listdir(CONFIG.CHEMICSMODELCODEPATH)
        endpoints.remove("__init__.py")
        JSONobj = jsonify(endpoints=endpoints)
        return make_response(JSONobj, 200)
    except:
        app.logger.error(' Error in dynamically getting endpoint info ')
        return make_response(jsonify({"error": "ERROR"}), 500)


@app.route('/listAllAPendpoints')
def listAllAPendpoints():
    """ Returns a JSON object with all exposed endpoints.  """
    try:
        endpoints = CONFIG.ALLAPENDPOINTSLIST
        JSONobj = jsonify(endpoints=endpoints)
        return make_response(JSONobj, 200)
    except:
        app.logger.error('Error in listAllAPendpoints')
        return make_response(jsonify({"error": "ERROR"}), 500)


@app.route('/D360endpoints')
def D360endpoints():
    """ Returns a JSON object with all exposed endpoints.  """
    try:
        endpoints = CONFIG.D360ENDPOINTHIERARCHY
        JSONobj = jsonify(endpoints=endpoints)
        return make_response(JSONobj, 200)
    except:
        app.logger.error('Error in D360endpoints')
        return make_response(jsonify({"error": "ERROR"}), 500)


def getSinglePred(endpoint, ID, smiles, project = "dummyProject", series = "dummySeries"):

    # Import the endpoint specific module
    path = os.path.join(CONFIG.CHEMICSMODELCODEPATH, endpoint)
    moduleName = "predict"+endpoint
    fid, pathname, description = imp.find_module(moduleName, [path])
    endpointModule = imp.load_module(moduleName, fid, pathname, description)

    # Call the endpoint specific method
    prediction, confidence = getattr(endpointModule, endpoint)(ID, smiles, project, series, CONFIG.CHEMICSMODELDIR)
            
    fid.close()

    return prediction, confidence


def getSmiles(ID):
    url = 'http://semssr-rnd01/MVDBWS/MVDBStructures/'+ID+'?format=smiles'
    response = requests.get(url)
    smiles = json.loads(response.text)
    smiles = urllib.unquote(str(smiles))
    return smiles


def getUnitAndEndpoint(endpoint):
    # Get info for the descEndpoint and unit fields
    for elem in CONFIG.D360ENDPOINTS:
        if elem.keys()[0] == endpoint:
            unit = elem[endpoint]["unit"]
            version = elem[endpoint]["version"]
    descEndpoint = endpoint+"_"+version
    return unit, descEndpoint


def makePrediction(endpoint, ID, smiles, project, series):

    unit, descEndpoint = getUnitAndEndpoint(endpoint)

    # If the model is not from AP Check the quality of the smiles by transforming to an rdkit mol object
    code = CONFIG.ERRORCODE
    mol = Chem.MolFromSmiles(smiles)
    if not mol and endpoint not in CONFIG.APENDPOINTS: 
        descStatus = "Error converting this smiles into an rdk mol object"
        app.logger.error(descStatus+' : '+smiles)
        code = CONFIG.ERRORCODE
        results = {"ID":ID, "smiles":urllib.quote(str(smiles)), "project":project, "series":series, "prediction":"NaN", "confidence":"NaN", "status" : code, "descEndpoint": descEndpoint, "unit": unit, "descStatus": descStatus, "endpoint": endpoint}
    else:
        # Predict
        try:
            prediction, confidence = getSinglePred(endpoint, ID, smiles)
            if prediction == "Error":
                descStatus = confidence
                prediction = "NaN"
                confidence = "NaN"
                code = CONFIG.ERRORCODE
            else:
                code = CONFIG.FINISHEDCODE
                descStatus = code
            results = {"ID":ID, "smiles":urllib.quote(str(smiles)), "project":project, "series":series, "prediction":str(prediction), "confidence":str(confidence), "status" : code, "descEndpoint": descEndpoint, "unit": unit, "descStatus": descStatus, "endpoint": endpoint}
        except:
            app.logger.error("Prediction failed")
            code = CONFIG.ERRORCODE
            descStatus = "Prediction failed"
            results = {"ID":ID, "smiles":urllib.quote(str(smiles)), "project":project, "series":series, "prediction":"NaN", "confidence":"NaN", "status" : code,  "descEndpoint": descEndpoint, "unit": unit, "descStatus": descStatus, "endpoint": endpoint}
    return results, code


@app.route('/predictionMV/<endpoint>/<ID>/<project>/<series>')
def predictionMV(endpoint, ID, project, series):
    """
    Get prediction of endpoint for a single molecule.
    ID - molecular identifier, currently required to be an MV number
    """

    # Get smiles
    try:
        smiles = getSmiles(ID)
    except:
        app.logger.error('Error trying to get the SMILES for the following MV number: '+ID)
        descStatus = 'Error trying to get the SMILES for the following MV number: '+ID
        JSONobj = jsonify(ID=ID, smiles="None", project=project, series=series, prediction="NaN", confidence="NaN", status = CONFIG.ERRORCODE,\
                   descEndpoint= descEndpoint, unit= unit, descStatus= descStatus, endpoint= endpoint)
        return make_response(JSONobj, 200)

    if endpoint != "AllAPendpoints":
        unit, descEndpoint = getUnitAndEndpoint(endpoint)
    else:
        unit = "NaN"
        descEndpoint = "NaN"
     
    # Retry in case AP license is busy
    if endpoint in CONFIG.APENDPOINTS:
        idx = 0
        while idx < CONFIG.CHEMICSTIMEOUT:
            result, code = makePrediction(endpoint, ID, smiles, project, series)
            if result["descStatus"] == CONFIG.APLICENSEBUSY:
                time.sleep(1)
                idx = idx + 1
                JSONobj = jsonify(result)
            else:
                idx = CONFIG.CHEMICSTIMEOUT + 1
                JSONobj = jsonify(result)
    elif endpoint != "AllAPendpoints":
        result, code = makePrediction(endpoint, ID, smiles, project, series)
        JSONobj = jsonify(result)
    else:
        descStatus = "AllAPendpoints only exists for batch calculations. Please use batchPredictionsMV"
        JSONobj = jsonify(ID=ID, smiles=smiles, project=project, series=series, prediction="NaN", confidence="NaN", \
                          status = CONFIG.ERRORCODE, descEndpoint= descEndpoint, unit= unit, descStatus= descStatus, endpoint= endpoint)

    return  make_response(JSONobj, 200)


@app.route('/prediction/<endpoint>/<ID>/<path:smiles>/<project>/<series>')
def prediction(endpoint, ID, smiles, project, series):
    """
    Get prediction of endpoint for a single molecule. 
    ID - molecular identifier
    smiles - assumed to be a url encoded proper smiles string
    project - should be an established project name in MVDB or a dummy string if a non-project specific prediction is requested
    series - should be an integer or a dummy string is the prediction is not series specific
    """

    # Check the quality of the smiles by transforming to an rdkit mol object
    smiles = urllib.unquote(str(smiles))

    if endpoint != "AllAPendpoints":
        unit, descEndpoint = getUnitAndEndpoint(endpoint)
    else:
        unit = "NaN"
        descEndpoint = "NaN"

    # Retry in case AP license is busy
    if endpoint in CONFIG.APENDPOINTS:
        idx = 0
        while idx < CONFIG.CHEMICSTIMEOUT:
            result, code = makePrediction(endpoint, ID, smiles, project, series)
            if result["descStatus"] == CONFIG.APLICENSEBUSY:
                time.sleep(1)
                idx = idx + 1
                JSONobj = jsonify(result)
            else:
                idx = CONFIG.CHEMICSTIMEOUT + 1
                JSONobj = jsonify(result)
    elif endpoint != "AllAPendpoints":
        result, code = makePrediction(endpoint, ID, smiles, project, series)
        JSONobj = jsonify(result)
    else:
        descStatus = "AllAPendpoints only exists for batch calculations. Please use batchPredictionsMV"
        JSONobj = jsonify(ID=ID, smiles=smiles, project=project, series=series, prediction="NaN", confidence="NaN", \
                          status = CONFIG.ERRORCODE, descEndpoint= descEndpoint, unit= unit, descStatus= descStatus, endpoint= endpoint)

    return  make_response(JSONobj, 200)


@app.route('/startPrediction/<endpoint>/<ID>/<path:smiles>/<project>/<series>')
def startPrediction(endpoint, ID, smiles, project, series):
    """
    Get prediction of endpoint for a single molecule.
    ID - molecular identifier
    smiles - assumed to be a url encoded proper smiles string
    project - should be an established project name in MVDB or a dummy string if a non-project specific prediction is requested
    series - should be an integer or a dummy string is the prediction is not series specific
    Returns a job ID if the job could be started
    """

    # Check the quality of the smiles by transforming to an rdkit mol object
    smiles = urllib.unquote(str(smiles))

    # Retry in case AP license is busy
    jobID = "NaN"
    if endpoint in CONFIG.APENDPOINTS:
        idx = 0
        while idx < CONFIG.CHEMICSTIMEOUT:
            job = RQqueue.enqueue_call(func=makePrediction, args=(endpoint, ID, smiles, project, series,), result_ttl=5000)
            time.sleep(5)
            if job.result[1] != CONFIG.S_ERRORCODE:
                idx = CONFIG.CHEMICSTIMEOUT + 1
                jobID = job.get_id()
            else:
                time.sleep(1)
                idx = idx + 1
    else:
        job = RQqueue.enqueue_call(func=makePrediction, args=(endpoint, ID, smiles, project, series,), result_ttl=5000)
        jobID = job.get_id()

    return make_response(jsonify(jobID=jobID), 200)



@app.route('/getPrediction/<jobID>')
def getPrediction(jobID):

    job = Job.fetch(jobID, connection=conn)

    if job.is_finished:
        results = job.result
        JSONobj = jsonify(results[0])
    elif job.is_queued:
        JSONobj = jsonify(ID="tmpID", smiles="None", project="tmpProject", series="tmpSeries", prediction="NaN", confidence="NaN", status = CONFIG.RUNNINGCODE)
    elif job.is_started:
        JSONobj = jsonify(ID="tmpID", smiles="None", project="tmpProject", series="tmpSeries", prediction="NaN", confidence="NaN", status = CONFIG.RUNNINGCODE)
    elif job.is_failed:
        JSONobj = jsonify(ID="tmpID", smiles="None", project="tmpProject", series="tmpSeries", prediction="NaN", confidence="NaN", status = CONFIG.ERRORCODE)

    return make_response(JSONobj, 200)


@app.route('/startPredictionMV/<endpoint>/<ID>/<project>/<series>')
def startPredictionMV(endpoint, ID, project, series):
    """
    Get prediction of endpoint for a single molecule based on MV number (ID must be an MV number).
    ID - molecular identifier
    project - should be an established project name in MVDB or a dummy string if a non-project specific prediction is requested
    series - should be an integer or a dummy string is the prediction is not series specific
    Returns a job ID if the job could be started
    """

    # Get smiles
    try:
        smiles = getSmiles(ID)
    except:
        app.logger.error('Error trying to get the SMILES for the following MV number: '+ID)
        JSONobj = jsonify(ID=ID, smiles="None", project=project, series=series, prediction="NaN", confidence="NaN", status = CONFIG.ERRORCODE)
        return make_response(JSONobj, 200)


    # Retry in case AP license is busy
    jobID = "NaN"
    if endpoint in CONFIG.APENDPOINTS:
        idx = 0
        while idx < CONFIG.CHEMICSTIMEOUT:
            job = RQqueue.enqueue_call(func=makePrediction, args=(endpoint, ID, smiles, project, series,), result_ttl=5000)
            time.sleep(5)
            if job.result[1] != CONFIG.S_ERRORCODE:
                idx = CONFIG.CHEMICSTIMEOUT + 1
                jobID = job.get_id()
            else:
                time.sleep(1)
                idx = idx + 1
    else:
        job = RQqueue.enqueue_call(func=makePrediction, args=(endpoint, ID, smiles, project, series,), result_ttl=5000)
        jobID = job.get_id()

    return make_response(jsonify(jobID=jobID), 200)



def predictMolList(molList, endpoint, APjobID = None):

    if endpoint != "AllAPendpoints":
        unit, descEndpoint = getUnitAndEndpoint(endpoint)
    else:
        unit = "NaN"
        descEndpoint = "NaN"

    if endpoint != "AllAPendpoints":
        for elem in molList:
            elem["endpoint"] = endpoint
            elem["descEndpoint"] = descEndpoint
            elem["unit"] = unit
            if (len(molList) > CONFIG.NAPMOL and endpoint in CONFIG.APENDPOINTS):
                elem["prediction"] = "NaN"
                elem["confidence"] = "NaN"
                elem["status"] = CONFIG.ERRORCODE
                elem["descStatus"] = 'If ADMET Predictor predictions are requested for more than '+str(CONFIG.NAPMOL)+' molecules, please use the AllAPendpoints endpoint'
            else:
                # Check the quality of the smiles by transforming to an rdkit mol object
                smiles = urllib.unquote(str(elem["smiles"]))
                mol = Chem.MolFromSmiles(smiles)
                if not mol and endpoint not in CONFIG.APENDPOINTS and endpoint != "AllAPendpoints":
                    app.logger.error(' Error converting this smiles into an rdk mol object : '+smiles)
                    elem["prediction"] = "NaN"
                    elem["confidence"] = "NaN"
                    elem["smiles"] = urllib.quote(str(smiles))
                    elem["status"] = CONFIG.ERRORCODE
                    elem["descStatus"] = "Error converting this smiles into an rdk mol object"
                else:
                    # Predict and add to molDict
                    project = elem["project"]
                    series = elem["series"]
                    ID = elem["ID"]
                    prediction = "NaN"
                    confidence = "NaN"
                    if endpoint in CONFIG.APENDPOINTS:
                        idx = 0
                        while idx < CONFIG.CHEMICSTIMEOUT:
                            try:
                                prediction, confidence = getSinglePred(endpoint, ID, smiles, project, series)
                                if prediction != "Error":
                                    idx = CONFIG.CHEMICSTIMEOUT + 1
                                    status = CONFIG.FINISHEDCODE
                                elif confidence ==  "ADMET Predictor License busy":
                                    time.sleep(1)
                                    idx = idx + 1
                                    status = CONFIG.ERRORCODE
                                else: 
                                    idx = CONFIG.CHEMICSTIMEOUT + 1
                                    status = CONFIG.ERRORCODE
                            except:
                                idx = CONFIG.CHEMICSTIMEOUT + 1
                                status = CONFIG.ERRORCODE
                    else:
                        try:
                            prediction, confidence = getSinglePred(endpoint, ID, smiles, project, series)
                            status = CONFIG.FINISHEDCODE
                        except:
                            app.logger.error(' Error trying to predict in batch mode. smiles: '+smiles )
                            status = CONFIG.ERRORCODE
                    if prediction == "Error":
                        elem["prediction"] = None
                        elem["confidence"] = None
                        elem["descStatus"] = confidence
                    else:
                        elem["prediction"] = str(prediction)
                        elem["confidence"] = str(confidence)
                        elem["descStatus"] = status
                    elem["smiles"] = urllib.quote(str(smiles))
                    elem["status"] = status
    # Special route for AllAPendpoints, send batches to APWS
    else:
        for elem in molList:
            elem["endpoint"] = endpoint
            elem["descEndpoint"] = descEndpoint
            elem["unit"] = unit
            elem["prediction"] = "NaN"
            elem["confidence"] = "NaN"
            elem["status"] = CONFIG.ERRORCODE
            if len(molList) <= CONFIG.NAPMOLBATCH:
                elem["descStatus"] = 'Problem calling ADMET Predictor'
            else:
                elem["descStatus"] = 'ADMET Predictor predictions cannot be requested for more than '+str(CONFIG.NAPMOLBATCH)+' molecules'
        if len(molList) <= CONFIG.NAPMOLBATCH:
            molList = callAllAPendpoints(molList, endpoint, APjobID)

    return molList


@app.route('/startBatchPredictions/<endpoint>', methods = ['POST'])
def startBatchPredictions(endpoint):
    """
    Predict multiple molecules asynchronous. API as in batchPredictions.
    """
    molList = request.json
    APjobID = "jobID"+string.split(str(time.time()),".")[0]
    job = RQqueue.enqueue_call(func=predictMolList, args=(molList, endpoint, APjobID), result_ttl=5000)
    jobID = job.get_id()
    return make_response(jsonify(jobID=jobID, APjobID = APjobID), 200)


@app.route('/batchPredictions/<endpoint>', methods = ['POST'])
def batchPredictions(endpoint):
    """
    Predict multiple molecules.

    It is assumed that it is a JSON object that is being posted. 
    The JSON object is a list of dictionaries and each dictionary is assumed to have the keys; smiles, project and series. 
    Ex, JSONobj = [{"ID" : ID1, "smiles" : smiles1, "project" = project1, "series": series1},
                     .
                     .
                   {"ID" : IDN, "smiles" : smilesN, "project" = projectN, "series": seriesN}
                  ]     
    The returned object is also a JSON object with the key batchResults, which has the value of a list of dictionaries.
    Ex, JSONobj = {batchResults = [{"ID" : ID1, "smiles" : smiles1, "project" = project1, "series": series1, "prediction": prediction1, "confidence": confidence1, "status" = "Finished"},
                     .
                     .
                   {"ID" : IDN, "smiles" : smiles1, "project" = project1, "series": series1, "prediction": predictionN, "confidence": confidenceN, "status" = "Finished"}
                  ]}     
    """
    molList = request.json
    molList = predictMolList(molList, endpoint)
    try:
        JSONobj = jsonify(batchResults = molList)
        return make_response(JSONobj, 200)
    except:
        app.logger.error(' Error making JSON object from batch prediction')
        return make_response(jsonify({"error": "ERROR IN RESULTS FORMAT"}), 500)


def getSmilesBatch(MVdictList):

    MVlist = []
    for elem in MVdictList:
        MVlist.append(elem["ID"])

    # Get the smiles from mvdb - None returned from MVDB if smiles could not be found
    try:
    #if True:
        url = 'http://semssr-rnd01/MVDBWS/MVDBStructures.svc/compounds'
        smilesDict = {"MVNumberArray":MVlist}
        myData = json.dumps(smilesDict)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(url, data=myData, headers = headers)
        molList = json.loads(response.text)

        # Create the MVlistSMILES object containing a dictionary for each MVnr in MVlist
        # Each dictionary should have MVNumber and SMILES keys. If smiles could not be returned, the SMILES value is set to None
        gotSomeSMILES = False
        gotSmilesList = []
        MVlistSMILES = []
        for molDict in molList:
            if molDict:
                gotSomeSMILES = True
                gotSmilesList.append(molDict["MVNumber"])
        for MVnr in MVlist:  # MVlist now becomes a list of dictionaries MVlistSMILES
            if MVnr not in gotSmilesList:
                MVlistSMILES.append({"MVNumber": MVnr, "SMILES": None})   # Create a molDict object without a smiles for MV numbers with no smiles retrieved
            else:
                for molDict in molList:
                    if molDict:
                        if MVnr == molDict["MVNumber"]:
                            MVlistSMILES.append(molDict)
    except:
        app.logger.error('Error getting smiles from MVDB : '+str(MVlist))
        gotSomeSMILES = False
        MVlistSMILES = []

    return gotSomeSMILES, MVlistSMILES


def getAllAPendpoints(molListResults, APjobID = None):

    # Import the endpoint specific module
    path = os.path.join(CONFIG.CHEMICSMODELCODEPATH, "AllAPendpoints")
    moduleName = "predictAllAPendpoints"
    fid, pathname, description = imp.find_module(moduleName, [path])
    endpointModule = imp.load_module(moduleName, fid, pathname, description)

    # Call the endpoint specific method
    molListResults = getattr(endpointModule, "AllAPendpoints")(molListResults, APjobID, CONFIG.CHEMICSMODELDIR)

    return molListResults



@app.route('/batchPredictionsMV/<endpoint>', methods = ['POST'])
def batchPredictionsMV(endpoint):
    """
    Predict multiple molecules.

    It is assumed that it is a JSON object that is being posted. 
    The JSON object is a list of dictionaries and each dictionary is assumed to have the keys; project and series. 
    Ex, JSONobj = [{"ID" : ID1, "project" : project1, "series": series1},
                     .
                     .
                   {"ID" : IDN, "project" : projectN, "series": seriesN}
                  ]     
    The returned object is also a JSON object with the key batchResults, which has the value of a list of dictionaries.
    Ex, JSONobj = {batchResults = [{"ID" : ID1, "smiles" : smiles1, "project" = project1, "series": series1, "prediction": prediction1, "confidence": confidence1, "status" = "Finished"},
                     .
                     .
                   {"ID" : IDN, "smiles" : smiles1, "project" = project1, "series": series1, "prediction": predictionN, "confidence": confidenceN, "status" = "Finished"}
                  ]}     

    """
    # Get input into a list object
    MVdictList = request.json

    molListResult = getMolListResult(MVdictList, endpoint)

    # Return the response
    try:
        JSONobj = jsonify(batchResults = molListResult)
        return make_response(JSONobj, 200)
    except:
        app.logger.error(' Error making JSON object from batch prediction')
        return make_response(jsonify({"error": "ERROR predicting in batch mode"}), 500)


def getMolListResult(MVdictList, endpoint, APjobID = None):


    if endpoint != "AllAPendpoints":
        unit, descEndpoint = getUnitAndEndpoint(endpoint)
    else:
        unit = ""
        descEndpoint = ""

    # Get smiles from MV number
    gotSomeSMILES, MVlistSMILES = getSmilesBatch(MVdictList)


    molListResult = []
    # None of the MV numbers could be used to retrieve smiles
    if not gotSomeSMILES:
        app.logger.error('No smiles could be retrieved from MVDB : '+str(MVdictList))
        for mol in MVdictList:
            molListResult.append({"ID" : mol["ID"], "smiles" : None, "project" : mol["project"], "series": mol["series"], "endpoint": endpoint, "prediction": "", "confidence": "", "status" : CONFIG.ERRORCODE, "descStatus": 'No smiles could be retrieved from MVDB', "unit": unit, "descEndpoint": descEndpoint})
    else:
        # Allow only AllAPendpoints for more than NAPMOL and less than NAPMOLBATCH molecules
        if (len(MVlistSMILES) > CONFIG.NAPMOL and endpoint in CONFIG.APENDPOINTS) or (len(MVlistSMILES) > CONFIG.NAPMOLBATCH and endpoint == "AllAPendpoints"):
            for cmpd in MVdictList:
                project = cmpd["project"]
                series = cmpd["series"]
                ID = cmpd["ID"]
                for molDict in MVlistSMILES:
                    if molDict["MVNumber"] == ID:
                        try:
                            smiles = urllib.quote(molDict["SMILES"])
                        except:
                            smiles = molDict["SMILES"]
                if len(MVlistSMILES) > CONFIG.NAPMOL and endpoint in CONFIG.APENDPOINTS:
                    molListResult.append({"ID" : ID, "smiles" : smiles, "project" : project, "series": series, "endpoint": endpoint, "prediction": "", "confidence": "", "status" : CONFIG.ERRORCODE, "descStatus" : 'If ADMET Predictor predictions are requested for more than '+str(CONFIG.NAPMOL)+' molecules, please use the AllAPendpoints endpoint for up to'+str(CONFIG.NAPMOLBATCH) +'compounds', "unit": unit, "descEndpoint": descEndpoint})
                else:
                    molListResult.append({"ID" : ID, "smiles" : smiles, "project" : project, "series": series, "endpoint": endpoint, "prediction": "", "confidence": "", "status" : CONFIG.ERRORCODE, "descStatus" : 'ADMET Predictor predictions cannot be requested for more than '+str(CONFIG.NAPMOLBATCH)+' molecules' , "unit": unit, "descEndpoint": descEndpoint})
        else:
            # Loop over all molecules with smiles
            for molDict in MVlistSMILES:
                ID = molDict["MVNumber"]
                for mol in MVdictList:
                    if mol["ID"] == ID:
                        project = mol["project"]
                        series = mol["series"]
                # Only try to predict if a smiles could be obtained
                if molDict["SMILES"]:
                    smiles = molDict["SMILES"]
                    smiles = urllib.unquote(str(smiles))
                    # Check the quality of the smiles by transforming to an rdkit mol object if it is not an AP endpoints
                    noPred = False
                    if endpoint not in CONFIG.APENDPOINTS and endpoint != "AllAPendpoints":
                        mol = Chem.MolFromSmiles(smiles)
                        if not mol:
                            noPred = True
                            app.logger.error(' Error converting this smiles into an rdk mol object : '+smiles)
                            for cmpd in MVdictList:
                                if cmpd["ID"] == ID:
                                    project = cmpd["project"]
                                    series = cmpd["series"]
                            molListResult.append({"ID" : ID, "smiles" : urllib.quote(molDict["SMILES"]), "project" : project, "series": series, "endpoint": endpoint, "prediction": "", "confidence": "", "status" : CONFIG.ERRORCODE, "descStatus" : 'Error converting this smiles into an rdk mol object: '+smiles})
                    # If the existing smiles is OK predict
                    if not noPred:
                        prediction = ""
                        confidence = ""
                        status = CONFIG.ERRORCODE
                        descStatus = status
                        # Repeat attempts to predict with AP
                        if endpoint in CONFIG.APENDPOINTS and endpoint != "AllAPendpoints":
                            idx = 0
                            while idx < CONFIG.CHEMICSTIMEOUT:
                                try:
                                    #smiles = "CCCC."+smiles
                                    prediction, confidence = getSinglePred(endpoint, ID, smiles, project, series)
                                    if prediction != "Error":
                                        idx = CONFIG.CHEMICSTIMEOUT + 1
                                        status = CONFIG.FINISHEDCODE
                                        descStatus = status
                                    elif confidence ==  "ADMET Predictor License busy":
                                        time.sleep(1)
                                        idx = idx + 1
                                        status = CONFIG.ERRORCODE
                                        descStatus = confidence
                                        prediction = ""
                                        confidence = ""
                                    else:
                                        idx = CONFIG.CHEMICSTIMEOUT + 1
                                        status = CONFIG.ERRORCODE
                                        descStatus = confidence
                                        prediction = ""
                                        confidence = ""
                                except:
                                    idx = CONFIG.CHEMICSTIMEOUT + 1
                                    status = CONFIG.ERRORCODE
                                    descStatus = status
                                    prediction = ""
                                    confidence = ""
                        # Non AP endpoint
                        elif endpoint != "AllAPendpoints":
                            try:
                                prediction, confidence = getSinglePred(endpoint, ID, smiles, project, series)
                                status = CONFIG.FINISHEDCODE
                                descStatus = status
                            except:
                                app.logger.error(' Error trying to predict in batch mode. smiles: '+smiles )
                                status = CONFIG.ERRORCODE
                                descStatus = status
                        molListResult.append({"ID": ID, "smiles": urllib.quote(str(smiles)), "project": project, "series": series, "endpoint": endpoint, "prediction": str(prediction), "confidence": str(confidence), "status": status, "descStatus" : descStatus, "unit": unit, "descEndpoint": descEndpoint})
                # No smiles could be retrieved from the DB
                else:
                    app.logger.error('Error retrieving smiles from MVDB for : '+molDict["MVNumber"])
                    for mol in MVdictList:
                        if mol["ID"] == ID:
                            project = mol["project"]
                            series = mol["series"]
                    molListResult.append({"ID" : ID, "smiles" : None, "project" : project, "series": series, "endpoint": endpoint, "prediction": "", "confidence": "", "status" : CONFIG.ERRORCODE, "descStatus": 'No smiles could be retrieved from MVDB', "unit": unit, "descEndpoint": descEndpoint})

    # Special route for AllAPendpoints, send batches to APWS
    if endpoint == "AllAPendpoints" and gotSomeSMILES and len(MVlistSMILES) <= CONFIG.NAPMOLBATCH:
        molListResult = callAllAPendpoints(molListResult, endpoint, APjobID)      

    return molListResult


def callAllAPendpoints(molListResult, endpoint, APjobID):

        if endpoint != "AllAPendpoints":
            unit, descEndpoint = getUnitAndEndpoint(endpoint)
        else:
            unit = ""
            descEndpoint = ""

        idx = 0
        while idx < CONFIG.CHEMICSTIMEOUT:
            try:
                APresults = getAllAPendpoints(molListResult, APjobID)
                isLicenseBusy = False
                # The job was sent to AP
                if isinstance(APresults, dict) and APresults.has_key("batchResults"):
                    result = APresults["batchResults"]
                    for elem in result:
                        if elem["descStatus"] == "ADMET Predictor License busy":
                            isLicenseBusy = True
                            idx = idx + 1
                            time.sleep(1)
                    # The job should contain results because the license was not busy
                    if not isLicenseBusy:
                        idx = CONFIG.CHEMICSTIMEOUT + 1
                        status = CONFIG.FINISHEDCODE
                else:
                    idx = CONFIG.CHEMICSTIMEOUT + 1
                    status = CONFIG.ERRORCODE
                    for elem in result:
                        elem["status"] = status
                        elem["descStatus"] = "No results returned from ADMET Predictor"
                        elem["descEndpoint"] = descEndpoint
                        elem["unit"] = unit
            except:
                idx = CONFIG.CHEMICSTIMEOUT + 1
                status = CONFIG.ERRORCODE
                for elem in result:
                    elem["status"] = status
                    elem["descStatus"] = "Failing calling ADMET Predictor"
                    elem["descEndpoint"] = descEndpoint
                    elem["unit"] = unit

        # Check that all molecules are in result
        resMol = []
        for mol in result:
            molID = mol["ID"]
            resMol.append(molID)
        for elem in molListResult:
            ID = elem["ID"] 
            if ID not in resMol:
                for endpoint in CONFIG.ALLAPENDPOINTSLIST:
                    newElem = copy.deepcopy(elem)
                    unit, descEndpoint = getUnitAndEndpoint(endpoint)
                    newElem["descEndpoint"] = descEndpoint
                    newElem["endpoint"] = endpoint
                    result.append(newElem)

        return result
    



@app.route('/startBatchPredictionsMV/<endpoint>', methods = ['POST'])
def startBatchPredictionsMV(endpoint):
    """
    Predict multiple molecules asynchronous. API as in batchPredictionsMV.
    """
    molList = request.json
    APjobID = "jobID"+string.split(str(time.time()),".")[0]
    try:
        job = RQqueue.enqueue_call(func=getMolListResult, args=(molList, endpoint, APjobID), result_ttl=5000)
        jobID = job.get_id()
    except:
        jobID = None
    return make_response(jsonify(jobID=jobID, APjobID = APjobID), 200)


def parseStatuses(job):
    results = job.result
    descStatusList = []
    statusList = []
    for elem in results:
        descStatus = elem['descStatus']
        status = elem['status']
        if descStatus not in descStatusList:
            descStatusList.append(descStatus)
        if status not in statusList:
            statusList.append(status)
    return statusList, descStatusList



@app.route('/getStatus/<jobID>', methods = ['GET'])
def getStatus(jobID):

    """
    Return values:
    CONFIG.QUEUEDCODE
    CONFIG.RUNNINGCODE
    CONFIG.SUCCESSCODE
    CONFIG.PARTIALSUCCESSCODE
    CONFIG.FAILEDCODE + Specific error message
    """

    try:
        job = Job.fetch(jobID, connection=conn)
        if job.is_finished:
            statusList, descStatusList = parseStatuses(job)
            if len(statusList) == 1: 
                if statusList[0] == CONFIG.FINISHEDCODE:
                    JSONobj = jsonify(jobStatus = CONFIG.SUCCESSCODE)
                elif statusList[0] == CONFIG.ERRORCODE:
                    descStatus = string.join(descStatusList, ",")
                    JSONobj = jsonify(jobStatus = CONFIG.FAILEDCODE+descStatus)
            else:    
                JSONobj = jsonify(jobStatus = CONFIG.PARTIALSUCCESSCODE)
        elif job.is_failed:
            JSONobj = jsonify(jobStatus = CONFIG.FAILEDCODE)
        elif job.is_queued:
            JSONobj = jsonify(jobStatus = CONFIG.QUEUEDCODE)
        else:
            JSONobj = jsonify(jobStatus = CONFIG.RUNNINGCODE)
            # If licens is busy, break
            if job.result:
                statusList, descStatusList = parseStatuses(job)
                if len(statusList) == 1: 
                    descStatus = string.join(descStatusList, ",")
                    if descStatus == "ADMET Predictor License busy":
                        JSONobj = jsonify(jobStatus = CONFIG.FAILEDCODE+descStatus)
            else:
                print "No results yet - Running"
                pass
    except:
        JSONobj = jsonify(jobStatus = "No job with this ID")
        
    return make_response(JSONobj, 200)


@app.route('/jobCancellation/<jobID>/<APjobID>', methods = ['GET'])
def jobCancellation(jobID, APjobID):

    try:
        # Delete job from queue
        job = Job.fetch(jobID, connection=conn)
        Job.cancel(job)
        JSONobj = jsonify(jobStatus = "Job cancelled")
        # Kill AP job  
        APWS = os.environ["APWS"]
        url = 'http://'+APWS+'/cancelBatchPredictions/'+APjobID
        print "Kill the AP job on this url ", url
        response = requests.get(url)
        JSONobj = jsonify(jobStatus = "Job cancelled")
    except:
        JSONobj = jsonify(jobStatus = "Job could not be cancelled")

    return make_response(JSONobj, 200)


@app.route('/getBatchPredictions/<jobID>')
def getBatchPredictions(jobID):
    """
    Get results from asynchronous execution. molList object needed as input because even if the calculations fail the same type of object should 
    be returned. Return object as defined in the batchPredictionsMV method.  
    """

    # Don't require the full object. Return just a status string if not finished. #molList = request.json

    job = Job.fetch(jobID, connection=conn)

    if job.is_finished:
        results = job.result
        JSONobj = jsonify(batchResults = results)
    elif job.is_queued or job.is_started:
        JSONobj = jsonify(jobStatus = CONFIG.RUNNINGCODE)
    elif job.is_failed:
        JSONobj = jsonify(jobStatus = CONFIG.ERRORCODE)
    return make_response(JSONobj, 200)



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

    print "***************** Creating a log file ******************"
    if debugMode:
        logFid = logging.FileHandler("MyWSLogFile.txt", "a")   # Debug
    else:
        logFid = logging.FileHandler("MyWSLogFile.txt", "w")   # Production
    #logFid.setLevel(logging.WARNING)
    #logFid.setLevel(logging.INFO)
    logFid.setLevel(logging.DEBUG)
    logFid.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s ' '[in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(logFid)
    app.logger.warning('Initializing the log file')

    print "*********** Starting the application ******************"
    app.run(host='0.0.0.0', port=port, threaded=threadMode)
   
