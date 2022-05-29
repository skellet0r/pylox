import string

from pylox.error import error
from pylox.token import Token, TokenType


class Scanner:
    KEYWORDS = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []

        # start = points to the first char in the lexeme being scanned
        self.start = 0
        # current = points to the char currently being considered
        self.current = 0
        # tracks what source line current is on, needed for location tracking
        self.line = 1

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end:
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()

        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "!":
                if self.match_("="):
                    self.add_token(TokenType.BANG_EQUAL)
                else:
                    self.add_token(TokenType.BANG)
            case "=":
                if self.match_("="):
                    self.add_token(TokenType.EQUAL_EQUAL)
                else:
                    self.add_token(TokenType.EQUAL)
            case "<":
                if self.match_("="):
                    self.add_token(TokenType.LESS_EQUAL)
                else:
                    self.add_token(TokenType.LESS)
            case ">":
                if self.match_("="):
                    self.add_token(TokenType.GREATER_EQUAL)
                else:
                    self.add_token(TokenType.GREATER)
            case "/":
                if self.match_("/"):
                    while self.peek() != "\n" and not self.is_at_end:
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case _:
                if self.is_digit(c):
                    self.number()
                elif self.is_alpha(c):
                    self.identifier()
                else:
                    error(self.line, "Unexpected character.")

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source[self.start : self.current]
        type_ = self.KEYWORDS.get(text, TokenType.IDENTIFIER)
        self.add_token(type_)

    def is_alpha(self, char) -> bool:
        return char in string.ascii_letters

    def is_digit(self, char) -> bool:
        return char in string.digits or char == "_"

    def is_alpha_numeric(self, char):
        return self.is_alpha(char) or self.is_digit(char)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def match_(self, expected: str):
        if self.is_at_end:
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.is_at_end:
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def add_token(self, token_type: TokenType, literal: object = None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        return char

    def string(self):
        while self.peek() != '"' and not self.is_at_end:
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end:
            error(self.line, "Unterminated string")
            return

        self.advance()

        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    @property
    def is_at_end(self):
        return self.current >= len(self.source)
