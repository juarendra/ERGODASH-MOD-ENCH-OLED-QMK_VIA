# ENCHDASH Release Checklist

This checklist ensures every release meets compliance, quality, and compatibility standards before distribution.

---

## Pre-Release Validation

### 1. Local Repository Integrity

- [ ] Run `python tools/verify_repository.py` — all checks pass
- [ ] Run `python tests/test_verify_repository.py` — all tests pass
- [ ] Verify Git working tree clean (no uncommitted changes)
- [ ] Confirm current commit hash recorded
- [ ] All local documentation links verified (no 404s)
- [ ] All external links verified (GitHub, manufacturer tools, datasheets)

### 2. Legacy Binary Validation

- [ ] All firmware binaries present in `FIRMWARE/`
- [ ] `FIRMWARE/manifest.json` SHA-256 hashes computed
- [ ] Hash verification passes: computed hashes match manifest
- [ ] Provenance status recorded: `verified`, `functionally rebuilt`, or `incomplete`

**Example manifest hashes (template values for reference)**:
```json
{
  "ergodash_rev1_via.hex": "abc123...",
  "omkbd_ergodash_rev1_nowpmmousekey.hex": "def456...",
  "omkbd_ergodash_rev1_wpmnomousekey.hex": "ghi789..."
}
```
*Note: These are illustrative template values. Actual observed hashes are recorded in `FIRMWARE/manifest.json`.*

### 3. QMK Build Evidence (SOURCE-REPRODUCIBLE, HASH-DIVERGENT)

**Status**: Rebuilt 2026-10-10. All three variants compile cleanly from repo source with a documented toolchain (QMK `0.26.11`, `avr-gcc 15.1.0`). Rebuilt hashes differ from shipped because the original QMK commit/toolchain was never recorded. See [`docs/evidence/qmk-build.md`](evidence/qmk-build.md).

- [ ] Source QMK commit identified and recorded (original commit unknown; a representative 2024 release was used)
- [x] Build command documented in `FIRMWARE/manifest.json`
- [ ] Clean build reproduces identical or functionally equivalent binaries (compiles cleanly; byte-identical reproduction not achieved; functional equivalence not yet hardware-tested)
- [x] Build log and environment recorded (`build_environment` in manifest + evidence doc)
- [x] Diff analysis recorded (large byte differences consistent with newer QMK/avr-gcc; see evidence doc)

**Remaining**: `provenance_status` stays `incomplete`. Upgrade to `functionally rebuilt` requires flashing shipped + rebuilt `.hex` to hardware and confirming identical behaviour; `verified` requires an exact hash match (needs the original QMK commit). This is the only open release-blocking gate.

### 4. Device Enumeration and VIA Test (OWNER-ATTESTED)

**Status**: Owner-attested 2026-10-10. See [Device Test](evidence/device-test.md).

- [x] Firmware flashed to physical ATmega32u4 test hardware
- [x] USB enumeration verified (host recognizes device with `0x4D44:0x6061`)
- [x] All keys tested (matrix scan confirms every switch)
- [x] Encoder rotation and press tested
- [x] OLED display functional
- [x] RGB lighting functional (if variant includes RGB)
- [x] VIA desktop/web detects device with matching JSON
- [x] VIA key remapping tested and persists across power cycle

**Note**: Owner attestation; the product has been fabricated and sold working. Raw enumeration logs and VIA captures are retained by the owner, not committed here.

### 5. VIA JSON Validation (Local Only)

- [ ] `vendorId` and `productId` match firmware USB descriptor
- [ ] Matrix dimensions match firmware `MATRIX_ROWS` × `MATRIX_COLS`
- [ ] Layout matches physical key positions
- [ ] JSON syntax valid: `python -m json.tool FILENAME.json > NUL`

*Note: Full VIA detection confirmed on physical hardware (Gate 4, owner-attested).*

### 6. KiCad Owner Evidence (OWNER-ATTESTED)

**Status**: Owner-attested 2026-10-10. See [KiCad Owner Verification](evidence/kicad-owner-verification.md).

- [x] KiCad ERC: owner confirms pass, no blocking errors
- [x] KiCad DRC: owner confirms pass, no blocking errors
- [x] Title block updated per [Silkscreen Guide](SILKSCREEN-GUIDE.md)
- [x] Silkscreen attribution present and legible
- [x] Silkscreen does not overlap pads, holes, copper, or keepouts
- [x] Gerber files reviewed; `gerber_ergodash_mod_positron.rar` matches the Rev1.2 production design
- [x] First-article production confirmed (units fabricated and sold)
- [x] Evidence attested by Juarendra Ramadhani (Positron Electronic), 2026-10-10

**Note**: Owner attestation; supporting ERC/DRC reports, Gerber renders, and assembly photos are retained by the owner, not committed here.

### 7. Documentation Completeness

