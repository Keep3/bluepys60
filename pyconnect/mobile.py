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


import socket;

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


b = socket.socket(socket.AF_BT,socket.SOCK_STREAM);
b.bind(("",5))
b.listen(1)
while 1:
    try:
        print "listening"
        sock, info =  b.accept()
        print "connected"
        print "waiting for a code"
        x = recv(sock)
        print "running the code"
        s = run(x)
        print "done. sending the result back"
        sock.sendall(pickle_str(s))
        print "closing"
        sock.close()
        print "done."
    except:
        print "exception raised"
