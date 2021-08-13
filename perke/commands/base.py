import typer

app = typer.Typer(name='perke')


def setup_commands() -> None:
    """
    Setup all commands for perke.
    """
    app()
