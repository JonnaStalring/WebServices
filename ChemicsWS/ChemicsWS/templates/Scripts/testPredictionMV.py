import urllib
import requests


MYSERVER = "192.168.100.27:8081"
#MYSERVER = "chemics.medivir.com:8085"

def testSingle(ID, endpoint):

    url = 'http://'+MYSERVER+'/predictionMV/'+endpoint+'/'+ID+'/DummyProject/DummySeries'
    print url
    response = requests.get(url)
    print "Response from single molecule execution"
    print response.text

if __name__ == "__main__":

    ID = "MV002863"
    endpoint = "TPSA"
    testSingle(ID, endpoint)
