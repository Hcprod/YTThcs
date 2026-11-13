"""Versao Kindle (e-book colorido, layout fixo) do livro.

python3 ebook.py html   -> build/ebook.html (paginas coloridas)
node render_ebook.js    -> build/ebook_img/*.png + capa
python3 ebook.py pack   -> build/ebook-kindle.epub + build/capa-kindle.jpg
"""
import os
import sys
import uuid
import zipfile
from datetime import date

from config import TITULO, SUBTITULO, AUTOR, ANO
from book import (CSS, BUILD, PERSONAGENS, CAPITULOS, FINAL, svg, scene_gallery, scene_final,
                  bubble_text, clip_art, ground)
from art import carambola, pinhao, redemoinho, pitanga, caju, jabuticaba

M = 'color'
EXTRA_CSS = """
.ebook{padding:0.45in}
.ebook .textbox{background:#fffaf0}
.ebook .chip{background:#ffd23f}
"""


def page(body):
    return f'<section class="page ebook">{body}</section>'


def p_creditos():
    return page(f'''<div class="center small" style="justify-content:flex-end;padding-bottom:0.6in">
<p><b>{TITULO}</b><br>{SUBTITULO}</p>
<p>Criação: {AUTOR}<br>© {ANO} {AUTOR}. Todos os direitos reservados.</p>
<p>Esta é uma obra original. Os personagens, o Pomar da Serra Dourada e as histórias<br>foram criados para este livro. As lendas do folclore brasileiro que inspiraram<br>alguns capítulos (Saci, Iara e Curupira) são de domínio público e foram recontadas livremente.</p>
<p>Fontes tipográficas: Fredoka e Nunito (SIL Open Font License).</p>
</div>''')


def p_turma():
    itens = ''.join(f'<p style="margin-bottom:0.09in;font-size:14pt;line-height:1.35"><b>{nome}</b> — {desc}</p>'
                    for _, nome, desc in PERSONAGENS)
    spot = svg(pitanga(120, 95, 0.36, M, 'joy', 4.5) + caju(300, 95, 0.36, M, 'happy', 4.5)
               + jabuticaba(470, 100, 0.36, M, 'happy', 4.5, notebook=False), 600, 170, 'spot-svg')
    return page(f'''<div class="textbox"><span class="chip">Bem-vindo!</span>
<h1>Conheça a turma do Pomar da Serra Dourada</h1>
<p style="font-size:14pt">Lá no alto da serra existe um pomar onde as frutas falam, brincam e vivem aventuras. Venha conhecer cada um deles!</p>
{itens}
<div class="spot" style="height:1.6in">{spot}</div></div>''')


def p_galeria(kind, nome, desc):
    return page(svg(scene_gallery(kind, M)) + f'<div class="caption">{nome}<small>{desc}</small></div>')


def p_cap_texto(cap):
    paras = ''.join(f'<p>{t}</p>' for t in cap['texto'])
    return page(f'''<div class="textbox"><span class="chip">Capítulo {cap["n"]}</span>
<h1>{cap["titulo"]}</h1>{paras}<div class="spot" style="height:2.0in">{svg(cap["spot"](M), 600, 220, "spot-svg")}</div></div>''')


def p_cap_arte(cap):
    return page(svg(cap['cena'](M)) + f'<div class="caption">Capítulo {cap["n"]} · {cap["titulo"]}</div>')


def p_final_texto():
    paras = ''.join(f'<p>{t}</p>' for t in FINAL)
    spot = svg(redemoinho(300, 110, 0.42, M, 4.5, expr='joy'), 600, 220, 'spot-svg')
    return page(f'''<div class="textbox"><span class="chip">Epílogo</span>
<h1>Histórias debaixo do Pé de Laranja</h1>{paras}<div class="spot" style="height:2.2in">{spot}</div></div>''')


def p_fim():
    a = [bubble_text(350, 300, 'Fim!', 150, M, 'orange', 14)]
    a.append('<text x="350" y="400" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="30">…ou será que a aventura continua?</text>')
    a.append(ground(700, M))
    a.append(carambola(200, 610, 0.5, M, 'happy', 5.5))
    a.append(pinhao(500, 590, 0.5, M, 'joy', 5.5, prop='book'))
    return page(svg(clip_art(''.join(a), M)))


def pages():
    ps = [p_creditos(), p_turma()]
    for k, nome, desc in PERSONAGENS:
        ps.append(p_galeria(k, nome, desc))
    for cap in CAPITULOS:
        ps += [p_cap_texto(cap), p_cap_arte(cap)]
    ps += [p_final_texto(), page(svg(scene_final(M)) + '<div class="caption">Boa noite, Pomar da Serra Dourada!</div>'),
           p_fim()]
    return ps


def build_html():
    ps = pages()
    html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}{EXTRA_CSS}</style></head>'
            f'<body>{"".join(ps)}</body></html>')
    open(os.path.join(BUILD, 'ebook.html'), 'w').write(html)
    print('paginas do e-book:', len(ps))


