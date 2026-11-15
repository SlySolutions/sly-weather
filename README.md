# Sly Weather

**Weather and rain for your own spot in the Netherlands, without sharing your location.**
A single HTML file: no server, no account, no cookies, no analytics. Dutch and English.

Live: **https://slysolutions.nl/weather/** (open on your phone and choose *Add to home screen*).

*Nederlands: zie [README.nl.md](README.nl.md).*


## What it does

- Current temperature, feels-like, wind and humidity for one or more saved places.
- Shower timeline for the next two hours: when the current shower ends, when the next one starts, and a dry window.
- Precipitation in mm for the next hour and the next 12 hours.
- Hourly chart for 48 hours (temperature, precipitation, chance) and a 7-day forecast.
- Animated rain radar for the whole country, past hour and next hour.
- Built-in offline map of the Netherlands (municipalities, places, districts, motorways, rivers) to pick a spot by tapping, by place name or by four-digit postcode. Optional GPS button.
- Three themes in the Sly Solutions style (light, dark, nerd), reorderable and collapsible tiles.

## Privacy by design

Exactly two requests leave your device per refresh:

1. One request to **Open-Meteo** (KNMI HARMONIE model) with your coordinate **rounded to about 1 km**.
2. One request for the **national Buienradar radar image**, which is identical for everyone. The local rain nowcast is read from that image on your device.

No geocoding, no map tiles, no third-party fonts or scripts: the map, fonts and Leaflet are embedded in the file. Saved places and settings live in your browser's local storage. "Nerd mode" shows a log of every outgoing request. GPS is used only when you press the button and never leaves the device.

## Run it yourself

Download [`sly-weather.html` from the latest release](../../releases/latest) and open it in a browser, or host the `site/weather/` folder on any https server (then it is installable as a PWA and works offline).

## Build from source

```bash
python3 src/build.py
```

`src/app_template.html` holds the app (CSS, HTML, JavaScript). `build.py` inlines the fonts, Leaflet and the map data from `src/data/` and writes `sly-weather.html` and `site/weather/index.html`. Map data was prepared from CBS/Kadaster, OpenStreetMap (Overpass), GeoNames and the 4pp postcode table; the preparation scripts are not needed to build.

## Data and licenses

Weather: [Open-Meteo](https://open-meteo.com) (CC BY 4.0) · radar: [Buienradar](https://www.buienradar.nl) · map: CBS/Kadaster, © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors (ODbL), [GeoNames](https://www.geonames.org) (CC BY 4.0), [4pp](https://github.com/bobdenotter/4pp) · Leaflet (BSD-2) · Manrope and Space Mono (OFL).

App: CC BY-NC-SA 4.0, see [LICENSE](LICENSE) and [NOTICE](NOTICE) (name and logo excluded). A [Sly Solutions](https://slysolutions.nl) project.

## Feedback welcome

This is a first release and real-world feedback is the fastest way to improve it.

- **Bug or something unclear?** Open an [issue](../../issues/new?template=bug.md). A screenshot and the version number (bottom of the page) help a lot.
- **Idea?** Open an [idea](../../issues/new?template=idea.md), or comment on an existing one.
- **Like it?** A star helps others find it, and the live app at [slysolutions.nl/weather](https://slysolutions.nl/weather/) is free to share.

Ideas that keep the app as data-light as it is now are the easiest to adopt.
