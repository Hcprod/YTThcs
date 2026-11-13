"""Cenas (ilustracoes de pagina inteira) do livro. Area de desenho: 700 x 880."""
import math
from art import (G, PAL, place, mk, catmull, leaf, leaf_d, face, rounded_star, f, uid,
                 pitanga, caju, jabuticaba, jaca, manga, pinhao, carambola,
                 redemoinho, vitoria_regia, guardiao,
                 tree, bush, flower_at, grass, rock, sun, cloud, hills, butterfly, bird,
                 ground_line)

AW, AH = 700, 880
SW = 5.5  # espessura do traco dos personagens nas cenas
BG = 5.0  # espessura do traco do cenario


def frame(mode='line', inset=6, r=34, w=7):
    return (f'<rect x="{inset}" y="{inset}" width="{AW - 2 * inset}" height="{AH - 2 * inset}" '
            f'rx="{r}" fill="{"#fff" if mode == "line" else PAL["sky"]}" stroke="#000" stroke-width="{w}"/>')


def clip_art(inner, mode='line'):
    cid = uid('frame')
    return (f'<clipPath id="{cid}"><rect x="9" y="9" width="{AW - 18}" height="{AH - 18}" rx="31"/></clipPath>'
            f'{frame(mode)}<g clip-path="url(#{cid})">{inner}</g>'
            f'<rect x="6" y="6" width="{AW - 12}" height="{AH - 12}" rx="34" fill="none" stroke="#000" stroke-width="7"/>')


def bubble_text(x, y, text, size, mode='line', key='yellow', sw=None, anchor='middle', rot=0):
    sw = sw or max(4, size * 0.12)
    fill = '#fff' if mode == 'line' else PAL.get(key, key)
    tr = f' transform="rotate({rot} {x} {y})"' if rot else ''
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Fredoka" font-weight="700" '
            f'font-size="{size}" fill="{fill}" stroke="#000" stroke-width="{sw:.1f}" stroke-linejoin="round" '
            f'paint-order="stroke" letter-spacing="1"{tr}>{text}</text>')


def ground(y, mode='line', key='grass'):
    g = G(mode, BG)
    pts = [(-20, y + 10), (120, y - 8), (260, y + 6), (420, y - 10), (560, y + 4), (720, y - 6)]
    g.path(catmull(pts) + f' L 720 {AH + 20} L -20 {AH + 20} Z', key)
    return g.svg()


# ----------------------------------------------------------- objetos ------
def pot(x, y, s=1.0, mode='line', rot=0):
    g = mk(mode, s, BG)
    g.path('M -50 -10 Q -50 40 0 44 Q 50 40 50 -10 Z', 'pot')
    g.ellipse(0, -10, 54, 12, 'pot')
    g.tube([(-54, -6), (-74, -14)], 8, 'pot', 0.8)
    g.tube([(54, -6), (74, -14)], 8, 'pot', 0.8)
    return place(g, x, y, s, rot=rot)


def spoon(x, y, s=1.0, mode='line', rot=0):
    g = mk(mode, s, BG)
    g.tube([(0, 0), (0, 80)], 10, 'wood', 0.9)
    g.ellipse(0, -18, 18, 26, 'wood', 0.9)
    return place(g, x, y, s, rot=rot)


def cup(x, y, s=1.0, mode='line', rot=0):
    g = mk(mode, s, BG)
    g.path('M -24 -30 L 24 -30 L 18 30 L -18 30 Z', 'white')
    g.path('M 24 -16 Q 44 -14 40 6 Q 36 18 20 14', None, 0.9)
    g.line('M -21 -6 L 21 -6', 0.6)
    return place(g, x, y, s, rot=rot)


def sieve(x, y, s=1.0, mode='line', rot=0):
    g = mk(mode, s, BG)
    g.path('M -40 0 Q 0 50 40 0 Z', 'pot')
    for t in (-20, 0, 20):
        g.line(f'M {t} 4 L {t} {f(16 - abs(t) * 0.3)}', 0.5)
    g.tube([(40, 0), (90, -6)], 8, 'wood', 0.8)
    return place(g, x, y, s, rot=rot)


