from pylox.token import Token, TokenType


class Lexer:
    """Scan source code capturing valid tokens."""

    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []

        self._current = 0
        self._start = 0
        self._lineno = 1

    def scan(self) -> list[Token]:
        # loop through source scanning for tokens
        while self._current < len(self.source):
            self._start = self._current
            self.scan_token()

        # the last token should be the EOF
        if len(self.tokens) != 0 and self.tokens[-1].token_type is not TokenType.EOF:
            eof_token = Token(TokenType.EOF, "", None, self._lineno)
            self.tokens.append(eof_token)

        return self.tokens

    def scan_token(self):
        char = self.consume()

        match char:
            # one character tokens
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
            case " " | "\r" | "\t":
                # skip whitespace
                pass
            case "\n":
                # newline increment line number
                self._lineno += 1

    def consume(self) -> str:
        char = self.source[self._current]
        self._current += 1
        return char

    def add_token(self, token_type: TokenType, literal: object = None):
        token = Token(token_type, self.source[self._start : self._current], literal, self._lineno)
        self.tokens.append(token)
