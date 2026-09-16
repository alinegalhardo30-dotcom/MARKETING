"""Helpers: font text -> SVG path outlines, 14-segment LCD glyphs, QR matrix."""
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Identity

import os
FONT_DIR = os.environ.get("NP_FONT_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts"))
_cache = {}

def load(name, **axes):
    key = (name, tuple(sorted(axes.items())))
    if key in _cache:
        return _cache[key]
    f = TTFont(f"{FONT_DIR}/{name}")
    if axes:
        f = instantiateVariableFont(f, axes, inplace=True, updateFontNames=False)
    _cache[key] = f
    return f

def text_path(font, text, size, tracking=0.0, x=0.0, y=0.0, weight_axis=None):
    """Return (path_d, advance_width). tracking in em units. y = baseline."""
    upem = font["head"].unitsPerEm
    scale = size / upem
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    kern = None
    pen_out = []
    cursor = 0.0
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            gname = cmap.get(ord(" "))
        adv = hmtx[gname][0]
        spen = SVGPathPen(gs, ntos=lambda v: f"{v:.3f}")
        tp = TransformPen(spen, (scale, 0, 0, -scale, x + cursor * scale, y))
        gs[gname].draw(tp)
        d = spen.getCommands()
        if d:
            pen_out.append(d)
        cursor += adv + tracking * upem
    cursor -= tracking * upem if text else 0
    return " ".join(pen_out), cursor * scale

def text_width(font, text, size, tracking=0.0):
    return text_path(font, text, size, tracking)[1]

# ---------------------------------------------------------------- 14-segment
# segment ids: a1 a2 (top), f j b (upper verticals), g1 g2 (middle),
#              e m c (lower verticals), d1 d2 (bottom), h k (upper diag), n l (lower diag)
SEG14 = {
    'A': "a1 a2 f b g1 g2 e c", 'B': "a1 a2 j b g2 m c d1 d2",
    'C': "a1 a2 f e d1 d2", 'D': "a1 a2 j b m c d1 d2",
    'E': "a1 a2 f e g1 g2 d1 d2", 'F': "a1 a2 f e g1",
    'G': "a1 a2 f e c d1 d2 g2", 'H': "f b e c g1 g2",
    'I': "a1 a2 j m d1 d2", 'J': "b c d1 d2 e",
    'K': "f e g1 k l", 'L': "f e d1 d2",
    'M': "f b e c h j", 'N': "f b e c h l",
    'O': "a1 a2 f b e c d1 d2", 'P': "a1 a2 f b e g1 g2",
    'Q': "a1 a2 f b e c d1 d2 l", 'R': "a1 a2 f b e g1 g2 l",
    'S': "a1 a2 f g1 g2 c d1 d2", 'T': "a1 a2 j m",
    'U': "f b e c d1 d2", 'V': "f e k n",
    'W': "f b e c n l", 'X': "h k n l",
    'Y': "h k m", 'Z': "a1 a2 k n d1 d2",
    '0': "a1 a2 f b e c d1 d2", '1': "b c",
    '2': "a1 a2 b g1 g2 e d1 d2", '3': "a1 a2 b g2 c d1 d2",
    '4': "f b g1 g2 c", '5': "a1 a2 f g1 g2 c d1 d2",
    '6': "a1 a2 f g1 g2 e c d1 d2", '7': "a1 a2 b c",
    '8': "a1 a2 f b g1 g2 e c d1 d2", '9': "a1 a2 f b g1 g2 c d1 d2",
    '-': "g1 g2", ' ': "", '.': "", '/': "k n",
}

