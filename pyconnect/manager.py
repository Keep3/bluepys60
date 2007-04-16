def mobile():
    """Are we running on the S60?"""
    m=False
    try:
        import e32
        m=True
    except:
        pass
    return m

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

def pickle_str(s):
    x = "%.12d"%len(s)+s
    return x

print "starting"
if mobile():
    #f = open(r"E:\ondra\test.py","w")
    #f.write("xj=35")
    #f.close()
    #import sys
    #sys.path.append("E:\ondra")
    #import test
    #print test.xj
    import socket
    #uncomment this - it will raise an exception in the mobile app.
    #b = socket.socket(socket.AF_BT,socket.SOCK_STREAM)
    #b.connect(("11:11:11:11:11:11",5))
else:
    print "listening"
print "done."
