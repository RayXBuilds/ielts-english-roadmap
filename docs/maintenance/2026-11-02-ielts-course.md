# 2026-11-02 雅思系统课程维护

用户要求继续寻找系统资料并规划课程。起始 main 与 origin/main 一致，工作区干净；未覆盖用户修改。读取原有课程、材料目录、贡献指南和维护记录后，新增 U00、U02、U03，保留 U01 和基础编号。

本次查询使用 BC 中国、IELTS、剑桥官方页面。权限和访问结果记录在 resources/ielts-systematic.md。没有登录付费平台，没有新增第三方下载；没有声称中国大陆播放已验证。原创练习包含答案证据与统计单位辨析，示例段不标作完整范文或官方分数。任务共 46 项、48 小时预算；第 8 周连续练习单独预留 180 分钟。

离线构建增加资料指南；客户端复制文档以保留本地引用，桥接单元不再统一显示为 30 分钟。校验保留固定内容数量、84 天序列、46 项专项任务序列、53 个客户端条目及内部链接、24 个媒体哈希、ZIP CRC。无新媒体，不重复下载或解码既有已验文件。

发布目标：独立资料 v0.5.0-ielts-course 与客户端 client-v0.2.1。上传成功并验证远端哈希后再清理旧版；本记录不单独证明发布成功，回执另行补充。

发布前复核：U03 第 4 题改为直接判断统计口径，避免由计数方法推断实际重复来访。已完成 9 项状态测试、独立 QA 客户端的搜索、U02→U03 跳转、正文排版和答案折叠检查。首次上传在草稿阶段停止并重建，未发布有歧义的候选包。

## 发布与保留回执

课程与客户端发布指向 c07faeabb64e591f5ccdb0af36da0a679f90d7f2。两个 Release 均已公开；以下五个文件状态 uploaded，远端大小与 SHA-256 均与本地一致：

- ielts-english-roadmap-v0.5-full.zip：228961606 字节；SHA-256 c8abe8c45531b257daee30e94a24d9019994d6845840eb77c4ac0d7d29bfe4f8。
- ielts-english-roadmap-v0.5-audio.zip：9698807 字节；SHA-256 b6c962091a9755bb0ffc8bf5f852a639b30154a9df6f0fdf3a4bad7df1f00c5d。
- SHA256SUMS-v0.5.txt：205 字节；SHA-256 210e7516c725da6b3f46e56cfe9d5cca25bc334d9096be2cb1a494877a6047c8。
- Stepwise-English-macOS-arm64-v0.2.1.zip：229500885 字节；SHA-256 da48b313fef4e011c9f0c7a4baab100cadfbdf63d7c20a1d54a4121203acd4d9。
- SHA256SUMS-client.txt：106 字节；SHA-256 cf2ed05f87e8066028711f042d25599d7953df2b371f542ae1e193b4a6f2173c。

下载：[课程 v0.5](https://github.com/RayXBuilds/ielts-english-roadmap/releases/tag/v0.5.0-ielts-course) · [客户端 0.2.1](https://github.com/RayXBuilds/ielts-english-roadmap/releases/tag/client-v0.2.1)。

按用户仅保留新版的要求，核验后删除 client-v0.2.0 和 v0.4.0-evidence 的发布与标签，以及相应本地旧包。保留最新 app、安装 ZIP、完整/音频课程 ZIP 和校验文件；清理图标中间文件与本轮 QA 应用，不触碰 Application Support 学习记录或 Git 历史。
