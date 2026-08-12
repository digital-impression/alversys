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
| `gang.jpg` | [Duke Humfrey's Library Interior 5](https://commons.wikimedia.org/wiki/File:Duke_Humfrey%27s_Library_Interior_5,_Bodleian_Library,_Oxford,_UK_-_Diliff.jpg) | Diliff | CC BY-SA 3.0 |
| `bibliotheek.jpg` | [Duke Humfrey's Library Interior 6](https://commons.wikimedia.org/wiki/File:Duke_Humfrey%27s_Library_Interior_6,_Bodleian_Library,_Oxford,_UK_-_Diliff.jpg) | Diliff | CC BY-SA 3.0 |
| `trap.jpg` | [Säppi majakka](https://commons.wikimedia.org/wiki/File:S%C3%A4ppi_majakka.jpg) | kallerna | CC BY-SA 3.0 |
| `doorgang.jpg` | [Underground city in Nushabad](https://commons.wikimedia.org/wiki/File:Underground_city_in_Nushabad,_Kashan,_Iran3.jpg) | Amirpashaei | CC BY-SA 4.0 |
| `gewelf.jpg` | [Escalier spirale voûte château de l'Herm](https://commons.wikimedia.org/wiki/File:Escalier_spirale_vo%C3%BBte_ch%C3%A2teau_de_l%27Herm.jpg) | Jebulon | CC0 |

**Let op:** CC BY-SA verplicht tot naamsvermelding én verspreiding van de
bewerking onder dezelfde licentie. Zolang deze foto's op de site staan, moet
de vermelding op `juridische-informatie.html` blijven staan. Vervangen we ze
door eigen foto's, dan vervalt die verplichting — wat de eenvoudigste weg is
voor een advocatenkantoor.

De toonbehandeling is reproduceerbaar met `tools/beeld.py`.

## Code

De HTML, CSS en JavaScript in deze repository zijn voor Veerle Borremans
gemaakt en worden aan haar overgedragen.
