#!/usr/bin/env python3
"""Grafico de pressao de vento: altura maxima L (m) x largura do vao b (m), uma curva por pressao.

Premissas em src/data/estrutural.yaml (PRELIMINAR). Perfis estruturais por sistema em
blocos perfis_estruturais de src/data/categorias/*.yaml. Saida: relatorios/graficos/{codigo}.svg
(nao vai para docs/ enquanto publicar_graficos for false) e relatorios/dxf_pendentes.md.

Modelo (montante bi-apoiado, carga uniforme w = p x b):
  resistencia: L_res = sqrt(8 sigma W / (p b))
  flecha:      delta = 5 p b L^4 / (384 E J) <= min(L/175, teto)
               -> L_rel  = cbrt(384 E J / (5 x 175 x p b))   (limite relativo L/175)
               -> L_teto = (384 E J teto / (5 p b))^(1/4)     (limite absoluto)
               L_fle = min(L_rel, L_teto)  (resolve em forma fechada o que a iteracao de
               delta = min(L/175, teto) daria)
  L = min(L_res, L_fle). Unidades: sigma, E em kgf/mm2; p em kgf/mm2 (kgf/m2 / 1e6); b, L em mm.

Uso:
  python scripts/grafico_pressao.py --teste     # teste obrigatorio (caso MM-040)
  python scripts/grafico_pressao.py             # teste + graficos + dxf_pendentes.md + tabela
"""
import math
import sys
from pathlib import Path
from xml.sax.saxutils import escape

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from padroes import chave_codigo, chave_ordem  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "src" / "data"
SAIDA = RAIZ / "relatorios"
CALCULO = RAIZ / "cad-fonte" / "ARQUIVOS" / "CALCULO"
CORES = ["#1b9e77", "#7570b3", "#b8860b", "#d95f02", "#8c564b", "#e7298a"]


def carregar(arq):
    return yaml.safe_load(Path(arq).read_text(encoding="utf-8")) or {}


def comprimento(W, J, p_kgf_m2, b_m, premissas):
    """Altura maxima L (m) e criterio que governa, para W (mm3), J (mm4), p (kgf/m2), b (m)."""
    sigma = premissas["sigma_adm_kgf_mm2"]
    E = premissas["E_kgf_mm2"]
    rel = premissas["flecha_relativa"]
    teto = premissas["flecha_teto_mm"]
    w = (p_kgf_m2 / 1e6) * (b_m * 1000.0)  # kgf/mm (p x b)
    L_res = math.sqrt(8 * sigma * W / w)
    L_rel = (384 * E * J / (5 * rel * w)) ** (1 / 3)
    L_teto = (384 * E * J * teto / (5 * w)) ** 0.25
    L_fle = min(L_rel, L_teto)
    if L_res <= L_fle:
        crit = "resistência"
    else:
        crit = "flecha L/%d" % rel if L_rel <= L_teto else "flecha (teto %g mm)" % teto
    return min(L_res, L_fle) / 1000.0, crit, L_res / 1000.0, L_fle / 1000.0


def teste(premissas):
    """Caso MM-040: sigma=7, E=7000, Wx=16191.39, Jx=1024915.15, p=180 kgf/m2, b=2.6 m."""
    prem = dict(premissas, sigma_adm_kgf_mm2=7, E_kgf_mm2=7000)
    L, crit, L_res, L_fle = comprimento(16191.39, 1024915.15, 180, 2.6, prem)
    esperado = {"L_res": 1.392, "L_fle": 1.888, "L": 1.392}
    obtido = {"L_res": L_res, "L_fle": L_fle, "L": L}
    ok = True
    for k, v in esperado.items():
        d = abs(obtido[k] - v) / v
        ok &= d <= 0.01
        print("  teste MM-040 %-6s calculado=%.4f m  esperado=%.3f m  dif=%.3f%%" % (k, obtido[k], v, d * 100))
    ok &= crit == "resistência"
    print("  criterio que governa: %s (esperado: resistência)" % crit)
    print("TESTE MM-040:", "OK" if ok else "FALHOU")
    return ok


def larguras(premissas):
    g = premissas["largura_m"]
    n = int(round((g["max"] - g["min"]) / g["passo"]))
    return [round(g["min"] + i * g["passo"], 2) for i in range(n + 1)]


def eixo_wj(perfil, premissas):
    eixo = perfil.get("eixo_vento") or premissas.get("eixo_padrao", "x")
    if eixo == "y":
        return "y", perfil.get("modulo_wy_mm3"), perfil.get("inercia_jy_mm4")
    return "x", perfil.get("modulo_wx_mm3"), perfil.get("inercia_jx_mm4")


