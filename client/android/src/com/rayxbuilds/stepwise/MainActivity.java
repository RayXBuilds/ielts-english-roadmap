package com.rayxbuilds.stepwise;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.content.res.AssetFileDescriptor;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.util.AtomicFile;
import android.view.WindowInsets;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import org.json.JSONObject;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.HashMap;
import java.util.Arrays;
import java.util.Locale;
import java.util.Map;

/** Offline-only host. No network or shared-storage permission is requested. */
public class MainActivity extends Activity {
    private static final String ORIGIN = "https://appassets.androidplatform.net";
    private static final String START = ORIGIN + "/site/client/index.html";
    private static final int LIMIT = 10 * 1024 * 1024;
    private static final int EXPORT = 1;
    private static final int IMPORT = 2;
    private WebView web;
    private AtomicFile store;
    private String pendingExport;
    private File exportCache;
    private boolean readFailed;

    @Override public void onCreate(Bundle saved) {
        super.onCreate(saved);
        store = new AtomicFile(new File(getFilesDir(), "progress.json"));
        exportCache = new File(getCacheDir(), "pending-export.json");
        FrameLayout container = new FrameLayout(this);
        container.setBackgroundColor(Color.rgb(247, 248, 250));
        container.setOnApplyWindowInsetsListener((view, insets) -> {
            // API 35 enforces edge-to-edge. Keep controls outside system bars and keyboard.
            if (android.os.Build.VERSION.SDK_INT >= 30) {
                android.graphics.Insets safe = insets.getInsets(WindowInsets.Type.systemBars()
                    | WindowInsets.Type.displayCutout() | WindowInsets.Type.ime());
                view.setPadding(safe.left, safe.top, safe.right, safe.bottom);
            } else {
                view.setPadding(insets.getSystemWindowInsetLeft(), insets.getSystemWindowInsetTop(),
                    insets.getSystemWindowInsetRight(), insets.getSystemWindowInsetBottom());
            }
            return insets;
        });
        web = new WebView(this);
        WebSettings settings = web.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(false);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setMediaPlaybackRequiresUserGesture(true);
        settings.setSupportMultipleWindows(false);
        web.setBackgroundColor(Color.rgb(247, 248, 250));
        web.addJavascriptInterface(new Bridge(), "StepwiseAndroid");
        web.setWebChromeClient(new WebChromeClient());
        web.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                // Navigation stays on the bundled entry document. Course changes are in-page.
                return !START.equals(request.getUrl().toString());
            }
            @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                return serve(request);
            }
        });
        container.addView(web, new FrameLayout.LayoutParams(-1, -1));
        setContentView(container);
        web.loadUrl(START);
    }

    private void callback(String function, String value) {
        runOnUiThread(() -> web.evaluateJavascript("window." + function + "(" + JSONObject.quote(value) + ")", null));
    }

    private byte[] readLimited(InputStream input) throws IOException {
        try (InputStream in = input; ByteArrayOutputStream out = new ByteArrayOutputStream()) {
            byte[] buffer = new byte[8192];
            int count;
            while ((count = in.read(buffer)) != -1) {
                if (out.size() + count >= LIMIT) throw new IOException("备份超过 10 MB");
                out.write(buffer, 0, count);
            }
            return out.toByteArray();
        }
    }

    private synchronized String loadState() {
        JSONObject result = new JSONObject();
        try {
            result.put("state", JSONObject.NULL);
            // AtomicFile.openRead recovers an interrupted previous write.
            if (hasStoredState()) {
                String raw = new String(readLimited(store.openRead()), StandardCharsets.UTF_8);
                result.put("state", new JSONObject(raw));
            }
        } catch (Exception error) {
            readFailed = true;
        }
        try { result.put("error", readFailed); } catch (Exception ignored) { }
        return result.toString();
    }

    private synchronized String writeState(String raw, boolean restoring) {
        FileOutputStream output = null;
        try {
            byte[] bytes = raw.getBytes(StandardCharsets.UTF_8);
            if (bytes.length >= LIMIT) throw new IOException("记录超过 10 MB");
            new JSONObject(raw);
            if (readFailed && !restoring) throw new IOException("原记录读取异常，请恢复有效备份");
            if (restoring && hasStoredState()) {
                File copy = new File(getFilesDir(), "before-restore-" + System.currentTimeMillis() + ".json");
                try (InputStream in = store.openRead()) {
                    Files.copy(in, copy.toPath());
                }
            }
            output = store.startWrite();
            output.write(bytes);
            store.finishWrite(output);
            output = null;
            if (!Arrays.equals(bytes, readLimited(store.openRead()))) throw new IOException("记录写入校验失败");
            readFailed = false;
            return "";
        } catch (Exception error) {
            if (output != null) store.failWrite(output);
            return "保存失败，请导出备份。" + error.getMessage();
        }
    }

    private boolean hasStoredState() {
        return store.getBaseFile().exists() || new File(store.getBaseFile().getPath() + ".bak").exists();
    }

    public final class Bridge {
        @JavascriptInterface public String load() { return loadState(); }
        @JavascriptInterface public String save(String raw, boolean restoring) {
            return writeState(raw, restoring);
        }
        @JavascriptInterface public void exportBackup(String raw) {
            if (raw == null || raw.getBytes(StandardCharsets.UTF_8).length >= LIMIT) return;
            runOnUiThread(() -> {
                try {
                    // Survives activity recreation while the system file picker is open.
                    Files.write(exportCache.toPath(), raw.getBytes(StandardCharsets.UTF_8));
                    pendingExport = raw;
                    Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
                    intent.setType("application/json");
                    intent.addCategory(Intent.CATEGORY_OPENABLE);
                    intent.putExtra(Intent.EXTRA_TITLE, "stepwise-backup.json");
                    startActivityForResult(intent, EXPORT);
                } catch (Exception error) { callback("nativeNotice", "无法打开文件选择器"); }
            });
        }
        @JavascriptInterface public void importBackup() {
            runOnUiThread(() -> new AlertDialog.Builder(MainActivity.this)
                .setTitle("恢复备份将替换当前学习记录")
                .setMessage("请先导出当前记录。恢复前会在应用内保留原文件副本。")
                .setNegativeButton("取消", null)
                .setPositiveButton("选择备份", (dialog, which) -> {
                    Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
                    intent.setType("*/*");
                    intent.addCategory(Intent.CATEGORY_OPENABLE);
                    try { startActivityForResult(intent, IMPORT); }
                    catch (Exception error) { callback("nativeNotice", "无法打开文件选择器"); }
                }).show());
        }
        @JavascriptInterface public void finishApp() { runOnUiThread(() -> finish()); }
    }

    @Override protected void onActivityResult(int request, int result, Intent data) {
        super.onActivityResult(request, result, data);
        if (result != RESULT_OK || data == null || data.getData() == null) {
            if (request == EXPORT) { pendingExport = null; exportCache.delete(); }
            return;
        }
        try {
            if (request == EXPORT) {
                byte[] bytes = pendingExport != null ? pendingExport.getBytes(StandardCharsets.UTF_8)
                    : readLimited(Files.newInputStream(exportCache.toPath()));
                try (OutputStream output = getContentResolver().openOutputStream(data.getData(), "wt")) {
                    if (output == null) throw new IOException("文件不可写入");
                    output.write(bytes);
                }
                callback("nativeNotice", "备份已导出");
            } else if (request == IMPORT) {
                InputStream input = getContentResolver().openInputStream(data.getData());
                if (input == null) throw new IOException("文件不可读取");
                String raw = new String(readLimited(input), StandardCharsets.UTF_8);
                callback("restoreBackup", raw);
            }
        } catch (Exception error) { callback("nativeNotice", "文件操作失败。" + error.getMessage()); }
        finally {
            if (request == EXPORT) { pendingExport = null; exportCache.delete(); }
        }
    }

    @Override public void onBackPressed() {
        web.evaluateJavascript("window.androidBack ? window.androidBack() : false", handled -> {
            if (!"true".equals(handled)) super.onBackPressed();
        });
    }
    @Override protected void onPause() {
        web.evaluateJavascript("document.querySelectorAll('audio,video').forEach(m=>m.pause());if(typeof save==='function')save()", null);
        web.onPause();
        super.onPause();
    }
    @Override protected void onResume() { super.onResume(); if (web != null) web.onResume(); }
    @Override protected void onDestroy() {
        web.removeJavascriptInterface("StepwiseAndroid");
        web.destroy();
        super.onDestroy();
    }

    private WebResourceResponse failure(int code, String reason) {
        return new WebResourceResponse("text/plain", "UTF-8", code, reason,
            new HashMap<>(), new ByteArrayInputStream(new byte[0]));
    }
    private WebResourceResponse serve(WebResourceRequest request) {
        Uri uri = request.getUrl();
        String path = uri.getPath();
        if (!"https".equals(uri.getScheme()) || !"appassets.androidplatform.net".equals(uri.getHost())
            || uri.getPort() != -1 || !"GET".equals(request.getMethod())
            || path == null || !path.startsWith("/site/") || path.contains("..")
            || path.contains("\\") || uri.getQuery() != null) return failure(403, "Forbidden");
        String asset = path.substring(1);
        try {
            String mime = mimeType(asset);
            Map<String, String> headers = new HashMap<>();
            headers.put("X-Content-Type-Options", "nosniff");
            headers.put("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; media-src 'self'; connect-src 'none'; frame-src 'none'; object-src 'none'; base-uri 'none'");
            if (asset.endsWith(".mp3") || asset.endsWith(".mp4")) {
                // Uncompressed APK media supports precise range reads for offline seeking.
                AssetFileDescriptor descriptor = getAssets().openFd(asset);
                long total = descriptor.getLength();
                descriptor.close();
                String range = request.getRequestHeaders().get("Range");
                if (range == null) range = request.getRequestHeaders().get("range");
                long[] bounds;
                try { bounds = MediaRange.parse(range, total); }
                catch (IllegalArgumentException invalid) { return failure(416, "Range Not Satisfiable"); }
                InputStream input = getAssets().open(asset);
                long skipped = 0;
                while (skipped < bounds[0]) {
                    long step = input.skip(bounds[0] - skipped);
                    if (step == 0) { input.close(); throw new IOException("Cannot seek asset"); }
                    skipped += step;
                }
                long length = bounds[1] - bounds[0] + 1;
                headers.put("Accept-Ranges", "bytes");
                headers.put("Content-Length", Long.toString(length));
                if (range != null) headers.put("Content-Range", "bytes " + bounds[0] + "-" + bounds[1] + "/" + total);
                return new WebResourceResponse(mime, null, range == null ? 200 : 206,
                    range == null ? "OK" : "Partial Content", headers, new LimitedInputStream(input, length));
            }
            return new WebResourceResponse(mime, "UTF-8", 200, "OK", headers, getAssets().open(asset));
        } catch (IOException error) { return failure(404, "Not Found"); }
    }
    private String mimeType(String name) {
        String extension = name.substring(name.lastIndexOf('.') + 1).toLowerCase(Locale.ROOT);
        switch (extension) {
            case "html": return "text/html";
            case "js": return "application/javascript";
            case "css": return "text/css";
            case "svg": return "image/svg+xml";
            case "png": return "image/png";
            case "jpg": case "jpeg": return "image/jpeg";
            case "mp3": return "audio/mpeg";
            case "mp4": return "video/mp4";
            case "json": return "application/json";
            default: return "text/plain";
        }
    }
}
