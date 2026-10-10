# ENCHDASH Review Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Correct unsupported compliance, compatibility, provenance, and release claims; make repository validation match its documented contract; preserve all shipped firmware, VIA JSON, QMK source, and KiCad files byte-for-byte.

**Architecture:** Keep the existing Python validator as the single local integrity gate. It resolves every manifest path from the repository root, validates manifest structure and local links, and reports only observable repository facts. Documentation separates verified repository evidence, owner-supplied evidence, and unknown provenance; release and deployment documents cannot claim completion until firmware, hardware, link, and owner-approval gates have evidence.

**Tech Stack:** Python 3 standard library, `unittest`, Bash, Markdown, JSON, existing QMK/VIA/KiCad artifacts. No new dependency.

---

## Scope and Non-Goals

- Preserve unchanged: `FIRMWARE/*.hex`, `FIRMWARE/QMK/**`, all VIA JSON files, `Hardware/**`, `DOC/**`, and existing legacy download paths.
- Modify only documentation, validator/tests, and the commit helper listed below.
- Do not assign a new VID/PID, create a future firmware target, build firmware, edit KiCad, rename the GitHub repository, push, publish, contact customers, or make marketplace changes in this remediation.
- Treat `tests/__pycache__/` as unrelated working-tree state; do not stage or delete it unless the owner separately requests cleanup.
- A successful local validator proves repository consistency only. It does not prove legal compliance, firmware reproducibility, hardware compatibility, manufacturing quality, or external URL availability.

## Review Findings Mapped to Tasks

| Finding | Remediation task |
|---|---|
| Unsupported “production-ready/fully compliant/deployed” claims | Tasks 4 and 7 |
| Unsupported third-party licenses and ownership assertions | Task 5 |
| Rev1.2/sold-unit compatibility overclaim | Task 3 |
| Hardware attribution overclaims and I²C/serial conflation | Task 5 |
| Validator paths depend on current working directory | Task 1 |
| Validator contract incomplete | Tasks 1 and 2 |
| Missing owner KiCad evidence file | Task 6 |
| HEX file size presented as flash usage; unverified build claims | Task 3 and Task 7 |
| Broken firmware-guide link | Task 3 |
| Rollback instructions delete compliance history | Task 7 |
| `git add -A` stages unrelated work | Task 8 |
| Release checklist lacks owner-approval gate | Task 6 |
| GitHub/link verification claimed without evidence | Tasks 6 and 9 |

## File Map

- Modify `tools/verify_repository.py`: root-independent path resolution, manifest schema checks, required evidence paths, local Markdown link checking, truthful validator output.
- Modify `tests/test_verify_repository.py`: tests for root-independent paths, manifest contract, required evidence, and local links.
- Modify `README.md`, `FIRMWARE/README.md`, `docs/LEGACY-SUPPORT.md`: distinguish repository-source mapping from physical compatibility and build provenance; fix links and feature wording.
- Modify `docs/HARDWARE-ATTRIBUTION.md`, `THIRD_PARTY_NOTICES.md`: remove unsupported technical/license/ownership assertions and label unknowns.
- Modify `docs/DEPLOYMENT-REPORT.md`, `docs/IMPLEMENTATION-SUMMARY.md`, `QUICKSTART.md`, `CHANGELOG.md`: convert completion claims and unsafe release/rollback instructions into historical, evidence-bounded guidance.
- Modify `docs/RELEASE-CHECKLIST.md`, `docs/SILKSCREEN-GUIDE.md`: add hard evidence and owner-approval gates; remove fake checked evidence.
- Create `docs/evidence/kicad-owner-verification.md`: unchecked owner evidence checklist.
- Modify `tools/commit_compliance.sh`: allowlist changed paths and prevent accidental staging.
- Create `docs/evidence/review-remediation.md`: record observed validation results and any still-blocked external/device evidence.

---

### Task 1: Make validator path resolution repository-root independent

**Files:**
- Modify: `tools/verify_repository.py:52-153,211-220`
- Modify: `tests/test_verify_repository.py:63-218`

