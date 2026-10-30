Canônico em docs/ (build preserva). Atualizado 2026-10-30.

# ESTADO_SESSAO — catalogo_tecnico

## Sessão
- A 99 (claude_ia) e B 100 (claude_code), vinculadas, fechadas em 2026-10-30 (99 às 20:33, 100 às 20:34).
- Passo 109 (id 110 em gov_passos) e demanda 302, ambos concluídos.
- Último commit: 7815278 (em origin/main).
- Repositório conexaoiatech/catalogo-tecnico. Site no ar em catalogo.solucaointeligentes.com (VPS srv1849835), com deploy automático por GitHub Actions e rsync restrito por rrsync. A raiz é a escolha de marca; solucao/ e blindex/ publicadas.

## Feito
- Relação de peças gerada dos YAML, em linha por perfil (isométrica, desenho técnico e dados técnicos), A4 retrato com 3 por página: Solução com 40 perfis e Blindex com 39 (docs/{marca}/relacao-pecas.html e docs/pdf/{marca}/relacao-pecas.pdf).
- Campo codigo_extrusora (PPF) em 7 perfis: SS-001, SS-002, SS-003, SS-004, SS-005, SS-007 e SS-010.
- Recorte do desenho corrigido por regra geral em src/build_pdf.py (SS-003, SS-019 e SS-027 completos); os 10 PDFs por sistema foram regenerados.
- Versão folheável da relação de peças na seção 1 da biblioteca de perfis de cada marca (pypdfium2 5.14.0 e page-flip 2.0.7, sem CDN).
- GUIA_EDICAO atualizado com a relação de peças, o visualizador, a pasta folhear e o recorte.
- Demanda 302 e passo 109 fechados; sessões 99 e 100 fechadas.

## Decisões
- Regras únicas em scripts/padroes.py: nome de imagem (minúsculo, {codigo}-{detalhe}.jpg e -isometrico.jpg), status calculado de perfil completo e ordem por código (SS, LT, F, FE, DSL).
- src/data/marcas.yaml guarda nomes dos sistemas, cores e logos por marca (Solução e Blindex publicadas).
- Relação de peças: A4 retrato, 3 perfis por página (aprovado pela pessoa); RELACAO_MARCAS em src/build.py = solucao e blindex; cada marca só lista os perfis dos próprios sistemas, com o rodapé do fabricante Solução.
- Recorte do desenho: a ficha CAD tem 3 linhas de tabela no topo e o desenho começa depois delas (sem RECORTE_EXCECOES).
- Ficha individual prevalece sobre o YAML, com exceções: SS-002 (vale o YAML) e FE-0207 (área 274.43, ficha corrigida).
- Gráficos de pressão adiados: src/data/estrutural.yaml está PRELIMINAR e publicar_graficos é false.
- O build corrige nome de imagem, valida o catálogo e regenera docs/ preservando hist/, ESTADO_SESSAO.md, PLANO.md e ROTEIRO.md.

## Pendente
- 3w: 404.html no repo conexaoiatech.github.io (redirecionamento do link antigo), repo catalogo-tecnico privado, testar o link antigo
- 3x: GUIA_EDICAO passo 4 ainda cita GitHub Pages; requirements sem Playwright e pypdf; campos sem uso em biblioteca.yaml (imagem e fonte_desenho_mestre); fechar a demanda da hospedagem; trocar 3 linhas da instrução do projeto
- Demanda 300 (PDF determinístico, logos dos 10 produtos)
- Demanda 298 (gráficos de pressão, adiada até o Coordenador de Produção validar)
- data_fim das sessões 97 e 98

## Próximo passo
3w.
