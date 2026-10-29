"""Gera o site estático do Catálogo Técnico em /docs a partir de src/data + src/templates.

Corrige nomes de imagem (padrão minúsculo), valida o catálogo e só então regenera docs/,
preservando hist/, ESTADO_SESSAO.md, PLANO.md e ROTEIRO.md.

Uso: python src/build.py   (executar a partir da raiz do repositório)
"""
import csv
import os
import re
import shutil
import sys
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from padroes import RE_ISO, campos_faltando, chave_codigo, chave_ordem, nome_padrao, nome_valido  # noqa: E402
from validar_catalogo import validar  # noqa: E402

SRC = os.path.join(ROOT, "src")
DATA = os.path.join(SRC, "data")
DOCS = os.path.join(ROOT, "docs")
IMG_PERFIS = os.path.join(SRC, "assets", "img", "perfis")
RENOMEACAO_CSV = os.path.join(ROOT, "relatorios", "renomeacao_imagens.csv")

# Itens de docs/ que NAO sao gerados pelo build e sobrevivem a cada rodada
# (governanca do projeto). Todo o resto de docs/ e apagado e regenerado.
PRESERVAR = ["hist", "ESTADO_SESSAO.md", "PLANO.md", "ROTEIRO.md"]

# Camadas de marca a publicar nesta rodada de build.
# Ordem de trabalho combinada: Solução completa e validada primeiro,
# Blindex entra depois (segunda passada de tema sobre os mesmos dados).
MARCAS_ATIVAS = ["solucao"]

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
        if nome_valido(fname):
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
                    ("d", "arquivo de imagem fora do padrão")):
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


def anota_navegacao(perfis, categorias, marcas):
    """Pagina propria de cada perfil (perfis/{codigo minusculo}.html), sistemas onde aparece
    (a partir dos blocos profiles das categorias) e ordem para anterior/proximo."""
    usado = {}
    ordem_cat = {}  # slug da categoria -> chaves de codigo na ordem em que a pagina do sistema lista
    for cat_slug, cat in sorted(categorias.items(), key=lambda kv: kv[1]["ordem"]):
        pagina = None
        for marca_slug in MARCAS_ATIVAS:
            produto = marcas[marca_slug]["produtos"].get(cat_slug)
            if produto:
                pagina = (produto["nome"], f"{marca_slug}/{produto['page_slug']}.html")
                break
        if not pagina:
            continue
        for b in cat.get("blocks", []):
            if b.get("tipo") != "profiles":
                continue
            for g in b.get("grupos", []):
                for c in g.get("codigos", []):
                    usado.setdefault(chave_codigo(c), []).append(
                        dict(slug=cat_slug, nome=pagina[0], pagina=pagina[1]))
                    ordem_cat.setdefault(cat_slug, []).append(chave_codigo(c))
    for lista in ordem_cat.values():  # vizinhos por sistema: mesma chave unica de ordem
        lista.sort(key=chave_ordem)
    por_chave = {chave_codigo(p["codigo"]): p for p in perfis.values()}
    for p in perfis.values():
        k = chave_codigo(p["codigo"])
        p["arquivo"] = k
        p["pagina"] = f"perfis/{k}.html"
        p["usado_em"] = usado.get(k, [])

    def viz(chave):
        q = por_chave[chave]
        return dict(codigo=q["codigo"], pagina=q["pagina"])

    for p in perfis.values():
        k = p["arquivo"]
        p["viz_cat"] = {}
        for u in p["usado_em"]:
            lista = ordem_cat[u["slug"]]
            i = lista.index(k)
            p["viz_cat"][u["slug"]] = dict(
                nome=u["nome"], pagina=u["pagina"],
                ant=viz(lista[i - 1]) if i > 0 else None,
                prox=viz(lista[i + 1]) if i < len(lista) - 1 else None)
    return sorted(perfis.values(), key=_ordem_codigo)


