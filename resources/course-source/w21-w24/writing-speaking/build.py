from pathlib import Path
import json,re,hashlib
from content import items
from speaking import weeks
from figures import generate
from transfer import transfer_for
ROOT=Path(__file__).resolve().parent
for w in range(21,25): (ROOT/f'W{w:02d}').mkdir(exist_ok=True)
generate()
def wc(s): return len(re.findall(r"[A-Za-z0-9]+(?:[’'-][A-Za-z0-9]+)*",s))
def write(p,s):
    target=ROOT/p; content=s.strip()+'\n'
    if not target.exists() or target.read_text()!=content: target.write_text(content)
common='''## 使用与记录

原创教学练习，非真题、非标准化模拟，难度未校准。先完成本页再打开参考页。人物、机构、经历与数据均为教学虚构。范例的身份、地点、动作和细节不是强制要求。口语优先用真实经历或真实观察，并说明来源；没有相关经历时，可将假设回答明确标为技能练习，不伪装成亲历。不要背诵示例。自评和 AI 反馈不能代替独立真人评分，未获得真人评阅时标记“分数未确认”。

保存：任务ID、实际日期、用时、初稿或原始录音、证据化反馈、重写/重答、三条修改理由。没有学生提交物，不得填写“已批改”或“已完成训练”。
'''
inv=[]
for x in items:
 w=x['week']; kind=x['kind']; id=f'WS-W{w:02d}-{kind}'; base=f'W{w:02d}/{kind.lower()}'
 is2=kind=='T2'; minimum=250 if is2 else 150
 # Counts conservatively exclude letter greeting and sign-off.
 model=x['model']; body=model
 if kind=='T1G': body='\n\n'.join(model.split('\n\n')[1:-1])
 n=wc(body)
 assert n>=minimum,(id,n)
 budget=105 if is2 else 75
 prompt=x['prompt']+f'\n\nWrite at least {minimum} words. '+('You do not need to write any addresses. ' if kind=='T1G' else '')+f'Spend about {40 if is2 else 20} minutes on this task.'
 student=f'''# {id} 学生页：{x['title']}

周次 W{w:02d}｜题型 {kind}｜能力点：{'观点展开与任务回应' if is2 else ({21:'趋势、限时与漏项检查',22:'流程条件与阶段记录',23:'地图变化与反馈核验',24:'比例、总量与证据边界'}[w] if kind=='T1A' else '书信目的、要点与语气')}\n\n{'Task 1 的 A/G 分支二选一，另一分支不计入本周作业。' if not is2 else 'A/G 共用本题。'}

{common}
## 完整题干

{prompt}

{x['data']}

## 任务预算（含首次审题，不额外加时）

{'初稿40分钟（审题规划5、写作30、检查5）；诊断15；反馈阅读与证据核查10；完整重写35；对照归档5。合计105分钟。' if is2 else '初稿20分钟（审题规划3、写作15、检查2）；诊断15；反馈阅读与证据核查10；完整重写25；对照归档5。合计75分钟。'}

## 初稿后自评清单

- [ ] 达到最低字数；全文连贯成段，没有用项目符号代替作文。
- [ ] {'直接回答题目的所有问句，有始终一致的立场。' if is2 else ('概述给主要特征；数据、阶段或方位都与题图逐项相符，不推断未提供的原因。' if kind=='T1A' else '三个要点均展开；称呼、目的、语气和结束语适合收信人。')}
- [ ] 每段可写出一个功能标签；例子或数据与该段要点相连。
- [ ] 核查两处词汇搭配和两处句法；如有疑点先试改再核实，无问题则记录通过证据。
- [ ] 如有影响理解的问题，记录原句；否则记通过或待核查，不填写自猜分数。

## 反馈与重写

打开 [独立参考页]({kind.lower()}-reference.md)，按逐段检查和通用协议核验。重写任务：{x['rewrite']}
'''
 ref=f'''# {id} 独立参考页

只在初稿完成后阅读；不是唯一答案，也没有官方分数。以下是对原创示例的教学讲评，不是对学生尚未提交作文的已完成批改。

## 思路拆解

{x['plan']}

## 原创示例

<!-- MODEL_START -->
{model}
<!-- MODEL_END -->

示例正文词数：{n}（本项目正则计数；书信不含称呼、结束语与署名；连字符词作一词）。

## 逐段反馈与迁移

以下只分析上方原创示例。题干要点及图表事实必须遵守；书信、议论文的自拟身份、日期、经历和例子不是新增强制要求。按自己的合理设定核验，不为对齐范例编造经历。

'''+ '\n\n'.join('- '+f for f in x['feedback'])+f'''

## 常见失误

{x['errors']}

## 可执行反馈步骤

1. 先把自己的段落标为引入、概述/论点、支持、收束；分段可不同于示例，按功能核查，不照抄段数。
2. 对照上方逐段检查，逐项标“已有证据/缺失/不适用”。每条意见必须附自己的原句或缺失位置。
3. 按 [反馈协议](../FEEDBACK.md) 的四维表记录；有争议的 AI 意见回题干、数据或语法依据核验。
4. 只选至多两项有证据的优先点执行整篇重写；如未发现问题，可改变组织或表达练迁移，但不把它标成纠错；保留原稿，禁止把示例替换为自己的作业。

## 重写任务

{x['rewrite']}

完成后重新勾选 [学生页]({kind.lower()}-student.md) 清单；将一处改前/改后及理由交给独立评阅者核查。真人评阅状态目前为“待安排”，不是已完成。
'''
 student+='\n## 本周重点操作（已含原预算）\n\n'+transfer_for(w,kind)+'\n\n记录表见[阶段证据与交接表](../EVIDENCE.md)，只在上述原时段填写相关行。\n'
 write(base+'-student.md',student);write(base+'-reference.md',ref)
 inv.append(dict(id=id,week=f'W{w:02d}',type=kind,student_path=base+'-student.md',reference_path=base+'-reference.md',model_word_count=n,question_count=1,duration_minutes=budget,source='Original teaching material; fictional data and scenarios',license='CC BY 4.0; Copyright © 2026 RayXBuilds and contributors; original teaching text, prompts, data and examples only; https://creativecommons.org/licenses/by/4.0/',validation_status='self_checked_pending_independent_QA',skills=x['plan'],branch_group=f'W{w:02d}-Task1' if not is2 else None))
 write('STATUS.md',f'# 写作口语制作状态\n\n最近完成：{id}。写作题已生成 {len(inv)} 道；正在制作本批，其余未声明完成。独立验收待进行。')
