(function(){
const D=__DATA__;
const page=document.body.dataset.page;
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
function store(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem(k));localStorage.setItem(k,JSON.stringify(v))}catch(e){return null}}
function shuffle(a){a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}

/* Haken: welche Schritte sind fertig */
const DONE=new Set(store("bio-themen")||[]);
const saveDone=()=>store("bio-themen",[...DONE]);
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

/* Tippen sicher erkennen: Nach einem Zieh-Vorgang verschluckt der Browser manchmal den nächsten Klick. */
function onTap(el,fn){let t=null,last=0;const run=e=>{const n=Date.now();if(n-last<450)return;last=n;fn(e)};
  el.addEventListener("click",e=>{clearTimeout(t);run(e)});
  el.addEventListener("pointerup",e=>{if(e.pointerType==="mouse")return;clearTimeout(t);t=setTimeout(()=>run(e),280)})}

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

/* Quiz: Die erste Antwort ist die richtige, die Reihenfolge wird gemischt. */
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

/* Zuordnen / Beschriften: Wörter mit dem Finger auf die Felder ziehen (oder antippen, dann Feld antippen). */
function mountMatch(el,M,key){
  const W=M.slots.map(s=>s[1]);                       // jedes Wort gibt es genau einmal
  let put,picked,checked;
  const reset=()=>{put=M.slots.map(()=>null);picked=null;checked=false};reset();
  const order=shuffle(W.map((_,i)=>i));
  el.innerHTML=(M.fig||"")+`<p class="hint">👆 <b>${M.how||"Zieh jedes Wort auf das passende Feld."}</b> Oder: Wort antippen, dann Feld antippen. Falsch hingelegt? Tippe das Wort im Feld an, dann geht es zurück.</p>
<div class="mslots ${M.wide?"wide":""}"></div><p class="meta" data-tip aria-live="polite"></p><div class="mtray" aria-label="Wörter zum Ziehen"></div>
<div class="row"><button class="btn" data-check>Prüfen</button><button class="btn ghost" data-clear>Alles leeren</button></div><div data-fb></div>`;
  const S=el.querySelector(".mslots"),T=el.querySelector(".mtray"),FB=el.querySelector("[data-fb]");
  S.innerHTML=M.slots.map((s,i)=>`<div class="mslot" data-s="${i}" role="button" tabindex="0"><span class="mlab">${s[0]}</span><span class="mval"></span></div>`).join("");
  const slots=[...S.querySelectorAll(".mslot")];
  const slotAt=(x,y)=>slots.find(z=>{const r=z.getBoundingClientRect();return x>=r.left-6&&x<=r.right+6&&y>=r.top-6&&y<=r.bottom+6});
  function unmark(){if(checked){checked=false;FB.innerHTML=""}}
  function paint(){
    slots.forEach((z,i)=>{const k=put[i],v=z.querySelector(".mval");
      if(k===null){v.innerHTML='<span class="empty">hierhin ziehen</span>';z.classList.remove("ok","no")}
      else{v.innerHTML=`<button class="word placed" data-k="${k}" data-from="${i}">${W[k]}</button>`;
        z.classList.toggle("ok",checked&&k===i);z.classList.toggle("no",checked&&k!==i)}
      z.classList.toggle("armed",picked!==null&&k===null)});
    const free=order.filter(k=>!put.includes(k));
    T.innerHTML=free.length?free.map(k=>`<button class="word${picked===k?" picked":""}" data-k="${k}">${W[k]}</button>`).join(""):'<p class="meta" style="margin:.2rem">Alle Wörter liegen. Tippe auf „Prüfen“.</p>';
    el.querySelectorAll(".word").forEach(bind);
    el.querySelector("[data-tip]").textContent=picked!==null?"Tippe jetzt auf das passende Feld.":"";
  }
  function place(k,to,from){
    if(from!==null&&from!==to){put[from]=put[to]}       // tauschen, wenn das Ziel schon belegt ist
    put[to]=k;picked=null;unmark();paint();
  }
  function bind(b){
    b.addEventListener("pointerdown",e=>{
      if(e.button>0)return;
      const k=+b.dataset.k,from=b.dataset.from!==undefined?+b.dataset.from:null,sx=e.clientX,sy=e.clientY;let moved=false,ghost=null;
      try{b.setPointerCapture(e.pointerId)}catch(_){}
      const over=z=>slots.forEach(x=>x.classList.toggle("over",x===z));
      const move=ev=>{
        if(!moved&&Math.hypot(ev.clientX-sx,ev.clientY-sy)<8)return;
        if(!moved){moved=true;ghost=b.cloneNode(true);ghost.classList.add("ghost");ghost.style.width=b.offsetWidth+"px";document.body.appendChild(ghost);b.classList.add("dragging")}
        ghost.style.left=ev.clientX+"px";ghost.style.top=ev.clientY+"px";over(slotAt(ev.clientX,ev.clientY));ev.preventDefault()};
      const end=ev=>{
        b.removeEventListener("pointermove",move);b.removeEventListener("pointerup",end);b.removeEventListener("pointercancel",end);
        if(ghost)ghost.remove();b.classList.remove("dragging");over(null);
        if(ev.type==="pointercancel")return;
        if(!moved){if(from!==null&&picked!==null&&picked!==k){place(picked,from,null)}else if(from!==null){put[from]=null;unmark();paint()}else{picked=picked===k?null:k;paint()}return}
        const z=slotAt(ev.clientX,ev.clientY);
        if(z)place(k,+z.dataset.s,from);else if(from!==null){put[from]=null;unmark();paint()}};
      b.addEventListener("pointermove",move);b.addEventListener("pointerup",end);b.addEventListener("pointercancel",end);
    });
    b.addEventListener("click",e=>{if(e.detail!==0)return;const k=+b.dataset.k;   // Tastatur
      if(b.dataset.from!==undefined){put[+b.dataset.from]=null;unmark()}else picked=picked===k?null:k;paint()});
  }
  slots.forEach(z=>{const go=()=>{if(picked!==null)place(picked,+z.dataset.s,null)};
    onTap(z,e=>{if(e.target.closest&&e.target.closest(".placed"))return;go()});
    z.addEventListener("keydown",e=>{if(e.target===z&&(e.key==="Enter"||e.key===" ")){e.preventDefault();go()}})});
  onTap(el.querySelector("[data-clear]"),()=>{reset();FB.innerHTML="";paint()});
  onTap(el.querySelector("[data-check]"),()=>{
    const empty=put.filter(k=>k===null).length,bad=put.filter((k,i)=>k!==null&&k!==i).length,ok=!empty&&!bad;
    checked=true;picked=null;paint();
    if(ok){const d=store(key)||[];if(!d.includes(M.id)){d.push(M.id);store(key,d)}}
    const msgs=[];if(bad)msgs.push(`${bad===1?"1 Wort liegt":bad+" Wörter liegen"} falsch (rot). Tippe ${bad===1?"es":"sie"} an und versuch es nochmal.`);
    if(empty)msgs.push(`${empty===1?"1 Feld ist":empty+" Felder sind"} noch leer.`);
    FB.innerHTML=`<div class="fb ${ok?"right":"wrong"}"><b>${ok?"Alles richtig! 🎉":"Noch nicht ganz."}</b>${ok?(M.why?`<p style="margin-bottom:0">${M.why}</p>`:""):"<ul>"+msgs.map(m=>`<li>${m}</li>`).join("")+"</ul>"}</div>${ok?"":`<details class="loes"><summary>Ich komme nicht weiter: Lösung ansehen</summary><ul>${M.slots.map(s=>`<li><b>${s[0]}</b>: ${s[1]}</li>`).join("")}</ul></details>`}`;
  });
  paint();
}

