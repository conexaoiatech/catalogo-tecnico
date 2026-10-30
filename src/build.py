"""Gera o site estático do Catálogo Técnico em /docs a partir de src/data + src/templates.

Corrige nomes de imagem (padrão minúsculo), valida o catálogo e só então regenera docs/,
preservando hist/, ESTADO_SESSAO.md, PLANO.md e ROTEIRO.md.

Uso: python src/build.py   (executar a partir da raiz do repositório)
"""
import csv
import io
import os
import re
import shutil
import sys
import yaml
import numpy as np
from PIL import Image
from jinja2 import Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from padroes import IGNORAR_ARQUIVOS, RE_ISO, campos_faltando, chave_codigo, chave_ordem, nome_padrao, nome_valido  # noqa: E402
from validar_catalogo import validar  # noqa: E402

SRC = os.path.join(ROOT, "src")
DATA = os.path.join(SRC, "data")
DOCS = os.path.join(ROOT, "docs")
IMG_PERFIS = os.path.join(SRC, "assets", "img", "perfis")
RENOMEACAO_CSV = os.path.join(ROOT, "relatorios", "renomeacao_imagens.csv")

# Itens de docs/ que NAO sao gerados pelo build e sobrevivem a cada rodada
# (governanca do projeto). Todo o resto de docs/ e apagado e regenerado.
PRESERVAR = ["hist", "ESTADO_SESSAO.md", "PLANO.md", "ROTEIRO.md"]

# Marcas publicadas: as que tem publicada: true em src/data/marcas.yaml.
MARCA_PADRAO = "solucao"  # tema das paginas sem marca propria (selantes)

