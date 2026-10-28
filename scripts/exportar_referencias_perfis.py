#!/usr/bin/env python3
"""Planilha de referencias perfil x categoria (somente leitura dos YAML).

Gera relatorios/referencias_perfis.csv (; UTF-8 BOM) e
relatorios/referencias_perfis_guia.md (grupos existentes por categoria).
"""
import csv
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "src" / "data"
IMG = RAIZ / "src" / "assets" / "img" / "perfis"
SAIDA = RAIZ / "relatorios"
RE_COD = re.compile(r"^(SS|DSL|FE|LT|F)[\s_-]?(\d+)", re.IGNORECASE)
SEM_ROTULO = "(sem rotulo)"


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn")


def chave(codigo):
    """SS-014, ss_014, SS014 -> SS14 ; F-98 / F98 -> F98."""
    m = RE_COD.match(sem_acento(str(codigo)).strip())
    if not m:
        return None
    return m.group(1).upper() + str(int(m.group(2)))


def carregar(arq):
    with open(arq, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main():
    perfis = {}
    for arq in sorted((DATA / "perfis").glob("*.yaml")):
        d = carregar(arq)
        perfis[chave(d.get("codigo", arq.stem))] = d

    cats = []  # (slug, titulo, [rotulos de grupo na ordem])
    onde = defaultdict(lambda: defaultdict(list))  # chave -> slug -> [grupos]
    for arq in sorted((DATA / "categorias").glob("*.yaml")):
        cat = carregar(arq)
        slug = cat.get("slug", arq.stem)
        grupos = []
        for bloco in cat.get("blocks", []):
            if bloco.get("tipo") != "profiles":
                continue
            for g in bloco.get("grupos", []):
                rotulo = g.get("label") or SEM_ROTULO
                grupos.append(rotulo)
                for cod in g.get("codigos", []):
                    onde[chave(cod)][slug].append(rotulo)
        cats.append((slug, cat.get("titulo", slug), grupos))
    slugs = [c[0] for c in cats]

    imagens = defaultdict(list)
    cod_img = {}
    for arq in sorted(p for p in IMG.rglob("*") if p.is_file()):
        if arq.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            continue
        m = RE_COD.match(arq.stem)
        if not m:
            continue
        k = chave(arq.stem)
        imagens[k].append(arq.relative_to(IMG).as_posix())
        cod_img.setdefault(k, "%s-%s" % (m.group(1).upper(), m.group(2)))

    linhas = []
    for k in set(perfis) | set(imagens) | set(onde):
        d = perfis.get(k)
        cod = str(d.get("codigo")) if d else cod_img.get(k, k)
        cats_perfil = sorted(d.get("categorias") or []) if d else []
        cats_onde = sorted(onde.get(k, {}))
        celulas = [" / ".join(onde[k][s]) if s in onde.get(k, {}) else ""
                   for s in slugs]
        obs = []
        if not d:
            obs.append("SEM_YAML")
        if not imagens.get(k):
            obs.append("SEM_IMAGEM")
        div = ""
        if d:
            div = "SIM" if cats_perfil != cats_onde else "NAO"
        linhas.append([cod, (d.get("descricao") or "") if d else ""] + celulas + [
            ", ".join(cats_perfil), div, ", ".join(imagens.get(k, [])),
            " ".join(obs)])
    linhas.sort(key=lambda r: (re.sub(r"\d+", "", r[0]), int(re.sub(r"\D", "", r[0]) or 0), r[0]))

    SAIDA.mkdir(exist_ok=True)
    with open(SAIDA / "referencias_perfis.csv", "w", encoding="utf-8-sig",
              newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["codigo", "descricao"] + slugs + [
            "categorias_no_perfil", "divergencia", "imagens", "observacao"])
        w.writerows(linhas)

    md = ["# Guia de grupos por categoria", "",
          "Nomes exatos dos grupos em blocks[tipo=profiles].grupos, na ordem.", ""]
    for slug, titulo, grupos in cats:
        md += ["## %s" % titulo, "", "- slug: `%s`" % slug, "- grupos:"]
        md += ["  %d. %s" % (i, g) for i, g in enumerate(grupos, 1)] or ["  (nenhum)"]
        md.append("")
    (SAIDA / "referencias_perfis_guia.md").write_text("\n".join(md), encoding="utf-8")
    print("%d linhas" % len(linhas))


if __name__ == "__main__":
    main()