def table(x, y, w=180, mode='line'):
    g = G(mode, BG)
    g.path(f'M {-w / 2} -12 L {w / 2} -12 L {w / 2} 6 L {-w / 2} 6 Z', 'table')
    for lx in (-w / 2 + 16, w / 2 - 26):
        g.path(f'M {lx} 6 L {lx + 10} 6 L {lx + 10} 90 L {lx} 90 Z', 'table', 0.9)
    # jarra de suco
    g.path('M -20 -12 L -26 -70 Q 0 -78 26 -70 L 20 -12 Z', 'orange')
    g.path('M 24 -60 Q 44 -56 40 -36 Q 36 -24 22 -26', None, 0.8)
    g.line('M -24 -50 L 24 -50', 0.5)
    for fx in (-60, 60):
        g.circle(fx, -30, 18, 'orange', 0.9)
        g.line(f'M {fx} -48 l 3 -8', 0.6)
    return place(g, x, y, 1)


def stove(x, y, mode='line'):
    """Fogao a lenha de tijolos."""
    g = G(mode, BG)
    g.path('M -90 0 L 90 0 L 90 -120 L -90 -120 Z', 'red')
    for row in range(1, 4):
        yy = -30 * row
        g.line(f'M -90 {yy} L 90 {yy}', 0.5)
    for row in range(4):
        off = 0 if row % 2 == 0 else 30
        for bx in range(-90 + off + 60, 90, 60):
            g.line(f'M {bx} {-30 * row} L {bx} {-30 * row - 30}', 0.5)
    g.path('M -90 -120 L 100 -120 L 100 -136 L -90 -136 Z', 'rock')
    g.path('M -40 0 Q -40 -50 0 -50 Q 40 -50 40 0 Z', 'white')
    for lx in (-22, 0, 22):
        g.path(f'M {lx - 10} 0 L {lx + 10} 0 L {lx} -24 Z', 'flame', 0.6)
    g.path('M 50 -136 L 82 -136 L 82 -260 L 50 -260 Z', 'red')
    for t in (-160, -200, -240):
        g.line(f'M 50 {t} L 82 {t}', 0.5)
    return place(g, x, y, 1)


def fence(x0, x1, y, mode='line'):
    g = G(mode, BG)
    g.path(f'M {x0} {y - 70} L {x1} {y - 70} L {x1} {y - 54} L {x0} {y - 54} Z', 'wood')
    g.path(f'M {x0} {y - 34} L {x1} {y - 34} L {x1} {y - 18} L {x0} {y - 18} Z', 'wood')
    px = x0 + 10
    while px < x1 - 10:
        g.path(f'M {px} {y} L {px} {y - 90} L {px + 12} {y - 102} L {px + 24} {y - 90} L {px + 24} {y} Z', 'wood')
        px += 70
    return g.svg()


def lily_pad(x, y, r, mode='line', s=1.0):
    g = mk(mode, s, BG)
    g.path(f'M 0 0 L {r} -6 A {r} {r * 0.38} 0 1 1 {r} 6 Z', 'lily')
    g.line(f'M 0 0 L {-r * 0.7} {-r * 0.2} M 0 0 L {-r * 0.6} {r * 0.25} M 0 0 L {r * 0.2} {-r * 0.33}', 0.5)
    return place(g, x, y, s)


def fish(x, y, s=1.0, mode='line', flip=False, rot=0):
    g = mk(mode, s, BG)
    g.path('M -40 0 Q 0 -30 40 0 Q 0 30 -40 0 Z', 'blue')
    g.path('M -38 0 L -66 -20 L -60 0 L -66 20 Z', 'blue')
    g.dot(20, -4, 5)
    g.line('M -6 -18 Q 0 0 -6 18', 0.5)
    g.line('M 30 8 Q 36 10 40 6', 0.5)
    return place(g, x, y, s, flip, rot)


