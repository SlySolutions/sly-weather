#!/usr/bin/env python3
"""Sly Weather build: a Sly Solutions project (https://slysolutions.nl)
Source: https://github.com/SlySolutions/sly-weather · License CC BY-NC-SA 4.0

Assembles ../sly-weather.html and ../site/weather/index.html from app_template.html:
fonts, Leaflet, map data and the logo are inlined so the app is one self-contained file.
The Content-Security-Policy meta tag gets a sha256 hash per inline script, so the browser
enforces "nothing but Open-Meteo and the Buienradar image" instead of the app just promising it.
Blocks between <!-- site-only --> and <!-- /site-only --> (manifest, icons, service worker,
share preview) are left out of the standalone file, which is meant to be opened from disk."""
import base64, hashlib, json, os, re
H = os.path.dirname(os.path.abspath(__file__))
S = lambda p: open(os.path.join(H, p), encoding='utf-8').read()
B = lambda p: base64.b64encode(open(os.path.join(H, p), 'rb').read()).decode()
brand = S('brand.svg').replace('class="icon o"', '')
ASSETS = {
    '{{FONT_MANROPE}}': B('fonts/manrope.woff2'), '{{FONT_MONO400}}': B('fonts/spacemono400.woff2'), '{{FONT_MONO700}}': B('fonts/spacemono700.woff2'),
    '{{LEAFLET_CSS}}': S('libs/leaflet.css'), '{{LEAFLET_JS}}': S('libs/leaflet.js'),
    '{{BRAND_SVG_SMALL}}': brand,
    '{{GEMEENTEN}}': S('data/nl_gemeenten.json'), '{{PROVINCIES}}': S('data/nl_provincies.json'),
    '{{LIJNEN}}': S('data/nl_lijnen.json'), '{{PLAATSEN}}': S('data/nl_plaatsen.txt').replace('\\', '\\\\').replace('`', ''),
    '{{PC4}}': S('data/nl_pc4.txt').strip(),
    # Hoekpunten Buienradar RadarMapRainNL 550x512, Mercator, geijkt op de provinciegrenzen (IoU 0,84)
    '{{RADAR_BOUNDS}}': json.dumps({'west': 0.0, 'east': 10.0, 'north': 54.75, 'south': 49.41}),
}

def assemble(template, scripts_expected):
    """Fill the placeholders a template uses and add the CSP with one sha256 per inline script."""
    t = S(template)
    for k, v in ASSETS.items():
        if k in t:
            t = t.replace(k, v)
    scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', t, flags=re.S)
    assert len(scripts) == scripts_expected, f'{template}: {len(scripts)} inline scripts, expected {scripts_expected}'
    hashes = ' '.join("'sha256-" + base64.b64encode(hashlib.sha256(x.encode('utf-8')).digest()).decode() + "'" for x in scripts)
    csp = '; '.join([
        "default-src 'none'",
        'script-src ' + hashes,
        "style-src 'unsafe-inline'",                              # inline <style> and style attributes (Leaflet, tiles)
        "img-src 'self' data: https://image.buienradar.nl https://image-cdn.buienradar.nl",  # icons, radar frames as data URLs, the Buienradar sprite (image.buienradar.nl redirects to image-cdn)
        'connect-src https://api.open-meteo.com',                 # the only fetch()
        'font-src data:',                                         # fonts are inlined
        "manifest-src 'self'", "worker-src 'self'",               # PWA files next to index.html
        "base-uri 'none'", "form-action 'none'",
    ])
    assert '{{CSP}}' in t
    t = t.replace('{{CSP}}', csp)
    assert not re.search(r'\{\{[A-Z_0-9]+\}\}', t), 'placeholder niet vervangen in ' + template
    assert chr(0x2014) not in t, 'em dash in output of ' + template
    return t, csp

def write(path, text):
    open(path, 'w', encoding='utf-8').write(text); print('geschreven', os.path.relpath(path, os.path.join(H, '..')), round(len(text.encode()) / 1024), 'KB')

site = os.path.join(H, '..', 'site', 'weather')
t, csp = assemble('app_template.html', 4)   # early theme/tile script, Leaflet, app, service worker
if os.path.isdir(site):
    write(os.path.join(site, 'index.html'), t)
standalone = re.sub(r'<!-- site-only -->.*?<!-- /site-only -->\n?', '', t, flags=re.S)
assert 'site-only' not in standalone
write(os.path.join(H, '..', 'sly-weather.html'), standalone)
print('CSP:', csp)
