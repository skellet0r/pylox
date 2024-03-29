from collections import UserList

from pylox.token import Token, TokenType


class ExceptionList(UserList):
    def __init__(self, data):
        self.data = data

    def raise_if_not_empty(self):
        match len(self.data):
            case 0:
                return
            case 1:
                raise self.data.pop()
            case _:
                error_msg = ["Multiple exceptions occurred."]
                error_msg += [f"{type(exc).__name__}: {exc}" for exc in self.data[::-1]]
                raise PyloxException("\n".join(error_msg))


class PyloxException(Exception):
    """Base Pylox exception class"""

    def __init__(self, msg: str):
        self.msg = msg


class LexicalError(PyloxException):
    def __init__(self, lineno: int, where: str, message: str):
        self.lineno = lineno
        self.where = where
        self.message = message

    def __str__(self) -> str:
        return f"[Line {self.lineno}] Error{self.where}: {self.message}"


class SyntacticalError(PyloxException):
    def __init__(self, token: Token, msg: str):
        self.token = token
        self.msg = msg

    def __str__(self) -> str:
        if self.token.token_type is TokenType.EOF:
            return f"[Line {self.token.lineno}] Error at end: {self.msg}"
        return f"[Line {self.token.lineno}] Error at '{self.token.lexeme}': {self.msg}"


class PyloxRuntimeError(PyloxException):
    def __init__(self, token: Token, msg: str):
        self.token = token
        self.msg = msg
