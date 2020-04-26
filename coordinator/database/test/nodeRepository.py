import unittest
# from coordinator import clientRepository
from core.core.client import client
from core.core.task import task
from coordinator.database.taskRepository import taskRepository
from coordinator.taskRepository import taskRepository
from node.nodeRequest import nodeRequest
from coordinator.database.taskRepository import taskRepository
from coordinator.database.nodeRepository import nodeRepository

nodeRepositoryObj = nodeRepository()
nodeRequestObj = nodeRequest()
taskRepositoryObj = taskRepository()
clientObj = client()
taskObj = task()

from coordinator.database.clientRepository import clientRepository

clientRepositoryObj = clientRepository()


class nodeRepository(unittest.TestCase):
    def testAddDelete(self):
        nodeId = nodeRepositoryObj.add(nodeRequestObj.prepareRequest())
        self.assertTrue(nodeId)
        self.assertEqual(taskRepositoryObj.delete(nodeId), 0)
        self.assertNotEqual(taskRepositoryObj.delete(("xxx")), 0)


if __name__ == '__main__':
    unittest.main()
