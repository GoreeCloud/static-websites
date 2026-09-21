#!/usr/bin/env python3
"""Validate the retained historical Suite portfolio snapshot.

The current website uses the later reconciled 45-product Suite registry. This
validator preserves the 2026-09-01 snapshot as provenance only and deliberately
does not render it into current public pages.
"""

from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
SNAPSHOT=ROOT / "docs" / "suite-portfolio.json"


def main() -> int:
    errors: list[str]=[]
    try:
        data=json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc:
        print(f"Historical Suite snapshot validation failed: {exc}")
        return 1

    if data.get("schema_version") != 1:
        errors.append("schema_version must remain 1")
    if data.get("record_role") != "historical-snapshot":
        errors.append("record_role must be historical-snapshot")
    if data.get("current_authority") is not False:
        errors.append("historical Suite snapshot must not claim current authority")
    if "45-product Suite registry" not in data.get("current_authority_note",""):
        errors.append("snapshot must identify the later 45-product registry as current website authority")

    as_of=data.get("as_of")
    try:
        reviewed=date.fromisoformat(as_of) if isinstance(as_of,str) else None
    except ValueError:
        reviewed=None
    if reviewed is None or reviewed > date.today():
        errors.append("as_of must be a valid non-future date")

    groups=data.get("groups")
    if not isinstance(groups,list) or not groups:
        errors.append("historical groups must remain a non-empty list")
        groups=[]

    ids=[]
    names=[]
    for group in groups:
        apps=group.get("applications") if isinstance(group,dict) else None
        if not isinstance(apps,list):
            errors.append("each historical Suite group must contain an applications list")
            continue
        for app in apps:
            if not isinstance(app,dict):
                errors.append("historical Suite application must be an object")
                continue
            app_id=app.get("id")
            name=app.get("name")
            if not isinstance(app_id,str) or not app_id:
                errors.append("historical Suite application id must be non-empty")
            else:
                ids.append(app_id)
            if not isinstance(name,str) or not name:
                errors.append("historical Suite application name must be non-empty")
            else:
                names.append(name)

    if len(ids) != len(set(ids)):
        errors.append("historical Suite snapshot contains duplicate ids")
    if len(names) != len(set(names)):
        errors.append("historical Suite snapshot contains duplicate names")

    if errors:
        print("Historical Suite snapshot validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Historical Suite snapshot valid for {as_of}: {len(ids)} preserved entries. Current website authority is the reconciled 45-product registry.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
