#!/usr/bin/env python3
"""Valida src/data sem build: YAML de perfil x categoria x imagens.

(a) todo codigo citado em categoria tem YAML de perfil
(b) categorias do perfil = categorias que o citam
(c) imagem_desenho e imagem_isometrica existem em src/assets/img/perfis
(d) nenhum arquivo em perfis fora do padrao minusculo
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "src" / "data"
IMG = RAIZ / "src" / "assets" / "img" / "perfis"
PADRAO = re.compile(r"^[a-z0-9]+(-[a-z0-9_]+)+(-isometrico)?\.jpg$")


def carregar(arq):
    return yaml.safe_load(arq.read_text(encoding="utf-8")) or {}


def main():
    erros = {"a": [], "b": [], "c": [], "d": []}
    perfis = {}
    for arq in sorted((DATA / "perfis").glob("*.yaml")):
        d = carregar(arq)
        perfis[str(d["codigo"]).upper()] = d
    citam = defaultdict(set)
    for arq in sorted((DATA / "categorias").glob("*.yaml")):
        cat = carregar(arq)
        slug = cat.get("slug", arq.stem)
        for bloco in cat.get("blocks", []):
            if bloco.get("tipo") != "profiles":
                continue
            for g in bloco.get("grupos", []):
                for c in g.get("codigos", []):
                    citam[str(c).upper()].add(slug)
    for c in sorted(citam):
        if c not in perfis:
            erros["a"].append(c)
    for c, d in sorted(perfis.items()):
        if set(d.get("categorias") or []) != citam.get(c, set()):
            erros["b"].append("%s: perfil %s x categorias %s" % (
                c, sorted(d.get("categorias") or []), sorted(citam.get(c, set()))))
        for campo in ("imagem_desenho", "imagem_isometrica"):
            n = d.get(campo)
            if not n or not (IMG / n).is_file() or n not in {p.name for p in IMG.iterdir()}:
                erros["c"].append("%s %s: %s" % (c, campo, n))
    for p in sorted(IMG.iterdir()):
        if not PADRAO.match(p.name):
            erros["d"].append(p.name)
    print("perfis: %d  categorias citando perfis: %d codigos" % (len(perfis), len(citam)))
    for k in "abcd":
        print("(%s) %s %s" % (k, "OK" if not erros[k] else "ERRO", erros[k] or ""))
    sys.exit(1 if any(erros.values()) else 0)


if __name__ == "__main__":
    main()
