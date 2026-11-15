# Sly Weather — ontwerp en gedachtegang

Dit document legt uit hoe het project is bedacht en gegroeid, welke problemen onderweg opdoken en hoe die zijn opgelost, en hoe je verder bouwt of een volgend project op dezelfde manier aanpakt. Het hoort bij `BESLISSINGEN.md` (de korte lijst met keuzes) en `README.nl.md` (gebruik en opbouw).

---

## 1. De vraag

Een weer-app voor Android, maar eerst als los HTML-bestand, met voor een eigen plek: temperatuur en neerslag nu, een tijdlijn en grafiek per uur, hoe lang de huidige bui duurt en wanneer de volgende komt, millimeters voor het komende uur en 12 uur, een meerdaagse verwachting, en een kaart waarop de neerslag beweegt.

De eis die alles bepaalde kwam direct daarna: **zo min mogelijk data delen, liever geen.** Vanaf dat moment was dit geen weer-app met wat privacy, maar een privacy-oefening die toevallig over weer gaat. Elke functie is daarna beoordeeld op de vraag: wat verlaat het toestel, en wat zegt dat over de gebruiker?

## 2. Eerst denken, dan bouwen

Voordat er code was, is uitgezocht welke bronnen bestaan en wat ze van je weten:

- **Weermodellen.** Open-Meteo bleek de enige bron die gratis is, geen sleutel vraagt, vanuit een browser bereikbaar is (CORS) en het Nederlandse KNMI-model aanbiedt. Je stuurt één coördinaat. Dat is het enige persoonlijke dat de deur uitgaat, en dat kon worden afgerond.
- **Radar.** Buienradar publiceert een landelijk radarbeeld als reeks van 24 plaatjes (12 terug, 12 vooruit, per 5 minuten). Cruciaal inzicht: dat beeld is voor iedereen hetzelfde. Wie het ophaalt, verraadt niets. De lokale buienverwachting ("over 20 minuten droog") kan het toestel zelf uit de pixels op jouw plek lezen. Zo ontstond de combinatie: één algemeen plaatje, lokaal uitgelezen.
- **Locatie.** GPS was het voor de hand liggende antwoord en tegelijk het grootste lek. De oplossing: een kaart in de app waarop je je plek aantikt, afgerond op ongeveer een kilometer. Dat vraagt een kaart zonder tegelserver, want tegels verraden per tegel waar je kijkt. Dus: eigen vectordata van Nederland inbakken.
- **Waarschuwingen.** KNMI vraagt een API-sleutel, MeteoAlarm weigert browserverzoeken. Geparkeerd, met als route lokaal berekende attentiepunten uit de data die er al is.

Het resultaat van deze fase was een helder model: **twee verzoeken per verversing, verder niets.** Alles daarna is uitvoering van dat model.

## 3. Hoe de app in elkaar zit

Eén bestand (`sly-weather.html`), gebouwd uit `src/app_template.html` door `build.py`, dat lettertypen, Leaflet, kaartdata en logo erin plakt. Geen framework; gewone HTML, CSS en JavaScript.

- **Data ophalen.** `refreshAll()` doet het Open-Meteo-verzoek (huidig weer, kwartieren voor 24 uur, uren voor 7 dagen, dagen) met tien minuten cache in localStorage, en `loadRadar()` haalt de radarsprite op en leest hem in een canvas.
- **Buienanalyse.** `sampleRadar()` leest per radarbeeld een 3×3-blokje pixels op jouw plek en vertaalt kleur naar intensiteit; `buildSeries()` plakt die 5-minutenreeks aan de kwartieren van het model; `analyse()` leidt daaruit af of het nu regent, wanneer het stopt, wanneer de volgende bui komt en hoe lang die duurt; `dryWindow()` zoekt het langste droge venster.
- **Kaart.** Leaflet zonder tegellaag, met ingebakken gemeente- en provinciegrenzen (CBS), snelwegen, autowegen, hoofd- en binnenwegen, rivieren en kanalen (OpenStreetMap), plaatsen en wijken (GeoNames, woonplaatsenlijst, OSM-buurten) en postcodecentroïden (4pp). De radar ligt als beeld in een eigen laag boven het land. Labels worden per zoomniveau geselecteerd en botsen niet.
- **Kiezen van een plek.** Tikken op de kaart, zoeken op plaatsnaam of postcode (lokale lijst), of de GPS-knop (alleen op verzoek, alleen werkend via https). Alles wordt afgerond en alleen lokaal bewaard; meerdere plekken mogelijk.
- **Presentatie.** Tegels (nu, buien 2 uur, grafiek 48 uur, radar, komende dagen) die je kunt verplaatsen en inklappen; drie thema's in de stijl van slysolutions.nl; Nederlands en Engels; nerd mode met verzoeklog, ruwe waarden en instellingen.
- **Hosting.** Als PWA op slysolutions.nl/weather: manifest, service worker (pagina netwerk-eerst, weerdata nooit gecachet), iconen. Daardoor installeerbaar, offline bruikbaar, en nieuwe versies komen direct door.

