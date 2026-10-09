# ENCHDASH Compliance and Identity Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate the sold product to the ENCHDASH identity, satisfy hardware/firmware attribution duties, preserve legacy-unit support, and leave future releases reproducible and verifiable.

**Architecture:** Apply remediation in compatibility-first stages. First add licenses, attribution, legacy manifests, and automated integrity checks without moving working files; then add a separately build-tested ENCHDASH firmware/VIA target; owner applies KiCad metadata and silkscreen changes; repository rename and public communications remain gated actions requiring explicit authorization.

**Tech Stack:** Markdown, JSON, Python 3 standard library, Git, QMK CLI/toolchain, VIA definition JSON, KiCad/ERC/DRC/Gerber review performed by owner.

**Approved specification:** `docs/superpowers/specs/2026-10-08-enchdash-remediation-design.md`

**Execution constraints:** Work only in `D:/Pribadi/ERGODASH-MOD-ENCH-OLED-QMK_VIA`. Do not commit, push, rename the GitHub repository, publish a release, contact customers, edit marketplaces, or edit KiCad files without the separate approvals named below.

---

## File map

### Create

- `LICENSE` — scope index for mixed-license repository; does not relicense third-party work.
- `LICENSES/MIT-ErgoDash.txt` — unmodified upstream ErgoDash MIT text and omkbd notice.
- `LICENSES/GPL-2.0-or-later.txt` — full GPL firmware license text from QMK/FSF source.
- `THIRD_PARTY_NOTICES.md` — asset/library origin, license, modification, and use status.
- `CHANGELOG.md` — identity/compliance change history and rollback notes.
- `FIRMWARE/manifest.json` — machine-readable legacy binary/source/VIA provenance.
- `FIRMWARE/README.md` — customer-safe firmware selection, build, and flashing guidance.
- `docs/LEGACY-SUPPORT.md` — mapping from sold product name to supported artifacts.
- `docs/HARDWARE-ATTRIBUTION.md` — hardware origin, modifications, and license boundaries.
- `docs/RELEASE-CHECKLIST.md` — mandatory release gates.
- `docs/SILKSCREEN-GUIDE.md` — exact owner-applied KiCad metadata and marking rules.
- `tools/verify_repository.py` — standard-library integrity and identity validator.
- `tests/test_verify_repository.py` — behavioral checks for hash and USB/VIA mismatch detection.
- `FIRMWARE/QMK/enchdash/` — future ENCHDASH QMK target, created only after build baseline is known.
- `FIRMWARE/ENCHDASH.json` — future VIA definition paired with the ENCHDASH firmware target.
- `docs/evidence/qmk-build.md` — pinned QMK revision, commands, outputs, and artifact hashes.
- `docs/evidence/kicad-owner-verification.md` — owner evidence checklist; no fabricated pass state.

### Modify

- `README.md` — ENCHDASH primary identity, attribution, legacy support, compatibility, and corrected links.
- Future source copied into `FIRMWARE/QMK/enchdash/` — ENCHDASH metadata and retained upstream notices.
- No existing legacy source, `.hex`, VIA JSON, manual, PDF, image, or KiCad file changes during Tasks 1–6.

---

### Task 1: Freeze and inventory the sold legacy artifacts

**Files:**
- Create: `FIRMWARE/manifest.json`
- Create: `docs/LEGACY-SUPPORT.md`
- Inspect: `FIRMWARE/*.hex`
- Inspect: `FIRMWARE/*.json`
- Inspect: `FIRMWARE/QMK/**`
- Inspect: `NEW_ErgoDash_4key_V3_mod_positron_elektronik.json`
- Inspect: `ErgoDash_4key_mod_positron_elektronik.json`

- [ ] **Step 1: Verify the execution root and clean baseline**

Run:

```bash
git rev-parse --show-toplevel
git status --short --branch
git rev-parse HEAD
```

Expected:

```text
D:/Pribadi/ERGODASH-MOD-ENCH-OLED-QMK_VIA
## main...origin/main
744c49cfca07d7403443afcf7c8720f0fba70752
```

If status contains user changes, preserve them and adjust touched paths; do not reset or clean.

- [ ] **Step 2: Recompute the three shipped binary hashes**

Run:

```bash
sha256sum FIRMWARE/*.hex
```

Expected hashes:

```text
cdc3d67382e8ffd0240a79fe39064930dce1abeb77b785657436fe11396e2f0c  FIRMWARE/ergodash_rev1_via.hex
22665732e1977332298f524e00f63c9e683aa2db3e8f1a2571d20f6d71aa436d  FIRMWARE/omkbd_ergodash_rev1_nowpmmousekey.hex
4ee05ef6ac855e19fcd5f552cb140e9924d83e6fc92767f69c2c633827fc6a04  FIRMWARE/omkbd_ergodash_rev1_wpmnomousekey.hex
```

