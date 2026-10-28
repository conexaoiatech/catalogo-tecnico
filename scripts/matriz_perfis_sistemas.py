#!/usr/bin/env python3
"""Matriz perfil x categoria x imagens (somente leitura).

Cruza src/data/perfis/*.yaml, src/data/categorias/*.yaml e as imagens de
src/assets/img/perfis. Gera relatorios/matriz_perfis_sistemas.md.
"""
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "src" / "data"
IMG = RAIZ / "src" / "assets" / "img" / "perfis"
SAIDA = RAIZ / "relatorios"
RE_COD = re.compile(r"^([a-z]+)[\s_-]?(\d+)", re.IGNORECASE)
RE_ISO = re.compile(r"(?<![a-z])(isometrico|isometric|iso)(?![a-z])", re.IGNORECASE)


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn")


def chave(codigo):
    """SS-014, ss_014, SS014 -> SS14 ; F-98 / F98 -> F98."""
    m = RE_COD.match(sem_acento(str(codigo)).strip())
    if not m:
        return None
    return m.group(1).upper() + str(int(m.group(2)))


def snake(t):
    t = sem_acento(t).lower()
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", t)).strip("_")


def carregar(arq):
    with open(arq, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main():
    perfis = {}
    for arq in sorted((DATA / "perfis").glob("*.yaml")):
        d = carregar(arq)
        k = chave(d.get("codigo", arq.stem))
        perfis[k] = d

    # categoria -> codigos (blocos profiles) ; une com perfil.categorias
    cats_do_perfil = defaultdict(set)
    refs_cat = defaultdict(set)  # chave -> {codigo como escrito}
    for arq in sorted((DATA / "categorias").glob("*.yaml")):
        cat = carregar(arq)
        slug = cat.get("slug", arq.stem)
        for bloco in cat.get("blocks", []):
            if bloco.get("tipo") != "profiles":
                continue
            for g in bloco.get("grupos", []):
                for cod in g.get("codigos", []):
                    cats_do_perfil[chave(cod)].add(slug)
                    refs_cat[chave(cod)].add(str(cod))
    for k, d in perfis.items():
        for c in d.get("categorias") or []:
            cats_do_perfil[k].add(c)

    # imagens
    imagens = defaultdict(list)  # chave -> [pasta/arquivo]
    sem_chave = []
    nao_imagem = []
    for arq in sorted(p for p in IMG.rglob("*") if p.is_file()):
        rel = arq.relative_to(IMG).as_posix()
        if arq.suffix.lower() not in (".jpg", ".jpeg"):
            nao_imagem.append(rel)
            continue
        k = chave(arq.stem)
        if k is None:
            sem_chave.append(rel)
        else:
            imagens[k].append(rel)

    # 6a
    linhas = []
    for k, d in perfis.items():
        cod = d.get("codigo", k)
        desc = d.get("descricao") or ""
        base = "%s-%s" % (cod, snake(desc)) if desc else "%s-(sem_descricao)" % cod
        cats = sorted(cats_do_perfil.get(k, []))
        linhas.append((cod, desc or "(sem descricao)", cats, len(cats),
                       imagens.get(k, []), base + ".jpg", base + "-isometrico.jpg"))
    linhas.sort(key=lambda r: (-r[3], r[0]))

    md = ["# Matriz perfil x categoria x imagens", "",
          "Fonte: src/data/perfis, src/data/categorias, src/assets/img/perfis. "
          "Chave de cruzamento: letras + numero sem zeros a esquerda "
          "(SS-014 = ss_014 = SS014; F-98 = F98).", "",
          "## a. Perfis (por qtd de categorias)", "",
          "| codigo | nome no YAML | categorias | qtd_cat | imagens encontradas | nome padrao proposto |",
          "|---|---|---|---|---|---|"]
    for cod, desc, cats, n, imgs, p1, p2 in linhas:
        md.append("| %s | %s | %s | %d | %s | %s<br>%s |" % (
            cod, desc, ", ".join(cats) or "-", n,
            "<br>".join(imgs) or "-", p1, p2))

    md += ["", "## b. Perfis referenciados em categoria sem YAML de perfil", ""]
    b = sorted(k for k in refs_cat if k not in perfis)
    md += ["- %s (categorias: %s)" % (", ".join(sorted(refs_cat[k])),
                                      ", ".join(sorted(cats_do_perfil[k]))) for k in b]
    if not b:
        md.append("(nenhum)")

    md += ["", "## c. Perfis com YAML mas sem nenhuma imagem", ""]
    c = [r for r in linhas if not r[4]]
    md += ["- %s (%s)" % (r[0], r[1]) for r in c]
    if not c:
        md.append("(nenhum)")

    md += ["", "## d. Imagens cujo codigo nao tem YAML de perfil", ""]
    d_itens = []
    for k in sorted(imagens):
        if k not in perfis:
            d_itens += ["- %s (codigo %s)" % (i, k) for i in imagens[k]]
    # SEM_CODIGO pelo padrao do inventario (so SS/DSL), mas com chave lenient
    for k, lst in imagens.items():
        if k in perfis and not re.match(r"^(SS|DSL)\d", k):
            d_itens += ["- %s (fora do padrao SS/DSL; casa com YAML %s)" %
                        (i, perfis[k].get("codigo")) for i in lst]
    d_itens += ["- %s (sem codigo)" % i for i in sem_chave]
    d_itens += ["- %s (nao e imagem)" % i for i in nao_imagem]
    md += d_itens or ["(nenhuma)"]

    SAIDA.mkdir(exist_ok=True)
    (SAIDA / "matriz_perfis_sistemas.md").write_text("\n".join(md) + "\n",
                                                      encoding="utf-8")
    print("%d perfis; %d imagens" % (len(perfis), sum(map(len, imagens.values()))))


if __name__ == "__main__":
    main()
