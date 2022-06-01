from pylox.expr import BaseExpr, BinaryExpr, GroupingExpr, LiteralExpr, UnaryExpr
from pylox.token import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens

        self._current = 0

    def parse(self) -> BaseExpr:
        try:
            return self.expression()
        except SyntaxError:
            return None

    def expression(self):
        return self.equality()

    def equality(self) -> BaseExpr:
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def comparison(self) -> BaseExpr:
        expr = self.term()

        while self.match(
            TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL
        ):
            operator = self.previous()
            right = self.term()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def term(self) -> BaseExpr:
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def factor(self) -> BaseExpr:
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def unary(self) -> BaseExpr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return UnaryExpr(operator, right)

        return self.primary()

    def primary(self) -> BaseExpr:
        if self.match(TokenType.FALSE):
            return LiteralExpr(False)
        elif self.match(TokenType.TRUE):
            return LiteralExpr(True)
        elif self.match(TokenType.NIL):
            return LiteralExpr(None)
        elif self.match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self.previous().literal)
        elif self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression.")
            return GroupingExpr(expr)

        raise self.error(self.peek(), "Expect expression.")

    def match(self, *token_types: list[TokenType]) -> bool:
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True

        return False

    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end:
            return False
        return self.peek().token_type is token_type

    def advance(self):
        if not self.is_at_end:
            self._current += 1
        return self.previous()

    @property
    def is_at_end(self):
        return self.peek().token_type is TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self._current]

    def previous(self) -> Token:
        return self.tokens[self._current - 1]

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()

        raise self.error(self.peek(), message)

    def error(self, token: Token, msg: str):
        if token.token_type is TokenType.EOF:
            print(token.lineno, " at end", msg)
        else:
            print(token.lineno, " at '", token.lexeme, "'", msg)

        return SyntaxError()

    def synchronize(self):
        self.advance()

        while not self.is_at_end:
            if self.previous().token_type is TokenType:
                return

            if self.peek().token_type in [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ]:
                return

            self.advance()
