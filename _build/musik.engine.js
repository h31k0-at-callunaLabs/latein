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
