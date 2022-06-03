from typing import Optional

from pylox.exceptions import PyloxRuntimeError
from pylox.token import Token


class Environment:
    def __init__(self, enclosing: Optional[dict] = None):
        self.enclosing = enclosing
        self.values = {}

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise PyloxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def define(self, name: str, value: object):
        self.values[name] = value

    def get(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise PyloxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
