import cPickle as pickle
import multiprocessing
import taskHandler
import logging
import socket
import errno
import time

from coordinator.TDSConfiguration import TDS_Configuration
from core.comm.TDSResponse import TDSResponse
from core.comm.TDSRequest import TDSRequest

TDSConfiguration = TDS_Configuration()
TDSResponseObj = TDSResponse()
TDSRequestObj = TDSRequest()


class taskReceiver:
    def writeResponse(self, TDSRespomse):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((TDSConfiguration.getIpAddr(), TDSConfiguration.getPort()))
            while (1):
                time.sleep(2)
                retur = s.send(pickle.dumps(TDSRespomse))
                response = pickle.loads(s.recv(1024))
        except s as err:
            if err == errno.ECONNREFUSED or err == errno.ECONNRESET:
                logging.exception("socket creation failed with error %s" % (err))
                raise
        except Exception as e:
                logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
                raise Exception(str(e))

    def disconnectCoordinator(self, conn):
        TDSResponseObj.setMethod('task-found')
        logging.info("coordinator is disconnecting from node")
        conn.sendall(pickle.dumps(TDSResponseObj))

    def processNodeRequest(self, conn):
        try:
            TDSRequest = pickle.loads(conn.recv(1024))
            logging.info("Request received in node/taskReceiver.py")
            response = taskHandler.taskHandler().processRequest(TDSRequest)
            logging.info("Process of request has completed in node/taskReceiver.py")
            self.writeResponse(response)
        except Exception as e:
            logging.exception('Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise Exception(str(e))

    def nodeThread(self, conn):
        try:
            startcoordinatorDisconnectorThread = multiprocessing.Process(target=self.disconnectCoordinator, args=(conn,))
            startcoordinatorDisconnectorThread.start()
            time.sleep(2)
            startTaskExecuteThread = multiprocessing.Process(target=self.processNodeRequest, args=(conn,))
            startTaskExecuteThread.start()
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise Exception(str(e))