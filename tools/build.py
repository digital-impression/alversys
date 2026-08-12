#!/usr/bin/env python3
"""
Bouwt de statische site van Veerle Borremans.

Elke pagina in pages/ bevat alleen de inhoud van <main>, met bovenaan een
klein blok metagegevens. Dit script plakt daar de gedeelde schil omheen
(kop, navigatie, voet, metatags, JSON-LD) en schrijft kant-en-klare
HTML-bestanden naar de hoofdmap.

    python3 tools/build.py

De uitvoer is gewone HTML: de site heeft geen bouwstap nodig om te draaien.
Dit script bestaat enkel om te vermijden dat dertien pagina's uit elkaar
gaan lopen. Inhoud wijzig je in pages/, daarna dit script opnieuw uitvoeren.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "pages"

# --------------------------------------------------------------------------
# Vaste gegevens van het kantoor.
# Wijzig hier, dan wordt het overal op de site doorgevoerd.
# --------------------------------------------------------------------------

SITE = {
    "name": "Veerle Borremans",
    "role": "Advocaat & bemiddelaar",
    "base_url": "https://www.veerleborremans.be",
    "street": "Vital Decosterstraat 46 bus 6",
    "postcode": "3000",
    "city": "Leuven",
    "country": "BE",
    "tel_display": "0490 43 67 93",
    "tel_href": "+32490436793",
    "email": "info@veerleborremans.be",
    "bar": "Balie Leuven",
    "iban_derden": "BE36 6300 9506 2281",
    "year": "2026",
}

NAV = [
    ("over-mij", "Over mij", "over-mij.html"),
    ("rechtsdomeinen", "Rechtsdomeinen", "rechtsdomeinen.html"),
    ("bemiddeling", "Bemiddeling", "bemiddeling.html"),
    ("tarieven", "Tarieven", "tarieven.html"),
]

# --------------------------------------------------------------------------
# Sjablonen
# --------------------------------------------------------------------------

JSON_LD = """{
  "@context": "https://schema.org",
  "@type": "Attorney",
  "@id": "%(base_url)s/#kantoor",
  "name": "%(name)s",
  "description": "Advocaat en erkend bemiddelaar te Leuven. Familierecht, jeugdrecht, personenrecht en strafrecht.",
  "url": "%(base_url)s/",
  "email": "%(email)s",
  "telephone": "+32 490 43 67 93",
  "image": "%(base_url)s/assets/img/monogram.svg",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "%(street)s",
    "postalCode": "%(postcode)s",
    "addressLocality": "%(city)s",
    "addressCountry": "%(country)s"
  },
  "areaServed": [
    { "@type": "City", "name": "Leuven" },
    { "@type": "AdministrativeArea", "name": "Vlaams-Brabant" }
  ],
  "knowsLanguage": "nl-BE",
  "memberOf": { "@type": "Organization", "name": "Orde van Advocaten te Leuven" },
  "knowsAbout": [
    "Familierecht", "Echtscheiding", "Jeugdrecht", "Personenrecht",
    "Strafrecht", "Familiale bemiddeling"
  ]
}""" % SITE

CTA_BLOCK = """
      <section class="closer">
        <div class="shell closer__grid">
          <div>
            <p class="eyebrow">Kennismaken</p>
            <h2>Uw situatie rustig bespreken, voor u iets beslist</h2>
            <p style="margin-top:var(--s5)">
              Een eerste gesprek dient om te luisteren. U vertelt wat er speelt, ik
              schets welke wegen openstaan en wat elk daarvan realistisch betekent:
              in tijd, in kosten en voor de mensen om u heen. Pas daarna beslist u
              of u verdergaat.
            </p>
            <div class="btn-row">
              <a class="btn" href="contact.html">Een afspraak vragen</a>
              <a class="link-arrow" href="tel:{tel_href}">{tel_display}</a>
            </div>
            <dl class="dossier">
              <div>
                <dt>Bereikbaar</dt>
                <dd><span class="tbc">Ma tot vr, 9 tot 17 uur</span></dd>
              </div>
              <div>
                <dt>Kantoor</dt>
                <dd>{street}, {postcode} {city}, enkel op afspraak</dd>
              </div>
            </dl>
          </div>

          <div>
            <div class="map">
              <svg viewBox="0 0 600 420" role="img" aria-labelledby="kaart-titel">
                <title id="kaart-titel">Schematische ligging van het kantoor tussen het station van Leuven en de Bondgenotenlaan</title>
                <rect width="600" height="420" fill="#15241b"/>
                <g stroke="#27412f" stroke-width="26" stroke-linecap="square" fill="none">
                  <path d="M470 -20V440"/>
                  <path d="M-20 300H620"/>
                  <path d="M60 440 380 90"/>
                </g>
                <g stroke="#1d3226" stroke-width="10" fill="none">
                  <path d="M180 300 300 168"/>
                  <path d="M300 380H470"/>
                  <path d="M120 300V120H300"/>
                </g>
                <rect x="486" y="248" width="96" height="72" fill="#27412f"/>
                <text x="534" y="290" text-anchor="middle" font-family="Georgia, serif" font-size="15" fill="#e6e2d8">Station</text>
                <g font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#bfa267" letter-spacing="1.5">
                  <text x="24" y="288">BONDGENOTENLAAN</text>
                  <text x="492" y="60" transform="rotate(90 492 60)">TIENSEVEST</text>
                  <text x="300" y="342">MARTELARENPLEIN</text>
                </g>
                <g>
                  <circle cx="300" cy="168" r="13" fill="#a98a4b"/>
                  <circle cx="300" cy="168" r="26" fill="none" stroke="#a98a4b" stroke-width="1"/>
                  <text x="324" y="164" font-family="Georgia, serif" font-size="16" fill="#f5f2ea">Vital Decosterstraat 46</text>
                  <text x="324" y="184" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#e6e2d8">bus 6, 3000 Leuven</text>
                </g>
              </svg>
              <p class="map__note">Schematisch, niet op schaal &middot; <span class="tbc">te voet 5 minuten van het station</span></p>
            </div>

            <dl class="dossier" style="margin-top:var(--s6)">
              <div>
                <dt>Parkeren</dt>
                <dd><span class="tbc">Parking Vital Decoster of blauwe zone</span></dd>
              </div>
              <div>
                <dt>Openbaar vervoer</dt>
                <dd><span class="tbc">Station Leuven, 5 minuten te voet</span></dd>
              </div>
            </dl>
          </div>
        </div>
      </section>
