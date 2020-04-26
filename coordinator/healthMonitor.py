import logging
import socket
import errno
import time

from coordinator.database.nodeRepository import nodeRepository
from core.core.unicodeToString import unicodeToString
from core.comm.TDSRequest import TDSRequest
from core.core.config import config

unicodeToStringObj = unicodeToString()
nodeRepositoryObj = nodeRepository()
TDSRequestObj = TDSRequest()
configObj = config()


class healthMonitor:

    def checkNodeStatus(self):
       try:
           while True:
               logging.info('Health monitor is running')
               totalNodes = nodeRepositoryObj.getAllNodes()
               time.sleep(10)
               for Node in totalNodes:
                   response = self.getResponse(Node)
                   time.sleep(1)
                   if response == configObj.server['NOT-OPERATIONAL']:
                       logging.info(str(Node) + ': NOT-OPERATIONAL')
                       isNodeStatechanged = nodeRepositoryObj.modifyNodeStatus(Node[0], 3)
                       logging.info(Node, response)

                   elif response == configObj.server['AVAILABLE']:
                       logging.info(str(Node) + ': AVAILABLE')
                       nodeRepositoryObj.modifyNodeStatus(Node[0], 1)
                       logging.info(Node, response)

       except Exception as e:
           logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
           raise Exception(str(e))

    def getResponse(self, TDSRequestObj):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((unicodeToStringObj.unicodeToString(TDSRequestObj[1]), TDSRequestObj[2]))
            return "Server is ready to accept the request"
        except s._sock as err:
            logging.exception('Timeout!!! Try again...')
        except Exception as err:
            if (err.errno and (err.errno == errno.ECONNREFUSED or err.errno == errno.ECONNRESET)) or err.message == \
                    configObj.error['TIMED_OUT']:
                logging.exception("Error Code:" + str(err.errno) + "  &&  " + "Error Message:" + err.message)
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(2)
                    s.connect((unicodeToStringObj.unicodeToString(TDSRequestObj[1]), TDSRequestObj[2]))
                    return "Server is ready to accept the request"
                except Exception as err:
                    if (err.errno and (
                            err.errno == errno.ECONNREFUSED or err.errno == errno.ECONNRESET)) or err.message == \
                            configObj.error['TIMED_OUT']:
                        logging.exception("Error Code:" + str(err.errno) + "  &&  " + "Error Message:" + err.message)
                        try:
                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            s.settimeout(2)
                            s.connect((unicodeToStringObj.unicodeToString(TDSRequestObj[1]), TDSRequestObj[2]))
                            return "Server is ready to accept the request"
                        except Exception as err:
                            if (err.errno and (
                                    err.errno == errno.ECONNREFUSED or err.errno == errno.ECONNRESET)) or err.message == \
                                    configObj.error['TIMED_OUT']:
                                logging.exception("Server is dead, changing the status in databse: " + err.message)
                                return "Server is not ready"
            elif err.strerror and (err.strerror == configObj.error['CONNECTION_REFUSED']):
                logging.exception("Error Code: " + str(err.errno) + " && " + err.strerror)

        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise Exception(str(e))


# healthMonitor().checkNodeStatus()
