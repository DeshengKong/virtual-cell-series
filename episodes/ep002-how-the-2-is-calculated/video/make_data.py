"""由 toycell 生成第 2 期动画数据（柱子高度、表格里的数字都来自这里，不允许手写）。

输出 data.js：
  SIM.koC    从稳态 (1,1,1) 出发关掉 C 的轨迹（1.3、4.10）
  SIM.fill   单根柱子"水龙头一开"：A 从 0 起、C 关掉 → A 的生产恒为 2（3.6）
  SIM.drain  单根柱子"关水龙头"：A 从 2 起、A 关掉 → 只剩分解（3.7 车速表）
  NUM        各张小表里的数，由 toycell 的系数函数算出
  CURVE      两条系数曲线（5.11），0–4 每 0.05 一点
运行（在本期目录下）：../../toycell/.venv/bin/python video/make_data.py
"""

import json
import pathlib

import numpy as np
from toycell import Params, Perturbation, derivatives, predict, simulate
from toycell.model import _activate, _repress

HERE = pathlib.Path(__file__).parent
STEP = 5  # dt = 0.01，每 5 步取一帧 → 0.05
P = Params()


def traj(state0, t_end, ko=()):
    _, tr = simulate(state0, t_end=t_end, perturbation=Perturbation(knockout=set(ko)))
    return {"dt": 0.01 * STEP, "x": [[round(float(v), 4) for v in row] for row in tr[::STEP]]}


rep = lambda c: float(_repress(c, P.k, P.n))
act = lambda a: float(_activate(a, P.k, P.n))
r3 = lambda v: round(v, 3)

vec = lambda d: np.array([d[g] for g in "ABC"]) if isinstance(d, dict) else np.asarray(d)
koC = vec(predict([1, 1, 1], Perturbation(knockout={"C"})))
koB = vec(predict([1, 1, 1], Perturbation(knockout={"B"})))
rest = vec(predict([0.1] * 3))
assert np.allclose(rest, 1, atol=1e-3) and np.allclose(derivatives(np.ones(3), P), 0, atol=1e-9)
assert np.allclose(koC, [2, 1.6, 0], atol=1e-3) and np.allclose(koB, [2, 0, 0], atol=1e-3)

data = {
    "koC": traj([1.0, 1.0, 1.0], 12, ["C"]),
    "fill": traj([0.0, 0.0, 0.0], 6, ["C"]),
    "drain": traj([2.0, 0.0, 0.0], 4, ["A", "B", "C"]),
}
num = {
    "rest": [r3(v) for v in rest],
    "koC": [r3(v) for v in koC],
    "koB": [r3(v) for v in koB],
    "rep": {str(c): r3(rep(c)) for c in (0, 1, 2)},
    "act": {str(a): r3(act(a)) for a in (0, 0.5, 1, 2)},
    "act1": {str(a): r3(a / (1 + a)) for a in (0.5, 2)},        # 只用 A 的对照（不进 toycell）
    "Bfrom": {str(a): r3(P.production["B"] * act(a)) for a in (2, 3, 4, 10)},  # 假设从外面加 A：只代算式
    "start": [r3(v) for v in derivatives(np.zeros(3), P)],     # 思考题答案（本期不显示）
}
assert num["rep"] == {"0": 1.0, "1": 0.5, "2": 0.2}
assert num["act"] == {"0": 0.0, "0.5": 0.2, "1": 0.5, "2": 0.8}
assert num["Bfrom"] == {"2": 1.6, "3": 1.8, "4": 1.882, "10": 1.98}
xs = [round(x, 2) for x in np.arange(0, 4.0001, 0.05)]
curve = {"x": xs, "rep": [r3(rep(x)) for x in xs], "act": [r3(act(x)) for x in xs]}
(HERE / "data.js").write_text(
    "const SIM = " + json.dumps(data) + ";\nconst NUM = " + json.dumps(num) + ";\nconst CURVE = " + json.dumps(curve) + ";\n",
    encoding="utf-8")
for k, v in data.items():
    print(k, "frames", len(v["x"]), "end", v["x"][-1])
print(json.dumps(num, ensure_ascii=False))
