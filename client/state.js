'use strict';
const $ = selector => document.querySelector(selector);
const D = window.COURSE_DATA;
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const blank = () => ({version:1, completed:{}, days:{}, notes:{}, words:[], last:'r01', media:{}, preferences:{fontSize:18}});

// Version 1 backups from the original client remain readable. Imported strings
// are data only; lesson identifiers are checked against the bundled curriculum.
function validate(value) {
  if (!value || value.version !== 1 || !Array.isArray(value.words) || value.words.length > 10000) throw Error('备份格式不正确');
  const next = blank();
  const ids = new Set(D.lessons.map(l => l.id));
  for (const key of ['completed','days','notes','media']) {
    if (!value[key] || typeof value[key] !== 'object' || Array.isArray(value[key])) throw Error('备份字段缺失');
  }
  for (const [id, v] of Object.entries(value.completed)) if (ids.has(id) && v === true) next.completed[id] = true;
  for (const [id, v] of Object.entries(value.days)) if (/^\d+$/.test(id) && +id >= 1 && +id <= 84 && v === true) next.days[id] = true;
  for (const [id, v] of Object.entries(value.notes)) if (ids.has(id) && typeof v === 'string') {
    if (v.length > 200000) throw Error('笔记超过长度限制');
    next.notes[id] = v;
  }
  for (const [id, v] of Object.entries(value.media)) if (ids.has(id) && /^l\d{2}$/.test(id) && Number.isFinite(v) && v >= 0 && v < 86400) next.media[id] = v;
  next.words = value.words.map(w => {
    if (!w || typeof w.term !== 'string' || typeof w.meaning !== 'string' || !w.term.trim() || w.term.length > 200 || w.meaning.length > 2000) throw Error('生词格式不正确');
    return {term:w.term, meaning:w.meaning, source:typeof w.source === 'string' ? w.source.slice(0,100) : '', reviewed:!!w.reviewed};
  });
  if (ids.has(value.last)) next.last = value.last;
  if ([16,18,21].includes(value.preferences?.fontSize)) next.preferences.fontSize = value.preferences.fontSize;
  return next;
}
let state = blank();
try {
  const raw = window.NATIVE_MODE ? window.NATIVE_STATE : JSON.parse(localStorage.getItem('stepwise.v1') || 'null');
  if (raw) state = validate(raw);
} catch (_) { window.STATE_ERROR = true; }

function native(action, payload) { window.webkit.messageHandlers.app.postMessage({action,payload}); }
function setStorageWarning(message) {
  const el = $('#storageWarning');
  if (el) { el.textContent = message; el.hidden = !message; }
}
window.nativeSaved = () => {
  const el = $('#saveStatus');
  if (el) el.textContent = '已保存到本机';
  if (!window.STATE_ERROR) setStorageWarning('');
};
window.nativeSaveFailed = message => {
  const el = $('#saveStatus');
  if (el) el.textContent = '尚未保存';
  setStorageWarning(message);
  toast(message);
};
window.nativeNotice = message => toast(message);
function save() {
  if (window.STATE_ERROR) { setStorageWarning('学习记录读取异常，已暂停写入以保留原文件。请到「设置与备份」恢复有效备份。'); return false; }
  try {
    const raw = JSON.stringify(state);
    if (new TextEncoder().encode(raw).length >= 10 * 1024 * 1024) throw Error('学习记录过大，请先导出并整理笔记');
    if (window.NATIVE_MODE) native('save',raw);
    else { localStorage.setItem('stepwise.v1',raw); window.nativeSaved(); }
    return true;
  } catch (error) { window.nativeSaveFailed(error.message || '保存失败，请导出备份'); return false; }
}
window.restoreBackup = raw => {
  try {
    const next = validate(JSON.parse(raw));
    // Stop the old player before replacement so its pause event cannot modify
    // newly imported playback positions.
    if (typeof stopMedia === 'function') stopMedia();
    else document.querySelectorAll('audio,video').forEach(media => media.pause());
    state = next;
    window.STATE_ERROR = false;
    const ok = save();
    navigate('home');
    if (ok) toast('备份已载入');
  } catch (error) { toast('无法恢复：' + error.message); }
};
function addWord(term, meaning, source) {
  term = term.trim(); meaning = meaning.trim();
  if (!term || !meaning) return false;
  if (term.length > 200 || meaning.length > 2000) { toast('表达或释义超过长度限制'); return false; }
  if (state.words.some(w => w.term.toLowerCase() === term.toLowerCase())) { toast('这个表达已经在生词本中'); return false; }
  if (state.words.length >= 10000) { toast('生词本已满，请先导出并整理'); return false; }
  state.words.push({term,meaning,source,reviewed:false}); save(); toast('已收藏，可在生词本补充例句'); return true;
}
