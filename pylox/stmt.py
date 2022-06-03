from dataclasses import dataclass
from typing import Any

from pylox.expr import BaseExpr
from pylox.token import Token


class BaseStmt:
    def accept(self, visitor: type) -> Any:
        return getattr(visitor, f"visit{self.__class__.__name__}")(self)


@dataclass(slots=True)
class ExpressionStmt(BaseStmt):
    expression: BaseExpr


@dataclass(slots=True)
class PrintStmt(BaseStmt):
    expression: BaseExpr


@dataclass(slots=True)
class VarStmt(BaseStmt):
    name: Token
    initializer: BaseExpr


@dataclass(slots=True)
class BlockStmt(BaseStmt):
    statements: list[BaseStmt]
