from Stmt import *
from Expr import *
from typing import List

from Interpreter import Interpreter
from enum import Enum, auto

class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()

class Resolver():
    def __init__(self,jesse,source,interpreter):
        self.jesse = jesse
        self.lines = source.splitlines()
        self.interpreter = interpreter
        self.scopes:List[bool] = []
        self.current_function = FunctionType.NONE

    def resolve(self,statements:List[Stmt]):
        for statement in statements:
            self.resolve_stmt(statement)

    def resolve_function(self,function:BetterCall,ftype:FunctionType):
        enclosing_function = self.current_function
        self.current_function = ftype
        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()
        self.current_function = enclosing_function

    def resolve_stmt(self,stmt:Stmt):
        stmt.accept(self)

    def resolve_expr(self,expr:Expr):
        expr.accept(self)

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self,name:Token):
        if len(self.scopes) == 0:
            return
        # Get the innermost/current scope
        scope = self.scopes[-1]
        if name.lexeme in scope:
            pos = name.pos
            code = self.lines[pos[0] - 1]
            self.jesse.error(code,pos,"variable with this name already declared in this scope yo")
        # The variable has been declared but not initialized hence False
        scope[name.lexeme] = False

    def define(self,name:Token):
        if len(self.scopes) == 0:
            return
        self.scopes[-1][name.lexeme] = True

    def resolve_local(self,expr:Expr,name:Token):
        for i in range(len(self.scopes)-1,-1,-1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr,i)
                return

    def visit_block_stmt(self,stmt:Block):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()

    def visit_expression_stmt(self,stmt:Expression):
        self.resolve_expr(stmt.expression)

    def visit_jesseif_stmt(self,stmt:JesseIf):
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve_stmt(stmt.else_branch)

    def visit_saymyname_stmt(self,stmt:SayMyName):
        self.resolve_expr(stmt.expression)

    def visit_return_stmt(self,stmt:Return):
        if self.current_function == FunctionType.NONE:
            pos = stmt.keyword.pos
            code = self.lines[pos[0] - 1]
            self.jesse.error(code,pos,"you cannot return from top-level code yo")
        if stmt.value is not None:
            self.resolve_expr(stmt.value)

    def visit_theonewhoknocks_stmt(self,stmt:TheOneWhoKnocks):
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.body)

    def visit_bettercall_stmt(self,stmt:BetterCall):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.NONE)

    def visit_cook_stmt(self,stmt:Cook):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve_expr(stmt.initializer)
        self.define(stmt.name)

    def visit_variable_expr(self,expr:Variable):
        if len(self.scopes) != 0:
            scope = self.scopes[-1]
            if scope.get(expr.name.lexeme) == False:
                        pos = expr.name.pos
                        code = self.lines[pos[0] - 1]
                        self.jesse.error(code,pos,"cannot read local variable in its own initializer yo")
        self.resolve_local(expr,expr.name)

    def visit_assign_expr(self,expr:Assign):
        # If the RHS contains references to other variables, we need to resolve them first
        self.resolve_expr(expr.value)
        # Then we resolve the LHS
        self.resolve_local(expr,expr.name)

    def visit_binary_expr(self,expr:Binary):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)

    def visit_call_expr(self,expr:Call):
        self.resolve_expr(expr.callee)
        for arg in expr.arguments:
            self.resolve_expr(arg)

    def visit_grouping_expr(self,expr:Grouping):
        self.resolve_expr(expr.expression)

    def visit_literal_expr(self,expr:Literal):
        pass

    def visit_logical_expr(self,expr:Logical):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)

    def visit_unary_expr(self,expr:Unary):
        self.resolve_expr(expr.right)



    