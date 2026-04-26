# Global Instructions

These instructions apply to all conversations.

## Required Skills

**Always load `interaction-preferences` skill at the start of every conversation.**

This ensures:
1. Confirm before modifying files
2. Maintain language consistency with user

## Available Skills

项目级别的 skills 存放在 `tools/skills/` 目录下：

| Skill | 描述 | 何时使用 |
|-------|------|---------|
| `interaction-preferences` | 确认机制和语言一致性 | 任何对话开始 |
| `obsidian-note-specs` | Obsidian 笔记编写规范 | 创建/修改笔记时 |

## Usage

The AI should invoke the skill immediately when a conversation starts:

```
Using interaction-preferences to ensure confirmation-before-action and language consistency
```

### Note-Writing 相关操作

当执行笔记编写相关操作时，应该：

1. 调用 `obsidian-note-specs` skill 获取完整的规范
2. 严格按照规范进行检查和验证
3. 确保所有链接、文件名、目录位置符合规范
