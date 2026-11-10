#!/usr/bin/env python3
"""前置闭合检查：每一期用到的概念，必须在更早的期数讲过，或者本期当场讲。

读 docs/concepts.yml、各期 episodes/*/meta.yml、docs/frontier-pool.md，检查：

  1. concepts.yml 自身：id 不重复；kind 合法；introduced 是期号、0（高中常识）或 null。
  2. 每期 meta.yml 的 introduces：概念存在，且 concepts.yml 里 introduced 就是这一期（两边对得上）。
  3. 每期 meta.yml 的 uses：概念存在，且在更早的期数引入过（只"点过名"的不算）。
  4. 每期新增的正式术语（kind: term）不超过 3 个。
  5. frontier-pool.md 里每条候选的 needs：概念存在；报告已解锁 / 还缺什么。

写新一期之前，先查打算用的概念是否闭合：

  python tools/check_prereq.py --plan 2 --uses cell-state,push,hold-back,balance

依赖 PyYAML（pip install pyyaml）。有错误时退出码为 1。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("需要 PyYAML：pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
KINDS = {"term", "everyday", "school"}
MAX_NEW_TERMS = 3


def load_concepts(path: Path, errors: list[str]) -> dict[str, dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for c in data.get("concepts", []):
        cid = c.get("id")
        if not cid:
            errors.append(f"concepts.yml：有一条没有 id：{c}")
            continue
        if cid in out:
            errors.append(f"concepts.yml：id 重复：{cid}")
        if c.get("kind") not in KINDS:
            errors.append(f"concepts.yml：{cid} 的 kind 不合法：{c.get('kind')}")
        intro = c.get("introduced")
        if intro is not None and not (isinstance(intro, int) and intro >= 0):
            errors.append(f"concepts.yml：{cid} 的 introduced 应为期号、0 或 null：{intro!r}")
        if c.get("kind") == "school" and intro != 0:
            errors.append(f"concepts.yml：{cid} 是高中常识，introduced 应为 0")
        out[cid] = c
    return out


def load_episodes(errors: list[str]) -> dict[int, dict]:
    eps: dict[int, dict] = {}
    for meta in sorted((ROOT / "episodes").glob("ep*/meta.yml")):
        m = yaml.safe_load(meta.read_text(encoding="utf-8")) or {}
        n = m.get("episode")
        if not isinstance(n, int):
            errors.append(f"{meta.relative_to(ROOT)}：缺 episode 期号")
            continue
        m["_path"] = str(meta.relative_to(ROOT))
        eps[n] = m
    return eps


def available_before(concepts: dict[str, dict], n: int) -> set[str]:
    return {cid for cid, c in concepts.items()
            if isinstance(c.get("introduced"), int) and c["introduced"] < n}


def why_missing(concepts: dict[str, dict], cid: str, n: int) -> str:
    c = concepts.get(cid)
    if c is None:
        return f"{cid}（concepts.yml 里没有）"
    intro = c.get("introduced")
    if intro is None:
        hint = f"计划 {c['planned']}" if c.get("planned") is not None else "没排期"
        if c.get("mentioned"):
            hint += f"；第 {c['mentioned']} 期只点过名"
        return f"{cid}（还没讲，{hint}）"
    return f"{cid}（第 {intro} 期才讲）"


def check_episodes(concepts: dict[str, dict], eps: dict[int, dict], errors: list[str]) -> None:
    for n, m in sorted(eps.items()):
        where = m["_path"]
        introduces = m.get("introduces")
        uses = m.get("uses")
        if introduces is None or uses is None:
            errors.append(f"{where}：缺 introduces / uses 字段")
            continue
        for cid in introduces:
            c = concepts.get(cid)
            if c is None:
                errors.append(f"{where}：introduces 里的 {cid} 不在 concepts.yml")
            elif c.get("introduced") != n:
                errors.append(f"{where}：introduces 写了 {cid}，但 concepts.yml 里它的 introduced 是 {c.get('introduced')!r}")
        for cid, c in concepts.items():
            if c.get("introduced") == n and cid not in introduces:
                errors.append(f"{where}：concepts.yml 说 {cid} 在第 {n} 期引入，但本期 introduces 里没有")
        ok = available_before(concepts, n) | set(introduces)
        for cid in uses:
            if cid not in ok:
                errors.append(f"{where}：前置不闭合：{why_missing(concepts, cid, n)}")
        new_terms = [cid for cid in introduces if concepts.get(cid, {}).get("kind") == "term"]
        if len(new_terms) > MAX_NEW_TERMS:
            errors.append(f"{where}：新术语 {len(new_terms)} 个（{', '.join(new_terms)}），超过 {MAX_NEW_TERMS} 个，该拆期了")


def check_frontier(concepts: dict[str, dict], latest: int, errors: list[str]) -> list[str]:
    path = ROOT / "docs" / "frontier-pool.md"
    lines: list[str] = []
    if not path.exists():
        return lines
    title = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith("### "):
            title = raw[4:].strip()
        m = re.match(r"\s*-\s*needs[：:]\s*\[(.*)\]", raw)
        if m and title and not title.startswith("标题"):
            needs = [x.strip() for x in m.group(1).split(",") if x.strip()]
            for cid in needs:
                if cid not in concepts:
                    errors.append(f"frontier-pool.md：「{title}」的 needs 里 {cid} 不在 concepts.yml")
            have = available_before(concepts, latest + 1)
            missing = [why_missing(concepts, cid, latest + 1) for cid in needs if cid in concepts and cid not in have]
            lines.append(f"  {'已解锁' if not missing else '未解锁'}：{title}" + (f"\n      还缺：{'；'.join(missing)}" if missing else ""))
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--plan", type=int, help="打算写的期号")
    ap.add_argument("--uses", default="", help="打算用到的概念 id，逗号分隔（配合 --plan）")
    args = ap.parse_args()

    errors: list[str] = []
    concepts = load_concepts(ROOT / "docs" / "concepts.yml", errors)
    eps = load_episodes(errors)
    check_episodes(concepts, eps, errors)
    latest = max(eps) if eps else 0
    frontier = check_frontier(concepts, latest, errors)

    n_done = sum(1 for c in concepts.values() if isinstance(c.get("introduced"), int) and c["introduced"] > 0)
    print(f"概念 {len(concepts)} 个：已讲 {n_done}，高中常识 {sum(c.get('kind') == 'school' for c in concepts.values())}，"
          f"未讲 {sum(c.get('introduced') is None for c in concepts.values())}；已有 {len(eps)} 期（到第 {latest} 期）")
    if frontier:
        print("前沿候选：")
        print("\n".join(frontier))

    if args.plan is not None:
        want = [x.strip() for x in args.uses.split(",") if x.strip()]
        have = available_before(concepts, args.plan)
        missing = [why_missing(concepts, cid, args.plan) for cid in want if cid not in have]
        print(f"第 {args.plan} 期计划用到 {len(want)} 个概念：" + ("全部闭合" if not missing else "以下要在本期当场讲清，或先加铺垫期"))
        for x in missing:
            print(f"  - {x}")

    if errors:
        print(f"\n{len(errors)} 个错误：")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print("前置检查通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
