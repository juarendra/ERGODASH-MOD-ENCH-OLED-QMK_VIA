# ENCHDASH Legacy Support

Products previously sold as `ERGODASH-MOD-ENCH-OLED-QMK_VIA` remain supported. The ENCHDASH naming change does not indicate an electrical redesign and does not require owners to reflash working units.

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
| `FIRMWARE/ergodash_rev1_via.hex` | Rev1.2 (repo source) | 0x4D44:0x6061 | `ErgoDash_4key_mod_positron_elektronik.json` | `cdc3d67...96e2f0c` | incomplete |
| `FIRMWARE/omkbd_ergodash_rev1_nowpmmousekey.hex` | Rev1.2 (repo source) | 0x4D44:0x6061 | `NEW_ErgoDash_4key_V3_mod_positron_elektronik.json` | `2266573...1aa436d` | incomplete |
| `FIRMWARE/omkbd_ergodash_rev1_wpmnomousekey.hex` | Rev1.2 (repo source) | 0x4D44:0x6061 | `NEW_ErgoDash_4key_V3_mod_positron_elektronik.json` | `4ee05ef...7fc6a04` | incomplete |

### Firmware variant features

- **ergodash_rev1_via.hex** — Base VIA firmware with encoder + OLED support
- **omkbd_ergodash_rev1_nowpmmousekey.hex** — No WPM tracking, mouse keys enabled
- **omkbd_ergodash_rev1_wpmnomousekey.hex** — WPM tracking enabled, no mouse keys

## VIA JSON compatibility

Two VIA definition files exist in the repository:

1. **ErgoDash_4key_mod_positron_elektronik.json** — Used by `ergodash_rev1_via.hex`
2. **NEW_ErgoDash_4key_V3_mod_positron_elektronik.json** — Used by the two `omkbd_ergodash_rev1_*` variants

Both files define USB VID:PID as `0x4D44:0x6061`. Ensure the VIA application loads the correct JSON for your flashed firmware.

## Source mapping

| Firmware | Source Path |
|----------|-------------|
| `ergodash_rev1_via.hex` | `FIRMWARE/QMK/ergodash/` |
| `omkbd_ergodash_rev1_nowpmmousekey.hex` | `FIRMWARE/QMK/ergodash_nowpm_mousekey/ergodash/` |
| `omkbd_ergodash_rev1_wpmnomousekey.hex` | `FIRMWARE/QMK/ergodash_wpm_nomousekey/ergodash/` |

A fourth source variant exists (`FIRMWARE/QMK/ergodash_mod_v3/`) but no corresponding `.hex` is distributed.

## Support policy

Existing units remain supported indefinitely. Legacy firmware binaries, VIA JSON files, and source code will not be removed from the repository. Future ENCHDASH-branded releases will coexist with legacy artifacts to ensure backward compatibility.
