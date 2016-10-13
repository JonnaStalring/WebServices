import ChemicsWS   # The import will instanciate the WS
from flask import Flask, url_for
import logging
import os


DEBUGMODE = False
DEBUGLOGFILE = "DebugLogFile.txt"
#PORT = 8085 # Test server for Peter
PORT = 8081  # My developer instance


if not DEBUGMODE:
    ChemicsWS.app.debug = False
    threadMode = True
else:
    ChemicsWS.app.debug = True
    threadMode = False

if not DEBUGMODE:
   logSid = logging.StreamHandler()
   logSid.setLevel(logging.WARNING)
   logSid.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s ' '[in %(pathname)s:%(lineno)d]'))
   ChemicsWS.app.logger.addHandler(logSid)
else:
    logFid = logging.FileHandler(DEBUGLOGFILE, "w") 
    #logFid.setLevel(logging.WARNING)
    logFid.setLevel(logging.INFO)
    logFid.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s ' '[in %(pathname)s:%(lineno)d]'))
    ChemicsWS.app.logger.addHandler(logFid)
    ChemicsWS.app.logger.warning('Initializing the log file')

# Start the WS
ChemicsWS.app.run(host='0.0.0.0', port=PORT, threaded=threadMode)
