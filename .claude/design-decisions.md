# Next Pro — Design Decisions

## Contexto

Site institucional/de serviços para a empresa **Next Pro**. Repositório também hospeda o design de arquitetura do componente `com_campaigns` (`.claude/architecture/com_campaigns.md`) — os dois projetos convivem neste repo, mas são independentes: o template não depende do componente para funcionar.

## Decisões

### 1. Bootstrap 5 sem build tool
**Contexto**: sem time de frontend dedicado, prioridade é entregar rápido e manter fácil.
**Decisão**: usar Bootstrap 5.3 via CDN, CSS próprio em arquivos planos (`template.css` + `custom.css`), sem Sass/Vite/Webpack.
**Consequência**: menos flexibilidade de customização profunda do Bootstrap (não é possível recompilar variáveis Sass), mas zero passo de build — qualquer editor já funciona, inclusive editar `custom.css` direto no servidor se necessário.
**Alternativa considerada**: Tailwind CSS — descartado por exigir pipeline de build (Vite) que adiciona complexidade sem um ganho claro para um site institucional simples.

### 2. Bootstrap via CDN, não empacotado
**Contexto**: sem build tool, ou se baixa os arquivos manualmente ou se referencia via CDN.
**Decisão**: referenciar `bootstrap.min.css`/`bootstrap.bundle.min.js` do jsdelivr no `joomla.asset.json`.
**Consequência**: depende de disponibilidade externa (jsdelivr) e adiciona uma requisição a domínio de terceiro. **Recomendação para produção**: baixar os arquivos e colocá-los em `templates/nextpro/css/vendor/` e `js/vendor/`, atualizando as URIs no `joomla.asset.json` para caminhos locais — evita dependência externa e problemas de privacidade/CSP.

### 3. Estrutura de páginas institucional
**Decisão**: estrutura de menu recomendada — Home, Sobre, Serviços, Contato (mais Blog/Notícias se o cliente quiser conteúdo recorrente). Position `banner` no `index.php` foi criada especificamente para uma hero de destaque na Home; páginas internas normalmente não a usam.
**Nota importante**: essas páginas/menus são criados dentro do Joomla (Conteúdo > Artigos, Menus > Menu principal) depois que o Joomla estiver instalado na hospedagem — não são arquivos deste repositório.

### 4. Sem sidebar por padrão
**Decisão**: `sidebarPosition` default = `none`. Site institucional geralmente usa layout full-width nas páginas de conteúdo.
**Quando mudar**: se o cliente quiser uma seção de blog com sidebar (categorias, posts recentes), ativar o parâmetro do template e adicionar módulos na posição `sidebar`.

### 5. pt-BR como idioma principal do template
**Decisão**: arquivos de idioma criados para `en-GB` (obrigatório como fallback no Joomla) e `pt-BR` (idioma real do site). Ao instalar, configure `pt-BR` como idioma padrão do site em Sistema > Idiomas.

## Cross-check com padrões deprecados

Nenhum padrão descrito em `.claude/includes/joomla-depreciated.md` foi usado — o template não toca em código de extensão/backend, então a maioria das regras daquele arquivo (DI, MVC, Table classes) não se aplica a este projeto de front-end.
