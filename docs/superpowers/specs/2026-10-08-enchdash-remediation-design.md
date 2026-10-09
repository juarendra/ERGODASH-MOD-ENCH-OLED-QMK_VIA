# ENCHDASH Compliance and Identity Remediation Design

Date: 2026-10-08
Status: Approved 2026-10-08
Target repository: https://github.com/juarendra/ERGODASH-MOD-ENCH-OLED-QMK_VIA

## 1. Goal

Migrate the already-sold product from the legacy identity `ERGODASH-MOD-ENCH-OLED-QMK_VIA` to `ENCHDASH` while preserving support for existing units, adding complete attribution and license records, and preventing misleading affiliation claims.

This work is compliance and identity remediation, not a redesign of working hardware.

## 2. Confirmed identity

- Product name: `ENCHDASH`
- Copyright holder for modifications: `Juarendra Ramadhani`
- Commercial identity: `Positron Electronic`
- Original design attribution: `ErgoDash by omkbd`, copyright 2018, MIT License
- Relationship statement: independent derivative; not official, approved, maintained, or endorsed by omkbd
- Legacy name: `ERGODASH-MOD-ENCH-OLED-QMK_VIA`

## 3. Current evidence

Public repository inspection found:

- GitHub reports no root license (`license: null`); root `LICENSE` is absent.
- Root README identifies the product primarily as `Ergodash-Mod-QMK-VIA` and lacks a formal omkbd attribution/disclaimer.
- `Hardware/PCB/Rev1.2/ergodash.kicad_pcb` title block says `ErgoDash Rev2`, revision `2.0`, company `Omkbd`, date `2018-06-07`.
- The repository contains native KiCad source, generated hardware files, footprint libraries, QMK-derived firmware source, VIA JSON files, and three distributed `.hex` binaries.
- Modified QMK metadata contains `keyboard_name: ErgoDash Hotswap By Positron`, `manufacturer: Positron Electronic`, and USB identity `0x4D44:0x6061`.
- Current VIA JSON uses the name `ErgoDash` and USB identity `0x4D44:0x6061`.
- A sampled modified `keymap.c` contains a GPLv2-or-later-compatible header for Juarendra Ramadhani.
- Embedded footprint libraries include separate licenses, including CERN OHL material; no root third-party license index explains which assets are used.

These observations define audit inputs, not a complete legal conclusion.

## 4. Scope

### Included

1. Add root licensing and third-party attribution documents.
2. Rewrite public product documentation around the ENCHDASH identity.
3. Preserve and document legacy hardware, firmware, VIA JSON, URLs, and product name.
4. Inventory every distributed firmware binary and map it to hardware revision, USB identity, VIA JSON, source path, build command, source revision, and checksum where evidence exists.
5. Audit QMK source notices and buildability.
6. Audit VIA JSON consistency with firmware USB identity.
7. Audit USB VID/PID provenance before any identity change.
8. Audit bundled footprint/library licenses and retain required notices.
9. Provide an exact KiCad metadata and silkscreen guide for the owner to apply.
10. Provide release and customer-notice procedures for future batches and existing customers.
11. Rename the GitHub repository only after internal links and compatibility references are prepared.

### Excluded

- Editing KiCad files; owner performs those edits from the approved guide.
- Changing electrical design, matrix, pinout, controller, bootloader, or physical compatibility.
- Reflashing already-sold units automatically.
- Changing USB VID/PID before provenance and compatibility review passes.
- Deleting legacy `.hex`, VIA JSON, source, documentation, tags, or Git history.
- Claiming legal certification or giving jurisdiction-specific legal advice.
- Contacting omkbd, customers, or marketplaces without separate owner approval.
- Using omkbd, QMK, or VIA logos unless their applicable branding permission is separately verified.

## 5. Migration model

Use a staged, backward-compatible migration.

### Stage A: Compliance baseline

Add license texts, third-party notices, origin statement, legacy support statement, and firmware provenance table without moving working files. Existing links remain valid.

### Stage B: ENCHDASH public identity