def inicio(base_url, marca_slug=None):
    """Primeiro nivel da trilha. Hoje e sempre o Inicio da Solucao; quando houver Blindex,
    e aqui que o Inicio passa a depender da marca (marca_slug)."""
    return dict(label="Início", href=base_url + "index.html")


def descr_curta(p, limite=30):
    d = (p.get("descricao") or "").strip()
    return d if len(d) <= limite else d[:limite - 1].rstrip() + "…"


def valida_marcas(marcas):
    """Marca publicada precisa de logo existente em src/; marca ativa precisa estar publicada.
    A marca nao publicada (blindex) so guarda o caminho do logo, sem aparecer em pagina."""
    for slug in MARCAS_ATIVAS:
        if not marcas[slug].get("publicada"):
            raise SystemExit(f"Build interrompido: marca '{slug}' esta em MARCAS_ATIVAS mas nao esta publicada em marcas.yaml.")
    for slug, m in marcas.items():
        if m.get("publicada") and not os.path.isfile(os.path.join(SRC, m["logo"])):
            raise SystemExit(f"Build interrompido: logo da marca '{slug}' nao encontrado em src/{m['logo']}.")
        if not os.path.isfile(os.path.join(SRC, m["logo"])):
            print(f"AVISO: logo da marca nao publicada '{slug}' ausente em src/{m['logo']}")


