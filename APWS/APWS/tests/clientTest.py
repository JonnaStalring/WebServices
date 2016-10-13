import urllib2
import urllib
import json
import requests

#MYCLIENT = "192.168.100.27:8081" # Frigg
MYCLIENT = "192.168.100.238:8082" # Thor
#MYCLIENT = "chemics.medivir.com:8085"



def testHelpText():

    url = 'http://'+MYCLIENT+'/api/help'
    response = requests.get(url)
    print "Functions and help text"
    print response.text


def testSingle(smiles):

    smiles = urllib.quote(smiles)
    #url = 'http://'+MYCLIENT+'/prediction/HeavyAtomCount/123/'+smiles+'/DummyProject/DummySeries'
    url = 'http://'+MYCLIENT+'/prediction/logP/123/'+smiles+'/DummyProject/DummySeries'
    response = requests.get(url)
    print "Response from single molecule execution"
    print response.text


def testMultiple():

    url = 'http://'+MYCLIENT+'/batchPredictions/HeavyAtomCount'
    smilesDict = { ID : {"smiles": smiles, "project" : "dummyProject", "series": "dummySeries"},
                  "Simeprevir" : {"smiles": "CC1=C(C=CC2=C1N=C(C=C2OC3CC4C(C3)C(=O)N(CCCCC=CC5CC5(NC4=O)C(=O)NS(=O)(=O)C6CC6)C)C7=NC(=CS7)C(C)C)OC", "project" : "dummyProject", "series": "dummySeries"},
                  "L-alanine" : {"smiles": urllib.quote("N[C@@H](C)C(=O)O"), "project" : "dummyProject", "series": "dummySeries"},
                  "Ibuprofen" : {"smiles": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O", "project" : "dummyProject", "series": "dummySeries"}}
    myData = json.dumps(smilesDict)

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(url, data=myData, headers = headers)

    print "Response from batch execution"
    print response.text



if __name__ == "__main__":

    print "Testing web service: ", MYCLIENT
    #testUrllib2()
    #smiles = "C#N"
    #ID = "Cyanide"
    smiles = "CC1=C(C=CC2=C1N=C(C=C2OC3CC4C(C3)C(=O)N(CCCCC=CC5CC5(NC4=O)C(=O)NS(=O)(=O)C6CC6)C)C7=NC(=CS7)C(C)C)OC"
    ID = "Simeprevir"
    #smiles = "CCO"
    #ID = "Ethanol"
    smiles = "C1=CC=NC=C1"
    testSingle(smiles)
    #testMultiple()
    #testHelpText()
