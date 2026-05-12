---
title: MinerU 安装与使用
tags: [ai/mineru, ai/ocr, ai/pdf]
status: learning
difficulty: intermediate
time_spent: 3h
date: 2026-05-03
updated: 2026-05-03
source:
  - https://github.com/opendatalab/MinerU
  - https://huggingface.co/opendatalab/PDF-Extract-Kit-1.0
next_steps: []
---

# MinerU 安装与使用

## 概述

MinerU 是 OpenDataLab 开源的 PDF/文档解析工具（Python），将 PDF、图片、DOCX、PPTX、XLSX 解析为结构化 Markdown/JSON。基于 PDF-Extract-Kit-1.0 模型套件。

### 组件架构

```
pipeline 后端（默认）          hybrid 后端
  Layout Detection             pipeline + VLM 兜底
  + OCR (PaddleOCR)            ↕
  + MFR (UniMERNet)            VLM (Qwen2-VL 1.2B)
  + Table (SLANet+/UNet)
```

## 安装流程

### 环境准备（openclaw venv）

```bash
# 从零创建并安装
uv venv ~/.openclaw/venvs/mineru-pdf-parser --python 3.11
uv pip install --python ~/.openclaw/venvs/mineru-pdf-parser/bin/python \
  "mineru[pipeline]"

# 或使用已有 venv
source ~/.openclaw/venvs/mineru-pdf-parser/bin/activate
```

### 安装 PyTorch（CUDA 12.6，如果单独装）

```bash
uv pip install --python ~/.openclaw/venvs/mineru-pdf-parser/bin/python \
  torch torchvision torchaudio \
  --index-url https://download.pytorch.org/whl/cu126
```

### 安装 MinerU（完整）

```bash
# pipeline 后端（轻量，4GB VRAM，~3s/页）
uv pip install --python ~/.openclaw/venvs/mineru-pdf-parser/bin/python \
  "mineru[pipeline]"

# VLM 后端（需额外 ~2.2GB 模型，8GB VRAM，~10s/页）
uv pip install --python ~/.openclaw/venvs/mineru-pdf-parser/bin/python \
  "mineru[vlm]"
```

### uv 镜像加速

```bash
# PyTorch 官方源（cu126）
--index-url https://download.pytorch.org/whl/cu126
# PyPI 镜像（选一个）
--extra-index-url https://pypi.tuna.tsinghua.edu.cn/simple   # 清华（mineru 可能 403 限流）
--extra-index-url https://mirrors.aliyun.com/pypi/simple/    # 阿里云
# 或不用 PyPI 镜像，uv 自动 fallback 到 pypi.org
```

**注意**：`-i` 和 `--index-url` 冲突，不能同时用。PyTorch 用 `--index-url`，PyPI 用 `--extra-index-url`。

### 模型下载

首次运行自动下载到 `~/.cache/huggingface/hub/`（~1.2GB）。

```bash
# 先关代理（关键！代理会拦 HTTPS）
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY

# HF 镜像（推荐）
export HF_ENDPOINT=https://hf-mirror.com
# 或 ModelScope
export MINERU_MODEL_SOURCE=modelscope
```

**注意**：ModelScope 缓存到 `~/.cache/modelscope/hub/`，与 HF 缓存不共享。切换源会重新下载。

## 使用

### 解析 PDF

```bash
source ~/.openclaw/venvs/mineru-pdf-parser/bin/activate

# pipeline 后端（默认，最快，~3s/页）
mineru -p paper.pdf

# hybrid 后端（质量更高，但慢 4-5x，~10-19s/页）
mineru -p paper.pdf -b hybrid-auto-engine
```

### 输出结构

```
output/paper_name/auto/
  paper_name.md              # 主要输出
  *_content_list*.json       # 结构化内容
  *_middle.json              # 中间数据（bbox）
  *_model.json               # 模型原始输出
  *_layout.pdf               # 布局可视化
  *_span.pdf                 # Span可视化
  *_origin.pdf               # PDF副本
  images/                    # 提取的图片
```

## 模型位置

| 模型 | Repo | 大小 | 备注 |
|------|------|------|------|
| Pipeline 模型 | `opendatalab/PDF-Extract-Kit-1.0` | ~1.15 GB | Layout + OCR + MFR + Table |
| VLM 模型 | `opendatalab/MinerU2.5-Pro-2604-1.2B` | ~2.2 GB | Qwen2-VL 1.2B 基座 |

