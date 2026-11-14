(function(){
const D=__DATA__;
const page=document.body.dataset.page;
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
function store(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem(k));localStorage.setItem(k,JSON.stringify(v))}catch(e){return null}}
function shuffle(a){a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}

/* Haken: welche Schritte sind fertig */
const DONE=new Set(store("chem-themen")||[]);
const saveDone=()=>store("chem-themen",[...DONE]);
$$("[data-finish]").forEach(a=>a.addEventListener("click",()=>{DONE.add(a.dataset.finish);saveDone()}));
function paintDone(){
  const steps=$$("a.step[data-step]");
  let next=false;
  steps.forEach(s=>{const d=DONE.has(s.dataset.step);s.classList.toggle("done",d);s.classList.remove("next");if(!d&&!next){s.classList.add("next");next=true}});
  const left=D.steps.filter(id=>!DONE.has(id)).length;
  if($("#st-left"))$("#st-left").textContent=left?`Noch ${left} von ${D.steps.length} Schritten.`:"";
  if($("#st-all"))$("#st-all").hidden=left>0;
}
if(page==="start"){paintDone();$("#st-reset").onclick=()=>{DONE.clear();saveDone();paintDone()}}
const cur=$("nav [aria-current]");if(cur&&cur.scrollIntoView)try{cur.scrollIntoView({inline:"center",block:"nearest"})}catch(e){}

/* Pfeil-Bilder */
const E={ed:["Enthal\u00adpie der Edukte","chem"],pr:["Enthal\u00adpie der Pro\u00addukte","chem"],th:["ther\u00admische Ener\u00adgie","th"],st:["Strah\u00adlungs\u00adener\u00adgie","st"],el:["elek\u00adtrische Ener\u00adgie","el"],be:["Bewe\u00adgungs\u00adener\u00adgie","be"],sc:["Schall\u00adener\u00adgie","sc"]};
const ORDER=["ed","pr","th","st","el","be","sc"];
function diag(pre,mid,post){const a=k=>`<div class="arrow e-${E[k][1]}">${E[k][0]}</div>`;
  return `<div class="diag"><div class="col">${pre.map(a).join("")}</div><div class="mid">${mid}</div><div class="col">${post.map(a).join("")}</div></div>`}
const SC=[
 {id:"feuer",name:"Lagerfeuer",text:"Holz brennt in einem Lagerfeuer. Es wurde mit einem Streichholz angezündet. Das Feuer leuchtet und gibt Wärme ab.",mid:"Chemische Reaktion (Ver\u00adbrennung)",pre:["ed","th"],post:["pr","th","st"],typ:"exo",why:"Zum Anzünden wird etwas Wärme zugeführt. Abgegeben werden viel Wärme und Licht. Deshalb ist die Verbrennung exotherm."},
 {id:"luminol",name:"Luminol",text:"Luminol reagiert und leuchtet blau. Die Temperatur ändert sich dabei nicht.",mid:"Chemische Reaktion",pre:["ed"],post:["pr","st"],typ:"exo",why:"Die Energie wird als Licht abgegeben, also exotherm. Weil es nicht wärmer wird, steht rechts keine thermische Energie."},
 {id:"ki",name:"Kaliumiodid lösen",text:"Kaliumiodid wird in Wasser gelöst. Die Lösung ist danach kälter als die Ausgangsstoffe.",mid:"Löse\u00advorgang",pre:["ed","th"],post:["pr"],typ:"endo",why:"Wärme wird aus der Umgebung aufgenommen, deshalb wird die Lösung kälter. Das ist endotherm."},
 {id:"knall",name:"Knalldose",text:"In der Knalldose wird ein Gasgemisch mit einem Zündfunken angezündet. Es gibt einen Lichtblitz und einen Knall, der Deckel fliegt weg, und die Dose wird wärmer.",mid:"Chemische Reaktion (Explosion)",pre:["ed","th"],post:["pr","th","st","be","sc"],typ:"exo",why:"Energie wird als Wärme, Licht, Bewegung des Deckels und Schall abgegeben. Das ist exotherm."},
 {id:"hand",name:"Handwärmer",text:"In einem Einmal-Handwärmer rostet Eisenpulver, sobald man die Packung öffnet. Der Handwärmer wird warm.",mid:"Chemische Reaktion (Rosten)",pre:["ed"],post:["pr","th"],typ:"exo",why:"Energie wird als Wärme abgegeben. Das ist exotherm."},
 {id:"led",name:"LED-Lampe",text:"Eine LED-Lampe ist eingeschaltet. Sie leuchtet und wird etwas warm.",mid:"Lampe (LED)",pre:["el"],post:["th","st"],typ:null,why:"Die LED ist ein Energiewandler. Es entsteht kein neuer Stoff, deshalb ist das keine chemische Reaktion."}
];
const DG=Object.fromEntries(SC.map(s=>[s.id,[s.pre,s.mid,s.post]]));
DG.wunder=[["ed","th"],"Chemische Reaktion (Ver\u00adbrennung)",["pr","th","st","sc"]];
DG.kuehl=[["ed","th"],"Löse\u00advorgang",["pr"]];
$$("[data-diag]").forEach(el=>{const d=DG[el.dataset.diag];if(d)el.innerHTML=diag(...d)});

/* Karten */
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

