import math

from pylox.exceptions import ExceptionList, PyloxRuntimeError
from pylox.expr import BaseExpr, BinaryExpr, GroupingExpr, LiteralExpr, UnaryExpr
from pylox.token import Token, TokenType


class Interpreter:
    def __init__(self, exception_list: ExceptionList):
        self.exception_list = exception_list

    def interpret(self, expr: BaseExpr) -> object:
        try:
            value = self.evaluate(expr)
            return value
        except PyloxRuntimeError as e:
            self.exception_list.append(e)

    def visitLiteralExpr(self, expr: LiteralExpr) -> object:
        return expr.value

    def visitGroupingExpr(self, expr: GroupingExpr) -> object:
        return self.evaluate(expr.expression)

    def visitUnaryExpr(self, expr: UnaryExpr) -> object:
        right = self.evaluate(expr.right)

        match expr.operator.token_type:
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, right)
                return -right
            case TokenType.BANG:
                return not self.is_truthy(right)
            case _:
                return None

    def visitBinaryExpr(self, expr: BinaryExpr) -> object:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.token_type in [
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.MINUS,
            TokenType.SLASH,
            TokenType.STAR,
        ]:
            self.check_number_operands(expr.operator, left, right)

        match expr.operator.token_type:
            case TokenType.BANG_EQUAL:
                return left != right
            case TokenType.EQUAL_EQUAL:
                return left == right
            case TokenType.GREATER:
                return left > right
            case TokenType.GREATER_EQUAL:
                return left >= right
            case TokenType.LESS:
                return left < right
            case TokenType.LESS_EQUAL:
                return left <= right
            case TokenType.MINUS:
                return left - right
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    self.check_number_operands(expr.operator, left, right)
                    return left + right
                elif isinstance(left, str) and isinstance(right, str):
                    return left + right
            case TokenType.SLASH:
                # need to handle division by zero
                try:
                    return left / right
                except ZeroDivisionError:
                    return math.inf * left * right
            case TokenType.STAR:
                return left * right
            case _:
                return None

    def evaluate(self, expr: BaseExpr) -> object:
        return expr.accept(self)

    @staticmethod
    def is_truthy(obj: object) -> bool:
        match obj:
            case None:
                return False
            case True | False:
                return obj
            case _:
                return True

    def check_number_operands(self, operator: Token, *operands: list[object]):
        for operand in operands:
            if isinstance(operand, float):
                continue
            raise PyloxRuntimeError(operator, "Operand must be a number.")
