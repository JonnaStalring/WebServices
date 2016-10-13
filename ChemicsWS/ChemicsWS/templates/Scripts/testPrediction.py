import urllib
import requests


MYSERVER = "192.168.100.27:8081"
#MYSERVER = "chemics.medivir.com:8085"

def testSingle(smiles, ID, endpoint):

    smiles = urllib.quote(smiles)
    url = 'http://'+MYSERVER+'/prediction/'+endpoint+'/'+ID+'/'+smiles+'/DummyProject/DummySeries'
    print url
    response = requests.get(url)
    print "Response from single molecule execution"
    print response.text

if __name__ == "__main__":

    smiles = "N(C(=S)NCCc1ncccc1)c1ncc(cc1)C"
    ID = "Ibuprofen"
    endpoint = "logP"
    testSingle(smiles, ID, endpoint)
