"""Local vision adapter (Florence-2 / Llava via transformers).

Stub for v0.4. Will run fully offline on user's machine.
"""

from __future__ import annotations

from mimic.models import WidgetTree
from mimic.vision.base import VisionInput, VisionProvider


class LocalVision(VisionProvider):
    name = "local"

    def __init__(self, model: str = "microsoft/Florence-2-base") -> None:
        self._model_name = model

    async def analyze(self, source: VisionInput) -> WidgetTree:
        raise NotImplementedError(
            "Local vision is planned for v0.4. "
            "Track progress at https://github.com/vladimir120307-droid/mimic/issues."
        )
