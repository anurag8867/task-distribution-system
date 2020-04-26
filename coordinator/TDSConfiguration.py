import os
import socket
import getpass

from bs4 import BeautifulSoup


class TDS_Configuration:

    # def __getElementByTagName(self, tagName):
    def getElementByTagName(self, tagName):
        cwd = os.getcwd()
        theurl = cwd + "/resources/tds.xml"
        soup = BeautifulSoup(open(theurl).read(), "lxml")
        return soup.find(tagName).string

    def getElementByTag(self, tagName):
        # return self.__getElementByTagName(tagName)
        return self.getElementByTagName(tagName)

    def getIpAddr(self):
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        return IPAddr

    def getPort(self):
        return 4000

    def getNodePort(self):
        return 5000

    def getHostName(self):
        hostname = socket.gethostname()
        return hostname

    def getHomeDir(self):
        homedir = os.environ['HOME']
        return homedir

    def getUserName(self):
        username = getpass.getuser()
        return username


TDSConfig = TDS_Configuration()
