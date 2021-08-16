import typer
from typer.main import get_command

app = typer.Typer(name='perke')


def setup_cli() -> None:
    """
    Setup command-line interface for perke.
    """
    # Ensure that the help messages always display the correct prompt
    command = get_command(app)
    command(prog_name='python -m perke')
