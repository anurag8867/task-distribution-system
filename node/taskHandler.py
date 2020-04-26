import logging

from core.comm.TDSResponse import TDSResponse
from core.comm.TDSRequest import TDSRequest
from node.taskExecuter import taskExecuter
from node.nodeClient import nodeClient
from core.core.config import config

taskExecuterObj = taskExecuter()
TDSResponseObj = TDSResponse()
TDSRequestObj = TDSRequest()
nodeClientObj = nodeClient()
configObj = config()


class taskHandler:

    # def startTaskHandler(self):
    #     nodeServerObj.startServer()

    # it will prepare the response to sent back to coordinator
    def prepareResponse(self, executionStatus, taskId, nodeId):
        try:
            string = executionStatus.split('/$/$/', 2)
            if string[0] == configObj.statusCode['SUCCESS']:
                TDSResponseObj.setStatus(configObj.taskResultEnums['SUCCESS'])
                TDSResponseObj.setErrorCode(0)
                TDSResponseObj.setErrorMessage(string[1])
            else:
                TDSResponseObj.setStatus(configObj.taskResultEnums['FAILED'])
                TDSResponseObj.setErrorCode(1)
                TDSResponseObj.setErrorMessage(string[1])
            if string[2]:
                TDSResponseObj.setResultBuffer(string[2])
            else:
                TDSResponseObj.setResultBuffer('')
            TDSResponseObj.setTaskId(taskId)
            TDSResponseObj.setNodeId(nodeId)
            TDSResponseObj.setMethod('task-result')
            logging.info('Response is prepared to sent back to coordinator')
            return TDSResponseObj
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise Exception(str(e))

    # it will process the task to resolve it
    def processRequest(self, TDSRequest):
        try:
            logging.info('Execution of the task has started')
            executionStatus = taskExecuterObj.executeTask(TDSRequest)
            logging.info('Execution of the task has completed')
            if TDSRequest._taskId and TDSRequest._nodeId:
                prepareResonse = taskHandler().prepareResponse(executionStatus, TDSRequest._taskId, TDSRequest._nodeId)
            else:
                logging.error("It doesn't have node and task ID")
            return prepareResonse
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise Exception(str(e))
