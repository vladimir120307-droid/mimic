import asyncio
from pathlib import Path

import pytest

from mimic.codegen import list_targets
from mimic.pipeline import Pipeline
from mimic.vision.base import VisionInput
from mimic.vision.mock import MockVision, list_fixtures


def test_mock_lists_known_fixtures():
    fixtures = list_fixtures()
    assert "login" in fixtures
    assert "dashboard" in fixtures


def test_mock_unknown_fixture_raises():
    with pytest.raises(ValueError):
        MockVision(fixture="nope")


def test_mock_returns_valid_widget_tree(tmp_path: Path):
    img = tmp_path / "x.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n")  # not actually a real image — mock ignores

    async def go():
        provider = MockVision("dashboard")
        tree = await provider.analyze(VisionInput.from_image(img))
        assert len(tree.screens) == 2
        assert tree.initial_screen.name == "Home"
        assert tree.interactions, "dashboard mock should have at least one interaction"

    asyncio.run(go())


@pytest.mark.parametrize("target", list_targets())
def test_mock_pipeline_generates_files_for_each_target(target, tmp_path: Path):
    img = tmp_path / "x.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n")

    pipeline = Pipeline(provider="mock:dashboard", target=target)
    result = asyncio.run(pipeline.run(VisionInput.from_image(img)))
    assert result.files, f"target {target!r} produced no files"
    written = result.write_to(tmp_path / "out")
    for path in written:
        assert path.exists()
        assert path.stat().st_size > 0