Any mismatch stops execution: repository artifact changed after this plan was written.

- [ ] **Step 3: Create the initial immutable legacy manifest**

Create `FIRMWARE/manifest.json` with exactly this initial evidence. `null` means evidence is unavailable; it must not be guessed.

```json
{
  "schema_version": 1,
  "legacy_product_name": "ERGODASH-MOD-ENCH-OLED-QMK_VIA",
  "current_product_name": "ENCHDASH",
  "usb_identity": {
    "vid": "0x4D44",
    "pid": "0x6061",
    "status": "legacy-preserved; provenance audit required before reuse in a new allocation"
  },
  "artifacts": [
    {
      "path": "FIRMWARE/ergodash_rev1_via.hex",
      "sha256": "cdc3d67382e8ffd0240a79fe39064930dce1abeb77b785657436fe11396e2f0c",
      "hardware_revision": "Rev1.2 repository source; physical sold-unit marking not yet evidenced",
      "source_path": "FIRMWARE/QMK/ergodash",
      "via_json": "ErgoDash_4key_mod_positron_elektronik.json",
      "qmk_base_commit": null,
      "source_commit": null,
      "build_command": null,
      "provenance_status": "incomplete"
    },
    {
      "path": "FIRMWARE/omkbd_ergodash_rev1_nowpmmousekey.hex",
      "sha256": "22665732e1977332298f524e00f63c9e683aa2db3e8f1a2571d20f6d71aa436d",
      "hardware_revision": "Rev1.2 repository source; physical sold-unit marking not yet evidenced",
      "source_path": "FIRMWARE/QMK/ergodash_nowpm_mousekey/ergodash",
      "via_json": "NEW_ErgoDash_4key_V3_mod_positron_elektronik.json",
      "qmk_base_commit": null,
      "source_commit": null,
      "build_command": null,
      "provenance_status": "incomplete"
    },
    {
      "path": "FIRMWARE/omkbd_ergodash_rev1_wpmnomousekey.hex",
      "sha256": "4ee05ef6ac855e19fcd5f552cb140e9924d83e6fc92767f69c2c633827fc6a04",
      "hardware_revision": "Rev1.2 repository source; physical sold-unit marking not yet evidenced",
      "source_path": "FIRMWARE/QMK/ergodash_wpm_nomousekey/ergodash",
      "via_json": "NEW_ErgoDash_4key_V3_mod_positron_elektronik.json",
      "qmk_base_commit": null,
      "source_commit": null,
      "build_command": null,
      "provenance_status": "incomplete"
    }
  ]
}
```

Do not change `provenance_status` until source-to-binary evidence exists.

- [ ] **Step 4: Create legacy support guidance**

Create `docs/LEGACY-SUPPORT.md` with these mandatory sections and statements:

```markdown
# ENCHDASH Legacy Support

Products previously sold as `ERGODASH-MOD-ENCH-OLED-QMK_VIA` remain
supported. The ENCHDASH naming change does not indicate an electrical
redesign and does not require owners to reflash working units.

## Safety rules

- Keep a working legacy firmware and matching VIA JSON together.
- Do not cross-flash a firmware whose hardware revision is not confirmed.
- Do not replace USB VID/PID values merely to change the displayed name.
- Preserve the original binary before testing any new build.

## Artifact status

The authoritative machine-readable inventory is `FIRMWARE/manifest.json`.
A `provenance_status` of `incomplete` means historical build evidence has
not yet been reconstructed; it does not mean the shipped binary is known
bad.

## Support identity

Legacy name: `ERGODASH-MOD-ENCH-OLED-QMK_VIA`
Current name: `ENCHDASH`
Commercial identity: `Positron Electronic`
Copyright in modifications: Juarendra Ramadhani
```

Add a table generated from all three manifest rows; do not claim an exact physical revision beyond available evidence.

- [ ] **Step 5: Validate JSON syntax and hashes**

Run:

```bash
python -m json.tool FIRMWARE/manifest.json > NUL
python -c "import hashlib,json,pathlib; d=json.load(open('FIRMWARE/manifest.json')); bad=[x['path'] for x in d['artifacts'] if hashlib.sha256(pathlib.Path(x['path']).read_bytes()).hexdigest()!=x['sha256']]; assert not bad, 'hash mismatch: '+', '.join(bad); print('OK: all manifest hashes match')"
```

Expected: JSON exits 0; all three artifacts report `OK`.

---

### Task 2: Add explicit license scope and third-party notices

