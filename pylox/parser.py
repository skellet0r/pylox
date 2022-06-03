from typing import Optional

from pylox.exceptions import ExceptionList, SyntacticalError
from pylox.expr import (
    AssignExpr,
    BaseExpr,
    BinaryExpr,
    GroupingExpr,
    LiteralExpr,
    LogicalExpr,
    UnaryExpr,
    VariableExpr,
)
from pylox.stmt import BaseStmt, BlockStmt, ExpressionStmt, IfStmt, PrintStmt, VarStmt, WhileStmt
from pylox.token import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token], exception_list: ExceptionList):
        self.tokens = tokens
        self.exception_list = exception_list

        self._current = 0

    def parse(self) -> list[BaseStmt]:
        statements: list[BaseStmt] = []
        while self.peek().token_type is not TokenType.EOF:
            statements.append(self.declaration())

        return statements

    def peek(self, n: int = 0) -> Optional[Token]:
        if (idx := self._current + n) >= 0 and idx < len(self.tokens):
            return self.tokens[idx]
        return None

    def consume(self) -> Token:
        self._current += 1
        return self.peek(-1)

    def declaration(self) -> BaseStmt:
        try:
            if (token := self.consume()).token_type is TokenType.VAR:
                return self.var_declaration(self.consume())
            else:
                return self.statement(token)
        except SyntacticalError as e:
            self.exception_list.append(e)
            self.synchronize()

    def var_declaration(self, name_token: Token) -> BaseStmt:
        if name_token.token_type is not TokenType.IDENTIFIER:
            raise SyntacticalError(name_token, "Expected variable name.")

        initializer = None
        if self.peek().token_type is TokenType.EQUAL:
            self._current += 1  # consume '='
            initializer = self.expression(self.consume())

        if (next_token := self.peek()).token_type is not TokenType.SEMICOLON:
            raise SyntacticalError(next_token, "Expected ';' after variable declaration")
        self._current += 1  # consume ';'
        return VarStmt(name_token, initializer)

    def statement(self, token: Token) -> BaseStmt:
        if token.token_type is TokenType.FOR:
            return self.for_statement()

        if token.token_type is TokenType.IF:
            return self.if_statement()

        if token.token_type is TokenType.PRINT:
            return self.print_statement(self.consume())

        if token.token_type is TokenType.WHILE:
            return self.while_statement()

        if token.token_type is TokenType.LEFT_BRACE:
            return BlockStmt(self.block_statement())

        return self.expression_statement(token)

    def for_statement(self) -> BaseStmt:
        if (token := self.peek()).token_type is not TokenType.LEFT_PAREN:
            raise SyntacticalError(token, "Expected '(' after 'for'.")
        else:
            self._current += 1

        initializer = None
        match (token := self.consume()).token_type:
            case TokenType.SEMICOLON:
                pass
            case TokenType.VAR:
                initializer = self.var_declaration(self.consume())
            case _:
                initializer = self.expression_statement(token)

        condition = None
        if (token := self.consume()).token_type is not TokenType.SEMICOLON:
            condition = self.expression(token)
            if (token := self.peek()).token_type is not TokenType.SEMICOLON:
                raise SyntacticalError(token, "Expected ';' after expression.")
            self._current += 1

        increment = None
        if (token := self.consume()).token_type is not TokenType.RIGHT_PAREN:
            increment = self.expression(token)
            if (token := self.peek()).token_type is not TokenType.RIGHT_PAREN:
                raise SyntacticalError(token, "Expected ')' after expression.")
            self._current += 1

        body = self.statement(self.consume())

        if increment is not None:
            body = BlockStmt([body, increment])

        if condition is None:
            condition = LiteralExpr(True)
        body = WhileStmt(condition, body)

        if initializer is not None:
            body = BlockStmt([initializer, body])

        return body

    def while_statement(self) -> BaseStmt:
        if (token := self.peek()).token_type is not TokenType.LEFT_PAREN:
            raise SyntacticalError(token, "Expected '(' after 'while'.")
        else:
            self._current += 1

        condition = self.expression(self.consume())

        if (token := self.peek()).token_type is not TokenType.RIGHT_PAREN:
            raise SyntacticalError(token, "Expected ')' after condition.")
        else:
            self._current += 1

        body = self.statement(self.consume())

        return WhileStmt(condition, body)

    def if_statement(self) -> BaseStmt:
        if (token := self.peek()).token_type is not TokenType.LEFT_PAREN:
            raise SyntacticalError(token, "Expected '(' after 'if'.")
        self._current += 1  # consume

        condition = self.expression(self.consume())

        if (token := self.peek()).token_type is not TokenType.RIGHT_PAREN:
            raise SyntacticalError(token, "Expected '(' after 'if'.")
        self._current += 1  # consume

        then_branch = self.statement(self.consume())
        else_branch = None
        if (token := self.peek()).token_type is TokenType.ELSE:
            self._current += 1
            else_branch = self.statement(self.consume())

        return IfStmt(condition, then_branch, else_branch)

    def block_statement(self) -> list[BaseStmt]:
        statements = []

        while self.peek().token_type is not TokenType.RIGHT_BRACE:
            statements.append(self.declaration())

        if (token := self.peek()).token_type is not TokenType.RIGHT_BRACE:
            raise SyntacticalError(token, "Expected '}' after block.")

        self._current += 1  # consume '}'
        return statements

    def print_statement(self, token: Token) -> BaseStmt:
        value = self.expression(token)
        if (next_token := self.peek()).token_type is not TokenType.SEMICOLON:
            raise SyntacticalError(next_token, "Expected ';' after value.")
        else:
            self._current += 1  # consume the semicolon
        return PrintStmt(value)

    def expression_statement(self, token: Token) -> BaseStmt:
        value = self.expression(token)
        if (next_token := self.peek()).token_type is not TokenType.SEMICOLON:
            raise SyntacticalError(next_token, "Expected ';' after value.")
        else:
            self._current += 1  # consume the semicolon
        return ExpressionStmt(value)

    def expression(self, token: Token) -> BaseExpr:
        return self.assignment(token)

    def assignment(self, token: Token) -> BaseExpr:
        expr = self.or_(token)

        if (next_token := self.peek()).token_type is TokenType.EQUAL:
            equals = self.consume()
            value = self.assignment(self.consume())

            if isinstance(expr, VariableExpr):
                name = expr.name
                return AssignExpr(name, value)

            raise SyntacticalError(equals, "Invalid assignment target.")

        return expr

    def or_(self, token: Token) -> BaseExpr:
        expr = self.and_(token)

        while (self.peek()).token_type is TokenType.OR:
            operator = self.consume()
            right = self.and_(self.consume())
            expr = LogicalExpr(expr, operator, right)

        return expr

    def and_(self, token: Token) -> BaseExpr:
        expr = self.equality(token)

        while (self.peek()).token_type is TokenType.AND:
            operator = self.consume()
            right = self.equality(self.consume())
            expr = LogicalExpr(expr, operator, right)

        return expr

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
            case TokenType.IDENTIFIER:
                return VariableExpr(token)
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
