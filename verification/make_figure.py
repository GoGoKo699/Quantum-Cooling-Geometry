#!/usr/bin/env python3
"""Generate the exact contact-layout schematic from its declared path geometry."""
from pathlib import Path

N = 16
LAYOUTS = [("Spread contacts", set(range(0, N, 2))), ("Clustered contacts", set(range(N // 2)))]
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="340" viewBox="0 0 1000 340" role="img" aria-labelledby="title desc">',
       '<title id="title">Equal contact counts, different cooling geometry</title>',
       '<desc id="desc">Sixteen qubits with eight teal reset contacts. Alternating contacts have distance sum 8. Contacts clustered on the left half have distance sum 36.</desc>',
       '<rect width="1000" height="340" fill="#fbfdfd"/>',
       '<g font-family="Arial, Helvetica, sans-serif" fill="#163c42">',
       '<text x="36" y="38" font-size="24" font-weight="bold">The same 8 contacts can give different noise burdens</text>']
for row, (name, ports) in enumerate(LAYOUTS):
    y = 111 + 143 * row
    distances = [min(abs(i-s) for s in ports) for i in range(N)]
    svg += [f'<text x="36" y="{y-30}" font-size="19" font-weight="bold">{name}</text>',
            f'<text x="700" y="{y-30}" font-size="18">Distance sum M = {sum(distances)}</text>',
            f'<line x1="52" y1="{y}" x2="937" y2="{y}" stroke="#9bafb3" stroke-width="3"/>']
    for i, d in enumerate(distances):
        x = 52 + 59*i
        fill = '#08636a' if i in ports else '#edf2f2'
        color = 'white' if i in ports else '#244c53'
        svg += [f'<circle cx="{x}" cy="{y}" r="17" fill="{fill}" stroke="#08636a" stroke-width="2"/>',
                f'<text x="{x}" y="{y+6}" text-anchor="middle" font-size="16" fill="{color}">{d}</text>']
    svg += [f'<text x="36" y="{y+47}" font-size="15">Teal: reset contact. Number: distance to the nearest contact.</text>']
svg += ['</g></svg>']
out = Path(__file__).resolve().parents[1] / 'figures' / 'contact-layouts.svg'
out.parent.mkdir(exist_ok=True)
out.write_text('\n'.join(svg)+'\n', encoding='utf-8')
print(out.relative_to(out.parents[1]))
