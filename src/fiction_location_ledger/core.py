from __future__ import annotations

import json
from typing import Any

PROJECT = "fiction-location-ledger"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _locations(data: dict[str, Any]) -> dict[str, Any]:
    locations: dict[str, dict[str, Any]] = {}
    for order, scene in enumerate(_require(data, "scenes"), 1):
        scene_id = str(scene.get("id", order))
        for item in scene.get("locations", []):
            name = str(item.get("name", "")).strip()
            if not name:
                raise ValueError("locations need names")
            record = locations.setdefault(
                name.casefold(),
                {"name": name, "first_scene": scene_id, "scenes": [], "descriptions": []},
            )
            if scene_id not in record["scenes"]:
                record["scenes"].append(scene_id)
            description = str(item.get("description", "")).strip()
            if description and description not in record["descriptions"]:
                record["descriptions"].append(description)
    return {"locations": sorted(locations.values(), key=lambda item: item["name"].casefold())}


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    return {"version": 1, "project": PROJECT, **_locations(data)}


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# {report['project'].replace('-', ' ').title()} report", ""]
    for key, value in report.items():
        if key not in {"version", "project"}:
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.append("")
            lines.append(f"```json\n{json.dumps(value, indent=2, ensure_ascii=False)}\n```")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
