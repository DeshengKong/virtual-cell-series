# 每期制作流程

第 1 期（2026-11-08 至 11-09）跑通后总结，2026-11-09 按 `docs/decisions/2026-11-09-plan-v2.md` 修订。

需要你确认的地方只有三处，标了 👤：**脚本 + 分镜**、**中英成片**、**发布**。其余环节由脚本和审核 agent 把关，出了它们判断不了的问题才来问你。

相关规范：讲法 `episodes/README.md`；画面 `docs/directing.md`；审核 `docs/feynman-review.md`；谁查什么 `docs/agents.md`；配音 `docs/voice.md`。

## 0. 选题与前置检查

1. 按 `docs/curriculum.md` 确定这期只回答的**一个问题**、地图上亮哪一格。
2. 看 `docs/promises.md`：这期要还哪些账。
3. 列出这期打算用到的概念，先查前置：
   ```bash
   ~/.venvs/media/bin/python tools/check_prereq.py --plan 2 --uses cell-state,push,hold-back,balance,rule-formula
   ```
   没讲过的概念，要么在本期当场讲清（新术语 ≤ 3 个），要么先加一期铺垫。
4. 脚本按"弧"成批写（一次 3–4 期），一个弧里的前置一起检查。

## 1. 写稿

1. `script.md` 初稿：骨架见 `docs/directing.md` 第 1 节，讲法规则见 `episodes/README.md`。时长不卡死，把问题讲明白优先。
2. `storyboard.md` 分镜表（`docs/directing.md` 第 7 节）：每个节拍画面上有什么、什么在动、数字从哪来。**分镜通过之前不写画面代码。**
3. `facts.md`：每条事实性说法 + 出处，PubMed / 官方页面逐条核对。
4. `meta.yml`：填 `introduces` 和 `uses`（`docs/concepts.yml` 的 id），新概念同时写进 `concepts.yml`。再跑一次 `tools/check_prereq.py`，不带参数，必须通过。

## 2. 脚本审核（规范：`docs/feynman-review.md`）

并行起四个 agent，互相看不到对方的结果：

| agent | 给它什么 |
|---|---|
| `freshman-follower` | 本期 `script.md` + 之前各期 `script.md` |
| `freshman-dropin` | 只听版：`python3 tools/strip_cues.py episodes/epNNN-…/script.md > <仓库外的临时文件>` |
| `feynman-reviewer` | 本期 `script.md` |
| `fact-checker` | 本期 `script.md`（它做完自己的清单才会去看 `facts.md`） |

- 模型数字：toycell 复算。`check_numbers` 脚本第 2–3 期写，写好之前由事实核查手工复算。
- 汇总到 `reviews/feynman.md` 和 `reviews/factcheck.md`，开头写明各 agent 的版本号。按严重度修订；改了讲法重跑两个新生，改了事实重跑事实核查。
- 更新两本账：`docs/concepts.yml`、`docs/promises.md`。

### 👤 关卡 1：脚本 + 分镜

给你三样：`script.md`、`storyboard.md`、一页审核摘要（各审核的结论、改了什么、没改的理由、新生在揭晓前猜了什么）。按意见修订，直到 `facts.md` 全部 ✅。

## 3. 配音（规范：`docs/voice.md`）

- 按 `## 节` 拆段，用 gemini-voice-mcp `synthesize_speech`（voice `Charon`、固定风格提示、`zh-CN`）逐段合成 → `audio/sec1..N.wav`。
  - 单次上限 2000 字符，长节分两半合成后加 0.6 s 静音拼接。
  - 工具结果过大会存进 tool-results 文件：用 `jq -r '.[1].text' 文件 | jq -r .data | base64 -d` 解出 WAV。
- faster-whisper 转写逐段比对原稿，查读音。**疑似误读要把片段单独切出来再转写**，排除语境偏差（第 1 期英文 sec4 "cell" 被读成 "sale"，重合成后解决）。
- 只把比对后仍然可疑的片段交给你听。音色整体由关卡 2 的成片把关。

## 4. 卡点

```bash
~/.venvs/media/bin/python video/make_cues.py zh     # → audio/vo_final.wav + cues.zh.json
```
- 在 `make_cues.py` 的 `PAUSES` 里加"让观众先猜"的停顿（2 秒）。
- 打印每节句子起点占比（见第 1 期做法），把 `frame.html` 里的节拍阈值对到句子起点上。

## 5. 画面（规范：`docs/directing.md`）

