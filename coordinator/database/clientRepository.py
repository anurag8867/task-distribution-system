import logging

from coordinator.database.DBManager import DB_Manager

DB_Manager = DB_Manager()


class clientRepository:
    def add(self, clientObj):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "INSERT INTO client (hostName, userName) VALUES (%s, %s)"
            val = (clientObj._hostName, clientObj._userName)
            # val = ("111111111", "John")
            cursor.execute(sql, val)
            connection.commit()
            if cursor._last_insert_id:
                logging.info(str(cursor.rowcount) +" client inserted")
                print str(cursor.rowcount) +" client inserted"
                return cursor._last_insert_id
            else:
                logging.warning('Task is not added')
            return

        except Exception as e:
            logging.exception(e)
            logging.exception('Error occured while adding data into task')
            raise

        finally:
            DB_Manager.closeConnection()

    # add("s", "1111111", "John")

    def modify(self, hostName, userName, clientId):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "UPDATE client SET hostName = " + hostName + ", userName = " + userName + " WHERE clientId = " + str(
                clientId)
            # sql = "UPDATE client SET userName='hell' WHERE " + str(clientIdd)
            # "UPDATE node SET nodeStatus='hell' WHERE nodeId =382"
            # sql = "UPDATE task SET taskState = 'PENDING' WHERE taskId = 5"
            cursor.execute(sql)
            connection.commit()
            print(cursor.rowcount, "client modified.")

        except Exception as e:
            logging.exception(e)
            logging.exception('Error occured while modifying data into task')

        finally:
            DB_Manager.closeConnection()

    # modify("s", `"1111111"`, `"Johny"`, 1111115)

    def delete(self, clientId):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "DELETE FROM client WHERE clientId=" + str(clientId)
            cursor.execute(sql)
            connection.commit()
            print cursor.rowcount, " client deleted."
            return cursor._last_insert_id
        except Exception as e:
            # logging.exception(e)
            # logging.exception('Error occured while deleting data in task')
            print "Error Occured"
            return e

        finally:
            DB_Manager.closeConnection()

    # delete("s", 1111114)
    def getClients(self):
        try:
            connection = DB_Manager.getConnection()
            print connection
            cursor = connection.cursor()
            sql = "SELECT * FROM client"
            cursor.execute(sql)
            myresult = cursor.fetchall()
            for x in myresult:
                print(x)

        except Exception as e:
            logging.exception(e)
            logging.exception('Error occured while getting Clients in task')

        finally:
            DB_Manager.closeConnection()

    # getClients("a")