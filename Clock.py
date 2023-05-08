import time
from JesseCallable import JesseCallable

class Clock(JesseCallable):
    '''
    This class represents the clock function in Jesse.
    '''
    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        return time.time()

    def __str__(self):
        return "<jesse native fn>"