# -*- coding: utf-8 -*-
"""Next Pro — card "Projetado e fabricado no Brasil" (vector rebuild)."""
import lib, logo

W, H = 1990, 1806
GREEN = "#19d898"
MINT = "#2fe3ae"

orb = lib.load("Orbitron-VF.ttf", wght=800)
inter4 = lib.load("Inter-VF.ttf", wght=400)
inter5 = lib.load("Inter-VF.ttf", wght=500)

P = []
add = P.append

add(f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0.35" y2="1">
  <stop offset="0" stop-color="#0c0e0d"/><stop offset=".5" stop-color="#090a0a"/>
  <stop offset="1" stop-color="#040505"/></linearGradient>
<radialGradient id="glow" cx=".47" cy=".42" r=".62">
  <stop offset="0" stop-color="#16201d" stop-opacity=".75"/>
  <stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<linearGradient id="ruleg" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>
  <stop offset=".5" stop-color="{GREEN}" stop-opacity=".85"/>
  <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>
<linearGradient id="fTop" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{MINT}"/>
  <stop offset=".5" stop-color="{GREEN}" stop-opacity=".62"/>
  <stop offset="1" stop-color="{MINT}"/></linearGradient>
<linearGradient id="fRight" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{MINT}"/>
  <stop offset=".55" stop-color="{GREEN}" stop-opacity=".5"/>
  <stop offset="1" stop-color="{MINT}"/></linearGradient>
<linearGradient id="fBottom" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{MINT}"/><stop offset=".5" stop-color="{MINT}"/>
  <stop offset="1" stop-color="{MINT}"/></linearGradient>
<linearGradient id="fLeft" x1="0" y1="1" x2="0" y2="0">
  <stop offset="0" stop-color="{MINT}"/>
  <stop offset=".5" stop-color="{GREEN}" stop-opacity=".62"/>
  <stop offset="1" stop-color="{MINT}"/></linearGradient>
</defs>''')

add(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
add(f'<rect width="{W}" height="{H}" fill="url(#glow)"/>')

# ---- faint instrument-cluster texture ---------------------------------
tex = ['<g opacity=".028">']
CLUSTERS = (
    (505, 690, ("TEMP", "FUEL", "OIL")),
    (1035, 660, ("0", "12", "24", "36")),
    (1560, 700, ("dB", "PFC", "AC")),
)
for gx, gy, labels in CLUSTERS:
    tex.append(f'<g fill="none" stroke="#bdf2df" stroke-width="3">'
               f'<circle cx="{gx}" cy="{gy}" r="132"/>'
               f'<circle cx="{gx}" cy="{gy}" r="112" stroke-dasharray="3 24"/>'
               f'<path d="M{gx-52},{gy+52} L{gx+38},{gy-50}" stroke-width="6"/></g>')
    for i, lbl in enumerate(labels):
        d, _ = lib.text_path(inter4, lbl, 26, tracking=0.05,
                             x=gx - 250, y=gy - 60 + i * 46)
        tex.append(f'<path d="{d}" fill="#bdf2df"/>')
tex.append('</g>')
add("".join(tex))

# ---- logo --------------------------------------------------------------
add(logo.mark(228, 590, 368, 360, uid="m2"))

CAP = 135
size = CAP / 0.720
tr = lib.fit_tracking(orb, "NEXT PRO", size, 1080)
d, wpx = lib.text_path(orb, "NEXT PRO", size, tracking=tr, x=668, y=868)
add(f'<path d="{d}" fill="#ffffff"/>')

# ---- hairline ----------------------------------------------------------
add('<rect x="518" y="1071" width="954" height="3" fill="url(#ruleg)"/>')

# ---- segmented headline ------------------------------------------------
TXT = "PROJETADO E FABRICADO NO BRASIL"
SEG, RATIO = 62, 0.62
trk = lib.seg14_fit(TXT, SEG, RATIO, 1476)
d, wpx = lib.seg14_text(TXT, SEG, RATIO, trk, 256, 1150,
                        thickness_ratio=0.135, gap_ratio=0.018)
add(f'<path d="{d}" fill="{GREEN}"/>')

# ---- tagline -----------------------------------------------------------
TAG = "TECNOLOGIA EM ÁUDIO QUE IMPULSIONA O SEU PROJETO"
tsize = 31
trk = lib.fit_tracking(inter5, TAG, tsize, 1414)
d, wpx = lib.text_path(inter5, TAG, tsize, tracking=trk, x=288, y=1536)
add(f'<path d="{d}" fill="#8c918f"/>')

# ---- frame -------------------------------------------------------------
B = 9
add(f'<rect x="0" y="0" width="{W}" height="{B}" fill="url(#fTop)"/>'
    f'<rect x="{W-B}" y="0" width="{B}" height="{H}" fill="url(#fRight)"/>'
    f'<rect x="0" y="{H-B}" width="{W}" height="{B}" fill="url(#fBottom)"/>'
    f'<rect x="0" y="0" width="{B}" height="{H}" fill="url(#fLeft)"/>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}" role="img" aria-label="Next Pro — projetado e '
       f'fabricado no Brasil">' + "".join(P) + "</svg>")
import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
DEST = os.path.normpath(os.path.join(ROOT, "marca-next-pro-projetado-fabricado-brasil.svg"))
open(DEST, "w").write(svg)
try:                     # pré-visualização PNG (opcional)
    import cairosvg
    cairosvg.svg2png(url=DEST, write_to="preview2.png", output_width=1000)
except ImportError:
    pass
print(DEST, len(svg), "bytes")
