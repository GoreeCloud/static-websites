#!/usr/bin/env python3
"""Validate the retained historical repository-portfolio snapshot.

Current repository authority is live GitHub. This validator deliberately does
not render the snapshot into current public pages or require historical names,
counts, or visibility to equal present-day GitHub state.
"""

from __future__ import annotations

from collections import Counter
from datetime import date
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "docs" / "repository-portfolio.json"


def main() -> int:
    errors: list[str] = []
    try:
        data=json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc:
        print(f"Historical repository snapshot validation failed: {exc}")
        return 1

    if data.get("schema_version") != 1:
        errors.append("schema_version must remain 1")
    if data.get("record_role") != "historical-snapshot":
        errors.append("record_role must be historical-snapshot")
    if data.get("current_authority") is not False:
        errors.append("historical repository snapshot must not claim current authority")
    if "Live GitHub controls current repository" not in data.get("current_authority_note",""):
        errors.append("snapshot must identify live GitHub as current repository authority")

    as_of=data.get("as_of")
    try:
        reviewed=date.fromisoformat(as_of) if isinstance(as_of,str) else None
    except ValueError:
        reviewed=None
    if reviewed is None or reviewed > date.today():
        errors.append("as_of must be a valid non-future date")

    groups=data.get("groups")
    counts=data.get("counts")
    if not isinstance(groups,list) or not groups:
        errors.append("historical groups must remain a non-empty list")
        groups=[]
    if not isinstance(counts,dict):
        errors.append("historical counts must remain an object")
        counts={}

    names=[]
    visibilities=[]
    group_ids=[]
    for group in groups:
        if not isinstance(group,dict):
            errors.append("every historical group must be an object")
            continue
        group_id=group.get("id")
        repos=group.get("repositories")
        if not isinstance(group_id,str) or not group_id:
            errors.append("historical group id must be non-empty")
        else:
            group_ids.append(group_id)
        if not isinstance(repos,list):
            errors.append(f"historical group {group_id!r} repositories must be a list")
            continue
        for entry in repos:
            if not isinstance(entry,dict):
                errors.append(f"historical repository in {group_id!r} must be an object")
                continue
            name=entry.get("name")
            visibility=entry.get("visibility")
            if not isinstance(name,str) or not name:
                errors.append(f"historical repository in {group_id!r} has invalid name")
                continue
            if visibility not in {"public","private"}:
                errors.append(f"historical repository {name} has invalid visibility")
                continue
            names.append(name)
            visibilities.append(visibility)

    if any(count>1 for count in Counter(group_ids).values()):
        errors.append("historical snapshot contains duplicate group ids")
    if any(count>1 for count in Counter(names).values()):
        errors.append("historical snapshot contains duplicate repository names")

    computed={
        "total":len(names),
        "public":visibilities.count("public"),
        "private":visibilities.count("private"),
        "functional_groups":len(group_ids),
    }
    for key,value in computed.items():
        if counts.get(key) != value:
            errors.append(f"historical count {key} must equal preserved entries ({value})")

    if errors:
        print("Historical repository snapshot validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Historical repository snapshot valid for {as_of}: {len(names)} preserved entries. Live GitHub remains current authority.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
