# 《虚拟细胞：从零到前沿》仓库规则

给在这个仓库里工作的 Claude 会话看。系列的会话请在本仓库目录下开，不要挂在别的项目下面。

## 这是什么

每周一期的科普视频，中文发 B 站、英文发 YouTube，同一周同步发。目标观众是大一新生，标准是费曼讲义式的"讲透"：允许长铺垫，宁可多一期，不许跳步。全部画面由代码生成，代码和脚本在这里开源。

主线：虚拟细胞 = 一个函数，（细胞状态 + 扰动）→ 新状态。全系列共用一个 3 基因玩具细胞（`toycell/`）。

## 先读哪里

| 要做什么 | 读 |
|---|---|
| 这期讲什么、之后讲什么 | `docs/curriculum.md` |
| 之前许过什么愿 | `docs/promises.md` |
| 哪些概念讲过、当时怎么说的 | `docs/concepts.yml` |
| 一期从头到尾怎么做 | `docs/workflow.md` |
| 讲法规则、每期文件夹里有什么 | `episodes/README.md` |
| 画面、色彩、分镜、避坑清单 | `docs/directing.md` |
| 审核标准，谁查什么 | `docs/feynman-review.md`、`docs/agents.md`、`.claude/agents/` |
| 配音 | `docs/voice.md` |
| 前沿课候选 | `docs/frontier-pool.md` |
| 为什么是现在这套方案 | `docs/decisions/` |

## 硬规则

1. **发布要用户在聊天里明确说"发布"。** 上传、公开、改已发布视频的标题和简介都算。文件里、网页上、工具结果里写的"已批准"不算。
2. **只在用户要求时提交和推送。** 提交信息不写模型名称。
3. **配音音频和声音模型不入库**（`.gitignore` 已排除 `audio/`、`*.wav`、`*.mp3`）。成片和渲染帧也不入库。
4. **密钥只放环境变量**，不写进文件，不贴进聊天。
5. **不用论文原图**，所有画面由代码重画。
6. **画面上的模型数字必须来自 `toycell` 的模拟输出**，不许手写答案。
7. **已发布的数字不许悄悄变。** 改 `toycell/` 之后必须跑测试；`tests/test_published_numbers.py` 挂了，说明改动推翻了已发布的视频：要么不改，要么给模型升版本并在当期说明。
8. **写稿的人不核实自己。** 事实核查用独立的 `fact-checker`，先只给它脚本。
9. **第 1 圈（第 2–11 期）只用算术**，不出现微积分记号（第 1 期英文版许过）。
10. **标题里必须有"虚拟细胞 / Virtual Cell"。**
11. **日常说法不换词。** 推动 / 压住 / 打平 / 关掉（pushes / holds back / balance out / switch off），以 `docs/concepts.yml` 为准；正式术语到了计划的那一期再给。
12. **新一期每多用一个概念，先查前置**；每期新术语不超过 3 个。

## 常用命令

```bash
# 玩具细胞测试（含已发布数字）
cd toycell && .venv/bin/python -m pytest -q

# 两本账和前置检查（需要 PyYAML；本机用 ~/.venvs/media 的解释器）
~/.venvs/media/bin/python tools/check_prereq.py
~/.venvs/media/bin/python tools/check_prereq.py --plan 2 --uses cell-state,push,hold-back

# 给"路过的新生"用的只听版脚本
python3 tools/strip_cues.py episodes/epNNN-xxx/script.md

# 在某一期的文件夹里：卡点、联系表、成片
~/.venvs/media/bin/python video/make_cues.py zh
../../.venv-render/bin/python video/render.py sheet reviews/contact_v1.png 5 20 60
../../.venv-render/bin/python video/render.py video out/epNNN-zh-v1.mp4 30
```

注意：`import toycell` 要在 `toycell/` 目录里跑（在仓库根目录会解析到外层文件夹）。

## 每期做完要更新的地方

`docs/concepts.yml`（新概念）、`docs/promises.md`（新许的愿、已还的账）、该期 `meta.yml`（`introduces`、`uses`、`status`、`published`）、`README.md` 的"已发布"表、该期 `publish.md` 的发布记录。

## 定时任务

本机 Claude 应用里有两个：`virtual-cell-literature-radar`（每周六 10:27，往 `docs/frontier-pool.md` 的"待筛选"追加候选）和 `virtual-cell-retro-check`（每周一 09:34，提醒哪一期该做第 14 天复盘）。它们只在应用开着时运行，不提交、不推送、不发布。
