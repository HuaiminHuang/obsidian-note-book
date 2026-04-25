# Callout 信息块

Obsidian 的 Callout 语法用于突出显示重要信息。

## 语法

```markdown
> [!类型] 标题
> 内容
```

## 常用类型

| 类型 | 用途 |
|------|------|
| `note` | 默认，普通注释 |
| `tip` | 提示建议 |
| `warning` | 警告 |
| `danger` | 危险/重要警告 |
| `info` | 信息 |
| `todo` | 待办事项 |
| `success` / `check` | 完成提示 |
| `failure` / `fail` | 失败提示 |
| `bug` | Bug 记录 |
| `example` | 示例 |
| `quote` | 引用 |

## 示例

> [!note] 笔记
> 这是一个普通笔记块

> [!tip] 提示
> 这是一个提示块

> [!warning] 警告
> 这是一个警告块

> [!danger]+ 可折叠（默认展开）
> 点击可折叠

> [!info]- 可折叠（默认收起）
> 点击展开

## 与标准 Markdown 的区别

标准 MD 的 `>` 仅表示引用块，无类型区分和样式渲染。
