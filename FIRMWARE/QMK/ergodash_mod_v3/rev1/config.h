/* Copyright 2024 Juarendra Ramadhani <jrjuarendra@gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#pragma once


/* key matrix size */
// Rows are doubled-up
#define MATRIX_ROWS 12
#define MATRIX_COLS 7

// wiring of each half
#define MATRIX_ROW_PINS { D4, D7, E6, B4, B5 , B0}
#define MATRIX_COL_PINS { C6, F5, F6, F7, B1, B3, B2 }
// #define MATRIX_COL_PINS { B2, B3, B1, F7, F6, F5, F4 } //uncomment this line and comment line above if you need to reverse left-to-right key order

#define DIODE_DIRECTION COL2ROW

/* define tapping term */
#define TAPPING_TERM 120

/* Set 0 if debouncing isn't needed */
#define DEBOUNCE 5

/* Mechanical locking support. Use KC_LCAP, KC_LNUM or KC_LSCR instead in keymap */
#define LOCKING_SUPPORT_ENABLE
/* Locking resynchronize hack */
#define LOCKING_RESYNC_ENABLE

#define ENCODERS_PAD_A { F4 }
#define ENCODERS_PAD_B { B6 }
#define ENCODER_RESOLUTION 4
#define TAP_CODE_DELAY  10

// Add RGB underglow
// by defining in the keyboard, incompatible keymaps will fail to compile.
#ifdef RGBLIGHT_ENABLE
#    define WS2812_DI_PIN D3
#    define RGBLED_NUM 24
#    define RGBLED_SPLIT {12,12}
#    define RGBLIGHT_LIMIT_VAL 100 // LED Brightness, high power draw may exceed the USB limitations of 0.6A and cause a crash.
#    define RGBLIGHT_HUE_STEP  10
#    define RGBLIGHT_SAT_STEP  17
#    define RGBLIGHT_VAL_STEP  17
//#    define RGBLIGHT_LAYERS //Enable layer light indicators. Not required as updates are done in layer_state_set_user and led_update_user (+588).
#    define RGBLIGHT_SLEEP //Turn off LEDs when computer sleeping (+72)
#endif

#define SOFT_SERIAL_PIN D2
#define SPLIT_USB_DETECT

// OLED settings
#define OLED_TIMEOUT    80000
#define OLED_BRIGHTNESS 90

#define SPLIT_OLED_ENABLE
#define SPLIT_TRANSPORT_MIRROR

#ifdef RGBLIGHT_ENABLE
#    define RGBLIGHT_DEFAULT_MODE RGBLIGHT_MODE_RAINBOW_SWIRL+2

// Disabling some of these is a good way to save flash space.
//#    define RGBLIGHT_EFFECT_ALTERNATING     // 108
#    define RGBLIGHT_EFFECT_RAINBOW_MOOD    // 160
#    define RGBLIGHT_EFFECT_STATIC_GRADIENT // 168
#    define RGBLIGHT_EFFECT_RAINBOW_SWIRL   // 192
#    define RGBLIGHT_EFFECT_BREATHING       // 348
//#    define RGBLIGHT_EFFECT_KNIGHT          // 336
//#    define RGBLIGHT_EFFECT_SNAKE           // 406
/*
#define RGBLIGHT_EFFECT_TWINKLE         // 1156
*/
#endif