from typing import List
from Token import Token

from Expr import Expr

class Stmt:
    pass

class Expression(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)

class SayMyName(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_saymyname_stmt(self)

class Cook(Stmt):
    def __init__(self, name: Token, initializer: Expr) -> None:
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_cook_stmt(self)