def svg(perfil, eixo, W, J, premissas):
    bs = larguras(premissas)
    ps = premissas["pressoes_kgf_m2"]
    curvas = {p: [comprimento(W, J, p, b, premissas) for b in bs] for p in ps}
    ymax_dado = max(L for c in curvas.values() for L, *_ in c)
    ymax = max(1.0, math.ceil(ymax_dado * 2) / 2.0)
    wd, ht = 900, 600
    ml, mr, mt, mb = 76, 120, 70, 150
    pw, ph = wd - ml - mr, ht - mt - mb

    def X(b):
        return ml + (b - bs[0]) / (bs[-1] - bs[0]) * pw

    def Y(L):
        return mt + ph - L / ymax * ph

    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="Arial, Helvetica, sans-serif">' % (wd, ht, wd, ht),
           '<rect width="100%" height="100%" fill="#ffffff"/>',
           '<text x="%d" y="30" font-size="18" font-weight="700" fill="#1c2126">%s</text>' % (ml, escape("%s — %s" % (perfil["codigo"], perfil.get("descricao", "")))),
           '<text x="%d" y="52" font-size="12.5" fill="#5b6470">Altura máxima do vão × largura do vão, por pressão de vento (kgf/m²)</text>' % ml]
    # grade e eixos
    passo_y = 0.5
    n = 0
    while n * passo_y <= ymax + 1e-9:
        v = n * passo_y
        out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#e3e6ea"/>' % (ml, Y(v), ml + pw, Y(v)))
        out.append('<text x="%d" y="%.1f" font-size="11" text-anchor="end" fill="#5b6470">%.1f</text>' % (ml - 8, Y(v) + 4, v))
        n += 1
    for b in bs:
        if abs(round(b * 10) - b * 10) < 1e-6 and int(round(b * 10)) % 2 == 0:
            out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#e3e6ea"/>' % (X(b), mt, X(b), mt + ph))
            out.append('<text x="%.1f" y="%d" font-size="11" text-anchor="middle" fill="#5b6470">%.1f</text>' % (X(b), mt + ph + 18, b))
    out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#9aa1a9"/>' % (ml, mt, pw, ph))
    out.append('<text x="%.1f" y="%d" font-size="12" text-anchor="middle" fill="#1c2126">Largura do vão b (m)</text>' % (ml + pw / 2, mt + ph + 40))
    out.append('<text transform="translate(18 %.1f) rotate(-90)" font-size="12" text-anchor="middle" fill="#1c2126">Altura máxima L (m)</text>' % (mt + ph / 2))
    # marca d'agua
    out.append('<text x="%.1f" y="%.1f" font-size="96" font-weight="700" fill="#c41e2a" fill-opacity="0.10" text-anchor="middle" transform="rotate(-20 %.1f %.1f)">PRELIMINAR</text>' % (ml + pw / 2, mt + ph / 2 + 30, ml + pw / 2, mt + ph / 2 + 30))
    # curvas
    contagem = {}
    for i, p in enumerate(ps):
        cor = CORES[i % len(CORES)]
        pts = " ".join("%.1f,%.1f" % (X(b), Y(L)) for b, (L, *_r) in zip(bs, curvas[p]))
        out.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.2"/>' % (pts, cor))
        ultimo = curvas[p][-1][0]
        out.append('<text x="%.1f" y="%.1f" font-size="12" font-weight="700" fill="%s">%d</text>' % (X(bs[-1]) + 8, Y(ultimo) + 4, cor, p))
        for _L, crit, *_r in curvas[p]:
            contagem[crit] = contagem.get(crit, 0) + 1
    out.append('<text x="%.1f" y="%d" font-size="11" fill="#5b6470">kgf/m²</text>' % (X(bs[-1]) + 8, mt - 8))
    # rodape
    total = sum(contagem.values())
    gov = "; ".join("%s em %d de %d pontos" % (k, v, total) for k, v in sorted(contagem.items(), key=lambda kv: -kv[1]))
    linhas = ["Premissas: liga %s · σadm %g kgf/mm² · E %g kgf/mm² · %s · carga %s · flecha ≤ L/%d e ≤ %g mm (teto a confirmar na %s)" % (
                  premissas["liga"], premissas["sigma_adm_kgf_mm2"], premissas["E_kgf_mm2"], premissas["esquema"],
                  premissas["carga_por_montante"], premissas["flecha_relativa"], premissas["flecha_teto_mm"], premissas["norma"]),
              "Eixo usado: W%s = %s mm³ · J%s = %s mm⁴ · critério que governa: %s" % (eixo, "{:,.2f}".format(W).replace(",", " "), eixo, "{:,.2f}".format(J).replace(",", " "), gov),
              "Status: %s · validador: %s · não publicar antes da validação" % (premissas["status"], premissas["validador"])]
    for k, t in enumerate(linhas):
        out.append('<text x="%d" y="%d" font-size="10.5" fill="#3b4148">%s</text>' % (ml, ht - 62 + k * 16, escape(t)))
    out.append("</svg>")
    return "\n".join(out), curvas


