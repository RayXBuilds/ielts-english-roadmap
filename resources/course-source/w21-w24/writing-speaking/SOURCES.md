# 来源、许可与边界

本批题干、数据、人物情境、英文示例、教学说明与SVG为原创教学材料，由本次制作编写；不是历年真题、标准化试卷或学生真实经历。未导入第三方作文/音频全文。示例没有官方评分，难度未校准。代码生成SVG，qa-renders为对应SVG的系统渲染检查件，无AI光栅生成图。

Copyright © 2026 RayXBuilds and contributors。原创教学内容与SVG采用[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，分享或改编须署名、链接许可并注明修改。外部网站、商标和第三方试题不随此许可开放，本包仅提供来源链接，不复制受限整卷。

## 规则参考

2026-11-03实际读取官方页面，以下仅支持考试格式和评分原则，不代表官方认可本课程或题目：

| 来源 | 本批使用范围 |
|---|---|
| [IELTS Academic Writing格式](https://ielts.org/take-a-test/test-types/ielts-academic-test/ielts-academic-format-writing) | 两题、Task 1至少150词约20分钟、Task 2至少250词约40分钟、连贯成文及四个维度 |
| [IELTS General Training Writing格式](https://ielts.org/take-a-test/test-types/ielts-general-training-test/ielts-general-training-format-writing) | 书信情境与三要点、语气、最低字数和写作时限 |
| [IELTS Speaking格式](https://ielts.org/take-a-test/test-types/ielts-academic-test/ielts-academic-format-speaking) | 三部分，总11～14分钟；Part 1/3各4～5分钟，Part 2含准备约3～4分钟；四个评价维度 |
| [IELTS评分说明](https://ielts.org/take-a-test/your-results/ielts-scoring-in-detail) | 总分与各单项分别记录；听读原始分和换算依据；模考估计不能冒充官方成绩 |

课内任务选择、分钟分配、每周180/120分钟、24周规划、T22/T24记录与报考检查，是本项目教学安排。依据只读的U04（implementation/repos/ielts-english-roadmap/lessons/bridge/u04-exam-preparation.md）及本次派工落实；不修改U04或共享仓库。

## W21实际界面待办入口

[IDP官方熟悉材料介绍](https://ielts.idp.com/about/ielts-familiarisation-tests)可作为后续查找入口。本次搜索可见介绍，但直接读取返回403；未进入或试用实际界面，不能写已完成或已验证与所选考场相同。另一个British Council熟悉页面本次读取超时，因此也没有记为实际操作完成。

可从[IELTS官方考试形式说明](https://www.ielts.org/take-a-test/why-choose-ielts/ways-to-take-ielts)确认适合所选形式的入口。学生应按当地真实可报形式核实；本课“纸笔/键入”仅指输入练习方式，不宣称各地当前同时提供所有考试形式。普通客户端不能冒充考试环境。

## 原始源文件与复现

[content.py](content.py)：12写作题与示例；[speaking.py](speaking.py)：12口语任务与示例；[figures.py](figures.py)：4张SVG；[transfer.py](transfer.py)：各周证据与交接操作；[build.py](build.py)：独立生成学生/参考页与清单；[validate.py](validate.py)：结构、计数、预算、链接、算术与前批保护；[freeze.py](freeze.py)：冻结哈希。

冻结后不主动重跑生成器；只有明确返工授权后才重建本批，并更新自检及冻结清单。不运行前批生成器。外部正式卷仍由学习者在合法私人副本完成，本批不声称提供T22/T24整卷或真实成绩。
