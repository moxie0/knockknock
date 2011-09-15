
import asyncore
import string
import socket

class EndpointConnection(asyncore.dispatcher_with_send):

    def __init__(self, shuttle, host, port):
        asyncore.dispatcher_with_send.__init__(self)
        self.shuttle        = shuttle
        self.buffer         = ""
        self.closed         = False

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))

    def handle_connect(self):
        (localIP, localPort) = self.socket.getsockname()        
        self.shuttle.connectSucceeded(localIP, localPort)

    def handle_close(self):
        if (not self.closed):
            self.closed = True
            self.shuttle.handle_close()
            self.close()

#    def handle_error(self):        
#        print "handlerrror"

    def handle_read(self):
        data = self.recv(4096)
        self.shuttle.receivedData(data)

    def write(self, data):
        if (not self.closed):
            self.send(data)
