"""OpenAI GPT-4 Vision adapter."""

from __future__ import annotations

import json
import os

from mimic.models import WidgetTree
from mimic.vision.base import VisionInput, VisionProvider
from mimic.vision.prompts import SYSTEM_PROMPT, schema_block


class OpenAIVision(VisionProvider):
    name = "openai"

    def __init__(self, model: str = "gpt-4o", api_key: str | None = None) -> None:
        try:
            from openai import AsyncOpenAI
        except ImportError as e:
            raise RuntimeError(
                "The 'openai' package is required. Install with `pip install openai`."
            ) from e
        self._client = AsyncOpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
        self._model = model

    async def analyze(self, source: VisionInput) -> WidgetTree:
        if not source.images_b64:
            raise ValueError("VisionInput must contain at least one image.")

        schema_json = json.dumps(WidgetTree.model_json_schema(), indent=2)
        user_content: list[dict[str, object]] = [
            {"type": "text", "text": schema_block(schema_json)},
        ]
        for img_b64 in source.images_b64:
            user_content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{source.mime_type};base64,{img_b64}",
                    },
                }
            )

        response = await self._client.chat.completions.create(
            model=self._model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            max_tokens=8192,
        )
        raw = response.choices[0].message.content or "{}"
        return WidgetTree.model_validate_json(raw)
