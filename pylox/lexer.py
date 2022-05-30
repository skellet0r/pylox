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
            # one or two character tokens
            case "!":
                # default to single character token
                token_type = TokenType.BANG
                if self.peek() == "=":
                    # if the next token is '=' char type is different
                    token_type = TokenType.BANG_EQUAL
                    # increment the counter
                    self._current += 1
                # add the token either one or two character
                self.add_token(token_type)
            case "=":
                token_type = TokenType.EQUAL
                if self.peek() == "=":
                    token_type = TokenType.EQUAL_EQUAL
                    self._current += 1
                self.add_token(token_type)
            case "<":
                token_type = TokenType.LESS
                if self.peek() == "=":
                    token_type = TokenType.LESS_EQUAL
                    self._current += 1
                self.add_token(token_type)
            case ">":
                token_type = TokenType.GREATER
                if self.peek() == "=":
                    token_type = TokenType.GREATER_EQUAL
                    self._current += 1
                self.add_token(token_type)
            # special case
            case "/":
                # '/' can be followed by another '/' to represent a comment
                # in which case the rest of the line from that point is a comment
                if self.peek() == "/":
                    # '\0' represents a EOF
                    while self.peek() not in ["\n", "\0"]:
                        self._current += 1
                else:
                    self.add_token(TokenType.SLASH)

    def consume(self) -> str:
        char = self.source[self._current]
        self._current += 1
        return char

    def peek(self, n: int = 0) -> str:
        if (idx := self._current + n) < len(self.source) and idx > -1:
            return self.source[idx]
        return "\0"

    def add_token(self, token_type: TokenType, literal: object = None):
        token = Token(token_type, self.source[self._start : self._current], literal, self._lineno)
        self.tokens.append(token)
