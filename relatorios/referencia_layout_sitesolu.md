# Referência de layout — SITESOLU (site novo)

Levantamento só leitura de `C:\GITHUB\SITESOLU` (nada foi alterado lá). Gerado em 2026-10-28, passo 3n.

## 1. O que existe no SITESOLU

| Item | Onde | O que é |
|---|---|---|
| Site novo (referência de design) | `docs/solucao-sacadas-demo.html` (24 KB) = `index.html` da branch `novo` (idênticos) | Página única, HTML + CSS inline, sem build. Publicada como demo em `solucao-sacadas-demo.netlify.app` |
| Pacote do site | `docs/solucao-sacadas-site.zip` (5,6 KB) | Só contém o mesmo `index.html` |
| Site legado | `naocomitar/bkp_site_checklist/.../solucao-2017/` (fora do git, tema WordPress) | Tema `solucao-2017` com fontes Exo, Source Sans Pro, Montserrat e Corbert. Identidade antiga, **não é a referência** |
| Governança | `CLAUDE.md`, `MANUAL_SITESOLU.md`, `INSTRUÇÃO_CLAUDE_IA.txt`, `docs/` | Fluxo GOV_IA_CORE, banco, workflows n8n. Nada de design |
| Build / config | — | **Não há** build, `package.json`, Tailwind nem pasta de imagens ou fontes locais |

Branches do repositório: `master` (trabalho atual, com o demo não rastreado em `docs/`), `legado` (WordPress) e `novo` (só o `index.html` do site novo).

## 2. Skill ou design system

**Nenhum skill nem design system está registrado no SITESOLU.** Busca feita por `SKILL.md`, `design-taste`, `frontend-design`, `.claude/` (só `settings.json` com permissões de n8n), comentários no HTML e README: nada.

A única pista de origem está no HIST de 2026-10-22 (`docs/hist/HIST_2026-10-22_a_2026-10-22_sitesolu_separacao-branches-legado-novo.md`, passo P1): o site foi montado como *"site de demonstração (hero, cards de produto, timeline, depoimentos, CTA) com identidade visual tech escura"* via **artifact Design + export HTML**, e publicado no Netlify. O design ficou todo no HTML; não há tokens em arquivo separado.

## 3. Design extraído de `solucao-sacadas-demo.html`

### Paleta (variáveis CSS em `:root`)
| Token | Hex | Uso |
|---|---|---|
| `--bg` | `#080A10` | fundo da página |
| `--bg-2` | `#0D1018` | faixas alternadas (marquee, depoimentos) |
| `--surface` / `--surface-2` | `#11141D` / `#161A26` | cards (gradiente vertical entre os dois) |
| `--line` | `#232838` | bordas e divisórias |
| `--text` | `#F2F4F8` | texto principal |
| `--text-dim` | `#8B93A7` | texto secundário |
| `--accent` | `#3D5AFE` | azul de ação (botão primário, destaques) |
| `--accent-2` | `#00E5FF` | ciano (links, ícones, números) |
| `--glass` | `rgba(61,90,254,.12)` | fundo de ícone e de passo |

Gradientes: `linear-gradient(120deg, accent, accent-2)` em texto de destaque e logo; `linear-gradient(120deg,#fff, accent-2)` nos números grandes. Não há modo claro; **o site é só escuro**.

### Tipografia
- **Space Grotesk** (títulos, botões, números): pesos 400–700, `letter-spacing:-0.02/-0.03em`. Fonte do **Google Fonts** via `@import`.
- **Inter** (corpo): pesos 400–600, mesma origem.
- Tamanhos: h1 76px (44px no celular), h2 38–44px, h3 18–19px, corpo 14–16px, lede 19px, rótulos 12–13px.

### Espaçamento, grid, formas
- Container `max-width:1280px`, padding lateral 24px. Seções com 100–140px de respiro vertical.
- Grade de cards: 3 colunas, gap 24px (1 coluna até 960px).
- Raios: botões e chips em pílula (999px), cards 20px, ícones 14px, CTA 32px.
- Sombras: sobre hover `0 24px 48px -20px rgba(0,0,0,.6)` no card; `0 14px 32px -8px rgba(61,90,254,.65)` no botão primário. "Glow orbs" desfocados (blur 90px, opacidade .35) em azul e ciano como fundo.

