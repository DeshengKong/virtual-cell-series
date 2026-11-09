# 虚拟细胞：从零到前沿

一套每期 3–5 分钟的视频课程，从零讲到前沿，目标是让大一新生也能真正弄懂"虚拟细胞"。
**每周更新，计划持续 3 年。** 每期的脚本、动画代码和可运行的实验都在这个仓库里。

## 一句话讲清虚拟细胞

> **细胞现在的状态 + 你对它做了什么 → 它接下来会变成什么**

虚拟细胞就是在电脑里实现这个预测函数。整个系列都围绕四个问题展开：

| | 问题 | 涉及的内容 |
|---|---|---|
| ① | 细胞的"状态"怎么用数字描述？ | 细胞生物学、测序、单细胞数据 |
| ② | "做了什么"有哪些？ | 药物、基因敲除、信号、扰动实验 |
| ③ | 这个函数从哪里来？ | 按原理推导（机理模型）／从数据学习（AI 模型） |
| ④ | 怎么知道它预测得对？ | 评估、基线、因果、前沿争议 |

## 玩具细胞

全系列共用一个只有 3 个基因的极简细胞：A 激活 B，B 激活 C，C 反过来抑制 A。
同一个细胞会被反复用不同方法观察，你可以亲手运行：

```bash
cd toycell
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/python -c "from toycell import *; print(predict([0.1,0.1,0.1], Perturbation(knockout={'B'})))"
# {'A': 2.0, 'B': 0.0, 'C': 0.0}  —— 敲掉 B，C 熄火，A 失去抑制而升高
.venv/bin/python -m pytest -q   # 运行测试
```

## 目录

```
toycell/     玩具细胞 Python 库（全系列共用）
design/      共享的画面组件、配色、四问题地图、片头片尾
episodes/    每期一个文件夹：脚本、事实清单与参考文献、动画代码、notebook
docs/        课程大纲、前置知识关系、写作规范
```

## 已发布

| 期 | 标题 | 地图位置 | 视频 |
|---|---|---|---|
| 1 | [什么是虚拟细胞](episodes/ep001-what-is-a-virtual-cell/) / What Is a Virtual Cell? | 序章 | [B 站（中文）](https://www.bilibili.com/video/BV1k3W86SEYT) · [YouTube（English）](https://youtu.be/ANYJK46OmbQ) |

## 纠错与建议

发现讲错了，或者有没讲清楚的地方，请提 [Issue](../../issues/new/choose)。每一条都会被认真处理，必要时出修订版。

## 授权

- 代码（`toycell/`、`design/`、各期渲染代码）：[MIT](LICENSE)
- 讲解内容（脚本、文字、视频画面）：[CC BY-NC 4.0](LICENSE-CONTENT.md)，转载请署名，禁止商用