def pack():
    from PIL import Image
    imgdir = os.path.join(BUILD, 'ebook_img')
    files = sorted(f for f in os.listdir(imgdir) if f.startswith('p') and f.endswith('.png'))
    W, H = 1600, 2071
    jpgs = []
    for fn in ['cover.png'] + files:
        im = Image.open(os.path.join(imgdir, fn)).convert('RGB').resize((W, H), Image.LANCZOS)
        name = fn.replace('.png', '.jpg')
        im.save(os.path.join(imgdir, name), 'JPEG', quality=88, optimize=True)
        jpgs.append(name)
    # capa separada para o campo "Capa do e-book" do KDP
    # KDP prefere capa 1600 x 2560 (proporcao 1,6): completa com ceu em cima e grama embaixo
    im = Image.open(os.path.join(imgdir, 'cover.jpg')).convert('RGB')
    top, bot = im.getpixel((40, 6)), im.getpixel((40, H - 7))
    pad = (2560 - H) // 2
    capa = Image.new('RGB', (W, 2560), top)
    capa.paste(Image.new('RGB', (W, 2560 - pad - H), bot), (0, pad + H))
    capa.paste(im, (0, pad))
    capa.save(os.path.join(BUILD, 'capa-kindle.jpg'), 'JPEG', quality=90, dpi=(300, 300))

    book_id = 'urn:uuid:' + str(uuid.uuid5(uuid.NAMESPACE_URL, TITULO))
    out = os.path.join(BUILD, 'ebook-kindle.epub')
    z = zipfile.ZipFile(out, 'w')
    z.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
    z.writestr('META-INF/container.xml', '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>''')
    manifest, spine, nav_items = [], [], []
    for i, j in enumerate(jpgs):
        z.write(os.path.join(imgdir, j), f'OEBPS/img/{j}', compress_type=zipfile.ZIP_DEFLATED)
        pid = f'pg{i:02d}'
        alt = 'Capa' if i == 0 else f'Página {i}'
        xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="pt-BR" xml:lang="pt-BR">
<head><meta charset="UTF-8"/><meta name="viewport" content="width={W}, height={H}"/><title>{alt}</title>
<style>html,body{{margin:0;padding:0;width:{W}px;height:{H}px}}img{{display:block;width:{W}px;height:{H}px}}</style></head>
<body><img src="img/{j}" alt="{alt}"/></body></html>'''
        z.writestr(f'OEBPS/{pid}.xhtml', xhtml)
        props = ' properties="cover-image"' if i == 0 else ''
        manifest.append(f'<item id="img{i:02d}" href="img/{j}" media-type="image/jpeg"{props}/>')
        manifest.append(f'<item id="{pid}" href="{pid}.xhtml" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="{pid}"/>')
    # sumario
    marcos = [('Capa', 0), ('Conheça a turma', 2)]
    base = 3 + len(PERSONAGENS)
    for k, cap in enumerate(CAPITULOS):
        marcos.append((f'Capítulo {cap["n"]}: {cap["titulo"]}', base + 2 * k))
    marcos.append(('Epílogo', base + 2 * len(CAPITULOS)))
    for t, idx in marcos:
        nav_items.append(f'<li><a href="pg{idx:02d}.xhtml">{t}</a></li>')
    z.writestr('OEBPS/nav.xhtml', f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="pt-BR" xml:lang="pt-BR">
<head><meta charset="UTF-8"/><title>Sumário</title></head>
<body><nav epub:type="toc" id="toc"><h1>Sumário</h1><ol>{''.join(nav_items)}</ol></nav>
<nav epub:type="landmarks"><ol><li><a epub:type="cover" href="pg00.xhtml">Capa</a></li>
<li><a epub:type="bodymatter" href="pg02.xhtml">Início</a></li></ol></nav></body></html>''')
    manifest.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')
    z.writestr('OEBPS/content.opf', f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="pt-BR" prefix="rendition: http://www.idpf.org/vocab/rendition/#">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">{book_id}</dc:identifier>
<dc:title>{TITULO}</dc:title>
<dc:creator>{AUTOR}</dc:creator>
<dc:language>pt-BR</dc:language>
<dc:date>{date.today().isoformat()}</dc:date>
<meta property="dcterms:modified">{date.today().isoformat()}T00:00:00Z</meta>
<meta property="rendition:layout">pre-paginated</meta>
<meta property="rendition:orientation">portrait</meta>
<meta property="rendition:spread">none</meta>
<meta name="cover" content="img00"/>
<meta name="fixed-layout" content="true"/>
<meta name="original-resolution" content="{W}x{H}"/>
<meta name="book-type" content="children"/>
<meta name="orientation-lock" content="portrait"/>
<meta name="RegionMagnification" content="true"/>
</metadata>
<manifest>{''.join(manifest)}</manifest>
<spine>{''.join(spine)}</spine>
</package>''')
    z.close()
    print('ok', out, f'{os.path.getsize(out) / 1e6:.1f} MB', len(jpgs), 'paginas')


if __name__ == '__main__':
    os.makedirs(BUILD, exist_ok=True)
    if sys.argv[1:] == ['pack']:
        pack()
    else:
        build_html()
