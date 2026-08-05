# Next Pro — Design Decisions

## Contexto

Redesign do template do site já em produção **www.amplificadoresnextpro.com.br** (Next Pro, fabricante brasileira de amplificadores de potência digitais). O site atual já roda em Joomla (URLs `/index.php/produtos/serie-pro-r/r2`); este template (`templates/nextpro/`) é a nova camada visual para ele. Repositório também hospeda o design de arquitetura do componente `com_campaigns` (`.claude/architecture/com_campaigns.md`) — independente deste template.

**Correção importante**: a primeira versão deste template (paleta azul institucional, conteúdo de "consultoria e serviços") foi feita sem consultar a marca real e estava errada — a Next Pro é uma empresa de hardware de áudio profissional, não uma consultoria. Esta versão foi refeita a partir do brand kit real da empresa no Canva.

## Decisões

### 1. Verde como único destaque — remoção deliberada do ciano
**Contexto**: o material histórico da Next Pro usa ciano/azul vibrante (ex: "R" de "PRO-R"). A empresa pediu explicitamente para reduzir o uso do ciano e migrar para o verde-menta gradualmente, e este site novo é parte dessa transição.
**Decisão**: usar `--color-primary` (verde `#29e6ac`) como única cor de destaque em todo o template. Nenhum componente novo usa ciano. Um token `--color-accent-legacy-cyan` fica comentado no CSS só como registro histórico, não utilizado.
**Consequência**: qualquer peça que precisar do ciano (ex: replicar um gráfico antigo) precisa de decisão explícita — o padrão do template não oferece a cor.

### 2. Escuro como identidade padrão, não um "dark mode" opcional
**Contexto**: todo o material de marca (catálogo, logo, apresentações) usa fundo escuro/preto. Um site "modo claro por padrão, escuro opcional" inverteria a identidade real.
**Decisão**: `colorScheme` do template tem `dark` como default. `light` continua disponível como opção (parâmetro do template), mas não é a identidade da marca — é uma alternativa de acessibilidade/preferência do usuário final.

### 3. Tipografia condensada bold para títulos
**Contexto**: o catálogo usa uma condensada bold em caixa-alta para todos os títulos ("CATÁLOGO DIGITAL 2026", "NOSSOS DIFERENCIAIS", "PRO-R").
**Decisão**: `Barlow Condensed` (600/700/800) via Google Fonts, uppercase + letter-spacing leve em `h1`–`h6`. Fonte de corpo continua `Inter` (contraste legível para texto técnico longo).
**Alternativa considerada**: recriar o efeito condensado só com CSS (negative letter-spacing sobre fonte de sistema) — descartado porque o resultado não se aproximava o suficiente do peso visual real da marca.

### 4. Logo: placeholder SVG, não o PNG real
**Contexto**: o PNG exportado do Canva não pôde ser baixado — a política de rede deste ambiente de execução bloqueia o domínio de export do Canva (`export-download.canva.com`), então o arquivo binário não chegou ao repositório.
**Decisão**: recriar a forma do chevron/seta (3 traços diagonais com opacidade decrescente) como SVG inline em `index.php`, usado só quando o parâmetro "Logo" do template não está configurado.
**Ação pendente**: fazer upload do PNG/SVG oficial via Joomla (parâmetro "Logo" do template) ou enviá-lo para a sessão de código para substituir o placeholder em `templates/nextpro/images/`.

### 5. Estrutura de conteúdo: catálogo de produtos, não páginas institucionais genéricas
**Contexto**: o site real já organiza produtos por série (Pro-R, Nano, NanoMix, NanoBox) com páginas individuais por modelo.
**Decisão**: o template mantém `banner`, `breadcrumbs` e module positions genéricas o suficiente para servir tanto páginas de série/produto quanto uma home institucional — nenhuma estrutura de menu é fixada nos arquivos do template (isso continua sendo definido no Joomla, em Menus, espelhando a estrutura de URLs já existente).

## Cross-check com padrões deprecados

Nenhum padrão descrito em `.claude/includes/joomla-depreciated.md` foi usado — o template não toca em código de extensão/backend.