## 4. Wat onderweg misging en wat het leerde

Dit zijn de momenten die het project beter maakten. Ze zijn bijna allemaal door gebruik op een echte telefoon ontdekt, niet in de testbrowser.

1. **Radar achter de kaart.** De regen was alleen boven zee zichtbaar. Oorzaak: Leaflet tekende de gemeentevlakken op een canvas dat boven het radarbeeld lag. Oplossing: eigen laag voor de radar. Les: test met echte regen; droog weer verbergt dit soort fouten.
2. **Labels op de verkeerde plek.** Plaatsnamen stonden tientallen pixels naast hun plek en de kaart oogde druk. Oorzaak: één CSS-regel (`position: relative`) die alle labels in de documentstroom onder elkaar zette. Dit zat er al twee versies in zonder dat het opviel. Les: meet posities na met code, vertrouw niet alleen op een schermafbeelding die "ongeveer goed" lijkt.
3. **Snelwegen die er niet lagen.** Natural Earth is bedoeld voor wereldkaarten; bij inzoomen liep de A2 dwars door Eindhoven. Oplossing: OpenStreetMap-data via Overpass, geknipt op Nederland, dubbele rijbanen ontdubbeld, vereenvoudigd tot ±60 m, en als compacte polyline-tekst opgeslagen zodat ook hoofd- en binnenwegen pasten. Les: controleer een databron op de schaal waarop je hem toont, niet op de schaal waarop je hem downloadt.
4. **Plaats of wijk.** GeoNames-codes zetten wijken als plaats neer. De officiële woonplaatsenlijst (BAG) bleek de juiste scheidslijn; buurten kwamen uit OpenStreetMap. Les: voor "wat is officieel" altijd de overheidsbron, voor "wat noemen mensen het" de gemeenschapsbron.
5. **GPS die niet werkte.** Browsers geven alleen locatie vrij op https, localhost of in een app-schil. Een bestand dat op Android vanuit Downloads opent (`content://`) valt daarbuiten en krijgt stilzwijgend "geweigerd". Firefox Focus voegde daar een tweede laag aan toe: de site-vraag verschijnt wel, maar als de app Focus zelf op Android geen locatierecht heeft, meldt hij toch "geweigerd". Oplossing: hosting via https, en meldingen die precies zeggen wat er aan de hand is. Les: een knop die zwijgend faalt is erger dan geen knop; leg de oorzaak uit op de plek waar de gebruiker kijkt.
6. **Bestand werd te groot.** Elke verbetering van de kaart kostte kilobytes. Compact coderen (polyline-tekst, tab-gescheiden plaatsen, lat/lon als gehele getallen) bracht de lijndata van 730 KB terug naar 160 KB. Les: eerst comprimeren, dan pas uitbreiden.
7. **Bestandsoverdracht naar hosting.** Vanuit het browserpaneel kon cPanel geen lokale bestanden zien, en de cPanel-pagina mocht geen lokale server benaderen tot de browser daarvoor toestemming kreeg. Daarna werkte uploaden via cPanel's eigen API. Les: hosting-paneel plus browser-API is een werkbare route zonder FTP-wachtwoorden rond te sturen.
8. **Zichtbaarheid op GitHub.** Een overschreven commit bleef in GitHub's cache zichtbaar als bijdrager. Alleen de repository verwijderen en opnieuw aanmaken maakte het definitief schoon. Les: begin een repository meteen met de juiste identiteit; achteraf repareren is omslachtiger dan vooraf instellen.

## 5. Wat bewust níet is gedaan

