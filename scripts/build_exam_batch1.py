"""Compile accepted W01–04 text into weekly readers without changing source text."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'resources/course-source/w01-w04'
for row in json.loads((SRC/'manifest.json').read_text())['source_files']:
 assert hashlib.sha256((SRC/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
def body(p):
 s=p.read_text()
 s=re.sub(r'<!--.*?-->','',s,flags=re.S)
 # Reader cannot open arbitrary Markdown; references are in the same unit or U10.
 def link(m):
  label,url=m.groups()
  if url.startswith(('https://','http://')):return m[0]
  if 'FEEDBACK.md' in url:return '[反馈协议](u10-feedback.md)'
  return label+'（本节下方展开参考）'
 s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,s)
 return re.sub(r'^(#+) ',lambda m:'#'*(len(m[1])+2)+' ',s,flags=re.M).strip()
for w in range(1,5):
 week=f'W{w:02}';uid=f'u{w+5:02}'
 out=[f'# {uid.upper()} 第{w}周：长篇阅读、写作与口语',
 '本页为已独立核验的原创文字课程。先完成学生题目，再展开对应参考。非真题、非标准化模考，不换算雅思分数。听力尚未补齐，本页不代表全科课程已完成。',
 '每周选A或G类Task 1一题，加Task 2及三次口语。参考范文不是学生已完成作业，仍须提交初稿、录音和重写，独立真人评分另行安排。',
 f'阅读必做{180 if w==1 else 120}分钟（含延迟复测）；写作180分钟；口语120分钟。第2～4周另可用60分钟复盘本周错因、长句和段落主旨；这些是复习，不能记为新篇。词汇60分钟、听力180分钟另列，听力材料未验收前标待补，不勾整周完成。',
 'W01如使用正式T01建立基线，替换本周相应首答时段，不能把两套首答同时塞入预算。后续周数与达标规则见 [U04](u04-exam-preparation.md)。',
 '## 阅读：首答不查词']
 for d in sorted((SRC/'reading').glob(f'R-{week}-*')):
  out += [body(d/'student.md'),'<details>',f'<summary>{d.name} 答案、证据与精读（首答后展开）</summary>',body(d/'answers.md'),'</details>']
 out+=['## 写作与口语：Task 1双分支择一']
 for name in ['t1a','t1g','t2','s1','s2','s3']:
  out += [body(SRC/f'writing-speaking/{week}/{name}-student.md'),'<details>',f'<summary>{week} {name.upper()} 示例、反馈与重练（首答后展开）</summary>',body(SRC/f'writing-speaking/{week}/{name}-reference.md'),'</details>']
 out += ['## 许可','原创文字：RayXBuilds and contributors，CC BY 4.0。此页由已验收分课汇编，调整了标题和导航；题干、正文和答案内容保留。公开第三方音频未包含。']
 (ROOT/f'lessons/bridge/{uid}-week-{w:02}.md').write_text('\n\n'.join(out)+'\n')
(ROOT/'lessons/bridge/u10-feedback.md').write_text('# U10 写作与口语反馈协议\n\n'+body(SRC/'writing-speaking/FEEDBACK.md')+'\n')
print('Compiled U06–U10 from',len(json.loads((SRC/'manifest.json').read_text())['source_files']),'verified source files')
