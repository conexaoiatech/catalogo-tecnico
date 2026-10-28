#!/usr/bin/env python3
"""Area, perimetro, centroide e inercias de perfis a partir de DXF limpos (ezdxf).

Uso:
  python scripts/calcular_propriedades_dxf.py SS-108 [FE-0202 ...]   # imprime e gera PNG
  python scripts/calcular_propriedades_dxf.py --csv FE-0202 ...      # tambem grava relatorios/calculo_dxf.csv
  --escala N força o fator para mm (o INSUNITS do DXF pode estar errado: SS-108 diz polegada mas esta em mm)
  --girados A,B  perfis cujo DXF esta girado 90 graus em relacao a ficha (confira pelas cotas)
  --jx x|y   Ix calculado (x) ou Iy calculado (y) corresponde ao Jx da ficha

DXF em cad-fonte/ARQUIVOS/CALCULO/<CODIGO>.dxf. Contornos fechados vindos de LWPOLYLINE,
POLYLINE, LINE+ARC encadeados, CIRCLE etc.; furos por contencao (profundidade impar);
unidade: INSUNITS 1 = polegada, 4 = mm, 5 = cm, 6 = m, 0 = assume mm (confira o bbox).
Ix = integral de y^2 dA (eixo horizontal); Iy = integral de x^2 dA.
"""
import csv
import math
import re
import sys
from pathlib import Path

import ezdxf
import yaml
from ezdxf import path as ezpath
from PIL import Image, ImageDraw

RAIZ = Path(__file__).resolve().parent.parent
CALC = RAIZ / "cad-fonte" / "ARQUIVOS" / "CALCULO"
SAIDA = RAIZ / "relatorios"
ESCALA_UNIDADE = {0: 1.0, 1: 25.4, 2: 304.8, 4: 1.0, 5: 10.0, 6: 1000.0}


def pedacos(msp, tol_seg):
    """Cada entidade vira uma lista de pontos (x, y)."""
    out, ignoradas = [], []
    for e in msp:
        t = e.dxftype()
        if t in ("TEXT", "MTEXT", "DIMENSION", "POINT", "INSERT", "HATCH"):
            ignoradas.append(t)
            continue
        try:
            p = ezpath.make_path(e)
        except TypeError:
            ignoradas.append(t)
            continue
        pts = [(v.x, v.y) for v in p.flattening(tol_seg, segments=8)]
        if len(pts) >= 2:
            out.append(pts)
    return out, ignoradas


def encadear(pecas, tol):
    """Une pecas pelos extremos; devolve (lacos, n_pecas_soltas)."""
    nos = []

    def no(pt):
        for i, q in enumerate(nos):
            if abs(q[0] - pt[0]) <= tol and abs(q[1] - pt[1]) <= tol:
                return i
        nos.append(pt)
        return len(nos) - 1

    lacos, abertas = [], []
    arestas = []  # (no_a, no_b, indice_peca)
    for i, p in enumerate(pecas):
        a, b = no(p[0]), no(p[-1])
        if a == b:
            lacos.append(p[:-1] if p[0] == p[-1] else p)
        else:
            arestas.append((a, b, i))
    por_no = {}
    for a, b, i in arestas:
        por_no.setdefault(a, []).append((b, i, False))
        por_no.setdefault(b, []).append((a, i, True))
    usadas = set()
    for a, b, i in arestas:
        if i in usadas:
            continue
        pts, atual, ini = [], a, a
        prox, idx, rev = b, i, False
        ok = True
        while True:
            usadas.add(idx)
            seg = pecas[idx][::-1] if rev else pecas[idx]
            pts.extend(seg[:-1])
            atual = prox
            if atual == ini:
                break
            cand = [(n, j, r) for n, j, r in por_no[atual] if j not in usadas]
            if len(cand) != 1:
                ok = False
                break
            prox, idx, rev = cand[0]
        if ok:
            lacos.append(pts)
        else:
            abertas.append(pts)
    return lacos, len(abertas)


def area_assinada(pts):
    return sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1])) / 2


def dentro(pt, poly):
    x, y = pt
    c = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def propriedades(pts):
    """Area, centroide*area, Ixx0, Iyy0 (em torno da origem), perimetro; area positiva."""
    a = sx = sy = ix = iy = per = 0.0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        c = x1 * y2 - x2 * y1
        a += c / 2
        sx += (x1 + x2) * c / 6
        sy += (y1 + y2) * c / 6
        ix += (y1 * y1 + y1 * y2 + y2 * y2) * c / 12
        iy += (x1 * x1 + x1 * x2 + x2 * x2) * c / 12
        per += math.hypot(x2 - x1, y2 - y1)
    s = 1 if a >= 0 else -1
    return a * s, sx * s, sy * s, ix * s, iy * s, per


