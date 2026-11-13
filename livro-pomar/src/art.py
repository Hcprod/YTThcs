"""Biblioteca de desenhos vetoriais (SVG) do livro "O Pomar da Serra Dourada".

Todos os personagens sao desenhados do zero com formas geometricas simples.
Cada funcao de personagem devolve um <g> SVG posicionado em (x, y) = centro
do corpo, na escala s. O modo 'line' gera arte de colorir (traco preto,
preenchimento branco); o modo 'color' gera a versao colorida (capa).
"""
import math

# ---------------------------------------------------------------- paleta ----
PAL = {
    'pitanga': '#e8392f', 'pitanga2': '#c92a22',
    'leaf': '#5fb84a', 'leaf2': '#3f8f32', 'leafl': '#9fd66b',
    'caju': '#ffb12b', 'nut': '#a8774a', 'straw': '#f3d27a', 'straw2': '#d9ad48',
    'vine': '#7a9b3a', 'wood': '#a86b3c', 'wood2': '#7b4a26',
    'jabuti': '#4a2a5e', 'jabuti2': '#6e4489', 'paper': '#e9d39a',
    'jaca': '#b9c94a', 'jaca2': '#9aab33', 'glass': '#dff3ff', 'shawl': '#f28fb0',
    'manga': '#ffc531', 'mangar': '#ff8a5b', 'apron': '#ffffff', 'check': '#e5534b',
    'pinhao': '#8a5530', 'shirt': '#ffffff', 'bow': '#d33b4a', 'gold': '#f2c230',
    'caram': '#f6e04a', 'caram2': '#d8bd1d', 'patch': '#7fc8e8',
    'cheek': '#ff9cab', 'mouth': '#d8434f', 'tongue': '#ff8c9a', 'white': '#ffffff',
    'shoe': '#6b4a3a', 'wind': '#d6f0ff', 'cap': '#e8392f',
    'lily': '#5fb84a', 'petal': '#ffd1e0', 'petal2': '#ff9fc2', 'mer': '#c9f0d0',
    'bark': '#8a5a3a', 'flame': '#ff8c2b', 'flame2': '#ffd23f',
    'sky': '#bfe8ff', 'grass': '#8fd16a', 'hill': '#f4c94a', 'hill2': '#e9a93a',
    'water': '#7fd0f0', 'rock': '#b8b0a8', 'cave': '#8d8178', 'cauldron': '#4b4b55',
    'pot': '#c0c4cc', 'smoke1': '#b88cff', 'smoke2': '#7fe3c0', 'smoke3': '#ffb3d9',
    'sun': '#ffd23f', 'cloud': '#ffffff', 'table': '#c98a52', 'flower': '#ff6fa3',
    'flowerc': '#ffd23f', 'trunk': '#9a6a42', 'canopy': '#5fb84a', 'orange': '#ff9a1f',
    'red': '#e8392f', 'blue': '#4aa3e8', 'purple': '#9a6ad8', 'yellow': '#ffd23f',
}

_uid = [0]


def uid(prefix='c'):
    _uid[0] += 1
    return f'{prefix}{_uid[0]}'


def f(v):
    return f'{v:.1f}'


def catmull(pts, closed=False):
    """Curva suave (Catmull-Rom -> Bezier) passando pelos pontos."""
    if closed:
        p = [pts[-1]] + pts + [pts[0], pts[1]]
    else:
        p = [pts[0]] + pts + [pts[-1]]
    d = f'M {f(p[1][0])} {f(p[1][1])} '
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f'C {f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])} '
    if closed:
        d += 'Z'
    return d


def polar_shape(cx, cy, rx, ry, rfun, n=180, rot=0.0):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        r = rfun(t)
        a = t + rot
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    d = 'M ' + ' L '.join(f'{f(x)} {f(y)}' for x, y in pts) + ' Z'
    return d


def rounded_star(cx, cy, R, r, n=5, rot=-math.pi / 2):
    verts = []
    for i in range(2 * n):
        rad = R if i % 2 == 0 else r
        a = rot + math.pi * i / n
        verts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    mids = [((verts[i][0] + verts[(i + 1) % len(verts)][0]) / 2,
             (verts[i][1] + verts[(i + 1) % len(verts)][1]) / 2) for i in range(len(verts))]
    d = f'M {f(mids[-1][0])} {f(mids[-1][1])} '
    for i in range(len(verts)):
        d += f'Q {f(verts[i][0])} {f(verts[i][1])} {f(mids[i][0])} {f(mids[i][1])} '
    return d + 'Z', verts


class G:
    """Acumulador de SVG em coordenadas locais de um personagem."""

    def __init__(self, mode='line', sw=6.0):
        self.mode = mode
        self.sw = sw
        self.out = []

    def col(self, key):
        if key is None:
            return 'none'
        if key == 'black':
            return '#000'
        if self.mode == 'line':
            return '#fff'
        return PAL.get(key, key)

    def raw(self, s):
        self.out.append(s)

    def path(self, d, key='white', w=1.0, extra=''):
        self.out.append(
            f'<path d="{d}" fill="{self.col(key)}" stroke="#000" stroke-width="{f(self.sw * w)}" '
            f'stroke-linejoin="round" stroke-linecap="round" {extra}/>')

    def line(self, d, w=1.0):
        self.path(d, None, w)

    def circle(self, x, y, r, key='white', w=1.0):
        self.out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{self.col(key)}" '
                        f'stroke="#000" stroke-width="{f(self.sw * w)}"/>')

    def ellipse(self, x, y, rx, ry, key='white', w=1.0, rot=0):
        tr = f' transform="rotate({rot} {f(x)} {f(y)})"' if rot else ''
        self.out.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(rx)}" ry="{f(ry)}" '
                        f'fill="{self.col(key)}" stroke="#000" stroke-width="{f(self.sw * w)}"{tr}/>')

    def dot(self, x, y, r):
        self.out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="#000"/>')

    def tube(self, pts, thick, key='white', w=1.0):
        """Membro com contorno (braco/perna) que continua pintavel por dentro."""
        d = catmull(pts) if len(pts) > 2 else f'M {f(pts[0][0])} {f(pts[0][1])} L {f(pts[1][0])} {f(pts[1][1])}'
        self.out.append(f'<path d="{d}" fill="none" stroke="#000" stroke-width="{f(thick + 2 * self.sw * w)}" '
                        f'stroke-linecap="round" stroke-linejoin="round"/>')
        self.out.append(f'<path d="{d}" fill="none" stroke="{self.col(key)}" stroke-width="{f(thick)}" '
                        f'stroke-linecap="round" stroke-linejoin="round"/>')

    def clip_begin(self, d):
        cid = uid('clip')
        self.out.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">')

    def clip_end(self):
        self.out.append('</g>')

    def svg(self):
        return ''.join(self.out)


