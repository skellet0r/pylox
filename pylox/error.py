import click

HAD_ERROR = False  # noqa: F841


def report(line: int, where: str, message: str):
    # report error to stderr
    click.echo(f"[line {line}] Error {where}: {message}", err=True)
    HAD_ERROR = True


def error(line: int, message: str):
    # error utility function
    report(line, "", message)
