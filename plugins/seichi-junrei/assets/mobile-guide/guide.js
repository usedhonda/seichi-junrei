(()=>{'use strict';
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const data=JSON.parse($('#guide-data').textContent),viewIds=data.navigation.map(x=>x.id);
const media={...(data.supportArt||{})};$$('img[data-art]').forEach(i=>{if(!media[i.dataset.art])media[i.dataset.art]={src:i.src,alt:i.alt};});
const originalHtml='<!doctype html>\n'+document.documentElement.outerHTML;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const storageKey='pilgrimage:'+data.guideId;let saved={},storageOK=true;
const validMissions=new Set(data.missions.map(m=>m.id));
const validBookmarks=new Set(data.stages.map(x=>x.id));
try{
 const raw=JSON.parse(localStorage.getItem(storageKey)||'{}');
 if(raw&&typeof raw==='object'&&!Array.isArray(raw))saved=raw;
 // Reading may be allowed even when writes are blocked. Probe without changing progress.
 const probe=storageKey+':write-test';localStorage.setItem(probe,'1');localStorage.removeItem(probe);
}catch(e){storageOK=false;}
const done=new Set((Array.isArray(saved.done)?saved.done:[]).filter(id=>validMissions.has(id)));
const bookmarks=new Set((Array.isArray(saved.bookmarks)?saved.bookmarks:[]).filter(id=>validBookmarks.has(id)));
const prefersReduced=matchMedia('(prefers-reduced-motion: reduce)');
let motion=saved.motion!==false&&!prefersReduced.matches;
function store(){try{localStorage.setItem(storageKey,JSON.stringify({done:[...done],bookmarks:[...bookmarks],motion}));storageOK=true;}catch(e){storageOK=false;}syncStorageNotice();}
function setMotion(){document.body.dataset.motion=motion?'on':'off';$$('[data-action="motion"]').forEach(b=>{b.textContent=motion?'ON':'OFF';b.setAttribute('aria-pressed',String(motion));});if(!motion)$$('.reveal.waiting').forEach(el=>{el.classList.remove('waiting');el.classList.add('entered');});}
prefersReduced.addEventListener?.('change',e=>{if(e.matches){motion=false;setMotion();}});
function missionStats(scope){
 const ids=new Set(scope?$$('[data-mission]',scope).map(i=>i.dataset.mission).filter(id=>validMissions.has(id)):validMissions);
 return {count:[...ids].filter(id=>done.has(id)).length,total:ids.size};
}
function syncStorageNotice(){
 const message=storageOK?'チェックはこのブラウザに保存されます。仲間の端末とは同期しません。':'この画面内のチェックは使えますが、この表示では再読み込み後の保存ができません。Safariなどのブラウザで開いてください。';
 $$('[data-mission-storage]').forEach(n=>n.textContent=message);
}
function sync(){
 $$('[data-mission]').forEach(i=>{i.checked=done.has(i.dataset.mission);i.closest('.mission')?.classList.toggle('is-done',i.checked);});
 $$('[data-mission-scope]').forEach(group=>{
  const {count,total}=missionStats(group),label=group.dataset.missionLabel||'';
  const counter=$('[data-mission-count]',group);if(counter)counter.textContent=label+' '+count+' / '+total+' 完了';
  const progress=$('[data-mission-progress]',group);if(progress)progress.style.width=(total?100*count/total:0)+'%';
  const meter=$('[data-mission-meter]',group);if(meter){meter.setAttribute('aria-valuemax',String(total));meter.setAttribute('aria-valuenow',String(count));meter.setAttribute('aria-valuetext',count+' / '+total+' 完了');}
 });
 const global=missionStats();$$('[data-mission-menu-count]').forEach(n=>n.textContent=global.count+' / '+global.total);
 $$('[data-bookmark]').forEach(b=>{const active=bookmarks.has(b.dataset.bookmark);b.classList.toggle('saved',active);b.setAttribute('aria-pressed',String(active));if(b.lastChild)b.lastChild.textContent=active?' 保存済み':' この章を保存';});
 syncStorageNotice();
}
let toastTimer;function toast(text){const t=$('.toast');t.textContent=text;t.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.classList.remove('show'),3400);}
// Native checkbox change only: label, ring and text taps must never toggle twice.
document.addEventListener('change',e=>{
 const input=e.target;if(!(input instanceof HTMLInputElement)||!input.matches('[data-mission]'))return;
 const id=input.dataset.mission;if(!validMissions.has(id))return;
 const checked=input.checked;checked?done.add(id):done.delete(id);
 store();sync();
 const totals=missionStats(),group=input.closest('[data-mission-scope]'),local=missionStats(group);
 const message=checked?(totals.count===totals.total?'全'+totals.total+'項目を達成。TO BE CONTINUED →':(group?.dataset.missionLabel||'チェック')+' '+local.count+' / '+local.total+' 完了'):'チェックを外しました。';
 toast(message);
});
document.documentElement.classList.add('checklists-ready');sync();
const sheet=$('#sheet'),artbox=$('#artbox');let lastFocus=null,currentEpisode=null;
function lock(){document.body.classList.toggle('modal-open',sheet.open||artbox.open);}
function close(id){const el=document.getElementById(id);if(el?.open)el.close();}
function openSheet(title,content){lastFocus=document.activeElement;$('#sheet-title').textContent=title;$('#sheet-content').innerHTML=content;if(!sheet.open)sheet.showModal();sheet.scrollTop=0;lock();setMotion();$('.close',sheet).focus({preventScroll:true});}
sheet.addEventListener('close',()=>{sheet.style.transform='';lock();lastFocus?.focus?.({preventScroll:true});});
artbox.addEventListener('close',lock);
function sourceLink(url,text='物語の出典を見る'){return '<a class="source" href="'+esc(url)+'" target="_blank" rel="noopener noreferrer">'+esc(text)+' ↗</a>';}
function episode(id){const e=data.episodes.find(e=>e.id===String(id));if(!e)return;currentEpisode=e.id;const m=media[e.art];
 openSheet('STORY / '+e.place,'<button class="image-button" data-full="'+e.art+'" aria-label="ファンアートを拡大"><img class="dialog-image" src="'+m.src+'" alt="'+esc(m.alt)+'"></button><p class="detail-art-note">STORY ART · 出典・制作記録はメニューから</p><div class="dialog-body"><span class="kicker">'+esc(e.tag)+'</span><h2>'+esc(e.title)+'</h2>'+e.body.map(p=>'<p>'+esc(p)+'</p>').join('')+(e.spoiler?'<details><summary>結末まで振り返る（ネタバレ）</summary><p>'+esc(e.spoiler)+'</p></details>':'')+'<p class="note">'+esc(e.note)+'</p>'+sourceLink(e.source)+'<div class="dialog-footer"><button data-ep-step="-1" '+(data.episodes.indexOf(e)===0?'disabled':'')+'>← 前の話</button><button data-ep-step="1" '+(data.episodes.indexOf(e)===data.episodes.length-1?'disabled':'')+'>次の話 →</button></div></div>');}
function scene(id){const s=data.scenes.find(s=>s.id===id);if(!s)return;const m=media[s.art];
 openSheet('SCENE × MEMORY','<button class="image-button" data-full="'+s.art+'" aria-label="挿絵を拡大"><img class="dialog-image" src="'+m.src+'" alt="'+esc(m.alt)+'"></button><p class="detail-art-note">STORY ART · 挿絵と実在の場所の関係は本文を参照</p><div class="dialog-body"><span class="kicker">'+esc(s.caption)+'</span><h2>'+esc(s.name)+'</h2><p>'+esc(s.text)+'</p>'+(s.episode?'<button class="btn primary" data-episode="'+esc(s.episode)+'">物語を振り返る →</button>':'')+'<p class="note">挿絵は現地の記録写真ではありません。画像の制作記録はメニューから確認できます。</p>'+sourceLink(s.source)+'</div>');}
function full(id){const m=media[id];if(!m)return;$('#full-art-img').src=m.src;$('#full-art-img').alt=m.alt;$('#full-art-caption').textContent=m.alt+'｜公式場面画像ではありません。';if(!artbox.open)artbox.showModal();lock();}
function sources(){openSheet('SOURCES & ART','<div class="dialog-body"><div class="kicker">STORY PILGRIMAGE</div><h2>物語と、旅の根拠。</h2><p>'+esc(data.artNote)+'</p><ul class="source-list">'+data.sources.map(s=>'<li>'+sourceLink(s.url,s.title)+'</li>').join('')+'</ul><h3>画像の制作記録</h3>'+data.provenance.map(p=>'<p class="note">'+esc(p.label)+' — '+esc(p.creator)+' / '+esc(p.notes)+'</p>').join('')+'<p class="note">'+esc(data.checkedNote)+'</p></div>');}

function howto(){openSheet('HOW TO USE / MOBILE GUIDE','<div class="dialog-body"><h2>片手で、物語を持ち歩く。</h2><h3>横にめくる</h3><p>話数カードと場面カードは横スワイプ。タップで詳しい読み物が下から開きます。</p><h3>絵を大きく見る</h3><p>挿絵の拡大ボタンやエピソード詳細の画像をタップ。描かれたキャラとその場面を、みんなで見返してください。</p><h3>しおりとミッション</h3><p>章の保存・ミッションのチェックは、この端末のブラウザに保存します。共有相手のチェック状況とは同期しません。ブラウザの設定によって保存できない場合は、その場の操作だけ利用できます。</p><h3>仲間に渡す</h3><p>公開ページでは同じURLを共有できます。「画像込みで保存」から、通信なしでも読めるHTMLを保存できます。</p><h3>動きを控えめに</h3><p>メニューの「動き」で切替。端末の「視差効果を減らす」設定も尊重します。</p></div>');}
function menu(){const savedList=[...bookmarks].map(id=>data.stages.find(s=>s.id===id)?.label).filter(Boolean).join('・');
 openSheet('YOUR FIELDGUIDE','<div class="dialog-body"><div class="kicker">'+esc(data.title)+'</div><h2>次は、どの物語へ。</h2><div class="menu-list">'+data.navigation.map(n=>[n.id,n.label]).map(([id,label])=>'<a href="#'+esc(id)+'">'+esc(label)+'<span>→</span></a>').join('')+'<button data-action="save">画像込みで保存 <span>↓</span></button><button data-action="share">旅仲間に渡す <span>↗</span></button><button data-open="sources">出典・ファンアートについて <span>→</span></button></div><div class="setting"><span>画面の動き</span><button data-action="motion" aria-pressed="'+motion+'">'+(motion?'ON':'OFF')+'</button></div><p class="note">保存した章：'+(savedList||'まだありません')+'<br>ミッション：<span data-mission-menu-count>'+missionStats().count+' / '+missionStats().total+'</span>'+(storageOK?'':'<br>このブラウザでは永続保存を利用できません。')+'</p></div>');}
let active='home',scrollPositions={},raf=0,routeRAF=0;
const observer='IntersectionObserver'in window?new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.remove('waiting');e.target.classList.add('entered');observer.unobserve(e.target);}}),{threshold:.06}):null;
function observe(){const v=document.getElementById(active);$$('.reveal',v).forEach(el=>{if(el.classList.contains('entered'))return;if(motion&&observer&&el.getBoundingClientRect().top>innerHeight){el.classList.add('waiting');observer.observe(el);}else{el.classList.add('entered');el.classList.remove('waiting');}});}
function jump(y){document.documentElement.style.scrollBehavior='auto';window.scrollTo(0,Math.max(0,y));requestAnimationFrame(()=>document.documentElement.style.scrollBehavior='');}
function updateScroll(){raf=0;const max=Math.max(1,document.documentElement.scrollHeight-innerHeight);$('.progress').style.transform='scaleX('+Math.min(1,Math.max(0,scrollY/max))+')';if(active==='home'&&motion&&scrollY<900){$('.hero-art').style.setProperty('--parallax',Math.min(28,scrollY*.055)+'px');}}
addEventListener('scroll',()=>{if(!raf)raf=requestAnimationFrame(updateScroll);},{passive:true});
function showRoute(hash,back=false){const target=document.getElementById(hash||'home');if(!target)return;const view=target.classList.contains('view')?target:target.closest('.view');if(!view)return;const next=view.id;
 if(next!==active){scrollPositions[active]=scrollY;$$('.view').forEach(v=>{v.classList.toggle('active',v===view);v.inert=v!==view;});active=next;$$('.bottom-nav a').forEach(a=>{if(a.getAttribute('href')==='#'+next)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});}
 close('artbox');close('sheet');document.title=(active==='home'?data.title:(data.navigation.find(n=>n.id===active)?.label+' — '+data.title));
 requestAnimationFrame(()=>{if(target===view)jump(back?(scrollPositions[next]||0):0);else jump(scrollY+target.getBoundingClientRect().top-18);observe();updateScroll();updateRails();});}
