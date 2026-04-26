---
title: Templates 插件使用指南
tags: [obsidian, templates, plugin]
date: 2026-03-15
status: completed
---

# Templates 插件使用指南

## 配置步骤

### 1. 确认 Templates 插件设置
1. 打开 Obsidian 设置（`Ctrl/Cmd + ,`）
2. 点击 **核心插件**
3. 找到 **Templates** 并确保它已开启（开关为蓝色）
4. 点击 **Templates** 进入插件设置

### 2. 配置模板文件夹
在 Templates 设置中：
- **Template folder location** → 应该显示 `templates`
- 如果没有，点击文件夹图标选择 `templates` 目录

### 3. 尝试使用模板
设置完成后：
1. `Ctrl/Cmd + P` 打开命令面板
2. 输入 `template`
3. 选择 **Insert template**
4. 应该能看到 4 个模板选项：
   - `concept-note.md` - 概念知识点笔记
   - `daily-note.md` - 日常学习日记
   - `todo.md` - 待办事项
   - `troubleshooting.md` - 问题排查笔记

## 可用模板

### daily-note.md
用途：日常学习日记
```markdown
---
tags: [daily, learning]
---

# {{date}} - 学习{{title}}

## 学习内容

...

## 关键知识点

- 知识点1 [相关笔记](../02-Python/concepts/)
- 知识点2 [相关笔记](../02-Python/concepts/)

## 代码示例

```python
# 代码示例
...
```

## 待办事项

- [ ] 任务1
- [ ] 任务2

## 后续计划

...
```

### concept-note.md
用途：概念知识点笔记

### troubleshooting.md
用途：问题排查笔记

### todo.md
用途：待办事项

## 注意事项

### 如果模板列表为空
1. 确认 `templates/` 目录存在且有 `.md` 文件
2. 检查 Templates 插件设置中的文件夹路径
3. 完全关闭并重新打开 Obsidian

### 如果"无效属性"警告
这是正常现象，因为 `{{date}}`、`{{title}}` 是变量占位符，创建笔记时会自动替换。

## 替代方案

如果 Templates 插件一直有问题，可以直接**手动创建笔记**，复制相应模板的内容。

---

**文档创建**: 2026-03-14
**最后更新**: 2026-03-14
