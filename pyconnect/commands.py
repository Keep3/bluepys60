def commands(send, recv):
    send("test.py",r"E:\ondra\test.py")
    send("test.py",r"E:\ondra\test2.py")
    recv(r"E:\ondra\test2.py", "/tmp/x")