def _registra_renomeacao(antigo, novo):
    """Grava de-para em relatorios/renomeacao_imagens.csv ANTES de renomear."""
    os.makedirs(os.path.dirname(RENOMEACAO_CSV), exist_ok=True)
    existe = os.path.exists(RENOMEACAO_CSV)
    with open(RENOMEACAO_CSV, "a", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        if not existe:
            w.writerow(["nome_antigo", "nome_novo"])
        w.writerow([antigo, novo])


def _substitui_referencia_yaml(yaml_path, antigo, novo):
    if not os.path.exists(yaml_path):
        return
    with open(yaml_path, "r", encoding="utf-8", newline="") as f:
        texto = f.read()
    if antigo not in texto:
        return
    with open(yaml_path, "w", encoding="utf-8", newline="") as f:
        f.write(texto.replace(antigo, novo))


def verifica_imagens_perfis(perfis, img_dir=IMG_PERFIS, perfis_dir=None):
    """Corrige nomes de imagem fora do padrao de scripts/padroes.py
    ({codigo minusculo}-{detalhe}[-isometrico].jpg) quando o codigo (pelo prefixo
    do arquivo) e a descricao do YAML do perfil permitem montar o nome; grava o
    de-para em relatorios/renomeacao_imagens.csv e atualiza imagem_desenho /
    imagem_isometrica no YAML. Arquivo sem como montar o nome interrompe o build.
    """
    perfis_dir = perfis_dir or os.path.join(DATA, "perfis")
    if not os.path.isdir(img_dir):
        return

    por_codigo = {}
    for slug, p in perfis.items():
        k = chave_codigo(p.get("codigo", ""))
        if k:
            por_codigo[k] = (slug, p)

    corrigidos, nao_corrigidos = [], []
    for fname in sorted(os.listdir(img_dir)):
        if nome_valido(fname) or fname in IGNORAR_ARQUIVOS:
            continue
        nome, ext = os.path.splitext(fname)
        k = chave_codigo(nome) if ext.lower() == ".jpg" else None
        slug, p = por_codigo.get(k, (None, None))
        novo = nome_padrao(k, p.get("descricao"), bool(RE_ISO.search(nome[len(k):]))) if p else None
        if novo is None or os.path.exists(os.path.join(img_dir, novo)):
            nao_corrigidos.append(fname)
            continue

        _registra_renomeacao(fname, novo)
        os.rename(os.path.join(img_dir, fname), os.path.join(img_dir, novo))
        corrigidos.append((fname, novo))
        _substitui_referencia_yaml(os.path.join(perfis_dir, f"{slug}.yaml"), fname, novo)
        for campo in ("imagem_desenho", "imagem_isometrica"):
            if p.get(campo) == fname:
                p[campo] = novo

    if corrigidos:
        print("Correção automática de nomes de imagem em src/assets/img/perfis/:")
        for antigo, novo in corrigidos:
            print(f"  {antigo}  ->  {novo}")
    else:
        print("Checagem de nomes de imagem: todos os arquivos já seguem o padrão.")

    if nao_corrigidos:
        print("ATENÇÃO: arquivos fora do padrão que NÃO foram corrigidos automaticamente (decisão manual necessária):")
        for fname in nao_corrigidos:
            print(f"  {fname}")
        raise SystemExit(
            "Build interrompido: revise manualmente os arquivos listados acima em "
            f"{img_dir} antes de rodar o build novamente."
        )


def valida_catalogo():
    """Roda a validacao (a, b, c, d) de scripts/validar_catalogo.py; erro -> sai com codigo 1
    antes de apagar ou gerar qualquer coisa em docs/."""
    erros, n_perfis, n_citados, _avisos = validar()
    print(f"Validação: {n_perfis} perfis, {n_citados} códigos citados em categorias.")
    for k, nome in (("a", "código citado sem YAML de perfil"),
                    ("b", "categorias do perfil != categorias que o citam"),
                    ("c", "imagem referenciada não existe"),
                    ("d", "arquivo de imagem fora do padrão"),
                    ("e", "perfis_estruturais fora da lista da categoria")):
        print(f"  ({k}) {'OK' if not erros[k] else 'ERRO - ' + nome}")
        for e in erros[k]:
            print(f"      {e}")
    if any(erros.values()):
        raise SystemExit("Build interrompido: validação do catálogo falhou; docs/ não foi alterado.")


def anota_perfis(perfis, img_dir=IMG_PERFIS):
    """Campos calculados lidos pelos templates: completo (scripts/padroes.py), faltando e
    tem_imagem / tem_iso (arquivo existe, comparacao exata de maiusculas). Imprime AVISOs."""
    arquivos = set(os.listdir(img_dir)) if os.path.isdir(img_dir) else set()
    for codigo, p in sorted(perfis.items()):
        p["faltando"] = campos_faltando(p)
        p["completo"] = not p["faltando"]
        p["tem_imagem"] = bool(p.get("imagem_desenho")) and p["imagem_desenho"] in arquivos
        p["tem_iso"] = bool(p.get("imagem_isometrica")) and p["imagem_isometrica"] in arquivos
        origem = p["imagem_isometrica"] if p["tem_iso"] else (p["imagem_desenho"] if p["tem_imagem"] else None)
        p["thumb"] = ("assets/img/perfis-thumb/" + origem) if origem else None
        if not p["tem_imagem"]:
            print(f"AVISO: {p.get('codigo', codigo)} sem imagem de desenho existente em {img_dir}")
        if p["faltando"]:
            print(f"AVISO: {p.get('codigo', codigo)} incompleto, falta: {', '.join(p['faltando'])}")


def _ordem_codigo(p):
    return chave_ordem(p["codigo"])


def ordena_categorias(categorias):
    """Ordena, em memoria, os codigos de cada grupo dos blocos profiles pela chave unica de
    scripts/padroes.py (grupos mantidos). A ordem escrita nos YAML nao importa."""
    for cat in categorias.values():
        for b in cat.get("blocks", []):
            if b.get("tipo") == "profiles":
                for g in b.get("grupos", []):
                    g["codigos"] = sorted(g.get("codigos", []), key=chave_ordem)


def perfis_da_marca(perfis, categorias, marcas, marca_slug):
    """Copias dos perfis usados nos sistemas da marca, com a navegacao da marca: pagina propria
    ({marca}/perfis/{codigo}.html), sistemas onde aparece (so os da marca) e vizinhos por sistema.
    Devolve (dict como o de perfis, lista na ordem unica de codigo)."""
    produtos = marcas[marca_slug]["produtos"]
    usado, ordem_cat = {}, {}
    for cat_slug, cat in sorted(categorias.items(), key=lambda kv: kv[1]["ordem"]):
        produto = produtos.get(cat_slug)
        if not produto:
            continue
        pagina = f"{marca_slug}/{produto['page_slug']}.html"
        for b in cat.get("blocks", []):
            if b.get("tipo") != "profiles":
                continue
            for g in b.get("grupos", []):
                for c in g.get("codigos", []):
                    k = chave_codigo(c)
                    usado.setdefault(k, []).append(dict(slug=cat_slug, nome=produto["nome"], pagina=pagina))
                    ordem_cat.setdefault(cat_slug, []).append(k)
    for lista in ordem_cat.values():  # vizinhos por sistema: mesma chave unica de ordem
        lista.sort(key=chave_ordem)

    pm = {}
    for chave, p in perfis.items():
        k = chave_codigo(p["codigo"])
        if k not in usado:
            continue
        q = dict(p)
        q["arquivo"] = k
        q["pagina"] = f"{marca_slug}/perfis/{k}.html"
        q["usado_em"] = usado[k]
        q["cats_marca"] = [u["slug"] for u in usado[k]]
        q["nomes_marca"] = [u["nome"] for u in usado[k]]
        pm[chave] = q
    por_chave = {q["arquivo"]: q for q in pm.values()}

    def viz(chave):
        q = por_chave[chave]
        return dict(codigo=q["codigo"], pagina=q["pagina"])

    for q in pm.values():
        k = q["arquivo"]
        q["viz_cat"] = {}
        for u in q["usado_em"]:
            lista = ordem_cat[u["slug"]]
            i = lista.index(k)
            q["viz_cat"][u["slug"]] = dict(
                nome=u["nome"], pagina=u["pagina"],
                ant=viz(lista[i - 1]) if i > 0 else None,
                prox=viz(lista[i + 1]) if i < len(lista) - 1 else None)
    return pm, sorted(pm.values(), key=_ordem_codigo)


def inicio(base_url, marca_slug):
    """Primeiro nivel da trilha: o Inicio da propria marca."""
    return dict(label="Início", href=f"{base_url}{marca_slug}/index.html")


def descr_curta(p, limite=30):
    d = (p.get("descricao") or "").strip()
    return d if len(d) <= limite else d[:limite - 1].rstrip() + "…"


def valida_marcas(marcas):
    """Marca publicada precisa de logo e logo_claro existentes em src/ e de cor, acao e destaque.
    A marca padrao (selantes, entrada) precisa estar publicada."""
    if not marcas.get(MARCA_PADRAO, {}).get("publicada"):
        raise SystemExit(f"Build interrompido: a marca padrao '{MARCA_PADRAO}' precisa estar publicada em marcas.yaml.")
    for slug, m in marcas.items():
        if not m.get("publicada"):
            if not os.path.isfile(os.path.join(SRC, m["logo"])):
                print(f"AVISO: logo da marca nao publicada '{slug}' ausente em src/{m['logo']}")
            continue
        for campo in ("logo", "logo_claro"):
            if not os.path.isfile(os.path.join(SRC, m.get(campo, ""))):
                raise SystemExit(f"Build interrompido: {campo} da marca '{slug}' nao encontrado em src/{m.get(campo)}.")
        for campo in ("color", "acao", "destaque", "tint"):
            if not m.get(campo):
                raise SystemExit(f"Build interrompido: marca '{slug}' sem '{campo}' em marcas.yaml.")


def rgb_csv(hexa):
    hexa = hexa.lstrip("#")
    return ",".join(str(int(hexa[i:i + 2], 16)) for i in (0, 2, 4))


def _ignora_pasta_vazia_em_uso(func, caminho, exc_info):
    """No Windows uma pasta aberta no Explorer (ou em outro programa) nao pode ser removida
    mesmo vazia; tolera isso (o conteudo ja foi apagado e o copytree reaproveita a pasta)."""
    sem_arquivos = not any(files for _r, _d, files in os.walk(caminho))
    if func is os.rmdir and isinstance(exc_info[1], OSError) and sem_arquivos:
        print(f"AVISO: pasta em uso por outro programa, mantida sem arquivos: {os.path.relpath(caminho, ROOT)}")
        return
    raise exc_info[1]


def recorta_ficha(im):
    """Corta as margens brancas da ficha (e a moldura fina da folha), com um respiro pequeno."""
    im = im.convert("RGB")
    g = np.asarray(im.convert("L"))
    alto, larg = g.shape
    escuro = g < 215
    linhas = np.where(escuro.sum(axis=1) > 0.85 * larg)[0]
    colunas = np.where(escuro.sum(axis=0) > 0.55 * alto)[0]
    x0, y0, x1, y1 = 0, 0, larg, alto
    if len(linhas) >= 2 and len(colunas) >= 2 and linhas.max() - linhas.min() > 0.3 * alto:
        x0, x1 = int(colunas.min()) + 5, int(colunas.max()) - 4
        y0, y1 = int(linhas.min()) + 5, int(linhas.max()) - 4
    miolo = g[y0:y1, x0:x1] < 235
    ys, xs = np.where(miolo)
    if len(xs) == 0:
        return im
    pad = max(24, larg // 60)
    cx0, cx1 = max(x0, x0 + int(xs.min()) - pad), min(x1, x0 + int(xs.max()) + pad)
    cy0, cy1 = max(y0, y0 + int(ys.min()) - pad), min(y1, y0 + int(ys.max()) + pad)
    if cx1 - cx0 < 100 or cy1 - cy0 < 100:
        return im
    return im.crop((cx0, cy0, cx1, cy1))


def gera_imagens(perfis):
    """Em docs/: fichas recortadas (mesmo nome do src) e miniaturas isometricas em
    assets/img/perfis-thumb/. Os originais em src nao sao alterados."""
    pasta = os.path.join(DOCS, "assets", "img", "perfis")
    thumbs = os.path.join(DOCS, "assets", "img", "perfis-thumb")
    os.makedirs(thumbs, exist_ok=True)
    n_ficha = n_thumb = 0
    for p in perfis.values():
        if p.get("tem_imagem"):
            with Image.open(os.path.join(IMG_PERFIS, p["imagem_desenho"])) as im:
                recorta_ficha(im).save(os.path.join(pasta, p["imagem_desenho"]), "JPEG", quality=88, optimize=True)
            n_ficha += 1
        origem = p["imagem_isometrica"] if p.get("tem_iso") else (p["imagem_desenho"] if p.get("tem_imagem") else None)
        if origem:
            with Image.open(os.path.join(IMG_PERFIS, origem)) as im:
                im = recorta_ficha(im) if origem == p.get("imagem_desenho") else im.convert("RGB")
                im.thumbnail((520, 520), Image.LANCZOS)
                im.save(os.path.join(thumbs, origem), "JPEG", quality=82, optimize=True)
            n_thumb += 1
    print(f"Imagens: {n_ficha} fichas recortadas e {n_thumb} miniaturas em docs/.")


def gera_logo(origem, destino, largura=640, tirar_fundo_preto=False):
    """Copia otimizada do logo (largura maxima 640, PNG). Com tirar_fundo_preto, o preto vira
    transparencia (alpha = brilho, cor desmisturada), para o logo assentar em qualquer fundo escuro."""
    with Image.open(origem) as im:
        if tirar_fundo_preto or im.width > largura:
            im = im.convert("RGBA")
        if im.width > largura:
            im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
        if tirar_fundo_preto:
            a = np.asarray(im).astype("float32")
            alfa = a[..., :3].max(axis=2) / 255.0
            alfa[alfa < 0.03] = 0
            for c in range(3):
                a[..., c] = np.where(alfa > 0, np.clip(a[..., c] / np.maximum(alfa, 1e-6), 0, 255), 0)
            a[..., 3] = alfa * 255
            im = Image.fromarray(a.astype("uint8"), "RGBA")
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        im.save(destino, "PNG", optimize=True)
    return os.path.getsize(destino)


def gera_logos(marcas):
    for slug, m in marcas.items():
        if not m.get("publicada"):
            continue
        t = gera_logo(os.path.join(SRC, m["logo"]), os.path.join(DOCS, m["logo"]),
                      tirar_fundo_preto=bool(m.get("logo_fundo_preto")))
        if m["logo_claro"] != m["logo"]:
            c = gera_logo(os.path.join(SRC, m["logo_claro"]), os.path.join(DOCS, m["logo_claro"]))
        else:
            c = t
        print(f"Logos da marca {slug}: {m['logo']} {t/1024:.1f} KB, {m['logo_claro']} {c/1024:.1f} KB (impressao).")


def limpa_docs():
    """Apaga o conteudo de docs/ preservando os itens de PRESERVAR."""
    os.makedirs(DOCS, exist_ok=True)
    for nome in os.listdir(DOCS):
        if nome in PRESERVAR:
            continue
        caminho = os.path.join(DOCS, nome)
        if os.path.isdir(caminho):
            shutil.rmtree(caminho, onerror=_ignora_pasta_vazia_em_uso)
        else:
            os.remove(caminho)


def br_num(value):
    """Formata número no padrão BR: milhar com ponto, decimal com vírgula."""
    if value is None:
        return ""
    if isinstance(value, int):
        base, dec = str(value), ""
    elif float(value) == int(value):
        base, dec = str(int(value)), ""
    else:
        s = f"{value}"
        base, dec = s.split(".") if "." in s else (s, "")
    neg = base.startswith("-")
    if neg:
        base = base[1:]
    if len(base) > 3:
        parts = []
        while len(base) > 3:
            parts.insert(0, base[-3:])
            base = base[:-3]
        parts.insert(0, base)
        base = ".".join(parts)
    if neg:
        base = "-" + base
    return base + ("," + dec if dec else "")


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_dir(path):
    out = {}
    for fname in sorted(os.listdir(path)):
        if fname.endswith(".yaml"):
            slug = fname[:-5]
            out[slug] = load_yaml(os.path.join(path, fname))
    return out


def main():
    marcas = load_yaml(os.path.join(DATA, "marcas.yaml"))
    categorias = load_dir(os.path.join(DATA, "categorias"))
    perfis = load_dir(os.path.join(DATA, "perfis"))
    biblioteca = load_yaml(os.path.join(DATA, "biblioteca.yaml"))
    selantes = load_yaml(os.path.join(DATA, "selantes.yaml"))

    valida_marcas(marcas)
    publicadas = [s for s, m in marcas.items() if m.get("publicada")]

    # normaliza categorias em cada perfil para lista (alguns podem vir com 1 item)
    for p in perfis.values():
        p.setdefault("categorias", [])

    verifica_imagens_perfis(perfis)
    valida_catalogo()
    anota_perfis(perfis)
    ordena_categorias(categorias)

    env = Environment(loader=FileSystemLoader(os.path.join(SRC, "templates")), autoescape=False)
    env.filters["categoria_titulo"] = lambda slug: categorias.get(slug, {}).get("titulo", slug)
    env.filters["br_num"] = br_num

    limpa_docs()

    def menu_da_marca(marca_slug, base_url, current_page):
        """Itens do menu: sistemas da marca (ordem das categorias), biblioteca da marca e,
        so na Solucao, selantes."""
        itens = []
        for cat_slug, cat in sorted(categorias.items(), key=lambda kv: kv[1]["ordem"]):
            produto = marcas[marca_slug]["produtos"].get(cat_slug)
            if produto:
                rel = f"{marca_slug}/{produto['page_slug']}.html"
                itens.append(dict(nome=produto["nome"], href=base_url + rel, atual=(current_page == rel)))
        itens.append(dict(nome="Biblioteca de perfis", href=f"{base_url}{marca_slug}/biblioteca-perfis.html",
                          atual=(current_page == f"{marca_slug}/biblioteca-perfis.html"
                                 or str(current_page).startswith(f"{marca_slug}/perfis/"))))
        if marca_slug == "solucao":
            itens.append(dict(nome="Selantes", href=base_url + "selantes.html", atual=(current_page == "selantes.html")))
        return itens

    def base_ctx(base_url, marca_slug, current_page):
        slug = marca_slug or MARCA_PADRAO
        m = marcas[slug]
        return dict(
            base_url=base_url, marca_slug=slug, marca=m, marcas=marcas,
            pc=m["color"], tint=m["tint"], acao=m["acao"], destaque=m["destaque"],
            acao_rgb=rgb_csv(m["acao"]), destaque_rgb=rgb_csv(m["destaque"]),
            current_page=current_page,
            logo=m["logo"], logo_claro=m["logo_claro"], logo_alt=m["logo_alt"], logo_pilula=bool(m.get("logo_pilula")),
            menu=menu_da_marca(slug, base_url, current_page),
            inicio_href=f"{base_url}{slug}/index.html",
            outras_marcas=[dict(label=marcas[o]["label"], href=f"{base_url}{o}/index.html")
                           for o in publicadas if o != slug],
            entrada_href=base_url + "index.html",
        )

    def render(template_name, out_path, **ctx):
        full_out = os.path.join(DOCS, out_path)
        os.makedirs(os.path.dirname(full_out), exist_ok=True)
        html = env.get_template(template_name).render(**ctx)
        with open(full_out, "w", encoding="utf-8") as f:
            f.write(html)

    resumo = []
    for marca_slug in publicadas:
        marca = marcas[marca_slug]
        perfis_m, ordem_m = perfis_da_marca(perfis, categorias, marcas, marca_slug)
        cats_marca = [(cs, c) for cs, c in sorted(categorias.items(), key=lambda kv: kv[1]["ordem"])
                      if cs in marca["produtos"]]

        # ---- capa da marca ----
        cards = []
        for cat_slug, cat in cats_marca:
            produto = marca["produtos"][cat_slug]
            n = sum(len(g.get("codigos", [])) for b in cat.get("blocks", []) if b.get("tipo") == "profiles"
                    for g in b.get("grupos", []))
            cards.append(dict(nome=produto["nome"], subtitulo=produto.get("subtitulo", ""),
                              href=f"{produto['page_slug']}.html", n_perfis=n, ordem=len(cards) + 1))
        ctx = base_ctx("../", marca_slug, f"{marca_slug}/index.html")
        ctx.update(page_title=f"Capa {marca['label']}", cards=cards, produtos=cards, total_perfis=len(perfis_m))
        render("index.html", f"{marca_slug}/index.html", **ctx)

        # ---- paginas de sistema ----
        for cat_slug, cat in cats_marca:
            produto = marca["produtos"][cat_slug]
            page_rel = f"{marca_slug}/{produto['page_slug']}.html"
            ctx = base_ctx("../", marca_slug, page_rel)
            ini = inicio("../", marca_slug)
            ctx.update(
                trilha=[ini, dict(label=produto["nome"], href="../" + page_rel)],
                voltar=ini,
                page_title=produto["nome"],
                produto=produto,
                categoria=cat,
                slug=cat_slug,
                perfis=perfis_m,
                total_categorias=len(marca["produtos"]),
                badges=[b for b in cat.get("badges", []) if b not in produto.get("ocultar_badges", [])],
            )
            render("product.html", page_rel, **ctx)

        # ---- biblioteca da marca ----
        grupos = {}
        for fp in perfis_m.values():
            grupos.setdefault(tuple(fp["nomes_marca"]), []).append(fp["codigo"])
        grupos_list = [dict(categorias=list(nomes), codigos=sorted(cods, key=chave_ordem))
                       for nomes, cods in grupos.items()]
        ctx = base_ctx("../", marca_slug, f"{marca_slug}/biblioteca-perfis.html")
        ini = inicio("../", marca_slug)
        ctx.update(
            trilha=[ini, dict(label="Biblioteca de perfis", href="biblioteca-perfis.html")],
            voltar=ini,
            page_title="Mapa geral de perfis",
            biblioteca=biblioteca,
            perfis=perfis_m,
            perfis_ordenados=ordem_m,
            filtros=[dict(slug=cs, titulo=marca["produtos"][cs]["nome"]) for cs, _c in cats_marca
                     if any(cs in p["cats_marca"] for p in perfis_m.values())],
            grupos_compartilhamento=grupos_list,
        )
        render("biblioteca-perfis.html", f"{marca_slug}/biblioteca-perfis.html", **ctx)

        # ---- uma pagina por perfil ----
        for i, fp in enumerate(ordem_m):
            ctx = base_ctx("../../", marca_slug, fp["pagina"])
            ini = inicio("../../", marca_slug)
            bib = dict(label="Biblioteca de perfis", href="../biblioteca-perfis.html")
            ctx.update(
                trilha=[ini, bib, dict(label=f"{fp['codigo']} {descr_curta(fp)}".strip(), href=f"{fp['arquivo']}.html")],
                voltar=bib,
                page_title=f"{fp['codigo']} — {fp.get('descricao', '')}",
                fp=fp,
                anterior=ordem_m[i - 1] if i > 0 else None,
                proximo=ordem_m[i + 1] if i < len(ordem_m) - 1 else None,
                categorias_perfil=fp["nomes_marca"],
            )
            render("perfil.html", fp["pagina"], **ctx)
        resumo.append((marca_slug, len(marca["produtos"]), len(perfis_m)))

    # ---- entrada: escolha de marca ----
    ctx = base_ctx("", None, "index.html")
    ctx.update(page_title="Escolha a marca", entrada=True,
               cards_marca=[dict(slug=sl, nome=marcas[sl]["label"], logo=marcas[sl]["logo"], alt=marcas[sl]["logo_alt"],
                                 pilula=bool(marcas[sl].get("logo_pilula")), cor=marcas[sl]["color"],
                                 descricao=marcas[sl].get("entrada_texto", ""), href=f"{sl}/index.html",
                                 n_sistemas=n_s, n_perfis=n_p)
                            for sl, n_s, n_p in resumo])
    render("entrada.html", "index.html", **ctx)

    # ---- links antigos: redirecionam para a Solucao ----
    padrao = MARCA_PADRAO
    _pm, ordem_padrao = perfis_da_marca(perfis, categorias, marcas, padrao)
    for fp in ordem_padrao:
        render("redirect.html", f"perfis/{fp['arquivo']}.html", page_title=f"{fp['codigo']} — redirecionando",
               destino=f"../{padrao}/perfis/{fp['arquivo']}.html", mantem_query=True,
               texto=f"Esta página mudou para {marcas[padrao]['label']}")
    render("redirect.html", "biblioteca-perfis.html", page_title="Biblioteca de perfis — redirecionando",
           destino=f"{padrao}/biblioteca-perfis.html", mantem_query=False,
           texto=f"A biblioteca de perfis mudou para {marcas[padrao]['label']}")

    # ---- linha de selantes (so Solucao) ----
    ctx = base_ctx("", padrao, "selantes.html")
    ini = inicio("", padrao)
    ctx.update(trilha=[ini, dict(label="Linha de Selantes", href="selantes.html")], voltar=ini,
               page_title="Linha de Selantes", selantes=selantes)
    render("selantes.html", "selantes.html", **ctx)

    # ---- assets ----
    # logos de marcas nao publicadas ficam so na fonte (nao vao para docs/)
    nao_publicados = {os.path.normpath(os.path.join(SRC, m["logo"])) for m in marcas.values() if not m.get("publicada")}
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(DOCS, "assets"), dirs_exist_ok=True,
                    ignore=lambda d, nomes: list(nomes) if os.path.basename(d) == "marcas" else
                    [n for n in nomes if n in IGNORAR_ARQUIVOS or os.path.normpath(os.path.join(d, n)) in nao_publicados])
    gera_logos(marcas)
    gera_imagens(perfis)

    # ---- PDF por sistema e marca (docs/pdf/<marca>/<page_slug>.pdf) ----
    if "--sem-pdf" not in sys.argv:
        import build_pdf
        build_pdf.gerar()

    for sl, n_s, n_p in resumo:
        print(f"Marca {sl}: {n_s} sistemas, {n_p} perfis.")
    print(f"Build concluído. Marcas publicadas: {publicadas}. Perfis: {len(perfis)}. Categorias: {len(categorias)}.")


if __name__ == "__main__":
    main()
