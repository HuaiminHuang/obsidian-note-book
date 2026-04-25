---
title: whisper.cpp 常用命令速查
date: 2026-04-24
tags: [ai/whisper, command, reference]
status: completed
---

# whisper.cpp 常用命令速查

## 编译

```bash
# 默认 CPU 编译
cd ~/whisper.cpp && make -j

# CUDA 编译
cd ~/whisper.cpp
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j
```

## 推理

```bash
# 基本转写
whisper-cli -m ~/models/ggml-whisper/ggml-large-v3-turbo.bin -f audio.wav

# 中文音频
whisper-cli -m ~/models/ggml-whisper/ggml-large-v3-turbo.bin -f audio.wav -l zh

# CPU 多线程
whisper-cli -m ~/models/ggml-whisper/ggml-large-v3-turbo.bin -f audio.wav -l zh -t 20

# 输出带时间戳
whisper-cli -m ~/models/ggml-whisper/ggml-large-v3-turbo.bin -f audio.wav -l zh -t 20 -ot

# 翻译为英文（task = translate）
whisper-cli -m ~/models/ggml-whisper/ggml-large-v3-turbo.bin -f audio.wav -l zh -tr
```

## 编译输出位置

| 命令 | 路径 |
|------|------|
| CPU 编译（make） | `~/whisper.cpp/main` |
| CUDA 编译（cmake） | `~/whisper.cpp/build/bin/whisper-cli` |

## 模型下载

```bash
# HuggingFace 镜像
HF_ENDPOINT=https://hf-mirror.com hf download ggerganov/whisper.cpp ggml-large-v3-turbo.bin --local-dir ~/models/ggml-whisper

# aria2c 多线程
aria2c -x 8 -s 8 "https://hf-mirror.com/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin" -d ~/models/ggml-whisper
```

## 关键参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-m` | 模型路径 | 必填 |
| `-f` | 音频文件 | 必填 |
| `-l` | 语言代码（zh, en, ja） | auto |
| `-t` | 线程数 | 4 |
| `-tr` | 翻译模式（转英文） | 关闭 |
| `-ot` | 打印时间戳 | 关闭 |
| `-ng` | 禁用 GPU | 关闭 |

---

**创建日期**: 2026-04-24
**最后更新**: 2026-04-24
