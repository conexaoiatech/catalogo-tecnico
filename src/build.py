"""Gera o site estático do Catálogo Técnico em /docs a partir de src/data + src/templates.

Uso: python src/build.py   (executar a partir da raiz do repositório)
"""
import os
import re
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
DATA = os.path.join(SRC, "data")
DOCS = os.path.join(ROOT, "docs")
IMG_PERFIS = os.path.join(SRC, "assets", "img", "perfis")

# Camadas de marca a publicar nesta rodada de build.
# Ordem de trabalho combinada: Solução completa e validada primeiro,
# Blindex entra depois (segunda passada de tema sobre os mesmos dados).
MARCAS_ATIVAS = ["solucao"]

# {CODIGO}-{detalhe_snake_case}.jpg  ou  {CODIGO}-{detalhe_snake_case}-isometrico.jpg
IMG_PATTERN = re.compile(r"^[A-Z]{2,3}-\d{3,4}-[a-z0-9_]+(-isometrico)?\.jpg$")


def _infere_nome_correto(fname, codigos_validos):
    """Tenta inferir a forma correta de um nome de imagem fora do padrão.

    Retorna o novo nome se for possível corrigir com segurança, ou None
    caso o código do perfil ou o detalhe não possam ser inferidos sem
    adivinhação (ex: extensão diferente de .jpg, que pode indicar um
    formato de arquivo real diferente do nome).
    """
    nome, ext = os.path.splitext(fname)
    if ext.lower() != ".jpg":
        return None

    codigo = next((c for c in codigos_validos if nome.upper().startswith(c.upper() + "-")), None)
    if codigo is None:
        return None

    resto = nome[len(codigo) + 1:]
    if not resto:
        return None

    isometrico = bool(re.search(r"[-_]isometric[oa]?$", resto, re.IGNORECASE))
    if isometrico:
        resto = re.sub(r"[-_]isometric[oa]?$", "", resto, flags=re.IGNORECASE)

    detalhe = re.sub(r"[^a-zA-Z0-9]+", "_", resto).strip("_").lower()
    if not detalhe:
        return None

    novo = f"{codigo}-{detalhe}{'-isometrico' if isometrico else ''}.jpg"
    return novo if IMG_PATTERN.match(novo) else None


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
    """Varre as imagens de perfis e corrige automaticamente nomes fora do
    padrão {CODIGO}-{detalhe}[-isometrico].jpg, atualizando também a
    referência correspondente no YAML do perfil. Interrompe o build se
    encontrar algum arquivo que não possa ser corrigido com segurança.
    """
    perfis_dir = perfis_dir or os.path.join(DATA, "perfis")
    if not os.path.isdir(img_dir):
        return

    codigos_validos = sorted(
        {p.get("codigo") for p in perfis.values() if p.get("codigo")},
        key=len, reverse=True,
    )

    corrigidos = []
    nao_corrigidos = []

    for fname in sorted(os.listdir(img_dir)):
        if IMG_PATTERN.match(fname):
            continue

        novo = _infere_nome_correto(fname, codigos_validos)
        old_path = os.path.join(img_dir, fname)
        if novo is None or os.path.exists(os.path.join(img_dir, novo)):
            nao_corrigidos.append(fname)
            continue

        os.rename(old_path, os.path.join(img_dir, novo))
        corrigidos.append((fname, novo))

        codigo = next((c for c in codigos_validos if fname.upper().startswith(c.upper() + "-")), None)
        for slug, p in perfis.items():
            if p.get("codigo") != codigo:
                continue
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

    # normaliza categorias em cada perfil para lista (alguns podem vir com 1 item)
    for p in perfis.values():
        p.setdefault("categorias", [])

    verifica_imagens_perfis(perfis)

    env = Environment(loader=FileSystemLoader(os.path.join(SRC, "templates")), autoescape=False)
    env.filters["categoria_titulo"] = lambda slug: categorias.get(slug, {}).get("titulo", slug)
    env.filters["br_num"] = br_num

    if os.path.exists(DOCS):
        shutil.rmtree(DOCS)
    os.makedirs(DOCS)

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
            ctx.update(
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
        dict(categorias=[categorias.get(c, {}).get("titulo", c) for c in key], codigos=sorted(codigos))
        for key, codigos in grupos_compartilhamento.items()
    ]

    ctx = base_ctx("", None, "biblioteca-perfis.html")
    ctx.update(
        page_title="Mapa geral de perfis",
        biblioteca=biblioteca,
        perfis=dict(sorted(perfis.items())),
        perfis_completos=[c for c, p in perfis.items() if p.get("status") == "completo"],
        grupos_compartilhamento=grupos_list,
    )
    render("biblioteca-perfis.html", "biblioteca-perfis.html", **ctx)

    # ---- linha de selantes (neutra de marca) ----
    ctx = base_ctx("", None, "selantes.html")
    ctx.update(page_title="Linha de Selantes", selantes=selantes, pc="#C41E2A", tint="#FBE9EA")
    render("selantes.html", "selantes.html", **ctx)

    # ---- assets ----
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(DOCS, "assets"))

    print(f"Build concluído. Marcas publicadas: {MARCAS_ATIVAS}. Perfis: {len(perfis)}. Categorias: {len(categorias)}.")


if __name__ == "__main__":
    main()
