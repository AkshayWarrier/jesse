from Expr import *
from typing import List, TypeVar
from Token import Token
from TokenType import TokenType

Jesse = TypeVar('Jesse')
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
    def __init__(self, jesse:Jesse, source:str, tokens: List[Token]) -> None:
        self.jesse = jesse
        self.source = source
        self.lines = source.splitlines()
        self.tokens = tokens
        self.current = 0

    def parse(self) -> None:
        try:
            return self.expression()
        except ParseError:
            return None    

    def expression(self) -> Expr:
        return self.equality()

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

        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.DEA):
            return Literal(False)
        if self.match(TokenType.CARTEL):
            return Literal(True)
        if self.match(TokenType.I_AM_THE_DANGER):
            return Literal(None)

        if self.match(TokenType.METH, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            # TODO: Make this a better error message
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        # TODO: Make this a better error message
        raise self.error(self.peek(), "Expect expression.")
    
    def match(self, *types: TokenType) -> bool:
        # Try to match the current token with one of the types in the list
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type: TokenType, message: str) -> Token:
        # Try to consume a token of a given token_type
        if self.check(token_type):
            return self.advance()
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
                TokenType.WE_ARE_DONE_WHEN_I_SAY_WE_ARE_DONE,
            ):
                return

            self.advance()

    