import sys

import click

from pylox.scanner import Scanner

HAD_ERROR = False  # noqa: F841


@click.command()
@click.argument("file", type=click.File(), required=False)
def main(file: click.File):
    # entrypoint for the pylox interpreter
    if file is None:
        # interactive interpreter
        while True:
            # header message
            click.echo("Pylox 0.1.0 Interactive Prompt")
            # run each line
            run(input("> "))
    else:
        # execute entire file
        run(file.read())
        if HAD_ERROR:
            # exit with a non-zero exit code
            sys.exit(65)


def run(source: str):
    # scan the source code
    scanner = Scanner(source)
    # collect all the tokens in a list
    tokens = scanner.scan_tokens()

    # print tokens to the console
    for token in tokens:
        click.echo(token)


def error(line: int, message: str):
    # error utility function
    report(line, "", message)


def report(line: int, where: str, message: str):
    # report error to stderr
    click.echo(f"[line {line}] Error {where}: {message}", err=True)
    HAD_ERROR = True
