from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
assert json.loads((R/'validation-result.json').read_text())['status']=='PASS'
files=sorted(p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ['FREEZE.json','SHA256SUMS'])
hashes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
manifest={'batch':'W21-W24','status':'frozen_pending_independent_QA','timezone':'Asia/Shanghai','frozen_date':'2026-11-03','license':'CC BY 4.0; RayXBuilds and contributors','files':hashes,'exclusions':['__pycache__ (derived Python cache)','FREEZE.json and SHA256SUMS (manifest recursion)'],'note':'SHA256SUMS also hashes FREEZE.json; no learner scores or completed grading claimed.'}
(R/'FREEZE.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
hashes['FREEZE.json']=hashlib.sha256((R/'FREEZE.json').read_bytes()).hexdigest()
(R/'SHA256SUMS').write_text(''.join(h+'  '+p+'\n' for p,h in sorted(hashes.items())))
for p,h in hashes.items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
print('Frozen and verified',len(hashes),'files')
