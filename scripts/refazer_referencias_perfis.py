#!/usr/bin/env python3
"""Refaz relatorios/referencias_perfis.csv a partir das fichas lidas.

Entradas (somente leitura): relatorios/fichas_lidas.csv, src/data/perfis,
src/data/categorias e src/assets/img/perfis.
Saida: relatorios/referencias_perfis.csv e, com --renomear, renomeia as imagens
de linhas OK/SEM_ISO gravando relatorios/renomeacao_imagens.csv antes de cada uma.
"""
import csv
import os
import re
import subprocess
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "src" / "data"
IMG = RAIZ / "src" / "assets" / "img" / "perfis"
SAIDA = RAIZ / "relatorios"
RE_COD = re.compile(r"^(SS|DSL|DLS|FE|LT|F)[\s_-]?(\d+)", re.IGNORECASE)
RE_ISO = re.compile(r"(isometrico|iso)", re.IGNORECASE)
CAMPOS = [("peso", "peso", "peso_kg_m"),
          ("area", "area_mm2", "superficie_area_mm2_mml"),
          ("perimetro", "perimetro_mm", "superficie_perimetro_mm2_mml"),
          ("jx", "jx_mm4", "inercia_jx_mm4"),
          ("jy", "jy_mm4", "inercia_jy_mm4")]


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn")


def snake(t):
    t = sem_acento(t).lower()
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", t)).strip("_")


def codigo(txt):
    """Codigo normalizado: SS/DSL 3 digitos, FE 4, F sem hifen; DLS vira DSL."""
    m = RE_COD.match(sem_acento(str(txt)).strip())
    if not m:
        return None
    pre, num = m.group(1).upper(), int(m.group(2))
    pre = "DSL" if pre == "DLS" else pre
    if pre == "F":
        return "f%d" % num
    return "%s-%0*d" % (pre.lower(), 4 if pre == "FE" else 3, num)


def num(v):
    try:
        return float(str(v).replace(",", "."))
    except ValueError:
        return None


def virgula(v):
    return str(v).replace(".", ",") if v not in (None, "") else ""


