from mimic.codegen.base import CodeGenerator, GeneratedFile, Target

_TARGETS = ("flutter", "html", "react", "react-ts", "vue", "swiftui")


def get_generator(target: Target) -> CodeGenerator:
    if target == "flutter":
        from mimic.codegen.flutter import FlutterGenerator

        return FlutterGenerator()
    if target == "html":
        from mimic.codegen.html import HtmlGenerator

        return HtmlGenerator()
    if target == "react":
        from mimic.codegen.react import ReactGenerator

        return ReactGenerator(typescript=False)
    if target == "react-ts":
        from mimic.codegen.react import ReactGenerator

        return ReactGenerator(typescript=True)
    if target == "vue":
        from mimic.codegen.vue import VueGenerator

        return VueGenerator()
    if target == "swiftui":
        from mimic.codegen.swiftui import SwiftUIGenerator

        return SwiftUIGenerator()
    raise ValueError(f"Unknown target: {target!r}. Supported: {_TARGETS}")


def list_targets() -> tuple[str, ...]:
    return _TARGETS


__all__ = ["CodeGenerator", "GeneratedFile", "Target", "get_generator", "list_targets"]
