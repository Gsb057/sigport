from pathlib import Path

import typer

from sigport import __version__
from sigport.hgnc import load_hgnc
from sigport.resolve import GeneResolver

app = typer.Typer()

# Matches the snapshot frozen by scripts/download_hgnc.sh; see data/snapshots/SNAPSHOT.md.
DEFAULT_SNAPSHOT_DATE = "2026-10-06"


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(False, "--version", help="Show the sigport version and exit."),
) -> None:
    if version:
        typer.echo(f"sigport {__version__}")
        raise typer.Exit()


@app.command()
def resolve(
    symbols: list[str] = typer.Argument(..., help="Gene symbols to resolve."),
    snapshot: str = typer.Option(
        DEFAULT_SNAPSHOT_DATE, "--snapshot", help="HGNC snapshot date (YYYY-MM-DD)."
    ),
) -> None:
    """Resolve gene symbols to HGNC IDs against the frozen snapshot."""
    snapshot_dir = Path("data/snapshots")
    tables = load_hgnc(
        snapshot_dir / f"hgnc_complete_set_{snapshot}.txt",
        snapshot_dir / f"withdrawn_{snapshot}.txt",
    )
    df = GeneResolver(tables).resolve(symbols)
    typer.echo(f"HGNC snapshot: {snapshot}")
    typer.echo(df.to_string(index=False))


if __name__ == "__main__":
    app()
