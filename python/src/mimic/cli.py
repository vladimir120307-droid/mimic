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
    dry_run: Annotated[
        bool, typer.Option("--dry-run", help="Show what would be generated without writing files.")
    ] = False,
    output_format: Annotated[
        str,
        typer.Option(
            "--format",
            help="Result format: 'table' (default), 'json' for machine-readable output.",
        ),
    ] = "table",
) -> None:
    """Generate code from a single screenshot."""
    pipeline = Pipeline(provider=provider, target=target)
    result = asyncio.run(pipeline.run(VisionInput.from_image(image)))

    if output_format == "json":
        import json as _json

        payload = {
            "target":     target,
            "elapsed_ms": result.elapsed_ms,
            "dry_run":    dry_run,
            "files": [
                {"path": f.path, "size": len(f.content.encode("utf-8")), "language": f.language}
                for f in result.files
            ],
        }
        if not dry_run:
            paths = result.write_to(out)
            payload["written_to"] = str(out)
            payload["paths"] = [str(p) for p in paths]
        print(_json.dumps(payload, indent=2))
        return

    if dry_run:
        table = Table(title=f"Would generate ({target}) — dry run, no files written")
        table.add_column("File")
        table.add_column("Size", justify="right")
        for f in result.files:
            table.add_row(f.path, f"{len(f.content.encode('utf-8'))} B")
        console.print(table)
        console.print(f"[yellow]dry run[/]: {len(result.files)} files would be written to {out}")
        return

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
        "flutter":  "stable",
        "html":     "stable",
        "react":    "stable",
        "react-ts": "stable",
    }
    for t in list_targets():
        table.add_row(t, status.get(t, "experimental"))
    console.print(table)


@app.command()
def init(
    name: Annotated[
        str, typer.Argument(help="Project folder name, created in the current directory.")
    ],
    fixture: Annotated[
        str,
        typer.Option(
            "--fixture",
            help="Mock fixture to seed the project from: login / dashboard / chat / calendar / ecommerce / settings.",
        ),
    ] = "dashboard",
    target: Annotated[
        Target, typer.Option("--target", "-t", help="Initial target framework.")
    ] = "flutter",
) -> None:
    """Scaffold a new project directory pre-seeded with a generated example."""
    project = Path.cwd() / name
    if project.exists() and any(project.iterdir()):
        console.print(f"[red]error[/]: {project} already exists and is not empty")
        raise typer.Exit(code=1)
    project.mkdir(parents=True, exist_ok=True)

    dummy = project / "_seed.png"
    try:
        from PIL import Image

        Image.new("RGB", (375, 812), "#F8FAFC").save(dummy)
    except Exception:
        dummy.write_bytes(b"\x89PNG\r\n\x1a\n")

    pipeline = Pipeline(provider=f"mock:{fixture}", target=target)
    result = asyncio.run(pipeline.run(VisionInput.from_image(dummy)))
    result.write_to(project)
    dummy.unlink(missing_ok=True)

    console.print(
        f"[green]✓[/] Scaffolded [bold]{name}[/] from [cyan]mock:{fixture}[/] → "
        f"[cyan]{target}[/] ({len(result.files)} files in {result.elapsed_ms:.0f} ms)"
    )
    console.print(f"  cd {name}")
    if target == "flutter":
        console.print("  flutter run")
    elif target == "html":
        console.print("  open index.html  # or xdg-open / start")
    elif target in {"react", "react-ts"}:
        console.print("  npm install && npm run dev")


@app.command()
def bench(
    target: Annotated[
        Target, typer.Option("--target", "-t", help="Target to benchmark.")
    ] = "flutter",
    iterations: Annotated[
        int, typer.Option("--iterations", "-n", help="Number of runs per fixture.")
    ] = 5,
) -> None:
    """Benchmark the codegen pipeline across all mock fixtures."""
    import time

    from mimic.vision.mock import list_fixtures

    table = Table(title=f"mimic bench — {target}, {iterations} iterations")
    table.add_column("Fixture")
    table.add_column("Files",      justify="right")
    table.add_column("Min (ms)",   justify="right")
    table.add_column("Median (ms)",justify="right")
    table.add_column("Max (ms)",   justify="right")

    for fix in list_fixtures():
        pipeline = Pipeline(provider=f"mock:{fix}", target=target)
        timings: list[float] = []
        files_count = 0
        for _ in range(iterations):
            t0 = time.perf_counter()
            result = asyncio.run(pipeline.run(VisionInput(images_b64=["dummy"])))
            timings.append((time.perf_counter() - t0) * 1000.0)
            files_count = len(result.files)
        timings.sort()
        median = timings[len(timings) // 2]
        table.add_row(
            fix,
            str(files_count),
            f"{timings[0]:.2f}",
            f"{median:.2f}",
            f"{timings[-1]:.2f}",
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
