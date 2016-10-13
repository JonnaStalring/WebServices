import string
import urllib
import requests
import json
import time

MYSERVER = "192.168.100.27:8081"
#MYSERVER = "chemics.medivir.com:8085"

def startBatchJob(MVDict, endpoint):
    url = 'http://'+MYSERVER+'/startBatchPredictionsMV/'+endpoint
    myData = json.dumps(MVDict)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(url, data=myData, headers = headers)
    return json.loads(response.text)

def getBatchJobResult(jobID):
    url = 'http://'+MYSERVER+'/getBatchPredictions/'+jobID
    response = requests.get(url)
    return json.loads(response.text)

def getStatus(jobID):
    url = 'http://'+MYSERVER+'/getStatus/'+jobID
    response = requests.get(url)
    return json.loads(response.text)


def testBatchAsync(endpoint):

    TIMEOUT = 30
    MVDict = [{ "ID" : "MV084958", "project" : "dummyProject", "series": "dummySeries"},
              {"ID" : "MV087263", "project" : "dummyProject", "series": "dummySeries"},
              {"ID" : "MV087333", "project" : "dummyProject", "series": "dummySeries"}]
    result = startBatchJob(MVDict, endpoint)
    jobID = str(result["jobID"])
    runTime = 0
    while runTime < TIMEOUT:
         status = getStatus(jobID)
         print "Status ", status["jobStatus"] 
         if string.find(status["jobStatus"], "Completed") != -1:
             runTime = TIMEOUT + 1
             result = getBatchJobResult(jobID)
         else:
             print "Job not finished. Waiting 5 s"
             time.sleep(5)
             runTime = runTime + 5

    print json.dumps(result)

if __name__ == "__main__":

    #endpoint = "AllAPendpoints"
    endpoint = "logP"
    testBatchAsync(endpoint)
