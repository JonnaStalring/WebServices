import urllib
import requests
import json

MYSERVER = "192.168.100.27:8081"
#MYSERVER = "chemics.medivir.com:8085"

def testBatchPrediction(smilesList, endpoint):

    url = 'http://'+MYSERVER+'/batchPredictions/'+endpoint
    print url

    myData = json.dumps(smilesList)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(url, data=myData, headers = headers)

    print "Response from batch execution"
    print response.text

if __name__ == "__main__":

    smilesList = [{ "ID" : "Simeprevir", "smiles": "ACC1=C(C=CC2=C1N=C(C=C2OC3CC4C(C3)C(=O)N(CCCCC=CC5CC5(NC4=O)C(=O)NS(=O)(=O)C6CC6)C)C7=NC(=CS7)C(C)C)OC", "project" : "dummyProject", "series": "dummySeries"},
                  {"ID" : "L-alanine", "smiles": urllib.quote("N[C@@H](C)C(=O)O"), "project" : "dummyProject", "series": "dummySeries"},
                  {"ID" : "Ibuprofen", "smiles": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O", "project" : "dummyProject", "series": "dummySeries"}]
    endpoint = "Basic_pKa"
    testBatchPrediction(smilesList, endpoint)
