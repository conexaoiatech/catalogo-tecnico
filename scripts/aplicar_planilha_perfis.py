#!/usr/bin/env python3
"""Aplica relatorios/referencias_perfis_rev.csv nos YAML de perfil e categoria.

Passos: ajusta a planilha (-> referencias_perfis_aplicada.csv), renomeia imagens,
atualiza src/data/perfis e src/data/categorias. A planilha revisada vem do Excel
em cp850, separador ';' e virgula decimal.
"""
import csv
import os
import re
import subprocess
import unicodedata
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "src" / "data"
IMG = RAIZ / "src" / "assets" / "img" / "perfis"
REL = RAIZ / "relatorios"
SLUGS = ["pele-vidro", "persianas", "portas-minimalistas", "portas-robustas", "ripado", "sacada"]
SEM_BLOCO = set()  # categorias sem blocks[tipo=profiles] (nenhuma desde o passo 2d)
RE_COD = re.compile(r"^(SS|DSL|FE|LT|F)[\s_-]?(\d+)", re.IGNORECASE)
RE_ISO = re.compile(r"(isometrico|iso)", re.IGNORECASE)
DESCRICAO_PESSOA = {
    "fe-0202": "Bagete Passante",
    "fe-0203": "Capa Coluna Lateral",
    "fe-0204": "Acab. Vertical Meio Coluna - Passante",
    "fe-0205": "Montante do Quadro",
    "fe-0207": "Acab. Vertical Meio Coluna - Colante",
    "fe-0208": "Baguete Vedação Vertical",
    "lt-077": "Cantoneira Acab. Lateral",
}
CAMPOS = [("peso_kg_m", 2), ("superficie_area_mm2_mml", 3), ("superficie_perimetro_mm2_mml", 4),
          ("inercia_jx_mm4", 5), ("inercia_jy_mm4", 6)]
ORDEM = ["codigo", "descricao", "categorias", "peso_kg_m", "superficie_area_mm2_mml",
         "superficie_perimetro_mm2_mml", "inercia_jx_mm4", "inercia_jy_mm4"]


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def snake(t):
    t = sem_acento(t).lower()
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", t)).strip("_")


def codigo(txt):
    """Chave minuscula: ss-108, dsl-001, fe-0202, lt-077, f98."""
    m = RE_COD.match(sem_acento(str(txt)).strip())
    if not m:
        return None
    pre, n = m.group(1).lower(), int(m.group(2))
    if pre == "f":
        return "f%d" % n
    return "%s-%0*d" % (pre, 4 if pre == "fe" else 3, n)


def numero(v):
    v = v.strip()
    return float(v.replace(",", ".")) if v else None


def rastreado(rel):
    return subprocess.run(["git", "ls-files", "--error-unmatch", rel], cwd=RAIZ,
                          capture_output=True).returncode == 0


def git_ou_rename(a, b):
    if rastreado(a.relative_to(RAIZ).as_posix()):
        subprocess.run(["git", "mv", str(a), str(b)], cwd=RAIZ, check=True)
    else:
        os.rename(a, b)


def atualizar_categorias(linhas, i_cat):
    """YAML de categoria: edicao textual para nao reformatar o resto do arquivo."""
    for i, slug in zip(i_cat, SLUGS):
        if slug in SEM_BLOCO:
            continue
        queridos = [r[0] for r in linhas if r[i].strip()]
        arq = DATA / "categorias" / ("%s.yaml" % slug)
        txt = arq.read_text(encoding="utf-8").split("\n")
        ini = next(n for n, l in enumerate(txt) if l == "  tipo: profiles")
        fim = next((n for n in range(ini + 1, len(txt)) if txt[n].startswith("- id:")), len(txt))
        saiu, entrou, grupo_ult, novos = [], [], {}, []
        grupo_atual, rotulo = -1, {}
        saida = txt[:ini]
        presentes = []
        for l in txt[ini:fim]:
            m = re.match(r"^  - label: (.*)$", l)
            if m:
                grupo_atual += 1
                rotulo[grupo_atual] = m.group(1).strip()
            m = re.match(r"^    - (\S+)\s*$", l)
            if m and grupo_atual >= 0:
                k = codigo(m.group(1))
                if k not in queridos:
                    saiu.append(m.group(1))
                    continue
                presentes.append(k)
                grupo_ult[grupo_atual] = len(saida)
            saida.append(l)
        alvo = next((g for g, t in rotulo.items() if t == ("Exclusivos" if slug == "pele-vidro" else "null")),
                    None)
        ins = grupo_ult.get(alvo)
        if ins is None:
            ins = max(grupo_ult.values())
        novos = [k for k in queridos if k not in presentes]
        for k in reversed(novos):
            saida.insert(ins + 1, "    - " + k.upper())
        entrou = [k.upper() for k in novos]
        saida += txt[fim:]
        arq.write_text("\n".join(saida), encoding="utf-8")
        print("categoria %s: entraram %s; sairam %s" % (slug, entrou, saiu))