/* Sortieren: Kärtchen in Gruppen ziehen (oder antippen, dann Gruppe antippen). */
function mountSort(el,S,key){
  const I=S.items;let put,picked,checked;
  const reset=()=>{put=I.map(()=>null);picked=null;checked=false};reset();
  const order=shuffle(I.map((_,i)=>i));
  el.innerHTML=`<p class="hint">👆 <b>${S.how}</b> Oder: Kärtchen antippen, dann Gruppe antippen. Falsch einsortiert? Kärtchen antippen, dann geht es zurück.</p>
<div class="sbins" style="--n:${S.bins.length}">${S.bins.map((b,i)=>`<div class="sbin" data-b="${i}" role="button" tabindex="0"><div class="sbl">${b}</div><div class="sbody"></div></div>`).join("")}</div>
<p class="meta" data-tip aria-live="polite"></p><div class="mtray"></div>
<div class="row"><button class="btn" data-check>Prüfen</button><button class="btn ghost" data-clear>Alles leeren</button></div><div data-fb></div>`;
  const bins=[...el.querySelectorAll(".sbin")],T=el.querySelector(".mtray"),FB=el.querySelector("[data-fb]");
  const binAt=(x,y)=>bins.find(z=>{const r=z.getBoundingClientRect();return x>=r.left-6&&x<=r.right+6&&y>=r.top-6&&y<=r.bottom+6});
  function unmark(){if(checked){checked=false;FB.innerHTML=""}}
  function paint(){
    bins.forEach((z,b)=>{const ks=order.filter(k=>put[k]===b);
      z.querySelector(".sbody").innerHTML=ks.length?ks.map(k=>`<button class="word placed${checked?(I[k][1]===b?" ok":" no"):""}" data-k="${k}" data-from="${b}">${I[k][0]}${checked?(I[k][1]===b?" ✓":" ✕"):""}</button>`).join(""):'<span class="empty">hierhin ziehen</span>';
      z.classList.toggle("armed",picked!==null)});
    const free=order.filter(k=>put[k]===null);
    T.innerHTML=free.length?free.map(k=>`<button class="word${picked===k?" picked":""}" data-k="${k}">${I[k][0]}</button>`).join(""):'<p class="meta" style="margin:.2rem">Alle Kärtchen liegen. Tippe auf „Prüfen“.</p>';
    el.querySelectorAll(".word").forEach(bind);
    el.querySelector("[data-tip]").textContent=picked!==null?"Tippe jetzt auf die passende Gruppe.":"";
  }
  function place(k,b){put[k]=b;picked=null;unmark();paint()}
  function bind(w){
    w.addEventListener("pointerdown",e=>{
      if(e.button>0)return;
      const k=+w.dataset.k,from=w.dataset.from!==undefined,sx=e.clientX,sy=e.clientY;let moved=false,ghost=null;
      try{w.setPointerCapture(e.pointerId)}catch(_){}
      const over=z=>bins.forEach(x=>x.classList.toggle("over",x===z));
      const move=ev=>{
        if(!moved&&Math.hypot(ev.clientX-sx,ev.clientY-sy)<8)return;
        if(!moved){moved=true;ghost=w.cloneNode(true);ghost.classList.add("ghost");ghost.style.width=w.offsetWidth+"px";document.body.appendChild(ghost);w.classList.add("dragging")}
        ghost.style.left=ev.clientX+"px";ghost.style.top=ev.clientY+"px";over(binAt(ev.clientX,ev.clientY));ev.preventDefault()};
      const end=ev=>{
        w.removeEventListener("pointermove",move);w.removeEventListener("pointerup",end);w.removeEventListener("pointercancel",end);
        if(ghost)ghost.remove();w.classList.remove("dragging");over(null);
        if(ev.type==="pointercancel")return;
        if(!moved){if(from&&picked!==null&&picked!==k){place(picked,put[k])}else if(from){put[k]=null;unmark();paint()}else{picked=picked===k?null:k;paint()}return}
        const z=binAt(ev.clientX,ev.clientY);
        if(z)place(k,+z.dataset.b);else if(from){put[k]=null;unmark();paint()}};
      w.addEventListener("pointermove",move);w.addEventListener("pointerup",end);w.addEventListener("pointercancel",end);
    });
    w.addEventListener("click",e=>{if(e.detail!==0)return;const k=+w.dataset.k;
      if(w.dataset.from!==undefined){put[k]=null;unmark()}else picked=picked===k?null:k;paint()});
  }
  bins.forEach(z=>{const go=()=>{if(picked!==null)place(picked,+z.dataset.b)};
    onTap(z,e=>{if(e.target.closest&&e.target.closest(".placed"))return;go()});
    z.addEventListener("keydown",e=>{if(e.target===z&&(e.key==="Enter"||e.key===" ")){e.preventDefault();go()}})});
  onTap(el.querySelector("[data-clear]"),()=>{reset();FB.innerHTML="";paint()});
  onTap(el.querySelector("[data-check]"),()=>{
    const empty=put.filter(b=>b===null).length,bad=put.filter((b,k)=>b!==null&&b!==I[k][1]).length,ok=!empty&&!bad;
    checked=true;picked=null;paint();
    if(ok){const d=store(key)||[];if(!d.includes(S.id)){d.push(S.id);store(key,d)}}
    const msgs=[];if(bad)msgs.push(`${bad===1?"1 Kärtchen liegt":bad+" Kärtchen liegen"} in der falschen Gruppe (rot ✕). Tippe ${bad===1?"es":"sie"} an und versuch es nochmal.`);
    if(empty)msgs.push(`${empty===1?"1 Kärtchen fehlt":empty+" Kärtchen fehlen"} noch.`);
    FB.innerHTML=`<div class="fb ${ok?"right":"wrong"}"><b>${ok?"Alles richtig! 🎉":"Noch nicht ganz."}</b>${ok?(S.why?`<p style="margin-bottom:0">${S.why}</p>`:""):"<ul>"+msgs.map(m=>`<li>${m}</li>`).join("")+"</ul>"}</div>${ok?"":`<details class="loes"><summary>Ich komme nicht weiter: Lösung ansehen</summary>${S.bins.map((b,i)=>`<p><b>${b}:</b> ${I.filter(x=>x[1]===i).map(x=>x[0]).join(" · ")}</p>`).join("")}</details>`}`;
  });
  paint();
}

