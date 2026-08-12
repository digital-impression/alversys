#!/usr/bin/env python3
"""Zet tools/page.html om in één zelfstandig bestand: lettertypes, foto's,
iconen en de kaart worden ingesloten. Geen enkele externe request."""

import base64, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'tools', 'page.html')
OUT = os.path.join(ROOT, 'jacobs-law.html')

def b64(path):
    return base64.b64encode(open(path, 'rb').read()).decode()

# ── foto's: opnieuw comprimeren via Chromium, één keer per beeld ──────────
def images():
    spec = {  # naam -> (bestand, maxbreedte, kwaliteit)
        'gesprek':  ('kantoor-gesprek.jpg',  1500, 0.78),
        'overleg':  ('kantoor-overleg.jpg',  1200, 0.78),
        'liesbet':  ('portret-liesbet.jpg',   900, 0.82),
        'michelle': ('portret-michelle.jpg',  900, 0.82),
    }
    import json, tempfile
    base = os.environ.get('JL_NODE_DIR') or tempfile.gettempdir()
    script = os.path.join(base, '_jl_img.mjs')
    open(script, 'w').write('''
import { chromium } from 'playwright';
const spec = JSON.parse(process.argv[2]);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage();
await p.goto('http://localhost:8899/index.html', { waitUntil: 'load' });
const out = {};
for (const [k, v] of Object.entries(spec)) {
  out[k] = await p.evaluate(async ([file, maxW, q]) => {
    const img = new Image(); img.src = '/assets/img/' + file; await img.decode();
    const s = Math.min(1, maxW / img.naturalWidth);
    const c = document.createElement('canvas');
    c.width = Math.round(img.naturalWidth * s); c.height = Math.round(img.naturalHeight * s);
    const cx = c.getContext('2d'); cx.imageSmoothingQuality = 'high';
    cx.drawImage(img, 0, 0, c.width, c.height);
    return c.toDataURL('image/jpeg', q);
  }, v);
}
console.log(JSON.stringify(out));
await b.close();
''')
    # Playwright is geïnstalleerd in de scratchpad, niet in de repo.
    pw = os.environ.get('JL_NODE_DIR') or os.path.dirname(script)
    for cand in (pw, os.path.expanduser('~')):
        if os.path.isdir(os.path.join(cand, 'node_modules', 'playwright')):
            pw = cand
            break
    r = subprocess.run(['node', script, json.dumps(spec)],
                       capture_output=True, text=True, cwd=pw)
    if r.returncode != 0:
        sys.exit('beeldcompressie mislukt:\n' + r.stderr[-1500:])
    return json.loads(r.stdout.strip().splitlines()[-1])

# ── vaste onderdelen ──────────────────────────────────────────────────────
LOGO = ('<svg viewBox="0 0 32 32" fill="none" aria-hidden="true">'
        '<path d="M16 3.5 28.5 16 16 28.5 3.5 16Z" stroke="currentColor" stroke-width="1.15"/>'
        '<path d="M.5 16h31" stroke="#B4873C" stroke-width="1.15"/>'
        '<path d="M16 13.4 18.6 16 16 18.6 13.4 16Z" fill="#B4873C"/></svg>')

ARROW = ('<svg viewBox="0 0 15 10" fill="none" stroke="currentColor" stroke-width="1.4" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M0 5h13M9.5 1.5 13 5l-3.5 3.5"/></svg>')

I = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" '
     'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">')

ICON_TEL = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
            'style="width:14px;height:14px;opacity:.7">'
            '<path d="M14.5 11.4v2.1a1 1 0 0 1-1.1 1 12.7 12.7 0 0 1-5.5-2 12.5 12.5 0 0 1-3.8-3.8 '
            '12.7 12.7 0 0 1-2-5.6 1 1 0 0 1 1-1.1h2.1a1 1 0 0 1 1 .9c.07.6.2 1.2.4 1.8a1 1 0 0 1-.23 '
            '1.05l-.9.9a10 10 0 0 0 3.8 3.8l.9-.9a1 1 0 0 1 1.05-.23c.58.2 1.18.33 1.8.4a1 1 0 0 1 .9 1Z"/></svg>')

ICON_IG = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.2" '
           'aria-hidden="true"><rect x="2" y="2" width="12" height="12" rx="3.6"/>'
           '<circle cx="8" cy="8" r="2.9"/><circle cx="11.6" cy="4.4" r=".85" fill="currentColor" stroke="none"/></svg>')

ICON_MAIL = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.2" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<rect x="1.5" y="3.5" width="13" height="9" rx="1.2"/><path d="m2 4.5 6 4.2 6-4.2"/></svg>')

# Vertrouwensband — dezelfde ruit-taal, geen ingekochte iconen
ICON_SCALE = I + '<path d="M12 4v16M6 8h12M6 8 3 15h6ZM18 8l-3 7h6ZM8 20h8"/></svg>'
ICON_CHECK = I + '<path d="M12 3 4 6.5v5c0 4.6 3.3 8.5 8 9.5 4.7-1 8-4.9 8-9.5v-5Z"/><path d="m8.8 12 2.2 2.2 4.2-4.4"/></svg>'
ICON_DIA   = I + '<path d="M12 3.2 20.8 12 12 20.8 3.2 12Z"/><path d="M12 8.6 15.4 12 12 15.4 8.6 12Z" fill="currentColor" stroke="none"/></svg>'
ICON_HANDS = I + '<path d="M3 12.5 7 8.8a2 2 0 0 1 2.7 0L12 11l2.3-2.2a2 2 0 0 1 2.7 0l4 3.7"/><path d="M12 11v9"/><path d="M7 17.5h10"/></svg>'

