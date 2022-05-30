from typing import Optional, TextIO

import click

from pylox import Lox


@click.command()
@click.argument("script", type=click.File(), required=False)
def main(script: Optional[TextIO]) -> None:
    Lox.main(script)


if __name__ == "__main__":
    main()
