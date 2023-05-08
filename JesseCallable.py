
class JesseCallable:
    '''
    This is an abstract class that represents a callable object in Jesse.
    '''
    def __init__(self, callee=None):
        self.callee = callee

    def arity(self):
        pass

    def call(self, interpreter, arguments):
        pass

    def __str__(self):
        pass