"""

SHELL = """<!doctype html>
<html lang="nl-BE">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{base_url}/{slug}">
<meta name="theme-color" content="#1d3226">
<meta name="robots" content="{robots}">

<meta property="og:type" content="website">
<meta property="og:locale" content="nl_BE">
<meta property="og:site_name" content="{name}, {role}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{base_url}/{slug}">
<meta property="og:image" content="{base_url}/assets/img/monogram.svg">
<meta name="twitter:card" content="summary">

<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/monogram.svg">

<link rel="preload" href="assets/fonts/fraunces-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/sourcesans3-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">

<script type="application/ld+json">
{json_ld}
</script>
</head>
<body>
<a class="skip-link" href="#hoofdinhoud">Naar de hoofdinhoud</a>

<header class="site-header">
  <div class="site-header__meta">
    <div class="shell">
      <ul>
        <li>{street}, {postcode} {city}</li>
        <li><a href="tel:{tel_href}">{tel_display}</a></li>
        <li><a href="mailto:{email}">{email}</a></li>
      </ul>
      <span class="site-header__note">Enkel op afspraak &middot; Balie Leuven</span>
    </div>
  </div>

  <div class="shell site-header__bar">
    <a class="brand" href="index.html">
      <img class="brand__mark" src="assets/img/monogram.svg" alt="" width="34" height="42">
      <span class="brand__text">
        <span class="brand__name">Veerle Borremans</span>
        <span class="brand__role">Advocaat &amp; bemiddelaar</span>
      </span>
    </a>

    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="hoofdnavigatie" aria-label="Menu openen of sluiten">
      <span></span><span></span><span></span>
    </button>

    <nav class="nav" id="hoofdnavigatie" aria-label="Hoofdnavigatie">
{nav_links}
      <a class="btn nav__cta" href="contact.html">Afspraak</a>
    </nav>
  </div>
</header>

<main id="hoofdinhoud">
{body}{cta}</main>

<footer class="site-footer">
  <div class="shell">
    <div class="site-footer__grid">
      <div class="site-footer__brand">
        <span class="brand__text">
          <span class="brand__name">Veerle Borremans</span>
          <span class="brand__role">Advocaat &amp; bemiddelaar</span>
        </span>
        <p style="margin-top:var(--s5);max-width:34ch">
          Advocatenkantoor te Leuven voor familierecht, jeugdrecht, personenrecht
          en strafrecht. Ingeschreven aan de balie te Leuven.
        </p>
      </div>

      <div>
        <p class="site-footer__title">Kantoor</p>
        <address>
          {street}<br>
          {postcode} {city}<br><br>
          <a href="tel:{tel_href}">{tel_display}</a><br>
          <a href="mailto:{email}">{email}</a>
        </address>
      </div>

      <div>
        <p class="site-footer__title">Wegwijs</p>
        <ul>
          <li><a href="over-mij.html">Over mij</a></li>
          <li><a href="rechtsdomeinen.html">Rechtsdomeinen</a></li>
          <li><a href="bemiddeling.html">Bemiddeling</a></li>
          <li><a href="tarieven.html">Erelonen en kosten</a></li>
          <li><a href="contact.html">Contact en afspraak</a></li>
        </ul>
      </div>

      <div>
        <p class="site-footer__title">Praktisch</p>
        <ul>
          <li><span class="tbc">Ma tot vr, 9 tot 17 uur</span></li>
          <li>Enkel op afspraak</li>
          <li>Orde van Advocaten te Leuven</li>
          <li><span class="tbc"><a href="https://www.linkedin.com" target="_blank" rel="noopener noreferrer">LinkedIn</a></span></li>
        </ul>
      </div>
    </div>

    <div class="site-footer__bottom">
      <p>&copy; {year} Veerle Borremans, advocaat te Leuven</p>
      <nav aria-label="Juridische informatie">
        <a href="juridische-informatie.html">Juridische informatie</a>
        <a href="privacybeleid.html">Privacybeleid</a>
      </nav>
    </div>
  </div>
