from mimic.codegen._dedup import analyze
from mimic.vision.mock import get_fixture


def test_dedup_finds_repeated_subtrees_in_ecommerce():
    tree = get_fixture("ecommerce")
    result = analyze(tree, min_occurrences=2, min_depth=2)
    assert result.shared, "expected repeated product cards to be detected"
    assert any(len(c.occurrences) >= 4 for c in result.shared)


def test_dedup_skips_when_no_repeats():
    tree = get_fixture("login")
    result = analyze(tree, min_occurrences=2, min_depth=2)
    assert result.shared == []


def test_dedup_skips_shallow_subtrees():
    tree = get_fixture("dashboard")
    result = analyze(tree, min_occurrences=2, min_depth=4)
    # at min_depth=4 nothing repeats; verify we don't over-share
    assert all(_node_depth(c.template) >= 4 for c in result.shared)


def _node_depth(node):
    if not node.children:
        return 1
    return 1 + max(_node_depth(c) for c in node.children)