function go(id){const hash='#'+id;if(location.hash!==hash){try{history.pushState({view:id},'',hash);}catch(e){/* Opaque previews may block history; keep in-page navigation working. */}}showRoute(id);}
function onHistory(){cancelAnimationFrame(routeRAF);routeRAF=requestAnimationFrame(()=>showRoute(decodeURIComponent(location.hash.slice(1))||'home',true));}
addEventListener('popstate',onHistory);addEventListener('hashchange',onHistory);
function chooseStory(id){$$('[data-story-tab]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.storyTab===id)));$$('[data-story-panel]').forEach(p=>p.hidden=p.dataset.storyPanel!==id);}
function chooseDay(id){$$('[data-day]').forEach(b=>b.setAttribute('aria-selected',String(b.dataset.day===id)));$$('[data-day-panel]').forEach(p=>p.hidden=p.dataset.dayPanel!==id);}

function download(){const blob=new Blob([originalHtml],{type:'text/html;charset=utf-8'}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download=data.guideId+'.html';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),5000);toast('画像入りHTMLを保存します。ファイルを仲間に渡せます。');}
async function share(){
 const url=data.publicUrl||(/^https?:$/.test(location.protocol)&&!['localhost','127.0.0.1'].includes(location.hostname)?location.href.split('#')[0]:null);
 if(url){
  if(navigator.share){try{await navigator.share({title:data.title,url});return;}catch(e){if(e.name==='AbortError')return;}}
  try{await navigator.clipboard.writeText(url);toast('ページのURLをコピーしました。');return;}catch(e){openSheet('SHARE','<div class="dialog-body"><p><a href="'+esc(url)+'">'+esc(url)+'</a></p><p>このURLをコピーして共有できます。</p></div>');return;}
 }
 const file=new File([originalHtml],data.guideId+'.html',{type:'text/html'});
 if(navigator.share&&navigator.canShare?.({files:[file]})){try{await navigator.share({title:data.title,files:[file]});return;}catch(e){if(e.name==='AbortError')return;}}
 download();
}

function updateRails(){$$('.rail').forEach(rail=>{const dots=$('[data-rail="'+rail.id+'"]');if(!dots)return;const cards=[...rail.children],idx=cards.reduce((best,c,i)=>Math.abs(c.offsetLeft-rail.offsetLeft-22-rail.scrollLeft)<Math.abs(cards[best].offsetLeft-rail.offsetLeft-22-rail.scrollLeft)?i:best,0);$$('button',dots).forEach((b,i)=>{b.classList.toggle('active',i===idx);b.setAttribute('aria-current',i===idx?'true':'false');});});}
$$('[data-rail]').forEach(dots=>{const rail=document.getElementById(dots.dataset.rail);if(!rail)return;[...rail.children].forEach((c,i)=>{const b=document.createElement('button');b.type='button';b.setAttribute('aria-label',String(i+1)+'枚目へ');b.addEventListener('click',()=>{rail.scrollTo({left:Math.max(0,c.offsetLeft-rail.offsetLeft-22),behavior:motion?'smooth':'auto'});});dots.append(b);});rail.addEventListener('scroll',()=>requestAnimationFrame(updateRails),{passive:true});});
// Keep all controls in one delegated handler, including dynamically opened sheets.
document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#"]');if(a){const id=a.getAttribute('href').slice(1);if(document.getElementById(id)){e.preventDefault();go(id);}return;}
 const b=e.target.closest('button');if(!b)return;
 if(b.dataset.close){close(b.dataset.close);return;}
 if(b.dataset.episode){episode(b.dataset.episode);return;}
 if(b.dataset.scene){scene(b.dataset.scene);return;}
 if(b.dataset.full){full(b.dataset.full);return;}
 if(b.dataset.epStep){const index=data.episodes.findIndex(ep=>ep.id===currentEpisode)+Number(b.dataset.epStep);if(data.episodes[index])episode(data.episodes[index].id);return;}
 if(b.dataset.storyTab){chooseStory(b.dataset.storyTab);return;}
 if(b.dataset.day){chooseDay(b.dataset.day);return;}
 if(b.dataset.bookmark){const id=b.dataset.bookmark;bookmarks.has(id)?bookmarks.delete(id):bookmarks.add(id);store();sync();toast(bookmarks.has(id)?(storageOK?'この章をしおりに保存しました。':'この画面内のしおりに追加しました。'):'しおりを外しました。');return;}
 if(b.dataset.open){({menu,sources,howto}[b.dataset.open])?.();return;}
 if(b.dataset.action==='save'){download();return;}
 if(b.dataset.action==='share'){share();return;}
 if(b.dataset.action==='motion'){motion=!motion&&!prefersReduced.matches;setMotion();store();if(prefersReduced.matches)toast('端末の「視差効果を減らす」を尊重して、動きを抑えています。');return;}
});

