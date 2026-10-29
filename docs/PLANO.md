# Plano — catalogo_tecnico
Objetivo: Catálogo técnico HTML dos sistemas de envidraçamento da Solução (Sacada, MWO, BigSpace, SkinGlass, Ripado, Persianas) e das versões Blindex, para vidraceiros e equipe consultarem perfis, desenhos e especificações por link, com cada dado técnico mantido em fonte única.
Critério de sucesso: Solução e Blindex publicadas · 100% dos perfis completos e validados no build · navegação por sistema e por perfil · gráficos estruturais validados pelo responsável técnico.
Entregas (cada uma cita a parte do objetivo):
- E1 · Base de dados YAML em fonte única — FEITA (objetivo: "cada dado técnico mantido em fonte única")
- E2 · Imagens padronizadas e fichas aplicadas — FEITA, demanda 20 (objetivo: "perfis, desenhos e especificações")
- E3 · Site Solução com navegação e layout — FEITA (objetivo: "consultarem por link, por sistema e por perfil")
- E4 · Versão Blindex — FEITA (objetivo: "versões Blindex")
- E5 · Dados estruturais e gráficos de pressão — EM ANÁLISE, demanda nova de gráficos (objetivo: "especificações"; critério: gráficos validados pelo responsável técnico)
- E6 · Governança no repo e guia de edição — EM EXECUÇÃO, demanda 296 (objetivo: manter o catálogo por quem o consulta e o atualiza)
Fora de escopo: publicar CAD bruto; preços e condições comerciais; linha de adesivos e selantes Blindex/Neoklon; migração para o servidor próprio definitivo; editar à mão arquivos gerados em docs/.

