# File solely for testing parts of Python to understand *exact* functionality
class Outer():
    def __init__(self):
        self.val1 = 10
        self.val2 = 10

classVar = Outer()
x = classVar.val1
