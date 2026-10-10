# ENCHDASH Hardware Attribution

This document describes the origin of the ENCHDASH hardware design, modifications made from the original ErgoDash, and the boundaries between original and derivative work.

---

## Evidence Classification

This attribution is structured by evidence class:

1. **Repository evidence**: values and source files directly visible in the current repository (QMK source, KiCad file presence, info.json metadata).
2. **Owner/hardware evidence required**: physical PCB characteristics, routing, mechanical fit, sold-unit revision, ERC/DRC results, silkscreen, and first-article validation. See `docs/evidence/kicad-owner-verification.md` for the owner-evidence checklist.
3. **Historical attribution**: upstream projects (omkbd/ErgoDash, QMK) and their licenses, stated factually without implying endorsement.

Physical hardware claims not grounded in repository source or owner-supplied evidence are marked as requiring owner verification.

---

## Historical Attribution: ErgoDash by omkbd

ENCHDASH is derived from **ErgoDash**, an open-source split ergonomic keyboard designed by **omkbd**.

- **Designer**: omkbd
- **Original repository**: https://github.com/omkbd/ErgoDash
- **License**: MIT License
- **Copyright**: Copyright (c) 2018 omkbd
- **Date in repository title block**: 2018-06-07 (`Hardware/PCB/Rev1.2/ergodash.kicad_pcb` line 1)

The ErgoDash project provided:
- Schematic design for a split ergonomic keyboard using Pro Micro controllers
- PCB layout for 7×6 key matrix per half with MX switch footprints
- KiCad design files (schematic, PCB, footprint libraries)
- QMK firmware integration for the ErgoDash keyboard

ErgoDash itself was inspired by the ergonomic keyboard community and follows common split keyboard conventions. It is not derived from a single upstream project but represents an original design contribution to the mechanical keyboard ecosystem.

---

## Repository Evidence: Firmware Source

The following facts are verifiable from the QMK source trees in `FIRMWARE/QMK/ergodash/`, `FIRMWARE/QMK/ergodash_nowpm_mousekey/ergodash/`, `FIRMWARE/QMK/ergodash_wpm_nomousekey/ergodash/`, and `FIRMWARE/ergodash_mod_v3/`:

