"""Snapshot tests: ensure generated outputs are deterministic.

For each (fixture, target) pair, run the pipeline and compare against the
files checked into `examples/<fixture>/generated/<target>/`. Differences
indicate either a regression OR an intentional change that needs the
gallery refreshed.

Refresh with:

    cd python && MIMIC_UPDATE_SNAPSHOTS=1 pytest tests/test_snapshots.py
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import pytest

from mimic.pipeline import Pipeline
from mimic.vision.base import VisionInput
from mimic.vision.mock import list_fixtures

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = REPO_ROOT / "examples"
TARGETS = ("flutter", "html", "react", "react-ts")
UPDATE_ENV = "MIMIC_UPDATE_SNAPSHOTS"


def _run(fixture: str, target: str) -> dict[str, str]:
    pipeline = Pipeline(provider=f"mock:{fixture}", target=target)
    result = asyncio.run(pipeline.run(VisionInput(images_b64=["dummy"])))
    return {f.path: f.content for f in result.files}


def _load_snapshot(fixture: str, target: str) -> dict[str, str] | None:
    base = EXAMPLES / fixture / "generated" / target
    if not base.exists():
        return None
    out: dict[str, str] = {}
    for path in base.rglob("*"):
        if path.is_file():
            rel = path.relative_to(base).as_posix()
            out[rel] = path.read_text(encoding="utf-8")
    return out


def _write_snapshot(fixture: str, target: str, files: dict[str, str]) -> None:
    base = EXAMPLES / fixture / "generated" / target
    import shutil

    if base.exists():
        shutil.rmtree(base)
    for rel, content in files.items():
        path = base / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


@pytest.mark.parametrize("fixture", list_fixtures())
@pytest.mark.parametrize("target", TARGETS)
def test_snapshot_matches_examples(fixture: str, target: str) -> None:
    current = _run(fixture, target)
    if os.environ.get(UPDATE_ENV):
        _write_snapshot(fixture, target, current)
        return

    snapshot = _load_snapshot(fixture, target)
    if snapshot is None:
        pytest.skip(f"No snapshot for {fixture}/{target}. Set {UPDATE_ENV}=1 to generate it.")

    extra_in_current = set(current) - set(snapshot)
    missing_from_curr = set(snapshot) - set(current)
    assert not extra_in_current, (
        f"Generator added files not in snapshot for {fixture}/{target}: {sorted(extra_in_current)}"
    )
    assert not missing_from_curr, (
        f"Generator removed files present in snapshot for {fixture}/{target}: {sorted(missing_from_curr)}"
    )

    for rel in sorted(current):
        actual = current[rel].replace("\r\n", "\n")
        expected = snapshot[rel].replace("\r\n", "\n")
        assert actual == expected, (
            f"Output drift in {fixture}/{target}/{rel}. Refresh with {UPDATE_ENV}=1 pytest"
        )