- [ ] **Step 1: Add a failing relative-path test.**

Create a fixture with this structure inside `TemporaryDirectory()`:

```text
repo/
  FIRMWARE/manifest.json
  FIRMWARE/test.hex
  VIA/test.json
```

Use manifest values `"path": "FIRMWARE/test.hex"` and `"via_json": "VIA/test.json"`. Call `check_manifest_hashes(repo / "FIRMWARE/manifest.json")` and `check_usb_identity_consistency(repo / "FIRMWARE/manifest.json")` after changing the process CWD to a separate temporary directory. Assert both return `(True, [])`.

- [ ] **Step 2: Run the focused test and confirm failure.**

Run:

```bash
python -m unittest tests.test_verify_repository.TestManifestHashValidation tests.test_verify_repository.TestUSBIdentityConsistency -v
```

Expected before implementation: the new relative-path test fails because `Path(path_str)` is resolved against the caller CWD.

- [ ] **Step 3: Resolve manifest references from the repository root.**

Add one helper near the existing hash helper:

```python
def manifest_repo_root(manifest_path: Path) -> Path:
    return manifest_path.resolve().parents[1]


def repo_path(repo_root: Path, relative_path: str) -> Path:
    path = Path(relative_path)
    return path if path.is_absolute() else repo_root / path
```

In `check_manifest_hashes` and `check_usb_identity_consistency`, compute `repo_root = manifest_repo_root(manifest_path)` and resolve `path`/`via_json` through `repo_path`. Keep absolute fixture paths supported. In `main`, continue passing the resolved `FIRMWARE/manifest.json`; do not use `Path.cwd()`.

- [ ] **Step 4: Run focused tests and the validator from another CWD.**

Run from the repository root:

```bash
python -m unittest tests.test_verify_repository.TestManifestHashValidation tests.test_verify_repository.TestUSBIdentityConsistency -v
```

Then run from a separate directory:

```bash
python D:/Pribadi/ERGODASH-MOD-ENCH-OLED-QMK_VIA/tools/verify_repository.py
```

Expected: focused tests pass and the validator locates `FIRMWARE/*.hex` and VIA JSON files without relying on the current directory.

- [ ] **Step 5: Commit only the validator path change and tests.**

```bash
git add tools/verify_repository.py tests/test_verify_repository.py
git commit -m "fix: resolve validator paths from repository root"
```

Do not commit if the owner has not authorized commits; leave the command as the execution operator's checkpoint.

---

### Task 2: Enforce the validator's actual manifest, evidence, and link contract

**Files:**
- Modify: `tools/verify_repository.py:52-180,211-309`
- Modify: `tests/test_verify_repository.py:63-310`
- Modify: `docs/evidence/review-remediation.md`

- [ ] **Step 1: Add failing contract tests.**

Add tests for these observable behaviors:

```python
def test_manifest_rejects_invalid_sha256_and_status(self):
    # A 64-character lowercase hexadecimal SHA-256 and one of
    # incomplete, functionally rebuilt, or verified are required.
    valid, errors = validate_manifest(repo_root, manifest)
    self.assertFalse(valid)
    self.assertTrue(any("sha256" in error.lower() for error in errors))
    self.assertTrue(any("provenance_status" in error for error in errors))


def test_required_files_include_release_and_owner_evidence(self):
    # Omitting docs/evidence/kicad-owner-verification.md must fail.
    valid, errors = check_required_files(repo_root)
    self.assertFalse(valid)
    self.assertTrue(any("kicad-owner-verification.md" in error for error in errors))


def test_markdown_links_reject_missing_local_targets(self):
    # A relative target with no file must fail; https:// and #anchor targets pass.
    valid, errors = check_local_markdown_links(repo_root, [repo_root / "README.md"])
    self.assertFalse(valid)
    self.assertTrue(any("missing local link" in error.lower() for error in errors))
```

Use fixture paths under the temporary repository root. Do not test network access in unit tests.

- [ ] **Step 2: Run the new tests and confirm failure.**

