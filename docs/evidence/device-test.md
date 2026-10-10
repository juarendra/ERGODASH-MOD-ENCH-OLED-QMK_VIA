# Device Test (USB / VIA / Functional)

**Status:** Owner-attested (2026-10-10). The owner (Juarendra Ramadhani,
Positron Electronic) confirms the ENCHDASH has been flashed, enumerated, and
functionally tested on physical hardware, and the product has been sold in
working condition. This is an owner attestation, not a capture reproduced
within this repository; raw enumeration logs and VIA screenshots are retained
by the owner.

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

**USB identity note:** the shipped firmware enumerates as `0x4D44:0x6061`.
This value is inherited from upstream and is documented as a legacy descriptor
under audit (see `FIRMWARE/manifest.json` and `THIRD_PARTY_NOTICES.md`). A
future own-VID/PID release is tracked separately and requires a firmware
rebuild.

**Attested by:** Juarendra Ramadhani (Positron Electronic), 2026-10-10.

**Note:** This record reflects the owner's attestation that the device was
tested and shipped working. Supporting captures (enumeration logs, VIA
screenshots) live with the owner and are not committed here.
