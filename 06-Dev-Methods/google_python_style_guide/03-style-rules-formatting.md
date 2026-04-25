---
title: Google Python Style Guide - 风格规则（格式）
date: 2026-03-15
tags: [python, style-guide, google]
source: https://google.github.io/styleguide/pyguide.html
---

# 3 Python 风格规则（格式）

## 3.1 Semicolons 分号

不要用分号终止行，也不要用分号将两个语句放在同一行。

## 3.2 Line length 行长度

最大行长度为 *80 个字符*。

80 字符限制的明确例外：

- 长导入语句
- 注释中的 URL、路径名或长标志
- 不包含空格的长字符串模块级常量，这些常量不方便跨行拆分，如 URL 或路径名
    - Pylint 禁用注释（例如：`# pylint: disable=invalid-name`）

不要使用反斜杠进行[显式行续行](https://docs.python.org/3/reference/lexical_analysis.html#explicit-line-joining)。

相反，利用 Python 在括号、方括号和大括号内的[隐式行连接](http://docs.python.org/reference/lexical_analysis.html#implicit-line-joining)。如有必要，可以在表达式周围添加额外的括号对。

注意，此规则不禁止字符串内的反斜杠转义换行符（见[下文](#strings)）。

```python
Yes: foo_bar(self, width, height, color='black', design=None, x='foo',
             emphasis=None, highlight=0)
```

```python
Yes: if (width == 0 and height == 0 and
         color == 'red' and emphasis == 'strong'):

     (bridge_questions.clarification_on
      .average_airspeed_of.unladen_swallow) = 'African or European?'

     with (
         very_long_first_expression_function() as spam,
         very_long_second_expression_function() as beans,
         third_thing() as eggs,
     ):
       place_order(eggs, beans, spam, beans)
```

```python
No:  if width == 0 and height == 0 and \
         color == 'red' and emphasis == 'strong':

     bridge_questions.clarification_on \
         .average_airspeed_of.unladen_swallow = 'African or European?'

     with very_long_first_expression_function() as spam, \
           very_long_second_expression_function() as beans, \
           third_thing() as eggs:
       place_order(eggs, beans, spam, beans)
```

当字面字符串无法放在一行时，使用括号进行隐式行连接。

```python
x = ('This will build a very long long '
     'long long long long long long string')
```

优先在尽可能高的语法级别断行。如果必须断行两次，请在相同的语法级别断行。

```python
Yes: bridgekeeper.answer(
         name="Arthur", quest=questlib.find(owner="Arthur", perilous=True))

     answer = (a_long_line().of_chained_methods()
               .that_eventually_provides().an_answer())

     if (
         config is None
         or 'editor.language' not in config
         or config['editor.language'].use_spaces is False
     ):
       use_tabs()
```

```python
No: bridgekeeper.answer(name="Arthur", quest=questlib.find(
        owner="Arthur", perilous=True))

    answer = a_long_line().of_chained_methods().that_eventually_provides(
        ).an_answer()

    if (config is None or 'editor.language' not in config or config[
        'editor.language'].use_spaces is False):
      use_tabs()
```

在注释中，如有必要，将长 URL 放在单独的行上。

```python
Yes:  # See details at
      # http://www.example.com/us/developer/documentation/api/content/v2.0/csv_file_name_extension_full_specification.html
```

```python
No:  # See details at
     # http://www.example.com/us/developer/documentation/api/content/\
     # v2.0/csv_file_name_extension_full_specification.html
```

注意上面行续行示例中元素的缩进；有关说明，请参阅[缩进](#s3.4-indentation)部分。

[Docstring](#docstrings) 摘要行必须保持在 80 字符限制内。

在所有其他情况下，如果一行超过 80 个字符，并且 [Black](https://github.com/psf/black) 或 [Pyink](https://github.com/google/pyink) 自动格式化程序无法帮助将行降低到限制以下，则允许该行超过此最大值。鼓励作者在合理的情况下按照上述说明手动断行。

## 3.3 Parentheses 括号

谨慎使用括号。

在元组周围使用括号是可以的，虽然不是必需的。不要在 return 语句或条件语句中使用它们，除非使用括号进行隐式行续行或指示元组。

```python
Yes: if foo:
         bar()
     while x:
         x = bar()
     if x and y:
         bar()
     if not x:
         bar()
     # 对于单项元组，() 比逗号更明显
     onesie = (foo,)
     return foo
     return spam, beans
     return (spam, beans)
     for (x, y) in dict.items(): ...
```

```python
No:  if (x):
         bar()
     if not(x):
         bar()
     return (foo)
```

## 3.4 Indentation 缩进

用 *4 个空格*缩进代码块。

永远不要使用制表符。隐式行续行应该垂直对齐包装的元素（见[行长度示例](#s3.2-line-length)），或使用悬挂的 4 空格缩进。闭合的（圆、方或花）括号可以放在表达式的末尾，或放在单独的行上，但应与相应开放括号的行缩进相同。

```python
Yes:   # 与开放分隔符对齐
       foo = long_function_name(var_one, var_two,
                                var_three, var_four)
       meal = (spam,
               beans)

       # 与字典中的开放分隔符对齐
       foo = {
           'long_dictionary_key': value1 +
                                  value2,
           ...
       }

       # 4 空格悬挂缩进；第一行没有内容
       foo = long_function_name(
           var_one, var_two, var_three,
           var_four)
       meal = (
           spam,
           beans)

       # 4 空格悬挂缩进；第一行没有内容，
       # 闭合括号在新行上
       foo = long_function_name(
           var_one, var_two, var_three,
           var_four
       )
       meal = (
           spam,
           beans,
       )

       # 字典中的 4 空格悬挂缩进
       foo = {
           'long_dictionary_key':
               long_dictionary_value,
           ...
       }
```

```python
No:    # 第一行禁止有内容
       foo = long_function_name(var_one, var_two,
           var_three, var_four)
       meal = (spam,
           beans)

       # 禁止 2 空格悬挂缩进
       foo = long_function_name(
         var_one, var_two, var_three,
         var_four)

       # 字典中没有悬挂缩进
       foo = {
           'long_dictionary_key':
           long_dictionary_value,
           ...
       }
```

### 3.4.1 Trailing commas in sequences of items 序列项中的尾随逗号

仅当闭合容器标记 `]`、`)` 或 `}` 与最后一个元素不在同一行时，以及对于具有单个元素的元组，才建议在序列项中使用尾随逗号。尾随逗号的存在也用作 Python 代码自动格式化程序 [Black](https://github.com/psf/black) 或 [Pyink](https://github.com/google/pyink) 的提示，以在最后一个元素之后存在 `,` 时将项目容器自动格式化为每行一个项目。

```python
Yes:   golomb3 = [0, 1, 3]
       golomb4 = [
           0,
           1,
           4,
           6,
       ]
```

```python
No:    golomb4 = [
           0,
           1,
           4,
           6,]
```

## 3.5 Blank Lines 空行

顶级定义之间（无论是函数还是类定义）使用两个空行。方法定义之间以及 `class` 的 docstring 和第一个方法之间使用一个空行。`def` 行后没有空行。在函数或方法内根据您的判断使用单个空行。

空行不必固定在定义上。例如，紧接在函数、类和方法定义之前的相关注释可能有意义。考虑您的注释作为 docstring 的一部分是否更有用。

## 3.6 Whitespace 空格

遵循标点符号周围空格使用的标准排版规则。

括号、方括号或大括号内没有空格。

```python
Yes: spam(ham[1], {'eggs': 2}, [])
```

```python
No:  spam( ham[ 1 ], { 'eggs': 2 }, [ ] )
```

逗号、分号或冒号前没有空格。在逗号、分号或冒号后使用空格，行尾除外。

```python
Yes: if x == 4:
         print(x, y)
     x, y = y, x
```

```python
No:  if x == 4 :
         print(x , y)
     x , y = y , x
```

开始参数列表、索引或切片的开放括号/方括号前没有空格。

```python
Yes: spam(1)
```

```python
No:  spam (1)
```

```python
Yes: dict['key'] = list[index]
```

```python
No:  dict ['key'] = list [index]
```

没有尾随空格。

对于赋值（`=`）、比较（`==, <, >, !=, <>, <=, >=, in, not in, is, is not`）和布尔值（`and, or, not`），在二元运算符周围使用单个空格。对于算术运算符（`+`, `-`, `*`, `/`, `//`, `%`, `**`, `@`）周围空格的插入，请使用您更好的判断。

```python
Yes: x == 1
```

```python
No:  x<1
```

在传递关键字参数或定义默认参数值时，永远不要在 `=` 周围使用空格，但有一个例外：[当存在类型注解时](#typing-default-values)，默认参数值的 `=` 周围*要*使用空格。

```python
Yes: def complex(real, imag=0.0): return Magic(r=real, i=imag)
Yes: def complex(real, imag: float = 0.0): return Magic(r=real, i=imag)
```

```python
No:  def complex(real, imag = 0.0): return Magic(r = real, i = imag)
No:  def complex(real, imag: float=0.0): return Magic(r = real, i = imag)
```

不要使用空格在连续行上垂直对齐标记，因为这会成为维护负担（适用于 `:`、`#`、`=` 等）：

```python
Yes:
  foo = 1000  # comment
  long_name = 2  # comment that should not be aligned

  dictionary = {
      'foo': 1,
      'long_name': 2,
  }
```

```python
No:
  foo       = 1000  # comment
  long_name = 2     # comment that should not be aligned

  dictionary = {
      'foo'      : 1,
      'long_name': 2,
  }
```

## 3.7 Shebang Line Shebang 行

大多数 `.py` 文件不需要以 `#!` 行开头。使用 `#!/usr/bin/env python3`（以支持 virtualenv）或 `#!/usr/bin/python3`（根据 [PEP-394](https://peps.python.org/pep-0394/)）启动程序的主文件。

此行被内核用于查找 Python 解释器，但在导入模块时被 Python 忽略。它仅在打算直接执行的文件上是必需的。
