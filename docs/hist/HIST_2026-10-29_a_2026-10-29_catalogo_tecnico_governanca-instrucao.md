# HIST_2026-10-29_a_2026-10-29_catalogo_tecnico_governanca-instrucao
Chat: Imagens de perfil, dados técnicos, layout e versão Blindex (continuação) · Projeto: catalogo_tecnico · Conta: [NÃO INFORMADO] · Período: 2026-10-29 00:56 a 2026-10-29 22:29 · Mensagens: ~70 · Gerado em: 2026-10-29 22:31 · Prompt: v3.4
Sessões: 97/98 · abertas no encerramento: 97 (claude_ia, início 11:20) e 98 (claude_code, início 12:24:25) — fechar com "estou saindo"
Referência: HIST_2026-10-26_a_2026-10-29_catalogo_tecnico_imagens-dados-layout-blindex.md (seções 7 e 10, período até 2026-10-29 00:50) e espelho claude/ESTADO_CATALOGO_TECNICO.md (versão de 2026-10-29 12:41)

## 0. Contexto herdado (JÁ REGISTRADO, máx. 5 linhas)
| data/hora | fato | ponteiro |
|---|---|---|
| 2026-10-29 00:43 | Passos 81 a 101 fechados, Solução e Blindex publicadas, sessões 95/96 fechadas | Referência P39 |
| 2026-10-29 00:56 | HIST anterior registrado no repo (commit 7f58215) | Referência seção 15 |
| 2026-10-29 00:52 | Pendências: UPDATEs de demandas, Blindex citando a Solução, arquivos soltos, gráficos, 3D | Referência seção 10 |

## 1. Resumo
Sessão de arrumação e governança. As demandas foram postas em dia (20, 22, 295, 296 fechadas; 21 INCONSISTENTE; duas demandas novas), primeiro por SQL manual no Adminer — erro do Claude.ai, corrigido para o protocolo dos scripts. O SS-016 deixou de ser ficha em destaque no BigSpace, a edição manual da pessoa em marcas.yaml foi publicada, o .gitignore passou a bloquear CAD e referencia/, e o repo ganhou PLANO, ROTEIRO, CLAUDE.md, INSTRUÇÃO_CLAUDE_IA.txt e GUIA_EDICAO.md. A instrução do projeto foi consolidada pelo Code e a preferência "uma pergunta por vez" passou para a conduta (v2026-10-29a). O bloco final 3x foi entregue, sem PARADA recebida.

## 2. Rota
| # | data/hora | evento | tipo | ids (P/D/A) |
|---|---|---|---|---|
| 1 | 2026-10-29 11:20 | Estou entrando (sessão nova) | início | — |
| 2 | 2026-10-29 11:30 | UPDATEs e INSERTs de demanda rodados à mão no Adminer por SQL gerado pelo Claude.ai | erro relevante | P41 |
| 3 | 2026-10-29 11:39 | MUDOU ROTA: escrita em gov_* só pelo Code com scripts (de SQL manual no Adminer → gov-demanda.ps1) | MUDOU ROTA | D27 |
| 4 | 2026-10-29 12:40 | Blindex mantém a Solução como fabricante | decisão | D26 |
| 5 | 2026-10-29 16:44 | SS-016 aparecia como ficha aberta no BigSpace | erro relevante | P43 |
| 6 | 2026-10-29 18:23 | Repo continua público; guia vira GUIA_EDICAO.md no repo | decisão | D29, D30 |
| 7 | 2026-10-29 19:34 | Instrução do 3u veio de versão antiga reconstruída pelo Claude.ai | erro relevante | P47 |
| 8 | 2026-10-29 19:52 | MUDOU ROTA: "uma pergunta por vez" sai da instrução e entra na conduta (de regra do projeto → regra geral v2026-10-29a) | MUDOU ROTA | D32, A20 |
| 9 | 2026-10-29 22:29 | Fim: encerramento do chat, sessões 97/98 abertas, PARADA do 3x não recebida | fim | P50 |

## 3. Objetivo e escopo → PLANO
| data/hora | item | conteúdo |
|---|---|---|
| 2026-10-29 18:23 | entregas (PLANO, aprovado ao colar o bloco do 3t) | E1 base YAML · E2 imagens e fichas · E3 site Solução · E4 Blindex (feitas) · E5 dados estruturais e gráficos (em análise) · E6 governança e guia (em execução até o 3t) |
| 2026-10-29 18:23 | critério de sucesso | Solução e Blindex publicadas · 100% dos perfis completos e validados no build · navegação por sistema e perfil · gráficos validados pelo responsável técnico |
| 2026-10-29 19:43 | instrução do projeto | consolidada pelo Code (3w): sem a linha "Ordem", com F98, nomes por marca do marcas.yaml e site no Repo |

