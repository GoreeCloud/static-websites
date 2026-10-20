#!/usr/bin/env python3
"""Validate GoreeCloud production-readiness governance for the public website.

The website is currently an anonymous static publication surface. Multi-user
readiness is Not Applicable for this architecture, while security, accessibility,
and GC UI migration boundaries remain mandatory. This validator fails closed if
the repository drops those currently executable controls.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
GOVERNANCE = ROOT / "docs" / "governance-readiness.md"
BUILD = ROOT / "scripts" / "build_public_site.py"
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "validate-main-site.yml"
DEPLOYMENT_VALIDATOR = ROOT / "scripts" / "validate_deployment_contract.py"
ORIGIN_VALIDATOR = ROOT / "scripts" / "validate_browser_origin_integrity.py"
ADAPTIVE_VALIDATOR = ROOT / "scripts" / "validate_adaptive_presentation.py"
MIGRATION_RECORD = REPO_ROOT / "docs" / "GC_UI_RETAINED_SITE_RECONCILIATION.md"
ACCESSIBILITY_VALIDATOR = ROOT / "scripts" / "validate_accessibility.py"
INDEX = ROOT / "index.html"

REQUIRED_GOVERNANCE_MARKERS = (
    "Multi-user readiness: Not applicable to the current static public website",
    "Security readiness: Applicable",
    "GC UI design authority: Applicable",
    "If the website adds authentication",
    "this Not Applicable determination expires",
    "successful isolated `dist/` artifact and public-boundary validation",
    "repository-publication, reachable-history, creative-rights, and contextual-disclosure review",
    "governed merge and production authorization",
)

REQUIRED_BUILD_MARKERS = (
    "PUBLIC_FILES = (",
    "DIST = ROOT / \"dist\"",
)

PROHIBITED_DYNAMIC_MARKERS = (
    "<form",
    "firebase",
    "supabase",
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def require_regular_file(errors: list[str], path: Path, label: str) -> str:
    if not path.is_file() or path.is_symlink():
        fail(errors, f"{label} must exist as a regular repository file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []

    governance = require_regular_file(errors, GOVERNANCE, "Governance readiness record")
    migration = require_regular_file(errors, MIGRATION_RECORD, "GC UI migration authority record")
    build = require_regular_file(errors, BUILD, "Public artifact builder")
    workflow = require_regular_file(errors, WORKFLOW, "Validation workflow")
    index = require_regular_file(errors, INDEX, "Homepage")

    for validator, label in (
        (DEPLOYMENT_VALIDATOR, "deployment-contract validator"),
        (ORIGIN_VALIDATOR, "browser-origin validator"),
        (ADAPTIVE_VALIDATOR, "adaptive presentation validator"),
        (ACCESSIBILITY_VALIDATOR, "accessibility validator"),
    ):
        require_regular_file(errors, validator, label)

    if "GoreeCloud UI (GC UI)" not in migration or "no public GC UI cutover accepted" not in migration.lower():
        fail(errors, "GC UI authority and unaccepted website consumer state must remain documented")
    if "GoreeCloud/glaze" in workflow or "validate_glaze_ui.py" in workflow:
        fail(errors, "website validation workflow must not depend on the deleted predecessor")
    if "python sites/main/scripts/validate_adaptive_presentation.py" not in workflow:
        fail(errors, "website CI must retain the adaptive presentation gate")

    for marker in REQUIRED_GOVERNANCE_MARKERS:
        if marker not in governance:
            fail(errors, f"Governance readiness record is missing required boundary: {marker}")

    for marker in REQUIRED_BUILD_MARKERS:
        if marker not in build:
            fail(errors, f"Static public artifact contract is missing required marker: {marker}")

    lower_index = index.lower()
    for marker in PROHIBITED_DYNAMIC_MARKERS:
        if marker in lower_index:
            fail(
                errors,
                f"Current anonymous-static governance classification must be reviewed before homepage dynamic marker is introduced: {marker}",
            )

    required_workflow_commands = (
        "python sites/main/scripts/validate_governance_readiness.py",
        "python sites/main/scripts/validate_site.py",
        "python sites/main/scripts/validate_public_surface.py",
        "python sites/main/scripts/validate_adaptive_presentation.py",
        "python sites/main/scripts/build_public_site.py",
        "python sites/main/scripts/validate_build_artifact.py",
        "python sites/main/scripts/browser_artifact_smoke.py",
    )
    for command in required_workflow_commands:
        if command not in workflow:
            fail(errors, f"Validation workflow must retain governance-supporting gate: {command}")

    if errors:
        print("GoreeCloud governance readiness validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        "GoreeCloud governance readiness passed: current anonymous-static user scope, security, adaptive presentation, and unaccepted GC UI migration boundary."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
