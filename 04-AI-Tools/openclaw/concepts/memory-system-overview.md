---
title: OpenClaw 记忆系统总览
date: 2026-04-26
tags: [ai/openclaw, ai/memory, ai/embedding, ai/qwen3]
status: learning
difficulty: advanced
time_spent: 4h
source: [OpenClaw 官方文档, 实践配置]
---

# OpenClaw 记忆系统总览

## 架构概述

```
对话内容 → memory-core 分块(chunking 1024/128)
         → Ollama qwen3-embedding:0.6B 生成向量
         → SQLite (sqlite-vec + FTS5) 存储
         → dreaming 每天 light/deep/rem 三阶段自动整理
         → dream 产物通过 bridge 输出到 memory-wiki
         → wiki 编译出 entities/concepts/syntheses/reports
```

## 三层架构

| 层 | 负责内容 | 存储位置 |
|---|---|---|
| memory-core | recall、语义搜索、promotion、dreaming、memory 运行时 | ~/.openclaw/memory/main.sqlite |
| memory-wiki | 编译后的 wiki 页面、结构化主张、来源追踪、仪表板 | ~/.openclaw/wiki/main/ |
| dreaming | 自动整理记忆、发现模式、产出 dream 报告 | ~/.openclaw/workspace/memory/.dreams/ |

## Embedding 配置

配置路径：`agents.defaults.memorySearch`

| 参数 | 值 | 说明 |
|---|---|---|
| provider | ollama | 使用 Ollama embedding API |
| fallback | local | 回退到 node-llama-cpp |
| model | qwen3-embedding:0.6B | Ollama 中的模型名 |
| chunking.tokens | 1024 | 每块 token 数 |
| chunking.overlap | 128 | 块间重叠 |
| sync.onSessionStart | true | 会话启动时自动同步 |
| sync.onSearch | true | 搜索时懒同步 |
| sync.watch | true | 文件变更时自动同步 |
| cache.enabled | true | 缓存 embedding |
| cache.maxEntries | 10000 | 缓存上限 |

## Dreaming 配置

配置路径：`plugins.entries.memory-core.config.dreaming`

| 参数 | 值 | 说明 |
|---|---|---|
| enabled | true | 开启 dreaming |
| frequency | daily | 每天触发 |
| timezone | Asia/Shanghai | 东八区 |
| storage.mode | both | 内联+独立存储 |

### Dreaming 三阶段

| 阶段 | 说明 | 关键参数 |
|---|---|---|
| light | 轻量回顾近期记忆 | lookback 3 天, limit 50, 去重 |
| deep | 深度综合高价值片段 | limit 20, minScore 0.6, minRecallCount 2 |
| rem | 发现长期模式和规律 | lookback 7 天, limit 10 |

## 检索机制

- 不支持外部 Reranker 模型
- 内置混合检索：向量相似度 + BM25 关键词（hybrid search）
- MMR（Maximal Marginal Relevance）重排序去重
- `query.hybrid.vectorWeight` / `textWeight` 可调权重
- FTS tokenizer：`unicode61`（默认）或 `trigram`（中文更佳）

## 存储限制

- `store.driver` 硬编码只支持 SQLite（schema 中 `const: "sqlite"`）
- 不支持 PostgreSQL、Milvus 等外部向量库
- 向量搜索通过 sqlite-vec 扩展实现

## CLI 常用命令

```bash
openclaw memory status              # 查看记忆状态
openclaw memory status --deep       # 深度检查 embedding 提供商
openclaw memory index --force       # 强制全量索引
openclaw memory search "query"      # 搜索记忆
openclaw wiki status                # 查看 wiki 状态
openclaw wiki doctor                # wiki 诊断
openclaw wiki compile               # 编译 wiki
openclaw wiki lint                  # 结构检查
openclaw gateway stop               # 停止 gateway
openclaw gateway start              # 启动 gateway
openclaw config validate            # 验证配置
openclaw config schema              # 输出完整 JSON schema
```

## 配置文件位置

| 文件 | 路径 |
|---|---|
| 主配置 | ~/.openclaw/openclaw.json |
| 记忆数据库 | ~/.openclaw/memory/main.sqlite |
| Wiki 目录 | ~/.openclaw/wiki/main/ |
| Dream 产物 | ~/.openclaw/workspace/memory/.dreams/ |
| 配置备份 | .bak, .bak.1-.bak.4, .last-good, .clobbered.* |

## 相关笔记

- [[concepts/memory-wiki-overview]]
- [[troubleshooting/openclaw-config-clobber]]
- [[../../llama.cpp/concepts/qwen3-embedding-local]] - Qwen3-Embedding 模型详情
- [[../../llama.cpp/]] - llama.cpp 生态

## 相关资源

- [OpenClaw Memory Wiki 文档](https://docs.openclaw.ai/zh-CN/plugins/memory-wiki)
- [OpenClaw Memory Overview](https://docs.openclaw.ai/plugins/memory-overview)
