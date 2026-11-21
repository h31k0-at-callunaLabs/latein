"""Zeichnungen für Biologie: Lichtmikroskop und Blattquerschnitt (schematisch, nach Buch S. 18 und S. 24)."""
import math

def _marker(n, mx, my, tx, ty):
    # Linie vom Nummernkreis zum Bauteil, Punkt am Ziel
    dx, dy = tx - mx, ty - my
    d = math.hypot(dx, dy) or 1
    sx, sy = mx + dx / d * 15, my + dy / d * 15
    return (f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="#1D1930" stroke-width="1.6"/>'
            f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="3.2" fill="#1D1930"/>'
            f'<circle cx="{mx}" cy="{my}" r="15" fill="#4E3D96"/>'
            f'<text x="{mx}" y="{my + 5.5}" text-anchor="middle" font-size="16" font-weight="700" fill="#fff" font-family="Atkinson Hyperlegible, sans-serif">{n}</text>')

# ---------- Mikroskop ----------
ANG = 43  # Neigung des Tubus
def _rot(x, y, cx=300, cy=150, a=ANG):
    r = math.radians(a)
    x, y = x - cx, y - cy
    return cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r)

MIKRO_TEILE = ["Okular", "Tubus", "Objektivrevolver", "Objektiv", "Objekttisch",
               "Kondensor", "Blende", "Lichtquelle", "Trägerarm", "Grob- und Feintrieb"]

