#!/usr/bin/env python3
"""Baut die Musik-Seiten (eine Seite pro Thema) nach ../musik/. Aufruf: python3 _build/musik.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "musik")
B = os.path.join(ROOT, "_build")

TOPICS = [
 dict(id="t1", file="violinschluessel.html", nav="1 Violinschlüssel", title="Noten im Violinschlüssel", dur="15 Minuten", desc="Linien, Zwischenräume, Hilfslinien."),
 dict(id="t2", file="bassschluessel.html", nav="2 Bassschlüssel", title="Noten im Bassschlüssel", dur="15 Minuten", desc="Gleiche Stelle, anderer Name."),
 dict(id="t3", file="oktaven.html", nav="3 Oktaven", title="Oktavbezeichnungen", dur="10 Minuten", desc="C, c, c', c'': Wie schreibt man welche Oktave?"),
 dict(id="t4", file="intervalle.html", nav="4 Intervalle", title="Intervalle: Prime bis Oktave", dur="15 Minuten", desc="Grobbestimmung durch Zählen."),
 dict(id="t5", file="terzen.html", nav="5 Terzen", title="Terzen: groß oder klein?", dur="15 Minuten", desc="Feinbestimmung mit Halbtonschritten."),
 dict(id="t6", file="dreiklaenge.html", nav="6 Dreiklänge", title="Dur- und Molldreiklänge", dur="20 Minuten", desc="Grundton, Terzton, Quintton und der Terzaufbau."),
 dict(id="t7", file="begleitung.html", nav="7 Begleitung", title="Liedbegleitung mit Dreiklängen", dur="20 Minuten", desc="Die drei Regeln aus dem Heft, wie bei „Morning has broken“."),
]
EXTRA = [
 dict(id="gem", file="gemischt.html", nav="8 Großes Quiz", title="Großes Quiz: alles gemischt", dur="15 Minuten", desc="Alle Fragen aus allen Themen durcheinander."),
 dict(id="probe", file="probe.html", nav="9 Probe-Arbeit", title="Probe-Arbeit", dur="45 Minuten", desc="Wie die echte Arbeit, zum Ausdrucken. Am besten am Sonntag."),
]
STEPS = TOPICS + EXTRA

def st(spec, lab=None, names=False, cw=None, sc=None, top=None, cls="stbox", bars=None):
    a = f'<div class="{cls}" data-st="{spec}"'
    if bars or (bars is None and ">" in spec and spec.count("|") > 1): a += ' data-bars'
    if lab: a += f' data-lab="{lab}"'
    if top: a += f' data-top="{top}"'
    if names: a += ' data-names'
    if cw: a += f' data-cw="{cw}"'
    if sc: a += f' data-sc="{sc}"'
    return a + '></div>'

LESEN = {
"t1": f"""
<div class="box merke"><h3>Das musst du wissen</h3>
<ul><li>Die sieben <b>Stammtöne</b> heißen <b>c d e f g a h</b>. Nach dem h kommt wieder ein c.</li>
<li>Die fünf Notenlinien zählt man immer <b>von unten nach oben</b>.</li>
<li>Der Violinschlüssel heißt auch <b>G-Schlüssel</b>. Er beginnt mit seinem Kringel auf der <b>2. Linie</b>. Dort liegt das <b>g'</b>.</li>
<li>Jeder Schritt nach oben ist der nächste Buchstabe: Linie, Zwischenraum, Linie, Zwischenraum …</li></ul></div>
<div class="box"><h3>Alle Töne von c' bis a''</h3>
{st("v|c'|d'|e'|f'|g'|a'|h'", names=True, cw=30)}
{st("v|c''|d''|e''|f''|g''|a''", names=True, cw=30)}
<p class="meta">Das c' steht auf einer <b>Hilfslinie</b> unter dem Notensystem. Auch das a'' braucht eine Hilfslinie, oben.</p></div>
<div class="box"><h3>Linien und Zwischenräume</h3>
<p><b>Auf den Linien</b> (von unten): <b>e' g' h' d'' f''</b></p>
{st("v|e'|g'|h'|d''|f''", names=True, cw=30)}
<p class="meta">Eselsbrücke: <b>E</b>ine <b>G</b>ute <b>H</b>exe <b>D</b>arf <b>F</b>liegen.</p>
<p><b>In den Zwischenräumen</b> (von unten): <b>f' a' c'' e''</b></p>
{st("v|f'|a'|c''|e''", names=True, cw=30)}
<p class="meta">Eselsbrücke: Das ergibt das englische Wort <b>FACE</b> (Gesicht).</p></div>
<div class="box"><h3>Unter und über dem Notensystem</h3>
<div class="tbl"><table><tr><th>Wo?</th><th>Ton</th></tr>
<tr><td>auf der 1. Hilfslinie unten</td><td><b>c'</b></td></tr>
<tr><td>direkt unter der untersten Linie</td><td><b>d'</b></td></tr>
<tr><td>direkt über der obersten Linie</td><td><b>g''</b></td></tr>
<tr><td>auf der 1. Hilfslinie oben</td><td><b>a''</b></td></tr></table></div></div>
""",
"t2": f"""
<div class="box merke"><h3>Das musst du wissen</h3>
<ul><li>Tiefe Töne schreibt man im <b>Bassschlüssel</b>.</li>
<li>Er heißt auch <b>F-Schlüssel</b>. Seine zwei Punkte liegen um die <b>4. Linie</b>. Dort liegt das <b>f</b>.</li>
<li><b>Auf den Linien</b> (von unten): <b>G H d f a</b>.<br><span class="meta">Eselsbrücke: <b>G</b>rüne <b>H</b>asen <b>d</b>ürfen <b>f</b>ast <b>a</b>lles.</span></li>
<li><b>In den Zwischenräumen</b> (von unten): <b>A c e g</b>.<br><span class="meta">Eselsbrücke: <b>A</b>lle <b>C</b>lowns <b>e</b>ssen <b>g</b>ern.</span></li></ul></div>
<div class="box"><h3>Linien und Zwischenräume</h3>
{st("b|G|H|d|f|a", names=True, cw=30)}
{st("b|A|c|e|g", names=True, cw=30)}</div>
<div class="box"><h3>Alle Töne von E bis c'</h3>
{st("b|E|F|G|A|H|c|d", names=True, cw=30)}
{st("b|e|f|g|a|h|c'", names=True, cw=30)}
<div class="tbl"><table><tr><th>Wo?</th><th>Ton</th></tr>
<tr><td>auf der 1. Hilfslinie unten</td><td><b>E</b></td></tr>
<tr><td>direkt unter der untersten Linie</td><td><b>F</b></td></tr>
<tr><td>direkt über der obersten Linie</td><td><b>h</b></td></tr>
<tr><td>auf der 1. Hilfslinie oben</td><td><b>c'</b></td></tr></table></div>
<p>Das <b>c'</b> auf der Hilfslinie oben ist <b>derselbe Ton</b> wie das c' auf der Hilfslinie unten im Violinschlüssel. Man nennt es das <b>mittlere c</b>.</p></div>
<div class="box"><h3>Achtung: gleiche Stelle, anderer Name!</h3>
<p>Die unterste Linie ist im Violinschlüssel ein <b>e'</b>, im Bassschlüssel ein <b>G</b>.</p>
<div class="duo">{st("v|e'|f'|g'", names=True, cw=30)}{st("b|G|A|H", names=True, cw=30)}</div>
<p class="meta">Trick: An derselben Stelle ist der Bass-Name immer <b>zwei Buchstaben weiter</b> (c d e f g a h): aus e wird g, aus f wird a, aus g wird h. Lerne die Bass-Noten aber am besten direkt.</p></div>
""",
"t3": f"""
<div class="box merke"><h3>Das musst du wissen</h3>
<p>Die Stammtöne c d e f g a h wiederholen sich immer wieder, tiefer und höher. Jeder Bereich von <b>c bis h</b> heißt <b>Oktave</b> (Oktavraum). An der Schreibweise sieht man, aus welcher Oktave ein Ton ist:</p>
<div class="tbl"><table><tr><th>Oktave</th><th>So schreibt man sie</th></tr>
<tr><td>große Oktave</td><td><b>C D E F G A H</b> (große Buchstaben)</td></tr>
<tr><td>kleine Oktave</td><td><b>c d e f g a h</b> (kleine Buchstaben)</td></tr>
<tr><td>eingestrichene Oktave</td><td><b>c' d' e' f' g' a' h'</b> (ein Strich)</td></tr>
<tr><td>zweigestrichene Oktave</td><td><b>c'' d'' e'' f'' g'' a'' h''</b> (zwei Striche)</td></tr></table></div>
<p>Noch höher kommt die dreigestrichene Oktave (c'''), noch tiefer die Kontraoktave.</p></div>
<div class="box"><h3>Eine neue Oktave beginnt immer bei c</h3>
<p>Nach dem <b>h</b> kommt das nächste <b>c</b>, und dann wechselt die Schreibweise:</p>
<p class="nm">… a &nbsp;h &nbsp;<b>c'</b> &nbsp;d' &nbsp;… &nbsp;a' &nbsp;h' &nbsp;<b>c''</b> &nbsp;d'' …</p>
<p>Also: Auf h' folgt <b>c''</b>, nicht c'.</p>
<div data-kb="C|c|c'|c''"></div>
<p class="meta">Die gelben Tasten sind C, c, c' und c''. Dort beginnt jeweils eine neue Oktave.</p></div>
<div class="box"><h3>Welche Oktaven siehst du in den Notenschlüsseln?</h3>
<p><b>Bassschlüssel:</b> große und kleine Oktave, ganz oben das c'.</p>
{st("b|E|G|H|c|e|g|h|c'", names=True, cw=28)}
<p><b>Violinschlüssel:</b> eingestrichene und zweigestrichene Oktave.</p>
{st("v|c'|e'|g'|h'|c''|e''|g''|a''", names=True, cw=28)}
<p>Das <b>c'</b> (mittleres c) gehört zu beiden: im Violinschlüssel auf der 1. Hilfslinie unten, im Bassschlüssel auf der 1. Hilfslinie oben.</p></div>
""",
"t4": f"""
<div class="box merke"><h3>Das musst du wissen</h3>
<ul><li>Ein <b>Intervall</b> ist der <b>Abstand zwischen zwei Tönen</b>.</li>
<li>Ein einzelner Ton kann niemals ein Intervall sein.</li>
<li><b>Grobbestimmung:</b> Zähle von der unteren bis zur oberen Note alle Linien und Zwischenräume. <b>Beide Noten zählen mit!</b></li></ul></div>
<div class="box"><h3>Die acht Intervalle (von c' aus)</h3>
{st("v|c'>c'|c'>d'|c'>e'|c'>f'|c'>g'|c'>a'|c'>h'|c'>c''", lab="1 Prime|2 Sekunde|3 Terz|4 Quarte|5 Quinte|6 Sexte|7 Septime|8 Oktave", cw=58, sc=1.35)}
<div class="tbl"><table><tr><th>Zahl</th><th>Intervall</th><th>Eselsbrücke aus deinem Heft</th></tr>
<tr><td>1</td><td><b>Prime</b></td><td>Prima, also eine 1</td></tr>
<tr><td>2</td><td><b>Sekunde</b></td><td>Englisch: second = 2.</td></tr>
<tr><td>3</td><td><b>Terz</b></td><td>März ist der 3. Monat</td></tr>
<tr><td>4</td><td><b>Quarte</b></td><td>Quadrat (4 Ecken)</td></tr>
<tr><td>5</td><td><b>Quinte</b></td><td>Quintessenz: das 5. Element</td></tr>
<tr><td>6</td><td><b>Sexte</b></td><td>Latein: sex = 6</td></tr>
<tr><td>7</td><td><b>Septime</b></td><td>Latein: septem = 7</td></tr>
<tr><td>8</td><td><b>Oktave</b></td><td>Ein Oktopus hat 8 Arme</td></tr></table></div></div>
<div class="box"><h3>So zählst du: Beispiel</h3>
{st("v|g'>c''", cw=46)}
<p><b>g'</b> (1) – a' (2) – h' (3) – <b>c''</b> (4). Das sind 4 Töne → <b>Quarte</b>.</p>
<p>Es ist egal, ob der höhere Ton zuerst oder als zweiter kommt. Du zählst immer vom tieferen zum höheren Ton.</p></div>
<div class="box"><h3>Kontroll-Trick: Linie oder Zwischenraum?</h3>
<ul><li>Beide Noten auf <b>Linien</b> oder beide in <b>Zwischenräumen</b> → ungerade Zahl: Prime, Terz, Quinte, Septime.</li>
<li>Eine Note auf einer Linie, die andere in einem Zwischenraum → gerade Zahl: Sekunde, Quarte, Sexte, Oktave.</li></ul>
<p class="meta">Vorzeichen (♯ oder ♭) ändern an der Grobbestimmung nichts: c'–e' und c'–es' sind beide eine Terz. Ob groß oder klein, sagt erst die Feinbestimmung (Thema 5).</p></div>
""",
"t5": f"""
<div class="box merke"><h3>Das musst du wissen</h3>
<ul><li>Ein <b>Halbtonschritt</b> (HTS) ist der Weg von einer Taste zur <b>direkt benachbarten</b> Taste. Schwarze Tasten zählen mit!</li>
<li><b>große Terz = 4 Halbtonschritte</b> (g3)</li>
<li><b>kleine Terz = 3 Halbtonschritte</b> (k3)</li></ul></div>
<div class="box"><h3>So zählst du auf der Klaviatur</h3>
<p>Leg den Finger auf den unteren Ton. Jede nächste Taste ist ein Schritt, egal ob weiß oder schwarz. Zähle bis zum oberen Ton.</p>
<p><b>c' bis e':</b> 4 Halbtonschritte → <b>große Terz</b></p>
<div data-kb="c'|e'|count"></div>
<p><b>d' bis f':</b> 3 Halbtonschritte → <b>kleine Terz</b></p>
<div data-kb="d'|f'|count"></div>
<p>Wichtig: Zwischen <b>e und f</b> und zwischen <b>h und c</b> liegt keine schwarze Taste. Diese beiden Schritte sind schon Halbtonschritte.</p></div>
<div class="box"><h3>Alle Terzen ohne Vorzeichen</h3>
<div class="tbl"><table><tr><th>große Terz (4 HTS)</th><th>kleine Terz (3 HTS)</th></tr>
<tr><td>c – e<br>f – a<br>g – h</td><td>d – f<br>e – g<br>a – c<br>h – d</td></tr></table></div>
<p class="meta">Trick (nur ohne Vorzeichen): Steckt <b>e–f</b> oder <b>h–c</b> in der Terz, ist sie <b>klein</b>.</p></div>
<div class="box"><h3>Vorzeichen</h3>
<ul><li><b>♯ Kreuz:</b> erhöht den Ton um einen Halbtonschritt. Man hängt <b>-is</b> an: f → <b>fis</b>, c → <b>cis</b>, g → <b>gis</b>.</li>
<li><b>♭ b:</b> erniedrigt den Ton um einen Halbtonschritt. Man hängt <b>-es</b> an: d → <b>des</b>. Ausnahmen: e → <b>es</b>, a → <b>as</b>, h → <b>b</b>.</li></ul>
<p><b>Beispiel d' bis fis':</b> 4 Halbtonschritte → <b>große Terz</b>. Ohne Kreuz (d'–f') wäre es eine kleine Terz.</p>
{st("v|d'>fis'", cw=50)}
<div data-kb="d'|fis'|count"></div>
<p class="meta">Mit Vorzeichen gilt der Trick nicht. Dann zählst du immer genau.</p></div>
<div class="box"><h3>Aus dem Arbeitsheft (Aufgabe 5b)</h3>
<div class="tbl"><table><tr><th>Töne</th><th>HTS</th><th>Intervall</th></tr>
<tr><td>d'–f'</td><td>3</td><td>kleine Terz</td></tr>
<tr><td>c'–e'</td><td>4</td><td>große Terz</td></tr>
<tr><td>g'–h'</td><td>4</td><td>große Terz</td></tr>
<tr><td>h'–d''</td><td>3</td><td>kleine Terz</td></tr>
<tr><td>f'–a'</td><td>4</td><td>große Terz</td></tr>
<tr><td>a'–c''</td><td>3</td><td>kleine Terz</td></tr>
<tr><td>e'–g'</td><td>3</td><td>kleine Terz</td></tr></table></div></div>
""",
"t6": f"""
<div class="box merke"><h3>Das musst du wissen</h3>
<ul><li>Ein <b>Dreiklang</b> besteht aus <b>zwei Terzen übereinander</b> (Terzschichtung). Die drei Noten liegen alle auf Linien oder alle in Zwischenräumen.</li>
<li>Die drei Töne heißen von unten nach oben: <b>Grundton</b>, <b>Terzton</b>, <b>Quintton</b>.</li>
<li><b>Durdreiklang:</b> unten <b>große Terz</b>, oben <b>kleine Terz</b>.</li>
<li><b>Molldreiklang:</b> unten <b>kleine Terz</b>, oben <b>große Terz</b>.</li></ul>
<div class="duo">{st("v|d'+fis'+a'", lab="D-Dur", cw=60)}{st("v|d'+f'+a'", lab="d-Moll", cw=60)}</div>
<p class="meta">D-Dur: d'–fis' große Terz (4 HTS), fis'–a' kleine Terz (3 HTS). d-Moll: d'–f' kleine Terz (3 HTS), f'–a' große Terz (4 HTS). Nur der mittlere Ton ist anders!</p></div>
<div class="box"><h3>Die drei Töne (Arbeitsheft Aufgabe 9)</h3>
{st("v|c'+e'+g'", cw=60)}
<div class="tbl"><table><tr><th>Ton</th><th>Name</th><th>Abstand</th></tr>
<tr><td>g'</td><td>Quintton</td><td>e'–g': kleine Terz</td></tr>
<tr><td>e'</td><td>Terzton</td><td>c'–e': große Terz</td></tr>
<tr><td>c'</td><td>Grundton</td><td></td></tr></table></div>
<p>Unten große Terz, oben kleine Terz → <b>C-Dur</b>. Der Quintton liegt eine Quinte über dem Grundton.</p></div>
<div class="box"><h3>Richtig oder falsch? (Aufgabe 9e)</h3>
<ul><li>✓ Charakteristisch sind die zwei übereinanderliegenden Terzen (Terzschichtung).</li>
<li>✓ Dreiklangstöne können nacheinander (<b>sukzessiv</b>) oder gleichzeitig (<b>simultan</b>) erklingen.</li>
<li>✗ <s>Der Grundton ist der höchste Ton des Dreiklangs.</s> Er ist der <b>tiefste</b>.</li>
<li>✗ <s>Der Dreiklang klingt spannungsreich (dissonant).</s> Dur- und Molldreiklänge klingen wohl (<b>konsonant</b>).</li></ul></div>
<div class="box"><h3>So bestimmst du einen Dreiklang</h3>
<ol><li>Benenne die drei Töne von unten nach oben.</li>
<li>Der unterste Ton ist der <b>Grundton</b>. Er gibt dem Dreiklang den Namen.</li>
<li>Bestimme die <b>untere Terz</b>: 4 HTS = groß (g3), 3 HTS = klein (k3).</li>
<li>Bestimme die <b>obere Terz</b>.</li>
<li>Unten g3, oben k3 → <b>Dur</b>. Unten k3, oben g3 → <b>Moll</b>.</li>
<li>Schreib den Namen: Dur mit großem Buchstaben (<b>F-Dur</b>), Moll mit kleinem Buchstaben (<b>a-Moll</b>).</li></ol></div>
<div class="box"><h3>Aus dem Arbeitsheft (Aufgabe 11)</h3>
{st("v|f'+a'+c''|a'+c''+e''|e'+g'+h'|g'+h'+d''", lab="F-Dur|a-Moll|e-Moll|G-Dur", cw=58, sc=2)}
<div class="tbl"><table><tr><th>Dreiklang</th><th>unten</th><th>oben</th></tr>
<tr><td>F-Dur (f a c)</td><td>g3</td><td>k3</td></tr>
<tr><td>a-Moll (a c e)</td><td>k3</td><td>g3</td></tr>
<tr><td>e-Moll (e g h)</td><td>k3</td><td>g3</td></tr>
<tr><td>G-Dur (g h d)</td><td>g3</td><td>k3</td></tr></table></div></div>
<div class="box"><h3>Die wichtigsten Dreiklänge</h3>
<div class="tbl"><table><tr><th>Dur</th><th>Töne</th><th>Moll</th><th>Töne</th></tr>
<tr><td>C-Dur</td><td>c – e – g</td><td>a-Moll</td><td>a – c – e</td></tr>
<tr><td>F-Dur</td><td>f – a – c</td><td>d-Moll</td><td>d – f – a</td></tr>
<tr><td>G-Dur</td><td>g – h – d</td><td>e-Moll</td><td>e – g – h</td></tr>
<tr><td>D-Dur</td><td>d – fis – a</td><td>g-Moll</td><td>g – b – d</td></tr>
<tr><td>A-Dur</td><td>a – cis – e</td><td>c-Moll</td><td>c – es – g</td></tr>
<tr><td>E-Dur</td><td>e – gis – h</td><td>f-Moll</td><td>f – as – c</td></tr></table></div>
<p class="meta">Dur klingt oft hell und fröhlich, Moll oft dunkler oder trauriger.</p></div>
""",
"t7": """
<div class="box merke"><h3>Das musst du wissen</h3>
<p>Über den Noten eines Liedes stehen <b>Akkordsymbole</b>. Sie sagen dir, welcher Dreiklang begleitet:</p>
<ul><li>Nur ein Großbuchstabe = <b>Dur</b>: <b>C</b> = C-Dur (c e g), <b>G</b> = G-Dur (g h d), <b>D</b> = D-Dur (d fis a)</li>
<li>Großbuchstabe mit <b>m</b> = <b>Moll</b>: <b>Dm</b> = d-Moll (d f a), <b>Am</b> = a-Moll (a c e), <b>Em</b> = e-Moll (e g h)</li></ul></div>
<div class="box merke"><h3>Die drei Regeln aus deinem Heft</h3>
<ol><li><b>Wenig oder keine Tonsprünge</b>, lieber kleine Notenschritte.</li>
<li><b>Was liegen bleiben kann, bleibt liegen.</b> Töne, die zwei Akkorde gemeinsam haben, bleiben einfach stehen.</li>
<li><b>Der Grundton wird im Bass verdoppelt.</b> Im Bassschlüssel steht der Grundton des Akkords.</li></ol></div>
<div class="box"><h3>Du darfst die Töne umstellen</h3>
<p>Damit du wenig springen musst, darfst du die drei Töne in anderer Reihenfolge übereinander schreiben. Es bleibt derselbe Akkord, solange es dieselben drei Töne sind:</p>
<div data-st="v|c'+e'+g'|e'+g'+c''|g+c'+e'" data-lab="c' e' g'|e' g' c''|g c' e'" data-cw="62" data-top="C|C|C" class="stbox"></div>
<p class="meta">Alle drei sind C-Dur, denn es sind immer die Töne c, e und g.</p></div>
<div class="box"><h3>So gehst du vor</h3>
<ol><li>Schreib den ersten Akkord in Grundstellung, zum Beispiel C = c' e' g'.</li>
<li>Bestimme die Töne des nächsten Akkords.</li>
<li>Welche Töne hat der neue Akkord auch? Die <b>bleiben liegen</b>.</li>
<li>Die anderen Töne gehen zum <b>nächstgelegenen</b> Ton des neuen Akkords.</li>
<li>Schreib den <b>Grundton</b> in den Bassschlüssel.</li></ol></div>
<div class="box"><h3>Morning has broken, Takt 1 bis 6</h3>
<p>Akkorde: C | C | Dm | G | F | C. In Takt 2 bleibt C einfach liegen.</p>
<div data-sys="C Dm G F C" data-names class="stbox"></div>
<ul><li><b>C → Dm:</b> Kein gemeinsamer Ton. Alle drei gehen einen kleinen Schritt hoch: c'→d', e'→f', g'→a'.</li>
<li><b>Dm → G:</b> <b>d' bleibt liegen</b>. f'→g', a'→h'.</li>
<li><b>G → F:</b> Kein gemeinsamer Ton. Alle gehen einen Schritt runter: d'→c', g'→f', h'→a'. (Auch f' a' c'' wäre genauso wenig Bewegung.)</li>
<li><b>F → C:</b> <b>c' bleibt liegen</b>. f'→e', a'→g'.</li>
<li><b>Bass:</b> immer der Grundton: c, d, G, F, c.</li></ul></div>
<div class="box"><h3>Morning has broken, Takt 7 bis 10</h3>
<p>Akkorde: C | Em | F | G</p>
<div data-sys="C Em F G" data-names class="stbox"></div>
<ul><li><b>C → Em:</b> <b>e' und g' bleiben liegen</b>. Nur c' geht einen Halbtonschritt runter zum h.</li>
<li><b>Em → F:</b> Alle gehen einen Schritt hoch: h→c', e'→f', g'→a'.</li>
<li><b>F → G:</b> Alle gehen einen Schritt hoch: c'→d', f'→g', a'→h'. Auch h d' g' wäre gut gewesen, das ist genauso wenig Bewegung.</li></ul></div>
""",
}

CARDS = {
"t1": [
 ["Die sieben Stammtöne", "c d e f g a h"],
 ["Violinschlüssel: Töne auf den Linien (von unten)", "e' g' h' d'' f''<br><span class='meta'>Eine Gute Hexe Darf Fliegen</span>"],
 ["Violinschlüssel: Töne in den Zwischenräumen (von unten)", "f' a' c'' e'' (FACE)"],
 ["Wo liegt im Violinschlüssel das c'?", "Auf der 1. Hilfslinie unten."],
 ["Wo liegt das g'?", "Auf der 2. Linie von unten. Dort beginnt der Violinschlüssel (G-Schlüssel)."],
 ["Wie heißt diese Note? <div data-st='v|d&#39;&#39;'></div>", "d'' (4. Linie)"],
 ["Wie heißt diese Note? <div data-st='v|a&#39;'></div>", "a' (2. Zwischenraum)"],
 ["Wie heißt diese Note? <div data-st='v|d&#39;'></div>", "d' (direkt unter der untersten Linie)"],
 ["Wie heißt diese Note? <div data-st='v|a&#39;&#39;'></div>", "a'' (1. Hilfslinie oben)"],
],
"t2": [
 ["Bassschlüssel: Töne auf den Linien (von unten)", "G H d f a<br><span class='meta'>Grüne Hasen dürfen fast alles</span>"],
 ["Bassschlüssel: Töne in den Zwischenräumen (von unten)", "A c e g<br><span class='meta'>Alle Clowns essen gern</span>"],
 ["Warum heißt der Bassschlüssel F-Schlüssel?", "Seine zwei Punkte liegen um die 4. Linie. Dort liegt das f."],
 ["Bassschlüssel: Was liegt auf der 1. Hilfslinie oben?", "c' (das mittlere c)"],
 ["Bassschlüssel: Was liegt auf der 1. Hilfslinie unten?", "E"],
 ["Wie heißt diese Note? <div data-st='b|d'></div>", "d (3. Linie)"],
 ["Wie heißt diese Note? <div data-st='b|A'></div>", "A (1. Zwischenraum)"],
 ["Wie heißt diese Note? <div data-st='b|g'></div>", "g (4. Zwischenraum)"],
 ["Wie heißt diese Note? <div data-st='b|h'></div>", "h (direkt über der obersten Linie)"],
],
"t3": [
 ["große Oktave", "C D E F G A H (große Buchstaben)"],
 ["kleine Oktave", "c d e f g a h (kleine Buchstaben)"],
 ["eingestrichene Oktave", "c' d' e' f' g' a' h' (ein Strich)"],
 ["zweigestrichene Oktave", "c'' d'' e'' f'' g'' a'' h'' (zwei Striche)"],
 ["Bei welchem Ton beginnt eine neue Oktave?", "Immer bei c."],
 ["Welcher Ton kommt nach h'?", "c''"],
 ["Was ist das mittlere c?", "Das c'. Im Violinschlüssel auf der 1. Hilfslinie unten, im Bassschlüssel auf der 1. Hilfslinie oben."],
],
"t4": [
 ["Was ist ein Intervall?", "Der Abstand zwischen zwei Tönen. Ein einzelner Ton ist nie ein Intervall."],
 ["Wie geht die Grobbestimmung?", "Linien und Zwischenräume von der unteren bis zur oberen Note zählen. Beide Noten zählen mit."],
 ["Intervalle 1 bis 4", "Prime, Sekunde, Terz, Quarte"],
 ["Intervalle 5 bis 8", "Quinte, Sexte, Septime, Oktave"],
 ["Beide Noten auf Linien. Welche Intervalle sind möglich?", "Nur ungerade: Prime, Terz, Quinte, Septime"],
 ["Welches Intervall? <div data-st='v|e&#39;&gt;h&#39;' data-cw='46'></div>", "Quinte: e' f' g' a' h' = 5 Töne"],
 ["Welches Intervall? <div data-st='v|f&#39;&gt;d&#39;&#39;' data-cw='46'></div>", "Sexte: f' g' a' h' c'' d'' = 6 Töne"],
 ["Welches Intervall? <div data-st='b|c&gt;h' data-cw='46'></div>", "Septime: c d e f g a h = 7 Töne"],
],
"t5": [
 ["Halbtonschritt", "Abstand von einer Taste zur direkt benachbarten Taste (schwarze Tasten zählen mit)."],
 ["große Terz", "4 Halbtonschritte (g3)"],
 ["kleine Terz", "3 Halbtonschritte (k3)"],
 ["Zwischen welchen weißen Tasten liegt keine schwarze?", "e–f und h–c"],
 ["Große Terzen ohne Vorzeichen", "c–e, f–a, g–h"],
 ["Kleine Terzen ohne Vorzeichen", "d–f, e–g, a–c, h–d"],
 ["Was macht ein ♯?", "Es erhöht um einen Halbtonschritt: f → fis"],
 ["Was macht ein ♭?", "Es erniedrigt um einen Halbtonschritt: e → es, a → as, h → b"],
 ["d'–fis': groß oder klein?", "große Terz (4 HTS)"],
],
"t6": [
 ["Wie heißen die drei Töne eines Dreiklangs?", "Grundton (unten), Terzton (Mitte), Quintton (oben)"],
 ["Durdreiklang", "unten große Terz, oben kleine Terz"],
 ["Molldreiklang", "unten kleine Terz, oben große Terz"],
 ["Terzschichtung", "Zwei Terzen liegen übereinander. Das ist typisch für Dreiklänge."],
 ["sukzessiv und simultan", "sukzessiv = nacheinander, simultan = gleichzeitig"],
 ["Welcher Dreiklang? <div data-st='v|g&#39;+h&#39;+d&#39;&#39;' data-cw='60'></div>", "G-Dur: g'–h' große Terz, h'–d'' kleine Terz"],
 ["Welcher Dreiklang? <div data-st='v|a&#39;+c&#39;&#39;+e&#39;&#39;' data-cw='60'></div>", "a-Moll: a'–c'' kleine Terz, c''–e'' große Terz"],
 ["Welcher Dreiklang? <div data-st='v|d&#39;+fis&#39;+a&#39;' data-cw='60'></div>", "D-Dur: d'–fis' große Terz, fis'–a' kleine Terz"],
 ["Wie schreibt man Dur und Moll?", "Dur mit großem Buchstaben (F-Dur), Moll mit kleinem (e-Moll)."],
],
"t7": [
 ["Akkordsymbol C", "C-Dur: c – e – g"],
 ["Akkordsymbol Dm", "d-Moll: d – f – a"],
 ["Akkordsymbol Em", "e-Moll: e – g – h"],
 ["Akkordsymbol Am", "a-Moll: a – c – e"],
 ["Akkordsymbol F", "F-Dur: f – a – c"],
 ["Akkordsymbol G", "G-Dur: g – h – d"],
 ["Regel 1 der Liedbegleitung", "Wenig oder keine Tonsprünge, lieber kleine Notenschritte."],
 ["Regel 2 der Liedbegleitung", "Was liegen bleiben kann, bleibt liegen."],
 ["Regel 3 der Liedbegleitung", "Der Grundton wird im Bass verdoppelt."],
],
}

QUIZ = {
"t1": [
 ["Wie heißt diese Note?", ["g'", "e'", "h'", "f'"], "Auf der 2. Linie von unten liegt das g'. Dort beginnt der Violinschlüssel.", "v|g'"],
 ["Wie heißt diese Note?", ["c'", "d'", "a", "e'"], "Das c' liegt auf der 1. Hilfslinie unten.", "v|c'"],
 ["Wie heißt diese Note?", ["f''", "e''", "d''", "g''"], "Die oberste (5.) Linie ist f''.", "v|f''"],
 ["Wie heißt diese Note?", ["a'", "f'", "c''", "g'"], "Im 2. Zwischenraum liegt a' (FACE: f' a' c'' e'').", "v|a'"],
 ["Wie heißt diese Note?", ["e''", "c''", "d''", "f''"], "Im 4. Zwischenraum liegt e'' (FACE).", "v|e''"],
 ["Welche Töne liegen im Violinschlüssel auf den Linien (von unten)?", ["e' g' h' d'' f''", "f' a' c'' e'' g''", "G H d f a", "c' e' g' h' d''"], "Eine Gute Hexe Darf Fliegen."],
 ["Wie heißen die sieben Stammtöne?", ["c d e f g a h", "c d e f g a b", "a b c d e f g", "c d e f g h a"], "Im Deutschen heißt der Ton nach a: h."],
 ["Welche Note liegt direkt unter der untersten Linie?", ["d'", "c'", "e'", "h"], "Die unterste Linie ist e'. Einen Schritt tiefer liegt d'."],
],
"t2": [
 ["Wie heißt diese Note?", ["f", "a", "d", "e"], "Die zwei Punkte des Bassschlüssels liegen um die 4. Linie. Dort liegt f.", "b|f"],
 ["Wie heißt diese Note?", ["G", "e'", "E", "A"], "Die unterste Linie im Bassschlüssel ist G. (Im Violinschlüssel wäre es e'.)", "b|G"],
 ["Wie heißt diese Note?", ["c'", "a", "h", "e"], "Auf der 1. Hilfslinie oben liegt das mittlere c, also c'.", "b|c'"],
 ["Wie heißt diese Note?", ["c", "a'", "e", "H"], "Im 2. Zwischenraum liegt c (A c e g).", "b|c"],
 ["Wie heißt diese Note?", ["H", "G", "d", "g'"], "Auf der 2. Linie liegt H (G H d f a).", "b|H"],
 ["Welche Töne liegen im Bassschlüssel auf den Linien (von unten)?", ["G H d f a", "A c e g h", "e' g' h' d'' f''", "F A c e g"], "Grüne Hasen dürfen fast alles."],
 ["Welche Töne liegen im Bassschlüssel in den Zwischenräumen (von unten)?", ["A c e g", "F A c e", "f' a' c'' e''", "H d f a"], "Alle Clowns essen gern."],
 ["Warum heißt der Bassschlüssel auch F-Schlüssel?", ["Seine Punkte zeigen, wo das f liegt (4. Linie).", "Er beginnt auf der untersten Linie mit F.", "Er ist für Flöten.", "Er sieht aus wie ein F."], "Die beiden Punkte umschließen die 4. Linie. Dort liegt f."],
],
"t3": [
 ["Wie schreibt man das c aus der eingestrichenen Oktave?", ["c'", "c", "C", "c''"], "Eingestrichen = ein Strich."],
 ["Bei welchem Ton beginnt eine neue Oktave?", ["bei c", "bei a", "bei h", "bei g"], "Jede Oktave geht von c bis h."],
 ["Welcher Ton kommt direkt nach h'?", ["c''", "c'", "a'", "h''"], "Nach h beginnt mit c die nächste Oktave. Deshalb zwei Striche."],
 ["Wie schreibt man die Töne der großen Oktave?", ["mit großen Buchstaben, z. B. G", "mit kleinen Buchstaben, z. B. g", "mit einem Strich, z. B. g'", "mit zwei Strichen, z. B. g''"], "Große Oktave = große Buchstaben."],
 ["Wie heißt diese Note genau?", ["A", "a", "a'", "a''"], "1. Zwischenraum im Bassschlüssel: A aus der großen Oktave.", "b|A"],
 ["Wie heißt diese Note genau?", ["e''", "e'", "e", "E"], "4. Zwischenraum im Violinschlüssel: e'' aus der zweigestrichenen Oktave.", "v|e''"],
 ["In welcher Oktave liegt das d (kleiner Buchstabe, ohne Strich)?", ["kleine Oktave", "große Oktave", "eingestrichene Oktave", "zweigestrichene Oktave"], "Kleiner Buchstabe ohne Strich = kleine Oktave."],
 ["Das c auf der 1. Hilfslinie unten im Violinschlüssel und das c auf der 1. Hilfslinie oben im Bassschlüssel sind …", ["derselbe Ton: c'", "zwei verschiedene Töne: c' und c", "c'' und c'", "C und c"], "Beides ist das mittlere c, also c'."],
],
"t4": [
 ["Was ist ein Intervall?", ["der Abstand zwischen zwei Tönen", "ein einzelner Ton", "ein Dreiklang", "eine Pause"], "Ein einzelner Ton kann nie ein Intervall sein."],
 ["Welches Intervall ist das?", ["Quinte", "Quarte", "Sexte", "Terz"], "c' d' e' f' g' = 5 Töne.", "v|c'>g'"],
 ["Welches Intervall ist das?", ["Sekunde", "Prime", "Terz", "Quarte"], "e' und f' liegen direkt nebeneinander: 2 Töne.", "v|e'>f'"],
 ["Welches Intervall ist das?", ["Oktave", "Septime", "Sexte", "Prime"], "d' bis d'': 8 Töne. Gleicher Buchstabe, eine Oktave höher.", "v|d'>d''"],
 ["Welches Intervall ist das?", ["Quarte", "Quinte", "Terz", "Sexte"], "f' g' a' h' = 4 Töne.", "v|f'>h'"],
 ["Welches Intervall ist das?", ["Terz", "Sekunde", "Quarte", "Quinte"], "Von unten gezählt: a' (1) h' (2) c'' (3) = 3 Töne. Die Richtung ist egal.", "v|c''>a'"],
 ["Welches Intervall ist das?", ["Sexte", "Quinte", "Septime", "Quarte"], "G A H c d e = 6 Töne.", "b|G>e"],
 ["Beide Noten liegen auf Linien. Welches Intervall kann es NICHT sein?", ["Quarte", "Terz", "Quinte", "Septime"], "Linie und Linie ergibt immer eine ungerade Zahl: Prime, Terz, Quinte oder Septime."],
 ["c'–e' und c'–es': Was sind sie in der Grobbestimmung?", ["Beides sind Terzen.", "c'–e' ist eine Terz, c'–es' eine Sekunde.", "Beides sind Quarten.", "c'–es' ist kein Intervall."], "Vorzeichen ändern die Grobbestimmung nicht."],
],
"t5": [
 ["Wie viele Halbtonschritte hat eine große Terz?", ["4", "3", "2", "5"], "große Terz = 4 HTS."],
 ["Wie viele Halbtonschritte hat eine kleine Terz?", ["3", "4", "2", "1"], "kleine Terz = 3 HTS."],
 ["Zwischen welchen weißen Tasten liegt keine schwarze Taste?", ["e–f und h–c", "c–d und f–g", "g–a und a–h", "d–e und e–f"], "e–f und h–c sind Halbtonschritte."],
 ["Große oder kleine Terz?", ["kleine Terz", "große Terz"], "d' – dis'/es' – e' – f': 3 HTS.", "v|d'>f'"],
 ["Große oder kleine Terz?", ["große Terz", "kleine Terz"], "f' – fis' – g' – gis' – a': 4 HTS.", "v|f'>a'"],
 ["Große oder kleine Terz?", ["große Terz", "kleine Terz"], "Durch das Kreuz wird es eine große Terz: d' bis fis' = 4 HTS.", "v|d'>fis'"],
 ["Große oder kleine Terz?", ["kleine Terz", "große Terz"], "a' – b' – h' – c'': 3 HTS. Zwischen h und c ist nur ein Halbtonschritt.", "v|a'>c''"],
 ["Was macht ein ♯ (Kreuz)?", ["Es erhöht den Ton um einen Halbtonschritt.", "Es erniedrigt den Ton um einen Halbtonschritt.", "Es erhöht den Ton um eine Oktave.", "Es macht den Ton lauter."], "Aus f wird fis."],
 ["Wie heißt das h, wenn ein ♭ davor steht?", ["b", "hes", "his", "bes"], "Ausnahme: h mit ♭ heißt b."],
 ["Wie heißt das e, wenn ein ♭ davor steht?", ["es", "ees", "eis", "e♭"], "Ausnahme: e mit ♭ heißt es (und a mit ♭ heißt as)."],
],
"t6": [
 ["Wie ist ein Durdreiklang aufgebaut (von unten nach oben)?", ["unten große Terz, oben kleine Terz", "unten kleine Terz, oben große Terz", "zwei große Terzen", "zwei kleine Terzen"], "Dur: g3 unten, k3 oben."],
 ["Wie ist ein Molldreiklang aufgebaut (von unten nach oben)?", ["unten kleine Terz, oben große Terz", "unten große Terz, oben kleine Terz", "zwei große Terzen", "eine Quarte und eine Terz"], "Moll: k3 unten, g3 oben."],
 ["Welcher Dreiklang ist das?", ["F-Dur", "f-Moll", "a-Moll", "C-Dur"], "f'–a' große Terz, a'–c'' kleine Terz → F-Dur.", "v|f'+a'+c''"],
 ["Welcher Dreiklang ist das?", ["a-Moll", "A-Dur", "C-Dur", "e-Moll"], "a'–c'' kleine Terz, c''–e'' große Terz → a-Moll.", "v|a'+c''+e''"],
 ["Welcher Dreiklang ist das?", ["e-Moll", "E-Dur", "G-Dur", "h-Moll"], "e'–g' kleine Terz, g'–h' große Terz → e-Moll.", "v|e'+g'+h'"],
 ["Welcher Dreiklang ist das?", ["D-Dur", "d-Moll", "F-Dur", "fis-Moll"], "d'–fis' große Terz, fis'–a' kleine Terz → D-Dur.", "v|d'+fis'+a'"],
 ["Wie heißen die drei Töne eines Dreiklangs (von unten)?", ["Grundton, Terzton, Quintton", "Grundton, Quintton, Terzton", "Prime, Sekunde, Terz", "Bass, Mitte, Spitze"], "Der Terzton liegt eine Terz, der Quintton eine Quinte über dem Grundton."],
 ["Welche Aussage ist FALSCH?", ["Der Grundton ist der höchste Ton des Dreiklangs.", "Ein Dreiklang besteht aus zwei übereinanderliegenden Terzen.", "Dreiklangstöne können nacheinander oder gleichzeitig erklingen.", "Der Quintton liegt eine Quinte über dem Grundton."], "Der Grundton ist der tiefste Ton."],
 ["Was bedeutet „simultan“?", ["gleichzeitig", "nacheinander", "laut", "spannungsreich"], "Simultan = gleichzeitig, sukzessiv = nacheinander."],
 ["Welche Töne hat G-Dur?", ["g – h – d", "g – b – d", "g – h – e", "g – c – e"], "g–h große Terz, h–d kleine Terz."],
 ["Wie schreibt man den Namen eines Molldreiklangs?", ["mit kleinem Buchstaben: a-Moll", "mit großem Buchstaben: A-Moll", "mit Strich: a'-Moll", "nur mit m: am"], "Dur groß (A-Dur), Moll klein (a-Moll)."],
],
"t7": [
 ["Was bedeutet das Akkordsymbol Dm?", ["d-Moll-Dreiklang: d – f – a", "D-Dur-Dreiklang: d – fis – a", "nur der Ton d im Bass", "d-Moll-Tonleiter"], "Großbuchstabe mit m = Moll."],
 ["Was bedeutet das Akkordsymbol G?", ["G-Dur-Dreiklang: g – h – d", "g-Moll-Dreiklang: g – b – d", "nur der Ton G", "G-Schlüssel"], "Nur ein Großbuchstabe = Dur."],
 ["Welcher Ton kommt in den Bass?", ["der Grundton", "der Terzton", "der Quintton", "der höchste Ton der Melodie"], "Regel 3: Der Grundton wird im Bass verdoppelt."],
 ["Zwei Akkorde nacheinander haben einen Ton gemeinsam. Was machst du mit ihm?", ["Er bleibt liegen.", "Er springt eine Oktave hoch.", "Er fällt weg.", "Er kommt in den Bass."], "Regel 2: Was liegen bleiben kann, bleibt liegen."],
 ["Darf man g c' e' statt c' e' g' schreiben?", ["Ja, es sind dieselben Töne c, e, g, also C-Dur.", "Nein, dann ist es kein C-Dur mehr.", "Nein, dann ist es G-Dur.", "Nur im Bassschlüssel."], "Die Reihenfolge darf sich ändern, die Töne bleiben gleich."],
 ["Vorher steht C (c' e' g'). Dann kommt Am. Welche Lage passt am besten?", ["c' e' a'", "a c' e'", "e' a' c''", "a' c'' e''"], "c' und e' bleiben liegen, nur g' geht einen Schritt hoch zu a'.", None],
 ["Vorher steht G (d' g' h'). Dann kommt C. Welche Lage passt am besten?", ["e' g' c''", "c' e' g'", "g c' e'", "c'' e'' g''"], "g' bleibt liegen, d'→e' und h'→c'' sind kleine Schritte."],
 ["Vorher steht F (c' f' a'). Dann kommt C. Welche Lage passt am besten?", ["c' e' g'", "e' g' c''", "g c' e'", "c'' e'' g''"], "c' bleibt liegen, f'→e' und a'→g' sind kleine Schritte."],
 ["Welche Töne hat Em?", ["e – g – h", "e – gis – h", "e – g – b", "e – a – c"], "e-Moll: e–g kleine Terz, g–h große Terz."],
],
}
for k in QUIZ:
    QUIZ[k] = [q[:3] + ([q[3]] if len(q) > 3 and q[3] else []) for q in QUIZ[k]]

PROG = [
 dict(name="Morning has broken T. 1–6", syms=["C", "Dm", "G", "F", "C"]),
 dict(name="Morning has broken T. 7–10", syms=["C", "Em", "F", "G"]),
 dict(name="Morning has broken T. 13–18", syms=["C", "F", "C", "Am", "D"]),
 dict(name="Morning has broken T. 19–23", syms=["C", "Em", "F", "G", "C"]),
 dict(name="Übung: C F G C", syms=["C", "F", "G", "C"]),
 dict(name="Übung: C Am Dm G C", syms=["C", "Am", "Dm", "G", "C"]),
 dict(name="Übung: G C D G", syms=["G", "C", "D", "G"]),
 dict(name="Übung: Am Dm E Am", syms=["Am", "Dm", "E", "Am"]),
]

UEBEN = {
 "t1": [("Noten benennen", "Tippe auf den richtigen Buchstaben. Was du falsch hast, kommt am Ende nochmal.", "name-v"),
        ("Noten setzen", "Jetzt umgekehrt: Setze die Note an die richtige Stelle. So wie beim Notieren in der Arbeit.", "setzen-v")],
 "t2": [("Noten benennen", "Tippe auf den richtigen Buchstaben.", "name-b"),
        ("Noten setzen", "Setze die Note an die richtige Stelle im Bassschlüssel.", "setzen-b")],
 "t3": [("Genau benennen", "Wähle den Namen mit der richtigen Oktave. Mal Violinschlüssel, mal Bassschlüssel.", "oktave")],
 "t4": [("Intervalle bestimmen", "Zähle und tippe auf das Intervall.", "intervall")],
 "t5": [("Große oder kleine Terz?", "Zähle die Halbtonschritte auf der Klaviatur.", "terz")],
 "t6": [("Dreiklänge bestimmen", "Wie Aufgabe 11 im Arbeitsheft: Grundton, Terzaufbau, Dur oder Moll.", "dreiklang"),
        ("Dreiklänge notieren", "Setze die drei Töne selbst ins Notensystem.", "bauen")],
 "t7": [("Begleitung bauen", "Wähle oben ein Lied oder eine Übung. Bei jedem Akkord: erst die Töne, dann die beste Lage.", "begleitung")],
}

def task(n, title, pts, body):
    return f'<div class="task"><h3>{n}. {title} <b class="pts">{pts}</b></h3>{body}</div>\n'

def probe():
    h = '<div class="box"><h2>Probe-Arbeit Musik</h2><p class="meta">Intervalle, Terzen, Dreiklänge, Liedbegleitung, Notennamen. Zeit: 45 Minuten.</p>\n'
    h += task(1, "Benenne die Noten mit Oktavbezeichnung (Violinschlüssel).", "AFB 1",
        st("v|g'|d''|c'|f''|a'|h'|e''", lab="a)|b)|c)|d)|e)|f)|g)", cw=34) +
        '<div class="sol">a) g' + "'" + ' b) d' + "''" + ' c) c' + "'" + ' d) f' + "''" + ' e) a' + "'" + ' f) h' + "'" + ' g) e' + "''" + '</div>')
    h += task(2, "Benenne die Noten mit Oktavbezeichnung (Bassschlüssel).", "AFB 1",
        st("b|G|d|c'|A|f|E|h", lab="a)|b)|c)|d)|e)|f)|g)", cw=34) +
        "<div class=\"sol\">a) G b) d c) c' d) A e) f f) E g) h</div>")
    h += task(3, "Notiere die Töne.", "AFB 2",
        "<p>Violinschlüssel: a) e'' b) c' c) g'' d) h'</p>" + st("v|_|_|_|_", lab="a)|b)|c)|d)", cw=44) +
        "<p>Bassschlüssel: e) H f) e g) F h) c'</p>" + st("b|_|_|_|_", lab="e)|f)|g)|h)", cw=44) +
        '<div class="sol">' + st("v|e''|c'|g''|h'", lab="e''|c'|g''|h'", cw=44, cls="") + st("b|H|e|F|c'", lab="H|e|F|c'", cw=44, cls="") + "</div>")
    h += task(4, "Bestimme die Intervalle (Grobbestimmung).", "AFB 1",
        st("v|c'>g'|e'>f'|d'>d''|a'>c''|g'>c''|f'>d''", lab="a)|b)|c)|d)|e)|f)", cw=60, sc=1.75) + st("b|c>h|G>d", lab="g)|h)", cw=60, sc=1.75) +
        '<div class="sol">a) Quinte b) Sekunde c) Oktave d) Terz e) Quarte f) Sexte g) Septime h) Quinte</div>')
    h += task(5, "Bestimme die Terzen genau: Zahl der Halbtonschritte und große oder kleine Terz.", "AFB 2",
        st("v|d'>f'|f'>a'|e'>g'|g'>h'|a'>cis''|c'>es'", lab="a)|b)|c)|d)|e)|f)", cw=64, sc=1.7) +
        '<div class="sol">a) 3 HTS, kleine Terz b) 4 HTS, große Terz c) 3 HTS, kleine Terz d) 4 HTS, große Terz e) 4 HTS, große Terz f) 3 HTS, kleine Terz</div>')
    h += task(6, "Bestimme die Dreiklänge: Nenne die Töne, markiere den Terzaufbau (g3/k3), nenne Grundton und Tongeschlecht.", "AFB 2",
        st("v|g'+h'+d''|d'+f'+a'|a'+cis''+e''|e'+g'+h'", lab="a)|b)|c)|d)", cw=60) +
        '<div class="sol">a) g\' h\' d\'\': unten g3, oben k3, Grundton g → <b>G-Dur</b><br>b) d\' f\' a\': unten k3, oben g3, Grundton d → <b>d-Moll</b><br>c) a\' cis\'\' e\'\': unten g3, oben k3, Grundton a → <b>A-Dur</b><br>d) e\' g\' h\': unten k3, oben g3, Grundton e → <b>e-Moll</b></div>')
    h += task(7, "Notiere die Dreiklänge über dem angegebenen Grundton.", "AFB 2",
        "<p>a) C-Dur auf c' b) a-Moll auf a' c) F-Dur auf f' d) D-Dur auf d'</p>" + st("v|_|_|_|_", lab="a)|b)|c)|d)", cw=56) +
        "<p>e) G-Dur auf G f) a-Moll auf A</p>" + st("b|_|_", lab="e)|f)", cw=56) +
        '<div class="sol">' + st("v|c'+e'+g'|a'+c''+e''|f'+a'+c''|d'+fis'+a'", lab="C-Dur|a-Moll|F-Dur|D-Dur", cw=56, cls="") + st("b|G+H+d|A+c+e", lab="G-Dur|a-Moll", cw=56, cls="") + "Bei D-Dur das Kreuz vor dem f' nicht vergessen: d' fis' a'.</div>")
    h += task(8, "Richtig oder falsch? Streiche die falschen Aussagen durch.", "AFB 1",
        "<ol type='a'><li>Ein Intervall ist der Abstand zwischen zwei Tönen.</li><li>Eine kleine Terz hat 4 Halbtonschritte.</li><li>Der Grundton ist der höchste Ton eines Dreiklangs.</li><li>Dreiklangstöne können nacheinander (sukzessiv) oder gleichzeitig (simultan) erklingen.</li><li>Im Bassschlüssel liegt auf der untersten Linie das G.</li><li>Nach h' kommt c'.</li></ol>" +
        '<div class="sol">Falsch sind: b) Eine kleine Terz hat 3 HTS. c) Der Grundton ist der tiefste Ton. f) Nach h\' kommt c\'\'. Richtig sind a), d), e).</div>')
    h += task(9, "Erkläre den Unterschied zwischen einem Dur- und einem Molldreiklang.", "AFB 2",
        '<div class="lines"></div><div class="lines"></div><div class="lines"></div>' +
        '<div class="sol">Beide bestehen aus zwei Terzen übereinander (Terzschichtung). Beim Durdreiklang liegt unten eine große Terz (4 HTS) und oben eine kleine Terz (3 HTS). Beim Molldreiklang ist es umgekehrt: unten eine kleine Terz, oben eine große Terz. Der Unterschied liegt also beim mittleren Ton, dem Terzton. Beispiel: D-Dur d fis a, d-Moll d f a.</div>')
    h += task(10, "Komponiere eine Liedbegleitung.", "AFB 3",
        "<p>Notiere zu den Akkorden C | Am | F | G | C die Dreiklänge im Violinschlüssel und den Grundton im Bassschlüssel. Beachte die drei Regeln. Begründe bei zwei Akkordwechseln, warum du die Töne so gesetzt hast.</p>" +
        '<div class="stbox" data-esys="C|Am|F|G|C"></div><div class="lines"></div><div class="lines"></div><div class="lines"></div>' +
        '<div class="sol"><div data-sys="C Am F G C" data-names></div><ul><li><b>C → Am:</b> c\' und e\' bleiben liegen (Regel 2), nur g\' geht einen Schritt hoch zu a\'.</li><li><b>Am → F:</b> c\' und a\' bleiben liegen, e\' geht einen Halbtonschritt hoch zu f\'.</li><li><b>F → G:</b> Kein gemeinsamer Ton, alle gehen einen Schritt hoch: c\'→d\', f\'→g\', a\'→h\' (Regel 1). Auch h d\' g\' ist richtig.</li><li><b>G → C:</b> g\' bleibt liegen, d\'→e\', h\'→c\'\'. (Wenn du G als h d\' g\' geschrieben hast: dann c\' e\' g\', g\' bleibt liegen.)</li><li>Im Bass steht immer der Grundton (Regel 3): c, A, F, G, c.</li></ul></div>')
    return h + "</div>"

HEAD = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} – Musik</title>
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Musik">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="app.css?v={ver}">
</head>
<body data-page="{pid}">
<nav class="noprint" aria-label="Themen"><div class="wrap">
{nav}
</div></nav>
<main><div class="wrap">
"""
FOOT = """
</div></main>
<script src="app.js?v={ver}"></script>
</body>
</html>
"""
VER = "1"

def nav(cur):
    items = [("../index.html", "← Fächer", None), ("index.html", "🏠 Start", "start")]
    items += [(s["file"], s["nav"], s["id"]) for s in STEPS]
    out = []
    for h, t, i in items:
        a = f'  <a href="{h}"'
        if i and i != "start": a += f' data-id="{i}"'
        if i == cur: a += ' aria-current="page"'
        out.append(a + f'>{t}</a>')
    return "\n".join(out)

def page(pid, title, body):
    return HEAD.format(title=title, pid=pid, nav=nav(pid), ver=VER) + body + FOOT.format(ver=VER)

def nextbtn(i):
    s = STEPS[i]
    if i + 1 < len(STEPS):
        n = STEPS[i + 1]
        return f'<a class="btn big noprint" data-finish="{s["id"]}" href="{n["file"]}">Fertig ✓ – weiter zu {n["nav"]} →</a>'
    return f'<a class="btn big noprint" data-finish="{s["id"]}" href="index.html">Fertig ✓ – zurück zum Start</a>'

def part(n, name, hint):
    return f'<h2 class="part"><span class="num">{n}</span> {name}</h2>\n<p class="hint">{hint}</p>\n'

def write(name, text):
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(text)

def main():
    os.makedirs(OUT, exist_ok=True)
    b = '<h1>Musik</h1>\n<p class="sub">Klassenarbeit am Dienstag, 24.11.</p>\n'
    b += '<div class="box merke"><h3>So lernst du</h3><p>Mach die Themen <b>der Reihe nach</b>. Jedes Thema ist eine eigene Seite: erst lesen, dann Karten, dann üben, dann Quiz. Unten tippst du auf <b>„Fertig ✓“</b>.</p><p class="meta" id="st-left"></p></div>\n'
    b += '<div class="box"><h3>Das kommt in der Arbeit dran</h3><ul><li>Notennamen im Violin- und Bassschlüssel mit Oktavbezeichnungen</li><li>Intervalle Prime bis Oktave (Grobbestimmung)</li><li>Terzen: groß (4 HTS) oder klein (3 HTS)</li><li>Dur- und Molldreiklänge mit Grundton, Terzton, Quintton</li><li>Liedbegleitung mit Dreiklängen</li></ul><p class="meta">AFB 1: nennen und benennen. AFB 2: anwenden, notieren, erklären. AFB 3: eine Liedbegleitung komponieren.</p></div>\n'
    for i, s in enumerate(STEPS):
        b += f'<a class="step" data-step="{s["id"]}" href="{s["file"]}"><span class="num">{i+1}</span><span class="stxt"><b>{s["title"]}</b><span class="meta"> · {s["dur"]}</span><br><span class="meta">{s["desc"]}</span></span></a>\n'
    b += '<div class="box" id="st-all" hidden><h3>🎉 Super, alles geschafft!</h3><p>Du bist gut vorbereitet. Am Abend vor der Arbeit: nochmal das große Quiz.</p></div>\n'
    b += '<p><button class="btn ghost small" id="st-reset">Alle Haken löschen</button></p>'
    write("index.html", page("start", "Start", b))
    for i, s in enumerate(TOPICS):
        t = s["id"]
        b = f'<p class="crumb">Thema {i+1} von {len(TOPICS)}</p>\n<h1>{s["title"]}</h1>\n'
        b += part(1, "Lesen", "Lies alles einmal in Ruhe durch.") + LESEN[t]
        b += part(2, "Karten", "Überleg dir die Antwort. Dann tippe auf die Karte.") + '<div id="cards"></div>\n'
        n = 3
        for title, hint, tr in UEBEN[t]:
            b += part(n, title, hint) + f'<div data-trainer="{tr}"></div>\n'
            n += 1
        b += part(n, "Quiz", "Tippe auf die richtige Antwort.") + '<div id="quiz"></div>\n'
        b += nextbtn(i)
        write(s["file"], page(t, s["title"], b))
    b = '<h1>Großes Quiz</h1>\n<p class="hint">Alle Fragen aus allen Themen, bunt gemischt. Ziel: höchstens 5 Fehler.</p>\n<div id="quiz"></div>\n' + nextbtn(len(TOPICS))
    write("gemischt.html", page("gem", "Großes Quiz", b))
    tools = '<div class="row noprint"><button class="btn ghost" data-sol>Lösungen zeigen</button><button class="btn" data-print="0">Drucken</button><button class="btn ghost" data-print="1">Mit Lösungen drucken</button></div>\n'
    b = '<p class="hint noprint">So geht\'s: Drucke die Arbeit aus oder schreib die Antworten auf einen Zettel. Nimm dir 45 Minuten. Erst danach tippst du auf „Lösungen zeigen“ und vergleichst.</p>\n' + tools + probe() + "\n" + nextbtn(len(STEPS) - 1)
    write("probe.html", page("probe", "Probe-Arbeit", b))
    eng = open(os.path.join(B, "musik.engine.js"), encoding="utf-8").read()
    ui = open(os.path.join(B, "musik.ui.js"), encoding="utf-8").read()
    gl = open(os.path.join(B, "musik.glyphs.json"), encoding="utf-8").read()
    data = dict(cards=CARDS, quiz=QUIZ, steps=[s["id"] for s in STEPS], topics=[s["id"] for s in TOPICS], prog=PROG)
    js = "/* Notenzeichen: Bravura (SIL Open Font License, siehe _build/BRAVURA-LICENSE.txt) */\n" + eng + "\n" + ui.replace("__DATA__", json.dumps(data, ensure_ascii=False)).replace("__GLYPHS__", gl)
    write("app.js", js)
    css = open(os.path.join(B, "app.css"), encoding="utf-8").read() + "\n/* Musik */\n" + open(os.path.join(B, "musik.css"), encoding="utf-8").read()
    write("app.css", css)
    print("gebaut:", sorted(os.listdir(OUT)))

if __name__ == "__main__":
    main()
