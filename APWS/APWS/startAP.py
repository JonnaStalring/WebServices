import APWS   # The import will instanciate the WS
from flask import Flask, url_for
import logging
import os


DEBUGMODE = False
#PORT = 8082 # Thor production
#DEBUGLOGFILE = "DebugLogFile.txt"
PORT = 8085  # My dev instance
#PORT = 8090  # Instance for Peter
DEBUGLOGFILE = "DebugLogFile_MyDev.txt"


if not DEBUGMODE:
    APWS.app.debug = False
    threadMode = True
else:
    APWS.app.debug = True
    threadMode = False

if not DEBUGMODE:
   logSid = logging.StreamHandler()
   logSid.setLevel(logging.WARNING)
   logSid.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s ' '[in %(pathname)s:%(lineno)d]'))
   APWS.app.logger.addHandler(logSid)
else:
    logFid = logging.FileHandler(DEBUGLOGFILE, "w") 
    #logFid.setLevel(logging.WARNING)
    logFid.setLevel(logging.INFO)
    logFid.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s ' '[in %(pathname)s:%(lineno)d]'))
    APWS.app.logger.addHandler(logFid)
    APWS.app.logger.warning('Initializing the log file')

# Start the WS
APWS.app.run(host='0.0.0.0', port=PORT, threaded=threadMode)
