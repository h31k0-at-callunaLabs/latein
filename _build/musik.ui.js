/* ===== Musik: Darstellung und Übungen im Browser ===== */
(function(){
const D=__DATA__,GL=__GLYPHS__;
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
