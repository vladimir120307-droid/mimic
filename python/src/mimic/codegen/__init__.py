from mimic.codegen.base import CodeGenerator, GeneratedFile, Target


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
    raise ValueError(f"Unknown target: {target!r}")


__all__ = ["CodeGenerator", "GeneratedFile", "Target", "get_generator"]
