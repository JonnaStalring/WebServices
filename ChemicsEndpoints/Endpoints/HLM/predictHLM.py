import string
import os.path
import imp



def HLM(ID, smiles, project, series, CHEMICSMODELDIR):
    
    # Check if a series specific model is requested 
    if series.isdigit():
        series = "Series"+str(series)
    else:
        series = None
    # Check if a project specific model is requested 
    project = string.replace(project, " ", "_")
    if project == "None": project = None

    if project and series:
        modelPath = os.path.join(CHEMICSMODELDIR, "HLM/local/"+project+"/"+series+"/predict.py")
    elif project and not series:
        modelPath = os.path.join(CHEMICSMODELDIR, "HLM/local/"+project+"/predict.py")
    else:
        modelPath = os.path.join(CHEMICSMODELDIR, "HLM/global/predict.py")

    # Check that the specified model exists
    if os.path.isfile(modelPath):
        modelDirPath, script = os.path.split(modelPath)
        fid, pathname, description = imp.find_module("predict", [modelDirPath])
        endpointModule = imp.load_module("predict", fid, pathname, description)
        prediction, confidence = getattr(endpointModule, "predict")(ID, smiles, modelDirPath)
        fid.close()
    else:
        prediction = None
        confidence = None
        
    return prediction, confidence

if __name__ == "__main__":
    CHEMICSMODELDIR = "/disk1/jonsta/dev/Chemics/ChemicsModelDir/"
    potency, confidence = HLM("123", "CCO", "RSV_FUSION_INHIBITOR", "1", CHEMICSMODELDIR)
    print potency, confidence
