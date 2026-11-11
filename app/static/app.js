const kushTimeline=[
 {date:"c. 2500 BCE onward",title:"Kerma rises",desc:"A major Middle Nile kingdom develops around Kerma."},
 {date:"c. 1550–1070 BCE",title:"Egyptian New Kingdom rule",desc:"Egypt extends imperial control into Nubia; local societies continue and adapt."},
 {date:"8th century BCE",title:"Napatan Kush",desc:"Kushite rulers based around Napata expand north."},
 {date:"c. 747–656 BCE",title:"Twenty-fifth Dynasty",desc:"Kushite kings rule Egypt; dates and sequence are based on current scholarly chronologies."},
 {date:"3rd century BCE onward",title:"Meroitic royal centre",desc:"Meroë becomes the principal royal residence and burial centre."},
 {date:"1st century BCE",title:"Conflict with Rome",desc:"Kush and Rome clash; Amanirenas is associated with this period."},
 {date:"4th century CE",title:"Transformation of Kush",desc:"Meroitic political power declines amid several debated regional changes."}
];
const kushSites=[
 {id:"kerma",name:"Kerma",lat:19.6008,lng:30.4097,detail:"Early Kushite kingdom and the Western Deffufa. UNESCO tentative-list coordinate."},
 {id:"gebel-barkal",name:"Gebel Barkal",lat:18.5370,lng:31.8280,detail:"Sacred mountain and major Napatan religious centre. UNESCO World Heritage coordinate."},
 {id:"el-kurru",name:"El-Kurru",lat:18.4100,lng:31.7714,detail:"Royal cemetery associated with Napatan rulers. UNESCO coordinate."},
 {id:"nuri",name:"Nuri",lat:18.5639,lng:31.9167,detail:"Royal pyramid cemetery. UNESCO coordinate."},
 {id:"meroe",name:"Meroë",lat:16.9333,lng:33.7167,detail:"Royal city and cemetery within the Island of Meroe World Heritage property. UNESCO nomination coordinate."},
 {id:"musawwarat",name:"Musawwarat es-Sufra",lat:16.4108,lng:33.3280,detail:"Temple and monumental complex in the Island of Meroe World Heritage property. UNESCO coordinate."},
 {id:"naqa",name:"Naqa",lat:16.2684,lng:33.2792,detail:"Religious and settlement centre in the Island of Meroe World Heritage property. UNESCO coordinate."}
];
const root=document.getElementById('articles'),q=document.getElementById('searchInput'),cat=document.getElementById('categorySelect'),count=document.getElementById('recordCount'),dlg=document.getElementById('articleDialog'),body=document.getElementById('dialogContent');let timer;
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
async function load(){const p=new URLSearchParams();if(q.value.trim())p.set('q',q.value.trim());if(cat.value)p.set('category',cat.value);try{const r=await fetch('/api/articles?'+p);if(!r.ok)throw Error();const d=await r.json();count.textContent=d.count+' archive records';root.innerHTML=d.items.length?d.items.map(a=>'<article class="article-card" tabindex="0" data-id="'+esc(a.id)+'"><div class="meta"><span>'+esc(a.category)+'</span><span>'+esc(a.status)+'</span></div><h3>'+esc(a.title)+'</h3><p>'+esc(a.summary)+'</p><div class="meta"><span>'+esc(a.period)+'</span><span>Read inside NILE HISTORY ↗</span></div></article>').join(''):'No matching records yet.';root.querySelectorAll('[data-id]').forEach(el=>{const open=()=>show(el.dataset.id);el.onclick=open;el.onkeydown=e=>{if(e.key==='Enter')open()}})}catch(e){root.textContent='Archive unavailable. Check the server and refresh.';count.textContent='Connection unavailable'}}
async function show(id){const r=await fetch('/api/articles/'+encodeURIComponent(id));if(!r.ok)return;const a=await r.json();const paragraphs=a.article_sections?'<div class="article-chapters">'+a.article_sections.map(s=>'<section class="article-chapter"><h3>'+esc(s[0])+'</h3><p class="article-paragraph">'+esc(s[1])+'</p></section>').join('')+'</div>' :(a.article_text||[a.summary]).map(p=>'<p class="article-paragraph">'+esc(p)+'</p>').join('');const refs=(a.source_leads||[]).map((s,i)=>'<li><b>['+(i+1)+'] '+esc(s.name)+'</b><br><a class="optional-source" target="_blank" rel="noopener" href="'+esc(s.url)+'">Optional: view original reference ↗</a></li>').join('');const visual=a.id==='kush'?'<section class="kush-visual"><h3>Kushite historical timeline</h3><div class="kush-timeline">'+kushTimeline.map(t=>'<article><small>'+esc(t.date)+'</small><b>'+esc(t.title)+'</b><p>'+esc(t.desc)+'</p></article>').join('')+'</div><h3>Historical atlas: verified archaeological locations</h3><p class="reference-intro">Real geographic map using OpenStreetMap tiles. Site coordinates are taken from UNESCO World Heritage Centre records and its Kerma tentative-list record. These pins locate archaeological places; they do not represent ancient political borders.</p><div id="kushLeafletMap" class="kush-leaflet-map" role="region" aria-label="Interactive map of Kushite archaeological sites"></div><p class="map-credit">Map data © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap contributors</a> · Coordinates: UNESCO World Heritage Centre. Map tiles load from OpenStreetMap.</p><div class="site-list">'+kushSites.map(p=>'<button type="button" data-site="'+p.id+'"><b>'+esc(p.name)+'</b><span>'+esc(p.detail)+'</span></button>').join('')+'</div><p class="site-detail" id="siteDetail" aria-live="polite">Select a marker or site name to see its location and historical context.</p></section>':''
body.innerHTML='<div class="eyebrow">'+esc(a.category)+' · '+esc(a.region)+'</div><h2>'+esc(a.title)+'</h2><p>'+esc(a.period)+' · '+esc(a.status)+'</p><div class="article-reading">'+paragraphs+'</div>'+visual+'<section class="citation-panel"><h3>References & further reading</h3><p class="reference-intro">This article is written for reading here in NILE HISTORY. The references below identify the evidence used; opening an external source is optional.</p><ol class="reference-list">'+refs+'</ol></section><div class="note"><b>Editorial note:</b> '+esc(a.note)+'</div>';
if(a.id==='kush'){const detail=document.getElementById('siteDetail');const mapNode=document.getElementById('kushLeafletMap');const choose=id=>{const p=kushSites.find(x=>x.id===id);if(p){detail.textContent=p.name+' — '+p.detail;if(window.kushMapInstance)window.kushMapInstance.setView([p.lat,p.lng],10);}};body.querySelectorAll('[data-site]').forEach(el=>{el.addEventListener('click',()=>choose(el.dataset.site));});if(window.L&&mapNode){if(window.kushMapInstance){window.kushMapInstance.remove();window.kushMapInstance=null;}const map=L.map(mapNode,{scrollWheelZoom:false}).setView([17.9,32.1],6);window.kushMapInstance=map;L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);kushSites.forEach(p=>L.marker([p.lat,p.lng]).addTo(map).bindPopup('<strong>'+esc(p.name)+'</strong><br>'+esc(p.detail)).on('click',()=>{detail.textContent=p.name+' — '+p.detail;}));const bounds=L.latLngBounds(kushSites.map(p=>[p.lat,p.lng]));map.fitBounds(bounds.pad(0.18));setTimeout(()=>{map.invalidateSize();map.fitBounds(bounds.pad(0.18));},250);}else{mapNode.textContent='The interactive map library could not load. The verified site list remains available below.';}}
dlg.showModal()}
q.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(load,220)});cat.addEventListener('change',load);document.getElementById('closeDialog').onclick=()=>dlg.close();dlg.addEventListener('click',e=>{if(e.target===dlg)dlg.close()});let promptEvent;window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();promptEvent=e;const b=document.getElementById('installBtn');b.hidden=false;b.onclick=async()=>{promptEvent.prompt();await promptEvent.userChoice;promptEvent=null;b.hidden=true}});if('serviceWorker'in navigator)addEventListener('load',()=>navigator.serviceWorker.register('/static/sw.js').catch(()=>{}));load();

