# Next Pro — Style Guide

> Guia de estilo do template `nextpro`. Os valores de cor abaixo são **placeholder** — ajuste para a identidade visual real da Next Pro (logo, paleta oficial) assim que estiverem definidos, editando `templates/nextpro/css/template.css`.

## Paleta de cores

| Token | Valor | Uso |
|-------|-------|-----|
| `--color-primary` | `#0b3d91` | Links, botões primários, marca |
| `--color-primary-dark` | `#082a66` | Hover de primária, topbar |
| `--color-secondary` | `#495867` | Texto secundário, elementos neutros |
| `--color-accent` | `#12a594` | Destaques, foco, CTAs secundários |
| `--color-background` | `#ffffff` (claro) / `#10151c` (escuro) | Fundo da página |
| `--color-surface` | `#f5f7fa` (claro) / `#171d26` (escuro) | Cards, footer, breadcrumbs |
| `--color-text` | `#1c2530` (claro) / `#e6e9ed` (escuro) | Texto principal |
| `--color-text-muted` | `#5b6672` (claro) / `#a2acb8` (escuro) | Texto secundário |
| `--color-border` | `#dfe4ea` (claro) / `#2a323d` (escuro) | Bordas, divisores |

O tema escuro segue `prefers-color-scheme: dark` automaticamente, ou pode ser forçado pelo parâmetro do template **Esquema de cores** (`data-color-scheme` no `<html>`).

## Tipografia

- **Fonte base**: `Inter` com fallback para `system-ui` — carregue o Inter via Google Fonts ou self-host se quiser evitar terceiros.
- **Escala**: usa `rem` a partir de `--font-size-base: 1rem`; títulos podem usar `clamp()` para fluidez responsiva.
- **Hierarquia**: um único `<h1>` por página, seguindo a ordem lógica `h1 > h2 > h3`.

## Espaçamento

Escala em `--space-xs` (0.25rem) até `--space-xl` (3rem) — ver `templates/nextpro/css/template.css`.

## Componentes de layout

- **Header**: logo/marca + navegação principal, com toggle mobile abaixo de 992px.
- **Topbar** (opcional): faixa fina acima do header — útil para telefone/e-mail de contato.
- **Banner** (opcional): faixa de destaque com gradiente, pensada para a hero da Home.
- **Sidebar** (opcional): ativada via parâmetro do template; usada em páginas de conteúdo/blog, não na Home institucional.
- **Footer**: módulos de footer + copyright automático.

## Framework

- **Bootstrap 5.3** carregado via CDN (`jsdelivr`) e registrado no `joomla.asset.json`. Para produção, considere hospedar os arquivos localmente em vez do CDN (ver `design-decisions.md`).
- **Sem build tool** — CSS puro em `css/template.css` (tokens + base) e `css/custom.css` (ajustes específicos do site, nunca sobrescrito por regeneração).

## Acessibilidade

Segue WCAG 2.1 AA: skip link, landmarks semânticos, foco visível (`:focus-visible`), contraste mínimo 4.5:1, `prefers-reduced-motion` respeitado, alvos de toque ≥44px.
