# Device Test (USB / VIA / Functional)

> **STALE — re-test required (2026-10-10).** The attestation below was made for
> the legacy USB identity `0x4D44:0x6061`. The shipped firmware was rebuilt to
> the project-owned pid.codes identity `0x1209:0x2013`, so the USB enumeration
> and VIA-detection checks no longer reflect the shipped `.hex`. The owner must
> re-flash the current binaries and re-run every check below, confirming the
> host enumerates `0x1209:0x2013`, before this record is valid again. See
> `docs/evidence/qmk-build.md` → "Path to `functionally rebuilt`".

**Status:** Owner-attested (2026-10-10) for the LEGACY `0x4D44:0x6061` build —
now superseded. The owner (Juarendra Ramadhani, Positron Electronic) confirmed
the ENCHDASH was flashed, enumerated, and functionally tested on physical
hardware, and the product was sold in working condition. This is an owner
attestation, not a capture reproduced within this repository; raw enumeration
logs and VIA screenshots are retained by the owner.

| Check | Result (owner-attested) |
|-------|-------------------------|
| Firmware flashed to physical ATmega32u4 | Confirmed |
| USB enumeration (host recognizes device) | Confirmed |
| All keys register (matrix scan) | Confirmed |
| Encoder rotation and press | Confirmed |
| OLED display (layer/caps on master, logo on slave) | Confirmed |
| RGB underglow | Confirmed |
| Split halves communicate over TRRS | Confirmed |
| VIA detects device with matching JSON | Confirmed |
| VIA remap persists across power cycle | Confirmed |

**USB identity note:** the shipped firmware now declares `0x1209:0x2013`,
allocated under the pid.codes open-source VID (org Positron-Electronic;
registration PR pidcodes/pidcodes.github.com#1303). The legacy `0x4D44:0x6061`
descriptor was inherited from upstream and is retired. Units flashed with the
earlier binaries still enumerate as the legacy ID until re-flashed.

**Attested by:** Juarendra Ramadhani (Positron Electronic), 2026-10-10.

**Note:** This record reflects the owner's attestation that the device was
tested and shipped working. Supporting captures (enumeration logs, VIA
screenshots) live with the owner and are not committed here.
