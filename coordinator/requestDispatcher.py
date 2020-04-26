import logging

from coordinator.clientController import clientController
from coordinator.nodeController import nodeController


class requestDispatcher:
    def getController(self, TDSRequest):
        if TDSRequest.head['method'] == 'node-register' or TDSRequest.head['method'] == 'node-status' or \
                TDSRequest.head['method'] == 'task-result':
            logging.info("returning a node controller")
            return nodeController
        elif TDSRequest.head['method'] == 'client-queueTask' or TDSRequest.head['method'] == 'client-queryTask' \
                or TDSRequest.head['method'] == 'client-resultTask':
            logging.info("returning a node controller")
            return clientController
