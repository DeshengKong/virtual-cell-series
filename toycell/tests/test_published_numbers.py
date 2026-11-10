"""已发布数字测试：视频里说出去的数字，模型以后怎么改都不许悄悄推翻。

每个测试对应一期已发布（或大纲里已写明）的说法，注释里写了出处。
如果确实要改模型导致这里失败，正确做法是：出修订期、在 docs/promises.md 记一笔，
而不是改这里的数字。
"""

import numpy as np
import pytest

from toycell import Params, Perturbation, derivatives, predict, simulate

REST = [1.0, 1.0, 1.0]
LOW = [0.1, 0.1, 0.1]
TOL = 1e-3  # 画面上最多显示两位小数


def close(got: dict, want: dict):
    for g, v in want.items():
        assert got[g] == pytest.approx(v, abs=TOL), f"{g}: 得到 {got[g]}，已发布的是 {v}"


# ---- 第 1 期（2026-11-09 发布） ----


def test_ep001_rest_state_is_1_1_1():
    # "三根柱子会停在一个固定的高度，我们把这个高度记作 1"
    close(predict(LOW), {"A": 1.0, "B": 1.0, "C": 1.0})
    close(predict(REST), {"A": 1.0, "B": 1.0, "C": 1.0})


def test_ep001_knockout_B_gives_2_0_0():
    # "没碰 A，A 却翻倍了"
    close(predict(REST, Perturbation(knockout={"B"})), {"A": 2.0, "B": 0.0, "C": 0.0})
    close(predict(LOW, Perturbation(knockout={"B"})), {"A": 2.0, "B": 0.0, "C": 0.0})


def test_ep001_knockout_C_gives_2_1p6_0():
    # 思考题答案（第 2 期开头揭晓）："B 会不会也正好升到 2？"——不会，只到 1.6
    close(predict(REST, Perturbation(knockout={"C"})), {"A": 2.0, "B": 1.6, "C": 0.0})


def test_ep001_C_at_normal_level_halves_A_production():
    # "C 在正常水平时，把 A 的生产压掉一半"；"压力没了，A 开足马力"
    p = Params()
    held = derivatives(np.array([0.0, 0.0, 1.0]), p)[0]  # A=0 时变化速度 = 生产速度
    free = derivatives(np.array([0.0, 0.0, 0.0]), p)[0]
    assert free == pytest.approx(2.0, abs=1e-9)
    assert held == pytest.approx(free / 2, abs=1e-9)


def test_ep001_knockout_B_order_and_no_overshoot():
    # 画面：B 先降，C 随后降，A 最后升；A 单调升到 2，不冲过头
    ts, tr = simulate(REST, t_end=20.0, perturbation=Perturbation(knockout={"B"}))
    t_b = ts[np.argmax(tr[:, 1] < 0.5)]
    t_c = ts[np.argmax(tr[:, 2] < 0.5)]
    t_a = ts[np.argmax(tr[:, 0] > 1.5)]
    assert t_b < t_c < t_a
    assert np.all(np.diff(tr[:, 0]) >= -1e-9)
    assert tr[:, 0].max() <= 2.0 + 1e-6


# ---- 大纲里已写明、将在第 1 圈用到的数字 ----


def test_outline_drug_halving_A_production_leaves_A_near_0p72():
    # 大纲第 4 期"反馈"：A 的生产 ×0.5，A 只降到约 0.72，而不是 0.5
    out = predict(REST, Perturbation(scale={"A": 0.5}))
    assert out["A"] == pytest.approx(0.716, abs=5e-3)
    assert out["A"] > 0.5
