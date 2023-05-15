from Stmt import *
from Expr import *
from typing import Any
from TokenType import TokenType

from Environment import Environment
from JesseCallable import JesseCallable
from JesseRuntimeError import JesseRuntimeError
from JesseFunction import JesseFunction
from Clock import Clock
from ReturnException import ReturnException

class Interpreter:
    '''
    The interpreter class for the Jesse programming language.
    It implements all the visitor methods for the AST nodes.
    '''

    def __init__(self, jesse:object,source:str) -> None:
        self.jesse = jesse
        self.globals = Environment()
        self.environment = self.globals
        self.source = source
        self.lines = source.splitlines()

        self.globals.define("clock", Clock())
        # Mappping of expressions to their depth in the stack
        self.locals = {}


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

    def visit_logical_expr(self, expr: Logical) -> Any:
        left = self.evaluate(expr.left)

        if expr.operator.token_type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left

        return self.evaluate(expr.right)

    def visit_unary_expr(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)

        if expr.operator.token_type == TokenType.BANG:
            return not self.is_truthy(right)
        elif expr.operator.token_type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -right

        # Unreachable.
        return None

    def visit_variable_expr(self, expr: Expr) -> None:
        return self.look_up_variable(expr.name, expr)

    def look_up_variable(self, name: Token, expr: Expr) -> Any:
        distance = self.locals.get(expr)
        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)
        else:
            return self.globals.get(name)

    def check_number_operand(self, operator: Token, operand: Any) -> None:
        if isinstance(operand, float):
            return
        raise JesseRuntimeError(operator.pos, "operands must be a numbers, its basic math yo")

    def check_number_operands(self, operator: Token, left: Any, right: Any) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise JesseRuntimeError(operator.pos, "operands must be numbers, its basic math yo")

    def is_truthy(self, obj: Any) -> bool:
        if obj is None or obj == 0:
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
            return obj.strip('"')
        
        return str(obj)

    def visit_grouping_expr(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expression)

    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def execute(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def resolve(self, expr:Expr, depth:int) -> None:
        self.locals[expr] = depth

    def execute_block(self, statements: List[Stmt], environment: Environment) -> None:
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visit_block_stmt(self, stmt: Block) -> None:
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_jesseif_stmt(self, stmt: JesseIf) -> None:
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_expression_stmt(self, stmt: Expression) -> None:
        self.evaluate(stmt.expression)

    def visit_bettercall_stmt(self, stmt: BetterCall) -> None:
        function = JesseFunction(stmt,self.environment)
        self.environment.define(stmt.name.lexeme, function)
        return None

    def visit_saymyname_stmt(self, stmt: SayMyName) -> None:
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visit_return_stmt(self, stmt: Return) -> None:
        value = None
        if stmt.value != None:
            value = self.evaluate(stmt.value)

        raise ReturnException(value)

    def visit_cook_stmt(self, stmt: Cook) -> None:
        value = None
        if(stmt.initializer != None):
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme,value)

    def visit_theonewhoknocks_stmt(self, stmt: TheOneWhoKnocks) -> None:
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

        return None

    def visit_assign_expr(self, expr: Assign) -> Any:
        value = self.evaluate(expr.value)
        distance = self.locals.get(expr)
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
        return value

    def visit_ternary_expr(self, expr: Ternary) -> Any:
        condition = self.evaluate(expr.condition)
        if self.is_truthy(condition):
            return self.evaluate(expr.then_branch)
        else:
            return self.evaluate(expr.else_branch)

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

    def visit_call_expr(self,expr: Call) -> Any:
        # Evaluate the callee, usually an identifier
        callee = self.evaluate(expr.callee)
        arguments = []
        # Evaluate the arguments which can also be identifiers or literals
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))
        # Check if the callee is a JesseCallable object
        if not isinstance(callee, JesseCallable):
            raise JesseRuntimeError(expr.paren.pos,"you can only call functions and classes yo")

        # Check arity of the function
        if len(arguments) != callee.arity():
            raise JesseRuntimeError(expr.paren.pos,f"expected {function.arity()} arguments but got {len(arguments)} yo")
        return callee.call(self,arguments)