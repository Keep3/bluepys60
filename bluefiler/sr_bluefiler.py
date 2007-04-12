import sys
sys.path.append('../common')
from bluetooth import *
import os
import re
import time
from i_bluefiler import *
from blueserver import *

CONFIG_FILE = '/home/tomas/projects/python/bluefiler/bluefiler.dirs'

class BlueFiler(BlueServer):
    """BlueFiler class to sending files to remote device.
    
    Deeper description not yet."""

    def __init__(self):
        print "BlueFiler version 1.0"
        commands={Commands.getinfo:self.send_info,Commands.getfile:self.send_file}
        BlueServer.__init__(self,5,commands)
        self.dirs = []
        self.files = []
        self.prog = re.compile("^.*\.(py|jpg|png)$")

    def send_info(self):
        assert(self.client_socket)
        print "Sending files info..."   

        self.load_dir_config()
        self.refresh_files()

        tosend = ''
        for file in self.files:
            tosend += file+SEPARATOR_CHAR
        tosend = tosend[:-1] + END_CHAR     # remove last SEPARATOR and add END_CHAR
        
        print tosend        
        self.client_socket.sendall(tosend)

    def send_file(self):
        assert(self.client_socket)
        filename = self.client_socket.recv(BUFFER_SIZE)

        print "Sending %s file..." % filename

        if len(filename) == 0:
            self.client_quit()
            return

        f = open(filename,'r')
        f.seek(0,2)
        fsize = f.tell()
        f.seek(0,0)
        fdata = f.read()
        f.close()
            
        self.client_socket.send(str(fsize))
        time.sleep(0.2)
        
        self.client_socket.sendall(fdata)

    def refresh_files(self):
        self.files = []
        for dir in self.dirs:
            f = os.listdir(dir)
            self.files.extend( [ dir+"/"+file for file in f if self.prog.match(file) ] )

    def add_dir(self,dir):
        self.dirs.append(dir)
    
    def load_dir_config(self):
        f = open(CONFIG_FILE)
        self.dirs = []
        for line in f:
            self.add_dir(line[:-1])     # remove last '\n' character.
        f.close()
        print self.dirs
    
bluefiler = BlueFiler()
if __name__ == '__main__':
    bluefiler.run()
