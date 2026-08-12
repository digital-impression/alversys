# Licenties van gebruikte bestanddelen

## Lettertypes

Beide lettertypes staan onder de **SIL Open Font License 1.1** en mogen vrij
worden gebruikt en zelf gehost, ook commercieel.

| Lettertype | Gebruikt voor | Auteur | Licentie |
|---|---|---|---|
| Fraunces (variabel) | Titels en citaten | Undercase Type — Phaedra Charles, Flavia Zimbardi | [OFL 1.1](https://openfontlicense.org) |
| Source Sans 3 (variabel) | Lopende tekst | Adobe — Paul D. Hunt | [OFL 1.1](https://openfontlicense.org) |

De bestanden staan in `assets/fonts/` en worden vanaf de eigen server geladen.
Ze worden bewust **niet** via de Google Fonts CDN opgehaald: daarbij wordt het
IP-adres van de bezoeker naar een derde partij gestuurd, wat voor een
advocatenkantoor een onnodig AVG-risico is.

## Beeld

Het monogram, de portretopvulling en het boogmotief zijn voor dit project
gemaakt.

De sfeerfoto's zijn **tijdelijk**. Ze komen van Wikimedia Commons, zijn vrij
herbruikbaar en werden hier bewerkt: bijgesneden en in de huisstijl getoond
(warm duotoon met korrel). Ze staan er om de vormgeving te tonen en horen
vervangen te worden door eigen beeldmateriaal — zie `INHOUD-TODO.md`.

| Bestand | Origineel | Auteur | Licentie |
|---|---|---|---|
| `begijnhof.jpg` | [Middenstraat, Groot Begijnhof of Leuven](https://commons.wikimedia.org/wiki/File:Middenstraat,_Groot_Begijnhof_of_Leuven_(DSCF0911).jpg) | Trougnouf (Benoit Brummer) | CC BY 4.0 |
| `weg.jpg` | [Groot Begijnhof in Leuven (2)](https://commons.wikimedia.org/wiki/File:Groot_Begijnhof_in_Leuven_(2).jpg) | Krzysztof Golik | CC BY-SA 4.0 |
| `gevel.jpg` | [Groot Begijnhof in Leuven (3)](https://commons.wikimedia.org/wiki/File:Groot_Begijnhof_in_Leuven_(3).jpg) | Krzysztof Golik | CC BY-SA 4.0 |
| `licht.jpg` | [Dülmen, Börnste, Waldweg](https://commons.wikimedia.org/wiki/File:D%C3%BClmen,_B%C3%B6rnste,_Waldweg_--_2024_--_6257.jpg) | Dietmar Rabich | CC BY-SA 4.0 |
| `pad.jpg` | [Prospect Park November 2016](https://commons.wikimedia.org/wiki/File:Prospect_Park_New_York_November_2016_001.jpg) | King of Hearts | CC BY-SA 4.0 |

**Let op:** CC BY-SA verplicht tot naamsvermelding én verspreiding van de
bewerking onder dezelfde licentie. Zolang deze foto's op de site staan, moet
de vermelding op `juridische-informatie.html` blijven staan. Vervangen we ze
door eigen foto's, dan vervalt die verplichting — wat de eenvoudigste weg is
voor een advocatenkantoor.

De toonbehandeling is reproduceerbaar met `tools/beeld.py`.

## Code

De HTML, CSS en JavaScript in deze repository zijn voor Veerle Borremans
gemaakt en worden aan haar overgedragen.
