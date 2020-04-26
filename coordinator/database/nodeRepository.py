import logging

from coordinator.database.DBManager import DB_Manager
from core.core.unicodeToString import unicodeToString

unicodeToStringObj = unicodeToString()
DB_Manager = DB_Manager()
unicodeToStringObj = unicodeToString()


class nodeRepository:

    def add(self, nodeObj):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "INSERT INTO node (nodeIp, nodePort, nodeStatus) VALUES (%s, %s, %s)"
            val = (nodeObj._ip, nodeObj._port, nodeObj._status)
            # val = ("192.168.6.137", 3000, 1)
            # val = ("127.0.0.1", 5000, 1)
            cursor.execute(sql, val)
            connection.commit()
            if cursor.rowcount:
                logging.info('1 node inserted.')
                return cursor._last_insert_id
            else:
                logging.warning("No record inserted.")
                return 'No record inserted.'
        except Exception as e:
            logging.exception(e)
            logging.exception('Error occured while adding data into node')

        finally:
            DB_Manager.closeConnection()

    # add("s",`11111121`)

    def modifyNodeStatus(self, nodeId, nodeStatus):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "UPDATE node SET nodeStatus = " + str(nodeStatus) + " WHERE nodeId = " + str(nodeId)
            cursor.execute(sql)
            connection.commit()
            if cursor.rowcount:
                logging.info("1 node modified.")
            return cursor.rowcount
        except Exception as e:
            logging.exception(e)
            logging.exception('Error occured while adding data into task')
            raise

        finally:
            DB_Manager.closeConnection()

    # modifyNodeStatus("S", 2, 18)

    def delete(self, nodeId):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            # sql = "DELETE FROM node WHERE nodeId = "+ str(nodeId)
            sql = "DELETE FROM node"
            cursor.execute(sql)
            connection.commit()
            if cursor.rowcount:
                print(cursor.rowcount, "record deleted.")
            else:
                print "OOPS !No record deleted---------"

        except Exception as e:
            logging.exception(e)
            logging.exception('Error occured while adding data into task')

        finally:
            DB_Manager.closeConnection()

    # delete("S", 1111111)

    def getAllNodes(self):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM node"
            cursor.execute(sql)
            myresult = cursor.fetchall()
            if myresult:
                logging.info('There are some nodes')
            return myresult

        except Exception as e:
            logging.exception(e)
            logging.exception('Error occured while fetching all the nodes: ' + e.message)
            raise


        finally:
            DB_Manager.closeConnection()

    # getAllNodes("S")

    def getAvailableNodes(self):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM node WHERE nodeStatus='AVAILABLE'"
            cursor.execute(sql)
            myresult = cursor.fetchall()
            if myresult:
                logging.info('There are more than zero available nodes')
            return myresult

        except Exception as e:
            logging.exception(e)
            logging.exception('Error occured while adding data into task')
            raise

        finally:
            DB_Manager.closeConnection()

    def getNodeStatusByNodeId(self, nodeId):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM node WHERE nodeId = " + str(nodeId)

            cursor.execute(sql)
            myresult = cursor.fetchall()
            if myresult:
                logging.info('Node status has found successfully')
                return unicodeToStringObj.unicodeToString(myresult[0][3])

        except Exception as e:
            logging.exception(e)
            logging.exception('Error occured while adding data into task')
            raise

        finally:
            DB_Manager.closeConnection()

    # getNodeStatusByNodeId("S", '402')
