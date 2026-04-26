---
title: 知识库结构设计
date: 2026-03-14
tags: [docs, design, knowledge-base]
status: completed
---

# 知识库结构设计

## 概述

本文档描述 Obsidian 知识库的整体架构设计。

**详细的规范说明请参见**：[[tools/skills/obsidian-note-specs]]

## 设计目标

构建一个面向程序员个人学习成长的知识库，重点在于：
- 知识体系的构建和快速检索
- 持续更新的学习内容
- 双向链接构建知识网络

## 目录结构

```
ObsidianNote/
├── 01-Daily/           # 日常学习日记（按时间归档）
├── 02-Python/          # Python 学习
├── 03-IDE-Tools/       # IDE 和工具
├── 04-AI-Tools/        # AI 工具使用
├── 05-Algorithms/      # 数据结构和算法
├── 06-Dev-Methods/     # 开发方法和规范
├── 07-Frameworks/      # 框架和技术
├── FIXED-01-Ubuntu/    # Linux/Ubuntu 使用指南（固定）
├── FIXED-02-Obsidian/  # Obsidian 使用指南（固定）
├── FIXED-03-Todo/      # 待办事项管理（固定）
├── FIXED-04-Resources/ # 资源收集（固定，始终最后）
├── docs/               # 文档
├── tools/              # 工具配置
└── templates/          # 模板库
```

## 设计原则

### 1. 时间归档 + 主题分类

- **日常日记**：使用 `01-Daily/` 按时间记录每日学习
- **主题知识**：使用 `02-Python/`、`03-IDE-Tools/` 等按主题归档永久知识
- **双向链接**：日记通过 `[[link]]` 引用主题知识点

### 2. README 作为知识地图

每个主题目录都有 `README.md`，包含：
- 学习路线图
- 重要知识点索引
- 快速导航

**重要**：README 必须使用双向链接 `[[ ]]` 引用文件。

### 3. 工具目录隔离

- `tools/` 目录下的 opencode 工具文件不参与序号排序
- 与学习知识库分离，避免混淆

## 目录编号规则

### 当前顺序

```
01-Daily/           # 日常学习日记
02-Python/          # Python 学习
03-IDE-Tools/       # IDE 和工具
04-AI-Tools/        # AI 工具使用
05-Algorithms/      # 数据结构和算法
06-Dev-Methods/     # 开发方法和规范
07-Frameworks/      # 框架和技术
FIXED-01-Ubuntu/    # Linux/Ubuntu 使用指南（固定）
FIXED-02-Obsidian/  # Obsidian 使用指南（固定）
FIXED-03-Todo/      # 待办事项管理（固定）
FIXED-04-Resources/ # 资源收集（固定，始终最后）
```

### 编号规则

1. **01-99**: 学习内容目录（可以扩展）
2. **FIXED-01-Ubuntu**: Linux/Ubuntu 使用指南（固定）
3. **FIXED-02-Obsidian**: 工具使用指南（固定）
4. **FIXED-03-Todo**: 待办事项管理（固定）
5. **FIXED-04-Resources**: 资源收集（始终置后，固定）

### 新增目录规则

**允许新增的位置**：新学习内容目录使用下一个编号（如：08-Database）

**禁止修改的位置**：
- `FIXED-01-Ubuntu`（固定）
- `FIXED-02-Obsidian`（固定）
- `FIXED-03-Todo`（固定）
- `FIXED-04-Resources`（始终置后，固定）

## Frontmatter 字段

### 必需字段

```yaml
---
title: 标题
date: YYYY-MM-DD
tags: [tag1, tag2]
status: learning|completed|archived
---
```

### 推荐字段

```yaml
---
difficulty: easy|intermediate|advanced
time_spent: 2h
---
```

## Agent 集成

### 可用的 Agents

- [[tools/agents/note-writer]] - 笔记编写 Agent
- [[tools/agents/explorer]] - 代码探索 Agent
- [[tools/agents/planner]] - 任务规划 Agent
- [[tools/agents/executor]] - 任务执行 Agent
- [[tools/agents/reviewer]] - 代码审查 Agent

### Agent 操作规范

所有 Agent 都应遵循以下规范：

1. **调用规范**：在操作前调用 `obsidian-note-specs` skill 获取规范
2. **确认机制**：修改文件前必须与用户确认（使用 `interaction-preferences` skill）
3. **链接格式**：始终使用 `[[ ]]` 双向链接
4. **目录顺序**：遵守目录编号规则

## 相关资源

- [[tools/skills/obsidian-note-specs]] - 完整的 Obsidian 笔记规范
- [[tools/skills/agents-to-notes]] - Agent 全局配置
- [[docs/agent-operations]] - Agent 文档管理操作指南
- [[docs/tags-best-practices]] - Tag 和 Frontmatter 最佳实践
- [[directory-structure]] - 知识库目录结构

---

**创建日期**: 2026-03-14
**最后更新**: 2026-03-15
**版本**: 2.0