- [ ] `README.md` links work (no 404s)
- [ ] `CHANGELOG.md` updated with release notes
- [ ] `FIRMWARE/manifest.json` matches distributed binaries
- [ ] [Legacy Support Guide](LEGACY-SUPPORT.md) updated if variants added
- [ ] [Firmware Documentation](../FIRMWARE/README.md) current
- [ ] Version numbers consistent across all files

---

## Release Artifact Preparation

### Required Files in Release Package

**Firmware** (choose variant for customer):
- [ ] `.hex` file with SHA-256 in filename or separate `.sha256` file
- [ ] Matching VIA JSON file
- [ ] [Flashing instructions](../FIRMWARE/README.md)
- [ ] Source code reference (Git commit or archive)

**Documentation**:
- [ ] Schematic PDF
- [ ] Flashing guide
- [ ] VIA setup guide
- [ ] Troubleshooting guide

**Hardware** (if selling PCBs):
- [ ] Gerber files
- [ ] BOM (CSV or PDF)
- [ ] Assembly instructions

---

## Rollback Artifact Preservation

Before publishing release:

- [ ] Previous working firmware `.hex` archived with commit hash
- [ ] Git commit of last known-good state recorded
- [ ] Rollback instructions documented (see Rollback Procedure below)

---

## Owner Approval Gate (FINAL GATE)

**All prior gates must pass before this section.**

- [ ] Repository integrity verified
- [ ] Legacy binary hashes verified
- [~] QMK build evidence (Gate 3): source compiles cleanly, environment recorded; byte-identical reproduction and functional-equivalence test still open
- [x] Device enumeration and VIA test passed (Gate 4, owner-attested)
- [x] KiCad owner evidence obtained (Gate 6, owner-attested)
- [ ] Documentation links verified
- [ ] Release artifacts prepared
- [ ] Rollback artifacts preserved

**Owner decision** (check all that apply):
- [ ] Approve GitHub repository rename (if applicable)
- [ ] Approve GitHub release publication
- [ ] Approve customer communication (if applicable)
- [ ] Approve marketplace listing updates (if applicable)
- [ ] Approve `git push` to public repository

**Explicit owner approval required**: ___________ \
**Date**: ___________

---

## Known Issues

**Status**: QMK build provenance is source-reproducible but hash-divergent. Device and hardware checks are owner-attested.

- **QMK Build Evidence** (Gate 3): Rebuilt 2026-10-10 — all three variants compile cleanly from repo source (QMK `0.26.11`, `avr-gcc 15.1.0`); environment, build commands, and rebuilt hashes recorded in `FIRMWARE/manifest.json` and `evidence/qmk-build.md`. Byte-identical reproduction not achieved (original QMK commit unknown); `provenance_status` stays `incomplete`.
- **Device Test** (Gate 4): Owner-attested (2026-10-10) — device flashed, enumerated, VIA-detected, and shipped working. Raw logs/screenshots retained by owner. See `evidence/device-test.md`.
- **KiCad Owner Evidence** (Gate 6): Owner-attested (2026-10-10) — ERC/DRC pass, Gerber matches production, first-article fabricated and sold. Raw artifacts retained by owner. See `evidence/kicad-owner-verification.md`.

Gate 3 (byte-identical QMK provenance) remains the only partially-open item; the source is proven to compile and Gates 4 and 6 are satisfied by owner attestation above.

---

## GitHub Release Steps

**Prerequisites**: All gates passed, owner approval obtained.

### 1. Version Tag

```bash
# Create annotated tag
git tag -a v1.0.0 -m "ENCHDASH v1.0.0 - Initial compliance release"

# Push tag
git push origin v1.0.0
```

**Tag naming**: `vMAJOR.MINOR.PATCH` (semantic versioning)

### 2. Release Notes Template

```markdown
## ENCHDASH vX.Y.Z

### Hardware
- Revision: Rev1.2
- Controller: Arduino Pro Micro (ATmega32u4)

### Firmware Variants

**ergodash_rev1_via.hex** (Recommended)
- SHA-256: `[see manifest.json]`
- Features: VIA, encoder, OLED, RGB
- VIA JSON: `ErgoDash_4key_mod_positron_elektronik.json`

**omkbd_ergodash_rev1_nowpmmousekey.hex**
- SHA-256: `[see manifest.json]`
- Features: VIA, encoder, OLED, RGB, mouse keys
- VIA JSON: `NEW_ErgoDash_4key_V3_mod_positron_elektronik.json`

**omkbd_ergodash_rev1_wpmnomousekey.hex**
- SHA-256: `[see manifest.json]`
- Features: VIA, encoder, OLED (with WPM), RGB
- VIA JSON: `NEW_ErgoDash_4key_V3_mod_positron_elektronik.json`

### Installation
See [FIRMWARE/README.md](../FIRMWARE/README.md) for flashing instructions.

### Changes
- Initial compliance and identity remediation
- Added comprehensive licensing and attribution
- Created legacy support documentation
- Established firmware provenance tracking

### Compatibility
Legacy units sold as "ERGODASH-MOD-ENCH-OLED-QMK_VIA" retain legacy firmware and VIA JSON availability; physical compatibility is not independently verified.

### Known Issues
See main checklist for gate status.

### Breaking Changes
None. This is a documentation and compliance update; no electrical changes.
```

