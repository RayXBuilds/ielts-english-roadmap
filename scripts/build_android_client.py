"""Build the offline Android APK with Android SDK tools and a private signing key.

No Gradle or runtime library download is needed. Requires JDK 17+ and Android SDK
platform 35 / build-tools 35.0.0. Build outputs and signing files stay outside Git.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ANDROID = ROOT / "client/android"
NS = "{http://schemas.android.com/apk/res/android}"


def run(*command):
    subprocess.run([str(arg) for arg in command], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--sdk", type=Path, required=True)
    parser.add_argument("--java-home", type=Path, required=True)
    parser.add_argument("--keystore", type=Path, required=True)
    parser.add_argument("--password-file", type=Path, required=True)
    parser.add_argument("--qa", action="store_true")
    args = parser.parse_args()
    output = args.output.resolve()
    if output == ROOT or ROOT in output.parents:
        parser.error("Build outside the repository")
    if output.exists():
        parser.error("Use a new output directory to preserve previous artifacts")
    if not args.keystore.is_file() or not args.password_file.is_file():
        parser.error("Provide an existing private signing key and password file")
    os.environ["JAVA_HOME"] = str(args.java_home.resolve())
    sdk = args.sdk.resolve()
    tool = sdk / "build-tools/35.0.0"
    android_jar = sdk / "platforms/android-35/android.jar"
    java = args.java_home / "bin"
    for required in [tool / "aapt2", tool / "d8", android_jar, java / "javac"]:
        if not required.is_file():
            parser.error(f"Missing build tool: {required}")
    output.mkdir(parents=True)
    run(sys.executable, ROOT / "scripts/build_offline.py")

    site = output / "assets/site"
    site.mkdir(parents=True)
    # Explicitly include learning content, with no native sources or personal files.
    for folder in ["assets", "lessons", "resources", "plans"]:
        shutil.copytree(ROOT / folder, site / folder)
    (site / "client/assets").mkdir(parents=True)
    for name in ["index.html", "style.css", "mobile.css", "mobile.js", "state.js", "app.js", "data.js", "LICENSE"]:
        shutil.copy2(ROOT / "client" / name, site / "client" / name)
    shutil.copy2(ROOT / "client/assets/app-icon.png", site / "client/assets/app-icon.png")
    shutil.copy2(ANDROID / "bootstrap.js", site / "client/android-bootstrap.js")
    shutil.copy2(ROOT / "LICENSE.md", site / "LICENSE.md")
    # Figure references under docs are selected by generated course HTML.
    import re
    for relative in set(re.findall(r'\.\./(docs/[^"\\<>]+)', (site / "client/data.js").read_text())):
        source = ROOT / relative
        if source.is_file():
            destination = site / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    index = site / "client/index.html"
    index.write_text(index.read_text().replace('<script src="data.js">', '<script src="android-bootstrap.js"></script><script src="data.js">'))
    media = json.loads((ROOT / "assets/voa/manifest.json").read_text())
    for row in media:
        path = site / row["path"]
        assert path.stat().st_size == row["bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]

    tree = ET.parse(ANDROID / "AndroidManifest.xml")
    manifest = tree.getroot()
    version = manifest.attrib[NS + "versionName"]
    app = manifest.find("application")
    if args.qa:
        manifest.set("package", "com.rayxbuilds.stepwise.qa")
        app.set(NS + "debuggable", "true")
        app.set(NS + "label", "拾阶英语验收")
        app.find("activity").set(NS + "name", "com.rayxbuilds.stepwise.MainActivity")
    tree.write(output / "AndroidManifest.xml", encoding="utf-8", xml_declaration=True)
    shutil.copytree(ANDROID / "res", output / "res")
    icon = output / "res/mipmap-hdpi/icon_image.png"
    icon.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "client/assets/app-icon.png", icon)
    run(tool / "aapt2", "compile", "--dir", output / "res", "-o", output / "resources.zip")
    run(tool / "aapt2", "link", "-I", android_jar, "--manifest", output / "AndroidManifest.xml",
        "-A", output / "assets", "-0", "mp3", "-0", "mp4", "-o", output / "unsigned.apk", output / "resources.zip")
    classes = output / "classes"
    classes.mkdir()
    run(java / "javac", "--release", "8", "-encoding", "UTF-8", "-classpath", android_jar,
        "-d", classes, *sorted((ANDROID / "src").rglob("*.java")))
    with zipfile.ZipFile(output / "classes.jar", "w") as archive:
        for file in classes.rglob("*.class"):
            archive.write(file, file.relative_to(classes))
    dex = output / "dex"
    dex.mkdir()
    run(tool / "d8", "--lib", android_jar, "--min-api", "26", "--output", dex, output / "classes.jar")
    with zipfile.ZipFile(output / "unsigned.apk", "a", compression=zipfile.ZIP_DEFLATED) as archive:
        for file in dex.glob("*.dex"):
            archive.write(file, file.name)
    run(tool / "zipalign", "-P", "16", "-f", "4", output / "unsigned.apk", output / "aligned.apk")
    filename = f"Stepwise-English-Android-v{version}{'-qa' if args.qa else ''}.apk"
    apk = output / filename
    run(tool / "apksigner", "sign", "--ks", args.keystore, "--ks-key-alias", "stepwise",
        "--ks-pass", "file:" + str(args.password_file), "--out", apk, output / "aligned.apk")
    run(tool / "apksigner", "verify", "--verbose", "--print-certs", apk)
    run(tool / "zipalign", "-c", "-P", "16", "4", apk)
    with zipfile.ZipFile(apk) as archive:
        assert archive.testzip() is None
        assert not any(Path(name).name == "progress.json" for name in archive.namelist())
        for row in media:
            entry = "assets/site/" + row["path"]
            assert archive.getinfo(entry).compress_type == zipfile.ZIP_STORED
            assert hashlib.sha256(archive.read(entry)).hexdigest() == row["sha256"]
    digest = hashlib.sha256(apk.read_bytes()).hexdigest()
    (output / "SHA256SUMS-android.txt").write_text(f"{digest}  {filename}\n")
    report = {"version": version, "course_version": json.loads((ROOT / "client/version.json").read_text())["course_version"],
              "bytes": apk.stat().st_size, "sha256": digest, "media_files": len(media), "qa": args.qa}
    (output / "build-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