/* Quiz */
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
    const [q,opts,ex]=QZ[qs[qi]];const order=shuffle(opts.map((_,i)=>i));
    el.innerHTML=`<p class="meta">Frage ${qi+1} von ${qs.length}</p><div class="bar"><i style="width:${qi/qs.length*100}%"></i></div><div class="box"><h3>${q}</h3>${order.map(i=>`<button class="opt" data-i="${i}">${opts[i]}</button>`).join("")}<div data-fb></div></div>`;
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

/* Pfeil-Bilder bauen */
function mountBau(){
  let cur=0,sel;const done=new Set(store("chem-bau")||[]);
  const reset=()=>{sel={pre:new Set(),post:new Set(),typ:null}};reset();
  function pick(){$("#b-pick").innerHTML=SC.map((s,i)=>`<button class="${i===cur?"cur":""} ${done.has(s.id)?"done":""}" data-i="${i}">${s.name}</button>`).join("");
    $$("#b-pick button").forEach(b=>b.onclick=()=>{cur=+b.dataset.i;reset();render()})}
  function render(){
    pick();const s=SC[cur],A=$("#b-area");
    const chips=side=>ORDER.map(k=>`<button class="chip e-${E[k][1]}" data-side="${side}" data-k="${k}" aria-pressed="${sel[side].has(k)}">${E[k][0]}</button>`).join("");
    A.innerHTML=`<h3>${s.name}</h3><p>${s.text}</p><p><b>Vorher (links):</b></p><div class="chips">${chips("pre")}</div><p><b>Nachher (rechts):</b></p><div class="chips">${chips("post")}</div>${s.typ?`<p><b>Der Vorgang ist …</b></p><div class="seg"><button data-t="exo" aria-pressed="false">exotherm</button><button data-t="endo" aria-pressed="false">endotherm</button></div>`:""}<div class="row"><button class="btn" data-check>Prüfen</button></div><div data-fb></div>`;
    A.querySelectorAll(".chip").forEach(c=>c.onclick=()=>{const set=sel[c.dataset.side],k=c.dataset.k;set.has(k)?set.delete(k):set.add(k);c.setAttribute("aria-pressed",set.has(k))});
    A.querySelectorAll(".seg button").forEach(b=>b.onclick=()=>{sel.typ=b.dataset.t;A.querySelectorAll(".seg button").forEach(x=>x.setAttribute("aria-pressed",x===b))});
    A.querySelector("[data-check]").onclick=check;
  }
  function check(){
    const s=SC[cur],msgs=[],A=$("#b-area");
    const cmp=(side,want,label)=>{const miss=want.filter(k=>!sel[side].has(k)),extra=[...sel[side]].filter(k=>!want.includes(k));
      if(miss.length)msgs.push(`${label} fehlt: ${miss.map(k=>E[k][0]).join(", ")}`);
      if(extra.length)msgs.push(`${label} gehört nicht dazu: ${extra.map(k=>E[k][0]).join(", ")}`)};
    cmp("pre",s.pre,"Vorher");cmp("post",s.post,"Nachher");
    if(s.typ&&sel.typ!==s.typ)msgs.push(sel.typ?`Der Vorgang ist ${s.typ==="exo"?"exotherm":"endotherm"}.`:"Entscheide noch: exotherm oder endotherm?");
    const ok=!msgs.length;if(ok){done.add(s.id);store("chem-bau",[...done]);pick()}
    A.querySelector("[data-fb]").innerHTML=`<div class="fb ${ok?"right":"wrong"}"><b>${ok?"Alles richtig.":"Noch nicht ganz."}</b>${ok?"":"<ul>"+msgs.map(m=>`<li>${m}</li>`).join("")+"</ul>"}<p style="margin-bottom:0">${s.why}</p></div><p class="meta">So sieht es richtig aus:</p>${diag(s.pre,s.mid,s.post)}${s.typ?`<p><span class="badge b-${s.typ}">${s.typ==="exo"?"exotherm":"endotherm"}</span></p>`:""}${cur<SC.length-1?'<div class="row"><button class="btn" data-nextb>Nächstes Pfeil-Bild</button></div>':'<p><b>Das war das letzte Pfeil-Bild.</b> Weiter geht es unten mit dem Quiz.</p>'}`;
    const n=A.querySelector("[data-nextb]");if(n)n.onclick=()=>{cur++;reset();render();$("#b-pick").scrollIntoView&&$("#b-pick").scrollIntoView({block:"start"})};
  }
  render();
}

if($("#cards")&&D.cards[page])mountCards($("#cards"),D.cards[page]);
if($("#quiz")){const list=page==="gem"?D.topics.flatMap(t=>D.quiz[t]):D.quiz[page];if(list)mountQuiz($("#quiz"),list,"chem-q-"+page)}
if($("#b-area"))mountBau();

/* Lösungen und Drucken */
$$("[data-sol]").forEach(b=>b.onclick=()=>{const on=document.body.classList.toggle("showsol");$$("[data-sol]").forEach(x=>x.textContent=on?"Lösungen verstecken":"Lösungen zeigen")});
$$("[data-print]").forEach(b=>b.onclick=()=>{document.body.dataset.sol=b.dataset.print;window.print()});
window.addEventListener("afterprint",()=>{delete document.body.dataset.sol});
})();
