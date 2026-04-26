---
title: whisper.cpp - 语音识别推理引擎
date: 2026-04-24
tags: [ai/whisper, ai/inference, cuda, audio]
status: completed
difficulty: intermediate
source: [https://github.com/ggerganov/whisper.cpp]
---

# whisper.cpp - 语音识别推理引擎

## 概念

whisper.cpp 是 OpenAI Whisper 模型的纯 C/C++ 实现，与 llama.cpp 同属 Georgi Gerganov 项目生态。

**核心特性**：
- **零外部依赖** - 单个二进制文件即可运行
- **CPU 优化** - AVX/AVX2/FMA 指令集加速
- **GPU 加速** - 支持 CUDA 后端
- **轻量级** - large-v3-turbo 模型仅 1.6GB

## 模型规格

| 模型 | 大小 | 速度 | 中文准确率 |
|------|------|------|-----------|
| ggml-tiny.bin | ~75MB | 极快 | 一般 |
| ggml-base.bin | ~142MB | 快 | 较好 |
| ggml-small.bin | ~466MB | 中等 | 好 |
| ggml-medium.bin | ~1.42GB | 慢 | 很好 |
| ggml-large-v3-turbo.bin | ~1.62GB | 较慢 | 最好 |

## 模型下载

使用 HuggingFace 镜像下载（国内加速）：

```bash
# hf-mirror.com（较稳定）
HF_ENDPOINT=https://hf-mirror.com hf download ggerganov/whisper.cpp ggml-large-v3-turbo.bin --local-dir ~/models/ggml-whisper

# 备选镜像
HF_ENDPOINT=https://hf.juncaixin.xyz hf download ggerganov/whisper.cpp ggml-small.bin --local-dir ~/models/ggml-whisper

# aria2c 多线程下载
aria2c -x 8 -s 8 "https://hf-mirror.com/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin" -d ~/models/ggml-whisper
```

国内 HuggingFace 镜像源：
| 镜像 | 地址 |
|------|------|
| hf-mirror.com | `https://hf-mirror.com` |
| hf.juncaixin.xyz | `https://hf.juncaixin.xyz` |
| hf.cool | `https://hf.cool` |

## 编译

### CPU 版本（默认）

```bash
cd whisper.cpp
make -j
```

### CUDA 版本（推荐，如有 NVIDIA GPU）

```bash
cd whisper.cpp
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j
```

## 推理命令

```bash
# CPU 推理
~/whisper.cpp/build/bin/whisper-cli \
  -m ~/models/ggml-whisper/ggml-large-v3-turbo.bin \
  -f ~/audio.wav \
  -l zh

# GPU 推理（编译 CUDA 版本后自动使用 GPU）
~/whisper.cpp/build/bin/whisper-cli \
  -m ~/models/ggml-whisper/ggml-large-v3-turbo.bin \
  -f ~/audio.wav \
  -l zh

# CPU 推理指定线程数
~/whisper.cpp/build/bin/whisper-cli \
  -m ~/models/ggml-whisper/ggml-large-v3-turbo.bin \
  -f ~/audio.wav \
  -l zh -t 20
```

## GPU vs CPU 推理

| 对比项 | CPU (AVX2, 4线程) | GPU (RTX 4060) |
|--------|-------------------|----------------|
| 30秒音频耗时 | ~77秒（2.5x 实时） | ~3-5秒（0.1x 实时） |
| 显存占用 | 0（使用系统内存） | ~2-3GB |
| 主要瓶颈 | encoder 编码（~41秒） | GPU 并行计算 |
| 适用场景 | 无 GPU 环境 | 有 NVIDIA 显卡 |

## 相关命令

- [[../code/whisper-commands]] - whisper.cpp 常用命令速查

## 相关笔记

- [[../troubleshooting/whisper-gpu-speed]] - GPU 推理加速配置

---

**创建日期**: 2026-04-24
**最后更新**: 2026-04-24
