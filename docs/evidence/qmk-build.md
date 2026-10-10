# ENCHDASH QMK Build Evidence

**Status**: source-reproducible, hash-divergent. The three shipped binaries were
rebuilt from the repository source with a current QMK toolchain. All three
compile cleanly to valid, flash-sized AVR images, but the rebuilt hashes differ
from the shipped hashes because the **original QMK base commit and toolchain
version used for the shipped `.hex` files were never recorded**. Physical device
function is owner-attested separately in `device-test.md`.

**Date rebuilt**: 2026-10-10
**Purpose**: Establish that the repository source compiles to working firmware
and record the exact build environment.

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

## Hash comparison

```
                                    shipped sha256                     rebuilt sha256
ergodash_rev1_via.hex               cdc3d673…396e2f0c                  f32d1c20…cb741e30
omkbd…nowpmmousekey.hex             22665732…71aa436d                  d3910cba…105f65283
omkbd…wpmnomousekey.hex             4ee05ef6…27fc6a04                  c587628a…4edcf375
```

Decoded-binary comparison (Intel-HEX → raw via `avr-objcopy`):

| Variant | Shipped bytes | Rebuilt bytes | Differing bytes |
|---------|---------------|---------------|-----------------|
| Base    | 28294 | 28320 | 26861 |
| No-WPM  | 28558 | 28340 | 24597 |
| WPM     | 28532 | 28062 | 24443 |

The large byte differences are consistent with a **different QMK revision and a
much newer avr-gcc** (code layout, inlining, and library objects all shift). This
is expected for AVR builds across compiler generations and does not by itself
indicate a source mismatch.

---

## Provenance conclusion

- **What is proven**: the repository source is complete and compiles to a valid,
  correctly-sized firmware image for all three variants with a documented
  toolchain. There is no missing or broken source.
- **What is not proven**: bit-for-bit (or byte-for-byte) reproduction of the
  shipped binaries. The original build's QMK commit and compiler version were
  never recorded, so an exact match cannot be reconstructed from the repository
  alone.
- **`provenance_status`** stays `incomplete` in `FIRMWARE/manifest.json`. Per the
  upgrade rules below, `verified` requires an exact hash match and
  `functionally rebuilt` requires flashing both the shipped and rebuilt binaries
  to hardware and confirming identical behaviour. Neither has been done here, so
  the status is not upgraded. The rebuilt hashes and the exact build environment
  are recorded in the manifest (`build_environment`, `rebuilt_sha256`,
  `qmk_base_commit`, `build_command`) for transparency.

### Provenance status upgrade rules

- `verified` **only** when the built artifact SHA-256 matches the corresponding
  manifest SHA-256 exactly.
- `functionally rebuilt` **only** when hashes differ **and** both versions are
  flashed to test hardware and matrix / encoder / OLED / RGB / split / VIA
  behaviour is confirmed identical.
- Otherwise `incomplete`.

### Path to a clean `verified`/`functionally rebuilt` (future work)

1. Identify the original QMK commit (bisect 2024 releases against a known-good
   shipped hash), **or**
2. Flash both the shipped and the rebuilt `.hex` to a physical board and run the
   smoke matrix in `docs/RELEASE-CHECKLIST.md`; if behaviour is identical, set
   `functionally rebuilt` and record the test.
3. For all future ENCHDASH builds, record the QMK commit + toolchain at build
   time so this gap never recurs.

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
