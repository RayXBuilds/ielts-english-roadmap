"""Validate local references and media hashes, then create full/audio ZIPs."""
from pathlib import Path
import re,json,hashlib,zipfile,sys
ROOT=Path(__file__).resolve().parents[1]
DEST=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/tmp/ielts-learning-packages')
DEST.mkdir(parents=True,exist_ok=True)
files=[f for f in ROOT.rglob('*') if f.is_file() and '.git' not in f.parts and '__pycache__' not in f.parts]
for f in files:
 if f.suffix!='.md':continue
 for url in re.findall(r'\]\(([^)]+)\)',f.read_text()):
  if url.startswith(('https://','http://','#')):continue
  assert (f.parent/url.split('#')[0]).exists(),(f,url)
for name in ['offline.html','offline-audio.html']:
 s=(ROOT/name).read_text();ids=set(re.findall(r'id="([^"]+)"',s))
 for attr,url in re.findall(r'(src|href)="([^"]+)"',s):
  if url=='#':continue
  if url.startswith('#'):assert url[1:] in ids,(name,url)
  else:assert (ROOT/url).exists(),(name,url)
 assert not re.search(r'(?:src|href)="https?://',s),'External dependency'
plan='\n'.join((ROOT/n).read_text() for n in ['plans/first-28-days.md','plans/days-29-84.md'])
assert [int(n) for n in re.findall(r'\| Day (\d+) \|',plan)]==list(range(1,85))
for folder,expected in [('readings',24),('listening',12),('speaking',12),('bridge',25)]:assert len(list((ROOT/'lessons'/folder).glob('*.md')))==expected
course=(ROOT/'lessons/bridge/u02-ielts-eight-weeks.md').read_text()
expected=[f'{w}.{d}' for w in range(1,8) for d in range(1,7)]+[f'8.{d}' for d in range(1,5)]
assert re.findall(r'^\| (\d+\.\d+) \|',course,re.M)==expected,'8-week task sequence'
manifest=json.loads((ROOT/'assets/voa/manifest.json').read_text());assert len(manifest)==24
for r in manifest:
 f=ROOT/r['path'];assert f.stat().st_size==r['bytes'];assert hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256']
 assert f.stat().st_size<50_000_000,'Unexpected oversized media'
for mode in ['full','audio']:
 dest=DEST/f'ielts-english-roadmap-v0.10-{mode}.zip'
 assert not dest.exists(),'Use a fresh output directory; do not overwrite published ZIPs'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
  for f in files:
   if mode=='audio' and (f.suffix=='.mp4' or f.name=='offline.html'):continue
   rel=str(f.relative_to(ROOT))
   if mode=='audio' and rel=='offline-audio.html':rel='offline.html'
   z.write(f,'ielts-english-roadmap/'+rel)
  if mode=='audio':z.writestr('ielts-english-roadmap/START-HERE.txt','文字与音频版：打开 offline.html。此包不含视频，Markdown 中的 MP4 链接仅在完整版有效。\n')
 with zipfile.ZipFile(dest) as z:
  assert z.testzip() is None
  names=set(z.namelist());s=z.read('ielts-english-roadmap/offline.html').decode()
  for src in re.findall(r'src="([^"]+)"',s):assert 'ielts-english-roadmap/'+src in names
 print(dest.name,dest.stat().st_size,hashlib.sha256(dest.read_bytes()).hexdigest())
print('PASS: links, local HTML, 84 days, 73 lesson files, 8-week course and resource guide, 24 media hashes, ZIP integrity')
