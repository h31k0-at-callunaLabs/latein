#!/usr/bin/env python3
"""Baut die Biologie-Seiten (eine Seite pro Thema) nach ../biologie/. Aufruf: python3 _build/bio.py
Quelle: Biologie-Buch S. 18 (Mikroskopieren), S. 20 (Zellen, Gewebe, Organ, Organismus),
S. 22 (Naturwissenschaftliche Erkenntnisgewinnung), S. 24 (Blätter – Orte der Fotosynthese)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bio_svg import mikroskop, blatt, MIKRO_TEILE, BLATT_TEILE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "biologie")
KLAUSUR = "Klausur: Datum kommt noch"   # z. B. "Klausur am Dienstag, 24.11."
VER = "1"

TOPICS = [
 dict(id="t1", file="mikroskop.html", nav="1 Mikroskop", title="Das Lichtmikroskop", dur="15 Minuten", desc="Teile beschriften, Aufgaben der Teile, Vergrößerung rechnen. Buch S. 18."),
 dict(id="t2", file="zellen.html", nav="2 Zelle → Organismus", title="Zelle, Gewebe, Organ, Organismus", dur="10 Minuten", desc="Spezialisierte Zellen und die Stufen bis zum Menschen. Buch S. 20."),
 dict(id="t3", file="forschen.html", nav="3 Forschen", title="Wie Forscher etwas herausfinden", dur="15 Minuten", desc="Die Schritte der Erkenntnisgewinnung und das Weiden-Experiment von van Helmont. Buch S. 22."),
 dict(id="t4", file="laubblatt.html", nav="4 Laubblatt", title="Das Laubblatt: Ort der Fotosynthese", dur="15 Minuten", desc="Die Schichten im Blatt beschriften und ihre Aufgaben kennen. Buch S. 24."),
]
EXTRA = [
 dict(id="gem", file="gemischt.html", nav="5 Großes Quiz", title="Großes Quiz: alles gemischt", dur="15 Minuten", desc="Alle Fragen aus allen Themen durcheinander."),
 dict(id="probe", file="probe.html", nav="6 Probe-Klausur", title="Probe-Klausur", dur="30 Minuten", desc="Aufgaben wie in einer Klausur, mit Lösungen zum Vergleichen."),
]
STEPS = TOPICS + EXTRA

# ---------------------------------------------------------------- Lesen
LESEN = {
"t1": f"""
<div class="box merke"><h3>Das musst du wissen</h3>
<p><b>Gesamtvergrößerung = Vergrößerung des Okulars · Vergrößerung des Objektivs</b></p>
<p>Beispiel: Okular 10-fach, Objektiv 40-fach → 10 · 40 = <b>400-fach</b>.</p>
<p><b>Tragen:</b> Eine Hand greift unter das Mikroskop, die andere Hand an den Trägerarm.</p></div>
<div class="box"><h3>Die Teile und ihre Aufgaben (Buch S. 18)</h3>
{mikroskop()}
<div class="tbl"><table>
<tr><th>Nr.</th><th>Teil</th><th>Aufgabe</th></tr>
<tr><td>1</td><td><b>Okular</b></td><td>Ein Linsensystem mit einer angegebenen Vergrößerung. Hier schaust du hinein.</td></tr>
<tr><td>2</td><td><b>Tubus</b></td><td>Eine Röhre, die das Okular enthält.</td></tr>
<tr><td>3</td><td><b>Objektivrevolver</b></td><td>Durch Drehen werden die verschiedenen Objektive gewechselt.</td></tr>
<tr><td>4</td><td><b>Objektiv</b></td><td>Linsen mit einer angegebenen Vergrößerung.</td></tr>
<tr><td>5</td><td><b>Objekttisch</b></td><td>Hier werden die Präparate abgelegt. Er ist in der Höhe verstellbar.</td></tr>
<tr><td>6</td><td><b>Kondensor</b></td><td>Bündelt die Strahlen, die von der Lichtquelle ausgehen.</td></tr>
<tr><td>7</td><td><b>Blende</b></td><td>Sorgt für eine gleichmäßige Beleuchtung des Präparats.</td></tr>
<tr><td>8</td><td><b>Lichtquelle</b></td><td>Befindet sich im Fuß des Mikroskops und hat meist einen Helligkeitsregler.</td></tr>
<tr><td>9</td><td><b>Trägerarm</b></td><td>Hier greift beim Tragen eine Hand an. Die andere Hand greift unter das Mikroskop.</td></tr>
<tr><td>10</td><td><b>Grob- und Feintrieb</b></td><td>Zwei Drehknöpfe. Sie verändern den Abstand zwischen Objekttisch und Objektiv. Damit stellst du das Bild scharf.</td></tr>
</table></div>
<p class="meta">Der gelbe Strich zeigt den Weg des Lichts: von der Lichtquelle durch Blende, Kondensor, Präparat, Objektiv und Tubus bis ins Okular.</p></div>
<div class="box"><h3>Merkhilfe</h3>
<ul><li>Das <b>Okular</b> ist oben, direkt am <b>Auge</b> (lateinisch oculus = Auge).</li>
<li>Das <b>Objektiv</b> ist unten, nah am <b>Objekt</b> (dem Präparat).</li>
<li>Der Objektiv<b>revolver</b> dreht sich wie die Trommel eines Revolvers.</li></ul></div>
""",
"t2": """
<div class="box merke"><h3>Das musst du wissen</h3>
<p>Von klein nach groß:</p>
<div class="chain"><span>Zelle</span><i>→</i><span>Gewebe</span><i>→</i><span>Organ</span><i>→</i><span>Organsystem</span><i>→</i><span>Organismus</span></div>
<p>Beispiel aus dem Buch: Drüsenzelle → Drüsengewebe der Magenschleimhaut → Magen → Verdauungssystem → Mensch.</p></div>
<div class="box"><h3>Spezialisierte Zellen</h3>
<p>Einzeller bestehen aus nur einer Zelle. Menschen, die meisten Tiere und Pflanzen bestehen aus <b>Milliarden von Zellen</b>. Diese Zellen haben verschiedene Aufgaben. Jeder Zelltyp erfüllt eine bestimmte Aufgabe. So findet eine <b>Arbeitsteilung</b> statt. Man spricht von <b>spezialisierten Zellen</b>.</p>
<div class="tbl"><table><tr><th>Zelle</th><th>spezialisiert auf …</th></tr>
<tr><td><b>Nervenzellen</b></td><td>die Weiterleitung von Informationen</td></tr>
<tr><td><b>Muskelzellen</b></td><td>Kontraktionen (sich zusammenziehen)</td></tr>
<tr><td><b>Rote Blutzellen</b></td><td>den Transport von Sauerstoff</td></tr></table></div>
<p>In den Zeichnungen im Buch sind diese Teile beschriftet: <b>Zellmembran</b>, <b>Cytoplasma</b> und <b>Zellkern</b>. Bei der roten Blutzelle ist kein Zellkern eingezeichnet: Rote Blutzellen des Menschen haben keinen Zellkern.</p></div>
<div class="box"><h3>Die Stufen (Buch S. 20)</h3>
<ul class="layers">
<li style="--c:#7DB8E6"><b>Zelle:</b> Die kleinste Stufe in dieser Reihe. Die Zelle ist die kleinste lebende Einheit. Beispiel: eine Drüsenzelle.</li>
<li style="--c:#2477B3"><b>Gewebe:</b> Spezialisierte Zellen sind zu Zellverbänden zusammengeschlossen. Beispiel: das Drüsengewebe der Magenschleimhaut.</li>
<li style="--c:#2E8A5E"><b>Organ:</b> Mehrere Gewebe erfüllen gemeinsam eine oder mehrere Aufgaben. Beispiel: der Magen. Er besteht aus verschiedenen Gewebetypen, die gemeinsam die Aufgabe der Verdauung erfüllen.</li>
<li style="--c:#B88A00"><b>Organsystem:</b> Mehrere Organe arbeiten zusammen. Beispiel: das Verdauungssystem. Dazu gehören zum Beispiel der Mund (mit Zähnen und Speicheldrüsen), der Magen, der Dünndarm und der Dickdarm.</li>
<li style="--c:#D85F1C"><b>Organismus:</b> Alle Organe und Organsysteme zusammen. Sie ergänzen sich mit ihren Aufgaben zum Organismus. Beispiel: der Mensch.</li>
</ul></div>
""",
"t3": """
<div class="box merke"><h3>Das musst du wissen</h3>
<p>So gewinnen Forscher neue Erkenntnisse:</p>
<div class="chain"><span>Beobachtung</span><i>→</i><span>Problemfrage</span><i>→</i><span>Hypothese</span><i>→</i><span>Untersuchung (z. B. Experiment)</span><i>→</i><span>Ergebnis</span><i>→</i><span>Schlussfolgerung</span><i>→</i><span>Erkenntnisgewinn</span></div>
<p>Eine <b>Hypothese</b> ist eine <b>begründete Vermutung</b>.</p></div>
<div class="box"><h3>Die Schritte erklärt (Buch S. 22)</h3>
<ol>
<li><b>Beobachtung:</b> Am Anfang steht meist etwas, das man mit seinem Vorwissen nicht erklären kann oder das sonderbar erscheint.</li>
<li><b>Problemfrage:</b> Dazu stellt man eine Frage, die untersucht werden soll. Die Frage genau zu formulieren, ist nicht immer einfach.</li>
<li><b>Hypothese:</b> Um die Frage zu beantworten, stellt man Hypothesen auf. Das sind begründete Vermutungen.</li>
<li><b>Untersuchung, zum Beispiel ein Experiment:</b> Damit überprüft man die Hypothese. Das Experiment ist in den Naturwissenschaften eine besonders wichtige Untersuchungsmethode.</li>
<li><b>Ergebnis und Schlussfolgerung:</b> Aus den Ergebnissen und den Schlussfolgerungen daraus kommt man zur Lösung der Problemfrage.</li>
<li><b>Erkenntnisgewinn:</b> Verallgemeinert man die Lösung, gewinnt man eine Erkenntnis. Sie kann der Startpunkt für neue Fragen sein.</li>
</ol>
<p class="meta">Auch die Fotosynthese wurde so erforscht: Durch viele Untersuchungen wurde sie Schritt für Schritt aufgedeckt und wie ein Puzzle zusammengesetzt.</p></div>
<div class="box"><h3>Das Weiden-Experiment von Johann van Helmont</h3>
<div class="tbl"><table>
<tr><th>Schritt</th><th>Bei van Helmont</th></tr>
<tr><td><b>Beobachtung</b></td><td>Pflanzen wachsen und nehmen dabei an Größe und Masse zu.</td></tr>
<tr><td><b>Problemfrage</b></td><td>Woher erhalten die Pflanzen die Stoffe für das Wachstum?</td></tr>
<tr><td><b>Hypothese</b></td><td>Pflanzen brauchen für das Wachstum Stoffe aus dem Erdboden und Wasser, weil sie mit den Wurzeln im Boden verankert sind.</td></tr>
<tr><td><b>Experiment</b></td><td>1635 pflanzte er eine junge Weide (2,3 kg) in einen Kübel mit 90,7 kg getrockneter Erde. Die Erde war mit einer durchlöcherten Metallplatte abgedeckt. Die Weide stand im Freien und wurde mit Regenwasser gegossen. Nach fünf Jahren (1640) wurde gewogen.</td></tr>
<tr><td><b>Ergebnis</b></td><td>Die Weide wog 76,7 kg. Sie war also <b>74,4 kg schwerer</b> geworden (76,7 − 2,3 = 74,4). Die Erde war nur <b>57 g leichter</b>.</td></tr>
<tr><td><b>Schlussfolgerung</b></td><td>Rückbezug zur Hypothese: Der Massezuwachs kommt vor allem von der Aufnahme von Wasser und nur zu einem kleinen Teil aus Stoffen aus dem Boden.</td></tr>
<tr><td><b>Erkenntnis</b></td><td>Die Pflanze muss das Gießwasser in pflanzliche Substanz umgewandelt haben.</td></tr>
</table></div>
<p class="meta">Achtung: 57 <b>Gramm</b>, nicht Kilogramm!</p></div>
<div class="box"><h3>Van Helmont hatte nur zum Teil recht</h3>
<p>Andere Forscher fragten sich, ob seine Schlussfolgerung stimmt. Hätte er die Weide am Ende vollständig getrocknet, wäre sie immer noch <b>etwa 13 kg schwerer</b> gewesen als am Anfang. Diese 13 kg sind also kein Wasser, das nur in der Pflanze gespeichert ist.</p>
<p>Die Forscher stellten deshalb eine <b>neue Hypothese</b> auf: Die Pflanze nimmt für ihr Wachstum <b>auch Stoffe aus der Luft</b> auf.</p>
<p class="meta">So wird ein Erkenntnisgewinn zum Startpunkt für eine neue Frage.</p></div>
""",
"t4": f"""
<div class="box merke"><h3>Das musst du wissen</h3>
<p>Das Laubblatt ist ein <b>Organ</b> aus mehreren Geweben. Durch seinen Bau ist es hervorragend an die Fotosynthese angepasst.</p>
<p>Von oben nach unten: <b>Kutikula → obere Epidermis → Palisadengewebe → Schwammgewebe → untere Epidermis (mit Spaltöffnungen) → Kutikula</b></p></div>
<div class="box"><h3>Der Blattquerschnitt (Buch S. 24)</h3>
{blatt()}
<div class="tbl"><table>
<tr><th>Nr.</th><th>Teil</th><th>Bau und Aufgabe</th></tr>
<tr><td>1</td><td><b>Kutikula</b></td><td>Eine Wasser abweisende Schicht aus Wachs. Deshalb perlen Regentropfen ab. Die Blatthaut gibt sie nach außen ab. Sie schützt das Blatt vor Schmutz und vor zu viel Wasserverlust durch Verdunstung.</td></tr>
<tr><td>2</td><td><b>obere Epidermis</b></td><td>Die Blatthaut: dicht aneinanderliegende Zellen. Sie schützt das Blatt vor Verletzungen. Ihre Zellen haben <b>keine Chloroplasten</b> und lassen deshalb das Licht gut durch.</td></tr>
<tr><td>3</td><td><b>Palisadengewebe</b></td><td>Lang gestreckte Zellen, die regelmäßig nebeneinanderstehen wie ein Palisadenzaun. Sie haben <b>besonders viele Chloroplasten</b> und sind deshalb kräftig grün.</td></tr>
<tr><td>4</td><td><b>Schwammgewebe</b></td><td>Unregelmäßig geformte Zellen mit Chloroplasten. Dazwischen liegen große, mit Luft gefüllte Hohlräume.</td></tr>
<tr><td>5</td><td><b>untere Epidermis</b></td><td>Blatthaut an der Unterseite. Hier sind <b>viele Spaltöffnungen</b>.</td></tr>
<tr><td>6</td><td><b>Chloroplast</b></td><td>Die grünen Körnchen in den Zellen. In ihnen findet die Fotosynthese statt.</td></tr>
<tr><td>7</td><td><b>Leitbündel</b></td><td>Bilden die Blattadern, die man von außen sieht. Darin werden zum Beispiel Wasser, Mineralsalze und Glucose transportiert.</td></tr>
<tr><td>8</td><td><b>Interzellulare</b></td><td>Ein luftgefüllter Hohlraum zwischen den Zellen des Schwammgewebes (Mehrzahl: Interzellularen). Die Hohlräume stehen mit den Spaltöffnungen in Verbindung.</td></tr>
<tr><td>9</td><td><b>Schließzelle</b></td><td>Zwei bohnenförmige Schließzellen bilden eine Spaltöffnung. Anders als die anderen Epidermiszellen haben sie <b>Chloroplasten</b>.</td></tr>
<tr><td>10</td><td><b>Spaltöffnung</b></td><td>Kann sich öffnen oder schließen. So findet ein kontrollierter <b>Gasaustausch</b> mit der Umgebung statt.</td></tr>
</table></div>
<p class="meta">Die Zeichnung ist vereinfacht. Kutikula und Epidermis gibt es oben und unten am Blatt. Von der Kutikula ist in der Zeichnung nur die obere nummeriert.</p></div>
"""
}

# ---------------------------------------------------------------- Zuordnen / Beschriften
MATCH = {
 "m-mikro": dict(fig=mikroskop(), how="Beschrifte das Mikroskop: Zieh jedes Wort auf die passende Nummer.",
   slots=[[str(i), n] for i, n in enumerate(MIKRO_TEILE, 1)],
   why="Super! Diese Beschriftung kommt oft in Klausuren dran."),
 "m-mikro-auf": dict(wide=True, how="Welches Teil hat welche Aufgabe? Zieh den Namen zur Aufgabe.",
   slots=[["Hier schaust du hinein. Es hat eine angegebene Vergrößerung.", "Okular"],
          ["Durch Drehen werden die Objektive gewechselt.", "Objektivrevolver"],
          ["Bündelt die Strahlen, die von der Lichtquelle ausgehen.", "Kondensor"],
          ["Sorgt für eine gleichmäßige Beleuchtung des Präparats.", "Blende"],
          ["Hier wird das Präparat abgelegt. Er ist in der Höhe verstellbar.", "Objekttisch"],
          ["Damit stellst du das Bild scharf.", "Grob- und Feintrieb"],
          ["Eine Röhre, die das Okular enthält.", "Tubus"]]),
 "m-stufen": dict(wide=True, how="Bring die Stufen in die richtige Reihenfolge, von klein nach groß.",
   slots=[["1. (am kleinsten)", "Zelle"], ["2.", "Gewebe"], ["3.", "Organ"], ["4.", "Organsystem"], ["5. (am größten)", "Organismus"]]),
 "m-magen": dict(wide=True, how="Das Beispiel aus dem Buch: Was ist was?",
   slots=[["Drüsenzelle", "Zelle"], ["Drüsengewebe der Magenschleimhaut", "Gewebe"], ["Magen", "Organ"], ["Verdauungssystem", "Organsystem"], ["Mensch", "Organismus"]]),
 "m-spez": dict(wide=True, how="Worauf ist welche Zelle spezialisiert?",
   slots=[["Nervenzelle", "Weiterleitung von Informationen"], ["Muskelzelle", "Kontraktionen (sich zusammenziehen)"], ["Rote Blutzelle", "Transport von Sauerstoff"]]),
 "m-schritte": dict(wide=True, how="Bring die Schritte der Erkenntnisgewinnung in die richtige Reihenfolge.",
   slots=[["1.", "Beobachtung"], ["2.", "Problemfrage"], ["3.", "Hypothese"], ["4.", "Untersuchung (z. B. Experiment)"], ["5.", "Ergebnis"], ["6.", "Schlussfolgerung"], ["7.", "Erkenntnisgewinn"]]),
 "m-helmont": dict(wide=True, how="Welcher Schritt ist das bei van Helmont? Zieh den Schritt zum passenden Satz.",
   slots=[["Pflanzen wachsen und nehmen an Größe und Masse zu.", "Beobachtung"],
          ["Woher erhalten die Pflanzen die Stoffe für das Wachstum?", "Problemfrage"],
          ["Pflanzen brauchen Stoffe aus dem Erdboden und Wasser, weil sie mit den Wurzeln im Boden verankert sind.", "Hypothese"],
          ["Eine Weide wird in einen Kübel mit getrockneter Erde gepflanzt, fünf Jahre gegossen und dann gewogen.", "Experiment"],
          ["Die Weide ist 74,4 kg schwerer, die Erde nur 57 g leichter.", "Ergebnis"],
          ["Der Massezuwachs kommt vor allem von der Aufnahme von Wasser, nur wenig aus dem Boden.", "Schlussfolgerung"],
          ["Die Pflanze muss das Gießwasser in pflanzliche Substanz umgewandelt haben.", "Erkenntnisgewinn"]]),
 "m-blatt": dict(fig=blatt(), how="Beschrifte den Blattquerschnitt: Zieh jedes Wort auf die passende Nummer.",
   slots=[[str(i), n] for i, n in enumerate(BLATT_TEILE, 1)],
   why="Super! Merke dir die Reihenfolge von oben nach unten."),
 "m-blatt-auf": dict(wide=True, how="Welches Teil hat welche Aufgabe? Zieh den Namen zur Aufgabe.",
   slots=[["Wachsschicht. Schützt vor Schmutz und vor Wasserverlust durch Verdunstung.", "Kutikula"],
          ["Dicht aneinanderliegende Zellen, fast alle ohne Chloroplasten. Schützt vor Verletzungen und lässt Licht durch.", "Epidermis"],
          ["Lang gestreckte Zellen mit besonders vielen Chloroplasten.", "Palisadengewebe"],
          ["Unregelmäßige Zellen mit großen Lufträumen dazwischen.", "Schwammgewebe"],
          ["Transportiert zum Beispiel Wasser, Mineralsalze und Glucose.", "Leitbündel"],
          ["Kann sich öffnen und schließen. Ermöglicht den Gasaustausch.", "Spaltöffnung"]]),
}
for k, m in MATCH.items():
    m["id"] = k
    assert len({s[1] for s in m["slots"]}) == len(m["slots"]), k

# ---------------------------------------------------------------- Karten
CARDS = {
"t1": [
 ["Okular", "Ein Linsensystem mit einer angegebenen Vergrößerung. Hier schaust du hinein."],
 ["Objektiv", "Linsen mit einer angegebenen Vergrößerung. Sie sind am Objektivrevolver, nah über dem Präparat."],
 ["Objektivrevolver", "Durch Drehen werden die verschiedenen Objektive gewechselt."],
 ["Tubus", "Eine Röhre, die das Okular enthält."],
 ["Objekttisch", "Hier werden die Präparate abgelegt. Er ist in der Höhe verstellbar."],
 ["Kondensor", "Bündelt die Strahlen, die von der Lichtquelle ausgehen."],
 ["Blende", "Sorgt für eine gleichmäßige Beleuchtung des Präparats."],
 ["Grob- und Feintrieb", "Zwei Drehknöpfe. Sie verändern den Abstand zwischen Objekttisch und Objektiv. Damit stellt man das Bild scharf."],
 ["Lichtquelle", "Sie ist im Fuß des Mikroskops und hat meist einen Helligkeitsregler."],
 ["Wie berechnet man die Gesamtvergrößerung?", "Vergrößerung des Okulars · Vergrößerung des Objektivs.<br>Beispiel: 10 · 40 = 400-fach."],
 ["Wie trägt man ein Mikroskop?", "Eine Hand greift unter das Mikroskop, die andere Hand an den Trägerarm."],
],
"t2": [
 ["Spezialisierte Zellen", "Zellen, die auf eine bestimmte Aufgabe spezialisiert sind. Jeder Zelltyp erfüllt eine bestimmte Aufgabe."],
 ["Arbeitsteilung", "In Vielzellern erfüllt jeder Zelltyp eine bestimmte Aufgabe."],
 ["Nervenzellen sind spezialisiert auf …", "… die Weiterleitung von Informationen."],
 ["Muskelzellen sind spezialisiert auf …", "… Kontraktionen (sich zusammenziehen)."],
 ["Rote Blutzellen sind spezialisiert auf …", "… den Transport von Sauerstoff."],
 ["Gewebe", "Spezialisierte Zellen, die zu Zellverbänden zusammengeschlossen sind.<br>Beispiel: Drüsengewebe der Magenschleimhaut."],
 ["Organ", "Mehrere Gewebe erfüllen gemeinsam eine oder mehrere Aufgaben.<br>Beispiel: der Magen."],
 ["Organsystem", "Mehrere Organe arbeiten zusammen.<br>Beispiel: das Verdauungssystem."],
 ["Organismus", "Alle Organe und Organsysteme zusammen.<br>Beispiel: der Mensch."],
 ["Die Stufen von klein nach groß", "Zelle → Gewebe → Organ → Organsystem → Organismus"],
 ["Nenne Organe, die zum Verdauungssystem gehören (Beispiele aus dem Buch).", "Zum Beispiel Mund mit Zähnen und Speicheldrüsen, Magen, Dünndarm und Dickdarm."],
 ["Was ist an der Zeichnung der roten Blutzelle besonders?", "Es ist kein Zellkern eingezeichnet. Rote Blutzellen des Menschen haben keinen Zellkern."],
],
"t3": [
 ["Beobachtung", "Steht meist am Anfang. Etwas, das man mit dem Vorwissen nicht erklären kann oder das sonderbar erscheint."],
 ["Problemfrage", "Die Frage, die untersucht werden soll."],
 ["Hypothese", "Eine begründete Vermutung."],
 ["Experiment", "Eine besonders wichtige Untersuchungsmethode. Damit überprüft man eine Hypothese."],
 ["Erkenntnisgewinn", "Entsteht, wenn man die Lösung der Problemfrage verallgemeinert. Er kann der Startpunkt für neue Fragen sein."],
 ["Die Schritte der Reihe nach", "Beobachtung → Problemfrage → Hypothese → Untersuchung (z. B. Experiment) → Ergebnis → Schlussfolgerung → Erkenntnisgewinn"],
 ["Van Helmont: Problemfrage", "Woher erhalten die Pflanzen die Stoffe für das Wachstum?"],
 ["Van Helmont: Hypothese", "Pflanzen brauchen für das Wachstum Stoffe aus dem Erdboden und Wasser, weil sie mit den Wurzeln im Boden verankert sind."],
 ["Van Helmont: Wie lief das Experiment?", "Eine junge Weide (2,3 kg) wurde 1635 in einen Kübel mit 90,7 kg getrockneter Erde gepflanzt. Die Erde wurde mit einer durchlöcherten Metallplatte abgedeckt. Die Weide stand im Freien und wurde mit Regenwasser gegossen. Nach fünf Jahren wurde gewogen."],
 ["Van Helmont: Ergebnis", "Die Weide wog 76,7 kg, also 74,4 kg mehr. Die Erde war nur 57 g leichter."],
 ["Van Helmont: Schlussfolgerung", "Der Massezuwachs kommt vor allem von der Aufnahme von Wasser, nur ein kleiner Teil aus dem Boden."],
 ["Van Helmont: Erkenntnis", "Die Pflanze muss das Gießwasser in pflanzliche Substanz umgewandelt haben."],
 ["Warum hatte van Helmont nur zum Teil recht?", "Getrocknet wäre die Weide immer noch etwa 13 kg schwerer gewesen als am Anfang. Diese 13 kg sind also kein Wasser, das nur in der Pflanze gespeichert ist. Neue Hypothese anderer Forscher: Die Pflanze nimmt auch Stoffe aus der Luft auf."],
],
"t4": [
 ["Kutikula", "Wasser abweisende Wachsschicht. Schützt das Blatt vor Schmutz und vor übermäßigem Wasserverlust durch Verdunstung."],
 ["Epidermis", "Die Blatthaut oben und unten: dicht aneinanderliegende Zellen ohne Chloroplasten (Ausnahme: die Schließzellen). Schützt vor Verletzungen und lässt das Licht gut durch."],
 ["Palisadengewebe", "Unter der oberen Epidermis. Lang gestreckte Zellen, regelmäßig angeordnet wie ein Palisadenzaun. Besonders viele Chloroplasten."],
 ["Schwammgewebe", "Unter dem Palisadengewebe. Unregelmäßig geformte Zellen mit Chloroplasten, dazwischen große luftgefüllte Hohlräume."],
 ["Interzellularen", "Große, mit Luft gefüllte Hohlräume zwischen den Zellen des Schwammgewebes. Sie stehen mit den Spaltöffnungen in Verbindung."],
 ["Spaltöffnung", "Vor allem in der unteren Epidermis. Wird von zwei bohnenförmigen Schließzellen gebildet und kann sich öffnen und schließen. So ist ein kontrollierter Gasaustausch möglich."],
 ["Schließzellen", "Zwei bohnenförmige Zellen, die eine Spaltöffnung bilden. Anders als die anderen Epidermiszellen haben sie Chloroplasten."],
 ["Leitbündel", "Bilden die Blattadern. Darin werden zum Beispiel Wasser, Mineralsalze und Glucose transportiert."],
 ["Schichten von oben nach unten", "Kutikula → obere Epidermis → Palisadengewebe → Schwammgewebe → untere Epidermis → Kutikula"],
 ["Ist das Blatt eine Zelle, ein Gewebe oder ein Organ?", "Ein Organ. Es ist aus mehreren verschiedenen Geweben aufgebaut."],
],
}

# ---------------------------------------------------------------- Quiz (erste Antwort ist richtig)
QUIZ = {
"t1": [
 ["Wie berechnet man die Gesamtvergrößerung?", ["Vergrößerung des Okulars mal Vergrößerung des Objektivs", "Vergrößerung des Okulars plus Vergrößerung des Objektivs", "Es zählt nur die Vergrößerung des Objektivs.", "Vergrößerung des Objektivs geteilt durch Vergrößerung des Okulars"], "Okular mal Objektiv. Zum Beispiel 10 · 40 = 400."],
 ["Okular 10-fach, Objektiv 40-fach. Wie stark ist die Gesamtvergrößerung?", ["400-fach", "50-fach", "40-fach", "4000-fach"], "10 · 40 = 400. Nicht plus rechnen!"],
 ["Okular 10-fach, Objektiv 10-fach. Wie stark ist die Gesamtvergrößerung?", ["100-fach", "20-fach", "10-fach", "1000-fach"], "10 · 10 = 100."],
 ["Womit wechselt man die Objektive?", ["mit dem Objektivrevolver", "mit dem Grobtrieb", "mit der Blende", "mit dem Kondensor"], "Durch Drehen des Objektivrevolvers werden die Objektive gewechselt."],
 ["Wozu dienen Grob- und Feintrieb?", ["Sie stellen das Bild scharf, indem sie den Abstand zwischen Objekttisch und Objektiv verändern.", "Sie machen das Licht heller oder dunkler.", "Sie wechseln die Objektive.", "Sie halten das Präparat fest."], "Mit den beiden Drehknöpfen stellt man die Bildschärfe ein."],
 ["Was macht der Kondensor?", ["Er bündelt die Strahlen, die von der Lichtquelle ausgehen.", "Er vergrößert das Bild.", "Er wechselt die Objektive.", "Er hält den Tubus fest."], "Der Kondensor sitzt unter dem Objekttisch und bündelt das Licht."],
 ["Was macht die Blende?", ["Sie sorgt für eine gleichmäßige Beleuchtung des Präparats.", "Sie stellt das Bild scharf.", "Sie vergrößert das Bild.", "Sie erzeugt das Licht."], "Die Blende sorgt für gleichmäßige Beleuchtung. Das Licht kommt aus der Lichtquelle im Fuß."],
 ["Wo werden die Präparate abgelegt?", ["auf dem Objekttisch", "im Tubus", "auf dem Okular", "im Fuß"], "Der Objekttisch ist außerdem in der Höhe verstellbar."],
 ["Was ist der Tubus?", ["eine Röhre, die das Okular enthält", "eine Linse direkt über dem Präparat", "ein Drehknopf zum Scharfstellen", "die Lampe im Fuß"], "Oben im Tubus steckt das Okular."],
 ["Wie trägst du ein Mikroskop richtig?", ["Eine Hand unter das Mikroskop, die andere an den Trägerarm.", "Mit einer Hand am Tubus.", "Mit beiden Händen am Objekttisch.", "Mit einer Hand am Okular."], "So steht es im Buch auf S. 18."],
 ["Wo befindet sich die Lichtquelle?", ["im Fuß des Mikroskops", "im Okular", "am Objektivrevolver", "im Tubus"], "Sie hat meist einen Helligkeitsregler."],
 ["In welches Teil schaust du hinein?", ["ins Okular", "ins Objektiv", "in den Kondensor", "in die Blende"], "Okular kommt von oculus = Auge."],
],
"t2": [
 ["Welche Reihenfolge stimmt (von klein nach groß)?", ["Zelle → Gewebe → Organ → Organsystem → Organismus", "Zelle → Organ → Gewebe → Organismus → Organsystem", "Gewebe → Zelle → Organ → Organsystem → Organismus", "Organ → Gewebe → Zelle → Organsystem → Organismus"], "Zellen bilden Gewebe, Gewebe bilden Organe, Organe bilden Organsysteme, alles zusammen ist der Organismus."],
 ["Was ist ein Gewebe?", ["spezialisierte Zellen, die zu Zellverbänden zusammengeschlossen sind", "mehrere Organe, die zusammenarbeiten", "ein ganzes Lebewesen", "ein einzelner Zellkern"], "Beispiel: das Drüsengewebe der Magenschleimhaut."],
 ["Was ist ein Organ?", ["Mehrere Gewebe erfüllen gemeinsam eine oder mehrere Aufgaben.", "Eine einzelne Zelle mit Zellkern.", "Alle Organsysteme zusammen.", "Ein Verband aus nur einer Sorte Zellen."], "Beispiel: der Magen. Ein Verband aus spezialisierten Zellen ist ein Gewebe."],
 ["Der Magen ist ein …", ["Organ", "Gewebe", "Organsystem", "Organismus"], "Der Magen besteht aus verschiedenen Geweben, die gemeinsam die Aufgabe der Verdauung erfüllen."],
 ["Das Verdauungssystem ist ein …", ["Organsystem", "Organ", "Gewebe", "Organismus"], "Mehrere Organe arbeiten zusammen, zum Beispiel Mund, Magen, Dünndarm und Dickdarm."],
 ["Auf welcher Stufe steht eine Drüsenzelle der Magenschleimhaut?", ["Zelle", "Gewebe", "Organ", "Organismus"], "Viele Drüsenzellen zusammen bilden das Drüsengewebe."],
 ["Worauf sind Muskelzellen spezialisiert?", ["auf Kontraktionen (sich zusammenziehen)", "auf den Transport von Sauerstoff", "auf die Weiterleitung von Informationen", "auf die Verdauung"], "Muskeln ziehen sich zusammen."],
 ["Worauf sind rote Blutzellen spezialisiert?", ["auf den Transport von Sauerstoff", "auf Kontraktionen", "auf die Weiterleitung von Informationen", "auf die Verdauung"], "Rote Blutzellen transportieren Sauerstoff."],
 ["Worauf sind Nervenzellen spezialisiert?", ["auf die Weiterleitung von Informationen", "auf den Transport von Sauerstoff", "auf Kontraktionen", "auf die Verdauung"], "Nervenzellen leiten Informationen weiter."],
 ["Welches Organ gehört NICHT zum Verdauungssystem?", ["Herz", "Magen", "Dünndarm", "Mund mit Zähnen"], "Zum Verdauungssystem gehören zum Beispiel Mund, Magen, Dünndarm und Dickdarm. Das Herz gehört zum Blutkreislauf."],
 ["Was bedeutet Arbeitsteilung bei Zellen?", ["Jeder Zelltyp erfüllt eine bestimmte Aufgabe.", "Alle Zellen machen genau dasselbe.", "Eine Zelle erledigt alle Aufgaben allein.", "Zellen arbeiten nur nachts."], "Deshalb spricht man von spezialisierten Zellen."],
 ["Was ist der Mensch?", ["ein Organismus", "ein Organsystem", "ein Organ", "ein Gewebe"], "Alle Organe und Organsysteme ergänzen sich zum Organismus."],
],
"t3": [
 ["Was steht meist am Anfang der Erkenntnisgewinnung?", ["eine Beobachtung", "ein Experiment", "der Erkenntnisgewinn", "eine Schlussfolgerung"], "Man beobachtet etwas, das man nicht erklären kann oder das sonderbar erscheint."],
 ["Was ist eine Hypothese?", ["eine begründete Vermutung", "ein sicheres Ergebnis", "eine Beobachtung", "ein Versuchsaufbau"], "So steht es im Buch: Hypothesen sind begründete Vermutungen."],
 ["Welche Untersuchungsmethode ist in den Naturwissenschaften besonders wichtig?", ["das Experiment", "die Hypothese", "die Problemfrage", "der Erkenntnisgewinn"], "Mit dem Experiment überprüft man die Hypothese."],
 ["Welche Reihenfolge stimmt?", ["Beobachtung → Problemfrage → Hypothese → Untersuchung", "Hypothese → Beobachtung → Untersuchung → Problemfrage", "Untersuchung → Hypothese → Problemfrage → Beobachtung", "Problemfrage → Untersuchung → Beobachtung → Hypothese"], "Danach kommen Ergebnis, Schlussfolgerung und Erkenntnisgewinn."],
 ["Was war van Helmonts Problemfrage?", ["Woher erhalten die Pflanzen die Stoffe für das Wachstum?", "Warum sind Blätter grün?", "Wie schnell wächst eine Weide?", "Wie viel Erde passt in einen Kübel?"], "Er sah, dass Pflanzen wachsen und schwerer werden, und fragte, woher die Stoffe dafür kommen."],
 ["Was war van Helmonts Hypothese?", ["Pflanzen brauchen Stoffe aus dem Erdboden und Wasser.", "Pflanzen brauchen nur Licht.", "Pflanzen nehmen Stoffe aus der Luft auf.", "Pflanzen wachsen ganz ohne Stoffe."], "Er begründete das mit den Wurzeln im Boden. Die Idee mit der Luft hatten erst spätere Forscher."],
 ["Um wie viel war die Weide nach fünf Jahren schwerer?", ["74,4 kg", "76,7 kg", "2,3 kg", "57 g"], "76,7 kg − 2,3 kg = 74,4 kg. 76,7 kg war ihr Gewicht am Ende."],
 ["Um wie viel war die Erde leichter geworden?", ["um 57 g", "um 57 kg", "um 74,4 kg", "gar nicht"], "Nur 57 Gramm, also fast nichts."],
 ["Welche Schlussfolgerung zog van Helmont aus seinem Ergebnis?", ["Der Massezuwachs kommt vor allem von der Aufnahme von Wasser.", "Der Massezuwachs kommt vor allem aus dem Boden.", "Die Pflanze nimmt Stoffe aus der Luft auf.", "Die Metallplatte hat die Pflanze schwerer gemacht."], "Weil die Erde nur 57 g leichter war, kann kaum etwas aus dem Boden kommen. Er dachte: Die Masse kommt vor allem vom Wasser."],
 ["Welche Erkenntnis gewann van Helmont daraus?", ["Die Pflanze muss das Gießwasser in pflanzliche Substanz umgewandelt haben.", "Die Pflanze braucht gar kein Wasser.", "Die Erde wird von der Pflanze vollständig aufgebraucht.", "Die Pflanze nimmt Stoffe aus der Luft auf."], "So steht es im Buch. Die Idee mit der Luft hatten erst spätere Forscher."],
 ["Was hätte van Helmont gemerkt, wenn er die Weide am Ende vollständig getrocknet hätte?", ["Sie wäre noch etwa 13 kg schwerer gewesen als am Anfang.", "Sie wäre leichter gewesen als am Anfang.", "Sie hätte genau 2,3 kg gewogen, so viel wie am Anfang.", "Sie hätte immer noch 76,7 kg gewogen."], "Die getrocknete Weide wäre etwa 13 kg schwerer gewesen. Deshalb hatte van Helmont nur zum Teil recht."],
 ["Welche neue Hypothese stellten die anderen Forscher auf?", ["Die Pflanze nimmt für ihr Wachstum auch Stoffe aus der Luft auf.", "Die Pflanze braucht kein Wasser.", "Die Pflanze nimmt alle Stoffe aus dem Boden auf.", "Die Pflanze wächst nur im Dunkeln."], "So wird ein Erkenntnisgewinn zum Startpunkt für eine neue Frage."],
 ["Was kann ein Erkenntnisgewinn sein?", ["der Ausgangspunkt für neue Fragestellungen", "das Ende jeder Forschung", "eine unbegründete Vermutung", "eine Beobachtung ohne Frage"], "Aus einer Erkenntnis entstehen oft neue Fragen, wie bei van Helmont."],
],
"t4": [
 ["Warum perlen Regentropfen vom Laubblatt ab?", ["wegen der Wasser abweisenden Wachsschicht, der Kutikula", "wegen der Spaltöffnungen", "weil das Blatt keine Zellen hat", "wegen der Leitbündel"], "Die Kutikula wird von der Blatthaut nach außen abgegeben."],
 ["Wovor schützt die Kutikula das Blatt?", ["vor Schmutz und vor übermäßigem Wasserverlust durch Verdunstung", "vor zu viel Licht und vor dem Austrocknen der Wurzeln", "vor Kohlenstoffdioxid und vor zu viel Sauerstoff", "vor Wärme und vor dem Eindringen von Licht"], "So steht es im Buch auf S. 24."],
 ["Wo befinden sich laut Buch viele Spaltöffnungen?", ["in der unteren Epidermis", "in der oberen Epidermis", "im Palisadengewebe", "in den Leitbündeln"], "In der unteren Epidermis befinden sich viele Spaltöffnungen."],
 ["Woraus besteht eine Spaltöffnung?", ["aus zwei bohnenförmigen Schließzellen", "aus einer runden Palisadenzelle", "aus Wachs", "aus einem Leitbündel"], "Zwischen den beiden Schließzellen ist der Spalt."],
 ["Wozu dienen die Spaltöffnungen?", ["für einen kontrollierten Gasaustausch mit der Umgebung", "zum Transport von Glucose", "zum Schutz vor Verletzungen", "zum Abweisen von Wasser"], "Sie können sich öffnen oder schließen."],
 ["Welches Gewebe hat besonders viele Chloroplasten?", ["das Palisadengewebe", "die Epidermis", "die Kutikula", "die Leitbündel"], "Deshalb ist es kräftig grün."],
 ["Warum ist die Epidermis gut lichtdurchlässig?", ["Ihren Zellen fehlen die Chloroplasten.", "Sie besteht nur aus Wachs.", "Sie hat große Lufträume.", "Sie ist besonders dick."], "So kommt das Licht gut zum Palisadengewebe darunter."],
 ["Was sind Interzellularen?", ["große, mit Luft gefüllte Hohlräume zwischen den Zellen des Schwammgewebes", "Zellen ohne Chloroplasten in der oberen und unteren Blatthaut", "die Blattadern, in denen Wasser und Glucose transportiert werden", "die Wachsschicht, die das Blatt vor Verdunstung schützt"], "Sie stehen mit den Spaltöffnungen in Verbindung."],
 ["Was wird in den Leitbündeln transportiert?", ["zum Beispiel Wasser, Mineralsalze und Glucose", "zum Beispiel Luft, Licht und Chlorophyll", "zum Beispiel Chloroplasten und Zellkerne", "nur Sauerstoff aus den Spaltöffnungen"], "Die Leitbündel bilden die Blattadern."],
 ["Welche Zellen der Epidermis haben Chloroplasten?", ["die Schließzellen", "alle Epidermiszellen", "nur die Zellen der oberen Epidermis", "keine einzige"], "Die anderen Epidermiszellen haben keine Chloroplasten."],
 ["Welche Reihenfolge von oben nach unten stimmt?", ["Kutikula – obere Epidermis – Palisadengewebe – Schwammgewebe – untere Epidermis – Kutikula", "Kutikula – Palisadengewebe – obere Epidermis – Schwammgewebe – untere Epidermis – Kutikula", "Kutikula – obere Epidermis – Schwammgewebe – Palisadengewebe – untere Epidermis – Kutikula", "obere Epidermis – Kutikula – Palisadengewebe – Schwammgewebe – Kutikula – untere Epidermis"], "Das Palisadengewebe liegt direkt unter der oberen Epidermis, darunter das Schwammgewebe."],
 ["Warum heißt das Palisadengewebe so?", ["Die lang gestreckten Zellen stehen regelmäßig nebeneinander wie ein Palisadenzaun.", "Es schützt das Blatt wie eine Mauer vor Verletzungen.", "Es liegt ganz außen am Blatt.", "Es ist hart wie Holz."], "Ein Palisadenzaun besteht aus Pfählen, die dicht nebeneinanderstehen."],
 ["Ist das Laubblatt eine Zelle, ein Gewebe oder ein Organ?", ["ein Organ", "ein Gewebe", "eine Zelle", "ein Organismus"], "Es ist aus mehreren verschiedenen Geweben aufgebaut."],
],
}

# ---------------------------------------------------------------- Probe-Klausur
PROBE = f"""
<div class="box">
<h2>Probe-Klausur Biologie</h2>
<div class="task"><h3>1. Beschrifte das Mikroskop.</h3>
{mikroskop()}
<div class="lines"></div><div class="lines"></div><div class="lines"></div>
<div class="sol">1 Okular · 2 Tubus · 3 Objektivrevolver · 4 Objektiv · 5 Objekttisch · 6 Kondensor · 7 Blende · 8 Lichtquelle · 9 Trägerarm · 10 Grob- und Feintrieb</div></div>
<div class="task"><h3>2. Nenne die Aufgabe von Kondensor, Blende und Objektivrevolver.</h3>
<div class="lines"></div><div class="lines"></div><div class="lines"></div>
<div class="sol">Kondensor: bündelt die Strahlen, die von der Lichtquelle ausgehen.<br>Blende: sorgt für eine gleichmäßige Beleuchtung des Präparats.<br>Objektivrevolver: Durch Drehen werden die Objektive gewechselt.</div></div>
<div class="task"><h3>3. Vergrößerung</h3>
<p>a) Okular 10-fach, Objektiv 40-fach. Berechne die Gesamtvergrößerung.<br>b) Okular 15-fach, Objektiv 10-fach. Berechne die Gesamtvergrößerung.<br>c) Das Okular vergrößert 10-fach. Du willst 100-fach vergrößern. Welches Objektiv brauchst du?</p>
<div class="lines"></div><div class="lines"></div><div class="lines"></div>
<div class="sol">a) 10 · 40 = 400-fach<br>b) 15 · 10 = 150-fach<br>c) Das 10-fach-Objektiv, denn 10 · 10 = 100.</div></div>
<div class="task"><h3>4. Wie trägst du ein Mikroskop richtig?</h3>
<div class="lines"></div>
<div class="sol">Eine Hand greift unter das Mikroskop, die andere Hand an den Trägerarm.</div></div>
<div class="task"><h3>5. Zelle, Gewebe, Organ</h3>
<p>a) Ordne von klein nach groß: Organ, Organismus, Zelle, Organsystem, Gewebe.<br>b) Ordne jedem Begriff aus a) das Beispiel aus dem Buch zu (Magen).<br>c) Erkläre die Begriffe <i>Gewebe</i> und <i>Organ</i>.</p>
<div class="lines"></div><div class="lines"></div><div class="lines"></div><div class="lines"></div>
<div class="sol">a) Zelle → Gewebe → Organ → Organsystem → Organismus<br>b) Drüsenzelle → Drüsengewebe der Magenschleimhaut → Magen → Verdauungssystem → Mensch<br>c) Gewebe: Spezialisierte Zellen sind zu Zellverbänden zusammengeschlossen. Organ: Mehrere Gewebe erfüllen gemeinsam eine oder mehrere Aufgaben.</div></div>
<div class="task"><h3>6. Nenne drei spezialisierte Zellen des Menschen und ihre Aufgabe.</h3>
<div class="lines"></div><div class="lines"></div><div class="lines"></div>
<div class="sol">Nervenzellen: Weiterleitung von Informationen. Muskelzellen: Kontraktionen (sich zusammenziehen). Rote Blutzellen: Transport von Sauerstoff.</div></div>
<div class="task"><h3>7. Nenne die Schritte der naturwissenschaftlichen Erkenntnisgewinnung in der richtigen Reihenfolge. Erkläre, was eine Hypothese ist.</h3>
<div class="lines"></div><div class="lines"></div>
<div class="sol">Beobachtung → Problemfrage → Hypothese → Untersuchung (z. B. Experiment) → Ergebnis → Schlussfolgerung → Erkenntnisgewinn. Eine Hypothese ist eine begründete Vermutung.</div></div>
<div class="task"><h3>8. Das Experiment von van Helmont</h3>
<p>1635 pflanzte van Helmont eine junge Weide mit 2,3 kg in einen Kübel mit 90,7 kg getrockneter Erde. Nach fünf Jahren wog die Weide 76,7 kg, die Erde hatte um 57 g abgenommen.</p>
<p>a) Nenne seine Problemfrage und seine Hypothese.<br>b) Berechne, um wie viel kg die Weide schwerer geworden ist.<br>c) Welche Schlussfolgerung zog van Helmont, und welche Erkenntnis gewann er daraus?<br>d) Erkläre, warum van Helmont nur zum Teil recht hatte. Welche neue Hypothese stellten andere Forscher auf?</p>
<div class="lines"></div><div class="lines"></div><div class="lines"></div><div class="lines"></div><div class="lines"></div>
<div class="sol">a) Problemfrage: Woher erhalten die Pflanzen die Stoffe für das Wachstum? Hypothese: Pflanzen brauchen für das Wachstum Stoffe aus dem Erdboden und Wasser, weil sie mit den Wurzeln im Boden verankert sind.<br>b) 76,7 kg − 2,3 kg = 74,4 kg<br>c) Schlussfolgerung: Der Massezuwachs kommt vor allem von der Aufnahme von Wasser und nur zu einem kleinen Teil aus dem Boden. Erkenntnis: Die Pflanze muss das Gießwasser in pflanzliche Substanz umgewandelt haben.<br>d) Hätte er die Weide vollständig getrocknet, wäre sie noch etwa 13 kg schwerer gewesen als am Anfang. Neue Hypothese: Die Pflanze nimmt für ihr Wachstum auch Stoffe aus der Luft auf.</div></div>
<div class="task"><h3>9. Beschrifte den Blattquerschnitt.</h3>
{blatt()}
<div class="lines"></div><div class="lines"></div><div class="lines"></div>
<div class="sol">1 Kutikula · 2 obere Epidermis · 3 Palisadengewebe · 4 Schwammgewebe · 5 untere Epidermis · 6 Chloroplast · 7 Leitbündel · 8 Interzellulare (Luftraum) · 9 Schließzelle · 10 Spaltöffnung</div></div>
<div class="task"><h3>10. Bau und Aufgabe</h3>
<p>a) Beschreibe Bau und Aufgabe einer Spaltöffnung.<br>b) Die Zellen der Epidermis haben keine Chloroplasten (außer den Schließzellen). Welche Folge hat das?<br>c) Warum ist das Palisadengewebe kräftig grün?</p>
<div class="lines"></div><div class="lines"></div><div class="lines"></div><div class="lines"></div>
<div class="sol">a) Eine Spaltöffnung wird von zwei bohnenförmigen Schließzellen gebildet. Sie kann sich öffnen oder schließen. So findet ein kontrollierter Gasaustausch mit der Umgebung statt. Viele Spaltöffnungen liegen in der unteren Epidermis.<br>b) Die Epidermis ist gut lichtdurchlässig.<br>c) Seine Zellen enthalten besonders viele Chloroplasten.</div></div>
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
    items += [(s["file"], s["nav"], s["id"]) for s in STEPS]
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

