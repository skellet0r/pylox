import click


@click.command()
@click.argument("file", type=click.File(), required=False)
def main(file):
    # entrypoint for the pylox interpreter
    if file is None:
        # interactive interpreter
        while True:
            # run each line
            run(input("> "))
    else:
        # execute entire file
        run(file.read())


def run(source):
    pass
