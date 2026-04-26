---
title: 快速参考
date: 2026-03-14
tags: [docs, reference, quick-start]
status: completed
---

# 快速参考

## 概述

Obsidian 笔记系统的快速参考指南。

**详细的规范说明请参见**：[[tools/skills/obsidian-note-specs]]

## Frontmatter 字段速查

### 必需字段（所有文件）

```yaml
---
title: 标题
tags: [tag1, tag2]
---
```

### 推荐字段组合

**概念笔记**：
```yaml
---
title: 装饰器
tags: [python, decorator]
status: learning
difficulty: intermediate
---
```

**问题排查**：
```yaml
---
title: Windsurf Codeium 插件下载问题
tags: [troubleshooting, linux]
status: resolved
---
```

**文档笔记**：
```yaml
---
title: 文档标题
date: YYYY-MM-DD
tags: [docs, type]
status: completed
---
```

## Tags 速查

### 基础分类

```yaml
tags: [daily]              # 日常学习
tags: [todo]               # 待办事项
tags: [obsidian]           # Obsidian 使用
tags: [troubleshooting]    # 问题排查
```

### 技术分类

```yaml
tags: [python]             # Python 相关
tags: [python/decorator]   # Python 装饰器

tags: [ide]                # IDE 工具
tags: [ide/vscode]        # VSCode

tags: [ai]                 # AI 工具
tags: [ai/codeium]         # Codeium

tags: [algorithm]          # 算法
tags: [algorithm/sort]     # 排序
```

### 状态分类

```yaml
tags: [status/learning]    # 学习中
tags: [status/completed]   # 已完成
tags: [status/archived]    # 已归档
```

## 双向链接格式速查

### 正确格式

| 链接类型 | 格式 | 示例 |
|---------|------|------|
| 链接同级文件 | `[[文件名]]` | `[[装饰器]]` |
| 链接子目录文件 | `[[子目录/文件名]]` | `[[vscode-basic/vscode-terminal-keybindings-settings]]` |
| 链接目录 | `[[目录名/]]` | `[[Python/]]` |
| 代码文件 | `[[文件名.扩展名]]` | `[[decorator.py]]` |
| 带描述 | `[[文件名]] - 描述` | `[[装饰器]] - 学习装饰器` |

### 错误格式（❌ 不要这样）

```markdown
- 装饰器 - 学习装饰器           ← 没有 [[ ]]
- [decorator](decorator.py)       ← 使用了 Markdown 链接
- `decorator.py` - 装饰器示例    ← 使用了反引号
```

## 文件类型和模板

| 文件类型 | 模板文件 | 必需字段 |
|---------|---------|---------|
| 日常日记 | `templates/daily-note.md` | title, tags, date |
| 概念笔记 | `templates/concept-note.md` | title, tags, status |
| 问题排查 | `templates/troubleshooting.md` | title, tags, status, date |
| 待办事项 | `templates/todo.md` | title, tags, date |
| 文档笔记 | `templates/doc-note.md` | title, tags, date, status |
| 资源收集 | 手动创建 | title, tags, source |

## 字段说明

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| title | string | 标题（必需） | `Python 装饰器` |
| tags | array | 标签（必需） | `[python, decorator]` |
| status | string | 状态 | `learning/completed/archived` |
| date | string | 日期 | `2026-03-14` |
| difficulty | string | 难度 | `easy/intermediate/advanced` |
| time_spent | string | 学习时长 | `2h` |
| priority | string | 优先级 | `high/medium/low` |
| source | string | 资源链接 | `https://example.com` |
| aliases | array | 别名 | `[Codeium 下载问题]` |
| date | string | 日期（必需） | `2026-03-14` |
| status | string | 状态（必需） | `learning/completed/archived` |

## 常见错误速查

### Tags 错误

- ❌ `#python-decorator`（使用 `-` 而不是 `/`）
- ✅ `#python/decorator`

- ❌ `[Python, 学习, 装饰器]`（中英文混用）
- ✅ `[python, learning, decorator]`

- ❌ 标签过多（> 5 个）
- ✅ 3-5 个标签

### Frontmatter 错误

- ❌ 缺少 title 或 tags
- ✅ 必须包含 title 和 tags

- ❌ 日期格式不正确
- ✅ 使用 `YYYY-MM-DD` 格式

### 链接错误

- ❌ 没有使用 `[[ ]]`
- ✅ 必须使用 `[[ ]]`

## 搜索技巧

### Frontmatter 搜索

```text
title:装饰器
tag:#python
tag:#python/decorator
status:learning
date:2026-03-01..2026-03-31
```

### 标签过滤

- 在标签面板点击 `#python` 显示所有 Python 笔记
- 使用搜索框过滤标签

## 相关资源

- [[tools/skills/obsidian-note-specs]] - 完整的 Obsidian 笔记规范
- [[docs/tags-best-practices]] - Tag 和 Frontmatter 最佳实践
- [[docs/knowledge-base-design]] - 知识库结构设计
- [[docs/agent-operations]] - Agent 文档管理操作指南

---

**创建日期**: 2026-03-14
**最后更新**: 2026-03-15
**版本**: 2.0
