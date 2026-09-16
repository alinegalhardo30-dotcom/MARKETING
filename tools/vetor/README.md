# Vetorização das peças de marca

Gera, em SVG 100% vetorial (sem bitmap embutido), as duas peças de marca que
ficam na raiz do repositório:

| Arquivo gerado | Peça | Tamanho |
| --- | --- | --- |
| `marca-next-pro-siga-qr.svg` | "Siga a Next Pro" — logo, linha de produtos e QR | 2000 × 1291 |
| `marca-next-pro-projetado-fabricado-brasil.svg` | "Projetado e fabricado no Brasil" | 1990 × 1806 |

Como o SVG é vetorial, as medidas acima são só o tamanho nominal: a peça pode
ser exportada em qualquer resolução sem perda.

## Como rodar

```bash
python3 -m pip install fonttools qrcode
# opcional, só para gerar o PNG de pré-visualização:
python3 -m pip install cairosvg

# as fontes não são versionadas aqui; baixe-as uma vez:
mkdir -p fonts && cd fonts
curl -LO https://raw.githubusercontent.com/google/fonts/main/ofl/orbitron/Orbitron%5Bwght%5D.ttf
mv 'Orbitron[wght].ttf' Orbitron-VF.ttf
curl -Lo Inter-VF.ttf 'https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz,wght%5D.ttf'
cd ..

python3 build1.py
python3 build2.py
```

`NP_FONT_DIR` permite apontar para outro diretório de fontes.

## Estrutura

- `lib.py` — converte texto em contornos (`path`), gera glifos de display
  segmentado (14 segmentos) e a matriz do QR.
- `logo.py` — o símbolo da marca (a "asa" listrada) desenhado como geometria
  vetorial paramétrica.
- `build1.py` / `build2.py` — montagem de cada peça.

## Observações sobre a reconstrução

- **Todo texto vira contorno** (`<path>`), não `<text>`: as peças abrem igual em
  qualquer máquina, sem depender de fonte instalada.
- **Tipografia**: o desenho usa Orbitron (títulos/caixa alta) e Inter (texto
  corrido), ambas SIL OFL. São as equivalentes livres mais próximas das fontes
  das peças originais; se a fonte oficial da marca estiver disponível, basta
  trocar o arquivo em `fonts/` e regerar.
- **QR Code**: regerado a partir da URL
  `https://www.instagram.com/amplificadoresnextpro` (nível de correção M,
  versão 4 / 33 × 33 módulos — o mesmo tamanho do QR original). O destino da
  leitura é o mesmo; o desenho dos módulos é o de um QR novo, não uma cópia
  módulo a módulo do bitmap antigo.
- **Fundo da peça 2**: a textura de painéis/mostradores ao fundo é uma
  reconstrução vetorial aproximada, em opacidade baixa.
