#!/usr/bin/env python3
"""
Trekt foto's in de huisstijl van de site.

    python3 tools/beeld.py bron.jpg naam 4:5 1100

Het resultaat is een bijgesneden, geschaalde en getoonde JPEG in
assets/img/. De toon is een gradient map van diep woudgroen via warm klei
naar bot, met een fractie van de oorspronkelijke kleur erdoor en een lichte
korrel. Daardoor lezen foto's van verschillende herkomst toch als één
geheel — belangrijk zolang we met tijdelijk beeldmateriaal werken, en even
handig wanneer straks de eigen foto's binnenkomen.

Vereist Pillow:  pip install pillow
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
UIT = ROOT / "assets/img"

SCHADUW = (43, 52, 45)   # bewust niet zwart: ingezakte zwarten
MIDDEN = (134, 120, 102)
HOOGLICHT = (245, 242, 234)  # gelijk aan --paper


def kleurtrap() -> list[int]:
    """Bouwt de opzoektabel voor de gradient map."""
    r, g, b = [], [], []
    for i in range(256):
        t = i / 255
        if t < 0.5:
            u, a, z = t / 0.5, SCHADUW, MIDDEN
        else:
            u, a, z = (t - 0.5) / 0.5, MIDDEN, HOOGLICHT
        u = u * u * (3 - 2 * u)  # smoothstep: zachte overgang
        r.append(int(a[0] + (z[0] - a[0]) * u))
        g.append(int(a[1] + (z[1] - a[1]) * u))
        b.append(int(a[2] + (z[2] - a[2]) * u))
    return r + g + b


TRAP = kleurtrap()


def korrel(afbeelding: Image.Image, sterkte: int = 5) -> Image.Image:
    ruis = Image.new("L", afbeelding.size)
    ruis.frombytes(
        bytes(bytearray(random.getrandbits(8) for _ in range(afbeelding.size[0] * afbeelding.size[1])))
    )
    ruis = ruis.filter(ImageFilter.GaussianBlur(0.4))
    return Image.blend(afbeelding, Image.merge("RGB", (ruis, ruis, ruis)), sterkte / 100)


def verwerk(bron: Path, naam: str, verhouding: float, breedte: int, kleurbehoud: float = 0.30) -> None:
    im = Image.open(bron).convert("RGB")

    b, h = im.size
    if b / h > verhouding:  # te breed: links en rechts bijsnijden
        nb = int(h * verhouding)
        im = im.crop(((b - nb) // 2, 0, (b - nb) // 2 + nb, h))
    else:  # te hoog: onderaan meer wegnemen dan bovenaan
        nh = int(b / verhouding)
        top = max(0, (h - nh) // 3)
        im = im.crop((0, top, b, top + nh))

    im = im.resize((breedte, int(breedte / verhouding)), Image.LANCZOS)

    grijs = ImageOps.autocontrast(im.convert("L"), cutoff=1)
    getoond = Image.merge("RGB", (grijs, grijs, grijs)).point(TRAP)
    uit = Image.blend(getoond, im, kleurbehoud)
    uit = ImageEnhance.Contrast(uit).enhance(1.04)
    uit = korrel(uit)

    UIT.mkdir(parents=True, exist_ok=True)
    doel = UIT / f"{naam}.jpg"
    uit.save(doel, "JPEG", quality=72, optimize=True, progressive=True)
    print(f"  ✓ {doel.name}  {uit.size[0]}x{uit.size[1]}  {doel.stat().st_size // 1024} kB")

    # kleinere variant voor srcset
    klein = max(700, breedte // 2)
    if klein < breedte:
        kl = uit.resize((klein, round(uit.height * klein / uit.width)), Image.LANCZOS)
        doel2 = UIT / f"{naam}-{klein}.jpg"
        kl.save(doel2, "JPEG", quality=72, optimize=True, progressive=True)
        print(f"  ✓ {doel2.name}  {kl.size[0]}x{kl.size[1]}  {doel2.stat().st_size // 1024} kB")


def main() -> int:
    if len(sys.argv) != 5:
        print(__doc__)
        return 1
    bron, naam, verhouding, breedte = sys.argv[1:]
    b, h = (float(x) for x in verhouding.split(":"))
    verwerk(Path(bron), naam, b / h, int(breedte))
    return 0


if __name__ == "__main__":
    sys.exit(main())
