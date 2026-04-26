---
name: obsidian-note-specs
description: Obsidian 笔记编写规范和标准操作流程 - 包含目录结构、文件命名、双向链接、frontmatter、标签等规范
---

# Obsidian 笔记编写规范

## Overview

此 skill 定义了 Obsidian 知识库笔记编写的完整规范，包括目录结构、文件命名、双向链接、frontmatter、标签系统、模板使用等标准。

## When to Use

- **创建新笔记前** - 确保符合规范
- **修改现有笔记时** - 验证是否符合规范
- **更新 README.md 时** - 确保链接格式正确
- **创建新主题目录时** - 确保目录序号正确

## 目录结构规范

### 当前目录结构

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
tools/              # 工具配置（不参与编号）
templates/          # 模板库
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

### 子目录结构

每个主题目录应包含以下子目录：

```
{主题目录}/
├── README.md                # 知识索引
├── concepts/                # 概念知识
├── code/                    # 代码示例
└── troubleshooting/         # 问题排查
```

## 文件命名规范

### 概念笔记

- **中文**：`装饰器.md`、`WSL2内存优化.md`
- **英文**：`decorator.md`、`wsl2-optimization.md`
- **清晰表达主题**

### 代码文件

- 保留原始扩展名：`decorator.py`、`config.json`
- 代码文件放在 `code/` 子目录

### 问题排查笔记

- 使用 kebab-case：`wsl2-memory-compression-release.md`
- 问题排查笔记放在 `troubleshooting/` 子目录

### 日常日记

- 格式：`YYYY-MM-DD.md`
- 路径：`01-Daily/YYYY/MM/YYYY-MM-DD.md`

### 禁止规则

- ❌ 使用特殊字符（`@`, `#`, `$`, `&`, `*`）
- ❌ 使用空格
- ❌ 过长的文件名

## 双向链接规范

### 正确格式

- **链接同级文件**：`[[装饰器]]`
- **链接子目录文件**：`[[子目录/文件名]]`
- **链接目录**：`[[目录名/]]`
- **代码文件**：`[[文件名.扩展名]]`
- **带描述**：`[[装饰器]] - 学习装饰器的使用和原理`

### 双向链接路径层级规则

不同层级使用不同的路径格式：

```
主题根目录/README.md
  → 同级笔记:    [[note-name]]              # 同级内
  → 子目录笔记:  [[note-name]]              # Obsidian 自动解析，无需前缀

主题根目录/concepts/note.md
  → 同级概念:    [[other-note]]             # 同 subdir，文件名即可
  → 兄弟 code:   [[../code/script]]         # 跨 subdir，用 ../ 相对路径
  → 兄弟 troubleshooting: [[../troubleshooting/issue]]
  → 唯一文件名:  [[globally-unique-name]]   # 全库唯一时可直接用文件名

主题根目录/troubleshooting/note.md
  → 同级:        [[other-note]]
  → 兄弟:        [[../concepts/note]]

跨主题目录（如 llama.cpp/ → openclaw/）
  → 使用 vault 绝对路径: [[主题名/子目录/文件名]]
    避免多层 ../../../
```

**路径选择原则**：

| 范围 | 格式 | 示例 | 理由 |
|------|------|------|------|
| 同级 subdir 内 | `[[文件名]]` | `[[memory-system-overview]]` | 简洁，Obsidian 自动匹配 |
| 跨 subdir (同主题) | `[[../子目录/文件名]]` | `[[../code/whisper-commands]]` | 子模块整体搬迁时内部链接不断 |
| 跨子主题 (从主题根 README) | `[[子主题/子目录/文件名]]` | `[[llama.cpp/concepts/qwen3-embedding-local]]` | README 在主题根目录，可直接引用同级目录 |
| 跨子主题 (从 subdir 内部) | `[[../../子主题/子目录/文件名]]` | `[[../../llama.cpp/concepts/qwen3-embedding-local]]` | 需要先 `../` 回到主题根目录 |

### 错误格式（❌ 不要这样）

- `装饰器` - 没有 `[[ ]]`
- `[decorator](decorator.py)` - 使用了 Markdown 链接
- `` `decorator.py` `` - 使用了反引号

### README 双向链接格式

```markdown
## 目录内容

### 概念知识 (`concepts/`)
- [[装饰器]] - 学习装饰器的使用和原理
- [[闭包]] - 学习闭包的概念和应用

### 代码示例 (`code/`)
- [[decorator.py]] - 装饰器示例
- [[closure.py]] - 闭包示例

### 问题排查 (`troubleshooting/`)
- [[wsl2-memory-compression-release]] - WSL2 Ubuntu内存压缩释放方案
```

## Frontmatter 规范

### 必需字段

```yaml
---
title: 标题
date: YYYY-MM-DD
tags: [tag1, tag2]
status: learning|completed|archived
---
```

