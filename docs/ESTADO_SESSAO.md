Canônico em docs/ (build preserva). Atualizado 2026-10-29.

# ESTADO_SESSAO — catalogo_tecnico

## Sessão
- A 97 (claude_ia) e B 98 (claude_code), vinculadas, de 2026-10-29 11:20 a 22:32.
- Passos 102 a 107 e 3x. Demanda 296.
- Repositório conexaoiatech/catalogo-tecnico. Site: https://conexaoiatech.github.io/catalogo-tecnico/ (a raiz é a escolha de marca; solucao/ e blindex/ publicadas).

## Feito
- Demandas 20, 22, 295 e 296 fechadas; 21 como INCONSISTENTE; 2 demandas novas criadas à mão (navegação, layout escuro e Blindex; dados estruturais e gráfico de pressão).
- SS-016 como card no BigSpace (sem ficha em destaque); edição manual de marcas.yaml publicada.
- .gitignore bloqueia extensões de CAD e referencia/.
- PLANO, ROTEIRO, CLAUDE.md, INSTRUÇÃO consolidada, GUIA_EDICAO e README atualizados.
- Conduta v2026-10-29a (a preferência "uma pergunta por vez" saiu da instrução e foi para a conduta).
- Catálogo em PDF publicado no commit 6c11ba0, com 10 PDFs em docs/pdf; HIST registrados em docs/hist.

## Decisões
- Regras únicas em scripts/padroes.py: nome de imagem (minúsculo, {codigo}-{detalhe}.jpg e -isometrico.jpg), status calculado de perfil completo e ordem por código (SS, LT, F, FE, DSL).
- src/data/marcas.yaml guarda nomes dos sistemas, cores e logos por marca (Solução e Blindex publicadas).
- Layout escuro no padrão do SITESOLU, com cabeçalho único, menu em gaveta no celular e impressão em fundo branco.
- Navegação por trilha e ?de= (origem do perfil), com vizinhos por sistema dentro de cada marca.
- Ficha individual prevalece sobre o YAML, com exceções: SS-002 (vale o YAML) e FE-0207 (área 274.43, ficha corrigida).
- Gráficos de pressão adiados: src/data/estrutural.yaml está PRELIMINAR e publicar_graficos é false.
- O build corrige nome de imagem, valida o catálogo e regenera docs/ preservando hist/, ESTADO_SESSAO.md, PLANO.md e ROTEIRO.md.

## Pendente
- PDF determinístico (alta), demanda 300
- Logos dos 10 produtos em src/assets/img/produtos, demanda 300
- Gráficos de pressão, demanda 298 (EM_ANALISE, adiada até o Coordenador de Produção validar), 16 DXF e 3D por extrusão
- Conferir o site publicado: solucao/sacada.html (botão) e pdf/solucao/sacada.pdf
- Conferir a cota de cima no recorte de SS-003, SS-019 e SS-027
- Conferir data_fim das sessões 97 e 98
- Verificar o git remote local
- Decidir entre apagar e ignorar: sacada.pdf e skin-vista.pdf na raiz, relatorios/referencia_layout_sitesolu.md e relatorios/teste_visual/
- Ficha repete tabela, pinch-zoom no aparelho, conferir logo com fundo convertido
- Confirmar selantes.html só na Solução

## Próximo passo
Estou entrando; depois escolher entre E5 (gráficos de pressão) e o 3D por extrusão.
