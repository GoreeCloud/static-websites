#!/usr/bin/env python3
"""Fail-closed Glaze V1.7 source-adoption validation for the GoreeCloud website."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "glaze.lock.json"
ACCEPTANCE = ROOT / "acceptance/glaze-ui-v1.7-consumer-acceptance.json"
PAGES = (
    ROOT / "index.html",
    ROOT / "platform-systems/index.html",
    ROOT / "suite/index.html",
    ROOT / "office-suite/index.html",
    ROOT / "firefox/index.html",
    ROOT / "github/index.html",
    ROOT / "contact/index.html",
    ROOT / "design/index.html",
    ROOT / "security/index.html",
    ROOT / "privacy/index.html",
)
EXPECTED = {
    "version": "1.7.0",
    "lifecycle": "Stable",
    "repository": "GoreeCloud/glaze",
    "stable_commit": "1a5756daed2294155be2e9972b24f580f6222b7b",
    "stable_baseline": "1.6.0",
    "accepted_release_source": "1a5756daed2294155be2e9972b24f580f6222b7b",
    "entrypoint": "js/glaze-v1.7.0.mjs",
    "entrypoint_blob": "c669d9c6f1738b2a56cb02b2e00fa0ca229117c0",
    "consumer_state": "source-adopted-unaccepted",
}


def git_blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\x00"
    return hashlib.sha1(header + data, usedforsecurity=False).hexdigest()


def main() -> int:
    errors: list[str] = []

    try:
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Glaze V1.7 validation failed: {exc}")
        return 1

    for key, value in EXPECTED.items():
        if lock.get(key) != value:
            errors.append(f"glaze.lock.json {key} must be {value!r}; found {lock.get(key)!r}")

    try:
        acceptance = json.loads(ACCEPTANCE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"V1.7 consumer acceptance record missing or invalid: {exc}")
        acceptance = {}

    if acceptance:
        required = {
            "schemaVersion": 1,
            "consumerName": "GoreeCloud Website",
            "repository": "GoreeCloud/static-websites",
            "targetVersion": "1.7.0",
            "designSystemStableRevision": EXPECTED["stable_commit"],
            "designSystemEntrypoint": EXPECTED["entrypoint"],
            "designSystemEntrypointBlob": EXPECTED["entrypoint_blob"],
        }
        for key, value in required.items():
            if acceptance.get(key) != value:
                errors.append(f"consumer acceptance {key} must be {value!r}; found {acceptance.get(key)!r}")

        status = acceptance.get("status")
        if status not in {"pending-evidence", "pending-human-acceptance", "accepted-v1"}:
            errors.append(f"unsupported consumer acceptance status: {status!r}")

        machine = acceptance.get("machineEvidence")
        machine_keys = (
            "repositoryValidation",
            "websiteValidation",
            "renderedPublicTreeEquivalence",
            "responsiveAndInteraction",
            "isolatedArtifact",
            "privacyAndSecurity",
        )
        machine_passed = isinstance(machine, dict) and all(
            isinstance(machine.get(key), dict) and machine[key].get("status") == "passed"
            for key in machine_keys
        )

        human = acceptance.get("humanEvidence")
        human_passed = isinstance(human, dict) and all(
            isinstance(human.get(key), dict) and human[key].get("status") == "passed"
            for key in ("visualReview", "keyboardReview", "assistiveTechnologyReview")
        )

        if status == "pending-human-acceptance" and not machine_passed:
            errors.append("pending-human-acceptance requires all required machine evidence to be passed")

        if status == "accepted-v1":
            if not machine_passed or not human_passed:
                errors.append("accepted-v1 requires all required machine and human evidence to pass")
            performance = acceptance.get("performance")
            if not isinstance(performance, dict) or performance.get("status") != "passed":
                errors.append("accepted-v1 requires passed representative performance evidence")

        approval = acceptance.get("productionApproval")
        if not isinstance(approval, dict):
            errors.append("consumer acceptance productionApproval must be an object")
        elif status != "accepted-v1" and approval.get("approved") is not False:
            errors.append("production approval must remain false before current consumer acceptance")

    source_root = os.environ.get("GLAZE_UI_SOURCE")
    if source_root:
        source = Path(source_root)
        version = source / "VERSION"
        entrypoint = source / EXPECTED["entrypoint"]
        if not version.is_file() or version.read_text(encoding="utf-8").strip() != EXPECTED["version"]:
            errors.append("pinned Glaze source VERSION is not 1.7.0")
        if not entrypoint.is_file():
            errors.append("pinned Glaze V1.7.0 runtime entrypoint is missing")
        elif git_blob_sha(entrypoint.read_bytes()) != EXPECTED["entrypoint_blob"]:
            errors.append("pinned Glaze V1.7.0 runtime entrypoint bytes do not match the accepted blob")

    for page in PAGES:
        if not page.is_file():
            errors.append(f"missing V1.7 consumer page: {page.relative_to(ROOT)}")
            continue
        text = page.read_text(encoding="utf-8")
        for marker in (
            'data-glaze-version="1.7.0"',
            'name="goreecloud-glaze-ui" content="1.7.0"',
            'name="goreecloud-glaze-consumer-state" content="source-adopted-unaccepted"',
        ):
            if marker not in text:
                errors.append(f"{page.relative_to(ROOT)} missing V1.7 source-adoption marker: {marker}")
        for forbidden in (
            'data-glaze-version="1.6.0"',
            'name="goreecloud-glaze-ui" content="1.6.0"',
            'consumer-state" content="accepted',
            "production-eligible",
            "Glaze V1.7 conformant",
        ):
            if forbidden in text:
                errors.append(f"{page.relative_to(ROOT)} contains forbidden stale/overclaim marker: {forbidden}")

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
            errors.append(f"website visual CSS missing accessibility/adaptive marker: {marker}")

    if errors:
        print("Glaze V1.7 source-adoption validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        "Glaze V1.7 source-adoption validation passed. "
        "Consumer state remains source-adopted-unaccepted; downstream acceptance is still pending."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
