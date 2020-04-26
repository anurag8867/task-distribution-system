import unittest
import random

from coordinator.database.clientRepository import clientRepository
from coordinator.database.taskRepository import taskRepository
from coordinator.database.nodeRepository import nodeRepository
from core.comm.TDSRequest import TDSRequest
from node.nodeRequest import nodeRequest
from core.core.client import client
from core.core.task import task

clientRepositoryObj = clientRepository()
nodeRepositoryObj = nodeRepository()
taskRepositoryObj = taskRepository()
nodeRequestObj = nodeRequest()
TDSRequestObj = TDSRequest()
clientObj = client()
taskObj = task()


class nodeRepository(unittest.TestCase):

    # pre - requisite
    def setupNode(self):
        TDSRequestObj.setSourceIp(random.randint(100000000, 900000011))
        TDSRequestObj.setSourcePort(12345678)
        TDSRequestObj.setParameters("status", 'AVAILABLE')
        return TDSRequestObj

    def testAdd(self):
        nodeId = nodeRepositoryObj.add(self.setupNode())
        self.assertTrue(nodeId)
        # self.assertEqual(taskRepositoryObj.delete(nodeId), 0)
        # self.assertNotEqual(taskRepositoryObj.delete(("xxx")), 0)


if __name__ == '__main__':
    unittest.main()
