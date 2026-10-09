# Repository Guidelines

## Project Overview

ErgoDash keyboard firmware mod with encoder, OLED, hotswap support. QMK firmware for ATmega32u4 (Arduino Pro Micro Type-C). VIA-compatible for runtime keymap programming without reflashing.

Four firmware variants in `FIRMWARE/QMK/`:
- `ergodash_mod_v3` — base with encoder + OLED
- `ergodash_wpm_nomousekey` — adds WPM tracking, removes mouse keys
- `ergodash_nowpm_mousekey` — no WPM, has mouse keys
- `ergodash` — minimal base

## Architecture & Data Flow

Split keyboard architecture:
- Left/right halves communicate via SOFT_SERIAL_PIN (D2)
- Master half handles USB, OLED status display
- Slave half shows static logo
- Matrix scanning: 6 rows × 7 cols per half (doubled to 12 rows total)
- Encoder support: left encoder (F4/B6), right encoder with separate resolution

Layer system:
- 4 layers: QWERTY (0), COLEMAK (1), LOWER (2), RAISE (3)
- MO() for momentary layer activation
- `CYCLE` custom keycode rotates base layers

Feature modules:
- RGB underglow: WS2812 on D3, 24 LEDs (12 per side)
- OLED: 270° rotation, master shows layer/caps status, slave shows logo
- Encoder map: volume/page on layer 0, RGB controls on layers 2-3

## Key Directories

```
FIRMWARE/QMK/ergodash_mod_v3/
├── config.h              — keyboard-level feature flags (empty, uses rev1)
├── rules.mk              — MCU, bootloader, feature enables
├── ergodash.c/h          — keyboard init (minimal)
├── info.json             — VIA metadata
└── rev1/
    ├── config.h          — pin definitions, matrix size, RGB/OLED config
    ├── rev1.c/h          — hardware revision code
    └── keymaps/default/
        ├── keymap.c      — layer definitions, encoder map, process_record_user
        ├── oled.c        — OLED rendering logic (included via #include)
        ├── config.h      — keymap-specific overrides
        └── rules.mk      — keymap feature overrides (empty)

Hardware/                 — PCB gerbers, schematic, 3D case
DOC/                      — user manuals (Indonesian)
*.json                    — VIA definition files
```

## Development Commands

This repo contains pre-compiled firmware, not a buildable QMK environment. To modify:

1. Copy one variant to QMK firmware tree:
   ```bash
   cp -r FIRMWARE/QMK/ergodash_mod_v3 <qmk_firmware>/keyboards/ergodash_mod_v3
   ```

2. Build from QMK root:
   ```bash
   qmk compile -kb ergodash_mod_v3/rev1 -km default
   ```

3. Flash:
   ```bash
   qmk flash -kb ergodash_mod_v3/rev1 -km default
   # Or use precompiled .hex with QMK Toolbox, AVRdude, etc.
   ```

Pre-compiled .hex files in `FIRMWARE/`:
- `ergodash_rev1_via.hex` — main VIA firmware
- `omkbd_ergodash_rev1_wpmnomousekey.hex` — WPM variant
- `omkbd_ergodash_rev1_nowpmmousekey.hex` — mouse key variant

## Code Conventions & Common Patterns

### File Organization
- Hardware config in `rev1/config.h`
- Feature toggles in `rules.mk`
- All keymaps in `keymap.c`
- OLED code in separate `oled.c`, included via `#include` (not compiled separately)

### Naming
- Layers: `_QWERTY`, `_COLEMAK`, `_LOWER`, `_RAISE` (underscore prefix)
- Custom keycodes: `PLACEHOLDER`, `CYCLE` (enum starting at SAFE_RANGE)
- Pin defines: `MATRIX_ROW_PINS`, `ENCODERS_PAD_A`, `WS2812_DI_PIN`
- QMK keycodes: `KC_` prefix (e.g., `KC_VOLU`, `KC_TAB`)
- Modifier macros: `MO(layer)`, `LCTL(KC_C)`, `LCA(KC_DEL)`

