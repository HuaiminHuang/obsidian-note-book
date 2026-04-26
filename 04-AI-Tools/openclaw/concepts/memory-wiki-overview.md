---
title: Memory Wiki 插件概述
date: 2026-04-26
tags: [ai/openclaw, ai/memory, ai/wiki]
status: learning
difficulty: intermediate
---

# Memory Wiki 插件概述

## 定位

memory-wiki 是 OpenClaw 内置插件，不替换 memory-core，与其并列工作。它从 memory-core 的产物（如 dream 报告）中编译出结构化的知识页面。

## 三种运行模式

| 模式 | 说明 | 推荐 |
|---|---|---|
| isolated | 独立运行，不从 memory-core 读取数据 | 否 |
| bridge | 桥接模式，从 memory-core 读取产物编译知识 | **推荐** |
| unsafe-local | 实验模式，直接访问本地文件系统 | 否 |

**推荐使用 bridge 模式**：既能利用 memory-core 的全部能力，又能产出结构化知识。

## 知识库布局

```
~/.openclaw/wiki/main/
├── entities/       # 实体页面（人物、项目、技术等）
├── concepts/       # 概念页面（抽象知识）
├── syntheses/      # 综合页面（跨主题整合）
├── sources/        # 来源追踪（原始记忆出处）
└── reports/        # 报告（定期汇总）
```

## 结构化主张系统

Wiki 使用 claims frontmatter 来表示知识主张：

```yaml
---
claims:
  - id: claim-001
    text: "Qwen3-Embedding 支持 8192 token 上下文"
    status: verified
    confidence: 0.95
    evidence:
      - "来源：Qwen3 官方技术报告"
      - "来源：Ollama 模型配置验证"
---
```

## 编译管线

编译过程产出两个关键文件：

- `agent-digest.json` — agent 摘要，用于上下文注入
- `claims.jsonl` — 结构化主张，每行一个 claim

## 搜索配置

| 参数 | 选项 | 说明 |
|---|---|---|
| search.backend | shared | 共享 memory 搜索后端 |
| search.backend | local | Wiki 独立搜索后端 |
| search.corpus | wiki | 仅搜索 wiki 内容 |
| search.corpus | memory | 仅搜索原始记忆 |
| search.corpus | all | 搜索全部（推荐） |

## Obsidian 友好模式

设置 `renderMode = obsidian` 可启用 Obsidian 兼容渲染，输出格式更贴合 Obsidian 笔记习惯。

## 实体提取

- LLM 驱动的知识提取，非传统 NER（命名实体识别）
- 自动从记忆中发现和提取实体、关系、概念
- 支持实体消歧和合并

## Bridge 配置要点

```json
{
  "bridge": {
    "enabled": true,
    "readMemoryArtifacts": true,
    "indexDreamReports": true,
    "indexDailyNotes": true,
    "indexMemoryRoot": true,
    "followMemoryEvents": true
  }
}
```

开启 bridge 后，memory-wiki 会自动索引 dream 报告、日记和记忆根目录的内容。

## 相关笔记

- [[memory-system-overview]]
- [[../troubleshooting/openclaw-config-clobber]]
