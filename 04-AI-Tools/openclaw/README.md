---
title: OpenClaw 记忆系统
date: 2026-04-26
tags: [ai/openclaw, ai/memory, ai/embedding]
status: learning
---

# OpenClaw 记忆系统

OpenClaw 是一个 AI 智能体平台（版本 2026.4.23），内置多层记忆系统，支持语义检索、自动整理和知识编译。

## 记忆系统架构

记忆系统包含三层：

- **memory-core** — 语义检索层：负责对话记忆的分块、向量化、存储和检索
- **dreaming** — 自动整理层：每天触发三阶段（light/deep/rem）自动整理记忆，发现模式
- **memory-wiki** — 知识编译层：从记忆产物编译出结构化知识页面

### 技术栈

- **Embedding 后端**：Qwen3-Embedding-0.6B，通过 Ollama 提供 API
- **存储**：SQLite + sqlite-vec 向量扩展 + FTS5 全文搜索
- **检索**：内置混合检索（向量相似度 + BM25 关键词），MMR 重排序去重

## 目录索引

### 概念知识（`concepts/`）

- [[concepts/memory-system-overview]] - 记忆系统总览与配置详解
- [[concepts/memory-wiki-overview]] - Memory Wiki 插件与知识编译
- [[concepts/exec-security-allowlist]] - Exec 安全策略与白名单机制

### 代码示例（`code/`）

- [[code/openclaw-memory-config]] - 完整记忆系统配置参考

### 问题排查（`troubleshooting/`）

- [[troubleshooting/openclaw-config-clobber]] - 配置文件被覆盖问题排查

## 相关资源

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [Memory Wiki 插件文档](https://docs.openclaw.ai/zh-CN/plugins/memory-wiki)
- [Memory Overview 文档](https://docs.openclaw.ai/plugins/memory-overview)
