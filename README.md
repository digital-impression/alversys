# DS Comfort — website

Een op maat ontworpen website voor **DS Comfort bv**, erkend koeltechnisch bedrijf
uit Heverlee, gespecialiseerd in airconditioning en warmtepompen in de regio Leuven.

Statische HTML, CSS en JavaScript. Geen framework, geen buildstap, geen
afhankelijkheden. Upload de map en de site draait.

---

## 1. Het ontwerp in het kort

### Uitgangspunt: comfort in huis, niet techniek

Dit is een website over aangenaam wonen, niet over koeltechniek. Licht,
fotogedreven en vlot leesbaar. Blauw voor de koelkant, warm amber voor de
verwarmingskant, en verder zo veel mogelijk wit en lucht.

| Kleur | Rol |
|---|---|
| **Blauw** (`#1476B7`) | koelen, airco, links, accenten |
| **Amber** (`#B45A12`) | verwarmen, knoppen, alles wat om actie vraagt |
| **Marine** (`#0B2032`) | hero-overlay, CTA-band en voettekst |
| **Wit / zacht grijsblauw** (`#FFF` / `#F4F8FA`) | de grond waarop alles staat |

De amberknop is bewust een tint donkerder dan de accentkleur: wit op het lichtere
amber haalde maar 3,45:1 en zakte daarmee onder de leesbaarheidsdrempel.

### Typografie

- **Figtree** — koppen, knoppen en labels. Vriendelijk, stevig en zeer leesbaar
  op grote formaten.
- **Source Sans 3** — lopende tekst. Getekend om te lezen, ook op kleine maten.

Basisgrootte 18px met regelafstand 1,7, en een vlakkere typeschaal dan
gebruikelijk. Alle tekst haalt **WCAG AA** — met alfatransparantie meegerekend.

### Beeld

De site is **rond fotografie gebouwd**: elk beeldkader heeft al de juiste
verhouding en plaats. Zolang er nog geen foto in zit, toont het kader een
verzorgde tussenoplossing met de naam van de gewenste opname.

Zie **[FOTOS.md](FOTOS.md)** voor de volledige shotlijst, de bestandsnamen en
hoe u een foto plaatst (twee handelingen per beeld).

### Positionering

De sterkste boodschap van DS Comfort stond op de oude site verstopt als een
excuus: *"wij herstellen en onderhouden enkel installaties die wij zelf geplaatst
hebben."* Hier is dat een **verkoopargument** geworden, met een eigen pagina. Het
verklaart meteen waarom er maar twee merken zijn en waarom het werkgebied beperkt
blijft: één consistent verhaal over kwaliteit boven volume.

---

## 2. Structuur

```
index.html                  Home
airco.html                  Airconditioning
warmtepompen.html           Warmtepompen (+ #sanitair, #hybride, #zwembad)
onderhoud.html              Onderhoud & herstelling
over-ons.html               Over ons (+ #werkgebied)
contact.html                Contact & offerteformulier
privacybeleid.html          Privacybeleid
algemene-voorwaarden.html   Algemene voorwaarden  ← nog aan te vullen, zie §5
404.html                    Foutpagina

assets/css/style.css        Volledig ontwerpsysteem (alle kleuren, maten, componenten)
assets/js/main.js           Menu, accordeon, scroll-reveal, formuliervalidatie
assets/img/icons.svg        Icoonset (wordt in elke pagina ingevoegd)
assets/img/photos/          Uw foto's — zie FOTOS.md
assets/img/favicon.svg      Favicon
assets/img/og-image.svg     Bron van de deelafbeelding
assets/img/og-image.png     Deelafbeelding voor Facebook/LinkedIn/WhatsApp

_partials/                  Gedeelde blokken (header, footer, CTA)
build.py                    Giet die blokken in elke pagina
sitemap.xml, robots.txt     SEO
FOTOS.md                    Shotlijst en instructies voor de fotografie
```

### De gedeelde blokken

Header, footer en de CTA-balk staan in `_partials/` zodat ze niet op negen plaatsen
uiteen gaan lopen. Na een aanpassing daar:

```bash
python3 build.py
```

Het script is idempotent — het mag zo vaak draaien als u wil. **U hoeft het niet te
gebruiken:** elke HTML-pagina is volledig zelfstandig, en wie liever rechtstreeks in
de HTML werkt, laat het script gewoon links liggen.

---

## 3. Lokaal bekijken

```bash
python3 -m http.server 8000
```

Daarna → <http://localhost:8000>

---

## 4. Publiceren

De site is puur statisch en draait overal: Netlify, Vercel, Cloudflare Pages,
GitHub Pages, of gewoon via FTP naar de huidige host.

Eén ding om te controleren bij de overstap van de bestaande site: de oude
adressen waren `/airco`, `/warmtepomp` en `/contact` (zonder `.html`). Zet daarvoor
een 301-redirect op, zodat bestaande links en zoekresultaten blijven werken:

