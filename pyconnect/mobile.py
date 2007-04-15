
x = [1,2,"ano"]

def python2str(x):
    import pickle
    import StringIO
    output = StringIO.StringIO()
    pickle.dump(x, output)
    return output.getvalue()

def str2python(s):
    import pickle
    import StringIO
    input = StringIO.StringIO(s)
    return pickle.load(input)

s= python2str([1,2])
print str2python(s)

