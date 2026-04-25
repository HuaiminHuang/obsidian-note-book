---
title: Qwen3-Embedding 本地部署
date: 2026-04-26
tags: [ai/llama-cpp, ai/embedding, ai/qwen3, cuda]
status: learning
---

# Qwen3-Embedding 本地部署

## 概述

Qwen3-Embedding-0.6B 是阿里 Qwen3 系列的 embedding 模型，用于将文本转换为向量表示，支持语义搜索、文本分类等下游任务。

**模型参数**：

| 参数 | 值 |
|------|------|
| 架构 | `Qwen3ForCausalLM` |
| llama.cpp 对应 | `LLM_ARCH_QWEN3` / `LLM_TYPE_0_6B` |
| 层数 | 28 |
| hidden_size | 1024 |
| tie_word_embeddings | true |
| 输出向量维度 | 1024 |

## 模型文件

- HF 模型目录：`~/models/embedding/Qwen3-Embedding-0.6B/`
- GGUF 模型文件：`~/models/embedding/Qwen3-Embedding-0.6B.gguf`
- 转换脚本：`python convert_hf_to_gguf.py ~/models/embedding/Qwen3-Embedding-0.6B/`

## llama.cpp 推理配置

### 编译

```bash
cmake -B build -DGGML_CUDA=ON && cmake --build build --config Release
```

### 关键参数

| 参数 | 说明 |
|------|------|
| `--pooling last` | Qwen3 Embedding 特殊处理，取最后一层输出 |
| `--embd-normalize 2` | L2 归一化，用于余弦相似度计算 |
| `-ngl 99` | 全部层卸载到 GPU |
| `-t 16` | CPU 线程数 |

### 推理脚本

`~/llama.cpp/qwen3-embedding-0p6B.sh`

## Python 依赖（convert_hf_to_gguf）

```
torch
gguf
sentencepiece
protobuf
numpy
transformers>=5.5.1
```

## Ollama 部署

| 项目 | 值 |
|------|------|
| 模型名 | `qwen3-embedding:0.6B`（639 MB） |
| API 端点 | `http://localhost:11434/api/embeddings` |
| 优势 | 自动管理 GPU 内存（空闲时卸载） |

## 硬件环境

- GPU：RTX 4060 Laptop 8GB
- CUDA：12.8

## 相关资源

- [Qwen3-Embedding HuggingFace](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)
- [llama.cpp GitHub](https://github.com/ggml-org/llama.cpp)
- [llama.cpp Embedding 文档](https://github.com/ggml-org/llama.cpp/blob/master/examples/embedding/README.md)

---

**创建日期**: 2026-04-26
**最后更新**: 2026-04-26
