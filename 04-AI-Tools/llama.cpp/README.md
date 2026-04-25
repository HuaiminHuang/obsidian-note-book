---
title: llama.cpp 项目生态
date: 2026-04-24
tags: [ai/llama-cpp, ai/inference, cuda, whisper, opencode]
status: learning
---

# llama.cpp 项目生态

## 项目概述

[[../../04-AI-Tools/llama-cpp]] - llama.cpp LLM 推理引擎（核心笔记）

llama.cpp 生态包含多个子项目，支持本地 LLM 推理和语音识别。

## 目录内容

### 概念知识（`concepts/`）

- [[concepts/whisper-cpp-usage]] - whisper.cpp 语音识别引擎使用指南
- [[concepts/opencode-model-variants]] - OpenCode 模型变体机制 (reasoning effort)
- [[concepts/qwen3-embedding-local]] - Qwen3-Embedding-0.6B 本地部署与配置

### 代码示例（`code/`）

- [[code/whisper-commands]] - whisper.cpp 常用命令速查

### 问题排查（`troubleshooting/`）

- [[troubleshooting/whisper-gpu-speed]] - whisper.cpp GPU 推理加速配置

## 相关外部资源

- [llama.cpp GitHub](https://github.com/ggerganov/llama.cpp)
- [whisper.cpp GitHub](https://github.com/ggerganov/whisper.cpp)
- [OpenCode GitHub](https://github.com/anomalyco/opencode)
- [models.dev](https://models.dev)

## 相关笔记

- [[../openclaw/]] - OpenClaw 记忆系统（使用 Qwen3-Embedding 作为后端）

---

**创建日期**: 2026-04-24
**最后更新**: 2026-04-26