# Kaart: schematisch en waar — Aartselaar ligt ten zuiden van Antwerpen aan de A12.
# Geen nagemaakte stratenkaart; wel de ruit als marker.
MAP = '''<svg viewBox="0 0 400 300" role="img" aria-label="Schematische ligging: Aartselaar ligt ten zuiden van Antwerpen, aan de A12.">
  <defs>
    <pattern id="jl-g" width="25" height="25" patternUnits="userSpaceOnUse">
      <path d="M25 0H0v25" fill="none" stroke="rgba(180,135,60,.10)" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="400" height="300" fill="#1F1913"/>
  <rect width="400" height="300" fill="url(#jl-g)"/>
  <path d="M232 -10 C 226 70, 214 132, 200 196 L 190 310" fill="none"
        stroke="rgba(221,184,120,.34)" stroke-width="10" stroke-linecap="round"/>
  <path d="M232 -10 C 226 70, 214 132, 200 196 L 190 310" fill="none"
        stroke="rgba(221,184,120,.5)" stroke-width="1" stroke-dasharray="7 9"/>
  <path d="M60 120 C 130 132, 190 150, 340 128" fill="none"
        stroke="rgba(241,235,226,.13)" stroke-width="6" stroke-linecap="round"/>
  <path d="M40 236 C 120 226, 250 244, 372 224" fill="none"
        stroke="rgba(241,235,226,.10)" stroke-width="5" stroke-linecap="round"/>
  <text x="248" y="44" fill="#BCB1A2" font-family="system-ui,sans-serif" font-size="12"
        letter-spacing="2.4">ANTWERPEN</text>
  <text x="243" y="112" fill="rgba(221,184,120,.85)" font-family="system-ui,sans-serif"
        font-size="11" letter-spacing="2.2">A12</text>
  <g transform="translate(200 196)">
    <circle r="30" fill="none" stroke="rgba(221,184,120,.16)"/>
    <circle r="18" fill="none" stroke="rgba(221,184,120,.28)"/>
    <path d="M0 -9 9 0 0 9 -9 0Z" fill="#B4873C"/>
  </g>
  <text x="200" y="252" fill="#F1EBE2" font-family="system-ui,sans-serif" font-size="13"
        letter-spacing="1.6" text-anchor="middle">AARTSELAAR</text>
  <text x="200" y="272" fill="#BCB1A2" font-family="system-ui,sans-serif" font-size="11"
        text-anchor="middle">Populierenlaan 43</text>
</svg>'''

FAVICON = ("data:image/svg+xml,"
           "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' fill='%2314100D'/%3E"
           "%3Cpath d='M16 5.5 26.5 16 16 26.5 5.5 16Z' fill='none' stroke='%23F1EBE2' stroke-width='1.4'/%3E"
           "%3Cpath d='M2 16h28' stroke='%23B4873C' stroke-width='1.4'/%3E"
           "%3Cpath d='M16 13.2 18.8 16 16 18.8 13.2 16Z' fill='%23B4873C'/%3E%3C/svg%3E")


def main():
    html = open(SRC, encoding='utf-8').read()
    imgs = images()
    fonts = os.path.join(ROOT, 'assets', 'fonts')

    subs = {
        '__F_SERIF__': b64(os.path.join(fonts, 'fraunces-normal-300-600-latin.woff2')),
        '__F_SANS__':  b64(os.path.join(fonts, 'inter-tight-400-700-latin.woff2')),
        '__LOGO__': LOGO, '__ARROW__': ARROW, '__FAVICON__': FAVICON, '__MAP__': MAP,
        '__ICON_TEL__': ICON_TEL, '__ICON_IG__': ICON_IG, '__ICON_MAIL__': ICON_MAIL,
        '__ICON_SCALE__': ICON_SCALE, '__ICON_CHECK__': ICON_CHECK,
        '__ICON_DIA__': ICON_DIA, '__ICON_HANDS__': ICON_HANDS,
        '__IMG_gesprek__': imgs['gesprek'], '__IMG_overleg__': imgs['overleg'],
        '__IMG_liesbet__': imgs['liesbet'], '__IMG_michelle__': imgs['michelle'],
    }
    for k, v in subs.items():
        if k not in html:
            sys.exit('plaatshouder ontbreekt in page.html: ' + k)
        html = html.replace(k, v)

    left = re.findall(r'__[A-Z_a-z]+__', html)
    if left:
        sys.exit('niet-ingevulde plaatshouders: ' + ', '.join(sorted(set(left))))

    open(OUT, 'w', encoding='utf-8').write(html)
    print('geschreven: %s  (%.2f MB)' % (OUT, len(html.encode()) / 1024 / 1024))


if __name__ == '__main__':
    main()
