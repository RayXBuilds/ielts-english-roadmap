"""Compile independently accepted supplemental workshops and source guide."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'resources/supplement-source'
manifest = json.loads((SOURCE / 'manifest.json').read_text())
for entry in manifest['source_files']:
    assert hashlib.sha256((SOURCE / entry['path']).read_bytes()).hexdigest() == entry['sha256'], entry['path']


def body(path):
    def link(match):
        image, label, url = match.groups()
        if url.startswith(('https://', 'http://')):
            return f'{label}（{url}）'
        if image:
            target = (path.parent / url).resolve()
            assert target.is_file() and target.suffix == '.svg'
            return f'![{label}](../../{target.relative_to(ROOT)})'
        return f'{label}（本页下方展开参考）'

    text = re.sub(r'<!--.*?-->', '', path.read_text(), flags=re.S)
    text = re.sub(r'(!?)\[([^\]]+)\]\(([^)]+)\)', link, text)
    return re.sub(r'^(#+) ', lambda m: '#' * (len(m[1]) + 1) + ' ', text, flags=re.M).strip()


def lesson(number, student, reference):
    title = student.read_text().splitlines()[0].lstrip('# ')
    text = [
        f'# U{number} {title}',
        '原创专项补充。先完成学生任务，再展开参考答案。用本单元笔记记录首答、错因和重练结果，实际录音与真人反馈另行完成。',
        body(student),
        '<details>',
        '<summary>完成首答后查看参考、证据与修订</summary>',
        body(reference),
        '</details>',
        '## 许可说明',
        '原创文字和图示采用 CC BY 4.0，RayXBuilds and contributors。原创专项不换算正式雅思分数。',
    ]
    (ROOT / f'lessons/bridge/u{number}-supplement.md').write_text('\n\n'.join(text) + '\n')


for index in range(1, 9):
    batch = 'reading-batch-01' if index <= 4 else 'reading-batch-02'
    folder = SOURCE / batch / f'SR-{index:02}'
    lesson(59 + index, folder / 'student.md', folder / 'answers.md')
for group, prefix, offset in [('writing', 'W', 67), ('speaking', 'S', 71)]:
    for index in range(1, 5):
        folder = SOURCE / group
        lesson(offset + index, folder / f'{prefix}{index:02}-student.md', folder / f'{prefix}{index:02}-reference.md')

guide = '# U76 剑桥历版资料与官方免费样题\n\n联网时可复制下列完整网址到浏览器。按页面标明的免费、购买或借阅条件获取材料，所列出版年用于识别版本。\n\n'
guide += body(SOURCE / 'official-sources/真题查找指南.md') + '\n'
(ROOT / 'lessons/bridge/u76-official-sources.md').write_text(guide)
print('Compiled U60–U76 from', len(manifest['source_files']), 'accepted source files')
