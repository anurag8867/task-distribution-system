import multiprocessing
import logging
import socket

from coordinator.socketHandler import socketHandler
from coordinator.taskScheduler import taskScheduler
from coordinator.healthMonitor import healthMonitor
from TDSConfiguration import TDS_Configuration
from core.logging.TDSLogger import TDSLogger

TDSConfiguration = TDS_Configuration()
taskSchedulerObj = taskScheduler()
healthMonitorObj = healthMonitor()
TDSLoggerObj = TDSLogger()


class server:
    def multiprocessCoordinator(self):  # Multithreading has global interpreter lock, So, I am using multiprocessing
        startTaskSchedulerThread = multiprocessing.Process(target=self.startTaskScheduler)
        startTaskSchedulerThread.start()
        startHealthMonitorThread = multiprocessing.Process(target=healthMonitorObj.checkNodeStatus)
        startHealthMonitorThread.start()
        self.startServer()
        # startServerThread = multiprocessing.Process(target=self.startServer)
        # startServerThread.start()

    def startServer(self):
        try:
            self.generateLogs()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((TDSConfiguration.getIpAddr(), TDSConfiguration.getPort()))
            logging.info('Server is running on port 4000')
            s.listen(5)
            while True:
                conn, addr = s.accept()
                logging.info("Resquest has reached to coordinator and ready to process further")
                socketHandler().processRequest(conn)
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise Exception(str(e))

    def generateLogs(
            self):  # It will save the logs for this particular process at the local direcotr of the respective server.
        try:
            TDSLoggerObj.getLogsAtAbsFilePath()
        except socket.error as err:
            logging.exception("Log genration has failed %s" % (err) + "in generateLogs of coordinator/server.py")
        return

    def startTaskScheduler(self):
        try:
            taskSchedulerObj.run()
        except:
            logging.exception('An error occurred in startTaskScheduler of coordinator/server.py.')
        return

    def getSocket(self):
        try:
            return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            logging.exception('An error occurred in startTaskScheduler of coordinator/server.py.')


server().multiprocessCoordinator()
