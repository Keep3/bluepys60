## Installation ##

You need to install [python-s60](http://code.google.com/p/bluepys60/wiki/pythons60) and check that it works. Nothing else is needed.

## File manager ##

Run
```
ondra@syslik:~/bluepys60/pyconnect$ python manager.py
starting
```
leave it running and in another terminal, run:
```
ondra@syslik:~/bluepys60/pyconnect$ ./python-s60 manager.py
starting
done.
```
This will execute the `commands()` function in `commands.py` (on the computer):
```
def commands(send, recv):
    send("test.py",r"E:\ondra\test.py")
    send("test.py",r"E:\ondra\test2.py")
    recv(r"E:\ondra\test2.py", "/tmp/x")
```
and the first terminal will look like this:
```
ondra@syslik:~/bluepys60/pyconnect$ python manager.py
starting
sending: test.py -> E:\ondra\test.py
sending: test.py -> E:\ondra\test2.py
receiving: E:\ondra\test2.py -> /tmp/x
done.
```