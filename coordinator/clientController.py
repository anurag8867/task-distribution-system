import unicodedata
import datetime
import logging
import os

from coordinator.database.taskResultRepository import taskResultRepository
from coordinator.database.clientRepository import clientRepository
from coordinator.database.nodeRepository import nodeRepository
from coordinator.database.taskRepository import taskRepository
from core.comm.TDSResponse import TDSResponse
from core.comm.TDSRequest import TDSRequest
from core.core.client import client
from core.core.config import config
from core.core.task import task
from core.core.node import node

taskResultRepositoryObj = taskResultRepository()
clientRepositoryObj = clientRepository()
nodeRepositoryObj = nodeRepository()
taskRepositoryObj = taskRepository()
TDSResponseObj = TDSResponse()
TDSRequestObj = TDSRequest()
configObj = config()
clientObj = client()
nodeObj = node()
taskObj = task()


class clientController:
    # It will process the request in respect to the commands
    # It is the first point of execution in coordinator side
    def processRequest(self, TDSRequest):
        if (TDSRequest.head['method'] == 'client-queueTask'):
            response = self.processQueueRequest(TDSRequest)
        elif (TDSRequest.head['method'] == 'client-queryTask'):
            response = self.processQueryRequest(TDSRequest)
        elif (TDSRequest.head['method'] == 'client-resultTask'):
            response = self.processResultRequest(TDSRequest)
        else:
            logging.exception("OPPS! Something has gone wrong in processRequest of coordinator/clientController.py")
        return response

    def processQueueRequest(self, request):
       try:
           task = self.queueTask(request)
           response = self.prepareResponse(request)
           response.setStatus("SUCCESS")
           response.setValue("taskId", str(task._taskId))
           response.setValue("taskState", str(task._taskState))
           return response
       except Exception as e:
           logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
           raise Exception(str(e))

    def queueTask(self, TDSRequest):
       try:
           clientId = self.addClient(TDSRequest)
           filePath = self.getFilePath(TDSRequest)
           self.writeTaskInFilePath(TDSRequest, filePath)
           task = self.prepareTask(TDSRequest, clientId, filePath)
           taskId = taskRepositoryObj.add(task)
           if taskId:
               taskObj.setId(taskId)
           else:
               taskObj.setId(0)
           logging.info("Task has registered with " + str(taskId) + " task Id")
           logging.info("Task added successfully with task id: " + str(task._taskId))
           return task
       except Exception as e:
           logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
           raise Exception(str(e))

    def getAvailableNode(self):
        availableNodes = nodeRepositoryObj.getAvailableNodes()
        totalAvailableNodes = len(availableNodes)
        if totalAvailableNodes > 0:
            node = list(availableNodes[totalAvailableNodes - 1])
            # TO DO: Find available node id
        return node[0]

    def prepareTask(self, TDSRequest, clientId, filePath):
        taskObj.setTaskName(TDSRequest.head['taskName'])
        taskObj.setTaskParameters(TDSRequest.head['parameters'])
        taskObj.setTaskExePath(filePath)
        taskObj.setUserId(str(clientId))
        taskObj.setTaskState(configObj.taskStateEnums['PENDING'])
        return taskObj;

    def addClient(self, TDSRequest):
        try:
            clientObj.setHostName(TDSRequest.head['hostName'])
            clientObj.setUserName(TDSRequest.head['userName'])
            clientId = clientRepositoryObj.add(clientObj)
            logging.info("Client added in Database with client id: " + str(clientId))
            return clientId
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise Exception(str(e))

    def convertToByte(self, taskPath):
        try:
            return open(taskPath, "rb").read().encode()
        except:
            logging.exception("convertToByte failed")

    def writeTaskInFilePath(self, TDSRequest, filePath):
        file = open(filePath, 'w')
        file.write(TDSRequest._data)
        return

    def prepareFileName(self, TDSRequest):
        date = datetime.datetime.now()
        filePath = 'taskFiles/' + TDSRequest.head['taskName'][0:TDSRequest.head['taskName'].index('.')] + '-' + str(
            date) + '.py'
        logging.info(filePath)
        return filePath

    def getFilePath(self, TDSRequest):
        fileName = self.prepareFileName(TDSRequest)
        filePath = os.path.abspath(fileName)
        logging.info("Task file strored at: " + filePath)
        return filePath

    def processQueryRequest(self, request):
        try:
            taskState = taskRepositoryObj.getTaskStateById(request.head['taskId'])
            return self.prepareResultResponse(request, taskState)
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise Exception(str(e))

    def processResultRequest(self, request):
       try:
           taskResult = taskResultRepositoryObj.getTaskOutcomeByTaskId(request.head['taskId'])
           response = self.prepareOutcomeResponse(request, taskResult)
           return response
       except Exception as e:
           logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
           raise Exception(str(e))

    def updateTaskState(self, taskId, taskState):
        taskUpdateSatus = taskRepositoryObj.updateTaskState(taskId, taskState)
        return taskUpdateSatus

    def prepareResponse(self, TDSRequest):
        TDSResponseObj.setSourceIp(TDSRequest.getDestIp())
        TDSResponseObj.setDestIp(TDSRequest.getSourceIp())
        TDSResponseObj.setDestPort(TDSRequest.getSourcePort())
        TDSResponseObj.setProtocolFormat(TDSRequest.getProtocolFormat())
        TDSResponseObj.setProtocolVersion(TDSRequest.getProtocolVersion())
        return TDSResponseObj

    # this function will prepare the outcome response
    def prepareOutcomeResponse(self, TDSRequest, taskResult):
        # Converting unicode data into string form
        taskOutcome = unicodedata.normalize('NFKD', taskResult[0][2]).encode('ascii', 'ignore')
        try:
            if (taskOutcome == configObj.taskOutcome['SUCCESS']):
                TDSResponseObj.setTaskId(TDSRequest.head['taskId'])
                TDSResponseObj.setOutcome(taskOutcome)
            elif (taskOutcome == configObj.taskOutcome['FAILED']):
                TDSResponseObj.setTaskId(TDSRequest.head['taskId'])
                TDSResponseObj.setOutcome(taskOutcome)
                TDSResponseObj.setErrorCode(str(taskResult[0][3]))
                TDSResponseObj.setErrorMessage(
                    unicodedata.normalize('NFKD', taskResult[0][4]).encode('ascii', 'ignore'))
            else:
                TDSResponseObj.setTaskId(TDSRequest.head['taskId'])
                TDSResponseObj.setOutcome("Invalid Outcome")
        except Exception as e:
                logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
                raise Exception(str(e))
        return TDSResponseObj;

    # this function will prepare the result response
    def prepareResultResponse(self, TDSRequest, taskState):
        try:
            if (taskState == configObj.taskStates['PENDING']):
                TDSResponseObj.setTaskId(TDSRequest.head['taskId'])
                TDSResponseObj.setStatus(taskState)
            elif (taskState == configObj.taskStates['IN_PROGRESS']):
                TDSResponseObj.setTaskId(TDSRequest.head['taskId'])
                TDSResponseObj.setStatus(taskState)
            elif (taskState == configObj.taskStates['COMPLETED']):
                TDSResponseObj.setTaskId(TDSRequest.head['taskId'])
                TDSResponseObj.setStatus(taskState)
            else:
                TDSResponseObj.setTaskId(TDSRequest.head['taskId'])
                TDSResponseObj.setStatus("Invalid Result")
        except Exception as e:
                logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
                raise Exception(str(e))
        return TDSResponseObj;
