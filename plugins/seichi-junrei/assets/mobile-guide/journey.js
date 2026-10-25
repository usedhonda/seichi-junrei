(()=>{'use strict';
if(document.body.dataset.readingFlow!=='journey')return;
const config=JSON.parse(document.getElementById('route-map-data').textContent);
const navigation=JSON.parse(document.getElementById('guide-data').textContent).navigation;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const localMaps=new Map();
document.querySelectorAll('.local-map-details').forEach(details=>details.addEventListener('toggle',()=>{
 if(!details.open)return;
 const el=details.querySelector('[data-local-map]');if(!el)return;
 requestAnimationFrame(()=>{
  if(localMaps.has(el)){localMaps.get(el).invalidateSize({pan:false});return;}
  const point=config.stops.find(s=>s.id===el.dataset.localMap);if(!point)return;
  const map=L.map(el,{scrollWheelZoom:false,fadeAnimation:false,zoomAnimation:false}).setView([point.lat,point.lon],17);localMaps.set(el,map);
  const credit='&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors';map.attributionControl.addAttribution(credit);
  if(/^https?:$/.test(location.protocol)&&navigator.onLine)L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,referrerPolicy:'strict-origin-when-cross-origin'}).addTo(map);
  else{const notice=document.createElement('p');notice.className='local-map-offline';notice.textContent='保存版では背景地図を表示しません。地点の位置と、下の地図リンクをご利用ください。';el.after(notice);}
  L.marker([point.lat,point.lon],{title:point.label,icon:L.divIcon({className:'route-pin-wrap',html:'<span class="route-pin">'+point.number+'</span>',iconSize:[32,38],iconAnchor:[16,36]})}).addTo(map).bindPopup(esc(point.label));
  el.dataset.mapReady='true';
 });
}));
let queued=false;
function mark(){queued=false;let current='home';for(const item of navigation.slice(1)){const node=document.getElementById(item.id);if(node&&node.getBoundingClientRect().top<=120)current=item.id;}
 document.querySelectorAll('.bottom-nav a').forEach(a=>{if(a.hash==='#'+current)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
}
addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(mark);}},{passive:true});mark();
})();
