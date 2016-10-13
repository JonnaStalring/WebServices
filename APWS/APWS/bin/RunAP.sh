#!/bin/sh

# This file must be executable to work! chmod 755!

# In the ADMET_PREDICTOR_PATH variable replace MyADMETPredictorPath with the
# actual path to the directory containing the program's folder
export ADMET_PREDICTOR_PATH=/disk1/jonsta/lib/ADMET_Predictor_v71/

# In SIMPLUS_LICENSE_FILE specify either @IP-Address of the Flexera
# server or @localhost if the server runs locally
#export SIMPLUS_LICENSE_FILE=@localhost
#export SIMPLUS_LICENSE_FILE=@192.168.100.238
export SIMPLUS_LICENSE_FILE=@semssr-flexlm.medivir.com   # Windows server

# Optionally, uncomment FLEXLM_DIAGNOSTICS for extra debug information
# related to Flexera licensing
# export FLEXLM_DIAGNOSTICS=3

# This command executes ADMET Predictor with options given on the command line
echo $*
#exec $ADMET_PREDICTOR_PATH/ADMET_Predictor $* 1 > std_out_sh.txt 2 > std_err.txt
$ADMET_PREDICTOR_PATH/ADMET_Predictor $*