def frog(x, y, s=1.0, mode='line'):
    g = mk(mode, s, BG)
    g.ellipse(0, 0, 44, 30, 'leaf')
    for sx in (-1, 1):
        g.circle(sx * 22, -28, 15, 'leaf')
        g.dot(sx * 22, -28, 6)
    g.line('M -18 4 Q 0 16 18 4', 0.7)
    for sx in (-1, 1):
        g.ellipse(sx * 40, 24, 20, 9, 'leaf', 0.8)
    return place(g, x, y, s)


def turtle(x, y, s=1.0, mode='line'):
    g = mk(mode, s, BG)
    g.ellipse(-50, 12, 12, 9, 'leaf', 0.8)
    g.ellipse(30, 14, 12, 9, 'leaf', 0.8)
    g.circle(58, -6, 18, 'leaf')
    g.line('M 54 -10 Q 60 -4 66 -10', 0.6)
    g.line('M 58 2 Q 64 6 70 2', 0.5)
    g.path('M -60 10 Q -50 -50 0 -50 Q 50 -50 50 10 Z', 'jaca')
    g.path('M -24 -36 L 14 -36 L 22 -10 L -32 -10 Z', None, 0.5)
    g.ellipse(-80, 8, 0, 0, 'leaf', 0)
    for zx, zy, zs in ((84, -40, 14), (104, -64, 18)):
        g.raw(f'<text x="{zx}" y="{zy}" font-family="Fredoka" font-weight="700" font-size="{zs * 2}" fill="#fff" stroke="#000" stroke-width="{BG / s * 0.6:.1f}" paint-order="stroke">z</text>')
    return place(g, x, y, s)


def duck(x, y, s=1.0, mode='line'):
    g = mk(mode, s, BG)
    g.path('M -60 0 Q -64 -40 -20 -36 Q 10 -34 20 -20 Q 40 -60 60 -40 Q 76 -24 60 -6 Q 40 20 0 22 Q -50 22 -60 0 Z', 'yellow')
    g.path('M 64 -42 L 92 -36 L 66 -28 Z', 'orange', 0.8)
    g.dot(52, -46, 4.5)
    g.line('M -30 -6 Q -10 6 10 -8', 0.6)
    g.line('M -80 26 q 20 -12 40 0 q 20 12 40 0 q 20 -12 40 0 q 20 12 40 0', 0.6)
    return place(g, x, y, s)


def mushroom(x, y, s=1.0, mode='line'):
    g = mk(mode, s, BG)
    g.path('M -14 0 L -12 -34 L 12 -34 L 14 0 Z', 'white')
    g.path('M -44 -30 Q -40 -80 0 -82 Q 40 -80 44 -30 Z', 'red')
    for px, py, r in ((-20, -54, 8), (12, -64, 7), (24, -42, 6)):
        g.circle(px, py, r, 'white', 0.6)
    return place(g, x, y, s)


def footprint(x, y, s=1.0, rot=0, mode='line'):
    """Pegada invertida: os dedos apontam para tras do caminho."""
    g = mk(mode, s, BG)
    g.path('M -16 -24 Q -20 6 -12 20 Q 0 30 12 20 Q 20 6 16 -24 Q 0 -34 -16 -24 Z', 'wood')
    for i, tx in enumerate((-14, -5, 5, 14)):
        g.circle(tx, 32 + (3 if i in (0, 3) else 0), 5.5 - (1 if i in (0, 3) else 0), 'wood', 0.6)
    return place(g, x, y, s, rot=rot)