for s in weeks:
 w=s['w']
 for k in [1,2,3]:
  id=f'WS-W{w:02d}-S{k}';base=f'W{w:02d}/s{k}';mins=60 if k==3 else 30
  if k==1:
   questions='## Part 1专项题\n\n'+'\n'.join(f'{i+1}. {q}' for i,q in enumerate(s['p1']))+'\n\n追问：\n\n'+'\n'.join('- '+q for q in s['p1follow'])
   questions+='\n\n首答6分钟内依次答4个主问，每题约40～60秒；两条追问只选1条答约30～45秒，其余时间用于转题。备用追问留给重答，不要求全部说完。'
   models=[s['short']]; labels=['直接回应→原因→具体情境的展开示例']
   budget='设备与审题3分钟；首答录音6；回听及局部转写7；示例和诊断5；不看稿重答6；归档3。共30分钟。'
   rewrite='如有笼统判断，选择至多两个答案补具体情境；如没有，选择两题换角度重答并保留切题证据；重答一条追问，检查是否真正回应其新角度。'
   count=6
  elif k==2:
   questions='## Part 2专项任务卡\n\n'+s['card']+'\n\n准备1分钟，说1～2分钟。只记5个关键词，不预写句子。\n\n收尾追问：\n\n'+'\n'.join('- '+q for q in s['round'])
   questions+='\n\n每轮5分钟包含准备1分钟、连续说1～2分钟、两条收尾追问选1条答20～30秒及转题缓冲；另一条可用于重答。不把备用题全部加进本轮。'
   models=[s['long']]; labels=['原创长答示例（时长须以个人实际录音测量）']
   budget='准备、首答录音及追问5分钟；回听及局部转写8；示例与诊断5；关键词重组3；重答及追问5；归档4。共30分钟。'
   rewrite='用五个关键词重答完整任务卡1～2分钟，再从两条追问中选1条答20～30秒；如缺具体细节则补、如有无关背景则删；若已清楚，换表达但保持事实。比较首答与重答，不背示例。'
   count=3
  else:
   questions='''## 连续三部分全流程（首答不可看参考）

找同伴读题，或独练逐题揭示。完整首答11～14分钟，中途不暂停纠错。模拟同伴不是认证考官；自行读题的练习记录不能冒充真实面试。

### Part 1：4～5分钟

'''+ '\n'.join(f'{i+1}. {q}' for i,q in enumerate(s['fullp1']))+'''

可按回答追加 Why? / Can you give an example? 到时转下部分，不强行说完全部备用问题。

### Part 2：3～4分钟（含准备）

'''+s['fullcard']+'\n\n准备1分钟，连续说1～2分钟。收尾追问：\n\n'+'\n'.join('- '+q for q in s['fullround'])+'''\n\n### Part 3：4～5分钟

'''+ '\n'.join(f'{i+1}. {q}' for i,q in enumerate(s['p3']))+'\n\n根据回答追加追问：\n\n'+'\n'.join('- '+q for q in s['deepfollow'])
   questions+='\n\nPart 2收尾追问两条选1条，答20～30秒，含在3～4分钟内。Part 3从4个主问中选3个，每个约60～75秒，再从2条追问中选1条答30～45秒；连同读题控制在4～5分钟，到时结束。题库数量不是必答数量。'
   models=[s['fulllong'],s['deep']];labels=['Part 2原创展开示例（个人语速不同，不能以词数推录音时长）','Part 3观点→理由→条件展开示例']
   budget='D5：设备与流程准备2分钟，连续首答11～14分钟，余14～17分钟完整回听标记，共30分钟。D6：局部转写诊断10，阅读示例与调整5，重答与新追问10，对照归档5，共30分钟。合计60分钟。'
   rewrite='在10分钟重答时段：选择一个有核查需要的Part 1主问答约1分钟；Part 2准备1分钟、答1～2分钟，再选一条收尾追问答20～30秒；Part 3只选一个主问答约1分钟，再选一条未用追问答30～45秒。余时用于换题和回听；无薄弱项则选已通过题换角度练迁移，保持真实细节，不复述范例。局部重答不另计全流程。'
   count=15
  student=f'''# {id} 学生页

周次W{w:02d}｜{'三部分全流程' if k==3 else 'Part '+str(k)+'专项'}｜能力点：{s['focus']}｜{mins}分钟

{common}
## 操作与预算

{budget}

{questions}

## 录音回听清单

- [ ] 保留首答原音，记录实际时长、是否中断、是否看稿；只报真实完成状态；短于目标时长如实记，不用沉默或无关内容凑时。
- [ ] 流利与连贯：标出两处时间戳，区分构思停顿与重复搜词，检查是否偏离问句。
- [ ] 词汇：如有模糊词或无效重复，引用一处并先解释原意再试改；无则记录清楚的表达，不为难词改变意思。
- [ ] 语法：核对经历与习惯的时态；局部转写核查；如存在妨碍理解的问题才更正，无则记通过。
- [ ] 发音：不看转写听30秒，如有听不清的词尾、重音或断句则标时间戳，无则记录清楚证据；没有音频不能判断发音。
- [ ] 展开：主要回答有具体情境或理由；追问后第一句回应追问的新角度。

## 重答要求

{rewrite}

首答回听后才打开[独立参考页](s{k}-reference.md)。按[反馈协议](../FEEDBACK.md)填至少三个时间戳，不以文字转写替代音频评阅。
'''
  ref=f'''# {id} 独立参考页

原创教学示例，非真题或评分结果。未收到学生音频；以下是示例分析与待执行反馈，不能登记为已完成学生批改。

## 展开示例

'''
  for label,model in zip(labels,models):ref+=f'### {label}\n\n<!-- MODEL_START -->\n{model}\n<!-- MODEL_END -->\n\n'
  n=sum(wc(m) for m in models)
  ref+=f'''纯口答示例词数：{n}；只计MODEL标记内实际英文口答，不含标题、标签、说明。词数不能证明录音时长或流利度。

## 展开与反馈

本周能力：{s['focus']}。

1. {'示例先表态，再说明偏好理由，最后提供条件或场景。检查自己是否用一个词回答后就结束。' if k==1 else '长答示例按背景、行动/观察、变化与意义组织。每段都推进内容；检查自己是否只有背景而没有具体事件。'}
2. 找到一个具体细节：物品、动作、对话或地点。用真实经历或注明来源的真实观察替换；假设回答须标为技能练习。保持切题，不强制复制范例细节，不照搬身份与经历。
3. {'Part 3示例不把个人选择强加给所有人；先讲机制，再说明条件或例外。检查自己的追问答案是否直接回应新问题。' if k==3 else '追问要重新回应，不能继续背长答。首句先回答追问，再用一条理由支持。'}
4. 如存在听不清或语法影响理解处，标原音时间戳；否则标一处清楚的原音证据；先尝试最小修正。不要把自然停顿一概当成错误，或用加快语速掩盖逻辑断裂。

## 常见失误

空泛形容词替代具体过程；给了经历却没解释为什么重要；Part 3只有个人故事没有一般解释；AI只看转写就判断发音。逐项回原音核对，不能凭范例推断自己已达到某个分数。

## 可执行重答与反馈

{rewrite}

填写[反馈协议](../FEEDBACK.md)四维表，附三个时间戳和原话证据。如存在，选至多一个内容问题与一个语言问题先修；否则记录清楚的证据并做迁移重答；重答后并排听两段，记录改善与仍未解决之处。自评与AI不能替代独立真人评分；独立评阅目前待安排，分数未确认。
'''
  student+='\n## 本周重点操作（已含原预算）\n\n'+transfer_for(w,f'S{k}')+'\n\n记录表见[阶段证据与交接表](../EVIDENCE.md)，只在上述原时段填写相关行。\n'
  write(base+'-student.md',student);write(base+'-reference.md',ref)
  inv.append(dict(id=id,week=f'W{w:02d}',type='Speaking-full' if k==3 else f'Speaking-P{k}',student_path=base+'-student.md',reference_path=base+'-reference.md',model_word_count=n,question_count=count,question_count_note='Available bank count, not mandatory spoken count. Main questions, one cue card and explicit follow-ups counted; generic probes and cue bullets excluded. Follow selection and time caps appear on each student page.',duration_minutes=mins,recording_target_minutes=[11,14] if k==3 else None,source='Original fictional teaching prompts and examples; not official test material',license='CC BY 4.0; Copyright © 2026 RayXBuilds and contributors; https://creativecommons.org/licenses/by/4.0/',validation_status='self_checked_pending_independent_QA',skills=s['focus']))
  write('STATUS.md',f'# W21～24制作状态\n\n最新完成{id}；共{len(inv)}课项。待批次自检与冻结，不代表学生已完成任务。')
