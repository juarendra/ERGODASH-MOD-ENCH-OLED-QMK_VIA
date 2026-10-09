# ENCHDASH Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Comprehensive licensing and attribution documentation
- Repository integrity validator (`tools/verify_repository.py`)
- Unit tests for validator (`tests/test_verify_repository.py`)
- Firmware provenance manifest (`FIRMWARE/manifest.json`)
- Legacy support documentation (`docs/LEGACY-SUPPORT.md`)
- Hardware attribution documentation (`docs/HARDWARE-ATTRIBUTION.md`)
- Firmware selection guide (`FIRMWARE/README.md`)
- Third-party notices (`THIRD_PARTY_NOTICES.md`)
- KiCad silkscreen guide for owner (`docs/SILKSCREEN-GUIDE.md`)
- Release checklist (`docs/RELEASE-CHECKLIST.md`)
- QMK build evidence placeholder (`docs/evidence/qmk-build.md`)

### Changed
- **Product name**: `ERGODASH-MOD-ENCH-OLED-QMK_VIA` → `ENCHDASH` (primary identity)
- **README.md**: Complete rewrite with ENCHDASH branding, attribution, and compliance information
- **Repository description**: Now clearly states independent derivative status and omkbd attribution

### Fixed
- Malformed firmware link in original README (`hhttps://` → correct URL)
- Missing root LICENSE file
- Missing GPL and MIT license texts
- Absence of third-party component license inventory

### Deprecated
- Legacy product name `ERGODASH-MOD-ENCH-OLED-QMK_VIA` remains supported but will appear only in legacy documentation

### Security
- Established firmware integrity verification via SHA-256 checksums
- USB VID/PID provenance audit initiated (status: incomplete)

---

## [0.0.0] - Pre-Compliance (Before 2026-10-08)

### Context
Original repository state before compliance and identity remediation. Product sold as "ERGODASH-MOD-ENCH-OLED-QMK_VIA" without formal licensing structure or attribution chain.

### Existing Features (Preserved)
- Split ergonomic keyboard based on ErgoDash design
- Arduino Pro Micro (ATmega32u4) controller with USB Type-C
- Hotswap sockets (Kailh)
- Rotary encoder support (1 per half)
- OLED displays (128×32, status + logo)
- RGB underglow (WS2812, 24 LEDs)
- QMK firmware with VIA support
- Three firmware variants: base, mouse keys, WPM tracking
- 4 layers, 7×6 matrix per half

### Known Issues
- No root LICENSE file
- Missing omkbd attribution in README
- No firmware provenance documentation
- KiCad title block still referenced "omkbd" as company
- USB VID/PID provenance unknown
- Third-party footprint library licenses not inventoried

---

## Rollback Notes

### To Revert to Pre-Compliance State

If this update causes unforeseen issues and you need to return to the original state:

```bash
# Revert to commit before compliance work
git log --oneline --grep="ENCHDASH"  # find first ENCHDASH commit
git revert <commit-hash>

# Or reset to specific commit (destructive)
git reset --hard <commit-before-enchdash>
```

**Impact of rollback**:
- Repository name reverts to `ERGODASH-MOD-ENCH-OLED-QMK_VIA`
- LICENSE, attribution, and compliance files removed
- README returns to original version
- Firmware binaries and VIA JSON remain unchanged (hardware-compatible)
- Existing customers unaffected (firmware/VIA JSON compatibility preserved)

**Data loss**: Compliance documentation, validator scripts, and evidence files will be lost.

**Recommendation**: Keep a separate Git branch (`pre-compliance`) as a snapshot before applying these changes.

---

## Version Numbering

ENCHDASH follows semantic versioning:

- **MAJOR**: Breaking hardware changes (new PCB revision, incompatible firmware)
- **MINOR**: Feature additions (new firmware variant, documentation improvements)
- **PATCH**: Bug fixes, compliance updates, non-functional changes

**Current status**: Unreleased (no tagged versions yet)

**First release**: Will be tagged `v1.0.0` after QMK build baseline is established and owner approves commit.

---

## Migration Path for Existing Units

Units sold as "ERGODASH-MOD-ENCH-OLED-QMK_VIA" require no changes:

| Aspect | Action Required | Compatibility |
|--------|-----------------|---------------|
| Firmware | No change needed | 100% compatible |
| VIA JSON | Continue using existing file | 100% compatible |
| Hardware | No physical changes | Identical PCB |
| Branding | Update is optional | Legacy name supported |
| Documentation | Use new guides (recommended) | Applies to legacy units |

**Optional update path**:
1. Read new `FIRMWARE/README.md` for improved flashing instructions
2. Use `FIRMWARE/manifest.json` to verify firmware integrity
3. Continue using same firmware and VIA JSON as before

**No forced migration**: ENCHDASH identity change is for future batches and compliance; existing units remain "ERGODASH-MOD-ENCH-OLED-QMK_VIA" functionally.

---

## Future Roadmap

### Planned (Not Committed)

- [ ] Establish QMK build baseline (Task 5)
- [ ] Create ENCHDASH-branded firmware target (Task 6)
- [ ] Generate new VIA JSON with ENCHDASH identity (Task 6)
- [ ] Obtain valid USB VID/PID allocation
- [ ] Update KiCad silkscreen per owner guide
- [ ] Manufacture first ENCHDASH-branded PCB batch
- [ ] Repository rename: `ERGODASH-MOD-ENCH-OLED-QMK_VIA` → `ENCHDASH-QMK-VIA`

### Under Consideration

- [ ] Rev1.3 PCB with USB-C on both halves (eliminate Pro Micro)
- [ ] Wireless variant (nice!nano or similar)
- [ ] Alternative case designs (aluminum, acrylic)
- [ ] Pre-assembled option

---

## Contributors

### ENCHDASH Modifications
- **Juarendra Ramadhani** — Hardware modifications, firmware customization, commercial development
- **Positron Electronic** — Commercial identity and distribution

### Original ErgoDash Design
- **omkbd** — Original ErgoDash hardware design (2018), MIT License

### Third-Party Components
- See `THIRD_PARTY_NOTICES.md` for complete attribution

---

## License History

- **Pre-2026-10-08**: No explicit repository license; source available but license unclear
- **2026-10-08**: Multi-license repository structure established:
  - Hardware: MIT (preserving ErgoDash's original license)
  - Firmware: GPL-2.0-or-later (inherited from QMK)
  - Third-party: Various (see `THIRD_PARTY_NOTICES.md`)

---

## Contact

- **Repository**: https://github.com/juarendra/ERGODASH-MOD-ENCH-OLED-QMK_VIA (pending rename)
- **Commercial**: Positron Electronic
- **Issues**: GitHub issue tracker
- **Email**: jrjuarendra@gmail.com (from firmware copyright headers)

---

**Note**: This changelog documents the compliance and identity remediation process. Functional hardware and firmware capabilities remain unchanged from pre-compliance state.
