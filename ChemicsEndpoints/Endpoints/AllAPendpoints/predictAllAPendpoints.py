import string
import time
import os
import requests
import json
import urllib

def AllAPendpoints(molListResults, jobID, CHEMICSMODELDIR):
    """
    """

    APWS = os.environ["APWS"]

    url = 'http://'+APWS+'/batchPredictions/'+str(jobID)
    myData = json.dumps(molListResults)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        response = requests.post(url, data=myData, headers = headers)
        molListResults = json.loads(response.text)
    except:
        molListResults = "Error calling APWS"

    return molListResults


if __name__ == "__main__":

    print "Neet to create object"
    #ID = "test1"
    #smiles = "CC(=O)Nc1ccc(OCC)cc1"
    #project = "DummyProject"
    #series = "DummySeries"
    #CHEMICSMODELDIR = "."
    #molListResults = AllAPendpoints()
    #print "Predicted logP ", SPlogP, conf
