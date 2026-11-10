package com.rayxbuilds.stepwise.checks;

import android.app.Activity;
import android.app.Instrumentation;
import android.content.ComponentName;
import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.os.SystemClock;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.view.accessibility.AccessibilityNodeInfo;
import android.webkit.WebView;
import org.json.JSONArray;
import java.io.File;
import java.io.FileOutputStream;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;

/** Runs only against the isolated .qa package on an emulator or test device. */
public class SmokeInstrumentation extends Instrumentation {
    private Activity activity;
    private WebView web;
    private int checks;

    @Override public void onCreate(Bundle arguments) { super.onCreate(arguments); start(); }
    private WebView findWeb(View view) {
        if (view instanceof WebView) return (WebView) view;
        if (view instanceof ViewGroup) {
            ViewGroup group = (ViewGroup) view;
            for (int i = 0; i < group.getChildCount(); i++) {
                WebView result = findWeb(group.getChildAt(i));
                if (result != null) return result;
            }
        }
        return null;
    }
    private void launch() throws Exception {
        Intent intent = new Intent(Intent.ACTION_MAIN);
        intent.setComponent(new ComponentName("com.rayxbuilds.stepwise.qa", "com.rayxbuilds.stepwise.MainActivity"));
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        activity = startActivitySync(intent);
        runOnMainSync(() -> web = findWeb(activity.getWindow().getDecorView()));
        await("typeof state !== 'undefined' && document.querySelector('#view').textContent.length>100", "app start");
    }
    private String js(String source) throws Exception {
        CountDownLatch ready = new CountDownLatch(1);
        AtomicReference<String> result = new AtomicReference<>();
        runOnMainSync(() -> web.evaluateJavascript(source, value -> { result.set(value); ready.countDown(); }));
        if (!ready.await(15, TimeUnit.SECONDS)) throw new AssertionError("JavaScript timed out");
        return result.get();
    }
    private void check(String source, String label) throws Exception {
        if (!"true".equals(js(source))) throw new AssertionError(label + ": " + js(source));
        checks++;
    }
    private void await(String source, String label) throws Exception {
        long deadline = SystemClock.uptimeMillis() + 20000;
        while (SystemClock.uptimeMillis() < deadline) {
            if ("true".equals(js(source))) { checks++; return; }
            SystemClock.sleep(200);
        }
        throw new AssertionError("Timed out: " + label + " / " + js("document.body.innerText.slice(0,500)"));
    }
    private void tap(String selector) throws Exception {
        js("document.querySelector(" + org.json.JSONObject.quote(selector) + ").scrollIntoView({block:'center'})");
        SystemClock.sleep(300);
        JSONArray point = new JSONArray(js("(()=>{const r=document.querySelector(" + org.json.JSONObject.quote(selector)
            + ").getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2,innerWidth]})()"));
        int[] location = new int[2];
        runOnMainSync(() -> web.getLocationOnScreen(location));
        float scale = web.getWidth() / (float) point.getDouble(2);
        float x = location[0] + (float) point.getDouble(0) * scale;
        float y = location[1] + (float) point.getDouble(1) * scale;
        long now = SystemClock.uptimeMillis();
        sendPointerSync(MotionEvent.obtain(now, now, MotionEvent.ACTION_DOWN, x, y, 0));
        sendPointerSync(MotionEvent.obtain(now, now + 60, MotionEvent.ACTION_UP, x, y, 0));
    }
    private void screenshot(String name) throws Exception {
        CountDownLatch painted = new CountDownLatch(1);
        runOnMainSync(() -> web.postVisualStateCallback(1, new WebView.VisualStateCallback() {
            @Override public void onComplete(long id) { painted.countDown(); }
        }));
        if (!painted.await(10, TimeUnit.SECONDS)) throw new AssertionError("Frame did not render");
        SystemClock.sleep(1000);
        Bitmap bitmap = getUiAutomation().takeScreenshot();
        if (bitmap == null) throw new AssertionError("Screenshot unavailable");
        File file = new File(activity.getFilesDir(), name + ".png");
        try (FileOutputStream out = new FileOutputStream(file)) { bitmap.compress(Bitmap.CompressFormat.PNG, 100, out); }
        bitmap.recycle();
    }
    private void clickSystemText(String text) throws Exception {
        long deadline = SystemClock.uptimeMillis() + 15000;
        while (SystemClock.uptimeMillis() < deadline) {
            AccessibilityNodeInfo root = getUiAutomation().getRootInActiveWindow();
            if (root != null) {
                for (AccessibilityNodeInfo node : root.findAccessibilityNodeInfosByText(text)) {
                    if (node.getText() == null || !text.equalsIgnoreCase(node.getText().toString())) continue;
                    AccessibilityNodeInfo target = node;
                    while (target != null && !target.isClickable()) target = target.getParent();
                    if (target != null && target.performAction(AccessibilityNodeInfo.ACTION_CLICK)) return;
                }
            }
            SystemClock.sleep(300);
        }
        throw new AssertionError("System picker button missing: " + text);
    }
    @Override public void onStart() {
        Bundle result = new Bundle();
        try {
            launch();
            js("window.restoreBackup(JSON.stringify(blank()))");
            check("D.lessons.length===126 && D.days.length===84 && window.ANDROID_MODE===true", "bundled course count");
            screenshot("android-home");
            for (String route : new String[]{"home", "reading", "listening", "speaking", "plan", "words", "settings"}) {
                js("navigate('" + route + "')");
                check("document.documentElement.scrollWidth <= innerWidth+1", "phone overflow " + route);
            }
            js("document.querySelector('#mobileMenu').click()");
            check("document.body.classList.contains('menu-open')", "drawer opens");
            check("window.androidBack() && !document.body.classList.contains('menu-open')", "back closes drawer");
            js("openSearch();document.querySelector('#allSearch').value='u68';searchAll()");
            check("document.querySelectorAll('#searchResults [data-open]').length===1", "search finds advanced writing");
            js("document.querySelector('#searchResults [data-open]').click()");
            check("current==='u68' && document.querySelectorAll('.lesson details').length>0", "search opens lesson");
            check("document.documentElement.scrollWidth <= innerWidth+1", "writing fits phone");
            js("openLesson('r01');document.querySelector('#notes').value='Android 中文笔记';document.querySelector('#notes').dispatchEvent(new Event('input'));document.querySelector('#complete').click();addWord('offline','离线','r01')");
            check("state.completed.r01===true && state.words.length===1", "course completion and vocabulary");
            check("JSON.parse(window.StepwiseAndroid.load()).state.notes.r01==='Android 中文笔记'", "native disk save");
            js("window.restoreBackup('{}')");
            check("state.notes.r01==='Android 中文笔记'", "invalid backup preserves notes");
            runOnMainSync(() -> activity.finish());
            waitForIdleSync();
            launch();
            check("state.notes.r01==='Android 中文笔记' && state.completed.r01===true && state.words[0].term==='offline'", "restart persistence");
            js("navigate('settings');document.querySelector('#export').click()");
            clickSystemText("Save");
            SystemClock.sleep(1000);
            AccessibilityNodeInfo picker = getUiAutomation().getRootInActiveWindow();
            if (picker != null && !picker.findAccessibilityNodeInfosByText("Replace").isEmpty()) clickSystemText("Replace");
            await("document.querySelector('#toast').textContent.includes('备份已导出')", "system picker export");
            js("state.notes.r01='temporary replacement';save();document.querySelector('#import').click()");
            clickSystemText("选择备份");
            clickSystemText("stepwise-backup.json");
            await("state.notes.r01==='Android 中文笔记'", "system picker restore round trip");
            js("openLesson('l01')");
            await("Number.isFinite(document.querySelector('#audio').duration) && !document.querySelector('#playAudio').disabled", "audio metadata offline");
            tap("#playAudio");
            await("document.querySelector('#audio').currentTime > 0.5 && !document.querySelector('#audio').paused", "audio plays");
            js("document.querySelector('#audio').currentTime=8;document.querySelector('#audio').playbackRate=1.25");
            await("document.querySelector('#audio').currentTime>=8 && !document.querySelector('#audio').seeking", "audio seek");
            js("document.querySelector('#audio').pause();document.querySelector('.video-panel').open=true;document.querySelector('video').play()");
            await("document.querySelector('video').currentTime>0.5 && document.querySelector('video').videoWidth>0", "video decodes offline");
            js("document.querySelector('video').currentTime=20");
            await("document.querySelector('video').currentTime>=20 && !document.querySelector('video').seeking", "video seek");
            js("document.querySelector('video').pause();document.querySelector('.video-panel').open=false;window.scrollTo(0,0)");
            screenshot("android-listening");
            js("const old=blank();delete old.previewRead;delete old.preferences;old.notes.r01='Mac compatible backup';old.completed.u36=true;window.restoreBackup(JSON.stringify(old))");
            check("state.notes.r01==='Mac compatible backup' && state.previewRead.u36===true && !state.completed.u36", "legacy Mac backup migration");
            js("window.restoreBackup(JSON.stringify(blank()))");
            js("openLesson('r01')");
            sendKeyDownUpSync(android.view.KeyEvent.KEYCODE_BACK);
            await("current===null && route==='reading'", "Android system back");
            js("navigate('home')");
            result.putString("stream", "PASS " + checks + " Android runtime checks\n");
            finish(Activity.RESULT_OK, result);
        } catch (Throwable error) {
            result.putString("stream", "FAIL " + error + "\n");
            finish(Activity.RESULT_CANCELED, result);
        }
    }
}
