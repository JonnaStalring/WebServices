import urllib2
import urllib
import json
import requests
import string
import time
import unittest

#MYSERVER = "0.0.0.0:8081"
MYSERVER = "10.247.2.96:8081"  # On Linux11
#MYSERVER = "chemics.medivir.com"
#MYSERVER = "chemics.medivir.com:8085" # Test
#MYSERVER = "192.168.100.27:8081"
#MYSERVER = "192.168.100.27:8085"


class TestChemics(unittest.TestCase):

    def hidetestSingleRDK(self):
        #endpoint = "logP"
        endpoint = "TPSA"
        #endpoint = "AllAPendpoints"
        smiles = "OC1COc2ccccc2OCCOCCOc2ccccc2OC1"
        smiles = urllib.quote(smiles)
        url = 'http://'+MYSERVER+'/prediction/'+endpoint+'/123/'+smiles+'/DummyProject/DummySeries'
        print url
        response = requests.get(url)
        print "Response from single molecule execution"
        print response.text
        respDict = json.loads(response.text)
        pred = float(respDict["prediction"])
        #self.assertEqual(4.589, round(pred, 3))
        self.assertEqual(66.38, round(pred, 2)) # TPSA

    def testSingleAZO(self):
        endpoint = "ADOI"
        smiles = "OC1COc2ccccc2OCCOCCOc2ccccc2OC1"
        #smiles = "Nc1ccc(CC2=CC=CC2)cc1"
        smiles = urllib.quote(smiles)
        url = 'http://'+MYSERVER+'/prediction/'+endpoint+'/123/'+smiles+'/None/None'
        print url
        response = requests.get(url)
        print "Response from single molecule execution"
        print response.text
        respDict = json.loads(response.text)
        pred = respDict["prediction"]
        self.assertEqual("Inactive", pred) 


    def hidetestSingleSA(self): # SMARTS definition file missing
        endpoint = "SA2D"
        smiles = "Nc1ccc(CC2=CC=CC2)cc1"
        smiles = urllib.quote(smiles)
        url = 'http://'+MYSERVER+'/prediction/'+endpoint+'/123/'+smiles+'/DummyProject/DummySeries'
        print url
        response = requests.get(url)
        print "Response from single molecule execution"
        print response.text
        respDict = json.loads(response.text)
        pred = respDict["prediction"]
        self.assertEqual("Aromatic_Amine", pred)


    def hidetestMultiple(self):
        #endpoint = "logP"
        endpoint = "TPSA"
        #endpoint = "AllAPendpoints"
        url = 'http://'+MYSERVER+'/batchPredictions/'+endpoint
        smilesDict = [{ "ID" : "Simeprevir", "smiles": "ACC1=C(C=CC2=C1N=C(C=C2OC3CC4C(C3)C(=O)N(CCCCC=CC5CC5(NC4=O)C(=O)NS(=O)(=O)C6CC6)C)C7=NC(=CS7)C(C)C)OC", "project" : "dummyProject", "series": "dummySeries"},
                      {"ID" : "L-alanine", "smiles": urllib.quote("N[C@@H](C)C(=O)O"), "project" : "dummyProject", "series": "dummySeries"},
                      {"ID" : "Ibuprofen", "smiles": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O", "project" : "dummyProject", "series": "dummySeries"}]
        myData = json.dumps(smilesDict)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(url, data=myData, headers = headers)
        print "Response from batch execution"
        print response.text
        respDict = json.loads(response.text)
        status = respDict["batchResults"][0]["status"]   # First smiles is wrong
        self.assertEqual("Error", status)
        pred = float(respDict["batchResults"][1]["prediction"])
        self.assertEqual(63.32, round(pred, 2))
        pred = float(respDict["batchResults"][2]["prediction"])
        self.assertEqual(37.3, round(pred, 2))


    def hidetestMultipleAZO(self):
        endpoint = "ADOI"
        url = 'http://'+MYSERVER+'/batchPredictions/'+endpoint
        smilesDict = [{ "ID" : "Simeprevir", "smiles": "ACC1=C(C=CC2=C1N=C(C=C2OC3CC4C(C3)C(=O)N(CCCCC=CC5CC5(NC4=O)C(=O)NS(=O)(=O)C6CC6)C)C7=NC(=CS7)C(C)C)OC", "project" : "None", "series": "None"},
                      {"ID" : "L-alanine", "smiles": urllib.quote("N[C@@H](C)C(=O)O"), "project" : "None", "series": "None"},
                      {"ID" : "Ibuprofen", "smiles": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O", "project" : "None", "series": "None"}]
        myData = json.dumps(smilesDict)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(url, data=myData, headers = headers)
        print "Response from batch execution"
        print response.text
        respDict = json.loads(response.text)
 
        print respDict

        status = respDict["batchResults"][0]["status"]   # First smiles is wrong
        self.assertEqual("Error", status)
        pred = respDict["batchResults"][1]["prediction"]
        self.assertEqual("Inactive", pred)
        pred = respDict["batchResults"][2]["prediction"]
        self.assertEqual("Inactive", pred)



    def hidetestMultipleSA(self):  # No SA file
        endpoint = "SA2D"
        url = 'http://'+MYSERVER+'/batchPredictions/'+endpoint
        smilesDict = [{ "ID" : "ArAmine", "smiles": "Nc1ccc(CC2=CC=CC2)cc1", "project" : "dummyProject", "series": "dummySeries"},
                      {"ID" : "Benzylamine", "smiles": urllib.quote("NCc1ccccc1"), "project" : "dummyProject", "series": "dummySeries"},
                      {"ID" : "Thiophene", "smiles": urllib.quote("c1ccc(-c2ccsc2)cc1"), "project" : "dummyProject", "series": "dummySeries"},
                      {"ID" : "Furan", "smiles": "c1ccc(-c2ccoc2)cc1", "project" : "dummyProject", "series": "dummySeries"}]
        myData = json.dumps(smilesDict)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(url, data=myData, headers = headers)
        print "Response from batch execution"
        print response.text
        respDict = json.loads(response.text)
        pred = respDict["batchResults"][1]["prediction"]
        self.assertEqual("Benzylamine", pred)
        pred = respDict["batchResults"][2]["prediction"]
        self.assertEqual("Thiophene", pred)


    def hidetestMultipleMVAllAP(self):  # Requires compound name and ADMET Predictor
        #endpoint = "logP"
        #endpoint = "TPSA"
        endpoint = "AllAPendpoints"
        #MVlist = ["MV080290", "MV007515"]
        MVlist = ["MV089083", "MV089045"]
        url = 'http://'+MYSERVER+'/batchPredictionsMV/'+endpoint
        MVdictList = []
        for elem in MVlist:
            MVdictList.append({"ID" :elem, "project" : "DummyProject", "series" : "DummySeries"})
        myData = json.dumps(MVdictList)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(url, data=myData, headers = headers)
        print "Response from batch execution with AllAPendpoints"
        print response.text
        respDict = json.loads(response.text)
        status = respDict["batchResults"][1]["status"]
        self.assertEqual("Finished", status)
        for elem in respDict["batchResults"]:
            if elem["endpoint"] == "Sp" and elem["ID"] == "MV080290":
                pred = float(elem["prediction"])
                print pred 
        self.assertEqual(40.98, round(pred, 2))


    def hidetestMultipleMV(self): # Requires compound name
        endpoint = "logP"
        #endpoint = "AllAPendpoints"
        MVlist = ["MV080290", "MV007515"] 
        url = 'http://'+MYSERVER+'/batchPredictionsMV/'+endpoint
        MVdictList = []
        for elem in MVlist:
            MVdictList.append({"ID" :elem, "project" : "DummyProject", "series" : "DummySeries"})
        myData = json.dumps(MVdictList)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(url, data=myData, headers = headers)
        print "Response from batch execution"
        print response.text
        respDict = json.loads(response.text)
        status = respDict["batchResults"][1]["status"]   
        self.assertEqual("Finished", status)
        pred = float(respDict["batchResults"][0]["prediction"])
        self.assertEqual(2.273, round(pred, 3))


    def startJob(self, smiles, endpoint):
        url = 'http://'+MYSERVER+'/startPrediction/'+endpoint+'/ID/'+smiles+'/dummy/dummy'
        response = requests.get(url)
        return json.loads(response.text)

    def getJobResult(self, jobID):
        url = 'http://'+MYSERVER+'/getPrediction/'+jobID
        response = requests.get(url)
        return json.loads(response.text)

    def cancelJob(self, jobID, APjobID = None):
        url = 'http://'+MYSERVER+'/jobCancellation/'+jobID+"/"+APjobID
        print url
        response = requests.get(url)
        return json.loads(response.text)


    def hidetestSingleAsync(self):
        smiles = "Nc1ccc(CC2=CC=CC2)cc1"
        TIMEOUT = 50
        endpoint = "TPSA"
        result = self.startJob(smiles, endpoint)
        jobID = result["jobID"]
        print jobID
        runTime = 0
        while runTime < TIMEOUT:
             result = self.getJobResult(jobID)
             print result
             if result["status"] == "Finished" or result["status"] == "Error" :
                 runTime = TIMEOUT + 1
             else:
                 print "Job not finished. Waiting 5 s"
                 time.sleep(5)
                 runTime = runTime + 5
        pred = float(result["prediction"])
        self.assertEqual(26.02, round(pred, 2))

    def startBatchJob(self, smilesDict, endpoint):
        url = 'http://'+MYSERVER+'/startBatchPredictions/'+endpoint
        myData = json.dumps(smilesDict)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(url, data=myData, headers = headers)
        return json.loads(response.text)

    def getBatchJobResult(self, jobID):
        url = 'http://'+MYSERVER+'/getBatchPredictions/'+jobID
        response = requests.get(url)
        return json.loads(response.text)
        #return response.text

    def getStatus(self, jobID):
        url = 'http://'+MYSERVER+'/getStatus/'+jobID
        response = requests.get(url)
        return json.loads(response.text)

    def hidetestBatchAsync(self):  # Using molecular names
         TIMEOUT = 200
         endpoint = "ADOI"
         #endpoint = "SA2D"
         #endpoint = "MDCK"
         #endpoint = "TPSA"
         #endpoint = "AllAPendpoints"
         smilesDict = [{ "ID" : "ArAmine", "smiles": "Nc1ccc(CC2=CC=CC2)cc1", "project" : "None", "series": "None"},
                      {"ID" : "Benzylamine", "smiles": urllib.quote("NCc1ccccc1"), "project" : "None", "series": "None"},
                      {"ID" : "Thiophene", "smiles": urllib.quote("c1ccc(-c2ccsc2)cc1"), "project" : "None", "series": "None"},
                      {"ID" : "Furan", "smiles": "c1ccc(-c2ccoc2)cc1", "project" : "None", "series": "None"}]
         result = self.startBatchJob(smilesDict, endpoint)
         jobID = result["jobID"]
         runTime = 0
         while runTime < TIMEOUT:
              status = self.getStatus(jobID)
              print "Status ", status
              if string.find(status["jobStatus"], "Completed") != -1 or string.find(status["jobStatus"], "Incomplete") != -1:
              #if status["jobStatus"] == "Finished":
                  runTime = TIMEOUT + 1
                  result = self.getBatchJobResult(jobID)
              else:
                  print "Job not finished. Waiting 1 s"
                  time.sleep(1)
                  runTime = runTime + 1
         print result

         status = result["batchResults"][0]["status"] 
         self.assertEqual("Finished", status)
         pred = result["batchResults"][1]["prediction"]
         self.assertEqual("Inactive", pred)
         pred = result["batchResults"][2]["prediction"]
         self.assertEqual("Inactive", pred)
    

    def hidetestAllAPEP(self):  # ADMET Predictor
        smiles = "CC1=C"
        APendpoints = ["logP", "logD", "MDCK", "Peff", "Sp", "RuleOf5", "RuleOf3", "Acidic_pKa", "Acidic_pKa_74prox", "Basic_pKa", \
                       "Basic_pKa_74prox", "Mixed_pKa", "Mixed_pKa_74prox"]
        smiles = urllib.quote(smiles)
        for endpoint in APendpoints:
            url = 'http://'+MYSERVER+'/prediction/'+endpoint+'/123/'+smiles+'/DummyProject/DummySeries'
            print "url ", url
            response = requests.get(url)
            print "Prediction for ", endpoint
            print response.text
            respDict = json.loads(response.text)
            status = respDict["status"]
            self.assertEqual("Finished", status)


    def hidegetMVlist(self):
        fileName = "AllMVnumbersSMILES_1000.txt"
        #fileName = "AllMVnumbersSMILES_3000_nofrag.txt"
        #fileName = "AllMVnumbersSMILES_small.txt"
        fid = open(fileName)
        MVlist = []
        for line in fid:
            lineList = string.split(line)
            smiles = lineList[0]
            ID = string.strip(lineList[1])
            MVlist.append(ID)
        fid.close()
        return MVlist


    def hidetestBatchAsyncCancel(self):

        TIMEOUT = 600
        CANCELTIMEOUT = 10
        endpoint = "AllAPendpoints"

        # Get molecules
        MVlist = self.getMVlist()
        smilesDict = []
        for elem in MVlist:
            smilesDict.append({"ID" :elem, "project" : "DummyProject", "series" : "DummySeries"})
        print "Number of submitted molecules ", len(smilesDict)

        # Start the job
        result = self.startBatchJob(smilesDict, endpoint)
        jobID = result["jobID"]
        APjobID = result["APjobID"]
        print "Result from startBatch ", jobID, APjobID

        # Check status 
        runTime = 0
        while runTime < TIMEOUT:
             status = self.getStatus(jobID)
             print "status", status
             if string.find(status["jobStatus"], "Completed") != -1:
                 runTime = TIMEOUT + 1
                 result = self.getBatchJobResult(jobID)
             elif status["jobStatus"] != "No job with this ID":
                 print "Job not finished. Waiting 5 s"
                 time.sleep(5)
                 runTime = runTime + 5
                 if runTime > CANCELTIMEOUT:
                     print "Cancelling job"
                     cancelResp = self.cancelJob(jobID, APjobID)
                     print cancelResp
                     status = self.getStatus(jobID)
                     print "status ", status
                     runTime = TIMEOUT + 1
             else:
                 runTime = TIMEOUT + 1

        self.assertEqual(cancelResp["jobStatus"], 'Job cancelled')



if __name__ == '__main__':

    unittest.main()



