
def read(filename):
    final=''
    f1=open(filename,'r')
    for i in f1.read():
        final+=i
    return final
