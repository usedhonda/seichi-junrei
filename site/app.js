(()=>{'use strict';
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const data=JSON.parse($('#guide-data').textContent),viewIds=['home','story','aswan','abu','route'];
const media={};$$('img[data-art]').forEach(i=>{if(!media[i.dataset.art])media[i.dataset.art]={src:i.src,alt:i.alt};});
const originalHtml='<!doctype html>\n'+document.documentElement.outerHTML;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const storageKey='stardust-mobile-fanart-v1';let saved={},storageOK=true;
const validMissions=new Set(data.missions.map(m=>m.id));
const validBookmarks=new Set(['aswan','abu']);
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
function sourceLink(url,text='公式あらすじを見る'){return '<a class="source" href="'+esc(url)+'" target="_blank" rel="noopener noreferrer">'+esc(text)+' ↗</a>';}
function episode(id){const e=data.episodes.find(e=>e.id===String(id));if(!e)return;currentEpisode=e.id;const m=media[e.art];
 openSheet('EPISODE '+e.id+' / '+e.place,'<button class="image-button" data-full="'+e.art+'" aria-label="ファンアートを拡大"><img class="dialog-image" src="'+m.src+'" alt="'+esc(m.alt)+'"></button><p class="detail-art-note">ORIGINAL FAN ART · 公式の場面画像ではありません</p><div class="dialog-body"><span class="kicker">'+e.tag+'</span><h2>'+esc(e.title)+'</h2>'+e.body.map(p=>'<p>'+esc(p)+'</p>').join('')+(e.spoiler?'<details><summary>結末まで振り返る（ネタバレ）</summary><p>'+esc(e.spoiler)+'</p></details>':'')+'<p class="note">'+esc(e.note)+'</p>'+sourceLink(e.source)+'<div class="dialog-footer"><button data-ep-step="-1" '+(id==='25'?'disabled':'')+'>← 前の話</button><button data-ep-step="1" '+(id==='29'?'disabled':'')+'>次の話 →</button></div></div>');}
function scene(id){const s=data.scenes.find(s=>s.id===id);if(!s)return;const m=media[s.art];
 openSheet('SCENE × MEMORY / EP.'+s.episode,'<button class="image-button" data-full="'+s.art+'" aria-label="挿絵を拡大"><img class="dialog-image" src="'+m.src+'" alt="'+esc(m.alt)+'"></button><p class="detail-art-note">ORIGINAL FAN ART · キャラ・場面を題材にした創作です</p><div class="dialog-body"><span class="kicker">'+esc(s.caption)+'</span><h2>'+esc(s.name)+'</h2><p>'+esc(s.text)+'</p><button class="btn primary" data-episode="'+s.episode+'">第'+s.episode+'話を振り返る →</button><p class="note">絵の背景やキャラの表現は、アニメの該当カットを忠実に再現したものではありません。</p>'+sourceLink(s.source)+'</div>');}
function full(id){const m=media[id];if(!m)return;$('#full-art-img').src=m.src;$('#full-art-img').alt=m.alt;$('#full-art-caption').textContent=m.alt+'｜公式場面画像ではありません。';if(!artbox.open)artbox.showModal();lock();}
function sources(){openSheet('SOURCES & FAN ART','<div class="dialog-body"><div class="kicker">THE SCENES STAY IN THE JOURNEY</div><h2>キャラと物語がいる、<br>旅のしおり。</h2><p>承太郎、イギー、オインゴ・ボインゴなどのファンアートを、現地をめぐる物語の主役として使っています。景色だけの観光ガイドには置き換えていません。</p><p class="note">挿絵はこの会話で生成された非公式ファンアート・情景イラストです。公式のアニメ画像、原作コマ、記録写真ではなく、キャラ・場面・地理を創作的に組み合わせています。作品との実際の関係は解説と下記出典を参照してください。公開・再配布の権利を保証する表示ではありません。</p><h3>物語と観光情報の出典</h3><ul class="source-list">'+data.sources.map(s=>'<li><a href="'+esc(s.url)+'" target="_blank" rel="noopener noreferrer">'+esc(s.title)+' ↗</a></li>').join('')+'</ul><p class="note">話数の対応と観光情報は2026年10月23日に確認。料金や入場時間は変わる場合があるため、公式リンクを優先してください。</p></div>');}
function howto(){openSheet('HOW TO USE / MOBILE GUIDE','<div class="dialog-body"><h2>片手で、物語を持ち歩く。</h2><h3>横にめくる</h3><p>話数カードと場面カードは横スワイプ。タップで詳しい読み物が下から開きます。</p><h3>絵を大きく見る</h3><p>挿絵の拡大ボタンやエピソード詳細の画像をタップ。描かれたキャラとその場面を、みんなで見返してください。</p><h3>しおりとミッション</h3><p>章の保存・ミッションのチェックは、この端末のブラウザに保存します。共有相手のチェック状況とは同期しません。ブラウザの設定によって保存できない場合は、その場の操作だけ利用できます。</p><h3>仲間に渡す</h3><p>公開ページでは同じURLを共有できます。「画像込みで保存」から、通信なしでも読めるHTMLを保存できます。</p><h3>動きを控えめに</h3><p>メニューの「動き」で切替。端末の「視差効果を減らす」設定も尊重します。</p></div>');}
function menu(){const savedList=[...bookmarks].map(id=>({aswan:'アスワン',abu:'アブ・シンベル'}[id])).filter(Boolean).join('・');
 openSheet('YOUR FIELDGUIDE','<div class="dialog-body"><div class="kicker">STARDUST ON THE NILE</div><h2>次は、どの物語へ。</h2><div class="menu-list">'+[['home','表紙へ'],['story','第25〜29話を振り返る'],['aswan','アスワンの章'],['abu','アブ・シンベルの章'],['route','旅程とメモ']].map(([id,label])=>'<a href="#'+id+'">'+label+'<span>→</span></a>').join('')+'<button data-action="save">画像込みで保存 <span>↓</span></button><button data-action="share">旅仲間に渡す <span>↗</span></button><button data-open="sources">出典・ファンアートについて <span>→</span></button></div><div class="setting"><span>画面の動き</span><button data-action="motion" aria-pressed="'+motion+'">'+(motion?'ON':'OFF')+'</button></div><p class="note">保存した章：'+(savedList||'まだありません')+'<br>ミッション：<span data-mission-menu-count>'+missionStats().count+' / '+missionStats().total+'</span>'+(storageOK?'':'<br>このブラウザでは永続保存を利用できません。')+'</p></div>');}
let active='home',scrollPositions={},raf=0,routeRAF=0;
const observer='IntersectionObserver'in window?new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.remove('waiting');e.target.classList.add('entered');observer.unobserve(e.target);}}),{threshold:.06}):null;
function observe(){const v=document.getElementById(active);$$('.reveal',v).forEach(el=>{if(el.classList.contains('entered'))return;if(motion&&observer&&el.getBoundingClientRect().top>innerHeight){el.classList.add('waiting');observer.observe(el);}else{el.classList.add('entered');el.classList.remove('waiting');}});}
function jump(y){document.documentElement.style.scrollBehavior='auto';window.scrollTo(0,Math.max(0,y));requestAnimationFrame(()=>document.documentElement.style.scrollBehavior='');}
function updateScroll(){raf=0;const max=Math.max(1,document.documentElement.scrollHeight-innerHeight);$('.progress').style.transform='scaleX('+Math.min(1,Math.max(0,scrollY/max))+')';if(active==='home'&&motion&&scrollY<900){$('.hero-art').style.setProperty('--parallax',Math.min(28,scrollY*.055)+'px');}}
addEventListener('scroll',()=>{if(!raf)raf=requestAnimationFrame(updateScroll);},{passive:true});
function showRoute(hash,back=false){const target=document.getElementById(hash||'home');if(!target)return;const view=target.classList.contains('view')?target:target.closest('.view');if(!view)return;const next=view.id;
 if(next!==active){scrollPositions[active]=scrollY;$$('.view').forEach(v=>{v.classList.toggle('active',v===view);v.inert=v!==view;});active=next;$$('.bottom-nav a').forEach(a=>{if(a.getAttribute('href')==='#'+next)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});}
 close('artbox');close('sheet');document.title=(active==='home'?'STARDUST ON THE NILE':({story:'EPISODE GUIDE',aswan:'ASWAN',abu:'ABU SIMBEL',route:'OUR JOURNEY'}[active]+' — STARDUST ON THE NILE'));
 requestAnimationFrame(()=>{if(target===view)jump(back?(scrollPositions[next]||0):0);else jump(scrollY+target.getBoundingClientRect().top-18);observe();updateScroll();updateRails();});}
