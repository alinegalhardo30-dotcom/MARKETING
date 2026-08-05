# Next Pro — Style Guide

> Fonte: brand kit "NEXT PRO OFICIAL" e "Catálogo Digital 2026" no Canva da empresa. A Next Pro é fabricante brasileira de amplificadores de potência digitais (áudio profissional/PA), sediada em Valinhos, SP. Slogan: *"Potência que inspira confiança"* / *"A tecnologia que você pode confiar"*.

## Paleta de cores

| Token | Valor | Uso |
|-------|-------|-----|
| `--color-primary` | `#29e6ac` | Cor de destaque **principal** da marca — links, botões, títulos de seção, badges |
| `--color-primary-strong` | `#1fc794` | Hover/estado ativo do verde |
| `--color-ink` | `#0d0f11` | Preto/grafite mais escuro — topbar, footer |
| `--color-background` | `#14171a` | Fundo padrão da página (identidade é **escura por padrão**, não clara) |
| `--color-surface` | `#1c2024` | Cards, painéis de destaque ("Nossos Diferenciais") |
| `--color-surface-raised` | `#22262b` | Elementos elevados sobre a surface |
| `--color-border` | `#2b3036` | Bordas, divisores |
| `--color-text` | `#f2f4f3` | Texto principal (branco levemente suave) |
| `--color-text-muted` | `#9aa3a0` | Texto secundário |

**Sobre o ciano**: o material antigo da Next Pro usa um azul-ciano vibrante (visível no "R" de "PRO-R"). A empresa está **migrando deliberadamente do ciano para o verde** — por isso este template usa **apenas verde** como destaque; o ciano não é usado em nenhum componente novo. Um token `--color-accent-legacy-cyan` fica comentado no CSS só como referência histórica.

Cores acima são estimadas visualmente a partir do material do Canva (não há um seletor de cor exato disponível via API) — se precisar de precisão absoluta (ex: para impressos), confirme o hex exato abrindo o brand kit direto no Canva.

## Tipografia

- **Títulos**: `Barlow Condensed` (600–800), uppercase, letter-spacing leve — reproduz a tipografia condensada bold usada no catálogo ("CATÁLOGO DIGITAL", "PRO-R", "NOSSOS DIFERENCIAIS"). Carregada via Google Fonts no `joomla.asset.json`.
- **Corpo**: `Inter` com fallback `system-ui` — mantém legibilidade em textos longos de especificação técnica.
- Sem itálico decorativo — o material da marca é todo caixa-alta/bold para destaque, regular para corpo.

## Logo

- Marca: seta/chevron formada por 3 traços diagonais (fade de opacidade) + wordmark "NEXT PRO" em condensada bold.
- **O arquivo PNG oficial não está neste repositório** — a política de rede deste ambiente bloqueou o download direto do Canva. Um placeholder SVG equivalente está embutido em `templates/nextpro/index.php` (classe `.tpl-brand__mark`) até o arquivo real ser enviado.
- Para usar o logo real: exporte no Canva (design "Logotipo nome minimalista em branco e preto") e faça upload via **Sistema → Modelos → nextpro → parâmetro "Logo"** no Joomla, ou envie o PNG para a sessão de código para eu incluir em `templates/nextpro/images/`.

## Layout e componentes

- **Header/topbar/footer**: fundo escuro contínuo (`--color-ink`/`--color-background`), sem separação clara vs. escura — a marca não tem versão "modo claro" nos materiais originais.
- **Esquema de cores**: parâmetro do template tem `dark` como padrão; `light` existe como opção alternativa (não é a identidade real da marca, é uma opção de acessibilidade/preferência).
- **Cantos**: raio de borda pequeno (`0.25rem`) — visual mais técnico/anguloso, ecoando o chevron do logo, não o arredondado suave de um site de serviços.
- **Cards** ("Nossos Diferenciais", produtos): fundo `--color-surface`, borda sutil, sem sombra pesada — mesmo padrão visual do catálogo digital.

## Conteúdo real da marca (para uso nos textos do site)

- **Diferenciais**: 100% desenvolvido e fabricado no Brasil · Sistema MultiFLEX · PFC Ativo · Operação 100–260VAC sem perda de potência (única do mundo a suportar até 420VAC)
- **Linhas de produto**: Série Pro-R (R2, R3, R6, R10, R10Q — touring/PA), Série Nano (NA-2650, NA-4350, NA-2350, NA-2100, linha CVT para 70,7V/141,4V), NanoMix (PowerMix, PreMixer Stereo/One Zone/Dual Zone), NanoBox (M300, M700, M12, M25, M1000/M2000 Cross)
- **Contato**: WhatsApp (19) 3327-7101 · Instagram @amplificadoresnextpro · Alameda Itatinga, 937, Joapiranga, Valinhos–SP, CEP 13278-480
- **Site atual**: www.amplificadoresnextpro.com.br (já roda em Joomla — `/index.php/produtos/...`)

## Acessibilidade

WCAG 2.1 AA: skip link, landmarks semânticos, foco visível (`:focus-visible` em verde), `prefers-reduced-motion` respeitado, alvos de toque ≥44px. Contraste do verde (#29e6ac) sobre o fundo escuro (#14171a) é alto — validar contraste também para texto verde sobre `--color-surface` em componentes novos.
