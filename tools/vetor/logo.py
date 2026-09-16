"""Next Pro logo mark: striped wing/leaf, pure vector geometry."""
import math

DEF = dict(
    top=(0.24, 0.0), bot=(0.12, 1.0),
    r1=(0.72, 0.05), r2=(1.0, 0.28), rmid=(1.0, 0.53),
    r3=(1.0, 0.80), r4=(0.62, 0.99),
    l1=(0.22, 0.70), l2=(0.33, 0.30),
    ang=68.0, nbands=8, tipmul=1.25, gapmul=0.30, start=-0.42, endf=1.0,
)

def outline(x, y, w, h, p=DEF):
    def P(u):
        return (x + u[0] * w, y + u[1] * h)
    T, B = P(p["top"]), P(p["bot"])
    c = {k: P(v) for k, v in p.items() if isinstance(v, tuple)}
    return (f"M{T[0]:.2f},{T[1]:.2f} "
            f"C{c['r1'][0]:.2f},{c['r1'][1]:.2f} {c['r2'][0]:.2f},{c['r2'][1]:.2f} "
            f"{c['rmid'][0]:.2f},{c['rmid'][1]:.2f} "
            f"C{c['r3'][0]:.2f},{c['r3'][1]:.2f} {c['r4'][0]:.2f},{c['r4'][1]:.2f} "
            f"{B[0]:.2f},{B[1]:.2f} "
            f"C{c['l1'][0]:.2f},{c['l1'][1]:.2f} {c['l2'][0]:.2f},{c['l2'][1]:.2f} "
            f"{T[0]:.2f},{T[1]:.2f} Z")

def mark(x, y, w, h, color="#ffffff", uid="lg", p=DEF):
    d = outline(x, y, w, h, p)
    ang = math.radians(p["ang"])
    ux, uy = math.cos(ang), -math.sin(ang)
    nx, ny = -uy, ux
    cx, cy = x + w * 0.5, y + h * 0.5
    span = (w + h) * 1.2
    n = p["nbands"]
    stripe = (w * (p["endf"] - p["start"])) / (n + p["tipmul"] - 1 + (n - 1) * p["gapmul"])
    bands, off, i = [], p["start"] * w, 0
    while off < p["endf"] * w and i < 40:
        th = stripe * (p["tipmul"] if i == 0 else 1.0)
        a, b = off, off + th
        p1 = (cx + nx * a - ux * span, cy + ny * a - uy * span)
        p2 = (cx + nx * a + ux * span, cy + ny * a + uy * span)
        p3 = (cx + nx * b + ux * span, cy + ny * b + uy * span)
        p4 = (cx + nx * b - ux * span, cy + ny * b - uy * span)
        bands.append(f"M{p1[0]:.2f},{p1[1]:.2f} L{p2[0]:.2f},{p2[1]:.2f} "
                     f"L{p3[0]:.2f},{p3[1]:.2f} L{p4[0]:.2f},{p4[1]:.2f} Z")
        off = b + stripe * p["gapmul"]
        i += 1
    return (f'<clipPath id="{uid}-clip"><path d="{d}"/></clipPath>'
            f'<g clip-path="url(#{uid}-clip)" fill="{color}">'
            f'<path d="{" ".join(bands)}"/></g>')
