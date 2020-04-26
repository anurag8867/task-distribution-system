import unittest

from coordinator.database.clientRepository import clientRepository
from coordinator.database.taskRepository import taskRepository
from core.core.client import client
from core.core.task import task

taskRepositoryObj = taskRepository()
clientObj = client()
taskObj = task()

clientRepositoryObj = clientRepository()


class taskRepositoryTest(unittest.TestCase):
    # pre - requisite
    def setupTask(self):
        taskObj.setTaskName('taskName')
        taskObj.setTaskParameters('parameters')
        taskObj.setTaskExePath('xxxxxxxx')
        taskObj.setUserId(str(100))
        taskObj.setTaskState(1)
        return taskObj

    def testAdd(self):
        taskId = taskRepositoryObj.add(self.setupTask())
        self.assertTrue(taskId)
        self.assertEqual(taskRepositoryObj.delete(taskId), 0)
        self.assertNotEqual(taskRepositoryObj.delete(("xxx")), 0)


if __name__ == '__main__':
    unittest.main()
