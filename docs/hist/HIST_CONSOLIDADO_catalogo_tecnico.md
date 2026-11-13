# HIST_CONSOLIDADO_catalogo_tecnico
Versão: 2026-11-13 19:50 (v1, migração inicial) · Período: 2026-09-15 a 2026-11-13 · HIST incluídos: 9 (último: HIST_2026-11-13_a_2026-11-13_catalogo_tecnico_projnovo-regularizacao-a7.md) · Fonte extra: espelho ESTADO de 2026-10-30 (chat da hospedagem e da relação de peças, sem HIST próprio)
Ids próprios: C-M (marco), C-D (decisão), C-A (artefato). Origem: <arquivo abreviado>#<id do HIST>. Abreviações: EST = estrutura-dupla-marca-imagens · REC = reconstrucao-gov-demandas · ATU = atualizacao-gov-demandas · STA = status-projeto · PUS = push-hist-estado-sessao · IMG = imagens-dados-layout-blindex · PDF = catalogo-pdf · GOV = governanca-instrucao · A7 = projnovo-regularizacao-a7 · E30 = espelho ESTADO 2026-10-30.

## 1. Linha do tempo (mais recente por último)
| id | data/hora | marco | tipo | origem |
|---|---|---|---|---|
| C-M1 | 2026-09 (15 a 29) | Pedido do catálogo HTML; protótipos v1/v2; dupla marca; plano Python+Jinja2; Pages no ar com repo público; padronização de nomes e imagens (c8dc33f); DSL não-alumínio; SS-0108 por DXF | resumo do mês | EST#2 a #18 |
| C-M2 | 2026-09-18 20:41 | Projeto cadastrado em projetos; demandas 17 a 21 | marco | REC#5, #6 |
| C-M3 | 2026-10-26 14:58 | Skill relatorio-objetivos-gov criada (só leitura) | marco | ATU#4 |
| C-M4 | 2026-10-26 20:47 | 1º docs/ESTADO_SESSAO.md (bee21e6) | marco | PUS#7 |
| C-M5 | 2026-10-28 14:55 | Fichas lidas e 72 imagens renomeadas; YAML corrigidos (64b3580) | marco | IMG P15, P17 |
| C-M6 | 2026-10-28 19:50 | Build com validador e padrões únicos (aa73c96) | marco | IMG P22 |
| C-M7 | 2026-10-28 20:22 | MUDOU ROTA: repo definitivo em conexaoiatech | MUDOU ROTA | IMG#9 |
| C-M8 | 2026-10-28 22:29 | MUDOU ROTA: gráficos de pressão adiados | MUDOU ROTA | IMG#12 |
| C-M9 | 2026-10-29 00:38 | Layout escuro SITESOLU e versão Blindex publicada (470f5f6) | marco | IMG P37 a P39 |
| C-M10 | 2026-10-29 11:39 | MUDOU ROTA: escrita em gov_* só pelo Code com scripts | MUDOU ROTA | GOV#3 |
| C-M11 | 2026-10-29 18:30 | PLANO, ROTEIRO, CLAUDE.md, INSTRUÇÃO e GUIA_EDICAO no repo (10f0a91, d851fcc) | marco | GOV P46, P47 |
| C-M12 | 2026-10-29 21:08 | 10 PDFs por sistema e marca publicados (6c11ba0) | marco | PDF P45 |
| C-M13 | 2026-10-30 ~20:00 | Catálogo no ar em catalogo.solucaointeligentes.com (VPS srv1849835, deploy por Action); relação de peças (7815278) | marco | E30 |
| C-M14 | 2026-11-13 17:25 | MUDOU ROTA: /projnovo vira regularização (projeto já cadastrado) | MUDOU ROTA | A7#6 |
| C-M15 | 2026-11-13 19:43 | A7 fechado: 7cc213b, d353e00, c758b2f; gate producao; 351 FINALIZADO_SUCESSO | marco | A7#10 a #13 |

## 2. Decisões (cronológicas, mais recente por último)
| id | data/hora | [assunto] | decisão | situação | origem |
|---|---|---|---|---|---|
| C-D1 | 2026-09-15 23:05 | [dupla-marca] | 4 categorias com nome Solução (azul) e Blindex (vermelho); Ripado e Persianas só Solução | vigente | EST D29 |
| C-D2 | 2026-09-15 23:05 | [ordem-marcas] | Solução completa primeiro, Blindex depois | superada por C-D21 (2026-10-29) | EST D29 |
| C-D3 | 2026-09-15 23:19 | [stack] | Python + Jinja2 + PyYAML, HTML gerado em /docs na main | vigente | EST D30 |
| C-D4 | 2026-09-15 23:19 | [repo] | repo na org Solucao-Fechamento-Inteligente | superada por C-D15 (2026-10-28) | EST D30 |
| C-D5 | 2026-09-17 12:45 | [nome-imagem] | {CODIGO}-{nome_snake}.jpg | superada por C-D12 (2026-10-28) | EST D31 |
| C-D6 | 2026-09-17 12:50 | [formato-bloco] | "> RODAR EM" dentro do bloco | superada por C-D23 (2026-10-29) | EST D32 |
| C-D7 | 2026-09-23 10:30 | [imagens-fonte] | imagens só em src/assets/img/perfis; docs/ é gerado | vigente | EST D37 |
| C-D8 | 2026-09-18 20:40 | [gate] | projeto cadastrado em implementacao_gradual | superada por C-D40 (2026-11-13) | REC D1 |
| C-D9 | 2026-10-26 15:29 | [escrita-governanca] | escrita em gov_* manual no Adminer | superada por C-D22 (2026-10-29) | ATU D4 |
| C-D10 | 2026-10-27 17:13 | [imagens-pasta] | pasta única, sem subpasta por produto | vigente | IMG D1 |
| C-D11 | 2026-10-28 00:12 | [branch] | push em main (master não existe) | superada por C-D34 (2026-11-13) | IMG D4 |
| C-D12 | 2026-10-28 14:51 | [nome-imagem] | nome = {codigo}-{descrição da ficha}, minúsculo, regra em scripts/padroes.py | vigente | IMG D6 |
| C-D13 | 2026-10-28 16:01 | [ficha-prevalece] | ficha individual prevalece; exceção SS-002 (vale o YAML) | vigente | IMG D7 |
| C-D14 | 2026-10-28 19:15 | [ficha-prevalece] | exceção FE-0207 área 274.43; LT-077 vale a ficha | vigente | IMG D11 |
| C-D15 | 2026-10-28 20:23 | [repo] | conexaoiatech/catalogo-tecnico (definitivo) | vigente | IMG D16 |
| C-D16 | 2026-10-28 20:11 | [dsl] | DSL = UHMW-PE, perfil deslizante | vigente | IMG D15 |
| C-D17 | 2026-10-28 20:43 | [navegacao] | trilha hierárquica, voltar um nível, ?de=, vizinhos por sistema | vigente | IMG D17 |
| C-D18 | 2026-10-28 21:20 | [ordem-perfis] | ordem por código (SS, LT, F, FE, DSL) | vigente | IMG D20 |
| C-D19 | 2026-10-28 22:29 | [graficos] | método clássico 6063-T5, validação do Coordenador de Produção; gráficos adiados | vigente | IMG D12, D22 |
| C-D20 | 2026-10-28 23:32 | [layout] | tema escuro total padrão SITESOLU | vigente | IMG D24 |
| C-D21 | 2026-10-29 00:00 | [ordem-marcas] | Blindex publicada já, sem "Solução Sacadas", fonte "Desenho-mestre CAD" | vigente | IMG D25 |
| C-D22 | 2026-10-29 11:39 | [escrita-governanca] | escrita em gov_* só pelo Code com gov-*.ps1 e motor | vigente | GOV D27 |
| C-D23 | 2026-10-29 ~12:00 | [formato-bloco] | destino fora do bloco de cópia | vigente | EST seção 11 |
| C-D24 | 2026-10-29 12:40 | [blindex-fabricante] | Blindex mantém a Solução como fabricante (rodapé, link, "sob licença") | vigente | GOV D26 |
| C-D25 | 2026-10-29 17:08 | [demanda-21] | demanda 21 INCONSISTENTE | superada por C-D38 (2026-11-13) | GOV D28 |
| C-D26 | 2026-10-29 18:20 | [guia] | guia oficial = GUIA_EDICAO.md no repo, atualizado no mesmo commit | vigente | GOV D29 |
| C-D27 | 2026-10-29 18:23 | [repo-visibilidade] | repo continua público | superada por C-D31 (2026-10-30) | GOV D30 |
| C-D28 | 2026-10-29 19:52 | [preferencias] | "uma pergunta por vez" sai da instrução e vai para a conduta | vigente | GOV D32 |
| C-D29 | 2026-10-29 20:13 | [pdf] | 2 fichas por página, 1 PDF por sistema e marca, botão de download | vigente | PDF D26 a D28 |
| C-D30 | 2026-10-30 | [hospedagem] | catalogo.solucaointeligentes.com na VPS srv1849835, deploy rsync por Action, links antigos por 404.html | vigente | E30 |
| C-D31 | 2026-10-30 | [repo-visibilidade] | repo volta a ser privado (só a hospedagem sai do GitHub) | superada por C-D41 (2026-11-13, mesma direção) | E30 |
| C-D32 | 2026-10-30 | [relacao-pecas] | uma linha por perfil, ordem de código, iso + desenho + dados, sistemas compatíveis | vigente | E30 |
| C-D33 | 2026-11-13 17:25 | [entrada] | regularização A7, momento 3 Avançado | vigente | A7 D2 |
| C-D34 | 2026-11-13 17:27 | [branch] | main com exceção em projetos.excecoes_convencao | vigente | A7 D4 |
| C-D35 | 2026-11-13 17:26 | [bracket] | [CATALOGOTECNICO] | vigente | A7 D3 |
| C-D36 | 2026-11-13 17:27 | [alvo] | verdade = catalogo.solucaointeligentes.com; Pages só redireciona | vigente | A7 D5 |
| C-D37 | 2026-11-13 18:26 | [sem-n8n] | exceção sem_n8n (etapas 4-8, 10, 12 N/A) | vigente | A7 D8 |
| C-D38 | 2026-11-13 18:34 | [demanda-21] | INCONSISTENTE com observação de encerramento | vigente | A7 D10 |
| C-D39 | 2026-11-13 18:34 | [relatorios] | referencia_layout_sitesolu.md versionado; relatorios/teste_visual/ ignorado | vigente | A7 D9 |
| C-D40 | 2026-11-13 19:41 | [gate] | producao | vigente | A7 D13 |
| C-D41 | 2026-11-13 19:24 | [repo-visibilidade] | repo privado na instrução; tornar privado na interface = pendência 3w | vigente | A7 D11 |

## 3. Decisões vigentes por assunto
| [assunto] | id | data/hora | decisão |
|---|---|---|---|
| [alvo] | C-D36 | 2026-11-13 17:27 | verdade na VPS (catalogo.solucaointeligentes.com); ensaio build local + Live Server |
| [blindex-fabricante] | C-D24 | 2026-10-29 12:40 | Blindex cita a Solução como fabricante |
| [bracket] | C-D35 | 2026-11-13 17:26 | [CATALOGOTECNICO] |
| [branch] | C-D34 | 2026-11-13 17:27 | main com exceção registrada |
| [demanda-21] | C-D38 | 2026-11-13 18:34 | INCONSISTENTE com observação |
| [dsl] | C-D16 | 2026-10-28 20:11 | UHMW-PE |
| [dupla-marca] | C-D1 | 2026-09-15 23:05 | marcas.yaml, 4 categorias com dois nomes |
| [entrada] | C-D33 | 2026-11-13 17:25 | regularização A7, Avançado |
| [escrita-governanca] | C-D22 | 2026-10-29 11:39 | só Code com scripts e motor |
| [ficha-prevalece] | C-D14 | 2026-10-28 19:15 | ficha individual; exceções SS-002 e FE-0207 |
| [formato-bloco] | C-D23 | 2026-10-29 | destino fora do bloco de cópia |
| [gate] | C-D40 | 2026-11-13 19:41 | producao |
| [graficos] | C-D19 | 2026-10-28 22:29 | método clássico, adiados |
| [guia] | C-D26 | 2026-10-29 18:20 | GUIA_EDICAO.md no repo |
| [hospedagem] | C-D30 | 2026-10-30 | VPS srv1849835, deploy por Action |
| [imagens-fonte] | C-D7 | 2026-09-23 10:30 | só src; docs/ gerado |
| [imagens-pasta] | C-D10 | 2026-10-27 17:13 | pasta única |
| [layout] | C-D20 | 2026-10-28 23:32 | tema escuro SITESOLU |
| [navegacao] | C-D17 | 2026-10-28 20:43 | trilha hierárquica |
| [nome-imagem] | C-D12 | 2026-10-28 14:51 | {codigo}-{descrição da ficha}, minúsculo |
| [ordem-marcas] | C-D21 | 2026-10-29 00:00 | Blindex junto com a Solução |
| [ordem-perfis] | C-D18 | 2026-10-28 21:20 | por código |
| [pdf] | C-D29 | 2026-10-29 20:13 | 2 fichas/página, 10 PDFs, botão |
| [preferencias] | C-D28 | 2026-10-29 19:52 | regra na conduta |
| [relacao-pecas] | C-D32 | 2026-10-30 | uma linha por perfil |
| [relatorios] | C-D39 | 2026-11-13 18:34 | referência versionada, teste visual ignorado |
| [repo] | C-D15 | 2026-10-28 20:23 | conexaoiatech/catalogo-tecnico |
| [repo-visibilidade] | C-D41 | 2026-11-13 19:24 | privado (falta tornar na interface) |
| [sem-n8n] | C-D37 | 2026-11-13 18:26 | exceção sem_n8n |
| [stack] | C-D3 | 2026-09-15 23:19 | Python + Jinja2 + YAML, docs/ gerado |

## 4. Artefatos e commits relevantes
| id | data/hora | tipo | nome ou caminho | estado | origem |
|---|---|---|---|---|---|
| C-A1 | 2026-09-17 13:30 | commit | c8dc33f SS-002 e integridade de imagens | em origin/main | EST P62 |
| C-A2 | 2026-10-28 19:50 | código | src/build.py, scripts/padroes.py, scripts/validar_catalogo.py (aa73c96) | vigente | IMG A6 |
| C-A3 | 2026-10-28 18:28 | script | scripts/calcular_propriedades_dxf.py | validado | IMG A5 |
| C-A4 | 2026-10-28 22:20 | dados | src/data/estrutural.yaml (PRELIMINAR), scripts/grafico_pressao.py | não publicado | IMG A7, A8 |
| C-A5 | 2026-10-29 00:43 | commit | 470f5f6 Blindex publicada | em origin/main | IMG P39 |
| C-A6 | 2026-10-29 18:30 | docs | docs/PLANO.md, docs/ROTEIRO.md, CLAUDE.md, GUIA_EDICAO.md (10f0a91, d851fcc) | vigente | GOV A17 |
| C-A7 | 2026-10-29 21:08 | site | 10 PDFs em docs/pdf (6c11ba0), src/build_pdf.py | publicados; não determinísticos (demanda 300) | PDF A18 a A20 |
| C-A8 | 2026-10-30 | infra | stack nginx na VPS srv1849835, Action deploy-vps (secrets DEPLOY_SSH_KEY, DEPLOY_KNOWN_HOSTS) | no ar | E30 |
| C-A9 | 2026-10-30 | commit | 7815278 relação de peças | em origin/main | E30 |
| C-A10 | 2026-11-13 19:22 | commit | 7cc213b regularização A7 (.gitignore, MANUAL, PLANO, INSTRUÇÃO) | em origin/main | A7 P8 |
| C-A11 | 2026-11-13 19:28 | commit | d353e00 ajustes A7 (CLAUDE.md, repo privado, docs/hist/arquivo) | em origin/main | A7 P9 |
| C-A12 | 2026-11-13 19:43 | commit | c758b2f ESTADO_SESSAO gerado do banco | em origin/main | A7 P10 |

## 5. Contradições resolvidas e "a confirmar"
| data/hora | [assunto] | antiga → vigente | como resolveu |
|---|---|---|---|
| 2026-10-26 18:0x | [resize] | 1000×1000 [PROPOSTO] → originais mantidos e cópias otimizadas no build | a confirmar com a pessoa (sem decisão datada) |
| 2026-10-26 | [ids-hist] | D, P e A com significados diferentes entre HIST antigos | resolvido: o consolidado usa C-D/C-M/C-A com origem |
| 2026-10-29 / 2026-11-13 | [plano-numeracao] | "repo público" é D30 no HIST GOV e D27 no PLANO | resolvido: vale o texto e a data; PLANO marcado superada |
| 2026-10-30 / 2026-11-13 | [roteiro-numero] | passo 109 em dois registros (gov_passos 110 e 158) | a confirmar; identificar por id de gov_passos |
| 2026-09-23 / 2026-10-28 | [layout] | Netlify cancelado → SITESOLU | resolvido pela data mais recente (C-D20) |

## 6. Índice de HIST
| data | arquivo (docs/hist/arquivo/) | título | sessões |
|---|---|---|---|
| 2026-09-15 a 09-29 | HIST_2026-09-15_a_2026-09-29_catalogo_tecnico_estrutura-dupla-marca-imagens.md | estrutura, dupla marca, imagens, DSL | nenhuma |
| 2026-09-18 a 10-26 | HIST_2026-09-18_a_2026-10-26_catalogo_tecnico_reconstrucao-gov-demandas.md | reconstrução de gov_demandas | nenhuma |
| 2026-10-26 | HIST_2026-10-26_a_2026-10-26_catalogo_tecnico_status-projeto.md | status do projeto | nenhuma |
| 2026-10-26 | HIST_2026-10-26_a_2026-10-26_catalogo_tecnico_atualizacao-gov-demandas.md | skill de relatório e reconciliação | nenhuma |
| 2026-10-26 | HIST_2026-10-26_a_2026-10-26_catalogo_tecnico_push-hist-estado-sessao.md | push de HIST e 1º ESTADO | nenhuma |
| 2026-10-26 a 10-29 | HIST_2026-10-26_a_2026-10-29_catalogo_tecnico_imagens-dados-layout-blindex.md | imagens, dados, layout, Blindex | 93/94, 95/96 |
| 2026-10-29 | HIST_2026-10-29_a_2026-10-29_catalogo_tecnico_governanca-instrucao.md | governança e instrução | 97/98 |
| 2026-10-29 | HIST_2026-10-29_a_2026-10-29_catalogo_tecnico_catalogo-pdf.md | catálogo em PDF | nenhuma |
| 2026-10-30 | [sem HIST] chat da hospedagem e da relação de peças | resumo no espelho ESTADO 2026-10-30 | 99/100 |
| 2026-11-13 | HIST_2026-11-13_a_2026-11-13_catalogo_tecnico_projnovo-regularizacao-a7.md | /projnovo e regularização A7 | 124/125 |
