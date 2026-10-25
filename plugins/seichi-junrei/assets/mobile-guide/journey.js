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
  const ids=(el.dataset.localStops||el.dataset.localMap).split(' ');
  const points=ids.map(id=>config.stops.find(s=>s.id===id)).filter(Boolean);if(!points.length)return;
  const map=L.map(el,{scrollWheelZoom:false,fadeAnimation:false,zoomAnimation:false});localMaps.set(el,map);
  const credit='&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors';map.attributionControl.addAttribution(credit);L.control.scale({imperial:false}).addTo(map);
  const message=document.createElement('p');message.className='local-map-offline';message.setAttribute('role','status');el.after(message);
  if(/^https?:$/.test(location.protocol)&&navigator.onLine){
   const tiles=L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,referrerPolicy:'strict-origin-when-cross-origin'});
   tiles.on('tileerror',()=>message.textContent='背景地図を読み込めません。地点と下の地図リンクは使えます。');tiles.on('tileload',()=>message.textContent='');tiles.addTo(map);
  }else message.textContent='保存版では背景地図を表示しません。地点の位置と、下の地図リンクをご利用ください。';
  for(const point of points)L.marker([point.lat,point.lon],{title:point.label,icon:L.divIcon({className:'route-pin-wrap',html:'<span class="route-pin">'+point.number+'</span>',iconSize:[32,38],iconAnchor:[16,36]})}).addTo(map).bindPopup(esc(point.label));
  if(points.length>1){L.polyline(points.map(p=>[p.lat,p.lon]),{color:'#bd3e35',weight:2,dashArray:'5 7'}).addTo(map);map.fitBounds(points.map(p=>[p.lat,p.lon]),{padding:[35,35],maxZoom:16,animate:false});}
  else map.setView([points[0].lat,points[0].lon],17);
  el.dataset.stopCount=String(points.length);
  el.dataset.mapReady='true';
 });
}));
let queued=false;
function mark(){queued=false;let current='home';for(const item of navigation.slice(1)){const node=document.getElementById(item.id);if(node&&node.getBoundingClientRect().top<=120)current=item.id;}
 document.querySelectorAll('.bottom-nav a').forEach(a=>{if(a.hash==='#'+current)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
}
addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(mark);}},{passive:true});mark();
})();