def cauldron(x, y, s=1.0, mode='line'):
    g = mk(mode, s, BG)
    for lx in (-50, 0, 50):
        g.path(f'M {lx - 34} 92 L {lx + 34} 92 L {lx + 30} 74 L {lx - 30} 74 Z', 'wood', 0.8)
    for fx in (-40, 0, 40):
        g.path(f'M {fx - 18} 74 Q {fx - 10} 40 {fx} 28 Q {fx + 10} 40 {fx + 18} 74 Z', 'flame', 0.8)
    g.path('M -100 -20 Q -110 70 0 76 Q 110 70 100 -20 Z', 'cauldron')
    g.ellipse(0, -20, 108, 24, 'cauldron')
    g.ellipse(0, -20, 88, 14, 'smoke2', 0.6)
    g.tube([(-80, 50), (-90, 70)], 10, 'cauldron', 0.8)
    g.tube([(80, 50), (90, 70)], 10, 'cauldron', 0.8)
    return place(g, x, y, s)


def bubble(x, y, r, mode='line', w=0.8):
    g = G(mode, BG)
    g.circle(x, y, r, 'glass', w)
    g.path(f'M {f(x - r * 0.55)} {f(y - r * 0.1)} Q {f(x - r * 0.5)} {f(y - r * 0.55)} {f(x - r * 0.1)} {f(y - r * 0.6)}', None, 0.6)
    return g.svg()


def confetti(x, y, kind, size, rot, mode='line', key='yellow'):
    g = G(mode, BG * 0.8)
    if kind == 'star':
        d, _ = rounded_star(0, 0, size, size * 0.5, 5)
        g.path(d, key)
    elif kind == 'rect':
        g.path(f'M {-size} {-size * 0.45} L {size} {-size * 0.45} L {size} {size * 0.45} L {-size} {size * 0.45} Z', key)
    elif kind == 'swirl':
        g.line(f'M {-size} 0 Q {-size / 2} {-size} 0 0 Q {size / 2} {size} {size} 0', 1.1)
    elif kind == 'heart':
        g.path(f'M 0 {size * 0.9} C {-size * 1.4} 0 {-size * 0.6} {-size * 1.1} 0 {-size * 0.35} '
               f'C {size * 0.6} {-size * 1.1} {size * 1.4} 0 0 {size * 0.9} Z', key)
    return f'<g transform="translate({f(x)} {f(y)}) rotate({rot})">{g.svg()}</g>'


def moon(x, y, r, mode='line'):
    g = G(mode, BG)
    g.path(f'M 0 {-r} A {r} {r} 0 1 0 0 {r} A {r * 0.75} {r * 0.85} 0 1 1 0 {-r} Z', 'sun')
    return place(g, x, y, 1)


def star(x, y, r, mode='line'):
    g = G(mode, BG * 0.8)
    d, _ = rounded_star(0, 0, r, r * 0.48, 5)
    g.path(d, 'sun')
    return place(g, x, y, 1)


def blanket(cx, cy, mode='line'):
    g = G(mode, BG)
    d = f'M {cx - 250} {cy - 50} L {cx + 250} {cy - 50} L {cx + 320} {cy + 90} L {cx - 320} {cy + 90} Z'
    g.path(d, 'white')
    g.clip_begin(d)
    if mode == 'color':
        g.raw(f'<path d="{d}" fill="{PAL["check"]}" opacity="0.35"/>')
    for i in range(-6, 7):
        g.line(f'M {cx + i * 40} {cy - 50} L {cx + i * 52} {cy + 90}', 0.5)
    for yy in (cy - 15, cy + 25, cy + 60):
        g.line(f'M {cx - 400} {yy} L {cx + 400} {yy}', 0.5)
    g.clip_end()
    g.path(d, None)
    return g.svg()