def place(g, x, y, s, flip=False, rot=0):
    sx = -s if flip else s
    r = f' rotate({rot})' if rot else ''
    return f'<g transform="translate({f(x)} {f(y)}){r} scale({sx:.3f} {s:.3f})">{g.svg()}</g>'


def mk(mode, s, W):
    return G(mode, W / s)


# ------------------------------------------------------------ rostos -------
def eye(g, x, y, rx, ry):
    g.ellipse(x, y, rx, ry, 'black', 0)
    g.out.append(f'<circle cx="{f(x - rx * 0.32)}" cy="{f(y - ry * 0.38)}" r="{f(rx * 0.42)}" fill="#fff"/>')
    g.out.append(f'<circle cx="{f(x + rx * 0.35)}" cy="{f(y + ry * 0.35)}" r="{f(rx * 0.18)}" fill="#fff"/>')


def face(g, cx, cy, ex=34, er=13, expr='happy', my=26, cheeks=True, mw=16):
    """ex: meia distancia entre olhos; er: raio do olho; my: distancia ate a boca."""
    sw = 0.8
    if expr in ('happy', 'open', 'surprised', 'talk'):
        for sx in (-1, 1):
            eye(g, cx + sx * ex, cy, er, er * 1.2)
    elif expr in ('joy', 'laugh'):
        for sx in (-1, 1):
            g.line(f'M {f(cx + sx * ex - er)} {f(cy + 3)} Q {f(cx + sx * ex)} {f(cy - er * 1.3)} {f(cx + sx * ex + er)} {f(cy + 3)}', sw)
    elif expr in ('wise', 'sing'):
        for sx in (-1, 1):
            g.line(f'M {f(cx + sx * ex - er)} {f(cy - 2)} Q {f(cx + sx * ex)} {f(cy + er * 1.1)} {f(cx + sx * ex + er)} {f(cy - 2)}', sw)
    elif expr == 'grumpy':
        for sx in (-1, 1):
            x = cx + sx * ex
            # olho meio fechado (metade de baixo)
            g.path(f'M {f(x - er)} {f(cy - 2)} A {f(er)} {f(er * 1.1)} 0 0 0 {f(x + er)} {f(cy - 2)} Z', 'black', 0.5)
            g.out.append(f'<circle cx="{f(x - er * 0.3)}" cy="{f(cy + er * 0.25)}" r="{f(er * 0.3)}" fill="#fff"/>')
            # sobrancelha brava
            g.line(f'M {f(x - sx * er * 1.3)} {f(cy - er * 1.9)} L {f(x + sx * er * 1.1)} {f(cy - er * 0.9)}', 1.0)
    # sobrancelhas de surpresa
    if expr == 'surprised':
        for sx in (-1, 1):
            g.line(f'M {f(cx + sx * ex - er * 0.8)} {f(cy - er * 2.1)} Q {f(cx + sx * ex)} {f(cy - er * 2.7)} {f(cx + sx * ex + er * 0.8)} {f(cy - er * 2.1)}', 0.7)
    my_ = cy + my
    if expr in ('happy', 'wise'):
        g.line(f'M {f(cx - mw)} {f(my_)} Q {f(cx)} {f(my_ + mw * 0.9)} {f(cx + mw)} {f(my_)}', sw)
    elif expr in ('open', 'joy', 'laugh', 'talk'):
        h = mw * (1.3 if expr != 'talk' else 0.9)
        d = f'M {f(cx - mw)} {f(my_)} Q {f(cx)} {f(my_ + h * 1.6)} {f(cx + mw)} {f(my_)} Z'
        g.path(d, 'mouth', sw)
        g.path(f'M {f(cx - mw * 0.45)} {f(my_ + h * 0.62)} Q {f(cx)} {f(my_ + h * 0.3)} {f(cx + mw * 0.45)} {f(my_ + h * 0.62)} Q {f(cx)} {f(my_ + h * 0.85)} {f(cx - mw * 0.45)} {f(my_ + h * 0.62)} Z', 'tongue', 0.5)
    elif expr in ('surprised', 'sing'):
        g.ellipse(cx, my_ + 4, mw * 0.5, mw * 0.65, 'mouth', sw)
    elif expr == 'grumpy':
        g.line(f'M {f(cx - mw)} {f(my_ + 6)} Q {f(cx - mw / 2)} {f(my_ - 2)} {f(cx)} {f(my_ + 4)} Q {f(cx + mw / 2)} {f(my_ + 10)} {f(cx + mw)} {f(my_ + 1)}', sw)
    if cheeks:
        for sx in (-1, 1):
            g.ellipse(cx + sx * (ex + er * 1.6), cy + my * 0.62, er * 0.95, er * 0.55, 'cheek', 0.55)


