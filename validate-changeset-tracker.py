#!/usr/bin/env python3
"""
Validate changeset-tracker.json against the ChangeSet Tracker Schema v2.1.

Checks:
1. Valid JSON (not truncated)
2. Required top-level structure (schema_version, changesets array, summary)
3. Every changeset has required fields (id, title, status, department, platforms, created)
4. All statuses are spec-valid
5. All subtypes are spec-valid
5a. department is one of the 10 canonical enum values
5b. platforms[] is a non-empty array of strings (unknown values warn, not error)
5c. Legacy 'surface' field must not reappear (retired by AP-001)
6. sweep_flags are strings or objects with required 'flag' field
7. No duplicate changeset IDs
8. Summary counts match actual data
"""

import json
import sys
from collections import Counter

# ─── Canonical constants — loaded from _schema-constants.json (single source of truth) ─────────
#
# Constants live in data/_schema-constants.json, synced from the kgs-repo
# (kenetik-growth-system/commands/_schema-constants.json) on every push to main
# via the kgs-repo's sync-tracker-to-dashboards.yml workflow.
# §1b in the kgs-repo's changeset-common-functions.md describes the JSON for
# human readers; the JSON is the machine-readable source of truth.

import os
_CONSTANTS_PATH = os.path.join(os.path.dirname(__file__), 'data', '_schema-constants.json')
try:
    with open(_CONSTANTS_PATH, 'r') as _cf:
        _SC = json.load(_cf)
except FileNotFoundError:
    print(f"FATAL: schema constants not found at {_CONSTANTS_PATH}", file=sys.stderr)
    print("       Did the kgs-repo sync-tracker-to-dashboards.yml run? "
          "It should have copied _schema-constants.json into data/.")
    sys.exit(2)

VALID_STATUSES = set(_SC['valid_statuses'])
VALID_SUBTYPES = set(_SC['valid_subtypes'])
REQUIRED_FIELDS = set(_SC['required_fields'])
VALID_DEPARTMENTS = set(_SC['valid_departments'])
KNOWN_PLATFORMS = set(_SC['valid_platforms'])

