import cPickle as pickle
import logging
import socket
import errno

from coordinator.TDSConfiguration import TDS_Configuration

TDSConfiguration = TDS_Configuration()


class server:

    def getResponse(self, request):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((TDSConfiguration.getIpAddr(), TDSConfiguration.getPort()))
            while (1):
                retur = s.send(pickle.dumps(request))
                response = pickle.loads(s.recv(1024))
                return response
        except s as err:
            if err == errno.ECONNREFUSED or err == errno.ECONNRESET:
                logging.exception("socket creation failed with error %s" % (err))
            else:
                logging.exception("An error occured in getResponse of client/clientClient.py")
