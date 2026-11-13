# HIST_2026-09-15_a_2026-09-29_catalogo_tecnico_estrutura-dupla-marca-imagens
Chat: Catálogo técnico — estrutura, dupla marca, imagens de perfil, DSL e SS-0108 · Projeto: catalogo_tecnico · Conta: [NÃO INFORMADO] · Período: ~2026-09-15 21:50 a 2026-09-29 12:28 (encerramento pedido em 2026-10-29 21:22, fora do período) · Mensagens: ~110 da pessoa (estimado) · Gerado em: 2026-10-29 21:22 · Prompt: v3.4
Sessões: nenhuma registrada neste chat (o "estou entrando" de 2026-09-23 10:24 não foi executado; o Code informou sessão não aberta em 2026-09-23 12:03) · abertas no encerramento: nenhuma por este chat; 97/98 segundo o espelho do ESTADO (fecham no próximo "estou saindo")
Referência: espelho ESTADO_CATALOGO_TECNICO.md (atualizado 2026-10-29 11:40) e HIST_2026-10-29_a_2026-10-29_catalogo_tecnico_catalogo-pdf.md (seções 7 e 10, período 2026-10-29 20:04 a 21:12). Para classificar também foram lidos HIST_2026-10-26_a_2026-10-29_catalogo_tecnico_imagens-dados-layout-blindex.md e HIST_2026-09-18_a_2026-10-26_catalogo_tecnico_reconstrucao-gov-demandas.md. Este chat é anterior à Referência: boa parte dele é HISTÓRICO.

## 0. Contexto herdado (JÁ REGISTRADO, máx. 5 linhas)
| data/hora | fato | ponteiro |
|---|---|---|
| 2026-10-29 11:40 | Fonte única do dado técnico (YAML em src/data), docs/ gerado pelo build, Pages em /docs na main; fora de escopo: preço e CAD bruto | instrução do projeto; ESTADO, Decisões |
| 2026-10-29 11:40 | Ficha individual prevalece; exceção SS-002 (vale o YAML, c8dc33f) | instrução do projeto; HIST 10-26_a_10-29 D7 |
| 2026-10-29 11:40 | Dupla marca em src/data/marcas.yaml (Solução e Blindex, 4 categorias com os dois nomes; Ripado e Persianas só Solução) | ESTADO, Decisões; HIST 10-26_a_10-29 D25 |
| 2026-10-29 11:40 | Id 21 (conduta-geral-big) pendente, proposta INCONSISTENTE; id 295 (varredura .dwg/.sldprt) pendente | ESTADO, Pendente |
| 2026-10-26 18:0x | Fechar o id 20 exige o push do c8dc33f | HIST 10-26_a_10-29, seção 0 |

## 1. Resumo
Partiu do pedido de um catálogo técnico HTML por produto, com o PDF "todos os produtos" e o site de produtos como referência. Passou por protótipo v1 e v2, pela correção para dupla marca Solução/Blindex, pelo plano do Claude Code (Python + Jinja2, GitHub Pages) e pela padronização de dados e imagens de perfil (SS-001, SS-002, nome de arquivo, PNG falso em JPG, commit c8dc33f). Terminou com DSL definido como perfil deslizante não-alumínio e o cálculo do SS-0108 por DXF aguardando aprovação. A maior parte foi superada pelo trabalho de 2026-10-26 a 2026-10-29: repo em conexaoiatech, layout escuro, Blindex publicada, PDFs.

