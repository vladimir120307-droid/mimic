"""Code generator interface.

A generator is a pure function: `WidgetTree → list[GeneratedFile]`. Same input
always produces same output. No filesystem or network access happens inside a
generator — only when its caller writes the result.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol

from mimic.models import WidgetTree

Target = Literal["flutter", "html", "react"]


@dataclass
class GeneratedFile:
    path: str
    content: str
    language: str = "plaintext"


class CodeGenerator(Protocol):
    target: Target

    def generate(self, tree: WidgetTree) -> list[GeneratedFile]:
        ...
