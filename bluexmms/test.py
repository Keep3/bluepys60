import xmms
import time
xmms.control.playlist_next()
def a():
    xmms.playlist_next()
    print xmms.is_playing()
    time.sleep(0.1)

    print xmms.get_playlist_title(xmms.get_playlist_pos())

a()


def x(a):
    print a

c = lambda: x("ahoj")
c()
