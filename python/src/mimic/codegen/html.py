"""HTML + Tailwind code generator. Coming in v0.2."""

from __future__ import annotations

from mimic.codegen.base import GeneratedFile, Target
from mimic.models import WidgetTree


class HtmlGenerator:
    target: Target = "html"

    def generate(self, tree: WidgetTree) -> list[GeneratedFile]:
        raise NotImplementedError("HTML + Tailwind target is planned for v0.2.")