def validate(path='data/changeset-tracker.json'):
    errors = []
    warnings = []

    # 1. Parse JSON
    try:
        with open(path, 'r') as f:
            raw = f.read()
    except FileNotFoundError:
        print(f"⚠️  {path} not found — skipping validation (file may not exist yet)")
        sys.exit(0)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        errors.append(f"INVALID JSON (likely truncated during push): {e}")
        errors.append(f"File size: {len(raw)} chars")
        # Check for common truncation patterns
        if raw.rstrip()[-1:] not in ('}', ']'):
            errors.append("File does not end with } or ] — almost certainly truncated")
        print_results(errors, warnings)
        sys.exit(1)

    # 2. Top-level structure
    if not isinstance(data, dict):
        errors.append("Top-level is not an object")
        print_results(errors, warnings)
        sys.exit(1)

    if 'changesets' not in data or not isinstance(data.get('changesets'), list):
        errors.append("Missing or invalid 'changesets' array")

    if 'schema_version' not in data:
        warnings.append("Missing 'schema_version' field")

    changesets = data.get('changesets', [])

    # 3. Required fields per changeset
    for i, cs in enumerate(changesets):
        cs_id = cs.get('id', f'[index {i}]')
        missing = REQUIRED_FIELDS - set(cs.keys())
        if missing:
            errors.append(f"{cs_id}: missing required fields: {missing}")

    # 4. Status validation
    for cs in changesets:
        cs_id = cs.get('id', '?')
        status = cs.get('status', '')
        if status not in VALID_STATUSES:
            errors.append(f"{cs_id}: invalid status '{status}' — valid: {sorted(VALID_STATUSES)}")

    # 5. Subtype validation
    for cs in changesets:
        cs_id = cs.get('id', '?')
        subtype = cs.get('subtype')
        if subtype and subtype not in VALID_SUBTYPES:
            errors.append(f"{cs_id}: invalid subtype '{subtype}' — valid: {sorted(VALID_SUBTYPES)}")

    # 5a. Department enum validation (AP-001 retired 'surface' in favor of department + platforms[])
    for cs in changesets:
        cs_id = cs.get('id', '?')
        dept = cs.get('department')
        if dept is not None and dept not in VALID_DEPARTMENTS:
            errors.append(f"{cs_id}: invalid department '{dept}' — valid: {sorted(VALID_DEPARTMENTS)}")

    # 5b. Platforms validation — must be a non-empty array of strings; unknown values warn
    for cs in changesets:
        cs_id = cs.get('id', '?')
        platforms = cs.get('platforms')
        if platforms is None:
            continue  # already caught by REQUIRED_FIELDS above
        if not isinstance(platforms, list):
            errors.append(f"{cs_id}: platforms must be an array, got {type(platforms).__name__}")
            continue
        if not platforms:
            errors.append(f"{cs_id}: platforms array is empty — must list at least one platform")
            continue
        for j, p in enumerate(platforms):
            if not isinstance(p, str):
                errors.append(f"{cs_id}: platforms[{j}] is {type(p).__name__}, expected string")
            elif p not in KNOWN_PLATFORMS:
                warnings.append(f"{cs_id}: platforms[{j}]='{p}' is not in the known platform list (add to KNOWN_PLATFORMS if intentional)")

    # 5c. Legacy surface field must not reappear (AP-001 retirement)
    for cs in changesets:
        cs_id = cs.get('id', '?')
        if 'surface' in cs:
            errors.append(f"{cs_id}: legacy 'surface' field is retired (AP-001) — use 'department' + 'platforms[]'")

    # 6. sweep_flags validation (array of strings or objects with required 'flag' field)
    for cs in changesets:
        cs_id = cs.get('id', '?')
        flags = cs.get('sweep_flags', [])
        if not isinstance(flags, list):
            errors.append(f"{cs_id}: sweep_flags is not an array")
        else:
            for j, flag in enumerate(flags):
                if isinstance(flag, str):
                    pass  # legacy format, accepted
                elif isinstance(flag, dict):
                    if 'flag' not in flag or not isinstance(flag.get('flag'), str):
                        errors.append(f"{cs_id}: sweep_flags[{j}] is object but missing required 'flag' string field")
                else:
                    errors.append(f"{cs_id}: sweep_flags[{j}] is {type(flag).__name__}, expected string or object with 'flag' field")


    # 6b. Array-typed graph fields must be arrays (added 2026-05-04)
    # CS-117 through CS-140 regression: daily-pipeline writer emitted dependencies as free-text
    # string, which crashed the changeset-dashboard openDetail() popup with TypeError.
    array_fields = ('dependencies', 'blocks', 'spawned_changesets', 'routed_to')
    for cs in changesets:
        cs_id = cs.get('id', '?')
        for fname in array_fields:
            if fname not in cs or cs[fname] is None:
                continue
            if not isinstance(cs[fname], list):
                errors.append(
                    f"{cs_id}: '{fname}' must be an array (got "
                    f"{type(cs[fname]).__name__}). Wrap single values in []. "
                    "Free-text descriptions belong in 'notes', not in graph fields."
                )

    # 7. Duplicate ID check
    ids = [cs.get('id') for cs in changesets]
    dupes = [id for id, count in Counter(ids).items() if count > 1]
    if dupes:
        errors.append(f"Duplicate changeset IDs: {dupes}")

    # 7. Summary count validation
    summary = data.get('summary', {})
    by_status = summary.get('by_status', {})
    if by_status:
        actual_counts = Counter(cs.get('status', 'unknown') for cs in changesets)
        for status, expected in by_status.items():
            actual = actual_counts.get(status, 0)
            if actual != expected:
                warnings.append(f"summary.by_status.{status}: expected {expected}, actual {actual}")

    # summary.total_changesets retired 2026-05-04 — was redundant with summary.total.

    print_results(errors, warnings)
    if errors:
        sys.exit(1)
    else:
        print(f"\n✅ All {len(changesets)} changesets pass schema validation")
        sys.exit(0)


def print_results(errors, warnings):
    if errors:
        print(f"❌ {len(errors)} ERROR(S):")
        for e in errors:
            print(f"  ERROR: {e}")
    if warnings:
        print(f"⚠️  {len(warnings)} WARNING(S):")
        for w in warnings:
            print(f"  WARN: {w}")
    if not errors and not warnings:
        print("No issues found.")


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'data/changeset-tracker.json'
    validate(path)
