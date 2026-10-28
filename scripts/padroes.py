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
