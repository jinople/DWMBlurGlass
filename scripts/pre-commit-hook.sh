#!/bin/bash
# Pre-commit hook for DWMBlurGlass security scanning
# 
# To install this hook:
# cp scripts/pre-commit-hook.sh .git/hooks/pre-commit
# chmod +x .git/hooks/pre-commit

echo "Running security scan before commit..."

# Run security scanner
python3 scripts/security-scan.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Security scan detected potential issues!"
    echo "   Review the warnings above before committing."
    echo ""
    echo "To bypass this check (not recommended):"
    echo "  git commit --no-verify"
    echo ""
    exit 1
fi

echo "✅ Security scan passed"
exit 0
