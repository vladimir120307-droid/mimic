"""Pure-Python screen capture via `mss`.

Used when the native C++ module is not built. Slower, but works everywhere
Python runs.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


@dataclass
class _FallbackDisplay:
    index: int
    name: str
    bounds: Any
    dpi_scale: float
    is_primary: bool


def fallback_list_displays() -> list[Any]:
    try:
        import mss
    except ImportError:
        return []
    with mss.mss() as sct:
        out = []
        for i, mon in enumerate(sct.monitors[1:], start=0):
            out.append(
                _FallbackDisplay(
                    index=i,
                    name=f"display-{i}",
                    bounds=(mon["left"], mon["top"], mon["width"], mon["height"]),
                    dpi_scale=1.0,
                    is_primary=(i == 0),
                )
            )
        return out


def fallback_record(duration_s: int, target_fps: int) -> list[Any]:
    """Record using mss + lightweight perceptual-hash dedup in Python."""
    import mss
    import numpy as np

    interval = 1.0 / max(1, target_fps)
    end_at = time.monotonic() + duration_s
    last_hash: int | None = None
    threshold_bits = 64 * 0.02
    captured: list[Any] = []

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        while time.monotonic() < end_at:
            shot = sct.grab(monitor)
            arr = np.array(shot)
            h = _dhash(arr)
            if last_hash is None or _popcount(last_hash ^ h) >= threshold_bits:
                captured.append(_FallbackFrame(arr))
                last_hash = h
            time.sleep(interval)
    return captured


class _FallbackFrame:
    __slots__ = ("_arr",)

    def __init__(self, arr: Any) -> None:
        self._arr = arr

    def as_numpy(self) -> Any:
        return self._arr


def _dhash(arr: Any, size: int = 8) -> int:
    import numpy as np
    from PIL import Image

    img = Image.fromarray(arr[..., :3]).convert("L").resize((size + 1, size), Image.LANCZOS)
    pixels = np.asarray(img)
    diff = pixels[:, 1:] > pixels[:, :-1]
    h = 0
    for v in diff.flatten():
        h = (h << 1) | int(v)
    return h


def _popcount(x: int) -> int:
    return bin(x).count("1")