### Componentes
- **Cabeçalho:** sticky, `backdrop-filter:blur(14px)`, fundo translúcido, borda inferior. À esquerda quadrado com "S" em gradiente + nome; ao centro 4 "pills" de navegação; à direita botão ghost "Área do Cliente". **Sem logo em imagem.**
- **Navegação no celular:** os links centrais simplesmente somem (`display:none` abaixo de 960px). **Não há menu hambúrguer**; só o botão da direita continua.
- **Hero:** centralizado, chip com ponto ciano, h1 com palavra em gradiente, lede, dois botões (primário e ghost), linha de 3 estatísticas.
- **Marquee:** faixa rolando com os nomes dos sistemas, animação `scrollx 22s` linear infinita.
- **Cards:** gradiente + borda `--line`, ícone em caixa de vidro, título, texto dim, link ciano "Conheça melhor →". Hover: sobe 8px, borda azul, ícone gira.
- **Botões:** primário (azul, pílula, seta que desliza no hover) e ghost (borda, hover ciano).
- **Timeline "Como funciona":** coluna fixa (sticky) à esquerda e 4 passos numerados à direita, ligados por linha em gradiente.
- **Depoimentos:** 3 cards em grade. **CTA final:** bloco grande arredondado com gradiente e orbe.
- **Rodapé:** endereço, colunas Produtos e Contato, borda superior.
- **Tabelas:** não existem no site novo.

### Efeitos e acessibilidade
- Revelação ao rolar (`.reveal`, `IntersectionObserver`, `translateY(28px)`, 0,7 s).
- Hover com `transform` e transições de 0,3–0,45 s.
- `prefers-reduced-motion` desliga animações e transições. `scroll-behavior:smooth`.

### Logos e imagens
- O site novo **não usa nenhuma imagem de marca**; o logo é um quadrado CSS com a letra "S".
- Logos reais estão no catálogo: `src/assets/img/marcas/solucao.png` (2172×724, fundo branco, 1 MB) e `blindex.png`.
- Não há imagens nem fontes locais para copiar.

## 4. Comparação com o catálogo atual

| Aspecto | SITESOLU novo | Catálogo hoje |
|---|---|---|
| Tema | escuro, tech, gradientes azul-ciano | claro (`#FAFAF8`), sidebar escura `#1A1D21`, azul `#0077B6` |
| Fontes | Space Grotesk + Inter | Archivo / Archivo Expanded + Inter + Space Mono |
| Formas | pílulas e cantos 20–32px | cantos de 2–4px, estilo documento técnico |
| Navegação | topo, pills | sidebar fixa + trilha no topo |
| Celular | só some o menu | sidebar vira um bloco grande no topo |

## 5. O que dá para reaproveitar direto e o que exige adaptação

**Reaproveitar quase direto**
- Fontes **Space Grotesk e Inter** (Inter já é do catálogo; Space Grotesk substitui Archivo nos títulos).
- Escala tipográfica (h1/h2/h3, lede), `letter-spacing` negativo em títulos.
- Botões primário e ghost, chips, pílulas de navegação, `--glass` para ícones.
- Cards de sistema (gradiente + hover com elevação) na capa e nas páginas de sistema.
- Revelação ao rolar e o bloco `prefers-reduced-motion`, que são independentes de conteúdo.
- Cabeçalho sticky com `backdrop-filter`, que combina com a trilha atual.

**Exigem adaptação**
- **Tema escuro versus fichas técnicas:** as imagens das fichas têm fundo branco e traço preto. Em página escura precisam de moldura/painel claro, e a tabela técnica e a trilha também precisam de contraste revisado. Decidir entre escuro total, ou escuro no cabeçalho e na capa com miolo claro.
- **Cor por marca:** o catálogo usa `--pc` por marca (Solução azul, Blindex vermelho). O par azul/ciano do site novo precisa virar tokens por marca.
- **Sidebar:** o site novo não tem. É preciso decidir entre manter a sidebar ou migrar para navegação por topo com menu hambúrguer, que o site novo **não resolve** (só esconde os links no celular).
- **Logo:** o site novo usa um "S" em CSS. O catálogo precisa de um logo em imagem menor (o `solucao.png` tem 1 MB e fundo branco, ruim em fundo escuro).
- **Componentes sem equivalente no site novo:** tabelas técnicas, filtro e busca da biblioteca, lightbox, trilha, cards de perfil com miniatura.
- **Efeitos pesados** (orbes de blur, marquee) devem ser opcionais: custam desempenho e distraem em páginas de consulta técnica.

## 6. Prints

`relatorios/teste_visual/referencia/`: `sitesolu_home_{desktop,celular}.png` e `sitesolu_interna_produtos_{desktop,celular}.png` (o site novo tem uma página só; a "interna" é a seção de produtos).
`relatorios/teste_visual/antes/`: catálogo atual (ver os problemas listados no relatório do passo).
