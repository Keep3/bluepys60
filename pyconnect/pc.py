import pickle

def f():
    x = 1
    print "Man, it works:",x
    print eval("x")
    print eval("x", {x: x},{x: x})

class Runner(object):
    def __init__(self):
        pass

    def run(self, server):
        print "ok, we are there."
        print type(server)

r = [1, """print "ok" """]

open("/tmp/x","w").write(pickle.dumps(r))

f()

#links:
#http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/437932
#http://lybniz2.sourceforge.net/safeeval.html
