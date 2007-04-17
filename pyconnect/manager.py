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

    def listen(self,channel):
        """ Listens for a connection on the channel "channel",
        returns the address of the device, that connected.
        """
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

print "starting"
if mobile():
    y = bluesocket()
    y.listen(6)
    y.send("file")
    y.send("test.py")
    f = open(r"E:\ondra\test.py","w")
    f.write(y.recv())
    f.close()
    y.send("done")
else:
    y = bluesocket()
    #y.listen(6)
    y.connect("00:19:79:86:EB:BC",6)
    while 1:
        cmd = y.recv()
        if cmd == "file":
            filename = y.recv()
            print "sending a file '%s'..."%filename
            y.send(open(filename).read())
            print "  done."
        elif cmd == "done":
            break
        else:
            print "Unknown command:",cmd
print "done."
