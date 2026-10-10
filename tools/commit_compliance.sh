#!/bin/bash
# ENCHDASH Compliance Commit Helper
#
# Validates and previews only. NEVER stages, commits, or pushes by default.
# Owner approval is REQUIRED before any staging, committing, or pushing.
#
# Usage:
#   bash tools/commit_compliance.sh          # validate + allowlist-check + preview (default, non-committing)
#   bash tools/commit_compliance.sh --check  # status + allowlist check only (no validation, no prompts)
#   bash tools/commit_compliance.sh --stage  # allowlisted staging only (after checks pass; still no commit/push)
#
# Run from repository root.

set -eu
export GIT_PAGER=cat
# Also avoid pager issues on all git invocations.

# --- Allowlist (defined ONCE; used for path-check AND staged-file staging) ---
ALLOWLIST=(
  "AGENTS.md"
  "CHANGELOG.md"
  "LICENSE"
  "THIRD_PARTY_NOTICES.md"
  "README.md"
  "QUICKSTART.md"
  "FIRMWARE/README.md"
  "FIRMWARE/manifest.json"
  "docs/DEPLOYMENT-REPORT.md"
  "docs/IMPLEMENTATION-SUMMARY.md"
  "docs/LEGACY-SUPPORT.md"
  "docs/HARDWARE-ATTRIBUTION.md"
  "docs/RELEASE-CHECKLIST.md"
  "docs/SILKSCREEN-GUIDE.md"
  "docs/evidence/kicad-owner-verification.md"
  "docs/evidence/qmk-build.md"
  "docs/evidence/review-remediation.md"
  "tools/verify_repository.py"
  "tools/commit_compliance.sh"
  "tests/test_verify_repository.py"
)

# --- Colors for output ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Check if we're in repo root ---
if [ ! -d ".git" ]; then
  echo -e "${RED}Error: Must run from repository root${NC}"
  exit 1
fi

# --- Parse mode ---
MODE="default"
if [ "$1" = "--check" ] || [ "$1" = "--status" ]; then
  MODE="check"
elif [ "$1" = "--stage" ]; then
  MODE="stage"
fi

# --- Collect all changed paths across modified, untracked, and staged ---
# Sets: modified tracked + untracked (exclude-standard) + staged
set +e
CHANGED_PATHS=$(
  git diff --name-only 2>/dev/null
  git ls-files --others --exclude-standard 2>/dev/null
  git diff --cached --name-only 2>/dev/null
)
CHANGED_PATHS=$(echo "$CHANGED_PATHS" | grep -v '^$' | awk '!seen[$0]++')
set -e

# --- Allowlist check (runs BEFORE any staging; gates the exit) ---
# Returns 0 only if no non-allowlisted paths exist or (in check/status mode)
# prints the status. Collects violations into VIOLATIONS.
check_allowlist() {
  local violations=0
  local found=()
  if [ -n "$CHANGED_PATHS" ]; then
    while IFS= read -r f; do
      [ -z "$f" ] && continue
      local ok=0
      for a in "${ALLOWLIST[@]}"; do
        if [ "$f" = "$a" ]; then
          ok=1
          break
        fi
      done
      if [ "$ok" -ne 1 ]; then
        found+=("$f")
        violations=1
      fi
    done <<< "$CHANGED_PATHS"
  fi
  if [ "$violations" -ne 0 ]; then
    echo -e "${RED}ALLOWLIST VIOLATION: non-allowlisted files detected:${NC}"
    for f in "${found[@]}"; do
      echo -e "  ${RED}- $f${NC}"
    done
    echo ""
    echo -e "${YELLOW}These files are outside the allowlist and MUST NOT be staged or committed.${NC}"
    echo -e "${YELLOW}Remove them or obtain owner approval before proceeding.${NC}"
    return 1
  fi
  return 0
}

# ===================================================
echo "=================================================="
echo "ENCHDASH Compliance Implementation"
echo "Validation & Preview Script (owner approval required)"
echo "=================================================="
echo ""

# --- Show current branch ---
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
echo -e "Current branch: ${GREEN}${BRANCH}${NC}"

# --- Show uncommitted changes count ---
CHANGED=$(git status --short 2>/dev/null | wc -l | tr -d ' ')
echo -e "Uncommitted changes: ${YELLOW}${CHANGED} files${NC}"
echo ""

# --- Show what's changed ---
echo "Changed files:"
git status --short
echo ""

