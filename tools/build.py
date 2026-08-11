#!/usr/bin/env python3
"""
Jacobs Law — static site generator.

Renders the shared chrome (head, header, drawer, footer) around per-page
content so the eleven pages stay consistent. Output is plain HTML with no
runtime dependencies.

    python3 tools/build.py

Edit content here and re-run, or — if you'd rather hand the HTML to a CMS or
another developer — delete this script and edit the generated .html directly.
The site does not need it to run.
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.jacobs-law.be"

FIRM = "Jacobs Law"
STREET = "Populierenlaan 43"
CITY = "2630 Aartselaar"
TEL_DISPLAY = "+32 (0)3 844 95 00"
TEL_HREF = "+3238449500"
MAIL_L = "liesbet.jacobs@jacobs-law.be"
MAIL_M = "michelle.damen@jacobs-law.be"
INSTA = "https://www.instagram.com/jacobs_lawfirm/"
VAT = "BE 0669.531.513"

# --------------------------------------------------------------------------
# Icon vocabulary
#
# One family, one rule: linework plus a single brass diamond node. The diamond
# is the same mark that interrupts every hairline rule on the site and sits
# inside the logo, so the icons read as part of the identity rather than as
# bought-in clipart.
# --------------------------------------------------------------------------

ICON_OPEN = ('<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" '
             'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" '
             'aria-hidden="true" focusable="false">')

ICONS = {
    # A closed structure breached on one side, the diamond sitting in the gap:
    # an going concern that no longer holds.
    "faillissementen": ICON_OPEN + """
    <path d="M38 20V10H10v28h28v-6"/>
    <path d="M38 19.5 42.5 24 38 28.5 33.5 24Z" fill="currentColor" stroke="none"/>
  </svg>""",

    # A three-quarter turn returning to its starting point: recovery of a claim.
    "schulden": ICON_OPEN + """
    <path d="M38 24a14 14 0 1 1-14-14"/>
    <path d="M19 6.5 24 10l-5 3.5"/>
    <path d="M24 19.5 28.5 24 24 28.5 19.5 24Z" fill="currentColor" stroke="none"/>
  </svg>""",

    # Two facing brackets meeting on a diamond: terms agreed between parties.
    "burgerlijk-recht": ICON_OPEN + """
    <path d="M19 9H10v30h9"/>
    <path d="M29 9h9v30h-9"/>
    <path d="M24 18.5 29.5 24 24 29.5 18.5 24Z" fill="currentColor" stroke="none"/>
  </svg>""",

    # Two arcs sheltering a diamond: a household held together.
    "familierecht": ICON_OPEN + """
    <path d="M8 30a16 16 0 0 1 32 0"/>
    <path d="M16 30a8 8 0 0 1 16 0"/>
    <path d="M24 31.5 28.5 36 24 40.5 19.5 36Z" fill="currentColor" stroke="none"/>
  </svg>""",
}

ARROW = ('<svg class="btn__arrow" viewBox="0 0 15 10" fill="none" stroke="currentColor" '
         'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M0 5h13M9.5 1.5 13 5l-3.5 3.5"/></svg>')

ARROW_PLAIN = ARROW.replace('class="btn__arrow" ', '')

LOGO = """<svg class="brand__mark" viewBox="0 0 32 32" fill="none" aria-hidden="true" focusable="false">
      <path d="M16 3.5 28.5 16 16 28.5 3.5 16Z" stroke="currentColor" stroke-width="1.15"/>
      <path d="M0.5 16h31" stroke="#B08D57" stroke-width="1.15"/>
      <path d="M16 13.4 18.6 16 16 18.6 13.4 16Z" fill="#B08D57"/>
    </svg>"""

ICON_TEL = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M14.5 11.4v2.1a1 1 0 0 1-1.1 1 12.7 12.7 0 0 1-5.5-2 12.5 12.5 0 0 1-3.8-3.8 '
            '12.7 12.7 0 0 1-2-5.6 1 1 0 0 1 1-1.1h2.1a1 1 0 0 1 1 .9c.07.6.2 1.2.4 1.8a1 1 0 0 1-.23 '
            '1.05l-.9.9a10 10 0 0 0 3.8 3.8l.9-.9a1 1 0 0 1 1.05-.23c.58.2 1.18.33 1.8.4a1 1 0 0 1 .9 1Z"/></svg>')

ICON_INSTA = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.2" '
              'aria-hidden="true"><rect x="2" y="2" width="12" height="12" rx="3.6"/>'
              '<circle cx="8" cy="8" r="2.9"/><circle cx="11.6" cy="4.4" r=".85" fill="currentColor" stroke="none"/></svg>')

ICON_MAIL = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.2" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<rect x="1.5" y="3.5" width="13" height="9" rx="1.2"/><path d="m2 4.5 6 4.2 6-4.2"/></svg>')

RULE = '<div class="rule" role="presentation"><span class="rule__node"></span></div>'

# --------------------------------------------------------------------------
# Navigation
# --------------------------------------------------------------------------

DOMAINS = [
    ("faillissementen", "Faillissementen &amp; insolventie",
     "Curatele, nakende staking van betaling en begeleiding van ondernemers in moeilijkheden."),
    ("schulden", "Schulden &amp; invordering",
     "Onbetaalde facturen innen, betalingsregelingen uitwerken en schuldposities beheersbaar maken."),
    ("burgerlijk-recht", "Burgerlijk recht",
     "Huurrecht, contracten, betwiste facturen en de alledaagse geschillen die daaruit voortkomen."),
    ("familierecht", "Familierecht",
     "Echtscheiding, onderhoudsgeld, omgangsrecht en vereffening-verdeling — met de nodige omzichtigheid."),
]

NAV = [
    ("over-ons", "Over ons", None),
    ("domeinen", "Juridische domeinen", DOMAINS),
    ("tarieven", "Tarieven", None),
    ("contact", "Contact", None),
]


def nav_html(active):
    out = []
    for slug, label, children in NAV:
        if children:
            items = "".join(
                '<li><a href="{s}.html"><span class="index-num">0{i}</span>'
                '<span>{l}</span></a></li>'.format(s=c[0], l=c[1], i=n + 1)
                for n, c in enumerate(children)
            )
            is_active = active in [c[0] for c in children]
            out.append(
                '<div class="nav__item"><a class="nav__link" href="faillissementen.html"{cur}>'
                '{label}<svg class="nav__caret" viewBox="0 0 9 6" fill="none" stroke="currentColor" '
                'stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                '<path d="m1 1.5 3.5 3L8 1.5"/></svg></a>'
                '<ul class="nav__menu">{items}</ul></div>'.format(
                    label=label, items=items,
                    cur=' aria-current="page"' if is_active else "")
            )
        else:
            out.append(
                '<div class="nav__item"><a class="nav__link" href="{s}.html"{cur}>{l}</a></div>'.format(
                    s=slug, l=label, cur=' aria-current="page"' if active == slug else "")
            )
    return "".join(out)


def drawer_html():
    subs = "".join('<li><a href="{}.html">{}</a></li>'.format(c[0], c[1]) for c in DOMAINS)
    return """<div class="drawer" id="drawer" aria-hidden="true">
    <nav aria-label="Hoofdnavigatie (mobiel)">
      <ul>
        <li><a href="over-ons.html">Over ons</a></li>
        <li>
          <a href="faillissementen.html">Juridische domeinen</a>
          <ul class="drawer__sub">{subs}</ul>
        </li>
        <li><a href="tarieven.html">Tarieven</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
    </nav>
    <div class="drawer__foot">
      <a class="btn btn--on-ink" href="contact.html">Afspraak maken {arrow}</a>
      <a class="btn btn--ghost-ink" href="tel:{telh}">{teld}</a>
    </div>
    <p class="drawer__meta">{street}<br>{city}<br>
      <a href="mailto:{mail}">{mail}</a></p>
  </div>""".format(subs=subs, arrow=ARROW, telh=TEL_HREF, teld=TEL_DISPLAY,
                   street=STREET, city=CITY, mail=MAIL_L)


def header_html(active):
    return """<header class="header">
    <div class="wrap header__inner">
      <a class="brand" href="index.html" aria-label="{firm} — naar de startpagina">
        {logo}
        <span class="brand__text">
          <span class="brand__name">Jacobs Law</span>
          <span class="brand__sub">Advocaten</span>
        </span>
      </a>
      <nav class="nav" aria-label="Hoofdnavigatie">{nav}</nav>
      <div class="header__actions">
        <a class="header__tel" href="tel:{telh}">{icon}{teld}</a>
        <a class="btn btn--header" href="contact.html">Afspraak maken</a>
        <button class="burger" type="button" aria-expanded="false" aria-controls="drawer"
                aria-label="Menu openen en sluiten">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>
  {drawer}""".format(firm=FIRM, logo=LOGO, nav=nav_html(active), telh=TEL_HREF,
                     teld=TEL_DISPLAY, icon=ICON_TEL, drawer=drawer_html())


FOOTER = """<footer class="footer">
    <div class="wrap">
      <div class="footer__grid">
        <div>
          <a class="brand" href="index.html">
            {logo}
            <span class="brand__text">
              <span class="brand__name">Jacobs Law</span>
              <span class="brand__sub">Advocaten</span>
            </span>
          </a>
          <p class="footer__about">Advocatenkantoor te Aartselaar. Een frisse kijk op de zaak,
            heldere afspraken en een doelgerichte aanpak — voor ondernemingen en particulieren.</p>
          <div class="footer__social">
            <a href="{insta}" target="_blank" rel="noopener noreferrer" aria-label="Jacobs Law op Instagram">{ig}</a>
            <a href="mailto:{mail}" aria-label="Mail Jacobs Law">{ml}</a>
            <a href="tel:{telh}" aria-label="Bel Jacobs Law">{tl}</a>
          </div>
        </div>

        <div>
          <h4>Juridische domeinen</h4>
          <ul>{domain_links}</ul>
        </div>

        <div>
          <h4>Kantoor</h4>
          <ul>
            <li><a href="over-ons.html">Over ons</a></li>
            <li><a href="liesbet-jacobs.html">Mr. Liesbet Jacobs</a></li>
            <li><a href="michelle-damen.html">Mr. Michelle Damen</a></li>
            <li><a href="tarieven.html">Tarieven</a></li>
            <li><a href="contact.html">Contact &amp; afspraak</a></li>
          </ul>
        </div>

        <div>
          <h4>Contact</h4>
          <address>
            {street}<br>
            {city}<br><br>
            <a href="tel:{telh}">{teld}</a><br>
            <a href="mailto:{mail}">{mail}</a>
          </address>
        </div>
      </div>

      <div class="footer__bottom">
        <p style="margin:0">&copy; <span id="year">2026</span> Jacobs Law BV &middot; {vat}</p>
        <ul class="footer__legal">
          <li><a href="privacy-en-cookiebeleid.html">Privacy- en cookiebeleid</a></li>
          <li><a href="contact.html#klachten">Klachtenregeling</a></li>
        </ul>
      </div>
    </div>
  </footer>""".format(
    logo=LOGO, insta=INSTA, ig=ICON_INSTA, ml=ICON_MAIL, tl=ICON_TEL,
    mail=MAIL_L, telh=TEL_HREF, teld=TEL_DISPLAY, street=STREET, city=CITY, vat=VAT,
    domain_links="".join('<li><a href="{}.html">{}</a></li>'.format(d[0], d[1]) for d in DOMAINS),
)


# --------------------------------------------------------------------------
# Page shell
# --------------------------------------------------------------------------

FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect width='32' height='32' fill='%2314110E'/%3E"
    "%3Cpath d='M16 5.5 26.5 16 16 26.5 5.5 16Z' fill='none' stroke='%23F3EFE9' stroke-width='1.4'/%3E"
    "%3Cpath d='M2 16h28' stroke='%23B08D57' stroke-width='1.4'/%3E"
    "%3Cpath d='M16 13.2 18.8 16 16 18.8 13.2 16Z' fill='%23B08D57'/%3E%3C/svg%3E"
)


def page(slug, title, description, body, active=None, ink_hero=False, schema=""):
    active = active if active is not None else slug
    canonical = "{}/{}".format(SITE, "" if slug == "index" else slug + ".html")
    return """<!doctype html>
