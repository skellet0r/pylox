from typing import Optional, TextIO

import click

from pylox.exceptions import ExceptionList
from pylox.lexer import Lexer


class Lox:
    """Lox interpreter"""

    def __init__(self):
        self.exception_list = ExceptionList([])

    def run_prompt(self):
        """Run the pylox interactive prompt."""
        while True:
            self.run(input("> "))

    def run_script(self, script: TextIO):
        """Run a script file."""
        self.run(script.read())
        self.exception_list.raise_if_not_empty()

    def run(self, source: str):
        lexer = Lexer(source)
        tokens = lexer.scan()

        for token in tokens:
            click.echo(token)

    @classmethod
    def main(cls, script: Optional[TextIO]):
        """Run either the interactive prompt or a file."""
        if script is None:
            cls().run_prompt()
        else:
            cls().run_script(script)