def estruturais():
    """{codigo: [sistemas]} a partir de perfis_estruturais de cada categoria."""
    out = {}
    for arq in sorted((DATA / "categorias").glob("*.yaml")):
        cat = carregar(arq)
        for c in cat.get("perfis_estruturais") or []:
            out.setdefault(str(c).upper(), []).append(cat.get("slug", arq.stem))
    return out


def main():
    premissas = carregar(DATA / "estrutural.yaml")
    print("Teste obrigatorio:")
    if not teste(premissas):
        raise SystemExit("PARADA: teste MM-040 falhou; nenhum grafico gerado.")
    if "--teste" in sys.argv:
        return
    if premissas.get("publicar_graficos"):
        raise SystemExit("publicar_graficos: true nao e suportado por este script (saida so em relatorios/).")

    perfis = {}
    for arq in (DATA / "perfis").glob("*.yaml"):
        d = carregar(arq)
        perfis[str(d["codigo"]).upper()] = d
    est = estruturais()
    pasta = SAIDA / "graficos"
    pasta.mkdir(parents=True, exist_ok=True)

    gerados, pendentes = [], []
    for cod in sorted(est, key=chave_ordem):
        p = perfis[cod]
        eixo, W, J = eixo_wj(p, premissas)
        if not W or not J:
            pendentes.append(cod)
            continue
        txt, _curvas = svg(p, eixo, W, J, premissas)
        (pasta / ("%s.svg" % chave_codigo(cod))).write_text(txt, encoding="utf-8")
        gerados.append((cod, eixo, W, J))

    print("\nGraficos gerados (%d): %s" % (len(gerados), ", ".join(g[0] for g in gerados)))
    print("\nL (m) por largura b e pressao; criterio que governa:\n")
    print("| Perfil | eixo | b (m) | 80 kgf/m² | 180 kgf/m² |")
    print("|---|---|---|---|---|")
    for cod, eixo, W, J in gerados:
        for b in (1.0, 1.6, 2.6):
            c80 = comprimento(W, J, 80, b, premissas)
            c180 = comprimento(W, J, 180, b, premissas)
            print("| %s | %s | %.1f | %.3f (%s) | %.3f (%s) |" % (cod, eixo, b, c80[0], c80[1], c180[0], c180[1]))

    # dxf_pendentes.md
    linhas = ["# DXF pendentes para o gráfico de pressão", "",
              "Perfis estruturais (`perfis_estruturais` das categorias) sem `modulo_wx_mm3` (ou sem o módulo do eixo usado). "
              "Gerado por `scripts/grafico_pressao.py`.", "",
              "Regras do DXF limpo (as mesmas validadas no SS-108):", "",
              "- só o contorno da seção (sem cotas, textos, eixos, hachuras nem outros perfis);",
              "- unidades em mm, escala 1:1 (o `INSUNITS` do arquivo pode estar errado; vale o desenho em mm);",
              "- na orientação da ficha (se girado ou espelhado, avisar para ajustar `--orient`);",
              "- furos reais como contornos internos fechados;",
              "- contornos fechados, sem lacunas maiores que alguns centésimos de mm.", "",
              "| Perfil | Sistemas (estrutural) | Caminho esperado | DXF existe? |", "|---|---|---|---|"]
    for cod in sorted(pendentes, key=chave_ordem):
        caminho = r"cad-fonte\ARQUIVOS\CALCULO\%s.dxf" % cod
        existe = "sim" if (CALCULO / ("%s.dxf" % cod)).exists() else "não"
        linhas.append("| %s | %s | `%s` | %s |" % (cod, ", ".join(est[cod]), caminho, existe))
    linhas.append("")
    (SAIDA / "dxf_pendentes.md").write_text("\n".join(linhas), encoding="utf-8")
    print("\nDXF pendentes (%d): %s" % (len(pendentes), ", ".join(sorted(pendentes, key=chave_ordem))))


if __name__ == "__main__":
    main()
