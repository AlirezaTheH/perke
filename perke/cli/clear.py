import os
from os.path import dirname, join

import rich_click.typer as typer

from perke.cli.base import app


@app.command('clear')
def clear_command() -> None:
    """
    Clears the resources directory from downloaded files.
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
            typer.secho(f'{file_name} removed.', fg='green')
