#!/usr/bin/env python3
"""把解说词脚本变成"只听不看"的版本：去掉画面提示、开头的状态说明和内部备注。

给"路过的新生"审核用（.claude/agents/freshman-dropin.md）：他只能拿到观众耳朵听到的内容。

  python tools/strip_cues.py episodes/ep002-xxx/script.md > /tmp/ep002-listen.md
"""

import re
import sys
from pathlib import Path

CUE = re.compile(r"〔[^〕]*〕")


def strip(text: str) -> str:
    out = []
    for line in text.splitlines():
        if re.match(r"^##\s*(内部备注|Internal notes)", line):
            break
        if line.startswith(">"):          # 开头的状态、时长、核心洞见说明
            continue
        line = CUE.sub("", line).rstrip()
        out.append(line)
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)      # 整行都是画面提示时留下的空行
    return text.rstrip().rstrip("-").rstrip() + "\n"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.stdout.write(strip(Path(sys.argv[1]).read_text(encoding="utf-8")))
