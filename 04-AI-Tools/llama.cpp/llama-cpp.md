---
title: llama.cpp - 本地 LLM 推理引擎
date: 2026-04-16
tags: [ai/llama-cpp, ai/inference, cuda, ubuntu]
status: learning
difficulty: intermediate
---

# llama.cpp - 本地 LLM 推理引擎

## 项目简介

[llama.cpp](https://github.com/ggerganov/llama.cpp) 是一个高性能的本地大语言模型（LLM）推理引擎，由 Georgi Gerganov 发起维护。

**核心特性**：

- **纯 C/C++ 实现** - 零外部依赖，开箱即用
- **量化支持** - 支持 1.5-bit 到 8-bit 量化，大幅降低显存需求
- **多硬件加速** - Apple Metal / NVIDIA CUDA / AMD HIP / Vulkan / Intel SYCL
- **CPU+GPU 混合推理** - 灵活分配计算负载
- **GGUF 模型格式** - 统一高效的模型存储格式

- **许可证**：MIT
- **仓库地址**：https://github.com/ggerganov/llama.cpp

## 核心特性

| 特性 | 说明 |
|------|------|
| 零依赖纯 C/C++ | 无需 Python 环境，编译即可运行 |
| 量化支持 | 1.5-bit ~ 8-bit，显著降低内存占用 |
| Apple Silicon 加速 | Metal 框架原生支持 M1/M2/M3/M4 |
| x86 CPU 加速 | AVX / AVX2 / AVX512 指令集优化 |
| GPU 加速 | CUDA / HIP / Vulkan / SYCL 多后端 |
| CPU+GPU 混合推理 | 部分层放 GPU，其余放 CPU，灵活调配 |
| GGUF 模型格式 | 统一高效的模型文件格式，支持元数据 |

## 支持的硬件后端

| 后端 | 目标设备 |
|------|----------|
| Metal | Apple Silicon (M1/M2/M3/M4) |
| CUDA | NVIDIA GPU |
| HIP | AMD GPU |
| Vulkan | 通用 GPU |
| SYCL | Intel/NVIDIA GPU |
| CPU (AVX/AVX2/AVX512) | x86 处理器 |

## 安装方式

### 方式一：包管理器

**macOS (Homebrew)**：

```bash
brew install llama.cpp
```

**Windows (winget)**：

```bash
winget install GGV.Llama.CPP
```

### 方式二：预编译二进制

从 [GitHub Releases](https://github.com/ggerganov/llama.cpp/releases) 下载对应平台的预编译包，解压后直接使用。

### 方式三：Docker

```bash
docker pull ghcr.io/ggerganov/llama.cpp:full-cuda
```

### 方式四：源码编译

详见下方 [[#CUDA 源码编译完整流程]] 章节。

## CUDA 源码编译完整流程

以下是在 Ubuntu/WSL2 环境下使用 CUDA 12.8 编译 llama.cpp 的完整流程（RTX 40 系列显卡）。

### Step 1: 安装 CUDA Toolkit 12.8

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install cuda-toolkit-12-8
```

### Step 2: 配置环境变量

```bash
echo 'export PATH=/usr/local/cuda-12.8/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

### Step 3: 验证 nvcc

```bash
nvcc --version  # 应显示 12.8
```

### Step 4: 克隆并编译

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
rm -rf build
cmake -B build -DGGML_CUDA=ON \
  -DCMAKE_CUDA_COMPILER=/usr/local/cuda-12.8/bin/nvcc \
  -DCMAKE_CUDA_ARCHITECTURES=89
cmake --build build --config Release -j 1
```

### Step 5: 验证

```bash
./build/bin/llama-cli --version
```

### 关键参数说明

| 参数 | 值 | 说明 |
|------|-----|------|
| `-DGGML_CUDA=ON` | - | 启用 CUDA 后端 |
| `-DCMAKE_CUDA_COMPILER` | `/usr/local/cuda-12.8/bin/nvcc` | 显式指定避免 PATH 冲突 |
| `-DCMAKE_CUDA_ARCHITECTURES` | `89` | 只编译 sm_89（RTX 40 系列） |
| `-j 1` | - | 单线程编译避免 OOM |

## 编译常见问题速查

> 详细排障请参考 → [[troubleshooting/llama-cpp-cuda-build-guide]]

| # | 问题 | 原因 | 解决方法 |
|---|------|------|----------|
| 1 | CUDA Toolkit not found | 未安装开发包 | 安装 `cuda-toolkit-12-8` |
| 2 | Unsupported compute_89 | CUDA 版本过低 | 需要 CUDA ≥ 12.0 |
| 3 | nvcc 版本仍旧 | PATH 冲突 | 调整 PATH + 显式指定编译器 |
| 4 | 编译进程被杀 | 并行过多 OOM | 使用 `-j 1` |
| 5 | 编译超时 | 架构过多 | `-DCMAKE_CUDA_ARCHITECTURES=89` |

## 获取模型

### GGUF 格式

GGUF 是 llama.cpp 使用的模型格式，支持存储模型权重、量化参数和元数据。大多数主流开源模型都有 GGUF 版本。

### Hugging Face 自动下载

llama-cli 支持直接从 Hugging Face 下载模型：

```bash
./build/bin/llama-cli -hf ggml-org/gemma-3-1b-it-GGUF
```

### 手动下载 GGUF 文件

从 [Hugging Face](https://huggingface.co/) 搜索所需模型的 GGUF 版本，下载 `.gguf` 文件到本地。

### 自行转换量化

```bash
# Step 1: 转换 HuggingFace 模型为 GGUF
python convert_hf_to_gguf.py /path/to/model --outfile model.gguf

# Step 2: 量化
./build/bin/llama-quantize model.gguf model-Q4_K_M.gguf Q4_K_M
```

### 推荐模型

| 模型 | 大小 | Hugging Face 路径 |
|------|------|-------------------|
| Gemma 3 1B | 小 | `ggml-org/gemma-3-1b-it-GGUF` |
| Llama 3 8B | 中 | 搜索 `llama-3 gguf` |
| Qwen 2.5 7B | 中 | 搜索 `qwen2.5 gguf` |

## 核心工具使用

### llama-cli - 命令行对话

基本对话：

```bash
./build/bin/llama-cli -m model.gguf
```

从 HuggingFace 下载并对话：

```bash
./build/bin/llama-cli -hf ggml-org/gemma-3-1b-it-GGUF
```

使用指定聊天模板：

```bash
./build/bin/llama-cli -m model.gguf -cnv --chat-template chatml
```

JSON 结构化输出（使用 grammar）：

```bash
./build/bin/llama-cli -m model.gguf -n 256 --grammar-file grammars/json.gbnf -p 'Request: ...'
```

### llama-server - OpenAI 兼容 API 服务器

启动服务器：

```bash
./build/bin/llama-server -m model.gguf --port 8080
```

设置上下文长度和并行数：

```bash
./build/bin/llama-server -m model.gguf -c 16384 -np 4
```

使用 speculative decoding（草稿模型加速）：

```bash
./build/bin/llama-server -m model.gguf -md draft.gguf
```

- **Web UI**: http://localhost:8080
- **API**: http://localhost:8080/v1/chat/completions

### llama-bench - 性能测试

```bash
./build/bin/llama-bench -m model.gguf
```

## 生态工具

| 工具 | 说明 | 链接 |
|------|------|------|
| llama-cpp-python | Python 绑定，支持 LangChain 集成 | [abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) |
| llama.vscode | VS Code 插件，本地代码补全 | [ggml-org/llama.vscode](https://github.com/ggml-org/llama.vscode) |
| Ollama | 基于 llama.cpp 的上层封装，简化部署 | [ollama/ollama](https://github.com/ollama/ollama) |

## 官方文档索引

| 文档 | 路径 |
|------|------|
| 构建指南 | `docs/build.md` |
| Docker | `docs/docker.md` |
| 多模态 | `docs/multimodal.md` |
| Server API | `tools/server/README.md` |

## 相关笔记

- [[troubleshooting/llama-cpp-cuda-build-guide]] - CUDA 编译安装排障指南
- [[concepts/whisper-cpp-usage]] - whisper.cpp 语音识别引擎
- [[../opencode/concepts/opencode-model-variants]] - OpenCode 模型变体机制

---

**创建日期**: 2026-04-16
**最后更新**: 2026-04-16
