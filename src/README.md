# Source

Sly Weather is one HTML file; this folder holds the parts it is built from.

| Path | What |
|---|---|
| `app_template.html` | The app: CSS, HTML and JavaScript, with `{{PLACEHOLDERS}}` for the embedded assets. |
| `test_template.html` | The timeline experiment at `/weather/test/`: one timeline with the rain map and the forecast for the moment under your finger. Built by `build.py` into `../site/weather/test/index.html` (site only). |
| `build.py` | Fills the placeholders and writes `../sly-weather.html` and `../site/weather/index.html`. Run `python3 src/build.py`. |
| `data/` | Map data for the Netherlands: municipalities and provinces (CBS/Kadaster), places and districts (GeoNames, OSM, 4pp), PC4 postcode centroids (4pp), roads and rivers (OpenStreetMap, stored as polyline text). |
| `fonts/` | Manrope and Space Mono (OFL), inlined as base64. |
| `libs/` | Leaflet 1.9.4 (BSD-2), inlined. |
| `brand.svg` | The Sly Solutions mark used in the footer and the app icon. |
| `radar_ijking.py` | Calibration of the Buienradar image corners against the province outlines. |

Questions or ideas: open an issue at https://github.com/SlySolutions/sly-weather/issues or visit https://slysolutions.nl.