<html lang="nl-BE" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#14110E">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_BE">
<meta property="og:site_name" content="Jacobs Law">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{site}/assets/img/kantoor-gesprek.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{favicon}">
<link rel="preload" href="assets/fonts/fraunces-normal-300-600-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/instrument-sans-normal-400-700-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/fonts/fonts.css">
<link rel="stylesheet" href="assets/css/site.css">
{schema}
</head>
<body class="{bodyclass}">
  <a class="skip" href="#main">Naar de inhoud</a>
  {header}
  <main id="main">
{body}
  </main>
  {footer}
  <script src="assets/js/site.js" defer></script>
  <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
""".format(title=title, description=description, canonical=canonical, site=SITE,
           favicon=FAVICON, schema=schema, bodyclass="has-ink-hero" if ink_hero else "",
           header=header_html(active), body=body, footer=FOOTER)


def pagehead(crumb_label, h1, lead, extra=""):
    return """    <section class="pagehead">
      <div class="wrap">
        <ol class="crumbs">
          <li><a href="index.html">Home</a></li>
          <li aria-current="page">{crumb}</li>
        </ol>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
        {extra}
      </div>
    </section>
""".format(crumb=crumb_label, h1=h1, lead=lead, extra=extra)


CTA = """    <section class="section section--ink cta">
      <div class="wrap cta__inner">
        <div class="reveal">
          <p class="eyebrow">Een zaak voorleggen</p>
          <h2>Eerst even aftoetsen of we u kunnen helpen?</h2>
          <p class="lead">Een vrijblijvend consult duurt ongeveer een uur. U legt uw situatie voor,
            u krijgt een eerlijke inschatting en u weet meteen wat een verdere aanpak zou kosten.
            Kunnen wij u niet helpen, dan verwijzen wij u door naar een collega die dat wel kan.</p>
          <div class="cta__actions" style="margin-top:2rem">
            <a class="btn btn--on-ink" href="contact.html">Afspraak maken {arrow}</a>
            <a class="btn btn--ghost-ink" href="tel:{telh}">{teld}</a>
          </div>
        </div>
        <div class="reveal" data-delay="1">
          <div class="panel panel--ink">
            <p class="eyebrow" style="margin-bottom:1rem">Vrijblijvend consult</p>
            <div class="price">
              <span class="price__amount">&euro;110</span>
              <span class="price__unit">incl. btw</span>
            </div>
            <p style="font-size:.9375rem">Kennismaking en eerste mondeling advies. Bij ons is dat
              een vaste prijs, vooraf gekend — geen open einde.</p>
            <div class="rule" role="presentation" style="margin-block:1.5rem"><span class="rule__node"></span></div>
            <ul class="ticks">
              <li>Een eerlijke inschatting van uw slaagkansen</li>
              <li>Duidelijkheid over de te verwachten kosten</li>
              <li>Doorverwijzing als een collega beter geplaatst is</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
""".format(arrow=ARROW, telh=TEL_HREF, teld=TEL_DISPLAY)


# --------------------------------------------------------------------------
# Home
# --------------------------------------------------------------------------

def domain_rows():
    rows = []
    for i, (slug, title, blurb) in enumerate(DOMAINS):
        rows.append("""        <a class="domain reveal" href="{slug}.html">
          <span class="domain__icon" aria-hidden="true">{icon}</span>
          <span class="domain__title">
            <span class="index-num">0{n}</span>
            <h3>{title}</h3>
          </span>
          <span class="domain__body"><p>{blurb}</p></span>
          <span class="domain__go" aria-hidden="true">{arrow}</span>
        </a>""".format(slug=slug, icon=ICONS[slug], n=i + 1, title=title,
                       blurb=blurb, arrow=ARROW_PLAIN))
    return "\n".join(rows)


HOME_SCHEMA = """<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LegalService",
  "name": "Jacobs Law",
  "url": "{site}/",
  "telephone": "{tel}",
  "email": "{mail}",
  "image": "{site}/assets/img/kantoor-gesprek.jpg",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "{street}",
    "postalCode": "2630",
    "addressLocality": "Aartselaar",
    "addressCountry": "BE"
  }},
  "areaServed": "Provincie Antwerpen",
  "availableLanguage": "nl",
  "knowsAbout": [
    "Insolventierecht", "Faillissementen", "Invordering",
    "Burgerlijk recht", "Huurrecht", "Familierecht"
  ],
  "employee": [
    {{"@type": "Person", "name": "Liesbet Jacobs", "jobTitle": "Advocaat-vennoot"}},
    {{"@type": "Person", "name": "Michelle Damen", "jobTitle": "Advocaat"}}
  ]
}}
</script>""".format(site=SITE, tel=TEL_DISPLAY, mail=MAIL_L, street=STREET)


HOME = """    <section class="hero">
      <div class="hero__texture" aria-hidden="true"></div>
      <div class="hero__glow" aria-hidden="true"></div>
      <div class="wrap hero__inner">
        <div class="hero__grid">
          <div>
            <p class="eyebrow">Advocatenkantoor &middot; Aartselaar</p>
            <h1 class="display">Een frisse kijk<br>op de zaak.</h1>
            <p class="lead">Wij staan ondernemingen en particulieren bij in insolventie, invordering,
              burgerlijk recht en familierecht. Met heldere afspraken, snelle communicatie en
              een aanpak die op de zaak zelf gericht blijft.</p>
            <div class="hero__actions">
              <a class="btn btn--on-ink" href="contact.html">Vrijblijvend consult {arrow}</a>
              <a class="btn btn--ghost-ink" href="faillissementen.html">Onze domeinen</a>
            </div>
          </div>
          <div class="framed">
            <img src="assets/img/kantoor-gesprek.jpg" width="1600" height="1200"
                 alt="Een gesprek aan de lage tafel in het kantoor van Jacobs Law te Aartselaar."
                 fetchpriority="high" decoding="async">
          </div>
        </div>

        <dl class="credentials">
          <div><dt>2013</dt><dd>Curator ondernemings&shy;rechtbank Antwerpen</dd></div>
          <div><dt>2016 &middot; 2022</dt><dd>Ook afdeling Mechelen en Turnhout</dd></div>
          <div><dt>Peer&nbsp;Reviewed</dt><dd>Kwaliteitslabel Orde van Advocaten</dd></div>
          <div><dt>Collaboratief</dt><dd>Geaccrediteerd collaboratief advocaat</dd></div>
        </dl>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="grid grid--aside">
          <div class="reveal">
            <p class="eyebrow">Over het kantoor</p>
            <h2>Rechtsbijstand zonder<br>omhaal van woorden.</h2>
          </div>
          <div class="reveal" data-delay="1">
            <p class="lead" style="max-width:60ch">Jacobs Law is een advocatenkantoor in Aartselaar,
              net onder Antwerpen. Klein genoeg dat u telkens dezelfde advocaat aan de lijn krijgt,
              en gespecialiseerd genoeg om u in insolventie en familierecht echt vooruit te helpen.</p>
            <p>Wij nemen dossiers aan waarvan wij menen dat we er het verschil in kunnen maken.
              Kunnen wij u niet helpen, dan zeggen we dat en verwijzen we u door naar een collega
              die dat wel kan. Dat is voor iedereen de kortste weg.</p>

            <div class="rule" role="presentation"><span class="rule__node"></span></div>

            <blockquote class="quote">
              <p>Goede afspraken, een duidelijke en snelle communicatie evenals een doelgerichte aanpak.
                Dat is wat je van mij mag verwachten.</p>
              <cite>Mr. Liesbet Jacobs</cite>
            </blockquote>

            <div style="margin-top:2.25rem">
              <a class="tlink" href="over-ons.html">Meer over het kantoor {arrow}</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--tight section--sand">
      <div class="wrap">
        <div class="grid grid--split" style="align-items:stretch">
          <figure class="figure reveal">
            <img src="assets/img/kantoor-overleg.jpg" width="1600" height="1200" loading="lazy"
                 decoding="async" style="aspect-ratio:4/3"
                 alt="Overleg rond de vergadertafel in het kantoor te Aartselaar.">
            <figcaption>Populierenlaan 43, Aartselaar</figcaption>
          </figure>
          <div class="reveal" data-delay="1" style="align-self:center">
            <p class="eyebrow">Waarom cliënten hier terechtkomen</p>
            <h3 style="margin-bottom:1.5rem">Een dossier is pas goed behandeld als u begrijpt wat er gebeurt.</h3>
            <ul class="ticks">
              <li><strong>Eén vast aanspreekpunt.</strong> U hoeft uw verhaal niet elke keer opnieuw te doen.</li>
              <li><strong>Vooraf gekende kosten.</strong> Het eerste consult is een vaste prijs; daarna weet u waar u aan toe bent.</li>
              <li><strong>Minnelijk waar het kan.</strong> Een regeling die standhoudt is doorgaans meer waard dan een vonnis.</li>
              <li><strong>Procederen waar het moet.</strong> En dan grondig voorbereid.</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="reveal" style="margin-bottom:clamp(2.5rem,1.5rem + 3vw,4rem)">
          <p class="eyebrow">Juridische domeinen</p>
          <h2 style="max-width:18ch">Waarin dit kantoor thuis is.</h2>
        </div>
        <div class="domains">
{domain_rows}
        </div>
      </div>
    </section>

    <section class="section section--ink">
      <div class="wrap">
        <div class="grid grid--split-wide">
          <div class="reveal">
            <p class="eyebrow">Insolventie &amp; curatele</p>
            <h2 style="margin-bottom:1.5rem">Wij kennen het faillissement<br>van beide kanten.</h2>
            <p class="lead">Sinds 2013 staat mr. Jacobs op de lijst van curatoren bij de
              ondernemingsrechtbank te Antwerpen, sinds 2016 ook te Mechelen en sinds 2022 te Turnhout.
              Dat is een zeldzaam vertrekpunt: wie faillissementen afwikkelt in opdracht van de rechtbank,
              weet als geen ander wat een ondernemer vooraf beter anders had gedaan.</p>
            <p>Het is haar overtuiging dat het voor alle betrokkenen — en niet in het minst voor de
              maatschappij — van groot belang is dat zowel de aanloop naar een faillissement als het
              verloop ervan correct wordt afgehandeld. Ondernemers worden gewezen op de mogelijkheden
              en geholpen bij de moeilijkheden van een nakend faillissement.</p>
            <div style="margin-top:2.25rem">
              <a class="tlink" href="faillissementen.html">Faillissementen &amp; insolventie {arrow}</a>
            </div>
          </div>
          <div class="reveal" data-delay="1">
            <div class="panel panel--ink">
              <h3 style="margin-bottom:1.5rem">Aanstellingen &amp; mandaten</h3>
              <dl class="dl">
                <div><dt>Ondernemingsrechtbank Antwerpen</dt><dd><strong>sinds 2013</strong></dd></div>
                <div><dt>Afdeling Mechelen</dt><dd><strong>sinds 2016</strong></dd></div>
                <div><dt>Afdeling Turnhout</dt><dd><strong>sinds 2022</strong></dd></div>
                <div><dt>Bestuurslid vzw Pro Mandato</dt><dd><strong>sinds 2017</strong></dd></div>
              </dl>
              <p style="margin-top:1.5rem;font-size:.875rem">Als bestuurslid van Pro Mandato behartigt
                mr. Jacobs samen met de overige leden van de raad van bestuur de belangen van de
                curatoren in het gehele arrondissement Antwerpen.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="reveal" style="margin-bottom:clamp(2.5rem,1.5rem + 3vw,4rem)">
          <p class="eyebrow">Het kantoor</p>
          <h2 style="max-width:16ch">Twee advocaten, één aanspreekpunt.</h2>
        </div>
        <div class="people">
          <a class="person reveal" href="liesbet-jacobs.html">
            <div class="person__media">
              <img src="assets/img/portret-liesbet.jpg" width="860" height="1075" loading="lazy"
                   decoding="async" class="focus-right" alt="Portret van mr. Liesbet Jacobs.">
            </div>
            <p class="person__role">Advocaat-vennoot &middot; Balie Antwerpen</p>
            <h3 class="person__name">Liesbet Jacobs</h3>
            <p class="person__desc">Studeerde rechten aan de Universiteit Gent met een specialisatie
              in het ondernemingsrecht. Curator, collaboratief advocaat en oprichter van het kantoor.</p>
            <span class="tlink">Biografie {arrow}</span>
          </a>
          <a class="person reveal" data-delay="1" href="michelle-damen.html">
            <div class="person__media">
              <img src="assets/img/portret-michelle.jpg" width="860" height="1075" loading="lazy"
                   decoding="async" class="focus-left" alt="Portret van mr. Michelle Damen.">
            </div>
            <p class="person__role">Advocaat &middot; Balie Antwerpen</p>
            <h3 class="person__name">Michelle Damen</h3>
            <p class="person__desc">Studeerde in 2017 met onderscheiding af aan de Vrije Universiteit
              Brussel, specialisatie burgerlijk en procesrecht. Vervoegde het kantoor in 2020.</p>
            <span class="tlink">Biografie {arrow}</span>
          </a>
        </div>
      </div>
    </section>

    <section class="section section--ink section--tight">
      <div class="wrap">
        <div class="reveal" style="margin-bottom:clamp(2rem,1.4rem + 2vw,3rem)">
          <p class="eyebrow">Zo verloopt het</p>
          <h2 style="max-width:16ch">Van eerste telefoon tot afgerond dossier.</h2>
        </div>
        <div class="steps">
          <div class="step reveal">
            <span class="step__num">01 &mdash; Kennismaking</span>
            <h3>U legt de zaak voor</h3>
            <p>Een vrijblijvend consult van ongeveer een uur, aan een vaste prijs van &euro;110 incl. btw.
              U brengt mee wat u heeft; wij zeggen u eerlijk hoe de zaak ervoor staat.</p>
          </div>
          <div class="step reveal" data-delay="1">
            <span class="step__num">02 &mdash; Afspraken</span>
            <h3>Wij leggen vast wat we doen</h3>
            <p>Een concreet voorstel van aanpak, met de te verwachten kosten en doorlooptijd erbij.
              Geen open einde, geen verrassingen achteraf.</p>
          </div>
          <div class="step reveal" data-delay="2">
            <span class="step__num">03 &mdash; Uitvoering</span>
            <h3>Wij houden u op de hoogte</h3>
            <p>Minnelijk waar dat kan, procederen waar dat moet. U krijgt bericht bij elke stap
              die er werkelijk toe doet — en u kunt ons bellen.</p>
          </div>
        </div>
      </div>
    </section>

