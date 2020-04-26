import subprocess
import datetime
import logging
import os

from core.comm.TDSResponse import TDSResponse

TDSResponseObj = TDSResponse()


class taskExecuter:

    def writeTaskInFilePath(self, TDSRequest, filePath):
        try:
            file = open(filePath, 'w')
            file.write(TDSRequest._data)
            logging.info('task has written at ' + filePath)
            return
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise


    def getFilePath(self, TDSRequest):
        try:
            fileName = self.prepareFileName(TDSRequest)
            self.saveFile(TDSRequest, fileName)
            filePath = os.path.abspath(fileName)
            return filePath
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise

    def prepareFileName(self, TDSRequest):
        try:
            date = datetime.datetime.now()
            fileName = 'taskFiles/' + TDSRequest.head['taskName'][0:TDSRequest.head['taskName'].index('.')] + '-' + str(
                date) + '.py'
            filePath = os.path.abspath(fileName)
            if filePath:
                return filePath
            return logging.exception("File is not saved over the node because file path was nor established")
        except Exception as e:
            logging.exception("An exception occurred in prepareFileName node/taskExecuter.py")
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise

    # this function is responsible to resolve or execute the task
    def executeTask(self, TDSRequest):
        responseStatus = 200
        filePath = self.prepareFileName(TDSRequest)
        self.writeTaskInFilePath(TDSRequest, filePath)
        try:
            # execfile(filePath)
            p = subprocess.Popen(["python", "-u", filePath], stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
            executedData = p.stdout.readline()
            #deleting the saved file
            os.remove(filePath)
            logging.info('task has Resolved with No error')
            TDSResponseObj.setErrorMessage("Null")
            return str(responseStatus) + "/$/$/" + str(None) + "/$/$/" + executedData
        except Exception as e:
            logging.exception("An exception occurred resolveTask of node/taskExecuter.py")
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            responseStatus = 500
            os.remove(filePath)
            return str(responseStatus) + "/$/$/" + e.message + "/$/$/" + executedData
