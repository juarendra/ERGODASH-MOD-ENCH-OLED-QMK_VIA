# ENCHDASH Third-Party Notices

This document lists third-party components used in the ENCHDASH repository, their licenses, and modification status.

## Hardware Components

| Component | Repository Path | Upstream URL | License | Modified? | Used in Active Design? | Evidence/Status |
|-----------|----------------|--------------|---------|-----------|------------------------|-----------------|
| ErgoDash PCB design | `Hardware/PCB/Rev1.2/ergodash.*` | https://github.com/omkbd/ErgoDash | MIT | Yes | Active | Modified from ErgoDash Rev2 (2018-06-07) |
| ProMicro.pretty footprints | `Hardware/PCB/Rev1.2/ProMicro.pretty-master/` | https://github.com/Biacco42/ProMicro | MIT (Biacco42, 2017) | No | Active | Arduino Pro Micro footprints; contains derivatives of teensy 2.0 library (Ricardo Band, 2015, MIT) |
| keebs.pretty footprints | `Hardware/PCB/Rev1.2/keebs.pretty-master/` | https://github.com/egladman/keebs.pretty | CERN OHL v1.2 | No | Active | MX/Alps switch footprints, Teensy/Pro Micro modules |
| keyboard_parts.pretty | `Hardware/PCB/Rev1.2/keyboard_parts.pretty-master/` | https://github.com/tmk/keyboard_parts.pretty | Provenance not yet established | No | Usage status to be determined | TMK keyboard component library |
| Keebio-Parts.pretty | `Hardware/PCB/Rev1.2/Keebio-Parts.pretty/` | https://github.com/keebio/Keebio-Parts.pretty | Provenance not yet established | No | Usage status to be determined | Keebio component library |
| SofleKeyboard-footprint.pretty | `Hardware/PCB/Rev1.2/SofleKeyboard-footprint.pretty/` | https://github.com/josefadamcik/SofleKeyboard | Provenance not yet established | No | Usage status to be determined | Sofle keyboard footprints |
| 3D models | `Hardware/PCB/Rev1.2/3d/` | Various sources | Provenance not yet established | No | Usage status to be determined | STEP models for components |

## Firmware Components

| Component | Repository Path | Upstream URL | License | Modified? | Used in Active Design? | Evidence/Status |
|-----------|----------------|--------------|---------|-----------|------------------------|-----------------|
| QMK Firmware base | `FIRMWARE/QMK/ergodash*/` | https://github.com/qmk/qmk_firmware | GPL-2.0-or-later | Yes | Active | Modified for ENCHDASH hardware; file-level notices retained |
| ErgoDash QMK keyboard | `FIRMWARE/QMK/ergodash*/` | https://github.com/omkbd/ErgoDash (QMK integration) | GPL-2.0-or-later | Yes | Active | Modified from omkbd's ErgoDash QMK implementation |

## Documentation and Media

| Component | Repository Path | Upstream URL | License | Modified? | Used in Active Design? | Evidence/Status |
|-----------|----------------|--------------|---------|-----------|------------------------|-----------------|
| Hardware photos | `DOC/HARDWARE/*.{png,jpeg}` | Original photography | Copyright (c) 2024-2026 Juarendra Ramadhani | N/A | Active | Product photography |
| Schematic PDF | `Hardware/ErgoDash_Schematic.pdf` | Exported from modified KiCad files | Derived from MIT-licensed ErgoDash | N/A | Active | Generated from modified source |
| Tutorial video | `DOC/tutorial_load_json_file.mov` | Original content | Copyright (c) 2024-2026 Juarendra Ramadhani | N/A | Active | VIA setup tutorial |
| User manuals | `DOC/*.pdf` | Original documentation | Copyright (c) 2024-2026 Juarendra Ramadhani | N/A | Active | Indonesian/English user guides |

## VIA Configuration

| Component | Repository Path | Upstream URL | License | Modified? | Used in Active Design? | Evidence/Status |
|-----------|----------------|--------------|---------|-----------|------------------------|-----------------|
| VIA JSON definitions | `*.json` (root), `FIRMWARE/*.json` | Based on VIA specification | GPL-2.0-or-later (matching firmware) | N/A | Active | Custom definitions for ENCHDASH hardware |

## License Files

All referenced licenses are included in this repository:

- `LICENSES/MIT-ErgoDash.txt` — Original ErgoDash MIT License (omkbd, 2018)
- `LICENSES/GPL-2.0-or-later.txt` — GNU GPL v2 or later (from QMK)
- `Hardware/PCB/Rev1.2/keebs.pretty-master/LICENSE.md` — CERN OHL v1.2
- `Hardware/PCB/Rev1.2/ProMicro.pretty-master/LICENSE` — MIT License (Biacco42, Ricardo Band)

## Compliance Notes

1. **CERN OHL v1.2 (keebs.pretty)**: This license requires that modifications carry prominent notices and remain available in native CAD format. The ENCHDASH PCB files are distributed in KiCad native format and include modification history in version control.

2. **GPL-2.0-or-later (QMK firmware)**: Modified firmware source is distributed alongside binaries. File-level copyright notices from upstream QMK contributors are preserved. ENCHDASH modifications are marked with Juarendra Ramadhani's copyright where files were actually modified.

3. **MIT (ErgoDash hardware, ProMicro.pretty)**: Original copyright notices are retained. Attribution is provided in `docs/HARDWARE-ATTRIBUTION.md` and KiCad project metadata.

4. **Provenance incomplete**: Components marked "provenance not yet established" require further investigation to determine their upstream source, license, and whether they are actively used in the current PCB design. Until provenance is confirmed, these components cannot be claimed as properly licensed for distribution.

## Usage Determination

To determine which footprint libraries are actively used:

1. Open `Hardware/PCB/Rev1.2/ergodash.kicad_pcb` in KiCad
2. Generate a footprint usage report
3. Cross-reference with library directories

This verification has not yet been performed. The "Usage status to be determined" entries above should be updated with concrete evidence before claiming full compliance.

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

## Contact

For questions about third-party component usage or licensing:
- Repository: https://github.com/juarendra/ERGODASH-MOD-ENCH-OLED-QMK_VIA
- Commercial identity: Positron Electronic
- Copyright holder for modifications: Juarendra Ramadhani
