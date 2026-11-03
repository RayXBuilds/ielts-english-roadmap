"""Build, verify, and package the self-contained arm64 macOS client (MIT)."""
from pathlib import Path
import argparse,sys,subprocess,shutil,plistlib,hashlib,json,zipfile
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('output',nargs='?',default='/tmp/stepwise-client')
parser.add_argument('--qa',action='store_true',help='Isolated bundle ID and learning data for UI verification')
args=parser.parse_args()
out=Path(args.output).resolve()
assert root not in out.parents and out!=root,'Build outside the repository'
version=json.loads((root/'client/version.json').read_text())
name='拾阶英语预览' if args.qa else '拾阶英语'
app=out/(name+'.app');contents=app/'Contents';binary=contents/'MacOS';res=contents/'Resources';site=res/'site'
binary.mkdir(parents=True,exist_ok=True);site.mkdir(parents=True,exist_ok=True)
subprocess.run([sys.executable,str(root/'scripts/build_offline.py')],check=True)
subprocess.run(['swiftc','-target','arm64-apple-macos14.0','-module-cache-path','/tmp/stepwise-swift-cache','-O',str(root/'client/native/main.swift'),'-o',str(binary/'StepwiseEnglish'),'-framework','Cocoa','-framework','WebKit'],check=True)
for folder in ['client','assets','lessons','resources','docs','plans']:
 shutil.copytree(root/folder,site/folder,dirs_exist_ok=True,ignore=shutil.ignore_patterns('native','__pycache__'))
for row in json.loads((root/'assets/voa/manifest.json').read_text()):
 media=site/row['path']
 assert media.stat().st_size==row['bytes'] and hashlib.sha256(media.read_bytes()).hexdigest()==row['sha256']
shutil.copy2(root/'LICENSE.md',site/'LICENSE.md')
iconset=out/'Stepwise.iconset';iconset.mkdir(exist_ok=True)
subprocess.run(['swift','-module-cache-path','/tmp/stepwise-swift-cache',str(root/'client/native/icon.swift'),str(out/'icon.png')],check=True)
for size in [16,32,128,256,512]:
 for scale in [1,2]:
  dest=iconset/f'icon_{size}x{size}{"@2x" if scale==2 else ""}.png'
  subprocess.run(['sips','-z',str(size*scale),str(size*scale),str(out/'icon.png'),'--out',str(dest)],check=True,stdout=subprocess.DEVNULL)
subprocess.run(['iconutil','-c','icns',str(iconset),'-o',str(res/'Stepwise.icns')],check=True)
info={'CFBundleIconFile':'Stepwise.icns','CFBundleExecutable':'StepwiseEnglish','CFBundleIdentifier':'com.rayxbuilds.stepwise-english'+('.qa' if args.qa else ''),'CFBundleName':name,'CFBundleDisplayName':name,'CFBundleVersion':version['build'],'CFBundleShortVersionString':version['version'],'CFBundlePackageType':'APPL','LSMinimumSystemVersion':'14.0','NSHighResolutionCapable':True}
with (contents/'Info.plist').open('wb') as f:plistlib.dump(info,f)
subprocess.run(['codesign','--force','--deep','--sign','-',str(app)],check=True)
subprocess.run(['codesign','--verify','--deep','--strict',str(app)],check=True)
print(app)
if args.qa:sys.exit(0)
archive=out/f"Stepwise-English-macOS-arm64-v{version['version']}.zip"
assert not archive.exists(),'Use a fresh output directory; published ZIPs must not be overwritten'
subprocess.run(['ditto','-c','-k','--sequesterRsrc','--keepParent',str(app),str(archive)],check=True)
with zipfile.ZipFile(archive,'a') as z:
 z.writestr('开始使用.txt',f"拾阶英语 {version['version']} — 雅思英语离线学习客户端\nApple 芯片 Mac，最低构建目标 macOS 14。解压后将拾阶英语.app 放入应用程序。\n此版本为本地签名，未经 Apple 公证，可能被系统拦截。安装及使用说明：\nhttps://github.com/RayXBuilds/ielts-english-roadmap/blob/main/client/README.md\n课程与既有12课媒体随应用提供。新增24周听力材料为文字预览，完整音频待补。设置与备份页面可导出和恢复学习记录，兼容 0.1 版备份。升级前建议导出备份。\n")
 assert z.testzip() is None
 assert not any(n.endswith('progress.json') for n in z.namelist())
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
(out/'SHA256SUMS-client.txt').write_text(f'{digest}  {archive.name}\n')
print(archive.name,archive.stat().st_size,digest)
