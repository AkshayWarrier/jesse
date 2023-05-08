from typing import List
from Token import Token


class Expr:
    pass

class Assign(Expr):
    def __init__(self, name: Token, value: Expr) -> None:
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_expr(self)

class Ternary(Expr):
    def __init__(self, condition: Expr, then_branch: Expr, else_branch: Expr) -> None:
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_ternary_expr(self)

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

class Call(Expr):
    def __init__(self, callee: Expr, paren: Token, arguments: List[Expr]) -> None:
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call_expr(self)

class Grouping(Expr):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

class Literal(Expr):
    def __init__(self, value: object) -> None:
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)

class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logical_expr(self)

class Unary(Expr):
    def __init__(self, operator: Token, right: Expr) -> None:
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)

class Variable(Expr):
    def __init__(self, name: Token) -> None:
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)
