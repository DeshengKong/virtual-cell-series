# 第 1 期事实清单（对应脚本 v0.4）

每一条片中事实性说法及出处。状态：✅ 已核实 / ⏳ 待核实。全部 ✅ 后脚本才能定稿。

| # | 片中说法 | 出处 | 状态 |
|---|---|---|---|
| 1 | 今天的虚拟细胞能在特定实验里预测部分变化，但远做不到对任意细胞、任意药物可靠预测 | Ahlmann-Eltze C, Huber W, Anders S. Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines. *Nat Methods* 2025;22(8):1657–1661. [doi:10.1038/s41592-025-02772-6](https://doi.org/10.1038/s41592-025-02772-6)（5 个基础模型 + 2 个深度学习模型均未超过简单基线）；愿景与现状另见 #6 | ✅ PubMed 核对摘要 |
| 2 | 最常用的单细胞测序要先把细胞打碎（裂解） | Chen W, et al. Live-seq enables temporal transcriptomic recording of single cells. *Nature* 2022;608(7924):733–740. [doi:10.1038/s41586-022-05046-9](https://doi.org/10.1038/s41586-022-05046-9)（摘要："scRNA-seq requires lysing cells"） | ✅ PubMed 核对摘要 |
| 3 | 已有不打碎细胞的新方法，但还远不能像拍视频一样连续记录 | 同 #2：Live-seq 用流体力显微镜在保留细胞存活的前提下取样，可对同一细胞做前后测序；属特殊方法，非常规 | ✅ PubMed 核对摘要 |
| 4 | 单细胞测序读到的主要是 RNA，不是蛋白质本身 | scRNA-seq 的测量对象为 RNA（#2 及 Hwang B, et al. *Exp Mol Med* 2018;50(8):1–14. [doi:10.1038/s12276-018-0071-8](https://doi.org/10.1038/s12276-018-0071-8)） | ✅ |
| 5 | 人类有将近两万个能做出蛋白质的基因 | Amaral P, et al. The status of the human gene catalogue. *Nature* 2023;622(7981):41–47. [doi:10.1038/s41586-023-06490-x](https://doi.org/10.1038/s41586-023-06490-x)（"fewer than 20,000"）。审阅者另指 GENCODE v50 为 19,442，与"将近两万"一致，版本号待自查 | ✅ |
| 6 | "AI 虚拟细胞"是领域明确提出的目标方向（片中未点名） | Bunne C, et al. *Cell* 2024;187(25):7045–7063. [doi:10.1016/j.cell.2024.11.015](https://doi.org/10.1016/j.cell.2024.11.015) | ✅ |
| 7 | 医生会参考临床试验，有时还看基因检测选药 | U.S. FDA. [Table of Pharmacogenomic Biomarkers in Drug Labeling](https://www.fda.gov/drugs/science-and-research-drugs/table-pharmacogenomic-biomarkers-drug-labeling)（列出说明书中含药物基因组学信息的已批准药物，部分附有据生物标志物采取的具体用药措施） | ✅ 官方页面核对 |
| 8 | 天气预报有成熟的物理方程做基础，但细节（云、对流等）仍要近似处理 | ECMWF. [Atmospheric physics](https://www.ecmwf.int/en/research/modelling-and-prediction/atmospheric-physics)（辐射、云、对流、湍流等次网格过程以参数化表示）；[OpenIFS: Physical Processes](https://confluence.ecmwf.int/display/OIFS/3.2+OpenIFS:+Physical+Processes) | ✅ 官方页面核对 |
| 9 | 玩具细胞的全部数字（1/1/1；敲除 B → 2/0/0；敲除 C → 2/1.6/0；"一半马力"） | 本仓库 `toycell`，方程见 script.md 内部备注；费曼审核与用户审阅两次独立复算一致 | ✅ |

## 已删去的说法

- "成年人约 37 万亿个细胞"（v0.1）：与"预测一个细胞"无关。
- "我们没法拿天气做实验"（v0.3）：不准确，存在人工影响天气（如云催化）实验。改为"天气预报主要预测自然变化"。
- "显微镜可盯着活细胞看几天但只能看少数分子"（v0.3）：为控时长删去。
