# 虚拟细胞：从零到前沿

一套视频课程，从零讲到前沿，目标是让大一新生也能真正弄懂"虚拟细胞"。每期只回答一个问题，时长不卡死（第 1 期中文约 6 分钟），讲明白优先。
**每周更新，计划持续 3 年；中文版发 B 站，英文版发 YouTube，同步更新。** 每期的脚本、事实出处、动画代码和可运行的实验都在这个仓库里。

## 一句话讲清虚拟细胞

> **虚拟细胞，就是输入细胞的状态和你做的事，预测它会变成什么。**

整个系列都围绕这台"预测机器"的四个问题展开：

| | 问题 | 涉及的内容 |
|---|---|---|
| ① | 细胞的"状态"怎么用数字描述？ | 细胞生物学、测序、单细胞数据 |
| ② | "做了什么"有哪些？ | 药物、关掉基因、信号、扰动实验 |
| ③ | 这个函数从哪里来？ | 按原理推导（机理模型）／从数据学习（AI 模型） |
| ④ | 怎么知道它预测得对？ | 评估、最笨的办法能得几分、没见过的考题、前沿争议 |

课程是螺旋式的：先用下面这个三个基因的玩具细胞把四个问题完整走一圈（第 2–11 期，只用算术），再回到真实细胞一圈一圈加深。大纲见 [docs/curriculum.md](docs/curriculum.md)。

## 玩具细胞

全系列共用一个只有 3 个基因的极简细胞：A 推动 B，B 推动 C，C 反过来压住 A。
同一个细胞会被反复用不同方法观察，你可以亲手运行：

```bash
cd toycell
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/python -c "from toycell import *; print(predict([0.1,0.1,0.1], Perturbation(knockout={'B'})))"
# {'A': 2.0, 'B': 0.0, 'C': 0.0}  —— 关掉 B，C 跟着降到 0，A 没人压着，升到 2（平时是 1）
.venv/bin/python -m pytest -q   # 运行测试
```

## 目录

```
toycell/     玩具细胞 Python 库（全系列共用）；测试锁住了已发布视频里的每个数字
episodes/    每期一个文件夹：中英脚本、事实清单与出处、分镜、动画代码、审核记录
docs/        大纲、概念账（哪一期讲了什么）、欠账表（许过的愿）、导演与审核规范、制作流程
tools/       检查脚本（前置概念是否闭合等）
design/      共享画面组件（第 3 期后从各期代码里抽出来）
.claude/     审核用的 agent 提示词
```

## 已发布

YouTube 播放列表（按顺序看）：https://www.youtube.com/playlist?list=PLW1P6tnKxvAc

| 期 | 标题 | 地图位置 | 视频 |
|---|---|---|---|
| 1 | [什么是虚拟细胞](episodes/ep001-what-is-a-virtual-cell/) / What Is a Virtual Cell? | 序章 | [B 站（中文）](https://www.bilibili.com/video/BV1k3W86SEYT) · [YouTube（English）](https://youtu.be/ANYJK46OmbQ) |
| 2 | [那个"2"是怎么算出来的](episodes/ep002-how-the-2-is-calculated/) / Where Does That "2" Come From? | ③ 机器里的规则 | [B 站（中文）](https://www.bilibili.com/video/BV1PjW36vEHw) · [YouTube（English）](https://youtu.be/HeJvfHhY06s) |

## 纠错与建议

发现讲错了，或者有没讲清楚的地方，请提 [Issue](../../issues/new/choose)。每一条都会被认真处理，必要时出修订版。

每期怎么保证"讲透"和"没说错"：[审核标准](docs/feynman-review.md)、[谁查什么](docs/agents.md)。

## 授权

- 代码（`toycell/`、`design/`、各期渲染代码）：[MIT](LICENSE)
- 讲解内容（脚本、文字、视频画面）：[CC BY-NC 4.0](LICENSE-CONTENT.md)，转载请署名，禁止商用
