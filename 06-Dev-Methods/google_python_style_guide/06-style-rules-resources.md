---
title: Google Python Style Guide - 风格规则（资源管理）
date: 2026-03-15
tags: [python, style-guide, google]
source: https://google.github.io/styleguide/pyguide.html
---

# 3.11 Files, Sockets, and similar Stateful Resources 文件、Socket 和类似的有状态资源

完成后显式关闭文件和 socket。此规则自然扩展到内部使用 socket 的可关闭资源（如数据库连接），以及需要以类似方式关闭的其他资源。仅举几个例子，这也包括 [mmap](https://docs.python.org/3/library/mmap.html) 映射、[h5py File objects](https://docs.h5py.org/en/stable/high/file.html) 和 [matplotlib.pyplot figure windows](https://matplotlib.org/2.1.0/api/_as_gen/matplotlib.pyplot.close.html)。

不必要地保持文件、socket 或其他此类有状态对象打开有许多缺点：

- 它们可能消耗有限的系统资源，如文件描述符。如果不及时将资源归还给系统，处理许多此类对象的代码可能会不必要地耗尽这些资源。
- 保持文件打开可能会阻止其他操作，如移动或删除它们，或卸载文件系统。
- 在整个程序中共享的文件和 socket 可能会在逻辑关闭后被无意中读取或写入。如果它们实际上已关闭，则读取或写入它们的尝试将引发异常，从而更快地发现问题。

此外，虽然文件和 socket（以及一些类似行为的资源）在对象被销毁时会自动关闭，但将对象的生命周期与资源状态耦合是不良做法：

- 无法保证运行时何时实际调用 `__del__` 方法。不同的 Python 实现使用不同的内存管理技术，如延迟垃圾回收，这可能会任意和无限期地增加对象的生命周期。
- 对文件的意外引用（例如在全局变量或异常回溯中）可能会使其保留时间超过预期。

依靠终结器执行具有可观察副作用的自动清理已被反复发现会导致重大问题，跨越数十年和多种语言（参见例如 [Java 的这篇文章](https://wiki.sei.cmu.edu/confluence/display/java/MET12-J.+Do+not+use+finalizers)）。

管理文件和类似资源的首选方式是使用 [`with` 语句](http://docs.python.org/reference/compound_stmts.html#the-with-statement)：

```python
with open("hello.txt") as hello_file:
    for line in hello_file:
        print(line)
```

对于不支持 `with` 语句的类文件对象，使用 `contextlib.closing()`：

```python
import contextlib

with contextlib.closing(urllib.urlopen("http://www.python.org/")) as front_page:
    for line in front_page:
        print(line)
```

在极少数情况下，如果无法进行基于上下文的资源管理，代码文档必须清楚地解释资源生命周期是如何管理的。

# 3.12 TODO Comments TODO 注释

对于临时的、短期解决方案的、或足够好但不完美的代码，使用 `TODO` 注释。

`TODO` 注释以全大写的单词 `TODO` 开头，后跟冒号，以及包含上下文的资源链接（最好是 bug 引用）。bug 引用更好，因为 bug 会被跟踪并有后续评论。在此上下文之后，用连字符 `-` 引入解释性字符串。目的是有一个一致的 `TODO` 格式，可以搜索以找出如何获取更多详细信息。

```python
# TODO: crbug.com/192795 - Investigate cpufreq optimizations.
```

旧风格，以前推荐，但现在不鼓励在新代码中使用：

```python
# TODO(crbug.com/192795): Investigate cpufreq optimizations.
# TODO(yourusername): Use a "\*" here for concatenation operator.
```

避免添加引用个人或团队作为上下文的 TODO：

```python
# TODO: @yourusername - File an issue and use a '*' for repetition.
```

如果您的 `TODO` 是"在将来的某个日期做某事"的形式，请确保您包含一个非常具体的日期（"Fix by November 2009"）或一个非常具体的事件（"Remove this code when all clients can handle XML responses."），以便未来的代码维护者能够理解。Issues 是跟踪此内容的理想选择。

# 3.13 Imports formatting 导入格式

导入应该在单独的行上；[`typing` 和 `collections.abc` 导入](#typing-imports)有例外。

例如：

```python
Yes: from collections.abc import Mapping, Sequence
     import os
     import sys
     from typing import Any, NewType
```

```python
No:  import os, sys
```

导入总是放在文件的顶部，就在任何模块注释和 docstrings 之后，模块全局变量和常量之前。导入应该从最通用到最不通用分组：

1. Python future import 语句。例如：
   ```python
   from __future__ import annotations
   ```
   有关更多信息，请参阅[上文](#from-future-imports)。

2. Python 标准库导入。例如：
   ```python
   import sys
   ```

3. [第三方](https://pypi.org/) 模块或包导入。例如：
   ```python
   import tensorflow as tf
   ```

4. 代码仓库子包导入。例如：
   ```python
   from otherproject.ai import mind
   ```

5. **已弃用：** 与此文件属于同一顶级子包的应用程序特定导入。例如：
   ```python
   from myproject.backend.hgwells import time_machine
   ```
   您可能会发现旧的 Google Python Style 代码这样做，但现在不再需要。**新代码不需要这样做。** 只需将应用程序特定的子包导入与其他子包导入相同对待。

在每个分组内，导入应该按照每个模块的完整包路径（`from path import ...` 中的 `path`）按字母顺序排序，忽略大小写。代码可以选择在导入部分之间放置空行。

```python
import collections
import queue
import sys

from absl import app
from absl import flags
import bs4
import cryptography
import tensorflow as tf

from book.genres import scifi
from myproject.backend import huxley
from myproject.backend.hgwells import time_machine
from myproject.backend.state_machine import main_loop
from otherproject.ai import body
from otherproject.ai import mind
from otherproject.ai import soul

# Older style code may have these imports down here instead:
#from myproject.backend.hgwells import time_machine
#from myproject.backend.state_machine import main_loop
```

# 3.14 Statements 语句

通常每行一个语句。

但是，只有当整个语句适合放在一行时，才可以将测试结果与测试放在同一行。特别是，对于 `try`/`except` 永远不能这样做，因为 `try` 和 `except` 不能同时放在同一行，对于 `if`，只有在没有 `else` 的情况下才能这样做。

```python
Yes:
  if foo: bar(foo)
```

```python
No:
  if foo: bar(foo)
  else:   baz(foo)

  try:               bar(foo)
  except ValueError: baz(foo)

  try:
      bar(foo)
  except ValueError: baz(foo)
```

# 3.15 Getters and Setters 访问器和设置器

Getter 和 setter 函数（也称为访问器和修改器）应在它们为获取或设置变量值提供有意义角色或行为时使用。

特别是，当获取或设置变量很复杂或成本很高（无论是当前还是在合理的未来）时，应该使用它们。

例如，如果一对 getters/setters 只是读取和写入内部属性，则应该将内部属性公开。相比之下，如果设置变量意味着某些状态被无效化或重建，则它应该是一个 setter 函数。函数调用暗示正在发生潜在的非平凡操作。或者，当需要简单逻辑时，[properties](#properties) 可能是一个选项，或者重构为不再需要 getters 和 setters。

Getters 和 setters 应遵循 [Naming](#s3.16-naming) 指南，例如 `get_foo()` 和 `set_foo()`。

如果过去的行为允许通过属性访问，则不要将新的 getter/setter 函数绑定到该属性。任何仍然尝试通过旧方法访问变量的代码应该明显失败，以便他们意识到复杂性的变化。
