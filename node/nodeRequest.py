import logging

from coordinator.TDSConfiguration import TDS_Configuration
from core.comm.TDSRequest import TDSRequest
from node.nodeClient import nodeClient

TDSConfigurationObj = TDS_Configuration()
TDSRequestObj = TDSRequest()
TDSRequestObj = TDSRequest()
nodeClientObj = nodeClient()


class nodeRequest:

    def prepareRequest(self):
       try:
           TDSRequestObj.setProtocolVersion('1.0')
           TDSRequestObj.setProtocolFormat('JSON')
           TDSRequestObj.setSourceIp(TDSConfigurationObj.getIpAddr())
           # TDSRequestObj.setSourceIp(random.randint(100000000, 900000011))
           TDSRequestObj.setSourcePort(5000)
           TDSRequestObj.setDestIp(TDSConfigurationObj.getIpAddr())
           TDSRequestObj.setDestPort(TDSConfigurationObj.getPort())
           TDSRequestObj.setParameters("hostName", TDSConfigurationObj.getHostName())
           TDSRequestObj.setParameters("username", TDSConfigurationObj.getUserName())
           TDSRequestObj.setParameters("status", 'AVAILABLE')
           return TDSRequestObj
       except Exception as e:
           logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
       raise

    def registerNode(self):
        try:
            TDSRequestObj = nodeRequest().prepareRequest()
            TDSRequestObj.setMethod('node-register')
            response = nodeClientObj.getResponse(TDSRequestObj)
            return response
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
        raise

        # def startNodeServer(self):
    #     nodeServerObj.startServer()

    # def getNodeStatus(self, nodeId):
    #     # TDSRequestObj = nodeRequest().prepareRequest()
    #     TDSRequestObj.setMethod('node-status')
    #     TDSRequestObj.setParameters('node-id', nodeId)
    #     response = nodeServerObj.getResponse(TDSRequestObj)
    #     return response
# nodeRequest().startNodeServer()