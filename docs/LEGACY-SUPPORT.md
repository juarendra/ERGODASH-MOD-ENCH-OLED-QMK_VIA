# ENCHDASH Legacy Support

Products previously sold as `ERGODASH-MOD-ENCH-OLED-QMK_VIA` remain supported. The ENCHDASH naming change does not indicate an electrical redesign; no electrical redesign is documented in this repository. The renaming does not require owners to reflash working units. Legacy downloads and matching VIA JSON remain available. Physical compatibility and historical build provenance must be confirmed before new flashing.

## Safety rules

- Keep a working legacy firmware and matching VIA JSON together.
- Do not cross-flash a firmware whose hardware revision is not confirmed.
- Do not replace USB VID/PID values merely to change the displayed name.
- Preserve the original binary before testing any new build.

## Artifact status

The authoritative machine-readable inventory is `FIRMWARE/manifest.json`. A `provenance_status` of `incomplete` means historical build evidence has not yet been reconstructed; it does not mean the shipped binary is known bad.

## Support identity

**Legacy name:** `ERGODASH-MOD-ENCH-OLED-QMK_VIA`  
**Current name:** `ENCHDASH`  
**Commercial identity:** `Positron Electronic`  
**Copyright in modifications:** Juarendra Ramadhani

## Legacy firmware artifacts

| Firmware | Hardware Rev | USB VID:PID | VIA JSON | SHA-256 | Provenance |
|----------|--------------|-------------|----------|---------|------------|
| `FIRMWARE/ergodash_rev1_via.hex` | Rev1.2 (repo source) | 0x1209:0x2013 | `ErgoDash_4key_mod_positron_elektronik.json` | `13922cb...1ee6c4f6` | incomplete |
| `FIRMWARE/omkbd_ergodash_rev1_nowpmmousekey.hex` | Rev1.2 (repo source) | 0x1209:0x2013 | `NEW_ErgoDash_4key_V3_mod_positron_elektronik.json` | `9679257...8f51e2b7` | incomplete |
| `FIRMWARE/omkbd_ergodash_rev1_wpmnomousekey.hex` | Rev1.2 (repo source) | 0x1209:0x2013 | `NEW_ErgoDash_4key_V3_mod_positron_elektronik.json` | `b3372e2...cf94f57c` | incomplete |

### Firmware variant features

- **ergodash_rev1_via.hex** — Base VIA firmware with encoder + OLED support
- **omkbd_ergodash_rev1_nowpmmousekey.hex** — No WPM tracking, mouse keys enabled
- **omkbd_ergodash_rev1_wpmnomousekey.hex** — WPM tracking enabled, no mouse keys

## VIA JSON compatibility

Two VIA definition files are referenced by the manifest:

1. **ErgoDash_4key_mod_positron_elektronik.json** — Used by `ergodash_rev1_via.hex`
2. **NEW_ErgoDash_4key_V3_mod_positron_elektronik.json** — Used by the two `omkbd_ergodash_rev1_*` variants

Both files define USB VID:PID as `0x1209:0x2013`, allocated under the pid.codes open-source VID (org Positron-Electronic; registration PR pidcodes/pidcodes.github.com#1303). The shipped `.hex` are rebuilt from source carrying this identity. Ensure the VIA application loads the correct JSON for your flashed firmware.

## Source mapping

| Firmware | Source Path |
|----------|-------------|
| `ergodash_rev1_via.hex` | `FIRMWARE/QMK/ergodash/` |
| `omkbd_ergodash_rev1_nowpmmousekey.hex` | `FIRMWARE/QMK/ergodash_nowpm_mousekey/ergodash/` |
| `omkbd_ergodash_rev1_wpmnomousekey.hex` | `FIRMWARE/QMK/ergodash_wpm_nomousekey/ergodash/` |

A fourth source variant exists (`FIRMWARE/QMK/ergodash_mod_v3/`) but no corresponding `.hex` is distributed.

## Support policy
Existing units remain supported indefinitely. Legacy firmware binaries, VIA JSON files, and source code will not be removed from the repository. Future ENCHDASH-branded releases will coexist with legacy artifacts to ensure backward compatibility. The legacy product name `ERGODASH-MOD-ENCH-OLED-QMK_VIA` remains searchable.
