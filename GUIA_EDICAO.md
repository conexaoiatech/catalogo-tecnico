# Guia rápido — editar textos do Catálogo Técnico

Para quem vai alterar um texto do catálogo sem mexer no código. Tudo o que aparece no site vem de arquivos de texto em `src/`; a pasta `docs/` é o site pronto, gerado a partir deles.

## 1. Preparar o VS Code (uma vez)
1. Abra a **pasta raiz** do projeto: `C:\GITHUB\CATALOGO_TECNICO` (Arquivo → Abrir Pasta). Não abra só `src/` nem `docs/`, senão a busca e o Live Server não enxergam tudo.
2. Quando o VS Code perguntar, clique em **Trust Folder** (confiar nos autores da pasta).
3. Instale duas extensões (painel de extensões, `Ctrl+Shift+X`):
   - **YAML** (Red Hat): avisa quando o recuo ou os dois-pontos estão errados.
   - **Live Server** (Ritwick Dey): abre o site no navegador e atualiza ao salvar.
4. Feche o painel de chat do **Copilot** (ou desligue-o para esta pasta), para não receber sugestões automáticas dentro dos textos.

## 2. Onde fica cada texto
| O que você quer mudar | Arquivo |
|---|---|
| Frase de apresentação (lede), selos (badges), tipologia, limites, textos de montagem e usinagem de um sistema | `src/data/categorias/{sistema}.yaml` — `sacada`, `portas-minimalistas` (MWO / Unique), `portas-robustas` (BigSpace / Vista), `pele-vidro` (SkinGlass / Skin Vista), `ripado`, `persianas` |
| Nome comercial e subtítulo de cada sistema, por marca | `src/data/marcas.yaml` → `produtos` → `nome` / `subtitulo` |
| Frase da página de escolha de marca e frase da capa de cada marca | `src/data/marcas.yaml` → `entrada_texto` e `capa_lede` |
| Nome da marca, legenda abaixo do logo, cores | `src/data/marcas.yaml` → `label`, `brand_sub`, `color`, `acao`, `destaque` |
| Descrição, nota e dados de um perfil (peso, área, inércia) | `src/data/perfis/{CODIGO}.yaml` (ex.: `SS-016.yaml`, `FE-0202.yaml`) |
| Código da extrusora de um perfil (ex.: `PPF 0968`) | `src/data/perfis/{CODIGO}.yaml`, campo opcional `codigo_extrusora` (aparece em "Dados técnicos" da página de perfil e na relação de peças; sem o campo, a linha não aparece) |
| Página e PDF da "Relação de peças" (uma linha por perfil, filtro por sistema, PDF A4 paisagem com 2 perfis por página) | `src/templates/relacao-pecas.html` (rótulos e campos mostrados), `src/assets/js/relacao.js` (filtro) e a parte "Relação de peças" de `src/assets/css/catalogo.css` (tela e impressão). Os dados vêm dos YAML de perfil; nada é digitado no template |
| Quais marcas têm a relação de peças | constante `RELACAO_MARCAS` em `src/build.py` (hoje `solucao` e `blindex`; página `docs/{marca}/relacao-pecas.html`, PDF `docs/pdf/{marca}/relacao-pecas.pdf`). Cada marca só lista os perfis dos próprios sistemas, com os nomes de sistema do `marcas.yaml` |
| Relação de peças folheável (seção 1 da biblioteca de perfis: título, texto "Gerada dos dados técnicos · revisão", botões Baixar PDF e Ver em lista) | `src/templates/biblioteca-perfis.html` (textos), `src/assets/js/folhear.js` (setas, contador, teclado, arrastar) e a parte "Relação de peças folheável" de `src/assets/css/catalogo.css`. As páginas vêm do PDF: o build converte cada página em JPG (150 dpi) em `docs/assets/img/folhear/{marca}/relacao-pecas-NN.jpg` (não editar à mão). A biblioteca de efeito de página é `src/assets/js/vendor/page-flip.browser.js` (StPageFlip 2.0.7, licença MIT em `LICENSE-page-flip-2.0.7.txt`; nada é carregado de CDN) |
| Recorte do desenho técnico nas fichas (relação de peças e PDFs por sistema) | `src/build_pdf.py`, função `recorta_desenho_img`: regra geral (a ficha CAD tem 3 linhas de tabela no topo; o desenho começa depois delas, com folga). Não há exceções; se uma ficha nova não recortar bem, a lista `RECORTE_EXCECOES` em `scripts/padroes.py` seria o lugar (hoje não existe) |
| Lista de perfis de um sistema | `src/data/categorias/{sistema}.yaml`, bloco `perfis` → `grupos` → `codigos` |
| Texto de apresentação do "Mapa geral de perfis" | `src/data/biblioteca.yaml` → `intro` |
| Linha de selantes | `src/data/selantes.yaml` |
| Rodapé (empresa, certificações, telefones) | `src/templates/base.html` |
| Título e frase da página "Escolha a marca" | `src/templates/entrada.html` |
| Capa de cada marca (selo "Rev. 0.2", título, "Escolha um sistema", números) | `src/templates/index.html` |
| Rótulos da página de perfil ("Dados técnicos", "Ficha técnica", "Usado em:") e das linhas da tabela de dados | `src/templates/perfil.html` e `src/templates/partials/ficha-dados.html` |
| Rótulos do Mapa geral de perfis (títulos, busca, filtros) | `src/templates/biblioteca-perfis.html` |
| Aparência (espaços, tamanhos, cores do layout) | `src/assets/css/catalogo.css` |

