---
title: Agent 文档管理操作指南
date: 2026-03-14
created: 2026-03-14
updated: 2026-03-15
tags: [docs, agent, guide, operations]
status: active
version: 2.0
---

# Agent 文档管理操作指南

## 概述

本指南为 Agent 提供文档管理的核心规则。

**详细的规范说明请参见**：[[tools/skills/obsidian-note-specs]]

## 核心原则

### 1. 双向链接优先

所有 README 文件必须使用 `[[ ]]` 格式引用子文件。

**正确示例**：
```markdown
- [[装饰器]] - 学习装饰器的使用和原理
- [[decorator.py]] - 装饰器示例
```

### 2. 目录顺序固定

严格遵循目录编号规则。

**当前顺序**：
```
01-Daily/ → 02-Python/ → ... → 07-Frameworks/ → FIXED-01-Ubuntu/ → FIXED-02-Obsidian/ → FIXED-03-Todo/ → FIXED-04-Resources/
```

**规则**：
- 新增学习内容目录使用下一个编号（如：08-Database）
- 固定目录使用FIXED前缀，无需调整编号
- `FIXED-04-Resources` 始终保持在最后

### 3. 文件命名规范

- 概念笔记：中文或英文（`装饰器.md`, `decorator.md`）
- 代码文件：保留扩展名（`decorator.py`）
- 问题排查：kebab-case（`wsl2-memory-compression.md`）

### 4. 模板系统优先

创建新文件时，优先使用模板系统。

**可用模板**：
- `templates/daily-note.md` - 日常日记
- `templates/concept-note.md` - 概念笔记
- `templates/troubleshooting.md` - 问题排查
- `templates/todo.md` - 待办事项
- `templates/doc-note.md` - 文档笔记

## Agent 操作流程

### 创建新笔记

1. 调用 `obsidian-note-specs` skill 获取规范
2. 确定笔记类型和目录位置
3. 选择正确的模板
4. 按照规范创建笔记
5. 更新对应 README.md
6. 验证所有链接格式正确

### 创建新目录

1. 确认插入位置符合规则
2. 调整后续目录序号
3. 创建目录结构（concepts/, code/, troubleshooting/）
4. 创建 README.md
5. 更新相关文档

## 常见错误

### README 链接错误

❌ **没有使用双向链接**：
```markdown
- 装饰器 - 学习装饰器
```

✅ **正确**：
```markdown
- [[装饰器]] - 学习装饰器
```

### 目录顺序错误

❌ **违反顺序规则**：
```
06-Obsidian/
08-Database/    ← 错误：Resources 不应该在中间
```

✅ **正确**：
```
08-Database/    ← 新增学习内容目录
FIXED-01-Ubuntu/  ← 固定目录，无需调整
FIXED-02-Obsidian/ ← 固定目录，无需调整
FIXED-03-Todo/   ← 固定目录，无需调整
FIXED-04-Resources/ ← 固定目录，始终在最后
```

### 文件命名错误

❌ **包含特殊字符**：
```
@python decorator#.md
```

✅ **正确**：
```
装饰器.md
python-decorator.md
```

## 相关资源

- [[tools/skills/obsidian-note-specs]] - 完整的 Obsidian 笔记规范
- [[tools/agents/note-writer]] - 笔记编写 Agent
- [[docs/knowledge-base-design]] - 知识库结构设计

---

**创建日期**: 2026-03-14
**最后更新**: 2026-03-15
**版本**: 2.0
