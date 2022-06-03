from typing import Optional, TextIO

import click

from pylox.exceptions import ExceptionList
from pylox.interpreter import Interpreter
from pylox.lexer import Lexer
from pylox.parser import Parser


class Lox:
    """Lox interpreter"""

    def __init__(self):
        self.exception_list = ExceptionList([])
        self.interpreter = Interpreter(self.exception_list)

    def run_prompt(self):
        """Run the pylox interactive prompt."""
        while True:
            self.run(input("> "))
            for exc in self.exception_list:
                click.echo(exc)
            self.exception_list.clear()

    def run_script(self, script: TextIO):
        """Run a script file."""
        self.run(script.read())
        self.exception_list.raise_if_not_empty()

    def run(self, source: str):
        lexer = Lexer(source, self.exception_list)
        tokens = lexer.scan()

        parser = Parser(tokens, self.exception_list)
        stmts = [stmt for stmt in parser.parse() if stmt is not None]

        self.interpreter.interpret(stmts)

    @classmethod
    def main(cls, script: Optional[TextIO]):
        """Run either the interactive prompt or a file."""
        if script is None:
            cls().run_prompt()
        else:
            cls().run_script(script)