{cta}
""".format(arrow=ARROW_PLAIN, domain_rows=domain_rows(), cta=CTA)


# --------------------------------------------------------------------------
# Over ons
# --------------------------------------------------------------------------

OVER_ONS = pagehead(
    "Over ons",
    "Een klein kantoor dat zijn dossiers zelf kent.",
    "Jacobs Law werd in 2017 opgericht te Aartselaar. Wij zijn met twee advocaten — en dat is "
    "een bewuste keuze: uw dossier wordt behandeld door de advocaat met wie u het besprak."
) + """
    <section class="section">
      <div class="wrap">
        <div class="grid grid--aside">
          <div class="reveal">
            <p class="eyebrow">Het kantoor</p>
          </div>
          <div class="prose reveal" data-delay="1">
            <p class="lead">Een advocaat inschakelen is zelden een aangename stap. Er gaat meestal iets
              aan vooraf: een klant die niet betaalt, een onderneming die het niet haalt, een relatie die
              vastloopt. Wat u op zo'n moment nodig hebt, is iemand die de zaak snel doorgrondt en u in
              gewone taal vertelt waar u staat.</p>

            <p>Dat is waar dit kantoor voor gemaakt is. Wij werken zonder tussenlagen: u spreekt met de
              advocaat die uw dossier behandelt, niet met een medewerker die het nog moet inlezen. Wij
              antwoorden op telefoon en e-mail, ook wanneer het antwoord is dat er nog niets nieuws is.</p>

            <p>Het kantoor is bewust breed genoeg om een gezin door een echtscheiding te loodsen én
              scherp genoeg om een ondernemer door een nakend faillissement te begeleiden. Die twee
              werelden liggen dichter bij elkaar dan het lijkt: in beide gevallen gaat het over mensen
              die willen weten wat er nu gaat gebeuren.</p>

            <h2>Waar wij op letten</h2>
            <ul>
              <li><strong>Heldere afspraken vooraf.</strong> Over de aanpak, over de kosten, over wat
                realistisch is. Een cliënt die verrast wordt door een factuur, is een cliënt die niet
                goed werd ingelicht.</li>
              <li><strong>Snelle communicatie.</strong> Termijnen in het recht zijn hard. Wij houden ze,
                en wij laten u tijdig weten wanneer er van u iets verwacht wordt.</li>
              <li><strong>Een doelgerichte aanpak.</strong> Niet elk geschil verdient een procedure. Wij
                wegen af wat een uitspraak u werkelijk zou opleveren, en zeggen het wanneer dat weinig is.</li>
              <li><strong>Doorverwijzen zonder omwegen.</strong> Het credo van het kantoor is dat, wanneer
                wij u niet kunnen helpen, u wordt doorverwezen naar een collega die dat wél kan. Vragen
                staat steeds vrij.</li>
            </ul>

            <h2>Kwaliteit, controleerbaar</h2>
            <p>Het kantoor behaalde in 2020 het label <strong>Peer Reviewed</strong> van de Orde van
              Advocaten — een kwaliteitstoets waarbij confraters de werking van het kantoor doorlichten.
              Beide advocaten zijn ingeschreven aan de <strong>balie van Antwerpen</strong> en volgen de
              deontologische regels en permanente vorming die daarbij horen.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--tight section--sand">
      <div class="wrap">
        <div class="grid grid--split">
          <figure class="figure reveal">
            <img src="assets/img/kantoor-werkplek.jpg" width="1600" height="1200" loading="lazy"
                 decoding="async" style="aspect-ratio:4/3" alt="Werkplek met zicht op de tuin.">
            <figcaption>Het kantoor werkt vanuit een rustige, lichte omgeving</figcaption>
          </figure>
          <figure class="figure reveal" data-delay="1">
            <img src="assets/img/kantoor-trap.jpg" width="1600" height="1200" loading="lazy"
                 decoding="async" style="aspect-ratio:4/3" alt="Detail van de trap en houten lamellenwand.">
            <figcaption>Aartselaar, op tien minuten van de Antwerpse ring</figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="reveal" style="margin-bottom:clamp(2.5rem,1.5rem + 3vw,4rem)">
          <p class="eyebrow">Het team</p>
          <h2 style="max-width:16ch">Wie uw dossier behandelt.</h2>
        </div>
        <div class="people">
          <a class="person reveal" href="liesbet-jacobs.html">
            <div class="person__media">
              <img src="assets/img/portret-liesbet.jpg" width="860" height="1075" loading="lazy"
                   decoding="async" class="focus-right" alt="Portret van mr. Liesbet Jacobs.">
            </div>
            <p class="person__role">Advocaat-vennoot &middot; Balie Antwerpen</p>
            <h3 class="person__name">Liesbet Jacobs</h3>
            <p class="person__desc">Ondernemingsrecht (UGent), curator te Antwerpen, Mechelen en
              Turnhout, geaccrediteerd collaboratief advocaat en bestuurslid van vzw Pro Mandato.</p>
            <span class="tlink">Biografie {arrow}</span>
          </a>
          <a class="person reveal" data-delay="1" href="michelle-damen.html">
            <div class="person__media">
              <img src="assets/img/portret-michelle.jpg" width="860" height="1075" loading="lazy"
                   decoding="async" class="focus-left" alt="Portret van mr. Michelle Damen.">
            </div>
            <p class="person__role">Advocaat &middot; Balie Antwerpen</p>
            <h3 class="person__name">Michelle Damen</h3>
            <p class="person__desc">Burgerlijk en procesrecht (VUB, met onderscheiding). Verbintenissen-,
              aansprakelijkheids-, verkeers- en huurrecht en het personen- en familierecht.</p>
            <span class="tlink">Biografie {arrow}</span>
          </a>
        </div>
      </div>
    </section>

