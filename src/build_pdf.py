"""Catálogo técnico em PDF (formato catálogo de perfil) — um PDF por sistema e marca.

Lê a fonte única (src/data: marcas, categorias, perfis) e gera docs/pdf/<marca>/<page_slug>.pdf.
Chamado no fim do build.py; também roda sozinho: python src/build_pdf.py
Requisitos: playwright (Chromium), pypdf e pypdfium2.  pip install playwright pypdf pypdfium2  ·  playwright install chromium
Logo de produto (opcional): src/assets/img/produtos/<marca>-<page_slug>.png; sem arquivo, a capa usa o nome em texto.
"""
import base64
import datetime
import io
import os
import sys

import numpy as np
import yaml
from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
DATA = os.path.join(SRC, "data")
DOCS = os.path.join(ROOT, "docs")
IMG_PERFIS = os.path.join(SRC, "assets", "img", "perfis")
IMG_PRODUTOS = os.path.join(SRC, "assets", "img", "produtos")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from padroes import chave_codigo, chave_ordem  # noqa: E402

FABRICANTE = "SOLUÇÃO · FECHAMENTO INTELIGENTE"
SITE = "conexaoiatech.github.io/catalogo-tecnico"


def _yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _b64(im, fmt="PNG", lado=1400):
    im = im.copy()
    im.thumbnail((lado, lado))
    buf = io.BytesIO()
    im.save(buf, fmt)
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(buf.getvalue()).decode()


def _num(v, casas=2):
    if v is None or v == "":
        return None
    try:
        v = float(v)
    except (TypeError, ValueError):
        return str(v)
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def recorta_desenho(path):
    """Desenho cotado da ficha (ver recorta_desenho_img) como data URI PNG."""
    return _b64(recorta_desenho_img(path))


LINHAS_TABELA_FICHA = 3  # a ficha CAD traz sempre 3 linhas de tabela (código/nome, peso/superfície/inércia, valores)


def _linhas_finas(mascara, eixo, limite, espessura_max):
    """Índices de linhas (eixo=1: linhas da imagem; eixo=0: colunas) que cruzam mais que `limite` da imagem e
    formam uma risca FINA (até espessura_max px): a moldura da folha. Barras grossas do perfil não entram."""
    longas = np.where(mascara.sum(eixo) > limite)[0]
    if not len(longas):
        return longas
    finas, inicio = [], 0
    for i in range(1, len(longas) + 1):
        if i == len(longas) or longas[i] != longas[i - 1] + 1:
            if longas[i - 1] - longas[inicio] + 1 <= espessura_max:
                finas.extend(longas[inicio:i])
            inicio = i
    return np.array(finas, dtype=int)


def recorta_desenho_img(path):
    """A ficha CAD traz a tabela no topo: devolve (PIL, tons de cinza) só o desenho cotado, sem a tabela e sem a
    moldura da folha. Regra geral: a tabela são as LINHAS_TABELA_FICHA primeiras faixas de tinta (intervalo de 0,4 %
    da altura entre faixas); o desenho começa na faixa seguinte e o corte leva uma folga, para nenhuma parte do perfil
    nem das cotas ficar de fora. Usado no PDF por sistema e na relação de peças."""
    im = Image.open(path).convert("L")
    g = np.array(im)
    a0 = g < 200
    h, w = a0.shape
    esp = max(12, round(0.006 * max(h, w)))              # moldura: riscas até ~12 px (ficha SS-016 é menor e tem borda de 10 px)
    a = a0.copy()
    a[_linhas_finas(a0, 1, .6 * w, esp), :] = False      # linhas da moldura
    a[:, _linhas_finas(a0, 0, .6 * h, esp)] = False      # laterais da moldura
    linhas = np.where(a.any(1))[0]
    if not len(linhas):
        return im
    faixas, gap = [[linhas[0], linhas[0]]], .004 * h
    for y in linhas[1:]:
        if y - faixas[-1][1] > gap:
            faixas.append([y, y])
        else:
            faixas[-1][1] = y
    if len(faixas) <= LINHAS_TABELA_FICHA:
        return im
    fim_tabela = faixas[LINHAS_TABELA_FICHA - 1][1]
    corpo = a[fim_tabela + 1:]
    ys, xs = np.where(corpo)
    if not len(ys):
        return im
    folga = max(12, round(0.006 * max(h, w)))
    y0 = max(fim_tabela + 1, fim_tabela + 1 + int(ys.min()) - folga)
    y1 = min(h, fim_tabela + 1 + int(ys.max()) + 1 + folga)
    x0, x1 = max(0, int(xs.min()) - folga), min(w, int(xs.max()) + 1 + folga)
    return ImageOps.expand(Image.fromarray(g[y0:y1, x0:x1]), border=20, fill=255)


