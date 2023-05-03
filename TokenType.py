from enum import Enum, auto

class TokenType(Enum):
    # Single character tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()
    QUESTION_MARK = auto()
    COLON = auto()

    # One or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    METH = auto() # Number

    # Keywords
    AND = auto()
    # CLASS = auto()
    ELSE = auto()
    DEA = auto() # False value
    # FUN = auto()
    # THE_ONE_WHO_KNOCKS = auto() # For loop
    JESSE_IF = auto() # If statement
    I_AM_THE_DANGER = auto() # Null value
    OR = auto()
    SAY_MY_NAME = auto() # Print statement
    # RETURN = auto()
    # SUPER = auto()
    # THIS = auto()
    CARTEL = auto() # True value
    COOK = auto() # Variable declaration
    THE_ONE_WHO_KNOCKS = auto() # While loop
    EOF = auto()