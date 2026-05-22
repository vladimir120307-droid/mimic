"""End-to-end pipeline: input → WidgetTree → generated code files."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from mimic.codegen import get_generator
from mimic.codegen.base import GeneratedFile, Target
from mimic.models import WidgetTree
from mimic.vision import get_provider
from mimic.vision.base import VisionInput, VisionProvider


@dataclass
class PipelineResult:
    tree: WidgetTree
    files: list[GeneratedFile]
    target: Target
    elapsed_ms: float = 0.0
    warnings: list[str] = field(default_factory=list)

    def write_to(self, out_dir: Path) -> list[Path]:
        out_dir.mkdir(parents=True, exist_ok=True)
        written: list[Path] = []
        for f in self.files:
            path = out_dir / f.path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f.content, encoding="utf-8")
            written.append(path)
        return written


class Pipeline:
    def __init__(
        self,
        provider: VisionProvider | str = "claude",
        target: Target = "flutter",
    ) -> None:
        self.provider = (
            provider if isinstance(provider, VisionProvider) else get_provider(provider)
        )
        self.target = target
        self.generator = get_generator(target)

    async def run(self, source: VisionInput) -> PipelineResult:
        import time

        t0 = time.perf_counter()
        tree = await self.provider.analyze(source)
        files = self.generator.generate(tree)
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        return PipelineResult(
            tree=tree,
            files=files,
            target=self.target,
            elapsed_ms=elapsed_ms,
        )
