from mimic import __version__
from mimic.codegen import get_generator
from mimic.vision import get_provider


def test_version_is_string():
    assert isinstance(__version__, str)
    assert len(__version__) > 0


def test_generator_registry():
    assert get_generator("flutter").target == "flutter"


def test_vision_registry_unknown_raises():
    import pytest

    with pytest.raises(ValueError):
        get_provider("does-not-exist")
