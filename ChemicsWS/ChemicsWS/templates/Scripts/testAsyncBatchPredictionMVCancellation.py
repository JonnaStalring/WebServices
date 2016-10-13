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


def cancelJob(jobID, APjobID = None):
    url = 'http://'+MYSERVER+'/jobCancellation/'+jobID+"/"+APjobID
    print url
    response = requests.get(url)
    return json.loads(response.text)


def getMVlist():
     fileName = "AllMVnumbersSMILES_1200_nofrag.txt"
     fid = open(fileName)
     MVlist = []
     for line in fid:
         lineList = string.split(line)
         smiles = lineList[0]
         ID = string.strip(lineList[1])
         MVlist.append(ID)
     fid.close()
     return MVlist


def testBatchAsyncCancel(endpoint):

    TIMEOUT = 600
    CANCELTIMEOUT = 10

    # Get molecules
    MVlist = getMVlist()
    smilesDict = []
    for elem in MVlist:
        smilesDict.append({"ID" :elem, "project" : "DummyProject", "series" : "DummySeries"})
    print "Number of submitted molecules ", len(smilesDict)

    # Start the job
    result = startBatchJob(smilesDict, endpoint)
    jobID = result["jobID"]
    APjobID = result["APjobID"]
    print "Result from startBatch ", jobID, APjobID

    # Check status 
    runTime = 0
    while runTime < TIMEOUT:
         status = getStatus(jobID)
         print "status", status
         if string.find(status["jobStatus"], "Completed") != -1:
             runTime = TIMEOUT + 1
             result = getBatchJobResult(jobID)
         elif status["jobStatus"] != "No job with this ID":
             print "Job not finished. Waiting 5 s"
             time.sleep(5)
             runTime = runTime + 5
             if runTime > CANCELTIMEOUT:
                 print "Cancelling job"
                 cancelResp = cancelJob(jobID, APjobID)
                 print cancelResp
                 status = getStatus(jobID)
                 print "status ", status
                 runTime = TIMEOUT + 1
         else:
             runTime = TIMEOUT + 1

    print json.dumps(result)

if __name__ == "__main__":

    endpoint = "AllAPendpoints"
    #endpoint = "logP"
    testBatchAsyncCancel(endpoint)