## 4. Decisões → PLANO
| id | data/hora | de → para | motivo | impacto |
|---|---|---|---|---|
| D26 | 2026-10-29 12:40 | — → Blindex mantém a Solução como fabricante (rodapé, link de troca, frase "sob licença") | é a empresa fabricante | site sem mudança |
| D27 | 2026-10-29 11:39 | regra D4 "demanda manual via Adminer" → escrita em gov_* só pelo Code com gov-*.ps1 | planejamento e skill estou-entrando-saindo | registros manuais ficam; próximos só por script |
| D28 | 2026-10-29 17:08 | — → fechar demanda 21 como INCONSISTENTE e 295 se a varredura não achar CAD | seguir o recomendado | 3s |
| D29 | 2026-10-29 18:20 | PDF do guia → PDF temporário; referencia/ no .gitignore; guia oficial = GUIA_EDICAO.md no repo, atualizado pelo Code no mesmo commit | quer arquivo sempre atualizado | 3t |
| D30 | 2026-10-29 18:23 | — → repo continua público | Pages no plano Free exige repo público; site é público por link | sem custo; decisão sobre plano pago adiada |
| D31 | 2026-10-29 16:44 | SS-016 como ficha em destaque → card igual aos outros | consistência | 3q |
| D32 | 2026-10-29 19:52 | "uma pergunta por vez" na instrução → regra na conduta v2026-10-29a (§1) | instrução já manda ler a conduta | vale para todos os projetos; instrução sem linha de preferências |

## 5. Passos → ROTEIRO
| id | data/hora | nº roteiro | ação | alvo | evidência curta (com hash, se houver) | status |
|---|---|---|---|---|---|---|
| P41 | 2026-10-29 11:35 | — (pessoa no Adminer) | UPDATEs 20, 22, 295, 296 e 2 INSERTs de demanda | gov_demandas | 6 registros afetados; fora do protocolo | FEITO |
| P42 | 2026-10-29 12:24 | abertura | Sessões 97 e 98 abertas e vinculadas | gov_sessoes | ids 97/98; último commit 7f58215 | FEITO |
| P43 | 2026-10-29 16:47 | 3q (gov 102) | SS-016 como card no BigSpace e Vista | portas-robustas.yaml | 1b5de79 | FEITO |
| P44 | 2026-10-29 17:11 | 3s (gov 103) | WF-GOV-REGISTRO conferido (sem ação), demanda 21 INCONSISTENTE e 295 FINALIZADO por script, arquivos soltos em cad-fonte/_arquivo, .gitignore bloqueia CAD | gov_demandas, .gitignore | e47d447 | FEITO |
| P45 | 2026-10-29 ~17:40 | 3r (gov 104) | Publicar edição manual da pessoa em marcas.yaml | src/data/marcas.yaml | 95263a7 | FEITO |
| P46 | 2026-10-29 18:30 | 3t (gov 105) | PLANO, ROTEIRO, CLAUDE.md, INSTRUÇÃO e GUIA_EDICAO; demanda 296 fechada | docs, raiz | 10f0a91 | FEITO |
| P47 | 2026-10-29 19:30 | 3u (gov 106) | ROTEIRO, protótipo fora do git, README e instrução (texto antigo) | ROTEIRO, README, INSTRUÇÃO | d851fcc | FEITO |
| P48 | 2026-10-29 19:43 | 3w (gov 107) | Instrução consolidada em INSTRUÇÃO_CLAUDE_IA_atualizada.txt | raiz | sem commit | FEITO |
| P49 | 2026-10-29 19:52 | — | Conduta v2026-10-29a entregue para atualizar a skill no Claude.ai | skill conduta | texto entregue no chat | FEITO |
| P50 | 2026-10-29 20:50 | 3x | Instrução consolidada vira oficial, _old arquivado, README, ROTEIRO e PLANO | raiz, docs | bloco entregue, PARADA não recebida | PENDENTE |

