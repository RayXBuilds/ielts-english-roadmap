const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');

function harness() {
  const calls = [];
  let failure = '';
  const element = {textContent:'', hidden:true};
  const bridge = {
    save(raw, restoring) { calls.push({raw, restoring}); return failure; },
    exportBackup(raw) { calls.push({export:raw}); },
    importBackup() { calls.push({import:true}); },
  };
  const context = vm.createContext({TextEncoder, window:{ANDROID_MODE:true, NATIVE_MODE:true, NATIVE_STATE:null, StepwiseAndroid:bridge},
    document:{querySelector:()=>element, querySelectorAll:()=>[]}, toast(){}, navigate(){}});
  for (const file of ['data.js', 'state.js']) {
    vm.runInContext(fs.readFileSync(path.join(__dirname,'../client',file),'utf8'), context);
  }
  return {calls, fail(message){failure=message;}, run(source){return vm.runInContext(source,context);}};
}

test('Android saves through native storage and reports disk failures', () => {
  const h = harness();
  assert.equal(h.run('save()'), true);
  assert.equal(h.calls.at(-1).restoring, false);
  h.fail('disk full');
  assert.equal(h.run('save()'), false);
});

test('Android restoration persists before replacing current notes', () => {
  const h = harness();
  h.run("state.notes.r01='keep';const replacement=blank();replacement.notes.r01='imported'");
  h.fail('disk full');
  h.run('window.restoreBackup(JSON.stringify(replacement))');
  assert.equal(h.run('state.notes.r01'), 'keep');
  h.fail('');
  h.run('window.restoreBackup(JSON.stringify(replacement))');
  assert.equal(h.run('state.notes.r01'), 'imported');
  assert.equal(h.calls.at(-1).restoring, true);
});

test('Android rejects malformed restores and routes file operations to the system picker', () => {
  const h = harness();
  h.run("window.restoreBackup('{}')");
  assert.equal(h.calls.length, 0);
  h.run("native('export','{}');native('import',null)");
  assert.deepEqual(h.calls, [{export:'{}'}, {import:true}]);
});
