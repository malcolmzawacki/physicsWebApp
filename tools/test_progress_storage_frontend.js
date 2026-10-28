// Exercise the actual browser storage script with refresh/tab/clock simulations.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const {webcrypto} = require('node:crypto');
const source = fs.readFileSync(path.join(__dirname, '../utils/progress_storage_frontend/storage.js'), 'utf8');
const KEY = 'physics-practice.progress.v1';
const CODE_KEY = 'physics-practice.code.v1';
const TTL = 86400000;
let now = 1792692000000;
const values = new Map();
let blocked = false, quota = false, writes = 0;
const storage = {
  getItem(key) { if (blocked) throw Error('blocked'); return values.get(key) ?? null; },
  setItem(key, value) { if (blocked || quota) throw Error('unavailable'); values.set(key, value); writes++; },
  removeItem(key) { if (blocked) throw Error('blocked'); values.delete(key); },
};
let lockQueue = Promise.resolve();
const locks = {request(_key, callback) { const task = lockQueue.then(callback); lockQueue = task.catch(()=>{}); return task; }};
function client() {
  const handlers = {}, messages = [];
  const button = {textContent:'', addEventListener:(_type, cb)=>{button.click=cb;}};
  const status = {textContent:''};
  const parent = {postMessage:message=>messages.push(JSON.parse(JSON.stringify(message)))};
  const window = {parent, addEventListener:(type, cb)=>{handlers[type]=cb;}};
  class Clock extends Date { constructor(...args) { super(...(args.length ? args : [now])); } static now() { return now; } }
  const context = vm.createContext({window, document:{getElementById:id=>id==='status' ? status : button,
    body:{scrollHeight:80, style:{setProperty(){}}}}, localStorage:storage,
    navigator:{locks}, crypto:webcrypto, Date:Clock, Uint8Array, console});
  vm.runInContext(source, context);
  const flush = async()=>{ await vm.runInContext('queue', context); };
  const event = ()=>messages.filter(message=>message.type==='streamlit:setComponentValue').at(-1)?.value;
  return {status, button, event, flush,
    render:async(snapshot=null, history=[], known_record_ids=undefined)=>{
      handlers.message({source:parent, data:{type:'streamlit:render', args:{snapshot, history, known_record_ids}}});
      await flush(); return event();
    },
    storageEvent:async()=>{ handlers.storage({key:KEY}); await flush(); return event(); },
  };
}
const row = id=>({_record_id:id, Activity:'Motion', Result:'Correct', Date:'2026-10-22',
  Question:'How far?', 'Your answer':'5', 'Correct answer':'5', Equations:[], Diagrams:{},
  Difficulty:'Easy', Explanation:''});
