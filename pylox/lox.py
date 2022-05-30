from typing import Optional, TextIO


class Lox:
    """Lox interpreter"""

    def run_prompt(self):
        """Run the pylox interactive prompt."""
        while True:
            self.run(input("> "))

    def run_script(self, script: TextIO):
        """Run a script file."""
        self.run(script.read())

    def run(self, source: str):
        pass

    @classmethod
    def main(cls, script: Optional[TextIO]):
        """Run either the interactive prompt or a file."""
        if script is None:
            cls().run_prompt()
        else:
            cls().run_script(script)
