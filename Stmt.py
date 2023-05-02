from typing import List
from Token import Token

from Expr import Expr

class Stmt:
    pass

class Block(Stmt):
    def __init__(self, statements: List[Stmt]) -> None:
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)

class Expression(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)

class JesseIf(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt) -> None:
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_jesseif_stmt(self)

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
