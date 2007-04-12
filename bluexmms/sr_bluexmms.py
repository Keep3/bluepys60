import sys
sys.path.append('../common')
from blueserver import *
import i_bluexmms
from i_bluexmms import Commands
import xmms
import time
import commands

class BlueXMMS(BlueServer):
    """BlueXMMS class to control XMMS session from a remote device."""

    def __init__(self):
        print "BlueXMMS server v0.9"
        commands={  Commands.volume_get:self.volume_get,
                    Commands.volume_set:self.volume_set,
                    Commands.play_title:self.play_title,
                    Commands.play_next:self.play_next,
                    Commands.play_prev:self.play_prev,
                    Commands.shuffle_get:self.shuffle_get,
                    Commands.shuffle_toggle:self.shuffle_toggle,
                    Commands.play_stop:self.play_stop,
                    Commands.play_play:self.play_play,
                    Commands.shutdown:self.serv_shutdown,
                    Commands.play_pause:self.play_pause}
        BlueServer.__init__(self,i_bluexmms.PORT,commands)


    def _accept(self):
        BlueServer._accept(self)

        if not xmms.is_running():
            xmms.control.enqueue_and_play_launch_if_session_not_started([], xmms_prg='xmms', session=0, poll_delay=0.10000000000000001, timeout=10.0)
       

    def volume_get(self):
        vol = str(xmms.get_main_volume())
        print "Sending volume", vol
        self.client_socket.sendall(vol)
    
    def volume_set(self):
        try:
            volstr = self.client_socket.recv(3)
            vol = int(volstr)
        except ValueError:
            print """WARNING: Bad volume string obtained from remote
                   device ! (%s)""" % volstr
            return
        print "Setting volume to", vol
        xmms.set_main_volume(vol)

    def play_title(self):
        title = "XMMS not playing!"
        if xmms.is_playing():
            idx = xmms.get_playlist_pos()
            title = xmms.get_playlist_title(idx)

        print "Sending title '%s'." % title
        self.client_socket.sendall(title)

    def play_next(self):
        print "Playing next song."
        xmms.control.playlist_next()
        time.sleep(0.2)

    def play_prev(self):
        print "Playing previous song."
        xmms.playlist_prev()
        time.sleep(0.2)

    def shuffle_toggle(self):
        print "Toggleing shuffle."
        xmms.toggle_shuffle()
    
    def shuffle_get(self):
        shuffle = xmms.is_shuffle()
        print "Sending toggle: now is",shuffle == 1
        self.client_socket.sendall(str(shuffle))

    def play_play(self):
        print "Play."
        xmms.play()

    def play_stop(self):
        print "Stop."
        xmms.stop()

    def play_pause(self):
        xmms.play_pause()
        state = xmms.is_paused()
        print "Pause/Stop."
    
    def serv_shutdown(self):
        print "Shuting down!!!"
        commands.getoutput('shutdown -h now')

bluexmms = BlueXMMS()
if __name__ == '__main__':
    bluexmms.run()