def _iso(path):
    im = Image.open(path).convert("RGB")
    im.thumbnail((900, 900))
    return _b64(im, "JPEG")


def _ficha(p, produtos_marca):
    def img(campo, fn):
        nome = p.get(campo)
        path = os.path.join(IMG_PERFIS, nome) if nome else None
        return fn(path) if path and os.path.isfile(path) else None

    grupos = []
    for titulo, linhas in [
        ("Massa", [("Peso", _num(p.get("peso_kg_m"), 3), "kg/m")]),
        ("Superfície", [("Área", _num(p.get("superficie_area_mm2_mml")), "mm²"),
                        ("Perímetro", _num(p.get("superficie_perimetro_mm2_mml")), "mm")]),
        ("Inércia", [("Jx", _num(p.get("inercia_jx_mm4")), "mm⁴"), ("Jy", _num(p.get("inercia_jy_mm4")), "mm⁴")]),
    ]:
        linhas = [(r, v, u) for r, v, u in linhas if v is not None]
        if linhas:
            grupos.append((titulo, linhas))
    larg, alt = _num(p.get("largura_ref_mm")), _num(p.get("altura_ref_mm"))
    if larg and alt:
        grupos.append(("Envelope", [("Largura × altura", f"{larg} × {alt}", "mm")]))
    if p.get("material"):
        grupos.append(("Material", [("Tipo", str(p["material"]), "")]))
    return dict(
        codigo=p["codigo"], descricao=p.get("descricao", ""),
        desenho=img("imagem_desenho", recorta_desenho), iso=img("imagem_isometrica", _iso),
        grupos=grupos,
        sistemas=[produtos_marca[c]["nome"] for c in p.get("categorias", []) if c in produtos_marca],
    )