{cta}
""".format(arrow=ARROW_PLAIN, cta=CTA)


# --------------------------------------------------------------------------
# Biographies
# --------------------------------------------------------------------------

def bio_page(name, role, portrait, focus, lead, prose, facts, mail, other_slug,
             other_name, other_desc):
    fact_rows = "".join(
        '<div><dt>{}</dt><dd><strong>{}</strong></dd></div>'.format(k, v) for k, v in facts
    )
    return pagehead(name, name, lead) + """
    <section class="section">
      <div class="wrap">
        <div class="grid grid--aside">
          <div class="reveal">
            <div class="framed" style="margin-bottom:2.5rem">
              <img src="assets/img/{portrait}" width="1200" height="1500" loading="lazy"
                   decoding="async" class="{focus}"
                   style="aspect-ratio:4/4.9;object-fit:cover" alt="Portret van {name}.">
            </div>
            <p class="person__role" style="margin-bottom:.75rem">{role}</p>
            <p style="font-size:.9375rem;color:var(--fg-muted);margin-bottom:1.5rem">
              <a href="mailto:{mail}" style="color:var(--brass-deep)">{mail}</a><br>
              <a href="tel:{telh}" style="color:inherit;text-decoration:none">{teld}</a>
            </p>
            <a class="btn btn--ghost" href="contact.html">Afspraak maken {arrow}</a>
          </div>

          <div class="reveal" data-delay="1">
            <div class="prose">
{prose}
            </div>

            <div class="rule" role="presentation"><span class="rule__node"></span></div>

            <h2 style="font-size:var(--t-h3);margin-bottom:1.5rem">In het kort</h2>
            <dl class="dl">{facts}</dl>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--tight section--sand">
      <div class="wrap wrap--narrow">
        <p class="eyebrow">Ook op kantoor</p>
        <div class="grid grid--split" style="align-items:center">
          <div>
            <h2 style="font-size:var(--t-h3);margin-bottom:1rem">{other_name}</h2>
            <p style="color:var(--fg-muted);font-size:var(--t-small)">{other_desc}</p>
            <div style="margin-top:1.5rem"><a class="tlink" href="{other_slug}.html">Biografie {arrow}</a></div>
          </div>
        </div>
      </div>
    </section>

{cta}
""".format(portrait=portrait, focus=focus, name=name, role=role, mail=mail,
           telh=TEL_HREF, teld=TEL_DISPLAY, arrow=ARROW_PLAIN, prose=prose,
           facts=fact_rows, other_name=other_name, other_desc=other_desc,
           other_slug=other_slug, cta=CTA)


LIESBET = bio_page(
    name="Mr. Liesbet Jacobs",
    role="Advocaat-vennoot &middot; Balie Antwerpen",
    portrait="portret-liesbet.jpg",
    focus="focus-right",
    mail=MAIL_L,
    lead="Oprichter van het kantoor. Curator bij de ondernemingsrechtbank te Antwerpen, "
         "Mechelen en Turnhout, en geaccrediteerd collaboratief advocaat.",
    prose="""              <blockquote class="quote" style="margin-bottom:2.5rem">
                <p>Goede afspraken, een duidelijke en snelle communicatie evenals een doelgerichte
                  aanpak. Dat is wat je van mij mag verwachten.</p>
              </blockquote>

              <p>Aan de Universiteit Gent studeerde ik rechten met een specialisatie in het
                ondernemingsrecht. Die keuze heeft mijn praktijk gestuurd: het merendeel van mijn
                dossiers heeft op de een of andere manier met ondernemen te maken — en met wat er
                gebeurt wanneer ondernemen misloopt.</p>

              <p>In 2013 werd ik benoemd tot curator bij de ondernemingsrechtbank te Antwerpen,
                afdeling Antwerpen, in 2016 bij de afdeling Mechelen en in 2022 bij de afdeling
                Turnhout. Als curator wikkel ik faillissementen af in opdracht van de rechtbank.
                Dat werk levert een inzicht op dat je van buitenaf niet krijgt: je ziet precies
                welke beslissingen een onderneming in de maanden vóór het faillissement de das
                omdeden — en welke er nog te redden viel.</p>

              <p>Dat inzicht zet ik in voor ondernemers die er nog niet zijn. Wie tijdig komt,
                heeft doorgaans meer opties dan hij denkt. Wie te laat komt, moet weten waar hij
                persoonlijk aansprakelijk voor is. Beide gesprekken voer ik liever vroeg dan laat.</p>

              <p>Nadien werd een accreditatie van collaboratief advocaat behaald. In de
                collaboratieve praktijk verbinden alle partijen en hun advocaten zich er
                uitdrukkelijk toe om tot een akkoord te komen zonder te procederen. Dat is
                een veeleisende manier van werken, maar bij familiale dossiers vaak de enige
                die de verhoudingen intact laat.</p>

              <p>Als bestuurslid van de vzw Pro Mandato verdedig ik daarnaast, samen met de
                overige leden van de raad van bestuur, sinds 2017 de belangen van de curatoren
                in het gehele arrondissement Antwerpen.</p>""",
    facts=[
        ("Opleiding", "Rechten, Universiteit Gent"),
        ("Specialisatie", "Ondernemingsrecht"),
        ("Curator &mdash; afdeling Antwerpen", "2013"),
        ("Curator &mdash; afdeling Mechelen", "2016"),
        ("Curator &mdash; afdeling Turnhout", "2022"),
        ("Bestuurslid vzw Pro Mandato", "2017"),
        ("Collaboratief advocaat", "geaccrediteerd"),
        ("Balie", "Antwerpen"),
    ],
    other_slug="michelle-damen",
    other_name="Mr. Michelle Damen",
    other_desc="Burgerlijk en procesrecht (VUB, met onderscheiding). Verbintenissen-, "
               "aansprakelijkheids-, verkeers- en huurrecht en het personen- en familierecht.",
)

MICHELLE = bio_page(
    name="Mr. Michelle Damen",
    role="Advocaat &middot; Balie Antwerpen",
    portrait="portret-michelle.jpg",
    focus="focus-left",
    mail=MAIL_M,
    lead="Burgerlijk en procesrecht. Verbintenissen-, aansprakelijkheids-, verkeers- en "
         "huurrecht, en het personen- en familierecht.",
    prose="""              <p class="lead">Michelle Damen studeerde in 2017 met onderscheiding af als
                master in de rechten, specialisatie burgerlijk en procesrecht, aan de Vrije
                Universiteit Brussel.</p>

              <p>Vervolgens begon zij haar stage aan de Antwerpse balie bij het advocatenkantoor
                Hopland &amp; De Lei, onder begeleiding van haar stagemeester mr. Marc
                Bartholomeeusen. Sedert 2020 vervoegde zij onder meer het kantoor van mr. Jacobs.</p>

              <p>Tot haar voorkeursmateries behoren het algemeen verbintenissenrecht, het
                aansprakelijkheidsrecht, het verkeersrecht, het huurrecht en het personen- en
                familierecht.</p>

              <p>Het zijn stuk voor stuk domeinen waarin de feiten het pleit beslechten. Een
                aanrijding, een huurgeschil, een discussie over een geleverde prestatie: de
                juridische regel is doorgaans niet het probleem — de bewijsvoering wel. Daarom
                begint elk dossier hier met een nauwgezette reconstructie van wat er precies
                gebeurd is, en met de vraag welke stukken dat kunnen staven.</p>

              <p>In het personen- en familierecht komt daar iets bij. Die dossiers gaan over
                mensen die na afloop nog met elkaar verder moeten — als ouders, als buren, als
                ex-partners met een gemeenschappelijke woning. Een uitspraak die op papier klopt
                maar in de praktijk niet werkt, is dan weinig waard.</p>""",
    facts=[
        ("Opleiding", "Master in de rechten, VUB (2017)"),
        ("Onderscheiding", "cum laude"),
        ("Specialisatie", "Burgerlijk en procesrecht"),
        ("Stage", "Hopland &amp; De Lei, Antwerpen"),
        ("Stagemeester", "mr. Marc Bartholomeeusen"),
        ("Bij Jacobs Law", "sinds 2020"),
        ("Balie", "Antwerpen"),
    ],
    other_slug="liesbet-jacobs",
    other_name="Mr. Liesbet Jacobs",
    other_desc="Ondernemingsrecht (UGent), curator te Antwerpen, Mechelen en Turnhout, "
               "geaccrediteerd collaboratief advocaat en bestuurslid van vzw Pro Mandato.",
)


# --------------------------------------------------------------------------
# Practice areas
# --------------------------------------------------------------------------

def domain_page(slug, h1, lead, prose, sidebar_title, sidebar_items, image, image_alt, caption):
    others = [d for d in DOMAINS if d[0] != slug]
    other_cards = "".join(
        """          <a class="card" href="{s}.html">
            <span class="card__icon" aria-hidden="true">{icon}</span>
            <h3>{t}</h3>
            <p>{b}</p>
            <span class="tlink" style="margin-top:auto">Lees meer {arrow}</span>
          </a>""".format(s=d[0], icon=ICONS[d[0]], t=d[1], b=d[2], arrow=ARROW_PLAIN)
        for d in others
    )
    ticks = "".join("<li>{}</li>".format(i) for i in sidebar_items)

    return pagehead("Juridische domeinen", h1, lead, extra="""
        <div style="margin-top:2rem;display:flex;gap:.9rem;flex-wrap:wrap">
          <a class="btn" href="contact.html">Vrijblijvend consult {arrow}</a>
          <a class="btn btn--ghost" href="tel:{telh}">{teld}</a>
        </div>""".format(arrow=ARROW, telh=TEL_HREF, teld=TEL_DISPLAY)) + """
    <section class="section">
      <div class="wrap">
        <div class="grid grid--aside">
          <div class="reveal">
            <span class="domain__icon" aria-hidden="true" style="width:56px;height:56px;display:block;margin-bottom:1.5rem">{icon}</span>
            <div class="panel" style="position:sticky;top:6.5rem">
              <h2 style="font-size:1.15rem;margin-bottom:1.25rem">{sidebar_title}</h2>
              <ul class="ticks">{ticks}</ul>
            </div>
          </div>
          <div class="prose reveal" data-delay="1">
{prose}
          </div>
        </div>
      </div>
    </section>

    <section class="section section--tight section--sand">
      <div class="wrap">
        <figure class="figure reveal">
          <img src="assets/img/{image}" width="1600" height="1200" loading="lazy" decoding="async"
               style="aspect-ratio:21/9" alt="{image_alt}">
          <figcaption>{caption}</figcaption>
        </figure>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="reveal" style="margin-bottom:2.5rem">
          <p class="eyebrow">Andere domeinen</p>
          <h2 style="max-width:18ch">Waarin dit kantoor nog thuis is.</h2>
        </div>
        <div class="cards cards--3 reveal" data-delay="1">
{other_cards}
        </div>
      </div>
    </section>