```bash
python -m unittest tests.test_verify_repository -v
```

Expected before implementation: new symbols or required evidence checks are absent, so the added tests fail.

- [ ] **Step 3: Implement explicit manifest validation.**

Add constants:

```python
VALID_PROVENANCE = {"incomplete", "functionally rebuilt", "verified"}
REQUIRED_ARTIFACT_FIELDS = {
    "path", "sha256", "hardware_revision", "source_path",
    "via_json", "qmk_base_commit", "source_commit",
    "build_command", "provenance_status",
}
```

Implement `validate_manifest(repo_root, manifest)` with these checks:

1. Root is an object containing `schema_version`, `usb_identity`, and a non-empty `artifacts` list.
2. `usb_identity.vid` and `.pid` are strings matching `0x` plus four hexadecimal digits.
3. Each artifact is an object containing every field in `REQUIRED_ARTIFACT_FIELDS`.
4. `sha256` matches `^[0-9a-f]{64}$`.
5. `provenance_status` is exactly one of `incomplete`, `functionally rebuilt`, or `verified`.
6. `path`, `source_path`, and `via_json` are relative repository paths; the artifact file, source directory, and VIA JSON file exist.
7. `qmk_base_commit`, `source_commit`, and `build_command` may be `null` only when status is `incomplete`; a non-incomplete artifact must contain non-empty strings for all three.
8. A manifest row's VIA JSON has `vendorId` and `productId` matching normalized manifest VID/PID.

Return all errors; do not raise on malformed user data. Keep `check_manifest_hashes` and `check_usb_identity_consistency` as compatibility wrappers used by existing tests, with `validate_manifest` called by `main`.

- [ ] **Step 4: Add required evidence and local Markdown link checks.**

Extend `required_files` with:

```text
docs/RELEASE-CHECKLIST.md
docs/SILKSCREEN-GUIDE.md
docs/evidence/kicad-owner-verification.md
docs/evidence/qmk-build.md
docs/evidence/review-remediation.md
```

Implement `check_local_markdown_links(repo_root, markdown_files)` using only the standard library. Parse Markdown destinations with a conservative regex, skip `https://`, `http://`, `mailto:`, and `#anchor` destinations, strip an optional fragment, URL-decode the path, and resolve it relative to the Markdown file's parent. Check files and directories with `.exists()`. Report `missing local link: <source> -> <target>`.

Check only maintained public documents, not historical plan/spec files:

```text
README.md
QUICKSTART.md
FIRMWARE/README.md
LICENSE.md if present
THIRD_PARTY_NOTICES.md
docs/LEGACY-SUPPORT.md
docs/HARDWARE-ATTRIBUTION.md
docs/RELEASE-CHECKLIST.md
docs/SILKSCREEN-GUIDE.md
docs/DEPLOYMENT-REPORT.md
docs/IMPLEMENTATION-SUMMARY.md
```

If a maintained document contains a deliberately historical or template-only link, make that explicit in the document and exclude only that file from the active list with a code comment explaining why.

- [ ] **Step 5: Update validator output and entrypoint.**

Change the docstring from “Link integrity (basic checks)” to the exact checks performed: manifest hashes, manifest schema and local paths, USB/VIA consistency, required files, license markers, JSON syntax, and local Markdown targets. Add a sixth printed section for local links or combine it with required-file validation, but keep section labels aligned with actual checks. `--manifest-only` must run manifest schema and hash checks but may skip links and documentation checks.

- [ ] **Step 6: Run all validator tests and record evidence.**

```bash
python -m unittest tests.test_verify_repository -v
python tools/verify_repository.py --verbose
python -m json.tool FIRMWARE/manifest.json > NUL
```

Expected: all tests pass; validator reports no missing local targets; JSON exits 0. Record date, command, and output summary in `docs/evidence/review-remediation.md`. Do not claim external URL, build, USB enumeration, VIA device, or KiCad evidence here.

---

### Task 3: Correct firmware and compatibility documentation

