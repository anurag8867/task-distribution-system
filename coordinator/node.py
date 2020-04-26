import datetime
import logging
import os

from coordinator.TDSConfiguration import TDS_Configuration
from core.comm.TDSResponse import TDSResponse
from core.comm.TDSRequest import TDSRequest
from core.core.node import node

TDSConfigurationObj = TDS_Configuration()
TDSResponseObj = TDSResponse()
TDSRequestObj = TDSRequest()
nodeObj = node()


class node:
    def geTaskPath(self, TDSRequest):
        fileName = node().prepareFileName(TDSRequest)
        node().saveFile(TDSRequest, fileName)
        filePath = os.path.abspath(fileName)
        logging.info("Task file strored at: " + filePath)
        return filePath

    def prepareFileName(self, TDSRequest):
        date = datetime.datetime.now()
        filePath = 'taskFiles/name=' + TDSRequest.head['taskName'][0:len(TDSRequest.head['taskName'])-4] \
                   + '/' + str(date) + '.exe'
        return filePath

    def prepareRequest(self):
        TDSRequestObj.setProtocolVersion('1.0')
        TDSRequestObj.setProtocolFormat('JSON')
        TDSRequestObj.setSourceIp(TDSConfigurationObj.getIpAddr())
        TDSRequestObj.setSourcePort(TDSConfigurationObj.getPort())
        TDSRequestObj.setDestIp(TDSConfigurationObj.getIpAddr())
        TDSRequestObj.setDestPort(TDSConfigurationObj.getPort())
        TDSRequestObj.setParameters('hostName', TDSConfigurationObj.getHostName())
        TDSRequestObj.setParameters('userName', TDSConfigurationObj.getUserName())
        return TDSRequestObj