## Decisões
Formato: id · data · de → para · motivo · impacto.
- D1 · 2026-10-27 · subpastas por produto → pasta única src/assets/img/perfis · perfil compartilhado entre sistemas · a pessoa achatou as pastas; o build lê só a raiz
- D2 · 2026-10-27 · SS-0108 → ss-108 (confirmado em 2026-10-28 pela ficha "SS-0108 Montante do Vidro 12 mm") · código oficial · a leitura "SS-0208" foi erro de OCR
- D3 · 2026-10-27 · lista sem os FE → FE: 6 perfis (0202, 0203, 0204, 0205, 0207, 0208), código com 4 dígitos, DXF em cad-fonte\ARQUIVOS\SKINGLASS, dados calculados · faltavam na lista · YAML criados e preenchidos
- D4 · 2026-10-28 · push em master → main · master não existe · todos os blocos usam main
- D5 · 2026-10-28 · duas imagens do SS-014 → fica SS-014-capa_uniao (o outro foi apagado pela pessoa) · duplicata · ss-014-capa_de_uniao
- D6 · 2026-10-28 · renomear no passo 3 → renomear junto com a leitura das fichas, nome = {codigo}-{descrição da ficha} · pedido da pessoa · 72+ imagens renomeadas
- D7 · 2026-10-28 · ficha vale sobre o YAML → SS-002: vale o YAML (c8dc33f), não a ficha · correção anterior · exceção à regra da ficha
- D8 · 2026-10-28 · descrições FE e LT-077 em aberto → descrições definidas pela pessoa (Bagete Passante, Capa Coluna Lateral, Acab. Vertical Meio Coluna - Passante/Colante, Baguete Vedação Vertical, Cantoneira Acab. Lateral) · ficha · YAML e nomes de imagem
- D9 · 2026-10-28 · Ripado sem lista → Ripado com bloco de perfis (planilha rev) · o sistema usa perfis · 18 códigos
- D10 · 2026-10-28 · FF-0205/FF-0207 → FE-0205/FE-0207; FE-0208.DXF já limpo; LT-077 = SACADA_BLINDEX\LT-077.dxf · arquivos limpos da pessoa · cálculo pelos DXF
- D11 · 2026-10-28 · FE-0207 área 247.42 → 274.43; LT-077 vale a ficha 25,8 × 25,8 · a imagem estava errada e o DXF também · imagem e DXF corrigidos pela pessoa
- D12 · 2026-10-28 · sem método → gráfico pelo método clássico (resistência e flecha, vale o menor), liga 6063-T5, validação pelo Coordenador de Produção · catálogo Alump inconsistente · premissas em estrutural.yaml (PRELIMINAR)
- D13 · 2026-10-28 · ESTADO na raiz → ESTADO em docs/ com o build preservando hist, ESTADO_SESSAO, PLANO e ROTEIRO · as skills esperam docs/ · lista PRESERVAR no build
- D14 · 2026-10-28 · imagem só em status completo → imagem em todos os cards; status calculado pelo build; notas sem contagem fixa; campos unificados · o site estava sem imagens · 40 perfis com imagem
- D15 · 2026-10-28 · DSL sem material → UHMW-PE (polietileno de ultra-alto peso molecular) · completar as fichas · 40/40 completos
- D16 · 2026-10-28 · repo Solucao-Fechamento-Inteligente → conexaoiatech (definitivo) · situação real do repo · site em conexaoiatech.github.io/catalogo-tecnico
- D17 · 2026-10-28 · botão "Menu principal" → navegação hierárquica (trilha, voltar um nível, origem ?de=, vizinhos por sistema); Blindex depois · a pessoa saía do produto · passo 3g
- D18 · 2026-10-28 · SS-024 em MWO → SS-024 fora do MWO (pele-vidro, portas-robustas, ripado) · erro de referência · passo 3h
- D19 · 2026-10-28 · SS-018 e SS-019 fora da Sacada → também na Sacada · uso real · Sacada com 17 perfis
- D20 · 2026-10-28 · ordem de cadastro → ordem por código (SS, LT, F, FE, DSL), regra no build · leitura · passo 3j
- D21 · 2026-10-28 · sem logos → logos solucao.png e blindex.png em src/assets/img/marcas; Solução na entrada e no cabeçalho · identidade · passo 3k
- D22 · 2026-10-28 · estruturais sem lista → perfis estruturais por sistema (Sacada SS-001/002/003/010/108; BigSpace SS-004/016/017/024/F98; SkinGlass SS-016/017/024/027/028, FE-0204, FE-0207; MWO SS-001/004/005/010/020/021/022/023/F98); FE-0205 = Bagete 22.5 Graus; acabamentos ficam; depois, gráficos adiados · lista da pessoa; o modelo de perfil isolado se mostrou inadequado · perfis_estruturais nos YAML de categoria; nada publicado
- D23 · 2026-10-28 · fichas FE sem Jx/Jy → fichas FE reexportadas com Jx/Jy; conferir antes de substituir · o vidraceiro lê a imagem · conferência em 2 fases
- D24 · 2026-10-28 · tema claro → tema escuro total no padrão SITESOLU; logo solucao_pt.png; aprovado pela pessoa · identidade do site da Solução · passo 3n
- D25 · 2026-10-29 · Blindex depois → Blindex agora; sem a nota "Nome técnico de origem"; sem "Solução Sacadas"; fonte "Desenho-mestre CAD" · pedido da pessoa · passos 3o e 3p publicados
- D26 · 2026-10-29 · Blindex sem decisão sobre o fabricante → Blindex mantém a Solução como fabricante · decisão da pessoa · textos da marca Blindex citam a Solução (ex.: "Licenciado Solução Fechamento Inteligente")
- D27 · 2026-10-29 · repo a decidir → repo continua público · decisão da pessoa · CAD bruto e dados comerciais nunca entram no git
- D28 · 2026-10-29 · guia de edição fora do repo → guia de edição vira GUIA_EDICAO.md no repo · mantê-lo junto do código que ele descreve · ao mudar caminho, arquivo de texto ou template, atualizar o guia no mesmo commit
- D29 · 2026-10-29 · escrita em gov_* por SQL manual (regra antiga, chamada D4 no GOV_IA_CORE, sem relação com o D4 deste plano) → escrita em gov_* só pelos scripts · regra antiga superada · demandas e passos passam por gov-demanda.ps1 e gov-passo.ps1
- D30 · 2026-10-29 · preferência "uma pergunta por vez" na instrução do projeto → regra da conduta v2026-10-29a (sai da instrução) · vale para todos os projetos · instrução consolidada no 3w/3x
