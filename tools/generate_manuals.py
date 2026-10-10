#!/usr/bin/env python3
"""Generate branded ENCHDASH user manuals (Positron Electronic) as PDFs.

Source content preserved from the original DOC/*.pdf manuals; rebranded,
reference-corrected (canonical VIA JSON, GitHub repo, ENCHDASH name), and
laid out with a consistent Positron Electronic visual identity.

Usage: python tools/generate_manuals.py
Writes the four DOC/*.pdf manuals in place.
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    Image,
    ListFlowable,
    ListItem,
    PageTemplate,
    Paragraph,
    Spacer,
)

REPO = Path(__file__).resolve().parent.parent
DOC = REPO / "DOC"
HW = DOC / "HARDWARE"

# Positron Electronic brand palette
INK = colors.HexColor("#0B1020")       # near-black navy
ACCENT = colors.HexColor("#2DD4BF")    # teal
ACCENT2 = colors.HexColor("#6366F1")   # indigo
MUTED = colors.HexColor("#64748B")     # slate
LIGHT = colors.HexColor("#F1F5F9")     # light slate
RULE = colors.HexColor("#1E293B")

REPO_URL = "https://github.com/juarendra/ERGODASH-MOD-ENCH-OLED-QMK_VIA"
CANON_JSON = "NEW_ErgoDash_4key_V3_mod_positron_elektronik.json"

styles = getSampleStyleSheet()


def _styles():
    s = {}
    s["title"] = ParagraphStyle(
        "title", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=26, leading=30, textColor=INK, spaceAfter=2,
    )
    s["subtitle"] = ParagraphStyle(
        "subtitle", fontName="Helvetica", fontSize=12, leading=16,
        textColor=MUTED, spaceAfter=10,
    )
    s["h2"] = ParagraphStyle(
        "h2", fontName="Helvetica-Bold", fontSize=14, leading=18,
        textColor=ACCENT2, spaceBefore=14, spaceAfter=6,
    )
    s["body"] = ParagraphStyle(
        "body", fontName="Helvetica", fontSize=10.5, leading=15,
        textColor=INK, spaceAfter=6,
    )
    s["li"] = ParagraphStyle(
        "li", fontName="Helvetica", fontSize=10.5, leading=15,
        textColor=INK,
    )
    s["note"] = ParagraphStyle(
        "note", fontName="Helvetica-Oblique", fontSize=9.5, leading=14,
        textColor=MUTED, spaceBefore=6, spaceAfter=6,
        borderPadding=(6, 6, 6, 6), backColor=LIGHT, leftIndent=4, rightIndent=4,
    )
    s["code"] = ParagraphStyle(
        "code", fontName="Courier", fontSize=9.5, leading=13,
        textColor=INK, backColor=LIGHT, borderPadding=(4, 4, 4, 4),
        spaceAfter=6,
    )
    s["footer"] = ParagraphStyle(
        "footer", fontName="Helvetica", fontSize=7.5, leading=10,
        textColor=MUTED, alignment=TA_CENTER,
    )
    return s


S = _styles()


def _header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    # top brand band
    canvas.setFillColor(INK)
    canvas.rect(0, h - 18 * mm, w, 18 * mm, fill=1, stroke=0)
    canvas.setFillColor(ACCENT)
    canvas.rect(0, h - 18 * mm, w, 2 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(18 * mm, h - 12 * mm, "POSITRON ELECTRONIC")
    canvas.setFillColor(ACCENT)
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawRightString(w - 18 * mm, h - 12 * mm, "ENCHDASH")
    # footer
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, 14 * mm, w - 18 * mm, 14 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(18 * mm, 10 * mm, "ENCHDASH — Positron Electronic")
    canvas.drawCentredString(w / 2, 10 * mm, REPO_URL)
    canvas.drawRightString(w - 18 * mm, 10 * mm, "Hal. %d" % doc.page)
    canvas.restoreState()


def build(path, title, subtitle, story_fn):
    doc = BaseDocTemplate(
        str(path), pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=26 * mm, bottomMargin=20 * mm,
        title=title, author="Positron Electronic",
        subject="ENCHDASH user manual", creator="ENCHDASH / Positron Electronic",
    )
    frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height, id="main",
    )
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=_header_footer)])
    story = [
        Spacer(1, 2 * mm),
        Paragraph(title, S["title"]),
        Paragraph(subtitle, S["subtitle"]),
        HRFlowable(width="100%", thickness=1.2, color=ACCENT, spaceAfter=8),
    ]
    story += story_fn()
    doc.build(story)


def bullets(items, numbered=False):
    lis = [ListItem(Paragraph(t, S["li"])) for t in items]
    return ListFlowable(
        lis, bulletType="1" if numbered else "bullet",
        bulletColor=ACCENT2, leftIndent=14, bulletFontName="Helvetica-Bold",
        spaceBefore=2, spaceAfter=8,
    )


def p(t):
    return Paragraph(t, S["body"])


def h2(t):
    return Paragraph(t, S["h2"])


def note(t):
    return Paragraph(t, S["note"])


def code(t):
    return Paragraph(t, S["code"])


def hw_image(name, max_w=120 * mm, max_h=90 * mm):
    f = HW / name
    img = Image(str(f))
    iw, ih = img.imageWidth, img.imageHeight
    scale = min(max_w / iw, max_h / ih)
    img.drawWidth, img.drawHeight = iw * scale, ih * scale
    img.hAlign = "CENTER"
    return img


# ---------------------------------------------------------------- manuals

def panduan():
    return [
        p("Panduan ini membantu Anda mulai menggunakan keyboard <b>ENCHDASH</b> "
          "bersama aplikasi <b>VIA Configurator</b>. Dokumentasi lengkap dan berkas "
          "terbaru tersedia di repositori resmi:"),
        code(REPO_URL),
        hw_image("ergodash1.png"),
        Spacer(1, 4 * mm),
        h2("Berkas Pendukung"),
        bullets([
            "<b>Link Keycode.txt</b> — daftar keycode yang dapat dipakai saat menyetel keymap.",
            "<b>TUTORIAL MACRO ON VIA CONFIGURATOR.txt</b> — tautan tutorial membuat macro di VIA.",
            "<b>LINK TUTORIAL PENGGUNAAN</b> — tautan video tutorial penggunaan.",
            "<b>TUTORIAL MEMBUAT TOMBOL PINDAH LAYER</b> — panduan mengubah fungsi tombol sebagai pemindah layer.",
            "<b>%s</b> — berkas VIA JSON kanonik untuk di-load di VIA." % CANON_JSON,
        ]),
        note("Catatan: berkas VIA JSON legacy "
             "<font face='Courier'>ErgoDash_4key_mod_positron_elektronik.json</font> "
             "disediakan untuk unit lama. Untuk produk terbaru gunakan berkas kanonik di atas."),
        h2("Cara Menggunakan VIA pada Keyboard"),
        bullets([
            "Hubungkan ENCHDASH ke PC.",
            "Buka aplikasi VIA.",
            "Pada tab <b>Settings</b>, aktifkan <b>Show Design tab</b>.",
            "Buka tab <b>Design</b>.",
            "Load berkas <font face='Courier'>%s</font>." % CANON_JSON,
            "Buka tab <b>Configure</b> untuk mulai menyetel.",
            "Jika masih muncul gambar <i>searching</i>, ulangi proses load JSON.",
        ], numbered=True),
        h2("Tentang Batas Macro"),
        p("VIA hanya dapat menyimpan maksimal <b>15 macro</b> di seluruh layer. Untuk "
          "kombinasi sederhana seperti <b>Ctrl + Alt + Del</b>, gunakan fitur "
          "<b>Any Key</b> pada tab Special agar tidak memakai slot macro."),
        p("Panduan VIA selengkapnya: "
          "<font color='#6366F1'>https://www.caniusevia.com/docs/configuring</font>"),
    ]


def tutorial_penggunaan():
    return [
        p("Video tutorial penggunaan ENCHDASH dengan VIA Configurator:"),
        code("https://youtu.be/5S3UWNQlxmA"),
        hw_image("ergodash2.png"),
        Spacer(1, 4 * mm),
        h2("Langkah Penggunaan VIA"),
        bullets([
            "Hubungkan ENCHDASH ke PC terlebih dahulu.",
            "Buka aplikasi VIA.",
            "Pada tab <b>Settings</b>, aktifkan <b>Show Design tab</b>.",
            "Buka tab <b>Design</b>.",
            "Load berkas <font face='Courier'>%s</font>." % CANON_JSON,
            "Buka tab <b>Configure</b> untuk melakukan penyetelan.",
            "Jika masih muncul gambar <i>searching</i>, ulangi proses load JSON.",
        ], numbered=True),
        note("Lakukan langkah ini setiap kali ingin menyetel ENCHDASH melalui VIA."),
        h2("Unduh VIA Configurator"),
        p("Pilih sesuai sistem operasi yang Anda gunakan:"),
        code("https://github.com/the-via/releases/releases"),
    ]


def macro_usage():
    return [
        p("VIA memiliki ruang penyimpanan macro yang terbatas. Untuk memaksimalkan "
          "penggunaan, pakailah fitur <b>Any Key</b> jika macro Anda hanya kombinasi "
          "sederhana — fitur Any Key saat ini tidak memiliki batas jumlah."),
        h2("Jenis Macro"),
        bullets([
            "<b>Macro Normal</b> — untuk kombinasi rumit, gunakan tab/menu <b>MACRO</b>. "
            "<b>Macro Recorder</b> memungkinkan Anda merekam macro alih-alih mengetik keycode manual.",
            "<b>Keycode Entry</b> — ketik teks langsung tanpa perlu tahu nama keycode QMK; "
            "untuk keycode dasar, bungkus dengan kurung kurawal <font face='Courier'>{ }</font>.",
        ]),
        h2("Istilah Penting"),
        bullets([
            "<b>MO(layer)</b> — mengaktifkan layer selama ditekan; kembali saat dilepas "
            "(mirip Shift / Fn).",
            "<b>LM(layer, modifier)</b> — mengaktifkan layer sekaligus menahan modifier.",
            "<b>LT(layer, keycode)</b> — tahan untuk mengaktifkan layer, ketuk sebentar "
            "untuk mengirim keycode. Cocok untuk tombol seperti Tab atau Space.",
        ]),
        h2("Contoh Macro"),
        code("MyPassw0rd!            -> mengirim teks MyPassw0rd!<br/>"
             "{KC_A,KC_C,KC_E}       -> mengirim a, c, e<br/>"
             "{KC_LCTL,KC_C}         -> mengirim Ctrl-C"),
        h2("Any Key"),
        p("Any Key dapat menjalankan keycode yang lebih kompleks (melibatkan modifier, "
          "layer, atau mod-tap). Tidak semua alias didukung — misalnya "
          "<font face='Courier'>LCTL_T(kc)</font> tidak bisa dipakai, gunakan "
          "<font face='Courier'>MT(MOD_LCTL, kc)</font>."),
        code("LALT(KC_TAB)           -> Alt-Tab<br/>"
             "LCTL(KC_C)             -> Ctrl-C<br/>"
             "LGUI(KC_C)             -> Cmd-C / Win-C<br/>"
             "LSFT(LCTL(KC_END))     -> Shift-Ctrl-End<br/>"
             "MO(1)                  -> aktifkan layer 1 sementara<br/>"
             "LCA(KC_DEL)            -> Ctrl-Alt-Del<br/>"
             "MT(MOD_RSFT, KC_ENT)   -> Shift jika ditahan, Enter jika diketuk"),
    ]


def pindah_layer():
    return [
        p("Panduan mengatur satu tombol agar dapat memindahkan layer secara berurutan "
          "pada ENCHDASH menggunakan VIA Configurator."),
        h2("Langkah-langkah"),
        bullets([
            "Buka aplikasi <b>VIA Configurator</b>.",
            "Load berkas VIA JSON <font face='Courier'>%s</font>." % CANON_JSON,
            "Hubungkan ENCHDASH ke PC.",
            "Buka tab <b>Configure</b>.",
            "Pada tab Configure, pilih tab <b>Layer</b>.",
            "Tentukan satu tombol yang akan dipakai untuk perpindahan layer.",
            "Saat pertama terhubung, ENCHDASH otomatis berada di <b>layer 0</b>.",
            "Klik tombol tersebut, ganti fungsinya menjadi <b>TO(1)</b> — "
            "memindahkan layer sekarang ke layer 1.",
            "Pindah ke layer 1, klik tombol itu lagi, ganti menjadi <b>TO(2)</b>.",
            "Pindah ke layer 2, klik lagi, ganti menjadi <b>TO(3)</b>.",
            "Pindah ke layer 3, klik lagi, ganti menjadi <b>TO(0)</b> — kembali ke layer 0.",
        ], numbered=True),
        note("Alur akhir: layer 0 → layer 1 → layer 2 → layer 3 → layer 0 "
             "(TO(1) → TO(2) → TO(3) → TO(0))."),
        hw_image("ergodash1.png"),
    ]


MANUALS = [
    ("KERTAS PANDUAN ERGODASH.pdf", "Panduan Pengguna ENCHDASH",
     "Keyboard mekanik split — Positron Electronic", panduan),
    ("LINK TUTORIAL PENGGUNAAN.pdf", "Tutorial Penggunaan",
     "Menggunakan ENCHDASH dengan VIA Configurator", tutorial_penggunaan),
    ("MACRO VIA USAGE.pdf", "Panduan Macro VIA",
     "Membuat dan mengelola macro pada ENCHDASH", macro_usage),
    ("TUTORIAL MEMBUAT TOMBOL PINDAH LAYER.pdf", "Tutorial Tombol Pindah Layer",
     "Mengatur tombol perpindahan layer di VIA", pindah_layer),
]


def main():
    for fname, title, subtitle, fn in MANUALS:
        out = DOC / fname
        build(out, title, subtitle, fn)
        print("wrote", out.relative_to(REPO), out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
