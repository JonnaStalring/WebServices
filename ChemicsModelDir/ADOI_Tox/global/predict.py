# QSAR prediction, reg and class model
import random
import Orange
import orange
from AZutilities import AZOrangePredictor
from AZutilities import dataUtilities
#from AZutilities import ConfPredMondrian
import imp
import os.path

SCRATCHDIR = "/tmp/Chemics/"
if not os.path.exists(SCRATCHDIR):
    os.mkdir(SCRATCHDIR)


def getCP(classDataPath, predData):

    data = dataUtilities.DataTable(classDataPath)

    descList = ["SMILEStoPred", "origSmiles_1"]
    predData = dataUtilities.attributeDeselectionData(predData, descList)

    method = "probPred"
    measure = None
    resultsFile = os.path.join(SCRATCHDIR, "CPresults_"+method+".txt")
    fid = open(resultsFile, "w")
    fid.write("ActualLabel\tLabel1\tLabel2\tPvalue1\tPvalue2\tConf1\tConf2\tPrediction\n")
    fid.close()
    fid = open(resultsFile+"_Mondrian.txt", "w")
    fid.write("ActualLabel\tLabel1\tLabel2\tPvalue1\tPvalue2\tConf1\tConf2\tPrediction\n")
    fid.close()


    # Make sure that predData has a class variable because assumed class values will be used in prediction
    try:
        classValue = predData[0].get_class().value
    except:
        classValue = None
    if not classValue:
        classVar = data.domain.classVar
        newDomain = Orange.data.Domain(predData.domain.attributes, classVar)
        work = dataUtilities.DataTable(newDomain, predData)
    else:
        work = predData

    train = data
    SVMparam = None
    crap, resDict = ConfPredMondrian.getConfPred(train, work, method, SVMparam, measure, resultsFile, verbose = False)
    for key, value in resDict.iteritems():
        pred = value['prediction']
    return pred


def getPrediction(smi, modelDirPath):

    MODELPATH = os.path.join(modelDirPath, "RF_ADmodel")

    #predictor = AZOrangePredictor.AZOrangePredictor(MODELPATH)
    #predictor.getDescriptors(smi)
    #pred = predictor.predict()
    randInt = random.randint(0,1)
    if randInt == 0:
        pred = "Inactive"
    else:
        pred = "Active"
    conf = str(random.randint(0,100))
    #conf = "80"
    if smi == "CCO":  # Dummy value to assure that Anton can test out of AD
        pred = "NaN"
        conf = "NaN"

    return pred, conf



def predict(ID, smiles, modelDirPath):

    prediction, confidence = getPrediction(smiles, modelDirPath)

    return prediction, confidence



if __name__ == "__main__":
    modelDirPath = "."
    pred, conf = predict("123", "CCO", modelDirPath)
    print pred, conf
