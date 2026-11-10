# Android 首版与 Mac 下载入口

本次以公开提交 `7b6a106` 为基线，在独立工作区实现 Android 客户端。主工作区内课程 v0.17、客户端 0.2.13 与 Windows 候选修改保留，未混入本次安装包。

## 交付范围

- Android 0.1.0 预览版，独立版本序列，应用标识 `com.rayxbuilds.stepwise`。
- 内置课程 v0.14 的 126 条目、84 天任务、12 MP3 和 12 MP4。原媒体按 manifest 逐项校验，采用原署名与许可依据。
- 手机导航、搜索、阅读、笔记、生词、进度、倍速与定位播放、系统文件选择器备份。支持已有 Mac JSON 备份的已收录课程记录。
- 仓库首页增加 Mac 与 Android 下载表，Android 文档附一张实际模拟器截图。

## 验证

- JavaScript 共 14 项回归检查通过，包含 Android 写入失败和恢复失败时保留现有状态。
- Java 媒体范围与流边界检查通过，含开放区间、后缀区间、越界及非法区间。
- Android 15 / API 35 ARM64，WebView 124.0.6367.219，Pixel 7 模拟器。411dp 检查通过，最终 360dp 飞行模式回归通过 28 项检查。
- 原生检查包含导航、七个栏目与写作页无横向溢出、搜索、笔记、生词、标记完成、重启持久化、非法备份拒绝、Mac 旧备份迁移、系统文件选择器导出与恢复、音视频实际时间推进和跳转、系统返回键。
- 软件图形后端出现截图重影，改用 host 硬件后端后视觉检查通过。模拟器测试建议使用 `-gpu host -feature -Vulkan`。
- APK 压缩包 CRC、16 KB 对齐、v2/v3 签名及全部 24 个媒体哈希通过。发布包未启用 debuggable，未声明联网或存储权限。
- Mac 0.2.10 本地 ZIP CRC 与 codesign 验证通过，大小及 SHA-256 与既有发布记录一致。

## 发布文件

Android APK 大小为 237480031 字节。

```text
0c7511867e4696d265bdadb7a984d48fcced55ec13a9619c5b77d4432de2d088  Stepwise-English-Android-v0.1.0.apk
```

Android 签名证书 SHA-256 如下，私钥保存在本机私有构建目录，未进入仓库或发布包。

```text
106c54c90bfabd02dad00185355cbd0725bef40629b56ff2d8b3b3b05f712f93
```

最低构建目标 Android 8.0。其他 Android 版本、各厂商真机和用户实际安装仍需验证。新增 24 周听力的完整音频仍待补，本次继续提供文字预览。Mac 包仍采用 ad-hoc 签名，未经过 Apple 公证。

## 发布确认

已发布 `android-v0.1.0` 预览版，对应源码提交 `213ce717fe994851eaec8dd51a46935b697f2198`。GitHub API 确认 APK、SHA256SUMS-android.txt 和 build-report.json 三项资产均为 uploaded，远端大小及 SHA-256 与本地逐项一致。[Android 下载页](https://github.com/RayXBuilds/ielts-english-roadmap/releases/tag/android-v0.1.0)

最终安装包、校验文件、构建回执与运行检查记录保存于项目交付目录的 `android-v0.1.0/`。完整源码另保存在长期规划目录下 `implementation/worktrees/ielts-android-client`，便于在保留主工作区候选修改的同时继续维护。
