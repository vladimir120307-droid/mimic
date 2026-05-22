"""Common interface for vision providers.

Every backend (Claude, OpenAI, local) takes a `VisionInput` and returns a
`WidgetTree`. Backends never produce framework code — that is the codegen
layer's responsibility.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from mimic.models import WidgetTree


@dataclass
class VisionInput:
    """Source material handed to a vision provider."""

    images_b64: list[str] = field(default_factory=list)
    mime_type: str = "image/png"

    @classmethod
    def from_image(cls, path: Path) -> VisionInput:
        data = path.read_bytes()
        mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
        return cls(images_b64=[base64.b64encode(data).decode("ascii")], mime_type=mime)

    @classmethod
    def from_frames(cls, frames: list[Any]) -> VisionInput:
        """Encode pre-captured frames as PNG and return them as a VisionInput.

        Accepts anything that has an `.as_numpy()` method returning (H, W, 4)
        uint8 — which covers `_mimic_capture.Frame` and the pure-Python
        fallback alike.
        """
        from io import BytesIO

        from PIL import Image

        out: list[str] = []
        for f in frames:
            arr = f.as_numpy() if hasattr(f, "as_numpy") else f
            img = Image.fromarray(arr[..., :3][..., ::-1])  # BGRA → RGB
            buf = BytesIO()
            img.save(buf, format="PNG", optimize=True)
            out.append(base64.b64encode(buf.getvalue()).decode("ascii"))
        return cls(images_b64=out, mime_type="image/png")


class VisionProvider(Protocol):
    name: str

    async def analyze(self, source: VisionInput) -> WidgetTree:
        ...