def seg14_paths(ch, w, h, t, gap):
    """Polygons for one 14-segment character box (0,0)-(w,h)."""
    import math
    segs = SEG14.get(ch.upper(), "")
    if not segs:
        return []
    cx, cy = w / 2.0, h / 2.0
    g = gap
    ch_ = t * 0.34          # chamfer height at segment ends

    def horiz(x0, x1, ym):
        return [(x0 + t / 2, ym - t / 2), (x1 - t / 2, ym - t / 2),
                (x1, ym - ch_), (x1, ym + ch_),
                (x1 - t / 2, ym + t / 2), (x0 + t / 2, ym + t / 2),
                (x0, ym + ch_), (x0, ym - ch_)]

    def vert(y0, y1, xm):
        return [(xm - ch_, y0), (xm + ch_, y0), (xm + t / 2, y0 + t / 2),
                (xm + t / 2, y1 - t / 2), (xm + ch_, y1), (xm - ch_, y1),
                (xm - t / 2, y1 - t / 2), (xm - t / 2, y0 + t / 2)]

    def diag(p0, p1):
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dx, dy) or 1.0
        ux, uy = dx / L, dy / L
        px, py = -uy * t / 2, ux * t / 2
        return [(p0[0] + px + ux * t * .4, p0[1] + py + uy * t * .4),
                (p1[0] + px - ux * t * .4, p1[1] + py - uy * t * .4),
                (p1[0] - ux * t * .0, p1[1] - uy * t * .0),
                (p1[0] - px - ux * t * .4, p1[1] - py - uy * t * .4),
                (p0[0] - px + ux * t * .4, p0[1] - py + uy * t * .4),
                (p0[0] + ux * t * .0, p0[1] + uy * t * .0)]

    L, R, T, B = 0.0, w, 0.0, h
    geo = {
        'a1': horiz(L + g, cx - g, T + t / 2),
        'a2': horiz(cx + g, R - g, T + t / 2),
        'd1': horiz(L + g, cx - g, B - t / 2),
        'd2': horiz(cx + g, R - g, B - t / 2),
        'g1': horiz(L + g, cx - g, cy),
        'g2': horiz(cx + g, R - g, cy),
        'f':  vert(T + g, cy - g, L + t / 2),
        'e':  vert(cy + g, B - g, L + t / 2),
        'b':  vert(T + g, cy - g, R - t / 2),
        'c':  vert(cy + g, B - g, R - t / 2),
        'j':  vert(T + g, cy - g, cx),
        'm':  vert(cy + g, B - g, cx),
        'h':  diag((L + t * .95, T + t * .95), (cx - t * .70, cy - t * .70)),
        'k':  diag((R - t * .95, T + t * .95), (cx + t * .70, cy - t * .70)),
        'n':  diag((L + t * .95, B - t * .95), (cx - t * .70, cy + t * .70)),
        'l':  diag((R - t * .95, B - t * .95), (cx + t * .70, cy + t * .70)),
    }
    return [geo[s_] for s_ in segs.split()]


def seg14_text(text, size, box_w_ratio, tracking, x, y_top, thickness_ratio=0.16, gap_ratio=0.035):
    """Return path d for a 14-seg string. size = cap height. x,y_top = top-left."""
    h = size
    w = size * box_w_ratio
    t = size * thickness_ratio
    g = size * gap_ratio
    d = []
    cursor = x
    for ch in text:
        if ch != ' ':
            for poly in seg14_paths(ch, w, h, t, g):
                pts = " ".join(f"{cursor + px:.2f},{y_top + py:.2f}" for px, py in poly)
                d.append(f"M{pts}Z".replace(" ", " L", 1) if False else "M" + " L".join(
                    f"{cursor + px:.2f},{y_top + py:.2f}" for px, py in poly) + " Z")
        cursor += w + tracking
    return " ".join(d), cursor - tracking - x

def qr_matrix(data, error='M', border=0):
    import qrcode
    from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
    lvl = {'L': ERROR_CORRECT_L, 'M': ERROR_CORRECT_M, 'Q': ERROR_CORRECT_Q, 'H': ERROR_CORRECT_H}[error]
    q = qrcode.QRCode(version=None, error_correction=lvl, box_size=1, border=border)
    q.add_data(data)
    q.make(fit=True)
    return q.get_matrix()

def qr_path(matrix, x, y, module):
    d = []
    n = len(matrix)
    for r in range(n):
        c = 0
        while c < n:
            if matrix[r][c]:
                c2 = c
                while c2 + 1 < n and matrix[r][c2 + 1]:
                    c2 += 1
                d.append(f"M{x + c * module:.2f},{y + r * module:.2f}h{(c2 - c + 1) * module:.2f}v{module:.2f}h{-(c2 - c + 1) * module:.2f}Z")
                c = c2 + 1
            else:
                c += 1
    return " ".join(d), n

def fit_tracking(font, text, size, target_w):
    base = text_width(font, text, size, 0.0)
    n = max(len(text) - 1, 1)
    return (target_w - base) / n / size

def seg14_fit(text, size, box_w_ratio, target_w):
    n = len(text)
    return (target_w - n * size * box_w_ratio) / max(n - 1, 1)
