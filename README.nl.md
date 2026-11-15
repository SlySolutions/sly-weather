# Sly Weather

Weer en buien voor één of meer zelfgekozen plekken in Nederland, in één HTML-bestand (`sly-weather.html`, ±900 KB), in het Nederlands en Engels, zonder je locatie te delen.

## Gebruik

Open `sly-weather.html` in een browser (ook rechtstreeks vanaf schijf, of via een simpele webserver). Eerste keer: zoom in op de ingebouwde kaart, tik je plek aan, of zoek op plaatsnaam, wijk of 4-cijferige postcode (die lijsten zitten in het bestand; bij een postcode zie je plaats en wijk); geef de plek een naam, bewaren. De knop "Details" op de kaart zet wijk- en buurtnamen, autowegen, hoofdwegen (vanaf zoom 10,5) en gemeentenamen aan of uit. De kaart zoomt tot niveau 13 (±1 px = 12 m); verder heeft met een afronding op ±1 km geen zin en wordt de vereenvoudigde lijndata zichtbaar. Plaatsen staan donker, wijken en buurten (namen die niet in de officiële woonplaatsenlijst staan) licht en cursief. Daarna haalt de app de verwachting op.

Taal: NL/EN-knop rechtsboven (standaard volgt de browsertaal). Tegels: met ▲▼ verplaats je ze, met de pijl (of een tik op de titel) klap je ze in; volgorde en inklapstand worden onthouden. In nerd mode kun je de volgorde herstellen.

Thema's: Auto, Licht, Donker en Nerd (knoppen rechtsboven). Nerd mode toont onderaan het verzoeklog: precies wat je toestel heeft verstuurd, plus ruwe waarden en instellingen (afronding, model, radar aan/uit, handmatige coördinaten, alles wissen).

## Wat verlaat je toestel

Per verversing precies twee verzoeken:

1. `api.open-meteo.com`: een op 0,01° (≈1 km) afgerond coördinaat, model `knmi_seamless` (KNMI HARMONIE via Open-Meteo). Levert actueel weer, kwartierneerslag 24 u, uurwaarden 7 dagen, dagwaarden.
2. `image.buienradar.nl`: het landelijke radarbeeld (24 beelden van 5 minuten: afgelopen uur en komend uur) als één sprite. Dit verzoek is voor iedereen identiek. De buienverwachting voor jouw plek wordt uit de pixels op je eigen toestel afgelezen.

De GPS-knop (alleen in de kiesmodus) vraagt de positie aan het toestel en zet de stip erop, afgerond zoals een tik; de positie verlaat het toestel niet. Browsers staan locatie alleen toe via https of een app-schil; bij een lokaal geopend bestand legt de app uit waarom het niet werkt. De knop "Mijn plek" zoomt naar je opgeslagen plek.

## Bronnen

- Open-Meteo (CC BY 4.0), KNMI-model
- Buienradar, landelijk radarbeeld `RadarMapRainNL` 550×512; hoekpunten N 54,75 / Z 49,41 / W 0 / O 10 (Mercator), geijkt met `src/radar_ijking.py`
- Kaart: CBS/Kadaster gemeente- en provinciegrenzen 2025 via cartomap.github.io (vereenvoudigd, 3 decimalen); 7484 namen: plaatsen uit GeoNames (CC BY 4.0) en de 4pp-woonplaatsenlijst, plus 3909 wijken en buurten (OSM place=suburb/quarter/neighbourhood); een naam geldt als plaats als hij in de officiële woonplaatsenlijst staat, anders als wijk; 4077 PC4-postcodecentroïden uit 4pp (github.com/bobdenotter/4pp, afgeleid van CBS); snelwegen (met A-nummer), autowegen (N), hoofdwegen (primary, vanaf zoom 10,5) en drukke binnenwegen (secondary, vanaf zoom 11,5), grote rivieren en kanalen uit OpenStreetMap via Overpass (© OpenStreetMap-bijdragers, ODbL; ontdubbeld op één rijbaan, vereenvoudigd tot ±60 m en opgeslagen als polyline-tekst). Kaartdata samen ±520 KB; bouwscripts staan in `src/` niet, de ruwe downloads (±150 MB) zijn weggegooid.
- Leaflet 1.9.4 (ingebakken), lettertypen Manrope en Space Mono (ingebakken)

## Opnieuw bouwen

```
python3 src/build.py
```

Bewerk `src/app_template.html` (alle code en stijl staan daar), bouw opnieuw, klaar.

## Live op slysolutions.nl/weather

Sinds 15 november 2026 draait de app op <https://slysolutions.nl/weather/> (map `public_html/weather` op de cPanel-hosting, los van de rest van de site). De uploadmap staat in `site/weather/`: `index.html` (de gebouwde app, `build.py` schrijft hem daar ook heen), `manifest.webmanifest`, `sw.js` (service worker: pagina netwerk-eerst, offline uit cache; weerdata wordt nooit gecachet), vier iconen, `.htaccess`. Nieuwe versie uitrollen: `python3 src/build.py`, daarna alleen `index.html` opnieuw uploaden (de service worker haalt hem bij het volgende bezoek op). Bij wijzigingen aan sw.js zelf de cachenaam `sly-weather-v1` ophogen.

Bezoek tellen zonder tracking: in cPanel onder Metrics → *Visitors* (laatste hits, filter op `/weather/`) en *Awstats* (dagelijks bijgewerkt, pagina's per dag/maand). Dat zijn serverlogs, geen scripts of cookies in de app.

## Naar Android

Het bestand is bedoeld om later in een WebView-schil te zetten, bijvoorbeeld met Capacitor:

```
npm init @capacitor/app   # kies een naam, zet sly-weather.html als index.html in de www-map
npx cap add android
npx cap open android      # bouw de APK in Android Studio
```

Permissies: `INTERNET`, en `ACCESS_FINE_LOCATION` alleen als je de GPS-knop wilt laten werken. Geen Google-diensten. Op een eigen https-domein is het bestand meteen als PWA op het beginscherm te zetten.

## Bekende beperkingen

- De intensiteit uit de radarpixels is een schatting op kleur (licht/matig/zwaar); de millimeters komen van Open-Meteo.
- Het "nu"-beeld in de radarsprite is aangenomen als beeld 13 van 24 (12 terug, 12 vooruit). Controleer dit bij echte regen in nerd mode; afwijking is hooguit 5 minuten.
- De ingebouwde kaart dekt alleen Nederland. Daarbuiten: coördinaten handmatig invullen in nerd mode.
- Wegen en rivieren zijn vereenvoudigd tot ±60 m en tonen één rijbaan; de A10-ring en knooppunten zijn daardoor schematisch. Plaatsnamen en postcodecentroïden zijn nauwkeurig genoeg voor de afronding van ±1 km.
- Officiële KNMI-waarschuwingen zijn vanuit een los HTML-bestand niet op te halen (KNMI vraagt een API-sleutel, MeteoAlarm staat geen browserverzoeken toe); in een app-schil of via een eigen domein kan dat wel.
- Postcodes zijn op 4 cijfers (PC4-centroïde, ±1 km). De volledige PC6-tabel (±460.000 regels) zou het bestand meerdere MB groter maken en voegt met de afronding op ±1 km niets toe; tik na het zoeken desnoods de stip nog even goed.

## Achtergrond

- [docs/BESLISSINGEN.md](docs/BESLISSINGEN.md): alle ontwerpkeuzes met reden en afgewezen alternatief.
- [docs/GEDACHTEGANG.md](docs/GEDACHTEGANG.md): hoe het project is bedacht en gegroeid, wat misging, hoe je verder bouwt.