def limpa_docs():
    """Apaga o conteudo de docs/ preservando os itens de PRESERVAR."""
    os.makedirs(DOCS, exist_ok=True)
    for nome in os.listdir(DOCS):
        if nome in PRESERVAR:
            continue
        caminho = os.path.join(DOCS, nome)
        if os.path.isdir(caminho):
            shutil.rmtree(caminho)
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

    # normaliza categorias em cada perfil para lista (alguns podem vir com 1 item)
    for p in perfis.values():
        p.setdefault("categorias", [])

    verifica_imagens_perfis(perfis)
    valida_catalogo()
    anota_perfis(perfis)
    ordena_categorias(categorias)
    ordem_perfis = anota_navegacao(perfis, categorias, marcas)

    env = Environment(loader=FileSystemLoader(os.path.join(SRC, "templates")), autoescape=False)
    env.filters["categoria_titulo"] = lambda slug: categorias.get(slug, {}).get("titulo", slug)
    env.filters["br_num"] = br_num

    limpa_docs()

    nav_groups = {}
    for slug, cat in sorted(categorias.items(), key=lambda kv: kv[1]["ordem"]):
        nav_groups.setdefault(cat["nav_group"], []).append(cat)

    def base_ctx(base_url, marca_slug, current_page):
        marca = marcas.get(marca_slug) if marca_slug else None
        return dict(
            base_url=base_url,
            marca_slug=marca_slug,
            marcas=marcas,
            marcas_ativas=MARCAS_ATIVAS,
            sidebar_marca=marca,
            pc=marca["color"] if marca else "#5B6470",
            tint=marca["tint"] if marca else "#F1F0EC",
            nav_groups=nav_groups,
            current_page=current_page,
            logo=marcas[marca_slug or MARCAS_ATIVAS[0]]["logo"],
            logo_alt=marcas[marca_slug or MARCAS_ATIVAS[0]]["logo_alt"],
        )

    def render(template_name, out_path, **ctx):
        full_out = os.path.join(DOCS, out_path)
        os.makedirs(os.path.dirname(full_out), exist_ok=True)
        html = env.get_template(template_name).render(**ctx)
        with open(full_out, "w", encoding="utf-8") as f:
            f.write(html)

    # ---- páginas de marca (capa + produtos) ----
    for marca_slug in MARCAS_ATIVAS:
        marca = marcas[marca_slug]
        is_root = marca_slug == "solucao"
        base_url = "" if is_root else "../"
        capa_path = "index.html" if is_root else f"{marca_slug}/index.html"
        current_page = "index.html" if is_root else f"{marca_slug}/index.html"

        produtos_da_marca = []
        for cat_slug, cat in sorted(categorias.items(), key=lambda kv: kv[1]["ordem"]):
            produto = marca["produtos"].get(cat_slug)
            if produto:
                produtos_da_marca.append(produto)

        ctx = base_ctx(base_url, marca_slug, current_page)
        ctx.update(page_title=f"Capa {marca['label']}", produtos=produtos_da_marca,
                    total_perfis=len(perfis))
        render("index.html", capa_path, **ctx)

        for cat_slug, cat in categorias.items():
            produto = marca["produtos"].get(cat_slug)
            if not produto:
                continue
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
                perfis=perfis,
                total_categorias=len(marca["produtos"]),
            )
            render("product.html", page_rel, **ctx)

    # ---- biblioteca de perfis (neutra de marca) ----
    grupos_compartilhamento = {}
    for codigo, fp in perfis.items():
        key = tuple(sorted(fp.get("categorias", [])))
        grupos_compartilhamento.setdefault(key, []).append(codigo)
    grupos_list = [
        dict(categorias=[categorias.get(c, {}).get("titulo", c) for c in key], codigos=sorted(codigos, key=chave_ordem))
        for key, codigos in grupos_compartilhamento.items()
    ]

    ctx = base_ctx("", None, "biblioteca-perfis.html")
    ini = inicio("")
    ctx.update(
        trilha=[ini, dict(label="Biblioteca de perfis", href="biblioteca-perfis.html")],
        voltar=ini,
        page_title="Mapa geral de perfis",
        biblioteca=biblioteca,
        perfis=dict(sorted(perfis.items())),
        perfis_ordenados=ordem_perfis,
        filtros=[dict(slug=s, titulo=c["titulo"]) for s, c in sorted(categorias.items(), key=lambda kv: kv[1]["ordem"])
                 if any(s in p["categorias"] for p in perfis.values())],
        grupos_compartilhamento=grupos_list,
    )
    render("biblioteca-perfis.html", "biblioteca-perfis.html", **ctx)

    # ---- uma pagina por perfil ----
    for i, fp in enumerate(ordem_perfis):
        ctx = base_ctx("../", None, fp["pagina"])
        ini = inicio("../")
        bib = dict(label="Biblioteca de perfis", href="../biblioteca-perfis.html")
        ctx.update(
            trilha=[ini, bib, dict(label=f"{fp['codigo']} {descr_curta(fp)}".strip(), href=f"{fp['arquivo']}.html")],
            voltar=bib,
            page_title=f"{fp['codigo']} — {fp.get('descricao', '')}",
            fp=fp,
            anterior=ordem_perfis[i - 1] if i > 0 else None,
            proximo=ordem_perfis[i + 1] if i < len(ordem_perfis) - 1 else None,
            categorias_perfil=[categorias.get(c, {}).get("titulo", c) for c in fp["categorias"]],
        )
        render("perfil.html", fp["pagina"], **ctx)

    # ---- linha de selantes (neutra de marca) ----
    ctx = base_ctx("", None, "selantes.html")
    ini = inicio("")
    ctx.update(trilha=[ini, dict(label="Linha de Selantes", href="selantes.html")], voltar=ini,
               page_title="Linha de Selantes", selantes=selantes, pc="#C41E2A", tint="#FBE9EA")
    render("selantes.html", "selantes.html", **ctx)

    # ---- assets ----
    # logos de marcas nao publicadas ficam so na fonte (nao vao para docs/)
    nao_publicados = {os.path.normpath(os.path.join(SRC, m["logo"])) for m in marcas.values() if not m.get("publicada")}
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(DOCS, "assets"),
                    ignore=lambda d, nomes: [n for n in nomes if os.path.normpath(os.path.join(d, n)) in nao_publicados])

    print(f"Build concluído. Marcas publicadas: {MARCAS_ATIVAS}. Perfis: {len(perfis)}. Categorias: {len(categorias)}.")


if __name__ == "__main__":
    main()
