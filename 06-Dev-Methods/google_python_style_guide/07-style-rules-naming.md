---
title: Google Python Style Guide - 风格规则（命名）
date: 2026-03-15
tags: [python, style-guide, google]
source: https://google.github.io/styleguide/pyguide.html
---

# 3.16 Naming 命名

`module_name`, `package_name`, `ClassName`, `method_name`, `ExceptionName`, `function_name`, `GLOBAL_CONSTANT_NAME`, `global_var_name`, `instance_var_name`, `function_parameter_name`, `local_var_name`, `query_proper_noun_for_thing`, `send_acronym_via_https`.

名称应该具有描述性。这包括函数、类、变量、属性、文件和任何其他类型的命名实体。

避免缩写。特别是，不要使用在项目外部对读者来说模糊或不熟悉的缩写，不要通过删除单词中的字母来缩写。

始终使用 `.py` 文件扩展名。永远不要使用连字符。

## 3.16.1 Names to Avoid 应避免的名称

- 单字符名称，以下情况除外：
    - 计数器或迭代器（例如 `i`, `j`, `k`, `v` 等）
    - `try/except` 语句中作为异常标识符的 `e`
    - `with` 语句中作为文件句柄的 `f`
    - 无约束的私有 [type variables](#typing-type-var)（例如 `_T = TypeVar("_T")`, `_P = ParamSpec("_P")`）
    - 匹配参考论文或算法中既定符号的名称（见[数学符号](#math-notation)）
    
    请注意不要滥用单字符命名。一般来说，描述性应该与名称的可见范围成比例。例如，`i` 可能是 5 行代码块的合适名称，但在多个嵌套作用域中，它可能太模糊了。
    
- 任何包/模块名称中的连字符（`-`）
    
- `__double_leading_and_trailing_underscore__` 名称（Python 保留）
    
- 冒犯性术语
    
- 不必要地包含变量类型的名称（例如：`id_to_name_dict`）

## 3.16.2 Naming Conventions 命名约定

- "Internal" 表示模块内部，或类中的 protected 或 private。
    
- 前置单个下划线（`_`）对保护模块变量和函数有一定支持（linters 会标记 protected 成员访问）。请注意，单元测试可以访问被测模块的 protected 常量。
    
- 前置双下划线（`__`，也称为"dunder"）到实例变量或方法有效地使该变量或方法对其类私有（使用名称修饰）；我们不鼓励使用它，因为它影响可读性和可测试性，并且不是*真正*私有的。优先使用单个下划线。
    
- 将相关的类和顶级函数放在同一个模块中。与 Java 不同，不需要将自己限制为每个模块一个类。
    
- 类名使用 CapWords，但模块名使用 lower_with_under.py。虽然有一些名为 CapWords.py 的旧模块，但现在不鼓励这样做，因为当模块恰好以类命名时会令人困惑。（"等等——我是写了 `import StringIO` 还是 `from StringIO import StringIO`？"）
    
- 新的*单元测试*文件遵循 PEP 8 兼容的 lower_with_under 方法名称，例如 `test_<method_under_test>_<state>`。为了与遵循 CapWords 函数名称的旧模块保持一致（*），可以在以 `test` 开头的方法名称中使用下划线来分隔名称的逻辑组件。一种可能的模式是 `test<MethodUnderTest>_<state>`。

## 3.16.3 File Naming 文件命名

Python 文件名必须具有 `.py` 扩展名，并且不得包含连字符（`-`）。这允许它们被导入和单元测试。如果您希望可执行文件在没有扩展名的情况下可访问，请使用符号链接或包含 `exec "$0.py" "$@"` 的简单 bash 包装器。

## 3.16.4 Guidelines derived from Guido's Recommendations 源自 Guido 建议的指南

| 类型 | Public | Internal |
|------|--------|----------|
| Packages | `lower_with_under` | |
| Modules | `lower_with_under` | `_lower_with_under` |
| Classes | `CapWords` | `_CapWords` |
| Exceptions | `CapWords` | |
| Functions | `lower_with_under()` | `_lower_with_under()` |
| Global/Class Constants | `CAPS_WITH_UNDER` | `_CAPS_WITH_UNDER` |
| Global/Class Variables | `lower_with_under` | `_lower_with_under` |
| Instance Variables | `lower_with_under` | `_lower_with_under` (protected) |
| Method Names | `lower_with_under()` | `_lower_with_under()` (protected) |
| Function/Method Parameters | `lower_with_under` | |
| Local Variables | `lower_with_under` | |

## 3.16.5 Mathematical Notation 数学符号

对于数学密集的代码，当短变量名称匹配参考论文或算法中的既定符号时，即使违反风格指南也是首选。

使用基于既定符号的名称时：

1. 在注释或 docstring 中引用所有命名约定的来源，最好带有指向学术资源本身的超链接。如果来源不可访问，请清楚地记录命名约定。
2. 对于公共 API，优先使用 PEP8 兼容的 `descriptive_names`，因为它们更有可能在上下文之外遇到。
3. 使用范围狭窄的 `pylint: disable=invalid-name` 指令来消除警告。对于少量变量，对每个变量使用行尾注释；对于更多变量，在块的开头应用指令。
