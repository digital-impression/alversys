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
privacy-en-cookiebeleid.html  Privacy (DRAFT — see below)

assets/css/site.css           Design system, ~1000 lines, sectioned
assets/js/site.js             Header state, mobile drawer, scroll reveal
assets/fonts/                 Self-hosted variable fonts + fonts.css
assets/img/                   Photography (from the firm's current site)
tools/build.py                Page generator (optional — see below)
sitemap.xml, robots.txt
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

**1. Confirm two figures.** Everything on the site is taken from the firm's own
current website except two items, which came from a third-party lawyer
directory and are marked here rather than buried:

- the **€125 excl. btw hourly rate** on `tarieven.html`
- the **VAT/company number `BE 0669.531.513`** in the footer

The €110 incl. btw consultation fee *is* from the firm's own contact page. Also
worth confirming: the firm is listed elsewhere as holding a
*plaatsvervangend rechter* appointment in Boom — I left it off the site because
I could not verify it against a first-party source. Add it if it is current.

**2. Wire up the contact form.** It is marked up for **Netlify Forms**
(`data-netlify="true"` plus a honeypot) and works with zero configuration if
hosted there — submissions land in the Netlify dashboard and the visitor is sent
to `bedankt.html`. On any other host, point the `action` at a form endpoint
(Formspree, Basin) or a small mail script. Until then the form will not deliver.

**3. Have the privacy policy reviewed.** `privacy-en-cookiebeleid.html` is a
solid, accurate skeleton — the cookie section is genuinely correct (the site
sets none) — but bewaartermijnen and verwerkers must be checked by the firm.
The complaints section on `contact.html#klachten` likewise needs a check against
the Antwerp bar's current wording.

**4. Photography.** All images are the firm's own, pulled from the current site.
Two notes: the source portraits are low-ish resolution, and Liesbet's is framed
hard against the right edge of the original, so the pair cannot be cropped to
sit identically. The original files from the photographer — or a short re-shoot
— would visibly lift the team section. Nothing else is blocked on this.

**5. Redirects.** The old Wix URLs differ from the new ones. Map them:

| Old | New |
|---|---|
| `/biografieliesbet` | `/liesbet-jacobs.html` |
| `/biografiemichelle` | `/michelle-damen.html` |
| `/burgerlijkrecht` | `/burgerlijk-recht.html` |
| `/faillissementen` | `/faillissementen.html` |
| `/schulden` | `/schulden.html` |
| `/familierecht` | `/familierecht.html` |
| `/contact` | `/contact.html` |
| `/privacyencookieverklaring` | `/privacy-en-cookiebeleid.html` |

---

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
