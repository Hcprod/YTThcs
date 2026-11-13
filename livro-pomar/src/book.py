"""Monta o miolo (interior) e a capa do livro em HTML, prontos para virar PDF.

Uso:  python3 book.py   -> gera build/interior.html e build/capa.html
      node render.js    -> gera build/*.pdf
"""
import os
from config import TITULO, TITULO_LINHAS, SUBTITULO, AUTOR, ANO, PAPEL_ESPESSURA
from scenes import (AW, AH, scene_gallery, scene_ch1, scene_ch2, scene_ch3, scene_ch4,
                    scene_final, bubble_text, clip_art, star, cloud, sun, ground, flower_at,
                    butterfly, spoon, pot, frog, fish, footprint, bubble)
from art import (pitanga, caju, jabuticaba, jaca, manga, pinhao, carambola, redemoinho,
                 vitoria_regia, guardiao, tree, hills, G, PAL, leaf, catmull)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, 'build')

# ------------------------------------------------------------------ textos
PERSONAGENS = [
    ('pitanga', 'Pitanga', 'Agitada, tagarela e cheia de ideias mirabolantes. Onde tem confusão, a Pitanga chega primeiro!'),
    ('caju', 'Caju', 'O explorador da turma. Com seu chapéu de palha e o estilingue de galho, conhece cada trilha do pomar.'),
    ('jabuticaba', 'Jabuticaba', 'Quietinha e observadora. Anota tudo o que descobre no seu caderno de folhas secas.'),
    ('jaca', 'Vovó Jaca', 'A mais sábia do pomar. Toda noite conta histórias debaixo do velho Pé de Laranja.'),
    ('manga', 'Dona Manga', 'A cozinheira mágica! Faz os sucos e os bolos mais gostosos de toda a Serra Dourada.'),
    ('pinhao', 'Professor Pinhão', 'Cientista, inventor e leitor de livros enormes. Suas invenções quase sempre funcionam. Quase.'),
    ('carambola', 'Carambola', 'Vive numa caverna de pedra fazendo poções que sempre dão errado. É rabugenta, mas no fundo é uma estrela.'),
]

