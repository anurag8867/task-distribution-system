import mysql.connector
import logging

from coordinator.TDSConfiguration import TDS_Configuration

TDS_Config = TDS_Configuration()


class DB_Manager:
    try:
        def getConnection(self):
            conn = mysql.connector.connect(
                host=TDS_Config.getHostName(),
                user=TDS_Config.getElementByTagName("db-user-name"),
                passwd=TDS_Config.getElementByTagName("db-user-password"),
                database=TDS_Config.getElementByTagName("db-connection-string")
            )
            return conn

        def closeConnection(self):
            self.getConnection().close()

    except ValueError as ve:
        print(ve)
    except mysql.connector.Error as err:
        logging.exception("Something went wrong: {}".format(err))
    except TypeError, err:
        logging.exception("Something went wrong: {}".format(err))
    except ValueError, err:
        logging.exception("Something went wrong: {}".format(err))
    except:
        logging.exception('An error occurred in DB_Manager.')


DBManager = DB_Manager()
