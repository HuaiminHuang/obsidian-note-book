---
title: Google Python Style Guide - 语言规则（上）
date: 2026-03-15
status: completed
tags: [python, style-guide, google]
source: https://google.github.io/styleguide/pyguide.html
---

# 2 Python Language Rules 语言规则

## 2.1 Lint 代码检查

使用此 [pylintrc](https://google.github.io/styleguide/pylintrc) 配置文件对你的代码运行 `pylint`。

### 2.1.1 Definition 定义

`pylint` 是一个用于查找 Python 源代码中的 bug 和风格问题的工具。它发现的问题通常由 C 和 C++ 等动态性较低的语言的编译器捕获。由于 Python 的动态特性，某些警告可能是不正确的；然而，虚假警告应该相当少见。

### 2.1.2 Pros 优点

捕获容易遗漏的错误，如拼写错误、使用前未赋值的变量等。

### 2.1.3 Cons 缺点

`pylint` 并不完美。为了利用它，有时我们需要绕过它、抑制其警告或修复它。

### 2.1.4 Decision 决策

确保在代码上运行 `pylint`。

如果警告不合适，请抑制它们，以免隐藏其他问题。要抑制警告，可以设置行级注释：

```python
def do_PUT(self):  # WSGI name, so pylint: disable=invalid-name
  ...
```

`pylint` 警告每个都有符号名称标识（`empty-docstring`）。Google 特定的警告以 `g-` 开头。

如果抑制的原因从符号名称中不清楚，请添加解释。

以这种方式抑制的好处是我们可以轻松搜索抑制并重新审视它们。

你可以通过以下方式获取 `pylint` 警告列表：

```bash
pylint --list-msgs
```

要获取特定消息的更多信息，请使用：

```bash
pylint --help-msg=invalid-name
```

优先使用 `pylint: disable` 而不是已弃用的旧形式 `pylint: disable-msg`。

未使用参数的警告可以通过在函数开头删除变量来抑制。始终包含注释解释为什么要删除它。"Unused." 就足够了。例如：

```python
def viking_cafe_order(spam: str, beans: str, eggs: str | None = None) -> str:
    del beans, eggs  # Unused by vikings.
    return spam + spam + spam
```

抑制此警告的其他常见形式包括使用 '`_`' 作为未使用参数的标识符，或在参数名称前加上 '`unused_`' 前缀，或将它们赋值给 '`_`'。这些形式是允许的，但不再鼓励。这些形式会破坏按名称传递参数的调用者，并且不能强制参数实际上未被使用。

---

## 2.2 Imports 导入

仅对包和模块使用 `import` 语句，不对单独的类型、类或函数使用。

### 2.2.1 Definition 定义

用于在模块之间共享代码的重用机制。

### 2.2.2 Pros 优点

命名空间管理约定很简单。每个标识符的来源以一致的方式指示；`x.Obj` 表示对象 `Obj` 定义在模块 `x` 中。

### 2.2.3 Cons 缺点

模块名称仍然可能冲突。某些模块名称不方便过长。

### 2.2.4 Decision 决策

- 使用 `import x` 导入包和模块。
- 使用 `from x import y`，其中 `x` 是包前缀，`y` 是没有前缀的模块名称。
- 在以下任一情况下使用 `from x import y as z`：
  - 要导入两个名为 `y` 的模块。
  - `y` 与当前模块中定义的顶级名称冲突。
  - `y` 与作为公共 API 一部分的常见参数名称冲突（例如 `features`）。
  - `y` 是一个不方便的长名称。
  - `y` 在你的代码上下文中过于通用（例如 `from storage.file_system import options as fs_options`）。
- 仅当 `z` 是标准缩写时使用 `import y as z`（例如 `import numpy as np`）。

例如，模块 `sound.effects.echo` 可以如下导入：

```python
from sound.effects import echo
...
echo.EchoFilter(input, output, delay=0.7, atten=4)
```

不要在导入中使用相对名称。即使模块在同一个包中，也要使用完整的包名称。这有助于防止意外地两次导入一个包。

#### 2.2.4.1 Exemptions 豁免

此规则的豁免：

- 来自以下模块的符号用于支持静态分析和类型检查：
  - [`typing` 模块](#typing-imports)
  - [`collections.abc` 模块](#typing-imports)
  - [`typing_extensions` 模块](https://github.com/python/typing_extensions/blob/main/README.md)
- 来自 [six.moves 模块](https://six.readthedocs.io/#module-six.moves)的重定向。

---

## 2.3 Packages 包

使用模块的完整路径名位置导入每个模块。

### 2.3.1 Pros 优点

避免模块名称冲突或由于模块搜索路径不是作者预期而导致的错误导入。使查找模块更容易。

### 2.3.2 Cons 缺点

使代码部署更困难，因为你必须复制包层次结构。对于现代部署机制来说，这实际上不是问题。

### 2.3.3 Decision 决策

所有新代码都应通过其完整的包名称导入每个模块。

导入应如下所示：

```python
Yes:
  # Reference absl.flags in code with the complete name (verbose).
  import absl.flags
  from doctor.who import jodie

  _FOO = absl.flags.DEFINE_string(...)
```

```python
Yes:
  # Reference flags in code with just the module name (common).
  from absl import flags
  from doctor.who import jodie

  _FOO = flags.DEFINE_string(...)
```

*（假设此文件位于 `doctor/who/` 中，其中也存在 `jodie.py`）*

```python
No:
  # Unclear what module the author wanted and what will be imported.  The actual
  # import behavior depends on external factors controlling sys.path.
  # Which possible jodie module did the author intend to import?
  import jodie
```

尽管在某些环境中会发生这种情况，但不应假设主二进制文件所在的目录在 `sys.path` 中。在这种情况下，代码应假设 `import jodie` 引用的是名为 `jodie` 的第三方或顶级包，而不是本地 `jodie.py`。

---

## 2.4 Exceptions 异常

允许使用异常，但必须谨慎使用。

### 2.4.1 Definition 定义

异常是一种跳出正常控制流以处理错误或其他异常情况的方法。

### 2.4.2 Pros 优点

正常操作代码的控制流不会被错误处理代码弄得杂乱。它还允许控制流在发生特定条件时跳过多个帧，例如，一步从 N 个嵌套函数返回，而不是必须通过管道传递错误代码。

### 2.4.3 Cons 缺点

可能导致控制流令人困惑。在进行库调用时容易遗漏错误情况。

### 2.4.4 Decision 决策

异常必须遵循某些条件：

- 在有意义时使用内置异常类。例如，引发 `ValueError` 以指示编程错误，如违反前置条件，这在验证函数参数时可能发生。

- 不要使用 `assert` 语句代替条件或验证前置条件。它们不能是应用程序逻辑的关键。试金石测试是可以在不破坏代码的情况下删除 `assert`。`assert` 条件[不保证](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)被评估。对于基于 [pytest](https://pytest.org) 的测试，`assert` 是可以的，并且预期用于验证期望。例如：

```python
Yes:
  def connect_to_next_port(self, minimum: int) -> int:
    """Connects to the next available port.

    Args:
      minimum: A port value greater or equal to 1024.

    Returns:
      The new minimum port.

    Raises:
      ConnectionError: If no available port is found.
    """
    if minimum < 1024:
      # Note that this raising of ValueError is not mentioned in the doc
      # string's "Raises:" section because it is not appropriate to
      # guarantee this specific behavioral reaction to API misuse.
      raise ValueError(f'Min. port must be at least 1024, not {minimum}.')
    port = self._find_next_open_port(minimum)
    if port is None:
      raise ConnectionError(
          f'Could not connect to service on port {minimum} or higher.')
    # The code does not depend on the result of this assert.
    assert port >= minimum, (
        f'Unexpected port {port} when minimum was {minimum}.')
    return port
```

```python
No:
  def connect_to_next_port(self, minimum: int) -> int:
    """Connects to the next available port.

    Args:
      minimum: A port value greater or equal to 1024.

    Returns:
      The new minimum port.
    """
    assert minimum >= 1024, 'Minimum port must be at least 1024.'
    # The following code depends on the previous assert.
    port = self._find_next_open_port(minimum)
    assert port is not None
    # The type checking of the return statement relies on the assert.
    return port
```

- 库或包可以定义自己的异常。这样做时，它们必须从现有异常类继承。异常名称应以 `Error` 结尾，不应引入重复（`foo.FooError`）。

- 永远不要使用全捕获 `except:` 语句，或捕获 `Exception` 或 `StandardError`，除非你：
  - 重新引发异常，或
  - 在程序中创建一个隔离点，异常不会传播而是被记录和抑制，例如通过保护其最外层块来防止线程崩溃。

  Python 在这方面非常宽容，`except:` 真的会捕获所有内容，包括拼写错误的名称、sys.exit() 调用、Ctrl+C 中断、unittest 失败以及你根本不想捕获的各种其他异常。

- 最小化 `try`/`except` 块中的代码量。`try` 的主体越大，就越可能由你没想到会引发异常的代码行引发异常。在这些情况下，`try`/`except` 块会隐藏真正的错误。

- 使用 `finally` 子句执行代码，无论 `try` 块中是否引发异常。这通常对清理很有用，即关闭文件。

---

## 2.5 Mutable Global State 可变全局状态

避免可变全局状态。

### 2.5.1 Definition 定义

在程序执行期间可以发生变化的模块级值或类属性。

### 2.5.2 Pros 优点

偶尔有用。

### 2.5.3 Cons 缺点

- 破坏封装：这种设计可能使实现有效目标变得困难。例如，如果全局状态用于管理数据库连接，那么同时连接到两个不同的数据库（例如用于在迁移期间计算差异）就变得困难。类似的问题很容易在全局注册表中出现。

- 有可能在导入期间更改模块行为，因为对全局变量的赋值是在首次导入模块时完成的。

### 2.5.4 Decision 决策

避免可变全局状态。

在那些使用全局状态是合理的罕见情况下，可变全局实体应在模块级别声明或作为类属性，并通过在名称前加上 `_` 使其成为内部的。如有必要，对可变全局状态的外部访问必须通过公共函数或类方法完成。参见下面的 [命名](#316-naming)。请在注释或从注释链接的文档中解释使用可变全局状态的设计原因。

允许并鼓励使用模块级常量。例如：`_MAX_HOLY_HANDGRENADE_COUNT = 3` 用于内部使用常量，或 `SIR_LANCELOTS_FAVORITE_COLOR = "blue"` 用于公共 API 常量。常量必须使用全大写字母和下划线命名。参见下面的 [命名](#316-naming)。

---

## 2.6 Nested/Local/Inner Classes and Functions 嵌套/局部/内部类和函数

当用于闭包局部变量时，嵌套局部函数或类是可以的。内部类是可以的。

### 2.6.1 Definition 定义

类可以在方法、函数或类内部定义。函数可以在方法或函数内部定义。嵌套函数对封闭作用域中定义的变量具有只读访问权限。

### 2.6.2 Pros 优点

允许定义仅在非常有限的范围内使用的实用类和函数。非常 [ADT](https://en.wikipedia.org/wiki/Abstract_data_type) 化。通常用于实现 decorator。

### 2.6.3 Cons 缺点

嵌套函数和类不能直接测试。嵌套会使外部函数更长且可读性更差。

### 2.6.4 Decision 决策

它们是可以的，但有一些注意事项。避免嵌套函数或类，除非用于闭包 `self` 或 `cls` 以外的局部值。不要仅仅为了从模块用户那里隐藏函数而嵌套函数。相反，在模块级别为其名称加上 `_` 前缀，以便测试仍然可以访问它。

---

## 2.7 Comprehensions & Generator Expressions 推导式和生成器表达式

适用于简单情况。

### 2.7.1 Definition 定义

List、Dict 和 Set 推导式以及 generator 表达式提供了一种简洁高效的方式来创建容器类型和迭代器，而无需使用传统循环、`map()`、`filter()` 或 `lambda`。

### 2.7.2 Pros 优点

简单的推导式可以比其他 dict、list 或 set 创建技术更清晰、更简单。Generator 表达式可能非常高效，因为它们完全避免了创建列表。

### 2.7.3 Cons 缺点

复杂的推导式或 generator 表达式可能难以阅读。

### 2.7.4 Decision 决策

允许使用推导式，但不允许多个 `for` 子句或过滤表达式。优化可读性，而不是简洁性。

```python
Yes:
  result = [mapping_expr for value in iterable if filter_expr]

  result = [
      is_valid(metric={'key': value})
      for value in interesting_iterable
      if a_longer_filter_expression(value)
  ]

  descriptive_name = [
      transform({'key': key, 'value': value}, color='black')
      for key, value in generate_iterable(some_input)
      if complicated_condition_is_met(key, value)
  ]

  result = []
  for x in range(10):
    for y in range(5):
      if x * y > 10:
        result.append((x, y))

  return {
      x: complicated_transform(x)
      for x in long_generator_function(parameter)
      if x is not None
  }

  return (x**2 for x in range(10))

  unique_names = {user.name for user in users if user is not None}
```

```python
No:
  result = [(x, y) for x in range(10) for y in range(5) if x * y > 10]

  return (
      (x, y, z)
      for x in range(5)
      for y in range(5)
      if x != y
      for z in range(5)
      if y != z
  )
```

---

## 2.8 Default Iterators and Operators 默认迭代器和操作符

对支持它们的类型（如列表、字典和文件）使用默认迭代器和操作符。

### 2.8.1 Definition 定义

容器类型，如字典和列表，定义默认迭代器和成员测试操作符（"in" 和 "not in"）。

### 2.8.2 Pros 优点

默认迭代器和操作符简单高效。它们直接表达操作，没有额外的方法调用。使用默认操作符的函数是通用的。它可以用于任何支持该操作的类型。

### 2.8.3 Cons 缺点

通过读取方法名称无法判断对象的类型（除非变量有类型注解）。这也是一个优点。

### 2.8.4 Decision 决策

对支持它们的类型（如列表、字典和文件）使用默认迭代器和操作符。内置类型也定义迭代器方法。优先使用这些方法而不是返回列表的方法，但在迭代容器时不应该修改它。

```python
Yes:  for key in adict: ...
      if obj in alist: ...
      for line in afile: ...
      for k, v in adict.items(): ...
```

```python
No:   for key in adict.keys(): ...
      for line in afile.readlines(): ...
```

---

## 2.9 Generators 生成器

根据需要使用 generator。

### 2.9.1 Definition 定义

Generator 函数返回一个迭代器，每次执行 yield 语句时产生一个值。产生一个值后，generator 函数的运行时状态被挂起，直到需要下一个值。

### 2.9.2 Pros 优点

代码更简单，因为每次调用都保留局部变量和控制流的状态。Generator 比一次创建整个值列表的函数使用更少的内存。

### 2.9.3 Cons 缺点

Generator 中的局部变量不会被垃圾回收，直到 generator 被耗尽或本身被垃圾回收。

### 2.9.4 Decision 决策

可以。在 generator 函数的 docstring 中使用 "Yields:" 而不是 "Returns:"。

如果 generator 管理昂贵的资源，请确保强制清理。

进行清理的一个好方法是使用上下文管理器 [PEP-0533](https://peps.python.org/pep-0533/) 包装 generator。

---

## 2.10 Lambda Functions Lambda 函数

适用于单行代码。优先使用 generator 表达式而不是带 `lambda` 的 `map()` 或 `filter()`。

### 2.10.1 Definition 定义

Lambda 在表达式中定义匿名函数，而不是在语句中。

### 2.10.2 Pros 优点

方便。

### 2.10.3 Cons 缺点

比局部函数更难阅读和调试。缺乏名称意味着堆栈跟踪更难理解。表达能力有限，因为函数只能包含一个表达式。

### 2.10.4 Decision 决策

允许使用 Lambda。如果 lambda 函数内的代码跨越多行或超过 60-80 个字符，最好将其定义为常规的 [嵌套函数](#lexical-scoping)。

对于常见操作如乘法，使用 `operator` 模块中的函数而不是 lambda 函数。例如，优先使用 `operator.mul` 而不是 `lambda x, y: x * y`。

---

## 2.11 Conditional Expressions 条件表达式

适用于简单情况。

### 2.11.1 Definition 定义

条件表达式（有时称为"三元运算符"）是为 if 语句提供更短语法的机制。例如：`x = 1 if cond else 2`。

### 2.11.2 Pros 优点

比 if 语句更短、更方便。

### 2.11.3 Cons 缺点

可能比 if 语句更难阅读。如果表达式很长，条件可能难以定位。

### 2.11.4 Decision 决策

适用于简单情况。每个部分必须适合一行：true-expression、if-expression、else-expression。当事情变得更复杂时，使用完整的 if 语句。

```python
Yes:
    one_line = 'yes' if predicate(value) else 'no'
    slightly_split = ('yes' if predicate(value)
                      else 'no, nein, nyet')
    the_longest_ternary_style_that_can_be_done = (
        'yes, true, affirmative, confirmed, correct'
        if predicate(value)
        else 'no, false, negative, nay')
```

```python
No:
    bad_line_breaking = ('yes' if predicate(value) else
                         'no')
    portion_too_long = ('yes'
                        if some_long_module.some_long_predicate_function(
                            really_long_variable_name)
                        else 'no, false, negative, nay')
```

---

[[00-概述|返回目录]]