# --- Run allowlist check FIRST (gates staging and exit) ---
echo -e "${BLUE}Step 1: Allowlist Check${NC}"
echo "========================"
echo ""
echo "Allowlisted paths (${#ALLOWLIST[@]}):"
printf '  %s\n' "${ALLOWLIST[@]}"
echo ""
if ! check_allowlist; then
  echo -e "${RED}Allowlist check FAILED.${NC}"
  echo -e "${YELLOW}This script validates and previews only. No files have been staged, committed, or pushed.${NC}"
  echo -e "${YELLOW}Owner approval is required before any staging, committing, or pushing.${NC}"
  exit 1
fi
echo -e "${GREEN}✓ Allowlist check passed — all changed files are within the allowlist.${NC}"
echo ""

# --- In check/status mode, stop here (no validation, no prompts, no staging) ---
if [ "$MODE" = "check" ]; then
  echo -e "${BLUE}Status mode: stopping after allowlist check.${NC}"
  echo -e "${YELLOW}This script validates and previews only. No files have been staged, committed, or pushed.${NC}"
  echo -e "${YELLOW}Owner approval is required before any staging, committing, or pushing.${NC}"
  exit 0
fi

# --- Step 2: Validation (only in default/stage modes) ---
echo -e "${BLUE}Step 2: Validation${NC}"
echo "==================="
echo ""

echo "Running repository integrity validator..."
if python tools/verify_repository.py; then
  echo -e "${GREEN}✓ Validation passed${NC}"
else
  echo -e "${RED}✗ Validation failed - please fix issues before committing${NC}"
  echo -e "${YELLOW}Owner approval is required before any staging, committing, or pushing.${NC}"
  exit 1
fi
echo ""

# Run unit tests
echo "Running unit tests..."
if python tests/test_verify_repository.py > /dev/null 2>&1; then
  echo -e "${GREEN}✓ All tests passed${NC}"
else
  echo -e "${RED}✗ Tests failed - please investigate${NC}"
  echo -e "${YELLOW}Owner approval is required before any staging, committing, or pushing.${NC}"
  exit 1
fi
echo ""

# --- Step 3: Review Checklist ---
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
echo -e "${YELLOW}Owner approval is required before any staging, committing, or pushing.${NC}"
echo ""

# --- Step 4: Commit Preview ---
echo -e "${BLUE}Step 4: Commit Preview${NC}"
echo "======================"
echo ""

cat << 'EOF'
Suggested commit message (requires owner approval before use):

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
- Legacy artifacts preserved; physical compatibility and build provenance remain evidence-bounded.
- Legacy product name preserved in documentation

## Validation
- All integrity checks pass
- Unit tests pass
- Firmware hashes verified

Refs: docs/superpowers/plans/2026-10-08-enchdash-remediation-plan.md
---
EOF

# --- Step 5: Stage allowlisted files (only with explicit --stage flag) ---
if [ "$MODE" = "stage" ]; then
  echo -e "${BLUE}Step 5: Allowlisted Staging${NC}"
  echo "==========================="
  echo ""
  echo "Staging allowlisted modified/untracked files only..."
  staged=0
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    ok=0
    for a in "${ALLOWLIST[@]}"; do
      if [ "$f" = "$a" ]; then
        ok=1
        break
      fi
    done
    if [ "$ok" -eq 1 ] && [ -e "$f" ]; then
      echo "  Staged: $f"
      git add "$f"
      staged=1
    fi
  done <<< "$CHANGED_PATHS"
  if [ "$staged" -eq 0 ]; then
    echo -e "${YELLOW}No allowlisted modified/untracked files to stage.${NC}"
  else
    echo ""
    echo "Staged files:"
    git diff --cached --name-only
  fi
  echo ""
  echo -e "${YELLOW}Files are staged but NOT committed. Owner approval required before committing or pushing.${NC}"
fi

# --- Final summary (review-only; owner approval required) ---
echo ""
echo "=================================================="
echo "Validation & preview complete."
echo "=================================================="
echo ""
echo -e "${YELLOW}This script validates and previews only.${NC}"
echo -e "${YELLOW}No files were committed or pushed (default mode).${NC}"
echo -e "${YELLOW}Owner approval is required before staging, committing, or pushing.${NC}"
echo ""
echo "Next steps (require owner approval):"
echo "  1. Review the diff: git diff"
echo "  2. (Optional) Stage allowlisted files: bash tools/commit_compliance.sh --stage"
echo "  3. Commit: git commit (only after owner approval)"
echo "  4. Push to remote (only after owner approval)"