CAPITULOS = [
    {
        'n': 1, 'titulo': 'O Mistério do Redemoinho de Folhas',
        'texto': [
            'Toda manhã, Dona Manga preparava o famoso suco do pomar. Mas, naquele dia, a cozinha amanheceu de pernas para o ar.',
            '— Cadê minha colher de pau? E a panela? E o coador?! — gritou ela.',
            'Fiu-fiu-fiuuu! Um redemoinho de folhas passou rodopiando, dando risadinhas e levando tudo pelos ares.',
            '— Foi ele! — disse Pitanga, já correndo. — Vem, Caju!',
            'Depois de muita correria, a turma descobriu que o redemoinho não era malvado: ele só queria brincar! Dona Manga fez um acordo: ele devolveria tudo e, em troca, ganharia um copo de suco de pitanga.',
            '— Ei! Suco de QUÊ?! — reclamou Pitanga.',
        ],
        'cena': scene_ch1,
        'spot': lambda m='line': manga(150, 120, 0.4, m, 'surprised', 4.5, spoon=False) + spoon(330, 70, 0.7, m, rot=-30) + pot(470, 110, 0.7, m, rot=15),
    },
    {
        'n': 2, 'titulo': 'A Guardiã das Águas Claras',
        'texto': [
            'Depois de uma noite de trovoada, os bichos do pomar acordaram assustados. O sapo não coaxava, o peixe não nadava e o pato não queria sair do ninho.',
            'Foi então que uma música suave veio do riacho. Sentada numa folha gigante de vitória-régia estava a Vitória-Régia, a guardiã das águas claras.',
            '— Lá-lá-riii… — cantava ela, e os bichos foram se acalmando um por um.',
            'Jabuticaba anotou a melodia no caderno. O Professor Pinhão tentou gravar a canção com uma invenção nova, mas a máquina só sabia fazer “pim”.',
            '— Pim! — fez a máquina. E todo mundo caiu na risada.',
        ],
        'cena': scene_ch2,
        'spot': lambda m='line': frog(170, 140, 0.9, m) + fish(420, 120, 0.9, m, rot=-15),
    },
    {
        'n': 3, 'titulo': 'A Pegada Invertida na Trilha',
        'texto': [
            'Caju achou pegadas na trilha da mata e decidiu segui-las. Mas, quanto mais andava, mais longe ficava do lugar onde queria chegar!',
            '— Elementar! — disse o Professor Pinhão, olhando pela lupa. — Os dedos destas pegadas apontam para trás!',
            'De trás de uma árvore saiu uma figura de cabelos de folhas cor de fogo: era o Guardião Pé-Virado, protetor da mata.',
            '— Eu confundo quem quer arrancar mais frutas do que precisa — explicou ele. — Do pomar a gente cuida, não estraga.',
            'Caju prometeu colher só o necessário. E, desde então, o Guardião ensina a turma os caminhos secretos da floresta.',
        ],
        'cena': scene_ch3,
        'spot': lambda m='line': ''.join(footprint(120 + i * 90, 110 + (16 if i % 2 else -16), 1.3, 0, m) for i in range(5)),
    },
    {
        'n': 4, 'titulo': 'O Feitiço Trapalhão da Caverna',
        'texto': [
            'A Carambola queria muito, muito mesmo, a receita do bolo de fubá da Dona Manga. Então copiou a receita escondida… mas copiou tudo errado!',
            'Em vez de “fubá”, escreveu “fumaça”. Em vez de “ovos”, escreveu “bolhas”. E, em vez de “uma pitada de sal”, escreveu “uma pitada de sol”.',
            'Mexe, mexe, mexe… CABRUM! O caldeirão explodiu numa chuva de confetes e bolhas de sabão!',
            'Dona Manga e Pitanga chegaram correndo e não aguentaram de tanto rir. Depois, ensinaram a receita certinha para a Carambola.',
            '— Hunf… — resmungou ela, de boca cheia. — Até que ficou gostoso.',
        ],
        'cena': scene_ch4,
        'spot': lambda m='line': carambola(200, 110, 0.38, m, 'grumpy', 4.5) + bubble(380, 80, 30, m) + bubble(450, 140, 20, m) + bubble(500, 60, 24, m),
    },
]

FINAL = [
    'Quando a noite chegou, a turma toda se reuniu debaixo do velho Pé de Laranja, a árvore mais antiga da Serra Dourada.',
    'Vovó Jaca ajeitou os óculos, abriu seu livro e começou:',
    '— Era uma vez um pomar onde as frutas falavam, os redemoinhos brincavam e até a Carambola dava risada…',
    'E lá no céu, rodopiando bem devagarinho, o redemoinho de folhas também parou para ouvir.',
]

# ------------------------------------------------------------- estilos
CSS = """
@font-face{font-family:Fredoka;font-weight:500;src:url(../fonts/fredoka-latin-500-normal.woff2)}
@font-face{font-family:Fredoka;font-weight:600;src:url(../fonts/fredoka-latin-600-normal.woff2)}
@font-face{font-family:Fredoka;font-weight:700;src:url(../fonts/fredoka-latin-700-normal.woff2)}
@font-face{font-family:Nunito;font-weight:600;src:url(../fonts/nunito-latin-600-normal.woff2)}
@font-face{font-family:Nunito;font-weight:700;src:url(../fonts/nunito-latin-700-normal.woff2)}
@font-face{font-family:Nunito;font-weight:800;src:url(../fonts/nunito-latin-800-normal.woff2)}
@page{size:8.5in 11in;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff;color:#000}
body{font-family:Nunito,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:8.5in;height:11in;position:relative;overflow:hidden;page-break-after:always;break-after:page;background:#fff}
/* recto (impar, direita): medianiz (lombada) a esquerda; verso (par): a direita */
.recto{padding:0.5in 0.5in 0.55in 0.65in}
.verso{padding:0.5in 0.65in 0.55in 0.5in}
.art{width:100%;height:9.2in;display:block}
.caption{font-family:Fredoka;font-weight:600;font-size:15pt;text-align:center;margin-top:0.12in}
.caption small{display:block;font-family:Nunito;font-weight:600;font-size:12pt;margin-top:2px}
.textbox{height:100%;border:4px solid #000;border-radius:28px;padding:0.45in 0.5in;position:relative;display:flex;flex-direction:column}
.chip{align-self:flex-start;font-family:Fredoka;font-weight:600;font-size:14pt;border:3px solid #000;border-radius:30px;padding:3px 16px}
h1{font-family:Fredoka;font-weight:700;font-size:29pt;line-height:1.12;margin:0.18in 0 0.2in}
p{font-size:17.5pt;line-height:1.5;margin:0 0 0.13in;font-weight:600}
.spot{margin-top:auto;display:flex;justify-content:center}
.spot-svg{height:100%;width:auto;display:block}
.center{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;height:100%}
.small p{font-size:11pt;line-height:1.5;font-weight:600}
"""


