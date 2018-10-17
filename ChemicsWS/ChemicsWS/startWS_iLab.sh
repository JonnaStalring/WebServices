#!/bin/tcsh

source /home/centos/dev/AZOrange/templateProfile

setenv CHEMICSROOTPATH  "/home/centos/Chemics/WebServices/"

setenv ENDPOINTPATH {$CHEMICSROOTPATH}ChemicsEndpoints/Endpoints/

setenv PYTHONPATH {$PYTHONPATH}:{$CHEMICSROOTPATH}ChemicsEndpoints/Endpoints/

#setenv APWS "172.31.32.201:22"  
setenv APWS "172.31.32.201:8085"  

#echo "Plese make sure that a redis server is already running on the machine!"
#redis-server
#python RQworkerChemics.py  >& RQlogFile_8085.txt &
python RQworkerChemics.py  >& RQlogFile.txt &

python startChemics.py 