## 2. Rota
| # | data/hora | evento | tipo | ids (P/D/A) |
|---|---|---|---|---|
| 1 | ~2026-09-15 21:50 | Início: pedido de catálogo técnico HTML por produto; PDF "todos os produtos" e site de produtos como referência; "NÃO EXECUTE NADA AINDA": primeiro modelo e coleta de material | início | P48 |
| 2 | ~2026-09-15 22:44 | Protótipo v1 monolítico (6 sistemas, biblioteca de perfis, selantes) publicado | marco | P49, A22 |
| 3 | ~2026-09-15 23:05 | MUDOU ROTA: nomes Blindex (Unique, Vista, Skin Vista) como nomes finais únicos → dupla marca (nome Solução azul / nome Blindex vermelho) em 4 categorias; Ripado e Persianas só Solução; Solução primeiro, Blindex depois | MUDOU ROTA | D29, P50, A23 |
| 4 | ~2026-09-15 23:19 | Plano do Code aprovado: repo privado catalogo-tecnico na org Solucao-Fechamento-Inteligente, Python + Jinja2, HTML em /docs na main | decisão | D30, P51 |
| 5 | ~2026-09-15 23:21 | Piloto v2 (Sacada) com toggle de marca e diagrama de cota publicado | marco | P52, A24 |
| 6 | ~2026-09-15 23:40 | Ficha SS-001 (0,683 kg/m) e descrições código↔peça enviadas ao Code; ficha vale mais que a tabela-resumo | marco | P53, A25 |
| 7 | ~2026-09-16 01:04 | Pages bloqueado em repo privado (plano Free da org); repo tornado público; site no ar | erro relevante | P54, P55 |
| 8 | ~2026-09-16 01:10 | Pessoa avisa que as imagens publicadas estão erradas; Code instruído a não mexer até a revisão | erro relevante | P56 |
| 9 | ~2026-09-17 11:30 | Causa: src/assets/img/perfis (fonte, certa) × docs/assets/img/perfis (gerada e limpa a cada build) | marco | P56, A26 |
| 10 | 2026-09-17 12:45 | MUDOU ROTA: nome de imagem {CODIGO}-{nome-kebab}.png → {CODIGO}-{nome_snake}.jpg (hífen só após o código e antes de "isometrico", minúsculo) | MUDOU ROTA | D31, P57, A27 |
| 11 | ~2026-09-17 12:55 | Seção 17 (destino da instrução) para o skill conduta-geral-big; protocolo completo também no chat | decisão | D32, D33, P58, A28 |
| 12 | 2026-09-17 13:30 | Commit c8dc33f (SS-002 completo, nomes, PNG→JPEG real), sem push; depois F1/F2 da limpeza de docs/ e CAD aprovados, F3 não executado | marco | P59–P63, A30, A31 |
| 13 | ~2026-09-17 14:20 | Padronização de tamanho e recorte no build; teste de peso 800/1000/1200; 1000×1000 proposto | decisão | D34, P64 |
| 14 | ~2026-09-17 14:43 | Code acha 6 arquivos novos em src/assets/img/perfis, colocados pela pessoa | achado | D35, P65 |
| 15 | 2026-09-23 10:24 | Pedido de usar a linguagem visual de solucao-sacadas-demo.netlify.app; o fetch trouxe o painel GOV_IA_CORE; pessoa cancelou o assunto | decisão | D36, P66 |
| 16 | 2026-09-23 10:30 a 12:10 | Decisão de apagar docs/assets/img/perfis e usar só src; build do Code parou por 13 imagens sem nome descritivo; SS-002.jpg novo é a versão atual; sessão não aberta | erro relevante | D37, D38, P67, P68, P69 |
| 17 | 2026-09-27 18:38 | DSL = perfis deslizantes, não-alumínio, compartilhados entre BigSpace/Vista e MWO/Unique | decisão | D39, P70 |
| 18 | 2026-09-29 12:28 | Fim: DXF do SS-0108 extraído (214 vértices); script de cálculo aguardando aprovação | fim | D40, P71, P72 |

## 3. Objetivo e escopo → PLANO
| data/hora | item | conteúdo |
|---|---|---|
| ~2026-09-15 21:50 | objetivo [AFIRMADO] | Catálogo técnico em HTML, um por produto (Solução, Blindex Sacadas, MWO/Unique, SkinGlass/Skin Vista, BigSpace/Vista, depois Ripado e Persianas), na tipologia do PDF "todos os produtos"; depois catálogo físico e PDF; material chega aos poucos da equipe |
| ~2026-09-15 22:35 | escopo [AFIRMADO] | Menu por produto: Nome, Tipologia, Limites e dados técnicos, Perfis, Detalhe de montagem, Detalhe de usinagem (varia conforme o conteúdo); ficha de perfil com vista isométrica; perfil compartilhado listado em cada produto e ficha única |
| ~2026-09-17 14:20 | critério [AFIRMADO] | Desenho técnico e isométrica com o mesmo tamanho e proporção; reprocessar as 8 imagens já commitadas; redimensionar no build.py; dimensão-alvo em aberto (1000×1000 [PROPOSTO]) |
| 2026-09-29 12:22 | escopo [AFIRMADO] | Calcular área, perímetro, centroide e Jx/Jy de perfil a partir de DXF (SS-0108); peso fica pendente. HISTÓRICO · superado por A5 e P19 do HIST 10-26_a_10-29 (script validado) |

