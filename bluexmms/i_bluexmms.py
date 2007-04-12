PORT = 6
END_SEQ = "!@#"
class Commands:
    """ BlueXMMS protocol.

        When connection is made, server will start XMMS session if it is 
        not present. 
        Next will send to connected device:
        1) A title of currently playing song. (play_title)
        2) A volume settings. (volume_get)
        3) A shuffle state. (shuffle_get)
    """
    
    volume_get = "vo_get"   # Server will return actual volume.
    volume_set = "vo_set"   # Server will be waiting for volume string from device.
    play_title = "pla_ti"   # Server will return a title of playing song.
    play_next = "pla_ne" 
    play_prev = "pla_pr"
    shuffle_get = "sh_get"  #Server will return true if shuffle is toggled("1" or "0"). 
    shuffle_toggle = "sh_tog" 
    play_play = "pla_pl"
    play_stop = "pla_st"
    play_pause = "pla_pa"   
    shutdown = "shutdo"
