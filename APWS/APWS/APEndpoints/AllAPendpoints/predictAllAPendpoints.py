import copy
import string
import time
import os
import urllib
import subprocess
import APutilities
import CONFIG

SCRATCHDIR = "/tmp/Chemics/"

def writeSmiles(smiFileName, molList):
    fid = open(smiFileName, "w")
    fid.write("SMILES\tID\n")
    for elem in molList:
        smiles = urllib.unquote(str(elem["smiles"]))
        ID = str(elem["ID"])
        if smiles != "None":
            fid.write(smiles+"\t"+ID+"\n")
    fid.close()


def getUnitAndEndpoint(endpoint):
    # Get info for the descEndpoint and unit fields
    for elem in CONFIG.D360ENDPOINTS:
        if elem.keys()[0] == endpoint:
            unit = elem[endpoint]["unit"]
            version = elem[endpoint]["version"]
    descEndpoint = endpoint+"_"+version
    return unit, descEndpoint


def getExtremeOld(pKaList):
    mostAcidic = 14
    mostBasic = -14
    noneCount = 0
    for elem in pKaList:
        try:
            pKa = float(elem)
            if pKa < mostAcidic:
                mostAcidic = pKa
            if pKa > mostBasic:
                mostBasic = pKa
        except:
            noneCount = noneCount + 1
    if noneCount == len(pKaList):
        mostAcidic = None
        mostBasic = None
    return mostAcidic, mostBasic


def getHighest(pKaList):
    pKas = []
    for elem in pKaList:
        try:
            pKa = float(elem)
            pKas.append(pKa)
        except:
            pass
    if pKas:
        highest = max(pKas)
    else:
        highest = None
    return highest

def getLowest(pKaList):
    pKas = []
    for elem in pKaList:
        try:
            pKa = float(elem)
            pKas.append(pKa)
        except:
            pass
    if pKas:
        lowest = min(pKas)
    else:
        lowest = None
    return lowest


