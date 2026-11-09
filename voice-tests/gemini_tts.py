"""用 Gemini TTS 生成试音样本。

用法：
    export GEMINI_API_KEY=...        # 不要写进代码或提交到仓库
    python voice-tests/gemini_tts.py --list            # 列出可用的 TTS 模型
    python voice-tests/gemini_tts.py                   # 用默认模型和音色生成中英文样本
    python voice-tests/gemini_tts.py --model <名字> --voices Charon Kore

输出：voice-tests/out/<model>_<voice>_<lang>.wav（音频不入库）
"""

import argparse
import re
import sys
import wave
from pathlib import Path

from google import genai
from google.genai import types

HERE = Path(__file__).parent
STYLE = {
    "zh": "用耐心、清晰、温和的大学老师语气朗读，语速适中，讲到关键句时稍微放慢。英文术语按英语原本的读法念。",
    "en": "Read in a patient, clear, warm university-lecturer tone at a moderate pace, slowing slightly on key sentences.",
}


def load_samples():
    text = (HERE / "sample.md").read_text(encoding="utf-8")
    zh = re.search(r"## 中文\n\n(.+?)\n\n## English", text, re.S).group(1).strip()
    en = re.search(r"## English\n\n(.+)", text, re.S).group(1).strip()
    return {"zh": zh, "en": en}


def tts_models(client):
    return sorted(m.name.removeprefix("models/") for m in client.models.list() if "tts" in m.name)


def synth(client, model, voice, lang, text, out_path):
    resp = client.models.generate_content(
        model=model,
        contents=f"{STYLE[lang]}\n\n{text}",
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)
                )
            ),
        ),
    )
    pcm = resp.candidates[0].content.parts[0].inline_data.data
    with wave.open(str(out_path), "wb") as w:  # 24 kHz, 16-bit, mono PCM
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(24000)
        w.writeframes(pcm)
    return len(pcm) / 2 / 24000


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--model")
    ap.add_argument("--voices", nargs="+", default=["Charon", "Kore", "Sulafat"])
    ap.add_argument("--langs", nargs="+", default=["zh", "en"])
    args = ap.parse_args()

    client = genai.Client()  # 读取环境变量 GEMINI_API_KEY
    models = tts_models(client)
    if args.list:
        print("\n".join(models))
        return
    model = args.model or next((m for m in reversed(models) if "pro" in m), models[-1] if models else None)
    if not model:
        sys.exit("没有找到 TTS 模型")
    print("model:", model)

    out = HERE / "out"
    out.mkdir(exist_ok=True)
    samples = load_samples()
    for voice in args.voices:
        for lang in args.langs:
            p = out / f"{model}_{voice}_{lang}.wav"
            secs = synth(client, model, voice, lang, samples[lang], p)
            print(f"{p.name}  {secs:.1f}s")


if __name__ == "__main__":
    main()