function go(id){const hash='#'+id;if(location.hash!==hash){try{history.pushState({view:id},'',hash);}catch(e){/* Opaque previews may block history; keep in-page navigation working. */}}showRoute(id);}
function onHistory(){cancelAnimationFrame(routeRAF);routeRAF=requestAnimationFrame(()=>showRoute(decodeURIComponent(location.hash.slice(1))||'home',true));}
addEventListener('popstate',onHistory);addEventListener('hashchange',onHistory);
function chooseStory(id){$$('[data-story-tab]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.storyTab===id)));$$('[data-story-panel]').forEach(p=>p.hidden=p.dataset.storyPanel!==id);}
function chooseDay(id){$$('[data-day]').forEach(b=>b.setAttribute('aria-selected',String(b.dataset.day===id)));$('#day-1').hidden=id!=='1';$('#day-2').hidden=id!=='2';}
function download(){const blob=new Blob([originalHtml],{type:'text/html;charset=utf-8'}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='stardust-on-the-nile-mobile.html';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),5000);toast('画像入りHTMLを保存します。ファイルを仲間に渡せます。');}
async function share(){
 const url='https://usedhonda.github.io/seichi-junrei/';
 if(navigator.share){try{await navigator.share({title:'STARDUST ON THE NILE',url});return;}catch(e){if(e.name==='AbortError')return;}}
 try{await navigator.clipboard.writeText(url);toast('公開ページのURLをコピーしました。');}catch(e){openSheet('SHARE','<div class="dialog-body"><h2>旅仲間へ渡す</h2><p><a href="'+url+'">'+url+'</a></p><p>このURLをコピーして共有できます。</p></div>');}
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
 if(b.dataset.epStep){const id=Number(currentEpisode)+Number(b.dataset.epStep);if(id>=25&&id<=29)episode(String(id));return;}
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
$$('[data-day]').forEach(b=>b.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();const id=e.key==='Home'?'1':e.key==='End'?'2':b.dataset.day==='1'?'2':'1';chooseDay(id);$('[data-day="'+id+'"]').focus();}}));
// Mark as an interactive site only after all required controls have been wired.
document.documentElement.classList.add('js');setMotion();sync();showRoute(decodeURIComponent(location.hash.slice(1))||'home');updateRails();
window.__stardust={version:'mobile-fanart-1.1.1',views:viewIds,artCount:Object.keys(media).length,characterArtCount:7};
})();
