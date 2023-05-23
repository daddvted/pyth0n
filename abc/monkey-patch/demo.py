from monkey import M


def chant(self):
    print("No more monkey jumping on the bed")


M.sing = chant

obj = M()
obj.sing()
