"""Compile accepted W21–24 text into weekly readers without changing source text."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'resources/course-source/w21-w24'
for row in json.loads((SRC/'manifest.json').read_text())['source_files']:
 assert hashlib.sha256((SRC/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
def body(p):
 s=p.read_text()
 if p.name=='SOURCES.md':s=s.split('## 原始源文件与复现')[0]
 s=re.sub(r'<!--.*?-->','',s,flags=re.S)
 # Reader cannot open arbitrary Markdown; references are in the same unit or U35.
 def link(m):
  is_image,label,url=m.groups()
  if url.startswith(('https://','http://')):return m[0]
  if is_image:
   target=(p.parent/url).resolve();rel=target.relative_to(ROOT);assert target.is_file()
   return f'![{label}](../../{rel})'
  if 'SOURCES.md' in url:return '[来源与待核验界面入口](u35-feedback.md)'
  if 'EVIDENCE.md' in url:return '[阶段证据表](u35-feedback.md)'
  if 'FEEDBACK.md' in url:return '[反馈协议](u35-feedback.md)'
  if url.endswith('-student.md'):return label+'（见本节上方学生题）'
  return label+'（本节下方展开参考）'
 s=re.sub(r'(!?)\[([^\]]+)\]\(([^)]+)\)',link,s)
 for name,label in [('EXAM-INTERFACE.md','真实考试界面登记'),('FORMAL-ASSESSMENT.md','正式T22/T24登记'),('LEARNING-RECORD.md','学习记录与目标')]:
  s=s.replace(name,label+'（见U35对应表格）')
 return re.sub(r'^(#+) ',lambda m:'#'*(len(m[1])+2)+' ',s,flags=re.M).strip()
for w in range(21,25):
 week=f'W{w:02}';uid=f'u{w+10:02}'
 out=[f'# {uid.upper()} 第{w}周：长篇阅读、写作与口语',
 '本页为已独立核验的原创文字课程。先完成学生题目，再展开对应参考。非真题、非标准化模考，不换算雅思分数。听力尚未补齐，本页不代表全科课程已完成。',
 '每周选A或G类Task 1一题，加Task 2及三次口语。参考范文不是学生已完成作业，仍须提交初稿、录音和重写，独立真人评分另行安排。',
 '阅读每周180分钟（60分钟首次限时、120分钟证据精读与延迟复测），写作180分钟、口语120分钟。词汇60分钟、听力180分钟另列；新增完整听力未验收，不能勾整周完成。',
 'W22/W24原创阶段检查按实际证据复盘；正式T22/T24陌生整卷、所选真实考试界面操作及真人评分另记，缺少目标或真实证据时不能据此判断报考/延长，本页原创技能卷不能代替正式模拟。后续周数与达标规则见 [U04](u04-exam-preparation.md)。',
 '## 阅读：首答不查词']
 for d in sorted((SRC/'reading').glob(f'R-{week}-*')):
  out += [body(d/'student.md'),'<details>',f'<summary>{d.name} 答案、证据与精读（首答后展开）</summary>',body(d/'answers.md'),'</details>']
 out+=['## 写作与口语：Task 1双分支择一']
 for name in ['t1a','t1g','t2','s1','s2','s3']:
  out += [body(SRC/f'writing-speaking/{week}/{name}-student.md'),'<details>',f'<summary>{week} {name.upper()} 示例、反馈与重练（首答后展开）</summary>',body(SRC/f'writing-speaking/{week}/{name}-reference.md'),'</details>']
 out += ['## 许可','原创文字：RayXBuilds and contributors，CC BY 4.0。此页由已验收分课汇编，调整了标题和导航；题干、正文和答案内容保留。公开第三方音频未包含。']
 (ROOT/f'lessons/bridge/{uid}-week-{w:02}.md').write_text('\n\n'.join(out)+'\n')
(ROOT/'lessons/bridge/u35-feedback.md').write_text('# U35 阅读复盘与写作口语反馈协议\n\n'+body(SRC/'reading/STUDY-TRACKER.md')+'\n\n'+body(SRC/'writing-speaking/FEEDBACK.md')+'\n\n'+body(SRC/'writing-speaking/EVIDENCE.md')+'\n\n'+'\n\n'.join(body(SRC/'reading'/n) for n in ['EXAM-INTERFACE.md','FORMAL-ASSESSMENT.md','LEARNING-RECORD.md'])+'\n\n'+body(SRC/'writing-speaking/SOURCES.md')+'\n')
print('Compiled U31–U35 from',len(json.loads((SRC/'manifest.json').read_text())['source_files']),'verified source files')
