from typing import List, Optional, Tuple, TypeVar
from Token import Token
from TokenType import TokenType
import re



class Scanner:
    '''
    Scanner class for the Jesse programming language. 
    It makes use of regular expressions to match tokens.

    jesse: Jesse object
    source: Source code of the Jesse program
    '''
    def __init__(self, jesse:object, source: str):
        self.jesse = jesse
        self.source = source
        self.lines = source.splitlines()
        self.tokens: List[Token] = []
        self.column = 0
        self.line = 1

        self.single_char_to_token = {
            '(': TokenType.LEFT_PAREN,
            ')': TokenType.RIGHT_PAREN,
            '{': TokenType.LEFT_BRACE,
            '}': TokenType.RIGHT_BRACE,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
            '-': TokenType.MINUS,
            '+': TokenType.PLUS,
            '*': TokenType.STAR,
            ';': TokenType.SEMICOLON,
            '/': TokenType.SLASH,
            '!': TokenType.BANG,
            '=': TokenType.EQUAL,
            '<': TokenType.LESS,
            '>': TokenType.GREATER,
            '?': TokenType.QUESTION_MARK,
            ':': TokenType.COLON,
        }

        self.double_char_to_token = {
            '==': TokenType.EQUAL_EQUAL,
            '!=': TokenType.BANG_EQUAL,
            '<=': TokenType.LESS_EQUAL,
            '>=': TokenType.GREATER_EQUAL,
        }

        self.reserved_keywords = {
            "and": TokenType.AND,
            "cartel": TokenType.CARTEL,
            "cook": TokenType.COOK,
            "dea": TokenType.DEA,
            "else": TokenType.ELSE,
            "i am the danger" : TokenType.I_AM_THE_DANGER,
            "jesse if": TokenType.JESSE_IF,
            "or" : TokenType.OR,
            "say my name": TokenType.SAY_MY_NAME,
            "the one who knocks": TokenType.THE_ONE_WHO_KNOCKS,
            "better call": TokenType.BETTER_CALL,
            "return": TokenType.RETURN,
        }

        # Keywords that contain whitespaces
        self.whitespace_keywords = {key:self.reserved_keywords[key] for key in self.reserved_keywords if re.match(r'.*\s.*', key)}
        self.matching_string = '|'.join(self.whitespace_keywords.keys())

    def scan_tokens(self) -> List[Token]:
        
        while self.source:
            did_match = False

            # Matches whitespace
            # Match a whitespace character any number of times that is not a newline
            match = re.match(r'[^\S\r\n]', self.source)
            if match:
                self.column += match.end()
                self.source = self.source[match.end():]
                did_match = True
                continue
            # Matches newlines to keep track of line numbers
            match = re.match(r'\n', self.source)
            if match:
                self.column = 0
                self.source = self.source[match.end():]
                self.line += 1
                did_match = True
                continue
            # Matches comments
            # Match // followed by any character any number of times
            match = re.match(r'\/\/.*', self.source)
            if match:
                self.column += match.end()
                self.source = self.source[match.end():]
                did_match = True
                continue
            
            # Matches strings
            # Match " followed by any character any number of times that is not a " or is a escape character
            match = re.match(r'\"(\\.|[^"])*\"', self.source)
            if match:
                pos = (self.line, self.column)
                self.column += match.end() 
                self.add_token(TokenType.STRING, match.group(), match.group(), pos)
                self.source = self.source[match.end():]
                did_match = True
                continue
            # Check if there's an unterminated string
            match = re.match(r'\".*', self.source)
            if match:
                code = self.lines[self.line-1]
                pos = (self.line, self.column)
                self.jesse.error(code, pos, 'this string is not terminated yo')
                break

            # Matches keywords with whitespace
            match = re.match(rf'({self.matching_string})', self.source)
            if match:
                pos = (self.line, self.column)
                self.column += match.end()
                self.add_token(self.whitespace_keywords[match.group()], match.group(), None, pos)
                self.source = self.source[match.end():]
                did_match = True
                continue
            # Match identifiers and keywords
            match = re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',self.source)
            if match:
                pos = (self.line, self.column)
                self.column += match.end()
                self.add_token(self.reserved_keywords.get(match.group(), TokenType.IDENTIFIER), match.group(), None, pos)
                self.source = self.source[match.end():]
                did_match = True
                continue
            # Match meth (numbers)
            match = re.match(r'\d+(\.\d+)?', self.source)
            if match:
                # Try to match gm after the number
                # Otherwise raise an error
                if self.source[match.end():match.end()+2] == 'gm':
                    final_match = match.group()+"gm"
                    pos = (self.line, self.column)
                    self.column += match.end() + 2
                    self.add_token(TokenType.METH, final_match, float(match.group()), pos)
                    self.source = self.source[match.end()+2:]
                    did_match = True
                    continue
                else:
                    code = self.lines[self.line-1]
                    pos = (self.line, self.column+match.end()-1)
                    self.jesse.error(code, pos, "you haven't mentioned a unit of measurement for this number yo")
                    break
            # Match single character tokens
            match = re.match(r'[()\{\},\.\-+*/;?:]', self.source)
            if match:
                pos = (self.line, self.column)
                self.column += match.end()
                self.add_token(self.single_char_to_token[match.group()], match.group(), None, pos)
                self.source = self.source[match.end():]
                did_match = True
                continue
            # Match potential two character tokens
            match = re.match(r'[=!<>]', self.source)
            if match:
                if self.source[match.start():match.end()+1] in self.double_char_to_token:
                    pos = (self.line, self.column)
                    self.column += match.end() + 1
                    self.add_token(self.double_char_to_token[self.source[match.start():match.end()+1]], self.source[match.start():match.end()+1], None, pos)
                    self.source = self.source[match.end()+1:]
                    did_match = True
                    continue
                else:
                    pos = (self.line, self.column)
                    self.column += match.end()
                    self.add_token(self.single_char_to_token[match.group()], match.group(), None, pos)
                    self.source = self.source[match.end():]
                    did_match = True
                    continue
        
            if not did_match:
                code = self.lines[self.line-1]
                pos = (self.line, self.column)
                self.jesse.error(code, pos, "i don't understand this yo")
                break

        self.add_token(TokenType.EOF, "", None, (self.line, self.column))
        return self.tokens

    def add_token(self, token_type: TokenType, lexeme: str, literal: Optional[object], pos: Tuple[int,int]) -> None:
        self.tokens.append(Token(token_type, lexeme, literal, pos))
            