def main():
    with open(REL / "referencias_perfis_rev.csv", encoding="cp850", newline="") as f:
        rd = list(csv.reader(f, delimiter=";"))
    cab, linhas = rd[0], rd[1:]
    print("planilha: %d linhas" % len(linhas))
    print("cabecalho:", ";".join(cab))
    i_ped = cab.index("nome_novo_desenho")
    i_piso = cab.index("nome_novo_iso")
    i_cat = [cab.index(s) for s in SLUGS]

    # 4. ajustes na planilha
    for r in linhas:
        k = codigo(r[0])
        r[0] = k
        if r[i_cat[0]].strip().lower() in ("exclusivo", "exclusivos"):
            r[i_cat[0]] = "X"
        if k in DESCRICAO_PESSOA:
            r[1] = DESCRICAO_PESSOA[k]
        r[i_ped] = "%s-%s.jpg" % (k, snake(r[1]))
        r[i_piso] = "%s-%s-isometrico.jpg" % (k, snake(r[1]))
    with open(REL / "referencias_perfis_aplicada.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(cab)
        w.writerows(linhas)

    # 5. renomear imagens
    atuais = {}
    for p in sorted(IMG.iterdir()):
        k = codigo(p.name) if p.suffix.lower() == ".jpg" else None
        if k:
            atuais.setdefault((k, bool(RE_ISO.search(p.name))), []).append(p.name)
    de_para = REL / "renomeacao_imagens.csv"
    feitas, colisoes, sem_img = [], [], []
    with open(de_para, "a", encoding="utf-8-sig", newline="") as log:
        wl = csv.writer(log, delimiter=";")
        for r in linhas:
            k = r[0]
            for iso, alvo in ((False, r[i_ped]), (True, r[i_piso])):
                arqs = atuais.get((k, iso), [])
                if len(arqs) != 1:
                    sem_img.append((k, iso, arqs))
                    continue
                antigo = arqs[0]
                if antigo == alvo:
                    continue
                ori, dst = IMG / antigo, IMG / alvo
                if dst.exists() and antigo.lower() != alvo.lower():
                    colisoes.append((antigo, alvo))
                    continue
                wl.writerow([antigo, alvo])
                log.flush()
                if antigo.lower() == alvo.lower():
                    tmp = IMG / ("tmp_" + antigo)
                    git_ou_rename(ori, tmp)
                    git_ou_rename(tmp, dst)
                else:
                    git_ou_rename(ori, dst)
                feitas.append((antigo, alvo))
    print("renomeacoes feitas: %d" % len(feitas))
    for a, b in feitas:
        print("  %s -> %s" % (a, b))
    print("colisoes:", colisoes)
    print("sem imagem unica:", sem_img)

    # 6. YAML de perfil
    alterados, criados, divergencias = [], [], {}
    existentes = {}
    for arq in (DATA / "perfis").glob("*.yaml"):
        d = yaml.safe_load(arq.read_text(encoding="utf-8")) or {}
        existentes[codigo(d.get("codigo", arq.stem))] = (arq, d)
    for r in linhas:
        k = r[0]
        marcadas = [s for s, i in zip(SLUGS, i_cat) if r[i].strip() and s not in SEM_BLOCO]
        arq, d = existentes.get(k, (None, None))
        novo = d is None
        if novo:
            d = {"codigo": k.upper()}
            arq = DATA / "perfis" / ("%s.yaml" % k.upper())
        antes = dict(d)
        div = []
        if r[1].strip():
            if d.get("descricao") and d["descricao"] != r[1]:
                div.append("descricao: YAML anterior '%s'" % d["descricao"])
            d["descricao"] = r[1]
        if k != "ss-002":  # excecao definida pela pessoa: valores do YAML prevalecem
            for campo, i in CAMPOS:
                v = numero(r[i])
                if v is None:
                    continue
                ant = d.get(campo)
                if ant is not None and abs(float(ant) - v) > 1e-6:
                    div.append("%s: YAML anterior %s" % (campo, ant))
                d[campo] = v
        d["imagem_desenho"] = r[i_ped]
        d["imagem_isometrica"] = r[i_piso]
        antigas = d.get("categorias") or []
        d["categorias"] = [c for c in antigas if c in marcadas] + [c for c in SLUGS if c in marcadas and c not in antigas]
        if novo:
            d["status"] = "pendente"
        if div:
            texto = "Divergencias aplicadas (ficha individual prevalece): " + "; ".join(div) + "."
            d["nota"] = (d["nota"] + " " + texto) if d.get("nota") else texto
            divergencias[k] = div
        ordenado = {c: d[c] for c in ORDEM if c in d}
        ordenado.update({c: v for c, v in d.items() if c not in ordenado and c not in
                         ("imagem_desenho", "imagem_isometrica", "status", "nota")})
        for c in ("imagem_desenho", "imagem_isometrica", "status", "nota"):
            if c in d:
                ordenado[c] = d[c]
        if novo or ordenado != antes or list(ordenado) != list(antes):
            arq.write_text(yaml.safe_dump(ordenado, allow_unicode=True, sort_keys=False),
                           encoding="utf-8")
            (criados if novo else alterados).append(k)
    print("YAML criados (%d): %s" % (len(criados), criados))
    print("YAML alterados (%d): %s" % (len(alterados), alterados))
    print("divergencias registradas (%d):" % len(divergencias))
    for k, v in divergencias.items():
        print("  %s: %s" % (k, "; ".join(v)))

    atualizar_categorias(linhas, i_cat)

    # 8. plot.log
    log = IMG / "plot.log"
    if log.exists():
        log.unlink()
    gi = RAIZ / ".gitignore"
    t = gi.read_text(encoding="utf-8")
    if "plot.log" not in t.split("\n"):
        gi.write_text(t.rstrip("\n") + "\n\n# Log de plotagem do CAD\nplot.log\n", encoding="utf-8")


if __name__ == "__main__":
    main()
