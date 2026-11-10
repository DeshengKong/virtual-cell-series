# 第 2 期英文版审核记录

agent 版本：fidelity-reviewer v1、en-freshman-native v1、en-freshman-nonnative v1（2026-11-09）。
两个英文新生的 brief 写的是 `model: sonnet`；本会话 cwd 不在仓库内，按惯例用 general-purpose agent 读 brief 执行（继承主模型）。

## 第一轮（script.en.md v0.1）

### 忠实度（fidelity-reviewer）
结论：无大的科学错误；一处必须改。

| # | 问题 | 处理 |
|---|---|---|
| 1 | 加药句 "only reaches half of what it used to"：reaches 在全片指柱子高度，会听成 A 柱减半，等于提前给出第 4 期的错答案（实际约 0.72） | 改为 "Suppose a drug cuts A's full power in half."（概念账 full-power 的规定说法） |
| 2 | "a little short of 2" 太轻（A=2 时差 0.4） | "always stays below 2" |
| 3 | "the more there is, the faster" 弱于中文"成正比" | "twice as much means twice as fast" |
| 4 | lac 句 "controls when a gene gets to work" | "controls how hard a gene works" |
| 5 | 浴缸失效处 "come one at a time" 会听成进来的节奏 | "separate pieces you could count one by one" |
| 6 | 引用第 1 期 "running at half power"，第 1 期英文旁白没说过 | 改引第 1 期原话 "cuts A's production in half"，"half power" 只作画面标签 |
| 8 | 画面标签 "making" 与旁白 "production" 不一致 | 标签改 "production" |
| 10 | "set by the bar's own height" 与来源标签 "set by us" 撞词 | "depends on" |
| 11 | lac "switches this gene on" 与"不是真的开关"、思考题 "switched on" 撞词 | "gets this gene going" |
| 12 | concepts.yml 缺 hold-back factor / push factor 的英文 | 已补 `en_terms` |

行对应：每节行数一致，逐行内容对应。

### 新生（母语 / 非母语）
- 揭晓前的猜测：两人都在 "A 要多大" 处先猜 A = 3–5，读到 1.8 → 1.88 → 1.98 才明白"永远到不了"。思考题两人都答对（只有 A 在涨）。
- 共同卡点：思考题 "switched on" 与 "switch off a gene" 混淆（已改 "a brand-new toy cell, just starting up"）；"1 unit per unit of time" 拗口；"Say a drug means…" 难解析；"the new state…" 长句；参数清单句主语丢失。
- 非母语另列：in turn、of all numbers、falls short、taken apart（分解的第三个叫法）、smooths over、plug in、worthwhile、creeping up、sudden click、hassle、straight down the line、comes back round、hooked up、running along，均已换成平实说法；"perturbation" 首次出现加了同位解释。
- 母语另提、未改（与中文定稿一致，记入下期）：
  - "C 真的能降到正好 0 吗？分解随高度变慢，C 也只是越来越接近 0。" → 第 3 期正面回答（随时间的接近 vs 算式上限），已写入 script.en.md 内部备注。
  - 饱和溶液的"共同点"一句：盐是到顶就停，"越往后越不起作用"不太像。中文定稿已过费曼审核，暂不改；如关卡 2 你觉得别扭，中英一起改。
  - "A 要多大" 的问法预设了答案存在：有意为之，与中文一致。

## 第二轮（v0.2）
两人确认第一轮问题基本修复；思考题读来清楚。新指出：keeps pace（习语）、that number 无所指、is up to the driver、top speed（第四个叫法）、两个冒号连用、句后半重复。全部按建议改为 v0.3。

## 配音核对（faster-whisper）
- 中文：差异几乎全是同音字和数字写法。**"A 是 0.5 时""A 是 2 时"的"时"和"十"同音**，转写成 0.50、20，听众也可能听成"二十"。中文脚本改为"的时候"，第五节后半重配。
- 英文：两处疑似漏读（"staying flat at the top"、"When Episode 1 said"）单独切片逐词转写后确认读了，是转写语境误差。