**Files:**
- Create: `LICENSE`
- Create: `LICENSES/MIT-ErgoDash.txt`
- Create: `LICENSES/GPL-2.0-or-later.txt`
- Create: `THIRD_PARTY_NOTICES.md`
- Inspect: `Hardware/PCB/Rev1.2/keebs.pretty-master/LICENSE.md`
- Inspect: `Hardware/PCB/Rev1.2/ProMicro.pretty-master/LICENSE`
- Inspect: all copied footprint, 3D model, image, PDF, video, and firmware directories

- [ ] **Step 1: Add the unmodified ErgoDash MIT license**

Fetch the authoritative upstream file, then save it without edits:

```bash
python -c "import urllib.request; open('LICENSES/MIT-ErgoDash.txt','wb').write(urllib.request.urlopen('https://raw.githubusercontent.com/omkbd/ErgoDash/master/LICENSE').read())"
```

Verify:

```bash
python -c "p=open('LICENSES/MIT-ErgoDash.txt',encoding='utf-8').read(); assert 'Copyright (c) 2018 omkbd' in p; assert 'MIT License' in p"
```

Expected: exit 0.

- [ ] **Step 2: Add the full GPL-2.0-or-later-compatible license text**

Copy the authoritative `LICENSE` file from the exact QMK upstream revision selected during Task 6 into `LICENSES/GPL-2.0-or-later.txt`. Until Task 6 pins that revision, use QMK `master` only to prepare the file, then compare it with the pinned revision before completion:

```bash
python -c "import urllib.request; open('LICENSES/GPL-2.0-or-later.txt','wb').write(urllib.request.urlopen('https://raw.githubusercontent.com/qmk/qmk_firmware/master/LICENSE').read())"
```

Verify the file contains `GNU GENERAL PUBLIC LICENSE` and `Version 2, June 1991`.

- [ ] **Step 3: Create a non-ambiguous root license index**

Create `LICENSE`:

```text
ENCHDASH repository license index

This repository contains works under multiple licenses. This file does not
replace or override notices embedded in individual files.

1. ErgoDash-derived hardware design
   Original work Copyright (c) 2018 omkbd.
   ENCHDASH modifications Copyright (c) 2024-2026 Juarendra Ramadhani.
   Licensed under the MIT License; see LICENSES/MIT-ErgoDash.txt.

2. QMK-derived firmware
   Licensed under GNU GPL version 2 or, where the source file states it,
   any later version. Existing file-level notices remain controlling.
   See LICENSES/GPL-2.0-or-later.txt.

3. Third-party libraries, footprints, 3D models, images, documents, and media
   Remain under their respective licenses. See THIRD_PARTY_NOTICES.md and
   license files stored beside those assets.

4. Owner-created documentation and media
   Copyright (c) 2024-2026 Juarendra Ramadhani unless another notice is
   present. No trademark or endorsement rights are granted by this index.

The product is an independent derivative of ErgoDash. It is not an official
ErgoDash revision and is not maintained, approved, or endorsed by omkbd.
```

- [ ] **Step 4: Build the third-party inventory from evidence**

Create `THIRD_PARTY_NOTICES.md` with a table containing:

```text
Component | Repository path | Upstream URL | License | Modified? | Used by active design? | Evidence/status
```

Mandatory initial rows:

- ErgoDash hardware, `Hardware/PCB/Rev1.2/ergodash.*`, omkbd URL, MIT, modified, active.
- QMK/ErgoDash firmware, `FIRMWARE/QMK/**`, QMK and omkbd URLs, GPL file notices, modified, active/variant-specific.
- `keebs.pretty-master`, existing CERN OHL v1.2 file, usage status determined from KiCad footprint references.
- `ProMicro.pretty-master`, license read from its local `LICENSE`, usage status determined from KiCad references.
- `Keebio-Parts.pretty`, `SofleKeyboard-footprint.pretty`, 3D model directories, photos, PDFs, DOCX, and MOV files, each with evidence or the explicit status `provenance not yet established`.

Do not write `MIT` for unknown assets. Unknown provenance remains visible and blocks a blanket clean-compliance claim for that asset.

- [ ] **Step 5: Verify notices are retained**

Run bounded searches for `Copyright`, `License`, `CERN`, `GPL`, and upstream URLs across active source and copied-library roots. Compare every hit with `THIRD_PARTY_NOTICES.md`. Expected: each identified origin has a row; no existing local license file was deleted or edited.

---

### Task 3: Replace public identity and document hardware attribution

**Files:**
- Modify: `README.md`
- Create: `docs/HARDWARE-ATTRIBUTION.md`
- Create: `FIRMWARE/README.md`

- [ ] **Step 1: Rewrite the README header and identity block**

The first section must be exactly:

