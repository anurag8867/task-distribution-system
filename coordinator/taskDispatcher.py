import cPickle as pickle
import logging
import socket
import errno

from coordinator.TDSConfiguration import TDS_Configuration

TDSConfiguration = TDS_Configuration()

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
from core.core.unicodeToString import unicodeToString
taskResultRepositoryObj = taskResultRepository()
clientRepositoryObj = clientRepository()
nodeRepositoryObj = nodeRepository()
taskRepositoryObj = taskRepository()
unicodeToStringObj = unicodeToString()
TDSResponseObj = TDSResponse()
TDSRequestObj = TDSRequest()
configObj = config()
clientObj = client()
nodeObj = node()
taskObj = task()


class taskDispatcher:
    def dispatchTask(self, task, node):
    # def dispatchTask(self, taskObj, nodeObj):
        taskRepositoryObj.updateAssignedNode(task[0], node[0])
        TDSRequestObj = self.prepareRequest(task, node)
        self.changeNodeStatus(node[0], configObj.nodeStateEnums['BUSY'])
        # see if there is a need to return anything
        response = self.getResponse(TDSRequestObj)
        # Disconnect the client as soon as the request come here
        print "HI Anurag "
        print response

    def changeTaskState(self, taskId, taskState):
        istaskStatechanged = taskRepositoryObj.updateTaskState(taskId, taskState)
        if istaskStatechanged is 1:
            logging.info('Task state has changed')
        else:
            logging.info('OOPS! task state has not changed')
        return


    def changeNodeStatus(self, nodeId, nodeStatus):
        isNodeStatechanged = nodeRepositoryObj.modifyNodeStatus(nodeId, nodeStatus)
        if isNodeStatechanged is 1:
            logging.info('Node state has changed')
        else:
            logging.info('OOPS! Node state has not changed')
        return

    def prepareRequest(self, task, node):
        TDSRequestObj.setProtocolVersion(configObj.protocol['PROTOCOL_VERSION'])
        TDSRequestObj.setSourceIp(unicodeToStringObj.unicodeToString(node[1]))
        TDSRequestObj.setSourcePort(node[2])
        TDSRequestObj.setDestIp(unicodeToStringObj.unicodeToString(node[1]))
        TDSRequestObj.setDestPort(node[2])
        TDSRequestObj.setMethod(configObj.coordinator['COORDINATOR_EXECUTE_TASK'])
        TDSRequestObj.setParameters(configObj.task['TASK_NAME'], unicodeToStringObj.unicodeToString(task[1]))
        TDSRequestObj.setParameters(configObj.task['PARAMETERS'], unicodeToStringObj.unicodeToString(task[2]))
        TDSRequestObj.setData(self.convertToByte(task))
        TDSRequestObj.setTaskId(task[0])
        TDSRequestObj.setNodeId(node[0])
        return TDSRequestObj

    # Convert the data into bytes
    def convertToByte(self, task):
        try:
            return self.readAFile(task).encode()
        except:
            logging.info("convertToByte failed")

    # read the file from the given path and return the data
    def readAFile(self, task):
        return open(self.taskExistPath(task), "rb").read()

    # fetch the task's path from database
    # convert that path from unicode to string
    def taskExistPath(self, task):
        return unicodeToStringObj.unicodeToString(task[3])

    def getResponse(self, TDSRequestObj):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((TDSRequestObj.getDestIp(), 5000))
            # while (1):
            retur = s.send(pickle.dumps(TDSRequestObj))
            response = pickle.loads(s.recv(1024))
            if response.head['method'] == 'task-found':
                self.changeTaskState(TDSRequestObj.getTaskId(), configObj.taskStateEnums['IN_PROGRESS'])

        except s as err:
            if err == errno.ECONNREFUSED or err == errno.ECONNRESET:
                logging.exception("socket creation failed with error %s" % (err))
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise
