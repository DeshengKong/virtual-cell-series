"""玩具细胞：一个只有 3 个基因的极简细胞，全系列共用。

基因关系（环路 + 负反馈）：
    A ──激活──▶ B ──激活──▶ C
    ▲                        │
    └────────抑制────────────┘

虚拟细胞的本质就是一个函数：
    predict(细胞状态, 扰动) -> 新的细胞状态
本模块用"按原理写方程"（机理模型）的方式实现这个函数。
后面的期数会用数据驱动的模型去学习它，再比较两者。
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

GENES = ("A", "B", "C")


@dataclass
class Params:
    """每个基因：最大生产速率 production、降解速率 decay。
    k 是激活/抑制的"半效浓度"，n 是开关的陡峭程度（Hill 系数）。"""

    production: dict = field(default_factory=lambda: {"A": 2.0, "B": 2.0, "C": 2.0})
    decay: dict = field(default_factory=lambda: {"A": 1.0, "B": 1.0, "C": 1.0})
    k: float = 1.0
    n: float = 2.0


@dataclass
class Perturbation:
    """对细胞"做了什么"。

    knockout: 被敲除的基因（生产速率变为 0），例如 {"B"}
    scale:    按比例改变某基因生产速率（模拟药物），例如 {"A": 0.5}
    """

    knockout: set = field(default_factory=set)
    scale: dict = field(default_factory=dict)


def _activate(x, k, n):
    return x**n / (k**n + x**n)


def _repress(x, k, n):
    return k**n / (k**n + x**n)


def derivatives(state: np.ndarray, p: Params, pert: Perturbation | None = None) -> np.ndarray:
    """每个基因的变化速度 = 生产 − 降解。"""
    pert = pert or Perturbation()
    a, b, c = state
    drive = {
        "A": _repress(c, p.k, p.n),  # C 抑制 A
        "B": _activate(a, p.k, p.n),  # A 激活 B
        "C": _activate(b, p.k, p.n),  # B 激活 C
    }
    out = []
    for g, x in zip(GENES, state):
        prod = p.production[g] * pert.scale.get(g, 1.0)
        if g in pert.knockout:
            prod = 0.0
        out.append(prod * drive[g] - p.decay[g] * x)
    return np.array(out)


def simulate(
    state0,
    t_end: float = 20.0,
    dt: float = 0.01,
    params: Params | None = None,
    perturbation: Perturbation | None = None,
):
    """用四阶 Runge-Kutta 积分。返回 (时间数组, 状态轨迹[时间, 基因])。"""
    p = params or Params()
    x = np.asarray(state0, dtype=float)
    steps = int(round(t_end / dt))
    ts = np.linspace(0.0, steps * dt, steps + 1)
    traj = np.empty((steps + 1, 3))
    traj[0] = x
    f = lambda s: derivatives(s, p, perturbation)
    for i in range(steps):
        k1 = f(x)
        k2 = f(x + dt / 2 * k1)
        k3 = f(x + dt / 2 * k2)
        k4 = f(x + dt * k3)
        x = np.maximum(x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4), 0.0)
        traj[i + 1] = x
    return ts, traj


def predict(state, perturbation: Perturbation | None = None, params: Params | None = None, t_end: float = 50.0):
    """虚拟细胞的核心函数：给定当前状态和扰动，返回细胞最终会稳定到的状态。"""
    _, traj = simulate(state, t_end=t_end, params=params, perturbation=perturbation)
    return {g: float(v) for g, v in zip(GENES, traj[-1].round(4))}
