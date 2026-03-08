#!/bin/bash
# Install git hooks for kenetik-dashboards
# Run once: bash install-hooks.sh

HOOK_DIR=".git/hooks"
HOOK_FILE="$HOOK_DIR/pre-commit"

cat > "$HOOK_FILE" << 'HOOK'
#!/bin/bash
# KGS Dashboard pre-commit validation
# Runs validate-dashboard.py before every commit that touches dashboard files

CHANGED_FILES=$(git diff --cached --name-only)

# Only validate if dashboard files are being committed
if echo "$CHANGED_FILES" | grep -qE '(system-state\.json|kenetik-growth-system-dashboard\.html|system-state-definitions\.json)'; then
    echo "🔍 Running KGS dashboard validation..."
    python3 validate-dashboard.py
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ Commit blocked: dashboard validation failed."
        echo "Fix the errors above before committing."
        echo "To skip (emergency only): git commit --no-verify"
        exit 1
    fi
    echo ""
fi
HOOK

chmod +x "$HOOK_FILE"
echo "✅ Pre-commit hook installed at $HOOK_FILE"
