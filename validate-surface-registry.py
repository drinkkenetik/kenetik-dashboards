#!/usr/bin/env python3
"""
Surface Registry Gate (P4-T5)
=============================

Fails the build if a deployed HTML surface is not registered in
architecture/reporting/surface-registry.md / surface-registry.json.
This is the mechanism that prevents the next orphaned dashboard: you cannot
ship an HTML surface without declaring its owner, purpose, data sources, and
refresh cadence.

Modes:
    --dist DIR      scan DIR recursively for *.html (run AFTER the portal
                    dist/ build in publish-board-portal.yml)
    --html F [F..]  check an explicit list of HTML files (used by
                    kenetik-dashboards' validate-dashboard.yml against its
                    synced copy of the registry)

Every found HTML basename must match the basename of a registry entry's
`path` (or one of its `aliases`) whose status allows deployment
("deployed" or "pending-retirement-decision" — the latter is still live
until Devon's retirement call).

Exit: 0 = all surfaces registered; 1 = unregistered surface or invalid registry.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = REPO_ROOT / "architecture" / "reporting" / "surface-registry.json"
DEPLOYABLE = {"deployed", "pending-retirement-decision"}


def load_registry(path: pathlib.Path) -> dict:
    reg = json.loads(path.read_text())
    valid = set(reg["statuses"])
    for s in reg["surfaces"]:
        for key in ("id", "name", "path", "owner", "purpose",
                    "data_sources", "refresh_cadence", "deploy", "status"):
            if key not in s:
                sys.exit(f"FAIL: registry entry '{s.get('id', '?')}' missing required key '{key}'")
        if s["status"] not in valid:
            sys.exit(f"FAIL: registry entry '{s['id']}' has invalid status '{s['status']}'")
    return reg


def deployable_names(reg: dict) -> set[str]:
    names: set[str] = set()
    for s in reg["surfaces"]:
        if s["status"] in DEPLOYABLE:
            names.add(pathlib.Path(s["path"]).name)
            names.update(s.get("aliases", []))
    return names


def main() -> int:
    ap = argparse.ArgumentParser(description="Surface registry deploy gate (P4-T5)")
    ap.add_argument("--registry", type=pathlib.Path, default=DEFAULT_REGISTRY)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--dist", type=pathlib.Path, help="built output dir to scan for *.html")
    group.add_argument("--html", nargs="+", type=pathlib.Path, help="explicit HTML files to check")
    args = ap.parse_args()

    reg = load_registry(args.registry)
    allowed = deployable_names(reg)

    if args.dist:
        found = sorted({p.name for p in args.dist.rglob("*.html")})
    else:
        found = sorted({p.name for p in args.html})

    unregistered = [n for n in found if n not in allowed]
    print(f"surface-registry gate: {len(found)} deployed HTML surface(s), "
          f"{len(allowed)} registered deployable name(s)")
    for n in found:
        print(f"  {'x' if n in unregistered else 'ok'} {n}")
    if unregistered:
        print(f"\nFAIL: {len(unregistered)} deployed HTML surface(s) not in "
              f"{args.registry} with a deployable status: {', '.join(unregistered)}\n"
              f"Register the surface (owner, purpose, data sources, cadence) or remove it from the deploy.")
        return 1
    print("PASS - every deployed HTML surface is registered.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
