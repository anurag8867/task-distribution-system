import cPickle as pickle
import logging
import socket
import errno

from coordinator.TDSConfiguration import TDS_Configuration

TDSConfiguration = TDS_Configuration()


class nodeClient:
    def getResponse(self, TDSRequest):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((TDSConfiguration.getIpAddr(), TDSConfiguration.getPort()))
            while (1):
                s.send(pickle.dumps(TDSRequest))
                response = pickle.loads(s.recv(1024))
                return response
        except s as err:
            if err == errno.ECONNREFUSED or err == errno.ECONNRESET:
                logging.exception("socket creation failed")
                print "socket creation failed with error %s" % (err)
            else:
                print "error occured"
        except Exception as e:
            logging.exception('Error!-> Code: {c} && Message, {m}'.format(c=type(e).__name__, m=str(e)))
        raise
