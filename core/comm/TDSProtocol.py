class TDSProtocol():
    def __init__(self):
        pass

    def setProtocolVersion(self, version):
        self._version = version

    def setProtocolFormat(self, format):
        self._format = format

    def setSourceIp(self, sourceIp):
        self._sourceIp = sourceIp

    def setSourcePort(self, sourcePort):
        self._sourcePort = sourcePort

    def setDestIp(self, destIp):
        self._destIp = destIp

    def setDestPort(self, destPort):
        self._destPort = destPort

    def setData(self, data):
        self._data = data

    def getProtocolVersion(self):
        return self._version

    def getProtocolFormat(self):
        return self._format

    def getSourceIp(self):
        return self._sourceIp

    def getSourcePort(self):
        return self._sourcePort

    def getDestIp(self):
        return self._destIp

    def getDestPort(self):
        return self._destPort

    def getData(self):
        return self._data

    def getMethod(self):
        return self.method

    # def setA(self, a):
    #     print("setA(self, a)")
    #     self._a = a
    # def getA(self):
    #     print("getA(self)")
