# Sly Weather — beslissingenlogboek

Alle keuzes van betekenis, met de reden en wat er is afgewezen. Datum: 14–15 november 2026, versie 1.0.
Gebruik dit als je iets wilt veranderen: elke regel zegt waarom het nu zo is, zodat je weet wat je loslaat.

| # | Keuze | Waarom | Afgewezen alternatief |
|---|---|---|---|
| 1 | **Eén HTML-bestand**, geen server, geen build-afhankelijkheden bij gebruik | Maximale privacy en eenvoud: niets om te hosten, te lekken of te onderhouden; opent overal, ook offline vanaf schijf. | App met backend (ziet alle gebruikers), framework-build (zwaarder, meer afhankelijkheden). |
| 2 | **Locatie kiezen op een ingebouwde kaart**, niet via GPS als standaard | GPS en geocoding verraden waar je bent; een tik op een kaart deelt niets. Afronden op 0,01° (±1 km) is genoeg voor weer. | GPS-eerst (gebruikelijk), adres intypen met geocoding-dienst (stuurt je adres naar derden). |
| 3 | **Coördinaat afgerond op 0,01°** naar Open-Meteo, instelbaar naar 0,1° | Een weermodel heeft ±2 km resolutie; preciezer sturen voegt niets toe en verraadt meer. | Exacte coördinaat. |
| 4 | **Open-Meteo met KNMI HARMONIE-model** (`knmi_seamless`) | Gratis, geen sleutel, CORS open, Nederlands model van KNMI; één verzoek levert alles (nu, per kwartier, per uur, per dag). | KNMI Open Data rechtstreeks (API-sleutel nodig, geen CORS), Buienradar-API (niet publiek), commerciële API's. |
| 5 | **Landelijk Buienradar-radarbeeld** voor radar én lokale buienverwachting | Het beeld is voor iedereen identiek, dus het ophalen zegt niets over jou. De lokale verwachting lees ik op het toestel uit de pixels op jouw plek. | Buienradar's per-locatie "buienverwachting"-feed (stuurt je coördinaat; niet publiek). |
| 6 | **Radar-georeferentie geijkt op provinciegrenzen** (N 54,75 / Z 49,41 / W 0 / O 10) | Buienradar publiceert geen hoekpunten; ijken op bekende omtrekken gaf 84% overlap (IoU), ruim genoeg voor ±1 km. | Gokken op standaard-bounds. |
| 7 | **Precies twee verzoeken per verversing**, zichtbaar in nerd mode | Controleerbaar privacybeleid: de gebruiker kan zelf zien wat zijn toestel verlaat. | Meer bronnen (waarschuwingen, luchtkwaliteit) ten koste van extra verzoeken; later optioneel. |
| 8 | **Alles ingebakken**: lettertypen, Leaflet, kaartdata, logo | Geen enkel verzoek naar Google Fonts, CDN's of tegelservers; ook offline compleet. Prijs: ±0,9 MB bestand. | Externe CDN's (sneller eerste keer, maar extra partijen die je IP zien). |
| 9 | **Geen kaarttegels** (OSM/Google), wel eigen vectordata | Tegels verraden per tegel waar je kijkt. Eigen data: gemeenten (CBS), wegen/rivieren/wijken (OpenStreetMap), plaatsen (GeoNames, 4pp). | Tegellaag als opt-in (overwogen, niet gebouwd). |
| 10 | **Natural Earth-wegen vervangen door OpenStreetMap** (v3.2) | Natural Earth is 1:10 mln: bij inzoomen lagen snelwegen kilometers mis (A2 bij Eindhoven dwars door de stad). | Natural Earth houden met minder zoom. |
| 11 | **Plaats vs. wijk op de officiële woonplaatsenlijst** (BAG via 4pp) | GeoNames-codes bleken onbetrouwbaar (wijken als plaats). Woonplaatsenlijst is gezaghebbend en volledig. | GeoNames-featurecodes. |
| 12 | **OSM-buurten erbij, buurtschappen niet** | Gebruiker miste wijken zoals Genderbeemd. Buurtschappen (6600) kosten 150 KB en voegen weinig toe boven de woonplaatsenlijst. | Alles meenemen (bestand >1 MB). |
| 13 | **Lijnen als polyline-tekst** (factor 1000) in plaats van JSON-getallen | 3–4 bytes per punt in plaats van 14; maakte hoofd- en binnenwegen betaalbaar binnen de omvang. | Gewone JSON (160 KB → 730 KB). |
| 14 | **Maximale zoom 13** | Daar is 1 px ≈ 12 m; verder inzoomen heeft met ±1 km afronding geen zin en toont de vereenvoudiging van de lijndata. | Zoom 14+ met nog zwaardere data. |
| 15 | **Postcode op 4 cijfers**, geen letters | PC6-tabel is 460.000 regels (meerdere MB); PC4-centroïde is ±1 km, gelijk aan de afronding. | PC6 inbakken. |
| 16 | **Zoeken op plaats/postcode volledig lokaal** | Geen geocoding-verzoek; lijst zit in het bestand. | Nominatim/Google geocoding. |
| 17 | **GPS-knop: eerst weg, toen terug met uitleg** | Werkte niet vanuit lokaal geopend bestand (browsers eisen https). Na hosting via https wel zinvol; de app legt nu uit waarom het faalt (geen https, geweigerd, geen fix, Android-machtiging bij Firefox Focus). | Geen GPS (te beperkend zodra de app online staat). |
| 18 | **Stijl van slysolutions.nl**, drie thema's (licht/donker/nerd), geen standaardlook | Herkenbaarheid als Sly Solutions-project; nerd mode past bij de doelgroep en toont de verzoeklog. | Generieke app-styling. |
| 19 | **Tegels verplaatsbaar en inklapbaar**, volgorde onthouden | Gebruiker bepaalt wat bovenaan staat; op desktop twee kolommen. | Vaste volgorde. |
| 20 | **Radar in eigen Leaflet-laag (z 450)** | In de standaardlaag tekende de canvas-renderer de gemeentevlakken óver het radarbeeld. | Volgorde-trucs met bringToFront (werkten niet). |
| 21 | **Labels met botsingscontrole**, plaats donker / wijk licht-cursief, snelwegnummers eerst | Zonder botsingscontrole was de kaart onleesbaar. Een CSS-fout (position:relative) had labels zelfs verschoven. | Alle labels tonen. |
| 22 | **Hosting op eigen domein in submap /weather/**, Engelse padnaam | Gebruiker wilde eigen site en Engels adres; https maakt installeren (PWA) en GPS mogelijk; serverlogs tellen bezoek zonder tracking. | GitHub Pages (geen bezoekersstatistiek), los bestand downloaden (geen icoon, geen updates, geen GPS). |
| 23 | **PWA-bestanden**: manifest, service worker (netwerk-eerst, weerdata nooit gecachet), iconen met merkteken | Installeerbaar op het beginscherm, offline bruikbaar, nieuwe versie komt direct door. | Capacitor/Play Store (zwaarder; later mogelijk via Bubblewrap). |
| 24 | **Broncode openbaar op GitHub**, licentie **CC BY-NC-SA 4.0**, naam en logo uitgesloten | Zichtbaarheid, sterren, issues als feedbackkanaal, releases met downloadteller. Licentie: delen en verbeteren mag met naamsvermelding, niet commercieel, verbeteringen terug. Kopiëren is technisch toch niet te voorkomen; dit regelt de voorwaarden. | Alle rechten voorbehouden (ontmoedigt feedback), MIT (laat commercieel hergebruik toe). |
| 25 | **Commits op naam van Sly Solutions**, gekoppeld aan het GitHub-profiel via het anonieme GitHub-adres | Eén auteur, geen e-mailadres zichtbaar, wel groene activiteit op het profiel. Repository één keer opnieuw aangemaakt om een gecachte oude bijdrager definitief kwijt te raken. | — |
| 26 | **Waarschuwingen (KNMI/MeteoAlarm) nog niet** | Vanuit een los HTML-bestand niet ophaalbaar (API-sleutel / geen CORS). Lokaal berekende attentiepunten uit Open-Meteo-data zijn wel haalbaar zonder extra verzoek: geplande volgende stap. | Eigen proxy (extra server). |
| 27 | **Versienummer in het bestand** (voettekst, meta-tag, nerd mode) en als Release-tag | Nodig voor foutmeldingen van gebruikers en voor de downloadteller per versie. | — |

## Spelregels die uit deze keuzes volgen

- Elke nieuwe functie moet de vraag beantwoorden: *welk extra verzoek verlaat het toestel, en wat zegt dat over de gebruiker?* Liefst nul.
- Bestand liefst onder 1 MB houden; nieuwe kaartdata altijd eerst vereenvoudigen en compact coderen.
- Niets van derden tijdens gebruik laden (fonts, scripts, tegels), behalve de twee databronnen.
- Nieuwe versie = versienummer ophogen, `python3 src/build.py`, `index.html` uploaden naar `public_html/weather`, commit, push, Release met het bestand.
- Geen persoonlijke gegevens in repository, commits of profiel.
