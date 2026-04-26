---
name: obsidian-note-specs
description: Obsidian note writing standards and SOP - directory structure, file naming, bidirectional links, frontmatter, tags, and templates
---

# Obsidian Note Specs

## Overview

This skill defines the complete standards for writing notes in the Obsidian vault, including directory structure, file naming, bidirectional links, frontmatter, tag system, template usage, and more.

## When to Use

- **Before creating a new note** - ensure compliance
- **When modifying existing notes** - verify adherence
- **When updating README.md** - ensure correct link format
- **When creating new topic directories** - ensure correct numbering

## Directory Structure

### Current Layout

```
01-Daily/           # Daily study notes
02-Python/          # Python learning
03-IDE-Tools/       # IDE and tools
04-AI-Tools/        # AI tool usage
05-Algorithms/      # Data structures and algorithms
06-Ubuntu/          # Linux/Ubuntu guide
07-Obsidian/        # Obsidian usage guide
08-Todo/            # Todo items
09-Resources/       # Resource collection (always last)
tools/              # Tool configuration (not numbered)
templates/          # Template library
```

### Numbering Rules

1. **01-05**: Learning content (extensible)
2. **06-Ubuntu**: Linux/Ubuntu guide (fixed)
3. **07-Obsidian**: Tool usage guide (fixed)
4. **08-Todo**: Todo items (fixed)
5. **09-Resources**: Resource collection (always last, fixed)

### Adding New Directories

**Allowed position**: Between `05-Algorithms` and `06-Ubuntu`

**Forbidden positions**:
- `06-Ubuntu` (fixed)
- `07-Obsidian` (fixed)
- `08-Todo` (fixed)
- `09-Resources` (always last, fixed)

### Subdirectory Structure

Each topic directory should follow:

```
{topic}/
├── README.md                # Index
├── concepts/                # Conceptual notes
├── code/                    # Code examples
└── troubleshooting/         # Troubleshooting
```

### IDE-Specific Topic Layout

For IDE/tool topics (e.g., `vscode-basic/`), a flat layout is preferred over the standard subdirectory structure when tool-specific notes are organized by feature:

```
{topic}/
├── README.md                # Index
└── *.md                     # Feature notes
```

## File Naming

### General Rules