缓存位置：`~/.cache/huggingface/hub/models--{org}--{repo}/`

### Pipeline 内部模型

| 组件 | 模型文件 | 大小 |
|------|---------|------|
| Layout | PP-DocLayoutV2 (RT-DETR) | 205 MB |
| OCR Det | ch_PP-OCRv5_det_infer.pth | 14 MB |
| OCR Rec (en) | en_PP-OCRv5_rec_infer.pth | 23 MB |
| OCR Rec (zh) | ch_PP-OCRv5_rec_infer.pth | 31 MB |
| MFR (默认) | UniMERNet Small | 773 MB |
| MFR (中文) | PP-FormulaNet+ | 环境变量切换 |
| Wireless Table | SLANet+ (onnx) | 7 MB |
| Wired Table | UNet (onnx) | 8 MB |

## 踩坑记录

### 1. 网络问题 — HuggingFace 被墙

**症状**: 模型下载卡住、ConnectionResetError、"Fetching N files" 停在 0%

**解决**:

```bash
# 关代理（关键！代理会阻断 HTTPS）
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY

# 走国内镜像
export HF_ENDPOINT=https://hf-mirror.com
export MINERU_MODEL_SOURCE=modelscope
```

### 2. 代理与 HuggingFace 不兼容

`HTTP_PROXY=http://172.31.48.1:7890` 会阻隔 HuggingFace 的 HTTPS 直连。即使设了 `HF_ENDPOINT` 也可能失败。必须 `unset` 代理。

### 3. uv 安装失败（403 Forbidden）

清华镜像对 mineru 限流：

```
error: Failed to unzip wheel: mineru-3.1.6-py3-none-any.whl
HTTP status client error (403 Forbidden) for url (https://pypi.tuna.tsinghua.edu.cn/...)
```

**解决**：换阿里云镜像，或不用镜像（uv 自动 fallback 到 pypi.org）。

### 4. VLM/Hybrid 后端速度极慢

| 后端 | 速率 | 53 页耗时 |
|------|------|-----------|
| pipeline | ~3s/页 | ~2.5 min |
| hybrid/VLM | ~10-19s/页 | ~9-19 min |

RTX 4060 8GB 跑 VLM 1.2B 模型很吃力。普通学术论文用 pipeline 足够。

### 5. Hybrid 依赖 accelerate

```bash
# 如果出现 "requires accelerate" 错误
pip install accelerate
# 或直接装完整 VLM 依赖
uv pip install "mineru[vlm]"
```

### 6. 下载中断后的缓存

中断下载会留下 `.incomplete` 文件。下次重试前建议清理：

```bash
rm -rf ~/.cache/huggingface/hub/models--opendatalab--MinerU2.5-Pro-2604-1.2B
```

### 7. ModelScope 缓存位置不同

HuggingFace → `~/.cache/huggingface/hub/`
ModelScope → `~/.cache/modelscope/hub/`

切换源会重复下载。建议统一用 HuggingFace + HF 镜像。

### 8. `--index-url` 参数冲突

```bash
# 错误：-i 和 --index-url 冲突
uv pip install -i https://... --index-url https://...

# 正确：PyTorch 用 --index-url，PyPI 用 --extra-index-url
uv pip install "mineru[pipeline]" \
  --index-url https://download.pytorch.org/whl/cu126 \
  --extra-index-url https://mirrors.aliyun.com/pypi/simple/
```

## 自定义脚本

`~/ocr_pdf/mineru-pdf-parser/` 包含两脚本：

- `scripts/mineru-parse.sh` — 解析 PDF，支持 `-o -l -m -b --no-formula --no-table -s -e --models-dir --dry-run`

- `scripts/mineru-clean.sh` — 清理中间 JSON/PDF，保留 `.md` + `images/`

## 相关资源

- [MinerU GitHub](https://github.com/opendatalab/MinerU)
- [PDF-Extract-Kit-1.0 (HuggingFace)](https://huggingface.co/opendatalab/PDF-Extract-Kit-1.0)
- [PDF-Extract-Kit 工具包](https://github.com/opendatalab/PDF-Extract-Kit)

## 相关笔记

- [[../llama.cpp/concepts/qwen3-embedding-local]] - Qwen3-Embedding 本地部署
- [[../../FIXED-02-Obsidian/troubleshooting/obsidian-proxy-config]] - 代理配置

---

**创建日期**: 2026-05-03
**最后更新**: 2026-05-03