def svg(content, w=AW, h=AH, cls='art'):
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{content}</svg>'


def page(side, body):
    return f'<section class="page {side}">{body}</section>'


# --------------------------------------------------------------- paginas
def p_titulo():
    a = []
    a.append(hills(-20, 720, 880, 'line', 5))
    a.append(sun(590, 110, 46, 'line', 5))
    a.append(cloud(120, 110, 0.8))
    a.append(bubble_text(350, 300, TITULO_LINHAS[0], 62))
    a.append(bubble_text(350, 380, TITULO_LINHAS[1], 62))
    a.append(f'<text x="350" y="440" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="26">{SUBTITULO}</text>')
    a.append(pitanga(200, 650, 0.62, 'line', 'joy', 5.5, pose='wave'))
    a.append(caju(500, 650, 0.62, 'line', 'happy', 5.5, pose='point', flip=True))
    a.append(jabuticaba(350, 760, 0.42, 'line', 'happy', 5.5, notebook=False))
    return page('recto', svg(clip_art(''.join(a))) + f'<div class="caption">{AUTOR}</div>')


def p_creditos():
    return page('verso', f'''<div class="center small" style="justify-content:flex-end;padding-bottom:0.4in">
<p><b>{TITULO}</b><br>{SUBTITULO}</p>
<p>Criação: {AUTOR}<br>© {ANO} {AUTOR}. Todos os direitos reservados.</p>
<p>Nenhuma parte deste livro pode ser reproduzida sem autorização,<br>exceto as páginas de colorir, para uso pessoal.</p>
<p>Esta é uma obra original. Os personagens, o Pomar da Serra Dourada e as histórias<br>foram criados para este livro. As lendas do folclore brasileiro que inspiraram<br>alguns capítulos (Saci, Iara e Curupira) são de domínio público e foram recontadas livremente.</p>
<p>Fontes tipográficas: Fredoka e Nunito (SIL Open Font License).</p>
<p><b>Dica:</b> as páginas de desenho são impressas só de um lado.<br>Coloque uma folha de papel atrás da página ao usar canetinha.</p>
</div>''')


def p_pertence():
    a = []
    a.append(bubble_text(350, 140, 'Este livro', 70))
    a.append(bubble_text(350, 225, 'pertence a:', 70))
    g = G('line', 6)
    g.path('M 90 300 L 610 300 Q 640 300 640 330 L 640 430 Q 640 460 610 460 L 90 460 Q 60 460 60 430 L 60 330 Q 60 300 90 300 Z', 'white')
    g.line('M 110 410 L 590 410', 0.6)
    a.append(g.svg())
    for (x, y, r) in ((80, 560, 22), (630, 540, 26), (560, 620, 14), (150, 650, 14)):
        a.append(star(x, y, r, 'line'))
    a.append(ground(780, 'line'))
    a.append(manga(200, 690, 0.5, 'line', 'happy', 5.5))
    a.append(jaca(470, 680, 0.5, 'line', 'wise', 5.5))
    a.append(flower_at(640, 840, 1, 'line', 5, 50))
    return page('recto', svg(clip_art(''.join(a))))