## 6. Artefatos
Commits: 1b5de79 SS-016 como card · e47d447 gitignore bloqueia CAD · 95263a7 edição manual em marcas.yaml · 10f0a91 PLANO, ROTEIRO, CLAUDE.md, instrução e guia · d851fcc roteiro, protótipo fora do git e instrução
| id | data/hora | tipo | nome ou caminho | estado atual |
|---|---|---|---|---|
| A16 | 2026-10-29 16:47 | documento online | Guia rápido — editar textos do Catálogo Técnico (Claude Docs) | superado por GUIA_EDICAO.md (D29) |
| A17 | 2026-10-29 18:30 | documentos no repo | docs/PLANO.md, docs/ROTEIRO.md, CLAUDE.md, GUIA_EDICAO.md | publicados (10f0a91, d851fcc) |
| A18 | 2026-10-29 19:43 | instrução | INSTRUÇÃO_CLAUDE_IA_atualizada.txt (consolidada) | vira INSTRUÇÃO_CLAUDE_IA.txt no 3x (pendente de confirmação) |
| A19 | 2026-10-29 17:11 | pasta | cad-fonte\_arquivo\ (log_solu_fd_pt.png, cópia do espelho, protótipo HTML, _old da instrução) | fora do git |
| A20 | 2026-10-29 19:52 | skill | conduta v2026-10-29a (§1 com "uma pergunta por vez") | texto entregue; pessoa atualiza no Claude.ai |
| A21 | 2026-10-29 12:41 | espelho | claude/ESTADO_CATALOGO_TECNICO.md (Projeto) | última versão 12:41; não reflete 3q em diante |
| A22 | 2026-10-29 22:31 | documento | HIST_2026-10-29_a_2026-10-29_catalogo_tecnico_governanca-instrucao.md | gerado, falta registrar no repo (seção 15) |

## 7. Estado final → ESTADO
Última ação: bloco 3x entregue (20:50), PARADA não recebida. Último passo provado: gov 107 (3w); último commit provado d851fcc com push. Sessões 97 e 98 ABERTAS. Demandas: 17, 18, 19, 20, 22, 295, 296 e "Navegacao, layout escuro e versao Blindex" FINALIZADO_SUCESSO; 21 INCONSISTENTE; "Dados estruturais e grafico de pressao" EM_ANALISE (única aberta). Próximo passo exato: confirmar a PARADA do 3x (ou colar o bloco se não rodou) → "estou saindo" para fechar 97/98 e atualizar ESTADO_SESSAO e espelho.

## 8. Procedimentos → MANUAL
1. Editar texto do catálogo (validado 2026-10-29 17:40): VS Code na pasta raiz C:\GITHUB\CATALOGO_TECNICO (Trust Folder; extensões YAML Red Hat e Live Server; fechar o chat do Copilot) → Ctrl+Shift+F em src → editar → Ctrl+S → `python src\build.py` → conferir com Live Server em docs\index.html → publicar pelo Claude Code com bloco de publicação (abre passo, git diff, valida, build, commit, push, fecha passo). Detalhe em GUIA_EDICAO.md.
2. Escrita em governança (validado 2026-10-29 17:11): demandas só por `gov-demanda.ps1 criar|atualizar` (WF-GOV-REGISTRO grava só gov_demandas: project_id, titulo, status, data_inicio=now(), observacao, ref_externa; atualizar usa COALESCE). Status aceitos: EM_ANALISE, EM_ESTRUTURACAO, EM_EXECUCAO, FINALIZADO_SUCESSO, PENDENTE, INCONSISTENTE.

## 9. Lições
| data/hora | problema | causa | solução | evidência |
|---|---|---|---|---|
| 2026-10-29 11:39 | SQL de demanda gerado pelo Claude.ai e rodado à mão | Claude.ai seguiu regra D4 de HIST antigo, superada pela skill | skill vale sobre HIST; escrita só por gov-*.ps1 no Code | D27, P41 |
| 2026-10-29 19:34 | instrução gravada com texto antigo | Claude.ai reconstruiu a instrução de memória | instrução sempre a partir da fonte (Projeto ou arquivo), consolidada pelo Code com conferência no repo | P47, P48 |
| 2026-10-29 16:50 | pessoa abriu só a pasta src e o chat do Copilot no VS Code | ambiente novo | abrir a raiz; não usar o Copilot para editar o catálogo | GUIA_EDICAO.md |
| 2026-10-29 17:30 | edição manual da pessoa ficou fora do commit do 3s | blocos com git add de arquivos nomeados | bloco próprio de publicação com git diff antes | P45 |

