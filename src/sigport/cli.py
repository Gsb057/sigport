import typer

from sigport import __version__

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(False, "--version", help="Show the sigport version and exit."),
) -> None:
    if version:
        typer.echo(f"sigport {__version__}")
        raise typer.Exit()


if __name__ == "__main__":
    app()