def _pdf(html, path, cab=None, rod=None, url=None, paisagem=False):
    """PDF A4 pelo Chromium. Com url, carrega a página já gerada em docs/ (file://); senão usa o html."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page()
        if url:
            pg.goto(url, wait_until="load")
            pg.wait_for_timeout(300)
        else:
            pg.set_content(html, wait_until="networkidle")
        kw = dict(path=path, format="A4", landscape=paisagem, print_background=True)
        if cab:
            kw.update(display_header_footer=True, header_template=cab, footer_template=rod,
                      margin={"top": "20mm", "bottom": "15mm", "left": "14mm", "right": "14mm"})
        else:
            kw.update(margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        pg.pdf(**kw)
        br.close()


def gerar(saida_dir=os.path.join(DOCS, "pdf")):
    from pypdf import PdfWriter
    marcas = _yaml(os.path.join(DATA, "marcas.yaml"))
    categorias = {f[:-5]: _yaml(os.path.join(DATA, "categorias", f))
                  for f in sorted(os.listdir(os.path.join(DATA, "categorias"))) if f.endswith(".yaml")}
    perfis = {}
    for f in sorted(os.listdir(os.path.join(DATA, "perfis"))):
        if f.endswith(".yaml"):
            p = _yaml(os.path.join(DATA, "perfis", f))
            perfis[chave_codigo(p["codigo"])] = p
    env = Environment(loader=FileSystemLoader(os.path.join(SRC, "templates", "pdf")), autoescape=True)
    rev = datetime.date.today().strftime("%d/%m/%Y")
    tmp = os.path.join(saida_dir, "_tmp")
    os.makedirs(tmp, exist_ok=True)
    gerados = []

    for marca_slug, marca in marcas.items():
        if not marca.get("publicada"):
            continue
        logo = _b64(Image.open(os.path.join(SRC, marca["logo_claro"])), lado=600)
        for cat_slug, cat in sorted(categorias.items(), key=lambda kv: kv[1]["ordem"]):
            produto = marca["produtos"].get(cat_slug)
            if not produto:
                continue
            logo_prod_path = os.path.join(IMG_PRODUTOS, f"{marca_slug}-{produto['page_slug']}.png")
            logo_prod = _b64(Image.open(logo_prod_path)) if os.path.isfile(logo_prod_path) else None
            badges = [b for b in cat.get("badges", []) if b not in produto.get("ocultar_badges", [])]
            blocos, codigos = [], []
            for b in cat.get("blocks", []):
                if b.get("tipo") == "profiles":
                    for g in b.get("grupos", []):
                        for c in g.get("codigos", []):
                            if chave_codigo(c) not in [chave_codigo(x) for x in codigos]:
                                codigos.append(c)
                else:
                    blocos.append(b)
            codigos.sort(key=chave_ordem)
            indice, fichas = [], []
            for c in codigos:
                p = perfis.get(chave_codigo(c))
                if not p:
                    indice.append(dict(codigo=c, descricao="ficha não cadastrada", peso="—"))
                    print(f"AVISO PDF: {marca_slug}/{produto['page_slug']} perfil {c} sem YAML")
                    continue
                indice.append(dict(codigo=p["codigo"], descricao=p.get("descricao", ""),
                                   peso=_num(p.get("peso_kg_m"), 3) or "—"))
                fichas.append(_ficha(p, marca["produtos"]))
            ctx = dict(marca=marca, produto=produto, cat=cat, badges=badges, blocos=blocos, indice=indice,
                       pares=[fichas[i:i + 2] for i in range(0, len(fichas), 2)], logo=logo,
                       logo_prod=logo_prod, rev=rev, fabricante=FABRICANTE, site=SITE)
            capa_pdf = os.path.join(tmp, "capa.pdf")
            corpo_pdf = os.path.join(tmp, "corpo.pdf")
            _pdf(env.get_template("capa.html").render(**ctx), capa_pdf)
            _pdf(env.get_template("corpo.html").render(**ctx), corpo_pdf,
                 cab=env.get_template("cabecalho.html").render(**ctx),
                 rod=env.get_template("rodape.html").render(**ctx))
            destino = os.path.join(saida_dir, marca_slug, f"{produto['page_slug']}.pdf")
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            w = PdfWriter()
            for parte in (capa_pdf, corpo_pdf):
                w.append(parte)
            w.add_metadata({"/Title": f"Catálogo técnico — {produto['nome']}", "/Author": FABRICANTE})
            with open(destino, "wb") as f:
                w.write(f)
            gerados.append((destino, len(w.pages), len(fichas)))
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)
    for d, n, k in gerados:
        print(f"PDF {os.path.relpath(d, ROOT)}  {n} pág  {k} fichas")
    return gerados


def gerar_relacao(marca_slug, marca, rev, pagina_html, saida_dir=os.path.join(DOCS, "pdf")):
    """PDF da relação de peças da marca, A4 retrato: imprime a página docs/<marca>/relacao-pecas.html (já gerada
    pelo build, com o CSS de impressão: 3 perfis por página) com o cabeçalho e o rodapé do fabricante dos PDFs por sistema."""
    from pypdf import PdfWriter
    env = Environment(loader=FileSystemLoader(os.path.join(SRC, "templates", "pdf")), autoescape=True)
    logo = _b64(Image.open(os.path.join(SRC, marca["logo_claro"])), lado=600)
    cab = env.get_template("cabecalho.html").render(marca=marca, logo=logo, produto=dict(nome="Relação de peças"))
    rod = env.get_template("rodape.html").render(marca=marca, fabricante=FABRICANTE, rev=rev, site=SITE)
    destino = os.path.join(saida_dir, marca_slug, "relacao-pecas.pdf")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    bruto = destino + ".tmp"
    _pdf(None, bruto, cab=cab, rod=rod, url="file:///" + pagina_html.replace("\\", "/"))
    w = PdfWriter()
    w.append(bruto)
    w.add_metadata({"/Title": f"Relação de peças — {marca['label']}", "/Author": FABRICANTE})
    with open(destino, "wb") as f:
        w.write(f)
    os.remove(bruto)
    print(f"PDF {os.path.relpath(destino, ROOT)}  {len(w.pages)} pág")
    return destino


def paginas_em_imagem(pdf_path, marca_slug, dpi=150, qualidade=82, saida_dir=os.path.join(DOCS, "assets", "img", "folhear")):
    """Cada página do PDF vira JPG (docs/assets/img/folhear/<marca>/relacao-pecas-<nn>.jpg) para o visualizador
    folheável da biblioteca de perfis. Devolve (caminhos relativos a docs/, total de bytes)."""
    import pypdfium2 as pdfium
    pasta = os.path.join(saida_dir, marca_slug)
    os.makedirs(pasta, exist_ok=True)
    caminhos, total = [], 0
    pdf = pdfium.PdfDocument(pdf_path)
    try:
        for i in range(len(pdf)):
            im = pdf[i].render(scale=dpi / 72).to_pil().convert("RGB")
            nome = f"relacao-pecas-{i + 1:02d}.jpg"
            destino = os.path.join(pasta, nome)
            im.save(destino, "JPEG", quality=qualidade, optimize=True)
            total += os.path.getsize(destino)
            caminhos.append(f"assets/img/folhear/{marca_slug}/{nome}")
    finally:
        pdf.close()
    return caminhos, total


if __name__ == "__main__":
    gerar()