**Files:**
- Modify: `README.md:51-73,230-270`
- Modify: `FIRMWARE/README.md:7-35,143-197,313-333`
- Modify: `docs/LEGACY-SUPPORT.md:20-65`
- Preserve: all `FIRMWARE/*.hex`, `FIRMWARE/QMK/**`, and VIA JSON files.

- [ ] **Step 1: Replace physical-compatibility assertions with evidence-bounded wording.**

In `README.md` and `FIRMWARE/README.md`, replace “Current production”, “all built for Rev1.2 hardware”, and “All work with Rev1.2 hardware” with wording equivalent to:

```text
The repository maps these artifacts to Rev1.2 source files. Physical sold-unit
marking and compatibility are not independently evidenced here. Confirm the
PCB marking and matching VIA definition before flashing; do not cross-flash an
unconfirmed revision.
```

Keep the exact USB VID/PID as a recorded legacy descriptor/VIA value, but state that its allocation provenance remains under audit.

- [ ] **Step 2: Keep only source-confirmed feature claims.**

Retain encoder, OLED, RGB, mouse-key, WPM, VIA, and NKRO feature descriptions only where the corresponding `rules.mk`, `config.h`, or keymap confirms them. Change “Flash size” from `~77.7 KB`/`~78.5 KB` to `HEX container size; not compiler flash usage` or remove the column. Remove the statement that enabling both features definitely exceeds the flash limit unless a QMK compile output proves it; replace it with “Do not publish a combined variant until a size report proves it fits.”

- [ ] **Step 3: Correct build instructions.**

State that no current legacy artifact has a proven QMK base commit or reproducible build command. Point readers to `docs/evidence/qmk-build.md` for the blocked baseline procedure. Correct the WPM instructions to refer to the actual variant-specific `rules.mk` (`WPM_ENABLE = yes`) rather than instructing users to add a config define. Keep build commands as an unverified procedure, not as evidence that the shipped binaries can be reproduced.

- [ ] **Step 4: Fix links and legacy wording.**

Change `FIRMWARE/README.md` line 319 from `[docs/LEGACY-SUPPORT.md](LEGACY-SUPPORT.md)` to `[Legacy support](../docs/LEGACY-SUPPORT.md)`. Replace “fully supported” with “legacy downloads and matching VIA JSON remain available; physical compatibility and historical build provenance must be confirmed before new flashing.” Keep the legacy product name searchable.

- [ ] **Step 5: Run focused documentation checks.**

```bash
python tools/verify_repository.py
python -m unittest tests.test_verify_repository -v
```

Expected: the local link check passes and no active statement in these three files claims official endorsement, reproducible builds, physical compatibility, or measured flash usage without evidence.

---

### Task 4: Correct deployment and implementation status claims

**Files:**
- Modify: `docs/DEPLOYMENT-REPORT.md:1-7,25-65,104-147,410-439`
- Modify: `docs/IMPLEMENTATION-SUMMARY.md:1-24,76-100,130-145,283-355`
- Modify: `QUICKSTART.md:1-15,53-90,93-151,184-200`

- [ ] **Step 1: Reframe reports as historical documentation work, not a compliance certification.**

Use this status contract in both reports:

```text
Status: Documentation and repository-integrity baseline recorded; full
firmware, hardware, provenance, external-link, and owner-approval gates remain
open.
```

Retain factual historical commit/hash information only when it describes the prior repository history. Remove or change “DEPLOYED TO PRODUCTION”, “fully compliant”, “production-ready”, “ALL PASS”, “100% backward compatibility”, and “legacy support guaranteed”. Replace checked boxes for unperformed GitHub, external-link, device, QMK, and KiCad checks with unchecked boxes or `Not verified`.

- [ ] **Step 2: Distinguish local validation from blocked gates.**

The reports may claim only observed local results: manifest hashes match, JSON syntax is valid, required local files exist, and Python unit tests pass. Add an explicit table:

| Gate | Status | Evidence |
|---|---|---|
| Local repository integrity | `verified when validator passes` | `tools/verify_repository.py` output |
| Legacy binary reproducibility | `incomplete` | `FIRMWARE/manifest.json`, `docs/evidence/qmk-build.md` |
| Physical firmware compatibility | `not verified` | owner/device evidence required |
| KiCad/ERC/DRC/first article | `not verified` | `docs/evidence/kicad-owner-verification.md` |
| External links/GitHub rendering | `not verified locally` | owner/browser verification required |

- [ ] **Step 3: Remove unsafe Quick Start actions.**

Change `QUICKSTART.md` so the first action is review and local validation. Remove instructions that stage all files, push to `main`, reset hard, force-push, or call compliance achieved. Replace with:

```text
Do not commit or push from this guide. Review `git status --short`, run the
validator and tests, inspect the allowlisted diff, then obtain owner approval
for any commit or public action.
```

- [ ] **Step 4: Correct rollback language.**

Use `git revert <commit>` as the normal rollback. State that rollback must preserve Git history, license files, evidence, legacy binaries, and VIA JSON. Do not recommend `git reset --hard`, force-push, deleting compliance documents, or restoring an old README without an owner-approved compatibility review.

- [ ] **Step 5: Validate wording and links.**

```bash
python tools/verify_repository.py
```

Expected: local links pass and no active report/quickstart conclusion claims full compliance or production readiness.

---

### Task 5: Bound hardware attribution and third-party notices

**Files:**
- Modify: `docs/HARDWARE-ATTRIBUTION.md:27-99,122-171,191-208`
- Modify: `THIRD_PARTY_NOTICES.md:1-66,82-87`

- [ ] **Step 1: Split hardware statements by evidence class.**

Rewrite `docs/HARDWARE-ATTRIBUTION.md` headings to distinguish:

1. `Repository evidence`: paths and source values directly visible in the current repository, such as QMK encoder/OLED/RGB flags and pin definitions.
2. `Owner/hardware evidence required`: physical hotswap population, exact PCB routing, sold-unit revision, mounting-hole identity, case ancestry, ERC/DRC, silkscreen, and first-article results.
3. `Historical attribution`: omkbd/ErgoDash source and license, stated without implying endorsement.

Remove or qualify “original ErgoDash Rev2”, “electrical design unchanged”, “switch layout unchanged”, “mounting holes unchanged”, and “case not derived” unless the specific schematic/PCB/source evidence is cited. Replace the incorrect sentence about OLED communicating “via I²C on split keyboard serial line” with:

```text
The firmware enables QMK OLED support and split-display behavior. The current
repository does not establish that the OLED electrical bus is the split serial
transport; confirm the bus and routing from the KiCad schematic before making
that claim.
```

- [ ] **Step 2: Keep firmware statements source-grounded.**

Describe exact files and symbols (`rules.mk`, `config.h`, `keymap.c`, `oled.c`, `info.json`) without claiming a successful build or device behavior. Mark USB VID/PID provenance and source-to-binary identity as incomplete, matching `FIRMWARE/manifest.json`.

- [ ] **Step 3: Convert third-party inventory to an evidence ledger.**

Change the table so each row has `Claimed source`, `License status`, `Usage status`, and `Evidence`. For every item without a local license or verified usage report, use:

```text
License status: not independently established
Usage status: not established
Evidence: owner/KiCad audit required before distribution claim
```

Do not label VIA JSON as GPL merely because firmware is GPL. Do not label photos, videos, manuals, or schematic PDFs as owner-created/licensed unless that is explicitly owner-confirmed; use `owner attribution not independently verified`. Keep confirmed local license-file references only for files actually present and attributable.

- [ ] **Step 4: Update compliance notes.**

State that unknown provenance blocks a clean asset-level compliance claim. Do not state that all referenced licenses are included when the inventory itself identifies unresolved assets. Preserve omkbd and QMK attribution and the existing license files.

- [ ] **Step 5: Run local validation.**

```bash
python tools/verify_repository.py
```

Expected: no broken local links and no active unsupported license/endorsement claims in maintained attribution files.

