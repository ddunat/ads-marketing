
<script>
(function(){
  var root=document.getElementById('dci'); if(!root) return;

  /* ---------- language ---------- */
  var KEY='dci-lang';
  function setLang(l){
    root.classList.toggle('is-en',l==='en');
    root.querySelectorAll('.lang button').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.lang===l));});
    root.setAttribute('lang',l);
    try{localStorage.setItem(KEY,l);}catch(e){}
    if(window.__dciRender) window.__dciRender(true);
  }
  root.querySelectorAll('.lang button').forEach(function(b){b.addEventListener('click',function(){setLang(b.dataset.lang);});});
  var saved=null; try{saved=localStorage.getItem(KEY);}catch(e){}

  /* ---------- helpers ---------- */
  function dots(n){return String(n).replace(/\B(?=(\d{3})+(?!\d))/g,'.');}
  function range(a,b){return '€'+dots(a)+' – '+dots(b);}
  function clamp(x,a,b){return x<a?a:x>b?b:x;}
  function ease(x){return x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2;}
  function r100(x){return Math.round(x/100)*100;}

  /* ---------- static service-card costs (below the experience) ---------- */
  root.querySelectorAll('.cost').forEach(function(c){var v=c.querySelector('.v'); if(v) v.textContent=range(+c.dataset.min,+c.dataset.max);});

  /* ---------- scroll-through-the-house ---------- */
  var xp=root.querySelector('.xp'); if(!xp){setLang(saved==='en'?'en':'hr');return;}
  var scroller=xp.querySelector('.xp-scroller'), track=xp.querySelector('.xp-track');
  var scenes=[].slice.call(xp.querySelectorAll('.sc'));
  var panels=[].slice.call(xp.querySelectorAll('.tp'));
  var marks=[].slice.call(xp.querySelectorAll('.xp-house .mk'));
  var lvlEl=xp.querySelector('.xp-lvl'), houseLbl=xp.querySelector('.xp-houselbl'), stepEl=xp.querySelector('.xp-step');
  var totalEl=xp.querySelector('.xp-total b'), bigEl=document.getElementById('dci-total');
  var prog=xp.querySelector('.xp-prog span'), hint=xp.querySelector('.xp-hint'), endEl=xp.querySelector('.xp-end');
  var LV={hr:['Vanjski pregled','Balkon','Krov','Kupaonica','Prizemlje','Podovi','Konstrukcija','Temelji','Ukupno','Novogradnja'],
          en:['Exterior','Balcony','Roof','Bathroom','Ground floor','Floors','Structure','Foundations','Total','New build']};

  var starts=[],lens=[],T=0, sumMin=0,sumMax=0;
  scenes.forEach(function(s){var l=+s.dataset.len||1.6; starts.push(T); lens.push(l); T+=l; sumMin+=(+s.dataset.min||0); sumMax+=(+s.dataset.max||0);});
  var FADE=0.3;
  var pageMode=(window.self===window.top);
  if(pageMode) xp.classList.add('page');
  var H=720;

  function size(){
    var w=root.clientWidth||window.innerWidth;
    if(pageMode){ H=window.innerHeight; }
    else { H = w<700 ? Math.round(clamp(w*1.85,600,780)) : Math.round(clamp(w*0.56,560,820)); }
    xp.style.setProperty('--stage-h',H+'px');
    xp.style.setProperty('--steps',(T+1).toFixed(3));
    render(true);
  }
  function progress(){
    if(pageMode){ var r=track.getBoundingClientRect(); return clamp(-r.top/H,0,T); }
    return clamp(scroller.scrollTop/H,0,T);
  }

  var last=-1, ticking=false;
  function render(force){
    var t=progress(); if(!force && Math.abs(t-last)<0.0005) return; last=t;
    var lang=root.classList.contains('is-en')?'en':'hr';
    var active=0, runMin=0, runMax=0;
    for(var i=0;i<scenes.length;i++){
      var s=scenes[i], u=(t-starts[i])/lens[i];
      var op = i===0 ? 1 : clamp((t-starts[i]+FADE)/FADE,0,1);
      var next = i<scenes.length-1 ? clamp((t-starts[i+1]+FADE)/FADE,0,1) : 0;
      var vis = op>0 && next<1;
      s.classList.toggle('vis',vis);
      s.style.opacity=op;
      if(t>=starts[i]-FADE*0.5) active=i;
      if(!vis) continue;
      /* camera push-in */
      var cam=s.firstElementChild, k=clamp(u,-0.2,1.05);
      var sc=1.03+0.11*ease(clamp((k+0.2)/1.25,0,1));
      var dx=(s.dataset.key==='hero'?-1.5:0.8)*clamp(k,0,1), dy=-0.8*clamp(k,0,1);
      cam.style.transform='translate3d('+dx+'%,'+dy+'%,0) scale('+sc.toFixed(4)+')';
      /* scanner wipe A -> B */
      var b=s.querySelector('.b'), bar=s.querySelector('.bar');
      if(b){
        var w=clamp((u-0.18)/0.6,0,1), we=ease(w);
        b.style.clipPath='inset(0 0 '+((1-we)*100).toFixed(2)+'% 0)';
        if(bar){bar.style.height=(we*100).toFixed(2)+'%'; bar.style.opacity=(w>0&&w<1)?1:0;}
        s.classList.toggle('revealed',w>=0.98);
      }
    }
    /* running damage total: completed stops plus the one being revealed */
    for(var j=0;j<scenes.length;j++){
      var mn=+scenes[j].dataset.min||0, mx=+scenes[j].dataset.max||0; if(!mx) continue;
      var f=ease(clamp(((t-starts[j])/lens[j]-0.18)/0.6,0,1));
      runMin+=mn*f; runMax+=mx*f;
      var pv=panels[j]&&panels[j].querySelector('.xcost .v');
      if(pv) pv.textContent=range(r100(mn*f),r100(mx*f));
    }
    if(totalEl) totalEl.textContent='€'+dots(r100(runMin))+' – '+dots(r100(runMax));
    if(bigEl){ var ti=scenes.findIndex(function(x){return x.dataset.key==='tally';}); var tf=ti<0?1:ease(clamp((t-starts[ti])/(lens[ti]*0.55),0,1)); bigEl.textContent=range(r100(sumMin*Math.max(tf,0)),r100(sumMax*Math.max(tf,0))); }
    /* panels, labels, house */
    panels.forEach(function(p,ix){p.classList.toggle('on',ix===active);});
    var lv=+scenes[active].dataset.level||0;
    if(lvlEl) lvlEl.textContent=LV[lang][lv];
    if(houseLbl) houseLbl.textContent=LV[lang][lv];
    marks.forEach(function(m){var mi=+m.dataset.m; m.classList.toggle('on',mi===lv); m.classList.toggle('done',mi>0&&mi<lv);});
    if(stepEl) stepEl.textContent=(lv>=1&&lv<=7)?('0'+lv+' / 07'):(lv===0?(lang==='hr'?'Početak':'Start'):(lv===8?(lang==='hr'?'Zbroj':'Total'):(lang==='hr'?'Bonus':'Bonus')));
    if(prog) prog.style.width=(t/T*100).toFixed(2)+'%';
    if(hint) hint.style.opacity=clamp(1-t/0.25,0,1);
    if(endEl) endEl.classList.toggle('on',t>T-0.35);
  }
  window.__dciRender=render;

  function onScroll(){ if(!ticking){ticking=true; requestAnimationFrame(function(){ticking=false; render(false);});} }
  if(pageMode) window.addEventListener('scroll',onScroll,{passive:true}); else scroller.addEventListener('scroll',onScroll,{passive:true});
  window.addEventListener('resize',function(){size(); postHeight();});

  xp.querySelector('.xp-skip').addEventListener('click',function(){
    if(pageMode){ var r=track.getBoundingClientRect(); window.scrollTo({top:window.scrollY+r.bottom-H+2,behavior:'smooth'}); }
    else scroller.scrollTo({top:scroller.scrollHeight,behavior:'smooth'});
  });

  setLang(saved==='en'?'en':'hr');
  size();

  /* let a listening host page size the embed */
  function postHeight(){ try{ if(window.parent&&window.parent!==window) window.parent.postMessage({type:'dci-height',height:document.documentElement.scrollHeight},'*'); }catch(e){} }
  window.addEventListener('load',postHeight);
})();
</script>