// Accessible native dialogs: Escape and focus management are provided by <dialog>.
for(const d of [sheet,artbox])d.addEventListener('click',e=>{if(e.target!==d)return;const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close();});
let dragStart=null;const grip=$('[data-drag]');grip.style.touchAction='none';grip.addEventListener('pointerdown',e=>{if(e.target.closest('button'))return;dragStart=e.clientY;grip.setPointerCapture(e.pointerId);});grip.addEventListener('pointermove',e=>{if(dragStart===null)return;sheet.style.transform='translateY('+Math.max(0,e.clientY-dragStart)+'px)';});const finishDrag=e=>{if(dragStart===null)return;const dy=e.clientY-dragStart;dragStart=null;sheet.style.transform='';if(dy>95)close('sheet');};grip.addEventListener('pointerup',finishDrag);grip.addEventListener('pointercancel',()=>{dragStart=null;sheet.style.transform='';});
$$('[data-day]').forEach((b,index)=>b.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();const tabs=$$('[data-day]');const n=e.key==='Home'?0:e.key==='End'?tabs.length-1:(index+(e.key==='ArrowLeft'?-1:1)+tabs.length)%tabs.length;chooseDay(tabs[n].dataset.day);tabs[n].focus();}}));
// Mark as an interactive site only after all required controls have been wired.
document.documentElement.classList.add('js');setMotion();sync();showRoute(decodeURIComponent(location.hash.slice(1))||'home');updateRails();
window.__pilgrimage={version:'1.0',views:viewIds,artCount:Object.keys(media).length,characterArtCount:data.characterArtCount};
})();
