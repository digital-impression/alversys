# veerleborremans.be

Website voor **Veerle Borremans**, advocaat en bemiddelaar te Leuven.
Familierecht, jeugdrecht, personenrecht en strafrecht.

Statische site: HTML, CSS en een klein beetje JavaScript. Geen framework,
geen dependencies, geen cookies, geen externe verzoeken.

---

## Snel starten

```bash
python3 tools/build.py          # bouwt de HTML-pagina's + sitemap
python3 -m http.server 8000     # bekijk op http://localhost:8000
```

Openen via `file://` werkt niet volledig: de browser blokkeert dan het laden
van de lettertypes. Gebruik altijd een lokale server.

## Hoe het in elkaar zit

```
pages/            de inhoud van elke pagina (dit bewerk je)
tools/build.py    plakt de gedeelde schil rond elke pagina
assets/css/       één stylesheet met het volledige ontwerpsysteem
assets/js/        progressive enhancement; de site werkt ook zonder
assets/fonts/     zelf gehoste lettertypes (Fraunces, Source Sans 3)
assets/img/       monogram en portretopvulling
*.html            het resultaat — dit is wat gepubliceerd wordt
```

De gegenereerde HTML-bestanden staan mee in de repository, zodat de site
zonder bouwstap te publiceren is: elke host die bestanden kan serveren,
volstaat.

### Een pagina wijzigen

1. Bewerk het overeenkomstige bestand in `pages/`.
2. Voer `python3 tools/build.py` uit.
3. Commit zowel het bestand in `pages/` als de gegenereerde HTML.

Bovenaan elk bestand in `pages/` staan de metagegevens:

```
slug: contact.html          bestandsnaam van de uitvoer
title: Contact en afspraak  paginatitel (browser + Google)
description: …              omschrijving voor de zoekresultaten
nav: contact                welk menu-item oplicht
cta: nee                    laat het contactblok onderaan weg
```

### Kantoorgegevens wijzigen

Adres, telefoonnummer, e-mail en rekeningnummer staan één keer, bovenaan
`tools/build.py` in `SITE`. Aanpassen en opnieuw bouwen volstaat.

## Ontwerp

| | |
|---|---|
| Titels | Fraunces (variabel, optische groottes) |
| Tekst | Source Sans 3 |
| Kleuren | bot `#F7F4EF` · inkt `#1C1F1D` · woud `#2E4034` · klei `#B08968` |
| Motief | de boog — in het portretkader, de scheidingslijnen en het monogram |

De volledige tokens staan bovenaan `assets/css/style.css`.

## Privacy en beveiliging

Bewuste keuzes, omdat het om een advocatenkantoor gaat:

- **Lettertypes worden zelf gehost.** Geen Google Fonts CDN, dus geen
  IP-adressen van bezoekers naar derden.
- **Geen cookies, geen trackers, geen analytics.** Daardoor is er ook geen
  cookiebanner nodig.
- **Geen ingebedde kaart.** De verwijzing naar de kaart is een gewone link
  die de bezoeker zelf aanklikt.
- **Beveiligingsheaders** (CSP, HSTS, nosniff, frame-ancestors) staan in
  `netlify.toml`. Bij een andere host moeten die mee overgenomen worden.

## Publiceren

Klaar voor Netlify: `netlify.toml` regelt de bouwstap, de headers, het
caching-beleid en de omleidingen. Het certificaat en de https-afdwinging
komen daar automatisch mee.

Bij een klassieke webhost volstaat het om de bestanden uit de hoofdmap te
uploaden, met uitzondering van `pages/`, `tools/` en de markdownbestanden.
Zorg dan zelf voor een geldig certificaat en voor de headers uit
`netlify.toml`.

Het contactformulier gebruikt Netlify Forms. Op een andere host moet de
`<form>` in `pages/contact.html` een andere afhandeling krijgen.

## Nog te doen

Zie **[INHOUD-TODO.md](INHOUD-TODO.md)**. Alles wat nog van de cliënte moet
komen, staat daar opgesomd en is op de site gemarkeerd met een gele
onderlijning.
