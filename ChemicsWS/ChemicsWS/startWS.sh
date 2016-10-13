#!/bin/tcsh

source /disk1/jonsta/dev/AZOrange/AZOrange0.6.3/AZOrange/templateProfile

setenv CHEMICSROOTPATH  "/disk1/jonsta/dev/Chemics/"

setenv ENDPOINTPATH {$CHEMICSROOTPATH}ChemicsEndpoints/Endpoints

setenv PYTHONPATH {$PYTHONPATH}:{$CHEMICSROOTPATH}ChemicsEndpoints/Endpoints

#setenv APWS "192.168.100.238:8082"
#setenv APWS "192.168.100.238:8085"
setenv APWS "192.168.100.27:8085"  # Frigg
#setenv APWS "192.168.100.238:8083"

#echo "Plese make sure that a redis server is already running on the machine!"
#redis-server
#python RQworkerChemics.py  >& RQlogFile_8085.txt &
python RQworkerChemics.py  >& RQlogFile.txt &

python startChemics.py 