Make ENCHDASH the primary product name in README, repository description, release documentation, firmware metadata for future builds, and VIA metadata for future builds. State the old name as a searchable legacy alias.

### Stage C: New release namespace

Create a clean future firmware target such as `keyboards/positron/enchdash` only after a reproducible QMK build is proven. Keep old source trees read-only under a documented legacy classification. No mass rename is allowed before build and link verification.

### Stage D: Repository rename

Rename the GitHub repository to `ENCHDASH-QMK-VIA` after all repository-relative and absolute links are audited. GitHub redirect behavior is helpful but is not the verification mechanism; old and new URLs must both be tested.

## 6. Target documentation

Minimum target files:

```text
README.md
LICENSE
LICENSES/
  MIT-ErgoDash.txt
  GPL-2.0-or-later.txt
THIRD_PARTY_NOTICES.md
CHANGELOG.md
docs/
  LEGACY-SUPPORT.md
  HARDWARE-ATTRIBUTION.md
  RELEASE-CHECKLIST.md
  SILKSCREEN-GUIDE.md
FIRMWARE/
  README.md
```

Do not reorganize `Hardware/` or `FIRMWARE/` in the first compliance change. File movement is a later, independently verified task because public links and customer instructions already reference current paths.

### Root license policy

The root license must explicitly state which repository portions it covers. A single ambiguous license over mixed hardware, firmware, documentation, and third-party libraries is prohibited.

Chosen policy:

- ENCHDASH original and modified hardware design files: MIT, retaining ErgoDash's original MIT notice.
- QMK-derived firmware: GPL-2.0-or-later where inherited source permits/requires it, retaining upstream file notices.
- Third-party footprint/library files: their own upstream licenses, indexed rather than relicensed.
- Binary firmware: distributed with access to corresponding source and build/provenance information.
- Documentation and owner-created assets: explicitly identified in the root license; default to MIT only where Juarendra Ramadhani owns the material and no embedded third-party work conflicts.

## 7. README contract

README must start with:

```markdown
# ENCHDASH

ENCHDASH is an independent keyboard design derived from ErgoDash by
omkbd. It is not an official ErgoDash revision and is not maintained,
approved, or endorsed by omkbd.

Original ErgoDash hardware:
Copyright (c) 2018 omkbd
https://github.com/omkbd/ErgoDash
Licensed under the MIT License.

ENCHDASH modifications:
Copyright (c) 2024–2026 Juarendra Ramadhani
Commercial identity: Positron Electronic

Previously sold as ERGODASH-MOD-ENCH-OLED-QMK_VIA. Existing units remain
supported under that legacy name.
```

README must also contain:

- supported hardware revision table;
- legacy/new naming table;
- features stated only when confirmed by current files or hardware evidence;
- exact VIA JSON selection per hardware/firmware revision;
- firmware download and build links;
- source and license links;
- compatibility warning preventing cross-flashing unsupported revisions;
- link to legacy support and release checklist;
- corrected internal links, including the malformed current `hhttps://` firmware link.

## 8. Legacy compatibility contract

Existing units are immutable compatibility targets.

For each distributed variant, record:

| Field | Required evidence |
|---|---|
| Legacy product name | Existing README, manual, label, or marketplace record |
| Hardware revision | PCB source, physical board marking, or owner-confirmed production record |
| Controller/bootloader | Source metadata plus successful build or physical inspection |
| USB VID/PID | Firmware metadata and host enumeration where available |
| VIA JSON | Matching `vendorId`, `productId`, matrix, and layout |
| Firmware binary | Repository path and SHA-256 |
| Source | Exact repository path and source commit |
| QMK base | Exact upstream commit or explicitly recorded as not yet reconstructable |
| Build command | Command proven against the pinned QMK base |
| Reproducibility | `verified`, `functionally rebuilt`, or `unverified`; never inferred |

Files without enough historical evidence remain supported downloads but must be marked `provenance incomplete`; do not invent missing commits or claim reproducibility.

## 9. USB and VIA migration rules

