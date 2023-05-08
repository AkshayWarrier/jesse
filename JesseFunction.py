from JesseCallable import JesseCallable
from Environment import Environment
from ReturnException import ReturnException

class JesseFunction(JesseCallable):
    def __init__(self, declaration):
        self.declaration = declaration

    def arity(self):
        return len(self.declaration.params)

    def call(self,interpreter,arguments):
        environment = Environment(interpreter.globals)

        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme,arguments[i])
        try:
            interpreter.execute_block(self.declaration.body,environment)
        except ReturnException as e:
            return e.value

        return None

    def __str__(self):
        return "<jesse fn " + self.declaration.name.lexeme + ">"