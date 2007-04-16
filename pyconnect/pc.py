import pickle
import sys
import StringIO
import traceback
import time

IN_PC = 0
IN_MOBILE = 1

WHERE = -1

try:
    import bluetooth;
    WHERE = IN_PC;
except ImportError:
    import socket;
    WHERE = IN_MOBILE;

class bluesocket:
    """ The bluetooth socket which works on a pc via the python-bluez 
    as well as on a mobile via pyS60 sockets. 
        
    """

    def __init__(self,headersize):
        """ Inits a socket.

        param:
            headersize - fixed size of a header in bytes which is sent before each pickled object.
                         In this header is saved how large is pickled object so a recipient knows
                         how large data should recive recieve to succesfully unpickle the object. 
        """
                         
        self.headersize = headersize
        
        if WHERE == IN_PC:
           self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM);
        elif WHERE == IN_MOBILE:
            self.socket = socket.socket(socket.AF_BT,socket.SOCK_STREAM);

    def connect(self,addr,channel):
        self.socket.connect( (addr,channel) )

    def close(self):
        self.socket.close()

    def accept(self):
        return self.socket.accept()

    def bind(self,channel):
        self.socket.bind(("",channel))

    def send(self,obj):
        """ Sends a pickled object. """
        # pickkle our object & send its size in a header.
        data = cPickle.dumps(obj);
        self._send_header(len(data));

        # send object itself.
        return self.socket.sendall(data);

    def recv(self):
        """ Return an pickled object from socket. """

        # first let recieve only a header.
        header = self._recv_all(self.headersize)

        # get data size from the header & get the data from socket.
        datasize = int(header)
        data = self._recv_all(datasize)

        return data;

    def _send_header(self,datasize): 
        """ Send a header which contains a size of next pickled object. 
        
        param:
            datasize - a size of next pickled object to send.
        """
        header = "%%.%dd" % self.headersize 
        header = header % datasize

        self.socket.sendall(header)

    def _recv_all(self,size):
        """ Recieves a data from the socket of a required size.

        param:
            size - requested size to recieve.
        """
        msg = '';
        while len(msg) < size:
            chunk = self.sock.recv(size-len(msg))
            if chunk == '':
                raise RuntimeError, "socket connection broken"
            msg = msg + chunk
        return msg

def pickle_str(s):
    x = "%.12d"%len(s)+s
    return x

def recv_all(sock,size):
    """ Recieves a data from the socket of a required size.

    param:
        size - requested size to recieve.
    """
    msg = '';
    while len(msg) < size:
        chunk = sock.recv(size-len(msg))
        if chunk == '':
            raise RuntimeError, "socket connection broken"
        msg = msg + chunk
    return msg

def recv(sock):
    """ Return an pickled object from socket. """

    # first let recieve only a header.
    header = recv_all(sock,12)

    # get data size from the header & get the data from socket.
    datasize = int(header)
    data = recv_all(sock,datasize)

    return data

b = bluesocket(12)
print "connecting"
b.connect("00:19:79:86:EB:BC",5)
print "connected:"
print "sending str"
code=r"""\
print "This code runs on the phone"
import os, sys
print "current dir:",os.getcwd()
print "python version:"
print sys.version
"""
b.socket.sendall(pickle_str(code))
print "receiving"
print recv(b.socket)
print "stop"
