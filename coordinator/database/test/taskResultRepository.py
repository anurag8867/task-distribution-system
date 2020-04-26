import unittest
from node.taskHandler import taskHandler

taskHandlerObj = taskHandler()
from coordinator.database.taskResultRepository import taskResultRepository

taskResultRepositoryObj = taskResultRepository()
from core.core.client import client
from core.core.task import task
from coordinator.database.taskRepository import taskRepository

taskRepositoryObj = taskRepository()
clientObj = client()
taskObj = task()


class taskResultRepository(unittest.TestCase):
    def testAddDelete(self):
        taskObj.setTaskName('taskName')
        taskObj.setTaskParameters('parameters')
        taskObj.setTaskExePath('xxxxxxxx')
        taskObj.setUserId(str(100))
        taskObj.setTaskState(1)
        taskId = taskRepositoryObj.add(taskObj)
        taskResultId = taskResultRepositoryObj.add(taskHandlerObj.prepareResonse(200, taskId))
        self.assertTrue(taskResultId)
        self.assertEqual(taskResultRepositoryObj.delete(taskResultId), 0)
        self.assertNotEqual(taskResultRepositoryObj.delete(("xxx")), 0)
        self.assertTrue(taskId)
        self.assertEqual(taskRepositoryObj.delete(taskId), 0)
        self.assertNotEqual(taskRepositoryObj.delete(("xxx")), 0)


if __name__ == '__main__':
    unittest.main()
