import logging
import errno
import sys

from core.logging.TDSLogger import TDSLogger
from client import coordinatorController
from core.core.config import config

TDSLoggerObj = TDSLogger()
configObj = config()


class taskManager:
    def startTaskManager(self):
        TDSLoggerObj.getLogsAtAbsFilePath()  # It will save the logs for this particular process at the local direcotry of the respective server.
        msg = raw_input('Enter your name: ')
        while (1):
            print 'Queue! First parameter will be operation[query, queue, result] and second parameter will be path of the task E.G.-> query get.txt'
            sys.stdout.write('Please type %s> ' % msg)
            inputCommand = sys.stdin.readline().strip()
            inputCommand = 'queue hello.txt'
            # inputCommand = 'query 681'
            # inputCommand = 'result 609'
            try:
                if (inputCommand == 'quit'):
                    break

                else:
                    string = inputCommand.split(' ', 1)
                if (string[0].lower() == 'queue'):
                    logging.info('User has entered queue')
                    response = coordinatorController.coordinatorController().queueTask(inputCommand)
                    logging.info('Task Registered with ' + response.head['taskId'] + ' taskId')


                elif (string[0].lower() == 'query'):
                    logging.info('User has entered query')
                    response = coordinatorController.coordinatorController().queryTask(inputCommand)
                    logging.info("Status of the task having taskId as " + response._taskId + " is " + response._status)


                elif (string[0].lower() == 'result'):
                    logging.info('User has entered result')
                    response = coordinatorController.coordinatorController().fetchResult(inputCommand)

                    if response._taskOutcome == configObj.taskOutcome['SUCCESS']:
                        logging.info(
                            "Outcome of the task having taskId as " + response._taskId + " is " + response._taskOutcome)

                    elif response._taskOutcome == configObj.taskOutcome['FAILED']:
                        logging.info(
                            "Outcome of the task having taskId as " + response._taskId + " is " + response._taskOutcome + " with " + response._errorCode
                            + " ERROR CODE and " + response._errorMessage + " as " + "ERROR MESSAGE")

                    else:
                        logging.info("Some unexpected Outcome has come")


                else:
                    logging.exception('Not a valid command')
                    break

            except Exception as e:
                logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
                raise Exception(str(e))


taskManager().startTaskManager()
