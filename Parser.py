from Expr import *
from Stmt import *
from typing import List, Optional
from Token import Token
from TokenType import TokenType


class ParseError(Exception):
    '''
    ParseError class for the Jesse programming language.
    The error is raised internally and caught within the parser too.
    It doesn't escape the parser.
    '''
class Parser:
    '''
    A recursive descent parser for the Jesse programming language.

    jesse: Jesse object
    tokens: List of tokens to parse
    '''
    def __init__(self, jesse:object, source:str, tokens: List[Token]) -> None:
        self.jesse = jesse
        self.source = source
        self.lines = source.splitlines()
        self.tokens = tokens
        self.current = 0

    def parse(self) -> List[Stmt]:
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    def expression(self) -> Expr:
        return self.assignment()

    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.COOK):
                return self.cook_declaration()
            if self.match(TokenType.BETTER_CALL):
                return self.bettercall_declaration("function")
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def statement(self) -> Stmt:
        # Check if its a recognized statement
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.match(TokenType.THE_ONE_WHO_KNOCKS):
            return self.theonewhoknocks_statement()
        if self.match(TokenType.JESSE_IF):
            return self.jesseif_statement()
        if self.match(TokenType.SAY_MY_NAME):
            return self.saymyname_statement()
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        # If not then it must be an expression statement
        return self.expression_statement()

    def theonewhoknocks_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "where's my left paren b*tch?")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "where's my right paren b*tch?")
        body = self.statement()
        return TheOneWhoKnocks(condition, body)

    def jesseif_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "where's my left paren b*tch?")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "where's my right paren b*tch?")
        then_branch = self.statement()
        else_branch: Stmt = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()
        return JesseIf(condition, then_branch, else_branch)

    def saymyname_statement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "where's my semicolon b*tch?")
        return SayMyName(value)

    def return_statement(self) -> Stmt:
        keyword = self.previous()
        value: Expr = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()
        self.consume(TokenType.SEMICOLON, "where's my semicolon b*tch?")
        
        return Return(keyword, value)

    def cook_declaration(self) -> Stmt:
        name = self.consume(TokenType.IDENTIFIER, "what's the name of your cook yo")
        initializer: Expr = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "where's my semicolon b*tch?")
        return Cook(name, initializer) 

    def expression_statement(self) -> Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "where's my semicolon b*tch?")
        return Expression(expr)

    def bettercall_declaration(self, kind: str) -> Stmt:
        name = self.consume(TokenType.IDENTIFIER, "what's the name of your function yo")
        self.consume(TokenType.LEFT_PAREN, "where's my left paren b*tch?")
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                parameters.append(self.consume(TokenType.IDENTIFIER, "what's the name of your parameter yo"))
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RIGHT_PAREN, "where's my right paren b*tch?")
        self.consume(TokenType.LEFT_BRACE, "where's my left brace b*tch?")
        body = self.block()
        return BetterCall(name, parameters, body)

    def block(self) -> List[Stmt]:
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "where's my right brace b*tch?")
        return statements

    def assignment(self) -> Expr:
        expr = self.logical_or()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            self.error(equals, "this is an invalid assignment target yo")

        return expr

    def logical_or(self) -> Expr:
        expr = self.logical_and()

        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.logical_and()
            expr = Logical(expr, operator, right)

        return expr

    def logical_and(self) -> Expr:
        expr = self.ternary()

        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.ternary()
            expr = Logical(expr, operator, right)

        return expr
    
    # TODO: Add support for nested ternary expressions
    def ternary(self) -> Expr:
        condition = self.equality()
        if self.match(TokenType.QUESTION_MARK):
            then_branch = self.equality()
            if self.match(TokenType.COLON):
                else_branch = self.equality()
                return Ternary(condition,then_branch,else_branch)
            else:
                self.error(self.previous(),"this is an invalid ternary statement yo")
        return condition

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.call()

    def call(self) -> Expr:
        expr = self.primary()
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            else:
                break
        return expr

    def finish_call(self, callee: Expr) -> Call:
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                arguments.append(self.expression())
        paren = self.consume(TokenType.RIGHT_PAREN, "where's my right paren b*tch?")
        return Call(callee, paren, arguments)

    def primary(self) -> Expr:
        if self.match(TokenType.DEA):
            return Literal(False)
        elif self.match(TokenType.CARTEL):
            return Literal(True)
        elif self.match(TokenType.I_AM_THE_DANGER):
            return Literal(None)

        elif self.match(TokenType.METH, TokenType.STRING):
            return Literal(self.previous().literal)

        elif self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

        elif self.match(TokenType.LEFT_PAREN):
            matching_paren = self.previous()
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "you haven't closed this yo",matching=matching_paren)
            return Grouping(expr)

        raise self.error(self.peek(), "this ain't no expression yo")
    
    def match(self, *types: TokenType) -> bool:
        # Try to match the current token with one of the types in the list and consume it if it matches
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type: TokenType, message: str, matching: Optional[Token] = None) -> Token:
        # Try to consume a token of a given token_type
        if self.check(token_type):
            return self.advance()
        if matching:
            raise self.error(matching, message)
        raise self.error(self.peek(), message)

    def check(self, token_type: TokenType) -> bool:
        # Check if the current token is of the given token_type
        if self.is_at_end():
            return False
        return self.peek().token_type == token_type

    def advance(self) -> Token:
        # Advance the current token
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        # Pretty self explanatory
        return self.peek().token_type == TokenType.EOF

    def peek(self) -> Token:
        # Return the current token
        return self.tokens[self.current]

    def previous(self) -> Token:
        # Return the previous token
        return self.tokens[self.current - 1]

    def error(self, token: Token, message: str) -> ParseError:
        # Raise a parse error
        pos = token.pos
        code = self.lines[pos[0] - 1]
        self.jesse.error(code,pos,message)
        return ParseError()

    def synchronize(self) -> None:
        # Synchronize the parser
        self.advance()

        while not self.is_at_end():
            if self.previous().token_type == TokenType.SEMICOLON:
                return

            if self.peek().token_type in (
                TokenType.COOK,
                TokenType.JESSE_IF,
                TokenType.SAY_MY_NAME,
                TokenType.THE_ONE_WHO_KNOCKS,
                TokenType.BETTER_CALL,
            ):
                return

            self.advance()

    