### USB Device Descriptor (from `info.json`)
- `keyboard_name`: "ErgoDash Hotswap By Positron"
- `manufacturer`: "Positron Electronic"
- USB VID:PID: `0x1209:0x2013` (allocated under pid.codes, org Positron-Electronic; registration PR pidcodes/pidcodes.github.com#1303). Legacy was `0x4D44:0x6061` (upstream, retired).
- **Provenance status**: incomplete (per `FIRMWARE/manifest.json`). Shipped `.hex` are built from this source with the new identity; functional hardware attestation pending re-test.

### Enabled Features (from `rules.mk`, `config.h`, keymaps)
- **Bootloader**: `caterina` (Arduino-compatible)
- **Split keyboard**: `SPLIT_KEYBOARD = yes`
- **OLED**: `OLED_ENABLE = yes`, driver SSD1306
- **Encoder**: `ENCODER_ENABLE = yes`
- **VIA**: `VIA_ENABLE = yes`
- **RGB underglow**: `RGBLIGHT_ENABLE = yes` (firmware toggle; hardware routing not verified from firmware alone)
- **NKRO**: `NKRO_ENABLE = yes`

### Pin Definitions (from `FIRMWARE/QMK/ergodash/rev1/config.h`)
- **Matrix rows**: `D4, D7, E6, B4, B5, B0`
- **Matrix columns**: `C6, F5, F6, F7, B1, B3, B2`
- **Encoder pads**: `ENCODERS_PAD_A { F4 }`, `ENCODERS_PAD_B { B6 }`
- **WS2812 data**: `D3`
- **Split serial**: `SOFT_SERIAL_PIN D2`

### Firmware Modifications
- Added encoder map definitions (`encoder_map[][]`)
- Implemented OLED rendering functions (`oled.c`) with custom graphics and status display
- Modified `config.h` to define encoder pins, OLED settings, RGB configuration
- Added `info.json` metadata for VIA compatibility
- Modified USB device descriptor as shown above

### Firmware Source and Licensing
ENCHDASH firmware is derived from:
1. **QMK Firmware** (https://github.com/qmk/qmk_firmware) — GPL-2.0-or-later
2. **omkbd's ErgoDash QMK integration** (part of the QMK repository) — GPL-2.0-or-later

QMK core code is unmodified and used as-is from upstream. The omkbd ErgoDash keyboard implementation was used as a base and modified for ENCHDASH features. All modifications retain GPL-2.0-or-later licensing and upstream copyright notices.

### OLED Bus Clarification
The firmware enables QMK OLED support and split-display behavior. The current repository does not establish that the OLED electrical bus is the split serial transport; confirm the bus and routing from the KiCad schematic before making that claim.

---

## Owner/Hardware Evidence Required

The following claims require owner-supplied evidence per `docs/evidence/kicad-owner-verification.md`:

### Physical PCB Characteristics
- **Hotswap sockets**: Kailh hotswap socket footprints present in KiCad files; physical population and routing integrity require owner verification (PCB inspection, first-article photo, or Gerber review).
- **Encoder routing**: Encoder footprints present in KiCad files; electrical routing to F4/B6 and mechanical fit require schematic and Gerber verification.
- **OLED routing**: OLED module footprints present in KiCad files; I²C bus routing, power distribution, and split-serial integration require schematic verification.
- **USB Type-C**: Footprint compatibility with Pro Micro Type-C clones stated; verify connector pinout and mechanical fit from schematic and first-article.
- **RGB underglow routing**: WS2812 data line (D3) and power routing for 24 LEDs (12 per half) stated; verify routing and LED count from schematic and Gerber.
- **Switch layout preservation**: Claim that MX spacing and key positions match original ErgoDash requires side-by-side PCB comparison or owner attestation.
- **Mounting holes**: Claim that mounting holes remain unchanged from original ErgoDash requires PCB comparison or owner attestation.
- **Case ancestry**: Custom 3D-printed case stated as "not derived from omkbd's case files"; verify case model provenance and independence from any upstream case design.

### PCB Title Block and Silkscreen
- **Title block identity**: Modified title block to reflect ENCHDASH identity stated; current repository files retain original omkbd markings pending silkscreen update per `docs/SILKSCREEN-GUIDE.md`. Verify silkscreen changes from Gerber or first-article photo.

### Electrical Design and Validation
- **Matrix wiring**: 6 rows × 7 columns per half, diode direction COL2ROW stated; verify from schematic.
- **Communication**: TRRS cable carrying serial data (SOFT_SERIAL_PIN D2) and power stated; verify TRRS pinout and routing from schematic.
- **Split detection**: USB presence detection on master half stated; verify split detection circuit from schematic.
- **ERC/DRC**: Electrical and design rule checks not recorded; run and document per owner-evidence checklist.

### Sold Unit Revision
- **"Rev2" claim**: The baseline attribution stated "modifications to the original ErgoDash Rev2 design." The repository KiCad files are in `Hardware/PCB/Rev1.2/`. Verify the sold unit's actual revision and its correspondence to repository files.

---

## Attribution Chain

```
Original ErgoDash (2018)
  Designer: omkbd
  License: MIT
  Scope: Hardware design (schematic, PCB, KiCad files)
  
  ↓ Derived work

ENCHDASH (2024–2026)
  Modifier: Juarendra Ramadhani
  Commercial identity: Positron Electronic
  License: MIT (hardware), GPL-2.0-or-later (firmware)
  Scope: Hotswap, encoder, OLED, Type-C, firmware modifications (per repository evidence and owner verification)
```

---

## Files Modified from Original ErgoDash

### KiCad Hardware Files (repository evidence: file presence and modification history)
- `Hardware/PCB/Rev1.2/ergodash.kicad_pcb` — PCB layout (encoder, OLED, hotswap footprints visible in file; routing and correctness require schematic verification)
- `Hardware/PCB/Rev1.2/ergodash.kicad_sch` — Schematic (encoder, OLED routing claimed; verify from schematic inspection)
- `Hardware/PCB/Rev1.2/ergodash.kicad_pro` — Project settings
- Title block metadata (to be updated per `docs/SILKSCREEN-GUIDE.md`)

### Firmware Files (QMK-derived)
All files in `FIRMWARE/QMK/ergodash*/` are modifications of the upstream omkbd ErgoDash QMK implementation:
- `config.h` — encoder, OLED, RGB settings (values listed in Repository Evidence section)
- `rules.mk` — enabled encoder, OLED features
- `keymap.c` — modified keymaps, added encoder map
- `oled.c` — new file, OLED rendering logic
- `info.json` — VIA metadata and USB descriptor

---

## Third-Party Components Used

ENCHDASH hardware files include third-party footprint libraries and 3D models. See [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) for:
- ProMicro.pretty (MIT, Biacco42)
- keebs.pretty (CERN OHL v1.2, egladman)
- Other footprint libraries and 3D models (provenance incomplete)

These components are not part of the original ErgoDash distribution and were added during ENCHDASH development.

---

## Design Philosophy

ENCHDASH is a **compatibility-preserving enhancement** of ErgoDash:
- Maintains original matrix layout and electrical design (subject to schematic verification)
- Adds user-requested features (hotswap, encoder, OLED) without breaking core design (subject to owner verification)
- Keeps Pro Micro pinout compatibility for easy controller replacement (subject to schematic verification)
- Respects original design intent while extending functionality

This approach ensures that ENCHDASH remains recognizable as an ErgoDash derivative while adding practical improvements for modern keyboard users.

---

## Trademark and Endorsement

**"ErgoDash"** is the name of omkbd's original design. ENCHDASH uses this name factually for attribution purposes only.

**ENCHDASH is not:**
- An official ErgoDash product
- Endorsed, approved, or maintained by omkbd
- Affiliated with the original ErgoDash project

**ENCHDASH is:**
- An independent derivative work
- Permitted under the MIT License granted by omkbd
- A separate product with its own identity and support

---

## Contact

For questions about ENCHDASH hardware modifications:
- **Repository**: https://github.com/juarendra/ERGODASH-MOD-ENCH-OLED-QMK_VIA
- **Commercial identity**: Positron Electronic
- **Copyright holder (modifications)**: Juarendra Ramadhani

For questions about the original ErgoDash design:
- **Original repository**: https://github.com/omkbd/ErgoDash
- **Original designer**: omkbd

---

## License

This attribution document is part of the ENCHDASH repository and is provided under the same MIT License as the hardware modifications. See [LICENSE](../LICENSE) for details.

The original ErgoDash design remains under its original MIT License. See [LICENSES/MIT-ErgoDash.txt](../LICENSES/MIT-ErgoDash.txt) for the unmodified upstream license text.
