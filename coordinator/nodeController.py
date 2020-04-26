import logging

from coordinator.database.taskResultRepository import taskResultRepository
from coordinator.database.taskRepository import taskRepository
from coordinator.database.nodeRepository import nodeRepository
from coordinator.taskDispatcher import taskDispatcher
from core.comm.TDSResponse import TDSResponse
from core.core.config import config
from core.core.node import node

taskResultRepositoryObj = taskResultRepository()
nodeRepositoryObj = nodeRepository()
nodeRepositoryObj = nodeRepository()
taskDispatcherObj = taskDispatcher()
taskRepositoryObj = taskRepository()
TDSResponseObj = TDSResponse()
configObj = config()
nodeObj = node()


class nodeController:
    def getNodeStatus(self, nodeId):
        try:
            nodeStatus = nodeRepositoryObj.getNodeStatusByNodeId(nodeId)
            TDSResponseObj.setValue("nodeId", nodeId)
            TDSResponseObj.setValue("nodeStatus", nodeStatus)
            return TDSResponseObj
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
        raise

    def registerNode(self, request):
        try:
            nodeObj.setIp(request._sourceIp)
            nodeObj.setPort(request._sourcePort)
            nodeObj.setStatus(configObj.nodeStateEnums['AVAILABLE'])
            nodeId = nodeRepositoryObj.add(nodeObj)
            return nodeId
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
        raise

    def prepareTaskResponse(self, taskId):
        try:
            TDSResponseObj.setTaskId(str(taskId))
            TDSResponseObj.setTaskResult('Completed :)')
            return TDSResponseObj
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise Exception(str(e))

    def prepareNodeResponse(self, nodeId):
        try:
            if nodeId:
                TDSResponseObj.setValue("nodeId", str(nodeId))
            else:
                TDSResponseObj.setErrorCode("102")
                TDSResponseObj.setErrorMessage("Unable to register node")
            return TDSResponseObj
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
        raise Exception(str(e))

    def registerNodeRequest(self, TDSRequest):
        try:
            logging.info("registerNodeRequest coordinator/nodeController.py")
            nodeId = self.registerNode(TDSRequest)
            response = self.prepareNodeResponse(nodeId)
            return response
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise Exception(str(e))

    def updateTaskState(self, taskId, taskState):
        taskUpdateSatus = taskRepositoryObj.updateTaskState(taskId, taskState)
        return taskUpdateSatus

    def addTaskResult(self, taskResultResponse):
        try:
            taskResultId = taskResultRepositoryObj.add(taskResultResponse)
            # TO DO- find task id
            # TO DO- find NodeID
            if taskRepositoryObj.updateTaskState(taskResultResponse._taskId, configObj.taskStateEnums['COMPLETED']):
                logging.info('state of the task has updated')
            else:
                logging.error('OOPS! state of the task has not updated')

            if nodeRepositoryObj.modifyNodeStatus(taskResultResponse._nodeId, configObj.nodeStateEnums['AVAILABLE']):
                logging.info('state of the task has updated')
            else:
                logging.error('OOPS! state of the node has not updated')
                # get task id here as well
            logging.info("taskResult of task " + str(
                taskResultResponse._taskId) + " has saved into task result Db having taskResultId of "
                         + str(taskResultId))
            return self.prepareTaskResponse(taskResultResponse._taskId)
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise Exception(str(e))

    def processRequest(self, TDSRequest):
        try:
            logging.info("processing request")
            if TDSRequest.head['method'] == 'node-status':
                response = self.getNodeStatus(TDSRequest.head['node-id'])
                return response
            elif TDSRequest.head['method'] == 'node-register':
                response = self.registerNodeRequest(TDSRequest)
                return response
            elif TDSRequest.head['method'] == 'task-result':
                response = self.addTaskResult(TDSRequest)
                # return response
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise Exception(str(e))
