'use strict';
// PD Animatic Review — client. JSON on the server is the source of truth; localStorage is aux.

const $ = (s) => document.querySelector(s);
const video = $('#video');
let meta = {fps: 30, duration_seconds: null};
let review = null;
let fps = 30;
let captured = null; // {frame, seconds, timecode}
const STATE_JA = {not_started: '未開始', first_pass: '1回目視聴中', second_pass: '2回目コメント入力中', completed: 'レビュー完了'};

function fmtTc(seconds) {
  if (!isFinite(seconds) || seconds < 0) seconds = 0;
  const ms = Math.round((seconds - Math.floor(seconds)) * 1000);
  const s = Math.floor(seconds);
  const p = (n) => String(n).padStart(2, '0');
  return `${p(Math.floor(s / 3600))}:${p(Math.floor((s % 3600) / 60))}:${p(s % 60)}.${String(ms).padStart(3, '0')}`;
}
function nextId(prefix, arr, key) {
  let max = 0;
  for (const it of arr) { const m = /-(\d{4})$/.exec(it[key] || ''); if (m) max = Math.max(max, +m[1]); }
  return `${prefix}-${String(max + 1).padStart(4, '0')}`;
}
function pos() {
  const seconds = video.currentTime || 0;
  return {frame: Math.round(seconds * fps), seconds, timecode: fmtTc(seconds), fps};
}
function setSave(text, ok = true) {
  const el = $('#saveStatus'); el.textContent = text; el.className = 'save ' + (ok ? 'ok' : 'err');
}

async function api(method, path, body) {
  const r = await fetch(path, {method, headers: {'Content-Type': 'application/json'}, body: body ? JSON.stringify(body) : undefined});
  return r.ok ? r.json() : Promise.reject(await r.json().catch(() => ({error: r.statusText})));
}

async function saveReview() {
  const p = pos();
  review.player_state.current_frame = p.frame;
  review.player_state.current_seconds = p.seconds;
  review.player_state.playback_rate = video.playbackRate;
  review.session.updated_at = new Date().toISOString();
  try {
    const res = await api('PUT', '/api/review', review);
    setSave('保存OK ' + (res.last_saved_at || ''), true);
  } catch (e) { setSave('保存失敗: ' + (e.error || e), false); }
}

let draftTimer = null;
function autosaveDraft() {
  clearTimeout(draftTimer);
  draftTimer = setTimeout(() => {
    const draft = {
      active: !!captured, category: $('#category').value, severity: $('#severity').value,
      original_comment_ja: $('#commentText').value, timecode: captured ? captured.timecode : null,
      frame: captured ? captured.frame : null, seconds: captured ? captured.seconds : null,
      updated_at: new Date().toISOString(),
    };
    review.draft = draft;
    api('PUT', '/api/review/draft', draft).then(() => setSave('下書き自動保存', true)).catch(() => {});
    localStorage.setItem('pd_review_pos', String(video.currentTime || 0));
  }, 1500);
}

function render() {
  $('#reviewState').textContent = STATE_JA[review.review_state] || review.review_state;
  $('#mCount').textContent = review.markers.length;
  $('#cCount').textContent = review.comments.length;
  const ml = $('#markerList'); ml.innerHTML = '';
  for (const m of review.markers) {
    const li = document.createElement('li');
    li.innerHTML = `<a href="#" data-t="${m.seconds}">${m.timecode}</a> <b>${m.marker_type}</b>${m.note_ja ? ' · ' + m.note_ja : ''}`;
    ml.appendChild(li);
  }
  const cl = $('#commentList'); cl.innerHTML = '';
  for (const c of review.comments) {
    const li = document.createElement('li');
    li.innerHTML = `<a href="#" data-t="${c.seconds}">${c.timecode}</a> <b>${c.category}/${c.severity}</b> ${c.original_comment_ja}`;
    cl.appendChild(li);
  }
  document.querySelectorAll('[data-t]').forEach((a) => a.addEventListener('click', (e) => {
    e.preventDefault(); video.currentTime = +a.dataset.t; video.focus();
  }));
}

function setState(to) {
  if (review.review_state === to) return;
  review.state_history.push({from: review.review_state, to, changed_at: new Date().toISOString(), reason: 'owner_action'});
  review.review_state = to;
  if (to === 'completed') review.session.completed_at = new Date().toISOString();
  render(); saveReview();
}

function addMarker(type, severity = null) {
  const p = pos();
  review.markers.push({marker_id: nextId('MRK', review.markers, 'marker_id'), marker_type: type, severity,
    frame: p.frame, seconds: p.seconds, timecode: p.timecode, fps, scene_id: null, note_ja: null,
    created_at: new Date().toISOString()});
  if (review.review_state === 'not_started') setState('first_pass');
  render(); saveReview();
}

function capture() {
  captured = pos();
  $('#capTc').textContent = '位置: ' + captured.timecode;
  if (review.review_state !== 'completed') setState('second_pass');
  $('#commentText').focus();
}

