from toycell import Perturbation, predict


def test_unperturbed_reaches_positive_steady_state():
    out = predict([0.1, 0.1, 0.1])
    assert all(v > 0 for v in out.values())


def test_knockout_B_silences_C_and_releases_A():
    base = predict([0.1, 0.1, 0.1])
    ko = predict([0.1, 0.1, 0.1], Perturbation(knockout={"B"}))
    assert ko["B"] < 1e-3
    assert ko["C"] < 1e-3  # B 没了，C 失去激活
    assert ko["A"] > base["A"]  # C 没了，A 不再被抑制


def test_drug_scales_target_down():
    base = predict([0.1, 0.1, 0.1])
    drug = predict([0.1, 0.1, 0.1], Perturbation(scale={"A": 0.5}))
    assert drug["A"] < base["A"]