def p_turma():
    itens = ''.join(f'<p style="margin-bottom:0.09in;font-size:14pt;line-height:1.35"><b>{nome}</b> — {desc}</p>'
                    for _, nome, desc in PERSONAGENS)
    spot = svg(pitanga(120, 95, 0.36, 'line', 'joy', 4.5) + caju(300, 95, 0.36, 'line', 'happy', 4.5)
               + jabuticaba(470, 100, 0.36, 'line', 'happy', 4.5, notebook=False), 600, 170, 'spot-svg')
    return page('verso', f'''<div class="textbox"><span class="chip">Bem-vindo!</span>
<h1>Conheça a turma do Pomar da Serra Dourada</h1>
<p style="font-size:14pt">Lá no alto da serra existe um pomar onde as frutas falam, brincam e vivem aventuras. Pegue seus lápis de cor e venha conhecer cada um deles!</p>
{itens}
<div class="spot" style="height:1.6in">{spot}</div></div>''')


def p_galeria(kind, nome, desc):
    return page('recto', svg(scene_gallery(kind)) + f'<div class="caption">{nome}<small>{desc}</small></div>')


def p_teste(i):
    """Verso das paginas de desenho: area para testar cores (protege o proximo desenho)."""
    a = []
    if i % 2 == 0:
        a.append(bubble_text(350, 110, 'Teste suas cores!', 54))
        g = G('line', 5)
        for r in range(4):
            for c in range(4):
                cx, cy = 140 + c * 140, 230 + r * 150
                g.path(f'M {cx - 50} {cy} Q {cx - 46} {cy - 50} {cx} {cy - 48} Q {cx + 52} {cy - 44} {cx + 48} {cy + 4} '
                       f'Q {cx + 44} {cy + 52} {cx} {cy + 48} Q {cx - 54} {cy + 46} {cx - 50} {cy} Z', 'white')
        a.append(g.svg())
        a.append(f'<text x="350" y="840" text-anchor="middle" font-family="Fredoka" font-weight="500" font-size="22">Pinte uma cor em cada mancha antes de colorir o desenho.</text>')
    else:
        a.append(bubble_text(350, 110, 'Rabisque aqui!', 54))
        g = G('line', 5)
        g.raw('<rect x="60" y="160" width="580" height="620" rx="30" fill="#fff" stroke="#000" stroke-width="4" stroke-dasharray="18 14"/>')
        a.append(g.svg())
        a.append(f'<text x="350" y="840" text-anchor="middle" font-family="Fredoka" font-weight="500" font-size="22">Desenhe uma fruta nova para a turma do pomar!</text>')
    return page('verso', svg(clip_art(''.join(a))))


def p_capitulo_texto(cap):
    paras = ''.join(f'<p>{t}</p>' for t in cap['texto'])
    return page('verso', f'''<div class="textbox"><span class="chip">Capítulo {cap["n"]}</span>
<h1>{cap["titulo"]}</h1>{paras}<div class="spot" style="height:2.0in">{svg(cap["spot"](), 600, 220, "spot-svg")}</div></div>''')


def p_capitulo_arte(cap):
    return page('recto', svg(cap['cena']()) + f'<div class="caption">Capítulo {cap["n"]} · {cap["titulo"]}</div>')


def p_final_texto():
    paras = ''.join(f'<p>{t}</p>' for t in FINAL)
    spot = svg(redemoinho(300, 110, 0.42, 'line', 4.5, expr='joy'), 600, 220, 'spot-svg')
    return page('verso', f'''<div class="textbox"><span class="chip">Epílogo</span>
<h1>Histórias debaixo do Pé de Laranja</h1>{paras}<div class="spot" style="height:2.2in">{spot}</div></div>''')


def p_final_arte():
    return page('recto', svg(scene_final()) + '<div class="caption">Boa noite, Pomar da Serra Dourada!</div>')