function saveComment() {
  const text = $('#commentText').value.trim();
  if (!text) { setSave('コメントが空です', false); return; }
  const p = captured || pos();
  review.comments.push({comment_id: nextId('CMT', review.comments, 'comment_id'), marker_id: null,
    category: $('#category').value, severity: $('#severity').value, frame: p.frame, seconds: p.seconds,
    timecode: p.timecode, fps, scene_id: null, nearby_reference: null, original_comment_ja: text,
    instruction_en: null, translation_status: 'pending', status: 'open',
    created_at: new Date().toISOString(), updated_at: new Date().toISOString()});
  $('#commentText').value = ''; captured = null; $('#capTc').textContent = '位置: —';
  review.draft = {active: false, category: null, severity: null, original_comment_ja: '', timecode: null, frame: null, seconds: null, updated_at: null};
  render(); saveReview();
}

function showResume() {
  const hasWork = review.markers.length || review.comments.length;
  const draftActive = review.draft && review.draft.active;
  if (!hasWork && !draftActive) return;
  const last = review.player_state.current_seconds || 0;
  $('#resumeText').innerHTML = `前回のレビュー: <b>${STATE_JA[review.review_state]}</b> · ${fmtTc(last)} で中断` +
    `${draftActive ? ' · <b>未確定の下書きあり</b>' : ''} · マーカー${review.markers.length} / コメント${review.comments.length}`;
  $('#resume').classList.remove('hidden');
}

function bindKeys() {
  document.addEventListener('keydown', (e) => {
    const typing = ['TEXTAREA', 'INPUT', 'SELECT'].includes(document.activeElement.tagName);
    if (e.key === 'Escape') { $('#commentText').blur(); captured = null; $('#capTc').textContent = '位置: —'; return; }
    if (typing) {
      if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); saveComment(); }
      return;
    }
    switch (e.key) {
      case ' ': e.preventDefault(); video.paused ? video.play() : video.pause(); break;
      case 'ArrowLeft': video.currentTime = Math.max(0, video.currentTime - 5); break;
      case 'ArrowRight': video.currentTime += 5; break;
      case 'm': case 'M': capture(); break;
      case 'b': case 'B': addMarker('boring'); break;
      case 'u': case 'U': addMarker('unclear'); break;
      case 'a': case 'A': addMarker('awkward'); break;
      case 'x': case 'X': addMarker('blocker', 'blocker'); break;
      case '1': $('#severity').value = 'minor'; break;
      case '2': $('#severity').value = 'needs_fix'; break;
      case '3': $('#severity').value = 'blocker'; break;
      case 's': case 'S': saveReview(); break;
    }
  });
}

async function init() {
  meta = await api('GET', '/api/meta');
  fps = meta.fps || 30; $('#fps').textContent = fps;
  if (!meta.media_available) { setSave('動画が未レンダー: 先に miranda-animatic.mp4 を作成', false); }
  video.src = '/media/animatic.mp4';
  review = await api('GET', '/api/review');
  if (meta.duration_seconds) review.player_state.duration_seconds = meta.duration_seconds;
  review.player_state.fps = fps;

  video.addEventListener('loadedmetadata', () => {
    const d = isFinite(video.duration) ? video.duration : (meta.duration_seconds || 0);
    $('#duration').textContent = fmtTc(d);
    review.player_state.duration_seconds = review.player_state.duration_seconds || d;
    review.player_state.duration_frames = Math.round((review.player_state.duration_seconds || d) * fps);
  });
  video.addEventListener('timeupdate', () => { $('#timecode').textContent = fmtTc(video.currentTime); });

  // controls
  $('#playPause').onclick = () => video.paused ? video.play() : video.pause();
  document.querySelectorAll('[data-seek]').forEach((b) => b.onclick = () => { video.currentTime = Math.max(0, video.currentTime + (+b.dataset.seek)); });
  document.querySelectorAll('[data-rate]').forEach((b) => b.onclick = () => {
    video.playbackRate = +b.dataset.rate;
    document.querySelectorAll('[data-rate]').forEach((x) => x.classList.toggle('active', x === b));
  });
  document.querySelectorAll('[data-state]').forEach((b) => b.onclick = () => setState(b.dataset.state));
  document.querySelectorAll('[data-marker]').forEach((b) => b.onclick = () => addMarker(b.dataset.marker, b.dataset.marker === 'blocker' ? 'blocker' : null));
  $('#captureBtn').onclick = capture;
  $('#saveComment').onclick = saveComment;
  $('#cancelComment').onclick = () => { $('#commentText').value = ''; captured = null; $('#capTc').textContent = '位置: —'; };
  ['#commentText', '#category', '#severity'].forEach((s) => $(s).addEventListener('input', autosaveDraft));

  // resume
  document.querySelectorAll('[data-resume]').forEach((b) => b.onclick = () => {
    const mode = b.dataset.resume;
    if (mode === 'continue') video.currentTime = review.player_state.current_seconds || 0;
    else if (mode === 'lastComment' && review.comments.length) video.currentTime = review.comments[review.comments.length - 1].seconds;
    else if (mode === 'start') video.currentTime = 0;
    $('#resume').classList.add('hidden'); video.focus();
  });

  bindKeys();
  render();
  showResume();
  setSave('読み込み完了', true);
}

init().catch((e) => setSave('初期化失敗: ' + (e.error || e), false));