- Preserve `0x4D44:0x6061` for legacy artifacts until provenance is established.
- Do not assign a replacement VID/PID from guesswork or another vendor.
- Any future USB identity change requires an identified lawful allocation route, new firmware build, matching VIA JSON, host enumeration test, VIA detection test, and rollback artifact.
- A new VIA JSON name may say `ENCHDASH`; matching legacy JSON files retain their old names when needed by already-flashed firmware.
- VIA `vendorId` and `productId` must exactly match the compiled firmware identity.
- Firmware and JSON changes ship as one release unit.

## 10. Firmware compliance and release rules

Each distributed `.hex` requires a manifest row containing:

```text
artifact path
SHA-256
hardware revision
firmware version or release label
USB VID/PID
VIA JSON path
source path
source commit
authorized QMK base commit
exact build command
verification state
```

QMK-derived source rules:

- retain upstream copyright and GPL notices;
- add Juarendra Ramadhani's modification notice only to files actually modified;
- never replace upstream copyright with owner copyright;
- include full GPL-2.0-or-later license text;
- publish corresponding source and build instructions alongside binary releases;
- distinguish original QMK/ErgoDash code from ENCHDASH modifications;
- build both legacy and future ENCHDASH targets before changing customer instructions.

## 11. KiCad owner-edit guide

The implementation produces `docs/SILKSCREEN-GUIDE.md`; owner applies it to KiCad and returns exported evidence for review.

### Required project release markings for future PCB batches

These are ENCHDASH release requirements, not a claim that every line is universally mandated by law:

```text
ENCHDASH
hardware revision, for example R1.2
stable source URL or compact QR code resolving to it
```

### Chosen attribution marking

Use this when space and readability permit:

```text
ENCHDASH R1.2
ErgoDash-derived · Original © 2018 omkbd · MIT
MOD © 2024–2026 Juarendra Ramadhani
Positron Electronic
github.com/juarendra/ENCHDASH-QMK-VIA
```

Compact approved form:

```text
ENCHDASH R1.2
ErgoDash-derived · © omkbd 2018 · MIT
© J. Ramadhani 2024–2026
github.com/juarendra/ENCHDASH-QMK-VIA
```

If even the compact form does not fit legibly, the board keeps `ENCHDASH`, revision, and source URL/QR; full attribution remains in accompanying documentation and source distribution. This exception must be visually justified, not silently used.

### Prohibited or misleading markings

Do not place:

```text
Official ErgoDash
ErgoDash Rev2
ErgoDash by omkbd & Positron
Approved by omkbd
Endorsed by omkbd
Company: omkbd
```

Also prohibited without separate permission/evidence:

- omkbd logo;
- QMK or VIA logo used as a product endorsement;
- certification marks not earned for this product;
- unverified USB VID/PID;
- dead, private, temporary, or redirect-only source URL;
- a revision that does not match released manufacturing files.

`ErgoDash` may appear factually only as attribution such as `ErgoDash-derived`.

### KiCad metadata replacement

Owner changes the current title block to:

```text
Title: ENCHDASH
Revision: 1.2
Company: Positron Electronic
Comment: Independent derivative of ErgoDash by omkbd
Original work: Copyright (c) 2018 omkbd
Modifications: Copyright (c) 2024–2026 Juarendra Ramadhani
License: MIT
Source: https://github.com/juarendra/ENCHDASH-QMK-VIA
```

Revision and URL must match the actual release at edit time; `1.2` is used only if it is confirmed as the next manufactured revision.

### Owner verification evidence

Before manufacture, owner supplies:

1. KiCad title-block screenshot.
2. Front and back PCB render or Gerber viewer screenshots.
3. ERC result.
4. DRC result.
5. Confirmation that silkscreen does not overlap pads, exposed copper, solder-mask openings, board cuts, mounting holes, or component keepouts.
6. Confirmation that text remains visible after assembly.
7. Photo of first article from the next production batch.

## 12. Third-party asset audit

Inventory bundled libraries by source directory, upstream URL, license, modification state, and actual use in the board. Keep existing license files intact.