### 3. Attach Release Assets

- [ ] All three `.hex` files
- [ ] Both VIA JSON files
- [ ] Source code archive (auto-generated by GitHub)
- [ ] `CHANGELOG.md`
- [ ] Schematic PDF

---

## Post-Release

### 1. Customer Communication (If Updating Existing Products)

**Email template**:

```
Subject: ENCHDASH Firmware and Documentation Update

Dear [Customer],

Your ERGODASH-MOD-ENCH-OLED-QMK_VIA keyboard has been renamed to ENCHDASH 
as part of a compliance and attribution update.

What this means for you:
✓ Your keyboard is unaffected by the rename; confirm physical compatibility before any new flashing
✓ No reflashing required
✓ Legacy firmware and VIA JSON remain available (physical compatibility not independently verified)
✓ New documentation available at: [GitHub URL]

If you wish to update to the latest firmware (optional):
1. Download from: [Release URL]
2. Follow flashing guide: [FIRMWARE/README.md URL]
3. Use the same VIA JSON you currently have

Nothing changes if you don't update. Legacy firmware and VIA JSON remain available; physical compatibility and build provenance must be confirmed before new flashing.

Questions? Contact: [Support Email]

Regards,
Positron Electronic
```

### 2. Repository State

- [ ] GitHub description updated to "ENCHDASH"
- [ ] Topics/tags updated: `qmk`, `via`, `mechanical-keyboard`, `ergonomic`, `split-keyboard`
- [ ] README badges added (if applicable): build status, license
- [ ] `About` section updated with commercial identity

### 3. Marketplace Updates (If Applicable)

- [ ] Product listings updated with new name
- [ ] Links to GitHub repository updated
- [ ] Product photos/descriptions reference ENCHDASH
- [ ] Legacy name noted for searchability

---

## Rollback Procedure

If a release introduces critical issues:

### 1. Identify Safe Fallback

- [ ] Previous working firmware `.hex` identified
- [ ] Git commit of last known-good state recorded

### 2. Create Rollback Release

```bash
# Revert to previous commit
git revert --no-commit HEAD~1..HEAD
git commit -m "Rollback: Revert vX.Y.Z due to [issue]"

# Tag rollback
git tag -a vX.Y.Z-rollback -m "Rollback release"
git push origin vX.Y.Z-rollback
```

### 3. Customer Notification

- [ ] GitHub release notes explain rollback reason
- [ ] Email customers with working firmware link
- [ ] Issue tracker updated with root cause

---

## USB VID/PID Change Procedure (Future)

**Current USB ID**: `0x4D44:0x6061` (provenance under audit)

If changing USB VID/PID:

### 1. Obtain Valid VID/PID

- [ ] Purchase USB VID from USB-IF ($6,000) OR
- [ ] Use PID.codes community registry ($0) for experimental/hobby projects
- [ ] Document allocation source in `FIRMWARE/manifest.json`

### 2. Update Firmware

- [ ] Change `VENDOR_ID` and `PRODUCT_ID` in `config.h`
- [ ] Rebuild all firmware variants
- [ ] Test host enumeration on Windows/macOS/Linux

### 3. Update VIA JSON

- [ ] Change `vendorId` and `productId` in all VIA JSON files
- [ ] Create new JSON files for new USB ID (don't overwrite legacy)
- [ ] Test VIA detection with new firmware + new JSON

### 4. Compatibility Warning

- [ ] Document that new firmware requires new VIA JSON
- [ ] Provide migration instructions for existing users
- [ ] Keep legacy firmware + legacy JSON available indefinitely

---

## Regulatory Compliance (Optional but Recommended)

### FCC/CE (If Selling Commercially)

- [ ] EMC testing performed
- [ ] Certification obtained
- [ ] Certification marks added to silkscreen only if earned
- [ ] DoC (Declaration of Conformity) available

### RoHS/REACH (If Selling in EU)

- [ ] BOM reviewed for restricted substances
- [ ] Manufacturer compliance certificates obtained
- [ ] RoHS declaration issued

**Note**: These are not required for hobby/personal projects but are mandatory for commercial sale in many jurisdictions.

---

## Checklist Sign-Off

**Release version**: ___________  
**Release date**: ___________  
**Prepared by**: ___________  
**Reviewed by**: ___________  

- [ ] All pre-release validation passed
- [ ] All required artifacts attached
- [ ] GitHub release published
- [ ] Customers notified (if applicable)

**Approval**: ___________  
**Date**: ___________

---

**Last updated**: 2026-10-09 \
**Applies to**: ENCHDASH all revisions