| Oud | Nieuw |
|---|---|
| `/airco` | `/airco.html` |
| `/warmtepomp` | `/warmtepompen.html` |
| `/contact` | `/contact.html` |

Op Netlify volstaat een bestand `_redirects`:

```
/airco       /airco.html        301
/warmtepomp  /warmtepompen.html 301
/contact     /contact.html      301
```

---

## 5. Nog te doen vóór livegang

Dit zijn de punten die alleen DS Comfort zelf kan afwerken.

### 5.1 Het contactformulier aansluiten — *verplicht*

De site is statisch en heeft dus geen server om formulieren te verwerken. Op dit
moment staat in `contact.html`:

```html
action="https://formspree.io/f/VERVANG-DIT-DOOR-UW-EIGEN-ID"
```

Zolang daar `VERVANG` in staat, opent het formulier een **vooringevulde e-mail**
naar info@dscomfort.be. Dat werkt, maar het is niet ideaal.

Maak een gratis account op [Formspree](https://formspree.io) (of Basin, Web3Forms,
Netlify Forms) en vervang de hele URL door uw eigen endpoint. Het formulier
verstuurt dan zonder de pagina te verlaten en toont netjes een bevestiging.

Er zit al een verborgen anti-spamveld (`_gotcha`) in dat de meeste bots tegenhoudt.

### 5.2 Algemene voorwaarden invullen — *verplicht*

`algemene-voorwaarden.html` is een **raamwerk**, geen juridisch nagelezen document.
Overal waar `[TE BEVESTIGEN]` staat, moeten uw eigen termijnen en percentages
komen: geldigheidsduur van offertes, voorschot, betalingstermijn, garantie op
plaatsing, annuleringsvergoeding, klachtentermijn.

Hebt u al bestaande algemene voorwaarden? Plak die tekst dan gewoon in de plaats —
de opmaak past zich vanzelf aan. Laat het geheel in elk geval nog nalezen door uw
boekhouder of jurist, en verwijder daarna het gele aandachtsblok bovenaan die pagina.

### 5.3 Openingsuren bevestigen

Nergens op uw huidige site staan openingsuren, dus staat er nu
*"Werken en bezoeken op afspraak"* (footer en contactpagina). Klopt dat, dan is er
niets te doen. Wilt u wel uren tonen, laat het weten — dan zetten we ze erin, ook in
de gestructureerde gegevens voor Google.

### 5.4 Wat de site nog beter zou maken

Geen blokkers, wel de dingen die het meeste zouden opleveren:

1. **Foto's van eigen werk.** Vijf tot tien foto's van afgewerkte installaties —
   een nette buitenunit, weggewerkte leidingen, een split-unit in een leefruimte —
   zijn het krachtigste bewijs dat er bestaat. De schema's dragen de site nu
   prima, maar echte referentiefoto's zouden er een realisatiepagina bij
   verdienen.
2. **Een foto en een naam van de zaakvoerder.** Bij een eenmansbedrijf dat zijn
   hele verhaal bouwt op *"dezelfde vakman van begin tot eind"*, is een gezicht
   erbij enorm overtuigend. Op de pagina *Over ons* is daar bewust ruimte voor
   gelaten. Wij hebben bewust geen naam ingevuld die we niet konden verifiëren.
3. **Twee of drie echte Google-recensies.** De reviewsectie toont nu enkel het
   geverifieerde gemiddelde (4,4/5 uit 16 recensies). Letterlijke citaten van
   klanten zouden daar sterk bij winnen — die hebben we bewust niet verzonnen.
4. **Google Bedrijfsprofiel.** Zorg dat naam, adres en telefoonnummer daar exact
   overeenkomen met wat op de site staat. Dat is voor lokale vindbaarheid
   belangrijker dan eender welke ingreep op de site zelf.

---

## 6. Technisch

- **Toegankelijkheid** — semantische HTML, skip-link, zichtbare focusindicatie,
  correcte ARIA op menu/accordeon/formulier, alle schema's voorzien van
  `<title>` en `<desc>`, en volledige eerbiediging van `prefers-reduced-motion`.
- **SEO** — unieke titels en beschrijvingen per pagina, canonical-links,
  Open Graph, sitemap, en gestructureerde gegevens (`HVACBusiness`, `Service`,
  `FAQPage`, `ContactPage`) met adres, btw-nummer, merken, certificeringen en
  werkgebied.
- **Privacy** — geen analytics, geen trackingcookies, geen socialemediascripts.
  De enige externe verbinding zijn de lettertypen van Google Fonts; wilt u ook dat
  weg, dan kunnen die lokaal worden meegeleverd (staat zo vermeld in het
  privacybeleid).
- **Prestaties** — geen frameworks, geen fotobestanden, alle beeld is inline SVG.
- **Browsers** — alle courante browsers; de site blijft volledig leesbaar en
  bruikbaar wanneer JavaScript uitvalt.

### Iets aanpassen?

Bijna alles wat met vormgeving te maken heeft, staat bovenaan
`assets/css/style.css` in één blok met variabelen. Eén kleur daar wijzigen, past
de hele site aan.
