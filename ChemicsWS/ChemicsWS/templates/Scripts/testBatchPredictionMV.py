import urllib
import requests
import json

MYSERVER = "192.168.100.27:8081"
#MYSERVER = "chemics.medivir.com:8085"

def testBatchPredictionMV(IDList, endpoint):

    url = 'http://'+MYSERVER+'/batchPredictionsMV/'+endpoint
    print url

    myData = json.dumps(IDList)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(url, data=myData, headers = headers)

    print "Response from batch execution"
    print response.text

if __name__ == "__main__":

    IDList = [{ "ID" : "MV080290","project" : "dummyProject", "series": "dummySeries"},
                  {"ID" : "MV002863","project" : "dummyProject", "series": "dummySeries"}]
    endpoint = "AllAPendpoints"
    testBatchPredictionMV(IDList, endpoint)
