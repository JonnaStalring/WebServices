import urllib
import requests


MYSERVER = "192.168.100.27:8081"
#MYSERVER = "chemics.medivir.com:8085"

def D360endpoints():

    url = 'http://'+MYSERVER+'/D360endpoints'
    print url
    response = requests.get(url)
    print response.text

if __name__ == "__main__":

    D360endpoints()
