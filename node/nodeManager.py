import logging
import sys

from core.logging.TDSLogger import TDSLogger
from socket import error as socket_error
from node.nodeRequest import nodeRequest
from node.nodeServer import nodeServer
from core.core.node import node

nodeRequestObj = nodeRequest()
nodeServerObj = nodeServer()
TDSLoggerObj = TDSLogger()
nodeObj = node()


class nodeManager:
    def startNodeManager(self):
        TDSLoggerObj.getLogsAtAbsFilePath()# It will save the logs for this particular process at the local direcotry of the respective server.
        msg = raw_input('Enter your name: ')
        # First parameter will be operation[query, queue, result] and second parameter will be path of the task
        while (1):
            print 'Type node-register or node-status 418'
            sys.stdout.write('Hi Mr %s> ' % msg)
            inputCommand = sys.stdin.readline().strip()
            # inputCommand = 'node-status 419'
            inputCommand = 'node-register'
            try:
                if (inputCommand == 'quit'):
                    break
                else:
                    string = inputCommand.split(' ', 1)
                if (string[0].lower() == 'node-register'):
                    logging.info('User has entered node-register')
                    response = nodeRequestObj.registerNode()
                    if hasattr(response, 'head') and response.head['nodeId'] is not 'None':
                        logging.info('Node Registered with ' + response.head['nodeId'])
                        nodeServerObj.startServer()
                    else:
                        logging.error('Node is not registered' + 'because' + response._errorMessage)
                        break

                elif (string[0].lower() == 'node-status'):
                    logging.info('User has entered query')
                    response = nodeRequestObj.getNodeStatus(str(string[1]))
                    logging.info("Status of Node having nodeId as " + response.head['nodeId'] + " is " + response.head[
                        'nodeStatus'])
                else:
                    logging.error('Not a valid command')
            except Exception as e:
                logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
                raise


nodeManager().startNodeManager()
