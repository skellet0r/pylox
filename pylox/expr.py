from dataclasses import dataclass
from typing import Any

from pylox.token import Token


class BaseExpr:
    def accept(self, visitor: type) -> Any:
        return getattr(visitor, f"visit{self.__class__.__name__}")(self)


@dataclass(slots=True)
class BinaryExpr(BaseExpr):
    left: BaseExpr
    operator: Token
    right: BaseExpr


@dataclass(slots=True)
class GroupingExpr(BaseExpr):
    expression: BaseExpr


@dataclass(slots=True)
class LiteralExpr(BaseExpr):
    value: object


@dataclass(slots=True)
class UnaryExpr(BaseExpr):
    operator: Token
    right: BaseExpr
