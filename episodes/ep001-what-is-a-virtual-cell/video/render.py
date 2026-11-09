"""逐帧渲染：renderFrame(t) 任意时刻可单独出图。

用法（在 episodes/ep001-.../ 下运行，解释器用仓库根目录的 .venv-render）：
  python video/render.py stills reviews/stills [--lang zh] t1 t2 ...
  python video/render.py sheet  reviews/contact.png [--lang zh] t1 t2 ...   # 关键帧联系表
  python video/render.py video  out/ep001-zh.mp4 [--lang zh] [FPS]

时间轴：各节起止由 audio/sec1..6.wav 的实际时长决定；字幕按句子字数在节内分配
（之后改为 faster-whisper 逐字时间 cues.<lang>.json）。
"""

import json
import pathlib
import re
import subprocess
import sys
import tempfile
import wave

from playwright.sync_api import sync_playwright

EP = pathlib.Path(__file__).resolve().parent.parent
SRC = EP / "video" / "frame.html"


def section_bounds():
    t, out = 0.0, []
    for i in range(1, 7):
        with wave.open(str(EP / "audio" / f"sec{i}.wav")) as w:
            d = w.getnframes() / w.getframerate()
        out.append([t, t + d])
        t += d
    return out


def subtitles(bounds):
    text = (EP / "script.md").read_text(encoding="utf-8").split("## 内部备注")[0]
    secs = re.split(r"\n## ", text)[1:]
    subs = []
    for (a, b), sec in zip(bounds, secs):
        body = "\n".join(l for l in sec.split("\n")[1:] if not l.startswith((">", "---")))
        body = re.sub(r"〔.*?〕", "", body).replace("**", "")
        sents = [s.strip() for s in re.split(r"(?<=[。？！；])|\n", body) if s and s.strip()]
        total = sum(len(s) for s in sents)
        t = a
        for s in sents:
            d = (b - a) * len(s) / total
            subs.append([t, t + d, s.rstrip("。；")])
            t += d
    return subs


def open_page(p, lang):
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    pg.goto(SRC.as_uri())
    pg.evaluate("window.fontsReady")
    strs = json.loads((EP / "i18n" / f"{lang}.json").read_text(encoding="utf-8"))
    cues = EP / f"cues.{lang}.json"
    if cues.exists():  # 逐字卡点结果（make_cues.py）
        c = json.loads(cues.read_text(encoding="utf-8"))
        bounds, subs = c["sections"], c["subs"]
    else:
        bounds = section_bounds()
        subs = subtitles(bounds)
    pg.evaluate("([s,u,b])=>{STR=s;SUBS=u;SEC=b;}", [strs, subs, bounds])
    return b, pg, bounds


def shot(pg, t, path):
    pg.evaluate(f"renderFrame({t})")
    pg.locator("#stage").screenshot(path=str(path))


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
        if mode in ("stills", "sheet"):
            d = out if mode == "stills" else pathlib.Path(tempfile.mkdtemp())
            d.mkdir(parents=True, exist_ok=True)
            files = []
            for t in map(float, args[2:]):
                f = d / f"still_{t:07.2f}.png"
                shot(pg, t, f)
                files.append(f)
            if mode == "sheet":  # 3 列联系表，每格缩到 640×360，下方标时间
                cols = 3
                rows = (len(files) + cols - 1) // cols
                inputs, filt = [], []
                for i, f in enumerate(files):
                    inputs += ["-i", str(f)]
                    filt.append(f"[{i}]scale=640:360[v{i}]")
                layout = "|".join(f"{(i % cols) * 640}_{(i // cols) * 360}" for i in range(len(files)))
                filt.append("".join(f"[v{i}]" for i in range(len(files))) + f"xstack=inputs={len(files)}:layout={layout}:fill=black")
                out.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt), str(out)], check=True)
        else:
            fps = int(args[2]) if len(args) > 2 else 30
            audio = EP / "audio" / ("vo_final.wav" if (EP / f"cues.{lang}.json").exists() else "vo_raw.wav")
            with wave.open(str(audio)) as w:
                end = w.getnframes() / w.getframerate() + 1.5  # 片尾留 1.5 s 静帧
            with tempfile.TemporaryDirectory() as d:
                n = int(round(end * fps))
                for i in range(n):
                    shot(pg, i / fps, pathlib.Path(d) / f"{i:05d}.png")
                out.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", f"{d}/%05d.png",
                                "-i", str(audio), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                                "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-shortest", str(out)], check=True)
        b.close()


if __name__ == "__main__":
    main()
