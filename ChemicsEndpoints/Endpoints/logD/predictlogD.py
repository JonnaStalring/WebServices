import string
import time
import os
import requests
import json
import urllib
import os

def logD(ID, smiles, project, series, CHEMICSMODELDIR):
    """
    RunAP.sh in ChemicsEndpoints/bin directory
    """

    endpoint = "logD"
    APWS = os.environ["APWS"]
    smiles = urllib.quote(smiles)
    url = 'http://'+APWS+'/prediction/'+endpoint+'/'+ID+'/'+smiles+'/DummyProject/DummySeries'
    response = requests.get(url)
    results = json.loads(response.text)
    try:
        prediction = results["prediction"]
        confidence = results["confidence"]
    except:
        prediction = "Error"
        confidence = results["error"]

    return prediction, confidence


if __name__ == "__main__":

    ID = "test1"
    smiles = "CC(=O)Nc1ccc(OCC)cc1"
    project = "DummyProject"
    series = "DummySeries"
    CHEMICSMODELDIR = "."
    SPlogP, conf = logD(ID, smiles, project, series, CHEMICSMODELDIR)
    print "Predicted logP ", SPlogP, conf
