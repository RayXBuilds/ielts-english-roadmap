'use strict';
const paths = {
  home:'M3 10 12 3l9 7v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1Z',
  plan:'M5 4h14a2 2 0 0 1 2 2v14H3V6a2 2 0 0 1 2-2ZM7 2v4M17 2v4M3 9h18M7 13h3M14 13h3M7 17h3',
  reading:'M12 5C8 2 4 3 2 4v15c4-2 7-1 10 1 3-2 6-3 10-1V4c-2-1-6-2-10 1Zm0 0v15',
  listening:'M4 14v-3a8 8 0 0 1 16 0v3M4 12H3v7h4v-7Zm16 0h1v7h-4v-7Z',
  speaking:'M21 11a9 8 0 0 1-9 8H7l-5 3 2-6a8 8 0 0 1-1-5 9 8 0 0 1 18 0ZM8 10h8M8 14h5',
  words:'M6 3h12v19l-6-4-6 4ZM9 8h6M9 11h4',
  settings:'m12 3 3 3 4 1v4l2 3-3 3-1 4h-4l-3-2-4-1v-4l-2-3 3-3 1-4Zm0 5a4 4 0 1 0 0 8 4 4 0 0 0 0-8Z',
  search:'M10.5 3a7.5 7.5 0 1 0 0 15 7.5 7.5 0 0 0 0-15ZM16 16l5 5',
  arrow:'M5 12h14m-6-6 6 6-6 6', back:'M19 12H5m6-6-6 6 6 6',
  check:'m5 12 4 4L19 6', plus:'M12 5v14M5 12h14', close:'m6 6 12 12M6 18 18 6',
  clock:'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18Zm0 4v5l3 2',
  play:'m9 5 11 7-11 7Z', pause:'M8 5v14M16 5v14',
  rewind:'M3 9h7M3 9V2m0 7a9 9 0 1 1-1 7',
  focus:'M3 9V3h6m6 0h6v6m0 6v6h-6m-6 0H3v-6',
  download:'M12 3v12m-5-5 5 5 5-5M4 17v4h16v-4',
  upload:'M12 16V4m-5 5 5-5 5 5M4 17v4h16v-4',
  edit:'m4 16 12-12 4 4L8 20H4Zm9-9 4 4', trash:'M3 6h18M9 6V3h6v3M5 6l1 15h12l1-15M10 10v7M14 10v7',
  sound:'M3 9h4l5-4v14l-5-4H3Zm13-2a7 7 0 0 1 0 10m3-13a11 11 0 0 1 0 16',
  spark:'m12 2 2.8 7.2L22 12l-7.2 2.8L12 22l-2.8-7.2L2 12l7.2-2.8Z',
  chevron:'m9 5 7 7-7 7', note:'M5 3h10l4 4v14H5Zm10 0v5h4M8 12h8M8 16h6'
};
const icon = (name, cls='') => `<svg class="icon ${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${paths[name] || paths.reading}"/></svg>`;
const groups = [['home','今日学习'],['plan','学习计划'],['reading','阅读书房'],['listening','听力练习'],['speaking','口语与衔接'],['words','我的生词本']];
const types = {reading:['阅读','20 分钟训练'],listening:['听力','10 分钟精听'],speaking:['口语','10 分钟表达'],bridge:['雅思衔接','按单元分次完成'],check:['检查','独立完成后核对']};
const titleOf = lesson => lesson.title.replace(/^(?:R\d+|L\d+ 与 V\d+|S\d+|U\d+)\s*/, '');
const lessonGroup = lesson => ['bridge','check'].includes(lesson.type) ? 'speaking' : lesson.type;
let route='home', current=null, week=Math.ceil((D.days.find(d=>!state.days[d.day])?.day || 84)/7);
let editingWord=null, wordFilter='all', courseFilter='all', focusMode=false, toastTimer;