- **File names MUST be English kebab-case**
- Examples: `vscode-terminal-keybindings-settings.md`, `wsl2-memory-optimization.md`
- Must clearly describe the topic
- Frontmatter `title` may use Chinese (it's note content, not filename)

### Code Files

- Keep original extension: `decorator.py`, `config.json`
- Place in `code/` subdirectory

### Troubleshooting Notes

- Use kebab-case: `wsl2-memory-compression-release.md`
- Place in `troubleshooting/` subdirectory

### Daily Notes

- Format: `YYYY-MM-DD.md`
- Path: `01-Daily/YYYY/MM/YYYY-MM-DD.md`

### Prohibited

- Special characters (`@`, `#`, `$`, `&`, `*`)
- Spaces in filenames
- Excessively long filenames
- Chinese characters in filenames

## Bidirectional Links

### Correct Format

- **Link to peer**: `[[note-name]]`
- **Link to subdirectory file**: `[[subdir/filename]]`
- **Link to directory**: `[[dirname/]]`
- **Code file**: `[[filename.ext]]`
- **With description**: `[[note-name]] - description of what this is`

### Path Rules by Scope

| Scope | Format | Example | Reason |
|-------|--------|---------|--------|
| Same subdir | `[[filename]]` | `[[memory-system-overview]]` | Simple, Obsidian auto-resolves |
| Cross subdir (same topic) | `[[../subdir/filename]]` | `[[../code/whisper-commands]]` | Survives module relocation |
| Cross topic (from topic root README) | `[[topic/subdir/filename]]` | `[[llama.cpp/concepts/qwen3-embedding-local]]` | README at topic root |
| Cross topic (from subdir) | `../../topic/subdir/filename` | `../../llama.cpp/concepts/qwen3-embedding-local` | Navigate up to topic root first |

### Examples

```
topic-root/README.md
  → sibling note:    [[note-name]]
  → sub-note:        [[note-name]]              # Obsidian auto-resolves

topic-root/concepts/note.md
  → same subdir:     [[other-note]]
  → sibling code:    [[../code/script]]
  → troubleshooting: [[../troubleshooting/issue]]

topic-root/troubleshooting/note.md
  → same subdir:     [[other-note]]
  → sibling:         [[../concepts/note]]
```

### Wrong Format

- `装饰器` - missing `[[ ]]`
- `[decorator](decorator.py)` - Markdown link instead of wiki link
- `` `decorator.py` `` - backtick instead of link

### README Link Format

```markdown
## Contents

### Concepts (`concepts/`)
- [[decorator]] - Python decorator basics
- [[closure]] - Closure concepts and usage

### Code (`code/`)
- [[decorator.py]] - Decorator example
- [[closure.py]] - Closure example

### Troubleshooting (`troubleshooting/`)
- [[wsl2-memory-compression-release]] - WSL2 Ubuntu memory compression fix
```

## Frontmatter

### Required Fields

```yaml
---
title: title
date: YYYY-MM-DD
tags: [tag1, tag2]
status: learning|completed|archived
---
```

### Optional Fields

```yaml
---
aliases: [alias1, alias2]
difficulty: easy|intermediate|advanced
time_spent: 2h
source: [official docs, blog]
next_steps: [[related-note]]
related: [[related-note]]
---
```

### Status Values

- `learning` - Currently studying
- `completed` - Study finished
- `archived` - Archived

## Tags

### Tag Hierarchy

```
#python
  #python/decorator
  #python/learning
  #python/advanced
#ide
  #ide/vscode
  #ide/windsurf
  #ide/plugins
#ai
  #ai/codeium
  #ai/copilot
  #ai/claude
#algorithm
  #algorithm/sort
  #algorithm/search
  #algorithm/tree
#daily
#todo
#ubuntu
  #ubuntu/wsl2
  #ubuntu/command
  #ubuntu/troubleshooting
#obsidian
  #obsidian/templates
  #obsidian/plugins
```

### Tag Principles

1. **Hierarchical** - use `/` for levels
2. **Clear semantics** - tag names should express content
3. **Moderate count** - 2-5 tags per note
4. **Consistent** - follow established hierarchy

## Templates

### Available Templates

| File | Purpose | Path |
|------|---------|------|
| `daily-note.md` | Daily study journal | `templates/daily-note.md` |
| `concept-note.md` | Concept/knowledge note | `templates/concept-note.md` |
| `troubleshooting.md` | Troubleshooting note | `templates/troubleshooting.md` |
| `todo.md` | Todo items | `templates/todo.md` |

### Note Type to Template Mapping

| Note Type | Directory | Template | Example |
|-----------|-----------|----------|---------|
| Concept | `{topic}/concepts/` | `templates/concept-note.md` | Python decorators, Git branch strategy |
| Code example | `{topic}/code/` | `templates/concept-note.md` | Python scripts, config files |
| Troubleshooting | `{topic}/troubleshooting/` | `templates/troubleshooting.md` | WSL2 memory issues, plugin install failures |
| Daily journal | `01-Daily/YYYY/MM/` | `templates/daily-note.md` | 2026-03-15 study notes |

## SOP Checklist

### Before Creating

- [ ] Identify note topic and type
- [ ] Select the correct template
- [ ] Choose the correct directory and subdirectory
- [ ] Confirm file name follows the naming convention

### During Creation

- [ ] Fill complete frontmatter
- [ ] Organize content structure
- [ ] Add relevant tags
- [ ] Check link format

### After Creation

- [ ] Update the corresponding README.md
- [ ] Add correct bidirectional links
- [ ] Verify all links are clickable
- [ ] Check file name and location

### Verification

- [ ] Frontmatter completeness
- [ ] Bidirectional link format
- [ ] Tag format
- [ ] File naming convention
- [ ] Directory location rules

## Common Errors

### Error 1: README Missing Wiki Links

**Bad**:
```markdown
## Contents
- Decorator - learn about decorators
```

**Good**:
```markdown
## Contents
- [[decorator]] - learn about decorators
```

### Error 2: Wrong Link Format

**Bad**:
```markdown
- `decorator.py` - decorator example
- [decorator](decorator.py) - decorator example
```

**Good**:
```markdown
- [[decorator.py]] - decorator example
```

### Error 3: Wrong Directory Numbering

**Bad**:
```
05-Algorithms/
08-Database/    ← wrong number
09-Ubuntu/
08-Todo/
10-Resources/   ← wrong number
```

**Good**:
```
05-Algorithms/
06-Database/    ← correct
07-Ubuntu/      ← correct
08-Todo/        ← correct
09-Resources/   ← correct
```

### Error 4: Invalid File Name

**Bad**:
```
@python decorator#.md
my file name.md
```

**Good**:
```
python-decorator.md
decorator.md
```

## Related Resources

- [[docs/knowledge-base-design]] - Knowledge base structure design
- [[docs/agent-operations]] - Agent operation guide
- [[docs/tags-best-practices]] - Tag and frontmatter best practices
- [[directory-structure]] - Vault directory structure

---

**Created**: 2026-03-15
**Updated**: 2026-04-26
**Version**: 1.1