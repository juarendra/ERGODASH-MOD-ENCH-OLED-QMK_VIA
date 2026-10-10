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
- SofleKeyboard footprint library MIT license (`Hardware/PCB/Rev1.2/SofleKeyboard-footprint.pretty/LICENSE`, Josef Adamcik 2019)
- `.gitignore` (excludes `__pycache__/`, `.cooper/`)

### Changed
- **Product name**: `ERGODASH-MOD-ENCH-OLED-QMK_VIA` → `ENCHDASH` (primary identity)
- **README.md**: Complete rewrite with ENCHDASH branding, attribution, and compliance information
- **Repository description**: Now clearly states independent derivative status and omkbd attribution

### Fixed
- Malformed firmware link in original README (`hhttps://` → correct URL)
- Missing root LICENSE file
- Missing GPL and MIT license texts
- Absence of third-party component license inventory
- Unbounded device-behavior claims ("works exactly as before", "remains fully supported") in `docs/DEPLOYMENT-REPORT.md`, `docs/RELEASE-CHECKLIST.md`, `docs/IMPLEMENTATION-SUMMARY.md`, `QUICKSTART.md` — now bounded to repo-provable statements
- Stale validator section counts ("sections 1-6" → "all 7 sections") in `QUICKSTART.md`, `docs/IMPLEMENTATION-SUMMARY.md`
- Removed 4 unused vendored footprint libraries with zero PCB references (`Keebio-Parts.pretty`, `keyboard_parts.pretty-master`, `keebs.pretty-master`, `ProMicro.pretty-master`); PCB unchanged (footprint geometry embedded in `.kicad_pcb`)
- `THIRD_PARTY_NOTICES.md` updated with 2026-10-10 footprint usage audit (119 instances; SofleKeyboard MIT confirmed; SK6812/3D/media gaps documented)
- Documented SK6812 LED footprint (`prettylib:SK6812_mini_e_flipable`) as datasheet-derived PCB geometry (not a copyrightable work); upstream yaemk-split-kb GPL-3.0 credited, no copyleft propagated — owner-accepted position with upgrade path in `THIRD_PARTY_NOTICES.md`
- Documented 3D models (`Hardware/PCB/Rev1.2/3d/`) as KiCad visualization-only, excluded from manufacturing output and shipped product; vendor provenance recorded as non-blocking owner-accepted position with removal upgrade path in `THIRD_PARTY_NOTICES.md`
- Untracked stale `tools/__pycache__/*.pyc` (now covered by `.gitignore`; stops repeated working-tree churn)
- Bounded residual "Existing units remain supported" wording in `README.md` to the repo-provable legacy-availability statement
- Removed two redundant VIA JSON files in `FIRMWARE/`: `ErgoDash_4key_mod_positron_elektronik.json` (byte-identical duplicate of the root legacy file) and `ErgoDash_4key_V3_mod_positron_elektronik.json` (older V3 copy lacking the rgblight menu, superseded by the root canonical). Canonical VIA JSON is `NEW_ErgoDash_4key_V3_mod_positron_elektronik.json`; file contents unchanged, only duplicates removed. Clarified canonical vs legacy in `README.md`, `FIRMWARE/README.md`, `THIRD_PARTY_NOTICES.md`

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

Normal rollback: create an owner-approved `git revert` commit for the specific
change, preserve all Git history and legacy artifacts, then verify local links,
hashes, and customer download paths. Do not use force-push, `reset --hard`, or
remove license/provenance/evidence files as a rollback method.

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
| Firmware | No change needed | Legacy artifacts preserved; exact build provenance not evidenced |
| VIA JSON | Continue using existing file | Legacy artifacts preserved; identical PCB not independently verified |
| Hardware | No physical changes | Legacy artifacts preserved; physical compatibility not evidenced |
| Branding | Update is informational | Legacy name supported |
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
