from mimic.codegen._dedup import analyze
from mimic.models import (
    BoundingBox,
    Screen,
    Style,
    WidgetNode,
    WidgetTree,
)
from mimic.vision.mock import get_fixture


def _identical_card(idx: int) -> WidgetNode:
    """Build a card with byte-identical content — what strict dedup catches."""
    return WidgetNode(
        id=f"card_{idx}",
        kind="card",
        bounds=BoundingBox(x=0, y=idx * 0.2, width=1, height=0.18),
        style=Style(background_color="#FFFFFF", border_radius=12),
        children=[
            WidgetNode(
                id=f"card_title_{idx}",
                kind="text",
                text="Feature",  # same on every card
                bounds=BoundingBox(x=0, y=0, width=1, height=0.5),
                style=Style(font_size=16, font_weight="bold"),
            )
        ],
    )


def test_dedup_collapses_identical_subtrees():
    root = WidgetNode(
        id="root",
        kind="column",
        bounds=BoundingBox(x=0, y=0, width=1, height=1),
        children=[_identical_card(i) for i in range(3)],
    )
    tree = WidgetTree(screens=[Screen(id="s", name="Home", root=root)])
    result = analyze(tree, min_occurrences=2, min_depth=2)
    assert result.shared, "expected identical cards to be deduplicated"
    assert any(len(c.occurrences) >= 3 for c in result.shared)


def test_dedup_preserves_per_instance_content():
    """Ecommerce product cards differ by title/price/image — parameterized
    dedup collapses them into one shared widget AND captures the differing
    leaves as named slots so nothing is silently dropped."""
    tree = get_fixture("ecommerce")
    result = analyze(tree, min_occurrences=2, min_depth=2)
    product_shared = next(
        (s for s in result.shared if {f"prod_{i}" for i in range(4)} <= set(s.occurrences)),
        None,
    )
    assert product_shared, "expected the 4 product cards to share a hoisted widget"
    assert product_shared.slots, "expected per-instance leaves to become parameter slots"
    # Each instance must have a non-empty value for every slot — no dropped content.
    for prod_id in (f"prod_{i}" for i in range(4)):
        binding = product_shared.bindings[prod_id]
        assert all(v for v in binding.values()), (
            f"slot binding for {prod_id} contains an empty value: {binding}"
        )
    # All the original titles should appear somewhere in the bindings.
    all_values = {v for b in product_shared.bindings.values() for v in b.values()}
    for title in ("Linen shirt", "Knit sweater", "Wool coat", "Cotton trousers"):
        assert title in all_values, f"title {title!r} lost during dedup"


def test_dedup_skips_when_no_repeats():
    tree = get_fixture("login")
    result = analyze(tree, min_occurrences=2, min_depth=2)
    assert result.shared == []


def test_dedup_skips_shallow_subtrees():
    tree = get_fixture("dashboard")
    result = analyze(tree, min_occurrences=2, min_depth=4)
    assert all(_node_depth(c.template) >= 4 for c in result.shared)


def _node_depth(node):
    if not node.children:
        return 1
    return 1 + max(_node_depth(c) for c in node.children)
