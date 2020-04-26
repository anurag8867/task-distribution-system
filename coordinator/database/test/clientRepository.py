import unittest
# from coordinator import clientRepository
from core.core.client import client

clientObj = client()
from coordinator.database.clientRepository import clientRepository

clientRepositoryObj = clientRepository()


class test_clientRepository(unittest.TestCase):
    def testAddDelete(self):
        clientObj.setHostName('hostName')
        clientObj.setUserName('userName')
        clientId = clientRepositoryObj.add(clientObj)
        self.assertTrue(clientId)
        self.assertEqual(clientRepositoryObj.delete((clientId)), 0)
        self.assertNotEqual(clientRepositoryObj.delete(("xxx")), 0)


if __name__ == '__main__':
    unittest.main()
