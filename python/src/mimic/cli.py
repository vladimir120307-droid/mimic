"""Command-line interface for mimic."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from mimic import __version__
from mimic.codegen.base import Target
from mimic.pipeline import Pipeline
from mimic.vision.base import VisionInput

app = typer.Typer(
    name="mimic",
    help="Turn screen recordings and screenshots into working code.",
    no_args_is_help=True,
)
console = Console()


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"mimic [bold cyan]{__version__}[/]")
        raise typer.Exit


@app.callback()
def _root(
    version: Annotated[
        bool,
        typer.Option(
            "--version", callback=_version_callback, is_eager=True, help="Show version and exit."
        ),
    ] = False,
) -> None:
    pass


@app.command()
def gen(
    image: Annotated[Path, typer.Argument(exists=True, readable=True, help="Input image file.")],
    target: Annotated[
        Target, typer.Option("--target", "-t", help="Output framework.")
    ] = "flutter",
    provider: Annotated[
        str, typer.Option("--provider", "-p", help="Vision provider: claude / openai / local.")
    ] = "claude",
    out: Annotated[
        Path, typer.Option("--out", "-o", help="Output directory.")
    ] = Path("out"),
) -> None:
    """Generate code from a single screenshot."""
    pipeline = Pipeline(provider=provider, target=target)
    result = asyncio.run(pipeline.run(VisionInput.from_image(image)))
    paths = result.write_to(out)
    _print_result_table(target, result.elapsed_ms, paths)


@app.command()
def record(
    duration: Annotated[
        int, typer.Option("--duration", "-d", help="Recording duration, seconds.")
    ] = 15,
    target: Annotated[
        Target, typer.Option("--target", "-t", help="Output framework.")
    ] = "flutter",
    provider: Annotated[
        str, typer.Option("--provider", "-p", help="Vision provider.")
    ] = "claude",
    out: Annotated[
        Path, typer.Option("--out", "-o", help="Output directory.")
    ] = Path("out"),
) -> None:
    """Record the screen, then generate code from the recording."""
    from mimic.capture import record_screen

    console.print(f"[cyan]Recording for {duration}s…[/]")
    frames = record_screen(duration_s=duration)
    console.print(f"[green]Captured {len(frames)} unique frames after dedup.[/]")

    pipeline = Pipeline(provider=provider, target=target)
    result = asyncio.run(pipeline.run(VisionInput.from_frames(frames)))
    paths = result.write_to(out)
    _print_result_table(target, result.elapsed_ms, paths)


@app.command()
def ui() -> None:
    """Launch the Flutter desktop UI."""
    console.print(
        "[yellow]The desktop UI is not bundled with the Python package yet.[/]\n"
        "Download the latest installer from "
        "[link=https://github.com/Cyber-Lord/mimic/releases]Releases[/link], "
        "or run [cyan]flutter run[/] inside the [bold]ui/[/] folder."
    )


@app.command()
def displays() -> None:
    """List available displays."""
    from mimic.capture import list_displays

    table = Table(title="Displays")
    table.add_column("#", justify="right")
    table.add_column("Name")
    table.add_column("Bounds")
    table.add_column("DPI scale", justify="right")
    table.add_column("Primary", justify="center")
    for d in list_displays():
        table.add_row(
            str(d.index),
            d.name,
            f"{d.bounds.width}×{d.bounds.height}",
            f"{d.dpi_scale:.2f}",
            "✓" if d.is_primary else "",
        )
    console.print(table)


def _print_result_table(target: Target, elapsed_ms: float, paths: list[Path]) -> None:
    table = Table(title=f"Generated {target}")
    table.add_column("File")
    table.add_column("Size", justify="right")
    for p in paths:
        size = p.stat().st_size if p.exists() else 0
        table.add_row(str(p), f"{size} B")
    console.print(table)
    console.print(f"[green]Done in {elapsed_ms:.0f} ms[/]")


if __name__ == "__main__":
    app()
