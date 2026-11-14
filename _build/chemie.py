#!/usr/bin/env python3
"""Baut die Chemie-Seiten (eine Seite pro Thema) nach ../chemie/. Aufruf: python3 _build/chemie.py"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "chemie")
SRC = os.path.join(ROOT, "_build", "blaetter.html")  # Übungsblatt + Probe-Arbeit (Aufgaben)

TOPICS = [
 dict(id="t1", file="reaktion.html", nav="1 Reaktion", title="Was ist eine chemische Reaktion?", dur="10 Minuten", desc="Stoffumwandlung, Edukte und Produkte, Beispiele."),
 dict(id="t2", file="wortschema.html", nav="2 Wortschema", title="Das Wortschema", dur="10 Minuten", desc="Eine Reaktion in Worten aufschreiben."),
 dict(id="t3", file="energieformen.html", nav="3 Energie", title="Energieformen erkennen", dur="10 Minuten", desc="Wärme, Licht, Knall: Welche Energie ist das?"),
 dict(id="t4", file="exo-endo.html", nav="4 exo/endo", title="Exotherm und endotherm", dur="10 Minuten", desc="Wird Energie abgegeben oder aufgenommen?"),
 dict(id="t5", file="diagramme.html", nav="5 Pfeil-Bilder", title="Energieflussdiagramme (Pfeil-Bilder)", dur="15 Minuten", desc="Energie vorher, Vorgang, Energie nachher."),
 dict(id="t6", file="nachweise.html", nav="6 Nachweise", title="Kohlenstoffdioxid und Wasser nachweisen", dur="5 Minuten", desc="Kalkwasser und Watesmo-Papier."),
]
EXTRA = [
 dict(id="gem", file="gemischt.html", nav="7 Großes Quiz", title="Großes Quiz: alles gemischt", dur="15 Minuten", desc="Alle Fragen aus allen Themen durcheinander."),
 dict(id="probe", file="probe.html", nav="8 Probe-Arbeit", title="Probe-Arbeit", dur="45 Minuten", desc="Wie die echte Arbeit. Am besten am Montag."),
]
STEPS = TOPICS + EXTRA

LESEN = {
"t1": """
<div class="box merke"><h3>Das musst du wissen</h3>
<p>Eine chemische Reaktion erkennst du an zwei Dingen:</p>
<ul><li><b>Stoffumwandlung (immer):</b> Die Ausgangsstoffe werden verbraucht. Es entstehen <b>neue Stoffe mit neuen Eigenschaften</b>.</li>
<li><b>Energieumwandlung (meistens):</b> Energie wird aufgenommen oder abgegeben, zum Beispiel als Wärme oder Licht.</li></ul></div>
<div class="box"><h3>Zwei wichtige Wörter</h3>
<p><b>Edukte</b> sind die Ausgangsstoffe. Sie sind <b>vorher</b> da.</p>
<p><b>Produkte</b> sind die neuen Stoffe. Sie sind <b>nachher</b> da.</p>
<p>Beispiel aus dem Heft: Aus Holz wird Holzkohle hergestellt. Das Edukt ist Holz. Die Produkte sind Holzkohle, Teer, Holzgas und Holzflüssigkeit.</p></div>
<div class="box"><h3>Chemische Reaktion: ja oder nein?</h3>
<div class="tbl"><table><tr><th>Ja</th><th>Nein</th></tr>
<tr><td>Holz, Kerze oder Gas verbrennt</td><td>Eis schmilzt</td></tr>
<tr><td>Zucker karamellisiert</td><td>Wasser verdampft</td></tr>
<tr><td>Holzkohle wird aus Holz hergestellt</td><td>Eine LED leuchtet</td></tr>
<tr><td>Eisen rostet</td><td>Glas zerbricht</td></tr></table></div>
<p><b>Frag dich immer: Ist ein neuer Stoff entstanden?</b> Beim Schmelzen, Verdampfen oder Zerbrechen bleibt der Stoff derselbe. Wärme oder Licht allein reichen nicht: Eine LED leuchtet und wird warm, aber es entsteht kein neuer Stoff.</p>
<p>Beispiele für die Arbeit: <b>alle Verbrennungen</b> und <b>Karamellisieren</b>.</p></div>
""",
"t2": """
<div class="box merke"><h3>Das musst du wissen</h3>
<p>Ein Wortschema schreibt eine Reaktion in Worten auf.</p>
<ul><li><b>Links</b> stehen die Edukte, <b>rechts</b> die Produkte.</li>
<li>Den Pfeil → liest du <b>„reagiert zu“</b>.</li>
<li>Das Plus + liest du <b>„und“</b>.</li>
<li>Zustände: <b>(s)</b> fest, <b>(l)</b> flüssig, <b>(g)</b> gasförmig.</li></ul></div>
<div class="box"><h3>Beispiele</h3>
<div class="schema">Holz<sub>(s)</sub> → Holzkohle<sub>(s)</sub> + Teer<sub>(l)</sub> + Holzgas<sub>(g)</sub> + Holzflüssigkeit<sub>(l)</sub></div>
<p class="meta">Gelesen: Holz reagiert zu Holzkohle und Teer und Holzgas und Holzflüssigkeit.</p>
<div class="schema">Kerzenwachs + Sauerstoff → Kohlenstoffdioxid + Wasser</div>
<div class="schema">Holzkohle<sub>(s)</sub> + Sauerstoff<sub>(g)</sub> → Kohlenstoffdioxid<sub>(g)</sub></div></div>
<div class="box"><h3>Aus dem Heft: Herstellung von Holzkohle</h3>
<div class="tbl"><table><tr><th>Produkt</th><th>Eigenschaften</th></tr>
<tr><td>Holzkohle</td><td>fest, schwarz, Brennstoff</td></tr>
<tr><td>Teer</td><td>flüssig, schwarz, für Straßenbau und Schiffsbau (Dichtung)</td></tr>
<tr><td>Holzgas</td><td>gasförmig, intensiver Rauchgeruch, Brennstoff</td></tr>
<tr><td>Holzflüssigkeit</td><td>bräunlich, nicht brennbar</td></tr></table></div>
<p>Das Edukt Holz ist fest, brennbar und ein Brennstoff und Baumaterial.</p></div>
""",
"t3": """
<div class="box merke"><h3>Das musst du wissen</h3>
<p>Aus dem, was du beobachtest, erkennst du die Energieform:</p>
<div class="tbl"><table><tr><th>Das beobachtest du</th><th>Energieform</th></tr>
<tr><td>wird warm oder heiß</td><td><span class="tag e-th">thermische Energie (Wärme)</span></td></tr>
<tr><td>leuchtet, Lichtblitz, Flamme</td><td><span class="tag e-st">Strahlungsenergie (Licht)</span></td></tr>
<tr><td>Knall, Zischen, Knistern</td><td><span class="tag e-sc">Schallenergie</span></td></tr>
<tr><td>etwas fliegt weg oder bewegt sich</td><td><span class="tag e-be">Bewegungsenergie</span></td></tr>
<tr><td>Strom aus Steckdose oder Batterie</td><td><span class="tag e-el">elektrische Energie</span></td></tr>
<tr><td>steckt in den Stoffen</td><td><span class="tag e-chem">chemische Energie = Enthalpie</span></td></tr></table></div></div>
<div class="box"><h3>Enthalpie</h3>
<p><b>Enthalpie = chemische Energie.</b> Sie ist in den Stoffen gespeichert. Man sagt „Enthalpie der Edukte“ (vorher) und „Enthalpie der Produkte“ (nachher).</p></div>
<div class="box"><h3>Aus dem Heft: die Knalldose</h3>
<ul><li>Der Deckel fliegt weg → <b>Bewegungsenergie</b></li>
<li>Es knallt → <b>Schallenergie</b></li>
<li>Die Dose wird wärmer → <b>thermische Energie</b></li>
<li>Lichtblitz → <b>Strahlungsenergie</b></li></ul>
<p>Vorher: Zündfunke und Enthalpie der Edukte. Nachher: Strahlungsenergie, thermische Energie, Enthalpie der Produkte, Bewegungsenergie des Deckels und Schallenergie.</p></div>
""",
"t4": """
<div class="box merke"><h3>Das musst du wissen</h3>
<p><span class="badge b-exo">exotherm</span> Energie wird an die Umgebung <b>abgegeben</b>, zum Beispiel als Wärme oder Licht.<br><span class="meta">exo = hinaus, therm = Wärme</span></p>
<p><span class="badge b-endo">endotherm</span> Energie wird aus der Umgebung <b>aufgenommen</b>.<br><span class="meta">endo = hinein, therm = Wärme</span></p></div>
<div class="box"><h3>So erkennst du es</h3>
<ul><li>Es wird <b>warm</b> oder es <b>leuchtet</b> → exotherm</li>
<li>Es wird <b>kälter</b> → endotherm</li></ul></div>
<div class="box"><h3>Die drei Beispiele aus dem Heft</h3>
<p><b>Lagerfeuer:</b> <span class="badge b-exo">exotherm</span> Es gibt Wärme und Licht ab. Zum Anzünden braucht man nur wenig Energie, abgegeben wird viel mehr.</p>
<p><b>Luminol:</b> <span class="badge b-exo">exotherm</span> Es leuchtet. Die Energie wird als Licht abgegeben, auch wenn es nicht warm wird.</p>
<p><b>Kaliumiodid in Wasser lösen:</b> <span class="badge b-endo">endotherm</span> Die Lösung wird kälter, weil Wärme aus der Umgebung aufgenommen wird.</p></div>
""",
"t5": """
<div class="box merke"><h3>Das musst du wissen</h3>
<p>Ein Energieflussdiagramm zeigt, wie Energie umgewandelt wird. Es hat drei Teile:</p>
<ul><li><b>Links:</b> Energieformen <b>vorher</b></li>
<li><b>Mitte:</b> der Vorgang (der Energiewandler)</li>
<li><b>Rechts:</b> Energieformen <b>nachher</b></li></ul>
<div data-diag="led"></div>
<p class="meta">Beispiel aus dem Heft: Die Lampe (LED) ist der Energiewandler.</p></div>
<div class="box"><h3>So zeichnest du eins</h3>
<ol><li>Was passiert? Das kommt in die <b>Mitte</b>.</li>
<li>Welche Energie ist vorher da? Das kommt nach <b>links</b>. Bei chemischen Reaktionen immer: Enthalpie der Edukte.</li>
<li>Welche Energie ist nachher da? Das kommt nach <b>rechts</b>. Bei chemischen Reaktionen immer: Enthalpie der Produkte.</li>
<li>Schreib <b>exotherm</b> oder <b>endotherm</b> darunter.</li></ol></div>
<div class="box"><h3>Die Beispiele aus dem Heft</h3>
<p><b>Lagerfeuer</b> <span class="badge b-exo">exotherm</span></p><div data-diag="feuer"></div>
<p class="meta">Die thermische Energie links ist der Zündfunke zum Anzünden.</p>
<p><b>Luminol leuchtet</b> <span class="badge b-exo">exotherm</span></p><div data-diag="luminol"></div>
<p class="meta">Es wird nicht wärmer. Deshalb steht rechts keine thermische Energie.</p>
<p><b>Kaliumiodid in Wasser lösen</b> <span class="badge b-endo">endotherm</span></p><div data-diag="ki"></div>
<p class="meta">Die Wärme aus der Umgebung steht links. Deshalb wird die Lösung kälter.</p>
<p><b>Knalldose</b> <span class="badge b-exo">exotherm</span></p><div data-diag="knall"></div></div>
""",
"t6": """
<div class="box merke"><h3>Das musst du wissen</h3>
<div class="tbl"><table><tr><th>Stoff</th><th>So weist man ihn nach</th><th>Das sieht man</th></tr>
<tr><td><b>Kohlenstoffdioxid</b></td><td>Gas in Kalkwasser leiten (Kalkwasserprobe)</td><td>Kalkwasser wird <b>trüb</b></td></tr>
<tr><td><b>Wasser</b></td><td>Watesmo-Papier oder weißes Kupfersulfat</td><td>färbt sich <b>blau</b></td></tr></table></div></div>
<div class="box"><h3>Ergebnisse auswerten</h3>
<ul><li>Kalkwasser wird trüb → Kohlenstoffdioxid ist nachgewiesen.</li>
<li>Kalkwasser bleibt klar → Es ist kein Kohlenstoffdioxid nachweisbar.</li>
<li>Watesmo-Papier wird blau → Wasser ist nachgewiesen.</li></ul>
<p>Beispiel: Über einer brennenden Kerze wird Kalkwasser trüb und Watesmo-Papier blau. Also entstehen beim Verbrennen Kohlenstoffdioxid und Wasser.</p></div>
""",
}

CARDS = {
"t1": [
 ["Was ist eine chemische Reaktion?", "Ein Vorgang, bei dem aus Edukten neue Stoffe mit neuen Eigenschaften entstehen (Produkte). Meistens wird dabei auch Energie umgewandelt."],
 ["Edukt", "Ausgangsstoff einer chemischen Reaktion. Er ist vorher da."],
 ["Produkt", "Stoff, der bei der Reaktion neu entsteht. Er ist nachher da."],
 ["Stoffumwandlung", "Die Edukte werden verbraucht, und Produkte mit neuen Eigenschaften entstehen."],
 ["Energieumwandlung", "Eine Energieform wird in eine andere umgewandelt, z. B. chemische Energie in Wärme und Licht."],
 ["Ist Eisschmelzen eine chemische Reaktion?", "Nein. Es entsteht kein neuer Stoff, nur der Zustand ändert sich."],
 ["Nenne zwei Beispiele für chemische Reaktionen.", "Alle Verbrennungen (z. B. Holz, Kerze) und Karamellisieren."],
],
"t2": [
 ["Wo stehen im Wortschema die Edukte?", "Links vom Pfeil."],
 ["Wo stehen im Wortschema die Produkte?", "Rechts vom Pfeil."],
 ["Wie liest man den Pfeil → im Wortschema?", "„reagiert zu“ oder „reagieren zu“"],
 ["Wie liest man das Plus + im Wortschema?", "„und“"],
 ["(s), (l), (g)", "fest, flüssig, gasförmig"],
 ["Wortschema: Herstellung von Holzkohle", "Holz(s) → Holzkohle(s) + Teer(l) + Holzgas(g) + Holzflüssigkeit(l)"],
 ["Wortschema: Eine Kerze brennt", "Kerzenwachs + Sauerstoff → Kohlenstoffdioxid + Wasser"],
],
"t3": [
 ["Beobachtung: Es wird warm", "thermische Energie (Wärme)"],
 ["Beobachtung: Lichtblitz", "Strahlungsenergie"],
 ["Beobachtung: Knall", "Schallenergie"],
 ["Beobachtung: Deckel fliegt weg", "Bewegungsenergie"],
 ["Strom aus der Batterie", "elektrische Energie"],
 ["Enthalpie", "Die chemische Energie, die in Stoffen gespeichert ist."],
],
"t4": [
 ["exotherm", "Energie wird an die Umgebung abgegeben (exo = hinaus, therm = Wärme). Beispiel: jede Verbrennung."],
 ["endotherm", "Energie wird aus der Umgebung aufgenommen (endo = hinein). Beispiel: Kaliumiodid lösen, die Lösung wird kälter."],
 ["Kaliumiodid wird in Wasser gelöst. Exotherm oder endotherm?", "Endotherm. Die Lösung wird kälter."],
 ["Warum ist ein Lagerfeuer exotherm, obwohl man es anzünden muss?", "Zum Anzünden braucht man nur wenig Energie. Abgegeben wird viel mehr Energie als Wärme und Licht."],
 ["Warum ist Luminol exotherm, obwohl es nicht warm wird?", "Die Energie wird als Licht (Strahlungsenergie) an die Umgebung abgegeben."],
],
"t5": [
 ["Was steht im Energieflussdiagramm links?", "Die Energieformen vorher."],
 ["Was steht im Energieflussdiagramm in der Mitte?", "Der Vorgang bzw. der Energiewandler, z. B. „Chemische Reaktion (Verbrennung)“."],
 ["Was steht im Energieflussdiagramm rechts?", "Die Energieformen nachher."],
 ["Was steht bei einer chemischen Reaktion immer links und rechts?", "Links: Enthalpie der Edukte. Rechts: Enthalpie der Produkte."],
 ["LED-Lampe: Was ist vorher, was nachher?", "Vorher: elektrische Energie. Nachher: Wärme und Strahlungsenergie."],
],
"t6": [
 ["Nachweis von Kohlenstoffdioxid", "Kalkwasserprobe: Kalkwasser wird trüb."],
 ["Nachweis von Wasser", "Watesmo-Papier oder weißes Kupfersulfat färbt sich blau."],
 ["Kalkwasser bleibt klar. Was bedeutet das?", "Es ist kein Kohlenstoffdioxid nachweisbar."],
 ["Watesmo-Papier wird blau. Was ist nachgewiesen?", "Wasser."],
],
}

# Erste Antwort ist jeweils die richtige; wird in der App gemischt.
QUIZ = {
"t1": [
 ["Woran erkennt man sicher eine chemische Reaktion?", ["Es entsteht ein neuer Stoff mit neuen Eigenschaften.", "Es wird warm.", "Etwas leuchtet.", "Etwas ändert seine Form."], "Wärme und Licht gibt es auch ohne Reaktion, zum Beispiel bei einer Lampe. Entscheidend ist der neue Stoff."],
 ["Welcher Vorgang ist eine chemische Reaktion?", ["Zucker karamellisiert.", "Eis schmilzt.", "Wasser verdampft.", "Eine LED leuchtet."], "Beim Karamellisieren entsteht ein neuer Stoff. Schmelzen und Verdampfen ändern nur den Zustand."],
 ["Welcher Vorgang ist keine chemische Reaktion?", ["Glas zerbricht.", "Holz verbrennt.", "Eisen rostet.", "Eine Kerze brennt."], "Beim Zerbrechen bleibt es Glas. Es ändert sich nur die Form."],
 ["Was sind Edukte?", ["die Ausgangsstoffe einer Reaktion", "die Stoffe, die neu entstehen", "die Energieformen nach der Reaktion", "die Geräte im Versuch"], "Edukte sind die Ausgangsstoffe. Sie sind vorher da."],
 ["Was sind Produkte?", ["die Stoffe, die bei der Reaktion neu entstehen", "die Ausgangsstoffe einer Reaktion", "die Energieformen vor der Reaktion", "die Beobachtungen im Versuch"], "Produkte sind die neuen Stoffe. Sie sind nachher da."],
 ["Was passiert bei einer Reaktion mit den Edukten?", ["Sie werden verbraucht und in Produkte umgewandelt.", "Sie verschwinden einfach spurlos.", "Sie bleiben unverändert.", "Sie werden komplett zu Energie."], "Aus den Edukten werden neue Stoffe, die Produkte."],
],
"t2": [
 ["Wo stehen im Wortschema die Produkte?", ["rechts vom Pfeil", "links vom Pfeil", "über dem Pfeil", "unter dem Pfeil"], "Edukte links, Produkte rechts."],
 ["Wie liest man den Pfeil → im Wortschema?", ["reagiert zu", "ist gleich", "und", "minus"], "Der Pfeil heißt „reagiert zu“. Das Plus heißt „und“."],
 ["Was bedeutet die Angabe (g)?", ["gasförmig", "fest", "flüssig", "gefärbt"], "(s) fest, (l) flüssig, (g) gasförmig."],
 ["Was bedeutet die Angabe (s)?", ["fest", "flüssig", "gasförmig", "schwarz"], "(s) fest, (l) flüssig, (g) gasförmig."],
 ["Welches Wortschema beschreibt die Herstellung von Holzkohle?", ["Holz → Holzkohle + Teer + Holzgas + Holzflüssigkeit", "Holzkohle → Holz + Teer + Holzgas", "Holz + Teer → Holzkohle + Holzgas", "Holz → Holzkohle"], "Das Edukt ist Holz. Es entstehen vier Produkte."],
 ["Welches Wortschema beschreibt eine brennende Kerze?", ["Kerzenwachs + Sauerstoff → Kohlenstoffdioxid + Wasser", "Kohlenstoffdioxid + Wasser → Kerzenwachs + Sauerstoff", "Kerzenwachs → Sauerstoff + Wasser", "Kerzenwachs + Wasser → Kohlenstoffdioxid"], "Wachs reagiert mit Sauerstoff aus der Luft."],
],
"t3": [
 ["Knalldose: Der Deckel fliegt weg. Welche Energieform ist das?", ["Bewegungsenergie", "Schallenergie", "Strahlungsenergie", "elektrische Energie"], "Alles, was sich bewegt, hat Bewegungsenergie."],
 ["Knalldose: Es gibt einen lauten Knall. Welche Energieform ist das?", ["Schallenergie", "Bewegungsenergie", "thermische Energie", "Strahlungsenergie"], "Ein Knall ist Schall."],
 ["Die Dose wird wärmer. Welche Energieform ist das?", ["thermische Energie", "Strahlungsenergie", "Schallenergie", "elektrische Energie"], "Wärme ist thermische Energie."],
 ["Ein Lichtblitz ist zu sehen. Welche Energieform ist das?", ["Strahlungsenergie", "thermische Energie", "Bewegungsenergie", "Schallenergie"], "Licht ist Strahlungsenergie."],
 ["Wie heißt die chemische Energie, die in Stoffen gespeichert ist?", ["Enthalpie", "Temperatur", "Strahlung", "Masse"], "Enthalpie = chemische Energie."],
 ["Eine LED-Lampe wandelt elektrische Energie um in …", ["Strahlungsenergie und Wärme", "Enthalpie", "Bewegungsenergie", "Schallenergie"], "Die LED leuchtet und wird etwas warm."],
],
"t4": [
 ["Was bedeutet exotherm?", ["Energie wird an die Umgebung abgegeben.", "Energie wird aus der Umgebung aufgenommen.", "Es wird gar keine Energie umgewandelt.", "Es entsteht kein neuer Stoff."], "exo = hinaus, therm = Wärme."],
 ["Was bedeutet endotherm?", ["Energie wird aus der Umgebung aufgenommen.", "Energie wird an die Umgebung abgegeben.", "Es knallt.", "Es entsteht ein Gas."], "endo = hinein, therm = Wärme."],
 ["Kaliumiodid wird in Wasser gelöst, die Lösung wird kälter. Der Vorgang ist …", ["endotherm", "exotherm"], "Wärme wird aus der Umgebung aufgenommen, deshalb wird es kälter."],
 ["Luminol leuchtet, aber die Temperatur bleibt gleich. Die Reaktion ist …", ["exotherm, weil Energie als Licht abgegeben wird.", "endotherm, weil es nicht warm wird.", "endotherm, weil Licht aufgenommen wird.", "weder exotherm noch endotherm."], "Auch Licht ist abgegebene Energie. Exotherm heißt nicht nur „wird warm“."],
 ["Ein Lagerfeuer muss man erst anzünden. Die Verbrennung ist trotzdem …", ["exotherm", "endotherm"], "Zum Anzünden braucht man nur wenig Energie. Abgegeben wird viel mehr Energie als Wärme und Licht."],
],
"t5": [
 ["Was steht in der Mitte eines Energieflussdiagramms?", ["der Vorgang bzw. der Energiewandler", "die Energieformen vorher", "die Energieformen nachher", "die Temperatur"], "Links vorher, Mitte Vorgang, rechts nachher."],
 ["Was steht links in einem Energieflussdiagramm?", ["die Energieformen vorher", "die Energieformen nachher", "die Produkte", "exotherm oder endotherm"], "Links vorher, Mitte Vorgang, rechts nachher."],
 ["Lagerfeuer: Was steht rechts?", ["Enthalpie der Produkte, thermische Energie, Strahlungsenergie", "nur thermische Energie", "Enthalpie der Edukte und thermische Energie", "elektrische Energie und Strahlungsenergie"], "Nachher sind die Produkte da, und das Feuer gibt Wärme und Licht ab."],
 ["Kaliumiodid lösen: Was steht links neben der Enthalpie der Edukte?", ["thermische Energie", "Strahlungsenergie", "Schallenergie", "nichts"], "Die Wärme wird aus der Umgebung aufgenommen. Deshalb steht sie links."],
 ["Luminol: Warum steht rechts keine thermische Energie?", ["Weil sich die Temperatur nicht ändert.", "Weil Luminol kalt ist.", "Weil Licht keine Energie ist.", "Weil die Reaktion endotherm ist."], "Luminol leuchtet nur. Es wird nicht wärmer."],
],
"t6": [
 ["Wie weist man Kohlenstoffdioxid nach?", ["Kalkwasser wird trüb.", "Watesmo-Papier wird blau.", "Weißes Kupfersulfat wird blau.", "Ein glimmender Span flammt auf."], "Das ist die Kalkwasserprobe. Der aufflammende Span weist Sauerstoff nach."],
 ["Wie weist man Wasser nach?", ["Watesmo-Papier wird blau.", "Kalkwasser wird trüb.", "Ein glimmender Span flammt auf.", "Kalkwasser bleibt klar."], "Auch weißes Kupfersulfat färbt sich mit Wasser blau."],
 ["Ein Gas wird in Kalkwasser geleitet. Das Kalkwasser bleibt klar. Was folgt daraus?", ["Im Gas ist kein Kohlenstoffdioxid nachweisbar.", "Das Gas ist Kohlenstoffdioxid.", "Das Gas ist Wasser.", "Das Kalkwasser ist kaputt."], "Nur trübes Kalkwasser zeigt Kohlenstoffdioxid an."],
 ["Über einer Kerze wird Kalkwasser trüb und Watesmo-Papier blau. Was entsteht beim Verbrennen?", ["Kohlenstoffdioxid und Wasser", "nur Kohlenstoffdioxid", "nur Wasser", "Sauerstoff und Wasser"], "Trübes Kalkwasser zeigt Kohlenstoffdioxid, blaues Watesmo-Papier zeigt Wasser."],
],
}

HEAD = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} – Chemie</title>
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
VER = "11"

def nav(cur):
    items = [("../index.html", "← Fächer", None), ("index.html", "🏠 Start", "start")]
    items += [(s["file"], s["nav"], s["id"]) for s in STEPS]
    items.append(("blatt.html", "Extra-Blatt", "blatt"))
    return "\n".join(f'  <a href="{h}"{" aria-current=\"page\"" if i == cur else ""}>{t}</a>' for h, t, i in items)

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

def blatt(sec):
    h = open(SRC, encoding="utf-8").read()
    m = re.search(rf'<!--{sec}-->(.*?)<!--/{sec}-->', h, re.S)
    return m.group(1).strip()

def main():
    os.makedirs(OUT, exist_ok=True)
    # Start
    b = '<h1>Chemie</h1>\n<p class="sub">Arbeit am Dienstag, 17.11.</p>\n'
    b += '<div class="box merke"><h3>So lernst du</h3><p>Mach die Themen <b>der Reihe nach</b>. Jedes Thema ist eine eigene Seite: erst lesen, dann Karten, dann Quiz. Unten tippst du auf <b>„Fertig ✓“</b>.</p><p class="meta" id="st-left"></p></div>\n'
    for i, s in enumerate(STEPS):
        b += f'<a class="step" data-step="{s["id"]}" href="{s["file"]}"><span class="num">{i+1}</span><span class="stxt"><b>{s["title"]}</b><span class="meta"> · {s["dur"]}</span><br><span class="meta">{s["desc"]}</span></span></a>\n'
    b += '<a class="step extra" href="blatt.html"><span class="num">+</span><span class="stxt"><b>Extra: Übungsblatt</b><br><span class="meta">Noch mehr Aufgaben zum Ausdrucken, wenn du Lust hast.</span></span></a>\n'
    b += '<div class="box" id="st-all" hidden><h3>🎉 Super, alles geschafft!</h3><p>Du bist gut vorbereitet. Am Abend vor der Arbeit: nochmal das große Quiz.</p></div>\n'
    b += '<p><button class="btn ghost small" id="st-reset">Alle Haken löschen</button></p>'
    write("index.html", page("start", "Start", b))
    # Themen
    for i, s in enumerate(TOPICS):
        t = s["id"]
        b = f'<p class="crumb">Thema {i+1} von {len(TOPICS)}</p>\n<h1>{s["title"]}</h1>\n'
        b += part(1, "Lesen", "Lies alles einmal in Ruhe durch.") + LESEN[t]
        b += part(2, "Karten", "Überleg dir die Antwort. Dann tippe auf die Karte.") + '<div id="cards"></div>\n'
        n = 3
        if t == "t5":
            b += part(3, "Pfeil-Bilder bauen", "Bau das Pfeil-Bild selbst: Zieh die Pfeile mit dem Finger an die richtige Stelle. Dann tippe auf „Prüfen“.") + '<div class="picker" id="b-pick"></div>\n<div class="box" id="b-area"></div>\n'
            n = 4
        b += part(n, "Quiz", "Tippe auf die richtige Antwort.") + '<div id="quiz"></div>\n'
        b += nextbtn(i)
        write(s["file"], page(t, s["title"], b))
    # Großes Quiz
    b = '<h1>Großes Quiz</h1>\n<p class="hint">Alle Fragen aus allen Themen, bunt gemischt. Ziel: höchstens 4 Fehler.</p>\n<div id="quiz"></div>\n' + nextbtn(len(TOPICS))
    write("gemischt.html", page("gem", "Großes Quiz", b))
    # Probe-Arbeit und Blatt
    def tools(): return '<div class="row noprint"><button class="btn ghost" data-sol>Lösungen zeigen</button><button class="btn" data-print="0">Drucken</button><button class="btn ghost" data-print="1">Mit Lösungen drucken</button></div>\n'
    b = '<p class="hint noprint">So geht\'s: Drucke die Arbeit aus oder schreib die Antworten auf einen Zettel. Nimm dir 45 Minuten. Erst danach tippst du auf „Lösungen zeigen“ und vergleichst.</p>\n' + tools() + blatt("pk") + "\n" + nextbtn(len(STEPS) - 1)
    write("probe.html", page("probe", "Probe-Arbeit", b))
    b = '<p class="hint noprint">Extra-Aufgaben zum Ausdrucken. Mit „Lösungen zeigen“ kannst du vergleichen.</p>\n' + tools() + blatt("ub")
    write("blatt.html", page("blatt", "Übungsblatt", b))
    # JS-Daten
    js = open(os.path.join(ROOT, "_build", "app.src.js"), encoding="utf-8").read()
    data = dict(cards=CARDS, quiz=QUIZ, steps=[s["id"] for s in STEPS], topics=[s["id"] for s in TOPICS])
    write("app.js", js.replace("__DATA__", json.dumps(data, ensure_ascii=False)))
    write("app.css", open(os.path.join(ROOT, "_build", "app.css"), encoding="utf-8").read())
    print("gebaut:", sorted(os.listdir(OUT)))

if __name__ == "__main__":
    main()