---

### Task 6: Add owner evidence and hard release gates

**Files:**
- Create: `docs/evidence/kicad-owner-verification.md`
- Modify: `docs/RELEASE-CHECKLIST.md:1-292`
- Modify: `docs/SILKSCREEN-GUIDE.md:270-327`

- [ ] **Step 1: Create the unchecked KiCad evidence file.**

Create exactly this initial content, with no checked evidence:

```markdown
# KiCad Owner Verification

**Status:** Not verified. No owner-supplied KiCad or manufacturing evidence is recorded in this repository.

- [ ] KiCad title-block screenshot attached or linked.
- [ ] Front Gerber screenshot attached or linked.
- [ ] Back Gerber screenshot attached or linked.
- [ ] ERC result recorded.
- [ ] DRC result recorded.
- [ ] No silkscreen overlaps pads, exposed copper, mask openings, cuts, holes, or keepouts.
- [ ] Text remains visible after assembly.
- [ ] First-article production photo attached or linked.
- [ ] Evidence reviewer and date recorded.

Evidence may be checked only after the owner supplies the referenced artifacts and their paths or URLs.
```

- [ ] **Step 2: Remove fake evidence from the silkscreen guide.**

Keep the guide as instructions and template only. Remove checked marks, fake screenshot paths under `screenshots/`, `[Viewer name]`, and “Errors: 0” claims. Point the guide to `docs/evidence/kicad-owner-verification.md` for actual evidence. Keep the prohibited marking list and state that revision, URL, title block, and manufacturing markings require owner confirmation.

- [ ] **Step 3: Add release gates.**

`docs/RELEASE-CHECKLIST.md` must explicitly separate:

- local repository checks;
- legacy binary hash and manifest checks;
- QMK build/source evidence;
- USB enumeration and VIA device test;
- KiCad owner ERC/DRC/Gerber/first-article evidence;
- local and external link verification;
- rollback artifact preservation;
- explicit owner approval before repository rename, release, customer message, marketplace edit, or push.

Replace `Known Issues: None` with `Known Issues: unresolved provenance, unverified builds/device/hardware evidence until their gates pass`. Mark sample hashes as illustrative template values, never as observed results.

- [ ] **Step 4: Run required-file and local-link checks.**

```bash
python tools/verify_repository.py
```

Expected: the new owner-evidence file satisfies required-file validation; no template image link remains in maintained documents unless the file exists.

---

### Task 7: Correct changelog and future-build evidence wording

**Files:**
- Modify: `CHANGELOG.md:71-95,110-125`
- Modify: `docs/evidence/qmk-build.md:1-175`
- Modify: `FIRMWARE/manifest.json` only if observed evidence changes a field; otherwise preserve current `null` provenance fields.
- Create/modify: `docs/evidence/review-remediation.md`

- [ ] **Step 1: Make rollback safe and non-destructive.**

Replace the rollback section with:

```text
Normal rollback: create an owner-approved `git revert` commit for the specific
change, preserve all Git history and legacy artifacts, then verify local links,
hashes, and customer download paths. Do not use force-push, `reset --hard`, or
remove license/provenance/evidence files as a rollback method.
```

- [ ] **Step 2: Mark build evidence as blocked, not optional completion.**

Keep `docs/evidence/qmk-build.md` as a procedure, but change “optional” and “current shipped firmware remains fully supported” wording to:

```text
Status: incomplete. The repository records shipped binary hashes and source
mappings, but no QMK base commit, reproducible build, USB enumeration, VIA
device test, or hardware smoke test has been evidenced here.
```

The procedure must require exact QMK commit, compiler/toolchain details, command, output path, artifact hash, and—if hashes differ—documented device behavior tests before setting `verified` or `functionally rebuilt`.

- [ ] **Step 3: Keep the manifest honest.**

Do not fill `qmk_base_commit`, `source_commit`, or `build_command` with guesses. Keep `provenance_status: incomplete` until the evidence procedure produces the required facts. If a future verified build occurs, update only the matching artifact row and attach command/output evidence.

