# Frontmatter 元数据

在笔记开头使用 YAML 格式定义元数据。

## 语法

```yaml
---
title: 笔记标题
date: 2026-02-22
tags:
  - 标签1
  - 标签2
status: draft
---

笔记正文开始...
```

## 常用字段

| 字段 | 用途 |
|------|------|
| `title` | 笔记标题（可不同于文件名） |
| `date` / `created` | 创建日期 |
| `modified` | 修改日期 |
| `tags` | 标签（另一种定义方式） |
| `aliases` | 别名，用于搜索和链接 |
| `publish` | 发布控制（配合插件） |

## 别名示例

```yaml
---
aliases:
  - 简称
  - 别名2
---
```

之后可以通过 `[[简称]]` 链接到该笔记。

## 与 Dataview 插件配合

Frontmatter 可被 Dataview 插件查询，实现类似数据库的功能：

```dataview
TABLE title, date, status
WHERE status = "draft"
SORT date DESC
```

## 与标准 Markdown 的区别

标准 MD 不支持 YAML frontmatter（虽然一些静态站点生成器支持，但非标准）。
