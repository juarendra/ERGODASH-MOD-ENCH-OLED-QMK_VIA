# ENCHDASH Third-Party Notices

This document lists third-party components used in the ENCHDASH repository, their licenses, and modification status. Each entry includes an evidence column to distinguish repository-grounded facts from claims requiring owner or KiCad verification.

---

## Evidence Ledger Structure

Each component is recorded with:
- **Claimed source**: upstream project or author attribution
- **License status**: license identified from repository files, or "not independently established" when no local license file or verifiable upstream source exists
- **Usage status**: whether the component is confirmed active in the current design, or "not established" pending KiCad footprint usage audit
- **Evidence**: repository file path, owner verification requirement, or audit action needed

---

## Hardware Components

| Component | Repository Path | Claimed Source | License Status | Usage Status | Evidence |
|-----------|----------------|----------------|----------------|--------------|----------|
| ErgoDash PCB design | `Hardware/PCB/Rev1.2/ergodash.*` | https://github.com/omkbd/ErgoDash | MIT (omkbd, 2018) — local license `LICENSES/MIT-ErgoDash.txt` | Active (modified) | Repository evidence: KiCad files present; modification history in git; title block date 2018-06-07 |
| ProMicro footprint (`sofle:ArduinoProMicro-ZigZag-DoubleSided`) | embedded in `ergodash.kicad_pcb` | SofleKeyboard footprint lib | MIT (Josef Adamcik, 2019) — local license `SofleKeyboard-footprint.pretty/LICENSE` | Active (1 instance) | Repository evidence: footprint embedded in PCB; provided via SofleKeyboard lib |
| SofleKeyboard footprints | `Hardware/PCB/Rev1.2/SofleKeyboard-footprint.pretty/` | https://github.com/josefadamcik/SofleKeyboard | MIT (Josef Adamcik, 2019) — local license `SofleKeyboard-footprint.pretty/LICENSE` | Active (primary layout lib, 92 instances) | Repository evidence: footprint usage audit of `ergodash.kicad_pcb` (2026-10-10); upstream MIT confirmed |
| SK6812 LED footprint (`prettylib:SK6812_mini_e_flipable`) | embedded in `ergodash.kicad_pcb` | yaemk-split-kb (https://github.com/KarlK90/yaemk-split-kb) | GPL-3.0 upstream (lib source not vendored in repo) | Active (12 instances) | Owner action: generic SK6812 footprint; source lib not present locally. Replace with a clearly-licensed SK6812 footprint or vendor the yaemk GPL-3.0 lib + license before asserting full compliance |
| Project-local footprints (`library:`, `Rev1:` — MX_ALPS, conn3, hole, gundam, qr-positron) | embedded in `ergodash.kicad_pcb`; `gundam.kicad_mod`, `qr-positron.kicad_mod` | Owner / ErgoDash-derived | Owner-created or ErgoDash-derived (MIT) | Active (15 instances) | Repository evidence: footprint usage audit (2026-10-10); owner/ErgoDash origin |

**Footprint usage audit (2026-10-10)**: `ergodash.kicad_pcb` has 119 footprint instances. Only the libraries listed above are referenced. The following vendored libraries had **zero references** and were removed: `Keebio-Parts.pretty`, `keyboard_parts.pretty-master`, `keebs.pretty-master` (CERN OHL v1.2), `ProMicro.pretty-master`. Removing their source folders does not alter the PCB — KiCad embeds footprint geometry directly in `.kicad_pcb`.

---

## Firmware Components

| Component | Repository Path | Claimed Source | License Status | Usage Status | Evidence |
|-----------|----------------|----------------|----------------|--------------|----------|
| QMK Firmware base | `FIRMWARE/QMK/ergodash*/` | https://github.com/qmk/qmk_firmware | GPL-2.0-or-later — local license `LICENSES/GPL-2.0-or-later.txt` | Active (modified) | Repository evidence: QMK source files present; file-level copyright notices retained; build provenance incomplete per `FIRMWARE/manifest.json` |
| ErgoDash QMK keyboard | `FIRMWARE/QMK/ergodash*/` | https://github.com/omkbd/ErgoDash (QMK integration) | GPL-2.0-or-later | Active (modified) | Repository evidence: modified from omkbd's ErgoDash QMK implementation; upstream copyright notices retained |

---

## Documentation and Media

| Component | Repository Path | Claimed Source | License Status | Usage Status | Evidence |
|-----------|----------------|----------------|----------------|--------------|----------|
| Hardware photos | `DOC/HARDWARE/*.{png,jpeg}` | Original photography by Juarendra Ramadhani | Owner attribution not independently verified | Active | Owner verification required: no independent evidence of authorship or licensing; treat as owner-supplied content |
| Schematic PDF | `Hardware/ErgoDash_Schematic.pdf` | Exported from modified KiCad files | Derived from MIT-licensed ErgoDash (omkbd, 2018) | Active | Repository evidence: generated from modified source; derivative work under MIT |
| Tutorial video | `DOC/tutorial_load_json_file.mov` | Original content by Juarendra Ramadhani | Owner attribution not independently verified | Active | Owner verification required: no independent evidence of authorship or licensing; treat as owner-supplied content |
| User manuals | `DOC/*.pdf` | Original documentation by Juarendra Ramadhani | Owner attribution not independently verified | Active | Owner verification required: no independent evidence of authorship or licensing; treat as owner-supplied content |

---

## VIA Configuration

| Component | Repository Path | Claimed Source | License Status | Usage Status | Evidence |
|-----------|----------------|----------------|----------------|--------------|----------|
| VIA JSON definitions | `*.json` (root), `FIRMWARE/*.json` | Based on VIA specification | Not independently established | Active | Owner verification required: VIA JSON files are configuration data; licensing not established; do not assume GPL merely because firmware is GPL |

---

## License Files in Repository

The following license files are present and committed:
- `LICENSES/MIT-ErgoDash.txt` — Original ErgoDash MIT License (omkbd, 2018)
- `LICENSES/GPL-2.0-or-later.txt` — GNU GPL v2 or later (from QMK)
- `Hardware/PCB/Rev1.2/SofleKeyboard-footprint.pretty/LICENSE` — MIT License (Josef Adamcik, 2019)

---

## Compliance Notes

### Removed unused libraries (2026-10-10 audit)
The vendored libraries `keebs.pretty-master` (CERN OHL v1.2), `Keebio-Parts.pretty`, `keyboard_parts.pretty-master`, and `ProMicro.pretty-master` had zero footprint references in `ergodash.kicad_pcb` and were removed. No active footprint depends on them; the PCB is unchanged (footprint geometry is embedded in `.kicad_pcb`). The former CERN OHL v1.2 obligation (keebs.pretty) therefore no longer applies.

### GPL-2.0-or-later (QMK firmware)
Modified firmware source is distributed alongside binaries. File-level copyright notices from upstream QMK contributors are preserved. ENCHDASH modifications are marked with Juarendra Ramadhani's copyright where files were actually modified.

**Build provenance**: per `FIRMWARE/manifest.json`, all three shipped artifacts have `provenance_status: "incomplete"` and `build_provenance: null`. Source-to-binary identity is not established. Binary distribution claims require verified build provenance and reproducible build evidence.

### MIT (ErgoDash hardware, SofleKeyboard footprints)
Original copyright notices are retained. ErgoDash attribution is provided in `docs/HARDWARE-ATTRIBUTION.md` and KiCad project metadata. The SofleKeyboard footprint library (primary layout lib, 92 instances) carries its upstream MIT license at `SofleKeyboard-footprint.pretty/LICENSE`.

### Components with Incomplete Provenance
Components marked "not independently established" for license or usage status require further investigation to determine their upstream source, license, and whether they are actively used in the current PCB design. Until provenance is confirmed, these components cannot be claimed as properly licensed for distribution.

**Compliance status**: The 2026-10-10 footprint usage audit resolved the hardware footprint provenance. Remaining open items blocking a clean full-compliance claim: the `prettylib:SK6812_mini_e_flipable` LED footprint (upstream yaemk-split-kb GPL-3.0; source lib not vendored), 3D models (`3d/`), VIA JSON licensing, and media authorship. These gaps must be resolved before asserting full compliance.

---

## Usage Determination

The footprint usage audit was performed on 2026-10-10 by parsing `(footprint "lib:name"` references in `Hardware/PCB/Rev1.2/ergodash.kicad_pcb` (119 total instances) and cross-referencing against vendored library directories. Results are recorded in the Hardware Components table above. Four zero-reference libraries were removed.

**Still pending**: 3D model (`3d/`) provenance and usage, and the SK6812 LED footprint source license.

---

## Upstream Attribution

### ErgoDash
- **Original author**: omkbd
- **Original repository**: https://github.com/omkbd/ErgoDash
- **License**: MIT License
- **Copyright**: Copyright (c) 2018 omkbd

### QMK Firmware
- **Project**: QMK Firmware
- **Repository**: https://github.com/qmk/qmk_firmware
- **License**: GPL-2.0-or-later
- **Copyright**: Multiple contributors (see individual file headers)

---

## Contact

For questions about third-party component usage or licensing:
- **Repository**: https://github.com/juarendra/ERGODASH-MOD-ENCH-OLED-QMK_VIA
- **Commercial identity**: Positron Electronic
- **Copyright holder for modifications**: Juarendra Ramadhani
