# Estado — catalogo_tecnico

## Sessão
- id=125 origem=claude_code inicio=2026-11-13 19:17:17-03:00 fim=2026-11-13 19:42:21-03:00 resumo=Abertura das sessoes 124 e 125 e do passo 158, rotina do dia gravada, regularizacao A7 do repo com gitignore, MANUAL, PLANO, ROTEIRO e INSTRUCAO nos commits 7cc213b e d353e00 em origin/main, CLAUDE.md corrigido, docs/hist/arquivo criado, demandas 351 e 21 atualizadas e passo 158 fechado
- id=124 origem=claude_ia inicio=2026-11-13 18:35:21-03:00 fim=2026-11-13 19:41:27-03:00 resumo=Pacote projnovo do catalogo_tecnico montado e entregue ao GOV_IA_CORE, demanda 351 executada no repo com commits 7cc213b e d353e00, passo 158 fechado, checklist A7 do lado do repo verde, demanda 21 com observacao de encerramento

## Resumo
- demandas abertas: 5
- sessões abertas: 0
- último passo: id=158

## Rotina
| etapa | objetivo | sucesso | pct | fim previsto | status | passo |
|---|---|---|---|---|---|---|
| 1 Regularizacao A7 do repo | Repo catalogo_tecnico no padrao GOV_IA_CORE para fechar o A7 | push 7cc213b e d353e00 em origin/main, A7 lado repo verde, faltam E11 e E13 no GOV_IA_CORE | 100% | 2026-11-13 19:30:00-03:00 | FINALIZADO_SUCESSO | 158 |
| **total** | 1 etapas | 1 finalizadas | 100% (1 de 1 com pct) | | | |

## Planejado
- #298 Dados estruturais e grafico de pressao por sistema (EM_ANALISE)
- #300 PDF deterministico e logos dos produtos (EM_ANALISE)
- #352 Registrar arquitetura nivel A do catalogo_tecnico em arq_componentes (EM_ANALISE)

