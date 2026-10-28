#!/usr/bin/env python3
"""Passo 2d: reaplica so as referencias de categoria da planilha revisada.

- confere o acento de descricao dos YAML de perfil contra a planilha;
- troca o placeholder do ripado por um bloco profiles (um grupo sem rotulo);
- refaz blocks[tipo=profiles] de todas as categorias e o campo categorias dos perfis.
Nao altera valor tecnico nem imagem.
"""
import csv
import sys

import yaml

from aplicar_planilha_perfis import DATA, REL, SLUGS, atualizar_categorias, codigo

DECISOES = {"ss-024": ["pele-vidro", "portas-minimalistas", "portas-robustas", "ripado"]}
ENC = sys.argv[1] if len(sys.argv) > 1 else "cp850"


def main():
    with open(REL / "referencias_perfis_rev.csv", encoding=ENC, newline="") as f:
        rd = list(csv.reader(f, delimiter=";"))
    cab, linhas = rd[0], rd[1:]
    i_cat = [cab.index(s) for s in SLUGS]
    for r in linhas:
        r[0] = codigo(r[0])
    for r in linhas:  # decisao explicita da pessoa: prevalece sobre a planilha
        for k, slugs in DECISOES.items():
            if r[0] == k:
                for s in slugs:
                    r[i_cat[SLUGS.index(s)]] = "X"

    # 3. descricao dos YAML x planilha (aplicada, que ja tem as descricoes da pessoa)
    with open(REL / "referencias_perfis_aplicada.csv", encoding="utf-8-sig", newline="") as f:
        aplicada = {r[0]: r[1] for r in list(csv.reader(f, delimiter=";"))[1:]}
    corrigidas = []
    for arq in sorted((DATA / "perfis").glob("*.yaml")):
        d = yaml.safe_load(arq.read_text(encoding="utf-8"))
        k = codigo(d["codigo"])
        plan = aplicada.get(k)
        if plan and d.get("descricao") != plan:
            corrigidas.append((k, d.get("descricao"), plan))
            d["descricao"] = plan
            arq.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print("descricoes corrigidas (%d): %s" % (len(corrigidas), corrigidas))

    # 4. ripado: placeholder -> profiles
    i_rip = i_cat[SLUGS.index("ripado")]
    do_ripado = [r[0].upper() for r in linhas if r[i_rip].strip()]
    arq = DATA / "categorias" / "ripado.yaml"
    txt = arq.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in txt else "\n"
    linhas_txt = txt.split(nl)
    ini = next(n for n, l in enumerate(linhas_txt) if l == "- id: perfis")
    if "tipo: placeholder" in linhas_txt[ini + 1]:
        novo = ["- id: perfis", "  tipo: profiles", "  titulo: Perfis utilizados",
                "  grupos:", "  - label: null", "    codigos:"] + ["    - " + c for c in do_ripado]
        fim = next((n for n in range(ini + 1, len(linhas_txt)) if linhas_txt[n].startswith("- id:")),
                   len(linhas_txt))
        resto = linhas_txt[fim:]
        arq.write_text(nl.join(linhas_txt[:ini] + novo + ([""] if not resto else resto)),
                       encoding="utf-8")
    print("ripado (%d): %s" % (len(do_ripado), do_ripado))

    # 5. categorias de todas as categorias + campo categorias dos perfis
    atualizar_categorias(linhas, i_cat)
    alterados = []
    for r in linhas:
        arq = DATA / "perfis" / ("%s.yaml" % r[0].upper())
        d = yaml.safe_load(arq.read_text(encoding="utf-8"))
        marcadas = [s for s, i in zip(SLUGS, i_cat) if r[i].strip()]
        antigas = d.get("categorias") or []
        novas = [c for c in antigas if c in marcadas] + [c for c in SLUGS if c in marcadas and c not in antigas]
        if novas != antigas:
            d["categorias"] = novas
            arq.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False), encoding="utf-8")
            alterados.append((r[0], antigas, novas))
    print("perfis com categorias alteradas (%d):" % len(alterados))
    for a in alterados:
        print("  ", a)
    for k in ("ss-015", "ss-024"):
        d = yaml.safe_load((DATA / "perfis" / ("%s.yaml" % k.upper())).read_text(encoding="utf-8"))
        print(k, d["categorias"])


if __name__ == "__main__":
    main()
