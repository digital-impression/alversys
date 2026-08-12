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
# Wijzig hier — het wordt overal op de site doorgevoerd.
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
          <div class="reveal">
            <p class="eyebrow">Kennismaken</p>
            <h2>Uw situatie rustig bespreken, voor u iets beslist</h2>
            <p>
              Een eerste gesprek dient om te luisteren. U vertelt wat er speelt, ik
              schets welke wegen openstaan en wat elk daarvan realistisch betekent —
              in tijd, in kosten en voor de mensen om u heen. Pas daarna beslist u
              of u verdergaat.
            </p>
            <div class="btn-row">
              <a class="btn" href="contact.html">Een afspraak vragen</a>
              <a class="btn btn--ghost" href="tel:{tel_href}">{tel_display}</a>
            </div>
          </div>
          <div class="reveal">
            <div class="media media--arch framed">
              <img src="assets/img/gewelf.jpg" srcset="assets/img/gewelf-800.jpg 800w, assets/img/gewelf.jpg 1400w"
                   sizes="(max-width: 62rem) 0px, 30vw"
                   alt="" width="1400" height="787" loading="lazy" decoding="async">
            </div>
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
<meta name="theme-color" content="#2e4034">
<meta name="robots" content="{robots}">

<meta property="og:type" content="website">
<meta property="og:locale" content="nl_BE">
<meta property="og:site_name" content="{name} — {role}">
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

<div class="topbar">
  <div class="shell topbar__inner">
    <ul>
      <li>{street}, {postcode} {city}</li>
      <li><a href="tel:{tel_href}">{tel_display}</a></li>
      <li><a href="mailto:{email}">{email}</a></li>
    </ul>
    <span class="topbar__note">Enkel op afspraak &middot; Balie Leuven</span>
  </div>
</div>

<header class="site-header">
  <div class="shell site-header__inner">
    <a class="brand" href="index.html">
      <img class="brand__mark" src="assets/img/monogram.svg" alt="" width="40" height="40">
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
        <p style="margin-top:1.25rem;max-width:34ch">
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
    </div>

    <div class="site-footer__bottom">
      <p>&copy; {year} Veerle Borremans — Advocaat te Leuven</p>
      <nav aria-label="Juridische informatie">
        <a href="juridische-informatie.html">Juridische informatie</a>
        <a href="privacybeleid.html">Privacybeleid</a>
      </nav>
    </div>
  </div>
</footer>

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
            "\n    Zoek op 'tbc' in pages/ — zie INHOUD-TODO.md."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
