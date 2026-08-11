#!/usr/bin/env python3
"""
DS Comfort — partial-assembler.

De site is bewust "gewone" statische HTML: elk .html-bestand in de hoofdmap is
volledig zelfstandig en werkt zonder buildstap, zonder Node en zonder framework.

Om te vermijden dat de header/footer op zes plaatsen uiteen gaat lopen, staan
die gedeelde blokken in _partials/. Dit script giet ze in elke pagina, tussen
markeringen zoals:

    <!--HEADER-->   ...ingevoegde inhoud...   <!--/HEADER-->

Het script is idempotent: het mag zo vaak draaien als u wil. Bewerk dus
_partials/*.html en draai daarna:

    python3 build.py

Bewerkt u liever gewoon de HTML rechtstreeks? Dat mag ook — draai dit script
dan simpelweg niet meer.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
PARTIALS = ROOT / "_partials"

# marker -> pad naar het in te voegen fragment
SLOTS = {
    "ICON-SPRITE": ROOT / "assets" / "img" / "icons.svg",
    "HEADER": PARTIALS / "header.html",
    "CTA": PARTIALS / "cta.html",
    "FOOTER": PARTIALS / "footer.html",
}


def inject(html: str, name: str, content: str) -> str:
    """Vervang (of vul aan) het blok tussen <!--NAAM--> en <!--/NAAM-->."""
    open_tag, close_tag = f"<!--{name}-->", f"<!--/{name}-->"
    block = f"{open_tag}\n{content.strip()}\n{close_tag}"

    paired = re.compile(
        re.escape(open_tag) + r".*?" + re.escape(close_tag),
        re.DOTALL,
    )
    if paired.search(html):
        return paired.sub(lambda _: block, html, count=1)
    if open_tag in html:
        return html.replace(open_tag, block, 1)
    return html


def main() -> int:
    missing = [str(p) for p in SLOTS.values() if not p.exists()]
    if missing:
        print("Ontbrekende fragmenten: " + ", ".join(missing), file=sys.stderr)
        return 1

    fragments = {name: path.read_text(encoding="utf-8") for name, path in SLOTS.items()}
    pages = sorted(p for p in ROOT.glob("*.html"))
    if not pages:
        print("Geen HTML-pagina's gevonden.", file=sys.stderr)
        return 1

    for page in pages:
        original = page.read_text(encoding="utf-8")
        updated = original
        for name, content in fragments.items():
            updated = inject(updated, name, content)

        # Zorg dat elke pagina een doctype heeft.
        if not updated.lstrip().lower().startswith("<!doctype"):
            updated = "<!DOCTYPE html>\n" + updated.lstrip()

        if updated != original:
            page.write_text(updated, encoding="utf-8")
            print(f"  bijgewerkt  {page.name}")
        else:
            print(f"  ongewijzigd {page.name}")

    print(f"\n{len(pages)} pagina's verwerkt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