### 可选字段

```yaml
---
aliases: [别名1, 别名2]
difficulty: easy|intermediate|advanced
time_spent: 2h
source: [官方文档, 博客]
next_steps: [[相关笔记]]
related: [[相关笔记]]
---
```

### status 字段说明

- `learning` - 正在学习中
- `completed` - 已完成学习
- `archived` - 已归档

## 标签规范

### 层级标签

```
#python             # Python 相关
  #python/decorator
  #python/learning
  #python/advanced
#ide                # IDE 工具
  #ide/vscode
  #ide/windsurf
  #ide/plugins
#ai                 # AI 工具
  #ai/codeium
  #ai/copilot
  #ai/claude
#algorithm          # 算法
  #algorithm/sort
  #algorithm/search
  #algorithm/tree
#daily              # 日常学习
#todo               # 待办事项
#ubuntu             # Ubuntu/Linux
  #ubuntu/wsl2
  #ubuntu/command
  #ubuntu/troubleshooting
#obsidian           # Obsidian 使用
  #obsidian/templates
  #obsidian/plugins
```

### 标签使用原则

1. **层级清晰** - 使用 `/` 分隔层级
2. **语义明确** - 标签名称要能准确表达内容
3. **数量适中** - 每个笔记 2-5 个标签为宜
4. **统一规范** - 遵循已建立的标签体系

## 模板系统

### 可用模板

| 模板文件 | 用途 | 路径 |
|---------|------|------|
| `daily-note.md` | 日常学习日记 | `templates/daily-note.md` |
| `concept-note.md` | 概念知识点笔记 | `templates/concept-note.md` |
| `troubleshooting.md` | 问题排查笔记 | `templates/troubleshooting.md` |
| `todo.md` | 待办事项 | `templates/todo.md` |

### 笔记类型与模板映射

| 笔记类型 | 目录位置 | 模板文件 | 示例 |
|---------|---------|---------|------|
| 概念知识 | `{主题目录}/concepts/` | `templates/concept-note.md` | Python 装饰器、Git 分支策略 |
| 代码示例 | `{主题目录}/code/` | `templates/concept-note.md` | Python 脚本、配置文件 |
| 问题排查 | `{主题目录}/troubleshooting/` | `templates/troubleshooting.md` | WSL2 内存问题、插件安装失败 |
| 日常日记 | `01-Daily/YYYY/MM/` | `templates/daily-note.md` | 2026-03-15 学习笔记 |

## SOP 检查清单

### 创建笔记前

- [ ] 确认笔记主题和类型
- [ ] 选择正确的模板
- [ ] 定位正确的目录和子目录
- [ ] 确认文件名符合规范

### 创建笔记时

- [ ] 填充完整的 frontmatter
- [ ] 组织内容结构
- [ ] 添加相关标签
- [ ] 检查链接格式

### 创建笔记后

- [ ] 更新对应 README.md
- [ ] 添加正确的双向链接
- [ ] 验证所有链接可点击
- [ ] 检查文件命名和位置

### 验证阶段

- [ ] Frontmatter 完整性检查
- [ ] 双向链接格式验证
- [ ] 标签格式检查
- [ ] 文件命名规范验证
- [ ] 目录位置规则检查

## 常见错误和修正

### 错误 1：README 没有使用双向链接

**症状**：
```markdown
## 目录内容
- 装饰器 - 学习装饰器
```

**修正**：
```markdown
## 目录内容
- [[装饰器]] - 学习装饰器
```

### 错误 2：链接格式不正确

**症状**：
```markdown
- `decorator.py` - 装饰器示例
- [decorator](decorator.py) - 装饰器示例
```

**修正**：
```markdown
- [[decorator.py]] - 装饰器示例
```

### 错误 3：目录顺序错误

**症状**：
```
05-Algorithms/
08-Database/    ← 错误序号
10-Ubuntu/
11-Resources/   ← 错误序号
```

**修正**：
```
05-Algorithms/
06-Database/    ← 正确序号
07-Frameworks/   ← 正确序号
08-Ubuntu/       ← 正确序号
09-Obsidian/     ← 正确序号
10-Todo/         ← 正确序号
11-Resources/    ← 正确序号
```

### 错误 4：文件名不符合规范

**症状**：
```
@python decorator#.md
my file name.md
```

**修正**：
```
装饰器.md
python-decorator.md
decorator.md
```

## 相关资源

- [[docs/knowledge-base-design]] - 知识库结构设计
- [[docs/agent-operations]] - Agent 文档管理操作指南
- [[docs/tags-best-practices]] - Tag 和 Frontmatter 最佳实践
- [[directory-structure]] - 知识库目录结构

---

**创建日期**: 2026-03-15
**最后更新**: 2026-03-15
**版本**: 1.0
