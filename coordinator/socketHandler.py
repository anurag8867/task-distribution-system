import cPickle as pickle
import logging

from coordinator.requestDispatcher import requestDispatcher


class socketHandler:
    def writeResponse(self, conn, response):
        logging.info("Resquest has sent back to client after completing the whole process")
        conn.sendall(pickle.dumps(response))

    def processRequest(self, conn):
        try:
            logging.info("request received")
            TDSRequest = pickle.loads(conn.recv(1024))
            controller = requestDispatcher().getController(TDSRequest)
            response = controller().processRequest(TDSRequest)
            socketHandler().writeResponse(conn, response)
        except EOFError as error:
            logging.exception('EOFError as error: This is an info message in coordinator/socketHandler.py')
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
        except:
            logging.exception('EOFError in coordinator/socketHandler.py')
            # raise