Rules:

- unused bundled libraries may be removed only in a separate cleanup after proving the active KiCad project does not reference them;
- copied libraries requiring source/location notices retain those notices;
- CERN OHL-covered documentation is not silently relicensed as MIT;
- logos, fonts, 3D models, photos, PDFs, tutorial material, and VIA/QMK assets are audited separately from schematic/PCB copyright;
- unknown provenance is recorded and blocks a clean compliance claim for that asset.

## 13. Customer and marketplace migration

Prepare, but do not send without owner approval:

```text
Produk yang sebelumnya dijual sebagai ERGODASH-MOD-ENCH-OLED-QMK_VIA
sekarang menggunakan nama ENCHDASH.

Produk tetap sama dan tetap didukung. Dokumentasi diperbarui untuk
memperjelas bahwa desain ini merupakan turunan independen dari ErgoDash
by omkbd dan menggunakan firmware berbasis QMK.

Dokumentasi, source hardware, source firmware, dan pemberitahuan lisensi:
<stable ENCHDASH repository URL>
```

Marketplace updates must preserve a compatibility note for prior buyers and must not imply omkbd endorsement.

## 14. Verification gates

### Repository gate

- Root license scope is explicit.
- `LICENSES/MIT-ErgoDash.txt` exactly retains omkbd's 2018 notice and MIT terms.
- GPL text and applicable firmware notices exist.
- `THIRD_PARTY_NOTICES.md` maps every audited third-party source.
- No unsupported official/endorsement wording remains outside quoted historical records.
- All documented links return successfully.
- Legacy file paths referenced by shipped customer documentation still resolve.

### Firmware gate

- Every `.hex` has SHA-256 and manifest status.
- Every claimed reproducible binary has a proven source commit, QMK base, and successful build command.
- Legacy and future build targets compile with the pinned toolchain.
- USB identity matches its VIA JSON.
- VIA detects a test device for every newly published pairing.
- No new VID/PID is released without provenance evidence.

### Hardware gate

- Owner completes KiCad metadata and silkscreen edits.
- ERC and DRC pass or every accepted exception is documented.
- Gerber review confirms legible, non-overlapping markings.
- First-article PCB photo confirms manufactured markings.

### Migration gate

- New repository name is `ENCHDASH-QMK-VIA`.
- Old URL redirects and new URL resolves.
- README exposes the legacy name for search/support.
- Existing binary and VIA downloads remain available.
- Release notes explain naming change without claiming electrical redesign.

## 15. Rollback

Before rename or firmware publication:

- record current repository name and default-branch commit;
- preserve legacy releases and checksums;
- export current repository settings and public URLs where practical;
- prepare a release note explaining rollback.

If new firmware/VIA pairing fails, withdraw only that new release, restore prior download pointers, and leave compliance documents in place. Do not erase Git history or remove legacy artifacts.

If repository rename breaks critical customer links, restore the former repository name or create a clear compatibility landing repository; never leave the old public path ambiguous.

## 16. Completion criteria

Remediation is complete only when:

1. Public repository uses ENCHDASH as primary identity and labels the old name as legacy.
2. Original omkbd attribution and MIT terms are preserved.
3. Firmware GPL obligations and binary-to-source records are documented.
4. Third-party library licenses are indexed without incompatible relicensing.
5. Existing units retain working downloads and instructions.
6. Future ENCHDASH firmware and VIA pairing is build-tested and device-tested.
7. Owner-applied KiCad markings pass documented ERC, DRC, Gerber, and first-article checks.
8. Repository rename and old-link compatibility are verified.
9. No claim of official omkbd status or endorsement remains.

## 17. Execution constraints

- Work in a clone/worktree of the ENCHDASH repository, never in the WTTP repository.
- No commit, push, repository rename, release publication, customer message, or marketplace edit without explicit owner authorization for that action.
- Preserve working hardware behavior; compliance changes do not justify speculative firmware or PCB redesign.
- Evidence beats reconstruction: record unknown historical provenance plainly rather than inventing it.
