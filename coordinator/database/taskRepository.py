import logging

from coordinator.database.DBManager import DB_Manager
from core.core.unicodeToString import unicodeToString

unicodeToStringObj = unicodeToString()
DB_Manager = DB_Manager()


class taskRepository:
    def add(self, task):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "INSERT INTO task (taskName, taskParameter, taskPath, taskState, userID, assignedNodeId) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (task._taskName, task._taskParameters, task._taskExePath, task._taskState, task._taskUserId, None)
            # val = ("1111111", "John", "21", 3, '997', None)
            # val = (hostName, userName)

            # nodeid is foreign key of assignedNodeId
            # clientId is foreign key of userID
            cursor.execute(sql, val)
            connection.commit()
            if cursor._last_insert_id:
                logging.info(str(cursor.rowcount) + " task inserted.")
                return cursor._last_insert_id
            else:
                logging.warnings('Task is not added to DB')
                logging.error('Task is not added to DB')
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
            cursor.execute(sql)
            connection.commit()
            print(cursor.rowcount, "task modified.")

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
                logging.info("1 record updated.")
            else:
                print ('no record updated')
                logging.warnings('no record updated')
            return
        except Exception as e:
            logging.exception(e)
            error_msg = 'Error occured while setTaskStatus into task'
            logging.error(error_msg)
            raise

        finally:
            DB_Manager.closeConnection()

    # taskState IS ENUM [AVAILABLE OPTIONS->COMPLETED, PENDING OR IN_PROGRESS]
    # setTaskStatus("s", `"COMPLETED"`, 11)

    def getTaskStateById(self, taskId):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM task WHERE taskId = " + str(taskId)
            # sql = "SELECT * FROM task WHERE userID='1111113'";
            cursor.execute(sql)
            myresult = cursor.fetchall()
            return unicodeToStringObj.unicodeToString(myresult[0][4])

        except Exception as e:
            logging.exception(e)
            error_msg = 'Error occured in getTasksByClientId in coordinator/database/taskRepository.py'

        finally:
            DB_Manager.closeConnection()

    # getTaskStateByTaskId("S", 483)

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
    def updateTaskState(self, taskId, taskState):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "UPDATE task SET taskState = " + str(taskState) + " WHERE taskId = " + str(taskId)
            cursor.execute(sql)
            connection.commit()
            if cursor.rowcount:
                print(cursor.rowcount, "task modified.")
                return cursor.rowcount
            else:
                print "Task State is not modified."
                return "Task State is not modified."


        except Exception as e:
            logging.exception(e)
            error_msg = 'Error occured while getting in getTaskById in task'

        finally:
            DB_Manager.closeConnection()

    # updateTaskState("s", 8, 2)
    def getTasksByStatus(self, taskState):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM task WHERE taskState = " + str(taskState)
            cursor.execute(sql)
            myresult = cursor.fetchall()
            if myresult:
                logging.info('Task according to the status has fetched sucessfully')
            return myresult

        except Exception as e:
            logging.exception(e)
            error_msg = 'Error occured while getting in getTaskById in task'
            raise

        finally:
            DB_Manager.closeConnection()

    # getTasksByStatus("s", `'PENDING'`)
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
            logging.error(error_msg)
            raise

        finally:
            DB_Manager.closeConnection()

    # getTasksByNodeId("S", 3)

    def updateAssignedNode(self, taskId, assignedNodeID):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "UPDATE task SET assignedNodeId = " + str(assignedNodeID) + " WHERE taskId = " + str(taskId)
            cursor.execute(sql)
            connection.commit()
            if cursor.rowcount:
                print('assignedNodeId of a task is modified.')
                logging.info('assignedNodeId of a task is modified.')
            else:
                print 'No record Modified of Task'
                logging.error('No record Modified of Task')
            return cursor.rowcount

        except Exception as e:
            logging.exception(e)
            error_msg = 'Error occured while assigning in assignNode in task'
            logging.error(error_msg)
            raise

        finally:
            DB_Manager.closeConnection()

    # assignNode("s", `'COMPLETED'`, 3, 12)

    def getAlltasks(self):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM task"
            cursor.execute(sql)
            myresult = cursor.fetchall()
            if myresult:
                return myresult
            else:
                return 0

        except Exception as e:
            error_msg = 'Error occured while getting getAllRecords in task'
            logging.exception(str(error_msg) + ": " + str(e.message))
            raise

        finally:
            DB_Manager.closeConnection()

    # getAlltasks("s")
    def delete(self, taskId):
        try:
            connection = DB_Manager.getConnection()
            cursor = connection.cursor()
            sql = "DELETE FROM task WHERE taskId=" + str(taskId)
            cursor.execute(sql)
            connection.commit()
            print cursor.rowcount, "task deleted."
            return cursor._last_insert_id
        except Exception as e:
            # logging.exception(e)
            # logging.exception('Error occured while deleting data in task')
            print "Error Occured"
            return e

        finally:
            DB_Manager.closeConnection()
# taskRepository().delete(476)
