"""Detect subtrees that repeat across the WidgetTree.

When the same shape appears N times (regardless of leaf-text content), we can
hoist it into a named widget / component and reduce code size. This module
returns a `DedupResult` consumed by codegen targets.

Conservative: we only deduplicate when the same skeleton appears at least
`min_occurrences` times AND the subtree is deep enough that hoisting saves
meaningful lines (`min_depth`).
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from dataclasses import dataclass, field

from mimic.models import WidgetNode, WidgetTree


@dataclass
class SharedComponent:
    name: str
    template: WidgetNode
    occurrences: list[str]  # list of widget ids using this shape


@dataclass
class DedupResult:
    shared: list[SharedComponent] = field(default_factory=list)
    id_to_shared: dict[str, str] = field(default_factory=dict)

    def shared_name_for(self, node_id: str) -> str | None:
        return self.id_to_shared.get(node_id)


def analyze(tree: WidgetTree, *, min_occurrences: int = 2, min_depth: int = 2) -> DedupResult:
    skeletons: dict[str, list[WidgetNode]] = defaultdict(list)
    for screen in tree.screens:
        _gather(screen.root, depth=0, min_depth=min_depth, into=skeletons)

    result = DedupResult()
    counter = 0
    for _digest, nodes in skeletons.items():
        if len(nodes) < min_occurrences:
            continue
        counter += 1
        name = f"_Shared{counter}"
        template = nodes[0]
        result.shared.append(
            SharedComponent(name=name, template=template, occurrences=[n.id for n in nodes])
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
        digest = _skeleton_hash(node)
        into[digest].append(node)
    for child in node.children:
        _gather(child, depth=depth + 1, min_depth=min_depth, into=into)


def _node_depth(node: WidgetNode) -> int:
    if not node.children:
        return 1
    return 1 + max(_node_depth(c) for c in node.children)


def _skeleton_hash(node: WidgetNode) -> str:
    """Hash of the FULL subtree, including leaf content (text, icons, URLs).

    A future minor release will hoist same-shape-different-content subtrees
    into widgets parameterized by the differing leaves, but that's enough
    extra plumbing to defer. For v0.1.x we only collapse subtrees that are
    byte-for-byte identical so the shared widget never silently drops data
    that was on one instance but not another.
    """
    payload = {
        "kind":        node.kind,
        "style":       node.style.model_dump(),
        "text":        node.text,
        "placeholder": node.placeholder,
        "icon_name":   node.icon_name,
        "image_url":   node.image_url,
        "children":    [_skeleton_hash(c) for c in node.children],
    }
    return hashlib.sha1(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


