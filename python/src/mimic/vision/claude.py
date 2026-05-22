"""Anthropic Claude vision adapter."""

from __future__ import annotations

import json
import os

from mimic.models import WidgetTree
from mimic.vision.base import VisionInput, VisionProvider
from mimic.vision.prompts import SYSTEM_PROMPT, schema_block


class ClaudeVision(VisionProvider):
    name = "claude"

    def __init__(
        self,
        model: str = "claude-opus-4-7",
        api_key: str | None = None,
    ) -> None:
        try:
            from anthropic import AsyncAnthropic
        except ImportError as e:
            raise RuntimeError(
                "The 'anthropic' package is required. Install with `pip install anthropic`."
            ) from e
        self._client = AsyncAnthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self._model = model

    async def analyze(self, source: VisionInput) -> WidgetTree:
        if not source.images_b64:
            raise ValueError("VisionInput must contain at least one image.")

        schema_json = json.dumps(WidgetTree.model_json_schema(), indent=2)
        content: list[dict[str, object]] = [
            {"type": "text", "text": schema_block(schema_json)},
        ]
        for img_b64 in source.images_b64:
            content.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": source.mime_type,
                        "data": img_b64,
                    },
                }
            )

        response = await self._client.messages.create(
            model=self._model,
            max_tokens=8192,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": content}],
        )

        raw = "".join(
            getattr(block, "text", "")
            for block in response.content
            if getattr(block, "type", None) == "text"
        )
        return WidgetTree.model_validate_json(_strip_fences(raw))


def _strip_fences(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw
        if raw.endswith("```"):
            raw = raw.rsplit("```", 1)[0]
    return raw.strip()
