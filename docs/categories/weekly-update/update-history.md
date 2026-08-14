# 已有目录更新记录

## 本周记录

本周对已有论文/知识库内容的修订记录。

| 日期 | 项目 | 操作 | 状态 |
|:----|:-----|:----|:----|
| 06/29 | **weekly_update.py 修复** | 修复arXiv API查询顺序bug（HTTP→HTTPS、submittedDate→AND NOT顺序） | ✅ 完成 |
| 06/29 | **weekly-update/ 新增9领域论文** | 本周arXiv抓取9领域×20篇，筛选21篇高影响力论文撰写摘要 | ✅ 完成 |
| 06/29 | **新增论文页面更新** | new-papers.md重写：11篇精选论文完整中文摘要 | ✅ 完成 |
| 06/29 | **高影响力论文页面** | high-impact-papers.md 首次填充 | ✅ 完成 |
| 06/29 | **新增方法路线页面** | new-methods.md 首次填充 | ✅ 完成 |
| 06/29 | **重要模型发布页面** | model-releases.md 首次填充 | ✅ 完成 |
| 06/29 | **数据集与Benchmark页面** | datasets-benchmarks.md 首次填充 | ✅ 完成 |
| 06/29 | **开源项目页面** | open-source.md 首次填充 | ✅ 完成 |
| 06/29 | **产业与应用动态页面** | industry-news.md 首次填充 | ✅ 完成 |
| 06/29 | **推荐精读页面** | recommended-reading.md 首次填充 | ✅ 完成 |
| 06/29 | **下周重点观察页面** | next-week-focus.md 首次填充 | ✅ 完成 |
| 06/29 | **index.md** | 更新最后更新日期 | ✅ 完成 |

## 详细记录

### 🛠️ weekly_update.py 修复（06/29）

在排查本周论文抓取空结果问题时，发现两个关键bug并修复：

1. **HTTP→HTTPS**：arXiv API已迁移至HTTPS，（`http://export.arxiv.org` 301→`https://`），改为直接使用HTTPS
2. **提交日期查询顺序**：`submittedDate:[...]` 必须放在 `AND NOT` 排除条件之前，否则arXiv API静默丢弃日期筛选
3. 增加429限流自动重试和超时从30s延长至60s

详见 `D:\ai_research\weekly_update.py`。

### 📥 本周论文入库（06/29）

成功从arXiv抓取9领域×20篇本周论文（2026-06-21~2026-06-29），LLM评估后筛选21篇写入各领域摘要页。

---

*每周更新 — 2026-06-29*
