#!/usr/bin/env python3
"""
KGS Dashboard Validation Script
Validates system-state.json against the KGS v3.2 spec before any push.
Run: python3 validate-dashboard.py
Exit code 0 = valid, 1 = errors found

This script is the single source of truth for dashboard data integrity.
It MUST pass before any commit to kenetik-dashboards is pushed.
"""

import json
import sys
import os

ERRORS = []
WARNINGS = []

def error(msg):
    ERRORS.append(msg)
    print(f"  ✗ ERROR: {msg}")

def warn(msg):
    WARNINGS.append(msg)
    print(f"  ⚠ WARN:  {msg}")

def ok(msg):
    print(f"  ✓ {msg}")

# ── KGS v3.2 Canonical Role Structure ──
# This is the AUTHORITATIVE reference. If the spec changes, update HERE FIRST.
CANONICAL_ROLES = {
    "cgo":                 {"name": "Chief Growth Officer",              "layer": "Executive",       "procs": 5,  "prefix": "1."},
    "data_intelligence":   {"name": "Data Intelligence Lead",            "layer": "Intelligence",    "procs": 10, "prefix": "2."},
    "ops_intelligence":    {"name": "Operations Intelligence Lead",      "layer": "Intelligence",    "procs": 9,  "prefix": "3."},
    "creative_strategist": {"name": "Creative Strategist",               "layer": "Creative Engine", "procs": 9,  "prefix": "4a."},
    "content_producer":    {"name": "Content Producer (Larry 2.0)",      "layer": "Creative Engine", "procs": 6,  "prefix": "4b."},
    "creative_studio":     {"name": "Creative Studio Operator (Moe)",    "layer": "Creative Engine", "procs": 9,  "prefix": "4c."},
    "marketing_social":    {"name": "Marketing & Social Intelligence Lead", "layer": "Planning",     "procs": 9,  "prefix": "5."},
    "web_experimentation": {"name": "Web & Experimentation Lead",        "layer": "Execution",       "procs": 9,  "prefix": "6."},
    "channel_execution":   {"name": "Channel Execution Manager",         "layer": "Execution",       "procs": 9,  "prefix": "7."},
    "paid_media":          {"name": "Paid Media Manager",                "layer": "Execution",       "procs": 8,  "prefix": "8."},
    "amazon":              {"name": "Amazon Marketplace Manager",        "layer": "Execution",       "procs": 8,  "prefix": "9."},
    "project_manager":     {"name": "Project Manager",                   "layer": "Infrastructure",  "procs": 7,  "prefix": "10."},
}

VALID_LAYERS = ["Executive", "Intelligence", "Creative Engine", "Planning", "Execution", "Infrastructure"]
VALID_STATUSES = ["not_started", "in_progress", "built", "live", "consolidated"]
VALID_TRANSITIONS = {
    "not_started": ["in_progress", "built"],
    "in_progress": ["built", "not_started"],
    "built":       ["live", "in_progress"],
    "live":        ["consolidated", "built"],
    "consolidated": ["live"],
}

