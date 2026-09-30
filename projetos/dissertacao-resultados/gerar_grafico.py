"""Visualiza a Tabela 5.7; não executa a microssimulação da POF."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def numero(valor):
    return float(valor.replace('−', '-').replace(',', '.'))


def main():
    dados = json.loads((ROOT / 'tabelas.json').read_text(encoding='utf-8'))
    tabela = dados['tabelas']['5.7']
    assert tabela[0][:5] == ['Décimo', 'S0', 'S1', 'S2', 'D1']
    assert [int(r[0]) for r in tabela[1:]] == list(range(1, 11))
    series = [(numero(r[3]), numero(r[4])) for r in tabela[1:]]
    assert all(0 <= d1 <= s2 <= 10 for s2, d1 in series)
    desenhos = dados['tabelas']['5.13'][1:]
    assert len(desenhos) == 4 and all(numero(r[1]) == 452.74 for r in desenhos)
    assert numero(desenhos[0][4]) == series[0][1]
    s = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="620" viewBox="0 0 1000 620" role="img" aria-labelledby="titulo desc">',
         '<title id="titulo">Carga tributária reportada na dissertação por décimo de renda</title>',
         '<desc id="desc">Comparação S2 e D1 da Tabela 5.7. Primeiro décimo: 8,29% e 6,14%. Décimo superior: 3,18% em ambos.</desc>',
         '<rect width="1000" height="620" fill="#f8fafc"/><g font-family="sans-serif" fill="#16324f">',
         '<text x="55" y="40" font-size="25" font-weight="bold">Cashback e regressividade remanescente</text>',
         '<text x="55" y="72" font-size="16">Resultados reportados no manuscrito · Tabela 5.7 · Carga/renda (%)</text>']
    for v in (0, 2, 4, 6, 8, 10):
        y = 450-v*32
        s += [f'<line x1="75" y1="{y}" x2="950" y2="{y}" stroke="#dbe3ec"/>', f'<text x="35" y="{y+5}" font-size="14">{v}%</text>']
    for i, par in enumerate(series):
        x = 95+i*86
        for j, val in enumerate(par):
            cor = ('#16324f', '#0d9488')[j]
            s += [f'<rect x="{x+j*30}" y="{450-val*32:.2f}" width="26" height="{val*32:.2f}" fill="{cor}"/>',
                  f'<text x="{x+j*30+13}" y="{442-val*32:.2f}" font-size="10" text-anchor="middle">{val:.2f}</text>']
        s += [f'<text x="{x+28}" y="477" font-size="14" text-anchor="middle">{i+1}</text>']
    s += ['<text x="500" y="506" text-anchor="middle" font-size="15">Décimos de UC ordenados por renda disponível per capita</text>',
          '<rect x="160" y="527" width="16" height="16" fill="#16324f"/><text x="185" y="540" font-size="14">S2: base sem devolução</text>',
          '<rect x="545" y="527" width="16" height="16" fill="#0d9488"/><text x="570" y="540" font-size="14">D1: aproximação do desenho legal</text>',
          '<text x="55" y="574" font-size="13">Núcleo modelado: 52,64% da despesa monetária própria. Não representa o efeito total da reforma.</text>',
          '<text x="55" y="597" font-size="13">Fonte: Contreras (2026), manuscrito fornecido em 30/09/2026. Simulação original não reexecutada.</text>', '</g></svg>']
    (ROOT/'carga-reportada.svg').write_text('\n'.join(s),encoding='utf-8')
    print('Gráfico gerado; estrutura, orçamento comum e coerência do primeiro décimo conferidos.')


if __name__ == '__main__':
    main()
