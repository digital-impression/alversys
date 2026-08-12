# Wat we nog nodig hebben van Veerle

Alles wat hieronder staat, is op de site zichtbaar gemarkeerd met een zachte
gele onderlijning (`class="tbc"`). Zolang die markering ergens staat, is de
tekst een aanname van ons en **niet** bevestigd door de cliënte. Zoek in
`pages/` op `tbc` om alle plaatsen te vinden.

Verwijder telkens enkel het `<span class="tbc">…</span>` rond de tekst zodra
het gegeven bevestigd is, en voer daarna `python3 tools/build.py` uit.

---

## 1. Kritisch — de site mag hier niet mee online

Deze gegevens zijn wettelijk verplicht voor een advocaat (Boek III WER,
dienstenwetgeving). Zonder deze gegevens is `juridische-informatie.html`
onvolledig.

| Gegeven | Waar | Nu ingevuld |
|---|---|---|
| Ondernemingsnummer (KBO) | juridische-informatie | `BE 0000.000.000` |
| Btw-nummer | juridische-informatie | `BE 0000.000.000` |
| Verzekeraar beroepsaansprakelijkheid | juridische-informatie | `[naam verzekeraar]` |
| Polisnummer | juridische-informatie | `[polisnummer]` |
| Makelaar | juridische-informatie | `[naam makelaar]` |
| Verzekerd bedrag per schadegeval | juridische-informatie | `[bedrag]` |
| Geografische dekking van de polis | juridische-informatie | aanname: wereldwijd met uitzonderingen |
| Algemene voorwaarden van het kantoor | juridische-informatie | ontbreekt volledig |
| Datum laatste update | juridische-informatie, privacybeleid | `[datum]` |

**Ook nog na te gaan:** het juiste kantooradres. De eigen pagina vermeldt
*Vital Decosterstraat 46 bus 6* — advocaat.be vermeldt nog *Mercatorpad 11*.
Eén van beide is verouderd. Welk het ook is: laat het overal gelijktrekken
(advocaat.be, Google Bedrijfsprofiel, Gouden Gids, jeugdadvocaat.be). Voor de
vindbaarheid in Google telt consistentie van naam, adres en telefoon zwaar.

## 2. Tarieven — nu nog nulbedragen

De hele pagina `tarieven.html` staat er, maar met `€ 00` en `€ 000`.

- Tarief eerste consult (en: is dat betalend of gratis?)
- Uurtarief dossierbehandeling (excl. btw)
- Uurtarief bemiddeling (per uur, te delen tussen de partijen)
- Werkt zij met vaste prijzen voor afgebakende opdrachten? Zo ja, welke?
- Aanvaardt zij dossiers via het Bureau voor Juridische Bijstand
  (tweedelijnsbijstand)? Is er een wachtlijst?
- Kantoorkosten: forfait of doorrekening per stuk?

## 3. Bemiddeling — te bevestigen

- Is zij **erkend bemiddelaar** bij de Federale Bemiddelingscommissie? In
  welke categorie (familiaal / burgerlijk en handelsrecht / sociaal)?
  Sinds wanneer?
- Klopt de gemiddelde doorlooptijd van drie tot zes gesprekken?
- Is het kennismakingsgesprek bij bemiddeling vrijblijvend en kosteloos?

De volledige positionering van de site steunt hierop. Haar huidige site
draagt de paginatitel *"Advocaat en bemiddelaar"*, maar op de zichtbare
pagina staat daar niets over — het is dus ondergewaardeerd. Als de erkenning
er is, verdient die een prominente plaats; is ze er niet, dan moeten we het
woord "erkend" overal schrappen.

## 4. Over mij — nu grotendeels ingevuld door ons

De hele biografie is een plausibele invulling en moet door haar herschreven
of bevestigd worden:

- Waar studeerde zij rechten? In welk jaar legde zij de eed af?
- Opleiding tot bemiddelaar: waar, wanneer?
- Staat zij op de lijst van **jeugdadvocaten**? (jeugdadvocaat.be vermeldt
  haar, dus vermoedelijk ja — maar bevestiging nodig, dit is een
  beschermde kwalificatie.)
- Klopt de betrokkenheid bij **TEJO Leuven**? Wil zij die vermelden?
  (Gevonden via LinkedIn, niet via een officiële bron.)
- Eerdere loopbaan, stage, vroegere kantoren?
- Het citaat op de homepagina schreven wij. Vervangen door een eigen zin,
  of schrappen.

## 5. Beeldmateriaal

Dit is het grootste openstaande punt voor de uitstraling.

- **Portretfoto** — staand, 4:5, in natuurlijk licht, rustige achtergrond.
  Dit is het beeld waarop het hele ontwerp steunt. Vervang
  `assets/img/portret-placeholder.svg` door `assets/img/portret.jpg`.
- **Vier sfeerbeelden** die de site nu draagt (`gang`, `bibliotheek`,
  `trap`, `doorgang`, `gewelf`) zijn **tijdelijk**. Ze komen van Wikimedia
  Commons en zijn in de huisstijl bewerkt zodat ze als één geheel lezen.
  Zolang ze er staan, moet de naamsvermelding op `juridische-informatie.html`
  blijven staan (CC BY-SA). Vervangen we ze door eigen foto's, dan vervalt dat.
- Wat we in de plaats het liefst krijgen: het kantoor of de gespreksruimte,
  een detail van haar bureau, en desnoods een sfeerbeeld van Leuven.
- Nieuwe foto's krijgen dezelfde behandeling met
  `python3 tools/beeld.py foto.jpg naam 4:5 1100`, zodat ze meteen in de
  huisstijl passen.

## 6. Praktische werking

- Werkelijke bereikbaarheid per telefoon (nu: "werkdagen van 9 tot 18 uur")
- Realistische antwoordtermijn op e-mail (nu: "binnen twee werkdagen")
- Klopt "enkel op afspraak"?
- Beschrijving van de bereikbaarheid: afstand tot het station, parkeren,
  toegankelijkheid voor iemand met een rolstoel of kinderwagen
- Naar welk e-mailadres mogen de berichten uit het contactformulier gaan?
- Bewaartermijn dossiers in het privacybeleid (nu: vijf jaar) — komt dat
  overeen met haar eigen praktijk?

## 7. Technisch, aan onze kant

- Domeinnaam en hosting: wie beheert `veerleborremans.be` vandaag?
  De huidige site draait op **http zonder certificaat** — de browser toont
  "Niet beveiligd". Dat moet hoe dan ook weg.
- Beslissen waar we hosten (`netlify.toml` staat klaar voor Netlify, incl.
  gratis certificaat, beveiligingsheaders en formulierafhandeling).
- Werkt het contactformulier via Netlify Forms, of moet het naar een andere
  afhandeling? Vandaag stuurt het naar Netlify.
- Google Bedrijfsprofiel aanmaken of overnemen — voor een lokale praktijk
  levert dat meestal meer op dan de site zelf.
- 301-omleidingen van de oude URL's naar de nieuwe, als die bestaan.
