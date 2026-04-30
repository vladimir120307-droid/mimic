import numpy as np

from mimic.segmentation import segment


class _FakeFrame:
    def __init__(
        self,
        seed: int,
        cursor: tuple[int, int] = (50, 50),
        down: bool = False,
    ) -> None:
        rng = np.random.default_rng(seed)
        arr = rng.integers(0, 256, size=(32, 32, 4), dtype=np.uint8)
        arr[..., 3] = 255
        self._arr = arr
        self.width = 32
        self.height = 32
        self.cursor_x = cursor[0]
        self.cursor_y = cursor[1]
        self.mouse_down = down

    def as_numpy(self):
        return self._arr


def test_segment_empty_returns_empty():
    seg = segment([])
    assert seg.states == []
    assert seg.transitions == []


def test_segment_groups_similar_frames():
    same = [_FakeFrame(seed=1) for _ in range(5)]
    seg = segment(same)
    assert len(seg.states) == 1
    assert seg.states[0].member_count == 5


def test_segment_separates_distinct_frames():
    frames = [
        *[_FakeFrame(seed=1) for _ in range(3)],
        *[_FakeFrame(seed=42) for _ in range(3)],
        *[_FakeFrame(seed=999) for _ in range(3)],
    ]
    seg = segment(frames)
    assert 2 <= len(seg.states) <= 4
    assert sum(s.member_count for s in seg.states) == len(frames)


def test_segment_caps_max_states():
    frames = [_FakeFrame(seed=i) for i in range(40)]
    seg = segment(frames, max_states=4)
    assert len(seg.states) <= 4


def test_transitions_record_cursor_at_state_boundary():
    a = [_FakeFrame(seed=1, cursor=(100, 200)) for _ in range(2)]
    b = [_FakeFrame(seed=99, cursor=(50, 60)) for _ in range(2)]
    seg = segment(a + b)
    if len(seg.states) >= 2:
        assert seg.transitions
        assert seg.transitions[0].cursor_x == 100
        assert seg.transitions[0].cursor_y == 200
