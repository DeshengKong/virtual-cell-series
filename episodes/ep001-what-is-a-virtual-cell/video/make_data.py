"""由 toycell 模拟生成动画数据（柱子高度必须来自这里，不允许手绘）。

输出 data.js：
  SIM.koB / SIM.koC  —— 从稳态 (1,1,1) 出发敲除 B / C 的轨迹，每 0.05 时间单位一帧
  SIM.settle         —— 从低初值 (0.1,0.1,0.1) 出发、不扰动时"晃几下后停住"的轨迹
"""

import json
import pathlib

from toycell import Perturbation, simulate

HERE = pathlib.Path(__file__).parent
STEP = 5  # dt = 0.01，每 5 步取一帧 → 0.05


def traj(state0, t_end, ko=None):
    ts, tr = simulate(state0, t_end=t_end, perturbation=Perturbation(knockout=set(ko or [])))
    return {"dt": 0.01 * STEP, "x": [[round(float(v), 4) for v in row] for row in tr[::STEP]]}


data = {
    "settle": traj([0.1, 0.1, 0.1], 20),
    "koB": traj([1.0, 1.0, 1.0], 12, ["B"]),
    "koC": traj([1.0, 1.0, 1.0], 12, ["C"]),
}
(HERE / "data.js").write_text("const SIM = " + json.dumps(data) + ";\n", encoding="utf-8")
for k, v in data.items():
    print(k, "frames", len(v["x"]), "end", v["x"][-1])
