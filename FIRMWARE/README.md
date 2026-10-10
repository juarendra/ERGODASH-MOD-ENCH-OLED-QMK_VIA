# ENCHDASH Firmware Guide

This guide helps you select, flash, and build firmware for your ENCHDASH keyboard.

---

## Quick Start: Which Firmware Should I Use?

The repository maps these artifacts to Rev1.2 source files. Physical sold-unit marking and compatibility are not independently evidenced here. Confirm the PCB marking and matching VIA definition before flashing; do not cross-flash an unconfirmed revision. USB VID:PID `0x4D44:0x6061` is kept as a recorded legacy descriptor value; allocation provenance remains under audit per FIRMWARE/manifest.json.

| Firmware File | Best For | Features | VIA JSON |
|---------------|----------|----------|----------|
| **ergodash_rev1_via.hex** | Most users | Base VIA, encoder, OLED, RGB | `ErgoDash_4key_mod_positron_elektronik.json` |
| **omkbd_ergodash_rev1_nowpmmousekey.hex** | Users who need mouse keys | Mouse key support, no WPM tracking | `NEW_ErgoDash_4key_V3_mod_positron_elektronik.json` |
| **omkbd_ergodash_rev1_wpmnomousekey.hex** | Users who want WPM display | WPM tracking on OLED, no mouse keys | `NEW_ErgoDash_4key_V3_mod_positron_elektronik.json` |

**VIA JSON location**: the VIA JSON files referenced by the manifest live in the repository root (one level above this directory) — `ErgoDash_4key_mod_positron_elektronik.json` and `NEW_ErgoDash_4key_V3_mod_positron_elektronik.json`. `FIRMWARE/ErgoDash_4key_V3_mod_positron_elektronik.json` is an older copy without the rgblight menu and is not referenced by the manifest.

**Default recommendation**: `ergodash_rev1_via.hex` — covers most use cases.

---

**Feature comparison ground truth**: Cells reflect the mapped source tree's `rules.mk` and `config.h` settings. Shipped-binary features are not independently verified. The base variant's source tree enables WPM in `rev1/keymaps/default/rules.mk`.

## Firmware Feature Comparison

| Feature | ergodash_rev1_via | omkbd_nowpmmousekey | omkbd_wpmnomousekey |
|---------|-------------------|---------------------|---------------------|
| VIA support | ✅ | ✅ | ✅ |
| Rotary encoder | ✅ | ✅ | ✅ |
| OLED display | ✅ (status) | ✅ (status) | ✅ (status + WPM) |
| RGB underglow | ✅ | ✅ | ✅ |
| N-key rollover | ✅ | ✅ | ✅ |
| Mouse keys | ❌ | ✅ | ❌ |
| WPM tracking | ⚠️ | ❌ | ✅ |
| HEX file size | ~77.7 KB | ~78.5 KB | ~78.4 KB |

⚠️ **base variant WPM status**: The source tree `FIRMWARE/QMK/ergodash/rev1/keymaps/default/rules.mk` contains `WPM_ENABLE = yes`, so the shipped `ergodash_rev1_via.hex` binary's WPM behavior is ambiguous. Cell marked ⚠️.

**Flash limit note**: No combined mouse-keys + WPM variant has a size report. Do not publish a combined variant until a size report proves it fits. Note: two omkbd variants ship with exactly one of mouse keys or WPM enabled; no combined-build evidence exists.

---

## Flashing Pre-Compiled Firmware

### Prerequisites

- ENCHDASH keyboard with USB cable
- QMK Toolbox (recommended) or avrdude
- Firmware `.hex` file from `FIRMWARE/` directory
- Matching VIA JSON file

### Method 1: QMK Toolbox (Easiest)

1. **Download QMK Toolbox**: https://github.com/qmk/qmk_toolbox/releases
   - Windows: `qmk_toolbox.exe`
   - macOS: `QMK.Toolbox.app.zip`
   - Linux: `qmk_toolbox.pkg.tar.zst`

2. **Open QMK Toolbox**

3. **Select firmware**:
   - Click **"Open"**
   - Navigate to `FIRMWARE/` directory
   - Select your chosen `.hex` file

4. **Enter bootloader mode**:
   - Connect keyboard to PC
   - Press the reset button on the Pro Micro (or bridge RST to GND twice quickly)
   - QMK Toolbox will show: `*** Caterina device connected`

5. **Flash**:
   - Click **"Flash"**
   - Wait for completion: `avrdude done. Thank you.`

6. **Verify**:
   - Keyboard should reconnect automatically
   - Test keys and encoder

### Method 2: Command Line (avrdude)

**Windows**:
```cmd
avrdude -p atmega32u4 -c avr109 -P COM3 -U flash:w:FIRMWARE/ergodash_rev1_via.hex:i
```

