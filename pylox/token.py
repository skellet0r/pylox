from enum import Enum, auto


class TokenType(Enum):
    # single character tokens
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

    # one or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()


class Token:
    def __init__(self, type_: TokenType, lexeme: str, literal: object, line: int):
        self.type_ = type_
        # lexeme: a sequence of chars that grouped together represent something
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return f"{self.type_} {self.lexeme} {self.literal}"