### Common Patterns
- Matrix: `LAYOUT()` macro defines physical-to-logical mapping, 6 extra encoder positions at end
- Layers: use `_______` (transparent) to pass through lower layer, `KC_TRNS` equivalent
- Custom keycode handling: `process_record_user()`, check `record->event.pressed`, return `keycode < SAFE_RANGE`
- OLED: `oled_task_user()` split by `is_keyboard_master()`, returns `false` to yield
- Encoder: `encoder_map[][]` 2D array per layer, `ENCODER_CCW_CW(down, up)` macro
- Memory optimization: PROGMEM for const data, early returns in switch statements

### Feature Flags (rules.mk)
```makefile
MOUSEKEY_ENABLE = yes       # Mouse keys
EXTRAKEY_ENABLE = yes       # Media keys
NKRO_ENABLE = yes           # N-key rollover
RGBLIGHT_ENABLE = yes       # RGB underglow
ENCODER_ENABLE = yes        # Rotary encoders
ENCODER_MAP_ENABLE = yes    # Encoder keycode map
SPLIT_KEYBOARD = yes        # Split comms
```

### Pin Assignments (rev1/config.h)
```c
MATRIX_ROW_PINS { D4, D7, E6, B4, B5, B0 }
MATRIX_COL_PINS { C6, F5, F6, F7, B1, B3, B2 }
ENCODERS_PAD_A { F4 }
ENCODERS_PAD_B { B6 }
WS2812_DI_PIN D3
SOFT_SERIAL_PIN D2
```

### Error Handling
Embedded firmware, no dynamic allocation. No error handling in user code — QMK handles USB, matrix scan failures internally.

## Important Files

- `FIRMWARE/QMK/ergodash_mod_v3/rev1/keymaps/default/keymap.c` — main keymap, custom keycodes, encoder map
- `FIRMWARE/QMK/ergodash_mod_v3/rev1/config.h` — pin definitions, timing, RGB/OLED settings
- `FIRMWARE/QMK/ergodash_mod_v3/rules.mk` — MCU (atmega32u4), bootloader (caterina), feature enables
- `NEW_ErgoDash_4key_V3_mod_positron_elektronik.json` — VIA layout definition
- `README.md` — user guide (Indonesian/English), VIA setup, keycode reference

## Runtime/Tooling Preferences

- **MCU**: ATmega32u4 (16 MHz, 32 KB flash, 2.5 KB RAM)
- **Bootloader**: Caterina (Arduino-compatible, 500 ms timeout)
- **Toolchain**: avr-gcc, QMK CLI
- **Flashing**: QMK Toolbox, avrdude, or `qmk flash`
- **Configuration**: VIA for runtime remapping (no rebuild needed)
- **Memory constraints**: Program space critical (~80% used with all features), use PROGMEM for large const data

## Testing & QA

No automated tests. Verification process:

1. Compile size check: must fit in 28672 bytes (32 KB - bootloader)
2. Flash both halves
3. Physical test matrix:
   - All keys register in VIA
   - Both encoders rotate/click
   - Layer switching works
   - OLED displays correct layer/status
   - RGB effects cycle
   - Split communication stable

4. VIA compatibility:
   - Load JSON definition
   - Remap keys without reflash
   - Encoder assignments work
   - Macros function

## Common Modifications

### Add new layer
1. Add enum to `custom_layers`
2. Define `[_NEWLAYER] = LAYOUT(...)` in `keymaps[]`
3. Add encoder row to `encoder_map[]`
4. Update OLED `print_status_narrow()` switch case

### Change encoder behavior
Edit `encoder_map[][]` in `keymap.c`. Each layer gets 2 encoders × 2 directions:
```c
[layer] = { ENCODER_CCW_CW(down, up), ENCODER_CCW_CW(down, up) }
```

### Adjust RGB
In `rev1/config.h`:
- LED count: `RGBLED_NUM`
- Brightness: `RGBLIGHT_LIMIT_VAL` (max 100 to stay under 500 mA USB limit)
- Effects: enable/disable `RGBLIGHT_EFFECT_*` defines

### OLED customization
Edit `oled.c`:
- `render_logo()` — 128-byte bitmap array
- `print_status_narrow()` — text content
- `oled_init_user()` — rotation (270° for vertical mount)

### Flash size optimization
Disable unused RGB effects, reduce `RGBLED_NUM`, remove mouse keys, disable console/command. Check size: `qmk compile` reports bytes used.
