import os
from os.path import dirname, join

import typer

from perke.cli.base import app


@app.command('clear')
def clear_command() -> None:
    """
    Clears the resources directory.
    """
    clear()


def clear() -> None:
    """
    Function version of `clear_command` to be available in the package.
    """
    resources_path = join(dirname(dirname(__file__)), 'resources')
    for file_name in os.listdir(resources_path):
        if file_name != 'README.md':
            file_path = join(resources_path, file_name)
            os.remove(file_path)
            typer.echo(f'{file_name} removed.')
