# CLAUDE.md — catalogo_tecnico

Conduta, abertura e fechamento de sessão e estrutura de projeto seguem as skills `conduta`, `estou-entrando-saindo` e `estrutura-projeto`. Este arquivo não repete a conduta; lista só o que é específico deste repo.

- project_id: `catalogo_tecnico` · repo `conexaoiatech/catalogo-tecnico` · pasta `C:\GITHUB\CATALOGO_TECNICO`
- Plano, roteiro e estado: `docs/PLANO.md`, `docs/ROTEIRO.md`, `docs/ESTADO_SESSAO.md`. Instrução do projeto: `INSTRUÇÃO_CLAUDE_IA.txt`.

## Comandos
- Validar os dados (sem build): `python scripts/validar_catalogo.py`
- Gerar o site: `python src/build.py` (dependências em `src/requirements.txt`: Jinja2, PyYAML, Pillow e numpy)
- Os dois devem sair com 0 antes de qualquer commit que mexa em `src/`.

## Regras do repo
- `docs/` é gerado pelo build: nunca editar à mão. O build recria a pasta e preserva só `hist/`, `ESTADO_SESSAO.md`, `PLANO.md` e `ROTEIRO.md` (lista PRESERVAR em `src/build.py`).
- Fonte única: perfil em `src/data/perfis/{CODIGO}.yaml`; vínculo perfil × sistema em `src/data/categorias/*.yaml`; nomes, cores e logos por marca em `src/data/marcas.yaml`. Dado técnico nunca é duplicado por marca.
- Regras de nome de imagem, status de perfil completo e ordem por código ficam em `scripts/padroes.py` (usadas pelo build e pelo validador).
- Premissas dos gráficos de pressão: `src/data/estrutural.yaml` está PRELIMINAR e `publicar_graficos` é false até o Coordenador de Produção validar.
- CAD nunca entra no git (repo público): `cad-fonte/` e as extensões CAD estão no `.gitignore`. Não remover arquivo rastreado sem decisão da pessoa.
- Branch `main`. Publicação = GitHub Pages a partir de `/docs`. Site: https://conexaoiatech.github.io/catalogo-tecnico/
- Escrita em `gov_*` só pelos scripts do GOV_IA_CORE (`gov-passo.ps1`, `gov-demanda.ps1`, `gov-sessao.ps1`).
- Ao mudar caminho, arquivo de texto ou template, atualizar GUIA_EDICAO.md no mesmo commit.
