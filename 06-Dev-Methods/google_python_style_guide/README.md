---
title: Google Python Style Guide
date: 2026-03-15
tags: [python, style-guide, google, code-style]
source: https://google.github.io/styleguide/pyguide.html
updated: 2026-03-30
---

# Google Python Style Guide

Google Python 风格指南中文翻译版。

## 原文链接

https://google.github.io/styleguide/pyguide.html

## 目录索引

### Overview

- [[00-overview]] - 背景介绍、工具推荐（Black、Pyink）

### Language Rules (Python Language Rules)

- [[01-language-rules-part1]] - Lint、Imports、Packages、Exceptions、Mutable Global State、Nested Classes、Comprehensions、Default Iterators、Generators、Lambda、Conditional Expressions
- [[02-language-rules-part2]] - Default Arguments、Properties、True/False Evaluations、Lexical Scoping、Decorators、Threading、Power Features、Modern Python、Type Annotated Code

### Style Rules (Python Style Rules)

- [[03-style-rules-formatting]] - Semicolons、Line length、Parentheses、Indentation、Blank Lines、Whitespace、Shebang Line
- [[04-style-rules-comments]] - Comments and Docstrings（Modules、Functions、Classes、Block/Inline Comments）
- [[05-style-rules-strings]] - Strings、Logging、Error Messages
- [[06-style-rules-resources]] - Files/Sockets、TODO Comments、Imports formatting、Statements、Accessors
- [[07-style-rules-naming]] - Naming（Names to Avoid、Naming Conventions、File Naming、Mathematical Notation）
- [[08-style-rules-main-typing]] - Main、Function length、Type Annotations（详细规则）

### Parting Words

- [[09-parting-words]] - Parting Words（保持一致性）

### 学习问答

- [[qa-language-rules]] - 语言规则学习中的疑问与解答

## 快速参考

### 命名约定速查

| 类型 | 风格 | 示例 |
|------|------|------|
| 模块 | lower_with_under | `module_name` |
| 包 | lower_with_under | `package_name` |
| 类 | CapWords | `ClassName` |
| 异常 | CapWords | `ExceptionName` |
| 函数/方法 | lower_with_under() | `method_name()` |
| 常量 | CAPS_WITH_UNDER | `GLOBAL_CONSTANT` |
| 变量 | lower_with_under | `instance_var_name` |

### 关键规则

1. **行长度**: 最大 80 字符
2. **缩进**: 4 空格，禁止制表符
3. **导入**: 每行一个，按标准库→第三方→本地分组
4. **类型注解**: 强烈推荐，特别是公共 API
5. **docstring**: 使用 `"""` 格式，包含 Args/Returns/Raises

## 相关资源

- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Python typing documentation](https://docs.python.org/3/library/typing.html)
- [Black - The uncompromising code formatter](https://github.com/psf/black)
- [Pyink - Google's Python formatter](https://github.com/google/pyink)
