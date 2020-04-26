from core.comm.TDSProtocol import TDSProtocol


class TDSRequest(TDSProtocol):
    # def __init__(self, request):
    #     self.request = request

    global head
    head = {}

    def setParameters(self, key, value):
        head.update({key: value})
        self.head = head

    def getParameters(self, key):
        return head[key]

    def setMethod(self, method):
        self.setParameters("method", method)

    def getMethod(self):
        return self.getParameters("method")

    def setTaskId(self, taskId):
        self._taskId = taskId
    def setNodeId(self, nodeId):
        self._nodeId = nodeId
    def getTaskId(self):
        return self._taskId
    def getNodeId(self, nodeId):
        return self._nodeId
    def setAssignedNodeId(self, assignedNodeid):
        self._assignedNodeid = assignedNodeid
    def getAssignedNodeId(self):
        return self._assignedNodeid

# print TDS_Request().setParameters({'hell': 'hell'})
# print head
# dict['Age']