- Geen kaarttegels, ook niet als optie: één tegelverzoek verraadt meer dan het hele weermodel.
- Geen geocoding-dienst; daarom een ingebakken zoeklijst.
- Geen PC6-postcodes (bestand zou meerdere MB groeien zonder winst boven de afronding).
- Geen buurtschappen op de kaart (150 KB voor weinig extra oriëntatie).
- Geen analytics, cookies of trackers, ook geen "privacyvriendelijke": serverlogs volstaan om bezoek te tellen.
- Geen Play Store op dag één: de PWA doet hetzelfde zonder account, kosten of reviewproces. Bubblewrap kan later een Store-pakket van de PWA maken.
- Geen officiële weerwaarschuwingen zolang dat een sleutel of proxy vraagt.

## 6. Hoe je verder bouwt

**Een nieuwe versie uitbrengen**

1. Pas `src/app_template.html` aan; verhoog `APP_VERSION` en de meta-tag `version`.
2. `python3 src/build.py` schrijft `sly-weather.html` en `site/weather/index.html`.
3. Test lokaal (een simpele webserver in de map volstaat) en op een telefoon via de live URL.
4. Upload alleen `index.html` naar `public_html/weather` (cPanel → File Manager). Verander je `sw.js`, verhoog dan de cachenaam erin.
5. Commit en push naar GitHub; maak een Release met hetzelfde versienummer en `sly-weather.html` als bijlage.

**Kaartdata vernieuwen**

De data in `src/data/` is in november 2026 gemaakt uit: cartomap (gemeenten/provincies), GeoNames NL, 4pp (postcodes en woonplaatsen) en Overpass-query's op OpenStreetMap (motorway/trunk/primary/secondary, waterway=river/canal op naam, place=suburb/quarter/neighbourhood). De verwerkingsstappen: knippen op de gemeentepolygonen, dubbele rijbanen ontdubbelen op een raster van ±150 m, Douglas-Peucker-vereenvoudiging (0,0007°), polyline-codering met factor 1000. Overpass is vaak overbelast; probeer meerdere spiegels en stuur een User-Agent mee.

**Kandidaten voor de volgende versies, in volgorde van waarde per inspanning**

1. *Attentiepunten* uit de bestaande Open-Meteo-data met KNMI-drempels: gladheid, hitte, windstoten, onweer, mist, zware regen, zonkracht. Nul extra verzoeken.
2. *Zonsopkomst/-ondergang, UV-index, luchtvochtigheid per uur* (zit al in de data of één veld extra).
3. *Buienradar-weerbericht* (landelijke tekst, één extra verzoek dat niets over jou zegt) en dichtstbijzijnd meetstation als "gemeten nu".
4. *Compacte widgetmodus* en, in een app-schil, een melding "bui over 10 minuten".
5. *Luchtkwaliteit of pollen* via Open-Meteo Air Quality met hetzelfde afgeronde coördinaat.
6. *Officiële waarschuwingen* zodra er een app-schil is (geen CORS-beperking) of een eigen minimale proxy op het eigen domein.

## 7. Wat dit project leert voor een volgend project

- **Begin met de harde eis**, niet met de functielijst. Hier was dat "geen data delen"; daaruit volgden bijna alle keuzes vanzelf.
- **Zoek eerst naar bronnen die voor iedereen hetzelfde zijn.** Alles wat per gebruiker verschilt, is een lek; alles wat algemeen is, kun je lokaal personaliseren.
- **Maak het verifieerbaar.** Nerd mode met een verzoeklog bewijst de privacybelofte beter dan een tekst.
- **Eén bestand dwingt tot discipline** in omvang en afhankelijkheden, en levert een product dat overal werkt.
- **Test op het echte apparaat en in echte omstandigheden** (regen, andere browser, bestand uit Downloads). De meeste fouten hier kwamen daar vandaan.
- **Hosten via https op eigen domein** is de goedkoopste "app": installeerbaar, offline, eigen statistieken, geen store.
- **Zet identiteit, licentie en naamgeving vóór de eerste publicatie goed**; opnieuw beginnen is de enige manier om publieke sporen echt te wissen.
- **Houd een beslissingenlogboek bij** zoals `BESLISSINGEN.md`: het voorkomt dat je later een goede keuze terugdraait omdat je de reden vergeten bent.
