"""Compile accepted listening text; no player, audio or listening completion claim."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'resources/listening-source'
manifest = json.loads((SRC / 'manifest.json').read_text())
for row in manifest['source_files'] + manifest['acceptance_receipts']:
    assert hashlib.sha256((SRC / row['path']).read_bytes()).hexdigest() == row['sha256'], row['path']


def body(path):
    text = path.read_text()
    def link(match):
        image, label, url = match.groups()
        target = path.parent / url
        assert image and target.is_file() and target.suffix == '.svg', (path, url)
        return f'![{label}](../../{target.relative_to(ROOT)})'
    text = re.sub(r'(!?)\[([^\]]+)\]\(([^)]+)\)', link, text)
    return re.sub(r'^(#+) ', lambda m: '#' * (len(m[1]) + 2) + ' ', text, flags=re.M).strip()


for week in range(1, 25):
    lesson_id = f'L-W{week:02}'
    source = SRC / lesson_id
    uid = f'u{week + 35:02}'
    out = [
        f'# {uid.upper()} 第{week}周听力题面与复盘（音频待补）',
        '本页提供已核验的原创题目、参考答案和脚本。配套完整音频尚未验收，当前只能预览题面；不能进行有效的首次听力测试，也不能把读稿作答计作听力成绩或已完成一套听力。',
        '请先保留首次作答机会：批准音频就绪前，不要展开下方答案和脚本。若已读稿，请标记为熟悉材料，之后的练习不能充当陌生题诊断。页面阅读标记只代表看过文字，不代表完成听力。',
        '本材料非雅思真题、非标准化模考，不换算正式分数。计划分钟数不是实测音频时长；学习记录、正式测评和真人反馈须另行完成。',
        '## 学生题面',
        body(source / 'student.md'),
    ]
    for filename, label in [
        ('answers.md', '参考答案与证据（完成首次听力后再展开）'),
        ('script.md', '完整脚本（提前阅读会失去陌生题首答机会）'),
        ('intensive.md', '精听与复盘步骤（须有已验收配套音频）'),
    ]:
        out += ['<details>', f'<summary>{label}</summary>', body(source / filename), '</details>']
    out += ['## 许可说明', '原创文字和图示：RayXBuilds and contributors，CC BY 4.0。本页不包含配套音频；现有基础VOA媒体不能代替本套题的录音。']
    (ROOT / f'lessons/bridge/{uid}-listening-text-{week:02}.md').write_text('\n\n'.join(out) + '\n')

print('Compiled 24 listening text previews; approved new audio sets: 0')
