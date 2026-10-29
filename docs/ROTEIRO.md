# Roteiro — catalogo_tecnico
Origem: gov_passos 79 a 106 (HIST 2026-10-26 a 2026-10-29 e passos 102 a 106 desta sessão). A coluna # é o id em gov_passos; o nº do roteiro vem antes da ação.
Demanda: 20 para os passos 79 a 101 (ESTADO_SESSAO). Os passos 102 a 104 foram abertos sem demanda no registro. As duas demandas criadas à mão em 2026-10-29 ("Navegacao, layout escuro e versao Blindex do catalogo" e "Dados estruturais e grafico de pressao por sistema") não têm id neste repo.
Progresso: 28/28 passos FEITO.

| # | passo | entrega | demanda | alvo | status | evidência |
|---|---|---|---|---|---|---|
| 79 | 1 · Inventário das imagens de perfil | E2 | 20 | src/assets/img/perfis | FEITO | 59 arquivos, 0 OK; relatorios/inventario_imagens_perfis.md |
| 80 | 2a · Matriz perfil × sistema pelos YAML | E1 | 20 | src/data | FEITO | 34 perfis, 12 com descrição |
| 81 | 2b · Limpeza e planilha de referências | E1 | 20 | relatorios/referencias_perfis.csv | FEITO | 40 linhas, 6 SEM_YAML |
| 82 | 2b2 · Ler fichas das imagens e renomear | E2 | 20 | 41 fichas, 72 arquivos | FEITO | relatorios/fichas_lidas.csv e renomeacao_imagens.csv |
| 83 | 2b3 · Reler 4 fichas corrigidas, renomear pendentes | E2 | 20 | FE-0207, DSL-001, SS-002, SS-014 | FEITO | 39 de 40 OK |
| 84 | 2c · Aplicar a planilha nos YAML | E1 | 20 | src/data | FEITO | 64b3580; 6 YAML criados, 34 alterados, 21 divergências |
| 85 | 2d · Ripado com lista, referências reaplicadas, CAD fora de src | E1 | 20 | src/data, cad-fonte | FEITO | 5f9c2d7 |
| 86 | 4b · Jx/Jy e W pelos DXF (partes 1 a 3: FE, LT-077, FE-0207 e LT-077 corrigidos) | E1 | 20 | 5 FE, LT-077 e 7 YAML | FEITO | d6e62c6, 4cc2746, 984f21e; SS-108 ~0% |
| 87 | 3b · Build com validador, padrão minúsculo, preservação de governança | E1 | 20 | src/build.py, scripts/padroes.py | FEITO | aa73c96 |
| 88 | 3c · Imagem em todos os cards, status calculado, notas sem contagem | E2 | 20 | templates, YAML | FEITO | 95ab85e |
| 89 | 3d · Material UHMW-PE nos DSL | E1 | 20 | DSL-001 a DSL-003 | FEITO | 049a4c5; 40/40 completos |
| 90 | 3e · Desenho maior e lightbox | E3 | 20 | CSS e JS | FEITO | f751915 |
| 91 | 3f · Página por perfil, biblioteca como índice, menu | E3 | 20 | templates | FEITO | 3b7ca72 |
| 92 | 3g · Trilha, voltar um nível, ?de=, vizinhos por sistema | E3 | 20 | templates e JS | FEITO | 0268331 |
| 93 | 3h · SS-024 fora do MWO, matriz para revisão | E1 | 20 | YAML | FEITO | ec557a6; relatorios/matriz_sistemas.md |
| 94 | 3i · SS-018 e SS-019 na Sacada | E1 | 20 | YAML | FEITO | 7d1894a |
| 95 | 3j · Ordem por código | E3 | 20 | scripts/padroes.py | FEITO | 600c1a9 |
| 96 | 3k · Logos na entrada e no cabeçalho, marcas.yaml | E3 | 20 | src/assets/img/marcas | FEITO | f751bfe |
| 97 | 6-8 · FE-0205 = Bagete 22.5 Graus (parte A) e dados estruturais, grafico_pressao.py, dxf_pendentes (parte B) | E5 | 20 | YAML, imagens, src/data/estrutural.yaml, scripts | FEITO | ae436c4 e bb77a8d; teste MM-040 0,01%; gráficos não publicados |
| 98 | 3m · Fichas FE com Jx/Jy: conferência e substituição | E2 | 20 | 6 fichas | FEITO | 985e0f4 e 9fc6543 |
| 99 | 3n · Referência SITESOLU, teste visual e layout escuro | E3 | 20 | templates e CSS | FEITO | 515137d |
| 100 | 3o · Versão Blindex, entrada com escolha de marca, redirecionamentos | E4 | 20 | docs/blindex | FEITO | 1d8fe17 e 280792c |
| 101 | 3p · Blindex sem "Solução Sacadas", fonte "Desenho-mestre CAD", ESTADO_SESSAO | E4 | 20 | marcas.yaml, biblioteca.yaml, docs/ESTADO_SESSAO.md | FEITO | 470f5f6 |
| 102 | 3q · Remover ficha em destaque do SS-016 no BigSpace | E3 | — | portas-robustas.yaml | FEITO | 1b5de79; BigSpace e Vista com 18 cards |
| 103 | 3s · Arrumação: demandas manuais, demanda 21, limpeza e varredura de CAD | E6 | 21 e 295 por script | .gitignore, cad-fonte/_arquivo | FEITO | e47d447; nenhum CAD rastreado |
| 104 | 3r · Publicar alteração manual da pessoa em marcas.yaml | E3 | — | src/data/marcas.yaml | FEITO | 95263a7 |
| 105 | 3t · Governança no repo: PLANO, ROTEIRO, CLAUDE.md, INSTRUÇÃO e GUIA_EDICAO | E6 | 296 | docs, raiz | FEITO | 10f0a91 |
| 106 | 3u · Ajustes do 3t: ROTEIRO, protótipo fora do git e instrução do projeto | E6 | 296 | docs/ROTEIRO.md, README.md, INSTRUÇÃO_CLAUDE_IA.txt | FEITO | ver git log |

## Fila (espelho de gov_demandas backlog)
- 2026-10-28 · Gráficos de pressão: definir o modelo estrutural por sistema (Sacada: vão do vidro; SkinGlass: conjunto coluna + meio-coluna) com o Coordenador de Produção; estrutural.yaml segue PRELIMINAR e publicar_graficos false · D22 (E5)
- 2026-10-28 · 16 DXF de perfis estruturais pendentes (relatorios/dxf_pendentes.md), a entregar só depois do modelo definido · passo 97
- 2026-10-28 · Visualização 3D girando por extrusão do DXF (three.js), proposta, depende dos DXF limpos · chat
- 2026-10-28 · A ficha do perfil ainda repete a tabela de dados (problema visual 6, parcial) · passo 99
- 2026-10-28 · Pinch-zoom no celular não testado em aparelho · passo 99
- 2026-10-28 · Conferir o logo solucao_pt com o fundo convertido em transparência · passo 99
- 2026-10-28 · Avisar quem tem o link antigo do site (Solucao-Fechamento-Inteligente, hoje 404) · D16
- 2026-10-29 · Decisão sobre repo privado (hoje público, D27) · bloco do passo 105
