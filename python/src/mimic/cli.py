"""Command-line interface for mimic."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from mimic import __version__
from mimic.codegen.base import Target
from mimic.pipeline import Pipeline
from mimic.vision.base import VisionInput

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except OSError:
        pass

app = typer.Typer(
    name="mimic",
    help="Turn screen recordings and screenshots into working code.",
    no_args_is_help=True,
)
console = Console(legacy_windows=False)


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
        bounds_str = (
            f"{d.bounds[2]}×{d.bounds[3]}"
            if isinstance(d.bounds, tuple)
            else f"{d.bounds.width}×{d.bounds.height}"
        )
        table.add_row(
            str(d.index),
            d.name,
            bounds_str,
            f"{d.dpi_scale:.2f}",
            "✓" if d.is_primary else "",
        )
    console.print(table)


@app.command()
def doctor() -> None:
    """Diagnose your local environment."""
    from mimic.doctor import run_all

    table = Table(title="mimic doctor")
    table.add_column("Check")
    table.add_column("Status", justify="center")
    table.add_column("Detail")
    for r in run_all():
        symbol = {"ok": "[green]✓[/]", "warn": "[yellow]![/]", "fail": "[red]✗[/]"}[
            r.status
        ]
        table.add_row(r.name, symbol, r.detail)
        if r.fix and r.status != "ok":
            table.add_row("", "", f"[dim]→ {r.fix}[/]")
    console.print(table)


@app.command()
def serve(
    host: Annotated[str, typer.Option("--host", "-h", help="Bind host.")] = "127.0.0.1",
    port: Annotated[int, typer.Option("--port", "-p", help="Bind port.")] = 54321,
) -> None:
    """Run the JSON-RPC server the desktop UI talks to."""
    import logging

    from mimic.server import serve as run_server

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    console.print(f"[cyan]mimic server[/] listening on [bold]{host}:{port}[/]")
    console.print("[dim]Press Ctrl+C to stop.[/]")
    run_server(host=host, port=port)


@app.command()
def targets() -> None:
    """List supported output frameworks."""
    table = Table(title="Output targets")
    table.add_column("Target")
    table.add_column("Status")
    from mimic.codegen import list_targets

    status = {
        "flutter": "stable",
        "html":    "stable",
        "react":   "stable",
    }
    for t in list_targets():
        table.add_row(t, status.get(t, "experimental"))
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