for e in inv:
 for key in ['student_path','reference_path']:
  e[key.replace('_path','_sha256')]=hashlib.sha256((ROOT/e[key]).read_bytes()).hexdigest()
 e['word_count_method']='English alphanumeric tokens, internal apostrophes/hyphens treated as one; writing letters exclude greeting/closing; speaking counts actual model utterances only, no labels/instructions; not duration'
 if e['type']=='T1A':
  e['figure_path']=f"{e['week']}/assets/figure.svg";e['figure_sha256']=hashlib.sha256((ROOT/e['figure_path']).read_bytes()).hexdigest()
write('inventory.json',json.dumps(dict(batch='W21-W24',path_base='writing-speaking/batches/W21-W24/',status='self_checked_pending_independent_QA',writing_prompt_count=12,writing_selected_first_drafts=8,writing_selected_rewrites=8,speaking_tasks=12,full_speaking_tasks=4,weekly_minutes={'writing':180,'speaking':120},items=inv),ensure_ascii=False,indent=2))
print(json.dumps({e['id']:e['model_word_count'] for e in inv},ensure_ascii=False,indent=2))

write('manifest.json',json.dumps(dict(batch='W21-W24',inventory='inventory.json',inventory_sha256=hashlib.sha256((ROOT/'inventory.json').read_bytes()).hexdigest(),lesson_items=24,student_reference_pages=48,figures=4,source_files=['content.py','speaking.py','figures.py','transfer.py','build.py'],status='pending_independent_QA',license='CC BY 4.0; RayXBuilds and contributors'),ensure_ascii=False,indent=2))
