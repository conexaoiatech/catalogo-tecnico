# ESTADO_SESSAO — catalogo_tecnico

Gravado na raiz porque src/build.py apaga docs/ inteiro a cada build (shutil.rmtree(DOCS)), o que levaria o estado junto.

## Sessao
A 93 (claude_ia) e B 94 (claude_code), vinculadas, demanda 20. Passos 79 (inventario das imagens) e 80 (matriz perfil x categoria x imagens) FINALIZADO_SUCESSO. Sessoes 93 e 94 fechadas em 2026-10-28.

## Decisoes
- Pasta unica de imagens em src/assets/img/perfis (sem subpastas por sistema).
- Vinculo perfil x sistema pelo YAML de categoria.
- descricao do YAML de perfil como nome do detalhe da imagem.
- SS-0108 = ss-108.
- FE-0202, 0203, 0204, 0205, 0207 e 0208 com 4 digitos, calculados dos DXF de cad-fonte/ARQUIVOS/SKINGLASS.

## Pendente
- 2b: planilha de referencias (pronta, nao rodada).
- Conflito: build.py renomeia em maiusculo (IMG_PATTERN com codigo em maiusculas) x regra minuscula do inventario.
- scripts/ e relatorios/ criados e nao commitados.
- Demanda 19: push do commit c8dc33f.
- Branch de trabalho e main; o push do bloco pedia origin master.

## Proximo passo
2b, depois 2c aplicar, 3 renomear, 4 FE, 5 build e publicar.
