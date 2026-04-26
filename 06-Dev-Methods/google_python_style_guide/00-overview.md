---
title: Google Python Style Guide - 概述
date: 2026-03-15
status: completed
tags: [python, style-guide, google]
source: https://google.github.io/styleguide/pyguide.html
---

# Google Python 风格指南

## 1 Background 背景

Python 是 Google 使用的主要动态语言。本风格指南是 Python 程序的*注意事项清单*。

为了帮助你正确格式化代码，我们创建了 [Vim 设置文件](https://google.github.io/styleguide/google_python_style.vim)。对于 Emacs，默认设置应该就可以了。

许多团队使用 [Black](https://github.com/psf/black) 或 [Pyink](https://github.com/google/pyink) 自动格式化工具来避免格式争议。

---

## 目录索引

### 语言规则 (Python Language Rules)

- [[01-语言规则-上]]
  - 2.1 Lint 代码检查
  - 2.2 Imports 导入
  - 2.3 Packages 包
  - 2.4 Exceptions 异常
  - 2.5 Mutable Global State 可变全局状态
  - 2.6 Nested/Local/Inner Classes and Functions 嵌套/局部/内部类和函数
  - 2.7 Comprehensions & Generator Expressions 推导式和生成器表达式
  - 2.8 Default Iterators and Operators 默认迭代器和操作符
  - 2.9 Generators 生成器
  - 2.10 Lambda Functions Lambda 函数
  - 2.11 Conditional Expressions 条件表达式

- [[02-语言规则-下]]
  - 2.12 Default Argument Values 默认参数值
  - 2.13 Properties 属性
  - 2.14 True/False Evaluations 真/假值判断
  - 2.16 Lexical Scoping 词法作用域
  - 2.17 Function and Method Decorators 函数和方法装饰器
  - 2.18 Threading 线程
  - 2.19 Power Features 高级特性
  - 2.20 Modern Python 现代 Python
  - 2.21 Type Annotated Code 类型注解代码

### 风格规则 (Python Style Rules)

- [[03-风格规则-格式]]
  - 3.1 Semicolons 分号
  - 3.2 Line length 行长度
  - 3.3 Parentheses 括号
  - 3.4 Indentation 缩进
  - 3.5 Blank Lines 空行
  - 3.6 Whitespace 空白字符
  - 3.7 Shebang Line Shebang 行

- [[04-风格规则-注释]]
  - 3.8 Comments and Docstrings 注释和文档字符串

- [[05-风格规则-其他]]
  - 3.10 Strings 字符串
  - 3.11 Files, Sockets, and similar Stateful Resources 文件、套接字和类似的有状态资源
  - 3.12 TODO Comments TODO 注释
  - 3.13 Imports formatting 导入格式化
  - 3.14 Statements 语句
  - 3.15 Accessors 访问器
  - 3.16 Naming 命名
  - 3.17 Main 主函数
  - 3.18 Function length 函数长度
  - 3.19 Type Annotations 类型注解

---

## 相关链接

- [原文链接](https://google.github.io/styleguide/pyguide.html)
- [pylintrc 配置文件](https://google.github.io/styleguide/pylintrc)
- [Black 自动格式化工具](https://github.com/psf/black)
- [Pyink 自动格式化工具](https://github.com/google/pyink)
