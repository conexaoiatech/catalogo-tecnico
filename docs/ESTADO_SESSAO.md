Canônico em docs/ (build preserva). Atualizado 2026-10-29.

# ESTADO_SESSAO — catalogo_tecnico

## Sessão
- A 97 (claude_ia) e B 98 (claude_code) fechadas em 2026-10-29.
- Repositório conexaoiatech/catalogo-tecnico. Site: https://conexaoiatech.github.io/catalogo-tecnico/ (a raiz é a escolha de marca; solucao/ e blindex/ publicadas).

## Feito
- Catálogo em PDF publicado no commit 6c11ba0, com 10 PDFs em docs/pdf.
- HIST registrados em docs/hist (último 62f3213).

## Decisões
- Regras únicas em scripts/padroes.py: nome de imagem (minúsculo, {codigo}-{detalhe}.jpg e -isometrico.jpg), status calculado de perfil completo e ordem por código (SS, LT, F, FE, DSL).
- src/data/marcas.yaml guarda nomes dos sistemas, cores e logos por marca (Solução e Blindex publicadas).
- Layout escuro no padrão do SITESOLU, com cabeçalho único, menu em gaveta no celular e impressão em fundo branco.
- Navegação por trilha e ?de= (origem do perfil), com vizinhos por sistema dentro de cada marca.
- Ficha individual prevalece sobre o YAML, com exceções: SS-002 (vale o YAML) e FE-0207 (área 274.43, ficha corrigida).
- Gráficos de pressão adiados: src/data/estrutural.yaml está PRELIMINAR e publicar_graficos é false.
- O build corrige nome de imagem, valida o catálogo e regenera docs/ preservando hist/, ESTADO_SESSAO.md, PLANO.md e ROTEIRO.md.

## Pendente
- PDF determinístico (hash das entradas, preservar docs/pdf, data de revisão igual à última mudança).
- Logos dos 10 produtos em src/assets/img/produtos.
- Conferir o site publicado.
- Conferir a cota de cima no recorte de SS-003, SS-019 e SS-027.
- Registrar passo e demanda do PDF pelos scripts.
- Id 21: decidir.
- Id 295: varredura de dwg e sldprt.
- Id 296: PLANO, ROTEIRO e CLAUDE.md.
- Conferir os 2 registros de demanda criados à mão.
- selantes.html fica fora do escopo (só Solução).

## Próximo passo
A pessoa escolhe entre PDF só quando os dados mudarem e logos dos produtos.
Arquivos sem rastreio na raiz (sacada.pdf, skin-vista.pdf, relatorios/referencia_layout_sitesolu.md, relatorios/teste_visual) ficam fora do commit.
