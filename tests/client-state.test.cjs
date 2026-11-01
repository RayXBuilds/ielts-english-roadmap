// State import is a data-loss boundary: reject malformed backups before replacing records.
const {test}=require('node:test');const assert=require('node:assert/strict');const vm=require('node:vm');const fs=require('node:fs');const path=require('node:path');
const root=path.resolve(__dirname,'..');
function harness(){
 const elements=new Map(),writes=[];
 const el=s=>{if(!elements.has(s))elements.set(s,{innerHTML:'',textContent:'',style:{},value:'',querySelectorAll:()=>[],focus(){},reset(){}});return elements.get(s);};
 const c=vm.createContext({window:{NATIVE_MODE:true,NATIVE_STATE:null,scrollTo(){},webkit:{messageHandlers:{app:{postMessage:m=>writes.push(m)}}}},document:{querySelector:el,querySelectorAll:()=>[]},setTimeout:()=>0,clearTimeout(){}});
 for(const f of ['data.js','app.js'])vm.runInContext(fs.readFileSync(path.join(root,'client',f),'utf8'),c);
 return {c,writes,run:s=>vm.runInContext(s,c)};
}
test('valid backup survives native save and reload, preserving multilingual notes',()=>{
 const h=harness();h.run("state.notes.r01='中文笔记 <tag>';state.days[3]=true;state.completed.r01=true;addWord('keep going','继续前进','r01');state.media.l01=12.5;save()");
 const raw=h.writes.at(-1).payload;h.c.raw=raw;h.run('window.restoreBackup(raw)');assert.equal(h.run('state.notes.r01'),'中文笔记 <tag>');assert.equal(h.run('state.days[3]'),true);assert.equal(h.run('state.media.l01'),12.5);assert.equal(h.run('state.words[0].term'),'keep going');
 assert.equal(h.run("esc('<script>')"),'&lt;script&gt;');
});
test('invalid backups never replace existing records or trigger a save',()=>{
 const h=harness();h.run("state.notes.r01='keep this'");const count=h.writes.length;
 for(const raw of ['{}','{bad','null','{"version":2,"words":[]}']){h.c.raw=raw;h.run('window.restoreBackup(raw)');assert.equal(h.run('state.notes.r01'),'keep this');}
 assert.equal(h.writes.length,count);
});
test('import filters unknown course IDs, invalid media times, and invalid days',()=>{
 const h=harness();assert.equal(h.run("const x=blank();x.completed.fake=true;x.days[85]=true;x.media.l01=-1;JSON.stringify(validate(x))"),h.run('JSON.stringify(blank())'));
 assert.throws(()=>h.run("const y=blank();y.words=[{term:42,meaning:'bad'}];validate(y)"));
});
test('corrupt startup storage pauses persistence until valid restore',()=>{
 const h=harness();h.run('window.STATE_ERROR=true;save()');assert.equal(h.writes.length,0);h.run('window.restoreBackup(JSON.stringify(blank()))');assert.equal(h.writes.length,1);assert.equal(h.run('window.STATE_ERROR'),false);
});