/* Gesamtvergrößerung rechnen */
function mountCalc(el){
  const OK=[5,10,15],OB=[4,10,40,100];let a,b,n=0,right=0;
  el.innerHTML=`<div class="box"><p class="meta" data-c></p><h3 data-q></h3><div class="row calc"><input type="text" inputmode="numeric" pattern="[0-9]*" autocomplete="off" aria-label="Gesamtvergrößerung" data-in><span class="x">-fach</span><button class="btn" data-go>Prüfen</button></div><div data-fb></div></div>`;
  const inp=el.querySelector("[data-in]"),fb=el.querySelector("[data-fb]");
  function nu(){let na,nb;do{na=OK[Math.floor(Math.random()*OK.length)];nb=OB[Math.floor(Math.random()*OB.length)]}while(na===a&&nb===b);a=na;b=nb;
    el.querySelector("[data-q]").innerHTML=`Okular: <b>${a}-fach</b> · Objektiv: <b>${b}-fach</b><br>Wie stark ist die Gesamtvergrößerung?`;
    el.querySelector("[data-c]").textContent=n?`${right} von ${n} richtig`:"";inp.value="";fb.innerHTML="";inp.disabled=false;el.querySelector("[data-go]").hidden=false}
  function go(){const v=parseInt(inp.value.replace(/\D/g,""),10);if(isNaN(v)){inp.focus();return}
    n++;const ok=v===a*b;if(ok)right++;inp.disabled=true;el.querySelector("[data-go]").hidden=true;
    fb.innerHTML=`<div class="fb ${ok?"right":"wrong"}"><b>${ok?"Richtig!":"Nicht ganz."}</b> ${a} · ${b} = <b>${a*b}</b>. Die Gesamtvergrößerung ist ${a*b}-fach.</div><div class="row"><button class="btn" data-nx>Nächste Aufgabe</button></div>`;
    el.querySelector("[data-c]").textContent=`${right} von ${n} richtig`;
    el.querySelector("[data-nx]").onclick=nu}
  el.querySelector("[data-go]").onclick=go;inp.addEventListener("keydown",e=>{if(e.key==="Enter")go()});
  nu();
}

if($("#cards")&&D.cards[page])mountCards($("#cards"),D.cards[page]);
if($("#quiz")){const list=page==="gem"?D.topics.flatMap(t=>D.quiz[t]):D.quiz[page];if(list)mountQuiz($("#quiz"),list,"bio-q-"+page)}
$$("[data-match]").forEach(el=>{const M=D.match[el.dataset.match];if(M)mountMatch(el,M,"bio-match")});
$$("[data-sort]").forEach(el=>{const S=D.sort[el.dataset.sort];if(S)mountSort(el,S,"bio-sort")});
$$("[data-calc]").forEach(mountCalc);

/* Lösungen und Drucken */
$$("[data-sol]").forEach(b=>b.onclick=()=>{const on=document.body.classList.toggle("showsol");$$("[data-sol]").forEach(x=>x.textContent=on?"Lösungen verstecken":"Lösungen zeigen")});
$$("[data-print]").forEach(b=>b.onclick=()=>{document.body.dataset.sol=b.dataset.print;window.print()});
window.addEventListener("afterprint",()=>{delete document.body.dataset.sol});
})();
