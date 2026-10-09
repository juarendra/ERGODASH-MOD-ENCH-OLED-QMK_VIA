# ENCHDASH Hardware Attribution

This document describes the origin of the ENCHDASH hardware design, modifications made from the original ErgoDash, and the boundaries between original and derivative work.

---

## Original Design: ErgoDash by omkbd

ENCHDASH is derived from **ErgoDash**, an open-source split ergonomic keyboard designed by **omkbd** and released in 2018.

- **Designer**: omkbd
- **Original repository**: https://github.com/omkbd/ErgoDash
- **License**: MIT License
- **Copyright**: Copyright (c) 2018 omkbd
- **Original release date**: 2018-06-07 (based on PCB title block in repository)

The ErgoDash project provided:
- Schematic design for a split ergonomic keyboard using Pro Micro controllers
- PCB layout for 7×6 key matrix per half with MX switch footprints
- KiCad design files (schematic, PCB, footprint libraries)
- QMK firmware integration for the ErgoDash keyboard

ErgoDash itself was inspired by the ergonomic keyboard community and follows common split keyboard conventions. It is not derived from a single upstream project but represents an original design contribution to the mechanical keyboard ecosystem.

---

## ENCHDASH Modifications

ENCHDASH adds the following modifications to the original ErgoDash Rev2 design:

### Hardware Changes

1. **Hotswap Socket Support**
   - Added Kailh hotswap socket footprints to enable tool-free switch replacement
   - Modified PCB routing to accommodate socket clearance and mechanical stress

2. **Rotary Encoder Integration**
   - Added rotary encoder footprints (1 per half)
   - Routed encoder pins to available GPIO on Pro Micro (F4, B6 on master half)
   - Modified firmware to support encoder input via QMK `ENCODER_ENABLE`

3. **OLED Display Support**
   - Added 128×32 OLED module footprints and I²C routing (1 per half)
   - Implemented split OLED firmware logic (master displays status, slave displays logo)
   - OLED communicates via I²C on split keyboard serial line

4. **USB Type-C Controller**
   - Original design used Pro Micro with Mini-B USB
   - ENCHDASH uses Arduino Pro Micro clones with USB Type-C connectors
   - PCB footprint remains compatible with standard Pro Micro pinout

5. **RGB Underglow Routing**
   - Original ErgoDash had RGB support but not fully routed in all variants
   - ENCHDASH ensures WS2812 data line (D3) and power routing for 24 LEDs (12 per half)

6. **PCB Silkscreen and Markings**
   - Modified title block to reflect ENCHDASH identity (to be applied per owner guide)
   - Current repository PCB files retain original omkbd markings pending silkscreen update

### Electrical Design Unchanged

The following remain identical to the original ErgoDash:

- Controller: ATmega32u4 via Arduino Pro Micro
- Matrix wiring: 6 rows × 7 columns per half, diode direction COL2ROW
- Communication: TRRS cable carrying serial data (SOFT_SERIAL_PIN D2) and power
- Bootloader: Caterina (Arduino-compatible)
- Split detection: USB presence detection on master half

### Mechanical Design

- **Switch layout**: Unchanged from ErgoDash (MX spacing, key positions)
- **Mounting holes**: Unchanged
- **Case design**: Custom 3D-printed case designed for ENCHDASH (not derived from omkbd's case files, if any existed)

---

## Firmware Modifications

ENCHDASH firmware is derived from:

1. **QMK Firmware** (https://github.com/qmk/qmk_firmware) — GPL-2.0-or-later
2. **omkbd's ErgoDash QMK integration** (part of the QMK repository) — GPL-2.0-or-later

### Firmware Changes

- Added encoder map definitions (`ENCODER_MAP_ENABLE`, `encoder_map[][]`)
- Implemented OLED rendering functions (`oled.c`) with custom graphics and status display
- Modified `config.h` to define encoder pins, OLED settings, RGB configuration
- Added `info.json` metadata for VIA compatibility
- Modified USB device descriptor: `keyboard_name: ErgoDash Hotswap By Positron`, `manufacturer: Positron Electronic`
- USB VID:PID remains `0x4D44:0x6061` (provenance under audit)

### Firmware Boundaries

- QMK core code: unmodified, used as-is from upstream
- omkbd's ErgoDash keyboard implementation: used as a base, modified for ENCHDASH features
- ENCHDASH-specific code: encoder handling, OLED rendering, feature toggles
- All modifications retain GPL-2.0-or-later licensing and upstream copyright notices

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
  Scope: Hotswap, encoder, OLED, Type-C, firmware modifications
```

---

## Files Modified from Original ErgoDash

### KiCad Hardware Files

- `Hardware/PCB/Rev1.2/ergodash.kicad_pcb` — PCB layout (added encoder, OLED, hotswap footprints)
- `Hardware/PCB/Rev1.2/ergodash.kicad_sch` — Schematic (added encoder, OLED routing)
- `Hardware/PCB/Rev1.2/ergodash.kicad_pro` — Project settings
- Title block metadata (to be updated per `docs/SILKSCREEN-GUIDE.md`)

### Firmware Files (QMK-derived)

All files in `FIRMWARE/QMK/ergodash*/` are modifications of the upstream omkbd ErgoDash QMK implementation:

- `config.h` — added encoder, OLED, RGB settings
- `rules.mk` — enabled encoder, OLED features
- `keymap.c` — modified keymaps, added encoder map
- `oled.c` — new file, OLED rendering logic
- `info.json` — VIA metadata

### Files Unchanged from Original

- Matrix pin definitions (rows, columns)
- Bootloader selection
- Split keyboard communication protocol
- Core electrical design

---

## Third-Party Components Used

ENCHDASH hardware files include third-party footprint libraries and 3D models. See [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) for:

- ProMicro.pretty (MIT, Biacco42)
- keebs.pretty (CERN OHL v1.2, egladman)
- Other footprint libraries and 3D models

These components are not part of the original ErgoDash distribution and were added during ENCHDASH development.

---

## Design Philosophy

ENCHDASH is a **compatibility-preserving enhancement** of ErgoDash:

- Maintains original matrix layout and electrical design
- Adds user-requested features (hotswap, encoder, OLED) without breaking core design
- Keeps Pro Micro pinout compatibility for easy controller replacement
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