## Feito
- id=79 1 — Inventario e proposta de nomes das imagens de perfil — Inventario 59 arquivos em relatorios/inventario_imagens_perfis.md - 0 OK 13 RENOMEAR 43 SEM_DETALHE 2 SEM_CODIGO 1 EXTENSAO - nenhuma imagem alterada
- id=80 2a — Matriz perfil x sistema pelos YAML e diagnostico de pastas — Matriz 34 perfis em relatorios/matriz_perfis_sistemas.md - 22 sem descricao - referencias categoria x perfil incompletas
- id=81 2b — Limpeza de src e planilha de referencias perfil x sistema — Planilha relatorios/referencias_perfis.csv 40 linhas 0 divergencias 6 SEM_YAML
- id=82 2b2 — Ler fichas tecnicas das imagens, refazer planilha e renomear imagens — 41 fichas lidas em relatorios/fichas_lidas.csv - 36 perfis renomeados 72 arquivos de-para em relatorios/renomeacao_imagens.csv - 4 imagens com erro corrigidas pela pessoa
- id=83 2b3 — Reler fichas corrigidas, renomear pendentes e mover SLDPRT — Fichas FE-0207 DSL-001 SS-002 relidas OK - SS-014 resolvido - planilha 39 de 40 OK - SS-108 confirmado pela pessoa
- id=84 2c — Aplicar planilha revisada nos YAML, renomear pendentes e commit local — Commit local 64b3580 - 6 YAML criados 34 alterados 21 divergencias - validacao a b c d OK - ripado pendente
- id=85 2d — Reaplicar referencias da planilha corrigida, criar lista do Ripado, mover CAD de src — Ripado com lista de perfis - referencias reaplicadas da planilha 18:17 - SS-024 em 4 categorias - validacao OK - commit 5f9c2d7 com push
- id=86 4b — Calcular Jx Jy dos FE e LT-077 pelos DXF limpos — Jx Jy Wx Wy de FE-0202 a 0208 e LT-077 pelos DXF - metodo validado no SS-108 - FE-0207 area corrigida 274.43 - commits d6e62c6 4cc2746 984f21e
- id=87 3b — build.py com validador, padrao minusculo e preservacao da governanca em docs — build.py com validador e padrao minusculo - docs regenerado - governanca preservada - links OK - commit aa73c96 local
- id=88 3c — Imagem em todos os cards, status calculado, notas sem contagem, campos unificados — Imagem em todos os cards - status calculado em scripts/padroes.py - notas sem contagem - campos unificados - links OK - commit 95ab85e local
- id=89 3d — Material dos perfis DSL — Material UHMW-PE nos DSL - 40 de 40 perfis completos - commit 049a4c5 com push
- id=90 3e — Desenho da ficha maior e ampliacao ao clicar — Desenho da ficha sem limite de altura ate 720px, lightbox sem biblioteca, link tamanho original - commit f751915 com push
- id=91 3f — Pagina por perfil, biblioteca como indice e botao de menu — 40 paginas de perfil, biblioteca indice com filtro, menu principal, links OK - commit 3b7ca72 com push
- id=92 3g — Navegacao hierarquica com trilha e voltar um nivel — Trilha fixa, voltar um nivel, origem por ?de=, vizinhos por sistema, links OK - commit 0268331 com push
- id=93 3h — SS-024 fora do MWO e matriz perfil x sistema para revisao — SS-024 removido do MWO - relatorios/matriz_sistemas.md - commit ec557a6 com push
- id=94 3i — SS-018 e SS-019 incluidos na Sacada — SS-018 e SS-019 na Sacada - sacada 17 perfis - commit 7d1894a com push
- id=95 3j — Ordem dos perfis por codigo em todas as listas — Ordem por codigo em padroes.py aplicada em sistemas, biblioteca e vizinhos - commit 600c1a9 com push
- id=96 3k — Logos da marca na entrada e no cabecalho — Logos em src/assets/img/marcas, Solucao na entrada e no cabecalho, Blindex guardado - commit f751bfe com push
- id=97 6-8 — FE-0205 corrigido, premissas estruturais, perfis estruturais por sistema e gerador de grafico — FE-0205 Bagete 22.5 Graus - estrutural.yaml - perfis_estruturais em 4 sistemas - teste MM-040 OK - 3 graficos em relatorios/graficos - DXF pendentes listados - commits ae436c4 bb77a8d com push
- id=98 3m — Fichas FE com Jx Jy - conferencia e substituicao — 6 fichas FE com Jx Jy conferidas contra YAML e substituidas - commit 985e0f4 com push
- id=99 3n — Referencia de layout do SITESOLU e teste visual do catalogo atual — Layout escuro padrao SITESOLU, menu em gaveta, sidebar removida, miniaturas isometricas, fichas recortadas, logo otimizado, 7 de 8 problemas visuais corrigidos - commit 515137d com push
- id=100 3o — Versao Blindex do catalogo — Versao Blindex publicada (4 sistemas, 39 perfis), entrada com escolha de marca, redirecionamento dos links antigos, sem MWO/BigSpace/SkinGlass/Ripado na Blindex - commits 1d8fe17 e 280792c com push
- id=101 3p — Remover Solucao Sacadas dos textos da Blindex — Blindex sem Solucao Sacadas, fonte do desenho-mestre generica (Desenho-mestre CAD) - commit 470f5f6 com push
- id=102 3q — Remover ficha em destaque do SS-016 no BigSpace — ficha_destaque do SS-016 removida - BigSpace e Vista so com cards - commit 1b5de79 com push
- id=103 3s — Arrumacao: demandas manuais, demanda 21, limpeza e varredura de CAD — WF-GOV-REGISTRO conferido, demanda 21 e 295 tratadas pelo script, 2 arquivos soltos em cad-fonte/_arquivo, gitignore CAD - commit e47d447 com push
- id=104 3r — Publicar alteracao manual da pessoa em marcas.yaml — Ajuste manual em marcas.yaml publicado - commit 95263a7 com push
- id=105 3t — Governanca no repo: PLANO, ROTEIRO, CLAUDE.md, INSTRUCAO e GUIA_EDICAO — Governanca no repo criada - commit 10f0a91 com push - demanda 296 fechada
- id=106 3u — Ajustes do 3t: ROTEIRO, prototipo fora do git e instrucao do projeto — ROTEIRO com 3t FEITO, prototipo fora do git, README e INSTRUCAO atualizados - commit d851fcc com push
- id=107 3w — Consolidar a instrucao do projeto a partir das versoes na raiz — Instrucao consolidada em INSTRUCAO_CLAUDE_IA_atualizada.txt - sem commit, aguardando a pessoa
- id=108 3x — Aplicar instrucao consolidada no repo, README e ROTEIRO — Instrucao consolidada oficial, _old arquivado, README e ROTEIRO em dia - commit 4912185 com push
- id=110 109 — Modelo da relacao de pecas Solucao — Relacao de pecas gerada dos YAML em linha por perfil, A4 retrato 3 por pagina, Solucao 40 perfis e Blindex 39, PPF em 7 perfis, recorte corrigido por regra geral, versao folheavel na biblioteca. Commits f8fbe53 31ddf4a 6cb11be 7815278 em origin/main.
- id=158 109 — Regularizacao A7 do repo — commits 7cc213b e d353e00 em origin/main, A7 lado repo verde, docs/hist/arquivo criado

## Pendente
(nenhum)

## Próximo
- #301 Hospedagem propria do catalogo na VPS srv1849835 (EM_EXECUCAO)
