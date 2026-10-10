# ENCHDASH QMK Build Evidence

**Status**: incomplete. The repository records shipped binary hashes and source
mappings, but no QMK base commit or reproducible build has been evidenced here.
Physical device function (USB enumeration, VIA detection, smoke test) is
owner-attested separately in `device-test.md`; build provenance remains the
open item.

**Date**: 2026-10-08
**Purpose**: Document reproducible QMK build process for legacy firmware validation


---

## Goal

Establish a reproducible build baseline for the three distributed firmware binaries:
- `ergodash_rev1_via.hex` (SHA-256: `cdc3d67...`)
- `omkbd_ergodash_rev1_nowpmmousekey.hex` (SHA-256: `2266573...`)
- `omkbd_ergodash_rev1_wpmnomousekey.hex` (SHA-256: `4ee05ef...`)

This requires:
1. Identifying the QMK base commit used for the original builds
2. Confirming the source-to-binary mapping in `FIRMWARE/manifest.json`
3. Reproducing builds to match or functionally verify the shipped binaries

---

## Prerequisites

Before establishing the build baseline:

- [ ] QMK development environment installed: https://docs.qmk.fm/#/newbs_getting_started
- [ ] `qmk` CLI tool configured
- [ ] Python 3.8+ available
- [ ] Git available for QMK submodule management

**Installation**:
```bash
python3 -m pip install qmk
qmk setup
```

---

## Build Process (To Be Executed)

### Step 1: Identify QMK Base Commit

The original builds did not record the QMK commit. Strategies to identify it:

1. **Source file inspection**: Check for QMK version markers in source comments
2. **Feature flag archaeology**: Compare enabled features with QMK release timeline
3. **Trial builds**: Test multiple QMK releases (2023-2024) and compare binaries
4. **Functional equivalence**: Accept a different hash if behavior is verified identical

### Step 2: Copy Source to QMK Tree

```bash
# From QMK firmware root
cp -r /path/to/ENCHDASH/FIRMWARE/QMK/ergodash keyboards/ergodash_legacy_base
cp -r /path/to/ENCHDASH/FIRMWARE/QMK/ergodash_nowpm_mousekey keyboards/ergodash_legacy_mousekey
cp -r /path/to/ENCHDASH/FIRMWARE/QMK/ergodash_wpm_nomousekey keyboards/ergodash_legacy_wpm
```

### Step 3: Build Each Variant

```bash
# Base VIA firmware
qmk compile -kb ergodash_legacy_base/rev1 -km default

# Mouse key variant
qmk compile -kb ergodash_legacy_mousekey/rev1 -km default

# WPM variant
qmk compile -kb ergodash_legacy_wpm/rev1 -km default
```

### Step 4: Compare Hashes

```bash
# Compute hashes of built artifacts
sha256sum .build/ergodash_legacy_base_rev1_default.hex
sha256sum .build/ergodash_legacy_mousekey_rev1_default.hex
sha256sum .build/ergodash_legacy_wpm_rev1_default.hex

# Compare with manifest
cat FIRMWARE/manifest.json | grep sha256
```

### Step 5: Update Manifest

If hashes match or functional equivalence is verified, update `FIRMWARE/manifest.json`:

```json
{
  "qmk_base_commit": "abc123...",
  "source_commit": "744c49c...",
  "build_command": "qmk compile -kb ergodash_legacy_base/rev1 -km default",
  "provenance_status": "verified"
}
```

If hashes differ but behavior is identical:
```json
{
  "provenance_status": "functionally rebuilt",
  "notes": "Recompiled with QMK commit abc123; binary hash differs due to timestamp/metadata; functionality verified identical"
}
```

---

## Expected Outcomes

### Scenario A: Exact Hash Match

- **Action**: Update manifest with QMK commit, build command, set `provenance_status: "verified"`
- **Confidence**: High — bit-for-bit reproducibility achieved

### Scenario B: Different Hash, Verified Equivalent

- **Action**: Document QMK commit, note hash difference, set `provenance_status: "functionally rebuilt"`
- **Verification required**:
  - Flash both versions to test hardware
  - Verify matrix scanning, encoder, OLED, RGB all function identically
  - Test VIA compatibility with both binaries

### Scenario C: Cannot Reproduce

- **Action**: Keep `provenance_status: "incomplete"`, document attempted QMK commits
- **Impact**: Shipped binaries remain supported as legacy downloads; physical compatibility and build provenance must be confirmed before new flashing

---

## Verification Commands

After establishing the baseline, run these commands to verify:

```bash
# Validate manifest hashes match built artifacts
python tools/verify_repository.py --manifest-only

# Test flash and functionality
qmk flash -kb ergodash_legacy_base/rev1 -km default
# Connect hardware, verify keys/encoder/OLED/RGB
# Load VIA JSON, verify remapping works
```

---

## Documentation Requirements

Once baseline is established, document and attach the following evidence before
updating `FIRMWARE/manifest.json` provenance_status from `incomplete`:

1. **Exact QMK base commit** (full SHA) used for each variant build
2. **Compiler/toolchain details** (gcc-arm-none-eabi version, QMK version)
3. **Exact build command** (e.g., `qmk compile -kb ... -km default`)
4. **Output path** of the produced artifact
5. **Artifact SHA-256 hash** of the built `.hex`

### Provenance status upgrade rules

- `verified` **only** when the built artifact SHA-256 matches the corresponding
  manifest SHA-256 exactly.
- `functionally rebuilt` **only** when hashes differ **and** the following
  documented device behavior tests confirm identical functionality:
  - Flash both versions to test hardware
  - Verify matrix scanning, encoder, OLED, and RGB all function identically
  - Test VIA compatibility with both binaries

If any required evidence is missing, `provenance_status` remains `incomplete`.

---

## Current Status

**BLOCKED**: Requires QMK toolchain installation and build testing.

**Next actions**:
1. Install QMK development environment
2. Attempt builds with QMK releases from 2023-2024
3. Document successful QMK commit or mark as functionally rebuilt
4. Update manifest provenance

**Owner decision required**: Accept "functionally rebuilt" status if exact hash match cannot be achieved, or continue searching for original QMK commit.

---

## Notes

- Original builds were likely performed on a different machine with different compiler versions
- Exact reproducibility requires matching: QMK commit, compiler version, Python version, build timestamp
- Functional equivalence is acceptable for legacy support if verified through hardware testing
- Future ENCHDASH builds will record QMK commit at build time to avoid this issue