function toast(message, undo) {
  const el=$('#toast'); clearTimeout(toastTimer);
  el.innerHTML=`${icon('check')}<span>${esc(message)}</span>${undo ? '<button id="undoAction">撤销</button>' : ''}`;
  el.hidden=false;
  if (undo) $('#undoAction').onclick=()=>{undo();el.hidden=true;};
  toastTimer=setTimeout(()=>el.hidden=true,undo?8000:3500);
}
function nav() {
  $('#nav').innerHTML=groups.map(([id,label])=>`<button class="nav-button ${route===id?'active':''}" data-nav="${id}" ${route===id?'aria-current="page"':''}>${icon(id)}<span>${label}</span>${id==='words'&&state.words.length?`<span class="nav-count">${state.words.length}</span>`:''}</button>`).join('');
  $('#nav').querySelectorAll('[data-nav]').forEach(b=>b.onclick=()=>navigate(b.dataset.nav));
  $('#settingsButton').classList.toggle('active',route==='settings');
}
function stopMedia() {
  let changed=false;
  document.querySelectorAll('audio,video').forEach(media=>{
    if(media.dataset?.lesson && Number.isFinite(media.currentTime)) {state.media[media.dataset.lesson]=media.currentTime;delete media.dataset.lesson;changed=true;}
    for(const event of ['onpause','onplay','ontimeupdate','onloadedmetadata','onerror','onended'])media[event]=null;
    media.pause();
  });
  if(changed)save();
}
function navigate(next) {
  stopMedia();
  route=next; current=null; editingWord=null; focusMode=false;
  document.body.classList.remove('focus-mode'); nav(); render(); window.scrollTo(0,0);
}
function heading(kicker,title,description,action='') {
  return `<div class="page-heading"><div><p class="eyebrow">${kicker}</p><h1>${title}</h1><p class="description">${description}</p></div>${action}</div>`;
}
function sectionTitle(title,detail='') { return `<div class="section-title"><h2>${title}</h2>${detail}</div>`; }
function empty(title,description) { return `<div class="empty-state">${icon('search')}<h3>${title}</h3><p>${description}</p></div>`; }
function courseRows(lessons) {
  return lessons.map(l=>`<button class="course-row" data-open="${l.id}"><span class="course-symbol ${lessonGroup(l)}">${icon(lessonGroup(l))}</span><span class="course-row-text"><strong>${esc(titleOf(l))}</strong><small>${l.id.toUpperCase()} <span>·</span> ${types[l.type][0]} <span>·</span> ${types[l.type][1]}</small></span><span class="row-state">${marked(l)?(l.previewOnly?'已预览文字':icon('check')):(l.previewOnly?'预览':'学习')}</span>${icon('chevron')}</button>`).join('');
}
function cards(lessons) {
  if (!lessons.length) return empty('没有找到匹配的课程','换一个关键词，或选择「全部课程」。');
  return `<div class="course-grid">${lessons.map(l=>`<button class="course-card ${lessonGroup(l)}" data-open="${l.id}"><div class="course-card-top"><span class="course-number">${l.id.toUpperCase()}</span><span class="lesson-status ${marked(l)?'done':''}">${marked(l)?icon('check')+(l.previewOnly?'已预览文字':'已完成'):(l.previewOnly?'文字预览':types[l.type][0])}</span></div><span class="card-art" aria-hidden="true">${icon(lessonGroup(l))}<i></i><i></i></span><h3>${esc(titleOf(l))}</h3><p>${l.previewOnly?'题面预览 / 音频待补 / 不计听力完成':l.type==='reading'?'短文阅读 / 理解练习 / 自主表达':l.type==='listening'?'原声对话 / 完整视频 / 跟读练习':'情境练习 / 独立思考 / 开口表达'}</p><div class="course-card-bottom"><span>${icon('clock')}${types[l.type][1]}</span><span class="card-go">${state.last===l.id?'继续学习':'开始学习'} ${icon('arrow')}</span></div></button>`).join('')}</div>`;
}
function bindOpen(root=document) {
  root.querySelectorAll('[data-open]').forEach(b=>b.onclick=()=>openLesson(b.dataset.open));
  root.querySelectorAll('[data-route]').forEach(b=>b.onclick=()=>navigate(b.dataset.route));
}
function bindLinks(root) {
  root.querySelectorAll('a').forEach(a=>a.onclick=e=>{e.preventDefault();const href=a.getAttribute('href');if(href?.startsWith('#')&&D.lessons.some(l=>l.id===href.slice(1)))openLesson(href.slice(1));else toast('对应材料可在课程目录中找到');});
}
function heroArt() {
  return `<svg class="hero-art" viewBox="0 0 330 250" fill="none" aria-hidden="true"><circle cx="190" cy="120" r="105" fill="#E6E5F3"/><circle cx="190" cy="120" r="82" stroke="#CFCDDF" stroke-dasharray="3 8"/><ellipse cx="185" cy="220" rx="103" ry="13" fill="#DDDBE8"/><g transform="rotate(-12 175 130)"><rect x="80" y="64" width="156" height="152" rx="12" fill="#333650"/><path d="M98 72h132v128H98c-8 0-12 4-12 8V84c0-7 5-12 12-12Z" fill="#F9F7F2"/><path d="M104 61h132v135H104c-8 0-14 3-18 8V77c0-9 8-16 18-16Z" fill="#8E92C2"/><path d="M109 61v135" stroke="#B9BCE0" stroke-width="2"/><path d="M133 94h70M133 106h51" stroke="#DEE0F2" stroke-width="3" stroke-linecap="round"/><path d="m154 135 7 6 16-21" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M199 61v40l11-7 11 7V61" fill="#ED986E"/></g><rect x="224" y="135" width="68" height="68" rx="20" transform="rotate(12 224 135)" fill="#FFF"/><path d="m243 159 20 16-20 8Z" fill="#E48E61"/><path d="m65 59 4 10 10 4-10 4-4 10-4-10-10-4 10-4Z" fill="#E8A37F"/><circle cx="267" cy="66" r="5" fill="#9CA0C7"/></svg>`;
}
function renderHome() {
  const done=completedCount(), completedDays=Object.keys(state.days).length;
  const next=D.days.find(d=>!state.days[d.day]), day=next?.day||84;
  const w=Math.ceil(day/7), weekDays=D.days.filter(d=>Math.ceil(d.day/7)===w);
  const last=D.lessons.find(l=>l.id===state.last)||D.lessons[0];
  const progress=Math.round(done/trainingLessons().length*100), unread=state.words.filter(w=>!w.reviewed).length;
  const recommended=D.lessons.filter(l=>!marked(l)&&['r01','l01','r02','u01'].includes(l.id)).slice(0,3);
  const date=new Intl.DateTimeFormat('zh-CN',{month:'long',day:'numeric',weekday:'long'}).format(new Date());
  return heading('A LITTLE EVERY DAY','今天，也向前一步。','不必一次学会很多。读一篇，听一段，再试着说出来。',`<span class="date-label">${date}</span>`)+
    `<div class="dashboard"><div class="dashboard-main"><section class="hero"><div class="hero-copy"><span class="tiny-label">YOUR NEXT CHAPTER</span><h2>让英语，成为<br>生活的一部分。</h2><p>从 ${last.id.toUpperCase()} 开始，继续你的学习旅程。</p><button class="button primary" data-open="${last.id}">继续学习 ${icon('arrow')}</button><span class="hero-caption">${esc(titleOf(last))}</span></div>${heroArt()}</section>
    ${sectionTitle('选择一种方式，进入英语', '<span class="subtle">LEARN YOUR WAY</span>')}<div class="path-cards"><button class="path-card path-reading" data-route="reading"><span class="path-icon">${icon('reading')}</span><span><small>READ & UNDERSTAND</small><h3>从一篇好读的短文开始</h3><p>24 篇短文 · 理解、积累、复述</p></span>${icon('arrow')}</button><button class="path-card path-listening" data-route="listening"><span class="path-icon">${icon('listening')}</span><span><small>LISTEN & SPEAK</small><h3>听见英语的真实节奏</h3><p>12 课原声 · 音频与完整视频</p></span>${icon('arrow')}</button></div>
    ${sectionTitle('下一步，学点什么', '<button class="text-button" data-route="reading">查看课程 '+icon('arrow')+'</button>')}<div class="panel recommended">${courseRows(recommended.length?recommended:D.lessons.filter(l=>!marked(l)).slice(0,3))||'<p class="completion-message">现有训练单元已标记完成，文字预览另记；新增完整听力仍待补齐。</p>'}</div></div>
    <aside class="dashboard-side"><section class="panel week-panel"><div class="section-title"><h2>你的学习节奏</h2><span class="badge">第 ${w} 周</span></div><p class="muted">${next?'今天，从第 '+day+' 天继续':'84 天已完成，给自己一个肯定。'}</p><div class="week-dots">${weekDays.map(d=>`<button class="week-dot ${state.days[d.day]?'done':''} ${d.day===day?'today':''}" data-plan-day="${d.day}" aria-label="查看第 ${d.day} 天${state.days[d.day]?'，已完成':''}">${state.days[d.day]?icon('check'):d.day}<span>D${d.day}</span></button>`).join('')}</div><div class="progress-track"><span style="width:${Math.round(completedDays/84*100)}%"></span></div><div class="mini-row"><span>计划已完成</span><strong>${completedDays}<small> / 84 天</small></strong></div><button class="button secondary full" data-route="plan">查看学习计划 ${icon('arrow')}</button></section>
    <section class="panel overview"><div class="section-title"><h2>一点点，积累看得见</h2>${icon('spark')}</div><div class="progress-overview"><svg viewBox="0 0 100 100" class="progress-ring" aria-hidden="true"><circle cx="50" cy="50" r="42" fill="none" stroke="#eeedf2" stroke-width="6"/><circle cx="50" cy="50" r="42" fill="none" stroke="#8987b8" stroke-width="6" stroke-linecap="round" pathLength="100" stroke-dasharray="${progress} 100" transform="rotate(-90 50 50)"/><text x="50" y="55" text-anchor="middle">${progress}%</text></svg><div><strong>${done}<small> / ${trainingLessons().length}</small></strong><span>学习单元已完成</span></div></div><p class="fine-print">文字预览已读 ${Object.keys(state.previewRead).length} / ${D.lessons.filter(l=>l.previewOnly).length}，不计训练完成。</p><div class="overview-divider"></div><button class="word-summary" data-route="words"><span class="small-icon">${icon('words')}</span><span><strong>${state.words.length} 个收藏表达</strong><small>${unread?unread+' 个表达待复习':'给喜欢的表达留一个位置'}</small></span>${icon('chevron')}</button></section>
    <div class="daily-note"><span class="quote-mark">“</span><p>Small steps.<br>Real progress.</p><span>每一个小小的坚持，都算数。</span></div></aside></div>`;
}
function renderPlan() {
  const days=D.days.filter(d=>Math.ceil(d.day/7)===week),done=days.filter(d=>state.days[d.day]).length;
  const phases=['找回习惯','积累表达','连接信息'];
  return heading('YOUR 12-WEEK ROADMAP','把目标，拆成每一天。','每天约 30 分钟。材料、训练步骤和产出，都替你安排好了。')+
  `<div class="plan-layout"><aside class="panel week-list"><p class="eyebrow">12 周学习路线</p>${Array.from({length:12},(_,i)=>{const n=D.days.filter(d=>Math.ceil(d.day/7)===i+1&&state.days[d.day]).length;return `<button data-week="${i+1}" class="week-choice ${week===i+1?'active':''}"><span class="week-index">${String(i+1).padStart(2,'0')}</span><span><strong>第 ${i+1} 周</strong><small>${phases[Math.floor(i/4)]}</small></span><span class="week-count">${n}/7</span></button>`;}).join('')}</aside><section><div class="plan-week-heading"><div><span class="eyebrow">WEEK ${String(week).padStart(2,'0')}</span><h2>${phases[Math.floor((week-1)/4)]}，从今天的练习开始</h2></div><span class="badge">${done} / 7 天完成</span></div><div class="day-list">${days.map(d=>`<details class="day-card" id="day-${d.day}" ${d.day===(D.days.find(x=>!state.days[x.day])?.day)?'open':''}><summary><span class="day-index ${state.days[d.day]?'done':''}">${state.days[d.day]?icon('check'):String(d.day).padStart(2,'0')}</span><span class="day-heading"><small>DAY ${d.day}</small><strong>${esc(d.title)}</strong></span><span class="day-status">${state.days[d.day]?'已完成':'查看任务'}</span>${icon('chevron')}</summary><div class="day-body"><div class="day-materials">${d.materials}</div><div class="task-block"><span>01</span><div><h3>今天这样练</h3><p>${esc(d.steps)}</p></div></div><div class="task-block"><span>02</span><div><h3>留下你的学习成果</h3><p>${esc(d.output)}</p></div></div><button class="button ${state.days[d.day]?'secondary':'primary'}" data-day="${d.day}">${icon('check')}${state.days[d.day]?'撤销完成':'完成今天的任务'}</button></div></details>`).join('')}</div></section></div>`;
}
function renderLibrary() {
  const label=route==='reading'?'阅读书房':route==='listening'?'听见英语的真实节奏。':'从理解，到自然表达。';
  const description=route==='reading'?'从短文里读懂情境，把新表达变成自己的句子。':route==='listening'?'先听声音，再看文本。每一次重听，都能多发现一点。':'用角色对话、追问和改写，把学过的英语说出来。';
  return heading('YOUR PERSONAL LIBRARY',label,description)+`<div class="library-toolbar"><div class="segmented" role="group" aria-label="课程筛选"><button data-filter="all" class="${courseFilter==='all'?'active':''}">全部课程</button><button data-filter="todo" class="${courseFilter==='todo'?'active':''}">${route==='speaking'?'未完成 / 未预览':'未完成'}</button><button data-filter="done" class="${courseFilter==='done'?'active':''}">${route==='speaking'?'已完成 / 已预览':'已完成'}</button></div><label class="search-box">${icon('search')}<input id="courseSearch" type="search" placeholder="搜索标题或编号" aria-label="搜索当前课程"></label></div><div class="results-meta"><span id="resultCount"></span><span>由浅入深 · 随时重学</span></div><div id="courseList"></div>`;
}
function drawLibrary() {
  const query=$('#courseSearch').value.trim().toLowerCase();
  const items=D.lessons.filter(l=>lessonGroup(l)===route&&(l.title+' '+l.id).toLowerCase().includes(query)&&(courseFilter==='all'||!!marked(l)===(courseFilter==='done')));
  $('#courseList').innerHTML=cards(items); $('#resultCount').textContent=items.length+' 个学习单元'; bindOpen($('#courseList'));
}
function renderWords() {
  return heading('MAKE WORDS YOUR OWN','有用的表达，值得留下。','记下它的意思，再写一句属于自己的例句。',`<span class="count-badge">${state.words.length} 个收藏</span>`)+
  `<section class="panel word-composer"><div class="composer-title">${icon('plus')}<h2 id="wordFormTitle">添加一个新表达</h2></div><form id="wordForm"><label>单词或短语<input id="term" placeholder="例如：keep going" maxlength="200" required></label><label>含义或你的例句<input id="meaning" placeholder="例如：继续前进。Keep going, one step at a time." maxlength="2000" required></label><div class="form-actions"><button class="button primary" id="wordSubmit">${icon('plus')}添加表达</button><button class="button secondary" type="button" id="wordCancel" hidden>取消</button></div></form></section><div class="library-toolbar"><div class="segmented" role="group" aria-label="生词筛选">${[['all','全部表达'],['todo','待复习'],['done','已复习']].map(([id,text])=>`<button data-word-filter="${id}" class="${wordFilter===id?'active':''}">${text}</button>`).join('')}</div><label class="search-box">${icon('search')}<input type="search" id="wordSearch" placeholder="搜索表达或释义" aria-label="搜索生词"></label></div><div id="wordList"></div>`;
}
function resetWordForm() {
  editingWord=null; $('#wordForm').reset(); $('#wordSubmit').innerHTML=icon('plus')+'添加表达'; $('#wordFormTitle').textContent='添加一个新表达'; $('#wordCancel').hidden=true;
}
function drawWords() {
  if ($(".count-badge")) $(".count-badge").textContent=state.words.length+" 个收藏";
  const query=$('#wordSearch').value.toLowerCase();
  const items=state.words.map((word,index)=>({word,index})).filter(({word})=>(word.term+' '+word.meaning).toLowerCase().includes(query)&&(wordFilter==='all'||word.reviewed===(wordFilter==='done')));
  $('#wordList').innerHTML=items.length?`<div class="word-grid">${items.map(({word:w,index:i})=>`<article class="panel word-card"><div class="word-card-top"><span class="lesson-status ${w.reviewed?'done':''}">${w.reviewed?icon('check')+'已复习':'待复习'}</span><div class="word-actions"><button class="icon-button" data-edit="${i}" aria-label="编辑 ${esc(w.term)}">${icon('edit')}</button><button class="icon-button" data-delete="${i}" aria-label="移除 ${esc(w.term)}">${icon('trash')}</button></div></div><h3>${esc(w.term)}</h3><p>${esc(w.meaning)}</p><div class="word-card-bottom">${D.lessons.some(l=>l.id===w.source)?`<button class="text-button" data-open="${esc(w.source)}">来自 ${esc(w.source.toUpperCase())} ${icon('arrow')}</button>`:'<span class="muted">手动收藏</span>'}<button class="review-button ${w.reviewed?'reviewed':''}" data-review="${i}">${icon('check')}${w.reviewed?'标为待复习':'我记住了'}</button></div></article>`).join('')}</div>`:empty(state.words.length?'没有匹配的表达':'你的第一条表达，会是什么？',state.words.length?'试试其他关键词或复习状态。':'阅读时选中文字收藏，或在上方手动添加。');
  $('#wordList').querySelectorAll('[data-edit]').forEach(b=>b.onclick=()=>{editingWord=+b.dataset.edit;const w=state.words[editingWord];$('#term').value=w.term;$('#meaning').value=w.meaning;$('#wordSubmit').innerHTML=icon('check')+'保存修改';$('#wordFormTitle').textContent='编辑收藏表达';$('#wordCancel').hidden=false;$('#meaning').focus();window.scrollTo({top:0,behavior:'smooth'});});
  $('#wordList').querySelectorAll('[data-review]').forEach(b=>b.onclick=()=>{const w=state.words[+b.dataset.review];w.reviewed=!w.reviewed;save();drawWords();});
  $('#wordList').querySelectorAll('[data-delete]').forEach(b=>b.onclick=()=>{const i=+b.dataset.delete,[removed]=state.words.splice(i,1);resetWordForm();save();drawWords();nav();toast('表达已移除',()=>{state.words.splice(Math.min(i,state.words.length),0,removed);save();if(route==='words')drawWords();nav();});});
  bindOpen($('#wordList'));
}
function renderSettings() {
  return heading('YOUR SPACE, YOUR PACE','让学习，安心留在本机。','管理学习备份与阅读偏好。你的记录只属于你。')+
  `<div class="settings-grid"><section class="panel settings-panel"><span class="settings-icon">${icon('download')}</span><h2>学习记录与备份</h2><p>课程进度、笔记、生词本和音频位置都会保存在这台电脑上。升级应用前，建议导出一份备份。</p><div class="backup-summary"><span><strong>${completedCount()}</strong>完成单元</span><span><strong>${Object.values(state.notes).filter(Boolean).length}</strong>课程笔记</span><span><strong>${state.words.length}</strong>收藏表达</span></div><div class="settings-buttons"><button id="export" class="button primary">${icon('download')}导出学习备份</button><button id="import" class="button secondary">${icon('upload')}恢复备份</button></div><p class="fine-print">恢复会替换当前记录，操作前会再次提醒。兼容 0.1 版备份。</p></section><section class="panel settings-panel"><span class="settings-icon">${icon('reading')}</span><h2>适合自己的阅读字号</h2><p>设置将用于所有课程正文，也可以在阅读时随时调整。</p><div class="font-options">${[16,18,21].map(n=>`<button data-font="${n}" class="${state.preferences.fontSize===n?'active':''}"><span>${n===16?'A':n===18?'Aa':'Aa'}</span>${n===16?'紧凑':n===18?'标准':'舒展'}</button>`).join('')}</div><p class="font-preview" style="font-size:${state.preferences.fontSize}px">Small steps make a difference.<br>每一天，都比昨天多懂一点。</p></section><section class="panel settings-panel about-panel"><div><span class="badge">拾阶英语 ${esc(D.version)}</span><h2>为专注而设计，为长期学习而生。</h2><p>雅思英语学习路线 · 本机离线客户端。原创练习用于英语基础训练，并非官方真题，不承诺提分。与 IELTS 或 VOA 官方无隶属关系。</p><p class="fine-print">原创课程：RayXBuilds · CC BY 4.0。教学对话与媒体：VOA Learning English。程序代码：MIT。</p></div><details><summary>查看完整来源与许可 ${icon('chevron')}</summary><pre class="credits">${esc(D.credits)}</pre></details></section></div>`;
}
function render() {
  $('#crumb').textContent=groups.find(g=>g[0]===route)?.[1]||'设置与备份';
  const v=$('#view');
  if(route==='home') v.innerHTML=renderHome();
  else if(route==='plan') v.innerHTML=renderPlan();
  else if(route==='words') v.innerHTML=renderWords();
  else if(route==='settings') v.innerHTML=renderSettings();
  else v.innerHTML=renderLibrary();
  bindOpen(v);bindLinks(v);
  v.querySelectorAll('[data-plan-day]').forEach(b=>b.onclick=()=>{week=Math.ceil(+b.dataset.planDay/7);navigate('plan');const d=$('#day-'+b.dataset.planDay);d.open=true;d.scrollIntoView({block:'center'});});
  v.querySelectorAll('[data-week]').forEach(b=>b.onclick=()=>{week=+b.dataset.week;render();});
  v.querySelectorAll('[data-day]').forEach(b=>b.onclick=()=>{const id=b.dataset.day;if(state.days[id])delete state.days[id];else state.days[id]=true;save();render();const d=$('#day-'+id);d.open=true;});
  v.querySelectorAll('[data-filter]').forEach(b=>b.onclick=()=>{courseFilter=b.dataset.filter;v.querySelectorAll('[data-filter]').forEach(x=>x.classList.toggle('active',x===b));drawLibrary();});
  if($('#courseSearch')){$('#courseSearch').oninput=drawLibrary;drawLibrary();}
  if(route==='words') {
    drawWords(); $('#wordSearch').oninput=drawWords;
    v.querySelectorAll('[data-word-filter]').forEach(b=>b.onclick=()=>{wordFilter=b.dataset.wordFilter;v.querySelectorAll('[data-word-filter]').forEach(x=>x.classList.toggle('active',x===b));drawWords();});
    $('#wordCancel').onclick=resetWordForm;
    $('#wordForm').onsubmit=e=>{e.preventDefault();const term=$('#term').value.trim(),meaning=$('#meaning').value.trim();if(!term||!meaning)return;
      if(editingWord===null){if(!addWord(term,meaning,''))return;}
      else {if(state.words.some((w,i)=>i!==editingWord&&w.term.toLowerCase()===term.toLowerCase())){toast('已有同名表达');return;}Object.assign(state.words[editingWord],{term,meaning,reviewed:false});save();toast('表达已更新');}
      resetWordForm();drawWords();nav();};
  }
  if(route==='settings') {$('#export').onclick=exportBackup;$('#import').onclick=importBackup;v.querySelectorAll('[data-font]').forEach(b=>b.onclick=()=>{state.preferences.fontSize=+b.dataset.font;save();render();});}
}