{cta}
""".format(icon=ICONS[slug], sidebar_title=sidebar_title, ticks=ticks, prose=prose,
           image=image, image_alt=image_alt, caption=caption,
           other_cards=other_cards, cta=CTA)


FAILLISSEMENTEN = domain_page(
    slug="faillissementen",
    h1="Faillissementen &amp; insolventie",
    lead="Voor ondernemers die het water aan de lippen voelen staan, en voor wie al te maken "
         "kreeg met het faillissement van een tegenpartij. Wij kennen de procedure van beide zijden.",
    sidebar_title="Waarvoor u hier terecht kunt",
    sidebar_items=[
        "Begeleiding bij een nakend faillissement",
        "Aangifte van staking van betaling",
        "Gerechtelijke reorganisatie (WCO)",
        "Bestuurdersaansprakelijkheid",
        "Aangifte van schuldvordering in een faillissement",
        "Kwijtschelding voor de gefailleerde natuurlijke persoon",
        "Betwistingen met de curator",
    ],
    image="kantoor-werkplek.jpg",
    image_alt="Werkplek in het kantoor te Aartselaar.",
    caption="Wie tijdig komt, heeft doorgaans meer opties dan hij denkt",
    prose="""            <p class="lead">Sinds 2013 is mr. Jacobs opgenomen op de lijst van curatoren te
              Antwerpen en nadien te Mechelen en Turnhout. Het is haar overtuiging dat het voor alle
              betrokkenen — en niet in het minst voor de maatschappij — van groot belang is dat zowel
              de aanloop naar een faillissement als het verloop ervan correct wordt afgehandeld.</p>

            <p>Ondernemers worden gewezen op de mogelijkheden en geholpen bij de moeilijkheden van
              een nakend faillissement. Een goed advies is in die omstandigheden goud waard.</p>

            <h2>Komt u op tijd, dan valt er nog te kiezen</h2>
            <p>De meeste ondernemers die hier binnenstappen, komen laat. Begrijpelijk — er gaat een
              periode aan vooraf waarin men hoopt dat het nog keert. Maar het verschil tussen een
              gesprek in maand drie en een gesprek in maand tien is groot. In het eerste geval
              bespreken we een gerechtelijke reorganisatie, een afbetalingsplan met de fiscus of een
              geordende stopzetting. In het tweede geval bespreken we hoofdzakelijk hoe uw persoonlijke
              aansprakelijkheid beperkt kan blijven.</p>

            <p>De wet legt een bestuurder bovendien een termijn op: de staking van betaling moet
              binnen de maand worden aangegeven. Wie die termijn laat verstrijken terwijl hij wist
              of moest weten dat de onderneming er niet meer bovenop kwam, loopt een reëel risico
              op persoonlijke aansprakelijkheid voor het tekort.</p>

            <h2>Als curator, en als raadsman</h2>
            <p>Een curator wordt door de rechtbank aangesteld om een faillissement af te wikkelen:
              hij of zij maakt het actief te gelde, gaat de schuldvorderingen na en verdeelt de
              opbrengst volgens de wettelijke rangorde. Dat is geen partijdige rol — de curator
              behartigt de belangen van de boedel, niet die van de gefailleerde of van één
              schuldeiser.</p>

            <p>Voor u betekent dat twee dingen. Ten eerste: in dossiers waarin dit kantoor als
              curator optreedt, kunnen wij u niet als raadsman bijstaan. Ten tweede: in alle andere
              dossiers hebt u een raadsman die exact weet hoe de curator aan de overzijde zal
              redeneren, welke stukken hij zal opvragen en waar hij op zal doorbijten.</p>

            <h2>Bent u schuldeiser?</h2>
            <p>Ook wie geconfronteerd wordt met het faillissement van een klant of leverancier, kan
              hier terecht. Wij doen de aangifte van schuldvordering, gaan na of u een voorrecht of
              een eigendomsvoorbehoud kunt inroepen, en beoordelen of er aanknopingspunten zijn voor
              een vordering tegen de bestuurders. In veel gevallen is de vraag niet óf u iets krijgt,
              maar in welke rang u staat — en dat is precies waar het verschil zit.</p>

            <h2>Wat u meebrengt naar het eerste gesprek</h2>
            <ul>
              <li>De laatste neergelegde jaarrekening en de meest recente boekhoudkundige stand</li>
              <li>Een overzicht van de openstaande schulden, met vermelding van RSZ en fiscus</li>
              <li>De lopende kredieten en de eventuele persoonlijke zekerheden die u stelde</li>
              <li>De briefwisseling van schuldeisers, deurwaarders of de rechtbank</li>
            </ul>
            <p>Is een deel daarvan er niet, kom dan toch. Met een onvolledig beeld kunnen we nog
              altijd zeggen welke stap eerst gezet moet worden.</p>""",
)

SCHULDEN = domain_page(
    slug="schulden",
    h1="Schulden &amp; invordering",
    lead="Onbetaalde facturen innen, betalingsregelingen uitwerken en een schuldpositie weer "
         "beheersbaar maken — voor wie moet innen én voor wie moet betalen.",
    sidebar_title="Waarvoor u hier terecht kunt",
    sidebar_items=[
        "Invordering van onbetaalde facturen",
        "Ingebrekestelling en aanmaning",
        "Procedure voor de vrederechter of ondernemingsrechtbank",
        "Betwisting van een vordering die u wordt aangerekend",
        "Onderhandelen van een afbetalingsplan",
        "Verzet tegen beslag",
        "Collectieve schuldenregeling",
    ],
    image="kantoor-overleg.jpg",
    image_alt="Overleg rond de vergadertafel in het kantoor.",
    caption="Een regeling die standhoudt is doorgaans meer waard dan een vonnis",
    prose="""            <p class="lead">Betalingsproblemen zijn zelden een geïsoleerd feit. Een klant die
              niet betaalt, brengt uw eigen leveranciers in de knel; een schuld die aanzwelt met
              interesten en kosten, groeit sneller aan dan het inkomen waarmee ze moet worden
              afbetaald. In beide richtingen geldt: hoe vroeger er wordt ingegrepen, hoe meer er
              nog te regelen valt.</p>

            <h2>Moet u innen</h2>
            <p>Een onbetaalde factuur is in de eerste plaats een commercieel probleem en pas daarna
              een juridisch probleem. Daarom beginnen wij zelden met een dagvaarding. Een
              onderbouwde ingebrekestelling, met een correcte berekening van de verwijlinteresten en
              het schadebeding, brengt een aanzienlijk deel van de dossiers al tot betaling — tegen
              een fractie van de kostprijs van een procedure.</p>

            <p>Helpt dat niet, dan wegen wij af of procederen zinvol is. Die afweging gaat niet
              alleen over uw gelijk, maar ook over de solvabiliteit van uw tegenpartij: een vonnis
              tegen wie niets heeft, is een dure bevestiging van uw gelijk. Wij zeggen u dat op
              voorhand, niet achteraf.</p>

            <p>Voor invorderingsdossiers werkt het kantoor op forfaitaire basis, zodat u van bij de
              aanvang weet wat de inning u kost. Ondernemingen met terugkerende invorderingen kunnen
              daarover een vaste afspraak maken.</p>

            <h2>Moet u betalen</h2>
            <p>Wordt ú aangesproken, dan is de eerste vraag altijd of de vordering wel klopt. Is de
              prestatie geleverd zoals afgesproken? Is de factuur tijdig geprotesteerd? Is het
              schadebeding niet buitensporig — de rechter kan een onredelijk beding matigen of
              nietig verklaren. En is de vordering intussen niet verjaard?</p>

            <p>Klopt de vordering wel, dan is een realistisch afbetalingsplan doorgaans in ieders
              belang: de schuldeiser krijgt uitzicht op betaling, u vermijdt beslag en oplopende
              kosten. Wij onderhandelen dat plan en leggen het vast, zodat het achteraf niet in
              twijfel getrokken kan worden.</p>

            <h2>Wanneer het echt niet meer gaat</h2>
            <p>Voor wie structureel niet meer rondkomt, bestaat de collectieve schuldenregeling: een
              procedure voor de arbeidsrechtbank waarbij een schuldbemiddelaar uw inkomsten beheert,
              uw schuldeisers worden bevroren en er wordt toegewerkt naar een aanzuiveringsregeling.
              Dat is een ingrijpende stap met strikte voorwaarden, en niet in elke situatie de juiste.
              Wij gaan met u na of u ervoor in aanmerking komt en wat het concreet betekent.</p>

            <h2>Beslag en uitvoering</h2>
            <p>Ligt er al beslag, dan is er meestal minder tijd dan gedacht maar meer ruimte dan
              gevreesd. Bepaalde goederen zijn niet vatbaar voor beslag, op loon geldt een beschermd
              minimum, en tegen een onregelmatig gelegd beslag kan verzet worden aangetekend. Neem
              in dat geval snel contact op — bij uitvoeringsmaatregelen lopen de termijnen kort.</p>""",
)

BURGERLIJK = domain_page(
    slug="burgerlijk-recht",
    h1="Burgerlijk recht",
    lead="Huurrecht, contracten, betwiste facturen en de alledaagse geschillen die daaruit "
         "voortkomen. Het recht dat het vaakst aan de deur klopt.",
    sidebar_title="Waarvoor u hier terecht kunt",
    sidebar_items=[
        "Huurrecht &mdash; woninghuur en handelshuur",
        "Opmaak en nazicht van contracten",
        "Betwisting van facturen",
        "Inning van vorderingen",
        "Aansprakelijkheid en schadevergoeding",
        "Verkeersrecht en verkeersongevallen",
        "Geschillen met aannemers en leveranciers",
    ],
    image="kantoor-onthaal.jpg",
    image_alt="De lichte onthaalruimte van het kantoor.",
    caption="Kunnen wij u niet helpen, dan verwijzen wij u door naar wie dat wel kan",
    prose="""            <p class="lead">Het algemeen burgerlijk recht wordt behandeld op het
              advocatenkantoor Jacobs Law. Daaronder vallen onder meer het huurrecht, het
              contractenrecht, de betwisting van facturen, de inning van vorderingen enzovoort.</p>

            <h2>Huurrecht</h2>
            <p>Huurgeschillen lopen zelden over het principe en bijna altijd over de uitvoering:
              achterstallige huur, een betwiste plaatsbeschrijving, schade bij het einde van de
              huur, werken die de verhuurder had moeten uitvoeren, of een opzeg die niet in de
              juiste vorm werd gegeven. Woninghuur is bovendien geregionaliseerd — in Vlaanderen
              geldt het Vlaams Woninghuurdecreet, met eigen regels over waarborg, opzegtermijnen en
              vergoedingen.</p>

            <p>Voor handelshuur gelden weer andere regels, met dwingende bepalingen over de duur en
              de hernieuwing. Een handelshuurhernieuwing die niet tijdig en niet in de juiste vorm
              wordt gevraagd, is onherroepelijk verloren. Dat is een van de weinige domeinen waar
              een gemiste termijn werkelijk niet meer recht te zetten valt.</p>

            <h2>Contracten</h2>
            <p>Het beste moment om een contract door een advocaat te laten lezen, is vóór de
              ondertekening. Dat kost een fractie van wat een geschil erover later kost. Wij nemen
              overeenkomsten na op de punten die in de praktijk problemen geven: wie draagt welk
              risico, wat gebeurt er bij wanprestatie, hoe kan er opgezegd worden, welke rechter is
              bevoegd en welk recht is van toepassing.</p>

            <p>Is het contract al gesloten en loopt het mis, dan komt het aan op interpretatie en op
              bewijs. Wat is er precies afgesproken, en wat kunt u daarvan aantonen? Ook hier geldt
              dat de e-mails uit de beginperiode vaak beslissender zijn dan het contract zelf.</p>

            <h2>Betwiste facturen en invordering</h2>
            <p>Een factuur die niet tijdig wordt geprotesteerd, wordt tussen ondernemingen geacht
              aanvaard te zijn. Dat is een van de meest onderschatte regels in het handelsverkeer —
              en een van de vaakst doorslaggevende. Bent u het niet eens met een factuur, protesteer
              dan schriftelijk, gemotiveerd en snel.</p>
            <p>Voor de inning van uw eigen openstaande facturen verwijzen wij naar
              <a href="schulden.html">schulden en invordering</a>, waar het kantoor op forfaitaire
              basis werkt.</p>

            <h2>Als wij niet de juiste zijn</h2>
            <p>Het credo van het kantoor is dat, wanneer wij u niet kunnen helpen, u wordt
              doorverwezen naar een collega die dat wel kan. Vragen staat steeds vrij; wij helpen u
              graag aan de juiste specialist. Dat kost u niets en het scheelt u een omweg — het
              alternatief, een advocaat die een dossier aanneemt buiten zijn vertrouwde terrein, is
              in niemands voordeel.</p>""",
)

FAMILIERECHT = domain_page(
    slug="familierecht",
    h1="Familierecht",
    lead="Echtscheiding, onderhoudsgeld, omgangsrecht en vereffening-verdeling. Dossiers die "
         "een persoonlijke aanpak vragen en dus maatwerk zijn.",
    sidebar_title="Waarvoor u hier terecht kunt",
    sidebar_items=[
        "Echtscheiding door onderlinge toestemming (EOT)",
        "Echtscheiding op grond van onherstelbare ontwrichting",
        "Onderhoudsgeld voor kinderen en tussen ex-partners",
        "Verblijfsregeling en omgangsrecht",
        "Vereffening-verdeling van het huwelijksvermogen",
        "Feitelijke samenwoning en wettelijke samenwoning",
        "Collaboratieve onderhandeling",
    ],
    image="kantoor-gesprek.jpg",
    image_alt="Een gesprek aan de lage tafel in het kantoor.",
    caption="Zulke dossiers vragen een persoonlijke aanpak en zijn dus maatwerk",
    prose="""            <p class="lead">De laatste jaren heeft het kantoor zich bekwaamd in het afwikkelen
              van echtscheidingen, procedures betreffende onderhoudsgeld voor kinderen, discussies
              over omgangsrecht, echtelijke moeilijkheden en vereffening-verdeling. Zulke dossiers
              vragen een persoonlijke aanpak en zijn dus maatwerk.</p>

            <h2>Twee wegen uit een huwelijk</h2>
            <p>Wie uit de echt wil scheiden, heeft in België in wezen twee wegen. Bij een
              <strong>echtscheiding door onderlinge toestemming</strong> maken beide partners vooraf
              een volledige regeling op — over de kinderen, de woning, het vermogen en het
              onderhoudsgeld — en bekrachtigt de rechtbank die. Dat is doorgaans sneller, goedkoper
              en aanzienlijk minder belastend.</p>

            <p>Lukt dat niet, dan blijft de <strong>echtscheiding op grond van onherstelbare
              ontwrichting</strong>. Die kan al na korte tijd worden uitgesproken wanneer beide
              partijen ze vragen, en na een langere feitelijke scheiding wanneer één partij ze
              vraagt. De echtscheiding zelf is dan zelden het twistpunt; de discussies gaan over
              wat erna komt.</p>

            <h2>De kinderen eerst, ook procedureel</h2>
            <p>Verblijfsregeling en onderhoudsgeld worden beoordeeld door de familierechtbank, met
              het belang van het kind als leidraad. Gelijkmatig verdeeld verblijf is het wettelijke
              uitgangspunt, maar geen automatisme: leeftijd, schoolafstand, werkregimes en de
              onderlinge verstandhouding wegen mee.</p>

            <p>Onderhoudsgeld voor kinderen wordt berekend op basis van de middelen van beide ouders
              en de reële kosten van het kind. Die berekening is minder vrijblijvend dan vaak wordt
              gedacht — wie ze correct opbouwt en documenteert, staat sterker dan wie een bedrag
              vooropstelt. Wijzigen de omstandigheden nadien wezenlijk, dan kan de regeling worden
              herzien.</p>

            <h2>Vereffening-verdeling</h2>
            <p>Het vermogensrechtelijke luik is doorgaans het langste en het technischste. Wat is
              gemeenschappelijk en wat is eigen? Welke vergoedingen zijn er verschuldigd tussen de
              vermogens, bijvoorbeeld wanneer eigen gelden in de gezinswoning werden geïnvesteerd?
              Wat gebeurt er met het onverdeelde onroerend goed en met het openstaande krediet?
              Deze dossiers verlopen via een notaris-vereffenaar, en de kwaliteit van de aangifte
              van boedelbeschrijving bepaalt in grote mate de uitkomst.</p>

            <h2>Collaboratief onderhandelen</h2>
            <p>Mr. Jacobs is geaccrediteerd collaboratief advocaat. In die werkwijze verbinden beide
              partijen en hun advocaten zich er contractueel toe om tot een akkoord te komen zónder
              te procederen — en trekken de advocaten zich terug indien het toch tot een procedure
              komt. Dat legt echt gewicht in de schaal van het overleg. Waar er kinderen zijn en de
              ouders na de scheiding nog jaren met elkaar verder moeten, is dat vaak de aanpak die
              op termijn het meeste oplevert.</p>

            <h2>Wat u van ons mag verwachten</h2>
            <p>Familiedossiers hebben de neiging te escaleren op momenten dat niemand daar baat bij
              heeft. Wij zullen u zeggen wanneer een standpunt juridisch houdbaar is maar praktisch
              onverstandig, en wanneer een compromis dat vandaag zuur smaakt u over vijf jaar veel
              zal hebben bespaard. En wanneer er wél geprocedeerd moet worden, doen we dat grondig.</p>""",
)


# --------------------------------------------------------------------------
# Tarieven
# --------------------------------------------------------------------------

TARIEVEN = pagehead(
    "Tarieven",
    "Wat het kost, voordat u begint.",
    "Onduidelijkheid over erelonen is de meest gehoorde klacht over advocaten. Daarom zetten "
    "wij onze uitgangspunten hier op papier — en bevestigen wij ze schriftelijk voordat wij "
    "aan uw dossier beginnen."
) + """
    <section class="section">
      <div class="wrap">
        <div class="grid grid--split" style="align-items:start">
          <div class="reveal">
            <div class="panel panel--ink">
              <p class="eyebrow" style="margin-bottom:1rem">Het eerste gesprek</p>
              <div class="price">
                <span class="price__amount">&euro;110</span>
                <span class="price__unit">incl. btw &middot; vaste prijs</span>
              </div>
              <p style="margin-top:1rem">Vrijblijvend consult: kennismaking en eerste mondeling
                advies. Ongeveer een uur. U weet nadien of u een zaak hebt, wat een verdere aanpak
                zou inhouden en wat die ongeveer zou kosten.</p>
              <div class="rule" role="presentation" style="margin-block:1.75rem"><span class="rule__node"></span></div>
              <a class="btn btn--on-ink" href="contact.html" style="width:100%;justify-content:center">
                Consult inplannen {arrow}</a>
            </div>
          </div>

          <div class="prose reveal" data-delay="1">
            <h2 style="margin-top:0">Hoe wij rekenen</h2>
            <p>Een advocaat wordt vergoed voor twee zaken: het <strong>ereloon</strong> — de
              vergoeding voor het geleverde werk — en de <strong>kosten</strong>, zoals
              dagvaardingskosten, griffierechten, aangetekende zendingen en verplaatsingen. Die
              worden altijd afzonderlijk aangerekend, zodat u ziet waarvoor u betaalt.</p>

            <p>Voor de meeste dossiers werken wij aan een uurtarief. Voor invorderingen werken wij
              op forfaitaire basis: u weet dan vooraf exact wat de inning van een openstaande
              vordering u kost. Voor grotere of terugkerende opdrachten kunnen andere afspraken
              worden gemaakt — dat bespreken we tijdens het eerste consult.</p>

            <p>Bij aanvang van het dossier ontvangt u een schriftelijke bevestiging van de gemaakte
              afspraken. Tijdens de behandeling werken wij met tussentijdse provisies, zodat de
              eindafrekening nooit een verrassing is.</p>
          </div>
        </div>

        <div class="rule" role="presentation"><span class="rule__node"></span></div>

        <div class="grid grid--aside">
          <div class="reveal">
            <p class="eyebrow">Overzicht</p>
            <h2>Tarieven in het kort</h2>
          </div>
          <div class="reveal" data-delay="1">
            <dl class="dl">
              <div>
                <dt>Vrijblijvend consult<br><span style="font-weight:400;font-size:var(--t-small);color:var(--fg-muted)">Kennismaking en eerste mondeling advies</span></dt>
                <dd><strong>&euro;110</strong> incl. btw</dd>
              </div>
              <div>
                <dt>Ereloon<br><span style="font-weight:400;font-size:var(--t-small);color:var(--fg-muted)">Naargelang aard en complexiteit van het dossier</span></dt>
                <dd>vanaf <strong>&euro;125</strong> excl. btw / uur</dd>
              </div>
              <div>
                <dt>Invordering van facturen<br><span style="font-weight:400;font-size:var(--t-small);color:var(--fg-muted)">Vooraf gekende prijs per dossier</span></dt>
                <dd><strong>forfaitair</strong></dd>
              </div>
              <div>
                <dt>Kosten<br><span style="font-weight:400;font-size:var(--t-small);color:var(--fg-muted)">Griffierechten, dagvaarding, zendingen, verplaatsingen</span></dt>
                <dd>volgens <strong>werkelijke kost</strong></dd>
              </div>
            </dl>
            <p class="form__note" style="margin-top:1.75rem">Alle bedragen zijn indicatief en gelden
              tot herziening. Het tarief dat op uw dossier van toepassing is, wordt bij aanvang
              schriftelijk bevestigd.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--tight section--sand">
      <div class="wrap">
        <div class="reveal" style="margin-bottom:2.5rem">
          <p class="eyebrow">Goed om te weten</p>
          <h2 style="max-width:20ch">Mogelijk betaalt u niet alles zelf.</h2>
        </div>
        <div class="cards cards--3">
          <div class="card reveal">
            <h3>Rechtsbijstands&shy;verzekering</h3>
            <p>Veel gezins- en autopolissen bevatten een rechtsbijstandsluik dat het ereloon van uw
              advocaat geheel of gedeeltelijk dekt — ook bij verkeers-, huur- en contractgeschillen.
              U behoudt daarbij de vrije keuze van advocaat. Breng uw polis mee naar het eerste
              gesprek; wij gaan de dekking na.</p>
          </div>
          <div class="card reveal" data-delay="1">
            <h3>Juridische tweedelijnsbijstand</h3>
            <p>Wie onder bepaalde inkomensgrenzen valt, kan aanspraak maken op een geheel of
              gedeeltelijk kosteloze advocaat via het Bureau voor Juridische Bijstand van de balie.
              Wij zeggen u tijdens het eerste gesprek of u daarvoor in aanmerking komt en hoe u de
              aanvraag indient.</p>
          </div>
          <div class="card reveal" data-delay="2">
            <h3>Rechtsplegings&shy;vergoeding</h3>
            <p>Wint u de procedure, dan wordt de tegenpartij doorgaans veroordeeld tot een
              rechtsplegingsvergoeding: een forfaitaire tegemoetkoming in uw advocaatkosten. Die dekt
              zelden het volledige ereloon, maar drukt de eindfactuur wel merkbaar.</p>
          </div>
        </div>
      </div>
    </section>