def mikroskop(marks=True):
    g = '#E3E6EB'; s = '#5B6472'; dk = '#3A4250'; md = '#9AA3AF'
    p = []
    p.append(f'<path d="M290,418 L290,160 L300,150 L{_rot(300,14)[0]:.1f},{_rot(300,14)[1]:.1f}" stroke="#F2C230" stroke-width="5" fill="none" opacity=".75"/>')
    # Tubus + Okular (gedreht)
    p.append(f'<g transform="rotate({ANG} 300 150)">'
             f'<rect x="283" y="44" width="34" height="112" rx="3" fill="{g}" stroke="{s}" stroke-width="2"/>'
             f'<rect x="288" y="12" width="24" height="34" rx="3" fill="{dk}" stroke="{s}" stroke-width="2"/>'
             f'<line x1="288" y1="20" x2="312" y2="20" stroke="#fff" stroke-width="1.5" opacity=".5"/>'
             f'<path d="M290,160 L290,40" stroke="#F2C230" stroke-width="5" opacity=".75"/></g>')
    # Trägerarm
    p.append(f'<path d="M128,432 L148,198 Q154,150 205,146 L258,146 L258,190 L214,192 Q196,194 194,214 L186,432 Z" fill="{g}" stroke="{s}" stroke-width="2"/>')
    # Kopf
    p.append(f'<rect x="245" y="138" width="92" height="98" rx="8" fill="{g}" stroke="{s}" stroke-width="2"/>')
    p.append('<path d="M290,140 L290,236" stroke="#F2C230" stroke-width="5" opacity=".75"/>')
    # Objektivrevolver
    p.append(f'<path d="M252,236 L330,236 L342,256 L240,256 Z" fill="{md}" stroke="{s}" stroke-width="2"/>')
    p.append(''.join(f'<line x1="{x}" y1="240" x2="{x-2}" y2="253" stroke="{s}" stroke-width="1"/>' for x in range(252, 334, 8)))
    # Objektive (eins senkrecht, zwei schräg)
    for a, h in ((-28, 34), (28, 30)):
        p.append(f'<g transform="rotate({a} 290 256)"><rect x="281" y="256" width="18" height="{h}" rx="2" fill="#F4F5F7" stroke="{s}" stroke-width="2"/><rect x="284" y="{256+h}" width="12" height="7" fill="{dk}"/></g>')
    p.append(f'<rect x="279" y="256" width="22" height="36" rx="2" fill="#F4F5F7" stroke="{s}" stroke-width="2"/><rect x="282" y="268" width="16" height="4" fill="#C0392B"/><rect x="283" y="292" width="14" height="10" fill="{dk}"/>')
    # Halter für Tisch
    p.append(f'<rect x="186" y="318" width="40" height="22" fill="{g}" stroke="{s}" stroke-width="2"/>')
    # Objekttisch mit Präparat und Klemme
    p.append(f'<rect x="205" y="316" width="182" height="15" rx="2" fill="{dk}" stroke="{s}" stroke-width="2"/>')
    p.append('<rect x="252" y="310" width="76" height="6" fill="#BFE3F2" stroke="#5B6472" stroke-width="1"/>')
    p.append(f'<rect x="330" y="307" width="34" height="6" rx="2" fill="{md}" stroke="{s}" stroke-width="1.5"/>')
    p.append('<path d="M290,331 L290,418" stroke="#F2C230" stroke-width="5" opacity=".75"/>')
    # Kondensor
    p.append(f'<rect x="268" y="333" width="44" height="17" rx="2" fill="{md}" stroke="{s}" stroke-width="2"/><ellipse cx="290" cy="336" rx="16" ry="3" fill="#BFE3F2" stroke="{s}"/>')
    # Blende mit Hebel
    p.append(f'<rect x="258" y="352" width="64" height="9" rx="2" fill="#6B7280" stroke="{s}" stroke-width="2"/><rect x="322" y="354" width="24" height="5" rx="2" fill="#6B7280" stroke="{s}" stroke-width="1.5"/>')
    p.append(f'<rect x="232" y="336" width="8" height="26" fill="{g}" stroke="{s}" stroke-width="1.5"/><rect x="232" y="350" width="28" height="6" fill="{g}" stroke="{s}" stroke-width="1.5"/>')
    # Grob- und Feintrieb
    p.append(f'<circle cx="158" cy="372" r="25" fill="#D1D5DB" stroke="{s}" stroke-width="2"/><circle cx="158" cy="372" r="11" fill="#6B7280" stroke="{s}" stroke-width="2"/>')
    # Fuß mit Lichtquelle
    p.append(f'<rect x="104" y="430" width="320" height="42" rx="10" fill="{g}" stroke="{s}" stroke-width="2"/>')
    p.append(f'<rect x="272" y="410" width="36" height="22" rx="3" fill="#F4F5F7" stroke="{s}" stroke-width="2"/><circle cx="290" cy="420" r="7" fill="#F2C230" stroke="#B88A00"/>')
    p.append(f'<rect x="140" y="446" width="20" height="10" rx="2" fill="{md}" stroke="{s}"/>')
    if marks:
        T = {
            "Okular": ((492, 34), _rot(300, 28)),
            "Tubus": ((492, 100), _rot(317, 100)),
            "Objektivrevolver": ((492, 178), (338, 250)),
            "Objektiv": ((492, 238), (301, 280)),
            "Objekttisch": ((492, 296), (384, 324)),
            "Kondensor": ((492, 344), (312, 343)),
            "Blende": ((492, 386), (343, 357)),
            "Lichtquelle": ((492, 432), (297, 420)),
            "Trägerarm": ((40, 230), (166, 250)),
            "Grob- und Feintrieb": ((40, 372), (139, 372)),
        }
        for i, name in enumerate(MIKRO_TEILE, 1):
            (mx, my), (tx, ty) = T[name]
            p.append(_marker(i, mx, my, tx, ty))
    return f'<svg class="fig" viewBox="0 0 520 490" role="img" aria-label="Zeichnung eines Lichtmikroskops mit nummerierten Teilen">{"".join(p)}</svg>'

# ---------- Blattquerschnitt ----------
BLATT_TEILE = ["Kutikula", "obere Epidermis", "Palisadengewebe", "Schwammgewebe", "untere Epidermis",
               "Chloroplast", "Leitbündel", "Interzellulare (Luftraum)", "Schließzelle", "Spaltöffnung"]

