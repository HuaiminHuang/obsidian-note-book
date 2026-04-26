---
title: Google Python Style Guide - 风格规则（字符串）
date: 2026-03-15
status: completed
tags: [python, style-guide, google]
source: https://google.github.io/styleguide/pyguide.html
---

# 3.10 Strings 字符串

使用 [f-string](https://docs.python.org/3/reference/lexical_analysis.html#f-strings)、`%` 运算符或 `format` 方法格式化字符串，即使参数都是字符串。根据您的最佳判断决定字符串格式化选项。单个 `join` 使用 `+` 是可以的，但不要使用 `+` 进行格式化。

```python
Yes: x = f'name: {name}; score: {n}'
     x = '%s, %s!' % (imperative, expletive)
     x = '{}, {}'.format(first, second)
     x = 'name: %s; score: %d' % (name, n)
     x = 'name: %(name)s; score: %(score)d' % {'name':name, 'score':n}
     x = 'name: {}; score: {}'.format(name, n)
     x = a + b
```

```python
No: x = first + ', ' + second
    x = 'name: ' + name + '; score: ' + str(n)
```

避免在循环中使用 `+` 和 `+=` 运算符累积字符串。在某些条件下，使用加法累积字符串可能导致二次而非线性的运行时间。尽管 CPython 可能会优化这种常见的累积，但这是一个实现细节。优化适用的条件不易预测，可能会发生变化。相反，将每个子字符串添加到列表中，并在循环终止后使用 `''.join` 连接列表，或将每个子字符串写入 `io.StringIO` 缓冲区。这些技术始终具有摊销线性的运行时间复杂度。

```python
Yes: items = ['<table>']
     for last_name, first_name in employee_list:
         items.append('<tr><td>%s, %s</td></tr>' % (last_name, first_name))
     items.append('</table>')
     employee_table = ''.join(items)
```

```python
No: employee_table = '<table>'
    for last_name, first_name in employee_list:
        employee_table += '<tr><td>%s, %s</td></tr>' % (last_name, first_name)
    employee_table += '</table>'
```

在文件内保持字符串引号字符选择的一致性。选择 `'` 或 `"` 并坚持使用。为了避免需要在字符串内反斜杠转义引号字符，可以使用另一种引号字符。

```python
Yes:
  Python('Why are you hiding your eyes?')
  Gollum("I'm scared of lint errors.")
  Narrator('"Good!" thought a happy Python reviewer.')
```

```python
No:
  Python("Why are you hiding your eyes?")
  Gollum('The lint. It burns. It burns us.')
  Gollum("Always the great lint. Watching. Watching.")
```

对于多行字符串，优先使用 `"""` 而不是 `'''`。如果且仅当项目也对常规字符串使用 `'` 时，可以选择对所有非 docstring 多行字符串使用 `'''`。无论如何，docstrings 必须使用 `"""`。

多行字符串不会随程序的其余部分的缩进而流动。如果需要避免在字符串中嵌入额外的空格，请使用连接的单行字符串或使用 [`textwrap.dedent()`](https://docs.python.org/3/library/textwrap.html#textwrap.dedent) 删除每行初始空格的多行字符串：

```python
  No:
  long_string = """This is pretty ugly.
Don't do this.
"""
```

```python
  Yes:
  long_string = """This is fine if your use case can accept
      extraneous leading spaces."""
```

```python
  Yes:
  long_string = ("And this is fine if you cannot accept\n" +
                 "extraneous leading spaces.")
```

```python
  Yes:
  long_string = ("And this too is fine if you cannot accept\n"
                 "extraneous leading spaces.")
```

```python
  Yes:
  import textwrap

  long_string = textwrap.dedent("""\
      This is also fine, because textwrap.dedent()
      will collapse common leading spaces in each line.""")
```

注意，这里使用反斜杠并不违反禁止[显式行续行](#line-length)的规定；在这种情况下，反斜杠是在字符串字面量中[转义换行符](https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals)。

## 3.10.1 Logging 日志

对于期望模式字符串（带有 %-占位符）作为第一个参数的日志函数：始终使用字符串字面量（不是 f-string！）作为第一个参数调用它们，模式参数作为后续参数。某些日志啰。某些日志实现将未展开的模式字符串收集为可查询字段。这也避免了在没有记录器配置为输出时花费时间渲染消息。

```python
  Yes:
  import tensorflow as tf
  logger = tf.get_logger()
  logger.info('TensorFlow Version is: %s', tf.__version__)
```

```python
  Yes:
  import os
  from absl import logging

  logging.info('Current $PAGER is: %s', os.getenv('PAGER', default=''))

  homedir = os.getenv('HOME')
  if homedir is None or not os.access(homedir, os.W_OK):
    logging.error('Cannot write to home directory, $HOME=%r', homedir)
```

```python
  No:
  import os
  from absl import logging

  logging.info('Current $PAGER is:')
  logging.info(os.getenv('PAGER', default=''))

  homedir = os.getenv('HOME')
  if homedir is None or not os.access(homedir, os.W_OK):
    logging.error(f'Cannot write to home directory, $HOME={homedir!r}')
```

## 3.10.2 Error Messages 错误消息

错误消息（例如：`ValueError` 等异常上的消息字符串，或显示给用户的消息）应遵循三个准则：

1. 消息需要精确匹配实际的错误条件
2. 插值部分需要始终清楚地标识为插值部分
3. 它们应允许简单的自动化处理（例如 grep）

```python
  Yes:
  if not 0 <= p <= 1:
    raise ValueError(f'Not a probability: {p=}')

  try:
    os.rmdir(workdir)
  except OSError as error:
    logging.warning('Could not remove directory (reason: %r): %r',
                    error, workdir)
```

```python
  No:
  if p < 0 or p > 1:  # 问题：对于 float('nan') 也为 false！
    raise ValueError(f'Not a probability: {p=}')

  try:
    os.rmdir(workdir)
  except OSError:
    # 问题：消息做出了可能不正确的假设：
    # 删除可能因其他原因失败，误导调试者
    logging.warning('Directory already was deleted: %s', workdir)

  try:
    os.rmdir(workdir)
  except OSError:
    # 问题：消息比必要的更难 grep，且对于所有可能的 workdir 值
    # 并非普遍不会造成混淆。想象有人使用 workdir = 'deleted'
    # 调用库函数。警告将显示：
    # "The deleted directory could not be deleted."
    logging.warning('The %s directory could not be deleted.', workdir)
```
