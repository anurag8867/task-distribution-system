import logging

from coordinator.database.DBManager import DB_Manager

DB_Manager = DB_Manager()


class taskResultRepository:
    def add(self, taskResult):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "INSERT INTO taskresult (taskId, Outcome, ErrorCode, ErrorMsg, ResultBuffer) VALUES (%s, %s, %s, %s, %s)"
            val = (taskResult._taskId, taskResult._status, taskResult._errorCode, taskResult._errorMessage,
                   taskResult._resultBuffer)
            # val = (8, 2, 404, "400", "MEDIUMBLOB")
            cursor.execute(sql, val)
            connection.commit()
            if cursor.rowcount:
                logging.log(cursor.rowcount, "record inserted.")
                return cursor._last_insert_id
            else:
                logging.error('No task result inserted')
                return

        except Exception as e:
            logging.exception(e)
            raise

        finally:
            DB_Manager.closeConnection()

    # add("S", "1111111")

    def modify(self, taskName, taskParameter, taskPath, taskState, userID, assignedNodeId, taskId):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            # assignedNodeId is foreign key
            sql = "UPDATE task SET taskName = " + taskName + ", taskParameter = " + taskParameter + ", taskPath = " + taskPath + ", taskState = " + str(
                taskState) + ", userID = " + str(userID) + ", assignedNodeId = " + str(
                assignedNodeId) + " WHERE taskId = " + str(taskId)
            # sql = "UPDATE task SET taskName ='helll', taskParameter = '111', taskPath = '1111' , taskState = 1 , userID = 1111113, assignedNodeId = 3 WHERE taskId = 4"
            # sql = "UPDATE client SET hostName = " + hostName + ", userName = " + userName + " WHERE clientId = " + str(clientId)
            # print sql
            cursor.execute(sql)
            connection.commit()
            print(cursor.rowcount, "taskresult modified.")

        except Exception as e:
            logging.exception(e)
            error_msg = 'Error occured while modifying data into task'

        finally:
            DB_Manager.closeConnection()

    # modify("S", `"helll"`, `"111"`, `"1111"`, 1, 1111114, 3, 4)
    def setTaskStatus(self, taskState, taskId):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "UPDATE task SET taskState = " + taskState + " WHERE taskId = " + str(taskId)
            # sql = "UPDATE task SET taskState = 'PENDING'  WHERE taskId = 4"
            print sql
            cursor.execute(sql)
            connection.commit()
            if cursor.rowcount:
                print(cursor.rowcount, "record updated.")
            else:
                print ('no record updated')

        except Exception as e:
            logging.exception(e)
            error_msg = 'Error occured while setTaskStatus into task'

        finally:
            DB_Manager.closeConnection()

    # taskState IS ENUM [AVAILABLE OPTIONS->COMPLETED, PENDING OR IN_PROGRESS]
    # setTaskStatus("s", `"COMPLETED"`, 11)

    def getTasksByClientId(self, userID):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM task WHERE userID = " + str(userID)
            # sql = "SELECT * FROM task WHERE userID='1111113'";
            print sql
            cursor.execute(sql)
            myresult = cursor.fetchall()
            if myresult:
                for x in myresult:
                    print(x)
            else:
                print "no result found for the given clientId"

        except Exception as e:
            logging.exception(e)
            error_msg = 'Error occured while getting in getTasksByClientId in task'

        finally:
            DB_Manager.closeConnection()

    # getTasksByClientId("s", `'1111115'`)
    def getTaskOutcomeByTaskId(self, taskId):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM taskresult WHERE taskId = " + str(taskId)
            cursor.execute(sql)
            myresult = cursor.fetchall()
            return myresult

        except Exception as e:
            logging.exception(e)
            error_msg = 'Error occured while getting in getTaskById in task'

        finally:
            DB_Manager.closeConnection()

    # getTaskById("s", 11)
    def getTasksByStatus(self, outcome):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM task WHERE outcome = " + str(outcome)
            cursor.execute(sql)
            myresult = cursor.fetchall()
            for x in myresult:
                print(x)

        except Exception as e:
            logging.exception(e)
            error_msg = 'Error occured while getting in getTaskById in task'

        finally:
            DB_Manager.closeConnection()

    # getTasksByStatus("s", `'COMPLETED'`)
    def getTasksByNodeId(self, assignedNodeId):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM task WHERE assignedNodeId = " + str(assignedNodeId)
            cursor.execute(sql)
            myresult = cursor.fetchall()
            for x in myresult:
                print(x)

        except Exception as e:
            logging.exception(e)
            error_msg = 'Error occured while getting in getTasksByNodeId in task'

        finally:
            DB_Manager.closeConnection()

    # getTasksByNodeId("S", 3)

    def assignNode(self, taskState, assignedNodeId, taskId):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            # sql = "UPDATE task SET taskState = 'PENDING' WHERE taskId = 5"
            # sql = "UPDATE task SET taskState = ? , assignedNodeId = ? WHERE taskId = ?"
            sql = "UPDATE task SET taskState = " + taskState + ", assignedNodeId = " + str(
                assignedNodeId) + " WHERE taskId = " + str(taskId)
            print sql
            cursor.execute(sql)
            connection.commit()
            if cursor.rowcount:
                print(cursor.rowcount, "taskResult modified.")
            else:
                print "No record Modified of Task Result"

        except Exception as e:
            logging.exception(e)
            error_msg = 'Error occured while assigning in assignNode in task'

        finally:
            DB_Manager.closeConnection()

    # assignNode("s", `'COMPLETED'`, 3, 12)

    def getAllRecords(self):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM taskresult"
            cursor.execute(sql)
            myresult = cursor.fetchall()
            for x in myresult:
                print(x)


        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
            raise Exception(str(e))

        finally:
            DB_Manager.closeConnection()

    # getAllRecords("s")

    def delete(self, taskResultId):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "DELETE FROM taskresult WHERE resultId=" + str(taskResultId)
            cursor.execute(sql)
            connection.commit()
            print cursor.rowcount, "task deleted."
            return cursor._last_insert_id
        except Exception as e:
            logging.exception(e)
            logging.exception('Error occured while deleting data in task')
            raise

        finally:
            DB_Manager.closeConnection()
    # taskRepository().delete(476)
