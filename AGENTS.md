# Global Instructions

These instructions apply to all conversations.

## Language

- Reply in the same language the user uses (Chinese → Chinese, English → English)
- Code comments follow the user's language
- Technical terms may keep original language

## Confirmation Before Modification

Before modifying files or executing destructive commands:

1. Present the plan first
2. Wait for user confirmation
3. Then execute

Exceptions (no confirmation needed):
- User explicitly says "直接改", "执行", "开始"
- Running under `ultrawork` / `ulw` mode (OmO handles its own workflow)
- Read-only operations (search, list, read)

## Skill Discovery

When available skills or plugins are relevant to the current task, proactively load and follow them.
Do not limit yourself to any single skill — check for all applicable skills before responding.

## Priority

1. User's explicit instructions (AGENTS.md, direct requests) — highest
2. OmO plugin orchestration — drives workflow in ultrawork mode
3. Superpowers skills — provide discipline workflows when applicable
4. Default behavior — lowest
