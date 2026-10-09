# ENCHDASH KiCad Silkscreen and Metadata Guide

**Purpose**: Owner-applied KiCad metadata and silkscreen updates to reflect ENCHDASH identity and attribution requirements.

**Status**: Awaiting owner execution  
**Date**: 2026-10-08

---

## Important Notes

1. **Owner applies these changes** — agent does not edit KiCad files
2. **Apply before manufacturing new PCB batches** — existing sold units unchanged
3. **Verify all changes** — follow verification checklist at end of document
4. **Backup first** — save a copy of `ergodash.kicad_pcb` and `ergodash.kicad_sch` before editing

---

## Part 1: KiCad Project Metadata (Title Block)

### Location
Open `Hardware/PCB/Rev1.2/ergodash.kicad_pro` in KiCad → File → Page Settings

### Current State (to be replaced)

```
Title: ErgoDash Rev2
Revision: 2.0
Company: Omkbd
Date: 2018-06-07
```

### Required Changes

```
Title: ENCHDASH
Revision: 1.2
Company: Positron Electronic
Date: 2026-10-08 (or actual next manufacturing date)

Comment 1: Independent derivative of ErgoDash by omkbd
Comment 2: Original work: Copyright (c) 2018 omkbd
Comment 3: Modifications: Copyright (c) 2024-2026 Juarendra Ramadhani
Comment 4: License: MIT
Comment 5: https://github.com/juarendra/ENCHDASH-QMK-VIA
```

**Notes**:
- Use actual manufacturing date for "Date" field
- Revision `1.2` assumed — adjust if next revision is different
- Keep URL current if repository is renamed

---

## Part 2: PCB Silkscreen Markings

### Preferred Full Attribution (if space permits)

Place on bottom silkscreen, visible when board is flipped:

```
ENCHDASH R1.2
ErgoDash-derived · Original © 2018 omkbd · MIT
MOD © 2024–2026 Juarendra Ramadhani
Positron Electronic
github.com/juarendra/ENCHDASH-QMK-VIA
```

**Text specifications**:
- Font: KiCad default or legible sans-serif
- Size: 1.0–1.5 mm height (readable but compact)
- Placement: Bottom layer, outside component keepout areas
- Suggested location: Near USB connector or bottom center

### Compact Alternative (if space limited)

```
ENCHDASH R1.2
ErgoDash-derived · © omkbd 2018 · MIT
© J. Ramadhani 2024–2026
github.com/juarendra/ENCHDASH-QMK-VIA
```

### Minimum Required (if extremely constrained)

```
ENCHDASH R1.2
github.com/juarendra/ENCHDASH-QMK-VIA
```

OR use QR code pointing to repository (minimum 10×10 mm for reliable scanning).

**Requirement**: If using minimum version, full attribution MUST appear in:
- Printed manual included with keyboard
- Product listing description
- README.md (already present)

---

## Part 3: Prohibited Markings

**DO NOT use any of these**:

```
❌ Official ErgoDash
❌ ErgoDash Rev2 (without "derivative" qualifier)
❌ ErgoDash by omkbd & Positron
❌ Approved by omkbd
❌ Endorsed by omkbd
❌ Company: omkbd (in title block)
```

**DO NOT add**:
- omkbd logo
- QMK logo (unless QMK project grants permission)
- VIA logo (unless VIA project grants permission)
- Certification marks (FCC, CE, RoHS) not earned
- USB-IF logo (unless VID is officially allocated)
- Revision number that doesn't match released Gerber files

**Factual reference allowed**:
- "ErgoDash-derived"
- "Based on ErgoDash by omkbd"
- "Compatible with QMK firmware"
- "Supports VIA configurator"

---

## Part 4: Editing Steps in KiCad

### Step 1: Open Project

1. Launch KiCad 6.0 or later
2. Open `Hardware/PCB/Rev1.2/ergodash.kicad_pro`

### Step 2: Update Title Block

1. Open schematic: `ergodash.kicad_sch`
2. File → Page Settings
3. Update fields per Part 1 above
4. Click OK
5. Save schematic

### Step 3: Update PCB Silkscreen

1. Open PCB editor: `ergodash.kicad_pcb`
2. Select bottom silkscreen layer: `B.SilkS`
3. Place → Text
4. Enter attribution text (Part 2 above)
5. Position text in suitable location (check DRC clearance)
6. Verify text does not overlap:
   - Component pads
   - Exposed copper
   - Solder mask openings
   - Board outline cuts
   - Mounting holes
   - Component placement areas

### Step 4: Generate QR Code (Optional)

If space is limited, use QR code instead of URL text:

1. Generate QR code: https://www.qr-code-generator.com/
   - URL: `https://github.com/juarendra/ENCHDASH-QMK-VIA`
   - Size: minimum 10×10 mm on PCB
   - Error correction: H (high)

2. Save as PNG or SVG

3. KiCad PCB Editor:
   - File → Import → Graphics
   - Select QR code image
   - Place on `B.SilkS` layer
   - Scale to at least 10×10 mm

