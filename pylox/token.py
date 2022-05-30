import enum


class Token:
    def __init__(self, token_type: "TokenType", lexeme: str, literal: object, lineno: int):
        # raw substring from the source code
        # smallest sequence of characters that represent something
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.lineno = lineno

    def __repr__(self) -> str:
        return f"Token({self.token_type}, '{self.lexeme}', {self.literal}, {self.lineno})"


ONE_CHAR_TOKENS = (
    "LEFT_BRACE",
    "RIGHT_BRACE",
    "LEFT_PAREN",
    "RIGHT_PAREN",
    "COMMA",
    "DOT",
    "MINUS",
    "PLUS",
    "SEMICOLON",
    "SLASH",
    "STAR",
)
ONE_OR_TWO_CHAR_TOKENS = (
    "BANG",
    "BANG_EQUAL",
    "EQUAL",
    "EQUAL_EQUAL",
    "GREATER",
    "GREATER_EQUAL",
    "LESS",
    "LESS_EQUAL",
)
LITERAL_TOKENS = (
    "IDENTIFIER",
    "NUMBER",
    "STRING",
)
RESERVED_TOKENS = (
    "AND",
    "CLASS",
    "ELSE",
    "FALSE",
    "FOR",
    "FUN",
    "IF",
    "NIL",
    "OR",
    "PRINT",
    "RETURN",
    "SUPER",
    "THIS",
    "TRUE",
    "VAR",
    "WHILE",
)
EOF_TOKEN = ("EOF",)
ALL_TOKENS = ONE_CHAR_TOKENS + ONE_OR_TWO_CHAR_TOKENS + LITERAL_TOKENS + RESERVED_TOKENS + EOF_TOKEN

TokenType = enum.Enum("TokenType", ALL_TOKENS)
