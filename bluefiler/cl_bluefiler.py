import sys
sys.path.append('E:\\Python')
import mobilapp
import e32
from appuifw import *
import socket
from i_bluefiler import *

class BlueFilerApp(mobilapp.MobilApp):

    def startup(self):
        app.title = u'BlueFiler v1.3'
        app.screen = 'normal'
        self.entries = [(u'Not connected!',u'Select Menu->Connect')]
        app.body = Listbox(self.entries,self.lb_observe)

        self.set_connect_menu()
        self.menu_connect()
    
    def shutdown(self):
        self.close_connection()


    def lb_observe(self):
        if self.s:
            idx = app.body.current()
            self.get_file(self.entries[idx][1],'E:\\Python',True)

    def set_connect_menu(self):
        app.menu = [ (u'Connect', self.menu_connect) ]
        self.entries = [(u'Not connected!',u'Select Menu->Connect')]
        app.body.set_list(self.entries)

    def set_connected_menu(self):
        app.menu = [    (u'Get Info', self.get_info), 
                        (u'Download to...',self.download_to),
                        (u'Exec file',self.exec_script),
                        (u'Disconnect', self.menu_disconnect) ]


    def menu_connect(self):
        if self.connect("11:11:11:11:11:11",5):
            note(u'Connected to the server!','info')
            self.set_connected_menu()
            self.get_info()
        else:
            self.err_connection()

    def menu_disconnect(self):
        self.close_connection()
        self.set_connect_menu()
        note(u'Disconected','info')
    
    def get_info(self):
        try:
            self.s.send(Commands.getinfo)
            data = ""
            while True:
                d = self.s.recv(1024)
                idx = d.find(END_CHAR)
                if idx > -1:
                    d = d[:idx]         #string to index idx-1
                data += d
                if idx > -1:
                    break

            files = data.split(SEPARATOR_CHAR)
        
            self.entries = [ (unicode(file[ file.rfind('/')+1:]),unicode(file)) for file in files ]

            idx = len('/home/tomas/projects/python/') # prefix which is not shown.
            self.visibleentries = [ (a,u'..'+b[idx:]) for (a,b) in self.entries ]
            app.body.set_list(self.visibleentries)
        except:
            self.err_connection()
            raise
    
    def download_to(self):
        todir = query(u'Download to...','text',u'E:\\data\\')

        if todir:
            idx = app.body.current()
            self.get_file(self.entries[idx][1],todir,False)

    def get_file(self,file,distdir,ask):
        fname = file[ file.rfind('/') +1: ]
        if ask and not query(u'Download file %s?' % fname,'query'):
            return 
        try:
            self.s.send(Commands.getfile)
            e32.ao_sleep(0.2)
            self.s.send(file)
                
            fsize = int(self.s.recv(10))
            getsize = 0
            iter = 0

            if distdir[-1:] != '\\':        # append '\' if it is not present.
                distdir += '\\'
            f = open(distdir+fname,"w")

            while getsize != fsize:
                data = self.s.recv(fsize)
                getsize += len(data)
                iter += 1
                f.write(data)

            
            f.close()
            note(u'File %s%s saved![%iiter]' % (distdir,fname,iter),'info')
        except IOError:
            self.err_connection()

    def exec_script(self):
        if self.s:
            idx = app.body.current()
            script = 'E:\\Python\\'+self.entries[idx][0]
            execfile(script)

        

    def err_connection(self):
        note(u'Connection refused/lost!','error')
        self.close_connection()
        self.set_connect_menu()


myapp = BlueFilerApp()
if __name__ == '__main__':
        myapp.run()