### Step 5: Run Design Rule Check

1. Inspect → Design Rules Checker
2. Run DRC
3. Verify:
   - No silkscreen-to-pad clearance violations
   - No silkscreen outside board outline
   - No overlapping text

4. Fix any errors before continuing

### Step 6: Visual Inspection

1. View → 3D Viewer
2. Inspect bottom side — verify text visible and readable
3. Check text does not interfere with components when assembled

---

## Part 5: Pre-Manufacturing Verification

### Owner Verification Checklist

Submit these items for review before manufacturing:

- [ ] KiCad title block screenshot (File → Page Settings)
- [ ] PCB front render or Gerber viewer screenshot
- [ ] PCB back render (showing silkscreen attribution)
- [ ] ERC result: `Inspect → Electrical Rules Checker` → screenshot
- [ ] DRC result: `Inspect → Design Rules Checker` → screenshot
- [ ] Confirm silkscreen does not overlap pads/copper/holes
- [ ] Confirm text remains visible after assembly
- [ ] Confirm QR code (if used) scans correctly

### Export Gerber Files

After verification passes:

1. File → Fabrication Outputs → Gerbers (.gbr)
2. Output directory: `Hardware/PCB/Rev1.2/gerber_enchdash_r1.2/`
3. Include layers:
   - F.Cu, B.Cu (copper)
   - F.SilkS, B.SilkS (silkscreen)
   - F.Mask, B.Mask (solder mask)
   - Edge.Cuts (board outline)
4. Drill files: PTH and NPTH separate

5. Zip Gerbers for manufacturer

6. Review Gerbers with viewer before sending:
   - https://www.pcbway.com/project/OnlineGerberViewer.html
   - https://tracespace.io/view/

---

## Part 6: Manufacturing Notes

### First Article Inspection

When receiving first boards from manufacturer:

- [ ] Silkscreen legible under normal lighting
- [ ] Attribution text intact (not clipped by manufacturing process)
- [ ] QR code (if used) scans successfully with phone camera
- [ ] No silkscreen on pads or vias
- [ ] Board matches Gerber preview exactly

### Ongoing Quality

- [ ] Each batch spot-check: silkscreen quality maintained
- [ ] Keep dated photos of manufactured boards in `Hardware/photos/`
- [ ] Keep manufacturer revision log if they apply internal rev numbers

---

## Part 7: What NOT to Change

**Leave these unchanged**:

- Matrix pin assignments (`MATRIX_ROW_PINS`, `MATRIX_COL_PINS`)
- Controller footprint (Pro Micro pinout)
- Switch footprints and spacing
- Mounting hole positions
- TRRS connector pinout
- Power routing
- I²C routing for OLED
- Serial data line for split communication
- Encoder pinout
- RGB data line routing

**Reason**: Changing these breaks compatibility with existing firmware and requires new firmware builds + testing.

---

## Part 8: Evidence Submission

After completing KiCad edits, create `docs/evidence/kicad-owner-verification.md` with:

```markdown
# ENCHDASH KiCad Owner Verification Evidence

**Date**: YYYY-MM-DD  
**Verified by**: [Owner name]  
**Hardware revision**: Rev1.2

## Title Block

![Title block screenshot](../screenshots/title-block.png)

- Title: ENCHDASH ✓
- Revision: 1.2 ✓
- Company: Positron Electronic ✓
- Attribution comments present ✓

## PCB Renders

### Front
![Front render](../screenshots/pcb-front.png)

### Back (with attribution)
![Back render](../screenshots/pcb-back.png)

Attribution text visible and legible ✓

## ERC Result

![ERC](../screenshots/erc-result.png)

Errors: 0 ✓

## DRC Result

![DRC](../screenshots/drc-result.png)

Errors: 0 ✓
Silkscreen clearance violations: 0 ✓

## Gerber Preview

![Gerber back](../screenshots/gerber-back-silkscreen.png)

Reviewed with: [Viewer name]  
Silkscreen matches KiCad preview ✓

## Manufacturing Approval

- [ ] Ready for manufacturing
- [ ] First article inspection required before full batch

**Approved by**: ___________  
**Date**: ___________
```

---

## Part 9: Rollback

If manufactured boards have errors:

1. Revert `ergodash.kicad_pcb` to Git commit before changes
2. Document what went wrong in `docs/evidence/kicad-owner-verification.md`
3. Fix issues before re-exporting Gerbers
4. Do not ship boards with incorrect attribution

---

## Questions?

**Before manufacturing**, if uncertain about any marking:
1. Check this guide
2. Review `docs/HARDWARE-ATTRIBUTION.md`
3. Compare with MIT License requirements (LICENSES/MIT-ErgoDash.txt)
4. When in doubt: include more attribution, not less

**Principle**: Over-attribution is safe; under-attribution risks license violation.

---

**Last updated**: 2026-10-08  
**Applies to**: ENCHDASH Rev1.2 and future revisions
