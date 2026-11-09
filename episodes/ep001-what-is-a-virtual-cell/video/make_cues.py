"""逐字卡点：faster-whisper 逐字时间 → 句子起止 → 拼接带停顿的成片配音 + cues.<lang>.json。

用法（在 episodes/ep001-.../ 下，用 ~/.venvs/media 的 python）：
  python video/make_cues.py [zh]

停顿规则：
  - 各节之间留 GAP 秒
  - PAUSES 里列出的句子说完后，额外静音若干秒（让观众先猜）
输出：
  audio/vo_final.wav    拼好的成片配音（不入库）
  cues.zh.json          {"sections": [[起, 止], ...], "subs": [[起, 止, 句子], ...]}
"""

import difflib
import json
import pathlib
import re
import sys
import wave

from faster_whisper import WhisperModel

EP = pathlib.Path(__file__).resolve().parent.parent
LANG = sys.argv[1] if len(sys.argv) > 1 else "zh"
GAP = 0.8
PAUSES = {"你先猜一下：我们没有碰 A，A 会怎么样？": 2.0}
SR = 24000


def sections_text():
    text = (EP / "script.md").read_text(encoding="utf-8").split("## 内部备注")[0]
    out = []
    for sec in re.split(r"\n## ", text)[1:]:
        body = "\n".join(l for l in sec.split("\n")[1:] if not l.startswith((">", "---")))
        body = re.sub(r"〔.*?〕", "", body).replace("**", "")
        out.append([s.strip() for s in re.split(r"(?<=[。？！；])|\n", body) if s and s.strip()])
    return out


norm = lambda s: re.sub(r"[^\w]", "", s).lower()


def align(sents, words):
    """把脚本句子映射到 whisper 逐字时间：先建立字符级对应，再取每句首末字符的时间。"""
    ref = "".join(norm(s) for s in sents)
    hyp_chars, hyp_t = [], []
    for w in words:
        cs = norm(w.word)
        for k, c in enumerate(cs):
            hyp_chars.append(c)
            frac = k / max(len(cs), 1)
            hyp_t.append((w.start + (w.end - w.start) * frac, w.start + (w.end - w.start) * (k + 1) / max(len(cs), 1)))
    sm = difflib.SequenceMatcher(None, ref, "".join(hyp_chars), autojunk=False)
    m = {}
    for a, b, n in sm.get_matching_blocks():
        for i in range(n):
            m[a + i] = b + i
    res, pos = [], 0
    for s in sents:
        L = len(norm(s))
        idx = [m[i] for i in range(pos, pos + L) if i in m]
        res.append((hyp_t[idx[0]][0], hyp_t[idx[-1]][1]) if idx else None)
        pos += L
    # 缺失的句子用前后插值补
    for i, r in enumerate(res):
        if r is None:
            prev = res[i - 1][1] if i and res[i - 1] else 0.0
            nxt = next((x[0] for x in res[i + 1 :] if x), prev + 1.0)
            res[i] = (prev, nxt)
    return res


def read_pcm(p):
    with wave.open(str(p)) as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        return w.readframes(w.getnframes())


def main():
    model = WhisperModel("medium", compute_type="int8")
    secs = sections_text()
    pcm_out, subs, bounds, t0 = b"", [], [], 0.0
    silence = lambda s: b"\x00\x00" * int(round(s * SR))
    for i, sents in enumerate(secs, 1):
        f = EP / "audio" / f"sec{i}.wav"
        pcm = read_pcm(f)
        segs, _ = model.transcribe(str(f), language=LANG, word_timestamps=True)
        words = [w for s in segs for w in s.words]
        times = align(sents, words)
        # 按停顿切开音频并插入静音
        sec_start, shift, cursor = t0, 0.0, 0
        for s, (a, b) in zip(sents, times):
            subs.append([round(sec_start + a + shift, 3), round(sec_start + b + shift, 3), s.rstrip("。；")])
            if s in PAUSES:
                cut = int(round(b * SR)) * 2
                pcm_out += pcm[cursor:cut] + silence(PAUSES[s])
                cursor = cut
                shift += PAUSES[s]
        pcm_out += pcm[cursor:]
        dur = len(pcm) / 2 / SR + shift
        bounds.append([round(sec_start, 3), round(sec_start + dur, 3)])
        pcm_out += silence(GAP)
        t0 = sec_start + dur + GAP
        print(f"sec{i}: {dur:.1f}s, {len(sents)} 句")
    # 字幕：一句一换，句间停顿不显示；末尾延长到下一句开始前 0.15 s 以内
    for a, b in zip(subs, subs[1:]):
        a[1] = min(max(a[1], a[0] + 0.8), b[0] - 0.05)
    with wave.open(str(EP / "audio" / "vo_final.wav"), "wb") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(SR), w.writeframes(pcm_out)
    (EP / f"cues.{LANG}.json").write_text(json.dumps({"sections": bounds, "subs": subs}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("total", round(len(pcm_out) / 2 / SR, 1), "s")


if __name__ == "__main__":
    main()
