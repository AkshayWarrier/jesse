from typing import Tuple
from TokenType import TokenType

class Token:
    '''
    Token class for the Jesse programming language.
    
    token_type: TokenType object
    lexeme: String representation of the token
    literal: Literal value of the token if any
    pos: Position of the token in the source code in the form (line, column)
    '''
    def __init__(self, token_type: TokenType, lexeme: str, literal: object, pos: Tuple[int,int]) -> None:
        # Token type
        self.token_type = token_type
        # String representation of the token
        self.lexeme = lexeme
        # Literal value of the token if any
        self.literal = literal
        # Position of the token in the source code in the form (line, column)
        self.pos = pos

    def __str__(self) -> str:
        return f'Token({self.token_type}, {self.lexeme}, {self.literal}, {self.pos})'

if __name__ == '__main__':
    token = Token(TokenType.STRING, 'hello', 'hello', (1, 1))
    print(token)