## 4. Decisões → PLANO
| id | data/hora | de → para | motivo | impacto |
|---|---|---|---|---|
| D29 | ~2026-09-15 23:05 | [AFIRMADO] nomes Unique, Vista e Skin Vista como nomes finais únicos → 4 categorias com dois nomes e a mesma base técnica; Solução (azul) completa primeiro, Blindex (vermelho) depois | mesmo produto sob duas marcas | dupla marca: JÁ REGISTRADO (seção 0). "Solução primeiro": HISTÓRICO · superado por D25 (HIST 10-26_a_10-29) |
| D30 | ~2026-09-15 23:19 | [AFIRMADO] sem repo → GitHub Pages desde já como ambiente de trabalho (servidor próprio = destino final); repo privado catalogo-tecnico na org Solucao-Fechamento-Inteligente; Python + Jinja2 + PyYAML, HTML em /docs na main, sem CI | equipe entrega material aos poucos; link vivo e rastro no Git; sem Node | stack vigente. Org e URL: HISTÓRICO · superado por D16 (conexaoiatech) |
| D31 | 2026-09-17 12:45 | [AFIRMADO] {CODIGO}-{nome-kebab}.png → {CODIGO}-{nome_snake}.jpg e {CODIGO}-{nome_snake}-isometrico.jpg; hífen só após o código e antes de "isometrico"; sempre minúsculo; build corrige nome fora do padrão | nomes mistos (maiúscula, hífen e underscore no mesmo par) | HISTÓRICO · superado por D6 e P22 do HIST 10-26_a_10-29 (nome da ficha, código em minúsculo) |
| D32 | ~2026-09-17 12:50 | [AFIRMADO] toda instrução para outra tela (Code, terminal, banco, PowerShell) em bloco copiável com a linha "> RODAR EM: <ambiente>"; entra como seção 17 no skill conduta-geral-big via skill-creator | evitar rodar no lugar errado | formato HISTÓRICO · superado pela preferência de 2026-10-29: destino fora do bloco de cópia |
| D33 | ~2026-09-17 12:58 | [AFIRMADO] protocolo conduta-geral-big só no Code → também no chat (modos DIRETO, ANÁLISE, EXECUÇÃO; F1 a F4; [NÃO SEI]) | mesma conduta nas duas telas | respostas do chat passaram a vir em modos |
| D34 | ~2026-09-17 14:20 | [AFIRMADO] só nome → também tamanho e recorte: desenho e isométrica no mesmo padrão, reprocessar as 8 já commitadas, automático no build.py | uniformidade na ficha | dimensão nunca confirmada; Referência tem pendência equivalente (cópias otimizadas no build) |
| D35 | ~2026-09-17 14:55 | [AFIRMADO] SS-002-trilho_superior-isometrico.jpg é do SS-002 (nome do detalhe errado) | esclarecer antes de renomear | em 2026-09-23 o Code informou que esse arquivo não existe mais: sem efeito |
| D36 | 2026-09-23 10:24 | [AFIRMADO] adotar a linguagem visual de solucao-sacadas-demo.netlify.app → assunto cancelado ("CANCELE ESTE ASSUNTO") | a URL entregava o painel GOV_IA_CORE, não um site de sacadas | HISTÓRICO · superado por D24 (tema escuro padrão SITESOLU); se SITESOLU é a mesma referência: a confirmar |
| D37 | 2026-09-23 10:30 | [AFIRMADO] imagens em docs e src sem regra → apagar docs/assets/img/perfis (gerada) e usar só src/assets/img/perfis | docs/ é limpo a cada build | regra vigente; coberta pela lista PRESERVAR de P22 |
| D38 | ~2026-09-23 12:10 | [AFIRMADO] SS-002.jpg novo → versão mais atual, substitui SS-002-montante_do_vidro_8.jpg | resposta da pessoa | renomear e rodar build ficou pendente (P68) |
| D39 | 2026-09-27 18:38 | [AFIRMADO] DSL sem definição → perfis deslizantes, não-alumínio, DSL-001, 002 e 003 compartilhados entre BigSpace/Vista e MWO/Unique | resposta da pessoa | material depois definido: UHMW-PE (D15 do HIST 10-26_a_10-29); vínculo com os sistemas: a confirmar contra relatorios/matriz_sistemas.md |
| D40 | 2026-09-29 12:22 | [AFIRMADO] SS-0108 com seção maciça; categoria a definir; descricao "[a confirmar]"; peso pendente; DXF em cad-fonte\ARQUIVOS\SACADA_BLINDEX\SS-0108.dxf; cálculo por ezdxf com validação cruzada | sem espessura de parede informada | HISTÓRICO · superado por D2, D10, D11 e P19 do HIST 10-26_a_10-29 (SS-108 = Montante do Vidro 12 mm; script validado) |

