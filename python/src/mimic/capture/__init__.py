"""Screen capture facade.

Tries the native C++ capturer first; falls back to pure-Python `mss` when the
native module is unavailable (development without a built C++ core).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mimic.capture.fallback import fallback_list_displays, fallback_record


@dataclass
class DisplayInfo:
    index: int
    name: str
    bounds: tuple[int, int, int, int]
    dpi_scale: float
    is_primary: bool


def _try_native() -> Any | None:
    try:
        import _mimic_capture

        return _mimic_capture
    except ImportError:
        return None


def list_displays() -> list[DisplayInfo]:
    native = _try_native()
    if native is None:
        return fallback_list_displays()
    return [
        DisplayInfo(
            index=d.index,
            name=d.name,
            bounds=(d.bounds.x, d.bounds.y, d.bounds.width, d.bounds.height),
            dpi_scale=d.dpi_scale,
            is_primary=d.is_primary,
        )
        for d in native.list_displays()
    ]


def record_screen(duration_s: int, target_fps: int = 30) -> list[Any]:
    """Record the primary display for `duration_s` seconds and return deduped frames."""
    native = _try_native()
    if native is None:
        return fallback_record(duration_s=duration_s, target_fps=target_fps)

    cfg = native.CaptureConfig()
    cfg.target_fps = target_fps
    cfg.include_cursor = True
    cfg.enable_dedup = True
    cfg.dedup_threshold = 0.02

    cap = native.make_capturer()
    frames: list[Any] = []

    def _on_frame(f: Any) -> None:
        frames.append(f)

    cap.start(cfg, _on_frame)
    import time

    time.sleep(duration_s)
    cap.stop()
    return frames