async function showWikipedia(pageId){
 const labels={"sudan":"History of Sudan","south-sudan":"History of South Sudan","prehistory-sudan":"Prehistory of Sudan","nubia":"Nubia","kerma-culture":"Kerma culture","kingdom-kush":"Kingdom of Kush","napata":"Napata","meroe":"Meroë","nobatia":"Nobatia","makuria":"Makuria","alodia":"Alodia","funj-sultanate":"Funj Sultanate","darfur-sultanate":"Sultanate of Darfur","turco-egyptian":"Turco-Egyptian conquest of Sudan","mahdist-war":"Mahdist War","anglo-egyptian":"Anglo-Egyptian Sudan","first-civil-war":"First Sudanese Civil War","second-civil-war":"Second Sudanese Civil War","peace-agreement":"Comprehensive Peace Agreement","south-sudan-war":"South Sudanese Civil War","sudan-war":"War in Sudan (2023)"};
 body.innerHTML='<div class="eyebrow">WIKIPEDIA · FULL ARTICLE</div><h2>'+labels[pageId]+'</h2><p>Loading the complete article into NILE HISTORY…</p>';
 dlg.showModal();
 try{
  const response=await fetch('/api/library/wikipedia/'+encodeURIComponent(pageId));
  if(!response.ok)throw new Error('Source unavailable');
  const data=await response.json();
  const frame=document.createElement('iframe');
  frame.className='wiki-frame';frame.title=data.title+' — full article';
  frame.setAttribute('sandbox','allow-popups allow-popups-to-escape-sandbox');
  frame.srcdoc='<!doctype html><html><head><meta charset="utf-8"><base href="https://en.wikipedia.org/"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{font:16px/1.7 system-ui,sans-serif;color:#26332e;margin:18px;max-width:900px}img,table{max-width:100%;height:auto}table{border-collapse:collapse;display:block;overflow-x:auto}th,td{border:1px solid #ccd3ce;padding:7px}h2,h3,h4{line-height:1.3;margin-top:1.6em}a{color:#28634b} .mw-editsection,.navbox,.vertical-navbox,.metadata,.noprint,.mw-references-wrap{font-size:.9em} .hatnote{color:#59665f} </style></head><body>'+data.html+'</body></html>';
  const attribution=document.createElement('section');attribution.className='wiki-attribution';
  const licence=data.license||{};const licenceUrl=licence.url||'https://creativecommons.org/licenses/by-sa/4.0/';
  attribution.innerHTML='<h3>Source and reuse information</h3><p>Text reproduced from <a href="'+data.source_url+'" target="_blank" rel="noopener">'+data.title+'</a>, by Wikipedia contributors. <a href="'+data.history_url+'" target="_blank" rel="noopener">View revision history and contributors</a>. Revision: '+String(data.revision||'not supplied')+' · '+String(data.timestamp||'date not supplied')+'. Licence: <a href="'+licenceUrl+'" target="_blank" rel="noopener">'+String(licence.title||'Creative Commons Attribution-ShareAlike')+'</a>. The article is reproduced for reading inside NILE HISTORY; edits or additional formatting are identified by this app. Third-party media may have separate licences.</p>';
  body.replaceChildren();const heading=document.createElement('div');heading.className='eyebrow';heading.textContent='WIKIPEDIA · FULL ARTICLE';const title=document.createElement('h2');title.textContent=data.title;body.append(heading,title,frame,attribution);
 }catch(error){body.innerHTML='<h2>'+labels[pageId]+'</h2><p>The source could not be loaded right now. Please try again later.</p><p><a href="https://en.wikipedia.org/wiki/'+(pageId==='sudan'?'History_of_Sudan':'History_of_South_Sudan')+'" target="_blank" rel="noopener">Open original Wikipedia article</a></p>'}
}