## 5. Passos → ROTEIRO
| id | data/hora | nº roteiro | ação | alvo | evidência curta (com hash, se houver) | status |
|---|---|---|---|---|---|---|
| P48 | ~2026-09-15 21:55 | "levantamento" | Ler o site de produtos e o PDF "todos os produtos"; quadro de produtos | solucaosacadas.com.br/produtos, PDF no Projeto | quadro no chat; PDF no Projeto (2026-09-16 00:52 UTC) | FEITO |
| P49 | ~2026-09-15 22:44 | "protótipo v1" | HTML monolítico de 461 KB, 3 imagens em base64 | artifact do Claude.ai | artifact publicado | FEITO |
| P50 | ~2026-09-15 23:08 | "prompt Code" | prompt-claude-code.md em 2 versões; a 2ª com dupla marca | Claude Code | arquivo entregue | FEITO |
| P51 | ~2026-09-15 23:19 | "plano Code" | Plano de 11 passos do Code aprovado; modo "manually approve edits" na 1ª execução | Claude Code | plano exibido ("Ready to code?") | FEITO |
| P52 | ~2026-09-15 23:21 | "protótipo v2" | Piloto Sacada: toggle de marca, diagrama de cota SVG, callouts; corrigidos 2 bugs de cor | artifact do Claude.ai | capturas Playwright; artifact publicado | FEITO |
| P53 | ~2026-09-15 23:40 | "SS-001" | Ficha SS-001 (0,683 kg/m; 252,03; 307,44; 23.607,63; 62.744,70; 41,95 × 29,6); descrições SS-002 a SS-010; LT-077 | Code | resumo do Code: SS-001 corrigido, descrições aplicadas, LT-077 criado | FEITO |
| P54 | ~2026-09-16 00:30 | "estrutura" | Code gerou src/data (34 perfis, 6 categorias, marcas.yaml), build.py e templates; /docs da Solução; CAD de 41 MB movido para /cad-fonte | repo local | resumo do Code: build sem erro | FEITO |
| P55 | ~2026-09-16 01:04 | "Pages" | Repo público (plano Free não permite Pages em privado); Pages main /docs; [PROPOSTO] pelo Claude, aplicado pelo Code | GitHub | resumo do Code: site no ar | FEITO |
| P56 | ~2026-09-17 11:30 | "diagnóstico imagens" | Diagnóstico das duas pastas; imagem nova só em src; instruções ao Code | instrucoes-claude-code-correcao-imagens.md | pastas mostradas em print | FEITO |
| P57 | 2026-09-17 12:45 | "nomenclatura" | Convenção final de nome gravada no Projeto e na memória | instrucoes-claude-code-nomenclatura-final.md | arquivo no Projeto (12:45) | FEITO |
| P58 | ~2026-09-17 12:55 | "skill conduta" | Seção 17 para conduta-geral-big | atualizacao-skill-conduta-geral-big.md | arquivo entregue | PENDENTE · falta prova: skill-creator aplicou a seção |
| P59 | ~2026-09-17 13:00 | "checagem de nome" | Renomear 2 arquivos do SS-002; checagem automática no build (regex ^[A-Z]{2,3}-\d{3,4}-[a-z0-9_]+(-isometrico)?\.jpg$) | src/build.py | log: "todos os arquivos já seguem o padrão" | FEITO |
| P60 | ~2026-09-17 13:03 | "SS-002.yaml" | Ficha: 0.471; 173.90; 207.40; 11830.90; 8203.01; 24.3 × 31.23; status completo | src/data/perfis/SS-002.yaml | parse YAML OK; 34 YAML sem chave duplicada | FEITO |
| P61 | ~2026-09-17 13:23 | "PNG falso" | SS-014-capa_uniao, SS-016-montante_de_giro_esquerdo e o isométrico: .jpg com conteúdo PNG → JPEG real (alfa sobre branco, qualidade 95) | src/assets/img/perfis | magic bytes 8 de 8 OK; build sem erro | FEITO |
| P62 | 2026-09-17 13:30 | "commit" | Commit sem push, 22 arquivos | repo local | c8dc33f | FEITO |
| P63 | ~2026-09-17 13:40 | "limpeza docs e CAD" | F1 e F2 (11 etapas) aprovados: limpar docs/ órfão, varrer .dwg/.sldprt no repo e mover para cad-fonte\ARQUIVOS; etapa 1 enviada, pausada para terminar imagens | repo | checklist no chat | PENDENTE · falta prova: execução (id 295) |
| P64 | ~2026-09-17 14:20 | "teste de resize" | Desenho 850×940 (99,7 KB) e isométrica 1018×740 (126,6 KB): 800² = 67,7 e 66,0 KB; 1000² = 89,9 e 94,5 KB; 1200² = 118,3 e 124,5 KB | scratchpad do Code, fora do repo | tabela do Code | FEITO |
| P65 | ~2026-09-17 14:43 | "arquivos novos" | 6 arquivos não rastreados (SS-002-trilho_superior-isometrico, SS-003-trilho_superior, SS-004, SS-004_ISO, SS-005, plot.log); pessoa confirmou que colocou; nomes propostos pela tabela de descrições | src/assets/img/perfis | relato do Code | FEITO |
| P66 | 2026-09-23 10:17 | "Netlify" | WebFetch de solucao-sacadas-demo.netlify.app, 2 vezes: voltou o painel GOV_IA_CORE | web | 2 retornos iguais | CORTADO |
| P67 | 2026-09-23 10:30 | "A e B" | Instrução ao Code: renomear 4, apagar plot.log, limpar docs/assets/img/perfis, build, magic bytes | Claude Code | bloco enviado | FEITO |
| P68 | ~2026-09-23 10:35 | "limpeza Code" | 3 de 4 renomeações; plot.log apagado; docs limpa; build parou (código 1) por 13 imagens fora do padrão (DSL-001, DSL-001-ISO, DSL-002-ISO, DSL-003, DSL-003-ISO.JPG, SS-002, SS-005-ISO.JPG, SS-006 a SS-010, SS-017); 25 arquivos são JPEG real | repo local | relato do Code | PENDENTE · falta prova: nomes decididos e build verde |
| P69 | 2026-09-23 12:03 | "estou entrando" | Linha do projeto fornecida (catalogo_tecnico, repo, pasta, implementacao_gradual); Code não abriu sessão por falta de CLAUDE.md com canário e project_id | Code | relato do Code | PENDENTE · falta prova: sessão aberta |
| P70 | 2026-09-27 18:38 | "nomes de detalhe" | Pedidos os nomes de detalhe de DSL-001, 002, 003, SS-009 e SS-017 | pessoa | sem resposta neste chat | PENDENTE · falta prova: nomes recebidos |
| P71 | 2026-09-29 12:26 | "SS-0108 etapa 1" | DXF AC1015: 1 LWPOLYLINE, 214 vértices, 40 com bulge, fechada, sentido horário, 24,07 × 39,30 mm; $INSUNITS=1 (polegadas) com desenho em mm; U com abas de ~1,5 mm e 25 dentes por aba, simétrico | cad-fonte\ARQUIVOS\SACADA_BLINDEX\SS-0108.dxf | relato do Code (ezdxf 1.4.4) | FEITO |
| P72 | 2026-09-29 12:28 | "SS-0108 etapa 2" | Cálculo de área, perímetro, centroide e Jx/Jy com validação cruzada | props_ss0108.py no scratchpad | aguardando aprovação do comando | PENDENTE · falta prova: resultado |

