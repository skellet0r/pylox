from pylox.expr import BaseExpr, BinaryExpr, GroupingExpr, LiteralExpr, UnaryExpr


class ASTPrinter:
    def print(self, expr: BaseExpr) -> str:
        return expr.accept(self)

    def visitBinaryExpr(self, expr: BinaryExpr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: GroupingExpr) -> str:
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: LiteralExpr) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visitUnaryExpr(self, expr: UnaryExpr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: list[BaseExpr]) -> str:
        return f"({name} {' '.join((expr.accept(self) for expr in exprs))})"