- 第 2、3 期仍复制上一期的 `video/`（`frame.html`、`render.py`、`make_data.py`、`make_cues.py`）；第 3 期做完后把三期里重复的部分抽到 `design/`，之后各期只写本期特有的场景。
- 模型数值一律由 `make_data.py` 从 toycell 生成 `data.js`；需要和旁白对拍时只调**播放速度**，不改数据。
- 画面文字全部放 `i18n/zh.json`、`i18n/en.json`，代码里不写死文字。
- 关键帧联系表（解释器用仓库根目录 `.venv-render`）：
  ```bash
  ../../.venv-render/bin/python video/render.py sheet reviews/contact_vN.png t1 t2 ...
  ```
- 画面审核（`docs/directing.md` 第 8 节）：
  - 检查脚本：溢出、静止帧、数字（第 2–3 期写；写好之前按第 9 节避坑清单逐条自查）；
  - `silent-viewer`：只给联系表，不给脚本；
  - `fact-checker` 第二遍：只给联系表，查画面本身有没有说错科学。
- 联系表不再单独找你确认；审核发现拿不准的画面问题才问。

## 6. 成片

```bash
../../.venv-render/bin/python video/render.py video out/epNNN-zh-vN.mp4 30   # 约 6 分钟成片需 10–15 分钟
```
- 抽帧检查 + `volumedetect` 音量 + `silencedetect` 确认停顿。

## 7. 英文版（和中文版同一周做，同步发布）

1. **改写**：`script.en.md`，按意思改写而非直译，但**逐行与中文对应**（每节行数相同），画面节拍靠它对齐。用词以 `docs/concepts.yml` 的 `en` 为准。在内部备注里记下和中文有意不同的地方。
2. **审核**：`en-freshman-native`、`en-freshman-nonnative`（只给英文脚本）+ `fidelity-reviewer`（对照中文定稿、facts、概念账、欠账表）。修订后重跑两个新生。英文多许或少许的愿记入 `docs/promises.md`。
3. **画面文字**：`i18n/en.json`。西文专用版式改动一律用 `CJK()` 判断，保证中文画面逐像素不变（抽帧/封面 `cmp` 核对）。
4. **配音**：音频放 `audio/en/`，做法同第 3 步。
5. **卡点**：`~/.venvs/media/bin/python video/make_cues.py en`。停顿句在 `PAUSES` 里按英文切句后的那一句写。
6. **节拍**：不重调阈值。`render.py` 按逐行锚点把英文时间映射到中文节拍；行内的关键句在 `SENT_ANCHORS` 里成对登记（如 压力没了 ↔ Now that nothing holds it back）。
7. 联系表 → 成片 `render.py video out/epNNN-en-vN.mp4 --lang en 30` → 封面 `render.py cover out/en --lang en`。

### 👤 关卡 2：中英成片

两条成片一起给你看。通过后更新 `meta.yml` 状态。

## 8. 发布

写 `publish.md`：两个平台的标题、简介、章节时间、标签、设置。标题里必须有"虚拟细胞 / Virtual Cell"。

### 👤 关卡 3：你在聊天里明确说"发布"

没有这句话不上传、不公开。先传为私享 / 仅自己可见，你确认后再公开。

发布后：`publish.md` 的发布记录填链接和日期；`README.md` 的"已发布"表加一行；`meta.yml` 填 `status: published`、`published: YYYY-MM-DD` 和 `release` 链接。**`published` 是复盘任务认定"已发布"的依据，一定要填。**

## 9. 发布后

- **第 14 天复盘**：定时任务"复盘检查"每周一找出发布满 14 天、还没有 `retro.md` 的期并提醒。你从 B 站创作中心和 YouTube Studio 导出或截图留存曲线、平均观看时长、点击率，连同评论一起给我，写成该期 `retro.md`：
  - 观众在哪里走的（对到脚本的哪一句、哪个节拍）；
  - 评论里的疑问和纠错（纠错按 `README.md` 的流程处理，必要时出修订版）；
  - 对规范的修改建议（改 `docs/directing.md`、`episodes/README.md` 还是审核提示词），你点头后再改。
- **文献雷达**：定时任务每周六把新候选追加到 `docs/frontier-pool.md` 的"待筛选"。入池要过那里的三条标准，由人筛。

## 节奏

- 手里常备 2–3 期已定稿的存货，在第 1 圈内攒出来。
- 第 1 圈内找 2–3 个真的大一新生看一期，记下他们的复述和卡点，和模拟新生的结果对比，校准审核提示词。
- 每圈结束停更 1–2 周：抽共享组件、做复盘、清欠账。
