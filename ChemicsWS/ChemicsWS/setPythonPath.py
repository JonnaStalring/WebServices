import os

endpointDir = os.environ["ENDPOINTPATH"]

pythonPath = os.environ["PYTHONPATH"]
pythonPath = pythonPath+str(endpointDir)

dirs = os.listdir(endpointDir)
for dir in dirs:
    path = os.path.join(endpointDir, dir)
    isDir = os.path.isdir(os.path.join(endpointDir, dir))
    if isDir:
        pythonPath = pythonPath+":"+str(path)

print pythonPath

 