{cta}
""".format(arrow=ARROW, cta=CTA)


# --------------------------------------------------------------------------
# Contact
# --------------------------------------------------------------------------

MAPS_Q = "Populierenlaan+43,+2630+Aartselaar,+Belgi%C3%AB"

CONTACT = pagehead(
    "Contact",
    "Leg uw zaak voor.",
    "Bel ons, mail ons of laat hieronder uw gegevens achter. Wij nemen contact op om een "
    "afspraak in te plannen — doorgaans nog dezelfde of de eerstvolgende werkdag."
) + """
    <section class="section">
      <div class="wrap">
        <div class="grid grid--aside">

          <div class="reveal">
            <ul class="contact-list">
              <li>
                <p class="contact-list__label">Kantoor</p>
                <p class="contact-list__value">{street}<br>{city}<br>België</p>
                <p style="margin-top:1rem">
                  <a class="tlink" href="https://www.google.com/maps/search/?api=1&amp;query={q}"
                     target="_blank" rel="noopener noreferrer">Route berekenen {arrow}</a>
                </p>
              </li>
              <li>
                <p class="contact-list__label">Telefoon</p>
                <p class="contact-list__value"><a href="tel:{telh}">{teld}</a></p>
              </li>
              <li>
                <p class="contact-list__label">E-mail</p>
                <p class="contact-list__value" style="font-size:1.0625rem;line-height:1.9">
                  <a href="mailto:{mail_l}">{mail_l}</a><br>
                  <a href="mailto:{mail_m}">{mail_m}</a>
                </p>
              </li>
              <li>
                <p class="contact-list__label">Bereikbaarheid</p>
                <p style="font-size:var(--t-small);color:var(--fg-muted)">Consultaties uitsluitend
                  op afspraak. Wij zijn telefonisch en per e-mail bereikbaar tijdens de kantooruren;
                  zit een van ons op zitting, dan bellen wij dezelfde dag terug.</p>
              </li>
              <li>
                <p class="contact-list__label">Volg ons</p>
                <p style="font-size:var(--t-small)">
                  <a href="{insta}" target="_blank" rel="noopener noreferrer"
                     style="color:var(--brass-deep)">Instagram &mdash; @jacobs_lawfirm</a></p>
              </li>
            </ul>
          </div>

          <div class="reveal" data-delay="1">
            <div class="panel">
              <p class="eyebrow">Afspraak aanvragen</p>
              <h2 style="font-size:var(--t-h3);margin-bottom:.75rem">Vertel ons kort waar het over gaat</h2>
              <p style="font-size:var(--t-small);color:var(--fg-muted);margin-bottom:2rem">
                Velden met een <abbr title="verplicht" style="text-decoration:none;color:var(--brass-deep)">*</abbr>
                zijn verplicht. Stuur nog geen vertrouwelijke stukken mee — dat doen we na de kennismaking,
                via een beveiligd kanaal.</p>

              <form class="form" name="contact" method="POST" data-netlify="true"
                    netlify-honeypot="bot-field" action="/bedankt.html">
                <input type="hidden" name="form-name" value="contact">
                <p hidden><label>Laat dit veld leeg: <input name="bot-field"></label></p>

                <div class="form__row">
                  <div class="field">
                    <label for="naam">Naam <abbr title="verplicht">*</abbr></label>
                    <input id="naam" name="naam" type="text" autocomplete="name" required>
                  </div>
                  <div class="field">
                    <label for="telefoon">Telefoon <abbr title="verplicht">*</abbr></label>
                    <input id="telefoon" name="telefoon" type="tel" autocomplete="tel" required>
                  </div>
                </div>

                <div class="field">
                  <label for="email">E-mailadres <abbr title="verplicht">*</abbr></label>
                  <input id="email" name="email" type="email" autocomplete="email" required>
                </div>

                <div class="field">
                  <label for="domein">Waarover gaat het?</label>
                  <select id="domein" name="domein">
                    <option value="">Kies een domein &mdash; of laat open</option>
                    <option>Faillissementen &amp; insolventie</option>
                    <option>Schulden &amp; invordering</option>
                    <option>Burgerlijk recht</option>
                    <option>Familierecht</option>
                    <option>Iets anders</option>
                  </select>
                </div>

                <div class="field">
                  <label for="bericht">Uw vraag <abbr title="verplicht">*</abbr></label>
                  <textarea id="bericht" name="bericht" required
                    placeholder="Enkele zinnen volstaan. Vermeld gerust of er een termijn loopt."></textarea>
                  <p class="field__hint">Loopt er een dagvaarding, een zitting of een andere termijn?
                    Bel ons dan meteen op {teld}.</p>
                </div>

                <label class="consent">
                  <input type="checkbox" name="akkoord" required>
                  <span>Ik ga ermee akkoord dat Jacobs Law mijn gegevens gebruikt om op deze vraag te
                    antwoorden, zoals beschreven in het
                    <a href="privacy-en-cookiebeleid.html">privacy- en cookiebeleid</a>.</span>
                </label>

                <div>
                  <button class="btn" type="submit">Aanvraag versturen {arrow}</button>
                </div>

                <p class="form__note">Een aanvraag via dit formulier is geen cliëntenrelatie en stuit
                  geen verjarings- of beroepstermijn. Die ontstaat pas wanneer wij de opdracht
                  uitdrukkelijk hebben bevestigd.</p>
              </form>
            </div>
          </div>

        </div>
      </div>
    </section>

    <section class="section section--tight section--sand">
      <div class="wrap">
        <div class="grid grid--split">
          <figure class="figure reveal">
            <img src="assets/img/kantoor-onthaal.jpg" width="1600" height="1200" loading="lazy"
                 decoding="async" style="aspect-ratio:4/3" alt="De onthaalruimte van het kantoor.">
            <figcaption>U wordt ontvangen op de Populierenlaan</figcaption>
          </figure>
          <div class="reveal" data-delay="1" style="align-self:center">
            <p class="eyebrow">Hoe u er raakt</p>
            <h3 style="margin-bottom:1.5rem">Aartselaar, net onder Antwerpen.</h3>
            <ul class="ticks">
              <li><strong>Met de wagen.</strong> Vanaf de A12 richting Boom, afrit Aartselaar. Parkeren kan voor de deur.</li>
              <li><strong>Vanuit Antwerpen.</strong> Ongeveer een kwartier buiten de spits, via de A12.</li>
              <li><strong>Met het openbaar vervoer.</strong> Bus vanaf Antwerpen-Berchem tot Aartselaar; vandaar te voet.</li>
            </ul>
            <div style="margin-top:2rem">
              <a class="btn btn--ghost" href="https://www.google.com/maps/search/?api=1&amp;query={q}"
                 target="_blank" rel="noopener noreferrer">Openen in Google Maps {arrow2}</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--tight" id="klachten">
      <div class="wrap">
        <div class="grid grid--aside">
          <div class="reveal">
            <p class="eyebrow">Klachtenregeling</p>
            <h2 style="font-size:var(--t-h3)">Niet tevreden over onze dienstverlening?</h2>
          </div>
          <div class="prose reveal" data-delay="1">
            <p>Laat het ons in de eerste plaats zelf weten. De meeste klachten gaan over
              communicatie of over de aanrekening, en die zijn doorgaans in een gesprek uit de
              wereld. Richt uw klacht aan de advocaat die uw dossier behandelt, of schriftelijk aan
              het kantoor op het adres hierboven.</p>
            <p>Komt u er met ons niet uit, dan kunt u zich wenden tot de <strong>Orde van Advocaten
              te Antwerpen</strong>, waarbij beide advocaten van dit kantoor zijn ingeschreven.
              Voor consumenten bestaat daarnaast de <strong>Ombudsdienst Consumentengeschillen
              Advocatuur</strong>, een erkende buitengerechtelijke geschillenregeling
              (<a href="https://www.ligeca.be" target="_blank" rel="noopener noreferrer">ligeca.be</a>).</p>
            <p>Op de overeenkomst tussen u en het kantoor is het Belgische recht van toepassing;
              geschillen behoren tot de bevoegdheid van de rechtbanken van het gerechtelijk
              arrondissement Antwerpen.</p>
          </div>
        </div>
      </div>
    </section>