- [ ] **Step 4: Record remediation evidence.**

Create `docs/evidence/review-remediation.md` with:

```markdown
# Review Remediation Evidence

**Status:** Local documentation and validator remediation pending execution.

## Local checks

- [ ] `python -m unittest discover -s tests -v` output attached or summarized.
- [ ] `python tools/verify_repository.py --verbose` output attached or summarized.
- [ ] Validator run from a different CWD.
- [ ] Maintained Markdown local-link check passes.

## Not established by local checks

- QMK historical base commit and reproducible legacy builds.
- USB enumeration and VIA detection on physical hardware.
- Key, encoder, OLED, RGB, split, and reset smoke test.
- KiCad ERC/DRC, Gerber, silkscreen, and first-article evidence.
- External URL response and GitHub rendering verification.
- Owner approval for commit, rename, release, or customer communication.
```

Do not check items until the corresponding output or owner evidence is attached.

---

### Task 8: Prevent accidental staging of unrelated files

**Files:**
- Modify: `tools/commit_compliance.sh:36-43,46-67,129-220`
- Modify: `QUICKSTART.md` if it still recommends `git add -A`

- [ ] **Step 1: Add an allowlist check before validation/commit options.**

Define an allowlist containing only the intended remediation paths:

```text
AGENTS.md
CHANGELOG.md
LICENSE
THIRD_PARTY_NOTICES.md
README.md
QUICKSTART.md
FIRMWARE/README.md
FIRMWARE/manifest.json
docs/DEPLOYMENT-REPORT.md
docs/IMPLEMENTATION-SUMMARY.md
docs/LEGACY-SUPPORT.md
docs/HARDWARE-ATTRIBUTION.md
docs/RELEASE-CHECKLIST.md
docs/SILKSCREEN-GUIDE.md
docs/evidence/kicad-owner-verification.md
docs/evidence/qmk-build.md
docs/evidence/review-remediation.md
tools/verify_repository.py
tools/commit_compliance.sh
tests/test_verify_repository.py
```

Collect tracked modifications with `git diff --name-only` and untracked files with `git ls-files --others --exclude-standard`. If any path is not allowlisted, print it and exit nonzero before staging. Never include `FIRMWARE/*.hex`, `FIRMWARE/QMK/**`, `Hardware/**`, or arbitrary user files.

- [ ] **Step 2: Replace every `git add -A`.**

Stage the explicit allowlist only after the path check, for example:

```bash
git add -- AGENTS.md CHANGELOG.md LICENSE THIRD_PARTY_NOTICES.md README.md QUICKSTART.md \
  FIRMWARE/README.md FIRMWARE/manifest.json docs tools tests
```

Because `docs`, `tools`, and `tests` can contain unrelated files, filter them through the allowlist rather than staging those directories wholesale. Keep the script review-only by default; no push command is added.

- [ ] **Step 3: Update helper messaging.**

Change “commit preparation complete” and push instructions to state that the script validates and previews only; owner approval is required before staging, committing, or pushing. Remove the suggested claim “Existing units fully supported” from the commit template; use “Legacy artifacts preserved; physical compatibility and build provenance remain evidence-bounded.”

- [ ] **Step 4: Smoke-test the guard.**

Create a temporary untracked file outside the allowlist, run the helper's status/allowlist stage in a non-committing mode, and assert it exits nonzero naming that file. Remove only the temporary file after the check. Then run the helper with the current intended paths and confirm it does not propose unrelated `tests/__pycache__/` or hardware/QMK changes.

---

### Task 9: Final validation, review, and evidence recording

**Files:**
- Verify all files changed by Tasks 1–8.
- Update only `docs/evidence/review-remediation.md` with observed command results.

- [ ] **Step 1: Run the complete local test suite.**