SPONGY = [(85,192,22,15),(140,190,24,14),(200,195,22,16),(255,188,20,13),(390,190,24,15),(450,194,22,14),(510,189,24,15),(560,195,18,15),
          (100,234,26,16),(165,238,22,15),(225,232,22,16),(410,234,24,16),(545,238,24,15),
          (80,278,20,14),(135,272,24,15),(195,281,22,13),(250,275,24,16),(328,284,24,12),(395,277,24,14),(548,281,22,13)]

def blatt(marks=True):
    p = []
    cut = '#EADB8A'; cs = '#B09A3A'; ep = '#F1F7EA'; es = '#6B8E4E'; pal = '#BFE3A4'; ps = '#4D7C2F'; chl = '#2F7D23'
    p.append('<rect x="60" y="30" width="520" height="304" fill="#FFFFFF"/>')
    # Kutikula oben
    p.append(f'<rect x="60" y="28" width="520" height="9" fill="{cut}" stroke="{cs}" stroke-width="1"/>')
    # obere Epidermis
    p.append(''.join(f'<rect x="{60+40*i}" y="37" width="40" height="30" rx="3" fill="{ep}" stroke="{es}" stroke-width="1.5"/>' for i in range(13)))
    # Palisadengewebe
    for i in range(13):
        x0 = 64 + 40 * i
        p.append(f'<rect x="{x0}" y="70" width="32" height="100" rx="10" fill="{pal}" stroke="{ps}" stroke-width="1.5"/>')
        p.append(''.join(f'<ellipse cx="{x0+cx}" cy="{y}" rx="4.2" ry="3.2" fill="{chl}"/>' for y in range(82, 162, 12) for cx in (10, 22)))
    # Schwammgewebe
    for (cx, cy, rx, ry) in SPONGY:
        p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#D6EEC6" stroke="{ps}" stroke-width="1.5"/>')
        p.append(''.join(f'<ellipse cx="{cx+dx}" cy="{cy+dy}" rx="3.6" ry="2.8" fill="{chl}"/>' for dx, dy in ((-9, -3), (2, 5), (10, -4))))
    # Leitbündel
    p.append('<circle cx="320" cy="232" r="38" fill="#F1E6D2" stroke="#8A6D3B" stroke-width="2"/>')
    p.append(''.join(f'<circle cx="{320+dx}" cy="{232+dy}" r="{r}" fill="#D9C29A" stroke="#8A6D3B" stroke-width="1"/>'
                     for dx, dy, r in ((-14,-12,7),(0,-16,6),(14,-11,7),(-18,4,5),(-4,2,6),(10,4,5),(20,8,4),(-10,18,5),(4,18,5),(16,22,4))))
    # untere Epidermis mit Lücke für die Spaltöffnung (x 460–500)
    p.append(''.join(f'<rect x="{60+40*i}" y="300" width="40" height="26" rx="3" fill="{ep}" stroke="{es}" stroke-width="1.5"/>' for i in range(13) if 60+40*i != 460))
    # Schließzellen (bohnenförmig) mit Chloroplasten, dazwischen der Spalt
    p.append('<path d="M478,301 C457,301 457,325 478,325 C476,320 475,317 475,313 C475,309 476,306 478,301 Z" fill="#A8D88A" stroke="#4D7C2F" stroke-width="1.6"/>')
    p.append('<path d="M482,301 C503,301 503,325 482,325 C484,320 485,317 485,313 C485,309 484,306 482,301 Z" fill="#A8D88A" stroke="#4D7C2F" stroke-width="1.6"/>')
    p.append(''.join(f'<ellipse cx="{x}" cy="{y}" rx="2.6" ry="2" fill="{chl}"/>' for x, y in ((466,308),(466,318),(494,308),(494,318))))
    # Kutikula unten (mit Lücke an der Spaltöffnung)
    p.append(f'<rect x="60" y="326" width="414" height="7" fill="{cut}" stroke="{cs}" stroke-width="1"/><rect x="486" y="326" width="94" height="7" fill="{cut}" stroke="{cs}" stroke-width="1"/>')
    if marks:
        T = {
            "Kutikula": ((26, 32), (72, 32)),
            "obere Epidermis": ((26, 78), (80, 52)),
            "Palisadengewebe": ((26, 128), (64, 128)),
            "Schwammgewebe": ((26, 222), (76, 234)),
            "untere Epidermis": ((26, 312), (72, 313)),
            "Chloroplast": ((614, 96), (566, 94)),
            "Leitbündel": ((614, 158), (348, 214)),
            "Interzellulare (Luftraum)": ((614, 222), (478, 240)),
            "Schließzelle": ((614, 286), (492, 312)),
            "Spaltöffnung": ((614, 360), (480, 313)),
        }
        for i, name in enumerate(BLATT_TEILE, 1):
            (mx, my), (tx, ty) = T[name]
            p.append(_marker(i, mx, my, tx, ty))
    return f'<svg class="fig" viewBox="0 0 640 380" role="img" aria-label="Schematischer Querschnitt durch ein Laubblatt mit nummerierten Teilen">{"".join(p)}</svg>'