def cave_bg(mode='line'):
    g = G(mode, BG)
    # parede de pedra com abertura
    g.path(f'M -20 -20 L {AW + 20} -20 L {AW + 20} {AH + 20} L -20 {AH + 20} Z', 'cave')
    inner = ('M 60 820 Q 40 500 120 300 Q 220 110 400 120 Q 600 140 650 360 Q 690 560 660 820 Z')
    g.path(inner, 'rock')
    for (x, y, rx, ry, rt) in ((60, 120, 34, 22, -10), (640, 90, 40, 24, 8), (30, 470, 22, 34, 0),
                               (684, 620, 18, 30, 0), (220, 50, 44, 22, 4), (470, 40, 50, 24, -6)):
        g.ellipse(x, y, rx, ry, 'rock', 0.6, rot=rt)
        g.line(f'M {x - rx * 0.5} {y - ry * 0.2} q {rx * 0.4} {-ry * 0.4} {rx * 0.8} 0', 0.4)
    # estalactites
    for (x, ln) in ((220, 60), (300, 90), (480, 70), (560, 50)):
        top = 160 if x in (220, 560) else 125
        g.path(f'M {x - 22} {top} Q {x} {top + ln * 1.4} {x + 22} {top} Z', 'cave', 0.8)
    return g.svg()


# --------------------------------------------------------- cenas ----------
def scene_gallery(kind, mode='line'):
    """Pagina de apresentacao de personagem (desenho grande)."""
    a = []
    if kind == 'pitanga':
        a.append(sun(590, 120, 50, mode, BG))
        a.append(cloud(140, 130, 0.9, mode, BG))
        a.append(ground(700, mode))
        a.append(flower_at(90, 770, 1.1, mode, BG, 60))
        a.append(flower_at(610, 790, 1.0, mode, BG, 50))
        a.append(butterfly(560, 330, 0.9, mode, BG, -15))
        a.append(pitanga(350, 480, 1.45, mode, 'open', 7))
    elif kind == 'caju':
        a.append(tree(110, 640, 0.7, mode, BG))
        a.append(ground(650, mode))
        a.append(rock(590, 740, 60, 50, 1, mode, BG))
        a.append(bird(560, 160, 1.0, BG))
        a.append(bird(470, 120, 0.8, BG))
        a.append(caju(380, 470, 1.35, mode, 'happy', 7, pose='point'))
        a.append(grass(160, 800, 1.2, BG))
    elif kind == 'jabuticaba':
        a.append(cloud(560, 120, 0.9, mode, BG))
        a.append(ground(690, mode))
        a.append(butterfly(150, 300, 1.0, mode, BG, 15))
        a.append(flower_at(110, 790, 1.1, mode, BG, 60))
        a.append(flower_at(600, 800, 1.1, mode, BG, 40))
        a.append(jabuticaba(350, 470, 1.5, mode, 'happy', 7))
    elif kind == 'jaca':
        a.append(moon(580, 130, 50, mode))
        a.append(star(130, 120, 26, mode))
        a.append(star(220, 200, 18, mode))
        a.append(star(470, 90, 16, mode))
        a.append(ground(720, mode))
        a.append(jaca(350, 470, 1.35, mode, 'wise', 7, book=True))
    elif kind == 'manga':
        a.append(stove(140, 640, mode))
        a.append(ground(650, mode))
        a.append(table(560, 700, 190, mode))
        a.append(manga(350, 470, 1.3, mode, 'happy', 7))
    elif kind == 'pinhao':
        a.append(ground(720, mode))
        # pilha de livros e uma invencao (cata-vento de helice)
        g = G(mode, BG)
        for i, (w, key) in enumerate(((150, 'blue'), (130, 'red'), (140, 'leaf'), (110, 'purple'))):
            y = 790 - i * 34
            g.path(f'M {110 - w / 2} {y} L {110 + w / 2} {y} L {110 + w / 2} {y - 30} L {110 - w / 2} {y - 30} Z', key)
            g.line(f'M {110 - w / 2 + 14} {y - 15} L {110 + w / 2 - 14} {y - 15}', 0.5)
        g.tube([(590, 800), (590, 600)], 10, 'wood', 0.9)
        for ang in (0, 90, 180, 270):
            d, _ = leaf_d(590, 580, 70, 26, ang + 20)
            g.path(d, 'yellow')
        g.circle(590, 580, 12, 'red')
        a.append(g.svg())
        a.append(pinhao(350, 440, 1.3, mode, 'happy', 7, prop='magnifier'))
    elif kind == 'carambola':
        a.append(cave_bg(mode))
        a.append(cauldron(520, 720, 0.85, mode))
        for bx, by, r in ((480, 560, 24), (540, 500, 18), (600, 560, 14), (520, 430, 12)):
            a.append(bubble(bx, by, r, mode))
        a.append(carambola(270, 500, 1.25, mode, 'grumpy', 7))
    return clip_art(''.join(a), mode)


