// State import is a data-loss boundary: reject malformed backups before replacing records.
const {test}=require('node:test');const assert=require('node:assert/strict');const vm=require('node:vm');const fs=require('node:fs');const path=require('node:path');
const root=path.resolve(__dirname,'..');
const {TextEncoder}=require('node:util');
function harness(){
 const elements=new Map(),writes=[];
 const el=s=>{if(!elements.has(s))elements.set(s,{innerHTML:'',textContent:'',style:{},value:'',querySelectorAll:()=>[],focus(){},reset(){}});return elements.get(s);};
 const c=vm.createContext({TextEncoder,navigate(){},toast(){},window:{NATIVE_MODE:true,NATIVE_STATE:null,scrollTo(){},webkit:{messageHandlers:{app:{postMessage:m=>writes.push(m)}}}},document:{querySelector:el,querySelectorAll:()=>[]},setTimeout:()=>0,clearTimeout(){}});
 for(const f of ['data.js','state.js'])vm.runInContext(fs.readFileSync(path.join(root,'client',f),'utf8'),c);
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

test('0.1 backup migrates without losing progress, words, notes or audio',()=>{
 const h=harness();h.c.old={version:1,completed:{r01:true},days:{1:true},notes:{r01:'旧版笔记'},words:[{term:'habit',meaning:'习惯',source:'r01',reviewed:true}],last:'l01',media:{l01:9.5}};
 h.run('window.restoreBackup(JSON.stringify(old))');
 assert.equal(h.run('state.preferences.fontSize'),18);assert.equal(h.run('state.notes.r01'),'旧版笔记');assert.equal(h.run('state.completed.r01'),true);assert.equal(h.run('state.words[0].reviewed'),true);assert.equal(h.run('state.media.l01'),9.5);
});
test('font preferences round trip and invalid values fall back',()=>{
 const h=harness();assert.equal(h.run('const p=blank();p.preferences.fontSize=21;validate(p).preferences.fontSize'),21);
 assert.equal(h.run('p.preferences.fontSize=999;validate(p).preferences.fontSize'),18);
});
test('pausing an old player cannot overwrite imported playback positions',()=>{
 const h=harness();h.c.document.querySelectorAll=()=>[{pause(){h.run('state.media.l01=28')}}];
 h.run('const imported=blank();imported.media.l01=7;window.restoreBackup(JSON.stringify(imported))');assert.equal(h.run('state.media.l01'),7);
});
test('duplicate terms and oversized records do not write invalid state',()=>{
 const h=harness();h.run("addWord('Hello','你好','r01')");let n=h.writes.length;
 assert.equal(h.run("addWord('HELLO','你好','r01')"),false);assert.equal(h.writes.length,n);
 assert.equal(h.run("addWord('x'.repeat(201),'example','r01')"),false);
 h.run("state.notes.r01='x'.repeat(11*1024*1024)");assert.equal(h.run('save()'),false);assert.equal(h.writes.length,n);
});

test('leaving a player twice cannot overwrite a restored position or invoke stale handlers',()=>{
 const h=harness(), source=fs.readFileSync(path.join(root,'client/app.js'),'utf8');
 h.run(source.slice(source.indexOf('function stopMedia()'),source.indexOf('function navigate(next)')));
 const media={dataset:{lesson:'l01'},currentTime:26,onpause(){throw Error('stale handler')},pause(){if(this.onpause)this.onpause();}};
 h.c.document.querySelectorAll=()=>[media];
 h.run('stopMedia();state.media.l01=7;stopMedia()');assert.equal(h.run('state.media.l01'),7);assert.equal(media.onpause,null);
});