""".format(street=STREET, city=CITY, telh=TEL_HREF, teld=TEL_DISPLAY, mail_l=MAIL_L,
           mail_m=MAIL_M, insta=INSTA, arrow=ARROW, arrow2=ARROW, q=MAPS_Q)


BEDANKT = """    <section class="pagehead">
      <div class="wrap">
        <ol class="crumbs">
          <li><a href="index.html">Home</a></li>
          <li aria-current="page">Bedankt</li>
        </ol>
        <h1>Uw aanvraag is verstuurd.</h1>
        <p class="lead">Wij nemen contact op om een afspraak in te plannen — doorgaans nog dezelfde
          of de eerstvolgende werkdag. Loopt er ondertussen een termijn, bel ons dan gerust op
          <a href="tel:{telh}" style="color:var(--brass-deep)">{teld}</a>.</p>
        <div style="margin-top:2rem;display:flex;gap:.9rem;flex-wrap:wrap">
          <a class="btn" href="index.html">Terug naar de startpagina {arrow}</a>
          <a class="btn btn--ghost" href="tarieven.html">Tarieven bekijken</a>
        </div>
      </div>
    </section>
""".format(telh=TEL_HREF, teld=TEL_DISPLAY, arrow=ARROW)


# --------------------------------------------------------------------------
# Privacy
# --------------------------------------------------------------------------

PRIVACY = pagehead(
    "Privacy- en cookiebeleid",
    "Privacy- en cookiebeleid",
    "Hoe Jacobs Law omgaat met uw persoonsgegevens, en welke cookies deze website plaatst."
) + """
    <section class="section">
      <div class="wrap">
        <div class="prose reveal">
          <p class="form__note" style="margin-bottom:2.5rem">Deze tekst is een werkversie. Laat ze
            vóór publicatie nazien en aanvullen door het kantoor, zodat ze aansluit bij de eigen
            verwerkingen, bewaartermijnen en verwerkers.</p>

          <h2 style="margin-top:0">1. Verwerkings&shy;verantwoordelijke</h2>
          <p>Jacobs Law BV, met kantoor te {street}, {city}, België — ondernemingsnummer {vat}.
            Voor vragen over dit beleid of over uw gegevens: <a href="mailto:{mail}">{mail}</a> of
            <a href="tel:{telh}">{teld}</a>.</p>

          <h2>2. Welke gegevens wij verwerken</h2>
          <ul>
            <li><strong>Gegevens die u zelf verstrekt</strong> via het contactformulier, per e-mail
              of telefonisch: naam, contactgegevens en de inhoud van uw vraag.</li>
            <li><strong>Dossiergegevens</strong> van cliënten: alle gegevens die nodig zijn om de
              opdracht uit te voeren, met inbegrip van gegevens van tegenpartijen en derden.</li>
            <li><strong>Technische gegevens</strong> die uw browser automatisch meestuurt bij een
              bezoek aan deze website.</li>
          </ul>

          <h2>3. Waarvoor en op welke grondslag</h2>
          <ul>
            <li><strong>Uitvoering van de overeenkomst</strong> — de behandeling van uw dossier en
              de facturatie daarvan.</li>
            <li><strong>Wettelijke verplichting</strong> — onder meer de anti-witwaswetgeving, de
              boekhoudwetgeving en de deontologische regels van de Orde van Advocaten.</li>
            <li><strong>Gerechtvaardigd belang</strong> — de beveiliging van onze systemen en de
              opvolging van vragen die ons worden gesteld.</li>
            <li><strong>Toestemming</strong> — voor niet-noodzakelijke cookies, en voor
              communicatie waarvoor u zich uitdrukkelijk hebt opgegeven.</li>
          </ul>

          <h2>4. Beroepsgeheim</h2>
          <p>Advocaten zijn gebonden door het beroepsgeheim. Wat u ons toevertrouwt, wordt niet
            gedeeld met derden, behoudens wanneer dat noodzakelijk is voor de uitvoering van de
            opdracht (bijvoorbeeld met een gerechtsdeurwaarder, een notaris of de rechtbank) of
            wanneer de wet ons daartoe verplicht.</p>

          <h2>5. Bewaartermijn</h2>
          <p>Dossiergegevens worden bewaard gedurende de wettelijke en deontologische
            bewaartermijnen die op advocatendossiers van toepassing zijn. Gegevens uit
            contactaanvragen die niet tot een dossier leiden, worden verwijderd zodra de vraag is
            afgehandeld.</p>

          <h2>6. Uw rechten</h2>
          <p>U hebt het recht op inzage, verbetering, verwijdering en overdraagbaarheid van uw
            gegevens, en het recht om zich te verzetten tegen of de beperking te vragen van bepaalde
            verwerkingen. Deze rechten zijn beperkt in de mate dat het beroepsgeheim of een
            wettelijke bewaarplicht zich ertegen verzet. Een aanvraag richt u aan
            <a href="mailto:{mail}">{mail}</a>.</p>
          <p>Bent u niet tevreden over de afhandeling, dan kunt u klacht indienen bij de
            <a href="https://www.gegevensbeschermingsautoriteit.be" target="_blank"
               rel="noopener noreferrer">Gegevensbeschermingsautoriteit</a>, Drukpersstraat 35,
            1000 Brussel.</p>

          <h2>7. Cookies</h2>
          <p>Deze website plaatst geen cookies. Er worden geen tracking- of advertentiecookies
            gebruikt, er wordt geen bezoekersprofiel opgebouwd en er wordt geen inhoud van sociale
            media of kaartendiensten ingesloten. Ook de lettertypes worden vanaf onze eigen server
            geladen en niet bij een externe aanbieder opgehaald, zodat uw IP-adres bij een bezoek
            aan deze website niet aan derden wordt doorgegeven.</p>
          <p>Wordt later toch webstatistiek of een ingesloten kaart toegevoegd, dan hoort daar een
            voorafgaande toestemmingsbanner bij en moet deze paragraaf worden aangepast.</p>

          <h2>8. Wijzigingen</h2>
          <p>Dit beleid kan worden aangepast. De meest recente versie staat steeds op deze pagina.</p>
        </div>
      </div>
    </section>