def p_fim():
    a = [bubble_text(350, 300, 'Fim!', 150)]
    a.append(f'<text x="350" y="400" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="30">…ou será que a aventura continua?</text>')
    a.append(ground(700, 'line'))
    a.append(carambola(200, 610, 0.5, 'line', 'happy', 5.5))
    a.append(pinhao(500, 590, 0.5, 'line', 'joy', 5.5, prop='book'))
    return page('verso', svg(clip_art(''.join(a))))


def p_invente():
    a = [bubble_text(350, 105, 'Invente sua fruta!', 54)]
    g = G('line', 5)
    g.raw('<rect x="60" y="150" width="580" height="500" rx="30" fill="#fff" stroke="#000" stroke-width="4" stroke-dasharray="18 14"/>')
    for i, label in enumerate(('Nome:', 'Ela adora:', 'Seu poder secreto:')):
        y = 720 + i * 60
        g.raw(f'<text x="70" y="{y}" font-family="Fredoka" font-weight="600" font-size="26">{label}</text>')
        g.line(f'M {70 + len(label) * 14 + 30} {y + 4} L 630 {y + 4}', 0.6)
    a.append(g.svg())
    return page('recto', svg(clip_art(''.join(a))))


def p_anotacoes():
    a = [bubble_text(350, 110, 'Meu desenho favorito foi…', 44)]
    g = G('line', 5)
    for i in range(9):
        g.line(f'M 80 {220 + i * 66} L 620 {220 + i * 66}', 0.6)
    a.append(g.svg())
    a.append(guardiao(560, 790, 0.32, 'line', 4.5))
    a.append(vitoria_regia(170, 800, 0.34, 'line', 4.5))
    return page('verso', svg(clip_art(''.join(a))))


def interior():
    pages = [p_titulo(), p_creditos(), p_pertence(), p_turma()]
    for i, (k, nome, desc) in enumerate(PERSONAGENS):
        pages.append(p_galeria(k, nome, desc))
        if i < len(PERSONAGENS) - 1:
            pages.append(p_teste(i))
    for cap in CAPITULOS:
        pages.append(p_capitulo_texto(cap))
        pages.append(p_capitulo_arte(cap))
    pages += [p_final_texto(), p_final_arte(), p_fim(), p_invente(), p_anotacoes()]
    if len(pages) % 2:
        pages.append(page('verso', ''))
    return pages