## 6. Artefatos
Commits: c8dc33f fix: corrige dados técnicos do SS-002 e integridade de imagens (SS-002/SS-014/SS-016). O primeiro commit e push do repo (P54, P55): hash não aparece no chat [SEM EVIDÊNCIA].
| id | data/hora | tipo | nome ou caminho | estado atual |
|---|---|---|---|---|
| A22 | ~2026-09-15 22:44 | artifact | catálogo v1 monolítico (claude.ai/artifact/A5nvW75QJ2F9gSwyfJyeEE) | só referência; superado pelo repo |
| A23 | ~2026-09-15 23:08 | arquivo | prompt-claude-code.md (v1 e v2 com dupla marca) | usado; histórico |
| A24 | ~2026-09-15 23:21 | artifact | piloto v2 Sacada (claude.ai/artifact/DCdT9HxYTotCZFQMoXFx7W) | referência visual; layout superado por D24 |
| A25 | ~2026-09-15 23:40 | arquivo | instrucoes-claude-code-perfis-sacada.md | aplicado nos YAML; a cópia em docs/ foi apagada pelo build, conteúdo nos YAML (relato do Code) |
| A26 | ~2026-09-17 11:30 | arquivo | instrucoes-claude-code-correcao-imagens.md | aplicado |
| A27 | 2026-09-17 12:45 | documento | instrucoes-claude-code-nomenclatura-final.md (raiz do Projeto) | HISTÓRICO · convenção superada (D31) |
| A28 | ~2026-09-17 12:55 | arquivo | atualizacao-skill-conduta-geral-big.md | entregue; aplicação não provada (id 21) |
| A29 | 2026-09-17 12:35 | memória | areas/catalogo-tecnico.md do Projeto (convenção de nome) | atualizada; depois alterada por outros chats |
| A30 | 2026-09-17 13:30 | código | src/build.py com verifica_imagens_perfis | no repo (c8dc33f); build depois reconstruído (P22 do HIST 10-26_a_10-29) |
| A31 | 2026-09-17 13:30 | dados | src/data/perfis/SS-002.yaml | no repo (c8dc33f) |
| A32 | 2026-09-29 12:26 | script | extract_ss0108.py e props_ss0108.py (scratchpad do Code) | fora do repo; resultado do cálculo não visto |
| A33 | 2026-10-29 21:22 | documento | este HIST | gerado; falta registrar no repo (seção 15) |

