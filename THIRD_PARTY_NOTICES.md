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
| SK6812 LED footprint (`prettylib:SK6812_mini_e_flipable`, fab value `YAEMK_SK6812MINI-E`) | embedded in `ergodash.kicad_pcb` | Pad geometry per SK6812MINI-E manufacturer datasheet; footprint distributed via yaemk-split-kb (https://github.com/KarlK90/yaemk-split-kb, GPL-3.0) | Functional/factual PCB geometry — not treated as a copyrightable creative work (see Compliance Notes) | Active (12 instances) | Repository evidence: footprint usage audit (2026-10-10); geometry matches SK6812MINI-E datasheet pad/slot dimensions |
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
| Hardware photos | `DOC/HARDWARE/*.{png,jpeg}` | Original photography by Juarendra Ramadhani | MIT (owner-licensed) — Copyright (c) 2024-2026 Juarendra Ramadhani; see `LICENSES/MIT-ENCHDASH.txt` | Active | Owner-confirmed authorship (2026-10-10) |
| Schematic PDF | `Hardware/ErgoDash_Schematic.pdf` | Exported from modified KiCad files | Derived from MIT-licensed ErgoDash (omkbd, 2018) | Active | Repository evidence: generated from modified source; derivative work under MIT |
| Tutorial video | `DOC/tutorial_load_json_file.mov` | Original content by Juarendra Ramadhani | MIT (owner-licensed) — Copyright (c) 2024-2026 Juarendra Ramadhani; see `LICENSES/MIT-ENCHDASH.txt` | Active | Owner-confirmed authorship (2026-10-10) |
| User manuals | `DOC/*.pdf` | Original documentation by Juarendra Ramadhani | MIT (owner-licensed) — Copyright (c) 2024-2026 Juarendra Ramadhani; see `LICENSES/MIT-ENCHDASH.txt` | Active | Owner-confirmed authorship (2026-10-10) |

---

## 3D Models (KiCad visualization only)

3D models are referenced by KiCad footprints for the board's 3D viewer. They are **not part of the manufacturing output**: gerbers (`gerber/`, `gerber_1/`) contain only 2D copper/mask/silkscreen/drill data, and the models are not present in the shipped physical product or firmware. The PCB can be fabricated with the models absent.

| Component | Repository Path | Claimed Source | License Status | Usage Status | Evidence |
|-----------|----------------|----------------|----------------|--------------|----------|
| KiCad standard 3D models (`R0603.wrl`, `R_1206`, resistor shapes) | `${KISYS3DMOD}` (not vendored) | KiCad official 3D model library | KiCad library license (permissive) | Visualization only (15 refs) | Repository evidence: referenced via `${KISYS3DMOD}`; shipped with KiCad |
| Commodity part STEP models (`Kailh Polia.step`, `Kailh Hotswap MX v22.step`, `EC11_Rotary_Encoder_Switched.step`, `ARDUINO PRO MICRO.STEP`, `OLED 128 x 32 Display Assembly.step`, `PJ320A.STEP`, `SOD-123.step`, `TactileButton(6x3,5mm)_SMD.stp`) | `Hardware/PCB/Rev1.2/3d/` | Vendor/community CAD models of commodity parts | Vendor provenance not independently verified | Visualization only (~61 refs) | Owner-accepted (2026-10-10): models depict commodity parts, used for KiCad 3D view only, excluded from manufacturing output and shipped product |

---

## VIA Configuration

| Component | Repository Path | Claimed Source | License Status | Usage Status | Evidence |
|-----------|----------------|----------------|----------------|--------------|----------|
| VIA JSON definitions | `NEW_ErgoDash_4key_V3_mod_positron_elektronik.json` (canonical), `ErgoDash_4key_mod_positron_elektronik.json` (legacy non-V3) | Original VIA configuration by Juarendra Ramadhani (based on the VIA definition specification) | MIT (owner-licensed) — Copyright (c) 2024-2026 Juarendra Ramadhani; see `LICENSES/MIT-ENCHDASH.txt` | Active | Owner-confirmed authorship (2026-10-10): VIA JSON is owner-created configuration data; the VIA schema itself imposes no license on definitions |

---

## License Files in Repository

The following license files are present and committed:
- `LICENSES/MIT-ErgoDash.txt` — Original ErgoDash MIT License (omkbd, 2018)
- `LICENSES/MIT-ENCHDASH.txt` — MIT License for owner-created works (Juarendra Ramadhani, 2024-2026): VIA JSON, documentation, and media
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

### SK6812 LED footprint (`prettylib:SK6812_mini_e_flipable`)
This footprint originates from the yaemk-split-kb project (GPL-3.0). Only the footprint geometry is used, and it is embedded directly in `ergodash.kicad_pcb` (the `prettylib` source folder is not vendored). The pad layout, drill, and board-slot dimensions follow the SK6812MINI-E manufacturer datasheet — they describe how to physically mount a specific commodity LED part, which is functional/factual information rather than a copyrightable creative expression. On that basis the geometry is treated as not independently copyright-restricted, and no GPL-3.0 obligation is propagated to the PCB. The upstream project and its GPL-3.0 license are nonetheless credited here.

This is a deliberate owner-accepted position (recorded 2026-10-10), not a verified legal opinion. **Upgrade path**: if a stricter guarantee is required, replace this footprint with one from a permissively-licensed library (e.g. KiCad's official `LED_SMD` SK6812 footprint) and regenerate gerbers, or vendor the yaemk-split-kb library together with its GPL-3.0 license text.

### 3D models (visualization only)
The commodity-part STEP models in `Hardware/PCB/Rev1.2/3d/` are used solely by KiCad's 3D viewer. They are excluded from the manufacturing output (gerbers are 2D only) and from the shipped physical product. On that basis their vendor provenance is treated as non-blocking for distribution of the board and firmware; it is recorded here as an owner-accepted position (2026-10-10), not a verified legal opinion. KiCad's own standard 3D models (`${KISYS3DMOD}`) ship under the KiCad library license. **Upgrade path**: remove `3d/` entirely (zero impact on gerbers/PCB/firmware/product; only KiCad 3D preview loses the part models), or replace with models carrying explicit redistribution licenses.

### Components with Incomplete Provenance
Components marked "not independently established" for license or usage status require further investigation to determine their upstream source, license, and whether they are actively used in the current PCB design. Until provenance is confirmed, these components cannot be claimed as properly licensed for distribution.

**Compliance status**: The 2026-10-10 footprint usage audit resolved the hardware footprint provenance (SofleKeyboard MIT; SK6812 treated as datasheet geometry). 3D models are documented as visualization-only and excluded from manufacturing output. VIA JSON and owner-created media are owner-confirmed and MIT-licensed (`LICENSES/MIT-ENCHDASH.txt`). Remaining items are owner/toolchain/hardware-gated and not documentation gaps: QMK build provenance (`FIRMWARE/manifest.json`), USB/VIA device testing, KiCad ERC/DRC/gerber evidence, and own VID/PID allocation.

---

## Usage Determination

The footprint usage audit was performed on 2026-10-10 by parsing `(footprint "lib:name"` references in `Hardware/PCB/Rev1.2/ergodash.kicad_pcb` (119 total instances) and cross-referencing against vendored library directories. Results are recorded in the Hardware Components table above. Four zero-reference libraries were removed.

**Resolved (2026-10-10)**: VIA JSON licensing (MIT, owner) and media authorship (MIT, owner).

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
- **Repository**: https://github.com/juarendra/ENCHDASH-QMK-VIA
- **Commercial identity**: Positron Electronic
- **Copyright holder for modifications**: Juarendra Ramadhani