def validate():
    print("\n🔍 KGS Dashboard Validation (v3.2 spec)\n")

    # ── 1. File existence ──
    print("1. File checks")
    for f in ["system-state.json", "kenetik-growth-system-dashboard.html"]:
        if not os.path.exists(f):
            error(f"Missing required file: {f}")
            return False
        ok(f"{f} exists")

    # ── 2. JSON validity ──
    print("\n2. JSON validity")
    try:
        with open("system-state.json") as f:
            data = json.load(f)
        ok("system-state.json is valid JSON")
    except json.JSONDecodeError as e:
        error(f"system-state.json is invalid JSON: {e}")
        return False

    # ── 3. Role structure integrity ──
    print("\n3. Role structure (PROTECTED — must match KGS v3.2)")
    roles = data.get("roles", {})

    if len(roles) != len(CANONICAL_ROLES):
        error(f"Expected {len(CANONICAL_ROLES)} roles, found {len(roles)}")

    for role_id, expected in CANONICAL_ROLES.items():
        role = roles.get(role_id)
        if not role:
            error(f"Missing role: {role_id} ({expected['name']})")
            continue

        if role.get("name") != expected["name"]:
            error(f"Role {role_id} name mismatch: '{role.get('name')}' != '{expected['name']}'")

        if role.get("layer") != expected["layer"]:
            error(f"Role {role_id} layer mismatch: '{role.get('layer')}' != '{expected['layer']}'")

        procs = role.get("processes", [])
        if len(procs) != expected["procs"]:
            error(f"Role {role_id} has {len(procs)} processes, expected {expected['procs']}")

        for pid in procs:
            if not pid.startswith(expected["prefix"]):
                error(f"Role {role_id} process {pid} has wrong prefix (expected {expected['prefix']})")

    # Check for extra roles that shouldn't exist
    for role_id in roles:
        if role_id not in CANONICAL_ROLES:
            error(f"Unknown role '{role_id}' — not in KGS v3.2 spec")

    if not any(e.startswith("Role") or e.startswith("Missing role") or e.startswith("Expected") or e.startswith("Unknown role") for e in ERRORS):
        ok(f"All {len(CANONICAL_ROLES)} roles match KGS v3.2 spec")

    # ── 4. Process integrity ──
    print("\n4. Process integrity")
    processes = data.get("processes", {})

    # All role process refs must exist
    all_refs = set()
    for role in roles.values():
        for pid in role.get("processes", []):
            all_refs.add(pid)
            if pid not in processes:
                error(f"Role '{role.get('name')}' references process {pid} which doesn't exist")

    # All processes must be referenced by a role
    for pid in processes:
        if pid not in all_refs:
            warn(f"Orphaned process {pid} — not referenced by any role")

    # All processes must have valid status
    for pid, proc in processes.items():
        status = proc.get("status", "")
        if status not in VALID_STATUSES:
            error(f"Process {pid} has invalid status: '{status}'")

        if not proc.get("name"):
            error(f"Process {pid} is missing 'name' field (WILL CRASH DASHBOARD)")

    ok(f"{len(processes)} processes validated")

    # ── 5. Infrastructure integrity ──
    print("\n5. Infrastructure integrity")
    infra = data.get("infrastructure", {})
    for category_name in ["mcps", "platforms", "connections"]:
        category = infra.get(category_name, {})
        for key, item in category.items():
            if not item.get("name"):
                error(f"Infrastructure {category_name}.{key} missing 'name' (WILL CRASH DASHBOARD)")
            if not item.get("status"):
                warn(f"Infrastructure {category_name}.{key} missing 'status'")

    ok("Infrastructure entries validated")

    # ── 6. HTML file basic checks ──
    print("\n6. Dashboard HTML integrity")
    with open("kenetik-growth-system-dashboard.html") as f:
        html = f.read()

    line_count = html.count("\n") + 1
    if line_count < 1500:
        error(f"HTML has only {line_count} lines — likely stripped (should be ~1900+)")
    else:
        ok(f"HTML has {line_count} lines (healthy)")

    critical_functions = ["loadSystemState", "renderOrgChart", "renderRoles", "renderPatterns", "renderStats", "computeRoleStats", "initDashboard"]
    for fn in critical_functions:
        if fn not in html:
            error(f"HTML missing critical function: {fn}()")
    ok("All critical JS functions present")

    if "system-state.json" not in html:
        error("HTML doesn't reference system-state.json")
    ok("HTML references external JSON data files")

    # ── Results ──
    print(f"\n{'='*50}")
    if ERRORS:
        print(f"❌ FAILED: {len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        print(f"\nErrors:")
        for e in ERRORS:
            print(f"  • {e}")
        return False
    else:
        print(f"✅ PASSED: 0 errors, {len(WARNINGS)} warning(s)")
        return True


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)) if os.path.dirname(__file__) else ".")
    success = validate()
    sys.exit(0 if success else 1)
