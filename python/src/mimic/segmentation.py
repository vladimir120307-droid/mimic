"""Multi-frame segmentation: cluster frames into distinct UI states.

The native dedup layer drops frames that are *visually identical* to the last
one. This module does the next step: groups the remaining frames into stable
*states* — periods during which the user wasn't transitioning between
screens — and infers interactions at state boundaries.

Output is a `Segmentation` with N representative frames (one per state) and
M-1 inferred interactions (one per state-to-state transition).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


class FrameLike(Protocol):
    """Minimal duck-type interface for a frame from either the native or fallback path."""

    width: int
    height: int
    cursor_x: int
    cursor_y: int
    mouse_down: bool

    def as_numpy(self) -> Any: ...


@dataclass
class FrameState:
    """A cluster of consecutive similar frames — one UI state."""

    representative: Any
    member_count: int = 1
    first_index: int = 0
    last_index: int = 0
    mouse_clicks_at_exit: list[tuple[int, int]] = field(default_factory=list)


@dataclass
class InferredInteraction:
    """Cursor information observed when transitioning out of one state."""

    from_state_index: int
    to_state_index: int
    cursor_x: int
    cursor_y: int


@dataclass
class Segmentation:
    states: list[FrameState]
    transitions: list[InferredInteraction]

    @property
    def representatives(self) -> list[Any]:
        return [s.representative for s in self.states]


def _dhash(frame: FrameLike, size: int = 8) -> int:
    """Compute a perceptual difference-hash.

    Reuses the native implementation when the frame originated from the C++
    capturer (passes type check); falls back to a pure-Python implementation
    for any other frame-like object (mss fallback, test fixtures).
    """
    try:
        import _mimic_capture  # type: ignore[import-not-found]

        return _mimic_capture.dhash(frame, size)
    except (ImportError, TypeError):
        pass
    import numpy as np
    from PIL import Image

    arr = frame.as_numpy()
    img = Image.fromarray(arr[..., :3]).convert("L").resize((size + 1, size), Image.LANCZOS)
    pixels = np.asarray(img)
    diff = pixels[:, 1:] > pixels[:, :-1]
    h = 0
    for v in diff.flatten():
        h = (h << 1) | int(v)
    return h


def _hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


def segment(
    frames: list[FrameLike],
    *,
    state_change_threshold: float = 0.08,
    max_states: int = 8,
) -> Segmentation:
    """Cluster a sequence of frames into ~`max_states` distinct UI states.

    A frame opens a new state when its dhash differs from the current state's
    representative by more than `state_change_threshold` (fraction of 64 bits).
    The representative of each state is its FIRST frame (chronologically),
    which tends to be the most-stable instant before subsequent micro-jitter.
    """
    if not frames:
        return Segmentation(states=[], transitions=[])

    hashes = [_dhash(f) for f in frames]
    threshold_bits = 64 * max(0.01, state_change_threshold)

    states: list[FrameState] = [FrameState(representative=frames[0], first_index=0)]
    rep_hashes: list[int] = [hashes[0]]

    for i in range(1, len(frames)):
        cur_rep_hash = rep_hashes[-1]
        if _hamming(cur_rep_hash, hashes[i]) > threshold_bits:
            states.append(FrameState(representative=frames[i], first_index=i, last_index=i))
            rep_hashes.append(hashes[i])
        else:
            states[-1].member_count += 1
            states[-1].last_index = i

    if len(states) > max_states:
        states = _merge_smallest(states, rep_hashes, max_states)

    transitions = _infer_transitions(frames, states)
    return Segmentation(states=states, transitions=transitions)


def _merge_smallest(states: list[FrameState], hashes: list[int], target: int) -> list[FrameState]:
    while len(states) > target:
        smallest_i = min(range(len(states)), key=lambda i: states[i].member_count)
        candidates = [j for j in (smallest_i - 1, smallest_i + 1) if 0 <= j < len(states)]
        if not candidates:
            states.pop(smallest_i)
            hashes.pop(smallest_i)
            continue
        neighbor_i = min(candidates, key=lambda j: _hamming(hashes[j], hashes[smallest_i]))
        states[neighbor_i].member_count += states[smallest_i].member_count
        states[neighbor_i].last_index = max(
            states[neighbor_i].last_index, states[smallest_i].last_index
        )
        states.pop(smallest_i)
        hashes.pop(smallest_i)
    return states


def _infer_transitions(
    frames: list[FrameLike], states: list[FrameState]
) -> list[InferredInteraction]:
    out: list[InferredInteraction] = []
    for i in range(len(states) - 1):
        boundary_idx = states[i].last_index
        boundary = frames[boundary_idx]
        if boundary.cursor_x >= 0 and boundary.cursor_y >= 0:
            out.append(
                InferredInteraction(
                    from_state_index=i,
                    to_state_index=i + 1,
                    cursor_x=int(boundary.cursor_x),
                    cursor_y=int(boundary.cursor_y),
                )
            )
    return out
