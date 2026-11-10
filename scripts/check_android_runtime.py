"""Build and run native smoke checks against an isolated Android QA install."""
from pathlib import Path
import argparse
import os
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--sdk", type=Path, required=True)
    parser.add_argument("--java-home", type=Path, required=True)
    parser.add_argument("--keystore", type=Path, required=True)
    parser.add_argument("--password-file", type=Path, required=True)
    parser.add_argument("--serial", required=True, help="Explicit isolated emulator or test-device serial")
    args = parser.parse_args()
    out = args.output.resolve()
    if out.exists():
        parser.error("Use a new output directory")
    out.mkdir(parents=True)
    os.environ["JAVA_HOME"] = str(args.java_home)
    sdk = args.sdk
    tools = sdk / "build-tools/35.0.0"
    android = sdk / "platforms/android-35/android.jar"
    java = args.java_home / "bin"

    def run(*command):
        subprocess.run([str(arg) for arg in command], check=True)

    (out / "AndroidManifest.xml").write_text('''<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.rayxbuilds.stepwise.checks">
      <uses-sdk android:minSdkVersion="26" android:targetSdkVersion="35" />
      <application android:label="Stepwise checks" android:debuggable="true" />
      <instrumentation android:name="com.rayxbuilds.stepwise.checks.SmokeInstrumentation" android:targetPackage="com.rayxbuilds.stepwise.qa" />
    </manifest>''')
    run(tools / "aapt2", "link", "-I", android, "--manifest", out / "AndroidManifest.xml", "-o", out / "test.apk")
    (out / "classes").mkdir()
    run(java / "javac", "--release", "8", "-encoding", "UTF-8", "-classpath", android,
        "-d", out / "classes", ROOT / "tests/android/SmokeInstrumentation.java")
    with zipfile.ZipFile(out / "classes.jar", "w") as archive:
        for file in (out / "classes").rglob("*.class"):
            archive.write(file, file.relative_to(out / "classes"))
    (out / "dex").mkdir()
    run(tools / "d8", "--lib", android, "--min-api", "26", "--output", out / "dex", out / "classes.jar")
    with zipfile.ZipFile(out / "test.apk", "a") as archive:
        archive.write(out / "dex/classes.dex", "classes.dex")
    run(tools / "zipalign", "-f", "4", out / "test.apk", out / "aligned.apk")
    run(tools / "apksigner", "sign", "--ks", args.keystore, "--ks-key-alias", "stepwise",
        "--ks-pass", "file:" + str(args.password_file), "--out", out / "checks.apk", out / "aligned.apk")
    adb = [str(sdk / "platform-tools/adb"), "-s", args.serial]
    run(*adb, "install", "--no-incremental", "-r", out / "checks.apk")
    result = subprocess.run(adb + ["shell", "am", "instrument", "-w", "com.rayxbuilds.stepwise.checks/com.rayxbuilds.stepwise.checks.SmokeInstrumentation"], text=True, capture_output=True, timeout=240)
    (out / "runtime-results.txt").write_text(result.stdout + result.stderr)
    print(result.stdout, result.stderr)
    if result.returncode != 0 or "PASS " not in result.stdout or "FAIL " in result.stdout:
        raise SystemExit("Android runtime checks failed")
    for name in ["android-home", "android-listening"]:
        picture = subprocess.check_output(adb + ["exec-out", "run-as", "com.rayxbuilds.stepwise.qa", "cat", f"files/{name}.png"])
        (out / f"{name}.png").write_bytes(picture)


if __name__ == "__main__":
    main()