# ------------------------------------------------------------------ capa
def cover(n_pages):
    bleed = 0.125
    spine = n_pages * PAPEL_ESPESSURA
    W = bleed * 2 + 8.5 * 2 + spine
    H = 11 + bleed * 2
    dpi = 96
    Wp, Hp = W * dpi, H * dpi
    fx = (bleed + 8.5 + spine) * dpi  # inicio da capa frontal
    m = 'color'
    a = [f'<rect width="{Wp:.1f}" height="{Hp:.1f}" fill="{PAL["sky"]}"/>']
    # --- frente
    fr = []
    fr.append(hills(-60, 900, 760, m, 5))
    fr.append(sun(700, 150, 60, m, 5))
    fr.append(cloud(160, 170, 0.9, m, 5))
    g = G(m, 5)
    g.path('M -60 700 Q 200 660 420 690 Q 650 720 900 680 L 900 1200 L -60 1200 Z', 'grass')
    fr.append(g.svg())
    fr.append(tree(150, 760, 0.95, m, 5))
    fr.append(bubble_text(408, 300, TITULO_LINHAS[0], 80, m, 'orange', 9))
    fr.append(bubble_text(408, 400, TITULO_LINHAS[1], 80, m, 'orange', 9))
    fr.append(f'<rect x="98" y="430" width="620" height="54" rx="27" fill="#fff" stroke="#000" stroke-width="5"/>'
              f'<text x="408" y="466" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="27">{SUBTITULO}</text>')
    fr.append(jaca(560, 760, 0.62, m, 'wise', 5.5))
    fr.append(pinhao(720, 760, 0.55, m, 'happy', 5.5, prop='magnifier'))
    fr.append(manga(330, 790, 0.55, m, 'happy', 5.5))
    fr.append(pitanga(170, 920, 0.6, m, 'joy', 5.5, pose='wave'))
    fr.append(caju(380, 930, 0.6, m, 'happy', 5.5, pose='point'))
    fr.append(jabuticaba(580, 950, 0.56, m, 'happy', 5.5))
    fr.append(carambola(730, 940, 0.48, m, 'grumpy', 5.5))
    fr.append(f'<text x="408" y="1060" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="30" fill="#fff" stroke="#000" stroke-width="5" paint-order="stroke">{AUTOR}</text>')
    a.append(f'<clipPath id="front"><rect x="0" y="{-bleed * dpi:.1f}" width="{(8.5 + bleed) * dpi:.1f}" height="{Hp:.1f}"/></clipPath>'
             f'<g transform="translate({fx:.1f} {bleed * dpi:.1f})"><g clip-path="url(#front)">{"".join(fr)}</g></g>')
    # --- verso (contracapa)
    bk = []
    bk.append(f'<rect x="60" y="90" width="696" height="560" rx="34" fill="#fff" stroke="#000" stroke-width="5"/>')
    blurb = [
        'Lá no alto da Serra Dourada existe um pomar',
        'onde as frutas falam, brincam e vivem aventuras!',
        '',
        'Corra atrás de um redemoinho brincalhão, ouça',
        'a canção da guardiã do riacho, siga pegadas',
        'misteriosas e escape da poção mais trapalhona',
        'que já saiu de um caldeirão.',
        '',
        '• 4 capítulos de aventura inspirados no folclore',
        '• 12 ilustrações de página inteira para colorir',
        '• Páginas impressas de um lado só',
        '• Para crianças de 4 a 10 anos',
    ]
    for i, ln in enumerate(blurb):
        wgt = 700 if ln.startswith('•') else 600
        bk.append(f'<text x="100" y="{150 + i * 38}" font-family="Nunito" font-weight="{wgt}" font-size="25">{ln}</text>')
    bk.append(redemoinho(170, 830, 0.55, m, 5.5))
    bk.append(vitoria_regia(400, 900, 0.48, m, 5.5))
    bk.append(guardiao(230, 990, 0.3, m, 4.5))
    # area livre para o codigo de barras (KDP: 2" x 1.2", canto inferior direito)
    bk.append(f'<rect x="{816 - 0.25 * dpi - 2.1 * dpi:.1f}" y="{1056 - 0.25 * dpi - 1.3 * dpi:.1f}" width="{2.1 * dpi:.1f}" height="{1.3 * dpi:.1f}" fill="#fff"/>')
    a.append(f'<g transform="translate({bleed * dpi:.1f} {bleed * dpi:.1f})">{"".join(bk)}</g>')
    # lombada
    a.append(f'<rect x="{(bleed + 8.5) * dpi:.1f}" y="0" width="{spine * dpi:.2f}" height="{Hp:.1f}" fill="{PAL["orange"]}"/>')
    css = CSS.replace('@page{size:8.5in 11in;margin:0}', f'@page{{size:{W:.4f}in {H:.4f}in;margin:0}}')
    html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{css}</style></head><body>'
            f'<svg width="{W:.4f}in" height="{H:.4f}in" viewBox="0 0 {Wp:.1f} {Hp:.1f}" style="display:block">'
            f'{"".join(a)}</svg></body></html>')
    return html, W, H, spine


def main():
    os.makedirs(BUILD, exist_ok=True)
    pages = interior()
    html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{TITULO}</title>'
            f'<style>{CSS}</style></head><body>{"".join(pages)}</body></html>')
    open(os.path.join(BUILD, 'interior.html'), 'w').write(html)
    chtml, W, H, spine = cover(len(pages))
    open(os.path.join(BUILD, 'capa.html'), 'w').write(chtml)
    print(f'paginas={len(pages)} capa={W:.3f}x{H:.3f}in lombada={spine:.4f}in')


if __name__ == '__main__':
    main()
