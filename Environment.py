from JesseRuntimeError import JesseRuntimeError

from Token import Token

class Environment():
    def __init__(self,enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def get(self,name:Token):
        if(name.lexeme in self.values):
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise JesseRuntimeError(name.pos,"i don't remember defining this yo")

    def assign(self,name:Token,value:object):
        if(name.lexeme in self.values):
            self.values[name.lexeme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name,value)
            return
        
        raise JesseRuntimeError(name.pos,"i don't remember defining this yo")
    
    def define(self,name:str,value:object):
        self.values[name] = value

    def ancestor(self,distance:int):
        env = self
        for i in range(distance):
            env = env.enclosing
        return env

    def get_at(self,distance:int,name:str):
        return self.ancestor(distance).values[name]

    def assign_at(self,distance:int,name:Token,value:object):
        self.ancestor(distance).values[name.lexeme] = value
