# 配音规范

2026-11-08 试音后定稿（对比 Desheng 复刻 / Charon / Sulafat / Sadaltager，见 `voice-tests/`）。

| 项目 | 设定 |
|---|---|
| 工具 | gemini-voice-mcp 的 `synthesize_speech`（Cloud Run 版本 `gemini-voice-mcp-00005-gqp` 起支持 `voice`） |
| 主播音声线 | **Charon**（Google 官方预置，"Informative"） |
| 中文 | `language: zh-CN` |
| 英文 | `language: en-US` |
| 单次文本上限 | 2000 字符，长稿按段落分段合成后拼接 |

## 风格提示（固定，不随期改动）

- 中文：`用耐心、清晰、温和的大学老师语气朗读，语速适中，讲到关键句时稍微放慢。英文术语按英语原本的读法念。`
- 英文：`Read in a patient, clear, warm university-lecturer tone at a moderate pace, slowing slightly on key sentences.`

## 规则

- 每期在 `meta.yml` 记录声线、风格提示、生成日期和服务版本。
- 生成的音频不入库，本地保存在 `episodes/epNNN/audio/`（已被 .gitignore 排除）。
- 新术语第一次配音后，用 faster-whisper 转写抽查读音；读错的写进 `docs/concepts.yml` 该概念的 `tts` 字段（记下读错成什么、怎么改写的），并在脚本里改写。
- 如果 Charon 音色被上游更新而明显变化，全系列从当期起统一切换，并在 README 注明。
- 中文数字后面别直接跟"时"：如"A 是 2 时"会听成"二十"（第 2 期转写为 20、0.50）。写成"的时候"。
