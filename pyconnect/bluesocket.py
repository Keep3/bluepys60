"""
Contains a bluesocket class for communicating over bluetooth, that works both
in linux and s60 and has exactly the same interface on both platforms.

Usage:
======

server:
-------

y = bluesocket()
y.listen(6)
y.send("some string")
y.recv()
y.close()

client:
-------

y = bluesocket()
y.connect("00:16:41:7A:33:A4",6)
y.send("some string")
y.recv()
y.close()

These two examples above both work in linux and s60.

"""

class bluesocket:
    def __init__(self):
        self.mobile = mobile()
        if self.mobile:
            import socket
            self.blue = socket.socket(socket.AF_BT,socket.SOCK_STREAM)
        else:
            import bluetooth
            self.blue = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server = False

    def listen(self,channel):
        """ Listens for a connection on the channel "channel",
        returns the address of the device, that connected.
        """
        self.server = True
        self.blue.bind(("",6))
        self.blue.listen(1)
        self.sock, info = self.blue.accept()
        if self.mobile:
            return info
        else:
            assert len(info) == 2
            assert info[1] == channel
            return info[0]

    def connect(self, address, channel):
        """ Connects to an address "address" on the channel "channel".
        """
        self.blue.connect((address,channel))
        self.sock = self.blue

    def send(self, s):
        """ Sends a string "s" over the socket"""
        #the default number of digits is 12, see also recv()
        x = "%.12d"%len(s)+s
        self.sock.sendall(x)

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

    def recv(self):
        """ Returns a complete string from the socket. """
        #the default number of digits is 12, see also send()
        header = self._recv_all(12)
        return self._recv_all(int(header))

    def close(self):
        """ Waits until the other side is also ready to quit.

        It just exchanges a "magic" code between the server and the client. 
        """
        magic = "done123"
        if self.server:
            #tell the client that we want to quit
            self.send(magic)
            #wait until the client is ready to quit
            assert self.recv() == magic
        else:
            #wait until the server sends us that he's ready to quit
            assert self.recv() == magic
            #tell him that we are also ready
            self.send(magic)
            #wait a little bit, so that the server has enough time to
            #receive it
            import time
            time.sleep(0.1)

def mobile():
    """Are we running on the S60?"""
    m=False
    try:
        import e32
        m=True
    except:
        pass
    return m

