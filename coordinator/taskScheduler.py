import logging
import time

from coordinator.database.taskResultRepository import taskResultRepository
from coordinator.database.clientRepository import clientRepository
from coordinator.database.nodeRepository import nodeRepository
from coordinator.database.taskRepository import taskRepository
from coordinator.taskDispatcher import taskDispatcher
from core.comm.TDSResponse import TDSResponse
from core.comm.TDSRequest import TDSRequest
from core.core.client import client
from core.core.config import config
from core.core.task import task
from core.core.node import node

taskResultRepositoryObj = taskResultRepository()
clientRepositoryObj = clientRepository()
taskDispatcherObj = taskDispatcher()
nodeRepositoryObj = nodeRepository()
taskRepositoryObj = taskRepository()
TDSResponseObj = TDSResponse()
TDSRequestObj = TDSRequest()
configObj = config()
clientObj = client()
nodeObj = node()
taskObj = task()


class taskScheduler:
    def run(self):
        logging.info('Task Scheduler is ready to schedule the task')
        while True:
            try :
                time.sleep(2)
                pendingTasks = taskRepositoryObj.getTasksByStatus(`'PENDING'`)
                availableNodes = nodeRepositoryObj.getAvailableNodes()
                totalPendingTasks = len(pendingTasks)
                totalAvailableNodes = len(availableNodes)
                check = True
                while (totalPendingTasks > 0 and totalAvailableNodes > 0 and check):
                    check = False
                    time.sleep(2)
                    task = list(pendingTasks[totalPendingTasks - 1])   # Resolve the oldest Task and Node first
                    node = list(availableNodes[totalAvailableNodes - 1])
                    taskDispatcherObj.dispatchTask(task, node)

            except:
                logging.exception("Task scheduler start has failed in run of coordinator/taskScheduler.py")







# taskScheduler().run()