```bash
python -m unittest discover -s tests -v
python tools/verify_repository.py --verbose
python D:/Pribadi/ERGODASH-MOD-ENCH-OLED-QMK_VIA/tools/verify_repository.py --manifest-only
python -m json.tool FIRMWARE/manifest.json > NUL
python -m json.tool ErgoDash_4key_mod_positron_elektronik.json > NUL
python -m json.tool NEW_ErgoDash_4key_V3_mod_positron_elektronik.json > NUL
python -m json.tool FIRMWARE/ErgoDash_4key_mod_positron_elektronik.json > NUL
python -m json.tool FIRMWARE/ErgoDash_4key_V3_mod_positron_elektronik.json > NUL
```

Expected: unit tests pass, validator passes from repository and external CWD, and all five JSON files parse. Record exact test count and validator summaries.

- [ ] **Step 2: Verify immutable artifacts.**

Before and after the remediation, compare SHA-256 values for the three shipped HEX files and compare file contents for all VIA JSON files and QMK source directories. Use the existing manifest values as the expected HEX hashes. Any changed firmware, VIA JSON, QMK, or KiCad file blocks completion and must be investigated before proceeding.

- [ ] **Step 3: Run wording and link checks.**

Search maintained documents for active unsupported claims:

```text
fully compliant
production-ready
DEPLOYMENT COMPLETE
ALL PASS
100% compatible
all work with Rev1.2
built for Rev1.2
official ErgoDash
approved by omkbd
endorsed by omkbd
hhttps://
```

Historical quotations and prohibited-marking examples are allowed only when clearly labeled as historical/example/prohibited. Run the validator's local-link check and manually verify that the corrected firmware guide link resolves.

- [ ] **Step 4: Record external/device/hardware blockers accurately.**

Do not simulate browser, QMK, USB, VIA, or KiCad evidence. In `docs/evidence/review-remediation.md`, leave those items unchecked and list the exact owner action required. If later performed, attach the real output/screenshot path, date, tool version, and reviewer.

- [ ] **Step 5: Inspect the final diff without staging.**

```bash
git status --short
git diff -- README.md QUICKSTART.md LICENSE THIRD_PARTY_NOTICES.md CHANGELOG.md FIRMWARE docs tools tests
git diff --check
```

Expected: only planned documentation/validator/test/helper paths changed; no firmware, VIA, QMK, Hardware, or temporary-cache files are included; whitespace check exits 0. Do not commit or push without explicit owner authorization.

---

## Acceptance Criteria

Implementation is complete only when all are true:

1. Validator works from any CWD and resolves manifest paths from repository root.
2. Validator validates required artifact fields, SHA-256 shape, provenance status, local artifact/source/VIA paths, USB/VIA consistency, required evidence files, JSON syntax, and maintained-document local links.
3. Unit tests cover valid and invalid behavior for every new validator contract.
4. No maintained document presents repository-source mapping as proof of physical Rev1.2 compatibility.
5. No maintained document claims reproducible QMK builds, device behavior, KiCad results, external-link success, legal compliance, production readiness, or owner approval without attached evidence.
6. Hardware attribution distinguishes repository facts from owner/hardware evidence and does not conflate OLED electrical buses with split serial transport.
7. Third-party notices do not assign unsupported licenses or ownership; unresolved provenance is explicit.
8. `docs/evidence/kicad-owner-verification.md` exists with unchecked evidence items only.
9. Release and rollback guidance preserve history and legacy artifacts and require explicit owner approval for public actions.
10. Commit helper rejects unrelated changes and never stages with unrestricted `git add -A`.
11. All shipped HEX, VIA JSON, QMK source, and KiCad files remain unchanged.
12. Full local tests, validator, JSON parsing, hash checks, link checks, and final diff checks pass.
13. Remaining QMK, USB/VIA, hardware, external-link, and owner-approval work is reported as blocked—not silently marked complete.

## Execution Notes

- Execute tasks in order because Tasks 2–9 depend on the validator contract and evidence-file paths established earlier.
- Use separate commits only when the owner authorizes commits; otherwise use the task boundaries as review checkpoints without staging.
- No public rename, GitHub release, customer communication, marketplace edit, firmware publication, or KiCad manufacturing claim is part of this plan.
