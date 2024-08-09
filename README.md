# Ergodash-Mod-QMK-VIA
This is MOD of ergodash, the normal ergodash just have Swith MX. This mod is for add Encoder, Oled and make it hotswapable with Khail Hotswap

## Table of Content
* [Product Specsification](#product-specsification)
* [Download VIA](#download-via)
* [Load JSON File](#Load-JSON-File)
* [Link Keycode QMK](#Link-keycode-qmk)
* [Tutorial VIA Usage](#tutorial-via-usage)
* [Cara Setting Knob](#cara-setting-knob)
* [How To use MACRO](#how-to-use-macro)
* [Preview Hardware](#preview-hardware)
* [Preview VIA](#preview-via)
* [Cara Update/Upgrade Firmware](#cara-update/upgrade-firmware)
* [Documentation](#documentation)
  * [Pinout Diagram](#pinout-diagram)
  * [Dimension](#dimension)
  * [BOM](#bom)
  * [Schematic](#schematic)
  * [Example Program](#examples-program)
* [FAQ](#FAQ)

## Product Specsification
- Arduino Pro Micro Type C as Microcontroller
- QMK Firmware
- Support VIA, all key and knob can proggrammed
- RGB Underglow
- 4x Layer 
- Hotswap Switch
- 3D Case 
- Ergodash Profile

## Download VIA
Link Download VIA(CHOSEE BASED YOUR OS) : https://github.com/the-via/releases/releases
VIA WEB VERSION : https://usevia.app/


## Load JSON File
or you can load manually json file like a library for detect this macropad
- Connect your macropad to PC
- Open VIA
- In Tab Setting, enable "Show Design Tab"
- Open Design Tab
- Load file with name "NEW_ErgoDash_4key_V3_mod_positron_elektronik.json" 
- Open Configure Tab to setting your macropad
- If nothing happend , do it again from first 

## Link Keycode QMK
- mouse : https://github.com/qmk/qmk_firmware/blob/master/docs/feature_mouse_keys.md
- keyboard : https://github.com/qmk/qmk_firmware/blob/master/docs/keycodes.md

## Tutorial VIA Usage
- https://docs.keeb.io/via

## Cara Setting Knob
- Untuk melakukan setting di knob perlu memasukan command berupa keycode qmk, Jadi cara nya sama dengan melakuykan setting dengan Any key seperti petunjuk pada link berikut: 
https://docs.keeb.io/via

Here's some examples:

- LALT(KC_TAB) - Sends Alt-Tab
- LCTL(KC_C) - Sends Ctrl-C
- LGUI(KC_C) - Sends Cmd-C or Win-C
- LSFT(LCTL(KC_END)) - Sends Shift-Ctrl-End
- MO(1) - Momentarily turn on layer 1
- LCA(KC_DEL) - Sends Ctrl-Alt-Del
- MT(MOD_RSFT, KC_ENT) - Sends Shift if held, Enter if tapped
- MACRO (0) - macro 0

## How To use MACRO
you can read on [this file](https://github.com/juarendra/STREAMPAD-QMK-VIA/blob/main/DOC/MACRO%20VIA%20USAGE.pdf)
or you can read on this [web](https://www.keychron.com/blogs/archived/how-to-use-via-to-program-your-keyboard)
or you can see video [youtube](https://youtu.be/GtSeo69Y0Zw)

## Preview Hardware
<p align="center">
  <img src="DOC/HARDWARE/ergodash2.png" width="50%" height="50%">
  <img src="DOC/HARDWARE/ergodash4.jpeg" width="50%" height="50%">
  <img src="DOC/HARDWARE/ergodash5.jpeg" width="50%" height="50%">
  <img src="DOC/HARDWARE/ergodash6.jpeg" width="50%" height="50%">
</p>

## Preview VIA

https://github.com/juarendra/Zeapad-Pro-QMK-VIA/assets/43043633/afd7e68e-0a54-4b18-be12-b96c0f13611a

## Documentation
### Pinout Diagram
### Dimension
[Dimension File](https://github.com/juarendra/ERGODASH-MOD-ENCH-OLED-QMK_VIA/blob/main/Hardware/Dimension_Ergodash.pdf)
### BOM
### Schematic
[Schematic File](https://github.com/juarendra/ERGODASH-MOD-ENCH-OLED-QMK_VIA/blob/main/Hardware/ErgoDash_Schematic.pdf)
### Example Program
[Example Firmware](hhttps://github.com/juarendra/ERGODASH-MOD-ENCH-OLED-QMK_VIA/tree/main/FIRMWARE)
## FAQ
