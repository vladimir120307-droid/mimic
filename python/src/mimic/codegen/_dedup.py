"""Detect repeated subtrees and hoist them into parameterized shared widgets.

Strategy:

1. Walk every screen, hashing each subtree two ways:
   - **structural hash** ignores leaf content (text/icon/placeholder/url)
   - **identity hash** includes leaf content
2. Group subtrees by structural hash.
3. For each group with ≥ `min_occurrences` instances, derive parameters
   from the leaf positions where instances differ. The hoisted widget is
   the structural skeleton with named slots; each call site passes its
   per-instance text/icon/url through those slots.

This keeps the v0.1 "wow, 4 product cards collapsed into 1 widget" demo
while never silently dropping per-instance content (the v0.2 regression).
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from dataclasses import dataclass, field

from mimic.models import WidgetNode, WidgetTree


@dataclass
class SharedSlot:
    """One parameter of a hoisted shared widget."""

    name:       str   # e.g. "title", "price", "icon"
    kind:       str   # "text" | "icon" | "image" | "placeholder"
    path:       tuple[int, ...]  # child-index path from the shared root


@dataclass
class SharedComponent:
    name:        str
    template:    WidgetNode                 # canonical first instance
    occurrences: list[str]                  # widget ids that became this
    slots:       list[SharedSlot] = field(default_factory=list)
    # ids -> {slot_name: value}; one entry per occurrence
    bindings:    dict[str, dict[str, str]] = field(default_factory=dict)


@dataclass
class DedupResult:
    shared:       list[SharedComponent] = field(default_factory=list)
    id_to_shared: dict[str, str] = field(default_factory=dict)

    def shared_name_for(self, node_id: str) -> str | None:
        return self.id_to_shared.get(node_id)

    def component_for(self, node_id: str) -> SharedComponent | None:
        name = self.id_to_shared.get(node_id)
        if not name:
            return None
        return next((c for c in self.shared if c.name == name), None)


def analyze(
    tree: WidgetTree, *, min_occurrences: int = 2, min_depth: int = 2
) -> DedupResult:
    by_structure: dict[str, list[WidgetNode]] = defaultdict(list)
    for screen in tree.screens:
        _gather(screen.root, depth=0, min_depth=min_depth, into=by_structure)

    result = DedupResult()
    counter = 0
    for _digest, nodes in by_structure.items():
        if len(nodes) < min_occurrences:
            continue

        slots = _derive_slots(nodes)
        # Skip if all instances are byte-identical — there are no slots, the
        # call site doesn't even need parameters. Still worth deduping because
        # we save lines, so we keep it but with zero slots.

        counter += 1
        name = f"_Shared{counter}"
        template = nodes[0]
        bindings: dict[str, dict[str, str]] = {}
        for node in nodes:
            bindings[node.id] = _extract_bindings(node, slots)

        result.shared.append(
            SharedComponent(
                name=name,
                template=template,
                occurrences=[n.id for n in nodes],
                slots=slots,
                bindings=bindings,
            )
        )
        for n in nodes:
            result.id_to_shared[n.id] = name
    return result


def _gather(
    node: WidgetNode,
    *,
    depth: int,
    min_depth: int,
    into: dict[str, list[WidgetNode]],
) -> None:
    if _node_depth(node) >= min_depth:
        digest = _structural_hash(node)
        into[digest].append(node)
    for child in node.children:
        _gather(child, depth=depth + 1, min_depth=min_depth, into=into)


def _node_depth(node: WidgetNode) -> int:
    if not node.children:
        return 1
    return 1 + max(_node_depth(c) for c in node.children)


def _structural_hash(node: WidgetNode) -> str:
    """Skeleton hash — kind + style + children shape. Ignores leaf content."""
    payload = {
        "kind":     node.kind,
        "style":    node.style.model_dump(),
        "children": [_structural_hash(c) for c in node.children],
    }
    return hashlib.sha1(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _derive_slots(nodes: list[WidgetNode]) -> list[SharedSlot]:
    """Pick the leaf positions whose content varies across instances.

    A position becomes a slot only if at least two instances differ on it —
    otherwise the value is constant and can stay inlined in the template.
    """
    if len(nodes) < 2:
        return []

    leaves_per_instance: list[list[tuple[tuple[int, ...], str, str]]] = [
        _enumerate_leaves(n, ()) for n in nodes
    ]
    # All instances share the same skeleton so leaf lists have the same length
    # and aligned positions.
    if not leaves_per_instance:
        return []
    n_leaves = len(leaves_per_instance[0])

    slots: list[SharedSlot] = []
    used_names: set[str] = set()
    for i in range(n_leaves):
        path, kind, _ = leaves_per_instance[0][i]
        values = {tuple(inst[i][2:]) for inst in leaves_per_instance}
        if len(values) == 1:
            continue  # same across all instances — keep inlined
        name = _slot_name(kind, used_names)
        used_names.add(name)
        slots.append(SharedSlot(name=name, kind=kind, path=path))
    return slots


def _enumerate_leaves(
    node: WidgetNode, path: tuple[int, ...]
) -> list[tuple[tuple[int, ...], str, str]]:
    """Walk the subtree and yield (path, slot-kind, value) for every leaf-y attr.

    Each attribute we might want to parameterize (text / icon / image_url /
    placeholder) is one entry. Stable order so two structurally-identical
    subtrees yield aligned lists.
    """
    out: list[tuple[tuple[int, ...], str, str]] = []
    if node.text is not None:
        out.append((path, "text", node.text))
    if node.icon_name is not None:
        out.append((path, "icon", node.icon_name))
    if node.image_url is not None:
        out.append((path, "image", node.image_url))
    if node.placeholder is not None:
        out.append((path, "placeholder", node.placeholder))
    for idx, child in enumerate(node.children):
        out.extend(_enumerate_leaves(child, (*path, idx)))
    return out


def _extract_bindings(node: WidgetNode, slots: list[SharedSlot]) -> dict[str, str]:
    bindings: dict[str, str] = {}
    for slot in slots:
        target = node
        for idx in slot.path:
            if idx >= len(target.children):
                bindings[slot.name] = ""
                break
            target = target.children[idx]
        else:
            value = ""
            if slot.kind == "text":
                value = target.text or ""
            elif slot.kind == "icon":
                value = target.icon_name or ""
            elif slot.kind == "image":
                value = target.image_url or ""
            elif slot.kind == "placeholder":
                value = target.placeholder or ""
            bindings[slot.name] = value
    return bindings


def _slot_name(kind: str, used: set[str]) -> str:
    """Generate a stable readable slot name, avoiding collisions."""
    base = {
        "text":        "text",
        "icon":        "icon",
        "image":       "image",
        "placeholder": "placeholder",
    }.get(kind, "arg")
    name = base
    i = 2
    while name in used:
        name = f"{base}{i}"
        i += 1
    return name