## 7. Estado final → ESTADO
Estado vigente: ESTADO_CATALOGO_TECNICO.md (2026-10-29 11:40) e seção 7 do HIST 2026-10-29 catalogo-pdf. O estado abaixo é HISTÓRICO e não vale.
Última ação do chat: P72 (cálculo do SS-0108 aguardando aprovação, 2026-09-29 12:28). Último passo provado: P71 (extração do DXF). Próximo passo exato na época: aprovar o comando e conferir a unidade (polegadas × mm) contra DXF de perfis já catalogados. Aberto na época: build parado por 13 imagens sem nome (P68), sessão não aberta (P69), F3 da limpeza (P63), dimensão das imagens (D34).

## 8. Procedimentos → MANUAL
1. Conferir extensão × conteúdo das imagens e corrigir PNG disfarçado de JPG (validado 2026-09-17 13:23):
   ```
   for f in src/assets/img/perfis/*; do printf "%s: " "$f"; head -c 8 "$f" | xxd -p; done
   ```
   ffd8ff = JPEG real; 89504e47 = PNG. Para recodificar um arquivo PNG com alfa mantendo o nome (exige modo com canal alfa; sem alfa dá IndexError, e então salvar direto em RGB):
   ```
   python -c "
   from PIL import Image
   import os
   path = 'src/assets/img/perfis/<ARQUIVO>.jpg'
   im = Image.open(path)
   im.load()
   bg = Image.new('RGB', im.size, (255, 255, 255))
   bg.paste(im, mask=im.split()[3])
   tmp = path + '.tmp'
   bg.save(tmp, 'JPEG', quality=95)
   assert open(tmp, 'rb').read(3) == b'\xff\xd8\xff'
   os.replace(tmp, path)
   "
   ```
2. Validar o YAML de um perfil (validado 2026-09-17 13:03): `python -c "import yaml; yaml.safe_load(open('src/data/perfis/SS-002.yaml', encoding='utf-8'))"`. O safe_load não acusa chave duplicada; a varredura de duplicata nos 34 YAML foi um script do Code, não mostrado [SEM EVIDÊNCIA do código].
3. Cálculo de propriedades por DXF: já está no MANUAL da Referência (HIST 10-26_a_10-29, seção 8, item 2). Nada novo aqui.

## 9. Lições
| data/hora | problema | causa | solução | evidência |
|---|---|---|---|---|
| ~2026-09-15 23:25 | badges e numeração em cinza ao trocar de marca no piloto v2 | troca global de var(--sol) por var(--dc) criou --dc:var(--dc) circular | iniciar --dc na raiz com valor real e não redeclarar nos filhos | P52 |
| ~2026-09-15 23:30 | tabela "peso/br" divergia da ficha (SS-001: 3,833 × 0,683) | duas fontes e unidades diferentes | ficha individual vale; a tabela só serve para descrição | P53 |
| 2026-09-17 12:45 | nomes de imagem com padrões misturados (maiúscula em "Montante", "vidro-8" × "vidro_8") | convenção sem regra escrita | 3 perguntas fecharam a regra; build corrige | D31, P57 |
| ~2026-09-17 13:05 | Claude.ai tomou por chave duplicada um diff que mostrava antes e depois | leitura do diff do terminal sem marcação +/- | pedir o conteúdo atual do arquivo em disco antes de recusar a edição | P60 |
| ~2026-09-17 13:20 | 3 arquivos .jpg com conteúdo PNG | exportação com a extensão trocada | varredura de magic bytes e recodificação | P61 |
| ~2026-09-17 14:20 | 1200×1200 quase não reduz o peso | imagens originais já têm 850 a 1018 px | testar peso real antes de fixar a dimensão | P64 |
| 2026-09-23 10:20 | WebFetch do Netlify trouxe o painel GOV_IA_CORE, não um site de sacadas | causa não provada (domínio reaproveitado por outro deploy [AFIRMADO]) | a pessoa cancelou o assunto | P66 |
| ~2026-09-23 10:35 | build parou com 13 imagens fora do padrão | a checagem só corrige o que infere com segurança; nome sem detalhe pede decisão humana | pessoa informa o nome de cada detalhe | P68 |

