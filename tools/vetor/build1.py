# -*- coding: utf-8 -*-
"""Next Pro — card "Siga a Next Pro" com QR (vector rebuild)."""
import lib, logo

W, H = 2000, 1291
GREEN = "#19d898"
MINT = "#2fe3ae"
QR_URL = "https://www.instagram.com/amplificadoresnextpro"

orb8 = lib.load("Orbitron-VF.ttf", wght=800)
orb7 = lib.load("Orbitron-VF.ttf", wght=700)
inter4 = lib.load("Inter-VF.ttf", wght=400)

P = []
add = P.append

add(f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2=".3" y2="1">
  <stop offset="0" stop-color="#0c0e0d"/><stop offset=".55" stop-color="#090a0a"/>
  <stop offset="1" stop-color="#050606"/></linearGradient>
<radialGradient id="glow" cx=".3" cy=".45" r=".7">
  <stop offset="0" stop-color="#151d1a" stop-opacity=".7"/>
  <stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<linearGradient id="fTop" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{MINT}"/>
  <stop offset=".55" stop-color="{GREEN}" stop-opacity=".35"/>
  <stop offset="1" stop-color="#0a1210" stop-opacity=".15"/></linearGradient>
<linearGradient id="fLeft" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{MINT}"/>
  <stop offset=".55" stop-color="{GREEN}" stop-opacity=".45"/>
  <stop offset="1" stop-color="{MINT}"/></linearGradient>
<linearGradient id="fRight" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#0a1210" stop-opacity=".15"/>
  <stop offset=".6" stop-color="{GREEN}" stop-opacity=".35"/>
  <stop offset="1" stop-color="{MINT}"/></linearGradient>
</defs>''')

add(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
add(f'<rect width="{W}" height="{H}" fill="url(#glow)"/>')

# ---- logo --------------------------------------------------------------
add(logo.mark(150, 472, 200, 212, uid="m1"))

CAP = 72
size = CAP / 0.720
tr = lib.fit_tracking(orb8, "NEXT PRO", size, 612)
d, _ = lib.text_path(orb8, "NEXT PRO", size, tracking=tr, x=384, y=616)
add(f'<path d="{d}" fill="#ffffff"/>')

# ---- linha de produtos -------------------------------------------------
CAP2 = 38
s2 = CAP2 / 0.720
items = ["NANO", "NANOBOX", "NANOMIX", "PRO-R"]
sep_gap, dot_r = 44.0, 7.0
x = 0.0
paths, dots = [], []
for i, t in enumerate(items):
    d, w = lib.text_path(orb7, t, s2, tracking=0.012, x=x, y=806)
    paths.append(d)
    x += w
    if i < len(items) - 1:
        dots.append((x + sep_gap + dot_r, 806 - CAP2 * 0.36))
        x += sep_gap * 2 + dot_r * 2
sx = 1030.0 / x
add(f'<g transform="translate(155,0) scale({sx:.4f},1)">'
    f'<path d="{" ".join(paths)}" fill="#ffffff"/>'
    + "".join(f'<circle cx="{cx_:.1f}" cy="{cy_:.1f}" r="{dot_r/sx:.2f}" fill="{GREEN}"/>'
              for cx_, cy_ in dots) + '</g>')

# ---- QR ----------------------------------------------------------------
QX, QY, QS = 1408, 366, 380
add(f'<rect x="{QX}" y="{QY}" width="{QS}" height="{QS}" fill="#ffffff"/>')
matrix = lib.qr_matrix(QR_URL, "M")
n = len(matrix)
mod = (QS - 2 * 38) / n
d, _ = lib.qr_path(matrix, QX + 38, QY + 38, mod)
add(f'<path d="{d}" fill="#000000" shape-rendering="crispEdges"/>')

# ---- chamada -----------------------------------------------------------
CAP3 = 40
s3 = CAP3 / 0.720
d, w = lib.text_path(orb7, "SIGA A NEXT PRO", s3, tracking=0.02, x=0, y=806)
sx3 = 508.0 / w
add(f'<g transform="translate({QX + QS/2 - 508/2:.1f},0) scale({sx3:.4f},1)">'
    f'<path d="{d}" fill="#ffffff"/></g>')

for i, ln in enumerate(("e conheça mais dos nossos", "produtos")):
    d, w = lib.text_path(inter4, ln, 33, tracking=0.0, x=0, y=856 + i * 44)
    add(f'<g transform="translate({QX + QS/2 - w/2:.1f},0)"><path d="{d}" fill="#b6bab8"/></g>')

d, w = lib.text_path(inter4, "@amplificadoresnextpro", 33, tracking=0.0, x=0, y=944)
add(f'<g transform="translate({QX + QS/2 - w/2:.1f},0)"><path d="{d}" fill="{GREEN}"/></g>')

# ---- frame -------------------------------------------------------------
B = 8
add(f'<rect x="0" y="0" width="{W}" height="{B}" fill="url(#fTop)"/>'
    f'<rect x="0" y="0" width="{B}" height="{H}" fill="url(#fLeft)"/>'
    f'<rect x="0" y="{H-B}" width="{W}" height="{B}" fill="{MINT}"/>'
    f'<rect x="{W-B}" y="0" width="{B}" height="{H}" fill="url(#fRight)"/>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}" role="img" aria-label="Next Pro — siga a Next Pro">'
       + "".join(P) + "</svg>")
import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
DEST = os.path.normpath(os.path.join(ROOT, "marca-next-pro-siga-qr.svg"))
open(DEST, "w").write(svg)
try:                     # pré-visualização PNG (opcional)
    import cairosvg
    cairosvg.svg2png(url=DEST, write_to="preview1.png", output_width=1000)
except ImportError:
    pass
print(DEST, len(svg), "bytes,", n, "módulos de QR")
