"""Demonstração didática: números sintéticos, sem calibração para o Brasil."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# Dez grupos de igual tamanho; valores mensais por domicílio fictício.
RENDA = (1000, 1600, 2200, 2900, 3700, 4700, 6100, 8100, 11500, 21000)
PROP_CONSUMO = (.98, .95, .92, .89, .86, .82, .77, .71, .64, .50)


def calcular(renda, consumo, aliquota=.20, devolucao=0):
    """Consumo inclui tributo; alíquota incide sobre a base sem tributo."""
    if renda <= 0 or consumo < 0 or aliquota < 0 or not 0 <= devolucao <= 1:
        raise ValueError('Renda deve ser positiva; consumo/alíquota não negativos; devolução entre 0 e 1.')
    bruto = consumo * aliquota / (1 + aliquota)
    cashback = bruto * devolucao
    return bruto, cashback, bruto - cashback


def simular():
    linhas = []
    for d, (renda, prop) in enumerate(zip(RENDA, PROP_CONSUMO), 1):
        consumo = renda * prop
        # Regra puramente ilustrativa: devolução de 50% aos três primeiros grupos.
        bruto, cashback, liquido = calcular(renda, consumo, devolucao=.5 if d <= 3 else 0)
        linhas.append(dict(grupo=d, renda=renda, consumo=consumo, tributo_bruto=bruto,
                           cashback=cashback, tributo_liquido=liquido,
                           carga_bruta_pct=100*bruto/renda, carga_liquida_pct=100*liquido/renda))
    return linhas


def grafico(linhas):
    # SVG estático sem dependências: barras agrupadas, escala comum em porcentagem.
    partes = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="600" viewBox="0 0 1000 600" role="img" aria-labelledby="titulo desc">',
              '<title id="titulo">Carga tributária sobre a renda: demonstração sintética</title>',
              '<desc id="desc">Barras com carga bruta e líquida em dez grupos fictícios. Cashback de 50% do tributo apenas nos grupos 1 a 3.</desc>',
              '<rect width="1000" height="600" fill="#f8fafc"/>',
              '<g font-family="sans-serif" fill="#16324f">',
              '<text x="55" y="42" font-size="26" font-weight="bold">Cashback e carga tributária sobre a renda</text>',
              '<text x="55" y="72" font-size="16">DADOS SINTÉTICOS · Exemplo didático, sem estimativas para o Brasil</text>']
    for tick in (0, 5, 10, 15, 20):
        y = 465 - tick * 16
        partes += [f'<line x1="75" y1="{y}" x2="960" y2="{y}" stroke="#dbe3ec"/>',
                   f'<text x="30" y="{y+5}" font-size="14">{tick}%</text>']
    for i, linha in enumerate(linhas):
        x = 96 + i * 86
        for dx, campo, cor in ((0, 'carga_bruta_pct', '#16324f'), (29, 'carga_liquida_pct', '#0d9488')):
            valor = linha[campo]
            partes.append(f'<rect x="{x+dx}" y="{465-valor*16:.2f}" width="25" height="{valor*16:.2f}" fill="{cor}"/>')
            partes.append(f'<text x="{x+dx+12.5}" y="{456-valor*16:.2f}" font-size="11" text-anchor="middle">{valor:.1f}</text>')
        partes.append(f'<text x="{x+27}" y="490" font-size="14" text-anchor="middle">{i+1}</text>')
    partes += ['<text x="500" y="520" font-size="15" text-anchor="middle">Grupos de renda fictícios (menor → maior)</text>',
               '<rect x="280" y="545" width="18" height="18" fill="#16324f"/><text x="308" y="559" font-size="15">Carga bruta</text>',
               '<rect x="520" y="545" width="18" height="18" fill="#0d9488"/><text x="548" y="559" font-size="15">Carga após cashback</text>',
               '</g></svg>']
    return '\n'.join(partes)


def main():
    linhas = simular()
    saida = ROOT / 'resultados'
    saida.mkdir(exist_ok=True)
    with (saida / 'resultados.csv').open('w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=linhas[0].keys())
        escritor.writeheader()
        escritor.writerows({k: round(v, 6) for k, v in linha.items()} for linha in linhas)
    (saida / 'carga-tributaria.svg').write_text(grafico(linhas), encoding='utf-8')
    print(f'Resultados sintéticos gerados em {saida}')


if __name__ == '__main__':
    main()
