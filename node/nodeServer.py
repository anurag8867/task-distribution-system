import multiprocessing
import logging
import socket

from coordinator.TDSConfiguration import TDS_Configuration
from node.taskReceiver import taskReceiver
from core.logging.TDSLogger import TDSLogger

TDSConfigurationObj = TDS_Configuration()
taskReceiverObj = taskReceiver()
TDSLoggerObj = TDSLogger()


class nodeServer:
    def startServer(self):
        try:
            # It will save the logs for this particular process at the local direcotry
            # of the respective server.
            HOST = TDSConfigurationObj.getIpAddr()
            PORT = TDSConfigurationObj.getNodePort()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            logging.info("Server has started at"+ str(HOST)  +" and " + str(PORT))
            logging.info("Server is ready to process the request")
            s.listen(5)
            while True:
                conn, addr = s.accept()
                startTaskReceiverThread = multiprocessing.Process(target=taskReceiverObj.nodeThread, args=(conn, ))
                startTaskReceiverThread.start()
        except socket.error as err:
            s.close()
            logging.exception("socket creation failed with error %s" % (err))
            raise
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise

# To check Health of this node
# nodeServer().startServer()