def analisar(codigo, escala=None):
    arq = CALC / ("%s.dxf" % codigo)
    doc = ezdxf.readfile(str(arq))
    insunits = doc.header.get("$INSUNITS", 0)
    esc = escala if escala is not None else ESCALA_UNIDADE.get(insunits, 1.0)
    msp = doc.modelspace()
    pecas, ignoradas = pedacos(msp, 1e-3)
    xs = [p[0] for pc in pecas for p in pc]
    ys = [p[1] for pc in pecas for p in pc]
    diag = math.hypot(max(xs) - min(xs), max(ys) - min(ys))
    pecas, ignoradas = pedacos(msp, 1e-5 * diag)
    for fator in (1e-4, 1e-3, 3e-3):  # menor tolerancia de junção que fecha tudo
        tol_uso = fator * diag
        lacos, soltas = encadear(pecas, tol_uso)
        if lacos and not soltas:
            break
    if not lacos:
        raise SystemExit("%s: nenhum contorno fechado" % codigo)
    lacos = [[(x * esc, y * esc) for x, y in lc] for lc in lacos]
    prof = []
    for i, lc in enumerate(lacos):
        n = sum(1 for j, o in enumerate(lacos) if j != i and dentro(lc[0], o))
        prof.append(n)
    A = SX = SY = IX = IY = P = 0.0
    for lc, n in zip(lacos, prof):
        a, sx, sy, ix, iy, per = propriedades(lc)
        sinal = 1 if n % 2 == 0 else -1
        A += sinal * a
        SX += sinal * sx
        SY += sinal * sy
        IX += sinal * ix
        IY += sinal * iy
        P += per
    cx, cy = SX / A, SY / A
    return {
        "codigo": codigo, "insunits": insunits, "escala": esc,
        "bbox_raw": (max(xs) - min(xs), max(ys) - min(ys)),
        "bbox_mm": ((max(xs) - min(xs)) * esc, (max(ys) - min(ys)) * esc),
        "area": A, "perimetro": P, "cx": cx, "cy": cy,
        "ix": IX - A * cy * cy, "iy": IY - A * cx * cx,
        "contornos": sum(1 for n in prof if n % 2 == 0), "furos": sum(1 for n in prof if n % 2 == 1),
        "soltas": soltas, "tol_juncao": tol_uso, "ignoradas": sorted(set(ignoradas)), "lacos": lacos, "prof": prof,
    }


def png(r):
    pasta = SAIDA / "calculo_dxf"
    pasta.mkdir(parents=True, exist_ok=True)
    pts = [p for lc in r["lacos"] for p in lc]
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    L = 900
    k = (L - 60) / max(x1 - x0, y1 - y0)
    w, h = int((x1 - x0) * k) + 60, int((y1 - y0) * k) + 60
    im = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(im)

    def tr(p):
        return (30 + (p[0] - x0) * k, h - 30 - (p[1] - y0) * k)

    for lc, n in zip(r["lacos"], r["prof"]):
        fura = n % 2 == 1
        poly = [tr(p) for p in lc]
        d.polygon(poly, fill=(255, 220, 220) if fura else (205, 215, 235),
                  outline=(200, 0, 0) if fura else (0, 0, 120))
    d.text((8, 6), "%s  %.1f x %.1f mm  A=%.2f  P=%.2f" % (
        r["codigo"], r["bbox_mm"][0], r["bbox_mm"][1], r["area"], r["perimetro"]), fill="black")
    im.save(pasta / ("%s.png" % r["codigo"]))


def ficha(codigo):
    arq = RAIZ / "src" / "data" / "perfis" / ("%s.yaml" % codigo)
    return yaml.safe_load(arq.read_text(encoding="utf-8")) if arq.exists() else {}


def main():
    args = sys.argv[1:]
    gravar = "--csv" in args
    eixo = "x"  # convencao: Jx da ficha = Ix calculado (x) ou Iy calculado (y)
    if "--jx" in args:
        eixo = args[args.index("--jx") + 1]
    girados = args[args.index("--girados") + 1].split(",") if "--girados" in args else []
    escala = float(args[args.index("--escala") + 1]) if "--escala" in args else None
    codigos = list(dict.fromkeys(a for a in args if re.match(r"^[A-Za-z]{2,3}-\d+$", a)))
    linhas = []
    for c in codigos:
        r = analisar(c, escala)
        png(r)
        # --girados: DXF desenhado girado 90 graus em relacao a ficha (troca Ix e Iy)
        troca = (eixo == "y") != (c in girados)
        jx, jy = (r["iy"], r["ix"]) if troca else (r["ix"], r["iy"])
        print("%s INSUNITS=%s escala=%s bbox_raw=%.3f x %.3f bbox_mm=%.2f x %.2f" % (
            c, r["insunits"], r["escala"], *r["bbox_raw"], *r["bbox_mm"]))
        print("  area=%.2f perimetro=%.2f centroide=(%.3f, %.3f) Ix=%.2f Iy=%.2f contornos=%d furos=%d soltas=%d tol_juncao=%.4f ignoradas=%s"
              % (r["area"], r["perimetro"], r["cx"], r["cy"], r["ix"], r["iy"], r["contornos"], r["furos"],
                 r["soltas"], r["tol_juncao"], r["ignoradas"]))
        f = ficha(c)
        af, pf = f.get("superficie_area_mm2_mml"), f.get("superficie_perimetro_mm2_mml")
        dif = (r["area"] - af) / af * 100 if af else None
        status = "OK" if dif is not None and abs(dif) < 2 and not r["soltas"] else "DIVERGE"
        linhas.append([c, "%.2f" % r["area"], af if af is not None else "", "" if dif is None else "%.2f" % dif,
                       "%.2f" % r["perimetro"], pf if pf is not None else "", "%.2f" % jx, "%.2f" % jy,
                       r["contornos"], r["furos"], r["insunits"],
                       "%.2f x %.2f" % r["bbox_mm"], status])
    if gravar:
        with open(SAIDA / "calculo_dxf.csv", "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.writer(fh, delimiter=";")
            w.writerow(["codigo", "area_calc", "area_ficha", "dif_area_%", "perim_calc", "perim_ficha",
                        "jx_calc", "jy_calc", "contornos", "furos", "insunits", "bbox", "status"])
            for l in linhas:
                w.writerow([str(v).replace(".", ",") for v in l])


if __name__ == "__main__":
    main()
