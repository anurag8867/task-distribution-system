import unittest

from coordinator.database.clientRepository import clientRepository
from core.core.client import client

clientObj = client()
clientRepositoryObj = clientRepository()


class test_clientRepository(unittest.TestCase):
    global clientId
    # pre - requisite
    def setupClient(self):
        clientObj.setHostName('hostName')
        clientObj.setUserName('userName')
        return clientObj

    def testAdd(self):
        global clientId
        clientId = clientRepositoryObj.add(self.setupClient())
        self.assertTrue(clientId)

    def testDeleteWithValidId(self):
        global clientId
        self.assertEqual(clientRepositoryObj.delete((931)), 0)
        # self.assertNotEqual(clientRepositoryObj.delete(("xxx")), 0)

    def testDeleteWithInValidId(self):
        global clientId
        self.assertNotEqual(clientRepositoryObj.delete(("xxx")), 0)


if __name__ == '__main__':
    unittest.main()