if __name__ == "__main__":
    for name, f in (("mikro", mikroskop), ("blatt", blatt)):
        open(f"/tmp/{name}.svg", "w").write(f().replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" style="background:#fff" ', 1))

# ---------- Pflanzenzelle und Tierzelle ----------
PFL_TEILE = ["Zellwand", "Zellkern", "Zellmembran", "Cytoplasma", "Chloroplast", "Mitochondrium", "Vakuole"]
TIER_TEILE = ["Zellmembran", "Cytoplasma", "Zellkern", "Mitochondrium"]

def _mito(x, y, a=0):
    return (f'<g transform="rotate({a} {x} {y})"><ellipse cx="{x}" cy="{y}" rx="11" ry="6" fill="#F4B183" stroke="#B5651D" stroke-width="1.5"/>'
            f'<path d="M{x-7},{y} q2,-4 4,0 t4,0 t4,0" fill="none" stroke="#B5651D" stroke-width="1.2"/></g>')

def _chloro(x, y, a=0):
    return (f'<g transform="rotate({a} {x} {y})"><ellipse cx="{x}" cy="{y}" rx="12" ry="6.5" fill="#4CA64C" stroke="#2F6B2F" stroke-width="1.5"/>'
            f'<line x1="{x-6}" y1="{y-2}" x2="{x+6}" y2="{y-2}" stroke="#2F6B2F"/><line x1="{x-6}" y1="{y+2}" x2="{x+6}" y2="{y+2}" stroke="#2F6B2F"/></g>')

def pflanzenzelle(marks=True):
    p = ['<rect x="140" y="30" width="240" height="280" rx="6" fill="#A9CF7A" stroke="#5E8A2E" stroke-width="2"/>',
         '<rect x="154" y="44" width="212" height="252" rx="4" fill="#EEF7E4" stroke="#2D4F1A" stroke-width="2.5"/>',
         '<rect x="205" y="72" width="138" height="200" rx="26" fill="#D7ECF7" stroke="#5E93B5" stroke-width="2"/>',
         '<circle cx="180" cy="150" r="19" fill="#C9B6E8" stroke="#6A4FA0" stroke-width="2"/><circle cx="184" cy="146" r="5" fill="#8E73C4"/>']
    for x, y, a in ((172, 70, 0), (262, 58, 0), (322, 58, 0), (352, 112, 90), (352, 232, 90), (300, 284, 0), (225, 284, 0), (172, 235, 90)):
        p.append(_chloro(x, y, a))
    for x, y, a in ((352, 170, 90), (172, 98, 0), (262, 284, 0)):
        p.append(_mito(x, y, a))
    if marks:
        T = {"Zellwand": ((40, 60), (147, 60)), "Zellmembran": ((40, 205), (155, 205)), "Zellkern": ((40, 150), (172, 150)),
             "Cytoplasma": ((40, 270), (180, 266)), "Chloroplast": ((480, 70), (330, 58)), "Mitochondrium": ((480, 170), (352, 176)),
             "Vakuole": ((480, 250), (300, 220))}
        for i, n in enumerate(PFL_TEILE, 1):
            (mx, my), (tx, ty) = T[n]
            p.append(_marker(i, mx, my, tx, ty))
    return f'<svg class="fig" viewBox="0 0 520 340" role="img" aria-label="Schematische Pflanzenzelle mit nummerierten Teilen">{"".join(p)}</svg>'

def tierzelle(marks=True):
    p = ['<path d="M260,52 C340,46 392,96 388,160 C385,226 350,284 266,288 C190,292 134,250 132,176 C130,104 182,58 260,52 Z" fill="#FBE3DA" stroke="#9C3D2E" stroke-width="3"/>',
         '<circle cx="250" cy="168" r="34" fill="#C9B6E8" stroke="#6A4FA0" stroke-width="2"/><circle cx="256" cy="160" r="8" fill="#8E73C4"/>']
    for x, y, a in ((190, 112, -30), (322, 104, 20), (334, 226, -15), (196, 236, 30), (300, 168, 80)):
        p.append(_mito(x, y, a))
    if marks:
        T = {"Zellmembran": ((40, 120), (140, 130)), "Cytoplasma": ((40, 215), (170, 190)), "Zellkern": ((480, 60), (262, 145)),
             "Mitochondrium": ((480, 240), (342, 224))}
        for i, n in enumerate(TIER_TEILE, 1):
            (mx, my), (tx, ty) = T[n]
            p.append(_marker(i, mx, my, tx, ty))
    return f'<svg class="fig" viewBox="0 0 520 340" role="img" aria-label="Schematische Tierzelle mit nummerierten Teilen">{"".join(p)}</svg>'

# ---------- Diagramm Bläschenzählmethode (Buch S. 27, Abb. 6) ----------
BLAES = [(200, 0), (1000, 1), (4000, 4), (8000, 8), (16000, 12), (24000, 13), (32000, 13)]

def blaeschen_chart():
    X = lambda v: 70 + v / 32000 * 420
    Y = lambda v: 250 - v / 14 * 210
    p = ['<rect x="70" y="40" width="420" height="210" fill="#FAFAFD"/>']
    for v in range(0, 15, 2):
        p.append(f'<line x1="70" y1="{Y(v)}" x2="490" y2="{Y(v)}" stroke="#E2DFEA"/><text x="62" y="{Y(v)+5}" text-anchor="end" font-size="13" fill="#5C5675">{v}</text>')
    for v in range(0, 32001, 8000):
        p.append(f'<line x1="{X(v)}" y1="250" x2="{X(v)}" y2="255" stroke="#1D1930"/><text x="{X(v)}" y="272" text-anchor="middle" font-size="13" fill="#5C5675">{v:,}</text>'.replace(",", "."))
    p.append('<line x1="70" y1="250" x2="494" y2="250" stroke="#1D1930" stroke-width="1.5"/><line x1="70" y1="250" x2="70" y2="36" stroke="#1D1930" stroke-width="1.5"/>')
    p.append('<text x="280" y="294" text-anchor="middle" font-size="14" font-weight="700" fill="#1D1930">Beleuchtungsstärke in Lux</text>')
    p.append('<text x="18" y="145" text-anchor="middle" font-size="14" font-weight="700" fill="#1D1930" transform="rotate(-90 18 145)">Sauerstoff-Bläschen pro Minute</text>')
    pts = " ".join(f"{X(a):.1f},{Y(b):.1f}" for a, b in BLAES)
    p.append(f'<polyline points="{pts}" fill="none" stroke="#2E8A5E" stroke-width="3"/>')
    p.append("".join(f'<circle cx="{X(a):.1f}" cy="{Y(b):.1f}" r="5" fill="#2E8A5E"/>' for a, b in BLAES))
    return f'<svg class="fig" viewBox="0 0 520 305" role="img" aria-label="Diagramm: Sauerstoff-Bläschen pro Minute bei steigender Beleuchtungsstärke">{"".join(p)}</svg>'