```markdown
# ENCHDASH

ENCHDASH is an independent keyboard design derived from [ErgoDash by
omkbd](https://github.com/omkbd/ErgoDash). It is not an official ErgoDash
revision and is not maintained, approved, or endorsed by omkbd.

Original ErgoDash hardware: Copyright (c) 2018 omkbd, licensed under the
MIT License. ENCHDASH modifications: Copyright (c) 2024–2026 Juarendra
Ramadhani. Commercial identity: Positron Electronic.

This product was previously sold as `ERGODASH-MOD-ENCH-OLED-QMK_VIA`.
Existing units remain supported under that legacy name; see
[Legacy Support](docs/LEGACY-SUPPORT.md).
```

- [ ] **Step 2: Preserve verified product instructions while fixing naming and links**

Retain confirmed features and user instructions, but:

- change active product references from `ErgoDash-Mod` to `ENCHDASH`;
- use `ErgoDash-derived` only in origin/compatibility context;
- correct the malformed `hhttps://` firmware link to a relative `FIRMWARE/` link;
- replace absolute links to this repository with relative paths where possible;
- link `LICENSE`, `THIRD_PARTY_NOTICES.md`, `FIRMWARE/README.md`, `docs/HARDWARE-ATTRIBUTION.md`, and `docs/RELEASE-CHECKLIST.md`;
- state that current legacy VIA instructions require the JSON named in `FIRMWARE/manifest.json`;
- remove empty headings or mark unavailable material factually, never with a promise.

- [ ] **Step 3: Document hardware attribution and modifications**

Create `docs/HARDWARE-ATTRIBUTION.md` with:

```markdown
# ENCHDASH Hardware Attribution

## Origin

ENCHDASH is derived from ErgoDash by omkbd:
https://github.com/omkbd/ErgoDash

Original work Copyright (c) 2018 omkbd and licensed under MIT.
Modifications Copyright (c) 2024–2026 Juarendra Ramadhani.

## Relationship

ENCHDASH is independent. It is not an official ErgoDash revision and is not
maintained, approved, or endorsed by omkbd.

## Confirmed modifications

- Rotary encoder support.
- OLED support.
- Kailh MX hotswap socket support.
- Positron Electronic firmware/VIA variants and product documentation.

## Compatibility boundary

The repository does not claim full compatibility with original ErgoDash
cases, plates, PCB revisions, pin assignments, or firmware. Compatibility
must be verified against the exact ENCHDASH hardware revision.

## License

See `../LICENSE`, `../LICENSES/MIT-ErgoDash.txt`, and
`../THIRD_PARTY_NOTICES.md`.
```

Only add further modifications after checking schematic/PCB evidence.

- [ ] **Step 4: Create firmware selection guidance**

Create `FIRMWARE/README.md` from the manifest. It must explain:

- exact three binary names and SHA-256 values;
- their source-directory and VIA JSON mapping;
- `provenance incomplete` meaning;
- backup-before-flash rule;
- no cross-flashing without hardware confirmation;
- current legacy USB identity `0x4D44:0x6061` without claiming ownership;
- future ENCHDASH firmware location after Task 6 passes;
- GPL source/build obligation and license link.

- [ ] **Step 5: Check active wording and links**

Run:

```bash
python -c "from pathlib import Path; p=Path('README.md').read_text(encoding='utf-8'); assert p.startswith('# ENCHDASH\n'); assert 'hhttps://' not in p; assert 'not maintained, approved, or endorsed by omkbd' in p"
```

Expected: exit 0. Manually open every relative README link and confirm target exists.

---

### Task 4: Add machine-verifiable repository integrity

**Files:**
- Create: `tools/verify_repository.py`
- Create: `tests/test_verify_repository.py`

- [ ] **Step 1: Write failing behavioral tests**

Create `tests/test_verify_repository.py`:

