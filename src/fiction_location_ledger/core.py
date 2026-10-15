from __future__ import annotations

import json
import re
from typing import Any

PROJECT = "fiction-location-ledger"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _alias_targets(data: dict[str, Any], observed: dict[str, str]) -> dict[str, str]:
    entries = data.get("aliases", [])
    if not isinstance(entries, list):
        raise TypeError("aliases must be a list of alias/canonical objects")
    links: dict[str, str] = {}
    for entry in entries:
        if not isinstance(entry, dict) or any(
            not isinstance(entry.get(key), str) or not entry[key].strip()
            for key in ("alias", "canonical")
        ):
            raise ValueError("aliases need nonempty alias and canonical labels")
        alias, target = (entry[key].strip().casefold() for key in ("alias", "canonical"))
        if alias in links:
            raise ValueError(f"ambiguous alias: {entry['alias']}")
        links[alias] = target
    resolved = {}
    for alias in links:
        seen: set[str] = set()
        target = alias
        while target in links:
            if target in seen:
                raise ValueError(f"alias cycle: {alias}")
            seen.add(target)
            target = links[target]
        if target not in observed:
            raise ValueError(f"dangling canonical location: {target}")
        resolved[alias] = target
    return resolved


def _locations(data: dict[str, Any]) -> dict[str, Any]:
    scenes = _require(data, "scenes")
    observed: dict[str, str] = {}
    for scene in scenes:
        for item in scene.get("locations", []):
            name = str(item.get("name", "")).strip()
            if not name:
                raise ValueError("locations need names")
            observed.setdefault(name.casefold(), name)
    targets = _alias_targets(data, observed)
    locations: dict[str, dict[str, Any]] = {}
    for order, scene in enumerate(scenes, 1):
        scene_id = str(scene.get("id", order))
        for item in scene.get("locations", []):
            name = str(item.get("name", "")).strip()
            canonical = targets.get(name.casefold(), name.casefold())
            record = locations.setdefault(
                canonical,
                {
                    "name": observed[canonical],
                    "first_scene": scene_id,
                    "scenes": [],
                    "descriptions": [],
                },
            )
            if "aliases" in data:
                record["id"] = canonical
                record.setdefault("observations", []).append(
                    {"scene": scene_id, "location": dict(item)}
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
            payload = json.dumps(value, indent=2, ensure_ascii=False)
            fence = "`" * max(
                3,
                max((len(run) for run in re.findall(r"`+", payload)), default=0) + 1,
            )
            lines.append(f"{fence}json\n{payload}\n{fence}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
