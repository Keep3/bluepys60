from appuifw import *
from graphics import *
import e32

class MobilApp:
    """MyApp class doc string"""
    app_lock = e32.Ao_lock()
    timer = e32.Ao_timer()
        

    def __init__(self):
        self.old_title = app.title
        self.old_screen = app.screen
        self.old_menu = app.menu
        self.old_exit_key_handler = app.exit_key_handler
        
        self.s = None       # not connected yet
        
        self.startup()

    def connect(self,addr,channel):
        """ Connects to a remote device on selected channel. """
        import socket
        try:
            self.s = socket.socket(socket.AF_BT,socket.SOCK_STREAM)
            self.s.connect( (addr,channel) )
            return True
        except:
            return False
        
    def close_connection(self):
        """ Disconnect from remote device if it is connected. """
        if self.s:
            self.s.close()
            self.s = None
            return True
        else:
            return False

    def startup(self):
        return

    def shutdown(self):
        return
        
    def handle_keyboard_splash(self,event):
        self.app_lock.signal()

    def show_splash(self,filename, timeout = 0):
        img = Image.open(filename)
        old_screen = app.screen
        old_body = app.body
        app.screen = 'full'
        if timeout == 0:
            app.body = Canvas(event_callback=self.handle_keyboard_splash)
        else:
            app.body = Canvas()

        app.body.clear(0)
        app.body.blit(img)
        
        e32.ao_yield()
        
        if timeout == 0:
            self.app_lock.wait()
        else:
            self.timer.after(timeout)

        app.screen = old_screen
        app.body = old_body
        

    def exit_key_handler(self):
        app.exit_key_handler = None
        self.app_lock.signal()

    def run(self):
        app.exit_key_handler = self.exit_key_handler
        self.app_lock.wait()
        self.shutdown()
        app.title = self.old_title
        app.screen = self.old_screen
        app.menu = self.old_menu
        app.exit_key_handler = self.old_exit_key_handler
