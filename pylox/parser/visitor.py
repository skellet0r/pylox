from pylox.parser import expr


class ASTPrinter:
    def print(self, expr: expr.BaseExpr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr: expr.BinaryExpr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: expr.GroupingExpr) -> str:
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: expr.LiteralExpr) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visitUnaryExpr(self, expr: expr.UnaryExpr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: list[expr.BaseExpr]) -> str:
        return f"({name} {' '.join((expr.accept(self) for expr in exprs))})"
