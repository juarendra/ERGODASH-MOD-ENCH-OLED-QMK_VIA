# ENCHDASH QMK Build Evidence

**Status**: built-and-shipped from source. The three shipped binaries ARE the
output of this build — repo source compiled with QMK `0.26.11` + avr-gcc
`15.1.0`, carrying the new USB identity `0x1209:0x2013` (allocated under
pid.codes; registration PR pidcodes/pidcodes.github.com#1303). Each shipped
`.hex` sha256 equals its `rebuilt_sha256` in `FIRMWARE/manifest.json`. All three
compile cleanly to valid, flash-sized AVR images and the USB descriptor was
confirmed to contain `0x1209`/`0x2013` and no legacy `0x4D44`/`0x6061`.

**Not yet proven**: physical device function with the new identity. The prior
owner attestation in `device-test.md` covered the OLD `0x4D44:0x6061` binaries
and is now STALE — the USB identity changed, so the owner must re-flash and
re-run the smoke matrix. `provenance_status` stays `incomplete` until that
device re-test is recorded.

**Date rebuilt**: 2026-10-10
**Purpose**: Migrate the shipped firmware to the project-owned pid.codes USB
identity and record the exact build environment.

---

## Build environment (this rebuild)

| Item | Value |
|------|-------|
| QMK base commit | `3d4da6de29c8635c9cd232ce456d8fec8d31921b` |
| QMK tag | `0.26.11` |
| QMK CLI | `1.1.8` |
| Compiler | `avr-gcc (GCC) 15.1.0` |
| Make | `GNU Make 4.4.1` |
| Host | QMK MSYS (MINGW64) on Windows |
| Source commit (this repo) | `3e9668b528f0a995bde2ddca47f78af7bd187172` |

The QMK tag `0.26.11` was selected as a representative 2024-era release; it is
**not** proven to be the exact base of the shipped binaries (that information was
never recorded).

---

## Variants built

Each repo source tree was copied into the QMK `keyboards/` tree under a build
name and compiled with `-km default`.

| Variant | Source path | Build target | Flash size | Result |
|---------|-------------|--------------|-----------|--------|
| Base VIA | `FIRMWARE/QMK/ergodash` | `ench_base/rev1` | 28320 / 28672 B (98%) | OK |
| No-WPM + mouse keys | `FIRMWARE/QMK/ergodash_nowpm_mousekey/ergodash` | `ench_nowpm/rev1` | 28340 / 28672 B (98%) | OK |
| WPM, no mouse keys | `FIRMWARE/QMK/ergodash_wpm_nomousekey/ergodash` | `ench_wpm/rev1` | 28062 / 28672 B (97%) | OK |

All three link and produce a valid Intel-HEX load file within the
32 KB − bootloader budget.

### Build-tree compatibility shims (not applied to repo source)

The repo source predates several QMK renames. To compile under QMK `0.26.11`,
the following were adjusted **only in the throwaway build copies** under
`keyboards/ench_*` — the committed repo source in `FIRMWARE/QMK/` is untouched:

- `info.json` → `keyboard.json` (QMK data-driven keyboard marker).
- Non-empty `url` field (QMK lint rejects empty `url`).
- `OLED_DRIVER = SSD1306` → `ssd1306` (driver id lowercased upstream).
- Encoder pins moved from `ENCODERS_PAD_A/B` `#define`s into the data-driven
  `encoder`/`split.encoder` keys (QMK now defines these from JSON and errors on
  the duplicate `#define`).
- Added `WS2812_DI_PIN` alongside legacy `RGB_DI_PIN` (WS2812 driver rename).

These shims are what a modern QMK tree requires; they do not change keymap
behaviour, matrix, layers, or features.

---

## Hashes (shipped == this build)

The shipped `.hex` were overwritten with this build's output, so each shipped
sha256 now equals its `rebuilt_sha256`:

```
ergodash_rev1_via.hex                  13922cb81ccccc7ccf2c03f299f24d126f7d72859c8dd49ac93ba1ae1ee6c4f6
omkbd_ergodash_rev1_nowpmmousekey.hex  967925733b816a20effd5254c38162874a5aa296ca8abcd0e3e9d3c38f51e2b7
omkbd_ergodash_rev1_wpmnomousekey.hex  b3372e2f920233a6aac9cfb6e55d4d4cd97c53b1e0143aaaf6ee80bccf94f57c
```

USB descriptor check (Intel-HEX → raw via `avr-objcopy`, byte scan): each image
contains the little-endian `09 12` (VID `0x1209`) and `13 20` (PID `0x2013`)
and zero occurrences of the legacy `44 4d` / `61 60`.

The prior shipped binaries (legacy `0x4D44:0x6061`, hashes `cdc3d673…`,
`22665732…`, `4ee05ef6…`) are superseded; they remain recoverable from Git
history for rollback.

---

## Provenance conclusion

- **What is proven**: the repository source is complete and compiles to a valid,
  correctly-sized firmware image for all three variants with a documented
  toolchain. The shipped `.hex` are this build's output and carry the new USB
  identity `0x1209:0x2013` (descriptor byte-scan confirmed).
- **What is not proven**: physical device behaviour with the new identity. No
  board has been flashed and smoke-tested since the USB identity changed.
- **`provenance_status`** stays `incomplete` in `FIRMWARE/manifest.json`. It is
  NOT a hash-reproduction gap anymore (shipped == rebuilt by construction); it is
  a hardware-attestation gap. The status upgrades to `functionally rebuilt` once
  the owner flashes a board and confirms the smoke matrix.

### Provenance status upgrade rules

- `verified` **only** when the artifact is additionally confirmed against an
  independently-reproduced hash from a recorded toolchain.
- `functionally rebuilt` **only** when the shipped `.hex` is flashed to test
  hardware and matrix / encoder / OLED / RGB / split / VIA behaviour is confirmed
  working with the new `0x1209:0x2013` identity.
- Otherwise `incomplete`.

### Path to `functionally rebuilt` (owner device re-test — REQUIRED)

The USB identity changed, so the earlier `device-test.md` attestation (legacy
`0x4D44:0x6061`) is STALE. To clear it:

1. Flash each shipped `.hex` to a physical board.
2. Confirm the host enumerates `0x1209:0x2013`.
3. Load the matching VIA JSON; confirm every key, both encoder directions +
   presses, OLED, RGB, split link, and reset/bootloader path.
4. Record the result in `device-test.md` and set `functionally rebuilt`.
5. For all future ENCHDASH builds, record the QMK commit + toolchain at build
   time so provenance never regresses.

---

## Reproduction steps

```bash
# In a QMK MSYS (MINGW64) shell with avr-gcc + qmk CLI:
git clone https://github.com/qmk/qmk_firmware.git qmkbuild
cd qmkbuild
git checkout tags/0.26.11
git submodule update --init lib/lufa lib/printf

# Copy each repo variant into keyboards/ and apply the compat shims noted above,
# then:
qmk compile -kb ench_base/rev1  -km default
qmk compile -kb ench_nowpm/rev1 -km default
qmk compile -kb ench_wpm/rev1   -km default

# Compare:
sha256sum .build/ench_*_rev1_default.hex
```
