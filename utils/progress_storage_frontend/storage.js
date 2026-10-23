// Component-v1 protocol, entirely local: no external scripts or network storage.
const KEY = 'physics-practice.progress.v1';
const CODE_KEY = 'physics-practice.code.v1';
const TTL = 24 * 60 * 60 * 1000;
const statusElement = document.getElementById('status');
const clearButton = document.getElementById('clear');
let args = null, queue = Promise.resolve(), lastSent = '', volatileSnapshot = null;
let confirmation = false;
function send(type, fields) {
  window.parent.postMessage({isStreamlitMessage:true, type, ...fields}, '*');
}
function resize() { send('streamlit:setFrameHeight', {height:document.body.scrollHeight}); }
function newCode() {
  // Rejection sampling avoids biased decimal digits; this is a label, not a login.
  let digits = '';
  while (digits.length < 16) {
    for (const byte of crypto.getRandomValues(new Uint8Array(24))) {
      if (byte < 250 && digits.length < 16) digits += byte % 10;
    }
  }
  return digits.match(/.{4}/g).join('-');
}
function fresh(code = newCode()) {
  return {version:1, generation:crypto.randomUUID(), code,
          expires_at:Date.now() + TTL, history:[]};
}
function identity(legacyCode) {
  const stored = localStorage.getItem(CODE_KEY);
  if (/^\d{4}(-\d{4}){3}$/.test(stored)) return stored;
  // Preserve codes from the first implementation, including expired snapshots.
  const code = /^\d{4}(-\d{4}){3}$/.test(legacyCode) ? legacyCode : newCode();
  localStorage.setItem(CODE_KEY, code);
  return code;
}
function valid(value) {
  return value && value.version === 1 && typeof value.generation === 'string' &&
    value.generation.length > 0 &&
    /^\d{4}(-\d{4}){3}$/.test(value.code) && Number.isFinite(value.expires_at) &&
    value.expires_at <= Date.now() + TTL + 60000 && Array.isArray(value.history) &&
    new Set(value.history.map(row => row?._record_id)).size === value.history.length &&
    value.history.every(row => row && typeof row._record_id === 'string' && row._record_id.length > 0 &&
      typeof row.Activity === 'string' && ['Correct','Incorrect'].includes(row.Result) &&
      typeof row.Date === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(row.Date) &&
      typeof row.Difficulty === 'string' && typeof row.Explanation === 'string' &&
      ['Question', 'Your answer', 'Correct answer'].every(key => Object.hasOwn(row, key)) &&
      Array.isArray(row.Equations) && row.Equations.every(equation => typeof equation === 'string') &&
      row.Diagrams && typeof row.Diagrams === 'object' && !Array.isArray(row.Diagrams) &&
      Object.values(row.Diagrams).every(image => typeof image === 'string' &&
        /^data:image\/png;base64,[A-Za-z0-9+/]*={0,2}$/.test(image)));
}
function read() {
  const raw = localStorage.getItem(KEY);
  let value = null;
  try {
    value = JSON.parse(raw);
  } catch (_) { /* Invalid/expired data is deleted before it can be restored. */ }
  const code = identity(value?.code);
  if (valid(value) && value.code === code && value.expires_at > Date.now()) return value;
  if (raw !== null) localStorage.removeItem(KEY);
  return fresh(code);
}
function publish(snapshot, saved) {
  const value = {snapshot, saved};
  const encoded = JSON.stringify(value);
  if (encoded !== lastSent) {
    lastSent = encoded;
    send('streamlit:setComponentValue', {value, dataType:'json'});
  }
  statusElement.textContent = saved
    ? `Progress saved on this browser until ${new Date(snapshot.expires_at).toLocaleString('en-US', {timeZone:'America/New_York', timeZoneName:'short'})}. Visits do not extend this time. Your code stays until you delete it. Settings remain session-only.`
    : 'Progress and code are not being saved in this browser. They remain available in this open session. Browser storage may be blocked or full.';
  resize();
}
async function synchronize(clear = false) {
  if (!args) return;
  // Serialize read/merge/write across tabs. Chromium supports Web Locks.
  const update = () => {
    let snapshot, saved = true;
    try {
      if (clear) {
        localStorage.removeItem(KEY);
        localStorage.removeItem(CODE_KEY);
      }
      snapshot = read();
    }
    catch (_) { saved = false; snapshot = volatileSnapshot || (args.snapshot ? {...args.snapshot, history:[]} : fresh()); }
    if (snapshot.expires_at <= Date.now()) snapshot = fresh(snapshot.code);
    if (!clear && (!args.snapshot || args.snapshot.generation === snapshot.generation)) {
      const ids = new Set(snapshot.history.map(row => row._record_id));
      for (const row of args.history || []) {
        if (!ids.has(row._record_id)) { snapshot.history.push(row); ids.add(row._record_id); }
      }
    }
    try {
      const encoded = JSON.stringify(snapshot);
      if (localStorage.getItem(KEY) !== encoded) localStorage.setItem(KEY, encoded);
    }
    catch (_) { saved = false; }
    volatileSnapshot = snapshot;
    publish(snapshot, saved);
  };
  if (navigator.locks) await navigator.locks.request(KEY, update);
  else update();
}
function schedule(clear = false) {
  queue = queue.then(() => synchronize(clear)).catch(() => {
    statusElement.textContent = 'Browser saving is unavailable. This session still works.';
    resize();
  });
}
window.addEventListener('message', event => {
  if (event.source !== window.parent || event.data?.type !== 'streamlit:render') return;
  args = event.data.args;
  const theme = event.data.theme;
  if (theme?.textColor) document.body.style.setProperty('--text', theme.textColor);
  schedule();
});
window.addEventListener('storage', event => {
  if (event.key === KEY || event.key === CODE_KEY || event.key === null) schedule();
});
clearButton.addEventListener('click', () => {
  if (!confirmation) {
    confirmation = true;
    clearButton.textContent = 'Confirm: delete all saved answers, diagrams, stars and code';
    resize();
    return;
  }
  confirmation = false;
  clearButton.textContent = 'Delete saved progress and code';
  schedule(true);
});
send('streamlit:componentReady', {apiVersion:1});
resize();
