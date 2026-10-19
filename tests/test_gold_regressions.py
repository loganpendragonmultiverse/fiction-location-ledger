import copy
import json

import pytest

from fiction_location_ledger.cli import main
from fiction_location_ledger.core import analyze


@pytest.mark.parametrize(
    "data",
    [
        [],
        {},
        {"scenes": []},
        {"scenes": {}},
        {"scenes": [None]},
        {"scenes": [{"id": True}]},
        {"scenes": [{"id": " "}]},
        {"scenes": [{"id": 1}, {"id": "1"}]},
        {"scenes": [{"locations": {}}]},
        {"scenes": [{"locations": [None]}]},
        {"scenes": [{"locations": [{"name": None}]}]},
        {"scenes": [{"locations": [{"name": " "}]}]},
        {"scenes": [{"locations": [{"name": "Gate", "description": 3}]}]},
    ],
)
def test_invalid_inputs_are_actionable(data, tmp_path, capsys):
    source = tmp_path / "bad.json"
    source.write_text(json.dumps(data))
    with pytest.raises((TypeError, ValueError)):
        analyze(data)
    assert main([str(source)]) == 2
    assert "error:" in capsys.readouterr().err


def test_alias_chain_retains_observations_and_input():
    data = {
        "scenes": [
            {"id": "opening", "locations": [{"name": "Old", "description": "past"}]},
            {"id": "return", "locations": [{"name": "Gate", "description": "present"}]},
        ],
        "aliases": [{"alias": "old", "canonical": "GATE"}],
    }
    original = copy.deepcopy(data)
    result = analyze(data)["locations"][0]
    assert result["scenes"] == ["opening", "return"]
    assert result["observations"][0]["location"] == data["scenes"][0]["locations"][0]
    assert result["descriptions"] == ["past", "present"]
    assert data == original
