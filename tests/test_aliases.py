import copy
import json

import pytest

from fiction_location_ledger.core import analyze, render_json, render_markdown


def test_alias_chain_preserves_evidence_and_first_use():
    data = {
        "scenes": [
            {"id": "早", "locations": [{"name": "Old Gate", "description": "``` <&>"}]},
            {"id": "late", "locations": [{"name": "城門", "description": "stone"}]},
        ],
        "aliases": [
            {"alias": "Old Gate", "canonical": "Gate"},
            {"alias": "Gate", "canonical": "城門"},
        ],
    }
    original = copy.deepcopy(data)
    report = analyze(data)
    location = report["locations"][0]
    assert len(report["locations"]) == 1
    assert location["id"] == "城門"
    assert location["first_scene"] == "早"
    assert location["scenes"] == ["早", "late"]
    assert location["observations"][0]["location"]["name"] == "Old Gate"
    assert location["descriptions"] == ["``` <&>", "stone"]
    assert data == original
    assert json.loads(render_json(report)) == report
    assert "````json" in render_markdown(report)


@pytest.mark.parametrize(
    "aliases",
    [
        {},
        [None],
        [{"alias": "x"}],
        [{"alias": " ", "canonical": "Place"}],
        [{"alias": "x", "canonical": "missing"}],
        [{"alias": "x", "canonical": "x"}],
        [{"alias": "x", "canonical": "y"}, {"alias": "y", "canonical": "x"}],
        [{"alias": "X", "canonical": "Place"}, {"alias": " x ", "canonical": "Place"}],
    ],
)
def test_invalid_aliases_reject(aliases):
    with pytest.raises((ValueError, TypeError)):
        analyze({"scenes": [{"locations": [{"name": "Place"}]}], "aliases": aliases})


def test_legacy_casefold_and_empty_name():
    report = analyze({"scenes": [{"locations": [{"name": "Place"}, {"name": "PLACE"}]}]})
    assert report["locations"] == [
        {"name": "Place", "first_scene": "1", "scenes": ["1"], "descriptions": []}
    ]
    with pytest.raises(ValueError, match="names"):
        analyze({"scenes": [{"locations": [{}]}]})
