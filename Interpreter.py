from Stmt import *
from Expr import *
from typing import Tuple,Any
from TokenType import TokenType

class JesseRuntimeError(RuntimeError):
    def __init__(self, pos: Tuple[int], message: str) -> None:
        super().__init__(message)
        self.pos = pos

class Interpreter:
    '''
    The interpreter class for the Jesse programming language.
    It implements all the visitor methods for the AST nodes.
    '''

    def __init__(self, jesse:object,source:str) -> None:
        self.jesse = jesse
        self.source = source
        self.lines = source.splitlines()


    def interpret(self, statements: List[Stmt]) -> None:
        try:
            for statement in statements:
                self.execute(statement)
        except JesseRuntimeError as error:
            pos = error.pos
            code = self.lines[pos[0] - 1]
            self.jesse.runtime_error(code,pos,error)

    def visit_literal_expr(self, expr: Literal) -> Any:
        return expr.value

    def visit_unary_expr(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)

        if expr.operator.token_type == TokenType.BANG:
            return not self.is_truthy(right)
        elif expr.operator.token_type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -right

        # Unreachable.
        return None

    def check_number_operand(self, operator: Token, operand: Any) -> None:
        if isinstance(operand, float):
            return
        raise JesseRuntimeError(operator.pos, "operands must be a numbers, its basic math yo")

    def check_number_operands(self, operator: Token, left: Any, right: Any) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise JesseRuntimeError(operator.pos, "operands must be numbers, its basic math yo")

    def is_truthy(self, obj: Any) -> bool:
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def is_equal(self, a: Any, b: Any) -> bool:
        return a == b

    def stringify(self, obj: Any) -> str:
        # Convert None to "i am the danger".
        # Convert True to "cartel" and False to "dea"
        # Convert floats to strings and append "gm" at the end
        if obj is None:
            return "i am the danger"
        if isinstance(obj, bool):
            return "cartel" if obj else "dea"
        if isinstance(obj, float):
            return f"{obj:g}gm"
                
        if isinstance(obj, str):
            return obj
        
        return str(obj)

    def visit_grouping_expr(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expression)

    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def execute(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def visit_expression_stmt(self, stmt: Expression) -> None:
        self.evaluate(stmt.expression)

    def visit_saymyname_stmt(self, stmt: SayMyName) -> None:
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    

    def visit_binary_expr(self, expr: Binary) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.token_type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return left - right
        elif expr.operator.token_type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            return left / right
        elif expr.operator.token_type == TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return left * right
        elif expr.operator.token_type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            raise JesseRuntimeError(expr.operator.pos, "operands must be two numbers or two strings yo")
        elif expr.operator.token_type == TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return left > right
        elif expr.operator.token_type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left >= right
        elif expr.operator.token_type == TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return left < right
        elif expr.operator.token_type == TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left <= right
        elif expr.operator.token_type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif expr.operator.token_type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)