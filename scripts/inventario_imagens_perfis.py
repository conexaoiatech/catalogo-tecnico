#!/usr/bin/env python3
"""Inventario das imagens de perfil (somente leitura: NAO renomeia nada).

Gera relatorios/inventario_imagens_perfis.csv e .md a partir de
src/assets/img/perfis.
"""
import csv
import hashlib
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "src" / "assets" / "img" / "perfis"
SAIDA = RAIZ / "relatorios"
MARCADORES_ISO = {"isometrico", "isometric", "iso"}
EXT_OK = {".jpg", ".jpeg"}
RE_CODIGO = re.compile(r"(?<![a-z])(ss|dsl)[\s_-]?(\d+)", re.IGNORECASE)


def sem_acento(texto):
    nfd = unicodedata.normalize("NFD", texto)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def sha12(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()[:12]


def analisar(arquivo):
    nome = sem_acento(arquivo.stem).lower()
    m = RE_CODIGO.search(nome)
    codigo = ""
    resto = nome
    if m:
        codigo = "%s-%03d" % (m.group(1), int(m.group(2)))
        resto = nome[: m.start()] + " " + nome[m.end():]
    tokens = [t for t in re.split(r"[\s\-._]+", resto) if t]
    tipo = "desenho"
    detalhe = []
    for t in tokens:
        if t in MARCADORES_ISO:
            tipo = "isometrico"
        else:
            detalhe.append(t)
    detalhe = "_".join(detalhe)
    padrao = ""
    if codigo:
        padrao = codigo + ("-" + detalhe if detalhe else "")
        if tipo == "isometrico":
            padrao += "-isometrico"
        padrao += ".jpg"
    return codigo, detalhe, tipo, padrao


def main():
    linhas = []
    for arq in sorted(p for p in PASTA.rglob("*") if p.is_file()):
        rel = arq.relative_to(PASTA)
        sistema = rel.parts[0] if len(rel.parts) > 1 else "RAIZ"
        codigo, detalhe, tipo, padrao = analisar(arq)
        if arq.suffix.lower() not in EXT_OK:
            status = "EXTENSAO"
        elif not codigo:
            status = "SEM_CODIGO"
        elif not detalhe:
            status = "SEM_DETALHE"
        elif arq.name != padrao:
            status = "RENOMEAR"
        else:
            status = "OK"
        linhas.append({
            "sistema": sistema, "arquivo_atual": arq.name, "codigo": codigo,
            "detalhe": detalhe, "tipo": tipo, "nome_padrao": padrao,
            "status": status, "hash": sha12(arq),
        })

    # colisao: mesmo nome padrao na mesma pasta (nao sobrepoe EXTENSAO)
    grupos = defaultdict(list)
    for l in linhas:
        if l["nome_padrao"]:
            grupos[(l["sistema"], l["nome_padrao"].lower())].append(l)
    for membros in grupos.values():
        if len(membros) > 1:
            for l in membros:
                if l["status"] != "EXTENSAO":
                    l["status"] = "COLISAO"

    SAIDA.mkdir(exist_ok=True)
    campos = ["sistema", "arquivo_atual", "codigo", "detalhe", "tipo",
              "nome_padrao", "status", "hash"]
    with open(SAIDA / "inventario_imagens_perfis.csv", "w", newline="",
              encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=campos, delimiter=";")
        w.writeheader()
        w.writerows(linhas)

    # perfis em mais de um sistema
    por_codigo = defaultdict(list)
    for l in linhas:
        if l["codigo"]:
            por_codigo[l["codigo"]].append(l)
    multi = []
    for codigo, arqs in por_codigo.items():
        sistemas = sorted({a["sistema"] for a in arqs})
        if len(sistemas) < 2:
            continue
        detalhes_por_sis = {
            s: {a["detalhe"] for a in arqs if a["sistema"] == s}
            for s in sistemas
        }
        if len({frozenset(v) for v in detalhes_por_sis.values()}) > 1:
            situacao = "NOMES_DIFERENTES"
        else:
            por_nome = defaultdict(set)
            for a in arqs:
                por_nome[a["nome_padrao"]].add(a["hash"])
            situacao = ("DIVERGENTE" if any(len(h) > 1 for h in por_nome.values())
                        else "IDENTICO")
        multi.append((codigo, sistemas, len(arqs), situacao))
    multi.sort(key=lambda r: (-len(r[1]), r[0]))

    por_status = Counter(l["status"] for l in linhas)
    por_sistema = Counter(l["sistema"] for l in linhas)
    md = ["# Inventario de imagens de perfil", "",
          "Total de arquivos: %d" % len(linhas), "",
          "## 1. Contagens", "", "### Por status", "",
          "| status | qtd |", "|---|---|"]
    md += ["| %s | %d |" % (s, n) for s, n in sorted(por_status.items())]
    md += ["", "### Por sistema", "", "| sistema | qtd |", "|---|---|"]
    md += ["| %s | %d |" % (s, n) for s, n in sorted(por_sistema.items())]
    md += ["", "## 2. Perfis em mais de um sistema", "",
           "| codigo | sistemas | qtd_arquivos | situacao |", "|---|---|---|---|"]
    md += ["| %s | %s | %d | %s |" % (c, ", ".join(s), q, sit)
           for c, s, q, sit in multi]
    if not multi:
        md.append("| (nenhum) | | | |")
    md += ["", "## 3. Pendencias"]
    for status in ("SEM_CODIGO", "SEM_DETALHE", "EXTENSAO", "COLISAO"):
        md += ["", "### %s" % status, ""]
        itens = [l for l in linhas if l["status"] == status]
        md += ["- %s/%s" % (l["sistema"], l["arquivo_atual"]) for l in itens]
        if not itens:
            md.append("(nenhum)")
    with open(SAIDA / "inventario_imagens_perfis.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print("%d arquivos; status: %s" % (len(linhas), dict(por_status)))


if __name__ == "__main__":
    main()
