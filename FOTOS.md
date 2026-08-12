# Foto's — shotlijst voor DS Comfort

De site is **rond fotografie gebouwd**. Elk beeldkader heeft al de juiste
verhouding en plaats; er moet enkel nog een bestand in.

## Hoe u een foto plaatst

Elk kader ziet er in de HTML zo uit:

```html
<figure class="photo photo--4x3" data-shot="Foto: split-unit in een lichte woonkamer">
  <!-- <img src="assets/img/photos/airco.jpg" alt="Airco split-unit aan de wand in een woonkamer"> -->
</figure>
```

Twee dingen doen:

1. Zet het bestand in `assets/img/photos/`.
2. Haal de `<!--` en `-->` rond de `<img>`-regel weg.

Meer niet. Het kader, het bijschrift en de tussenoplossing verdwijnen dan
automatisch — dat is in de CSS geregeld met `.photo:has(img)`.

Vergeet de `alt`-tekst niet: die beschrijft wat er te zien is, voor
slechtziende bezoekers en voor Google.

---

## De lijst

Op volgorde van belang. De eerste vijf dragen de site; de rest is bonus.

| # | Bestand | Verhouding | Waar | Wat we willen zien |
|---|---|---|---|---|
| 1 | `hero.jpg` | 16:9 liggend, min. 1920px breed | Homepage, achtergrond | Een buitenunit netjes tegen de gevel van een gewone Vlaamse woning. Late namiddag, warm licht. Ruimte links in beeld, want daar staat de tekst overheen. |
| 2 | `airco.jpg` | 4:3 | Homepage, dienstenkaart | Split-unit aan de wand in een lichte, opgeruimde woonkamer. Toont dat het toestel niet stoort. |
| 3 | `warmtepomp.jpg` | 4:3 | Homepage, dienstenkaart | Buitenunit van een warmtepomp in een tuin of tegen een zijgevel, met wat groen errond. |
| 4 | `aan-het-werk.jpg` | 3:2 | Homepage, "Waarom DS Comfort" | Iemand van DS Comfort aan het werk bij een klant. Gezicht mag in beeld — dit is de belangrijkste vertrouwensfoto van de site. |
| 5 | `onderhoud.jpg` | 4:3 | Homepage, dienstenkaart | Handen die een filter of binnenunit nakijken. Van dichtbij. |
| 6 | `warm-water.jpg` | 4:3 | Homepage, dienstenkaart | Boiler of buffervat in een berging of technische ruimte. |
| 7 | `hero-airco.jpg` | 16:9, min. 1920px | Kop airco-pagina | Interieur met een split-unit, ruim genomen. |
| 8 | `airco-detail.jpg` | 4:3 | Airco-pagina | Binnenunit van dichtbij: strak gemonteerd, waterpas, geen zichtbare leidingen. |
| 9 | `buitenunit.jpg` | 4:5 staand | Airco-pagina | Buitenunit met de leidingen netjes weggewerkt. Dít is wat u van de concurrentie onderscheidt. |
| 10 | `hero-warmtepomp.jpg` | 16:9, min. 1920px | Kop warmtepompen | Warmtepomp bij een woning, ruim genomen. |
| 11 | `warmtepomp-buiten.jpg` | 3:2 | Warmtepompen | Buitenunit in gebruik, tegen een gevel. |
| 12 | `boiler.jpg` | 4:5 staand | Warmtepompen, warm water | Boiler met de aansluitingen verzorgd afgewerkt. |
| 13 | `zwembad.jpg` | 16:9 | Warmtepompen, zwembad | Zwembad in een tuin. Mag zonder mensen. |
| 14 | `hero-onderhoud.jpg` | 16:9, min. 1920px | Kop onderhoud | Technicus bij een installatie. |
| 15 | `onderhoud-detail.jpg` | 4:3 | Onderhoud | Filter die gereinigd wordt, of meetapparatuur op het circuit. |
| 16 | `zaakvoerder.jpg` | 4:5 staand | Over ons | **Sterk aanbevolen.** Portret van de zaakvoerder, bij voorkeur ter plaatse bij een klant en niet in studio. Bij een bedrijf dat draait om "altijd dezelfde vakman" is een gezicht enorm overtuigend. |
| 17 | `regio.jpg` | 4:3 | Homepage + Over ons | Bestelwagen met logo, of een herkenbaar straatbeeld uit Leuven of Heverlee. |

Ontbrekende foto's zijn geen probleem: die kaders tonen gewoon de
tussenoplossing verder. U kunt dus perfect starten met de eerste vijf en de
rest later aanvullen.

---

## Praktische tips voor het fotograferen

Een moderne smartphone volstaat ruimschoots. Wat wél uitmaakt:

- **Daglicht.** Fotografeer overdag, en zet binnen de lampen uit. Gemengd licht
  (daglicht + gele lamp) geeft vieze kleuren.
- **Ruim ademruimte laten.** Neem breder dan u denkt nodig te hebben. De site
  snijdt zelf bij naar de juiste verhouding; te krap kan niet bijgesneden worden.
- **Recht houden.** Verticale lijnen — deurstijlen, hoeken — recht in beeld.
  Scheve foto's van een strak gemonteerd toestel werken tegen u.
- **Opruimen vóór de foto.** Kabels, gereedschap en verpakkingen uit beeld.
- **Toestemming vragen** aan de klant vóór u in zijn woning fotografeert, zeker
  als het herkenbaar is. Kort schriftelijk (een berichtje volstaat) is het veiligst.
- **Liggend fotograferen**, behalve voor de drie waar hierboven "staand" staat.

## Als er voorlopig geen eigen foto's zijn

Dan zijn er twee tussenwegen:

1. **Beeldbank van de fabrikant.** Daikin en Panasonic stellen hun installateurs
   doorgaans productfoto's en sfeerbeelden ter beschikking. Vraag ernaar bij uw
   invoerder — dat is gratis en de rechten zijn geregeld.
2. **Stockfotografie.** Pexels en Unsplash zijn gratis en vrij voor commercieel
   gebruik. Zoek op *"air conditioner living room"*, *"heat pump house"*,
   *"hvac technician"*. Let er wel op dat u een samenhangende set kiest: dezelfde
   lichtsfeer en hetzelfde kleurgevoel, anders valt het uiteen.

Echte foto's van eigen werk blijven veruit het overtuigendst. Een bezoeker die
uw eigen installatie in een Leuvense woning ziet staan, gelooft u meteen; bij
een stockfoto van een Amerikaanse keuken gebeurt dat niet.
