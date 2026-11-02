"""Build standalone local readers from the checked-in lessons; Python stdlib only."""
from pathlib import Path
import html,re
ROOT=Path(__file__).resolve().parents[1]
sections=[]
for name,title in [('plans/first-28-days.md','Day 1–28'),('plans/days-29-84.md','Day 29–84')]:sections.append((ROOT/name,'plan'+('1' if 'first' in name else '2'),title))
for folder,prefix in [('readings','r'),('listening','l'),('speaking','s'),('bridge','u')]:
 for f in sorted((ROOT/'lessons'/folder).glob('*.md')):
  number=re.search(r'(\d+)',f.stem)[1];sections.append((f,prefix+number,f.read_text().splitlines()[0].lstrip('# ')))
sections.append((ROOT/'resources/ielts-systematic.md','u00','U00 雅思系统资料选用指南'))
sections.append((ROOT/'lessons/checkpoints.md','checks','阶段检查'))
ids={f.resolve():id for f,id,title in sections}
def inline(text,source):
 def link(m):
  label,url=m.groups()
  if url.startswith(('https://','http://')):return html.escape(label)+'（原始来源见文档）'
  target=(source.parent/url.split('#')[0]).resolve()
  if target in ids:return f'<a href="#{ids[target]}">{html.escape(label)}</a>'
  try:rel=str(target.relative_to(ROOT))
  except ValueError:return html.escape(label)
  return f'<a href="{html.escape(rel,quote=True)}">{html.escape(label)}</a>'
 # Escape all prose; only markdown links and bold are supported.
 parts=[];last=0
 for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)',text):parts.extend([html.escape(text[last:m.start()]),link(m)]);last=m.end()
 parts.append(html.escape(text[last:]));return re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',''.join(parts))
def render(text,source):
 out=[];paragraph=[];table=False
 def flush():
  if paragraph:out.append('<p>'+' '.join(paragraph)+'</p>');paragraph.clear()
 for line in text.splitlines():
  line=line.strip()
  if line.startswith('## 来源与许可'):break
  if line.startswith('|'):
   flush()
   if not table:out.append('<div class="table"><table>');table=True
   cells=[c.strip() for c in line.strip('|').split('|')]
   if all(re.fullmatch('[-: ]+',c) for c in cells):continue
   out.append('<tr>'+''.join('<td>'+inline(c,source)+'</td>' for c in cells)+'</tr>');continue
  if table:out.append('</table></div>');table=False
  if not line:flush();continue
  if line in ['<details>','</details>'] or re.fullmatch('<summary>[^<]+</summary>',line):flush();out.append(line);continue
  if line.startswith('#'):
   flush();level=min(4,len(line)-len(line.lstrip('#'))+1);out.append(f'<h{level}>'+inline(line.lstrip('# '),source)+f'</h{level}>');continue
  if re.match(r'(\d+\. |[-*] )',line):flush();out.append('<p class="item">'+inline(line,source)+'</p>');continue
  paragraph.append(inline(line,source))
 flush()
 if table:out.append('</table></div>')
 return '\n'.join(out)
css='body{margin:0;background:#f5f3ed;color:#263244;font:17px/1.8 system-ui,sans-serif}main{max-width:920px;margin:auto;padding:28px 20px}section{padding:24px;background:#fff;margin:24px 0;border-radius:12px}a{color:#1559a4}nav a{display:inline-block;margin:4px 12px 4px 0}summary{cursor:pointer;font-weight:600}audio,video{width:100%;max-height:450px}h1,h2,h3{line-height:1.4}.table{overflow:auto}td{border-bottom:1px solid #ddd;min-width:100px;padding:8px;vertical-align:top}table{border-collapse:collapse}.item{margin:8px 0}.muted{color:#647084}'
for mode in ['full','audio']:
 out=['<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>雅思英语学习路线 12 周基础与 8 周雅思专项课程</title><style>'+css+'</style><main><h1>雅思英语学习路线</h1><p>24 篇短文 · 12 课听力 · 12 周口语 · 84 天基础任务 · 8 周雅思专项 · 四项原创工作坊</p><p class="muted">解压完整目录后打开此页，无外部脚本、字体或播放器依赖。先独立作答，再展开文本或答案。原创练习非雅思真题，难度未经正式校准。阶段检查请留到第 8、12 周。</p>']
 for group,prefix in [('学习日程','plan'),('阅读短文','r'),('听力与视频','l'),('口语任务','s'),('衔接单元','u'),('阶段检查','checks')]:
  out.append('<nav><strong>'+group+'</strong><br>')
  out.extend(f'<a href="#{id}">{html.escape(title if prefix in ["plan","checks","u"] else id.upper())}</a>' for f,id,title in sections if id.startswith(prefix))
  out.append('</nav>')
 for f,id,title in sections:
  text=f.read_text()
  if mode=='audio':text=re.sub(r'\[([^\]]*(?:MP4|视频)[^\]]*)\]\([^)]+\.mp4\)','视频见完整版',text)
  out.append(f'<section id="{id}">')
  if id.startswith('l'):
   n=id[1:];out.append(f'<audio controls preload="none" src="assets/voa/lesson-{n}.mp3"></audio>')
   if mode=='full':out.append(f'<details><summary>播放完整课程视频</summary><video controls preload="none" src="assets/voa/lesson-{n}.mp4"></video></details>')
   else:out.append('<p>文字与音频版不包含视频，完整视频另见完整包。</p>')
  out.append(render(text,f));out.append('<a href="#">回到顶部</a></section>')
 out.append('<footer>原创文字：RayXBuilds，CC BY 4.0。对话与教学媒体：VOA Learning English，依据原站自制内容公共领域与署名转载政策收录。详情见 assets/voa/README.md。与 IELTS 或 VOA 官方无隶属关系。</footer></main></html>')
 (ROOT/('offline.html' if mode=='full' else 'offline-audio.html')).write_text('\n'.join(out))
print('Built 84-day readers from',len(sections),'source documents')

# Desktop curriculum shares the same generated sections and stable course IDs.
import runpy
runpy.run_path(str(ROOT/"scripts/build_client.py"))