def box(mid, title):
    return f'<div class="box"><h3>{title}</h3><div data-match="{mid}"></div></div>\n'

UEBEN = {
 "t1": ("Beschriften und Rechnen", "Beschrifte das Mikroskop und ordne die Aufgaben zu. Dann rechnest du Vergrößerungen.",
        box("m-mikro", "Beschrifte das Mikroskop") + box("m-mikro-auf", "Welches Teil macht was?")
        + '<h3>Gesamtvergrößerung rechnen</h3><p class="meta">Okular mal Objektiv. Es kommen immer neue Aufgaben.</p><div data-calc></div>\n'),
 "t2": ("Ordnen und Zuordnen", "Zieh die Wörter an die richtige Stelle.",
        box("m-stufen", "Von klein nach groß") + box("m-magen", "Das Beispiel Magen") + box("m-spez", "Spezialisierte Zellen")),
 "t3": ("Ordnen und Zuordnen", "Zieh die Wörter an die richtige Stelle.",
        box("m-schritte", "Die Schritte der Reihe nach") + box("m-helmont", "Die Schritte bei van Helmont")),
 "t4": ("Beschriften", "Beschrifte den Blattquerschnitt und ordne die Aufgaben zu.",
        box("m-blatt", "Beschrifte den Blattquerschnitt") + box("m-blatt-auf", "Welches Teil macht was?")),
}

