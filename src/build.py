#!/usr/bin/env python3
"""Sly Weather build — a Sly Solutions project (https://slysolutions.nl)
Source: https://github.com/SlySolutions/sly-weather · License CC BY-NC-SA 4.0

Assembles ../sly-weather.html and ../site/weather/index.html from app_template.html:
fonts, Leaflet, map data and the logo are inlined so the app is one self-contained file."""
import base64, json, os
H = os.path.dirname(os.path.abspath(__file__))
S = lambda p: open(os.path.join(H, p), encoding='utf-8').read()
B = lambda p: base64.b64encode(open(os.path.join(H, p), 'rb').read()).decode()
t = S('app_template.html')
brand = S('brand.svg').replace('class="icon o"', '')
rep = {
    '{{FONT_MANROPE}}': B('fonts/manrope.woff2'), '{{FONT_MONO400}}': B('fonts/spacemono400.woff2'), '{{FONT_MONO700}}': B('fonts/spacemono700.woff2'),
    '{{LEAFLET_CSS}}': S('libs/leaflet.css'), '{{LEAFLET_JS}}': S('libs/leaflet.js'),
    '{{BRAND_SVG_SMALL}}': brand,
    '{{GEMEENTEN}}': S('data/nl_gemeenten.json'), '{{PROVINCIES}}': S('data/nl_provincies.json'),
    '{{LIJNEN}}': S('data/nl_lijnen.json'), '{{PLAATSEN}}': S('data/nl_plaatsen.txt').replace('\\', '\\\\').replace('`', ''),
    '{{PC4}}': S('data/nl_pc4.txt').strip(),
    # Hoekpunten Buienradar RadarMapRainNL 550x512, Mercator, geijkt op de provinciegrenzen (IoU 0,84)
    '{{RADAR_BOUNDS}}': json.dumps({'west': 0.0, 'east': 10.0, 'north': 54.75, 'south': 49.41}),
}
for k, v in rep.items():
    assert k in t, k
    t = t.replace(k, v)
import re; assert not re.search(r'\{\{[A-Z_0-9]+\}\}', t), 'placeholder niet vervangen'
out = os.path.join(H, '..', 'sly-weather.html')
open(out, 'w', encoding='utf-8').write(t)
site = os.path.join(H, '..', 'site', 'weather', 'index.html')
if os.path.isdir(os.path.dirname(site)): open(site, 'w', encoding='utf-8').write(t); print('ook geschreven', site)
print('geschreven', out, round(len(t.encode()) / 1024), 'KB')
