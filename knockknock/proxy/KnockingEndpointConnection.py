
from EndpointConnection import EndpointConnection

import subprocess
import time

from struct import *

class KnockingEndpointConnection(EndpointConnection):

    def __init__(self, shuttle, profile, host, port):
        self.profile = profile
        self.host    = host
        self.port    = port

        self.sendKnock(profile, host, port)
        EndpointConnection.__init__(self, shuttle, host, port)

    def reconnect(self):
        self.sendKnock(self.profile, self.host, self.port)
        EndpointConnection.reconnect(self)

    def sendKnock(self, profile, host, port):
        port       = pack('!H', int(port))
        packetData = profile.encrypt(port)
        knockPort  = profile.getKnockPort()
        
        idField, seqField, ackField, winField = unpack('!HIIH', packetData)

        command = "hping3 -q -S -c 1 -p " + str(knockPort) + " -N " + str(idField) + " -w " + str(winField) + " -M " + str(seqField) + " -L " + str(ackField) + " " + host;
        command = command.split()

        subprocess.call(command, shell=False, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
        time.sleep(0.25)
