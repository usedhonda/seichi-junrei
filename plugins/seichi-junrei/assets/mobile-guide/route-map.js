(()=>{'use strict';
const configNode=document.getElementById('route-map-data');if(!configNode)return;
const d=JSON.parse(configNode.textContent),root=document.getElementById('journey-map');
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let map,layer,tiles,view=d.initialView||'day',currentDay='',markers=new Map();
const status=document.querySelector('[data-map-status]');
function day(){return d.days.find(x=>x.id===document.querySelector('[data-day][aria-selected="true"]')?.dataset.day)||d.days[0];}
function points(){return view==='all'?d.stops:day().stops.map(id=>d.stops.find(s=>s.id===id));}
function direction(a,b,mode){const p=new URLSearchParams({api:'1',origin:a.lat+','+a.lon,destination:b.lat+','+b.lon});if(['walking','transit','driving'].includes(mode))p.set('travelmode',mode);return 'https://www.google.com/maps/dir/?'+p;}
function create(){
 if(map)return;
 map=L.map(root,{scrollWheelZoom:false,zoomControl:true,minZoom:2,maxZoom:19,fadeAnimation:false,zoomAnimation:false});
 map.attributionControl.addAttribution('&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors');
 L.control.scale({imperial:false}).addTo(map);layer=L.layerGroup().addTo(map);
 // Only visible online maps load tiles. No prefetch, tile download or offline cache.
 if(/^https?:$/.test(location.protocol)&&navigator.onLine){
  tiles=L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,referrerPolicy:'strict-origin-when-cross-origin',attribution:'&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors'});
  tiles.on('tileload',()=>{status.textContent='地図を動かせます。番号を選ぶと場所の詳細が開きます。';root.dataset.tiles='loaded';});
  tiles.on('tileerror',()=>{status.textContent='背景地図を読み込めません。地点の一覧と「地図で開く」は使えます。';root.dataset.tiles='unavailable';});
  tiles.addTo(map);
 }else{
  status.textContent='保存版・オフラインでは背景地図を読み込みません。地点と訪問順を表示しています。経路案内は通信時に開いてください。';root.dataset.tiles='offline';
 }
}
function draw(force=false){
 if(!root.getClientRects().length)return;
 create();const selected=day(),signature=selected.id+':'+view;
 map.invalidateSize({pan:false});if(currentDay===signature&&!force)return;currentDay=signature;
 const pts=points();layer.clearLayers();markers.clear();
 document.querySelectorAll('[data-map-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mapView===view)));
 document.querySelector('[data-map-caption]').textContent=view==='all'?'旅全体の位置関係':(selected.label==='DAY '+selected.id?selected.label:'DAY '+selected.id+' / '+selected.label);
 const list=document.querySelector('[data-map-stops]');if(list)list.innerHTML=pts.map((s,i)=>{
  const next=pts[i+1];return '<article class="map-stop"><button data-map-stop="'+esc(s.id)+'" aria-label="'+esc(s.label)+'を地図で選ぶ"><b>'+s.number+'</b><span>'+esc(s.label)+'</span></button><div><a href="'+esc(s.url)+'" target="_blank" rel="noopener noreferrer">地図で開く ↗</a>'+(next?'<a class="directions-link" href="'+esc(direction(s,next,view==='day'?selected.mode:''))+'" target="_blank" rel="noopener noreferrer">'+next.number+'への経路 ↗</a>':'')+'</div></article>';
 }).join('');
 for(const s of pts){
  const icon=L.divIcon({className:'route-pin-wrap',html:'<span class="route-pin">'+s.number+'</span>',iconSize:[32,38],iconAnchor:[16,36]});
  const marker=L.marker([s.lat,s.lon],{icon,title:s.label,alt:s.label,keyboard:true}).addTo(layer);
  marker.bindPopup('<div class="map-popup"><small>STOP '+s.number+'</small><strong>'+esc(s.label)+'</strong><p>'+esc(s.note)+'</p>'+(s.stage?'<a href="#'+esc(s.stage)+'">この場所の章を読む →</a>':'')+'<a href="'+esc(s.url)+'" target="_blank" rel="noopener noreferrer">地図で開く ↗</a></div>');markers.set(s.id,marker);
 }
 if(pts.length>1){L.polyline(pts.map(s=>[s.lat,s.lon]),{color:getComputedStyle(document.body).getPropertyValue('--gold').trim()||'#a6292b',weight:2,dashArray:'5 7',interactive:false}).addTo(layer);map.fitBounds(pts.map(s=>[s.lat,s.lon]),{padding:[40,40],maxZoom:16,animate:false});}
 else if(pts.length)map.setView([pts[0].lat,pts[0].lon],16,{animate:false});
 else{status.textContent='この日の地点は未登録です。全体地図をご覧ください。';map.fitBounds(d.stops.map(s=>[s.lat,s.lon]),{padding:[40,40],maxZoom:15,animate:false});}
 root.dataset.mapReady='true';root.dataset.stopCount=String(pts.length);
}
document.addEventListener('click',e=>{
 const toggle=e.target.closest('[data-map-view]');if(toggle){view=toggle.dataset.mapView;draw(true);return;}
 const focus=e.target.closest('[data-map-stop]');if(focus){
  if(!points().some(s=>s.id===focus.dataset.mapStop))view='all';draw(true);
  const marker=markers.get(focus.dataset.mapStop);if(marker){map.setView(marker.getLatLng(),16,{animate:false});marker.openPopup();root.scrollIntoView({block:'start',behavior:'auto'});}return;
 }
 if(e.target.closest('[data-day],a[href="#route"]'))requestAnimationFrame(()=>requestAnimationFrame(()=>draw()));
});
document.addEventListener('keydown',e=>{if(e.target.closest('[data-day]'))requestAnimationFrame(()=>draw());});
addEventListener('hashchange',()=>requestAnimationFrame(()=>draw()));addEventListener('popstate',()=>requestAnimationFrame(()=>requestAnimationFrame(()=>draw())));
new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting))draw();},{threshold:.1}).observe(root);
})();
