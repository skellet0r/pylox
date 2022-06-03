from typing import Optional

from pylox.exceptions import ExceptionList, SyntacticalError
from pylox.expr import BaseExpr, BinaryExpr, GroupingExpr, LiteralExpr, UnaryExpr
from pylox.token import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token], exception_list: ExceptionList):
        self.tokens = tokens
        self.exception_list = exception_list

        self._current = 0

    def parse(self) -> BaseExpr:
        try:
            return self.expression()
        except SyntacticalError as e:
            self.exception_list.append(e)
            return None

    def peek(self, n: int = 0) -> Optional[Token]:
        if (idx := self._current + n) >= 0 and idx < len(self.tokens):
            return self.tokens[idx]
        return None

    def consume(self) -> Token:
        self._current += 1
        return self.peek(-1)

    def expression(self) -> BaseExpr:
        return self.equality(self.consume())

    def equality(self, token: Token) -> BaseExpr:
        expr = self.comparison(token)

        while self.peek().token_type in [TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]:
            operator = self.consume()
            right = self.comparison(self.consume())
            expr = BinaryExpr(expr, operator, right)

        return expr

    def comparison(self, token: Token) -> BaseExpr:
        expr = self.term(token)

        while self.peek().token_type in [
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ]:
            operator = self.consume()
            right = self.term(self.consume())
            expr = BinaryExpr(expr, operator, right)

        return expr

    def term(self, token: Token) -> BaseExpr:
        expr = self.factor(token)  # 4

        while self.peek().token_type in [TokenType.MINUS, TokenType.PLUS]:
            # token under the cursor is a '+' or '-' operator
            operator = self.consume()
            right = self.factor(self.consume())
            expr = BinaryExpr(expr, operator, right)

        return expr

    def factor(self, token: Token) -> BaseExpr:
        expr = self.unary(token)

        while self.peek().token_type in [TokenType.SLASH, TokenType.STAR]:
            # token under the cursor is a '/' or '*' operator
            operator = self.consume()
            right = self.unary(self.consume())
            expr = BinaryExpr(expr, operator, right)

        return expr

    def unary(self, token: Token) -> BaseExpr:
        if token.token_type in [TokenType.BANG, TokenType.MINUS]:
            # token is an '!' or '-' operator
            right = self.unary(self.consume())
            return UnaryExpr(token, right)

        # token is not an operator so must be a primary
        return self.primary(token)

    def primary(self, token: Token) -> BaseExpr:
        """Highest precendence, bottom of grammar productions."""
        match token.token_type:
            case TokenType.FALSE:
                return LiteralExpr(False)
            case TokenType.TRUE:
                return LiteralExpr(True)
            case TokenType.NIL:
                return LiteralExpr(None)
            case TokenType.NUMBER | TokenType.STRING:
                return LiteralExpr(token.literal)
            case TokenType.LEFT_PAREN:
                expr = self.expression()
                if (next_token := self.peek()).token_type is not TokenType.RIGHT_PAREN:
                    raise SyntacticalError(next_token, "Expected ')' after expression.")
                self._current += 1  # consume the ')'
                return GroupingExpr(expr)
            case _:
                raise SyntacticalError(token, "Expected expression.")

    def synchronize(self):
        if self.peek().token_type is not TokenType.EOF:
            self._current += 1

        while self.peek().token_type is not TokenType.EOF:
            if self.peek(-1).token_type is TokenType.SEMICOLON:
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

            self._current += 1  # consume the token