function playerHTML(id) {
  return `<section class="audio-player" aria-label="音频播放器"><audio id="audio" preload="metadata" src="../assets/voa/lesson-${id.slice(1)}.mp3"></audio><div class="player-heading"><span>${icon('listening')}原声对话</span><span class="badge">VOA LEARNING ENGLISH</span></div><div class="player-main"><button id="playAudio" class="play-button" aria-label="播放音频" disabled>${icon('play')}</button><div class="player-track"><div class="track-caption"><strong>先听，再看文本</strong><span id="audioTime">加载中…</span></div><input id="seekAudio" type="range" min="0" max="100" step="0.1" value="0" aria-label="音频播放进度" disabled><span class="track-hint" id="audioHint">跟读前，先完整听一遍。</span></div></div><div class="player-tools"><button id="rewind" class="text-button">${icon('rewind')}后退 5 秒</button><label>倍速 <select id="speed" aria-label="播放速度"><option value="0.75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option></select></label><button id="loop" class="text-button" aria-pressed="false">循环播放</button></div><p id="mediaError" class="media-error" role="alert" hidden></p></section><details class="video-panel"><summary>${icon('play')}观看完整教学视频<span>展开</span></summary><video controls playsinline preload="none" src="../assets/voa/lesson-${id.slice(1)}.mp4"></video><p>文本对应对话音频，完整视频还包含其他教学内容。</p></details>`;
}
function openLesson(id) {
  const l=D.lessons.find(l=>l.id===id); if(!l)return;
  stopMedia();
  state.last=id;current=id;route=lessonGroup(l);save();nav();
  $('#crumb').textContent=types[l.type][0]+' / '+id.toUpperCase();
  const sequence=D.lessons.filter(item=>lessonGroup(item)===route), position=sequence.findIndex(item=>item.id===id),next=sequence[position+1];
  const statusLabel=()=>l.previewOnly?(marked(l)?'已预览文字 · 撤销':'标记文字已读'):(marked(l)?'已完成 · 撤销':'标记完成');
  const content=l.html.replace(/<h2>.*?<\/h2>/s,'');
  $('#view').innerHTML=`<div class="study-toolbar"><button id="back" class="text-button">${icon('back')}返回课程</button><div class="study-tools"><label class="reader-size">字号 <select id="readerSize" aria-label="正文字号">${[16,18,21].map(n=>`<option value="${n}" ${state.preferences.fontSize===n?'selected':''}>${n===16?'紧凑':n===18?'标准':'舒展'}</option>`).join('')}</select></label><button id="focus" class="icon-label" aria-pressed="${focusMode}">${icon('focus')}<span>${focusMode?'退出专注':'专注阅读'}</span></button><button id="complete" class="button ${marked(l)?'secondary':'primary'}">${icon('check')}${statusLabel()}</button></div></div><div class="study-heading"><span class="eyebrow">${id.toUpperCase()} <span> / </span> ${types[l.type][0]}</span><h1>${esc(titleOf(l))}</h1><div class="study-meta"><span>${icon('clock')}${types[l.type][1]}</span><span>${icon('note')}理解 · 练习 · 表达</span><span>第 ${position+1} / ${sequence.length} 单元</span></div></div><div class="study-layout"><div class="study-main">${l.type==='listening'?playerHTML(id):''}<article class="lesson" style="--reading-size:${state.preferences.fontSize}px">${content}</article><div class="lesson-end"><div>${icon('spark')}<span>学完后，试着不用原文说出三个要点。</span></div>${next?`<button class="button secondary" data-open="${next.id}">下一课 ${icon('arrow')}</button>`:''}</div></div><aside class="study-aside"><section class="panel note-panel"><div class="section-title"><h2>${icon('note')}我的学习笔记</h2></div><p>留下自己的理解，比抄下原文更有用。</p><textarea id="notes" maxlength="200000" placeholder="写三句摘要，或记录一个想再听懂的地方…" aria-label="学习笔记"></textarea><div class="note-status"><span class="status-dot"></span><span id="saveStatus">输入后自动保存</span></div></section><section class="panel collect-panel"><span class="small-icon">${icon('words')}</span><h3>遇到好表达，留下来</h3><p>先选中正文里的单词或短语，再点击收藏。</p><button class="button secondary full" id="collect">${icon('plus')}收藏选中文本</button></section><section class="lesson-outline"><span class="eyebrow">本课导航</span><nav id="outline"></nav></section></aside></div>`;
  $('#notes').value=state.notes[id]||'';
  $('#notes').oninput=()=>{state.notes[id]=$('#notes').value;$('#saveStatus').textContent='正在保存…';save();};
  $('#back').onclick=()=>navigate(route);
  $('#complete').onclick=()=>{
    const record=l.previewOnly?state.previewRead:state.completed;
    if(record[id])delete record[id];else record[id]=true;
    save();$('#complete').className='button '+(marked(l)?'secondary':'primary');
    $('#complete').innerHTML=icon('check')+statusLabel();
    toast(l.previewOnly?(marked(l)?'已记录文字预览，不计听力或训练完成。':'已撤销文字预览记录'):(marked(l)?'这一课完成了，继续保持。':'已撤销完成状态'));
  };
  $('#focus').onclick=()=>{focusMode=!focusMode;document.body.classList.toggle('focus-mode',focusMode);$('#focus').setAttribute('aria-pressed',String(focusMode));$('#focus span').textContent=focusMode?'退出专注':'专注阅读';};
  $('#readerSize').onchange=e=>{state.preferences.fontSize=+e.target.value;$('.lesson').style.setProperty('--reading-size',e.target.value+'px');save();};
  $('#collect').onmousedown=e=>e.preventDefault();
  $('#collect').onclick=()=>{const selection=window.getSelection();if(!selection?.toString().trim()||!$('.lesson').contains(selection.anchorNode)){toast('请先选中课程正文中的表达');return;}const text=selection.toString().trim();if(text.length>200){toast('请选择 200 字以内的单词或短语');return;}if(addWord(text,'待补充释义或例句',id))nav();};
  const updateOutline=()=>{
    const headings=[...$('.lesson').querySelectorAll('h3,h4')].filter(h=>!h.closest('details:not([open])'));
    $('#outline').innerHTML=headings.map((h,i)=>`<button data-section="${i}">${esc(h.textContent)}</button>`).join('');
    $('#outline').querySelectorAll('button').forEach(b=>b.onclick=()=>{
      const h=headings[+b.dataset.section];
      if(!h.closest('details:not([open])'))h.scrollIntoView({behavior:'smooth',block:'start'});
    });
  };
  $('.lesson').querySelectorAll('details').forEach(d=>d.addEventListener('toggle',updateOutline));
  updateOutline();
  bindLinks($('.lesson'));bindOpen($('#view'));if(l.type==='listening')bindPlayer(id);window.scrollTo(0,0);
}
function formatTime(seconds) { if(!Number.isFinite(seconds))return '0:00';seconds=Math.max(0,Math.floor(seconds));return Math.floor(seconds/60)+':'+String(seconds%60).padStart(2,'0'); }
function bindPlayer(id) {
  const a=$('#audio'), video=$('.video-panel video'),seek=$('#seekAudio'),button=$('#playAudio');let lastSave=0;a.dataset.lesson=id;
  function update() { $('#audioTime').textContent=formatTime(a.currentTime)+' / '+formatTime(a.duration);seek.value=a.currentTime;seek.style.setProperty('--position',(Number.isFinite(a.duration)?a.currentTime/a.duration*100:0)+'%');seek.setAttribute('aria-valuetext',formatTime(a.currentTime));button.innerHTML=icon(a.paused?'play':'pause');button.setAttribute('aria-label',a.paused?'播放音频':'暂停音频'); }
  function remember() { if(Number.isFinite(a.currentTime)){state.media[id]=a.currentTime;save();} }
  a.onloadedmetadata=()=>{seek.max=a.duration;seek.disabled=false;button.disabled=false;a.currentTime=Math.min(state.media[id]||0,Math.max(a.duration-1,0));update();};
  a.ontimeupdate=()=>{update();if(Date.now()-lastSave>3000){remember();lastSave=Date.now();}};
  a.onpause=()=>{update();remember();};a.onplay=()=>{video.pause();update();};a.onended=update;
  button.onclick=()=>{if(a.paused)a.play().catch(()=>toast('音频未能播放，请重试或重新下载完整包'));else a.pause();};
  seek.oninput=()=>{a.currentTime=+seek.value;update();};seek.onchange=remember;
  $('#speed').onchange=e=>a.playbackRate=+e.target.value;
  $('#rewind').onclick=()=>{a.currentTime=Math.max(0,a.currentTime-5);update();};
  $('#loop').onclick=()=>{a.loop=!a.loop;$('#loop').setAttribute('aria-pressed',String(a.loop));$('#loop').textContent=a.loop?'循环已开启':'循环播放';};
  a.onerror=()=>{button.disabled=true;seek.disabled=true;$('#mediaError').hidden=false;$('#mediaError').textContent='音频文件无法读取。请检查是否使用了完整客户端包。';$('#audioTime').textContent='加载失败';};
  video.onplay=()=>a.pause();video.onerror=()=>toast('视频文件无法读取，请重新下载完整客户端包');
}
function exportBackup() {
  const raw=JSON.stringify(state,null,2);
  if(window.NATIVE_MODE)native('export',raw);
  else {const url=URL.createObjectURL(new Blob([raw],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='stepwise-backup.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
}
function importBackup() {if(window.NATIVE_MODE)native('import',null);else if(confirm('恢复备份将替换当前记录。建议先导出备份，是否继续？'))$('#importFile').click();}
$('#importFile').onchange=async e=>{const f=e.target.files[0];if(f){if(f.size>10*1024*1024)toast('备份超过 10 MB');else window.restoreBackup(await f.text());}e.target.value='';};
function searchAll() {
  const query=$('#allSearch').value.toLowerCase().trim();
  const items=query?D.lessons.filter(l=>(l.title+' '+l.id).toLowerCase().includes(query)):D.lessons.slice(0,5);
  $('#searchResults').innerHTML=`<p class="search-caption">${query?items.length+' 个匹配课程':'从这些课程开始'}</p>`+(items.length?courseRows(items):empty('暂时没有找到','试试课程编号，或输入更短的关键词。'));
  $('#searchResults').querySelectorAll('[data-open]').forEach(b=>b.onclick=()=>{$('#searchDialog').close();openLesson(b.dataset.open);});
}
function openSearch() {$('#searchDialog').showModal();$('#allSearch').value='';searchAll();$('#allSearch').focus();}
$('#globalSearch').innerHTML=icon('search')+'<span>搜索课程</span><kbd>⌘ K</kbd>';$('#globalSearch').onclick=openSearch;
$('#closeSearch').innerHTML=icon('close');$('#closeSearch').onclick=()=>$('#searchDialog').close();
$('#searchIcon').innerHTML=icon('search');$('#allSearch').oninput=searchAll;
$('#searchDialog').onclick=e=>{if(e.target===$('#searchDialog')){const r=e.target.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)e.target.close();}};
$('#settingsButton').innerHTML=icon('settings')+'<span>设置与备份</span>';$('#settingsButton').onclick=()=>navigate('settings');
$('.brand').onclick=e=>{e.preventDefault();navigate('home');};
document.addEventListener('keydown',e=>{if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();if(!$('#searchDialog').open)openSearch();}});
navigate('home');
if(window.STATE_ERROR)setStorageWarning('学习记录读取异常，已暂停写入。请到「设置与备份」恢复有效备份，原文件已保留。');