def carregar(arq):
    with open(arq, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def rastreado(rel):
    r = subprocess.run(["git", "ls-files", "--error-unmatch", rel],
                       cwd=RAIZ, capture_output=True)
    return r.returncode == 0


def main():
    renomear = "--renomear" in sys.argv

    perfis = {}
    for arq in sorted((DATA / "perfis").glob("*.yaml")):
        d = carregar(arq)
        perfis[codigo(d.get("codigo", arq.stem))] = d

    slugs, onde = [], defaultdict(dict)
    for arq in sorted((DATA / "categorias").glob("*.yaml")):
        cat = carregar(arq)
        slug = cat.get("slug", arq.stem)
        slugs.append(slug)
        for bloco in cat.get("blocks", []):
            if bloco.get("tipo") != "profiles":
                continue
            for g in bloco.get("grupos", []):
                for c in g.get("codigos", []):
                    onde[codigo(c)][slug] = g.get("label") or "X"
    for k in onde:
        for s, v in onde[k].items():
            onde[k][s] = v if s == "pele-vidro" else "X"

    # fichas lidas (uma por desenho)
    fichas = {}
    with open(SAIDA / "fichas_lidas.csv", encoding="utf-8-sig", newline="") as f:
        rd = csv.reader(f, delimiter=";")
        next(rd)
        for r in rd:
            r += [""] * (9 - len(r))
            fichas[r[0]] = dict(zip(
                ["arquivo", "cod", "descricao", "peso", "area_mm2", "perimetro_mm",
                 "jx_mm4", "jy_mm4", "status"], r))

    # arquivos de imagem por codigo do arquivo
    desenhos = defaultdict(list)
    isos = defaultdict(list)
    for arq in sorted(p.name for p in IMG.iterdir() if p.is_file()):
        k = codigo(arq)
        if k is None:
            continue
        (isos if RE_ISO.search(arq) else desenhos)[k].append(arq)

    # nomes novos por desenho
    novo = {}
    for k, arqs in desenhos.items():
        for a in arqs:
            fi = fichas[a]
            cod_fi = codigo(fi["cod"])
            novo[a] = "%s-%s.jpg" % (cod_fi, snake(fi["descricao"]))
    contagem = defaultdict(list)
    for a, n in novo.items():
        contagem[n.lower()].append(a)

    linhas, plano = [], []
    for k in sorted(set(desenhos) | set(perfis), key=lambda c: (re.sub(r"[\d-]", "", c), c)):
        arqs = desenhos.get(k, [])
        d = perfis.get(k)
        fi = fichas[arqs[0]] if arqs else None
        status = "OK"
        if not arqs:
            status = "SEM_DESENHO"
        elif any(codigo(fichas[a]["cod"]) != k for a in arqs):
            status = "CODIGO_DIFERENTE"
        elif any(len(contagem[novo[a].lower()]) > 1 for a in arqs) or len(arqs) > 1:
            status = "COLISAO"
        elif not isos.get(k):
            status = "SEM_ISO"
        elif len(isos[k]) > 1:
            status = "COLISAO"

        div = []
        if d and fi and status != "CODIGO_DIFERENTE":
            for nome, ch, cy in CAMPOS:
                a, b = fi[ch], d.get(cy)
                if a == "" and b is None:
                    continue
                if num(a) is None or b is None or abs(num(a) - float(b)) > 1e-6:
                    div.append("%s %s x %s" % (nome, virgula(a) or "(vazio)",
                                               virgula(b) if b is not None else "(vazio)"))
            if snake(fi["descricao"]) != snake(d.get("descricao") or ""):
                div.append("descricao %s x %s" % (fi["descricao"], d.get("descricao") or "(vazio)"))

        nn = novo[arqs[0]] if arqs and status != "COLISAO" else ""
        niso = nn.replace(".jpg", "-isometrico.jpg") if nn else ""
        if status == "COLISAO" and arqs:
            nn = " | ".join(sorted({novo[a] for a in arqs}))
            niso = ""
        linhas.append(
            [k, fi["descricao"] if fi else (d.get("descricao") or "" if d else ""),
             virgula(fi["peso"]) if fi else "", virgula(fi["area_mm2"]) if fi else "",
             virgula(fi["perimetro_mm"]) if fi else "", virgula(fi["jx_mm4"]) if fi else "",
             virgula(fi["jy_mm4"]) if fi else ""]
            + [onde.get(k, {}).get(s, "") for s in slugs]
            + ["", "SIM" if d else "NAO", " | ".join(div),
               ", ".join(arqs), ", ".join(isos.get(k, [])), nn, niso, status])
        if status in ("OK", "SEM_ISO"):
            plano.append((arqs[0], nn))
            if isos.get(k):
                plano.append((isos[k][0], niso))

    cab = (["codigo", "descricao", "peso_kg_m", "area_mm2", "perimetro_mm", "jx_mm4", "jy_mm4"]
           + slugs + ["aplicacao_observacao", "yaml_existe", "divergencia_yaml",
                      "arquivo_desenho_atual", "arquivo_iso_atual", "nome_novo_desenho",
                      "nome_novo_iso", "status"])
    with open(SAIDA / "referencias_perfis.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(cab)
        w.writerows(linhas)
    print("%d linhas" % len(linhas))

    if not renomear:
        return
    de_para = SAIDA / "renomeacao_imagens.csv"
    novo_arq = not de_para.exists()
    n = 0
    with open(de_para, "a", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        if novo_arq:
            w.writerow(["nome_antigo", "nome_novo"])
        for antigo, nome in plano:
            if antigo == nome:
                continue
            w.writerow([antigo, nome])
            f.flush()
            ori, dst = IMG / antigo, IMG / nome
            if dst.exists() and antigo.lower() != nome.lower():
                print("COLISAO com existente, nao renomeado:", antigo, "->", nome)
                continue
            if antigo.lower() == nome.lower():
                tmp = IMG / ("tmp_" + antigo)
                passos = [(ori, tmp), (tmp, dst)]
            else:
                passos = [(ori, dst)]
            rel = ori.relative_to(RAIZ).as_posix()
            git = rastreado(rel)
            for a, b in passos:
                if git:
                    subprocess.run(["git", "mv", str(a), str(b)], cwd=RAIZ, check=True)
                else:
                    os.rename(a, b)
            n += 1
    print("renomeados:", n)


if __name__ == "__main__":
    main()
