#!/usr/bin/env python3
"""
Validate changeset-tracker.json against the ChangeSet Tracker Schema v2.1.

Checks:
1. Valid JSON (not truncated)
2. Required top-level structure (schema_version, changesets array, summary)
3. Every changeset has required fields
4. All statuses are spec-valid
5. All subtypes are spec-valid
6. Summary counts match actual data
7. No duplicate changeset IDs
"""

import json
import sys
from collections import Counter

VALID_STATUSES = {'draft', 'needs_feedback', 'approved', 'published', 'rolled_back', 'closed'}
VALID_SUBTYPES = {'implementation', 'investigation', 'quick'}
REQUIRED_FIELDS = {'id', 'title', 'status', 'surface', 'created'}

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

    # 6. Duplicate ID check
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

    total = summary.get('total_changesets')
    if total is not None and total != len(changesets):
        warnings.append(f"summary.total_changesets: expected {total}, actual {len(changesets)}")

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
