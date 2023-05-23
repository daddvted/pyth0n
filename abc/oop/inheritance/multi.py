class A:
    def __init__(self, name):
        self.name = name

    def hi(self):
        print(f"Hi, {self.name}, from A")

class B:
    def __init__(self, name):
        self.name = name

    def hi(self):
        print(f"Hi, {self.name}, from B")


class C(B, A):
    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def hi(self):
        super(B, self).hi()
        print(self.name)

if __name__ == "__main__":
    c = C("shit")
    c.hi()