## 10. Pendências → FILA
| data/hora aberta | item | origem | depende de | urgência |
|---|---|---|---|---|
| 2026-10-29 20:50 | Confirmar PARADA do 3x (instrução oficial, _old arquivado, README, ROTEIRO, PLANO) ou colar o bloco | P50 | Code | alta |
| 2026-10-29 12:24 | Fechar sessões 97 e 98 ("estou saindo"), atualizar docs/ESTADO_SESSAO.md e espelho | P42 | Claude.ai + Code | alta |
| 2026-10-29 19:52 | Confirmar que a skill conduta foi atualizada para v2026-10-29a no Claude.ai | A20 | pessoa | média |
| 2026-10-29 11:35 | Ids das 2 demandas criadas à mão (ROTEIRO cita sem id) | P41 | leitura no banco | baixa |
| 2026-10-28 22:29 | E5: modelo estrutural por sistema com Coordenador de Produção; 16 DXF; teto de flecha na NBR 10821-2:2023 | Referência | informação técnica | média |
| 2026-10-28 21:39 | 3D por extrusão do DXF | Referência | DXF limpos | baixa |
| 2026-10-28 23:54 | Ficha repete a tabela; pinch-zoom no aparelho; logo com fundo convertido | Referência | teste em aparelho | baixa |
| 2026-10-29 18:21 | Repo privado (plano Team ou Netlify) — reavaliar se houver conteúdo sensível | D30 | decisão | baixa |
| 2026-10-29 19:43 | relatorios/referencia_layout_sitesolu.md e relatorios/teste_visual/ sem rastreio — decidir destino | P48 | pessoa | baixa |

## 11. Precedência e contradições
| data/hora antiga | data/hora vigente | assunto | antiga → vigente (ponteiros) | sentido |
|---|---|---|---|---|
| HIST anterior (regra D4) | 2026-10-29 11:39 | escrita em gov_demandas | manual via Adminer → só scripts no Code (D27) | chat supera; skill vence HIST |
| Referência seção 10 (id 21 "proposta INCONSISTENTE") | 2026-10-29 17:10 | demanda 21 | pendente → INCONSISTENTE pelo script (P44) | chat supera |
| Referência seção 10 (295, 296 abertas) | 2026-10-29 17:11 / 18:29 | demandas 295 e 296 | abertas → FINALIZADO_SUCESSO (P44, P46) | chat supera |
| Referência seção 10 (Blindex cita a Solução) | 2026-10-29 12:40 | menção à Solução na Blindex | a decidir → mantém (D26) | chat supera |
| instrução antiga ("Ordem: Solução primeiro") | 2026-10-29 19:43 | instrução do projeto | linha "Ordem" → removida, superada pela D25 (P48) | chat supera |
| 2026-10-29 19:29 (3u) | 2026-10-29 19:43 (3w) | texto da instrução no repo | versão antiga do Claude.ai → consolidada pelo Code | interna |
| instrução (Preferências) | 2026-10-29 19:52 | "uma pergunta por vez" | instrução → conduta v2026-10-29a (D32) | interna |
| 2026-10-29 16:46 | 2026-10-29 18:23 | guia de edição | documento online → GUIA_EDICAO.md no repo (D29) | interna |

## 12. Outros
Preferências do usuário: uma pergunta por vez (agora na conduta); conferir antes de substituir imagens (na instrução). Ferramenta adotada pela pessoa: VS Code com YAML (Red Hat) e Live Server. Omitido por sigilo: nenhum.

## 13. Checagem
Commits no chat 5 = seção 6 5 · Decisões do usuário 7 = seção 4 7 · MUDOU ROTA 2 = seção 2 2 · Sessões do chat 1 = cabeçalho 1 · Nenhum HISTÓRICO como vigente nas seções 3, 4 e 7: sim.

## 14. Pode apagar?
NÃO, ainda não: falta (1) confirmar a PARADA do 3x e (2) fechar as sessões 97 e 98 com "estou saindo". Depois disso e do bloco da seção 15, pode apagar.

## 15. Bloco para o Claude Code (registrar o HIST no repo)
Salve o HIST em C:\GITHUB\CATALOGO_TECNICO\docs\hist\ e cole o bloco no Claude Code: C:\GITHUB\CATALOGO_TECNICO
```
[TL-catalogo_tecnico-CODE] EXECUTAR:
Registrar no repo o HIST HIST_2026-10-29_a_2026-10-29_catalogo_tecnico_governanca-instrucao.md, salvo pela pessoa em docs\hist\.
ZONAS: leitura | repo-escrita
SENSÍVEIS: !git push origin main
TOLERADO: nenhum. NÃO DECLARADO: anotar e seguir.
ESCOPO DECLARADO:
1. Conferir que docs\hist\HIST_2026-10-29_a_2026-10-29_catalogo_tecnico_governanca-instrucao.md existe. Se não existir: PARADA.
2. git add docs/hist/HIST_2026-10-29_a_2026-10-29_catalogo_tecnico_governanca-instrucao.md
3. git commit -m "docs(hist): governanca-instrucao (2026-10-29)"
4. SENSÍVEL git push origin main
Proibido: abrir ou fechar sessão, alterar passos, demandas ou ESTADO_SESSAO.
PARADA FINAL: hash e push.
```
