import sys
import StringIO
import traceback

def run(s):
    saveout = sys.stdout
    out = StringIO.StringIO()
    sys.stdout = out
    try:
        try:
            exec s in globals()
        except:
            traceback.print_exc(file=sys.stdout)
    finally:
        sys.stdout = saveout
    return out.getvalue()

def mobile():
    """Are we running on the S60?"""
    m=False
    try:
        import e32
        m=True
    except:
        pass
    return m

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
        if not self.server:
            #running for the first time
            self.blue.bind(("",channel))
            self.blue.listen(1)
        self.server = True
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
        self.sock.close()

b = bluesocket()
while 1:
    print "listening"
    addr=b.listen(5)
    print "comp:",addr
    print "  waiting for a code"
    x = b.recv()
    print "  running the code"
    s = run(x)
    print "  sending results"
    b.send(s)
    print "  closing"
    b.close()
