"""Generate the desktop client's local curriculum from the offline reader."""
from pathlib import Path
import re,json,html
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'offline.html').read_text();lessons=[]
for id,body in re.findall(r'<section id="([^"]+)">(.*?)</section>',s,re.S):
 if id.startswith('plan'):continue
 title=re.search(r'<h2>(.*?)</h2>',body,re.S)
 title=html.unescape(re.sub('<[^>]+>','',title[1])) if title else id
 body=re.sub(r'<audio.*?</audio>','',body,flags=re.S)
 body=re.sub(r'<details><summary>播放完整课程视频</summary><video.*?</details>','',body,flags=re.S)
 body=body.replace('<a href="#">回到顶部</a>','')
 body=re.sub(r'<p><a href="assets/.*?</p>','',body,flags=re.S)
 body=re.sub(r'(href|src)="(?!#)([^"]+)"',r'\1="../\2"',body)
 lessons.append(dict(id=id,title=title,html=body,type='reading' if id.startswith('r') else 'listening' if id.startswith('l') else 'speaking' if id.startswith('s') else 'bridge' if id.startswith('u') else 'check'))
days=[]
for name in ['first-28-days.md','days-29-84.md']:
 for line in (ROOT/'plans'/name).read_text().splitlines():
  if not line.startswith('| Day '):continue
  c=[x.strip() for x in line.strip('|').split('|')]
  def link(m):
   label,path=m.groups();n=re.search(r'(\d+)',Path(path).stem)
   id=('r' if 'readings' in path else 's' if 'speaking' in path else 'l')+n[1]
   return f'<a href="#{id}">{html.escape(label)}</a>'
  material=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,c[2])
  days.append(dict(day=int(c[0].split()[1]),title=c[1],materials=material,steps=c[3],output=c[4]))
assert len(lessons)==55 and len({l['id'] for l in lessons})==len(lessons)
assert [d['day'] for d in days]==list(range(1,85))
ids={l['id'] for l in lessons}
assert {'u00','u01','u02','u03','u04','u05'} <= ids
for lesson in lessons:
 for target in re.findall(r'href="#([^"]+)"',lesson['html']):assert target in ids,(lesson['id'],target)
for d in days:
 for target in re.findall(r'href="#([^"]+)"',d['materials']):assert target in ids,(d['day'],target)
credits=(ROOT/'assets/voa/README.md').read_text()+'\n\n'+(ROOT/'LICENSE.md').read_text()
(ROOT/'client/data.js').write_text('window.COURSE_DATA='+json.dumps(dict(lessons=lessons,days=days,credits=credits,version=json.loads((ROOT/'client/version.json').read_text())['version']),ensure_ascii=False)+';\n')
print('Client data:',len(lessons),'units;',len(days),'days')
