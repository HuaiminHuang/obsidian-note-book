---
title: whisper.cpp GPU 推理加速配置
date: 2026-04-24
tags: [troubleshooting, whisper, gpu, cuda, performance]
status: completed
priority: medium
environment: Ubuntu + RTX 4060 (CUDA 13.0)
---

# whisper.cpp GPU 推理加速配置

## 问题描述

使用 whisper.cpp 进行语音转写时，30 秒音频耗时 77 秒（2.5x 实时），速度过慢。

### 关键日志

```
whisper_backend_init_gpu: no GPU found
encode time = 41245.97 ms /     2 runs ( 20622.99 ms per run)
    total time = 77634.47 ms
```

### 环境信息

- CPU: 20 线程（仅用了 4 线程）
- GPU: NVIDIA GeForce RTX 4060 (8GB)
- CUDA: 13.0
- 音频长度: 30.7 秒，491k 采样点

## 诊断过程

### 1. 问题定位

whisper-cli 默认使用 CPU 推理，RTX 4060 完全未利用。

### 2. 根本原因分析

- whisper.cpp 默认编译为 CPU-only 版本（`make`）
- CPU 推理时 encoder 编码是主要瓶颈（占 ~41 秒 / 总 77 秒）
- GPU 推理可将 encoder 时间从 41 秒缩短至 ~2 秒

### 3. 验证 GPU 可用性

```bash
$ nvidia-smi
GPU 0: NVIDIA GeForce RTX 4060 (8GB)
CUDA Version: 13.0
```

## 解决方案

### 方案 1：CUDA 编译（推荐）

```bash
cd ~/whisper.cpp
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j
```

编译后直接运行，whisper-cli 自动使用 GPU 推理。

### 方案 2：CPU 多线程（备用）

若无法使用 GPU，增加线程数：

```bash
whisper-cli -m model.bin -f audio.wav -l zh -t 20
```

### 方案 3：换小模型

```bash
# 下载 small 版本（466MB）
HF_ENDPOINT=https://hf-mirror.com hf download ggerganov/whisper.cpp ggml-small.bin --local-dir ~/models/ggml-whisper

# 推理速度比 large-v3-turbo 快 5-10 倍
whisper-cli -m ~/models/ggml-whisper/ggml-small.bin -f audio.wav -l zh
```

## 预期提升

| 方案 | 30秒音频耗时 | 加速比 |
|------|-------------|--------|
| CPU (原始) | ~77 秒 | 1x |
| CPU + 20线程 | ~30-40 秒 | ~2x |
| GPU (RTX 4060) | ~3-5 秒 | ~15-25x |
| GPU + small模型 | ~1-2 秒 | ~40-50x |

## 验证步骤

```bash
# 编译后运行，检查是否有 GPU 信息
whisper-cli -m model.bin -f audio.wav -l zh | grep -i gpu
# 应输出类似：whisper_init_with_params_no_state: use gpu = 1
```

## 预防措施

- 首次编译时默认启用 CUDA：`cmake -B build -DGGML_CUDA=ON`
- RTX 4060 有 8GB 显存，large-v3-turbo 仅占 ~2-3GB，完全够用

## 总结

| 问题 | 解决方法 | 状态 |
|------|----------|------|
| CPU 推理速度慢 | `cmake -B build -DGGML_CUDA=ON` 重新编译 | ✅ |

---

**文档创建**: 2026-04-24
**最后更新**: 2026-04-24
**版本**: 1.0
