from typing import List, Optional, Tuple, TypeVar
from Token import Token
from TokenType import TokenType


import re



# match = re.match(r'\/\*(.|\n)*?\*\/', self.source)
#             if match:
#                 self.source = self.source[match.end():]
#                 continue


Jesse = TypeVar('Jesse')

class Scanner:
    '''
    Scanner class for the Jesse programming language. 
    It makes use of regular expressions to match tokens.
    '''
    def __init__(self, jesse:Jesse, source: str):
        self.jesse = jesse
        self.source = source
        self.tokens: List[Token] = []
        self.column = 0
        self.line = 1


    def scan_tokens(self) -> List[Token]:
        while self.source:
            # Matches whitespace
            # Match a whitespace character any number of times that is not a newline
            match = re.match(r'[^\S\r\n]', self.source)
            if match:
                self.column += match.end()
                self.source = self.source[match.end():]
                continue
            # Matches newlines to keep track of line numbers
            match = re.match(r'\n', self.source)
            if match:
                self.column = 0
                self.source = self.source[match.end():]
                self.line += 1
                continue
            # Matches comments
            # Match // followed by any character any number of times
            match = re.match(r'\/\/.*', self.source)
            if match:
                self.column += match.end()
                self.source = self.source[match.end():]
                continue
            
            # Matches strings
            # Match " followed by any character any number of times that is not a " or is a escape character
            match = re.match(r'\"(\\.|[^"])*\"', self.source)
            if match:
                pos = (self.line, self.column)
                self.column += match.end() 
                self.add_token(TokenType.STRING, match.group(), match.group(), pos)
                self.source = self.source[match.end():]
                continue
            # Check if there's an unterminated string
            match = re.match(r'\".*', self.source)
            if match:
                code = self.source[match.start():match.end()]
                pos = (self.line, self.column)
                self.jesse.error(code, pos, 'Unterminated string.')
                break

           
                

                

        return self.tokens

    def add_token(self, token_type: TokenType, lexeme: str, literal: Optional[object], pos: Tuple[int,int]) -> None:
        self.tokens.append(Token(token_type, lexeme, literal, pos))
            
