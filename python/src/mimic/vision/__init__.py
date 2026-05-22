from mimic.vision.base import VisionInput, VisionProvider


def get_provider(name: str) -> VisionProvider:
    name = name.lower()
    if name == "claude":
        from mimic.vision.claude import ClaudeVision
        return ClaudeVision()
    if name == "openai":
        from mimic.vision.openai import OpenAIVision
        return OpenAIVision()
    if name == "local":
        from mimic.vision.local import LocalVision
        return LocalVision()
    if name.startswith("mock"):
        from mimic.vision.mock import MockVision
        fixture = name.split(":", 1)[1] if ":" in name else "dashboard"
        return MockVision(fixture=fixture)
    raise ValueError(f"Unknown vision provider: {name!r}")


__all__ = ["VisionInput", "VisionProvider", "get_provider"]