def leaf_d(x, y, length, width, ang):
    """Folha pontuda saindo de (x,y) na direcao ang (graus)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    tx, ty = x + ux * length, y + uy * length
    c1 = (x + ux * length * 0.4 + px * width, y + uy * length * 0.4 + py * width)
    c2 = (x + ux * length * 0.4 - px * width, y + uy * length * 0.4 - py * width)
    d = (f'M {f(x)} {f(y)} Q {f(c1[0])} {f(c1[1])} {f(tx)} {f(ty)} '
         f'Q {f(c2[0])} {f(c2[1])} {f(x)} {f(y)} Z')
    vein = f'M {f(x + ux * length * 0.12)} {f(y + uy * length * 0.12)} L {f(x + ux * length * 0.75)} {f(y + uy * length * 0.75)}'
    return d, vein


def leaf(g, x, y, length, width, ang, key='leaf', w=1.0, vein=True):
    d, v = leaf_d(x, y, length, width, ang)
    g.path(d, key, w)
    if vein:
        g.line(v, w * 0.6)


def feet(g, xs=(-38, 38), top=95, bottom=142, key='shoe', thick=20, turn=None):
    for i, x in enumerate(xs):
        sx = -1 if x < 0 else 1
        g.tube([(x, top), (x + sx * 3, bottom - 8)], thick, 'skin')
        dirx = sx if turn is None else turn
        g.ellipse(x + dirx * 12, bottom, 25, 13, key)


def arms(g, left, right, thick=17, key='skin', hand_r=13):
    for pts in (left, right):
        g.tube(pts, thick, key)
        hx, hy = pts[-1]
        g.circle(hx, hy, hand_r, key)


# membros usam a cor 'skin' -> definimos em PAL como tom claro neutro
PAL['skin'] = '#fff4e0'


# ===================================================== PERSONAGENS ==========
def pitanga(x, y, s=1.0, mode='line', expr='happy', W=6.5, flip=False, pose='wave'):
    g = mk(mode, s, W)
    # bracos atras do corpo
    if pose == 'wave':
        arms(g, [(-95, 20), (-130, 40), (-148, 75)], [(95, 5), (130, -30), (140, -75)])
    elif pose == 'run':
        arms(g, [(-95, 20), (-135, 0), (-160, -25)], [(95, 20), (125, 55), (150, 60)])
    else:
        arms(g, [(-95, 20), (-125, 55), (-130, 85)], [(95, 20), (125, 55), (130, 85)])
    feet(g, (-38, 38), 85, 138, 'shoe')
    body = polar_shape(0, 0, 115, 95, lambda t: 1 + 0.045 * math.cos(8 * t), 200)
    g.path(body, 'pitanga')
    # gomos: curvas curtas saindo do topo e da base
    for sx in (-1, 1):
        g.line(f'M {sx * 10} -86 Q {sx * 48} -76 {sx * 70} -48', 0.75)
        g.line(f'M {sx * 6} -90 Q {sx * 22} -70 {sx * 26} -52', 0.6)
        g.line(f'M {sx * 10} 86 Q {sx * 52} 80 {sx * 76} 52', 0.75)
    # coroinha (sepalas) na base
    # laco de folha no topo
    leaf(g, 0, -92, 62, 22, -150, 'leaf')
    leaf(g, 0, -92, 62, 22, -30, 'leaf')
    g.circle(0, -92, 11, 'leaf2')
    face(g, 0, 5, ex=36, er=14, expr=expr, my=28, mw=17)
    return place(g, x, y, s, flip)


def caju(x, y, s=1.0, mode='line', expr='happy', W=6.5, flip=False, pose='stand'):
    g = mk(mode, s, W)
    if pose == 'point':
        arms(g, [(-85, 0), (-118, 35), (-125, 72)], [(85, -10), (130, -35), (165, -50)])
    elif pose == 'run':
        arms(g, [(-85, 0), (-125, -20), (-150, -45)], [(85, 10), (115, 45), (140, 50)])
    else:
        arms(g, [(-85, 0), (-118, 35), (-125, 72)], [(85, 0), (118, 35), (125, 72)])
    feet(g, (-34, 34), 92, 142, 'shoe')
    body = ('M -92 -58 C -98 -122 98 -122 92 -58 C 88 20 72 100 0 104 '
            'C -72 100 -88 20 -92 -58 Z')
    g.path(body, 'caju')
    # pontinhos da casca
    for (px, py) in [(-60, -70), (62, -62), (-66, 40), (60, 50), (-30, 80), (34, 86)]:
        g.dot(px, py, 2.6)
    # cinto de cipo
    belt = 'M -88 34 Q 0 58 88 34 L 84 52 Q 0 76 -84 52 Z'
    g.path(belt, 'vine', 0.9)
    for bx in (-60, -30, 0, 30, 60):
        yy = 44 + 10 * (1 - (bx / 88) ** 2)
        g.line(f'M {bx - 6} {f(yy - 8)} Q {bx} {f(yy)} {bx + 6} {f(yy + 8)}', 0.55)
    # estilingue preso ao cinto (lado direito)
    g.tube([(62, 58), (66, 96)], 9, 'wood')
    g.tube([(66, 96), (54, 122)], 8, 'wood')
    g.tube([(66, 96), (84, 120)], 8, 'wood')
    g.line('M 54 122 Q 69 136 84 120', 0.6)
    # chapeu de palha (inclinado para tras)
    g.raw('<g transform="rotate(-14 -18 -104)">')
    g.path('M -60 -112 Q -58 -168 -16 -170 Q 28 -168 26 -112 Z', 'straw')
    g.path('M -58 -124 Q -18 -116 24 -124 L 25 -112 Q -18 -104 -59 -112 Z', 'straw2', 0.8)
    for hx in (-46, -32, -18, -4, 10):
        g.line(f'M {hx} -165 L {hx + 4} -128', 0.45)
    g.ellipse(-18, -108, 92, 20, 'straw')
    g.line('M -96 -108 Q -18 -96 60 -108', 0.45)
    g.raw('</g>')
    # castanha = topete (sobre a aba)
    nut = ('M -12 -100 C -24 -150 26 -178 62 -160 C 84 -148 76 -122 56 -124 '
           'C 38 -126 34 -112 30 -98 Q 10 -92 -12 -100 Z')
    g.path(nut, 'nut')
    g.line('M 4 -112 Q 18 -146 52 -150', 0.55)
    face(g, 0, -28, ex=32, er=13, expr=expr, my=28, mw=16)
    return place(g, x, y, s, flip)


def jabuticaba(x, y, s=1.0, mode='line', expr='happy', W=6.5, flip=False, notebook=True):
    g = mk(mode, s, W)
    if not notebook:
        arms(g, [(-88, 20), (-118, 50), (-122, 82)], [(88, 20), (118, 50), (122, 82)])
    feet(g, (-34, 34), 88, 140, 'shoe')
    g.circle(0, 0, 98, 'jabuti')
    # brilho
    g.ellipse(-56, -50, 11, 22, 'jabuti2', 0.55, rot=40)
    # coroinha (calice) no topo
    cal, _ = rounded_star(0, -100, 20, 8, 4, -math.pi / 2)
    g.path(cal, 'leaf2', 0.8)
    g.tube([(0, -108), (6, -126)], 7, 'wood')
    leaf(g, 6, -122, 40, 14, -40, 'leaf', 0.8)
    face(g, 0, -10, ex=34, er=15, expr=expr, my=30, mw=15)
    # cilios
    for sx in (-1, 1):
        ex = sx * 34
        g.line(f'M {ex + sx * 12} -24 L {ex + sx * 20} -31', 0.55)
        g.line(f'M {ex + sx * 15} -16 L {ex + sx * 24} -19', 0.55)
    if notebook:
        # caderno de folhas secas segurado na frente
        g.raw('<g transform="rotate(-8 30 62)">')
        g.path('M -14 34 L 70 30 Q 76 62 72 96 L -10 100 Q -16 66 -14 34 Z', 'paper', 0.9)
        g.line('M -14 34 Q 4 62 -10 100', 0.5)
        for ly in (48, 62, 76):
            g.line(f'M 8 {ly} Q 34 {ly - 4} 60 {ly}', 0.45)
        leaf(g, 46, 86, 22, 8, -20, 'leaf', 0.5, vein=False)
        g.raw('</g>')
        # lapis de graveto na outra mao
        arms(g, [(-88, 20), (-90, 60), (-24, 70)], [(88, 20), (100, 60), (74, 72)])
        g.tube([(-30, 62), (-60, 30)], 8, 'wood', 0.8)
    return place(g, x, y, s, flip)


def jaca(x, y, s=1.0, mode='line', expr='wise', W=6.5, flip=False, book=False):
    g = mk(mode, s, W)
    arms(g, [(-118, 30), (-150, 70), (-150, 106)], [(118, 30), (150, 70), (150, 106)], 19)
    feet(g, (-48, 48), 120, 172, 'shoe', 24)
    body = polar_shape(0, 0, 128, 150, lambda t: 1 + 0.018 * math.cos(22 * t), 260)
    g.path(body, 'jaca')
    # gomos suaves (calombinhos arredondados)
    bumps = [(-70, -100), (-30, -122), (14, -126), (56, -108), (-98, -56), (96, -60),
             (-108, 4), (110, 0), (-96, 64), (98, 64), (-60, 116), (62, 116), (0, 134)]
    for bx, by in bumps:
        g.line(f'M {bx - 9} {by + 4} Q {bx} {by - 8} {bx + 9} {by + 4}', 0.55)
    # cabinho
    g.tube([(0, -150), (-4, -170)], 12, 'wood')
    # oculos redondos
    for sx in (-1, 1):
        g.circle(sx * 42, -40, 30, 'glass', 0.8)
    g.line('M -12 -42 Q 0 -50 12 -42', 0.8)
    g.line('M -72 -44 L -100 -52', 0.7)
    g.line('M 72 -44 L 100 -52', 0.7)
    face(g, 0, -40, ex=42, er=12, expr=expr, my=40, mw=20)
    # xale de croche
    shawl = 'M -126 6 Q 0 50 126 6 Q 104 74 0 132 Q -104 74 -126 6 Z'
    g.path(shawl, 'shawl', 0.95)
    # recortes de croche: fileiras de buraquinhos
    for row, (yy, n, spread) in enumerate([(40, 7, 96), (66, 5, 66), (92, 3, 38)]):
        for i in range(n):
            px = -spread + 2 * spread * i / (n - 1)
            py = yy + 14 * (1 - (px / 126) ** 2) * (1 if row == 0 else 0.5)
            g.circle(px, py, 6.5, 'white', 0.5)
    # borda em escamas
    sc = 'M -126 6 '
    for i in range(1, 9):
        t = i / 8
        px = -126 + 126 * t
        py = 6 + 126 * t
        sc += f'Q {f(px - 18)} {f(py + 4)} {f(px)} {f(py)} '
    g.line(sc, 0.5)
    sc = 'M 126 6 '
    for i in range(1, 9):
        t = i / 8
        px = 126 - 126 * t
        py = 6 + 126 * t
        sc += f'Q {f(px + 18)} {f(py + 4)} {f(px)} {f(py)} '
    g.line(sc, 0.5)
    # pompom na ponta
    g.circle(0, 144, 12, 'shawl', 0.8)
    if book:
        g.path('M -70 96 L 0 112 L 70 96 L 70 140 L 0 156 L -70 140 Z', 'paper', 0.9)
        g.line('M 0 112 L 0 156', 0.6)
        for yy in (110, 124):
            g.line(f'M -56 {yy} L -14 {yy + 8}', 0.4)
            g.line(f'M 14 {yy + 8} L 56 {yy}', 0.4)
        g.circle(-74, 112, 15, 'skin')
        g.circle(74, 112, 15, 'skin')
    return place(g, x, y, s, flip)


def manga(x, y, s=1.0, mode='line', expr='happy', W=6.5, flip=False, spoon=True):
    g = mk(mode, s, W)
    arms(g, [(-100, 0), (-132, 36), (-138, 74)], [(98, -6), (130, -32), (142, -66)])
    feet(g, (-36, 36), 108, 158, 'shoe')
    body = ('M 4 -128 C 84 -130 118 -46 108 34 C 100 112 34 132 -14 126 '
            'C -84 118 -112 44 -100 -24 C -90 -84 -54 -126 4 -128 Z')
    g.path(body, 'manga')
    # rubor rosado da manga (area pintavel)
    g.path('M 60 -96 Q 96 -60 100 -10 Q 76 -20 64 -50 Q 52 -76 60 -96 Z', 'mangar', 0.5)
    # cabinho e folha
    g.tube([(6, -128), (12, -150)], 9, 'wood')
    leaf(g, 12, -146, 58, 18, -20, 'leaf')
    # avental xadrez
    apron = ('M -46 -6 L 46 -6 L 46 30 Q 82 34 86 62 Q 82 112 4 122 '
             'Q -76 116 -86 62 Q -82 34 -46 30 Z')
    g.path(apron, 'apron', 0.9)
    g.clip_begin(apron)
    step = 22
    if mode == 'color':
        for ix in range(-5, 5):
            for iy in range(0, 7):
                if (ix + iy) % 2 == 0:
                    g.raw(f'<rect x="{ix * step}" y="{-6 + iy * step}" width="{step}" height="{step}" fill="{PAL["check"]}" opacity="0.55"/>')
    for gx in range(-88, 90, step):
        g.line(f'M {gx} -10 L {gx} 130', 0.45)
    for gy in range(-6, 130, step):
        g.line(f'M -90 {gy} L 90 {gy}', 0.45)
    g.clip_end()
    g.path(apron, None, 0.9)
    g.line('M -46 -6 Q -50 -40 -30 -70', 0.6)
    g.line('M 46 -6 Q 50 -40 30 -70', 0.6)
    # bolso
    g.path('M -20 60 L 24 60 L 22 90 Q 2 96 -18 90 Z', 'apron', 0.6)
    face(g, 0, -60, ex=34, er=14, expr=expr, my=28, mw=17)
    if spoon:
        g.raw('<g transform="rotate(-20 142 -66)">')
        g.tube([(142, -40), (142, -110)], 10, 'wood', 0.9)
        g.ellipse(142, -130, 18, 26, 'wood', 0.9)
        g.ellipse(142, -128, 9, 14, 'wood2', 0.5)
        g.raw('</g>')
        g.circle(142, -66, 13, 'skin')
    return place(g, x, y, s, flip)


def pinhao(x, y, s=1.0, mode='line', expr='happy', W=6.5, flip=False, prop='book'):
    g = mk(mode, s, W)
    # abas do fraque (atras)
    g.path('M -60 70 Q -92 130 -84 168 Q -60 150 -40 110 Z', 'pinhao', 0.9)
    g.path('M 60 70 Q 92 130 84 168 Q 60 150 40 110 Z', 'pinhao', 0.9)
    if prop == 'magnifier':
        arms(g, [(-66, 10), (-96, 50), (-100, 92)], [(66, 0), (110, -10), (138, -40)], 14)
    else:
        arms(g, [(-66, 10), (-96, 50), (-100, 92)], [(66, 10), (84, 50), (52, 74)], 14)
    feet(g, (-26, 26), 112, 178, 'shoe', 15)
    body = ('M 0 -176 C 48 -128 74 -30 70 52 C 66 128 -66 128 -70 52 '
            'C -74 -30 -48 -128 0 -176 Z')
    g.path(body, 'pinhao')
    # ponta mais escura
    g.path('M 0 -176 C 14 -162 22 -148 26 -136 Q 0 -128 -26 -136 C -22 -148 -14 -162 0 -176 Z', 'wood2', 0.7)
    # camisa (peitilho) e lapelas
    g.path('M -30 -14 L 30 -14 L 0 70 Z', 'shirt', 0.8)
    g.line('M -30 -14 L -48 20 L -10 40', 0.6)
    g.line('M 30 -14 L 48 20 L 10 40', 0.6)
    # gravata borboleta
    g.path('M 0 -10 L -24 -22 L -24 2 Z', 'bow', 0.7)
    g.path('M 0 -10 L 24 -22 L 24 2 Z', 'bow', 0.7)
    g.circle(0, -10, 6, 'bow', 0.7)
    for by in (16, 36):
        g.circle(0, by, 3.8, 'white', 0.5)
    for bx, by in ((-34, 66), (34, 66)):
        g.circle(bx, by, 5, 'gold', 0.5)
    face(g, 0, -72, ex=24, er=11, expr=expr, my=26, mw=13, cheeks=True)
    # monoculo no olho direito
    g.circle(24, -72, 20, None, 0.8)
    g.line('M 42 -64 Q 60 -30 50 0', 0.45)
    # bigodinho
    g.line('M -12 -52 Q -4 -46 0 -50 Q 4 -46 12 -52', 0.6)
    if prop == 'book':
        g.raw('<g transform="rotate(-10 70 70)">')
        g.path('M 40 30 L 108 26 L 112 104 L 44 108 Z', 'bow', 0.9)
        g.path('M 44 108 L 112 104 L 112 114 L 46 118 Z', 'paper', 0.6)
        g.path('M 58 48 L 96 46 L 97 66 L 59 68 Z', 'white', 0.5)
        g.line('M 52 30 L 54 108', 0.5)
        g.raw('</g>')
        g.circle(52, 74, 11, 'skin')
    elif prop == 'magnifier':
        g.tube([(138, -40), (152, -64)], 8, 'wood', 0.8)
        g.circle(166, -92, 26, 'glass', 0.9)
        g.circle(138, -40, 11, 'skin')
    return place(g, x, y, s, flip)


def carambola(x, y, s=1.0, mode='line', expr='grumpy', W=6.5, flip=False, ladle=False):
    g = mk(mode, s, W)
    d, verts = rounded_star(0, 0, 135, 82, 5)
    # pernas a partir das pontas de baixo
    lb, rb = verts[6], verts[4]
    g.tube([(lb[0] * 0.75, lb[1] * 0.75), (lb[0] * 0.8, lb[1] + 30)], 17, 'skin')
    g.tube([(rb[0] * 0.75, rb[1] * 0.75), (rb[0] * 0.8, rb[1] + 30)], 17, 'skin')
    g.ellipse(lb[0] * 0.8 - 12, lb[1] + 40, 26, 13, 'shoe')
    g.ellipse(rb[0] * 0.8 + 12, rb[1] + 40, 26, 13, 'shoe')
    lh, rh = verts[8], verts[2]
    g.circle(lh[0] - 6, lh[1] + 4, 18, 'skin')
    g.circle(rh[0] + 6, rh[1] + 4, 18, 'skin')
    g.path(d, 'caram')
    # nervuras perto das pontas
    for i in range(0, 10, 2):
        vx, vy = verts[i]
        g.line(f'M {f(vx * 0.62)} {f(vy * 0.62)} L {f(vx * 0.84)} {f(vy * 0.84)}', 0.55)
    # cabinho torto na ponta de cima
    g.tube([(0, -128), (10, -150), (2, -164)], 8, 'wood')
    # remendo engracado
    g.raw('<g transform="rotate(12 -40 50)">')
    g.path('M -58 34 L -22 34 L -22 66 L -58 66 Z', 'patch', 0.6)
    for t in range(-54, -24, 8):
        g.line(f'M {t} 30 L {t + 2} 38', 0.4)
        g.line(f'M {t} 62 L {t + 2} 70', 0.4)
    g.raw('</g>')
    face(g, 0, -6, ex=30, er=13, expr=expr, my=30, mw=17)
    if ladle:
        g.tube([(rh[0] + 16, rh[1] + 4), (rh[0] + 42, rh[1] + 90)], 9, 'wood', 0.9)
        g.path(f'M {f(rh[0] + 24)} {f(rh[1] + 92)} Q {f(rh[0] + 44)} {f(rh[1] + 120)} {f(rh[0] + 66)} {f(rh[1] + 90)} Z', 'wood', 0.9)
        g.circle(rh[0] + 16, rh[1] + 4, 17, 'skin')
    return place(g, x, y, s, flip)


# ================================================ FOLCLORE (ADAPTADO) ======
def redemoinho(x, y, s=1.0, mode='line', W=6.5, flip=False, expr='joy'):
    """Redemoinho brincalhao (inspirado na lenda do Saci) - folhas e vento."""
    g = mk(mode, s, W)
    # rajadas de vento (bracinhos) com ponta enrolada
    g.line('M -96 -20 Q -150 -30 -176 -70 Q -190 -96 -166 -100 Q -146 -100 -156 -80', 0.9)
    g.line('M 96 -20 Q 150 -24 172 -60 Q 184 -84 162 -88 Q 144 -86 154 -68', 0.9)
    # funil (silhueta ondulada)
    pts = [(-128, -96), (-110, -40), (-120, 0), (-88, 40), (-96, 70), (-58, 100), (-52, 128),
           (-14, 150), (6, 176), (30, 160), (24, 130), (60, 104), (70, 70), (100, 38), (96, 0),
           (128, -40), (120, -96), (60, -124), (0, -128), (-60, -124)]
    g.path(catmull(pts, True), 'wind')
    # faixas em espiral
    g.line('M -112 -26 Q -10 10 108 -30', 0.7)
    g.line('M -100 50 Q -10 80 90 40 Q 110 30 100 18', 0.7)
    g.line('M -64 110 Q 0 132 60 100', 0.7)
    g.line('M -14 152 Q 14 160 28 146', 0.6)
    face(g, 0, -70, ex=34, er=13, expr=expr, my=24, mw=15)
    # capuz: uma folha vermelha enrolada
    g.raw('<g transform="rotate(-18 0 -120)">')
    g.path('M -44 -112 Q -30 -182 30 -190 Q 6 -162 36 -118 Q 0 -106 -44 -112 Z', 'cap')
    g.line('M -24 -114 Q -6 -150 22 -178', 0.55)
    g.raw('</g>')
    # folhas girando em volta
    leaf(g, -150, 30, 58, 20, 160, 'leaf', 0.8)
    leaf(g, 140, 100, 58, 20, 30, 'leaf', 0.8)
    leaf(g, -110, 150, 52, 18, 210, 'leafl', 0.8)
    leaf(g, 150, -130, 50, 18, -40, 'leafl', 0.8)
    for px, py in ((-170, 90), (168, 30)):
        g.line(f'M {px - 14} {py} q 14 -12 28 0', 0.6)
    return place(g, x, y, s, flip)


def vitoria_regia(x, y, s=1.0, mode='line', W=6.5, flip=False, expr='sing'):
    """Sereia-fruta guardia do riacho, sentada numa folha de vitoria-regia."""
    g = mk(mode, s, W)
    # folha gigante (base)
    g.path('M -200 120 Q -210 70 -100 58 L 0 58 Q 120 56 200 88 Q 222 128 140 150 Q 0 176 -140 158 Q -200 150 -200 120 Z', 'lily')
    g.path('M -184 110 Q -170 80 -100 74 L 0 74 Q 110 74 182 96 Q 196 122 132 136 Q 0 156 -132 144 Q -186 134 -184 110 Z', 'leafl', 0.5)
    # cauda de sereia em forma de folha
    g.path('M -30 40 Q -60 90 -120 112 Q -150 118 -170 100 Q -150 136 -110 136 Q -50 130 30 70 Z', 'mer')
    g.path('M -170 100 Q -200 84 -206 60 Q -176 70 -160 96 Z', 'mer', 0.8)
    g.path('M -170 100 Q -196 120 -200 146 Q -170 128 -160 108 Z', 'mer', 0.8)
    for t in (-110, -80, -50):
        g.line(f'M {t} {f(110 + (t + 110) * 0.3)} Q {t + 14} {f(100 + (t + 110) * 0.3)} {t + 20} {f(116 + (t + 110) * 0.3)}', 0.45)
    # corpo (vestido de petalas)
    g.path('M -40 -14 Q -54 40 -40 82 Q 0 96 44 82 Q 56 40 40 -14 Z', 'petal')
    for px in (-22, 0, 22):
        g.line(f'M {px} -6 Q {px + 6} 40 {px} 86', 0.5)
    arms(g, [(-38, 4), (-70, 30), (-82, 58)], [(38, 4), (72, -4), (96, -34)], 14)
    # cabeca: fruta redonda
    g.circle(0, -70, 66, 'mer')
    # coroa de petalas de vitoria-regia
    for ang in (-160, -130, -100, -80, -50, -20):
        a = math.radians(ang)
        bx, by = 54 * math.cos(a), -70 + 54 * math.sin(a)
        d, _ = leaf_d(bx, by, 50, 20, ang)
        g.path(d, 'petal2', 0.8)
    g.circle(0, -128, 14, 'flowerc', 0.8)
    face(g, 0, -64, ex=26, er=11, expr=expr, my=24, mw=14)
    # notas musicais
    for nx, ny, sc in ((96, -120, 1), (140, -170, 0.85), (172, -96, 0.7)):
        g.ellipse(nx, ny, 12 * sc, 9 * sc, 'black', 0, rot=-20)
        g.line(f'M {f(nx + 11 * sc)} {f(ny - 2)} L {f(nx + 11 * sc)} {f(ny - 44 * sc)} Q {f(nx + 24 * sc)} {f(ny - 36 * sc)} {f(nx + 28 * sc)} {f(ny - 24 * sc)}', 0.6)
    return place(g, x, y, s, flip)


def guardiao(x, y, s=1.0, mode='line', W=6.5, flip=False, expr='happy'):
    """Guardiao Pe-Virado (inspirado na lenda do Curupira): pes para tras."""
    g = mk(mode, s, W)
    # pes virados: o corpo olha para a direita, os dedos apontam para a esquerda
    for lx in (-26, 26):
        g.tube([(lx, 90), (lx, 140)], 18, 'bark')
        g.path(f'M {lx + 10} 132 Q {lx + 14} 154 {lx} 156 L {lx - 40} 156 Q {lx - 50} 146 {lx - 40} 136 Z', 'bark', 0.9)
        for t in (-38, -30, -22):
            g.circle(lx + t - 6, 152, 5, 'bark', 0.5)
    arms(g, [(-70, 10), (-100, 40), (-104, 74)], [(70, 0), (100, -20), (118, -50)], 15, 'bark')
    # cajado de galho
    g.tube([(118, -120), (124, 140)], 10, 'wood', 0.9)
    leaf(g, 118, -118, 36, 12, -120, 'leaf', 0.7)
    g.circle(118, -50, 13, 'bark')
    # corpo de semente com casca
    g.path('M 0 -96 C 62 -96 84 -30 80 30 C 76 90 40 106 0 106 C -40 106 -76 90 -80 30 C -84 -30 -62 -96 0 -96 Z', 'bark')
    for (a, b) in ((-56, 40), (-48, 70), (52, 50), (40, 80)):
        g.line(f'M {a} {b} q 8 -6 16 0', 0.5)
    # cabelo de folhas em forma de chama
    for ang, ln in ((-150, 70), (-125, 84), (-100, 96), (-78, 92), (-54, 80), (-30, 66)):
        a = math.radians(ang)
        bx, by = 56 * math.cos(a), -40 + 56 * math.sin(a)
        d, v = leaf_d(bx, by, ln, 22, ang + 8)
        g.path(d, 'flame', 0.9)
        g.line(v, 0.5)
    g.path('M -66 -60 Q 0 -110 66 -60 Q 40 -74 0 -72 Q -40 -74 -66 -60 Z', 'flame2', 0.7)
    face(g, 0, -20, ex=28, er=12, expr=expr, my=26, mw=14)
    return place(g, x, y, s, flip)


# ======================================================== CENARIO ==========
def tree(x, y, s=1.0, mode='line', W=6.5, fruits='circle', flip=False):
    g = mk(mode, s, W)
    g.path('M -30 0 Q -22 -120 -26 -200 L 26 -200 Q 22 -120 30 0 Q 44 6 54 14 L -54 14 Q -44 6 -30 0 Z', 'trunk')
    g.line('M -6 -40 Q 2 -60 -4 -84', 0.5)
    g.line('M 8 -120 Q 14 -140 6 -160', 0.5)
    g.ellipse(-2, -100, 9, 13, 'wood2', 0.6)
    canopy = [(-150, -230), (-130, -310), (-60, -350), (20, -362), (100, -330), (150, -260),
              (130, -190), (60, -170), (-10, -182), (-90, -170)]
    g.path(catmull(canopy, True), 'canopy')
    for cx, cy in ((-80, -300), (60, -300)):
        g.line(f'M {cx - 20} {cy} Q {cx} {cy - 20} {cx + 20} {cy}', 0.5)
    if fruits:
        for fx, fy in ((-90, -240), (-30, -290), (40, -230), (100, -280), (-10, -215), (90, -205)):
            g.circle(fx, fy, 14, 'orange', 0.8)
            g.line(f'M {fx} {fy - 14} l 3 -7', 0.5)
    return place(g, x, y, s, flip)


def bush(x, y, s=1.0, mode='line', W=6.5, flowers=True):
    g = mk(mode, s, W)
    pts = [(-90, 0), (-100, -40), (-60, -80), (0, -96), (60, -84), (100, -44), (90, 0)]
    g.path(catmull(pts) + ' Z', 'grass')
    if flowers:
        for fx, fy in ((-50, -40), (10, -64), (56, -30)):
            flower(g, fx, fy, 12)
    return place(g, x, y, s)


def flower(g, x, y, r):
    for i in range(5):
        a = 2 * math.pi * i / 5
        g.circle(x + r * math.cos(a), y + r * math.sin(a), r * 0.75, 'flower', 0.6)
    g.circle(x, y, r * 0.6, 'flowerc', 0.6)


def flower_at(x, y, s=1.0, mode='line', W=5, stem=40):
    g = mk(mode, s, W)
    g.tube([(0, 0), (2, -stem)], 6, 'leaf2', 0.8)
    leaf(g, 2, -stem * 0.4, 26, 9, -30, 'leaf', 0.7, False)
    flower(g, 2, -stem - 10, 12)
    return place(g, x, y, s)


def grass(x, y, s=1.0, W=5):
    g = mk('line', s, W)
    g.line('M -24 0 Q -20 -20 -28 -36 M -8 0 Q -4 -26 0 -44 M 10 0 Q 12 -20 22 -34', 1)
    return place(g, x, y, s)


def rock(x, y, w, h, s=1.0, mode='line', W=6):
    g = mk(mode, s, W)
    g.path(f'M {-w} 0 Q {-w} {-h * 0.8} {-w * 0.4} {-h} Q {w * 0.4} {-h * 1.1} {w} {-h * 0.4} Q {w * 1.05} 0 {w * 0.9} 0 Z', 'rock')
    g.line(f'M {-w * 0.3} {-h * 0.6} q {w * 0.2} {-h * 0.15} {w * 0.4} 0', 0.5)
    return place(g, x, y, s)


def sun(x, y, r, mode='line', W=6, face_on=True):
    g = G(mode, W)
    for i in range(10):
        a = 2 * math.pi * i / 10
        x1, y1 = (r + 12) * math.cos(a), (r + 12) * math.sin(a)
        x2, y2 = (r + 36) * math.cos(a), (r + 36) * math.sin(a)
        g.line(f'M {f(x1)} {f(y1)} L {f(x2)} {f(y2)}', 0.9)
    g.circle(0, 0, r, 'sun')
    if face_on:
        face(g, 0, -4, ex=r * 0.33, er=r * 0.1, expr='joy', my=r * 0.32, mw=r * 0.2)
    return place(g, x, y, 1)


def cloud(x, y, s=1.0, mode='line', W=6):
    g = mk(mode, s, W)
    pts = []
    for i in range(7):
        pts.append((-80 + i * 26, 18))
    bumps = [(95, 0), (70, -30), (30, -48), (-14, -44), (-52, -30), (-92, -4)]
    d = 'M -80 22 L 80 22 '
    prev = (80, 22)
    for bx, by in bumps + [(-80, 22)]:
        mx, my = (prev[0] + bx) / 2, (prev[1] + by) / 2
        dx, dy = bx - prev[0], by - prev[1]
        d += f'Q {f(mx - dy * 0.55)} {f(my + dx * 0.55)} {f(bx)} {f(by)} '
        prev = (bx, by)
    g.path(d + 'Z', 'cloud')
    return place(g, x, y, s)


def hills(x0, x1, ybase, mode='line', W=6):
    """Morros da Serra Dourada ao fundo."""
    g = G(mode, W)
    w = x1 - x0
    d = (f'M {x0} {ybase} L {x0} {ybase - 150} Q {x0 + w * 0.18} {ybase - 260} {x0 + w * 0.36} {ybase - 170} '
         f'Q {x0 + w * 0.55} {ybase - 300} {x0 + w * 0.74} {ybase - 180} Q {x0 + w * 0.88} {ybase - 240} {x1} {ybase - 160} L {x1} {ybase} Z')
    g.path(d, 'hill')
    return g.svg()


def butterfly(x, y, s=1.0, mode='line', W=5, rot=0):
    g = mk(mode, s, W)
    for sx in (-1, 1):
        g.ellipse(sx * 22, -14, 22, 18, 'purple', 0.8, rot=sx * 20)
        g.ellipse(sx * 16, 14, 14, 12, 'flower', 0.8, rot=sx * -20)
    g.ellipse(0, 0, 6, 24, 'black', 0)
    g.line('M -2 -22 Q -10 -40 -18 -42 M 2 -22 Q 10 -40 18 -42', 0.6)
    return place(g, x, y, s, rot=rot)


def bird(x, y, s=1.0, W=5):
    g = mk('line', s, W)
    g.line('M -30 0 Q -15 -18 0 0 Q 15 -18 30 0', 1)
    return place(g, x, y, s)


def ground_line(x0, x1, y, W=6, wave=10):
    pts = []
    n = 8
    for i in range(n + 1):
        px = x0 + (x1 - x0) * i / n
        pts.append((px, y + (wave if i % 2 else -wave) * 0.5))
    return f'<path d="{catmull(pts)}" fill="none" stroke="#000" stroke-width="{W}" stroke-linecap="round"/>'
