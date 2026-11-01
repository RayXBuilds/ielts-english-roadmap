"""Build a self-contained arm64 macOS app using the system Swift compiler."""
from pathlib import Path
import sys,subprocess,shutil,plistlib,hashlib,json,zipfile
root=Path(__file__).resolve().parents[1]
out=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/tmp/stepwise-client')
app=out/'拾阶英语.app';contents=app/'Contents';binary=contents/'MacOS';res=contents/'Resources';site=res/'site'
binary.mkdir(parents=True,exist_ok=True);site.mkdir(parents=True,exist_ok=True)
subprocess.run([sys.executable,str(root/'scripts/build_offline.py')],check=True)
subprocess.run(['swiftc','-target','arm64-apple-macos14.0','-module-cache-path','/tmp/stepwise-swift-cache','-O',str(root/'client/native/main.swift'),'-o',str(binary/'StepwiseEnglish'),'-framework','Cocoa','-framework','WebKit'],check=True)
shutil.copytree(root/'client',site/'client',dirs_exist_ok=True,ignore=shutil.ignore_patterns('native'))
shutil.copytree(root/'assets',site/'assets',dirs_exist_ok=True)
shutil.copytree(root/'lessons',site/'lessons',dirs_exist_ok=True)
for row in json.loads((root/'assets/voa/manifest.json').read_text()):
 media=site/row['path']
 assert media.stat().st_size==row['bytes'] and hashlib.sha256(media.read_bytes()).hexdigest()==row['sha256']
for f in ['LICENSE.md']:shutil.copy2(root/f,site/f)
iconset=out/'Stepwise.iconset';iconset.mkdir(exist_ok=True)
subprocess.run(['swift','-module-cache-path','/tmp/stepwise-swift-cache',str(root/'client/native/icon.swift'),str(out/'icon.png')],check=True)
for size in [16,32,128,256,512]:
 for scale in [1,2]:
  dest=iconset/f'icon_{size}x{size}{"@2x" if scale==2 else ""}.png'
  subprocess.run(['sips','-z',str(size*scale),str(size*scale),str(out/'icon.png'),'--out',str(dest)],check=True,stdout=subprocess.DEVNULL)
subprocess.run(['iconutil','-c','icns',str(iconset),'-o',str(res/'Stepwise.icns')],check=True)
with (contents/'Info.plist').open('wb') as f:plistlib.dump({'CFBundleIconFile':'Stepwise.icns','CFBundleExecutable':'StepwiseEnglish','CFBundleIdentifier':'com.rayxbuilds.stepwise-english','CFBundleName':'拾阶英语','CFBundleDisplayName':'拾阶英语','CFBundleVersion':'1','CFBundleShortVersionString':'0.1.0','CFBundlePackageType':'APPL','LSMinimumSystemVersion':'14.0','NSHighResolutionCapable':True},f)
subprocess.run(['codesign','--force','--deep','--sign','-',str(app)],check=True)
subprocess.run(['codesign','--verify','--deep','--strict',str(app)],check=True)
archive=out/'Stepwise-English-macOS-arm64-v0.1.0.zip'
subprocess.run(['ditto','-c','-k','--sequesterRsrc','--keepParent',str(app),str(archive)],check=True)
with zipfile.ZipFile(archive,'a') as z:
 z.writestr('开始使用.txt','拾阶英语 0.1.0 — 雅思英语离线学习客户端\nApple 芯片 Mac，构建最低目标 macOS 14。解压后将拾阶英语.app 放入应用程序。\n此预览版为本地签名，未经 Apple 公证，可能被系统拦截。安装及使用说明：\nhttps://github.com/RayXBuilds/ielts-english-roadmap/blob/main/client/README.md\n全部课程及音视频随应用提供，无需登录。学习记录保存在本机，请定期导出备份。\n')
 assert z.testzip() is None
 assert not any(n.endswith('progress.json') for n in z.namelist())
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
(out/'SHA256SUMS-client.txt').write_text(f'{digest}  {archive.name}\n')
print(app)
print(archive.name,archive.stat().st_size,digest)