def scene_ch1(mode='line'):
    a = [hills(-20, 720, 470, mode, BG), sun(110, 110, 44, mode, BG)]
    a.append(ground(600, mode))
    a.append(stove(600, 600, mode))
    a.append(fence(-10, 300, 600, mode))
    # redemoinho levando os utensilios
    a.append(redemoinho(380, 300, 0.85, mode, SW))
    a.append(spoon(205, 220, 0.9, mode, rot=-40))
    a.append(pot(560, 150, 0.85, mode, rot=18))
    a.append(sieve(260, 90, 0.8, mode, rot=-20))
    a.append(cup(510, 290, 0.9, mode, rot=25))
    a.append(manga(150, 640, 0.72, mode, 'surprised', SW, spoon=False))
    a.append(pitanga(400, 735, 0.62, mode, 'open', SW, pose='run'))
    a.append(caju(580, 720, 0.62, mode, 'open', SW, pose='point', flip=True))
    return clip_art(''.join(a), mode)


def scene_ch2(mode='line'):
    a = [cloud(560, 110, 0.8, mode, BG), cloud(140, 80, 0.6, mode, BG)]
    a.append(tree(110, 420, 0.75, mode, BG))
    # margem e agua
    g = G(mode, BG)
    g.path(f'M -20 380 L 720 380 L 720 540 Q 560 500 350 530 Q 150 560 -20 520 Z', 'grass')
    g.path(f'M -20 520 Q 150 560 350 530 Q 560 500 720 540 L 720 900 L -20 900 Z', 'water')
    for (wx, wy) in ((80, 620), (560, 600), (110, 790), (420, 810), (620, 740), (300, 700)):
        g.line(f'M {wx - 40} {wy} q 20 -14 40 0 q 20 14 40 0', 0.6)
    a.append(g.svg())
    a.append(lily_pad(110, 700, 60, mode))
    a.append(lily_pad(600, 830, 56, mode))
    a.append(frog(110, 680, 0.75, mode))
    a.append(fish(610, 660, 0.8, mode, rot=-25))
    a.append(duck(600, 590, 0.7, mode))
    a.append(jabuticaba(280, 410, 0.52, mode, 'happy', SW))
    a.append(pinhao(430, 380, 0.48, mode, 'surprised', SW, prop='book'))
    a.append(vitoria_regia(370, 680, 0.95, mode, SW))
    return clip_art(''.join(a), mode)


def scene_ch3(mode='line'):
    a = []
    # fundo de floresta
    a.append(tree(80, 380, 0.75, mode, BG, fruits=None))
    a.append(tree(640, 360, 0.7, mode, BG, fruits=None))
    a.append(ground(330, mode))
    # trilha
    g = G(mode, BG)
    g.path('M 260 900 Q 300 700 420 600 Q 520 500 400 420 Q 320 370 360 330 L 420 330 '
           'Q 400 380 470 420 Q 620 520 520 620 Q 420 720 460 900 Z', 'hill')
    a.append(g.svg())
    for (fx, fy, sc, rt) in ((360, 820, 1.25, 10), (420, 720, 1.15, 20), (480, 620, 1.05, 25),
                             (500, 520, 0.9, 0), (440, 440, 0.75, -30)):
        a.append(footprint(fx, fy, sc, rt, mode))
    a.append(bush(130, 420, 0.7, mode, BG))
    a.append(mushroom(90, 820, 0.9, mode))
    a.append(mushroom(150, 840, 0.6, mode))
    a.append(guardiao(590, 420, 0.62, mode, SW, flip=True))
    a.append(pinhao(150, 560, 0.58, mode, 'surprised', SW, prop='magnifier'))
    a.append(caju(590, 730, 0.6, mode, 'surprised', SW, flip=True))
    a.append(bird(200, 140, 0.9, BG))
    return clip_art(''.join(a), mode)


