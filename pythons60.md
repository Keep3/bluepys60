# Introduction #

`python-s60` is a python interpreter behaving just like a `python` command, but executing all commands remotely on the cell phone over the bluetooth.

# Installation #

Install bluetooth and python on s60, see InstallationNotes.

Then
```
cd pyconnect
obexftp -b 00:19:79:86:EB:BC -p mobile.py
```
Install the script in the phone and run it. It will start listening.

# Usage #

## Interactive console ##

On the computer, run:

```
ondra@syslik:~/bluepys60/pyconnect$ ./python-s60
2.2.2 (#0, Mar 23 2007, 12:02:04)
[GCC 2.9-psion-98r2 (Symbian build 546)]
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
>>> print sys.version
2.2.2 (#0, Mar 23 2007, 12:02:04)
[GCC 2.9-psion-98r2 (Symbian build 546)]
```

You can also be more verbose with the "-v" switch:
```
ondra@syslik:~/bluepys60/pyconnect$ ./python-s60 -v
# connecting to 00:19:79:86:EB:BC...
# sending the command...
# receiving results...
2.2.2 (#0, Mar 23 2007, 12:02:04)
[GCC 2.9-psion-98r2 (Symbian build 546)]
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
# sending the command...
# receiving results...
>>> print sys.version
# sending the command...
# receiving results...
2.2.2 (#0, Mar 23 2007, 12:02:04)
[GCC 2.9-psion-98r2 (Symbian build 546)]
>>>
```

The device address can be changed with the "-b" switch:
```
ondra@syslik:~/bluepys60/pyconnect$ ./python-s60 -v -b 00:19:79:86:EB:BC
# connecting to 00:19:79:86:EB:BC...
# sending the command...
# receiving results...
2.2.2 (#0, Mar 23 2007, 12:02:04)
[GCC 2.9-psion-98r2 (Symbian build 546)]
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
# sending the command...
# receiving results...
>>> print sys.version
# sending the command...
# receiving results...
2.2.2 (#0, Mar 23 2007, 12:02:04)
[GCC 2.9-psion-98r2 (Symbian build 546)]
>>>
```

Run `./python-s60 -h` for all options.

## Run a script ##

```
ondra@syslik:~/bluepys60/pyconnect$ cat test.py
import os, sys
print "python version:"
print sys.version
#print os.listdir(r"E:\system\Apps\Python\my")
ondra@syslik:~/bluepys60/pyconnect$ ./python-s60 test.py
python version:
2.2.2 (#0, Mar 23 2007, 12:02:04)
[GCC 2.9-psion-98r2 (Symbian build 546)]
ondra@syslik:~/bluepys60/pyconnect$ python test.py
python version:
2.4.4 (#2, Apr  5 2007, 20:11:18)
[GCC 4.1.2 20061115 (prerelease) (Debian 4.1.1-21)]
```