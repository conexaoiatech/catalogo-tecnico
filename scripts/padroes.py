"""Regra unica de nome das imagens de perfil (usada por src/build.py e scripts/validar_catalogo.py).

{codigo minusculo}-{detalhe snake_case}.jpg  ou  {codigo minusculo}-{detalhe snake_case}-isometrico.jpg
Codigos: ss, dsl e lt com 3 digitos; fe com 4; f98 (sem hifen).
"""
import re
import unicodedata

PADRAO_IMAGEM = re.compile(r"^(?:(?:ss|dsl|lt)-\d{3}|fe-\d{4}|f\d+)-[a-z0-9_]+(?:-isometrico)?\.jpg$")
RE_COD = re.compile(r"^(SS|DSL|DLS|FE|LT|F)[\s_-]?(\d+)", re.IGNORECASE)
RE_ISO = re.compile(r"(isometrico|iso)", re.IGNORECASE)


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def snake(t):
    t = sem_acento(t).lower()
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", t)).strip("_")


def chave_codigo(txt):
    """ss-014, dsl-001, fe-0202, lt-077, f98 a partir de qualquer grafia (SS_014, SS-0108, DLS-2...)."""
    m = RE_COD.match(sem_acento(str(txt)).strip())
    if not m:
        return None
    pre, n = m.group(1).lower(), int(m.group(2))
    pre = "dsl" if pre == "dls" else pre
    if pre == "f":
        return "f%d" % n
    return "%s-%0*d" % (pre, 4 if pre == "fe" else 3, n)


def nome_padrao(codigo, descricao, isometrico=False):
    """Nome padrao a partir do codigo e da descricao do YAML; None se nao der para montar."""
    k, d = chave_codigo(codigo), snake(descricao or "")
    if not k or not d:
        return None
    nome = "%s-%s%s.jpg" % (k, d, "-isometrico" if isometrico else "")
    return nome if PADRAO_IMAGEM.match(nome) else None


def nome_valido(nome):
    return bool(PADRAO_IMAGEM.match(nome))


# ---- completude do perfil (fonte unica; o campo status nao existe mais nos YAML) ----
# SS, FE, LT e F: ficha tecnica completa. DSL (polimero deslizante): codigo, descricao e material.
CAMPOS_FICHA = ["peso_kg_m", "superficie_area_mm2_mml", "superficie_perimetro_mm2_mml",
                "inercia_jx_mm4", "inercia_jy_mm4"]
CAMPOS_DSL = ["codigo", "descricao", "material"]


def _vazio(v):
    return v is None or v == ""


def campos_faltando(perfil):
    """Campos obrigatorios ainda vazios, segundo a familia do codigo."""
    k = chave_codigo(perfil.get("codigo", "")) or ""
    obrigatorios = CAMPOS_DSL if k.startswith("dsl") else CAMPOS_FICHA
    return [c for c in obrigatorios if _vazio(perfil.get(c))]


def perfil_completo(perfil):
    return not campos_faltando(perfil)


# ---- ordem unica dos perfis (decisao da pessoa): familia SS, LT, F, FE, DSL; dentro dela, pelo numero ----
ORDEM_FAMILIAS = ["ss", "lt", "f", "fe", "dsl"]


def chave_ordem(codigo):
    """Chave de ordenacao: SS-001 < ... < SS-108 < LT-077 < F98 < FE-0202 < ... < DSL-003."""
    k = chave_codigo(codigo) or ""
    fam = re.sub(r"[\d-]", "", k)
    num = int(re.sub(r"\D", "", k) or 0)
    return (ORDEM_FAMILIAS.index(fam) if fam in ORDEM_FAMILIAS else len(ORDEM_FAMILIAS), num)