def scene_ch4(mode='line'):
    a = [cave_bg(mode)]
    # nuvem de fumaca colorida saindo do caldeirao
    g = G(mode, BG)
    from art import polar_shape
    g.path(polar_shape(330, 480, 175, 190, lambda t: 1 + 0.08 * abs(math.sin(5 * t)), 240), 'smoke1')
    g.path(polar_shape(330, 520, 90, 110, lambda t: 1 + 0.1 * abs(math.sin(4 * t)), 200), 'smoke3', 0.7)
    a.append(g.svg())
    a.append(cauldron(330, 700, 1.0, mode))
    # explosao de confetes e bolhas
    import random
    rnd = random.Random(7)
    kinds = ['star', 'rect', 'heart', 'swirl']
    keys = ['yellow', 'red', 'blue', 'purple', 'flower', 'leaf']
    spots = [(560, 470), (120, 380), (590, 330), (230, 250), (150, 520), (470, 250), (330, 220),
             (420, 170), (600, 200), (110, 260), (540, 140), (240, 150)]
    for i, (x, y) in enumerate(spots):
        a.append(confetti(x + rnd.randint(-10, 10), y, kinds[i % 4], rnd.randint(22, 30), rnd.randint(-40, 40),
                          mode, keys[i % len(keys)]))
    for (x, y, r) in ((300, 560, 30), (390, 500, 24), (230, 470, 22), (450, 420, 32), (330, 400, 22),
                      (260, 340, 20), (400, 300, 28), (180, 190, 24), (500, 320, 20), (350, 140, 18)):
        a.append(bubble(x, y, r, mode))
    a.append(carambola(150, 690, 0.62, mode, 'surprised', SW))
    a.append(manga(590, 600, 0.5, mode, 'joy', SW, spoon=False, flip=True))
    a.append(pitanga(520, 790, 0.45, mode, 'laugh', SW, pose='wave', flip=True))
    return clip_art(''.join(a), mode)


def scene_final(mode='line'):
    a = []
    a.append(moon(590, 100, 46, mode))
    for (x, y, r) in ((120, 80, 18), (220, 150, 12), (420, 70, 14), (480, 170, 10), (660, 220, 12)):
        a.append(star(x, y, r, mode))
    a.append(redemoinho(330, 150, 0.32, mode, 4, expr='joy'))
    a.append(ground(460, mode))
    a.append(tree(110, 470, 0.85, mode, BG))
    a.append(blanket(350, 700, mode))
    a.append(jaca(370, 480, 0.68, mode, 'wise', SW, book=True))
    a.append(pinhao(590, 470, 0.45, mode, 'happy', SW, prop='book'))
    a.append(manga(170, 560, 0.48, mode, 'happy', SW))
    a.append(pitanga(120, 770, 0.42, mode, 'joy', SW, pose='down'))
    a.append(caju(270, 780, 0.42, mode, 'happy', SW))
    a.append(jabuticaba(440, 790, 0.42, mode, 'happy', SW, notebook=False))
    a.append(carambola(590, 750, 0.38, mode, 'happy', SW))
    return clip_art(''.join(a), mode)


def scene_title(mode='line'):
    a = []
    a.append(pitanga(220, 140, 0.55, mode, 'joy', SW, pose='wave'))
    a.append(caju(480, 140, 0.55, mode, 'happy', SW, pose='point', flip=True))
    return ''.join(a)
