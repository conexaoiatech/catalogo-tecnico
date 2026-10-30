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
- E5: gráficos de pressão (modelo por sistema e DXF dos 16 perfis estruturais, relatorios/dxf_pendentes.md).
- 3D por extrusão do DXF.
- Ids das 2 demandas novas criadas à mão (não constam no repo).
- Ficha do perfil ainda repete a tabela de dados.
- Pinch-zoom no celular não testado em aparelho.
- Conferir o logo solucao_pt com o fundo convertido em transparência.
- Destino de relatorios/ (referencia_layout_sitesolu.md e teste_visual/ seguem sem rastreio).
- PDF determinístico (hash das entradas, preservar docs/pdf), logos dos 10 produtos em src/assets/img/produtos e conferir o site publicado.

## Próximo passo
Estou entrando; depois escolher entre E5 (gráficos de pressão) e o 3D por extrusão.
