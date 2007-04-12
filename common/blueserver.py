from bluetooth import *
import sys
import os
import re
import time


class BlueServer:
    """BlueServer class represents bluetooth server."""

    def __init__(self,channel,commands,listen=1):
        """ Initializate Bluetooth server.
        
        Keyword arguments:
        channel  -- RFCOMM channel.
        commands -- Dictionary of commands->callable handler.
        listen   -- Queue size for accepting connection (defualt 1).

        """
        self.command_length = self._check_commands_length(commands) # check whether commands has same fixed length.
        self.commands = commands 

        self.server_socket=BluetoothSocket(RFCOMM)
        self.server_socket.bind(("",channel))
        self.server_socket.listen(listen)
        self.client_socket = None       # not yet connected.    

    def run(self):
        """ Runs the server. """
        while True:
            try:
                self._accept()
                while self.client_socket:
                    command_fce = self._recieve_command()
                    if command_fce:
                        command_fce()
            except IOError:
                pass    # The client has disconnected.
            except KeyboardInterrupt:
                print "Exiting server..."
                self._close_connection()
                return          

    def _accept(self):
        """ Waits for a connection on selected channel. """
        port = self.server_socket.getsockname()[1];
        print "Listening on RFCOMM channel %d." % port
        
        self.client_socket, self.client_info = self.server_socket.accept()
        
        print "Accepted connection from ", self.client_info

    def _recieve_command(self):
        """ Recieve a command from the client. 

            Return:
            None     --- if unknown request was sent or client disconnect.
            callable --- callable associated with request via the dictionary.
        """
    
        assert(self.client_socket)
        print "Waiting for commands..."
        data = self.client_socket.recv(self.command_length)
        if len(data) == 0: 
            # client has disconnect.
            self._client_quit()
            return None
        
        print "GET: %s" % data
        if self.commands.has_key(data):
            return self.commands[data]
        else:
            return None
        
    def _close_connection(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
        self.server_socket.close()

    def _client_quit(self):
        self.client_socket.close()
        self.client_socket = None
        
    def _check_commands_length(self,commands):
        """ Check whether all commands has same fixed length.
    
        Fixed length is required becouse of retrieving commands from a client.

        Keyword arguments:
        commands -- Dictionary of commands->callable handler.

        Return:
        Commands length which is equal to all commands or raise an exception.

        """
        length = len(commands.keys()[0])

        for pattern in commands.keys():
            if len(pattern) != length:
                raise NameError, "ERR: commands don't have same pattern length"
        return length       
