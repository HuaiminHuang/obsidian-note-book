---
title: Google Python Style Guide - 风格规则（注释）
date: 2026-03-15
status: completed
tags: [python, style-guide, google]
source: https://google.github.io/styleguide/pyguide.html
---

# 3 Python 风格规则（注释）

## 3.8 Comments and Docstrings 注释和文档字符串

确保对模块、函数、方法 docstring 和内联注释使用正确的风格。

### 3.8.1 Docstrings 文档字符串

Python 使用 *docstrings* 来记录代码。docstring 是作为包、模块、类或函数中第一个语句的字符串。这些字符串可以通过对象的 `__doc__` 成员自动提取，并被 `pydoc` 使用。（尝试在您的模块上运行 `pydoc` 看看它的样子。）始终使用三重双引号 `"""` 格式的 docstrings（根据 [PEP 257](https://peps.python.org/pep-0257/)）。docstring 应该组织为一个摘要行（一个不超过 80 个字符的物理行），以句号、问号或感叹号结尾。当写更多内容时（鼓励这样做），这必须后跟一个空行，然后是 docstring 的其余部分，从第一行第一个引号的相同光标位置开始。下面有更多关于 docstrings 的格式指南。

### 3.8.2 Modules 模块

每个文件都应包含许可证样板。选择项目使用的许可证的适当样板（例如，Apache 2.0、BSD、LGPL、GPL）。

文件应以描述模块内容和使用方法的 docstring 开头。

```python
"""A one-line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

Typical usage example:

  foo = ClassFoo()
  bar = foo.function_bar()
"""
```

#### 3.8.2.1 Test modules 测试模块

测试文件的模块级 docstrings 不是必需的。只有在有额外信息可以提供时才应包含它们。

示例包括关于如何运行测试的一些细节、对不常见设置模式的解释、对外部环境的依赖等。

```python
"""This blaze test uses golden files.

You can update those files by running
`blaze run //foo/bar:foo_test -- --update_golden_files` from the `google3`
directory.
"""
```

不应使用不提供任何新信息的 docstrings。

```python
"""Tests for foo.bar."""
```

### 3.8.3 Functions and Methods 函数和方法

在本节中，"function" 指的是方法、函数、generator 或 property。

对于具有以下一个或多个属性的每个函数，docstring 是强制性的：

- 是公共 API 的一部分
- 非平凡的大小
- 不明显的逻辑

docstring 应该提供足够的信息来编写对函数的调用，而无需阅读函数的代码。docstring 应该描述函数的调用语法及其语义，但通常不描述其实现细节，除非这些细节与如何使用函数相关。例如，作为副作用改变其参数之一的函数应该在其 docstring 中注明。否则，与调用者无关的函数实现的微妙但重要的细节最好作为代码旁边的注释表达，而不是在函数的 docstring 中。

docstring 可以是描述风格（`"""Fetches rows from a Bigtable."""`）或命令风格（`"""Fetch rows from a Bigtable."""`），但风格在文件内应保持一致。`@property` 数据描述符的 docstring 应使用与属性或[函数参数](#doc-function-args)相同的风格（`"""The Bigtable path."""`，而不是 `"""Returns the Bigtable path."""`）。

函数的某些方面应在特殊部分中记录，如下所列。每个部分以标题行开始，以冒号结尾。除标题外的所有部分应保持 2 或 4 个空格的悬挂缩进（在文件内保持一致）。在函数名称和签名足够信息丰富以至于可以使用单行 docstring 适当描述的情况下，可以省略这些部分。

[*Args:*](#doc-function-args)

按名称列出每个参数。描述应在名称之后，并用冒号后跟空格或换行符分隔。如果描述太长无法放在单个 80 字符行上，请使用比参数名称多 2 或 4 个空格的悬挂缩进（与文件中其余 docstrings 保持一致）。如果代码不包含相应的类型注解，描述应包括必需的类型。如果函数接受 `*foo`（可变长度参数列表）和/或 `**bar`（任意关键字参数），它们应列为 `*foo` 和 `**bar`。

[*Returns:* (或 generator 的 *Yields:*)](#doc-function-returns)

描述返回值的语义，包括类型注解未提供的任何类型信息。如果函数只返回 None，则不需要此部分。如果 docstring 以 "Return"、"Returns"、"Yield" 或 "Yields" 开头（例如 `"""Returns row from Bigtable as a tuple of strings."""`）*并且*开头句子足以描述返回值，也可以省略。不要模仿较旧的 'NumPy 风格'（[示例](https://numpy.org/doc/1.24/reference/generated/numpy.linalg.qr.html)），它经常将元组返回值记录为多个具有单独名称的返回值（从不提及元组）。相反，将这样的返回值描述为："Returns: A tuple (mat_a, mat_b), where mat_a is …, and …"。docstring 中的辅助名称不必一定对应于函数体中使用的任何内部名称（因为它们不是 API 的一部分）。如果函数使用 `yield`（是 generator），`Yields:` 部分应该记录 `next()` 返回的对象，而不是调用评估为的 generator 对象本身。

[*Raises:*](#doc-function-raises)

列出与接口相关的所有异常，后跟描述。使用类似的异常名称 + 冒号 + 空格或换行和悬挂缩进风格，如 *Args:* 中所述。您不应该记录在违反 docstring 中指定的 API 时引发的异常（因为这会矛盾地使违反 API 的行为成为 API 的一部分）。

```python
def fetch_smalltable_rows(
    table_handle: smalltable.Table,
    keys: Sequence[bytes | str],
    require_all_keys: bool = False,
) -> Mapping[bytes, tuple[str, ...]]:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle.  String keys will be UTF-8 encoded.

    Args:
        table_handle: An open smalltable.Table instance.
        keys: A sequence of strings representing the key of each table
          row to fetch.  String keys will be UTF-8 encoded.
        require_all_keys: If True only rows with values set for all keys will be
          returned.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {b'Serak': ('Rigel VII', 'Preparer'),
         b'Zim': ('Irk', 'Invader'),
         b'Lrrr': ('Omicron Persei 8', 'Emperor')}

        Returned keys are always bytes.  If a key from the keys argument is
        missing from the dictionary, then that row was not found in the
        table (and require_all_keys must have been False).

    Raises:
        IOError: An error occurred accessing the smalltable.
    """
```

同样，这种带换行的 `Args:` 变体也是允许的：

```python
def fetch_smalltable_rows(
    table_handle: smalltable.Table,
    keys: Sequence[bytes | str],
    require_all_keys: bool = False,
) -> Mapping[bytes, tuple[str, ...]]:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle.  String keys will be UTF-8 encoded.

    Args:
      table_handle:
        An open smalltable.Table instance.
      keys:
        A sequence of strings representing the key of each table row to
        fetch.  String keys will be UTF-8 encoded.
      require_all_keys:
        If True only rows with values set for all keys will be returned.

    Returns:
      A dict mapping keys to the corresponding table row data
      fetched. Each row is represented as a tuple of strings. For
      example:

      {b'Serak': ('Rigel VII', 'Preparer'),
       b'Zim': ('Irk', 'Invader'),
       b'Lrrr': ('Omicron Persei 8', 'Emperor')}

      Returned keys are always bytes.  If a key from the keys argument is
      missing from the dictionary, then that row was not found in the
      table (and require_all_keys must have been False).

    Raises:
      IOError: An error occurred accessing the smalltable.
    """
```

#### 3.8.3.1 Overridden Methods 覆盖的方法

如果方法用 [`@override`](https://typing-extensions.readthedocs.io/en/latest/#override)（来自 `typing_extensions` 或 `typing` 模块）显式装饰，则从基类覆盖方法的方法不需要 docstring，除非覆盖方法的行为实质上改进了基方法的契约，或需要提供细节（例如，记录额外的副作用），在这种情况下，覆盖方法上至少需要包含这些差异的 docstring。

```python
from typing_extensions import override

class Parent:
  def do_something(self):
    """Parent method, includes docstring."""

# Child class, method annotated with override.
class Child(Parent):
  @override
  def do_something(self):
    pass
```

```python
# Child class, but without @override decorator, a docstring is required.
class Child(Parent):
  def do_something(self):
    pass

# Docstring is trivial, @override is sufficient to indicate that docs can be
# found in the base class.
class Child(Parent):
  @override
  def do_something(self):
    """See base class."""
```

### 3.8.4 Classes 类

类应该在类定义下方有一个 docstring 来描述该类。公共属性（不包括 [properties](#properties)）应该在这里的 `Attributes` 部分中记录，并遵循与[函数的 `Args`](#doc-function-args) 部分相同的格式。

```python
class SampleClass:
    """Summary of class here.

    Longer class information...
    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, likes_spam: bool = False):
        """Initializes the instance based on spam preference.

        Args:
          likes_spam: Defines if instance exhibits this preference.
        """
        self.likes_spam = likes_spam
        self.eggs = 0

    @property
    def butter_sticks(self) -> int:
        """The number of butter sticks we have."""
