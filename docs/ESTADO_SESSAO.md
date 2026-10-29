Canônico em docs/ (build preserva). Atualizado 2026-10-29.

# ESTADO_SESSAO — catalogo_tecnico

## Sessão
- A 95 (claude_ia) e B 96 (claude_code), vinculadas, de 2026-10-28 14:14 a 2026-10-29.
- Passos 81 a 100 e 3p. Demanda 20.
- Repositório conexaoiatech/catalogo-tecnico. Site: https://conexaoiatech.github.io/catalogo-tecnico/ (a raiz é a escolha de marca; solucao/ e blindex/ publicadas).

## Decisões
- Regras únicas em scripts/padroes.py: nome de imagem (minúsculo, {codigo}-{detalhe}.jpg e -isometrico.jpg), status calculado de perfil completo e ordem por código (SS, LT, F, FE, DSL).
- src/data/marcas.yaml guarda nomes dos sistemas, cores e logos por marca (Solução e Blindex publicadas).
- Layout escuro no padrão do SITESOLU, com cabeçalho único, menu em gaveta no celular e impressão em fundo branco.
- Navegação por trilha e ?de= (origem do perfil), com vizinhos por sistema dentro de cada marca.
- Ficha individual prevalece sobre o YAML, com exceções: SS-002 (vale o YAML) e FE-0207 (área 274.43, ficha corrigida).
- Gráficos de pressão adiados: src/data/estrutural.yaml está PRELIMINAR e publicar_graficos é false.
- O build corrige nome de imagem, valida o catálogo e regenera docs/ preservando hist/, ESTADO_SESSAO.md, PLANO.md e ROTEIRO.md.

## Pendente
- Gráficos de pressão: modelo por sistema e DXF dos 16 perfis estruturais sem módulo W (relatorios/dxf_pendentes.md).
- 3D por extrusão do DXF.
- log_solu_fd_pt.png está solto na raiz do repositório, fora do git.
- selantes.html fica fora do escopo da Blindex (só Solução).
- UPDATEs de gov_demandas: 20, 22, 295, 296 e uma demanda nova para os gráficos.
- relatorios/referencia_layout_sitesolu.md e relatorios/teste_visual/ não foram versionados.

## Próximo passo
Estou entrando; depois fazer os UPDATEs de gov_demandas.