""".format(street=STREET, city=CITY, vat=VAT, mail=MAIL_L, telh=TEL_HREF, teld=TEL_DISPLAY)


# --------------------------------------------------------------------------
# Render
# --------------------------------------------------------------------------

PAGES = [
    ("index", "Jacobs Law &mdash; Advocatenkantoor te Aartselaar",
     "Advocatenkantoor Jacobs Law in Aartselaar. Insolventie en faillissementen, schulden en "
     "invordering, burgerlijk recht en familierecht. Vrijblijvend consult aan een vaste prijs.",
     HOME, "index", True, HOME_SCHEMA),

    ("over-ons", "Over ons &mdash; Jacobs Law",
     "Jacobs Law is een advocatenkantoor in Aartselaar met twee advocaten. Heldere afspraken, "
     "snelle communicatie en een doelgerichte aanpak.",
     OVER_ONS, "over-ons", False, ""),

    ("liesbet-jacobs", "Mr. Liesbet Jacobs &mdash; Jacobs Law",
     "Mr. Liesbet Jacobs: ondernemingsrecht (UGent), curator bij de ondernemingsrechtbank te "
     "Antwerpen, Mechelen en Turnhout, geaccrediteerd collaboratief advocaat.",
     LIESBET, "over-ons", False, ""),

    ("michelle-damen", "Mr. Michelle Damen &mdash; Jacobs Law",
     "Mr. Michelle Damen: burgerlijk en procesrecht (VUB). Verbintenissen-, aansprakelijkheids-, "
     "verkeers- en huurrecht en het personen- en familierecht.",
     MICHELLE, "over-ons", False, ""),

    ("faillissementen", "Faillissementen &amp; insolventie &mdash; Jacobs Law",
     "Begeleiding bij een nakend faillissement, gerechtelijke reorganisatie, "
     "bestuurdersaansprakelijkheid en aangifte van schuldvordering. Curator sinds 2013.",
     FAILLISSEMENTEN, "faillissementen", False, ""),

    ("schulden", "Schulden &amp; invordering &mdash; Jacobs Law",
     "Invordering van onbetaalde facturen op forfaitaire basis, betwisting van vorderingen, "
     "afbetalingsplannen, beslag en collectieve schuldenregeling.",
     SCHULDEN, "schulden", False, ""),

    ("burgerlijk-recht", "Burgerlijk recht &mdash; Jacobs Law",
     "Huurrecht, contracten, betwiste facturen, aansprakelijkheid en verkeersrecht bij "
     "advocatenkantoor Jacobs Law te Aartselaar.",
     BURGERLIJK, "burgerlijk-recht", False, ""),

    ("familierecht", "Familierecht &mdash; Jacobs Law",
     "Echtscheiding, onderhoudsgeld, verblijfsregeling en vereffening-verdeling. Ook "
     "collaboratieve onderhandeling met een geaccrediteerd collaboratief advocaat.",
     FAMILIERECHT, "familierecht", False, ""),

    ("tarieven", "Tarieven &mdash; Jacobs Law",
     "Vrijblijvend consult aan &euro;110 incl. btw. Ereloon, kosten, forfaitaire invordering, "
     "rechtsbijstandsverzekering en juridische tweedelijnsbijstand.",
     TARIEVEN, "tarieven", False, ""),

    ("contact", "Contact &mdash; Jacobs Law, Aartselaar",
     "Populierenlaan 43, 2630 Aartselaar. Bel +32 (0)3 844 95 00 of vraag online een afspraak aan.",
     CONTACT, "contact", False, ""),

    ("bedankt", "Bedankt &mdash; Jacobs Law",
     "Uw aanvraag is goed ontvangen.",
     BEDANKT, "contact", False, ""),

    ("privacy-en-cookiebeleid", "Privacy- en cookiebeleid &mdash; Jacobs Law",
     "Hoe Jacobs Law omgaat met persoonsgegevens en welke cookies deze website plaatst.",
     PRIVACY, None, False, ""),
]


def main():
    written = []
    for slug, title, desc, body, active, ink, schema in PAGES:
        html = page(slug, title, desc, body, active=active, ink_hero=ink, schema=schema)
        path = os.path.join(ROOT, slug + ".html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        written.append(slug + ".html")

    # sitemap
    urls = "".join(
        "  <url><loc>{}/{}</loc></url>\n".format(SITE, "" if s == "index" else s + ".html")
        for s, *_ in PAGES if s != "bedankt"
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                 + urls + "</urlset>\n")

    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write("User-agent: *\nAllow: /\n\nSitemap: {}/sitemap.xml\n".format(SITE))

    print("Gegenereerd: " + ", ".join(written) + ", sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
