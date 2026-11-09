# 每期制作流程

第 1 期（2026-11-08 至 11-09）跑通后总结。每期照此走，节点之间需要用户确认的地方标了 👤。

## 1. 脚本

1. 按 `docs/curriculum.md` 确定这期只回答的**一个问题**和前置期数。
2. 写 `script.md` 初稿（规则见 `episodes/README.md` 的 8 条讲法规则）。时长不卡死，把问题讲明白优先。
3. 写 `facts.md`：每条事实性说法 + 出处，PubMed / 官方页面逐条核对。
4. 写 `meta.yml`。

## 2. 两道独立审核（规范：`docs/feynman-review.md`）

- 并行起两个子代理：**新生复述测试**（只给脚本）、**费曼 9 条审核**（给脚本、大纲、facts、toycell）。
- 汇总到 `reviews/feynman.md`，按严重度修订；修订后重跑新生复述测试。
- 👤 用户审阅脚本；按意见修订直到 facts 全部 ✅。

## 3. 配音（规范：`docs/voice.md`）

- 按 `## 节` 拆段，用 gemini-voice-mcp `synthesize_speech`（voice `Charon`、固定风格提示、`zh-CN`）逐段合成 → `audio/sec1..N.wav`。
  - 工具结果过大会存进 tool-results 文件：用 `jq -r '.[1].text' 文件 | jq -r .data | base64 -d` 解出 WAV。
- faster-whisper 转写逐段比对原稿，查读音。
- 👤 用户试听。

## 4. 卡点

```bash
~/.venvs/media/bin/python video/make_cues.py zh     # → audio/vo_final.wav + cues.zh.json
```
- 在 `make_cues.py` 的 `PAUSES` 里加"让观众先猜"的停顿。
- 打印每节句子起点占比（见第 1 期做法），把 `frame.html` 里的节拍阈值对到句子起点上。

## 5. 画面

- 复制上一期的 `video/`（`frame.html`、`render.py`、`make_data.py`、`make_cues.py`）。
- 模型数值一律由 `make_data.py` 从 toycell 生成 `data.js`；需要和旁白对拍时只调**播放速度**，不改数据。
- 画面文字全部放 `i18n/zh.json`。
- 关键帧联系表（解释器用仓库根目录 `.venv-render`）：
  ```bash
  ../../.venv-render/bin/python video/render.py sheet reviews/contact_vN.png t1 t2 ...
  ```
- 按 `dark-explainer` 技能第 9 节避坑清单自查：溢出、压字、重复、颜色语义、科学误导（如药物分子穿过细胞核）。
- 👤 用户审联系表。

## 6. 成片

```bash
../../.venv-render/bin/python video/render.py video out/epNNN-zh-vN.mp4 30   # 约 6 分钟成片需 10–15 分钟
```
- 抽帧检查 + `volumedetect` 音量 + `silencedetect` 确认停顿。
- 👤 用户看成片。定稿后更新 `meta.yml` 状态和 README 的"已发布"表。

## 色彩语义（全系列固定）

钢蓝 = 柱子/正常；亮蓝箭头 = 推动；朱橙丁字头 = 压住；紫 = 人为干预（扰动、药物）；深灰 = 被关掉；金 = 临时焦点；绿只用于"正确 ✓"。