def write(name, text):
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(text)

def main():
    os.makedirs(OUT, exist_ok=True)
    b = f'<h1>Biologie</h1>\n<p class="sub">{KLAUSUR}</p>\n'
    b += '<div class="box merke"><h3>So lernst du</h3><p>Mach die Themen <b>der Reihe nach</b>. Jedes Thema ist eine eigene Seite: erst lesen, dann üben (Wörter mit dem Finger ziehen), dann Karten, dann Quiz. Unten tippst du auf <b>„Fertig ✓“</b>.</p><p class="meta" id="st-left"></p></div>\n'
    for i, s in enumerate(STEPS):
        b += f'<a class="step" data-step="{s["id"]}" href="{s["file"]}"><span class="num">{i+1}</span><span class="stxt"><b>{s["title"]}</b><span class="meta"> · {s["dur"]}</span><br><span class="meta">{s["desc"]}</span></span></a>\n'
    b += '<div class="box" id="st-all" hidden><h3>🎉 Super, alles geschafft!</h3><p>Du bist gut vorbereitet. Am Abend vor der Klausur: nochmal das große Quiz und beide Zeichnungen beschriften.</p></div>\n'
    b += '<p><button class="btn ghost small" id="st-reset">Alle Haken löschen</button></p>'
    write("index.html", page("start", "Start", b))
    for i, s in enumerate(TOPICS):
        t = s["id"]
        b = f'<p class="crumb">Thema {i+1} von {len(TOPICS)}</p>\n<h1>{s["title"]}</h1>\n'
        b += part(1, "Lesen", "Lies alles einmal in Ruhe durch.") + LESEN[t]
        name, hint, body = UEBEN[t]
        b += part(2, name, hint) + body
        b += part(3, "Karten", "Überleg dir die Antwort. Dann tippe auf die Karte.") + '<div id="cards"></div>\n'
        b += part(4, "Quiz", "Tippe auf die richtige Antwort.") + '<div id="quiz"></div>\n'
        b += nextbtn(i)
        write(s["file"], page(t, s["title"], b))
    b = '<h1>Großes Quiz</h1>\n<p class="hint">Alle Fragen aus allen Themen, bunt gemischt. Ziel: höchstens 5 Fehler.</p>\n<div id="quiz"></div>\n' + nextbtn(len(TOPICS))
    write("gemischt.html", page("gem", "Großes Quiz", b))
    tools = '<div class="row noprint"><button class="btn ghost" data-sol>Lösungen zeigen</button><button class="btn" data-print="0">Drucken</button><button class="btn ghost" data-print="1">Mit Lösungen drucken</button></div>\n'
    b = '<p class="hint noprint">So geht\'s: Drucke die Klausur aus oder schreib die Antworten auf einen Zettel. Nimm dir 30 Minuten. Erst danach tippst du auf „Lösungen zeigen“ und vergleichst.</p>\n' + tools + PROBE + nextbtn(len(STEPS) - 1)
    write("probe.html", page("probe", "Probe-Klausur", b))
    js = open(os.path.join(ROOT, "_build", "bio.src.js"), encoding="utf-8").read()
    data = dict(cards=CARDS, quiz=QUIZ, match=MATCH, steps=[s["id"] for s in STEPS], topics=[s["id"] for s in TOPICS])
    write("app.js", js.replace("__DATA__", json.dumps(data, ensure_ascii=False)))
    css = open(os.path.join(ROOT, "_build", "app.css"), encoding="utf-8").read() + open(os.path.join(ROOT, "_build", "bio-extra.css"), encoding="utf-8").read()
    write("app.css", css)
    print("gebaut:", sorted(os.listdir(OUT)))

if __name__ == "__main__":
    main()