async function loadWikipediaCatalog(){
 const catalog=document.getElementById('wikiCatalog'),search=document.getElementById('wikiSearch'),count=document.getElementById('wikiCount');
 try{
  const response=await fetch('/api/library/catalog');if(!response.ok)throw new Error('catalog');
  const data=await response.json();
  const render=()=>{const term=search.value.trim().toLowerCase();const items=data.items.filter(item=>(item.title+' '+item.group).toLowerCase().includes(term));count.textContent=items.length+' source articles in the catalogue';catalog.innerHTML=items.map(item=>'<button class="wiki-card" type="button" data-wiki="'+item.id+'"><span>'+item.group+'</span><b>'+item.title+'</b><small>Read full article inside NILE HISTORY →</small></button>').join('')||'<p>No matching source articles.</p>';catalog.querySelectorAll('[data-wiki]').forEach(button=>button.addEventListener('click',()=>showWikipedia(button.dataset.wiki)));};
  search.addEventListener('input',render);render();
 }catch(error){count.textContent='Could not load the source catalogue. Refresh to try again.';}
}
loadWikipediaCatalog();


async function loadBookCatalog(){
 const node=document.getElementById('bookCatalog');if(!node)return;
 try{
  const response=await fetch('/api/library/books');if(!response.ok)throw new Error('catalog');
  const data=await response.json();
  node.innerHTML=data.items.map(book=>'<article class="book-card"><div class="eyebrow">'+esc(book.year)+' · '+esc(book.language)+'</div><h3>'+esc(book.title)+'</h3><p><b>Author:</b> '+esc(book.author)+'<br><b>Editor:</b> '+esc(book.editor)+'<br><b>Publisher:</b> '+esc(book.publisher)+'</p><p>'+esc(book.description)+'</p><button type="button" class="primary book-open" data-book="'+esc(book.id)+'">Read complete book inside NILE HISTORY ↗</button><p class="book-rights">'+esc(book.rights)+'</p></article>').join('');
  node.querySelectorAll('[data-book]').forEach(button=>button.addEventListener('click',()=>openHistoricalBook(button.dataset.book,data.items.find(item=>item.id===button.dataset.book))));
 }catch(error){node.textContent='The historical book catalogue could not be loaded. Refresh to try again.';}
}
async function openHistoricalBook(id,book){
 body.replaceChildren();const eyebrow=document.createElement('div');eyebrow.className='eyebrow';eyebrow.textContent='DIGITISED PRIMARY SOURCE · FULL TEXT';
 const title=document.createElement('h2');title.textContent=book.title;
 const status=document.createElement('p');status.textContent='Loading the complete digitised text…';
 body.append(eyebrow,title,status);dlg.showModal();
 try{
  const response=await fetch('/api/library/books/'+encodeURIComponent(id)+'/text');if(!response.ok)throw new Error('source');
  const sourceText=await response.text();
  const warning=document.createElement('aside');warning.className='book-warning';warning.textContent=book.editorial_warning;
  const meta=document.createElement('p');meta.className='book-meta';meta.textContent=book.author+' · edited by '+book.editor+' · '+book.year+' · '+book.publisher;
  const reader=document.createElement('section');reader.className='book-reader-tools';
  const searchLabel=document.createElement('label');searchLabel.className='reader-search-label';searchLabel.textContent='Find in this book';
  const search=document.createElement('input');search.type='search';search.placeholder='Search words or phrases…';search.setAttribute('aria-label','Find text inside this book');
  const matchInfo=document.createElement('span');matchInfo.className='reader-match-info';matchInfo.textContent='Search the complete text';
  const previous=document.createElement('button');previous.type='button';previous.textContent='Previous match';
  const next=document.createElement('button');next.type='button';next.textContent='Next match';
  const smaller=document.createElement('button');smaller.type='button';smaller.textContent='A−';smaller.setAttribute('aria-label','Decrease book text size');
  const larger=document.createElement('button');larger.type='button';larger.textContent='A+';larger.setAttribute('aria-label','Increase book text size');
  const top=document.createElement('button');top.type='button';top.textContent='Back to beginning';
  reader.append(searchLabel,search,matchInfo,previous,next,smaller,larger,top);
  const pre=document.createElement('pre');pre.className='book-fulltext';pre.textContent=sourceText;pre.tabIndex=0;
  let matches=[],matchIndex=-1,fontSize=15;
  const findMatches=()=>{const term=search.value.trim().toLocaleLowerCase();matches=[];matchIndex=-1;if(term){const haystack=sourceText.toLocaleLowerCase();let at=0;while((at=haystack.indexOf(term,at))!==-1){matches.push(at);at+=Math.max(1,term.length);}}matchInfo.textContent=matches.length?matches.length+' match(es) found':'No matches yet';};
  const goToMatch=direction=>{if(!matches.length){findMatches();if(!matches.length)return;}matchIndex=(matchIndex+direction+matches.length)%matches.length;const ratio=matches[matchIndex]/Math.max(1,sourceText.length);pre.scrollTop=Math.max(0,ratio*pre.scrollHeight-pre.clientHeight*0.35);matchInfo.textContent='Match '+(matchIndex+1)+' of '+matches.length;};
  search.addEventListener('input',findMatches);previous.addEventListener('click',()=>goToMatch(-1));next.addEventListener('click',()=>goToMatch(1));
  smaller.addEventListener('click',()=>{fontSize=Math.max(11,fontSize-1);pre.style.fontSize=fontSize+'px';});
  larger.addEventListener('click',()=>{fontSize=Math.min(24,fontSize+1);pre.style.fontSize=fontSize+'px';});
  top.addEventListener('click',()=>{pre.scrollTop=0;});
  const attribution=document.createElement('section');attribution.className='wiki-attribution';
  const source=document.createElement('a');source.href=book.source_url;source.target='_blank';source.rel='noopener';source.textContent=book.source+' — bibliographic record and original edition';
  const rights=document.createElement('p');rights.textContent=book.rights;
  attribution.append(source,rights);
  body.replaceChildren(eyebrow,title,meta,warning,reader,pre,attribution);
 }catch(error){status.textContent='The full text could not be retrieved right now. Please try again later.';}
}
loadBookCatalog();
