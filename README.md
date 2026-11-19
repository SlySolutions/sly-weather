# Sly Weather

**Weather and rain for your own spot in the Netherlands, without sharing your location.**
A single HTML file: no server, no account, no cookies, no analytics. Dutch and English.

Live: **https://slysolutions.nl/weather/** (open on your phone and choose *Add to home screen*).

*Nederlands: zie [README.nl.md](README.nl.md). Design decisions and background (Dutch): [docs/](docs/).*


## What it does

- Current temperature, feels-like, wind and humidity for one or more saved places.
- Shower timeline for the next two hours: when the current shower ends, when the next one starts, and a dry window.
- Precipitation in mm for the next hour and the next 12 hours.
- Hourly chart for 48 hours (temperature, precipitation, chance) and a 7-day forecast.
- Animated rain radar for the whole country, past hour and next hour.
- Built-in offline map of the Netherlands (municipalities, places, districts, motorways, rivers) to pick a spot by tapping, by place name or by four-digit postcode.
- Optional "My location" button (https only): one tap shows the weather for where you are now as a temporary place, rounded on the device, saved only if you choose to.
- Three themes in the Sly Solutions style (light, dark, nerd), reorderable and collapsible tiles.
- Timeline tile: hours and week in one (3 h to 7 d) with rain bars, temperature (day high in red, night low in blue), wind and cloud cover; drag along it and a small map right under it (pinch or scroll to zoom, drag to pan, collapsible) plus a written forecast follow that moment (the big map follows too). With the cursor on now, the tile also shows the Now tile's shower line and key numbers. Within the radar hours the map shows the radar frame, beyond that a coarse model grid over the Netherlands (about 40 km).
- Timeline details (1.9): only the orange handle moves the time (the rest of the timeline scrolls the page), the Now button turns orange when you are away from now, the past is veiled, wind on a fixed scale over the full height with a narrow Bft axis (Beaufort 2, 4, 6, 8), and a dotted line for the chance of precipitation. The small map uses the same base as the big map (municipalities, rivers, roads and names by zoom, up to 16x) and shows the weather, temperature and wind at the chosen moment in its top-left corner. Both maps have a lock: locked means + and − only and the page scrolls over the map.
- Wind as Beaufort force first (Bft, with its name such as "moderate") and km/h alongside. The key numbers show the chance this hour, the peak in 12 hours and how long the dry window lasts.
- One flowing story under the small map, written from all data fetched for your place: at now it covers what it is like outside, the wind, the nearest station, the radar for the next hour, the rest of the day, tonight and in the evening tomorrow; for another moment it tells that hour and that whole day.
- Fast start: the service worker shows the saved version at once and fetches a new one in the background (a button offers to load it); while the file is still coming in, a short loading screen in the Sly Solutions style is shown instead of a half-built page.
- Sections menu (≡): tap a section to switch it on or off (saved), press and hold to show only that one while the menu is open.
- Tile mode: add `?tile=strip` (or `?tile=now,strip`, `tl`, `map`, `chart`, `days`) to the URL to show only those tiles with the place name, handy as a home-screen shortcut. Long-press the installed app icon for ready-made shortcuts (Showers, Now, Radar, Timeline).

## Privacy by design

Exactly four requests leave your device per refresh:

1. One request to **Open-Meteo** (KNMI HARMONIE model) with your coordinate **rounded to about 1 km**.
2. One request to **Open-Meteo** for a **fixed grid of 10 x 10 model points over the whole Netherlands** (hourly precipitation, 7 days), used for the map beyond the radar hours. The grid is identical for everyone and says nothing about you.
3. One request for the **national Buienradar radar image**, which is identical for everyone. The local rain nowcast is read from that image on your device.
4. One request for the **national readings of the KNMI weather stations** via Buienradar (temperature, wind, sunshine power, rain), also identical for everyone. Your device picks the nearest station itself; it gives the measured "now" and how light or dull it is outside.

No geocoding, no map tiles, no third-party fonts or scripts: the map, fonts and Leaflet are embedded in the file. Saved places and settings live in your browser's local storage. "Nerd mode" shows a log of every outgoing request. Location is used only when you press a button: the raw position is rounded at once, never stored and never leaves the device. A Content-Security-Policy in the page makes the browser enforce all of this: only Open-Meteo and the two Buienradar hosts (radar image, station readings) are allowed, nothing else can load or run.

## Run it yourself

Download [`sly-weather.html` from the latest release](../../releases/latest) and open it in a browser, or host the `site/weather/` folder on any https server (then it is installable as a PWA and works offline).

## Build from source

```bash
python3 src/build.py
```

`src/app_template.html` holds the app (CSS, HTML, JavaScript). `build.py` inlines the fonts, Leaflet and the map data from `src/data/`, computes the Content-Security-Policy hashes for the inline scripts, and writes `site/weather/index.html` (hosted copy with manifest, service worker and share preview) and `sly-weather.html` (standalone copy for opening from disk). Map data was prepared from CBS/Kadaster, OpenStreetMap (Overpass), GeoNames and the 4pp postcode table; the preparation scripts are not needed to build.

## Data and licenses

Weather: [Open-Meteo](https://open-meteo.com) (CC BY 4.0) · radar: [Buienradar](https://www.buienradar.nl) · map: CBS/Kadaster, © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors (ODbL), [GeoNames](https://www.geonames.org) (CC BY 4.0), [4pp](https://github.com/bobdenotter/4pp) · Leaflet (BSD-2) · Manrope and Space Mono (OFL).

App: CC BY-NC-SA 4.0, see [LICENSE](LICENSE) and [NOTICE](NOTICE) (name and logo excluded). A [Sly Solutions](https://slysolutions.nl) project.

## Feedback welcome

This is a first release and real-world feedback is the fastest way to improve it.

- **Bug or something unclear?** Open an [issue](../../issues/new?template=bug.md). A screenshot and the version number (bottom of the page) help a lot.
- **Idea?** Open an [idea](../../issues/new?template=idea.md), or comment on an existing one.
- **Like it?** A star helps others find it, and the live app at [slysolutions.nl/weather](https://slysolutions.nl/weather/) is free to share.

Ideas that keep the app as data-light as it is now are the easiest to adopt.
