#!/usr/bin/env python3
"""Valida src/data sem build: YAML de perfil x categoria x imagens.

(a) todo codigo citado em categoria tem YAML de perfil
(b) categorias do perfil = categorias que o citam
(c) imagem_desenho e imagem_isometrica existem em src/assets/img/perfis
(d) nenhum arquivo em perfis fora do padrao (scripts/padroes.py)
(e) todo codigo de perfis_estruturais esta na lista de perfis da propria categoria
"""
import sys
from collections import defaultdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from padroes import IGNORAR_ARQUIVOS, campos_faltando, nome_valido  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "src" / "data"
IMG = RAIZ / "src" / "assets" / "img" / "perfis"


def carregar(arq):
    return yaml.safe_load(arq.read_text(encoding="utf-8")) or {}


def validar(data=DATA, img=IMG):
    """Devolve (erros {a,b,c,d}, n_perfis, n_codigos_citados, avisos {codigo: [campos faltando]})."""
    erros = {"a": [], "b": [], "c": [], "d": [], "e": []}
    perfis = {}
    for arq in sorted((data / "perfis").glob("*.yaml")):
        d = carregar(arq)
        perfis[str(d["codigo"]).upper()] = d
    citam = defaultdict(set)
    for arq in sorted((data / "categorias").glob("*.yaml")):
        cat = carregar(arq)
        slug = cat.get("slug", arq.stem)
        na_categoria = set()
        for bloco in cat.get("blocks", []):
            if bloco.get("tipo") != "profiles":
                continue
            for g in bloco.get("grupos", []):
                for c in g.get("codigos", []):
                    citam[str(c).upper()].add(slug)
                    na_categoria.add(str(c).upper())
        for c in cat.get("perfis_estruturais", []) or []:
            if str(c).upper() not in na_categoria:
                erros["e"].append("%s: %s em perfis_estruturais mas fora da lista da categoria" % (slug, c))
    arquivos = {p.name for p in img.iterdir()} if img.is_dir() else set()
    for c in sorted(citam):
        if c not in perfis:
            erros["a"].append(c)
    for c, d in sorted(perfis.items()):
        if set(d.get("categorias") or []) != citam.get(c, set()):
            erros["b"].append("%s: perfil %s x categorias %s" % (
                c, sorted(d.get("categorias") or []), sorted(citam.get(c, set()))))
        for campo in ("imagem_desenho", "imagem_isometrica"):
            n = d.get(campo)
            if not n or n not in arquivos:
                erros["c"].append("%s %s: %s" % (c, campo, n))
    for nome in sorted(arquivos):
        if nome not in IGNORAR_ARQUIVOS and not nome_valido(nome):
            erros["d"].append(nome)
    avisos = {c: campos_faltando(d) for c, d in sorted(perfis.items()) if campos_faltando(d)}
    return erros, len(perfis), len(citam), avisos


def main():
    erros, n_perfis, n_citados, avisos = validar()
    print("perfis: %d  categorias citando perfis: %d codigos" % (n_perfis, n_citados))
    for k in "abcde":
        print("(%s) %s %s" % (k, "OK" if not erros[k] else "ERRO", erros[k] or ""))
    for c, faltam in avisos.items():
        print("AVISO %s incompleto: falta %s" % (c, ", ".join(faltam)))
    sys.exit(1 if any(erros.values()) else 0)


if __name__ == "__main__":
    main()
