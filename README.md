# Catálogo Técnico — Solução / Blindex

Catálogo técnico de referência dos sistemas de envidraçamento (sacadas, grandes vãos, pele de vidro) produzidos pela Solução Fechamento Inteligente, sob licença Blindex®.

Publicado via GitHub Pages a partir da pasta `/docs` (branch `main`).

## Estrutura

```
src/
  data/
    marcas.yaml          # nomes comerciais, cores, logos e publicação (campo publicada) por marca (Solução azul / Blindex vermelho)
    categorias/*.yaml     # conteúdo técnico neutro de marca (tipologia, limites, montagem, usinagem)
    perfis/*.yaml         # ficha de cada código de perfil (peso, área, inércia, imagens)
    biblioteca.yaml       # dados da página "Mapa geral de perfis"
    selantes.yaml         # dados da página "Linha de Selantes"
  templates/               # templates Jinja2 (base, capa, produto genérico, partials por tipo de bloco)
  assets/                  # css, js e imagens finais (fonte para o build)
  build.py                 # gera o site estático em /docs a partir de data/ + templates/
docs/                      # SAÍDA GERADA — nunca editar à mão, é sobrescrita a cada build
cad-fonte/                 # (fora do Git) arquivos CAD brutos — ver .gitignore
```

## Decisão de arquitetura: dado técnico × marca

4 das 6 categorias técnicas existem sob duas marcas (Solução e Blindex) com conteúdo técnico idêntico. Para nunca duplicar esse conteúdo:

- `src/data/categorias/*.yaml` guarda o conteúdo técnico **uma única vez**, sem menção a nome comercial.
- `src/data/marcas.yaml` mapeia cada categoria ao nome comercial e cor de cada marca.
- `src/build.py` renderiza uma página por combinação (categoria × marca) que existir — pulando as combinações que uma marca não tem (ex: Blindex não tem Ripado nem Persianas).

Perfis de alumínio seguem a mesma lógica: cada código tem um único arquivo YAML com um campo `categorias:` listando quem o usa — a tabela de compartilhamento na biblioteca de perfis é **derivada automaticamente** desse campo, nunca mantida manualmente.

## Convenção de imagens de perfil

Arquivo nomeado por `{codigo minúsculo}-{detalhe_snake_case}.jpg` (desenho cotado) e `{codigo minúsculo}-{detalhe_snake_case}-isometrico.jpg` (isométrica, quando houver), tudo minúsculo: por exemplo `ss-001-trilho_inferior.jpg`. O nome do arquivo é declarado nos campos `imagem_desenho:` / `imagem_isometrica:` do YAML do perfil. A regra está em `scripts/padroes.py`; o build corrige o nome fora do padrão e, se não puder corrigir, para e lista os arquivos.

## Como gerar o site

```bash
pip install -r src/requirements.txt
python src/build.py
```

Isso recria `/docs` do zero a partir de `src/data` e `src/templates` (preservando só `docs/hist`, `ESTADO_SESSAO.md`, `PLANO.md` e `ROTEIRO.md`). Abra `docs/index.html` no navegador para conferir antes de comitar: ele é a página de escolha de marca; a capa de cada marca fica em `docs/{marca}/index.html`.

## Marcas publicadas

As marcas **Solução** (azul) e **Blindex** (vermelho) estão publicadas, com o mesmo dado técnico e a identidade de cada uma. Quais marcas saem no build é definido em `src/data/marcas.yaml`, pelo campo `publicada` de cada marca.

## Documentos do projeto

- Guia de edição de textos: `GUIA_EDICAO.md`
- Plano e roteiro: `docs/PLANO.md` e `docs/ROTEIRO.md`
- Instrução do projeto: `INSTRUÇÃO_CLAUDE_IA.txt`
