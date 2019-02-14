import random
import Orange
import orange
from AZutilities import AZOrangePredictor
from AZutilities import dataUtilities
import imp
import os.path
from rdkit import DataStructs
from rdkit.Chem.Fingerprints import FingerprintMols
from rdkit import Chem
import numpy
from rdkit.Chem import AllChem


SCRATCHDIR = "/tmp/Chemics/"
if not os.path.exists(SCRATCHDIR):
    os.mkdir(SCRATCHDIR)

def getFps(data):

    molList = []
    for ex in data:
        mol = Chem.MolFromSmiles(ex["Smiles"].value)
        if mol:
            molList.append(mol)
        else:
            print ex["Smiles"].value
            print ex["Leonumber"].value
    fps = [FingerprintMols.FingerprintMol(x) for x in molList] # Topological
    #fps = [AllChem.GetMorganFingerprint(x, 2) for x in molList]
    #print "Length of data and fp ", len(data), len(fps)
    return fps

def getDist(queryFp, fps):

    distList = []
    for fp in fps:
        dist = DataStructs.FingerprintSimilarity(queryFp,fp) # Tanimoto
        #dist = DataStructs.DiceSimilarity(queryFp,fp) # Dice
        distList.append(dist)
    distList.sort()
    #medDist = numpy.median(distList[len(distList)-9:len(distList)])
    medDist = numpy.median(distList[len(distList)-4:len(distList)])
    return medDist


def getPrediction(smi, modelDirPath):

    MODELPATH = os.path.join(modelDirPath, "/home/centos/Chemics/WebServices/ChemicsModelDir/ADOI/global/OI_RFmodel")
    train = dataUtilities.DataTable("/home/centos/Chemics/WebServices/ChemicsModelDir/ADOI/global/Assay1350AZOdesc.txt")
    fps = getFps(train)

    predictor = AZOrangePredictor.AZOrangePredictor(MODELPATH)
    predictor.getDescriptors(smi)
    prediction, prob = predictor.predict(True)
    # Normalize prob
    prob = 200*abs(prob)
    if prob > 100:
        prob = 0.98

    # Create an Orange data set to calculate the fp of the smiles
    features = [Orange.data.variable.String("Smiles")]
    domain = Orange.data.Domain(features)
    smiData = Orange.data.Table(domain)
    smiData.append([smi])
    fpsSmiles = getFps(smiData)
    distSmi = getDist(fpsSmiles[0], fps)

    if distSmi < 0.75:  # Definition of outAD
        pred = "NaN"
        conf = "NaN"
    else:
        pred = prediction
        conf = prob 

    return pred, str(conf)


def predict(ID, smiles, modelDirPath):

    prediction, confidence = getPrediction(smiles, modelDirPath)

    return prediction, confidence



if __name__ == "__main__":
    modelDirPath = "."
    #smiles = "Nc1cccc2c1CN(C1CCC(=O)NC1=O)C2=O" # Inactive
    #smiles = "Cc1nc(=Nc2ncc(C(=O)Nc3c(C)cccc3Cl)s2)cc(N2CCN(CCO)CC2)[nH]1" # Active
    #smiles = "COc1cc(N=c2c(C#N)c[nH]c3cc(OCCCN4CCN(C)CC4)c(OC)cc23)c(Cl)cc1Cl" # Inactive
    smiles = "FC(F)(F)CC(=O)N1CCSC12CCN(C2)c3ncnc4[nH]ccc34"
    pred, conf = predict("123", smiles, modelDirPath)
    print pred, conf
