import pickle

class Server:
    def run(self,s):
        """Run the "s" that was received over the bluetooth"""
        o = pickle.loads(s)
        try:
            if o[0] == 1:
                #eval(o[1])
                eval("x=1")
            raise "wrong protocol"
        except:
            #TODO: print more useful info about the exception
            print "sorry, your code raised an exception"
            raise
        print "Done."

code = open("/tmp/x").read()

s = Server()
s.run(code)