```python
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.verify_repository import normalize_usb, validate_manifest


class VerifyRepositoryTest(unittest.TestCase):
    def test_normalize_usb_accepts_hex_case(self) -> None:
        self.assertEqual(normalize_usb("0X4d44"), "0x4D44")

    def test_manifest_rejects_changed_binary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifact = root / "firmware.hex"
            artifact.write_bytes(b"changed")
            manifest = {
                "usb_identity": {"vid": "0x4D44", "pid": "0x6061"},
                "artifacts": [{
                    "path": "firmware.hex",
                    "sha256": hashlib.sha256(b"original").hexdigest(),
                    "via_json": "via.json",
                    "source_path": "source",
                    "provenance_status": "incomplete"
                }]
            }
            (root / "via.json").write_text(json.dumps({
                "vendorId": "0x4D44", "productId": "0x6061"
            }), encoding="utf-8")
            (root / "source").mkdir()
            errors = validate_manifest(root, manifest)
            self.assertTrue(any("SHA-256 mismatch" in error for error in errors))

    def test_manifest_rejects_via_usb_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifact = root / "firmware.hex"
            artifact.write_bytes(b"firmware")
            manifest = {
                "usb_identity": {"vid": "0x4D44", "pid": "0x6061"},
                "artifacts": [{
                    "path": "firmware.hex",
                    "sha256": hashlib.sha256(b"firmware").hexdigest(),
                    "via_json": "via.json",
                    "source_path": "source",
                    "provenance_status": "incomplete"
                }]
            }
            (root / "via.json").write_text(json.dumps({
                "vendorId": "0x4D44", "productId": "0xFFFF"
            }), encoding="utf-8")
            (root / "source").mkdir()
            errors = validate_manifest(root, manifest)
            self.assertTrue(any("USB identity mismatch" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests and confirm failure**

Run:

```bash
python -m unittest tests.test_verify_repository -v
```

Expected: import failure because `tools.verify_repository` does not exist.

- [ ] **Step 3: Implement the minimal validator**

Create `tools/verify_repository.py`:

```python
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_PATHS = (
    "LICENSE",
    "LICENSES/MIT-ErgoDash.txt",
    "LICENSES/GPL-2.0-or-later.txt",
    "THIRD_PARTY_NOTICES.md",
    "FIRMWARE/manifest.json",
    "FIRMWARE/README.md",
    "docs/LEGACY-SUPPORT.md",
    "docs/HARDWARE-ATTRIBUTION.md",
    "docs/RELEASE-CHECKLIST.md",
    "docs/SILKSCREEN-GUIDE.md",
)