</footer>

<div class="action-bar">
  <a href="tel:{tel_href}">Bellen</a>
  <a href="contact.html">Afspraak</a>
</div>

<script src="assets/js/main.js" defer></script>
</body>
</html>
"""


def parse_page(path: Path) -> dict:
    """Leest een paginabestand: metagegevens boven een regel met ---, dan de inhoud."""
    raw = path.read_text(encoding="utf-8")
    if "\n---\n" not in raw:
        raise SystemExit(f"{path.name}: metagegevens ontbreken (verwacht een regel '---')")

    head, body = raw.split("\n---\n", 1)
    meta = {}
    for line in head.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()

    meta["body"] = body.strip("\n")
    meta["source"] = path.name
    return meta


def build_nav(current: str) -> str:
    out = []
    for key, label, href in NAV:
        current_attr = ' aria-current="page"' if key == current else ""
        out.append(f'      <a class="nav__link" href="{href}"{current_attr}>{label}</a>')
    return "\n".join(out)


def render(meta: dict) -> str:
    slug = meta["slug"]
    title = meta["title"]
    full_title = title if slug == "index.html" else f"{title} | Veerle Borremans"

    cta = ""
    if meta.get("cta", "ja").lower() not in ("nee", "no", "none"):
        cta = CTA_BLOCK.format(**SITE)

    return SHELL.format(
        title=html.escape(full_title, quote=True),
        og_title=html.escape(title, quote=True),
        description=html.escape(meta["description"], quote=True),
        slug="" if slug == "index.html" else slug,
        robots=meta.get("robots", "index,follow"),
        json_ld=JSON_LD,
        nav_links=build_nav(meta.get("nav", "")),
        body=meta["body"],
        cta=cta,
        **SITE,
    )


def build_sitemap(pages: list[dict]) -> str:
    entries = []
    for meta in sorted(pages, key=lambda m: m["slug"]):
        if meta.get("robots", "").startswith("noindex"):
            continue
        slug = "" if meta["slug"] == "index.html" else meta["slug"]
        priority = "1.0" if slug == "" else meta.get("priority", "0.7")
        entries.append(
            "  <url>\n"
            f"    <loc>{SITE['base_url']}/{slug}</loc>\n"
            f"    <changefreq>yearly</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            "  </url>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )


def main() -> int:
    if not PAGES.is_dir():
        raise SystemExit("map pages/ niet gevonden")

    built = []
    for path in sorted(PAGES.glob("*.html")):
        meta = parse_page(path)
        for required in ("slug", "title", "description"):
            if required not in meta:
                raise SystemExit(f"{path.name}: '{required}' ontbreekt in de metagegevens")
        (ROOT / meta["slug"]).write_text(render(meta), encoding="utf-8")
        built.append(meta)
        print(f"  ✓ {meta['slug']:<32} {meta['title']}")

    (ROOT / "sitemap.xml").write_text(build_sitemap(built), encoding="utf-8")
    print(f"  ✓ {'sitemap.xml':<32} {len(built)} pagina's")

    # Ruwe controle op verweesde interne links.
    bestaand = {m["slug"] for m in built}
    for meta in built:
        for href in re.findall(r'href="([^"#:?]+\.html)"', meta["body"]):
            if href not in bestaand:
                print(f"  ! {meta['slug']}: verwijst naar onbestaande pagina {href}")

    # Herinnering aan de nog niet bevestigde gegevens (zie INHOUD-TODO.md).
    openstaand = sum(m["body"].count('class="tbc"') for m in built)
    if openstaand:
        print(
            f"\n  ! {openstaand} plaatsen wachten nog op bevestiging door de cliënte."
            "\n    Zoek op 'tbc' in pages/, zie INHOUD-TODO.md."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
