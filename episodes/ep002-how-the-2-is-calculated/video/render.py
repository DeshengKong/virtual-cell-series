"""逐帧渲染：renderFrame(t) 任意时刻可单独出图。

用法（在 episodes/ep002-.../ 下运行，解释器用仓库根目录的 .venv-render）：
  python video/render.py stills reviews/stills [--lang zh] t1 t2 ...
  python video/render.py sheet  reviews/contact.png [--lang zh] t1 t2 ...   # 关键帧联系表
  python video/render.py beats  reviews/beats-zh.png [--lang zh]            # 每行旁白开头 +1.2 s 一格
  python video/render.py video  out/ep002-zh.mp4 [--lang zh] [FPS]
  python video/render.py cover  out/zh [--lang zh]

和第 1 期的不同：画面节拍挂在"第几行旁白"上（ANCH），中英各自从 cues.<lang>.json 算出，
不再做英文→中文的时间映射。提示音事件由 frame.html 的 SOUND 给出，这里合成进配音。
"""

import json
import math
import pathlib
import re
import struct
import subprocess
import sys
import tempfile
import wave

from playwright.sync_api import sync_playwright

EP = pathlib.Path(__file__).resolve().parent.parent
SRC = EP / "video" / "frame.html"
SCRIPT = {"zh": ("script.md", "## 内部备注"), "en": ("script.en.md", "## Internal notes")}
SPLIT = {"zh": r"(?<=[。？！；])|\n", "en": r"(?<=[.?!;])\s+|\n"}
SR = 24000


def anchors(lang):
    """每节每一行旁白的开始时刻（节内秒）。画面提示整行的行不算。"""
    fn, cut = SCRIPT[lang]
    text = (EP / fn).read_text(encoding="utf-8").split(cut)[0]
    c = json.loads((EP / f"cues.{lang}.json").read_text(encoding="utf-8"))
    subs, out, k = c["subs"], [], 0
    for (a, b), sec in zip(c["sections"], re.split(r"\n## ", text)[1:]):
        body = [re.sub(r"〔.*?〕", "", l).replace("**", "").strip()
                for l in sec.split("\n")[1:] if not l.startswith((">", "---"))]
        row = []
        for line in filter(None, body):
            n = len([x for x in re.split(SPLIT[lang], line) if x and x.strip()])
            row.append(round(subs[k][0] - a, 3))
            k += n
        out.append(row)
    assert k == len(subs), (k, len(subs))
    return out


def open_page(p, lang):
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    pg.goto(SRC.as_uri())
    pg.evaluate("window.fontsReady")
    strs = json.loads((EP / "i18n" / f"{lang}.json").read_text(encoding="utf-8"))
    c = json.loads((EP / f"cues.{lang}.json").read_text(encoding="utf-8"))
    pg.evaluate("([s,u,b,a])=>{STR=s;SUBS=u;SEC=b;ANCH=a;}", [strs, c["subs"], c["sections"], anchors(lang)])
    return b, pg, c["sections"]


def shot(pg, t, path):
    pg.evaluate(f"renderFrame({t})")
    pg.locator("#stage").screenshot(path=str(path))


def blip(kind):
    """代码合成的短提示音：bar = 一声低音，reveal = 上行两音，tick = 一声短高音。音量远低于人声。"""
    spec = {"bar": [(392, 0.09)], "reveal": [(523, 0.08), (784, 0.12)], "tick": [(880, 0.05)]}[kind]
    out = []
    for f, d in spec:
        n = int(d * SR)
        for i in range(n):
            env = math.sin(math.pi * i / n) ** 2
            out.append(0.12 * env * math.sin(2 * math.pi * f * i / SR))
    return out


def mix_sound(vo, events, dst):
    with wave.open(str(vo)) as w:
        pcm = list(struct.unpack(f"<{w.getnframes()}h", w.readframes(w.getnframes())))
    for t, kind in events:
        i0 = int(t * SR)
        for j, v in enumerate(blip(kind)):
            if 0 <= i0 + j < len(pcm):
                pcm[i0 + j] = max(-32768, min(32767, pcm[i0 + j] + int(v * 32767)))
    with wave.open(str(dst), "wb") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(SR)
        w.writeframes(struct.pack(f"<{len(pcm)}h", *pcm))


def sheet(files, out, cols=3):
    rows = (len(files) + cols - 1) // cols
    inputs, filt = [], []
    for i, f in enumerate(files):
        inputs += ["-i", str(f)]
        filt.append(f"[{i}]scale=640:360[v{i}]")
    layout = "|".join(f"{(i % cols) * 640}_{(i // cols) * 360}" for i in range(len(files)))
    filt.append("".join(f"[v{i}]" for i in range(len(files))) + f"xstack=inputs={len(files)}:layout={layout}:fill=black")
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt), str(out)], check=True)


def main():
    args = sys.argv[1:]
    lang = "zh"
    if "--lang" in args:
        i = args.index("--lang")
        lang = args[i + 1]
        del args[i : i + 2]
    mode, out = args[0], pathlib.Path(args[1])
    with sync_playwright() as p:
        b, pg, bounds = open_page(p, lang)
        if mode == "cover":
            out.mkdir(parents=True, exist_ok=True)
            for name, h in (("cover-16x9.png", 1080), ("cover-16x10.png", 1200)):
                pg.set_viewport_size({"width": 1920, "height": h})
                pg.evaluate(f"renderCover({h})")
                pg.locator("#stage").screenshot(path=str(out / name))
        elif mode in ("stills", "sheet", "beats"):
            if mode == "beats":  # 每行旁白开始后 1.2 s 一格（一节一张表）
                A = anchors(lang)
                times = [[bounds[i][0] + a + 1.2 for a in row] + [bounds[i][1] - 0.3] for i, row in enumerate(A)]
            else:
                times = [list(map(float, args[2:]))]
            for si, ts in enumerate(times):
                d = out if mode == "stills" else pathlib.Path(tempfile.mkdtemp())
                d.mkdir(parents=True, exist_ok=True)
                files = []
                for t in ts:
                    f = d / f"still_{t:07.2f}.png"
                    shot(pg, t, f)
                    files.append(f)
                if mode == "sheet":
                    sheet(files, out)
                elif mode == "beats":
                    sheet(files, out.with_name(f"{out.stem}-s{si + 1}{out.suffix}"))
        else:
            fps = int(args[2]) if len(args) > 2 else 30
            aud = EP / "audio" if lang == "zh" else EP / "audio" / lang
            events = pg.evaluate("soundEvents()")
            mixed = aud / "vo_mix.wav"
            mix_sound(aud / "vo_final.wav", events, mixed)
            with wave.open(str(mixed)) as w:
                end = w.getnframes() / w.getframerate() + 1.5
            with tempfile.TemporaryDirectory() as d:
                n = int(round(end * fps))
                for i in range(n):
                    shot(pg, i / fps, pathlib.Path(d) / f"{i:05d}.png")
                out.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", f"{d}/%05d.png",
                                "-i", str(mixed), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                                "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-shortest", str(out)], check=True)
        b.close()


if __name__ == "__main__":
    main()