def predictAllAPendpoints(molList, jobID, CHEMICSMODELDIR):
    """
    RunAP.sh in ChemicsEndpoints/bin directory
    """

    endpointDict = {"logP": "S+logP", "logD": "S+logD", "Acidic_pKa": "S+Acidic_pKa", "Acidic_pKa_74prox": "S+Acidic_pKa", \
                    "Basic_pKa": "S+Basic_pKa", "Basic_pKa_74prox":  "S+Basic_pKa", "MDCK": "S+MDCK", "Mixed_pKa": "S+Mixed_pKa", \
                    "Mixed_pKa_74prox": "S+Mixed_pKa", "Peff": "S+Peff", "RuleOf5": "RuleOf5", "Sp": "S+Sp", \
                    "pKa_mostAcidic": "S+Acidic_pKa", "pKa_mostBasic": "S+Basic_pKa", "RuleOf3": "RuleOf5"}

    SP_NAMES = ["HBD", "HBA", "MWt", "S+logP", "N_FrRotB" ]   # For Rule Of 3 calc

    # Create smi file
    if not os.path.exists(SCRATCHDIR):
        os.mkdir(SCRATCHDIR)
    smiFileName = os.path.join(SCRATCHDIR, "APresults"+str(time.time())+".smi")
    writeSmiles(smiFileName, molList)

    # Run AP shell command
    fileName, ext = os.path.splitext(smiFileName)
    outFileName = fileName+"stdOutAndErr.txt"
    os.chdir(SCRATCHDIR)
    #args = "RunAP.sh -m PCB -y -t SMI "+smiFileName+" >& "+outFileName  # Endpoints can be controlled in the ModelProperties.inp file of the AP installation
    args = "RunAP.sh -y -t SMI "+smiFileName+" >& "+outFileName
    process = subprocess.Popen(args, shell=True)
    pid = process.pid

    # Assure that AP is started
    time.sleep(5)  

    # Get PID by name and write to jobID specific file
    args = 'pgrep ADMET_Predictor'
    p = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
    pidAP = p.communicate()[0]  # Works
    print "Process PID for AP ", pidAP
    jobIDfileName = os.path.join(SCRATCHDIR, jobID+".txt")
    fid = open(jobIDfileName, "w")
    fid.write(str(pidAP))
    fid.close()

    # Dont read results until finished
    process.wait()

    newMolList = []
    # Parse info from the created dat and ots files (same name as smi file but with dat extention)
    if os.path.isfile(fileName+".dat"):
        datFileName = fileName+".dat"
        fid = open(datFileName)
        headerList = string.split(fid.readline(), "\t")
        for line in fid:
            lineList = string.split(line, "\t")
            idx = headerList.index("ID")
            ID = lineList[idx]
            for mol in molList:
                if mol["ID"] == ID:
                    #try:
                    if True:
                        pKaListBasic = []
                        pKaListAcidic = []
                        RuleOf3 = 0
                        for endpoint, SPendpoint in endpointDict.iteritems():
                            unit, descEndpoint = getUnitAndEndpoint(endpoint)
                            if "most" not in endpoint and "RuleOf3" not in endpoint:
                                idx = headerList.index(SPendpoint)
                                prediction = lineList[idx]
                            else:
                                prediction = ""

                            if "74prox" in endpoint:
                                prediction = APutilities.getProxpKa(prediction)
                            elif "pKa" in endpoint and "Basic" in endpoint and "most" not in endpoint:
                                pKaListBasic.extend(string.split(prediction, ";"))
                            elif "pKa" in endpoint and "Acidic" in endpoint and "most" not in endpoint:
                                pKaListAcidic.extend(string.split(prediction, ";"))

                            newmol = copy.deepcopy(mol)
                            newmol["prediction"] = prediction
                            newmol["endpoint"] = endpoint
                            newmol["descEndpoint"] = descEndpoint
                            newmol["unit"] = unit
                            newmol["status"] = "Finished"
                            newmol["descStatus"] = "ADMET Predictor calculation finished"
                            newMolList.append(newmol)

                        # Rule of 3
                        for r3endpoint in SP_NAMES:
                            idx = headerList.index(r3endpoint)
                            prediction = lineList[idx]
                            if r3endpoint == "HBD" and float(prediction) > 3:
                                RuleOf3 = RuleOf3 + 1
                            if r3endpoint == "HBA" and float(prediction) > 3:
                                RuleOf3 = RuleOf3 + 1
                            if r3endpoint == "S+logP" and float(prediction) > 3:
                                RuleOf3 = RuleOf3 + 1
                            if r3endpoint == "N_FrRotB" and float(prediction) > 3:
                                RuleOf3 = RuleOf3 + 1
                            if r3endpoint == "MWt" and float(prediction) > 300:
                                RuleOf3 = RuleOf3 + 1

                        mostAcidic = getLowest(pKaListAcidic)
                        mostBasic = getHighest(pKaListBasic)
                        for newmol in newMolList:
                            if newmol["ID"] == ID:
                                if newmol["endpoint"] == "pKa_mostAcidic":
                                    newmol["prediction"] = mostAcidic
                                elif newmol["endpoint"] == "pKa_mostBasic":
                                    newmol["prediction"] = mostBasic
                                elif newmol["endpoint"] == "RuleOf3":
                                    newmol["prediction"] = RuleOf3
                    else:
                    #except:
                        for endpoint, SPendpoint in endpointDict.iteritems():
                            unit, descEndpoint = getUnitAndEndpoint(endpoint)
                            newmol = copy.deepcopy(mol)
                            newmol["prediction"] = ""
                            newmol["endpoint"] = endpoint
                            newmol["descEndpoint"] = descEndpoint
                            newmol["unit"] = unit
                            newmol["status"] = "Error"
                            newmol["descStatus"] = "ADMET Predictor unable to process this molecule. Please check the smiles."
                            newMolList.append(newmol)
        fid.close()

        # Parse info from the ots file with AD info
        APIDs = []
        try:
            otsFileName = fileName+".ots"
            fid = open(otsFileName)
            headerList = string.split(fid.readline(), "\t")
            for line in fid:
                lineList = string.split(line, "\t")
                idx = headerList.index("Name")
                ID = lineList[idx]
                APIDs.append(ID)
                for mol in newMolList:
                    if mol["ID"] == ID:
                        for endpoint, SPendpoint in endpointDict.iteritems():
                            if "Outsider_of_"+SPendpoint in headerList:
                                idx = headerList.index("Outsider_of_"+SPendpoint)
                                AD = lineList[idx]
                                if AD == "0":
                                    conf = "inAD"
                                else:
                                    conf = "outAD"
                                if mol["endpoint"] == endpoint:
                                    mol["confidence"] = conf
                            else:
                                if mol["endpoint"] == endpoint:
                                    mol["confidence"] = None
            fid.close()
        except:
            for mol in newMolList:
                mol["confidence"] = None
        status = "Finished"
    else:
        newMolList = molList
        isLicenseBusy = APutilities.checkLicenseStatus(outFileName)
        if isLicenseBusy:
            status = "ADMET Predictor License busy"
            for mol in newMolList:
                mol["descStatus"] = status
        else:
            status = "Error executing ADMET Predictor."
            for mol in newMolList:
                mol["descStatus"] = status

    try:
        # Clean up files
        os.system("rm "+smiFileName)
        os.system("rm "+jobIDfileName)
        #os.system("rm "+outFileName)
        #os.system("rm "+datFileName)
        os.system("rm "+otsFileName)
    except: pass 


    return newMolList, status


if __name__ == "__main__":

    ID = "test1"
    smiles = "CC(=O)Nc1ccc(OCC)cc1"
    molList = [{"ID": ID, "smiles": smiles}]
    CHEMICSMODELDIR = "."
    jobID = "dummy"
    newMolList, status = predictAllAPendpoints(molList, jobID, CHEMICSMODELDIR)
    print "Calculation status ", status
    print "Predicted  ", newMolList
