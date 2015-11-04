# Install Bluetooth #

```
wajig install bluetooth obexftp
sudo hciconfig
```

Should print:
```
hci0:   Type: USB
        BD Address: 00:16:41:7A:33:A4 ACL MTU: 1017:8 SCO MTU: 64:0
        UP RUNNING PSCAN ISCAN
        RX bytes:391 acl:0 sco:0 events:17 errors:0
        TX bytes:317 acl:0 sco:0 commands:17 errors:0
```

Turn on the bluetooth on the mobile and
```
hcitool scan
```
should print:
```
Scanning ...
        00:19:79:86:EB:BC       Nokia N70
```

You can try to ping your phone
```
sudo l2ping 00:19:79:86:EB:BC
```
Prints on my computer:
```
Ping: 00:19:79:86:EB:BC from 00:16:41:7A:33:A4 (data size 44) ...
0 bytes from 00:19:79:86:EB:BC id 0 time 228.50ms
0 bytes from 00:19:79:86:EB:BC id 1 time 11.50ms
0 bytes from 00:19:79:86:EB:BC id 2 time 11.35ms
0 bytes from 00:19:79:86:EB:BC id 3 time 11.28ms
0 bytes from 00:19:79:86:EB:BC id 4 time 11.15ms
Send failed: Connection reset by peer
```

Now try to get a directory listing using an OBEX protocol:
```
obexftp -b 00:19:79:86:EB:BC -l
```
If it prints:
```
Browsing 00:19:79:86:EB:BC ...
Channel: 10
Connecting...done
Receiving "(null)"... <?xml version="1.0"?>    <!DOCTYPE folder-listing SYSTEM "obex-folder-listing.dtd">    <folder-listing version="1.0"></folder-listing>doneDisconnecting...done
```
Then you are done. However, if it prints
```
Browsing 00:19:79:86:EB:BC ...
Channel: 10
Connecting...failed: connect
Still trying to connect
Connecting...failed: connect
Still trying to connect
Connecting...failed: connect
Still trying to connect
```
then need to pair your phone:
```
wajig install pkg-config libdbus-1-dev
```
compile and run the:
```
./passkey-agent --default 1234
```
whose source is in the `/usr/share/doc/bluez-utils/examples/`. Leave it running, start another terminal and:
```
obexftp -b 00:19:79:86:EB:BC -l
```
on the phone a dialog will popup asking you to enter a pin, enter the 1234, as you gave to the passkey-agent and that should be it, the `obexftp` should print the listing and you are done. You can now kill the `passkey-agent` using CTRL-C.

## Sending a file to the phone ##

To send a file `/tmp/something` to the phone, use:
```
obexftp -b 00:19:79:86:EB:BC -p /tmp/something
```
The phone will ask you if you want to open it or save it somewhere.

Another option is to mount the memory card as a USB mass storage device, unfortunately this only works on some phones.

# Install Python #

Go to http://sourceforge.net/project/showfiles.php?group_id=154155 and install PythonForS60 package and then the PythonScriptShell. Depending on your version of Symbian, if for example you have the 2nd Edition, FP3, you need to install these two files:
```
PythonForS60_1_3_20_2ndEdFP3.SIS 
PythonScriptShell_1_3_20_2ndEdFP3.SIS
```

If you are new to Python on S60, start here:
http://wiki.forum.nokia.com/index.php/Category:Python