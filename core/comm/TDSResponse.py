from core.comm.TDSProtocol import TDSProtocol

TDS_Protocol = TDSProtocol()


class TDSResponse(TDSProtocol):
    def __init__(self):
        pass

    global head
    head = {}

    def setStatus(self, status):
        self._status = status

    def getStatus(self):
        return self._status

    def setErrorCode(self, errorCode):
        self._errorCode = errorCode

    def setOutcome(self, taskOutcome):
        self._taskOutcome = taskOutcome

    def getErrorCode(self):
        return self._errorCode

    def setErrorMessage(self, errorMessage):
        self._errorMessage = errorMessage

    def setTaskId(self, taskId):
        self._taskId = taskId

    def setTaskResult(self, taskResult):
        self._taskResult = taskResult

    def setNodeId(self, nodeId):
        self._nodeId = nodeId

    def getNodeId(self):
        return self._nodeId

    def setResultBuffer(self, resultBuffer):
        self._resultBuffer = resultBuffer

    def getErrorMessage(self):
        return self._errorMessage

    def setValue(self, key, value):
        head.update({key: value})
        self.head = head

    def setMethod(self, method):
        self.setValue("method", method)

    def getMethod(self, method):
        return head[method]

    def getValue(self, key):
        return head[key]