**Linux/macOS**:
```bash
avrdude -p atmega32u4 -c avr109 -P /dev/ttyACM0 -U flash:w:FIRMWARE/ergodash_rev1_via.hex:i
```

Replace:
- `COM3` (Windows) or `/dev/ttyACM0` (Linux/macOS) with your keyboard's serial port
- `ergodash_rev1_via.hex` with your chosen firmware file

**Finding the port**:
- **Windows**: Device Manager → Ports (COM & LPT) → look for "USB Serial Device"
- **Linux**: `ls /dev/ttyACM*`
- **macOS**: `ls /dev/tty.usbmodem*`

---

## VIA Setup After Flashing

1. **Download VIA**:
   - Desktop: https://github.com/the-via/releases/releases
   - Web: https://usevia.app/

2. **Load the correct VIA JSON**:
   - Open VIA → **Settings** → enable **"Show Design Tab"**
   - Go to **Design** tab → **Load**
   - Select the JSON file matching your firmware (see table above)

3. **Configure keys**:
   - Go to **Configure** tab
   - Click any key to remap it
   - Program encoders using QMK keycode syntax (see [Encoder Programming](#encoder-programming))

---

## Encoder Programming

Encoders are programmed in VIA using the **"Any"** key type with QMK keycodes.

### Common Encoder Keycodes

| Action | Keycode | Description |
|--------|---------|-------------|
| Volume up/down | `KC_VOLU`, `KC_VOLD` | Media volume control |
| Page up/down | `KC_PGUP`, `KC_PGDN` | Scroll pages |
| Alt-Tab | `LALT(KC_TAB)` | Switch windows |
| Ctrl-C / Ctrl-V | `LCTL(KC_C)`, `LCTL(KC_V)` | Copy/paste |
| Zoom in/out | `LCTL(KC_PLUS)`, `LCTL(KC_MINS)` | Browser/app zoom |
| Layer switch | `MO(1)` | Momentarily activate layer 1 |
| RGB brightness | `RGB_VAI`, `RGB_VAD` | Increase/decrease RGB brightness |

### Encoder Setup in VIA

1. Select the encoder position (last 6 keys in the layout, typically off-screen)
2. Click the key
3. Go to **"Special"** → **"Any"**
4. Enter the QMK keycode (e.g., `KC_VOLU`)
5. Assign clockwise and counter-clockwise actions separately

**Full keycode reference**: https://github.com/qmk/qmk_firmware/blob/master/docs/keycodes.md

---

## Building Firmware from Source

### Prerequisites

- QMK development environment: https://docs.qmk.fm/#/newbs_getting_started
- Python 3.8+
- Git
- `qmk` CLI tool

### Setup QMK

```bash
# Clone QMK firmware
git clone https://github.com/qmk/qmk_firmware.git
cd qmk_firmware

# Install dependencies
qmk setup

# Copy ENCHDASH source trees to QMK
cp -r /path/to/ENCHDASH/FIRMWARE/QMK/ergodash keyboards/ergodash
cp -r /path/to/ENCHDASH/FIRMWARE/QMK/ergodash_nowpm_mousekey/ergodash keyboards/ergodash_nowpm_mousekey
cp -r /path/to/ENCHDASH/FIRMWARE/QMK/ergodash_wpm_nomousekey/ergodash keyboards/ergodash_wpm_nomousekey
```

**Provenance note**: The QMK base commit is not pinned or recorded (provenance incomplete per FIRMWARE/manifest.json). These commands are an unverified procedure — see `docs/evidence/qmk-build.md` for the blocked baseline procedure.

### Build Commands

**Base firmware (ergodash_rev1_via.hex)**:
```bash
qmk compile -kb ergodash/rev1 -km default
```

**Mouse keys variant (nowpm)**:
```bash
qmk compile -kb ergodash_nowpm_mousekey/rev1 -km default
```

Mouse keys are enabled in `keyboards/ergodash_nowpm_mousekey/rules.mk` (`MOUSEKEY_ENABLE = yes`). The user does not edit it.

**WPM tracking variant (wpm)**:
```bash
qmk compile -kb ergodash_wpm_nomousekey/rev1 -km default
```

WPM is enabled in `keyboards/ergodash_wpm_nomousekey/rev1/keymaps/default/rules.mk` (`WPM_ENABLE = yes`). The nowpm tree has `#WPM_ENABLE = yes` commented out.

**Output**: `.hex` file in `qmk_firmware/.build/`

### Flash from QMK CLI

```bash
qmk flash -kb ergodash/rev1 -km default
```

This compiles and flashes in one command. Press reset when prompted.

---

## Troubleshooting

### "Device not found" when flashing

- **Check USB cable**: Use a data cable, not charge-only
- **Enter bootloader**: Press reset button or bridge RST to GND twice quickly (within 500 ms)
- **Check port**: Verify correct COM port or `/dev/ttyACM*`
- **Driver issues (Windows)**: Install Caterina bootloader driver from QMK Toolbox

### VIA does not detect keyboard

1. **Load VIA JSON manually** (see [VIA Setup](#via-setup-after-flashing))
2. **Verify firmware**: Ensure you flashed a VIA-enabled firmware variant
3. **Check USB VID:PID**: All ENCHDASH firmware uses `0x4D44:0x6061`
4. **Try VIA web version**: https://usevia.app/ (uses WebHID, no drivers needed)

### Keys not working after flash

- **Check both halves**: Ensure TRRS cable is connected before powering on
- **Test each half**: Connect each half directly via USB to isolate issues
- **Matrix test**: Use VIA's "Key Tester" or QMK's `CONSOLE_ENABLE` debug mode

### Flash memory full

ATmega32u4 has 28 KB available for firmware (32 KB - 4 KB bootloader). If compile fails with "sketch too large":

1. Disable unused features in `rules.mk`:
   - `MOUSEKEY_ENABLE = no`
   - `CONSOLE_ENABLE = no`
   - `COMMAND_ENABLE = no`
2. Remove unused RGB effects in `config.h`
3. Simplify OLED graphics (smaller bitmaps, less text)

### Encoder not working

- **Check wiring**: Encoder pins must match `config.h` definitions (`ENCODERS_PAD_A`, `ENCODERS_PAD_B`)
- **Physical installation**: Ensure encoder is soldered correctly
- **VIA programming**: Verify encoder keycodes are assigned in VIA

---

## Firmware Provenance and Verification

All distributed firmware binaries are documented in `FIRMWARE/manifest.json` with:

- SHA-256 checksums
- Source path
- VIA JSON pairing
- Build provenance status

**Verify firmware integrity**:

```bash
# Windows
certutil -hashfile FIRMWARE/ergodash_rev1_via.hex SHA256

# Linux/macOS
sha256sum FIRMWARE/ergodash_rev1_via.hex
```

Compare output with `manifest.json`.

**Provenance status**:
- **incomplete**: Historical build info not yet reconstructed; binary shipped with product but QMK base commit unknown
- **verified**: Source-to-binary reproducibility confirmed
- **functionally rebuilt**: Recompiled from source, functionally equivalent, minor hash differences

See `manifest.json` for current status of each firmware variant.

---

## Advanced: Custom Firmware Features

### Enabling Features via `rules.mk`

Edit `keyboards/ergodash/rules.mk` (or the variant tree you're customizing):

```makefile
MOUSEKEY_ENABLE = yes       # Mouse keys
EXTRAKEY_ENABLE = yes       # Media keys (required for VIA)
NKRO_ENABLE = yes           # N-key rollover
RGBLIGHT_ENABLE = yes       # RGB underglow
ENCODER_ENABLE = yes        # Rotary encoders
ENCODER_MAP_ENABLE = yes    # Encoder keycode map
CONSOLE_ENABLE = no         # Debug console (disable to save space)
COMMAND_ENABLE = no         # Debug commands (disable to save space)
```

### Custom OLED Graphics

Edit `keyboards/ergodash/rev1/keymaps/default/oled.c` (or the variant tree):

- `render_logo()`: Replace the 128-byte `raw_logo[]` array with your own bitmap
- `print_status_narrow()`: Customize status text and layout
- Use online tools to convert images to QMK-compatible OLED arrays: https://joric.github.io/qle/

### Custom Keymaps

Create a new keymap directory:

```bash
cp -r keyboards/ergodash/rev1/keymaps/default keyboards/ergodash/rev1/keymaps/myname
```

Edit `keyboards/ergodash/rev1/keymaps/myname/keymap.c` and compile:

```bash
qmk compile -kb ergodash/rev1 -km myname
```

---

## Support and Resources

- **Repository**: https://github.com/juarendra/ERGODASH-MOD-ENCH-OLED-QMK_VIA
- **QMK Documentation**: https://docs.qmk.fm/
- **VIA Documentation**: https://docs.keeb.io/via
- **Firmware manifest**: [FIRMWARE/manifest.json](../FIRMWARE/manifest.json)
- **Legacy support**: [Legacy support](../docs/LEGACY-SUPPORT.md)

---

## Safety Notes

1. **Backup before flashing**: Keep a working `.hex` file before testing new builds
2. **Do not cross-flash**: Only use firmware confirmed for your hardware revision
3. **Bootloader protection**: Never flash a different bootloader without understanding the risks
4. **TRRS cable**: Always connect/disconnect TRRS cable with power off to avoid shorts

---

**Last updated**: 2026-10-08  
**Applies to**: Mapped Rev1.2 source trees; physical sold-unit compatibility not independently evidenced
