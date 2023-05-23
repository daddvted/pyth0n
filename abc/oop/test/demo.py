class KnowAll:
    cls_count = 6

    def __init__(self, count:int = 0):
        self.count = count
    

    def __add__(self, num:int):
        self.count += num
    
    def __set_attr__(self, name, value):
        print(f'run __set_attr__: name-{name}, value-{value}')

    
    def value(self):
        print(self.count)