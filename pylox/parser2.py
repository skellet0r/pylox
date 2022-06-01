from typing import Optional

from pylox.exceptions import ExceptionList, SyntacticalError
from pylox.expr import BaseExpr, GroupingExpr, LiteralExpr
from pylox.token import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token], exception_list: ExceptionList):
        self.tokens = tokens
        self.exception_list = exception_list

        self._current = 0

    def peek(self, n: int = 0) -> Optional[Token]:
        if (idx := self._current + n) >= 0 and idx < len(self.tokens):
            return self.tokens[idx]
        return None

    @property
    def at_end(self) -> bool:
        return self.peek().token_type is TokenType.EOF

    def consume(self) -> Token:
        self._current += 1
        return self.peek(-1)

    def primary(self) -> BaseExpr:
        token = self.consume()
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
                if (next_token := self.consume()).token_type is not TokenType.RIGHT_PAREN:
                    raise SyntacticalError(next_token, "Expected ')' after expression.")
                return GroupingExpr(expr)
            case _:
                raise SyntacticalError(token, "Expected expression.")
