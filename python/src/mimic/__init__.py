"""mimic — turn screen recordings and screenshots into working code."""

from mimic.models import (
    BoundingBox,
    Interaction,
    Screen,
    WidgetNode,
    WidgetTree,
)
from mimic.pipeline import Pipeline, PipelineResult

__version__ = "0.2.0"

__all__ = [
    "BoundingBox",
    "Interaction",
    "Pipeline",
    "PipelineResult",
    "Screen",
    "WidgetNode",
    "WidgetTree",
    "__version__",
]
