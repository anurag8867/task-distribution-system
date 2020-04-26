import datetime
import logging
import sys
import os

# This class will generate the logs in the logs folder with respect to the time at the absolute path of the server
class TDSLogger:
    def getLogsAtAbsFilePath(self):
        try:
            fileName = self.prepareLogFileName()
            filePath = os.path.abspath(fileName)
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                                datefmt='%m-%d %H:%M',
                                filename=filePath,
                                filemode='w')
            # define a Handler which writes INFO messages or higher to the sys.stderr
            console = logging.StreamHandler(sys.stdout)
            # console.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s - %(funcName)s - line %(lineno)d"))
            console.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
            console.setLevel(logging.INFO)
            # add the handler to the root logger
            logging.getLogger('').addHandler(console)
            logging.info("Logs are getting stored at: " + filePath)
        except:
            logging.exception("An exception occurred in getFilePath core/logging/TDSLogger.py")
        return True

    def prepareLogFileName(self):
        try:
            date = datetime.datetime.now()
            fileName = 'logs/' + str(date) + '.log'
        except:
            logging.exception("An exception occurred in prepareFileName core/logging/TDSLogger.py")

        return fileName

# TDSLogger().getLogsAtAbsFilePath()