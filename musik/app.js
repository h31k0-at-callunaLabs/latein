/* Notenzeichen: Bravura (SIL Open Font License, siehe _build/BRAVURA-LICENSE.txt) */
/* ===== Musik: Notenlogik (ohne Browser, wird in Node getestet) ===== */
const STEPS="cdefgah",PC=[0,2,4,5,7,9,11];
const INT=["Prime","Sekunde","Terz","Quarte","Quinte","Sexte","Septime","Oktave"];
/* Notenname -> Note. Großbuchstabe = große Oktave, klein = kleine Oktave, ' = eingestrichen usw. */
function N(s){
  if(typeof s!=="string")return s;
  const m=/^([a-hA-H])(is|es|s)?('*)$/.exec(s.trim());if(!m)throw new Error("Note? "+s);
  const L=m[1],up=L!==L.toLowerCase(),l=L.toLowerCase(),suf=m[2]||"";let step,alt=0;
  if(l==="b"){if(suf)throw new Error("Note? "+s);step=6;alt=-1}
  else{step=STEPS.indexOf(l);
    if(suf==="is")alt=1;
    else if(suf==="s"){if(l!=="a"&&l!=="e")throw new Error("Note? "+s);alt=-1}
    else if(suf==="es"){if(l==="a"||l==="e"||l==="h")throw new Error("Note? "+s);alt=-1}}
  if(up&&m[3])throw new Error("Note? "+s);
  return mk(step,alt,up?2:3+m[3].length);
}
function mk(step,alt,oct){return{step,alt,oct,dia:oct*7+step,midi:12*(oct+1)+PC[step]+alt}}
function fromDia(dia,alt){return mk(((dia%7)+7)%7,alt||0,Math.floor(dia/7))}
function natMidi(dia){return fromDia(dia,0).midi}
function spell(dia,midi){const a=midi-natMidi(dia);return Math.abs(a)<=1?fromDia(dia,a):null}
function letter(n){const l=STEPS[n.step];if(n.alt===1)return l+"is";if(n.alt===-1)return l==="h"?"b":(l==="e"||l==="a")?l+"s":l+"es";return l}
function name(n){n=N(n);const s=letter(n);if(n.oct<=2)return s[0].toUpperCase()+s.slice(1);return s+"'".repeat(n.oct-3)}
function oktave(n){n=N(n);return["Kontraoktave","Kontraoktave","große Oktave","kleine Oktave","eingestrichene Oktave","zweigestrichene Oktave","dreigestrichene Oktave"][n.oct]}
/* Intervall-Grobbestimmung: Linien und Zwischenräume zählen (beide Noten mitzählen) */
function intNum(a,b){return Math.abs(N(b).dia-N(a).dia)+1}
function intName(a,b){const k=intNum(a,b);return k>=1&&k<=8?INT[k-1]:null}
function semis(a,b){return Math.abs(N(b).midi-N(a).midi)}
/* Terz fein: große Terz = 4 Halbtonschritte, kleine Terz = 3 */
function terz(a,b){if(intNum(a,b)!==3)return null;const h=semis(a,b);return h===4?"große Terz":h===3?"kleine Terz":null}
/* Dreiklang in Grundstellung über einem Grundton */
function triad(root,dur){const r=N(root);const t=spell(r.dia+2,r.midi+(dur?4:3)),q=spell(r.dia+4,r.midi+7);if(!t||!q)throw new Error("Dreiklang? "+root);return[r,t,q]}
function chordName(root,dur){const l=letter(N(root));return dur?l[0].toUpperCase()+l.slice(1)+"-Dur":l+"-Moll"}
function analyze(notes){ // Terzschichtung prüfen und bestimmen
  const n=notes.map(N).slice().sort((a,b)=>a.dia-b.dia);
  if(n.length!==3||n[1].dia-n[0].dia!==2||n[2].dia-n[1].dia!==2)return null;
  const lo=n[1].midi-n[0].midi,hi=n[2].midi-n[1].midi;
  const q=lo===4&&hi===3?"Dur":lo===3&&hi===4?"Moll":null;
  const T=h=>h===4?"große Terz":h===3?"kleine Terz":"?";
  return{root:n[0],third:n[1],fifth:n[2],lo:T(lo),hi:T(hi),q,name:q?chordName(n[0],q==="Dur"):null};
}
/* Akkordsymbole: C = C-Dur, Dm = d-Moll */
function chord(sym){const m=/^([A-H])(is|es|s)?(m?)$/.exec(sym);if(!m)throw new Error("Akkord? "+sym);
  const root=N(m[1].toLowerCase()+(m[2]||"")+"'"),dur=!m[3];
  return{sym,dur,tones:triad(root,dur),name:chordName(root,dur)}}
/* Lagen für die rechte Hand: drei Töne eng übereinander, tiefster Ton zwischen g und fis' */
function voicings(sym){
  const T=chord(sym).tones,out=[];
  for(let inv=0;inv<3;inv++){
    const order=[T[inv],T[(inv+1)%3],T[(inv+2)%3]];
    let o=3,low=null;
    for(;o<=4;o++){const c=mk(order[0].step,order[0].alt,o);if(c.midi>=55&&c.midi<=66){low=c;break}}
    const v=[low];
    for(let i=1;i<3;i++){const p=v[i-1],t=order[i];let dia=p.dia+(((t.step-p.step)%7+7)%7||7);v.push(fromDia(dia,t.alt))}
    out.push({inv,notes:v});
  }
  return out;
}
function moveCost(a,b){let s=0,mx=0,keep=0;for(let i=0;i<3;i++){const d=Math.abs(a[i].midi-b[i].midi);s+=d;mx=Math.max(mx,d)}
  b.forEach(x=>{if(a.some(y=>y.midi===x.midi))keep++});return{sum:s,max:mx,keep}}
/* Beste Lage = kleinste Gesamtbewegung (wenig Sprünge, gemeinsame Töne bleiben liegen) */
function bestNext(prev,sym){
  const c=voicings(sym).map(v=>Object.assign(v,moveCost(prev,v.notes)));
  const min=Math.min(...c.map(x=>x.sum));c.forEach(x=>x.best=x.sum===min);return c}
function bassRoot(sym){const r=chord(sym).tones[0];for(let o=1;o<=3;o++){const n=mk(r.step,r.alt,o);if(n.midi>=41&&n.midi<=52)return n}}
function planVoicing(syms){ // erste Lage: Grundstellung, danach jeweils die beste
  const res=[];let prev=null;
  syms.forEach(s=>{if(!prev){prev=voicings(s)[0].notes;res.push({sym:s,notes:prev,ties:1})}
    else{const c=bestNext(prev,s),b=c.filter(x=>x.best);b.sort((x,y)=>x.max-y.max);prev=b[0].notes;res.push({sym:s,notes:prev,ties:b.length,cands:c})}});
  return res;
}
/* Lage der Note im Notensystem beschreiben */
const BOTTOM={v:30,b:18}; // e' bzw. G auf der untersten Linie
function where(clef,n){n=N(n);const o=n.dia-BOTTOM[clef];
  if(o>=0&&o<=8)return o%2===0?`auf der ${o/2+1}. Linie von unten`:`im ${(o+1)/2}. Zwischenraum von unten`;
  if(o===-1)return"direkt unter der untersten Linie";
  if(o===9)return"direkt über der obersten Linie";
  if(o<0){const k=-o;return k%2===0?`auf der ${k/2}. Hilfslinie unten`:`unter der ${(k-1)/2}. Hilfslinie unten`}
  const k=o-8;return k%2===0?`auf der ${k/2}. Hilfslinie oben`:`über der ${(k-1)/2}. Hilfslinie oben`}
function onLine(clef,n){return(N(n).dia-BOTTOM[clef])%2===0}
function countChain(a,b){a=N(a);b=N(b);const lo=a.dia<=b.dia?a:b,hi=a.dia<=b.dia?b:a,out=[];
  for(let d=lo.dia;d<=hi.dia;d++)out.push(d===lo.dia?name(lo):d===hi.dia?name(hi):name(fromDia(d,0)));return out}
if(typeof module!=="undefined")module.exports={N,mk,fromDia,spell,letter,name,oktave,intNum,intName,semis,terz,triad,chordName,analyze,chord,voicings,moveCost,bestNext,bassRoot,planVoicing,where,onLine,countChain,INT,BOTTOM};

/* ===== Musik: Darstellung und Übungen im Browser ===== */
(function(){
const D={"cards": {"t1": [["Die sieben Stammtöne", "c d e f g a h"], ["Violinschlüssel: Töne auf den Linien (von unten)", "e' g' h' d'' f''<br><span class='meta'>Eine Gute Hexe Darf Fliegen</span>"], ["Violinschlüssel: Töne in den Zwischenräumen (von unten)", "f' a' c'' e'' (FACE)"], ["Wo liegt im Violinschlüssel das c'?", "Auf der 1. Hilfslinie unten."], ["Wo liegt das g'?", "Auf der 2. Linie von unten. Dort beginnt der Violinschlüssel (G-Schlüssel)."], ["Wie heißt diese Note? <div data-st='v|d&#39;&#39;'></div>", "d'' (4. Linie)"], ["Wie heißt diese Note? <div data-st='v|a&#39;'></div>", "a' (2. Zwischenraum)"], ["Wie heißt diese Note? <div data-st='v|d&#39;'></div>", "d' (direkt unter der untersten Linie)"], ["Wie heißt diese Note? <div data-st='v|a&#39;&#39;'></div>", "a'' (1. Hilfslinie oben)"]], "t2": [["Bassschlüssel: Töne auf den Linien (von unten)", "G H d f a<br><span class='meta'>Grüne Hasen dürfen fast alles</span>"], ["Bassschlüssel: Töne in den Zwischenräumen (von unten)", "A c e g<br><span class='meta'>Alle Clowns essen gern</span>"], ["Warum heißt der Bassschlüssel F-Schlüssel?", "Seine zwei Punkte liegen um die 4. Linie. Dort liegt das f."], ["Bassschlüssel: Was liegt auf der 1. Hilfslinie oben?", "c' (das mittlere c)"], ["Bassschlüssel: Was liegt auf der 1. Hilfslinie unten?", "E"], ["Wie heißt diese Note? <div data-st='b|d'></div>", "d (3. Linie)"], ["Wie heißt diese Note? <div data-st='b|A'></div>", "A (1. Zwischenraum)"], ["Wie heißt diese Note? <div data-st='b|g'></div>", "g (4. Zwischenraum)"], ["Wie heißt diese Note? <div data-st='b|h'></div>", "h (direkt über der obersten Linie)"]], "t3": [["große Oktave", "C D E F G A H (große Buchstaben)"], ["kleine Oktave", "c d e f g a h (kleine Buchstaben)"], ["eingestrichene Oktave", "c' d' e' f' g' a' h' (ein Strich)"], ["zweigestrichene Oktave", "c'' d'' e'' f'' g'' a'' h'' (zwei Striche)"], ["Bei welchem Ton beginnt eine neue Oktave?", "Immer bei c."], ["Welcher Ton kommt nach h'?", "c''"], ["Was ist das mittlere c?", "Das c'. Im Violinschlüssel auf der 1. Hilfslinie unten, im Bassschlüssel auf der 1. Hilfslinie oben."]], "t4": [["Was ist ein Intervall?", "Der Abstand zwischen zwei Tönen. Ein einzelner Ton ist nie ein Intervall."], ["Wie geht die Grobbestimmung?", "Linien und Zwischenräume von der unteren bis zur oberen Note zählen. Beide Noten zählen mit."], ["Intervalle 1 bis 4", "Prime, Sekunde, Terz, Quarte"], ["Intervalle 5 bis 8", "Quinte, Sexte, Septime, Oktave"], ["Beide Noten auf Linien. Welche Intervalle sind möglich?", "Nur ungerade: Prime, Terz, Quinte, Septime"], ["Welches Intervall? <div data-st='v|e&#39;&gt;h&#39;' data-cw='46'></div>", "Quinte: e' f' g' a' h' = 5 Töne"], ["Welches Intervall? <div data-st='v|f&#39;&gt;d&#39;&#39;' data-cw='46'></div>", "Sexte: f' g' a' h' c'' d'' = 6 Töne"], ["Welches Intervall? <div data-st='b|c&gt;h' data-cw='46'></div>", "Septime: c d e f g a h = 7 Töne"]], "t5": [["Halbtonschritt", "Abstand von einer Taste zur direkt benachbarten Taste (schwarze Tasten zählen mit)."], ["große Terz", "4 Halbtonschritte (g3)"], ["kleine Terz", "3 Halbtonschritte (k3)"], ["Zwischen welchen weißen Tasten liegt keine schwarze?", "e–f und h–c"], ["Große Terzen ohne Vorzeichen", "c–e, f–a, g–h"], ["Kleine Terzen ohne Vorzeichen", "d–f, e–g, a–c, h–d"], ["Was macht ein ♯?", "Es erhöht um einen Halbtonschritt: f → fis"], ["Was macht ein ♭?", "Es erniedrigt um einen Halbtonschritt: e → es, a → as, h → b"], ["d'–fis': groß oder klein?", "große Terz (4 HTS)"]], "t6": [["Wie heißen die drei Töne eines Dreiklangs?", "Grundton (unten), Terzton (Mitte), Quintton (oben)"], ["Durdreiklang", "unten große Terz, oben kleine Terz"], ["Molldreiklang", "unten kleine Terz, oben große Terz"], ["Terzschichtung", "Zwei Terzen liegen übereinander. Das ist typisch für Dreiklänge."], ["sukzessiv und simultan", "sukzessiv = nacheinander, simultan = gleichzeitig"], ["Welcher Dreiklang? <div data-st='v|g&#39;+h&#39;+d&#39;&#39;' data-cw='60'></div>", "G-Dur: g'–h' große Terz, h'–d'' kleine Terz"], ["Welcher Dreiklang? <div data-st='v|a&#39;+c&#39;&#39;+e&#39;&#39;' data-cw='60'></div>", "a-Moll: a'–c'' kleine Terz, c''–e'' große Terz"], ["Welcher Dreiklang? <div data-st='v|d&#39;+fis&#39;+a&#39;' data-cw='60'></div>", "D-Dur: d'–fis' große Terz, fis'–a' kleine Terz"], ["Wie schreibt man Dur und Moll?", "Dur mit großem Buchstaben (F-Dur), Moll mit kleinem (e-Moll)."]], "t7": [["Akkordsymbol C", "C-Dur: c – e – g"], ["Akkordsymbol Dm", "d-Moll: d – f – a"], ["Akkordsymbol Em", "e-Moll: e – g – h"], ["Akkordsymbol Am", "a-Moll: a – c – e"], ["Akkordsymbol F", "F-Dur: f – a – c"], ["Akkordsymbol G", "G-Dur: g – h – d"], ["Regel 1 der Liedbegleitung", "Wenig oder keine Tonsprünge, lieber kleine Notenschritte."], ["Regel 2 der Liedbegleitung", "Was liegen bleiben kann, bleibt liegen."], ["Regel 3 der Liedbegleitung", "Der Grundton wird im Bass verdoppelt."]]}, "quiz": {"t1": [["Wie heißt diese Note?", ["g'", "e'", "h'", "f'"], "Auf der 2. Linie von unten liegt das g'. Dort beginnt der Violinschlüssel.", "v|g'"], ["Wie heißt diese Note?", ["c'", "d'", "a", "e'"], "Das c' liegt auf der 1. Hilfslinie unten.", "v|c'"], ["Wie heißt diese Note?", ["f''", "e''", "d''", "g''"], "Die oberste (5.) Linie ist f''.", "v|f''"], ["Wie heißt diese Note?", ["a'", "f'", "c''", "g'"], "Im 2. Zwischenraum liegt a' (FACE: f' a' c'' e'').", "v|a'"], ["Wie heißt diese Note?", ["e''", "c''", "d''", "f''"], "Im 4. Zwischenraum liegt e'' (FACE).", "v|e''"], ["Welche Töne liegen im Violinschlüssel auf den Linien (von unten)?", ["e' g' h' d'' f''", "f' a' c'' e'' g''", "G H d f a", "c' e' g' h' d''"], "Eine Gute Hexe Darf Fliegen."], ["Wie heißen die sieben Stammtöne?", ["c d e f g a h", "c d e f g a b", "a b c d e f g", "c d e f g h a"], "Im Deutschen heißt der Ton nach a: h."], ["Welche Note liegt direkt unter der untersten Linie?", ["d'", "c'", "e'", "h"], "Die unterste Linie ist e'. Einen Schritt tiefer liegt d'."]], "t2": [["Wie heißt diese Note?", ["f", "a", "d", "e"], "Die zwei Punkte des Bassschlüssels liegen um die 4. Linie. Dort liegt f.", "b|f"], ["Wie heißt diese Note?", ["G", "e'", "E", "A"], "Die unterste Linie im Bassschlüssel ist G. (Im Violinschlüssel wäre es e'.)", "b|G"], ["Wie heißt diese Note?", ["c'", "a", "h", "e"], "Auf der 1. Hilfslinie oben liegt das mittlere c, also c'.", "b|c'"], ["Wie heißt diese Note?", ["c", "a'", "e", "H"], "Im 2. Zwischenraum liegt c (A c e g).", "b|c"], ["Wie heißt diese Note?", ["H", "G", "d", "g'"], "Auf der 2. Linie liegt H (G H d f a).", "b|H"], ["Welche Töne liegen im Bassschlüssel auf den Linien (von unten)?", ["G H d f a", "A c e g h", "e' g' h' d'' f''", "F A c e g"], "Grüne Hasen dürfen fast alles."], ["Welche Töne liegen im Bassschlüssel in den Zwischenräumen (von unten)?", ["A c e g", "F A c e", "f' a' c'' e''", "H d f a"], "Alle Clowns essen gern."], ["Warum heißt der Bassschlüssel auch F-Schlüssel?", ["Seine Punkte zeigen, wo das f liegt (4. Linie).", "Er beginnt auf der untersten Linie mit F.", "Er ist für Flöten.", "Er sieht aus wie ein F."], "Die beiden Punkte umschließen die 4. Linie. Dort liegt f."]], "t3": [["Wie schreibt man das c aus der eingestrichenen Oktave?", ["c'", "c", "C", "c''"], "Eingestrichen = ein Strich."], ["Bei welchem Ton beginnt eine neue Oktave?", ["bei c", "bei a", "bei h", "bei g"], "Jede Oktave geht von c bis h."], ["Welcher Ton kommt direkt nach h'?", ["c''", "c'", "a'", "h''"], "Nach h beginnt mit c die nächste Oktave. Deshalb zwei Striche."], ["Wie schreibt man die Töne der großen Oktave?", ["mit großen Buchstaben, z. B. G", "mit kleinen Buchstaben, z. B. g", "mit einem Strich, z. B. g'", "mit zwei Strichen, z. B. g''"], "Große Oktave = große Buchstaben."], ["Wie heißt diese Note genau?", ["A", "a", "a'", "a''"], "1. Zwischenraum im Bassschlüssel: A aus der großen Oktave.", "b|A"], ["Wie heißt diese Note genau?", ["e''", "e'", "e", "E"], "4. Zwischenraum im Violinschlüssel: e'' aus der zweigestrichenen Oktave.", "v|e''"], ["In welcher Oktave liegt das d (kleiner Buchstabe, ohne Strich)?", ["kleine Oktave", "große Oktave", "eingestrichene Oktave", "zweigestrichene Oktave"], "Kleiner Buchstabe ohne Strich = kleine Oktave."], ["Das c auf der 1. Hilfslinie unten im Violinschlüssel und das c auf der 1. Hilfslinie oben im Bassschlüssel sind …", ["derselbe Ton: c'", "zwei verschiedene Töne: c' und c", "c'' und c'", "C und c"], "Beides ist das mittlere c, also c'."]], "t4": [["Was ist ein Intervall?", ["der Abstand zwischen zwei Tönen", "ein einzelner Ton", "ein Dreiklang", "eine Pause"], "Ein einzelner Ton kann nie ein Intervall sein."], ["Welches Intervall ist das?", ["Quinte", "Quarte", "Sexte", "Terz"], "c' d' e' f' g' = 5 Töne.", "v|c'>g'"], ["Welches Intervall ist das?", ["Sekunde", "Prime", "Terz", "Quarte"], "e' und f' liegen direkt nebeneinander: 2 Töne.", "v|e'>f'"], ["Welches Intervall ist das?", ["Oktave", "Septime", "Sexte", "Prime"], "d' bis d'': 8 Töne. Gleicher Buchstabe, eine Oktave höher.", "v|d'>d''"], ["Welches Intervall ist das?", ["Quarte", "Quinte", "Terz", "Sexte"], "f' g' a' h' = 4 Töne.", "v|f'>h'"], ["Welches Intervall ist das?", ["Terz", "Sekunde", "Quarte", "Quinte"], "Von unten gezählt: a' (1) h' (2) c'' (3) = 3 Töne. Die Richtung ist egal.", "v|c''>a'"], ["Welches Intervall ist das?", ["Sexte", "Quinte", "Septime", "Quarte"], "G A H c d e = 6 Töne.", "b|G>e"], ["Beide Noten liegen auf Linien. Welches Intervall kann es NICHT sein?", ["Quarte", "Terz", "Quinte", "Septime"], "Linie und Linie ergibt immer eine ungerade Zahl: Prime, Terz, Quinte oder Septime."], ["c'–e' und c'–es': Was sind sie in der Grobbestimmung?", ["Beides sind Terzen.", "c'–e' ist eine Terz, c'–es' eine Sekunde.", "Beides sind Quarten.", "c'–es' ist kein Intervall."], "Vorzeichen ändern die Grobbestimmung nicht."]], "t5": [["Wie viele Halbtonschritte hat eine große Terz?", ["4", "3", "2", "5"], "große Terz = 4 HTS."], ["Wie viele Halbtonschritte hat eine kleine Terz?", ["3", "4", "2", "1"], "kleine Terz = 3 HTS."], ["Zwischen welchen weißen Tasten liegt keine schwarze Taste?", ["e–f und h–c", "c–d und f–g", "g–a und a–h", "d–e und e–f"], "e–f und h–c sind Halbtonschritte."], ["Große oder kleine Terz?", ["kleine Terz", "große Terz"], "d' – dis'/es' – e' – f': 3 HTS.", "v|d'>f'"], ["Große oder kleine Terz?", ["große Terz", "kleine Terz"], "f' – fis' – g' – gis' – a': 4 HTS.", "v|f'>a'"], ["Große oder kleine Terz?", ["große Terz", "kleine Terz"], "Durch das Kreuz wird es eine große Terz: d' bis fis' = 4 HTS.", "v|d'>fis'"], ["Große oder kleine Terz?", ["kleine Terz", "große Terz"], "a' – b' – h' – c'': 3 HTS. Zwischen h und c ist nur ein Halbtonschritt.", "v|a'>c''"], ["Was macht ein ♯ (Kreuz)?", ["Es erhöht den Ton um einen Halbtonschritt.", "Es erniedrigt den Ton um einen Halbtonschritt.", "Es erhöht den Ton um eine Oktave.", "Es macht den Ton lauter."], "Aus f wird fis."], ["Wie heißt das h, wenn ein ♭ davor steht?", ["b", "hes", "his", "bes"], "Ausnahme: h mit ♭ heißt b."], ["Wie heißt das e, wenn ein ♭ davor steht?", ["es", "ees", "eis", "e♭"], "Ausnahme: e mit ♭ heißt es (und a mit ♭ heißt as)."]], "t6": [["Wie ist ein Durdreiklang aufgebaut (von unten nach oben)?", ["unten große Terz, oben kleine Terz", "unten kleine Terz, oben große Terz", "zwei große Terzen", "zwei kleine Terzen"], "Dur: g3 unten, k3 oben."], ["Wie ist ein Molldreiklang aufgebaut (von unten nach oben)?", ["unten kleine Terz, oben große Terz", "unten große Terz, oben kleine Terz", "zwei große Terzen", "eine Quarte und eine Terz"], "Moll: k3 unten, g3 oben."], ["Welcher Dreiklang ist das?", ["F-Dur", "f-Moll", "a-Moll", "C-Dur"], "f'–a' große Terz, a'–c'' kleine Terz → F-Dur.", "v|f'+a'+c''"], ["Welcher Dreiklang ist das?", ["a-Moll", "A-Dur", "C-Dur", "e-Moll"], "a'–c'' kleine Terz, c''–e'' große Terz → a-Moll.", "v|a'+c''+e''"], ["Welcher Dreiklang ist das?", ["e-Moll", "E-Dur", "G-Dur", "h-Moll"], "e'–g' kleine Terz, g'–h' große Terz → e-Moll.", "v|e'+g'+h'"], ["Welcher Dreiklang ist das?", ["D-Dur", "d-Moll", "F-Dur", "fis-Moll"], "d'–fis' große Terz, fis'–a' kleine Terz → D-Dur.", "v|d'+fis'+a'"], ["Wie heißen die drei Töne eines Dreiklangs (von unten)?", ["Grundton, Terzton, Quintton", "Grundton, Quintton, Terzton", "Prime, Sekunde, Terz", "Bass, Mitte, Spitze"], "Der Terzton liegt eine Terz, der Quintton eine Quinte über dem Grundton."], ["Welche Aussage ist FALSCH?", ["Der Grundton ist der höchste Ton des Dreiklangs.", "Ein Dreiklang besteht aus zwei übereinanderliegenden Terzen.", "Dreiklangstöne können nacheinander oder gleichzeitig erklingen.", "Der Quintton liegt eine Quinte über dem Grundton."], "Der Grundton ist der tiefste Ton."], ["Was bedeutet „simultan“?", ["gleichzeitig", "nacheinander", "laut", "spannungsreich"], "Simultan = gleichzeitig, sukzessiv = nacheinander."], ["Welche Töne hat G-Dur?", ["g – h – d", "g – b – d", "g – h – e", "g – c – e"], "g–h große Terz, h–d kleine Terz."], ["Wie schreibt man den Namen eines Molldreiklangs?", ["mit kleinem Buchstaben: a-Moll", "mit großem Buchstaben: A-Moll", "mit Strich: a'-Moll", "nur mit m: am"], "Dur groß (A-Dur), Moll klein (a-Moll)."]], "t7": [["Was bedeutet das Akkordsymbol Dm?", ["d-Moll-Dreiklang: d – f – a", "D-Dur-Dreiklang: d – fis – a", "nur der Ton d im Bass", "d-Moll-Tonleiter"], "Großbuchstabe mit m = Moll."], ["Was bedeutet das Akkordsymbol G?", ["G-Dur-Dreiklang: g – h – d", "g-Moll-Dreiklang: g – b – d", "nur der Ton G", "G-Schlüssel"], "Nur ein Großbuchstabe = Dur."], ["Welcher Ton kommt in den Bass?", ["der Grundton", "der Terzton", "der Quintton", "der höchste Ton der Melodie"], "Regel 3: Der Grundton wird im Bass verdoppelt."], ["Zwei Akkorde nacheinander haben einen Ton gemeinsam. Was machst du mit ihm?", ["Er bleibt liegen.", "Er springt eine Oktave hoch.", "Er fällt weg.", "Er kommt in den Bass."], "Regel 2: Was liegen bleiben kann, bleibt liegen."], ["Darf man g c' e' statt c' e' g' schreiben?", ["Ja, es sind dieselben Töne c, e, g, also C-Dur.", "Nein, dann ist es kein C-Dur mehr.", "Nein, dann ist es G-Dur.", "Nur im Bassschlüssel."], "Die Reihenfolge darf sich ändern, die Töne bleiben gleich."], ["Vorher steht C (c' e' g'). Dann kommt Am. Welche Lage passt am besten?", ["c' e' a'", "a c' e'", "e' a' c''", "a' c'' e''"], "c' und e' bleiben liegen, nur g' geht einen Schritt hoch zu a'."], ["Vorher steht G (d' g' h'). Dann kommt C. Welche Lage passt am besten?", ["e' g' c''", "c' e' g'", "g c' e'", "c'' e'' g''"], "g' bleibt liegen, d'→e' und h'→c'' sind kleine Schritte."], ["Vorher steht F (c' f' a'). Dann kommt C. Welche Lage passt am besten?", ["c' e' g'", "e' g' c''", "g c' e'", "c'' e'' g''"], "c' bleibt liegen, f'→e' und a'→g' sind kleine Schritte."], ["Welche Töne hat Em?", ["e – g – h", "e – gis – h", "e – g – b", "e – a – c"], "e-Moll: e–g kleine Terz, g–h große Terz."]]}, "steps": ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "gem", "probe"], "topics": ["t1", "t2", "t3", "t4", "t5", "t6", "t7"], "prog": [{"name": "Morning has broken T. 1–6", "syms": ["C", "Dm", "G", "F", "C"]}, {"name": "Morning has broken T. 7–10", "syms": ["C", "Em", "F", "G"]}, {"name": "Morning has broken T. 13–18", "syms": ["C", "F", "C", "Am", "D"]}, {"name": "Morning has broken T. 19–23", "syms": ["C", "Em", "F", "G", "C"]}, {"name": "Übung: C F G C", "syms": ["C", "F", "G", "C"]}, {"name": "Übung: C Am Dm G C", "syms": ["C", "Am", "Dm", "G", "C"]}, {"name": "Übung: G C D G", "syms": ["G", "C", "D", "G"]}, {"name": "Übung: Am Dm E Am", "syms": ["Am", "Dm", "E", "Am"]}]},GL={"g": "M376 415C374 427 376 428 382 434C490 535 572 662 572 815C572 902 548 988 507 1048C492 1070 466 1098 455 1098C441 1098 410 1072 390 1050C316 968 292 843 292 739C292 681 299 616 306 575C308 563 309 561 297 551C153 432 0 289 0 87C0 -87 119 -252 364 -252C387 -252 413 -250 433 -246C444 -244 446 -243 448 -255C460 -322 475 -409 475 -456C475 -604 375 -622 316 -622C262 -622 236 -606 236 -593C236 -586 245 -583 268 -576C299 -567 335 -540 335 -482C335 -427 300 -380 239 -380C172 -380 132 -433 132 -495C132 -560 171 -658 322 -658C389 -658 519 -628 519 -458C519 -401 501 -306 490 -244C488 -232 489 -233 503 -227C604 -187 671 -102 671 11C671 139 577 252 430 252C404 252 404 252 401 270ZM470 943C503 943 530 916 530 861C530 750 435 660 356 591C349 585 345 586 343 599C339 625 337 659 337 691C337 847 409 943 470 943ZM361 262C364 243 364 244 346 238C258 208 201 129 201 44C201 -46 248 -110 316 -133C324 -136 336 -139 343 -139C351 -139 355 -134 355 -128C355 -121 347 -118 340 -115C298 -97 268 -54 268 -8C268 49 307 92 368 109C384 113 386 112 388 101L438 -197C440 -208 439 -208 424 -211C408 -214 388 -216 368 -216C193 -216 80 -119 80 20C80 79 90 158 173 252C233 319 279 356 326 394C336 402 338 401 340 390ZM430 103C428 115 429 118 441 117C522 110 589 42 589 -46C589 -109 551 -160 495 -188C483 -194 481 -194 479 -182Z", "f": "M252 262C78 262 0 135 0 39C0 -41 42 -110 123 -110C186 -110 229 -66 229 -4C229 60 182 100 133 100C106 100 96 93 83 93C70 93 67 101 67 111C67 151 127 224 229 224C335 224 381 120 381 -37C381 -316 243 -472 10 -605C1 -610 -5 -615 -5 -623C-5 -629 -1 -635 8 -635C13 -635 19 -633 25 -630C271 -510 531 -332 531 -28C531 146 425 262 252 262ZM629 180C598 180 574 156 574 125C574 94 598 70 629 70C660 70 684 94 684 125C684 156 660 180 629 180ZM630 -71C599 -71 576 -94 576 -125C576 -156 599 -179 630 -179C661 -179 684 -156 684 -125C684 -94 661 -71 630 -71Z", "whole": "M216 125C83 125 0 70 0 2C0 -65 57 -125 206 -125C370 -125 422 -68 422 2C422 73 309 125 216 125ZM111 63C122 98 159 103 190 103C259 103 314 29 314 -31C314 -62 301 -90 268 -98C258 -101 247 -102 237 -102C201 -102 164 -78 143 -50C123 -27 108 7 108 39C108 47 109 55 111 63Z", "black": "M97 -125C186 -125 295 -43 295 42C295 93 255 125 198 125C88 125 0 44 0 -42C0 -94 43 -125 97 -125Z", "sharp": "M237 118C244 121 249 129 249 135V206C249 211 246 214 242 214C240 214 239 214 237 213C237 213 217 205 212 204C205 204 198 209 198 217V339C198 345 192 350 184 350C174 350 168 345 168 339V209C167 199 164 186 155 180C143 173 109 159 92 155C83 155 80 167 80 175V295C80 301 73 306 66 306C56 306 50 301 50 295V160C50 146 44 136 38 133C32 130 12 122 12 122C5 120 0 112 0 106V35C0 29 3 26 9 26L11 27C12 27 27 33 35 37L36 38C44 38 50 28 50 20V-79C50 -90 45 -99 39 -102C33 -104 12 -113 12 -113C5 -115 0 -123 0 -129V-200C0 -206 3 -209 9 -209L11 -208C12 -208 26 -202 35 -199C36 -198 37 -198 38 -198C45 -198 50 -209 50 -214V-337C50 -343 56 -348 63 -348C73 -348 80 -343 80 -337V-198C80 -185 85 -178 90 -176L151 -151C151 -151 152 -151 152 -151L154 -150C163 -150 168 -162 168 -168V-293C168 -299 174 -304 181 -304C192 -304 198 -299 198 -293V-151C198 -143 202 -131 209 -128C216 -125 237 -117 237 -117C244 -114 249 -106 249 -100V-29C249 -24 246 -21 242 -21C240 -21 239 -21 237 -22L211 -32C205 -32 198 -26 198 -14V79C198 86 203 105 211 108ZM168 -45C162 -65 115 -85 92 -85C86 -85 81 -83 80 -80C78 -76 77 -54 77 -30C77 1 78 36 80 44C82 61 128 82 153 82C160 82 166 80 168 76C170 71 172 46 172 19C172 -8 170 -36 168 -45Z", "flat": "M12 -170C15 -174 18 -175 21 -175C24 -175 27 -173 27 -173C57 -156 81 -129 106 -112C195 -50 226 11 226 57C226 114 182 150 136 153C119 153 95 145 81 136C75 131 64 122 59 122C57 122 56 122 54 123C47 126 43 133 43 140C44 162 50 402 50 422C50 433 41 439 31 439C17 439 1 429 0 411C0 411 4 -160 12 -170ZM47 -81C47 -81 44 -21 44 19C44 35 45 47 46 51C53 71 93 100 116 100C145 100 157 67 157 42C157 -12 111 -66 68 -93C64 -95 61 -96 58 -96C49 -96 47 -86 47 -81Z", "nat": "M141 181C139 181 138 180 137 180C137 180 73 157 47 157C41 157 37 158 37 162V329C37 336 31 341 25 341H12C5 341 0 336 0 329V-186C0 -192 3 -195 9 -195L11 -194C12 -194 14 -194 15 -193C29 -187 85 -163 114 -163C124 -163 131 -166 131 -174V-323C131 -330 136 -335 143 -335H156C162 -335 168 -330 168 -323V179C168 184 164 187 160 187C159 187 157 187 156 186ZM37 39C37 53 98 79 122 79C128 79 131 78 131 74V-29C131 -47 74 -70 49 -70C42 -70 37 -68 37 -64Z"};
const page=document.body.dataset.page;
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
function store(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem(k));localStorage.setItem(k,JSON.stringify(v))}catch(e){return null}}
function shuffle(a){a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
const rnd=a=>a[Math.floor(Math.random()*a.length)];

/* ---------- Haken: welche Schritte sind fertig ---------- */
const DONE=new Set(store("mus-themen")||[]);
const saveDone=()=>store("mus-themen",[...DONE]);
$$("[data-finish]").forEach(a=>a.addEventListener("click",()=>{DONE.add(a.dataset.finish);saveDone()}));
function paintDone(){
  let next=false;
  $$("a.step[data-step]").forEach(s=>{const d=DONE.has(s.dataset.step);s.classList.toggle("done",d);s.classList.remove("next");if(!d&&!next){s.classList.add("next");next=true}});
  const left=D.steps.filter(id=>!DONE.has(id)).length;
  if($("#st-left"))$("#st-left").textContent=left?`Noch ${left} von ${D.steps.length} Schritten.`:"";
  if($("#st-all"))$("#st-all").hidden=left>0;
}
if(page==="start"){paintDone();$("#st-reset").onclick=()=>{DONE.clear();saveDone();paintDone()}}
$$("nav a[data-id]").forEach(a=>a.classList.toggle("done",DONE.has(a.dataset.id)));
const curNav=$("nav [aria-current]");if(curNav&&curNav.scrollIntoView)try{curNav.scrollIntoView({inline:"center",block:"nearest"})}catch(e){}

/* ---------- Notensystem zeichnen ---------- */
const S=0.04; // Bravura: 250 Einheiten = 1 Zwischenraum = 10 px im SVG
const glyph=(k,x,y,cls)=>`<path class="${cls||"gl"}" transform="translate(${x.toFixed(1)} ${y.toFixed(1)}) scale(${S} ${-S})" d="${GL[k]}"/>`;
function parseCol(c){if(typeof c==="string")c=c.includes(">")?{n:c.split(">"),seq:true}:{n:c==="_"?[]:c.split("+")};c.n=(c.n||[]).map(N);return c}
/* spec: {clef:"v"|"b", cols:[{n:[...], cls:[...], lab, top}], colW, bars, end, names, sc} */
function staffParts(spec){
  const clef=spec.clef||"v",B=BOTTOM[clef],cols=(spec.cols||[]).map(parseCol),cw=spec.colW||34,x0=38;
  const yOf=d=>-(d-B)*5;
  let dmin=B,dmax=B+8;cols.forEach(c=>c.n.forEach(n=>{dmin=Math.min(dmin,n.dia);dmax=Math.max(dmax,n.dia)}));
  if(spec.range){dmin=Math.min(dmin,spec.range[0]);dmax=Math.max(dmax,spec.range[1])}
  let top=Math.min(clef==="v"?-56:-44,yOf(dmax)-8),bot=Math.max(clef==="v"?19:6,yOf(dmin)+8);
  if(cols.some(c=>c.top))top-=16;
  const hasLab=cols.some(c=>c.lab)||spec.names,labY=Math.max(yOf(dmin)+8,6)+12;if(hasLab)bot=Math.max(bot,labY+4);
  const w=x0+cols.length*cw+(spec.end===false?4:10);
  let s="";
  for(let i=0;i<5;i++)s+=`<line class="sl" x1="0" x2="${w}" y1="${-i*10}" y2="${-i*10}"/>`;
  s+=`<line class="sl" x1="0.5" x2="0.5" y1="0" y2="-40"/>`;
  s+=clef==="v"?glyph("g",4,-10):glyph("f",3,-30);
  if(spec.end!==false)s+=`<line class="sl" x1="${w-4}" x2="${w-4}" y1="0" y2="-40"/><line class="sl thick" x1="${w-1.2}" x2="${w-1.2}" y1="0" y2="-40"/>`;
  cols.forEach((c,i)=>{
    const cx=x0+cw*i+cw/2+4;
    if(spec.bars&&i>0)s+=`<line class="sl" x1="${x0+cw*i}" x2="${x0+cw*i}" y1="0" y2="-40"/>`;
    // Notenköpfe: übereinander (Akkord) oder nacheinander (seq)
    const groups=c.seq?c.n.map((n,k)=>({x:cx+(k-(c.n.length-1)/2)*(cw/c.n.length)+(n.alt?3:0),ns:[[n,k]]})):[{x:cx,ns:c.n.map((n,k)=>[n,k])}];
    groups.forEach(g=>{const x=g.x,ds=g.ns.map(p=>p[0].dia);
      const lo=Math.min(...ds,B),hi=Math.max(...ds,B+8);
      for(let d=B-2;d>=lo;d-=2)s+=`<line class="sl" x1="${x-12}" x2="${x+12}" y1="${yOf(d)}" y2="${yOf(d)}"/>`;
      for(let d=B+10;d<=hi;d+=2)s+=`<line class="sl" x1="${x-12}" x2="${x+12}" y1="${yOf(d)}" y2="${yOf(d)}"/>`;
      let accN=0,prevD=null,prevOff=false;
      g.ns.slice().sort((a,b)=>a[0].dia-b[0].dia).forEach(([n,k])=>{
        const cls="nh"+(c.cls&&c.cls[k]?" "+c.cls[k]:"");
        const off=prevD!==null&&n.dia-prevD<=1&&!prevOff;prevD=n.dia;prevOff=off; // Sekunde im Akkord: Notenkopf daneben
        if(n.alt){const ax=x-8.4-13-(accN%2)*10;accN++;s+=glyph(n.alt>0?"sharp":"flat",ax,yOf(n.dia),cls)}
        s+=glyph("whole",x-8.44+(off?17:0),yOf(n.dia),cls);
      })});
    if(c.top)s+=`<text class="stt top" x="${cx}" y="${top+12}">${c.top}</text>`;
    const lab=c.lab!==undefined?c.lab:spec.names?(c.seq?c.n:c.n.slice().sort((a,b)=>a.dia-b.dia)).map(name).join(" "):"";
    if(lab)s+=`<text class="stt" x="${cx}" y="${labY}">${lab}</text>`;
    if(spec.hit)for(let d=spec.hit[0];d<=spec.hit[1];d++)s+=`<rect class="hit" data-dia="${d}" x="${cx-cw/2}" y="${yOf(d)-2.5}" width="${cw}" height="5"/>`;
  });
  return{s,w,top,bot};
}
function svgWrap(inner,w,top,h,sc,cls){return`<svg class="${cls||"staff"}" viewBox="-2 ${top} ${w+4} ${h}" style="width:${((w+4)*sc).toFixed(0)}px" role="img" aria-label="Notensystem">${inner}</svg>`}
function staff(spec){const p=staffParts(spec);return svgWrap(p.s,p.w,p.top,p.bot-p.top,spec.sc||2.4)}
/* Klaviersystem: Violin- und Bassschlüssel übereinander */
function system(t,b,sc){const P=staffParts(t),Q=staffParts(b),gap=12,dy=P.bot-Q.top+gap,w=Math.max(P.w,Q.w);
  let s=P.s+`<g transform="translate(0 ${dy})">${Q.s}</g><line class="sl" x1="0.5" x2="0.5" y1="-40" y2="${dy}"/>`;
  if(t.bars)(t.cols||[]).forEach((c,i)=>{if(i>0){const x=38+(t.colW||34)*i;s+=`<line class="sl" x1="${x}" x2="${x}" y1="0" y2="${dy-40}"/>`}});
  return svgWrap(s,w,P.top,dy+Q.bot-P.top,sc||2.2)}
/* Klaviatur: marks = Tasten zum Markieren, count = [von, bis] Halbtonschritte zählen */
function kb(o){
  const ms=(o.marks||[]).map(x=>N(x).midi),c0=Math.floor(Math.min(...ms)/12)*12,c1=Math.floor(Math.max(...ms)/12)*12+11;
  const W=22,H=86,BW=13,BH=52,white=[],black=[];
  for(let m=c0;m<=c1;m++)([1,3,6,8,10].includes(m%12)?black:white).push(m);
  const xw=m=>white.indexOf(m)*W,xb=m=>xw(m-1)+W-BW/2;
  const cnt=o.count?o.count.map(x=>N(x).midi).sort((a,b)=>a-b):null;
  let s="";
  white.forEach(m=>{const mk=ms.includes(m);s+=`<rect class="kw${mk?" mk":""}" x="${xw(m)}" y="0" width="${W}" height="${H}" rx="2"/>`;
    const L="cdefgah"[[0,2,4,5,7,9,11].indexOf(m%12)],o2=Math.floor(m/12)-1;
    s+=`<text class="kl" x="${xw(m)+W/2}" y="${H-5}">${name(mk2(L,o2))}</text>`});
  black.forEach(m=>{s+=`<rect class="kb${ms.includes(m)?" mk":""}" x="${xb(m)}" y="0" width="${BW}" height="${BH}" rx="2"/>`});
  if(cnt)for(let m=cnt[0]+1,k=1;m<=cnt[1];m++,k++){const isB=[1,3,6,8,10].includes(m%12),x=isB?xb(m)+BW/2:xw(m)+W/2,y=isB?BH-11:H-28;
    s+=`<circle class="kc" cx="${x}" cy="${y}" r="7.5"/><text class="kn" x="${x}" y="${y+4}">${k}</text>`}
  const w=white.length*W;return`<svg class="kbd" viewBox="-1 -1 ${w+2} ${H+2}" style="width:${Math.round(Math.min(680,(w+2)*2.3))}px" role="img" aria-label="Klaviatur">${s}</svg>`}
function mk2(L,o){return fromDia(o*7+"cdefgah".indexOf(L),0)}

/* Platzhalter in den Texten: data-st="v|c'+e'+g'|_", data-sys="C Dm G", data-kb="c'|e'|count" */
function renderStatic(root){
  root.querySelectorAll("[data-st]").forEach(el=>{const p=el.dataset.st.split("|"),clef=p.shift();
    const labs=el.dataset.lab?el.dataset.lab.split("|"):null,tops=el.dataset.top?el.dataset.top.split("|"):null;
    el.innerHTML=staff({clef,cols:p.map((c,i)=>{const o=parseCol(c);if(labs)o.lab=labs[i];if(tops)o.top=tops[i];return o}),names:el.hasAttribute("data-names"),colW:+(el.dataset.cw||34),bars:el.hasAttribute("data-bars"),sc:+(el.dataset.sc||2.4)})});
  root.querySelectorAll("[data-sys]").forEach(el=>{const syms=el.dataset.sys.split(" "),pl=planVoicing(syms);
    el.innerHTML=system({clef:"v",cols:pl.map(p=>({n:p.notes,top:p.sym,lab:el.hasAttribute("data-names")?p.notes.map(name).join(" "):undefined})),colW:46,bars:true,names:false},
      {clef:"b",cols:pl.map(p=>({n:[bassRoot(p.sym)],lab:el.hasAttribute("data-names")?name(bassRoot(p.sym)):undefined})),colW:46,bars:true},2.2)});
  root.querySelectorAll("[data-esys]").forEach(el=>{const syms=el.dataset.esys.split("|");
    el.innerHTML=system({clef:"v",cols:syms.map(s=>({n:[],top:s})),colW:60,bars:true,range:[N("g").dia,N("a''").dia]},{clef:"b",cols:syms.map(()=>({n:[]})),colW:60,bars:true,range:[N("E").dia,N("c'").dia]},2.2)});
  root.querySelectorAll("[data-kb]").forEach(el=>{const p=el.dataset.kb.split("|"),cnt=p.includes("count");const ns=p.filter(x=>x!=="count");
    el.innerHTML=kb({marks:ns,count:cnt?[ns[0],ns[ns.length-1]]:null})});
}
renderStatic(document);

/* ---------- Karten ---------- */
function mountCards(el,cards){
  let q=[],back=false,done=0;
  el.innerHTML='<p class="meta" data-m></p><div class="box card" role="button" tabindex="0" aria-live="polite"></div><div class="row" data-b><button class="btn ghost" data-again>Nochmal üben</button><button class="btn" data-ok>Gewusst</button></div><p><button class="btn ghost small" data-reset>Karten neu mischen</button></p>';
  const c=el.querySelector(".card"),m=el.querySelector("[data-m]"),b=el.querySelector("[data-b]");
  function render(){
    if(!q.length){c.className="box card";c.innerHTML="<div><b>Alle Karten gewusst! 🎉</b><br>Weiter geht es unten mit dem nächsten Teil.</div>";m.textContent="";b.style.display="none";return}
    b.style.display=back?"flex":"none";
    const [f,a]=cards[q[0]];
    c.className="box card"+(back?" back":"");
    c.innerHTML=back?`<div class="side">Antwort</div><div>${a}</div>`:`<div class="side">Antippen zum Umdrehen</div><div><b>${f}</b></div>`;
    renderStatic(c);
    m.textContent=`Noch ${q.length} ${q.length===1?"Karte":"Karten"} · ${done} gewusst`;
  }
  const start=()=>{q=shuffle(cards.map((_,i)=>i));done=0;back=false;render()};
  const flip=()=>{if(q.length){back=!back;render()}};
  c.addEventListener("click",flip);
  c.addEventListener("keydown",e=>{if(e.key===" "||e.key==="Enter"){e.preventDefault();flip()}});
  el.querySelector("[data-ok]").onclick=()=>{q.shift();done++;back=false;render()};
  el.querySelector("[data-again]").onclick=()=>{q.push(q.shift());back=false;render()};
  el.querySelector("[data-reset]").onclick=start;
  start();
}

/* ---------- Quiz (Fragen aus dem Text) ---------- */
function mountQuiz(el,QZ,key){
  let qs=[],qi=0,score=0,wrong=[];
  const start=list=>{qs=shuffle(list||QZ.map((_,i)=>i));qi=0;score=0;wrong=[];render()};
  function render(){
    if(qi>=qs.length){
      const full=qs.length===QZ.length;let best=store(key)||0;if(full){best=Math.max(best,score);store(key,best)}
      const msg=score===qs.length?"Alles richtig! 🎉":wrong.length<=1?"Fast alles richtig!":"Übe die falschen Fragen nochmal.";
      el.innerHTML=`<div class="box"><h3>${score} von ${qs.length} richtig</h3><p>${msg}</p>${full?`<p class="meta">Dein bestes Ergebnis: ${best} von ${QZ.length}</p>`:""}<div class="row">${wrong.length?'<button class="btn" data-retry>Falsche nochmal</button>':""}<button class="btn ghost" data-new>Quiz von vorn</button></div></div>`;
      const r=el.querySelector("[data-retry]");if(r)r.onclick=()=>start(wrong.slice());
      el.querySelector("[data-new]").onclick=()=>start();return;
    }
    const [q,opts,ex,st]=QZ[qs[qi]];const order=shuffle(opts.map((_,i)=>i));
    el.innerHTML=`<p class="meta">Frage ${qi+1} von ${qs.length}</p><div class="bar"><i style="width:${qi/qs.length*100}%"></i></div><div class="box"><h3>${q}</h3>${st?`<div class="stbox" data-st="${st}"></div>`:""}${order.map(i=>`<button class="opt" data-i="${i}">${opts[i]}</button>`).join("")}<div data-fb></div></div>`;
    renderStatic(el);
    el.querySelectorAll(".opt").forEach(b=>b.onclick=()=>{
      const ok=b.dataset.i==="0";
      el.querySelectorAll(".opt").forEach(x=>{x.disabled=true;if(x.dataset.i==="0")x.classList.add("right")});
      if(ok)score++;else{b.classList.add("wrong");wrong.push(qs[qi])}
      el.querySelector("[data-fb]").innerHTML=`<div class="fb ${ok?"right":"wrong"}"><b>${ok?"Richtig.":"Nicht ganz."}</b> ${ex}</div><div class="row"><button class="btn" data-next>Weiter</button></div>`;
      el.querySelector("[data-next]").onclick=()=>{qi++;render()};
    });
  }
  start();
}

/* ---------- Übungsrunden: falsche Aufgaben kommen am Ende nochmal ---------- */
function mountRound(el,o){
  let items=[],i=0,first=0,n0=0;
  const start=list=>{items=(list||o.make()).map(x=>Object.assign({},x,{again:false}));n0=items.length;i=0;first=0;render()};
  function render(){
    if(i>=items.length){
      el.innerHTML=`<div class="box"><h3>${first} von ${n0} beim ersten Versuch richtig</h3><p>${first===n0?"Super, alles richtig! 🎉":first>=n0-2?"Sehr gut!":"Mach am besten noch eine Runde."}</p>${o.after?'<div data-after></div>':""}<div class="row"><button class="btn" data-new>Neue Runde</button></div></div>`;
      if(o.after)o.after(el.querySelector("[data-after]"));
      el.querySelector("[data-new]").onclick=()=>start();return}
    const it=items[i];
    el.innerHTML=`<p class="meta">Aufgabe ${i+1} von ${items.length}${it.again?" · <b>Nochmal</b>":""}</p><div class="bar"><i style="width:${i/items.length*100}%"></i></div><div class="box tr"><div data-q></div><div data-fb></div></div>`;
    const q=el.querySelector("[data-q]"),fb=el.querySelector("[data-fb]");let done=false;
    o.show(it,q,(ok,html)=>{if(done)return;done=true;
      if(ok&&!it.again)first++;if(!ok&&!it.again&&o.repeat!==false)items.push(Object.assign({},it,{again:true}));
      fb.innerHTML=`<div class="fb ${ok?"right":"wrong"}"><b>${ok?"Richtig! ":"Nicht ganz. "}</b>${html||""}</div><div class="row"><button class="btn" data-next>Weiter →</button></div>`;
      renderStatic(fb);
      fb.querySelector("[data-next]").onclick=()=>{i++;render();const r=el.getBoundingClientRect();if(r.top<0&&el.scrollIntoView)el.scrollIntoView({block:"start"})}});
  }
  start();
}
/* Antwort-Knöpfe: Sofort prüfen */
function buttons(box,list,cls,onPick){
  box.innerHTML=list.map(([v,l])=>`<button class="${cls}" data-v="${v}">${l}</button>`).join("");
  box.querySelectorAll("button").forEach(b=>b.onclick=()=>{box.querySelectorAll("button").forEach(x=>x.disabled=true);onPick(b.dataset.v,b)});
}
function markButtons(box,right,picked){box.querySelectorAll("button").forEach(x=>{if(x.dataset.v===right)x.classList.add("right")});if(picked&&picked.dataset.v!==right)picked.classList.add("wrong")}
/* Auswahl-Gruppe ohne sofortiges Prüfen */
function seg(box,list,onChange){box.innerHTML=list.map(([v,l])=>`<button data-v="${v}" aria-pressed="false">${l}</button>`).join("");
  box.querySelectorAll("button").forEach(b=>b.onclick=()=>{box.querySelectorAll("button").forEach(x=>x.setAttribute("aria-pressed",x===b));onChange(b.dataset.v)})}
const LETTERS=[..."cdefgah"].map(l=>[l,l]);

/* ---------- Noten setzen (Tippen ins Notensystem) ---------- */
function mountPlace(box,o){ // o: {clef, multi, acc, range:[dmin,dmax]}
  const st={notes:[],acc:0,sel:null,locked:false};
  box.innerHTML=`${o.acc?'<div class="row accs"><span class="meta">Vorzeichen für die nächste Note:</span><div class="seg" data-acc></div></div>':""}<div class="place" data-svg></div><div class="row" data-move>${o.multi?"":'<button class="btn ghost" data-up aria-label="Note höher">▲ höher</button><button class="btn ghost" data-down aria-label="Note tiefer">▼ tiefer</button>'}<button class="btn ghost small" data-clear>Löschen</button></div>`;
  if(o.acc){seg(box.querySelector("[data-acc]"),[["0","ohne"],["1","♯ Kreuz"],["-1","♭ b"]],v=>st.acc=+v);box.querySelector("[data-acc] button").setAttribute("aria-pressed","true")}
  function draw(marks){
    const cols=[{n:st.notes.map(x=>fromDia(x.dia,x.alt)),cls:st.notes.map(x=>marks?marks(x):"v")}];
    box.querySelector("[data-svg]").innerHTML=staff({clef:o.clef,cols,colW:56,range:o.range,hit:st.locked?null:o.range,sc:3.1});
    box.querySelectorAll(".hit").forEach(r=>r.addEventListener("click",()=>tap(+r.dataset.dia)));
  }
  function tap(d){if(st.locked)return;
    if(o.multi){const k=st.notes.findIndex(x=>x.dia===d);
      if(k>=0){if(st.notes[k].alt!==st.acc)st.notes[k].alt=st.acc;else st.notes.splice(k,1)}
      else if(st.notes.length<(o.max||3))st.notes.push({dia:d,alt:st.acc})}
    else st.notes=[{dia:d,alt:0}];
    draw()}
  if(!o.multi){box.querySelector("[data-up]").onclick=()=>{if(st.locked)return;const d=st.notes.length?st.notes[0].dia+1:(o.start||o.range[0]+5);if(d<=o.range[1])st.notes=[{dia:d,alt:0}];draw()};
    box.querySelector("[data-down]").onclick=()=>{if(st.locked)return;const d=st.notes.length?st.notes[0].dia-1:(o.start||o.range[0]+5);if(d>=o.range[0])st.notes=[{dia:d,alt:0}];draw()}}
  box.querySelector("[data-clear]").onclick=()=>{if(!st.locked){st.notes=[];draw()}};
  draw();
  return{get:()=>st.notes.slice(),lock:marks=>{st.locked=true;box.querySelector("[data-move]").style.display="none";const a=box.querySelector(".accs");if(a)a.style.display="none";draw(marks)}};
}

/* ---------- Übungen ---------- */
const V_POOL=["c'","d'","e'","f'","g'","a'","h'","c''","d''","e''","f''","g''","a''"];
const B_POOL=["E","F","G","A","H","c","d","e","f","g","a","h","c'"];
const T={};
T["name"]=clef=>({make:()=>shuffle(clef==="v"?V_POOL:B_POOL).slice(0,10).map(n=>({clef,n})),
  show(it,q,fin){q.innerHTML=`<h3>Wie heißt diese Note?</h3>${staff({clef:it.clef,cols:[{n:[it.n]}],sc:2.8})}<div class="keys" data-k></div>`;
    const n=N(it.n);buttons(q.querySelector("[data-k]"),LETTERS,"key",(v,b)=>{const ok=v===letter(n);markButtons(q.querySelector("[data-k]"),letter(n),b);
      fin(ok,`Das ist ein <b>${name(n)}</b>. Es liegt ${where(it.clef,n)}.`)})}});
T["setzen"]=clef=>({make:()=>shuffle(clef==="v"?V_POOL:B_POOL).slice(0,8).map(n=>({clef,n})),
  show(it,q,fin){const n=N(it.n),B=BOTTOM[it.clef];
    q.innerHTML=`<h3>Setze die Note <span class="nm">${name(n)}</span> ins Notensystem.</h3><p class="meta">Tippe auf die Stelle. Mit ▲ und ▼ kannst du die Note verschieben.</p><div data-p></div><div class="row"><button class="btn" data-check>Prüfen</button></div>`;
    const P=mountPlace(q.querySelector("[data-p]"),{clef:it.clef,range:[B-3,B+11],start:B+4});
    q.querySelector("[data-check]").onclick=()=>{const g=P.get();if(!g.length){alert("Setze zuerst eine Note.");return}
      const ok=g[0].dia===n.dia;q.querySelector("[data-check]").remove();P.lock(x=>x.dia===n.dia?"g":"r");
      fin(ok,ok?`<b>${name(n)}</b> liegt ${where(it.clef,n)}.`:`Deine Note ist ein ${name(fromDia(g[0].dia,0))}. Das <b>${name(n)}</b> liegt ${where(it.clef,n)}:<div data-st="${it.clef}|${name(n)}" data-names></div>`)}}});
T["oktave"]=()=>({make:()=>shuffle([...V_POOL.map(n=>({clef:"v",n})),...B_POOL.map(n=>({clef:"b",n}))]).slice(0,10),
  show(it,q,fin){const n=N(it.n);const opts=[2,3,4,5].map(o=>name(mk(n.step,0,o)));
    q.innerHTML=`<h3>Wie heißt diese Note genau (mit Oktave)?</h3>${staff({clef:it.clef,cols:[{n:[n]}],sc:2.8})}<div class="keys wide" data-k></div>`;
    const k=q.querySelector("[data-k]");buttons(k,opts.map(x=>[x,x]),"key",(v,b)=>{markButtons(k,name(n),b);
      fin(v===name(n),`Das ist <b>${name(n)}</b> aus der ${oktave(n)}.${n.oct===4&&n.step===0?" Das c' ist das „mittlere c“.":""}`)})}});
T["intervall"]=()=>({make(){const out=[];for(let i=0;i<12;i++){const clef=Math.random()<.75?"v":"b",lo=clef==="v"?N("c'").dia:N("E").dia,hi=clef==="v"?N("a''").dia:N("c'").dia;
      const k=(i%8)+1,a=lo+Math.floor(Math.random()*(hi-lo-k+2)),A=fromDia(a,0),Bn=fromDia(a+k-1,0),down=Math.random()<.3;out.push({clef,a:name(down?Bn:A),b:name(down?A:Bn)})}return shuffle(out)},
  show(it,q,fin){const a=N(it.a),b=N(it.b),r=intName(a,b);
    q.innerHTML=`<h3>Welches Intervall ist das?</h3>${staff({clef:it.clef,cols:[{n:[a]},{n:[b]}],sc:2.6})}<div class="keys wide" data-k></div>`;
    const k=q.querySelector("[data-k]");buttons(k,INT.map((x,i)=>[x,`${i+1} ${x}`]),"key",(v,btn)=>{markButtons(k,r,btn);
      const ch=countChain(a,b),same=onLine(it.clef,a)===onLine(it.clef,b);
      fin(v===r,`Zähle von unten nach oben, beide Noten zählen mit: ${ch.map((x,i)=>`${x}&nbsp;(${i+1})`).join(" – ")}. Das sind ${ch.length===1?"zwei gleiche Töne":ch.length+" Töne"} → <b>${r}</b>.${ch.length>1?` <span class="meta">Beide Noten ${same?(onLine(it.clef,a)?"auf Linien":"in Zwischenräumen"):"liegen verschieden (Linie und Zwischenraum)"}: ${same?"ungerade Zahl":"gerade Zahl"}.</span>`:""}`)})}});
const TERZEN=[["c'","e'"],["d'","f'"],["e'","g'"],["f'","a'"],["g'","h'"],["a'","c''"],["h'","d''"],["d'","fis'"],["c'","es'"],["e'","gis'"],["g'","b'"],["a'","cis''"],["fis'","a'"],["f'","as'"],["es'","g'"],["b'","d''"],["c''","e''"],["e''","g''"]];
T["terz"]=()=>({make:()=>shuffle(TERZEN).slice(0,12).map(([a,b])=>({a,b})),
  show(it,q,fin){const r=terz(it.a,it.b),h=semis(it.a,it.b);
    q.innerHTML=`<h3>Große oder kleine Terz?</h3>${staff({clef:"v",cols:[{n:[it.a]},{n:[it.b]}],sc:2.6})}<p class="meta">Die beiden Töne sind auf der Klaviatur gelb. Zähle die Halbtonschritte.</p>${kb({marks:[it.a,it.b]})}<div class="keys wide" data-k></div>`;
    const k=q.querySelector("[data-k]");buttons(k,[["große Terz","große Terz (4 HTS)"],["kleine Terz","kleine Terz (3 HTS)"]],"key",(v,b)=>{markButtons(k,r,b);
      fin(v===r,`Von ${name(it.a)} bis ${name(it.b)} sind es <b>${h} Halbtonschritte</b> → <b>${r}</b>.${kb({marks:[it.a,it.b],count:[it.a,it.b]})}`)})}});
const TRIADS=[["c'",1],["d'",0],["e'",0],["f'",1],["g'",1],["a'",0],["d'",1],["a'",1],["e'",1],["g'",0],["c'",0],["f'",0]];
const BTRIADS=[["c",1],["d",0],["e",0],["F",1],["G",1],["A",0],["D",1],["a",0]];
T["dreiklang"]=()=>({make:()=>shuffle([...shuffle(TRIADS).slice(0,7).map(([r,d])=>({clef:"v",r,d})),...shuffle(BTRIADS).slice(0,3).map(([r,d])=>({clef:"b",r,d}))]),
  show(it,q,fin){const ns=triad(it.r,it.d),A=analyze(ns),ans={};
    q.innerHTML=`<h3>Bestimme den Dreiklang.</h3>${staff({clef:it.clef,cols:[{n:ns}],sc:2.8})}
    <p><b>1. Grundton:</b></p><div class="seg" data-g></div><p><b>2. Untere Terz (zwischen den unteren zwei Tönen):</b></p><div class="seg" data-lo></div>
    <p><b>3. Obere Terz:</b></p><div class="seg" data-hi></div><p><b>4. Tongeschlecht:</b></p><div class="seg" data-tg></div><div class="row"><button class="btn" data-check>Prüfen</button></div>`;
    const TZ=[["große Terz","g3 große Terz"],["kleine Terz","k3 kleine Terz"]];
    seg(q.querySelector("[data-g]"),LETTERS,v=>ans.g=v);seg(q.querySelector("[data-lo]"),TZ,v=>ans.lo=v);seg(q.querySelector("[data-hi]"),TZ,v=>ans.hi=v);seg(q.querySelector("[data-tg]"),[["Dur","Dur"],["Moll","Moll"]],v=>ans.q=v);
    q.querySelector("[data-check]").onclick=()=>{if(!ans.g||!ans.lo||!ans.hi||!ans.q){alert("Beantworte zuerst alle vier Fragen.");return}
      q.querySelectorAll(".seg button").forEach(x=>x.disabled=true);q.querySelector("[data-check]").remove();
      const parts=[["Grundton",ans.g,letter(A.root)],["Untere Terz",ans.lo,A.lo],["Obere Terz",ans.hi,A.hi],["Tongeschlecht",ans.q,A.q]];
      const ok=parts.every(p=>p[1]===p[2]);
      fin(ok,`<ul>${parts.map(p=>`<li>${p[0]}: <b>${p[2]}</b> ${p[1]===p[2]?"✓":"(du: "+p[1]+")"}</li>`).join("")}</ul>Die Töne sind ${ns.map(name).join(" – ")}. Unten ${A.lo}, oben ${A.hi} → <b>${A.name}</b>.`)}}});
const BUILD=[["C-Dur","c'",1],["d-Moll","d'",0],["e-Moll","e'",0],["F-Dur","f'",1],["G-Dur","g'",1],["a-Moll","a'",0],["D-Dur","d'",1],["A-Dur","a'",1],["E-Dur","e'",1],["g-Moll","g'",0]];
const BBUILD=[["C-Dur","c",1],["F-Dur","F",1],["G-Dur","G",1],["a-Moll","A",0],["d-Moll","d",0]];
T["bauen"]=()=>({make:()=>shuffle([...shuffle(BUILD).slice(0,5).map(x=>({clef:"v",x})),...shuffle(BBUILD).slice(0,2).map(x=>({clef:"b",x}))]),
  show(it,q,fin){const [nm,r,d]=it.x,want=triad(r,d),B=BOTTOM[it.clef];
    q.innerHTML=`<h3>Notiere den Dreiklang <span class="nm">${nm}</span>.</h3><p>Der Grundton ist <b>${name(r)}</b>. Tippe die drei Töne ins Notensystem. Tippst du nochmal auf eine Note, ist sie wieder weg. Für ♯ oder ♭ wählst du zuerst das Vorzeichen und tippst dann.</p><div data-p></div><div class="row"><button class="btn" data-check>Prüfen</button></div>`;
    const P=mountPlace(q.querySelector("[data-p]"),{clef:it.clef,multi:true,acc:true,range:[B-3,B+11]});
    q.querySelector("[data-check]").onclick=()=>{const g=P.get();if(g.length<3){alert("Setze drei Noten.");return}
      const isOk=x=>want.some(w=>w.dia===x.dia&&w.alt===x.alt);const ok=g.every(isOk)&&want.every(w=>g.some(x=>x.dia===w.dia&&x.alt===w.alt));
      q.querySelector("[data-check]").remove();P.lock(x=>isOk(x)?"g":"r");
      const msgs=[];g.forEach(x=>{if(!isOk(x)){const w=want.find(w=>w.dia===x.dia);msgs.push(w?`${name(fromDia(x.dia,x.alt))} ist falsch: Hier muss ${w.alt?(w.alt>0?"ein ♯":"ein ♭"):"kein Vorzeichen"} stehen (${name(w)}).`:`${name(fromDia(x.dia,x.alt))} gehört nicht dazu.`)}});
      fin(ok,`${ok?"":`<ul>${msgs.map(m=>`<li>${m}</li>`).join("")}</ul>`}${nm} = ${want.map(name).join(" – ")}. Unten ${d?"große":"kleine"} Terz, oben ${d?"kleine":"große"} Terz.<div data-st="${it.clef}|${want.map(name).join("+")}" data-names></div>`)}}});

/* Liedbegleitung: Töne finden, dann die beste Lage wählen */
const PROG=D.prog;
function chordOpts(sym){const c=chord(sym),r=c.tones[0],other=triad(r,!c.dur),up=fromDia(r.dia+1,0),nb=triad(up,c.dur);
  const f=t=>t.map(letter).join(" – ");const o=[[f(c.tones),1],[f(other),0]];if(f(nb)!==f(c.tones))o.push([f(nb),0]);return o}
T["begleitung"]=()=>{let pi=0;return{pick:true,
  make(){const p=PROG[pi],plan=planVoicing(p.syms);return plan.slice(1).map((x,i)=>({sym:x.sym,prev:plan[i],plan,i:i+1}))},
  after(el){const p=PROG[pi];el.innerHTML=`<p><b>So sieht die ganze Begleitung aus.</b> Unten im Bass steht immer der Grundton.</p><div data-sys="${p.syms.join(" ")}" data-names></div>`;renderStatic(el)},
  setProg(i){pi=i},
  show(it,q,fin){const c=chord(it.sym),ops=shuffle(chordOpts(it.sym));
    q.innerHTML=`<p class="meta">Der Akkord davor:</p><div data-st="v|${it.prev.notes.map(name).join("+")}" data-top="${it.prev.sym}" data-names></div>
    <h3>Nächster Akkord: <span class="nm">${it.sym}</span> <span class="meta">(${c.name})</span></h3><p><b>a) Welche Töne hat der Akkord?</b></p><div class="keys wide" data-t></div><div data-b></div>`;
    renderStatic(q);let okA;
    buttons(q.querySelector("[data-t]"),ops.map(([l,r])=>[r?"1":"0"+l,l]),"key",(v,b)=>{okA=v==="1";markButtons(q.querySelector("[data-t]"),"1",b);
      const cands=shuffle(bestNext(it.prev.notes,it.sym));
      q.querySelector("[data-b]").innerHTML=`${okA?"":`<p class="fb wrong">${c.name} hat die Töne <b>${c.tones.map(letter).join(" – ")}</b>.</p>`}<p><b>b) Welche Lage passt am besten nach dem Akkord davor?</b> Denk an die Regeln: wenig springen, gleiche Töne bleiben liegen.</p><div class="lagen">${cands.map((x,k)=>`<button class="lage" data-k="${k}">${staff({clef:"v",cols:[{n:x.notes}],end:false,sc:2})}</button>`).join("")}</div>`;
      q.querySelectorAll(".lage").forEach(btn=>btn.onclick=()=>{q.querySelectorAll(".lage").forEach(x=>x.disabled=true);
        const ch=cands[+btn.dataset.k],okB=ch.best;cands.forEach((x,k)=>{if(x.best)q.querySelectorAll(".lage")[k].classList.add("right")});if(!okB)btn.classList.add("wrong");
        const desc=x=>`${x.notes.map(name).join(" ")}: ${x.keep?x.keep+(x.keep===1?" Ton bleibt":" Töne bleiben")+" liegen, ":""}zusammen ${x.sum} Halbtonschritte Bewegung`;
        const best=cands.filter(x=>x.best);
        fin(okA&&okB,`${okB?"":"Diese Lage springt zu weit. "}${best.length>1?"Hier passen zwei Lagen gleich gut. ":""}<ul>${cands.slice().sort((a,b)=>a.sum-b.sum).map(x=>`<li${x.best?' class="ok"':""}>${desc(x)}${x.best?" ✓":""}</li>`).join("")}</ul>`)})})}}};

function mountTrainer(el){const kind=el.dataset.trainer,[k,arg]=kind.split("-");const o=T[k](arg);
  if(o.pick){const box=document.createElement("div");box.className="picker";el.before(box);
    const paint=i=>{box.innerHTML=PROG.map((p,j)=>`<button class="${j===i?"cur":""}" data-i="${j}">${p.name}</button>`).join("");
      box.querySelectorAll("button").forEach(b=>b.onclick=()=>{o.setProg(+b.dataset.i);paint(+b.dataset.i);mountRound(el,o)})};paint(0)}
  mountRound(el,o)}

if($("#cards")&&D.cards[page])mountCards($("#cards"),D.cards[page]);
if($("#quiz")){const list=page==="gem"?D.topics.flatMap(t=>D.quiz[t]):D.quiz[page];if(list)mountQuiz($("#quiz"),list,"mus-q-"+page)}
$$("[data-trainer]").forEach(mountTrainer);

/* Lösungen und Drucken */
$$("[data-sol]").forEach(b=>b.onclick=()=>{const on=document.body.classList.toggle("showsol");$$("[data-sol]").forEach(x=>x.textContent=on?"Lösungen verstecken":"Lösungen zeigen")});
$$("[data-print]").forEach(b=>b.onclick=()=>{document.body.dataset.sol=b.dataset.print;window.print()});
window.addEventListener("afterprint",()=>{delete document.body.dataset.sol});
})();