def normalize_usb(value: str) -> str:
    return f"0x{int(value, 16):04X}"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def validate_manifest(root: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    usb = manifest.get("usb_identity", {})
    expected_vid = normalize_usb(str(usb.get("vid", "0")))
    expected_pid = normalize_usb(str(usb.get("pid", "0")))
    for item in manifest.get("artifacts", []):
        artifact = root / item["path"]
        source = root / item["source_path"]
        via_path = root / item["via_json"]
        if not artifact.is_file():
            errors.append(f"missing artifact: {item['path']}")
        elif sha256_file(artifact) != item["sha256"]:
            errors.append(f"SHA-256 mismatch: {item['path']}")
        if not source.is_dir():
            errors.append(f"missing source directory: {item['source_path']}")
        if not via_path.is_file():
            errors.append(f"missing VIA JSON: {item['via_json']}")
            continue
        via = load_json(via_path)
        actual = (
            normalize_usb(str(via.get("vendorId", "0"))),
            normalize_usb(str(via.get("productId", "0"))),
        )
        if actual != (expected_vid, expected_pid):
            errors.append(
                f"USB identity mismatch: {item['via_json']} has "
                f"{actual[0]}:{actual[1]}, expected {expected_vid}:{expected_pid}"
            )
    return errors


def validate_repository(root: Path) -> list[str]:
    errors = [f"missing required path: {path}" for path in REQUIRED_PATHS if not (root / path).exists()]
    readme = (root / "README.md").read_text(encoding="utf-8")
    if not readme.startswith("# ENCHDASH\n"):
        errors.append("README must start with '# ENCHDASH'")
    if "hhttps://" in readme:
        errors.append("README contains malformed hhttps URL")
    license_text = (root / "LICENSES/MIT-ErgoDash.txt").read_text(encoding="utf-8")
    if "Copyright (c) 2018 omkbd" not in license_text:
        errors.append("ErgoDash copyright notice missing")
    manifest = load_json(root / "FIRMWARE/manifest.json")
    errors.extend(validate_manifest(root, manifest))
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate_repository(root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: ENCHDASH repository integrity checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests and repository check**

Run:

```bash
python -m unittest tests.test_verify_repository -v
python tools/verify_repository.py
```

Expected: three tests pass; repository validator prints `PASS: ENCHDASH repository integrity checks` after Tasks 1–5 create all required paths.

---

### Task 5: Write owner silkscreen guide and release gates

**Files:**
- Create: `docs/SILKSCREEN-GUIDE.md`
- Create: `docs/RELEASE-CHECKLIST.md`
- Create: `docs/evidence/kicad-owner-verification.md`
- Do not modify: `Hardware/PCB/Rev1.2/ergodash.kicad_pcb`
- Do not modify: `Hardware/PCB/Rev1.2/ergodash.kicad_sch`

- [ ] **Step 1: Write the exact silkscreen guide**

`docs/SILKSCREEN-GUIDE.md` must distinguish project policy from universal legal claims and contain:

```text
Preferred:
ENCHDASH R1.2
ErgoDash-derived · Original © 2018 omkbd · MIT
MOD © 2024–2026 Juarendra Ramadhani
Positron Electronic
github.com/juarendra/ENCHDASH-QMK-VIA

Compact:
ENCHDASH R1.2
ErgoDash-derived · © omkbd 2018 · MIT
© J. Ramadhani 2024–2026
github.com/juarendra/ENCHDASH-QMK-VIA
```

State that `R1.2` and final URL are used only when they match released manufacturing files. If compact text is illegible, retain ENCHDASH, actual revision, and stable source URL/QR on board; place full attribution in accompanying source/documentation.

- [ ] **Step 2: Record prohibited markings**

Include this exact prohibited list:

```text
Official ErgoDash
ErgoDash Rev2
ErgoDash by omkbd & Positron
Approved by omkbd
Endorsed by omkbd
Company: omkbd
```

Also prohibit omkbd/QMK/VIA logos without separate permission, unearned certification marks, unverified VID/PID, dead/private URLs, and revision strings that differ from manufacturing files.

- [ ] **Step 3: Give the owner exact KiCad metadata values**

Document:

```text
Title: ENCHDASH
Revision: actual manufacturing revision
Company: Positron Electronic
Comment: Independent derivative of ErgoDash by omkbd
Original work: Copyright (c) 2018 omkbd
Modifications: Copyright (c) 2024–2026 Juarendra Ramadhani
License: MIT
Source: final public ENCHDASH repository URL
```

Do not edit KiCad during implementation.

- [ ] **Step 4: Create release checklist**

`docs/RELEASE-CHECKLIST.md` must gate:

- license/notice presence;
- manifest/hash verification;
- firmware source and QMK revision recording;
- firmware build and artifact hash;
- USB enumeration and VIA pairing;
- owner ERC and DRC results;
- front/back Gerber screenshots;
- silkscreen readability and overlap checks;
- first-article PCB photo;
- compatibility table update;
- repository-link verification;
- rollback artifacts;
- explicit approval before public rename/release/customer communication.

- [ ] **Step 5: Create unclaimed owner-evidence checklist**

Create `docs/evidence/kicad-owner-verification.md` with unchecked boxes only:

```markdown
# KiCad Owner Verification

- [ ] KiCad title-block screenshot attached or linked.
- [ ] Front Gerber screenshot attached or linked.
- [ ] Back Gerber screenshot attached or linked.
- [ ] ERC result recorded.
- [ ] DRC result recorded.
- [ ] No silkscreen overlaps pads, exposed copper, mask openings, cuts, holes, or keepouts.
- [ ] Text remains visible after assembly.
- [ ] First-article production photo attached or linked.
```

No item becomes checked without owner-provided evidence.

---

### Task 6: Establish a build-tested ENCHDASH firmware and VIA target

**Files:**
- Create: `FIRMWARE/QMK/enchdash/**`
- Create: `FIRMWARE/ENCHDASH.json`
- Create: `docs/evidence/qmk-build.md`
- Modify: `FIRMWARE/manifest.json` only to add the new built artifact after proof
- Preserve unchanged: all current legacy directories and `.hex` files

- [ ] **Step 1: Install or select an isolated QMK checkout**

Use an external QMK checkout; do not vendor the entire QMK repository here. Run:

```bash
qmk setup -y
qmk doctor
qmk config user.qmk_home
```

Record the absolute QMK home and exact output of:

```bash
git -C <reported-qmk-home> rev-parse HEAD
git -C <reported-qmk-home> describe --tags --always
```

`<reported-qmk-home>` means the path printed by `qmk config user.qmk_home`; use that exact path during execution. Save the resolved SHA and tag in `docs/evidence/qmk-build.md`. Do not claim it is the historical base of legacy binaries.

- [ ] **Step 2: Attempt legacy builds without editing legacy source**

Copy each legacy keyboard directory into the external QMK checkout under a temporary keyboard namespace and run the appropriate default-keymap build. Record every command and result. A failure is evidence of historical incompatibility, not permission to rewrite shipped behavior silently.

Build targets:

```text
FIRMWARE/QMK/ergodash
FIRMWARE/QMK/ergodash_mod_v3
FIRMWARE/QMK/ergodash_nowpm_mousekey/ergodash
FIRMWARE/QMK/ergodash_wpm_nomousekey/ergodash
```

If target naming differs after copying, record the exact namespace. Do not mark old binaries reproducible unless source commit, QMK base, command, and output relationship are proven.

- [ ] **Step 3: Create future target from the confirmed active variant**

Use `FIRMWARE/QMK/ergodash_mod_v3` as the starting source only after confirming it matches the currently documented OLED/encoder/VIA feature set. Copy into `FIRMWARE/QMK/enchdash/`; do not move or delete the source directory.

Change only identity and maintained-path metadata initially:

```json
{
  "keyboard_name": "ENCHDASH",
  "manufacturer": "Positron Electronic",
  "maintainer": "juarendra",
  "url": "https://github.com/juarendra/ENCHDASH-QMK-VIA"
}
```

Preserve legacy `0x4D44:0x6061` for this compatibility build and label its provenance unresolved. Do not adopt another vendor's USB allocation.

Retain upstream GPL headers. Add `Copyright 2024–2026 Juarendra Ramadhani` only in copied files actually changed.

- [ ] **Step 4: Create matching VIA definition**

Copy the verified current matching JSON to `FIRMWARE/ENCHDASH.json`. Change product display name to `ENCHDASH`; preserve matrix, layout, encoder mapping, VID, and PID. Verify:

```bash
python -m json.tool FIRMWARE/ENCHDASH.json > NUL
python -c "import json; d=json.load(open('FIRMWARE/ENCHDASH.json')); assert d['name']=='ENCHDASH'; assert d['vendorId'].upper()=='0X4D44'; assert d['productId'].upper()=='0X6061'"
```

Expected: both commands exit 0.

- [ ] **Step 5: Build ENCHDASH and capture evidence**

Copy/symlink the ENCHDASH target into the external QMK checkout, then run:

```bash
qmk compile -kb positron/enchdash/rev1 -km default
```

If the copied target has no revision directory in the final QMK structure, the accepted command is:

```bash
qmk compile -kb positron/enchdash -km default
```

Choose the command matching the actual directory, document it, and require exit 0. Record compiler/tool versions, QMK SHA, command, firmware size, output path, and SHA-256 in `docs/evidence/qmk-build.md`.

- [ ] **Step 6: Perform hardware/VIA smoke testing**

On one sacrificial or recoverable unit matching the hardware revision:

1. Back up/retain the legacy `.hex`.
2. Flash the ENCHDASH build.
3. Confirm host enumerates `0x4D44:0x6061`.
4. Load `FIRMWARE/ENCHDASH.json` in VIA.
5. Confirm every key, both encoder directions/presses, OLED, RGB, split link, and reset/bootloader path.
6. Restore legacy firmware if any check fails.

Record results in `docs/evidence/qmk-build.md`. This step cannot be marked done from compilation alone.

- [ ] **Step 7: Add the proven ENCHDASH artifact to manifest**

Only after Steps 5–6 pass, copy the built `.hex` into `FIRMWARE/` using a versioned name, compute SHA-256, and add a manifest row with non-null QMK base commit, source commit/worktree state, build command, and `provenance_status: "verified"`.

Do not overwrite any existing `.hex`.

---

### Task 7: Apply owner KiCad changes and verify manufacturing outputs

**Files:**
- Owner modifies: `Hardware/PCB/Rev1.2/ergodash.kicad_pcb`
- Owner may modify: matching KiCad project/title metadata files
- Owner updates: `docs/evidence/kicad-owner-verification.md`
- Agent reviews: exported ERC/DRC/Gerber evidence

- [ ] **Step 1: Owner applies approved metadata and silkscreen**

Owner follows `docs/SILKSCREEN-GUIDE.md`. Agent does not automate or text-edit KiCad source.

- [ ] **Step 2: Owner runs ERC and DRC**

Use the KiCad version that opens the project without destructive conversion. Record tool version, error count, warning count, and accepted exceptions. Zero errors is required; warnings require written disposition.

- [ ] **Step 3: Owner exports and visually reviews Gerbers**

Review both PCB sides at production scale. Confirm no text intersects pads, mask openings, board cuts, mounting holes, component bodies, or assembly-hidden regions.

- [ ] **Step 4: Agent cross-checks textual identity**

Verify rendered evidence says ENCHDASH, uses actual revision, contains factual ErgoDash attribution, names Juarendra Ramadhani/Positron Electronic correctly, and contains no prohibited wording or unapproved logos.

- [ ] **Step 5: Verify first article**

Owner supplies a photo from the next manufactured batch. Check readability and correspondence to released Gerbers before declaring hardware migration complete.

---

### Task 8: Prepare public migration, changelog, and rollback

**Files:**
- Create/Modify: `CHANGELOG.md`
- Modify: documentation links only after final repository URL exists
- Do not execute public actions without separate authorization

- [ ] **Step 1: Add changelog entry**

Create the top entry:

```markdown
## 2026-10-08 — ENCHDASH identity and compliance remediation

### Context
The product was previously sold as ERGODASH-MOD-ENCH-OLED-QMK_VIA.
Repository attribution, mixed-license scope, and binary provenance were not
explicit enough for an independently maintained commercial derivative.

### Changed
- Made ENCHDASH the primary product identity while preserving the legacy name.
- Added ErgoDash/omkbd attribution and MIT license text.
- Added QMK/GPL and third-party license documentation.
- Added legacy firmware hashes, provenance status, and compatibility guidance.
- Added owner-applied KiCad silkscreen and release verification gates.

### Impact
Existing units and legacy downloads remain supported. No electrical redesign
or automatic reflashing is implied by the naming change.

### Rollback
Restore prior public naming and download pointers if migration links fail, but
retain attribution, license, and provenance documents. Never delete Git history
or legacy artifacts as rollback.
```

Append exact paths changed after implementation.

- [ ] **Step 2: Prepare repository rename checklist**

Target name: `ENCHDASH-QMK-VIA`.

Before rename, verify:

- no broken relative links;
- all planned absolute links use the final target URL;
- old name remains in legacy support/search text;
- current default branch and commit are recorded;
- existing release/download URLs are inventoried;
- rollback to old repository name is documented.

- [ ] **Step 3: Obtain explicit owner authorization for GitHub rename**

Stop and ask. Do not infer authorization from approval of this plan.

After approval only, rename through GitHub and verify both:

```text
https://github.com/juarendra/ENCHDASH-QMK-VIA
https://github.com/juarendra/ERGODASH-MOD-ENCH-OLED-QMK_VIA
```

Expected: new URL resolves directly; old URL redirects to the new repository.

- [ ] **Step 4: Prepare customer/marketplace notice**

Use:

```text
Produk yang sebelumnya dijual sebagai ERGODASH-MOD-ENCH-OLED-QMK_VIA
sekarang menggunakan nama ENCHDASH.

Produk tetap sama dan tetap didukung. Dokumentasi diperbarui untuk
memperjelas bahwa desain ini merupakan turunan independen dari ErgoDash
by omkbd dan menggunakan firmware berbasis QMK.

Dokumentasi, source hardware, source firmware, dan pemberitahuan lisensi:
https://github.com/juarendra/ENCHDASH-QMK-VIA
```

Do not send or publish without explicit approval.

---

### Task 9: Run final repository and product gates

**Files:**
- Verify all changed files
- Update: `FIRMWARE/manifest.json`, `docs/evidence/qmk-build.md`, and `docs/evidence/kicad-owner-verification.md` only with observed evidence

- [ ] **Step 1: Run automated repository tests**

Run:

```bash
python -m unittest discover -s tests -v
python tools/verify_repository.py
python -m json.tool FIRMWARE/manifest.json > NUL
python -m json.tool FIRMWARE/ENCHDASH.json > NUL
sha256sum FIRMWARE/*.hex
```

Expected: tests pass; validator prints PASS; JSON commands exit 0; hashes match manifest rows.

- [ ] **Step 2: Run wording and secret scan**

Search tracked text for secrets, private URLs, unsupported endorsement claims, `hhttps://`, and misleading primary-name remnants. Historical/prohibited examples inside the approved spec, plan, changelog context, and silkscreen guide are allowed only when clearly quoted as such.

Expected: no active product statement says official/approved/endorsed by omkbd; no credential/token/private URL exists.

- [ ] **Step 3: Run link validation**

Validate every Markdown link in README, license index, notices, firmware guide, and docs. Expected: local targets exist; public URLs return successful responses or documented redirects.

- [ ] **Step 4: Confirm firmware and VIA hardware evidence**

Require:

- QMK compile exit 0;
- built artifact SHA-256 recorded;
- USB enumeration recorded;
- VIA detection recorded;
- key/encoder/OLED/RGB/split/reset smoke results recorded;
- rollback firmware retained.

Compilation without device testing is not sufficient.

- [ ] **Step 5: Confirm owner KiCad evidence**

Require completed ERC, DRC, Gerber, overlap/readability, and first-article evidence. If first article has not been manufactured, report documentation/firmware remediation complete but hardware-marking rollout pending; do not claim full migration complete.

- [ ] **Step 6: Review working tree without committing**

Run:

```bash
git status --short
git diff -- README.md LICENSE THIRD_PARTY_NOTICES.md CHANGELOG.md FIRMWARE/manifest.json FIRMWARE/README.md docs tools tests
git diff --check
```

Expected: only planned paths changed; `git diff --check` exits 0. Do not `git add`, commit, or push until owner explicitly authorizes it.

---

## Acceptance summary

Implementation passes only when:

1. ENCHDASH is primary identity; legacy name remains searchable and supported.
2. omkbd attribution and full MIT terms are preserved.
3. QMK/GPL and third-party licenses are mapped without false relicensing.
4. All shipped `.hex` files retain their original bytes and verified hashes.
5. Unknown historical build provenance remains explicitly `incomplete`, not invented.
6. Future ENCHDASH firmware builds on a pinned QMK revision and passes real-device/VIA smoke testing.
7. Owner-applied KiCad markings pass ERC, DRC, Gerber, and first-article review.
8. Repository rename/public messaging occurs only after separate approval.
9. Automated checks and final diff validation pass.
10. No commit or push occurs without explicit owner authorization.
