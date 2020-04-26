import clientClient
import logging

from coordinator.TDSConfiguration import TDS_Configuration
from core.comm.TDSRequest import TDSRequest

TDSRequestObj = TDSRequest()


class coordinatorController:
    def queueTask(self, inputCommand):
        string = inputCommand.split(' ', 1)
        TDSRequestObj = self.generateBasicRequest()
        TDSRequestObj.setMethod("client-queueTask")
        TDSRequestObj.setParameters("taskName", open(string[1]).name)
        TDSRequestObj.setParameters("parameters", str(string[0]))
        TDSRequestObj.setData(self.convertToByte(string[1]))
        logging.info("TDSRequest has sent to coordinator")
        response = clientClient.server().getResponse(TDSRequestObj)
        logging.info("TDSResponse has came from coordinator")
        return response

    def queryTask(self, inputCommand):
        string = inputCommand.split(' ', 1)
        TDSRequestObj.setMethod("client-queryTask")
        TDSRequestObj.setParameters("taskId", str(string[1]))
        return clientClient.server().getResponse(TDSRequestObj)

    def fetchResult(self, inputCommand):
        string = inputCommand.split(' ', 1)
        TDSRequestObj.setMethod("client-resultTask")
        TDSRequestObj.setParameters("taskId", str(string[1]))
        return clientClient.server().getResponse(TDSRequestObj)

    def generateBasicRequest(self):
        TDSRequestObj.setProtocolVersion("1.0")
        TDSRequestObj.setProtocolFormat("JSON")
        TDSRequestObj.setSourceIp(TDS_Configuration().getIpAddr())
        TDSRequestObj.setSourcePort(TDS_Configuration().getPort())
        TDSRequestObj.setDestIp(TDS_Configuration().getIpAddr())
        TDSRequestObj.setDestPort(TDS_Configuration().getPort())
        TDSRequestObj.setParameters("hostName", TDS_Configuration().getHostName())
        TDSRequestObj.setParameters("userName", TDS_Configuration().getUserName())
        return TDSRequestObj

    def convertToByte(self, taskPath):
        try:
            return open(taskPath, "rb").read().encode()
        except:
            logging.exception("convert To Byte failed")