(async()=>{
  const first = client();
  let saved = (await first.render()).snapshot;
  assert.match(saved.code, /^\d{4}(-\d{4}){3}$/);
  assert.equal(values.get(CODE_KEY), saved.code, 'identity is stored separately without expiry');
  const expiry = saved.expires_at;
  saved = (await first.render(saved, [row('one')])).snapshot;
  assert.equal(saved.history.length, 1);
  const written = writes;
  const {history: ignored, ...metadata} = saved;
  await first.render(metadata, []);
  assert.equal(writes, written, 'idle polling does not rewrite unchanged history');
  const refreshed = client();
  assert.deepEqual((await refreshed.render()).snapshot, saved, 'refresh restores all fields');
  values.delete(CODE_KEY);
  assert.equal((await client().render()).snapshot.code, saved.code, 'migrate existing code without changing it');
  now += 3600000;
  saved = (await refreshed.render(saved, [row('one'), row('two')])).snapshot;
  assert.equal(saved.expires_at, expiry, 'visits and new work do not renew expiry');
  assert.equal(saved.history.length, 2);
  const other = client();
  await other.render();
  await Promise.all([first.render(saved, [row('three')]), other.render(saved, [row('four')])]);
  assert.equal(JSON.parse(values.get(KEY)).history.length, 4, 'concurrent tabs merge without overwriting');
  const stale = JSON.parse(values.get(KEY));
  other.button.click(); await other.flush();
  assert.equal(JSON.parse(values.get(KEY)).history.length, 4, 'clear requires confirmation');
  other.button.click(); await other.flush();
  const reset = other.event().snapshot;
  assert.notEqual(reset.code, saved.code);
  assert.equal(reset.history.length, 0);
  await first.render(stale, stale.history);
  assert.equal(JSON.parse(values.get(KEY)).history.length, 0, 'stale tab cannot resurrect cleared work');
  now = reset.expires_at;
  const expired = (await other.render(reset, [row('stale')])).snapshot;
  assert.equal(expired.history.length, 0);
  assert.notEqual(expired.generation, reset.generation);
  assert.equal(expired.expires_at, now + TTL);
  assert.equal(expired.code, reset.code, 'progress expiry preserves the code');
  now += 3 * TTL;
  const reopened = (await client().render()).snapshot;
  assert.equal(reopened.code, reset.code, 'code survives multiple expired windows and a fresh visit');
  assert.equal(reopened.history.length, 0);
  // Migration must also recover an expired code from the original single-key format.
  values.delete(CODE_KEY);
  values.set(KEY, JSON.stringify(expired));
  assert.equal((await client().render()).snapshot.code, reset.code);
  values.set(KEY, '{broken');
  const recovered = (await client().render()).snapshot;
  assert.equal(recovered.history.length, 0);
  assert.equal(recovered.code, reset.code, 'corrupt progress cannot erase the separate identity');
  blocked = true;
  const unavailable = client();
  let fallback = await unavailable.render(null, [row('unsaved')]);
  assert.equal(fallback.saved, false);
  assert.equal(fallback.snapshot.history.length, 1);
  assert.match(unavailable.status.textContent, /not being saved/);
  fallback = await unavailable.render(fallback.snapshot, [row('unsaved'), row('unsaved2')]);
  assert.equal(fallback.snapshot.history.length, 2, 'session still works without browser storage');
  blocked = false;
  const full = client();
  const current = (await full.render()).snapshot;
  quota = true;
  const failed = await full.render(current, [row('large')]);
  assert.equal(failed.saved, false);
  assert.equal(failed.snapshot.history.length, 1, 'quota failure does not silently discard current work');
  quota = false;
  values.clear();
  const incremental = client();
  let response = await incremental.render(null, [], []);
  assert.equal(response.delta, false, 'initial hydration stays complete');
  const meta = {...response.snapshot}; delete meta.history;
  const serverRows = [];
  let uploadBytes = 0, oldUploadBytes = 0;
  for (let i = 0; i < 30; i++) {
    const answer = {...row(`image-${i}`), Diagrams:{Forces:'data:image/png;base64,' + 'A'.repeat(40000)}};
    serverRows.push(answer);
    response = await incremental.render(meta, [answer], serverRows.map(r => r._record_id));
    assert.equal(response.delta, true);
    assert.equal(response.snapshot.history.length, 0, 'do not echo diagrams the server already owns');
    assert.equal(response.record_ids.length, serverRows.length, 'acknowledge every saved record');
    uploadBytes += JSON.stringify(response).length;
    oldUploadBytes += JSON.stringify({snapshot:{...meta, history:serverRows}, saved:true}).length;
  }
  assert.equal(JSON.parse(values.get(KEY)).history.length, 30, 'all diagrams remain in browser storage');
  assert.ok(uploadBytes < oldUploadBytes / 100, 'incremental saves remove over 99% of this repeated upload payload');
  const restored = client();
  const hydration = await restored.render(null, [], []);
  assert.equal(hydration.snapshot.history.length, 30, 'refresh restores complete answers and images');
  assert.equal(hydration.delta, false);
  await restored.render(meta, [], serverRows.map(r => r._record_id));
  const extra = row('from-other-tab'); serverRows.push(extra);
  await incremental.render(meta, [extra], serverRows.map(r => r._record_id));
  await restored.storageEvent();
  assert.deepEqual(restored.event().snapshot.history.map(r => r._record_id), ['from-other-tab'], 'cross-tab updates upload only missing records');
  assert.equal(restored.event().record_ids.length, 31);
  assert.equal(restored.event().delta, true);
  quota = true;
  const quotaAnswer = row('quota-pending'); serverRows.push(quotaAnswer);
  let pending = await incremental.render(meta, [quotaAnswer], serverRows.map(r => r._record_id));
  assert.equal(pending.saved, false);
  assert.equal(pending.delta, true);
  assert.equal(pending.record_ids.length, 32, 'failed save keeps the pending answer in the open session');
  assert.equal(JSON.parse(values.get(KEY)).history.length, 31);
  quota = false;
  pending = await incremental.render(meta, [quotaAnswer], serverRows.map(r => r._record_id));
  assert.equal(pending.saved, true);
  assert.equal(JSON.parse(values.get(KEY)).history.length, 32, 'retry saves pending work without duplicates');
  blocked = true;
  const blockedAnswer = row('blocked-pending'); serverRows.push(blockedAnswer);
  pending = await incremental.render(meta, [blockedAnswer], serverRows.map(r => r._record_id));
  assert.equal(pending.saved, false);
  assert.equal(pending.record_ids.length, 33);
  blocked = false;
  pending = await incremental.render(meta, [blockedAnswer], serverRows.map(r => r._record_id));
  assert.equal(pending.saved, true);
  assert.equal(JSON.parse(values.get(KEY)).history.length, 33);
  restored.button.click(); restored.button.click(); await restored.flush();
  assert.equal(restored.event().delta, false, 'deletion/reset sends a new full generation');
  assert.equal(restored.event().snapshot.history.length, 0);
  const typed = client();
  const initialTyped = (await typed.render()).snapshot;
  await typed.render(initialTyped, [row('legacy'), {...row('typed'), 'Problem type':'Type 2'}]);
  const typedHydration = (await client().render()).snapshot;
  assert.equal(typedHydration.history[0]['Problem type'], undefined, 'legacy records stay compatible');
  assert.equal(typedHydration.history[1]['Problem type'], 'Type 2', 'problem type survives refresh');
  const invalidTyped = {...typedHydration, history:[{...row('invalid-type'), 'Problem type':42}]};
  values.set(KEY, JSON.stringify(invalidTyped));
  assert.equal((await client().render()).snapshot.history.length, 0, 'reject a malformed optional problem type');
  console.log(`Incremental saves: ${uploadBytes} bytes versus ${oldUploadBytes} previous full-history bytes for 30 synthetic image answers.`);
  console.log('Browser persistence: refresh, fixed expiry, merging, clear, corrupt data, blocked storage and quota checks passed.');
})().catch(error=>{console.error(error); process.exitCode=1;});
