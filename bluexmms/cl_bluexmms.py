import sys
sys.path.append('E:\\Python')
import mobilapp
from appuifw import *
from i_bluexmms import *
from graphics import *
from key_codes import *


class BlueXMMSApp(mobilapp.MobilApp):

    def startup(self):
        app.title = u'BlueXMMS v1.0'
        app.screen = 'full'

        self.locked = False
        self.imgUI = Image.open('E:\\data\\bluexmms\\bluexmms_ui.jpg')
        self.imgVol = Image.open('E:\\data\\bluexmms\\volume.png')
        app.body = Canvas(self.canvas_redraw,self.canvas_key)


        self.show_splash('E:\\data\\bluexmms\\bluexmms.jpg',1)
        self.canvas_redraw(None)
        e32.ao_yield()

        self.set_connect_menu()
        self.menu_connect()

    
    def shutdown(self):
        self.close_connection()

    def canvas_redraw(self,rect):
        try:
            app.body.blit(self.imgUI)
        except:
            pass

    def canvas_key(self,event):
        if not self.s: return
        if event['type'] != EEventKey: return
        key = event['keycode']
        if key == EKeyUpArrow:
            self.volume_up()
        elif key == EKeyDownArrow:
            self.volume_down()
        elif key == EKeyLeftArrow:
            self.play_prev()
        elif key == EKeyRightArrow:
            self.play_next()
        
    def set_connect_menu(self):
        app.menu = [ (u'Connect', self.menu_connect) ]

    def set_connected_menu(self):
        app.menu = [    (u'Get title', lambda: self.get_title(True)), 
                        (u'Get volume',lambda: self.get_volume(True)),
                        (u'Get shuffle',lambda: self.get_shuffle(True)),
                        (u'Shutdown', self.menu_shutdown),
                        (u'Disconnect', self.menu_disconnect) ]

    def menu_shutdown(self):
        if query(u'Really shutdown?','query'):
            self.s.send(Commands.shutdown)
            self.exit_key_handler()

    def get_title(self,shownote = False):
        try:
            self.s.send(Commands.play_title)
            self.timer.after(0.1)
            title = self.s.recv(100)
        
            if shownote:
                note(u'%s'%title,'info')
        except IOError:
            self.err_connection()

    def get_volume(self,shownote = False):
        try:
            self.s.send(Commands.volume_get)
            self.timer.after(0.1)
            volume = self.s.recv(100)

            if shownote:
                note(unicode(volume),'info')
            self.volume = int(volume)
        except IOError:
            self.err_connection()

    def get_shuffle(self,shownote = False):
        try:
            self.s.send(Commands.shuffle_get)
            self.timer.after(0.1)
            shuffle = self.s.recv(100)

            if shownote:
                note(unicode(shuffle),'info')
            self.shuffle = shuffle == "1"
        except IOError:
            self.err_connection()


    def volume_up(self):
        if self.volume >= 95:
            return
        if self.locked: return
        self.locked = True
        try:
            self.s.send(Commands.volume_set)
            self.timer.after(0.2)
            self.volume += 5
            self.s.send(str(self.volume))
        except IOError:
            self.err_connection()
        self.locked = False


    def volume_down(self):
        if self.volume <= 5:
            return
        if self.locked: return
        self.locked = True
        try:
            self.s.send(Commands.volume_set)
            self.timer.after(0.2)
            self.volume -= 5
            self.s.send(str(self.volume))
        except IOError:
            self.err_connection()
        self.locked = False

    def play_next(self):
        if self.locked: return
        self.locked = True
        try:
            self.s.send(Commands.play_next)
            self.get_title()
        except IOError:
            self.err_connection()
        self.locked = False

    def play_prev(self):
        if self.locked: return
        self.locked = True
        try:
            self.s.send(Commands.play_prev)
            self.get_title()
        except IOError:
            self.err_connection()
        self.locked = False

    def menu_connect(self):
        if self.connect("11:11:11:11:11:11",PORT):
            note(u'Connected to the server!','info')
            self.set_connected_menu()
            self.locked = False

            self.get_title()
            self.timer.after(0.1)
            self.get_volume()
            self.timer.after(0.1)
            self.get_shuffle()
        else:
            self.err_connection()

    def menu_disconnect(self):
        self.close_connection()
        self.set_connect_menu()
        note(u'Disconected','info')
    
    def err_connection(self):
        note(u'Connection refused/lost!','error')
        self.close_connection()
        self.set_connect_menu()


myapp = BlueXMMSApp()
if __name__ == '__main__':
        myapp.run()

