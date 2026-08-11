# Jacobs Law — website

A bespoke static website for **Jacobs Law**, advocatenkantoor te Aartselaar
(Populierenlaan 43, 2630 Aartselaar).

Plain HTML, CSS and a little vanilla JavaScript. No framework, no build step at
runtime, no external requests — it will run from any static host or even from a
USB stick.

---

## Running it

Open `index.html`, or serve the folder:

```bash
python3 -m http.server 8000
```

## Deploying

Upload the repository root as-is. It works unchanged on Netlify, Vercel,
Cloudflare Pages, GitHub Pages or classic FTP hosting. There is nothing to
compile and no server-side code.

---

## Design

The direction is deliberately **not** the US "big law" look (mahogany, gavels,
navy-and-gold, stock photography of men with folded arms). Jacobs Law is a
two-lawyer boutique founded in 2017 whose own photography is bright, warm and
informal — so the site is built as warm editorial restraint instead.

**Palette.** Grown out of the firm's existing brand colours (`#DBD2C5` sand,
`#BCA77E` gold) rather than replacing them.

| Token | Value | Role |
|---|---|---|
| `--ink` | `#14110E` | Warm near-black. Hero, anchor sections, footer. |
| `--bone` | `#FAF8F5` | Page canvas. |
| `--sand-3` | `#F3EFE9` | Alternating band. |
| `--brass` | `#B08D57` | Decoration on ink, button fills. |
| `--brass-rule` | `#A7844F` | Decoration on light (≥3:1). |
| `--brass-deep` | `#87683A` | Small text on light (≥4.5:1). |
| `--brass-light` | `#D9BE92` | Small text on ink (≥4.5:1). |

The brass is split into four tones on purpose: a single accent colour cannot
clear WCAG AA as both a hairline on bone and as 12px uppercase text. Each tone
carries one contrast job — see the comment at the top of `assets/css/site.css`.

**Type.** Fraunces (display serif) over Instrument Sans (grotesk). Both are
variable fonts under the SIL Open Font License and are **self-hosted** in
`assets/fonts/` — nothing is fetched from Google, so no visitor IP address
reaches a third party and the site sets no cookies at all. Small numerals are
set in the grotesk deliberately: at 13px Fraunces' display cut renders a `3`
that reads as a `5`.

**The motif.** A hairline rule interrupted by a small brass diamond — "de
horizon". It recurs as the logo mark, the eyebrow rule, the section divider, the
list bullet and the core of every practice-area icon. The four icons are drawn
for this site from that one vocabulary (line plus diamond); they are not stock.

---

## Structure

```
index.html                    Home
over-ons.html                 Over ons
liesbet-jacobs.html           Biografie
michelle-damen.html           Biografie
faillissementen.html          Juridisch domein 01
schulden.html                 Juridisch domein 02
burgerlijk-recht.html         Juridisch domein 03
familierecht.html             Juridisch domein 04
tarieven.html                 Tarieven
contact.html                  Contact + klachtenregeling (#klachten)
bedankt.html                  Form success page
privacy-en-cookiebeleid.html  Privacy & cookies

assets/css/site.css           Design system, ~1000 lines, sectioned
assets/js/site.js             Header state, mobile drawer, scroll reveal
assets/fonts/                 Self-hosted variable fonts + fonts.css
assets/img/                   Photography (from the firm's current site)
tools/build.py                Page generator (optional — see below)
sitemap.xml, robots.txt
_redirects                    301s from the old Wix paths (Netlify/Cloudflare)
.htaccess                     Same redirects + headers for Apache hosting
netlify.toml                  No-build config, cache and security headers
```

### About `tools/build.py`

The eleven pages share a header, drawer and footer. Rather than maintain eleven
copies by hand, `tools/build.py` holds the shared chrome plus each page's
content and writes the HTML:

```bash
python3 tools/build.py
```

**The generated HTML is the deliverable.** The script is a convenience, not a
dependency — the site never runs it. Two ways to work:

- **Keep it:** edit content in `build.py`, re-run, commit the regenerated HTML.
- **Drop it:** delete `tools/`, edit the `.html` files directly from then on.

