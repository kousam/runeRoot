


class Vector():
    def __init__(self, data=(0,0)):
        # constructs a 'ai + bj' vector
        i,j = data
        self.i = i
        self.j = j

    def set(self, i, j):
        self.i = i
        self.j = j

        
    def get(self):
        return (self.i, self.j)
    


def addVectors(a,b):
    # adds two vectors
    # returns new vector info
    
    i1,j1 = a.get()
    i2,j2 = b.get()

    i = i1 + i2
    j = j1 + j2

    return (i,j)