## 10. Pendências → FILA
| data/hora aberta | item | origem | depende de | urgência |
|---|---|---|---|---|
| ~2026-09-17 12:55 | Ajustar a seção 17 do conduta-geral-big (destino fora do bloco de cópia) e confirmar que o skill-creator a aplicou | D32, A28 | id 21 e pessoa | baixa |
| ~2026-09-17 14:20 | Dimensão-alvo das imagens (1000×1000 [PROPOSTO]) nunca confirmada; Referência gera cópias otimizadas no build: confirmar se encerra | D34, P64 | pessoa | baixa |
| 2026-09-18 20:41 | Id 21: decidir (proposta INCONSISTENTE) | Referência | pessoa | baixa |
| 2026-09-27 18:38 | Confirmar o vínculo dos DSL-001, 002 e 003 com BigSpace/Vista e MWO/Unique em relatorios/matriz_sistemas.md | D39 | pessoa | baixa |
| ~2026-09-29 | Id 295: varredura .dwg/.sldprt (checklist F2 de 11 etapas deste chat, P63) | Referência | bloco no Code | baixa |
| 2026-10-26 | Id 296: PLANO.md, ROTEIRO.md, CLAUDE.md | Referência | bloco no Code | média |
| 2026-10-28 20:24 | Linha Repo na instrução do projeto; git remote; avisar quem tem o link antigo | Referência | pessoa | média |
| 2026-10-28 22:29 | Gráficos: modelo por sistema com o Coordenador de Produção; 16 DXF; 3D por extrusão [PROPOSTO] | Referência | informação técnica | média |
| 2026-10-28 23:54 | log_solu_fd_pt.png e referencia/ESTADO_CATALOGO_TECNICO.md no repo | Referência | pessoa | baixa |
| 2026-10-28 23:54 | Ficha repete tabela; pinch-zoom no aparelho; logo com fundo convertido | Referência | teste em aparelho | baixa |
| 2026-10-29 00:00 | selantes.html fora de escopo: decidir | Referência | pessoa | baixa |
| 2026-10-29 ~11:30 | Conferir os 2 registros de demanda criados à mão no Adminer | ESTADO | Code, só leitura | baixa |
| 2026-10-29 12:41 | Sessões 97/98 abertas segundo o espelho: fechar | ESTADO | "estou saindo" | média |
| 2026-10-29 20:12 | Logos dos 10 produtos em src/assets/img/produtos/ | Referência | pessoa enviar | média |
| ~2026-10-29 20:45 | Conferir a cota de cima no recorte de SS-003, SS-019 e SS-027 | Referência | pessoa | baixa |
| 2026-10-29 21:08 | Registrar o passo do PDF em gov_passos e no ROTEIRO/PLANO | Referência | "estou saindo" | média |
| 2026-10-29 21:10 | PDF determinístico: hash das entradas, preservar docs/pdf, data de revisão = última mudança | Referência | resposta da pessoa | alta |
| 2026-10-29 21:10 | Conferir o site: solucao/sacada.html (botão) e pdf/solucao/sacada.pdf | Referência | pessoa | média |
| 2026-10-29 21:22 | Registrar este HIST no repo (seção 15) | A33 | bloco no Code | média |

