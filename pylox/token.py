import dataclasses
import enum

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


@dataclasses.dataclass
class Token:
    token_type: TokenType
    lexeme: str
    literal: object
    lineno: int
