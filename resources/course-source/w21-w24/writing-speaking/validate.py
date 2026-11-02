from pathlib import Path
import re,json,hashlib,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent
D=json.loads((R/'inventory.json').read_text()); errors=[]
def ck(ok,msg):
 if not ok:errors.append(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wc(s):return len(re.findall(r"[A-Za-z0-9]+(?:[’'-][A-Za-z0-9]+)*",s))
ck(len(D['items'])==24,'24课项')
ck(len({e['id'] for e in D['items']})==24,'ID唯一')
ck(len(list(R.glob('W*/*-student.md')))==24,'24学生页')
ck(len(list(R.glob('W*/*-reference.md')))==24,'24参考页')
ck(len(list(R.glob('W*/assets/*.svg')))==4,'4 SVG')
allmodels={}
for e in D['items']:
 for field in ['student','reference']:
  p=R/e[field+'_path'];ck(p.is_file(),str(p));ck(sha(p)==e[field+'_sha256'],'哈希:'+e['id']+field)
 student=(R/e['student_path']).read_text();ref=(R/e['reference_path']).read_text()
 models=re.findall(r'<!-- MODEL_START -->\s*(.*?)\s*<!-- MODEL_END -->',ref,re.S);allmodels[e['id']]=models
 ck('MODEL_START' not in student,'学生页混入示例')
 counted=['\n\n'.join(models[0].split('\n\n')[1:-1])] if e['type']=='T1G' else models
 n=sum(wc(s) for s in counted);ck(n==e['model_word_count'],'词数:'+e['id'])
 if e['type'].startswith('T'):
  ck(len(models)==1,'写作示例数')
  ck(n>=(250 if e['type']=='T2' else 150),'最低词数:'+e['id'])
  for marker in ['思路拆解','逐段反馈','常见失误','重写任务','不是新增强制要求']:ck(marker in ref,'缺'+marker+e['id'])
 else:
  for marker in ['追问','录音回听清单','重答要求','无则']:ck(marker in student,'缺'+marker+e['id'])
  ck('范例的身份、地点、动作和细节不是强制要求' in student,'范例边界')
  ck(not any(m.startswith('Part ') for m in models),'口答计入标签')
  if e['type']=='Speaking-P1':ck('两条追问只选1条' in student,'S1选择')
  if e['type']=='Speaking-P2':ck('选1条答20～30秒' in student,'S2选择及时间')
 if e['type']=='Speaking-full':
  ck(len(models)==2,'S3两段示例')
  ck(all(f'### Part {i}' in student for i in [1,2,3]),'完整三部分')
  ck('Part 3只选一个主问' in student and '30～45秒' in student,'S3重答数量时间')
  ck('Part 3从4个主问中选3个' in student,'S3首答题数')
 if 'figure_path' in e:
  p=R/e['figure_path'];ET.parse(p);ck(sha(p)==e['figure_sha256'],'SVG哈希')
  png=R/'qa-renders'/e['week']/'figure.svg.png';ck(png.is_file() and png.read_bytes()[:8]==b'\x89PNG\r\n\x1a\n','逐图渲染存在')
 ck('CC BY 4.0' in e['license'],'许可')
 ck('## 本周重点操作（已含原预算）' in student and '3分钟' in student,'周重点及内含预算:'+e['id'])
 ck('问题存在才改' in student or any(s in student for s in ['如有问题','有证据问题','如存在','如有疑点']),'非预设问题:'+e['id'])
for w in ['W21','W22','W23','W24']:
 a=[e for e in D['items'] if e['week']==w];ck(len(a)==6,w+'数量')
 for branch in ['T1A','T1G']:ck(sum(e['duration_minutes'] for e in a if e['type'] in [branch,'T2'])==180,w+'写作预算')
 ck(sum(e['duration_minutes'] for e in a if e['type'].startswith('Speaking'))==120,w+'口语预算')
 ck(sum(e['type']=='Speaking-full' for e in a)==1,w+'全流程数')
ck(sum(e['type'].startswith('T') for e in D['items'])==12,'写作题数')
ck(sum(e['type'].startswith('Speaking') for e in D['items'])==12,'口语课数')
for p in R.rglob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' not in target and not target.startswith('#'):
   # The final freeze check must resolve these generated manifests too.
   ck(target in ['FREEZE.json','SHA256SUMS','validation-result.json'] or (p.parent/target.split('#')[0]).exists(),'链接:'+str(p)+':'+target)
prior=json.loads((R/'prior-batch-hashes.json').read_text());base=R.parent.parent
for name,h in prior.items():ck((base/name).is_file() and sha(base/name)==h,'前批变更:'+name)
# Check independently calculated values against published labels and model claims.
svg21=(R/'W21/assets/figure.svg').read_text()
for n in [100,140,150,170,240,300,330,360,390]:ck('>'+str(n)+'</text>' in svg21,'W21图中值'+str(n))
start=[300,150,100];end=[300,390,170]
ck(sum(start)==550 and sum(end)==860 and 330-300==30 and 390-300==90,'W21合计和差值')
ck(all(t in allmodels['WS-W21-T1A'][0] for t in ['860','550','thirty','ninety','unchanged at 140']),'W21模型主比较')
flow=' '.join(allmodels['WS-W22-T1A'])
ck(not re.search(r'\b(daily|weekly|monthly|washed|cleaned|sold)\b',flow,re.I),'W22图外频次/步骤')
for t in ['repair','checked again','fail','recycling','ineligible','storage']:ck(t in flow,'W22分支模型:'+t)
shares=[[70,20,10],[40,35,25]];totals=[2000,4000]
quantities=[[v*t//100 for v in row] for row,t in zip(shares,totals)]
ck(all(sum(r)==100 for r in shares) and quantities==[[1400,400,200],[1600,1400,1000]],'W24份额与数量')
ck(quantities[1][0]>quantities[0][0] and 1000/200==5 and 70-20==50 and 40-35==5 and 25-10==15,'W24对比')
svg24=(R/'W24/assets/figure.svg').read_text()
for n in [70,20,10,40,35,25]:ck('>'+str(n)+'%</text>' in svg24,'W24图中比例')
for v in ['2,000','4,000']:ck(v in svg24,'W24总数表')
manifest=json.loads((R/'manifest.json').read_text());ck(manifest['inventory_sha256']==sha(R/'inventory.json'),'manifest清单哈希')
for f in manifest['source_files']:ck((R/f).is_file(),'源:'+f)
evidence=(R/'EVIDENCE.md').read_text()
for term in ['正式T22登记','T24卷源','目标总分','听力最低要求','阅读最低要求','写作最低要求','口语最低要求','第一轮','第二轮','4～8周','最近两次未见整卷','未定','未完成/未确认']:ck(term in evidence,'证据表:'+term)
result={'status':'PASS' if not errors else 'FAIL','errors':errors,'lesson_items':24,'student_pages':24,'reference_pages':24,'svg_figures':4,'writing_selected_first_drafts':8,'writing_selected_whole_rewrites':8,'speaking_tasks':12,'full_speaking_tasks':4,'weekly_minutes':{'writing':180,'speaking':120},'model_words':{e['id']:e['model_word_count'] for e in D['items']},'writing_model_words_total':sum(e['model_word_count'] for e in D['items'] if e['type'].startswith('T')),'prior_batch_files_verified':len(prior),'limits':'Structural, arithmetic and hash checks; visual review separately in SELF-CHECK. Learner timing, real T22/T24, actual exam-interface practice, human feedback and independent QA remain unconfirmed.'}
(R/'validation-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