```

所有类的 docstring 应以描述类实例代表什么的单行摘要开始。这意味着 `Exception` 的子类也应该描述异常代表什么，而不是它可能发生的上下文。类 docstring 不应重复不必要的信息，例如该类是一个类。

```python
# Yes:
class CheeseShopAddress:
  """The address of a cheese shop.

  ...
  """

class OutOfCheeseError(Exception):
  """No more cheese is available."""
```

```python
# No:
class CheeseShopAddress:
  """Class that describes the address of a cheese shop.

  ...
  """

class OutOfCheeseError(Exception):
  """Raised when no more cheese is available."""
```

### 3.8.5 Block and Inline Comments 块注释和行内注释

注释的最后一个地方是在代码的棘手部分。如果你要在下一次[code review](http://en.wikipedia.org/wiki/Code_review)时解释它，你现在就应该注释它。复杂的操作在操作开始前会有几行注释。不明显的情况在行尾有注释。

```python
# We use a weighted dictionary search to find out where i is in
# the array.  We extrapolate position based on the largest num
# in the array and the array size and then do binary search to
# get the exact number.

if i & (i-1) == 0:  # True if i is 0 or a power of 2.
```

为了提高可读性，这些注释应该至少距离代码 2 个空格开始，注释字符 `#` 后面至少有一个空格，然后是注释本身的文本。

另一方面，永远不要描述代码。假设阅读代码的人比你更了解 Python（虽然不知道你想要做什么）。

```python
# BAD COMMENT: Now go through the b array and make sure whenever i occurs
# the next element is i+1
```

### 3.8.6 Punctuation, Spelling, and Grammar 标点、拼写和语法

注意标点、拼写和语法；编写良好的注释比编写不良的注释更容易阅读。

注释应该像叙述文本一样可读，具有适当的大写和标点符号。在许多情况下，完整的句子比句子片段更易读。较短的注释，例如代码行尾的注释，有时可以不太正式，但你应该保持风格一致。

虽然让代码审查者指出你应该使用分号而不是逗号可能令人沮丧，但源代码保持高水平的清晰度和可读性非常重要。适当的标点、拼写和语法有助于实现该目标。
