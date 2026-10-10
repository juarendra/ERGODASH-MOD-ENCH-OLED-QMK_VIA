# Review Remediation Evidence

**Status:** Complete (2026-10-10). Tasks 1-8 of the 2026-10-09 remediation plan are done and reviewed; final local validation recorded below (2026-10-10). Items under "Not established by local checks" remain blocked pending owner action or external evidence.

## Local checks

- [x] `python -m unittest discover -s tests -v` output attached or summarized.
- [x] `python tools/verify_repository.py --verbose` output attached or summarized.
- [x] Validator run from a different CWD.
- [x] Maintained Markdown local-link check passes.

Boxes checked in the final verification step (2026-10-10, section below); dated observations above are interim evidence recorded as tasks land.


### 2026-10-09: Unit tests

```
Ran 20 tests in 0.109s

OK
```

All 20 tests pass (14 original + 6 new contract tests: CWD-independent path resolution, manifest schema/rejection, provenance constraints, required evidence files, local markdown link targets).

### 2026-10-09: Validator run from repo root

```
python tools/verify_repository.py --verbose
```

Sections [1/7] through [6/7] all pass:
- Firmware manifest hash integrity: ✓
- Manifest schema and local paths: ✓
- USB VID/PID consistency: ✓
- Required documentation files: ✓ (now includes docs/RELEASE-CHECKLIST.md, docs/SILKSCREEN-GUIDE.md, docs/evidence/kicad-owner-verification.md, docs/evidence/qmk-build.md, docs/evidence/review-remediation.md)
- License file content: ✓
- JSON file syntax: ✓

Section [7/7] Local markdown link targets reports 8 broken links (expected; fixed by later tasks):
- `FIRMWARE\README.md -> LEGACY-SUPPORT.md` (Task 3 will fix: relative link should point to ../docs/LEGACY-SUPPORT.md)
- `docs\RELEASE-CHECKLIST.md -> FIRMWARE/README.md` (Task 6 will review)
- `docs\SILKSCREEN-GUIDE.md -> ../screenshots/*.png` (6 missing screenshot files; Task 6 will address)

Exit code: 1 (due to broken links; validator correctly detects issues that later tasks will fix).

### 2026-10-09: Validator from different CWD

```
cd D:/Pribadi
python ERGODASH-MOD-ENCH-OLED-QMK_VIA/tools/verify_repository.py --verbose
```

Works correctly. All path resolution uses repo_root. Same results as above.

### 2026-10-09: Manifest-only mode

```
python tools/verify_repository.py --manifest-only
```

Runs checks [1/7] and [2/7] (manifest hashes + manifest schema validation), then exits with code 0. Working as specified.

### 2026-10-10: Final validation (Tasks 1-8 complete)

```
python -m unittest discover -s tests
```
Ran 20 tests in 0.137s
OK

```
python tools/verify_repository.py --verbose
```
Sections [1/7] through [7/7] all pass, 0 broken local markdown links, exit code 0.
- [1/7] Firmware manifest hash integrity: 3/3 HEX match manifest
- [2/7] Manifest schema and local paths: valid
- [3/7] USB VID/PID consistency: 0x4D44:0x6061 in all VIA JSONs
- [4/7] Required documentation files: all present
- [5/7] License file content: MIT + GPL v2 headers verified
- [6/7] JSON file syntax: manifest + root VIA JSONs valid
- [7/7] Local markdown link targets: all valid

```
cd C:/Windows/System32
python "D:/Pribadi/ERGODASH-MOD-ENCH-OLED-QMK_VIA/tools/verify_repository.py" --manifest-only
```
Exit code 0 (sections [1/7] and [2/7] pass from external CWD).

`python -m json.tool` on FIRMWARE/manifest.json and all 5 VIA JSONs: all parse.

SHA-256 re-hash of all 3 shipped HEX matches FIRMWARE/manifest.json (cdc3d67382e8…, 22665732e197…, 4ee05ef6ac85…).

## Known pre-existing issues found during remediation

### Broken local links (detected by Task 2, fixed by later tasks)

1. `FIRMWARE/README.md -> LEGACY-SUPPORT.md` — relative link resolves to nonexistent `FIRMWARE/LEGACY-SUPPORT.md`; should be `../docs/LEGACY-SUPPORT.md`. **Task 3 will fix.**

2. `docs/RELEASE-CHECKLIST.md -> FIRMWARE/README.md` — relative link resolves to nonexistent `docs/FIRMWARE/README.md`; correct target from `docs/` is `../FIRMWARE/README.md`. **Task 6 will fix.**


3. `docs/SILKSCREEN-GUIDE.md -> ../screenshots/*.png` (6 broken image links):
   - `../screenshots/title-block.png`
   - `../screenshots/pcb-front.png`
   - `../screenshots/pcb-back.png`
   - `../screenshots/erc-result.png`
   - `../screenshots/drc-result.png`
   - `../screenshots/gerber-back-silkscreen.png`
   
   The `screenshots/` directory does not exist. **Task 6 will address** (either create screenshots or remove references).

## Not established by local checks

- QMK historical base commit and reproducible legacy builds. Owner action: record the exact QMK base commit, toolchain, build command, output path, and artifact hashes in `docs/evidence/qmk-build.md`; attach device-behavior tests if hashes differ.
- USB enumeration and VIA detection on physical hardware. Owner action: flash a shipped HEX to physical ATmega32u4 hardware and attach enumeration logs plus a VIA device capture (date, tool version).
- Key, encoder, OLED, RGB, split, and reset smoke test. Owner action: run and attach the physical test matrix from docs/RELEASE-CHECKLIST.md.
- KiCad ERC/DRC, Gerber, silkscreen, and first-article evidence. Owner action: run the KiCad checks and attach results to docs/evidence/kicad-owner-verification.md.
- External URL response and GitHub rendering verification. Owner action: verify the links in a browser and attach dated screenshots.
- Owner approval for commit, rename, release, or customer communication. Owner action: explicit written approval before any public action.
