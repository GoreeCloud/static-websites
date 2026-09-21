#!/usr/bin/env python3
"""Fail-closed Glaze UI V1.6 target validation for the website migration candidate."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "glaze.lock.json"
ACCEPTANCE = ROOT / "acceptance/glaze-ui-v1.6-consumer-acceptance.json"
PAGES = (
    ROOT / "index.html",
    ROOT / "platform-systems/index.html",
    ROOT / "suite/index.html",
    ROOT / "office-suite/index.html",
    ROOT / "firefox/index.html",
    ROOT / "github/index.html",
    ROOT / "contact/index.html",
)
EXPECTED = {
    "version": "1.6.0",
    "lifecycle": "Stable",
    "repository": "GoreeCloud/glaze-ui",
    "stable_commit": "081527eff1c5fe5001b6b9598d60439c8fb3c5e3",
    "accepted_release_source": "a7180679ea851389e0f3004515f9a25f420e716d",
    "entrypoint": "js/glaze-v1.6.0.mjs",
    "entrypoint_blob": "7dfc863d6c39def97c263de80b21b73efe54db1e",
    "consumer_state": "migration-candidate-unaccepted",
}


def git_blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\x00"
    return hashlib.sha1(header + data, usedforsecurity=False).hexdigest()


def main() -> int:
    errors: list[str] = []
    try:
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Glaze UI validation failed: {exc}")
        return 1

    for key, value in EXPECTED.items():
        if lock.get(key) != value:
            errors.append(f"glaze.lock.json {key} must be {value!r}; found {lock.get(key)!r}")

    try:
        acceptance = json.loads(ACCEPTANCE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"consumer acceptance record missing or invalid: {exc}")
        acceptance = {}

    if acceptance:
        for key, value in (
            ("schemaVersion", 1),
            ("consumerName", "GoreeCloud Website"),
            ("repository", "GoreeCloud/static-websites"),
            ("targetVersion", "1.6.0"),
            ("designSystemStableRevision", EXPECTED["stable_commit"]),
        ):
            if acceptance.get(key) != value:
                errors.append(f"consumer acceptance {key} must be {value!r}; found {acceptance.get(key)!r}")

        machine = acceptance.get("machineEvidence")
        if not isinstance(machine, dict):
            errors.append("consumer acceptance machineEvidence must be an object")
        else:
            for key in ("repositoryValidation", "websiteValidation", "renderedPublicTreeEquivalence", "responsiveAndInteraction", "isolatedArtifact", "privacyAndSecurity"):
                item = machine.get(key)
                if not isinstance(item, dict) or item.get("status") != "passed":
                    errors.append(f"consumer acceptance machine evidence {key} must be passed")

        human = acceptance.get("humanEvidence")
        status = acceptance.get("status")
        if not isinstance(human, dict):
            errors.append("consumer acceptance humanEvidence must be an object")
        else:
            human_statuses = []
            for key in ("visualReview", "keyboardReview", "assistiveTechnologyReview"):
                item = human.get(key)
                if not isinstance(item, dict):
                    errors.append(f"consumer acceptance humanEvidence.{key} must be an object")
                    continue
                human_statuses.append(item.get("status"))
            if status == "pending-human-acceptance":
                if all(value == "passed" for value in human_statuses):
                    errors.append("pending-human-acceptance must not remain after all human review lanes pass")
            elif status == "accepted-v1":
                if not human_statuses or any(value != "passed" for value in human_statuses):
                    errors.append("accepted-v1 requires all human review lanes to be passed")
                performance = acceptance.get("performance")
                if not isinstance(performance, dict) or performance.get("status") != "passed":
                    errors.append("accepted-v1 requires passed representative performance evidence")
            else:
                errors.append(f"unsupported consumer acceptance status: {status!r}")

        approval = acceptance.get("productionApproval")
        if not isinstance(approval, dict):
            errors.append("consumer acceptance productionApproval must be an object")
        elif status != "accepted-v1" and approval.get("approved") is not False:
            errors.append("production approval must remain false before consumer acceptance")

    source_root = os.environ.get("GLAZE_UI_SOURCE")
    if source_root:
        source = Path(source_root)
        version = source / "VERSION"
        entrypoint = source / EXPECTED["entrypoint"]
        if not version.is_file() or version.read_text(encoding="utf-8").strip() != EXPECTED["version"]:
            errors.append("pinned Glaze source VERSION is not 1.6.0")
        if not entrypoint.is_file():
            errors.append("pinned Glaze V1.6.0 runtime entrypoint is missing")
        elif git_blob_sha(entrypoint.read_bytes()) != EXPECTED["entrypoint_blob"]:
            errors.append("pinned Glaze V1.6.0 runtime entrypoint bytes do not match the accepted blob")

    for page in PAGES:
        if not page.is_file():
            errors.append(f"missing V1.6 consumer page: {page.relative_to(ROOT)}")
            continue
        text = page.read_text(encoding="utf-8")
        for marker in (
            'data-glaze-version="1.6.0"',
            'name="goreecloud-glaze-ui" content="1.6.0"',
            'name="goreecloud-glaze-consumer-state" content="migration-candidate-unaccepted"',
        ):
            if marker not in text:
                errors.append(f"{page.relative_to(ROOT)} missing V1.6 target marker: {marker}")
        for forbidden in ("consumer-state\" content=\"accepted", "production-eligible", "Glaze UI conformant"):
            if forbidden in text:
                errors.append(f"{page.relative_to(ROOT)} overclaims downstream Glaze acceptance: {forbidden}")

    css = (ROOT / "css/site-v9.css").read_text(encoding="utf-8")
    for marker in (
        ":focus-visible",
        "prefers-reduced-motion",
        "prefers-reduced-transparency",
        "prefers-contrast:more",
        "forced-colors:active",
        "min-height:48px",
    ):
        if marker not in css:
            errors.append(f"website V1.6 visual CSS missing accessibility/adaptive marker: {marker}")

    if errors:
        print("Glaze UI V1.6 target validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Glaze UI V1.6 target validation passed. Consumer state remains migration-candidate-unaccepted; this is not downstream acceptance.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
