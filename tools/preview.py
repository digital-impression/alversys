#!/usr/bin/env python3
"""
Bouwt één zelfstandig HTML-bestand met de volledige site erin, om als
voorbeeld door te sturen naar de cliënte.

    python3 tools/preview.py [uitvoerbestand]

Alles zit in dat ene bestand: stylesheet, lettertypes en afbeeldingen worden
als data-URI ingesloten, en de dertien pagina's worden onder elkaar gezet met
een kleine router die op de link in de navigatie reageert. Er is dus geen
server nodig — dubbelklikken volstaat.

Dit is uitsluitend een presentatiebestand. De echte site blijft de losse
pagina's in de hoofdmap.
"""

from __future__ import annotations

import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "preview.html"

PAGE_ORDER = [
    "index.html",
    "over-mij.html",
    "rechtsdomeinen.html",
    "familierecht.html",
    "jeugdrecht.html",
    "personenrecht.html",
    "strafrecht.html",
    "bemiddeling.html",
    "tarieven.html",
    "contact.html",
    "juridische-informatie.html",
    "privacybeleid.html",
    "404.html",
]

PREVIEW_CSS = """
/* ---- alleen voor dit voorbeeldbestand ---- */
.pv-page { display: none; }
.pv-page.is-active { display: block; }

.pv-badge {
  position: fixed;
  left: 1rem;
  bottom: 1rem;
  z-index: 300;
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.6rem 1rem;
  border-radius: 999px;
  background: rgba(34, 48, 42, 0.94);
  -webkit-backdrop-filter: blur(8px);
  backdrop-filter: blur(8px);
  color: #f7f4ef;
  font-family: var(--sans);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  box-shadow: 0 12px 28px -18px rgba(28, 31, 29, 0.9);
}
.pv-badge::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #b08968;
}
@media (max-width: 40rem) {
  .pv-badge { font-size: 0.62rem; padding: 0.5rem 0.8rem; left: 0.75rem; bottom: 0.75rem; }
}
"""

ROUTER_JS = """
/* ---- kleine router, alleen in het voorbeeldbestand ---- */
(function () {
  var pages = document.querySelectorAll('.pv-page');
  var byId = {};
  Array.prototype.forEach.call(pages, function (p) { byId[p.id] = p; });

  function show(id, instant) {
    var target = byId[id] || byId['p-index'];
    Array.prototype.forEach.call(pages, function (p) { p.classList.remove('is-active'); });
    target.classList.add('is-active');

    document.querySelectorAll('.nav__link').forEach(function (a) {
      var match = a.getAttribute('href') === '#' + id.replace('p-', '');
      if (match) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });

    document.title = target.getAttribute('data-title');
    window.scrollTo({ top: 0, behavior: instant ? 'auto' : 'auto' });

    window.requestAnimationFrame(function () {
      target.querySelectorAll('.reveal').forEach(function (el, i) {
        el.classList.remove('is-visible');
        window.setTimeout(function () { el.classList.add('is-visible'); }, Math.min(i * 45, 400));
      });
    });
  }

  function fromHash() {
    var raw = (location.hash || '#index').slice(1);
    // interne ankers binnen een pagina laten we met rust
    if (byId['p' + '-' + raw]) show('p-' + raw, true);
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) return;
    var id = 'p-' + a.getAttribute('href').slice(1);
    if (!byId[id]) return; // gewoon anker op de pagina zelf
    e.preventDefault();
    if (location.hash !== a.getAttribute('href')) history.pushState(null, '', a.getAttribute('href'));
    show(id);
  });

  window.addEventListener('popstate', fromHash);
  fromHash();
  if (!location.hash) show('p-index', true);

  // in een voorbeeld wordt er niets verstuurd
  var form = document.querySelector('form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var note = form.querySelector('.pv-form-note') || document.createElement('p');
      note.className = 'pv-form-note form__note';
      note.style.color = '#85603f';
      note.textContent = 'Dit is een ontwerpvoorbeeld — het formulier verstuurt hier nog niets.';
      form.appendChild(note);
    });
  }
})();
"""


def data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def inline_css() -> str:
    css = (ROOT / "assets/css/style.css").read_text(encoding="utf-8")
    for font in sorted((ROOT / "assets/fonts").glob("*.woff2")):
        css = css.replace(
            f"url('../fonts/{font.name}')",
            f"url({data_uri(font, 'font/woff2')})",
        )
    return css + PREVIEW_CSS


def main() -> int:
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT

    index = (ROOT / "index.html").read_text(encoding="utf-8")
    body = index.split("<body>", 1)[1].split("</body>", 1)[0]
    chrome_top, rest = body.split('<main id="hoofdinhoud">', 1)
    _, chrome_bottom = rest.split("</main>", 1)
    chrome_bottom = chrome_bottom.replace(
        '<script src="assets/js/main.js" defer></script>', ""
    )

    blocks = []
    for name in PAGE_ORDER:
        html = (ROOT / name).read_text(encoding="utf-8")
        main_html = html.split('<main id="hoofdinhoud">', 1)[1].split("</main>", 1)[0]
        title = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
        page_id = "p-" + name.replace(".html", "")
        blocks.append(
            f'<div class="pv-page" id="{page_id}" data-title="{title}">{main_html}</div>'
        )

    doc = "\n".join(
        [chrome_top, '<main id="hoofdinhoud">', *blocks, "</main>", chrome_bottom]
    )

    # interne links worden ankers
    for name in PAGE_ORDER:
        doc = doc.replace(f'href="{name}"', f'href="#{name.replace(".html", "")}"')

    # srcset en sizes hebben in één bestand geen nut en zouden elk beeld
    # dubbel insluiten
    doc = re.sub(r'\s+(?:srcset|sizes)="[^"]*"', "", doc)

    # afbeeldingen insluiten
    for img in sorted((ROOT / "assets/img").glob("*.svg")):
        doc = doc.replace(f"assets/img/{img.name}", data_uri(img, "image/svg+xml"))

    # foto's: neem de kleinste beschikbare variant, anders wordt het bestand
    # onnodig zwaar voor wat een voorbeeld is
    fotos = sorted((ROOT / "assets/img").glob("*.jpg"))
    basissen = {p.stem.split("-")[0] for p in fotos}
    for basis in sorted(basissen):
        varianten = sorted(
            (p for p in fotos if p.stem.split("-")[0] == basis),
            key=lambda p: p.stat().st_size,
        )
        uri = data_uri(varianten[0], "image/jpeg")
        for p in varianten:
            doc = doc.replace(f"assets/img/{p.name}", uri)

    js = (ROOT / "assets/js/main.js").read_text(encoding="utf-8")

    out = (
        '<meta charset="utf-8">\n'
        "<title>Veerle Borremans</title>\n"
        f"<style>\n{inline_css()}\n</style>\n"
        f"{doc}\n"
        '<div class="pv-badge">Ontwerpvoorbeeld — nog geen live site</div>\n'
        f"<script>\n{js}\n{ROUTER_JS}\n</script>\n"
    )

    out_path.write_text(out, encoding="utf-8")
    kb = len(out.encode("utf-8")) / 1024
    print(f"  ✓ {out_path} ({kb:.0f} kB, {len(PAGE_ORDER)} pagina's)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
