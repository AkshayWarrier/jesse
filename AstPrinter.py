from Expr import *

class AstPrinter:
    def print(self, expr:Expr):
        return expr.accept(self)

    def parenthesize(self, name:str, *exprs:Expr):
        result = "(" + name
        for expr in exprs:
            result += " "
            result += expr.accept(self)
        result += ")"
        return result

    def visit_binary_expr(self, expr:Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr:Grouping):
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr:Literal):
        if expr.value == None:
            return "i am the danger"
        return str(expr.value)

    def visit_unary_expr(self, expr:Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