## 11. Precedência e contradições
| data/hora antiga | data/hora vigente | assunto | antiga → vigente (ponteiros) | sentido |
|---|---|---|---|---|
| ~2026-09-15 22:44 | ~2026-09-15 23:05 | nomes dos produtos | Unique, Vista e Skin Vista como únicos (A22) → dupla marca (D29) | interna |
| ~2026-09-15 23:05 | 2026-10-29 00:00 | ordem Solução e Blindex | Solução primeiro (D29) → Blindex antecipada (D25 do HIST 10-26_a_10-29) | Referência supera |
| ~2026-09-15 23:19 | 2026-10-28 20:23 | repo e site | org Solucao-Fechamento-Inteligente e solucao-fechamento-inteligente.github.io (D30) → conexaoiatech/catalogo-tecnico e conexaoiatech.github.io (D16) | Referência supera |
| ~2026-09-15 23:19 | ~2026-09-16 01:04 | visibilidade do repo | privado (D30) → público (P55) | interna |
| 2026-09-17 12:45 | 2026-10-28 19:50 | nome de imagem | {CODIGO}-{nome_snake}.jpg (D31) → nome da ficha, código em minúsculo, regra em scripts/padroes.py (D6, P22) | Referência supera |
| ~2026-09-17 12:50 | 2026-10-29 | formato da instrução para outra tela | "> RODAR EM" dentro do bloco (D32) → destino fora do bloco de cópia (preferência salva) | Referência supera |
| 2026-09-17 13:30 | 2026-10-28 00:11 | push do c8dc33f | sem push (P62) → pushado (bee21e6..0894d5b, P13 do HIST 10-26_a_10-29) | pendência resolvida, Referência supera |
| ~2026-09-17 14:20 | 2026-10-26 18:0x | resize das imagens | 1000×1000 [PROPOSTO] (D34) → originais mantidos e cópias otimizadas no build | a confirmar |
| 2026-09-23 10:24 | 2026-10-28 23:32 | linguagem visual | Netlify cancelado (D36) → tema escuro padrão SITESOLU (D24) | Referência supera; se SITESOLU é a referência pedida: a confirmar |
| ~2026-09-23 10:35 | 2026-10-28 14:55 | 13 imagens sem nome | build parado (P68) → 72 imagens renomeadas e build com validador (P15, P16, P22) | Referência supera |
| 2026-09-23 12:03 | 2026-10-26 a 2026-10-28 | sessão | não aberta (P69) → sessões 93/94 e 95/96 abertas e fechadas | Referência supera |
| 2026-09-27 18:38 | 2026-10-28 20:11 | DSL | não-alumínio (D39) → UHMW-PE (D15) | Referência complementa |
| 2026-09-29 12:22 | 2026-10-28 18:28 | SS-0108 | "[a confirmar]" e cálculo pendente (D40, P72) → SS-108 = Montante do Vidro 12 mm, script validado (D2, P19) | Referência supera |
| 2026-09-18 20:41 | 2026-10-29 11:40 | id 21 (conduta-geral-big) | seção 17 entregue (A28) → proposta INCONSISTENTE no ESTADO | a confirmar |

## 12. Outros
Pessoas e papéis novos: nenhum. Preferências do usuário: resposta clara e direta, sem comentário antes ou depois; uma pergunta por vez; instrução para outra tela em bloco copiável com o destino indicado; mesmo protocolo de conduta no chat e no Code; conferir antes de substituir imagens (a pessoa quis apagar arquivos que ia gerar de novo; o Claude recomendou esperar o resultado da conversão). Omitido por sigilo: nenhum.

## 13. Checagem
Commits no chat 1 = seção 6 1 · Decisões do usuário 12 = seção 4 12 · MUDOU ROTA 2 = seção 2 2 · Sessões do chat 0 = cabeçalho 0 · Nenhum HISTÓRICO como vigente nas seções 3, 4 e 7: sim.

## 14. Pode apagar?
SIM, apague depois que o HIST estiver nos documentos do Projeto e o bloco da seção 15 tiver feito o push. Os artifacts v1 e v2 são só referência e não precisam ser baixados.

## 15. Bloco para o Claude Code (registrar o HIST no repo)
Salve o HIST em C:\GITHUB\CATALOGO_TECNICO\docs\hist\ e cole o bloco no Claude Code: C:\GITHUB\CATALOGO_TECNICO
```
[TL-catalogo_tecnico-CODE] EXECUTAR:
Registrar no repo o HIST HIST_2026-09-15_a_2026-09-29_catalogo_tecnico_estrutura-dupla-marca-imagens.md, salvo pela pessoa em docs\hist\.
ZONAS: leitura | repo-escrita
SENSÍVEIS: !git push origin main
TOLERADO: nenhum. NÃO DECLARADO: anotar e seguir.
ESCOPO DECLARADO:
1. Conferir que docs\hist\HIST_2026-09-15_a_2026-09-29_catalogo_tecnico_estrutura-dupla-marca-imagens.md existe. Se não existir: PARADA.
2. git add docs/hist/HIST_2026-09-15_a_2026-09-29_catalogo_tecnico_estrutura-dupla-marca-imagens.md
3. git commit -m "docs(hist): estrutura-dupla-marca-imagens (2026-09-15 a 2026-09-29)"
4. SENSÍVEL git push origin main
Proibido: abrir ou fechar sessão, alterar passos, demandas ou ESTADO_SESSAO.
PARADA FINAL: hash e push.
```