Não editar à mão: tudo em `docs/` (é sobrescrito a cada build) e `scripts/padroes.py` (regras que o build e o validador usam).

## 3. Achar e alterar em 5 passos
1. Abra a busca em todos os arquivos: `Ctrl+Shift+F`.
2. Em "arquivos a incluir", digite `src` e cole um trecho do texto que você vê no site (de preferência sem acento nem ponto final, para não errar).
3. Clique no resultado que estiver em `src/data/...` (ou em `src/templates/...` se for texto fixo da tela).
4. Altere o texto mantendo as aspas, os dois-pontos e o recuo (os espaços no início da linha) como estavam.
5. Salve (`Ctrl+S`). Se a extensão YAML sublinhar algo em vermelho, desfaça (`Ctrl+Z`) e confira o recuo.

Se o mesmo texto aparece em mais de um arquivo, altere em todos. Se não encontrar nada em `src/`, o texto vem de um nome de perfil ou de uma tabela; procure o código do perfil (por exemplo `SS-016`).

## 4. Exemplos comuns
- **Corrigir a frase de apresentação do BigSpace:** abra `src/data/categorias/portas-robustas.yaml` e altere a linha `lede:`.
- **Mudar o nome de um sistema só na Blindex:** em `src/data/marcas.yaml`, dentro de `blindex:` → `produtos:` → o sistema → `nome:`.
- **Alterar a descrição de um perfil:** abra `src/data/perfis/SS-016.yaml` e altere `descricao:`. O nome do arquivo de imagem do perfil não muda junto: ele é declarado em `imagem_desenho:` e `imagem_isometrica:` do mesmo YAML e segue o padrão de `scripts/padroes.py`.
- **Corrigir um limite dimensional:** em `src/data/categorias/sacada.yaml`, bloco `limites`, lista `linhas:` (cada linha tem dois itens: o nome do limite e o valor).
- **Frase da escolha de marca:** `src/data/marcas.yaml`, campo `entrada_texto` da marca.
- **Trocar o texto de contato do rodapé:** `src/templates/base.html`, linha `fcontact`.

## 5. Gerar, conferir e publicar
1. **Validar os dados:** no terminal do VS Code (`Ctrl+'`), rode `python scripts/validar_catalogo.py`. Deve mostrar (a) a (e) OK.
2. **Gerar o site:** `python src/build.py` (dependências em `src/requirements.txt`, incluindo `pypdfium2`, que transforma as páginas do PDF da relação de peças em imagem para o visualizador folheável; o PDF também usa Playwright e pypdf). Deve terminar com "Build concluído". (Se o Windows reclamar de pasta em uso, feche o Explorer na pasta `docs`.)
3. **Conferir no navegador:** botão direito em `docs/index.html` → **Open with Live Server**. Navegue até a página que você alterou e confira o texto.
4. **Publicar:** peça ao Claude.ai o bloco de publicação do que você alterou, cole no Claude Code aberto em `C:\GITHUB\CATALOGO_TECNICO` e deixe executar. O bloco valida, gera o site, confere os links, faz o commit e o push na branch `main`. O site atualiza no GitHub Pages: https://conexaoiatech.github.io/catalogo-tecnico/ (pode levar alguns minutos).

## 6. Regras e cuidados
- Edite só em `src/`. O que estiver em `docs/` é refeito pelo build e a sua alteração se perde.
- Um dado técnico mora em **um** arquivo (perfil em `src/data/perfis`, vínculo com o sistema em `src/data/categorias`, nome e cor da marca em `src/data/marcas.yaml`). Não copie o mesmo dado para outro arquivo.
- A ficha técnica individual do perfil prevalece sobre o YAML (exceções: SS-002 vale o YAML; FE-0207 tem área 274.43).
- Não coloque no repositório arquivos de CAD (.dwg, .dxf, .sldprt, .sldasm, .step, .bak, .plt), preços ou condições comerciais: o repositório é público. A pasta `cad-fonte/` fica só no seu computador.
- Não altere `src/data/estrutural.yaml` nem publique gráficos de pressão: as premissas são preliminares e dependem da validação do Coordenador de Produção.
- Textos de montagem e usinagem marcados como "em elaboração" são placeholders; troque pelo texto real no bloco `placeholder` da categoria.
- Se o build ou o validador mostrar erro, não publique: copie a mensagem (arquivo e linha) e peça ajuda ao Claude.ai.
- Mudou o caminho de um arquivo de texto ou criou um template? Atualize este guia no mesmo commit.
