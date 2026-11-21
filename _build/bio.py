#!/usr/bin/env python3
"""Baut die Biologie-Seiten nach ../biologie/. Aufruf: python3 _build/bio.py
Themen nach der Liste von Frau Brinkmann (Klasse 7). Quellen: Biologie-Buch S. 14–15, 18, 20, 22–27, 34–37.
Mikroskop (S. 18) und Zelle → Organismus (S. 20) stehen in bio_teil1.py und laufen hier als Zusatz."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bio_teil1 as A
from bio_svg import mikroskop, blatt, pflanzenzelle, tierzelle, blaeschen_chart, MIKRO_TEILE, BLATT_TEILE, PFL_TEILE, TIER_TEILE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "biologie")
KLAUSUR = "Klassenarbeit am Mittwoch, 25.11."
VER = "2"

TOPICS = [
 dict(id="t3", file="forschen.html", nav="1 Helmont & Priestley", title="Van Helmont und Priestley", dur="20 Minuten", desc="Was haben sie gemacht, was herausgefunden, welche neuen Fragen gab es? Buch S. 22–23."),
 dict(id="texp", file="experimente.html", nav="2 Experimente", title="Eigene Experimente planen und auswerten", dur="20 Minuten", desc="Versuchsprotokoll, Kontrollversuch, was man misst und was gleich bleiben muss. Buch S. 27."),
 dict(id="t4", file="laubblatt.html", nav="3 Blattquerschnitt", title="Der Blattquerschnitt", dur="20 Minuten", desc="Namen der Bauteile, Funktionen und Angepasstheiten. Buch S. 24–27."),
 dict(id="tzell", file="zellvergleich.html", nav="4 Tier & Pflanze", title="Tier- und Pflanzenzellen im Vergleich", dur="15 Minuten", desc="Was haben beide, was hat nur die Pflanzenzelle? Buch S. 14."),
 dict(id="tatm", file="zellatmung.html", nav="5 Zellatmung", title="Die Zellatmung", dur="20 Minuten", desc="Wortgleichung, Ort, Stofftransport und der Vergleich mit der Fotosynthese. Buch S. 34–37."),
]
EXTRA = [
 dict(id="gem", file="gemischt.html", nav="Großes Quiz", title="Großes Quiz: alles gemischt", dur="20 Minuten", desc="Alle Fragen aus den fünf Themen durcheinander."),
 dict(id="probe", file="probe.html", nav="Probe-Arbeit", title="Probe-Arbeit", dur="45 Minuten", desc="Aufgaben wie in der Arbeit, mit Lösungen zum Vergleichen."),
]
ZUSATZ = [
 dict(id="t1", file="mikroskop.html", nav="Zusatz: Mikroskop", title="Zusatz: Das Lichtmikroskop", dur="15 Minuten", desc="Zum Wiederholen. Buch S. 18."),
 dict(id="t2", file="zellen.html", nav="Zusatz: Zelle → Organismus", title="Zusatz: Zelle, Gewebe, Organ, Organismus", dur="10 Minuten", desc="Zum Wiederholen. Buch S. 20."),
]
STEPS = TOPICS + EXTRA

# ================================================================ LESEN
helmont = A.LESEN["t3"][A.LESEN["t3"].index('<div class="box"><h3>Das Weiden-Experiment'):]

LESEN = {
"t3": """
<div class="box merke"><h3>Das musst du wissen</h3>
<ul><li><b>Van Helmont (um 1640):</b> Eine Weide wurde in 5 Jahren 74,4 kg schwerer, die Erde nur 57 g leichter. Er dachte: Die Masse kommt vor allem vom Wasser.</li>
<li><b>Priestley (1771):</b> Tiere überleben in luftdicht abgeschlossenen Räumen sehr viel länger, wenn Pflanzen dabei sind. Die Pflanzen verändern also die <b>Luft</b>.</li>
<li><b>Neue Fragen:</b> Welcher Stoff in der Luft ist das? Warum läuft der Versuch nachts anders als am Tag? Was braucht die Pflanze dafür? Die Antworten fanden spätere Forscher (Erkenntnisspirale).</li></ul></div>
""" + helmont + """
<div class="box"><h3>Die Versuche von Joseph Priestley (1771, Buch S. 23)</h3>
<p>Priestley stellte Dinge unter eine luftdicht abgeschlossene Glasglocke:</p>
<div class="tbl"><table>
<tr><th>Versuch</th><th>Unter der Glocke</th><th>Beobachtung</th></tr>
<tr><td><b>a</b></td><td>brennende Kerze</td><td>Die Kerze erlosch nach einiger Zeit.</td></tr>
<tr><td><b>b</b></td><td>brennende Kerze und Maus</td><td>Die Kerze erlosch nach <b>viel kürzerer</b> Zeit als bei a. Die Maus wurde nach kurzer Zeit ohnmächtig.</td></tr>
<tr><td><b>c</b></td><td>nur eine Maus</td><td>Die Maus wurde ohnmächtig, aber erst nach <b>längerer</b> Zeit als bei b.</td></tr>
<tr><td><b>d</b></td><td>Maus und Pflanze</td><td>Die Maus wurde <b>nicht</b> ohnmächtig.</td></tr>
</table></div>
<p><b>Was Priestley herausfand:</b> Tiere überleben in luftdicht abgeschlossenen Räumen sehr viel länger, wenn Pflanzen anwesend sind. Außerdem beobachtete er, dass seine Versuche <b>abends und nachts anders abliefen als am Tag</b>.</p>
<p><b>Mehr als van Helmont:</b> Van Helmont dachte nur an Erde und Wasser. Priestley zeigte: Pflanzen verändern die Luft, sodass Tiere darin leben können.</p>
<p class="meta">Versuch c ist der Kontrollversuch zu d: Alles ist gleich, nur die Pflanze fehlt.</p></div>
<div class="box"><h3>So erklärt man Priestleys Versuche heute</h3>
<p>Mit dem Wissen der späteren Forscher (Lavoisier, Ingenhousz, Senebier):</p>
<ul><li>Die Kerze braucht zum Brennen <b>Sauerstoff</b>. Die Maus braucht ihn zum Atmen.</li>
<li><b>b:</b> Kerze und Maus verbrauchen den Sauerstoff gemeinsam. Deshalb ist er schneller verbraucht als bei a oder c.</li>
<li><b>d:</b> Die Pflanze stellt im Licht Sauerstoff her. Dafür nutzt sie das Kohlenstoffdioxid, das die Maus beim Atmen abgibt.</li>
<li><b>Nachts</b> stellt die Pflanze keinen Sauerstoff her, sondern gibt Kohlenstoffdioxid ab. Deshalb liefen die Versuche nachts anders.</li></ul></div>
<div class="box"><h3>Die Erkenntnisspirale zur Fotosynthese (Buch S. 23)</h3>
<p>Jede Entdeckung warf neue Fragen auf, die spätere Forscher beantworteten:</p>
<div class="tbl"><table>
<tr><th>Jahr</th><th>Forscher</th><th>Erkenntnis</th></tr>
<tr><td>um 1640</td><td>van Helmont</td><td>fünfjähriger Versuch zur Pflanzenernährung (Weide)</td></tr>
<tr><td>1727</td><td>Stephen Hales</td><td>behauptet, dass Pflanzen ihre Nahrung aus der Luft aufnehmen. Das verstand damals niemand.</td></tr>
<tr><td>1771</td><td>Joseph Priestley</td><td>Tiere überleben in abgeschlossenen Räumen viel länger, wenn Pflanzen anwesend sind. Nachts laufen die Versuche anders.</td></tr>
<tr><td>1775</td><td>Antoine de Lavoisier</td><td>berichtet über ein neues Element, das die Verbrennung ermöglicht und das Lebewesen zum Atmen brauchen. Erst „l’air vital“ genannt, vier Jahre später <b>Sauerstoff</b>.</td></tr>
<tr><td>1779</td><td>Jan Ingenhousz</td><td>Pflanzen stellen <b>nur im Licht</b> Sauerstoff her, im Dunkeln geben sie Kohlenstoffdioxid ab. Nur die <b>grünen</b> Pflanzenteile stellen Sauerstoff her.</td></tr>
<tr><td>1783</td><td>Jean Senebier</td><td>Pflanzen stellen im Licht nur dann Sauerstoff her, wenn auch <b>Kohlenstoffdioxid</b> da ist.</td></tr>
<tr><td>1804</td><td>Nicolas de Saussure</td><td>Pflanzen brauchen dafür auch <b>Wasser</b>.</td></tr>
<tr><td>1837</td><td>René Dutrochet</td><td>Der grüne Blattfarbstoff <b>Chlorophyll</b> ist notwendig.</td></tr>
<tr><td>1845</td><td>Robert Meyer <span class="meta">(oft auch Julius Robert Mayer geschrieben)</span></td><td>Bei der Fotosynthese wird Lichtenergie in chemische Energie umgewandelt.</td></tr>
<tr><td>1862</td><td>Julius Sachs</td><td>Zucker und Stärke werden in den grünen Chloroplasten gebildet.</td></tr>
</table></div>
<p>Heute fasst man das so zusammen:</p>
<div class="eq">Wasser + Kohlenstoffdioxid → Glucose + Sauerstoff<br><span class="meta">mit Licht und Chlorophyll</span></div>
<p class="meta">Wichtig für die Arbeit sind vor allem van Helmont, Priestley und die Fragen, die danach offen waren.</p></div>
<div class="box"><h3>Der Weg der Erkenntnisgewinnung (Buch S. 23, Abb. 3)</h3>
<ol><li>Beobachtung oder Phänomen</li><li>Formulierung des Phänomens</li><li>Aufstellen der Problemfrage</li><li>Formulierung von Hypothesen</li><li>Entwicklung der Lösungsstrategie</li><li>Durchführung der Untersuchungen</li><li>Formulierung eines Ergebnisses unter Rückbezug auf die Hypothesen</li><li>Erweiterung des Ergebnisses</li><li>Erkenntnisgewinn – Verallgemeinerung</li></ol>
<p>Eine <b>Hypothese</b> ist eine begründete Vermutung. Das Experiment ist eine besonders wichtige Untersuchungsmethode.</p></div>
""",

"texp": f"""
<div class="box merke"><h3>Das musst du wissen</h3>
<ul><li>Verändere <b>nur eine Bedingung</b>. Alles andere bleibt <b>gleich</b>: gleich lange Pflanzen, gleich viel Wasser, gleiche Temperatur, gleiches Licht, gleiche Dauer …</li>
<li>Lege vorher fest, <b>was du misst</b> und womit, zum Beispiel „Bläschen pro Minute“ oder „Länge in cm mit dem Lineal“.</li>
<li><b>Kontrollversuch nicht vergessen!</b> Er ist genauso aufgebaut, aber die untersuchte Bedingung wird <b>nicht</b> verändert. Erst der Vergleich zeigt, ob die Bedingung wirklich die Ursache ist.</li></ul></div>
<div class="box"><h3>Das Versuchsprotokoll</h3>
<p>So ist ein Protokoll aufgebaut:</p>
<ol><li><b>Frage:</b> Was will ich herausfinden?</li>
<li><b>Hypothese:</b> Was vermute ich und warum? (begründete Vermutung)</li>
<li><b>Material:</b> Was brauche ich?</li>
<li><b>Durchführung:</b> Wie baue ich den Versuch auf und was mache ich, Schritt für Schritt? Dazu gehört eine Skizze vom Versuchsaufbau.</li>
<li><b>Beobachtung:</b> Was sehe oder messe ich? Messwerte kommen in eine Tabelle.</li>
<li><b>Deutung (Auswertung):</b> Was bedeutet das? Stimmt die Hypothese? Was ist die Antwort auf die Frage?</li></ol>
<p class="meta">Falls im Heft andere Überschriften stehen, nimm die aus dem Heft.</p></div>
<div class="box"><h3>Drei Fragen beim Planen</h3>
<div class="tbl"><table>
<tr><th>Frage</th><th>Beispiel: Kohlenstoffdioxid und Fotosynthese (Buch S. 27)</th></tr>
<tr><td><b>Was verändere ich?</b> (nur eins!)</td><td>die Menge an Kohlenstoffdioxid im Wasser: einmal nur Leitungswasser, einmal Leitungswasser mit sprudelndem Mineralwasser (Sprudel enthält Kohlenstoffdioxid)</td></tr>
<tr><td><b>Was messe ich?</b></td><td>die Zahl der Sauerstoff-Bläschen pro Minute</td></tr>
<tr><td><b>Was bleibt gleich?</b></td><td>dieselbe Wasserpest-Pflanze, Wassertemperatur 20 °C, gleiche Lampe im gleichen Abstand, gleich viel Wasser im Glas, jeweils eine Minute zählen</td></tr>
<tr><td><b>Kontrollversuch</b></td><td>der Ansatz mit reinem Leitungswasser: Hier wird die Kohlenstoffdioxid-Menge nicht verändert.</td></tr>
</table></div>
<p><b>Tipp:</b> Nimm mehrere Pflanzen oder wiederhole die Messung. Dann kann ein Zufall das Ergebnis nicht so leicht verfälschen.</p></div>
<div class="box"><h3>Die Bläschenzählmethode (Buch S. 27)</h3>
<p>Ein Stängel der Wasserpest wird frisch angeschnitten, an einen Glasstab gebunden und mit der Schnittstelle nach oben in ein hohes Glas mit Wasser gestellt. Die Pflanze muss ganz unter Wasser sein. Dann wird sie mit einer starken Lampe beleuchtet. Gezählt werden die Sauerstoff-Bläschen, die pro Minute aufsteigen. <b>Je mehr Bläschen, desto höher ist die Fotosynthese-Leistung.</b></p></div>
<div class="box"><h3>Einen Versuch auswerten (Buch S. 27, Abb. 6)</h3>
<p>Die Bläschenzählmethode wurde bei verschiedenen Beleuchtungsstärken durchgeführt:</p>
<div class="tbl"><table>
<tr><th>Beleuchtungsstärke (Lux)</th><td>200</td><td>1000</td><td>4000</td><td>8000</td><td>16000</td><td>24000</td><td>32000</td></tr>
<tr><th>Bläschen pro Minute</th><td>0</td><td>1</td><td>4</td><td>8</td><td>12</td><td>13</td><td>13</td></tr>
</table></div>
{blaeschen_chart()}
<p><b>Beschreiben:</b> Bis 8000 Lux steigt die Zahl der Bläschen gleichmäßig an. Danach steigt sie langsamer. Ab 24000 Lux bleibt sie gleich bei 13 Bläschen pro Minute.</p>
<p><b>Erklären:</b> Je mehr Licht, desto mehr Fotosynthese, desto mehr Sauerstoff. Ab einer bestimmten Lichtstärke hilft mehr Licht nicht mehr. Dann begrenzt etwas anderes die Fotosynthese, zum Beispiel zu wenig Kohlenstoffdioxid oder die Temperatur.</p>
<p class="meta">So beschreibst du ein Diagramm: Erst sagen, was passiert (beschreiben). Dann sagen, warum (erklären).</p></div>
<div class="box"><h3>Typische Fehler beim Planen</h3>
<ul><li>Zwei Bedingungen auf einmal verändert, zum Beispiel Dünger <b>und</b> Licht. Dann weiß man nicht, was die Ursache ist.</li>
<li>Kein Kontrollversuch. Dann fehlt der Vergleich.</li>
<li>Pflanzen sind am Anfang unterschiedlich groß oder bekommen unterschiedlich viel Wasser.</li>
<li>Nur eine einzige Pflanze. Ein Zufall kann das Ergebnis verfälschen.</li>
<li>Nicht festgelegt, was gemessen wird.</li></ul></div>
""",

"t4": A.LESEN["t4"] + """
<div class="box"><h3>Was im Blatt bei der Fotosynthese passiert (Buch S. 26–27)</h3>
<div class="eq">Wasser + Kohlenstoffdioxid → Glucose + Sauerstoff<br><span class="meta">mit Licht und Chlorophyll</span></div>
<ul><li><b>Kohlenstoffdioxid</b> gelangt über die <b>Spaltöffnungen</b> ins Blatt und durch die <b>Interzellularen</b> zu den Blattzellen.</li>
<li><b>Wasser</b> gelangt über die <b>Leitbündel</b> in die Blätter.</li>
<li>Das <b>Chlorophyll</b> in den Chloroplasten nimmt die Energie des Sonnenlichts auf. Lichtenergie wird in chemische Energie umgewandelt.</li>
<li>Im <b>Palisadengewebe</b> ist die Fotosynthese besonders stark, weil diese Zellen besonders viel Chlorophyll enthalten.</li>
<li>Der <b>Sauerstoff</b> wird über die Spaltöffnungen abgegeben.</li>
<li>Die <b>Glucose</b> (Traubenzucker, ein energiereicher Stoff) wird über die Leitbündel in der ganzen Pflanze verteilt. Oft wird sie schnell in Stärke umgewandelt und gespeichert.</li></ul></div>
<div class="box"><h3>Angepasstheiten: Der Bau passt zur Aufgabe</h3>
<div class="tbl"><table>
<tr><th>Bau</th><th>Warum das nützt</th></tr>
<tr><td>Obere Epidermis ohne Chloroplasten</td><td>Sie ist durchsichtig. Das Licht kommt gut zum Palisadengewebe.</td></tr>
<tr><td>Palisadengewebe direkt unter der Oberseite, besonders viele Chloroplasten</td><td>Dort, wo das meiste Licht ankommt, findet die Fotosynthese besonders stark statt.</td></tr>
<tr><td>Kutikula aus Wachs</td><td>schützt vor zu viel Wasserverlust durch Verdunstung</td></tr>
<tr><td>Spaltöffnungen, die sich öffnen und schließen</td><td>kontrollierter Gasaustausch: Kohlenstoffdioxid hinein, Sauerstoff hinaus</td></tr>
<tr><td>Interzellularen im Schwammgewebe</td><td>Kohlenstoffdioxid kann sich im Blatt bis zu den Zellen verteilen.</td></tr>
<tr><td>Leitbündel</td><td>bringen Wasser ins Blatt und verteilen die Glucose in der Pflanze</td></tr>
</table></div>
<p><b>Angepasstheiten an das Licht</b> (Buch S. 26): Eine Topfpflanze auf der Fensterbank richtet ihre Blätter zum Fenster aus. Bäume überragen mit ihrem hohen Stamm viele andere Pflanzen. Ihre Blätter wachsen so, dass sie sich möglichst wenig gegenseitig verdecken. So bekommt jedes Blatt möglichst viel Licht.</p>
<p><b>Das Blatt als Organ:</b> Blatt (Organ) → Palisadengewebe (Gewebe) → Palisadenzelle (Zelle) → Chloroplast (Zellorganell).</p></div>
""",

"tzell": f"""
<div class="box merke"><h3>Das musst du wissen</h3>
<div class="tbl"><table>
<tr><th>Bestandteil</th><th>Pflanzenzelle</th><th>Tierzelle</th></tr>
<tr><td>Zellmembran</td><td>✓</td><td>✓</td></tr>
<tr><td>Cytoplasma (Zellplasma)</td><td>✓</td><td>✓</td></tr>
<tr><td>Zellkern</td><td>✓</td><td>✓</td></tr>
<tr><td>Mitochondrien</td><td>✓</td><td>✓</td></tr>
<tr><td><b>Zellwand</b></td><td>✓</td><td>–</td></tr>
<tr><td><b>Vakuole</b></td><td>✓</td><td>–</td></tr>
<tr><td><b>Chloroplasten</b></td><td>✓ (in grünen Pflanzenzellen)</td><td>–</td></tr>
</table></div>
<p><b>Nur Pflanzenzellen haben Zellwand, Vakuole und Chloroplasten.</b></p></div>
<div class="box"><h3>Die Pflanzenzelle (Buch S. 14, Abb. 1)</h3>
{pflanzenzelle()}
<div class="tbl"><table>
<tr><th>Teil</th><th>Bau und Aufgabe</th></tr>
<tr><td><b>Zellwand</b></td><td>Gibt der Zelle Stabilität. Innen liegt ihr die Zellmembran an. Über Zellwand und Zellmembran gelangen Stoffe aus der Zelle hinaus und von außen hinein.</td></tr>
<tr><td><b>Zellkern</b></td><td>Ist von einer Membran umgeben und enthält die Erbinformationen der Zelle. Er steuert die Lebensvorgänge der Zelle.</td></tr>
<tr><td><b>Zellmembran</b></td><td>Umgibt die Zelle. Durch sie werden Stoffe aufgenommen und abgegeben.</td></tr>
<tr><td><b>Cytoplasma</b></td><td>Füllt das Innere der Zelle. Stoffe von außen gelangen über das Cytoplasma zu ihrem Bestimmungsort. Cytoplasmastränge ziehen durch die Zellwand und verbinden die Zelle mit den Nachbarzellen.</td></tr>
<tr><td><b>Chloroplasten</b></td><td>Ein Merkmal grüner Pflanzenzellen. Sie sind von einer Doppelmembran umgeben und enthalten den grünen Blattfarbstoff Chlorophyll. Sie sind der Ort der Fotosynthese.</td></tr>
<tr><td><b>Mitochondrien</b></td><td>Der Ort der Zellatmung. Im Lichtmikroskop sind sie nicht sichtbar (Buch S. 34 und 36).</td></tr>
<tr><td><b>Vakuole</b></td><td>Gibt es nur in Pflanzenzellen. Sie ist von einer eigenen Membran umgeben (Vakuolenmembran) und enthält größtenteils Wasser, manchmal auch Farbstoffe. Sie kann Wasser aufnehmen und abgeben und stabilisiert gemeinsam mit der Zellwand die Zelle.</td></tr>
</table></div></div>
<div class="box"><h3>Die Tierzelle (Buch S. 14, Abb. 3)</h3>
{tierzelle()}
<p>Im Buch sind bei den Tierzellen <b>Zellmembran, Cytoplasma und Zellkern</b> beschriftet. Mitochondrien haben Tierzellen auch, aber man sieht sie im Lichtmikroskop nicht. Tierzellen haben keine Zellwand. Deshalb ist ihre Form unregelmäßiger als bei Pflanzenzellen.</p></div>
<div class="box"><h3>Organellen und Kompartimentierung</h3>
<p>Im Cytoplasma liegen verschiedene <b>Zellorganellen</b>, zum Beispiel Zellkern, Chloroplasten und Mitochondrien. Organellen sind <b>abgetrennte Reaktionsräume</b>. Darin können verschiedene Stoffwechselvorgänge gleichzeitig nebeneinander ablaufen, ohne sich zu stören. Diese räumliche Trennung nennt man <b>Kompartimentierung</b>.</p></div>
<div class="box"><h3>Das haben alle Zellen gemeinsam (Buch S. 14)</h3>
<ul><li>Zellen entstehen durch Teilung aus anderen Zellen.</li>
<li>Im Zellkern befindet sich die Erbinformation.</li>
<li>Zellen brauchen Energie.</li>
<li>Zellen sind von einer Membran umgeben. Durch sie werden Stoffe aufgenommen und abgegeben, über die ganze Zelloberfläche.</li>
<li>Zellen wandeln Stoffe um. Sie verwerten Nährstoffe, um eigene Stoffe aufzubauen und Energie bereitzustellen.</li></ul></div>
""",

"tatm": """
<div class="box merke"><h3>Das musst du wissen</h3>
<div class="eq">Glucose + Sauerstoff → Kohlenstoffdioxid + Wasser + Energie</div>
<ul><li><b>Ort:</b> in den <b>Mitochondrien</b> der Zellen (im Lichtmikroskop nicht sichtbar)</li>
<li><b>Wozu:</b> Die chemische Energie der Glucose wird für die Zellen nutzbar gemacht. Ein Teil wird zu Wärme.</li>
<li><b>Wer:</b> Menschen, Tiere, Pflanzen, Pilze und viele andere Lebewesen</li></ul></div>
<div class="box"><h3>Der Weg der Stoffe beim Menschen (Buch S. 34)</h3>
<ol><li><b>Stoffaufnahme:</b> Beim Atmen gelangt Sauerstoff über die <b>Lunge</b> ins Blut. Durch die Verdauung im <b>Darm</b> gelangen Glucose und andere Nährstoffe ins Blut.</li>
<li><b>Stofftransport:</b> Das <b>Blut</b> bringt Sauerstoff und Glucose in alle Teile des Körpers.</li>
<li><b>Stoffumwandlung:</b> In den Mitochondrien der Zellen wird die energiereiche Glucose unter Beteiligung von Sauerstoff Schritt für Schritt zu energiearmem Kohlenstoffdioxid und Wasser abgebaut. Dabei wird Energie für die Zelle nutzbar.</li>
<li><b>Stoffabgabe:</b> Das Kohlenstoffdioxid wird mit dem Blut zur Lunge gebracht und ausgeatmet.</li></ol></div>
<div class="box"><h3>Wofür die Energie gebraucht wird</h3>
<p>Energie aus der Zellatmung ist die Grundlage aller Lebensvorgänge. <b>Muskeln</b> brauchen sie, um sich zusammenzuziehen. Das <b>Gehirn</b> braucht sie für die Informationsverarbeitung. Auch alle anderen Organe sind darauf angewiesen.</p>
<p><b>Bei Anstrengung</b> brauchen die Muskelzellen mehr Energie. Dann läuft mehr Zellatmung ab, und die Muskeln brauchen mehr Sauerstoff und Glucose. Deshalb atmet man schneller.</p>
<p><b>Sauerstoffmangel im Gehirn</b> (Buch S. 35): Schon wenige Sekunden ohne Sauerstoff führen zu Störungen und zur Bewusstlosigkeit. Davon kann sich das Gehirn völlig erholen, wenn sofort wieder Sauerstoff kommt. Nach drei Minuten können Schäden entstehen, die nicht mehr rückgängig zu machen sind.</p></div>
<div class="box"><h3>Zellatmung und Kerzenflamme (Buch S. 35)</h3>
<div class="tbl"><table>
<tr><th></th><th>Zellatmung</th><th>Kerzenflamme</th></tr>
<tr><td>energiereicher Ausgangsstoff</td><td>Glucose</td><td>Kerzenwachs (enthält viel Kohlenstoff)</td></tr>
<tr><td>braucht Sauerstoff</td><td>ja</td><td>ja</td></tr>
<tr><td>es entstehen</td><td>Kohlenstoffdioxid und Wasser</td><td>unter anderem Kohlenstoffdioxid und Wasser, dazu Hunderte andere Verbrennungsprodukte</td></tr>
<tr><td>Ablauf</td><td>schnell, aber in vielen kleinen, geordneten Schritten in den Mitochondrien</td><td>in der Flamme, bei etwa 1400 °C</td></tr>
<tr><td>Energie</td><td>wird für die Zelle nutzbar, ein Teil wird zu Wärme</td><td>wird vor allem zu Wärme und Licht</td></tr>
</table></div></div>
<div class="box"><h3>Fotosynthese und Zellatmung (Buch S. 36)</h3>
<div class="eq">Fotosynthese: Wasser + Kohlenstoffdioxid → Glucose + Sauerstoff<br><span class="meta">mit Licht und Chlorophyll, in den Chloroplasten</span></div>
<div class="eq">Zellatmung: Glucose + Sauerstoff → Kohlenstoffdioxid + Wasser + Energie<br><span class="meta">in den Mitochondrien</span></div>
<div class="tbl"><table>
<tr><th></th><th>Fotosynthese</th><th>Zellatmung</th></tr>
<tr><td>Ort</td><td>Chloroplasten</td><td>Mitochondrien</td></tr>
<tr><td>wer</td><td>grüne Pflanzen</td><td>Menschen, Tiere, Pflanzen, Pilze und viele andere</td></tr>
<tr><td>wann</td><td>nur im Licht</td><td>immer, Tag und Nacht</td></tr>
<tr><td>Sauerstoff</td><td>wird frei</td><td>wird gebraucht</td></tr>
<tr><td>Glucose</td><td>wird hergestellt</td><td>wird abgebaut</td></tr>
<tr><td>Energie</td><td>Lichtenergie wird in chemische Energie der Glucose umgewandelt</td><td>chemische Energie der Glucose wird für die Zelle nutzbar</td></tr>
</table></div>
<p><b>Pflanzen machen beides:</b> Grüne Pflanzenzellen haben Chloroplasten <b>und</b> Mitochondrien. Im Licht betreiben sie Fotosynthese und zugleich Zellatmung. Im Tageslicht wird bei den meisten Pflanzen mehr Sauerstoff frei, als sie für die Zellatmung brauchen. Den Rest geben sie ab, und atmende Lebewesen können ihn nutzen. Im Dunkeln läuft nur die Zellatmung.</p>
<p><b>Wechselseitige Beziehung:</b> Den Sauerstoff aus der Fotosynthese brauchen Lebewesen zum Atmen. Das Kohlenstoffdioxid aus der Atmung braucht die Pflanze für die Fotosynthese. Luft enthält 21 % Sauerstoff und 0,04 % Kohlenstoffdioxid.</p></div>
<div class="box"><h3>Versuche aus dem Buch (S. 37)</h3>
<p><b>Efeublätter im Licht:</b> 20 Efeublätter stehen in Wasser unter einer beleuchteten Glasglocke. Ein Sensor misst den Kohlenstoffdioxid-Gehalt der Luft. Er sinkt in 15 Minuten von etwa 630 auf etwa 430 ppm. Die Blätter verbrauchen also bei der Fotosynthese Kohlenstoffdioxid. <b>Hypothese für Dunkelheit:</b> Ohne Licht läuft nur die Zellatmung. Der Kohlenstoffdioxid-Gehalt steigt dann an.</p>
<p><b>Modellgewässer:</b> In luftdicht geschlossenen Gefäßen mit Wasser gilt:</p>
<ul><li>Ohne Lebewesen ändert sich nichts.</li>
<li>Pflanzen im Licht: Sauerstoff steigt, Kohlenstoffdioxid sinkt (Fotosynthese überwiegt).</li>
<li>Pflanzen im Dunkeln und Tiere (hell oder dunkel): Sauerstoff sinkt, Kohlenstoffdioxid steigt (nur Atmung).</li>
<li>Pflanzen und Tiere im Dunkeln: Sauerstoff sinkt am schnellsten, denn alle atmen und keiner macht Fotosynthese.</li>
<li>Pflanzen und Tiere im Licht: Das hängt davon ab, wie viele Pflanzen und Tiere es sind.</li></ul></div>
""",
}
LESEN["t1"] = A.LESEN["t1"]
LESEN["t2"] = A.LESEN["t2"]

# ================================================================ Zuordnen
MATCH = {k: v for k, v in A.MATCH.items() if k != "m-schritte"}
MATCH.update({
 "m-schritte": dict(wide=True, how="Bring die Schritte der Erkenntnisgewinnung in die richtige Reihenfolge (Buch S. 23, Abb. 3).",
   slots=[[f"{i}.", s] for i, s in enumerate(["Beobachtung oder Phänomen", "Formulierung des Phänomens", "Aufstellen der Problemfrage", "Formulierung von Hypothesen",
          "Entwicklung der Lösungsstrategie", "Durchführung der Untersuchungen", "Ergebnis mit Rückbezug auf die Hypothesen", "Erweiterung des Ergebnisses", "Erkenntnisgewinn – Verallgemeinerung"], 1)]),
 "m-priestley": dict(wide=True, how="Was passierte in Priestleys Versuchen? Zieh die Beobachtung zum Versuch.",
   slots=[["a: nur eine brennende Kerze", "Die Kerze erlosch nach einiger Zeit."],
          ["b: Kerze und Maus", "Die Kerze erlosch viel schneller, die Maus wurde nach kurzer Zeit ohnmächtig."],
          ["c: nur eine Maus", "Die Maus wurde ohnmächtig, aber später als bei b."],
          ["d: Maus und Pflanze", "Die Maus wurde nicht ohnmächtig."]]),
 "m-spirale": dict(wide=True, how="Wer hat was herausgefunden? Zieh den Namen zur Erkenntnis.",
   slots=[["Ein Weidenbaum wird in 5 Jahren 74,4 kg schwerer, die Erde nur 57 g leichter.", "van Helmont"],
          ["Tiere überleben in abgeschlossenen Räumen viel länger, wenn Pflanzen dabei sind.", "Priestley"],
          ["Ein neues Element ermöglicht die Verbrennung und wird zum Atmen gebraucht: Sauerstoff.", "Lavoisier"],
          ["Pflanzen stellen nur im Licht und nur mit grünen Teilen Sauerstoff her.", "Ingenhousz"],
          ["Pflanzen stellen nur dann Sauerstoff her, wenn auch Kohlenstoffdioxid da ist.", "Senebier"]]),
 "m-protokoll": dict(wide=True, how="Bring die Teile eines Versuchsprotokolls in die richtige Reihenfolge.",
   slots=[["1.", "Frage"], ["2.", "Hypothese"], ["3.", "Material"], ["4.", "Durchführung (mit Skizze)"], ["5.", "Beobachtung (Messwerte)"], ["6.", "Deutung (Auswertung)"]]),
 "m-angepasst": dict(wide=True, how="Warum ist das Blatt so gebaut? Zieh den Grund zum Bauteil.",
   slots=[["Obere Epidermis ohne Chloroplasten", "Licht kommt gut zum Palisadengewebe."],
          ["Palisadengewebe mit sehr vielen Chloroplasten direkt unter der Oberseite", "Dort ist die Fotosynthese besonders stark."],
          ["Kutikula aus Wachs", "Schutz vor zu viel Wasserverlust"],
          ["Spaltöffnungen", "Kohlenstoffdioxid hinein, Sauerstoff hinaus"],
          ["Interzellularen im Schwammgewebe", "Kohlenstoffdioxid verteilt sich bis zu den Zellen."],
          ["Leitbündel", "Wasser ins Blatt, Glucose in die Pflanze"]]),
 "m-pfl": dict(fig=pflanzenzelle(), how="Beschrifte die Pflanzenzelle: Zieh jedes Wort auf die passende Nummer.",
   slots=[[str(i), n] for i, n in enumerate(PFL_TEILE, 1)]),
 "m-tier": dict(fig=tierzelle(), how="Beschrifte die Tierzelle.",
   slots=[[str(i), n] for i, n in enumerate(TIER_TEILE, 1)]),
 "m-zellteile": dict(wide=True, how="Welcher Zellbestandteil ist das?",
   slots=[["Gibt der Zelle Stabilität. Innen liegt ihr die Zellmembran an.", "Zellwand"],
          ["Enthält die Erbinformationen und steuert die Lebensvorgänge der Zelle.", "Zellkern"],
          ["Enthält größtenteils Wasser, kann Wasser aufnehmen und abgeben.", "Vakuole"],
          ["Enthält Chlorophyll. Ort der Fotosynthese.", "Chloroplast"],
          ["Ort der Zellatmung. Im Lichtmikroskop nicht sichtbar.", "Mitochondrium"],
          ["Füllt das Innere der Zelle. Stoffe gelangen darüber zu ihrem Bestimmungsort.", "Cytoplasma"]]),
 "m-weg": dict(wide=True, how="Der Weg der Stoffe bei der Zellatmung des Menschen (Buch S. 34): Zieh den Begriff zur Beschreibung.",
   slots=[["Sauerstoff gelangt über die Lunge ins Blut, Glucose über den Darm.", "Stoffaufnahme"],
          ["Das Blut bringt Sauerstoff und Glucose zu allen Zellen.", "Stofftransport"],
          ["In den Mitochondrien wird Glucose mit Sauerstoff zu Kohlenstoffdioxid und Wasser abgebaut.", "Stoffumwandlung"],
          ["Kohlenstoffdioxid wird mit dem Blut zur Lunge gebracht und ausgeatmet.", "Stoffabgabe"]]),
 "m-gleichung": dict(wide=True, how="Bau die Wortgleichung der Zellatmung zusammen.",
   slots=[["Ausgangsstoff 1 (energiereich)", "Glucose"], ["Ausgangsstoff 2", "Sauerstoff"], ["Produkt 1 (ein Gas, wird ausgeatmet)", "Kohlenstoffdioxid"], ["Produkt 2 (eine Flüssigkeit)", "Wasser"], ["wird für die Zelle nutzbar", "Energie"]]),
})
for k, m in MATCH.items():
    m["id"] = k
    assert len({s[1] for s in m["slots"]}) == len(m["slots"]), k

# ================================================================ Sortieren
SORT = {
 "s-variablen": dict(bins=["wird verändert", "wird gemessen", "bleibt gleich"],
   how="Versuch aus dem Buch (S. 27): Hängt die Fotosynthese von der Menge an Kohlenstoffdioxid ab? Sortiere die Kärtchen.",
   items=[["Menge an Kohlenstoffdioxid im Wasser", 0], ["Zahl der Sauerstoff-Bläschen pro Minute", 1],
          ["dieselbe Wasserpest-Pflanze", 2], ["Wassertemperatur 20 °C", 2], ["gleiche Lampe im gleichen Abstand", 2], ["gleich viel Wasser im Glas", 2], ["jeweils eine Minute lang zählen", 2]],
   why="Genau so muss es sein: Nur eine Bedingung wird verändert, alles andere bleibt gleich."),
 "s-duenger": dict(bins=["wird verändert", "wird gemessen", "bleibt gleich"],
   how="Ein eigenes Experiment: Wachsen Bohnenpflanzen mit Dünger besser? Sortiere die Kärtchen.",
   items=[["Dünger oder kein Dünger", 0], ["Länge der Pflanzen in cm nach zwei Wochen", 1],
          ["gleich lange Pflanzen am Anfang", 2], ["gleich viel Wasser", 2], ["gleiche Erde und gleiche Töpfe", 2], ["gleicher Platz am Fenster", 2], ["gleiche Bohnensorte", 2]],
   why="Und der Kontrollversuch? Das sind die Pflanzen ohne Dünger, die sonst genau gleich behandelt werden."),
 "s-zellen": dict(bins=["nur Pflanzenzelle", "Pflanzen- und Tierzelle"],
   how="Was hat nur die Pflanzenzelle, was haben beide?",
   items=[["Zellwand", 0], ["Vakuole", 0], ["Chloroplasten", 0], ["Zellmembran", 1], ["Zellkern", 1], ["Cytoplasma", 1], ["Mitochondrien", 1]],
   why="Merke: Zellwand, Vakuole und Chloroplasten gibt es nur in Pflanzenzellen."),
 "s-fs-za": dict(bins=["Fotosynthese", "Zellatmung"],
   how="Gehört das zur Fotosynthese oder zur Zellatmung?",
   items=[["findet in den Chloroplasten statt", 0], ["findet in den Mitochondrien statt", 1], ["nur im Licht", 0], ["Tag und Nacht", 1],
          ["Sauerstoff wird frei", 0], ["Sauerstoff wird gebraucht", 1], ["Glucose wird hergestellt", 0], ["Glucose wird abgebaut", 1],
          ["Kohlenstoffdioxid wird gebraucht", 0], ["Kohlenstoffdioxid entsteht", 1], ["Lichtenergie wird in chemische Energie umgewandelt", 0], ["auch bei Menschen, Tieren und Pilzen", 1]],
   why="Merke: Die Zellatmung ist fast die Umkehrung der Fotosynthese."),
 "s-gewaesser": dict(bins=["Sauerstoff steigt", "Sauerstoff sinkt", "keine Änderung"],
   how="Modellgewässer (Buch S. 37): Luftdicht geschlossene Gefäße mit Wasser. Wie ändert sich der Sauerstoff-Gehalt?",
   items=[["1: ohne Lebewesen, Licht", 2], ["2: ohne Lebewesen, dunkel", 2], ["3: Pflanzen, Licht", 0], ["4: Pflanzen, dunkel", 1],
          ["5: Tiere, Licht", 1], ["6: Tiere, dunkel", 1], ["8: Pflanzen und Tiere, dunkel", 1]],
   why="Im Dunkeln machen Pflanzen keine Fotosynthese, sondern nur Zellatmung. Gefäß 7 (Pflanzen und Tiere im Licht) fehlt hier: Es hängt davon ab, wie viele Pflanzen und Tiere darin sind."),
}
for k, m in SORT.items():
    m["id"] = k

# ================================================================ Karten
CARDS = {
"t3": [c for c in A.CARDS["t3"] if c[0] not in ("Die Schritte der Reihe nach", "Erkenntnisgewinn")] + [
 ["Priestley 1771: Was hat er herausgefunden?", "Tiere überleben in luftdicht abgeschlossenen Räumen sehr viel länger, wenn Pflanzen anwesend sind."],
 ["Priestley: Versuch d (Maus und Pflanze)", "Die Maus wurde nicht ohnmächtig."],
 ["Priestley: Warum erlosch die Kerze in Versuch b so schnell?", "Kerze und Maus verbrauchen beide Sauerstoff. Zusammen ist er schneller verbraucht."],
 ["Priestley: Was fiel ihm außerdem auf?", "Die Versuche liefen abends und nachts anders ab als am Tag."],
 ["Was wusste Priestley mehr als van Helmont?", "Pflanzen verändern die Luft. Mit Pflanzen können Tiere in abgeschlossener Luft viel länger überleben."],
 ["Welche neuen Fragen ergaben sich nach Priestley?", "Welcher Stoff der Luft ist es? Warum ist es nachts anders, braucht die Pflanze Licht? Was braucht die Pflanze sonst noch dafür?"],
 ["Lavoisier (1775)", "Ein neues Element ermöglicht die Verbrennung und wird zum Atmen gebraucht. Später heißt es Sauerstoff."],
 ["Ingenhousz (1779)", "Pflanzen stellen nur im Licht Sauerstoff her, im Dunkeln geben sie Kohlenstoffdioxid ab. Nur grüne Pflanzenteile stellen Sauerstoff her."],
 ["Senebier (1783)", "Pflanzen stellen im Licht nur dann Sauerstoff her, wenn auch Kohlenstoffdioxid da ist."],
 ["Wortgleichung der Fotosynthese", "Wasser + Kohlenstoffdioxid → Glucose + Sauerstoff (mit Licht und Chlorophyll)"],
 ["Die Schritte der Erkenntnisgewinnung (Buch S. 23)", "1 Beobachtung · 2 Formulierung des Phänomens · 3 Problemfrage · 4 Hypothesen · 5 Lösungsstrategie · 6 Durchführung der Untersuchungen · 7 Ergebnis mit Rückbezug auf die Hypothesen · 8 Erweiterung des Ergebnisses · 9 Erkenntnisgewinn"],
],
"texp": [
 ["Kontrollversuch", "Ein Ansatz, der genauso aufgebaut ist, bei dem die untersuchte Bedingung aber nicht verändert wird. Er dient zum Vergleich."],
 ["Wie viele Bedingungen veränderst du?", "Genau eine. Alles andere bleibt gleich."],
 ["Was muss gleich bleiben?", "Alles außer der untersuchten Bedingung: zum Beispiel gleich lange Pflanzen, gleich viel Wasser, gleiche Temperatur, gleiches Licht, gleiche Dauer."],
 ["Was misst man?", "Eine Größe, die man vorher festlegt, zum Beispiel Bläschen pro Minute oder die Länge in cm."],
 ["Die Teile eines Versuchsprotokolls", "Frage · Hypothese · Material · Durchführung (mit Skizze) · Beobachtung · Deutung"],
 ["Hypothese", "Eine begründete Vermutung, die man vor dem Versuch aufschreibt."],
 ["Deutung", "Man erklärt die Beobachtung und prüft, ob die Hypothese stimmt."],
 ["Bläschenzählmethode", "Die Wasserpest wird beleuchtet. Man zählt die Sauerstoff-Bläschen pro Minute. Je mehr Bläschen, desto höher ist die Fotosynthese-Leistung."],
 ["Warum mehrere Pflanzen nehmen?", "Damit ein Zufall das Ergebnis nicht verfälscht."],
 ["Priestley: Welcher Versuch ist der Kontrollversuch zu d?", "Versuch c (nur die Maus). Alles ist gleich, nur die Pflanze fehlt."],
 ["Bläschen-Versuch mit mehr Licht: Ergebnis", "Mit mehr Licht steigen mehr Bläschen auf. Ab etwa 24000 Lux bleibt es bei 13 Bläschen pro Minute."],
],
"t4": A.CARDS["t4"] + [
 ["Wie kommt Kohlenstoffdioxid zu den Blattzellen?", "Über die Spaltöffnungen ins Blatt und durch die Interzellularen zu den Zellen."],
 ["Wie kommt Wasser in das Blatt?", "Über die Leitbündel."],
 ["Was passiert mit der Glucose?", "Sie wird über die Leitbündel in der ganzen Pflanze verteilt. Oft wird sie in Stärke umgewandelt und gespeichert."],
 ["Wo ist die Fotosynthese besonders stark?", "Im Palisadengewebe, weil diese Zellen besonders viel Chlorophyll enthalten."],
 ["Angepasstheit: obere Epidermis ohne Chloroplasten", "Sie ist durchsichtig. So kommt das Licht gut zum Palisadengewebe."],
 ["Angepasstheiten an das Licht (Buch S. 26)", "Topfpflanzen richten ihre Blätter zum Fenster aus. Bäume überragen mit ihrem hohen Stamm andere Pflanzen. Ihre Blätter verdecken sich möglichst wenig gegenseitig."],
 ["Das Blatt als Organ: von groß nach klein", "Blatt (Organ) → Palisadengewebe (Gewebe) → Palisadenzelle (Zelle) → Chloroplast (Zellorganell)"],
],
"tzell": [
 ["Was hat nur die Pflanzenzelle?", "Zellwand, Vakuole und Chloroplasten."],
 ["Was haben Pflanzen- und Tierzelle beide?", "Zellmembran, Cytoplasma, Zellkern und Mitochondrien."],
 ["Zellwand", "Gibt der Zelle Stabilität. Innen liegt ihr die Zellmembran an."],
 ["Vakuole", "Nur in Pflanzenzellen. Von der Vakuolenmembran umgeben, enthält größtenteils Wasser, manchmal Farbstoffe. Stabilisiert gemeinsam mit der Zellwand die Zelle."],
 ["Chloroplasten", "Merkmal grüner Pflanzenzellen. Doppelmembran, enthalten Chlorophyll. Ort der Fotosynthese."],
 ["Zellkern", "Von einer Membran umgeben, enthält die Erbinformationen, steuert die Lebensvorgänge der Zelle."],
 ["Cytoplasma", "Füllt das Innere der Zelle. Stoffe von außen gelangen darüber zu ihrem Bestimmungsort. Anderes Wort: Zellplasma."],
 ["Zellmembran", "Umgibt die Zelle. Durch sie werden Stoffe aufgenommen und abgegeben."],
 ["Mitochondrien", "Ort der Zellatmung. In Pflanzen- und Tierzellen. Im Lichtmikroskop nicht sichtbar."],
 ["Zellorganellen", "Abgetrennte Reaktionsräume in der Zelle, zum Beispiel Zellkern, Chloroplasten, Mitochondrien."],
 ["Kompartimentierung", "Die Zelle ist in abgetrennte Räume aufgeteilt. So können verschiedene Vorgänge gleichzeitig ablaufen, ohne sich zu stören."],
 ["Euglena (Buch S. 15): Pflanze oder Tier?", "Man kann beides begründen. Für Pflanze spricht: Euglena hat Chloroplasten. Für Tier spricht: Sie hat eine Geißel zum Bewegen und einen Augenfleck, und außen ist nur eine Zellmembran eingezeichnet, keine Zellwand."],
 ["Was haben alle Zellen gemeinsam?", "Sie entstehen durch Teilung, haben die Erbinformation im Zellkern, brauchen Energie, sind von einer Membran umgeben und wandeln Stoffe um."],
],
"tatm": [
 ["Wortgleichung der Zellatmung", "Glucose + Sauerstoff → Kohlenstoffdioxid + Wasser + Energie"],
 ["Wo findet die Zellatmung statt?", "In den Mitochondrien der Zellen."],
 ["Wozu dient die Zellatmung?", "Die chemische Energie der Glucose wird für die Zellen nutzbar gemacht."],
 ["Was wird bei der Zellatmung außerdem frei?", "Wärme. Ein Teil der chemischen Energie der Glucose wird zu Wärmeenergie."],
 ["Wie kommen Sauerstoff und Glucose zu den Zellen?", "Sauerstoff über die Lunge ins Blut, Glucose durch die Verdauung über den Darm ins Blut. Das Blut bringt beides in alle Teile des Körpers."],
 ["Stoffaufnahme, Stofftransport, Stoffumwandlung, Stoffabgabe", "Aufnahme über Lunge und Darm · Transport mit dem Blut · Umwandlung in den Mitochondrien · Abgabe von Kohlenstoffdioxid über die Lunge"],
 ["Wer betreibt Zellatmung?", "Menschen, Tiere, Pflanzen, Pilze und viele andere Lebewesen."],
 ["Mitochondrien", "Zellorganellen mit Doppelmembran. Orte der Zellatmung. Im Lichtmikroskop nicht sichtbar."],
 ["Was passiert bei Anstrengung?", "Die Muskeln brauchen mehr Energie. Es läuft mehr Zellatmung ab, sie brauchen mehr Sauerstoff und Glucose. Man atmet schneller."],
 ["Sauerstoffmangel im Gehirn", "Wenige Sekunden: Störungen und Bewusstlosigkeit, davon kann sich das Gehirn erholen. Nach drei Minuten: Schäden, die nicht mehr rückgängig zu machen sind."],
 ["Zellatmung und Kerze: Gemeinsamkeit", "Beide brauchen Sauerstoff. Bei beiden entstehen Kohlenstoffdioxid und Wasser."],
 ["Zellatmung und Kerze: Unterschied", "Die Zellatmung läuft in vielen kleinen, geordneten Schritten ab, die Energie wird für die Zelle nutzbar. In der Kerzenflamme ist es etwa 1400 °C heiß, die Energie wird vor allem zu Wärme und Licht."],
 ["Fotosynthese und Zellatmung: Wechselbeziehung", "Den Sauerstoff aus der Fotosynthese brauchen Lebewesen zum Atmen. Das Kohlenstoffdioxid aus der Atmung braucht die Pflanze für die Fotosynthese."],
 ["Was macht eine Pflanze im Dunkeln?", "Nur Zellatmung: Sie nimmt Sauerstoff auf und gibt Kohlenstoffdioxid ab."],
],
}
CARDS["t1"] = A.CARDS["t1"]
CARDS["t2"] = A.CARDS["t2"]

# ================================================================ Quiz (erste Antwort ist richtig)
QUIZ = {
"t3": [q for q in A.QUIZ["t3"] if q[0] not in ("Welche Reihenfolge stimmt?", "Was kann ein Erkenntnisgewinn sein?")] + [
 ["Was entdeckte Priestley 1771?", ["Tiere überleben in abgeschlossenen Räumen viel länger, wenn Pflanzen anwesend sind.", "Pflanzen bekommen ihre Masse aus der Erde.", "Die Chloroplasten sind der Ort der Fotosynthese.", "Pflanzen brauchen Chlorophyll."], "Er stellte Kerze, Maus und Pflanze unter luftdichte Glasglocken."],
 ["Priestley, Versuch b: Warum erlosch die Kerze viel schneller als bei a?", ["Kerze und Maus haben beide Sauerstoff verbraucht.", "Die Maus hat die Kerze ausgepustet.", "Die Glasglocke war kleiner.", "Die Maus hat Sauerstoff hergestellt."], "Zwei Verbraucher: Der Sauerstoff ist schneller aufgebraucht."],
 ["Priestley, Versuch d: Maus und Pflanze unter der Glocke. Was passierte?", ["Die Maus wurde nicht ohnmächtig.", "Die Maus wurde sofort ohnmächtig.", "Die Pflanze ging ein.", "Die Maus wurde nach kurzer Zeit ohnmächtig, wie bei b."], "Die Pflanze stellt im Licht Sauerstoff her."],
 ["Welcher von Priestleys Versuchen ist der Kontrollversuch zu d (Maus und Pflanze)?", ["c: nur die Maus", "a: nur die Kerze", "b: Kerze und Maus", "Es gibt keinen."], "Bei c ist alles gleich wie bei d, nur die Pflanze fehlt."],
 ["Was beobachtete Priestley außerdem?", ["Abends und nachts liefen die Versuche anders ab als am Tag.", "Die Maus wuchs unter der Glocke.", "Die Kerze brannte nachts heller.", "Die Erde wurde leichter."], "Heute weiß man: Ohne Licht macht die Pflanze keine Fotosynthese."],
 ["Was wusste man nach Priestley mehr als nach van Helmont?", ["Pflanzen verändern die Luft, sodass Tiere darin länger überleben.", "Pflanzen bestehen vollständig aus Wasser und brauchen keine Luft.", "Pflanzen nehmen fast ihre ganze Masse aus dem Boden auf.", "Pflanzen brauchen kein Licht, um die Luft zu verändern."], "Van Helmont dachte nur an Erde und Wasser. Priestley zeigte, dass die Luft eine Rolle spielt."],
 ["Welche neue Frage ergab sich aus Priestleys Beobachtung in der Nacht?", ["Braucht die Pflanze Licht, um die Luft zu verbessern?", "Wie schwer ist eine Maus?", "Wie viel Erde braucht eine Weide?", "Warum sind Kerzen weiß?"], "Ingenhousz zeigte 1779: Pflanzen stellen nur im Licht Sauerstoff her."],
 ["Wer berichtete 1775 über ein neues Element, das später Sauerstoff genannt wurde?", ["Lavoisier", "Hales", "van Helmont", "Senebier"], "Lavoisier berichtete 1775 darüber. Zuerst hieß es „l’air vital“."],
 ["Was zeigte Ingenhousz 1779?", ["Pflanzen stellen nur im Licht Sauerstoff her, im Dunkeln geben sie Kohlenstoffdioxid ab.", "Pflanzen stellen auch im Dunkeln Sauerstoff her, im Licht sogar noch mehr.", "Pflanzen nehmen alle Stoffe für ihr Wachstum aus der Erde im Topf auf.", "Lichtenergie wird bei der Fotosynthese in chemische Energie umgewandelt."], "Außerdem: Nur die grünen Pflanzenteile stellen Sauerstoff her."],
 ["Was zeigte Senebier 1783?", ["Pflanzen stellen im Licht nur dann Sauerstoff her, wenn auch Kohlenstoffdioxid da ist.", "Pflanzen stellen nur dann Sauerstoff her, wenn sie auch genug Wasser bekommen.", "Tiere überleben nur dann länger unter der Glocke, wenn eine Pflanze dabei ist.", "Zucker und Stärke werden in den grünen Chloroplasten der Pflanzen gebildet."], "Kohlenstoffdioxid ist das Gas, das Tiere bei der Atmung freisetzen."],
 ["Wie lautet die Wortgleichung der Fotosynthese?", ["Wasser + Kohlenstoffdioxid → Glucose + Sauerstoff", "Glucose + Sauerstoff → Wasser + Kohlenstoffdioxid", "Wasser + Sauerstoff → Glucose + Kohlenstoffdioxid", "Glucose + Wasser → Sauerstoff + Kohlenstoffdioxid"], "Dafür braucht die Pflanze Licht und Chlorophyll."],
 ["Was ist der 3. Schritt der Erkenntnisgewinnung (Buch S. 23)?", ["Aufstellen der Problemfrage", "Formulierung von Hypothesen", "Durchführung der Untersuchungen", "Erkenntnisgewinn"], "1 Beobachtung, 2 Formulierung des Phänomens, 3 Problemfrage, 4 Hypothesen …"],
],
"texp": [
 ["Was ist ein Kontrollversuch?", ["Ein gleich aufgebauter Ansatz, bei dem die untersuchte Bedingung nicht verändert wird", "Ein Ansatz, bei dem man alle Bedingungen gleichzeitig verändert", "Ein Versuch, bei dem die Lehrerin die Ergebnisse kontrolliert", "Ein zweiter Versuch mit einer ganz anderen Frage"], "Erst der Vergleich mit dem Kontrollversuch zeigt, ob die Bedingung die Ursache ist."],
 ["Wie viele Bedingungen darfst du in einem Versuch verändern?", ["genau eine", "zwei", "so viele wie möglich", "keine"], "Sonst weißt du nicht, welche Bedingung das Ergebnis verursacht hat."],
 ["Lea will testen, ob Dünger Bohnen besser wachsen lässt. Pflanze A bekommt Dünger und steht am Fenster. Pflanze B bekommt keinen Dünger und steht im dunklen Keller. Was ist der größte Fehler?", ["Sie verändert zwei Bedingungen: Dünger und Licht.", "Pflanze B hätte auch Dünger bekommen müssen.", "Sie hätte die Pflanzen nicht gießen dürfen.", "Nichts, das ist richtig."], "Wächst A besser, weiß man nicht, ob es am Dünger oder am Licht liegt."],
 ["Tom vergleicht eine 5 cm lange und eine 12 cm lange Pflanze. Was sollte er besser machen?", ["Gleich lange Pflanzen nehmen", "Nur eine Pflanze nehmen", "Die Pflanzen nicht gießen", "Die Länge nicht messen"], "Alles außer der untersuchten Bedingung muss gleich sein, auch die Startgröße."],
 ["Warum nimmt man für jeden Ansatz am besten mehrere Pflanzen?", ["Damit ein Zufall das Ergebnis nicht verfälscht", "Damit es schneller geht", "Weil Pflanzen allein nicht wachsen", "Damit man weniger messen muss"], "Eine einzelne Pflanze kann zufällig krank oder besonders kräftig sein."],
 ["Bläschenzählmethode: Was wird gemessen?", ["die Zahl der Sauerstoff-Bläschen pro Minute", "die Länge der Wasserpest", "die Wassertemperatur", "die Farbe der Blätter"], "Je mehr Bläschen, desto höher ist die Fotosynthese-Leistung."],
 ["Bläschen-Versuch (Buch S. 27): Warum gibt man sprudelndes Mineralwasser ins Wasser?", ["Es enthält Kohlenstoffdioxid.", "Es enthält Sauerstoff.", "Es ist wärmer.", "Es färbt das Wasser."], "So kann man testen, ob mehr Kohlenstoffdioxid die Fotosynthese steigert."],
 ["Versuch mit Leitungswasser und mit Mineralwasser: Welcher Ansatz ist der Kontrollversuch?", ["der mit reinem Leitungswasser", "der mit Mineralwasser", "beide", "keiner"], "Beim Leitungswasser wird die Kohlenstoffdioxid-Menge nicht verändert."],
 ["Buch S. 27, Versuch b: Das Wasser hat 15 °C, 30 °C und 45 °C. Was wird hier verändert?", ["die Temperatur", "die Lichtstärke", "die Pflanze", "die Menge an Mineralwasser"], "Alles andere bleibt gleich, nur die Temperatur ändert sich."],
 ["Tabelle S. 27: Wie viele Bläschen pro Minute zählt man bei 8000 Lux?", ["8", "4", "12", "13"], "200 Lux: 0 · 1000: 1 · 4000: 4 · 8000: 8 · 16000: 12 · 24000: 13 · 32000: 13"],
 ["Tabelle S. 27: Was passiert zwischen 24000 und 32000 Lux?", ["Die Zahl der Bläschen bleibt gleich (13).", "Die Zahl der Bläschen verdoppelt sich.", "Es steigen keine Bläschen mehr auf.", "Die Zahl der Bläschen sinkt."], "Mehr Licht hilft dann nicht mehr. Etwas anderes begrenzt die Fotosynthese."],
 ["Welche Deutung passt zur Tabelle auf S. 27?", ["Je mehr Licht, desto mehr Fotosynthese, aber nur bis zu einer Grenze.", "Licht hat keinen Einfluss auf die Fotosynthese.", "Je mehr Licht, desto weniger Fotosynthese.", "Die Fotosynthese steigt immer weiter, egal wie hell."], "Bis 8000 Lux steigt die Zahl gleichmäßig, ab 24000 Lux bleibt sie gleich."],
 ["Was schreibst du in die Deutung eines Protokolls?", ["Was die Beobachtung bedeutet und ob die Hypothese stimmt", "Die Liste der Materialien", "Die Frage", "Nur die Messwerte"], "Messwerte gehören zur Beobachtung, die Erklärung zur Deutung."],
 ["Was ist eine Hypothese im Protokoll?", ["eine begründete Vermutung vor dem Versuch", "das Ergebnis nach dem Versuch", "eine Zeichnung des Versuchsaufbaus", "die Liste der Materialien"], "Nach dem Versuch prüfst du in der Deutung, ob sie stimmt."],
],
"t4": A.QUIZ["t4"] + [
 ["Wie gelangt Kohlenstoffdioxid zu den Blattzellen?", ["über die Spaltöffnungen und durch die Interzellularen", "über die Leitbündel aus der Wurzel", "durch die Kutikula", "gar nicht, die Zellen stellen es selbst her"], "So steht es im Buch auf S. 26."],
 ["Wie gelangt das Wasser für die Fotosynthese in das Blatt?", ["über die Leitbündel", "über die Spaltöffnungen", "durch die Kutikula", "durch die Interzellularen"], "Die Leitbündel bilden die Blattadern."],
 ["Wo im Blatt ist die Fotosynthese besonders stark?", ["im Palisadengewebe", "in der Kutikula", "in der oberen Epidermis", "in den Leitbündeln"], "Die Zellen des Palisadengewebes enthalten besonders viel Chlorophyll."],
 ["Wohin geht der Sauerstoff aus der Fotosynthese?", ["Er wird über die Spaltöffnungen abgegeben.", "Er wird in den Leitbündeln zur Wurzel gebracht.", "Er bleibt in der Vakuole.", "Er wird in Stärke umgewandelt."], "So steht es im Buch auf S. 26."],
 ["Was passiert oft mit der gebildeten Glucose?", ["Sie wird in Stärke umgewandelt und gespeichert.", "Sie wird über die Spaltöffnungen abgegeben.", "Sie wird über die Kutikula ausgeschieden.", "Sie bleibt in der Kutikula."], "Glucose wird über die Leitbündel verteilt und oft schnell in wasserunlösliche Stärke umgewandelt."],
 ["Welche Angepasstheit sorgt dafür, dass das Licht gut zum Palisadengewebe kommt?", ["Die obere Epidermis hat keine Chloroplasten und ist durchsichtig.", "Die Kutikula ist aus Wachs.", "Die Spaltöffnungen sind unten.", "Die Leitbündel transportieren Glucose."], "So kommt fast das ganze Licht bis zum Palisadengewebe."],
 ["Warum richtet eine Topfpflanze ihre Blätter zum Fenster aus?", ["um möglichst viel Licht einzufangen", "um weniger Wasser zu verdunsten", "um Tiere abzuwehren", "um wärmer zu werden"], "Pflanzen brauchen Licht für die Fotosynthese."],
],
"tzell": [
 ["Welche Bestandteile hat nur die Pflanzenzelle?", ["Zellwand, Vakuole und Chloroplasten", "Zellkern, Zellmembran und Cytoplasma", "Mitochondrien und Zellkern", "Zellmembran und Vakuole"], "Zellkern, Zellmembran, Cytoplasma und Mitochondrien haben beide."],
 ["Welche Bestandteile sind bei den Tierzellen im Buch (Abb. 3) beschriftet?", ["Zellmembran, Cytoplasma, Zellkern", "Zellwand, Zellkern, Vakuole", "Chloroplasten, Zellkern, Cytoplasma", "Zellwand, Zellmembran, Chloroplasten"], "Tierzellen haben keine Zellwand, keine Vakuole und keine Chloroplasten."],
 ["Was gibt der Pflanzenzelle Stabilität?", ["die Zellwand, zusammen mit der Vakuole", "der Zellkern, zusammen mit dem Cytoplasma", "die Mitochondrien, zusammen mit der Membran", "das Chlorophyll in den Chloroplasten"], "Die Vakuole stabilisiert die Zelle gemeinsam mit der Zellwand."],
 ["Was liegt der Zellwand innen an?", ["die Zellmembran", "die Vakuole", "der Zellkern", "die Kutikula"], "Über Zellwand und Zellmembran gelangen Stoffe hinein und hinaus."],
 ["Was enthält die Vakuole größtenteils?", ["Wasser", "Chlorophyll", "Erbinformationen", "Luft"], "Manchmal sind auch Farbstoffe darin."],
 ["Wo befindet sich der grüne Blattfarbstoff Chlorophyll?", ["in den Chloroplasten", "in der Vakuole", "im Zellkern", "in der Zellwand"], "Die Chloroplasten sind der Ort der Fotosynthese."],
 ["Was macht der Zellkern?", ["Er enthält die Erbinformationen und steuert die Lebensvorgänge der Zelle.", "Er stellt mithilfe von Chlorophyll Glucose für die Zelle her.", "Er gibt der Zelle von außen Stabilität und Form.", "Er speichert Wasser und Farbstoffe für die Zelle."], "Er ist von einer Membran umgeben."],
 ["Was sind Zellorganellen?", ["abgetrennte Reaktionsräume in der Zelle", "die Zellen eines Organs", "kleine Organe des Körpers", "die Löcher in der Zellwand"], "Zum Beispiel Zellkern, Chloroplasten und Mitochondrien."],
 ["Was bedeutet Kompartimentierung?", ["Die Zelle ist in abgetrennte Räume aufgeteilt, sodass Vorgänge sich nicht stören.", "Die Zelle teilt sich in zwei neue Zellen mit je einem Zellkern.", "Viele gleichartige Zellen schließen sich zu einem Gewebe zusammen.", "Die Zelle nimmt über ihre Membran Wasser und Nährstoffe auf."], "So können verschiedene Vorgänge gleichzeitig nebeneinander ablaufen."],
 ["Wo findest du Mitochondrien?", ["in Pflanzen- und in Tierzellen", "nur in Pflanzenzellen", "nur in Tierzellen", "nur in Blutzellen"], "Sie sind der Ort der Zellatmung. Im Lichtmikroskop sieht man sie nicht."],
 ["Welche Pflanzenzellen haben Chloroplasten?", ["grüne Pflanzenzellen", "alle Pflanzenzellen", "nur Wurzelzellen", "nur Zellen in der Erde"], "Im Buch steht: Chloroplasten sind ein Merkmal von grünen Pflanzenzellen."],
 ["Was gilt für ALLE Zellen?", ["Sie sind von einer Membran umgeben und brauchen Energie.", "Sie haben eine Zellwand.", "Sie haben Chloroplasten.", "Sie haben eine Vakuole."], "Zellwand, Chloroplasten und Vakuole haben nur Pflanzenzellen."],
 ["Was ist ein anderes Wort für Cytoplasma?", ["Zellplasma", "Zellwand", "Zellkern", "Chlorophyll"], "Beide Wörter kommen im Buch vor."],
],
"tatm": [
 ["Wie lautet die Wortgleichung der Zellatmung?", ["Glucose + Sauerstoff → Kohlenstoffdioxid + Wasser + Energie", "Kohlenstoffdioxid + Wasser → Glucose + Sauerstoff", "Glucose + Wasser → Sauerstoff + Energie", "Sauerstoff + Kohlenstoffdioxid → Glucose + Wasser"], "Wasser + Kohlenstoffdioxid → Glucose + Sauerstoff ist die Fotosynthese, also genau umgekehrt."],
 ["Wo findet die Zellatmung statt?", ["in den Mitochondrien", "in den Chloroplasten", "im Zellkern", "in der Lunge"], "In der Lunge wird nur Sauerstoff aufgenommen und Kohlenstoffdioxid abgegeben. Die Zellatmung selbst läuft in den Zellen ab."],
 ["Wozu dient die Zellatmung?", ["Sie macht die chemische Energie der Glucose für die Zellen nutzbar.", "Sie stellt Glucose her.", "Sie stellt Sauerstoff her.", "Sie transportiert Blut."], "Energie aus der Zellatmung ist die Grundlage aller Lebensvorgänge."],
 ["Welche Stoffe entstehen bei der Zellatmung?", ["Kohlenstoffdioxid und Wasser", "Glucose und Sauerstoff", "Sauerstoff und Wasser", "Stärke und Wasser"], "Sie sind energiearm, die Glucose war energiereich."],
 ["Wie gelangt die Glucose ins Blut?", ["durch die Verdauung über den Darm", "über die Lunge", "über die Haut", "aus den Mitochondrien"], "Sauerstoff gelangt beim Atmen über die Lunge ins Blut."],
 ["Was bringt Sauerstoff und Glucose zu den Zellen?", ["das Blut", "die Lunge", "der Darm", "die Mitochondrien"], "Das ist der Stofftransport."],
 ["Was wird bei der Zellatmung außer nutzbarer Energie noch frei?", ["Wärme", "Licht", "Schall", "Sauerstoff"], "Ein Teil der chemischen Energie der Glucose wird zu Wärmeenergie."],
 ["Wer betreibt Zellatmung?", ["Menschen, Tiere, Pflanzen, Pilze und viele andere Lebewesen", "nur Menschen und Tiere, aber keine Pflanzen", "nur grüne Pflanzen, wenn sie im Licht stehen", "nur Lebewesen, die eine Lunge haben"], "Auch Pflanzen atmen, Tag und Nacht."],
 ["Kann man Mitochondrien im Lichtmikroskop sehen?", ["Nein, sie sind nicht sichtbar.", "Ja, sie sind grün.", "Ja, sie sind die größten Organellen.", "Nur in Tierzellen."], "So steht es im Buch auf S. 34 und 36."],
 ["Jemand rennt schnell. Was passiert in den Muskelzellen?", ["Es läuft mehr Zellatmung ab, sie brauchen mehr Sauerstoff und Glucose.", "Die Zellatmung hört auf.", "Die Muskeln machen Fotosynthese.", "Sie brauchen weniger Sauerstoff."], "Deshalb atmet man bei Anstrengung schneller."],
 ["Ab wann können bei Sauerstoffmangel bleibende Schäden im Gehirn entstehen?", ["nach drei Minuten", "nach wenigen Sekunden", "nach einer Stunde", "nie"], "Nach wenigen Sekunden kommt es zu Störungen und Bewusstlosigkeit. Davon kann sich das Gehirn noch erholen."],
 ["Was haben Zellatmung und Kerzenflamme gemeinsam?", ["Beide brauchen Sauerstoff, und es entstehen Kohlenstoffdioxid und Wasser.", "Beide laufen bei 1400 °C ab.", "Bei beiden wird Glucose hergestellt.", "Beide finden in den Mitochondrien statt."], "Der Unterschied: Die Zellatmung läuft in vielen kleinen, geordneten Schritten ab, in der Kerzenflamme ist es etwa 1400 °C heiß."],
 ["Was macht eine grüne Pflanze im Licht?", ["Fotosynthese und zugleich Zellatmung", "nur Fotosynthese", "nur Zellatmung", "gar nichts"], "Grüne Pflanzenzellen haben Chloroplasten und Mitochondrien."],
 ["Was macht eine Pflanze im Dunkeln?", ["nur Zellatmung", "nur Fotosynthese", "Fotosynthese und Zellatmung", "gar nichts"], "Ohne Licht keine Fotosynthese. Die Zellatmung läuft immer."],
 ["Efeublätter unter einer beleuchteten Glocke (S. 37): Was passiert mit dem Kohlenstoffdioxid?", ["Es nimmt ab.", "Es nimmt zu.", "Es bleibt gleich.", "Es wird zu Glucose in der Luft."], "Von etwa 630 auf etwa 430 ppm in 15 Minuten. Die Blätter verbrauchen es bei der Fotosynthese."],
 ["Welche Hypothese passt, wenn die Efeublätter im Dunkeln stehen?", ["Der Kohlenstoffdioxid-Gehalt steigt.", "Der Kohlenstoffdioxid-Gehalt sinkt noch schneller.", "Es ändert sich gar nichts.", "Die Blätter geben Sauerstoff ab."], "Im Dunkeln läuft nur die Zellatmung, dabei entsteht Kohlenstoffdioxid."],
 ["Was bedeutet „wechselseitige Beziehung“ zwischen Pflanzen und Tieren?", ["Tiere brauchen den Sauerstoff aus der Fotosynthese, Pflanzen das Kohlenstoffdioxid aus der Atmung.", "Tiere und Pflanzen brauchen beide das Kohlenstoffdioxid aus der Luft zum Atmen.", "Pflanzen brauchen den Sauerstoff der Tiere, Tiere das Licht der Pflanzen.", "Pflanzen atmen nicht, deshalb bleibt mehr Sauerstoff für die Tiere übrig."], "Dazu kommt: Pflanzen liefern den Tieren auch Nährstoffe."],
],
}
QUIZ["t1"] = A.QUIZ["t1"]
QUIZ["t2"] = A.QUIZ["t2"]

# ================================================================ Probe-Arbeit
PROBE = f"""
<div class="box">
<h2>Probe-Arbeit Biologie</h2>
<div class="task"><h3>1. Van Helmont</h3>
<p>Van Helmont pflanzte eine junge Weide mit 2,3 kg in einen Kübel mit 90,7 kg getrockneter Erde. Nach fünf Jahren wog die Weide 76,7 kg. Die Erde hatte um 57 g abgenommen.</p>
<p>a) Nenne seine Problemfrage und seine Hypothese.<br>b) Berechne, um wie viel kg die Weide schwerer geworden ist.<br>c) Welche Erkenntnis gewann er?<br>d) Erkläre, warum er nur zum Teil recht hatte.</p>
<div class="lines"></div><div class="lines"></div><div class="lines"></div><div class="lines"></div>
<div class="sol">a) Problemfrage: Woher erhalten die Pflanzen die Stoffe für das Wachstum? Hypothese: Pflanzen brauchen Stoffe aus dem Erdboden und Wasser, weil sie mit den Wurzeln im Boden verankert sind.<br>b) 76,7 kg − 2,3 kg = 74,4 kg<br>c) Der Massezuwachs kommt vor allem vom Wasser. Die Pflanze muss das Gießwasser in pflanzliche Substanz umgewandelt haben.<br>d) Getrocknet wäre die Weide noch etwa 13 kg schwerer gewesen als am Anfang. Andere Forscher vermuteten deshalb, dass die Pflanze auch Stoffe aus der Luft aufnimmt.</div></div>
<div class="task"><h3>2. Priestley (1771)</h3>
<p>a) Kerze unter der Glocke: erlosch nach einiger Zeit. b) Kerze und Maus: Die Kerze erlosch viel schneller, die Maus wurde nach kurzer Zeit ohnmächtig. c) Nur die Maus: ohnmächtig, aber später als bei b. d) Maus und Pflanze: Die Maus wurde nicht ohnmächtig.</p>
<p>1) Erkläre die Ergebnisse von b, c und d mit dem heutigen Wissen.<br>2) Welcher Versuch ist der Kontrollversuch zu d? Begründe.<br>3) Welche zusätzliche Erkenntnis hatte Priestley gegenüber van Helmont?<br>4) Priestley bemerkte, dass die Versuche nachts anders abliefen. Welche neue Frage ergab sich daraus, und wer hat sie beantwortet?</p>
<div class="lines"></div><div class="lines"></div><div class="lines"></div><div class="lines"></div><div class="lines"></div>
<div class="sol">1) Kerze und Maus verbrauchen Sauerstoff. Bei b verbrauchen beide den Sauerstoff, deshalb ist er schnell aufgebraucht. Bei c verbraucht nur die Maus ihn, das dauert länger. Bei d stellt die Pflanze im Licht durch Fotosynthese Sauerstoff her und nutzt das Kohlenstoffdioxid, das die Maus ausatmet.<br>2) Versuch c: Er ist genauso aufgebaut wie d, nur die Pflanze fehlt.<br>3) Pflanzen verändern die Luft. Mit Pflanzen überleben Tiere in abgeschlossenen Räumen viel länger. Van Helmont dachte nur an Erde und Wasser.<br>4) Braucht die Pflanze Licht dafür? Ingenhousz zeigte 1779: Pflanzen stellen nur im Licht Sauerstoff her, im Dunkeln geben sie Kohlenstoffdioxid ab.</div></div>
<div class="task"><h3>3. Ein Experiment planen</h3>
<p>Plane ein Experiment zur Frage: <i>Wachsen Kressepflanzen mit Dünger besser als ohne?</i> Schreibe Hypothese, Durchführung und Kontrollversuch auf. Nenne, was du misst und was gleich bleiben muss.</p>
<div class="lines"></div><div class="lines"></div><div class="lines"></div><div class="lines"></div><div class="lines"></div>
<div class="sol">Hypothese zum Beispiel: Mit Dünger wachsen die Kressepflanzen höher, weil Dünger Mineralsalze enthält. (Eine Hypothese ist eine begründete Vermutung, sie kann auch anders lauten.)<br>Durchführung: Zwei Schalen mit gleich vielen, gleich großen Kressepflanzen. Schale 1 wird mit Dünger gegossen. Schale 2 ist der <b>Kontrollversuch</b>: Sie bekommt gleich viel Wasser, aber ohne Dünger.<br>Gemessen wird: die Länge der Pflanzen in cm nach einer bestimmten Zeit, zum Beispiel nach einer Woche, am besten bei mehreren Pflanzen.<br>Gleich bleiben: Kressesorte, Länge am Anfang, Wassermenge, Erde oder Watte, Schalen, Licht und Platz, Temperatur, Dauer.</div></div>
<div class="task"><h3>3b. Senebiers Frage selbst untersuchen</h3>
<p>Senebier fand 1783 heraus: Pflanzen stellen im Licht nur dann Sauerstoff her, wenn auch Kohlenstoffdioxid da ist. Plane mit der Bläschenzählmethode einen Versuch dazu: Frage, Hypothese, Durchführung, Kontrollversuch, was gemessen wird und was gleich bleibt.</p>
<div class="lines"></div><div class="lines"></div><div class="lines"></div><div class="lines"></div>
<div class="sol">Frage: Braucht die Pflanze Kohlenstoffdioxid, um im Licht Sauerstoff herzustellen?<br>Hypothese zum Beispiel: Mit mehr Kohlenstoffdioxid im Wasser steigen mehr Sauerstoff-Bläschen auf, weil die Pflanze Kohlenstoffdioxid für die Fotosynthese braucht.<br>Durchführung wie im Buch S. 27: Wasserpest in einem Glas mit Leitungswasser beleuchten und die Bläschen pro Minute zählen (<b>Kontrollversuch</b>). Dann dieselbe Pflanze in Leitungswasser mit sprudelndem Mineralwasser (enthält Kohlenstoffdioxid) und wieder zählen.<br>Gemessen: Zahl der Sauerstoff-Bläschen pro Minute.<br>Gleich bleiben: dieselbe Pflanze, gleiche Lampe und gleicher Abstand, gleiche Wassertemperatur (20 °C), gleiche Wassermenge, gleiche Zähldauer.</div></div>
<div class="task"><h3>4. Einen Versuch auswerten</h3>
<p>Mit der Bläschenzählmethode wurde bei verschiedenen Beleuchtungsstärken gezählt:</p>
<div class="tbl"><table><tr><th>Lux</th><td>200</td><td>1000</td><td>4000</td><td>8000</td><td>16000</td><td>24000</td><td>32000</td></tr><tr><th>Bläschen/min</th><td>0</td><td>1</td><td>4</td><td>8</td><td>12</td><td>13</td><td>13</td></tr></table></div>
<p>a) Was wird bei der Bläschenzählmethode gemessen, und was zeigt es an?<br>b) Beschreibe den Verlauf.<br>c) Erkläre den Verlauf.</p>
<div class="lines"></div><div class="lines"></div><div class="lines"></div><div class="lines"></div>
<div class="sol">a) Die Zahl der Sauerstoff-Bläschen pro Minute. Je mehr Bläschen, desto höher die Fotosynthese-Leistung.<br>b) Bis 8000 Lux steigt die Zahl gleichmäßig an, danach langsamer. Ab 24000 Lux bleibt sie gleich bei 13.<br>c) Mehr Licht bedeutet mehr Fotosynthese und mehr Sauerstoff. Ab einer bestimmten Lichtstärke hilft mehr Licht nicht mehr, dann begrenzt etwas anderes, zum Beispiel zu wenig Kohlenstoffdioxid oder die Temperatur.</div></div>
<div class="task"><h3>5. Der Blattquerschnitt</h3>
{blatt()}
<p>a) Beschrifte die Zeichnung.<br>b) Beschreibe den Weg von Kohlenstoffdioxid und Wasser zu den Blattzellen.<br>c) Nenne zwei Angepasstheiten des Blattes an die Fotosynthese.</p>
<div class="lines"></div><div class="lines"></div><div class="lines"></div><div class="lines"></div>
<div class="sol">a) 1 Kutikula · 2 obere Epidermis · 3 Palisadengewebe · 4 Schwammgewebe · 5 untere Epidermis · 6 Chloroplast · 7 Leitbündel · 8 Interzellulare (Luftraum) · 9 Schließzelle · 10 Spaltöffnung<br>b) Kohlenstoffdioxid gelangt über die Spaltöffnungen ins Blatt und durch die Interzellularen zu den Zellen. Wasser gelangt über die Leitbündel ins Blatt.<br>c) Zum Beispiel: Die obere Epidermis hat keine Chloroplasten, deshalb kommt das Licht gut zum Palisadengewebe. Das Palisadengewebe hat besonders viele Chloroplasten, dort ist die Fotosynthese besonders stark. Spaltöffnungen ermöglichen den Gasaustausch. Die Interzellularen verteilen das Kohlenstoffdioxid bis zu den Zellen.</div></div>
<div class="task"><h3>6. Tier- und Pflanzenzelle</h3>
{pflanzenzelle()}
<p>a) Beschrifte die Pflanzenzelle.<br>b) Vergleiche Pflanzen- und Tierzelle in einer Tabelle.<br>c) Nenne die Aufgabe der Vakuole.</p>
<div class="lines"></div><div class="lines"></div><div class="lines"></div><div class="lines"></div>
<div class="sol">a) 1 Zellwand · 2 Zellkern · 3 Zellmembran · 4 Cytoplasma · 5 Chloroplast · 6 Mitochondrium · 7 Vakuole<br>b) Beide: Zellmembran, Cytoplasma, Zellkern, Mitochondrien. Nur die Pflanzenzelle: Zellwand, Vakuole, Chloroplasten.<br>c) Sie enthält größtenteils Wasser, kann Wasser aufnehmen und abgeben und stabilisiert gemeinsam mit der Zellwand die Zelle.</div></div>
<div class="task"><h3>7. Die Zellatmung</h3>
<p>a) Schreibe die Wortgleichung der Zellatmung auf.<br>b) Wo findet sie statt, und wozu dient sie?<br>c) Beschreibe, wie Sauerstoff und Glucose zu den Zellen kommen und wie Kohlenstoffdioxid den Körper verlässt.<br>d) Vergleiche Zellatmung und Fotosynthese (Ausgangsstoffe, Produkte, Ort).</p>
<div class="lines"></div><div class="lines"></div><div class="lines"></div><div class="lines"></div><div class="lines"></div>
<div class="sol">a) Glucose + Sauerstoff → Kohlenstoffdioxid + Wasser + Energie<br>b) In den Mitochondrien der Zellen. Sie macht die chemische Energie der Glucose für die Zellen nutzbar. Ein Teil wird zu Wärme.<br>c) Sauerstoff gelangt beim Atmen über die Lunge ins Blut, Glucose durch die Verdauung über den Darm ins Blut. Das Blut bringt beides zu den Zellen. Das Kohlenstoffdioxid wird mit dem Blut zur Lunge gebracht und ausgeatmet.<br>d) Fotosynthese: Wasser + Kohlenstoffdioxid → Glucose + Sauerstoff, mit Licht, in den Chloroplasten. Zellatmung: genau umgekehrt, Glucose + Sauerstoff → Kohlenstoffdioxid + Wasser, in den Mitochondrien. Fotosynthese speichert Lichtenergie in der Glucose, Zellatmung macht diese Energie nutzbar.</div></div>
</div>
"""

# ---------------------------------------------------------------- Seitenrahmen
HEAD = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} – Biologie</title>
<meta name="apple-mobile-web-app-title" content="Biologie">
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

def nav(cur):
    items = [("../index.html", "← Fächer", None), ("index.html", "🏠 Start", "start")]
    items += [(s["file"], s["nav"], s["id"]) for s in STEPS + ZUSATZ]
    return "\n".join(f'  <a href="{h}"{" aria-current=\"page\"" if i == cur else ""}>{t}</a>' for h, t, i in items)

def page(pid, title, body):
    return HEAD.format(title=title, pid=pid, nav=nav(pid), ver=VER) + body + FOOT.format(ver=VER)

def nextbtn(sid):
    ids = [s["id"] for s in STEPS]
    if sid not in ids:
        return '<a class="btn big noprint" href="index.html">Fertig ✓ – zurück zum Start</a>'
    i = ids.index(sid)
    if i + 1 < len(STEPS):
        n = STEPS[i + 1]
        return f'<a class="btn big noprint" data-finish="{sid}" href="{n["file"]}">Fertig ✓ – weiter zu {n["nav"]} →</a>'
    return f'<a class="btn big noprint" data-finish="{sid}" href="index.html">Fertig ✓ – zurück zum Start</a>'

def part(n, name, hint):
    return f'<h2 class="part"><span class="num">{n}</span> {name}</h2>\n<p class="hint">{hint}</p>\n'

def mbox(mid, title):
    return f'<div class="box"><h3>{title}</h3><div data-match="{mid}"></div></div>\n'

def sbox(sid, title):
    return f'<div class="box"><h3>{title}</h3><div data-sort="{sid}"></div></div>\n'

UEBEN = {
 "t3": ("Zuordnen", "Zieh die Kärtchen an die richtige Stelle.",
        mbox("m-helmont", "Die Schritte bei van Helmont") + mbox("m-priestley", "Priestleys Versuche") + mbox("m-spirale", "Wer hat was herausgefunden?") + mbox("m-schritte", "Der Weg der Erkenntnisgewinnung")),
 "texp": ("Planen üben", "Sortiere, was verändert, gemessen und gleich gehalten wird.",
        sbox("s-variablen", "Versuch aus dem Buch") + sbox("s-duenger", "Ein eigenes Experiment") + mbox("m-protokoll", "Das Versuchsprotokoll")),
 "t4": ("Beschriften und Zuordnen", "Beschrifte den Blattquerschnitt und ordne Aufgaben und Angepasstheiten zu.",
        mbox("m-blatt", "Beschrifte den Blattquerschnitt") + mbox("m-blatt-auf", "Welches Teil macht was?") + mbox("m-angepasst", "Angepasstheiten")),
 "tzell": ("Beschriften und Sortieren", "Beschrifte beide Zellen und sortiere die Bestandteile.",
        mbox("m-pfl", "Beschrifte die Pflanzenzelle") + mbox("m-tier", "Beschrifte die Tierzelle") + sbox("s-zellen", "Nur Pflanze oder beide?") + mbox("m-zellteile", "Welcher Bestandteil ist das?")),
 "tatm": ("Zuordnen und Sortieren", "Zieh die Kärtchen an die richtige Stelle.",
        mbox("m-gleichung", "Die Wortgleichung") + mbox("m-weg", "Der Weg der Stoffe") + sbox("s-fs-za", "Fotosynthese oder Zellatmung?") + sbox("s-gewaesser", "Modellgewässer")),
 "t1": ("Beschriften und Rechnen", "Beschrifte das Mikroskop und ordne die Aufgaben zu. Dann rechnest du Vergrößerungen.",
        mbox("m-mikro", "Beschrifte das Mikroskop") + mbox("m-mikro-auf", "Welches Teil macht was?")
        + '<h3>Gesamtvergrößerung rechnen</h3><p class="meta">Okular mal Objektiv. Es kommen immer neue Aufgaben.</p><div data-calc></div>\n'),
 "t2": ("Ordnen und Zuordnen", "Zieh die Wörter an die richtige Stelle.",
        mbox("m-stufen", "Von klein nach groß") + mbox("m-magen", "Das Beispiel Magen") + mbox("m-spez", "Spezialisierte Zellen")),
}

def write(name, text):
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(text)

def stepcard(n, s, extra=False):
    attr = '' if extra else f' data-step="{s["id"]}"'
    return f'<a class="step{" extra" if extra else ""}"{attr} href="{s["file"]}"><span class="num">{n}</span><span class="stxt"><b>{s["title"]}</b><span class="meta"> · {s["dur"]}</span><br><span class="meta">{s["desc"]}</span></span></a>\n'

def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))
    b = f'<h1>Biologie</h1>\n<p class="sub">{KLAUSUR}</p>\n'
    b += '<div class="box merke"><h3>So lernst du</h3><p>Die fünf Themen sind genau die, die Frau Brinkmann genannt hat. Mach sie <b>der Reihe nach</b>. Jedes Thema ist eine eigene Seite: erst lesen, dann üben (Kärtchen mit dem Finger ziehen), dann Karten, dann Quiz. Unten tippst du auf <b>„Fertig ✓“</b>.</p><p class="meta" id="st-left"></p></div>\n'
    for i, s in enumerate(STEPS):
        b += stepcard(i + 1, s)
    b += '<div class="box" id="st-all" hidden><h3>🎉 Super, alles geschafft!</h3><p>Du bist gut vorbereitet. Am Abend vor der Arbeit: nochmal das große Quiz und die Zeichnungen beschriften.</p></div>\n'
    b += '<h2 style="margin-top:2rem">Zum Wiederholen</h2><p class="meta">„Alles bisher Erarbeitete kann drankommen.“ Diese Themen stehen nicht auf der Liste, sind aber gut zum Wiederholen.</p>\n'
    for s in ZUSATZ:
        b += stepcard("+", s, extra=True)
    b += '<p><button class="btn ghost small" id="st-reset">Alle Haken löschen</button></p>'
    write("index.html", page("start", "Start", b))
    for i, s in enumerate(TOPICS + ZUSATZ):
        t = s["id"]
        crumb = f"Thema {i+1} von {len(TOPICS)}" if s in TOPICS else "Zusatz zum Wiederholen"
        b = f'<p class="crumb">{crumb}</p>\n<h1>{s["title"]}</h1>\n'
        b += part(1, "Lesen", "Lies alles einmal in Ruhe durch.") + LESEN[t]
        name, hint, body = UEBEN[t]
        b += part(2, name, hint) + body
        b += part(3, "Karten", "Überleg dir die Antwort. Dann tippe auf die Karte.") + '<div id="cards"></div>\n'
        b += part(4, "Quiz", "Tippe auf die richtige Antwort.") + '<div id="quiz"></div>\n'
        b += nextbtn(t)
        write(s["file"], page(t, s["title"], b))
    b = '<h1>Großes Quiz</h1>\n<p class="hint">Alle Fragen aus den fünf Themen, bunt gemischt. Ziel: höchstens 8 Fehler.</p>\n<div id="quiz"></div>\n' + nextbtn("gem")
    write("gemischt.html", page("gem", "Großes Quiz", b))
    tools = '<div class="row noprint"><button class="btn ghost" data-sol>Lösungen zeigen</button><button class="btn" data-print="0">Drucken</button><button class="btn ghost" data-print="1">Mit Lösungen drucken</button></div>\n'
    b = '<p class="hint noprint">So geht\'s: Drucke die Arbeit aus oder schreib die Antworten auf einen Zettel. Nimm dir 45 Minuten. Erst danach tippst du auf „Lösungen zeigen“ und vergleichst.</p>\n' + tools + PROBE + nextbtn("probe")
    write("probe.html", page("probe", "Probe-Arbeit", b))
    js = open(os.path.join(ROOT, "_build", "bio.src.js"), encoding="utf-8").read()
    data = dict(cards=CARDS, quiz=QUIZ, match=MATCH, sort=SORT, steps=[s["id"] for s in STEPS], topics=[s["id"] for s in TOPICS])
    write("app.js", js.replace("__DATA__", json.dumps(data, ensure_ascii=False)))
    css = open(os.path.join(ROOT, "_build", "app.css"), encoding="utf-8").read() + open(os.path.join(ROOT, "_build", "bio-extra.css"), encoding="utf-8").read()
    write("app.css", css)
    print("gebaut:", sorted(os.listdir(OUT)))

if __name__ == "__main__":
    main()
