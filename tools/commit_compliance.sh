#!/bin/bash
# ENCHDASH Compliance Commit Helper
# 
# This script helps the owner review and commit the compliance changes.
# Run from repository root: bash tools/commit_compliance.sh

set -e

echo "=================================================="
echo "ENCHDASH Compliance Implementation"
echo "Commit Preparation Script"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in repo root
if [ ! -d ".git" ]; then
    echo -e "${RED}Error: Must run from repository root${NC}"
    exit 1
fi

echo -e "${BLUE}Step 1: Repository Status Check${NC}"
echo "=================================="
echo ""

# Show current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo -e "Current branch: ${GREEN}${BRANCH}${NC}"

# Show uncommitted changes count
CHANGED=$(git status --short | wc -l)
echo -e "Uncommitted changes: ${YELLOW}${CHANGED} files${NC}"
echo ""

# Show what's changed
echo "Changed files:"
git status --short
echo ""

echo -e "${BLUE}Step 2: Validation${NC}"
echo "==================="
echo ""

# Run validator
echo "Running repository integrity validator..."
if python tools/verify_repository.py; then
    echo -e "${GREEN}✓ Validation passed${NC}"
else
    echo -e "${RED}✗ Validation failed - please fix issues before committing${NC}"
    exit 1
fi
echo ""

# Run unit tests
echo "Running unit tests..."
if python tests/test_verify_repository.py > /dev/null 2>&1; then
    echo -e "${GREEN}✓ All tests passed${NC}"
else
    echo -e "${RED}✗ Tests failed - please investigate${NC}"
    exit 1
fi
echo ""

echo -e "${BLUE}Step 3: Review Checklist${NC}"
echo "========================"
echo ""

echo "Please confirm you have reviewed:"
echo "  [ ] README.md - ENCHDASH identity and attribution"
echo "  [ ] LICENSE - Multi-license structure correct"
echo "  [ ] CHANGELOG.md - Change history complete"
echo "  [ ] FIRMWARE/manifest.json - Firmware hashes correct"
echo "  [ ] docs/LEGACY-SUPPORT.md - Legacy policy acceptable"
echo "  [ ] docs/HARDWARE-ATTRIBUTION.md - Attribution accurate"
echo ""

read -p "Have you reviewed all files? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Please review files before committing.${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}Step 4: Commit Preview${NC}"
echo "======================"
echo ""

cat << 'EOF'
Suggested commit message:

---
feat: ENCHDASH compliance and identity remediation

Add comprehensive licensing, attribution, and provenance tracking
for ENCHDASH (formerly ERGODASH-MOD-ENCH-OLED-QMK_VIA).

## Changes
- Add LICENSE index and full license texts (MIT hardware, GPL firmware)
- Create firmware provenance manifest with SHA-256 checksums
- Establish legacy support documentation for existing units
- Add repository integrity validator and unit tests
- Rebrand README to ENCHDASH with prominent omkbd attribution
- Document hardware modifications and attribution chain
- Create release checklist and KiCad silkscreen guide

## Compatibility
- No hardware changes
- No firmware changes
- Existing units remain fully supported
- Legacy product name preserved in documentation

## Validation
- All integrity checks pass
- 14 unit tests pass
- Firmware hashes verified

Refs: docs/superpowers/plans/2026-10-08-enchdash-remediation-plan.md
---
EOF

echo ""
echo -e "${BLUE}Step 5: Commit Options${NC}"
echo "======================"
echo ""

echo "Choose an option:"
echo "  1) Stage all files and show diff (review before commit)"
echo "  2) Stage all files and commit with suggested message"
echo "  3) Stage all files and commit with custom message"
echo "  4) Exit without committing"
echo ""

read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "Staging all files..."
        git add -A
        echo -e "${GREEN}Files staged.${NC}"
        echo ""
        echo "Showing diff..."
        git diff --cached --stat
        echo ""
        echo "Run 'git diff --cached' to see full diff"
        echo "Run 'git commit' when ready to commit"
        ;;
    2)
        echo ""
        echo "Staging all files..."
        git add -A
        echo ""
        echo "Creating commit..."
        git commit -F - << 'EOF'
feat: ENCHDASH compliance and identity remediation

Add comprehensive licensing, attribution, and provenance tracking
for ENCHDASH (formerly ERGODASH-MOD-ENCH-OLED-QMK_VIA).

## Changes
- Add LICENSE index and full license texts (MIT hardware, GPL firmware)
- Create firmware provenance manifest with SHA-256 checksums
- Establish legacy support documentation for existing units
- Add repository integrity validator and unit tests
- Rebrand README to ENCHDASH with prominent omkbd attribution
- Document hardware modifications and attribution chain
- Create release checklist and KiCad silkscreen guide

## Compatibility
- No hardware changes
- No firmware changes
- Existing units remain fully supported
- Legacy product name preserved in documentation

## Validation
- All integrity checks pass
- 14 unit tests pass
- Firmware hashes verified

Refs: docs/superpowers/plans/2026-10-08-enchdash-remediation-plan.md
EOF
        echo -e "${GREEN}✓ Commit created${NC}"
        echo ""
        echo "Next steps:"
        echo "  1. Review commit: git show"
        echo "  2. Push to GitHub: git push origin ${BRANCH}"
        echo "  3. Verify on GitHub"
        ;;
    3)
        echo ""
        echo "Staging all files..."
        git add -A
        echo ""
        echo "Opening editor for commit message..."
        git commit
        ;;
    4)
        echo ""
        echo -e "${YELLOW}Exiting without committing.${NC}"
        echo "Files remain unstaged."
        exit 0
        ;;
    *)
        echo ""
        echo -e "${RED}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac

echo ""
echo "=================================================="
echo "Commit preparation complete!"
echo "=================================================="
