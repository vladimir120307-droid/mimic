from mimic.codegen.base import CodeGenerator, GeneratedFile, Target

_TARGETS = ("flutter", "html", "react")


def get_generator(target: Target) -> CodeGenerator:
    if target == "flutter":
        from mimic.codegen.flutter import FlutterGenerator
        return FlutterGenerator()
    if target == "html":
        from mimic.codegen.html import HtmlGenerator
        return HtmlGenerator()
    if target == "react":
        from mimic.codegen.react import ReactGenerator
        return ReactGenerator()
    raise ValueError(f"Unknown target: {target!r}. Supported: {_TARGETS}")


def list_targets() -> tuple[str, ...]:
    return _TARGETS


__all__ = ["CodeGenerator", "GeneratedFile", "Target", "get_generator", "list_targets"]
