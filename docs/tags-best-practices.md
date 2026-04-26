---
title: Tag 和 Frontmatter 最佳实践
date: 2026-03-14
tags: [docs, best-practices, tags, frontmatter]
status: completed
---

# Tag 和 Frontmatter 最佳实践

## 概述

本文档说明 Tag 和 Frontmatter 的最佳实践。

**详细的规范说明请参见**：[[tools/skills/obsidian-note-specs]]

## 核心原则

### 1. Frontmatter 字段

**必需字段**：
```yaml
---
title: 标题
date: YYYY-MM-DD
tags: [tag1, tag2]
status: learning|completed|archived
---
```

**推荐字段**：
- `difficulty: easy|intermediate|advanced` - 难度
- `time_spent: 2h` - 学习时长

### 2. Tag 规范

**层级结构**：
- 使用 `/` 分隔层级：`#python/decorator`
- 保持简洁，避免过于细分
- 统一使用英文标签

**示例**：
```yaml
tags: [python, decorator, learning]
```

## 常见错误

### Frontmatter 错误

❌ **缺少必需字段**：
```yaml
---
title: 装饰器
# 缺少 tags
---
```

✅ **正确**：
```yaml
---
title: 装饰器
tags: [python, decorator]
---
```

❌ **日期格式错误**：
```yaml
date: 2026/03/14
```

✅ **正确**：
```yaml
date: 2026-03-14
```

### Tag 错误

❌ **使用 `-` 而不是 `/`**：
```yaml
tags: [python-decorator]
```

✅ **正确**：
```yaml
tags: [python/decorator]
```

❌ **中英文混用**：
```yaml
tags: [Python, 学习, 装饰器]
```

✅ **正确**：
```yaml
tags: [python, learning, decorator]
```

❌ **标签过多**（>5个）：
```yaml
tags: [python, learning, decorator, advanced, oop, meta, class, function]
```

✅ **正确**（3-5个）：
```yaml
tags: [python, decorator, learning]
```

## 相关资源

- [[tools/skills/obsidian-note-specs]] - 完整的 Obsidian 笔记规范
- [[docs/quick-reference]] - 快速参考
- [[docs/knowledge-base-design]] - 知识库结构设计

---

**创建日期**: 2026-03-14
**最后更新**: 2026-03-15
**版本**: 2.0
