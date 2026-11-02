import Cocoa
import WebKit
import UniformTypeIdentifiers

class AppDelegate: NSObject, NSApplicationDelegate, WKScriptMessageHandler, WKNavigationDelegate {
    var window: NSWindow!
    var web: WKWebView!
    var site: URL!
    let store = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0].appendingPathComponent((Bundle.main.bundleIdentifier?.hasSuffix(".qa") == true ? "StepwiseEnglish-QA" : "StepwiseEnglish") + "/progress.json")
    func notice(_ text: String) {
        let data = try! JSONSerialization.data(withJSONObject: [text])
        web.evaluateJavaScript("window.nativeNotice(\(String(data:data,encoding:.utf8)!)[0])")
    }
    func applicationDidFinishLaunching(_ notification: Notification) {
        let menu = NSMenu(); let appItem = NSMenuItem(); menu.addItem(appItem)
        let appMenu = NSMenu(); appMenu.addItem(withTitle:"退出拾阶英语", action:#selector(NSApplication.terminate(_:)), keyEquivalent:"q"); appItem.submenu=appMenu
        let editItem=NSMenuItem();menu.addItem(editItem);let edit=NSMenu(title:"编辑");editItem.submenu=edit
        for (title,sel,key) in [("撤销","undo:","z"),("剪切","cut:","x"),("复制","copy:","c"),("粘贴","paste:","v"),("全选","selectAll:","a")] {edit.addItem(withTitle:title,action:Selector(sel),keyEquivalent:key)}
        NSApp.mainMenu=menu
        site=Bundle.main.resourceURL!.appendingPathComponent("site")
        var raw="null"; var loadFailed=false
        if FileManager.default.fileExists(atPath:store.path) {
            do { let data=try Data(contentsOf:store);_ = try JSONSerialization.jsonObject(with:data);raw=String(data:data,encoding:.utf8) ?? "null" } catch { loadFailed=true }
        }
        let config=WKWebViewConfiguration()
        config.userContentController.add(self,name:"app")
        config.userContentController.addUserScript(WKUserScript(source:"window.NATIVE_MODE=true;window.NATIVE_STATE=\(raw);window.STATE_ERROR=\(loadFailed);",injectionTime:.atDocumentStart,forMainFrameOnly:true))
        web=WKWebView(frame:.zero,configuration:config);web.navigationDelegate=self
        window=NSWindow(contentRect:NSRect(x:0,y:0,width:1280,height:860),styleMask:[.titled,.closable,.miniaturizable,.resizable],backing:.buffered,defer:false)
        window.appearance=NSAppearance(named:.aqua);window.title="拾阶英语 · 你的英语学习空间";window.setFrameAutosaveName("StepwiseMainWindow");window.minSize=NSSize(width:850,height:600);window.contentView=web;window.center();window.makeKeyAndOrderFront(nil)
        web.loadFileURL(site.appendingPathComponent("client/index.html"),allowingReadAccessTo:site)
        NSApp.activate(ignoringOtherApps:true)
        if loadFailed {let a=NSAlert();a.messageText="学习记录无法读取";a.informativeText="原文件已保留。请使用有效备份恢复；恢复前不会覆盖原记录。";a.runModal()}
    }
    func applicationShouldTerminateAfterLastWindowClosed(_ sender:NSApplication)->Bool {true}
    func webView(_ webView:WKWebView,decidePolicyFor action:WKNavigationAction,decisionHandler:@escaping(WKNavigationActionPolicy)->Void){
        guard let url=action.request.url, url.isFileURL, url.standardizedFileURL.path.hasPrefix(site.standardizedFileURL.path+"/") else {decisionHandler(.cancel);return}
        decisionHandler(.allow)
    }
    func userContentController(_ controller:WKUserContentController,didReceive message:WKScriptMessage){
        guard message.frameInfo.isMainFrame, let body=message.body as? [String:Any],let action=body["action"] as? String else{return}
        switch action {
        case "save", "export":
            guard let raw=body["payload"] as? String,raw.utf8.count<10*1024*1024,let data=raw.data(using:.utf8),(try? JSONSerialization.jsonObject(with:data)) != nil else {notice("记录格式无效，未保存");return}
            if action == "save" {
                do {try FileManager.default.createDirectory(at:store.deletingLastPathComponent(),withIntermediateDirectories:true);try data.write(to:store,options:.atomic);web.evaluateJavaScript("window.nativeSaved()") } catch { let message="保存失败，请导出备份：\(error.localizedDescription)";let arg=try! JSONSerialization.data(withJSONObject:[message]);web.evaluateJavaScript("window.nativeSaveFailed(\(String(data:arg,encoding:.utf8)!)[0])") }
            } else {
                let panel=NSSavePanel();panel.nameFieldStringValue="拾阶英语学习备份.json";panel.allowedContentTypes=[.json]
                panel.beginSheetModal(for:window){r in if r == .OK,let url=panel.url {do{try data.write(to:url,options:.atomic);self.notice("备份已导出")}catch{self.notice("导出失败：\(error.localizedDescription)")}}}
            }
        case "import":
            let alert=NSAlert();alert.messageText="恢复备份将替换当前学习记录";alert.informativeText="建议先导出当前记录。请选择本客户端导出的 JSON 文件。";alert.addButton(withTitle:"选择备份");alert.addButton(withTitle:"取消")
            alert.beginSheetModal(for:window){r in guard r == .alertFirstButtonReturn else{return};let panel=NSOpenPanel();panel.allowedContentTypes=[.json];panel.allowsMultipleSelection=false;panel.beginSheetModal(for:self.window){r in if r == .OK,let url=panel.url {do{let data=try Data(contentsOf:url);guard data.count<10*1024*1024,let raw=String(data:data,encoding:.utf8) else{self.notice("备份过大或编码无效");return};let arg=try JSONSerialization.data(withJSONObject:[raw]);self.web.evaluateJavaScript("window.restoreBackup(\(String(data:arg,encoding:.utf8)!)[0])")}catch{self.notice("读取备份失败")}}}}
        default:break
        }
    }
}
let app=NSApplication.shared
let delegate=AppDelegate()
app.delegate=delegate
app.setActivationPolicy(.regular)
app.run()