Do not mix the two: re-running the script overwrites hand edits to the HTML.

---

## Before this goes live

Most of the open items are now closed. What remains is listed honestly.

**Resolved — company details verified.** The legal identifiers were checked against
the official **KBO/BCE** register rather than left flagged: Jacobs Law, *Besloten
Vennootschap*, ondernemingsnummer **0669.531.513**, VAT-registered since
**12 January 2017**, seat at Populierenlaan 43, 2630 Aartselaar, NACE 69.101
(*activiteiten van advocaten*), Liesbet Jacobs as *bestuurder*. The footer now
reads "BTW BE 0669.531.513", which is the correct Belgian form, and the 2017
founding date used in the copy is confirmed.

**Resolved — no unverifiable price is published.** The €125/hr figure came from a
third-party directory and could not be confirmed, so it is **not on the site**.
Publishing a rate a client might rely on is not worth the risk. The tariff table
now reads "vooraf afgesproken" for the hourly fee, and the copy explains that the
rate is agreed at the first consultation and confirmed in writing — which is both
true and better practice. Only the **€110 incl. btw** consultation fee is stated
as a number, and that one is from the firm's own contact page.

If the firm confirms an hourly rate, it goes back in at one line in
`tools/build.py` (search for `vooraf afgesproken`).

**Resolved — redirects now ship as working config**, not just a table. `_redirects`
(Netlify / Cloudflare Pages) and `.htaccess` (classic Apache hosting) 301 every old
Wix path to its new page, so existing links and search rankings survive the move.

**Resolved — the form is never a dead end.** It is wired for **Netlify Forms**
(`data-netlify` plus a honeypot) and works there with no configuration, sending
visitors to `bedankt.html`. Underneath it there is now a direct "mail or call us"
line, so the page still works on a host without a form backend. On such a host,
point the form's `action` at an endpoint (Formspree, Basin) or delete the form and
keep the direct contact line.

**Still needs the firm: a legal read of the privacy policy.** The cookie section is
certainly correct — the site sets none, loads no third-party resources, and
self-hosts its fonts, so `netlify.toml` can and does ship a strict
`Content-Security-Policy` with no `unsafe-inline`. What the firm must supply is the
retention periods and the list of processors. The complaints text at
`contact.html#klachten` should get the same read against the Antwerp bar's wording.

**Still worth doing: better portraits.** Both are now cropped to a matching 4:5 and
framed at exactly that ratio, so the browser never re-crops and both sitters keep
identical headroom. But the sources are low-resolution and Liesbet's is framed hard
against the right edge of the original, which caps how well the pair can sit
together. The photographer's originals — or a short re-shoot — would lift the team
section. Nothing is blocked on this.

**Assumptions I made rather than leaving blanks.** Opening hours are given as
"consultaties uitsluitend op afspraak" with weekday phone and e-mail availability,
which is the safe reading for a two-lawyer practice — correct it if they keep set
hours. The four practice areas are exactly the ones in their current navigation.

## Copy

Dutch throughout. Where the firm's existing text was good it is reproduced
verbatim — the credo, the insolvency paragraphs, both biographies, the
referral promise, the familierecht opening. The rest was written to match that
voice: plain, direct, no padding.

One deliberate omission: the old *Schulden* page led with a 2020 COVID
paragraph. Republishing that in 2026 would have dated the site on day one, so
that page was rewritten around the same subject (invordering, betalingsregeling,
beslag, collectieve schuldenregeling).

## Quality checks

Verified in Chromium across 320–1920px:

- No horizontal overflow at any of twelve tested widths
- All body, footer and header text meets **WCAG AA** contrast (verified against
  computed styles, not just the token table)
- One `<h1>` per page, no heading-level skips
- Every image has an `alt`; every internal link resolves; no console errors
- Keyboard: skip link, visible focus rings, Escape closes the drawer
- `prefers-reduced-motion` disables reveals and smooth scrolling
- Renders without JavaScript — reveals are opacity-guarded by a `no-js` class
- Print stylesheet included
- No inline scripts, so the shipped CSP forbids them outright
