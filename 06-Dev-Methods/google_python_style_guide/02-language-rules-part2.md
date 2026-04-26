---
title: Google Python Style Guide - 语言规则（下）
date: 2026-03-15
status: completed
tags: [python, style-guide, google]
source: https://google.github.io/styleguide/pyguide.html
---

# 2 Python 语言规则（下）

## 2.12 Default Argument Values 默认参数值

在大多数情况下可以使用。

### 2.12.1 定义

可以在函数参数列表的末尾为变量指定默认值，例如 `def foo(a, b=0):`。如果只用一个参数调用 `foo`，则 `b` 被设置为 0。如果用两个参数调用，则 `b` 具有第二个参数的值。

### 2.12.2 优点

通常函数会使用很多默认值，但在极少数情况下需要覆盖这些默认值。默认参数值提供了一种简单的方法来实现这一点，而无需为罕见的例外情况定义大量函数。由于 Python 不支持方法/函数重载，默认参数是实现"模拟"重载行为的简单方法。

### 2.12.3 缺点

默认参数在模块加载时只计算一次。如果参数是可变对象（如列表或字典），这可能会导致问题。如果函数修改了该对象（例如，向列表添加元素），则默认值会被修改。

### 2.12.4 规范

可以使用，但有以下注意事项：

**不要在函数或方法定义中使用可变对象作为默认值。**

```python
Yes: def foo(a, b=None):
         if b is None:
             b = []
Yes: def foo(a, b: Sequence | None = None):
         if b is None:
             b = []
Yes: def foo(a, b: Sequence = ()):  # 空元组可以，因为元组是不可变的
         ...
```

```python
from absl import flags
_FOO = flags.DEFINE_string(...)

No:  def foo(a, b=[]):
         ...
No:  def foo(a, b=time.time()):  # `b` 是要表示模块加载时的时间吗？
         ...
No:  def foo(a, b=_FOO.value):  # sys.argv 还没有被解析...
         ...
No:  def foo(a, b: Mapping = {}):  # 可能仍然被传递到未经检查的代码中
         ...
```

## 2.13 Properties 属性

Properties 可用于控制需要简单计算或逻辑的属性获取或设置。Property 实现必须符合常规属性访问的一般预期：它们应该是廉价的、直接的、不令人惊讶的。

### 2.13.1 定义

一种将获取和设置属性的方法调用包装为标准属性访问的方式。

### 2.13.2 优点

- 允许使用属性访问和赋值 API，而不是 [getter 和 setter](#getters-and-setters) 方法调用
- 可用于使属性只读
- 允许延迟计算
- 提供一种在内部实现独立于类用户演进时维护类公共接口的方法

### 2.13.3 缺点

- 可能会隐藏副作用，就像运算符重载一样
- 可能会令子类困惑

### 2.13.4 规范

允许使用 Properties，但像运算符重载一样，只应在必要时使用，并符合典型属性访问的预期；否则请遵循 [getter 和 setter](#getters-and-setters) 规则。

例如，不允许使用 property 来简单地获取和设置内部属性：没有发生任何计算，因此 property 是不必要的（[改为将属性公开](#getters-and-setters)）。相比之下，使用 property 来控制属性访问或计算一个*简单*派生值是允许的：逻辑简单且不令人惊讶。

Properties 应该使用 `@property` [decorator](#s2.17-function-and-method-decorators) 创建。手动实现 property 描述符被认为是 [power feature](#power-features)。

使用 Properties 的继承可能不明显。不要使用 properties 来实现子类可能想要覆盖和扩展的计算。

## 2.14 True/False Evaluations 真值评估

尽可能使用"隐式" false（但有一些注意事项）。

### 2.14.1 定义

Python 在布尔上下文中将某些值评估为 `False`。一个快速的"经验法则"是所有"空"值都被视为 false，因此 `0, None, [], {}, ''` 在布尔上下文中都评估为 false。

### 2.14.2 优点

使用 Python 布尔值的条件更容易阅读且不易出错。在大多数情况下，它们也更快。

### 2.14.3 缺点

对 C/C++ 开发人员来说可能看起来很奇怪。

### 2.14.4 规范

尽可能使用"隐式" false，例如 `if foo:` 而不是 `if foo != []:`。但请注意以下几点：

- 始终使用 `if foo is None:`（或 `is not None`）来检查 `None` 值。例如，当测试默认为 `None` 的变量或参数是否被设置为其他值时。其他值可能是在布尔上下文中为 false 的值！
    
- 永远不要使用 `==` 将布尔变量与 `False` 进行比较。改用 `if not x:`。如果需要区分 `False` 和 `None`，则链接表达式，例如 `if not x and x is not None:`。
    
- 对于序列（字符串、列表、元组），利用空序列为 false 的事实，所以 `if seq:` 和 `if not seq:` 分别优于 `if len(seq):` 和 `if not len(seq):`。
    
- 处理整数时，隐式 false 可能弊大于利（即意外地将 `None` 处理为 0）。可以将已知为整数的值（且不是 `len()` 的结果）与整数 0 进行比较。
    
    ```python
    Yes: if not users:
             print('no users')
    
         if i % 10 == 0:
             self.handle_multiple_of_ten()
    
         def f(x=None):
             if x is None:
                 x = []
    ```
    
    ```python
    No:  if len(users) == 0:
             print('no users')
    
         if not i % 10:
             self.handle_multiple_of_ten()
    
         def f(x=None):
             x = x or []
    ```
    
- 注意 `'0'`（即作为字符串的 `0`）评估为 true。
    
- 注意 Numpy 数组可能会在隐式布尔上下文中引发异常。测试 `np.array` 是否为空时，最好使用 `.size` 属性（例如 `if not users.size`）。

## 2.16 Lexical Scoping 词法作用域

可以使用。

### 2.16.1 定义

嵌套的 Python 函数可以引用在封闭函数中定义的变量，但不能对它们赋值。变量绑定使用词法作用域解析，即基于静态程序文本。块中对名称的任何赋值都会导致 Python 将对该名称的所有引用视为局部变量，即使使用在赋值之前。如果出现全局声明，则该名称被视为全局变量。

使用此功能的示例：

```python
def get_adder(summand1: float) -> Callable[[float], float]:
    """Returns a function that adds numbers to a given number."""
    def adder(summand2: float) -> float:
        return summand1 + summand2

    return adder
```

### 2.16.2 优点

通常会产生更清晰、更优雅的代码。对于有经验的 Lisp 和 Scheme（以及 Haskell 和 ML 等）程序员来说尤其令人欣慰。

### 2.16.3 缺点

可能导致令人困惑的错误，例如这个基于 [PEP-0227](https://peps.python.org/pep-0227/) 的示例：

```python
i = 4
def foo(x: Iterable[int]):
    def bar():
        print(i, end='')
    # ...
    # 这里有一堆代码
    # ...
    for i in x:  # 啊，i *是* foo 的局部变量，所以这是 bar 看到的
        print(i, end='')
    bar()
```

所以 `foo([1, 2, 3])` 将打印 `1 2 3 3`，而不是 `1 2 3 4`。

### 2.16.4 规范

可以使用。

## 2.17 Function and Method Decorators 函数和方法装饰器

当有明确优势时谨慎使用装饰器。避免使用 `staticmethod` 并限制 `classmethod` 的使用。

### 2.17.1 定义

[函数和方法的装饰器](https://docs.python.org/3/glossary.html#term-decorator)（也称为"`@` 符号"）。一个常见的装饰器是 `@property`，用于将普通方法转换为动态计算的属性。然而，装饰器语法也允许用户定义的装饰器。具体来说，对于某个函数 `my_decorator`：

```python
class C:
    @my_decorator
    def method(self):
        # method body ...
```

等价于：

```python
class C:
    def method(self):
        # method body ...
    method = my_decorator(method)
```

### 2.17.2 优点

优雅地在方法上指定某些转换；转换可能会消除一些重复代码、强制执行不变量等。

### 2.17.3 缺点

装饰器可以对函数的参数或返回值执行任意操作，导致令人惊讶的隐式行为。此外，装饰器在对象定义时执行。对于模块级对象（类、模块函数……），这发生在导入时。装饰器代码中的故障几乎不可能恢复。

### 2.17.4 规范

当有明确优势时谨慎使用装饰器。装饰器应遵循与函数相同的导入和命名指南。装饰器的 docstring 应清楚地说明该函数是装饰器。为装饰器编写单元测试。

避免在装饰器本身中使用外部依赖（例如，不要依赖文件、socket、数据库连接等），因为在装饰器运行时（在导入时，可能来自 `pydoc` 或其他工具），它们可能不可用。使用有效参数调用的装饰器应该（尽可能）保证在所有情况下都能成功。

装饰器是"顶级代码"的一个特例 - 有关更多讨论，请参阅 [main](#s3.17-main)。

除非被迫与现有库中定义的 API 集成，否则永远不要使用 `staticmethod`。改为编写模块级函数。

仅在编写命名构造函数或修改必要全局状态（如进程范围缓存）的类特定例程时使用 `classmethod`。

## 2.18 Threading 线程

不要依赖内置类型的原子性。

虽然 Python 的内置数据类型（如字典）似乎具有原子操作，但在某些情况下它们不是原子的（例如，如果 `__hash__` 或 `__eq__` 被实现为 Python 方法），不应依赖它们的原子性。也不应该依赖原子变量赋值（因为这又依赖于字典）。

使用 `queue` 模块的 `Queue` 数据类型作为线程间通信数据的首选方式。否则，使用 `threading` 模块及其锁定原语。优先使用条件变量和 `threading.Condition`，而不是使用低级锁。

## 2.19 Power Features 高级特性

避免使用这些特性。

### 2.19.1 定义

Python 是一种极其灵活的语言，提供了许多高级特性，如自定义 metaclass、访问字节码、即时编译、动态继承、对象重新父级化、import hack、反射（例如 `getattr()` 的某些使用）、修改系统内部、实现自定义清理的 `__del__` 方法等。

### 2.19.2 优点

这些是强大的语言特性。它们可以使代码更紧凑。

### 2.19.3 缺点

在不绝对必要时使用这些"酷"特性是非常诱人的。使用不寻常特性的代码更难阅读、理解和调试。起初（对原作者来说）似乎不是这样，但在重新访问代码时，它往往比更长但直接的代码更难。

### 2.19.4 规范

在代码中避免使用这些特性。

内部使用这些特性的标准库模块和类可以使用（例如，`abc.ABCMeta`、`dataclasses` 和 `enum`）。

## 2.20 Modern Python: from \_\_future\_\_ imports 现代 Python

新的语言版本语义更改可能会被特殊的 future import 限制，以便在早期运行时中按文件启用它们。

### 2.20.1 定义

能够通过 `from __future__ import` 语句启用一些更现代的特性，允许早期使用预期未来 Python 版本的特性。

### 2.20.2 优点

这已被证明可以使运行时版本升级更顺畅，因为更改可以按文件进行，同时声明兼容性并防止这些文件内的回归。现代代码更易于维护，因为它不太可能积累在将来运行时升级期间会有问题的技术债务。

### 2.20.3 缺点

这样的代码可能无法在引入所需 future 语句之前的非常旧的解释器版本上运行。对于支持极其广泛环境的项目来说，这种需求更常见。

### 2.20.4 规范

鼓励使用 `from __future__ import` 语句。它允许给定的源文件今天开始使用更现代的 Python 语法特性。一旦您不再需要在隐藏在 `__future__` import 之后的特性的版本上运行，可以随意删除这些行。

在可能在 3.5 而不是 >= 3.7 的版本上执行的代码中，导入：

```python
from __future__ import generator_stop
```

有关更多信息，请阅读 [Python future statement definitions](https://docs.python.org/3/library/__future__.html) 文档。

在确信代码只在足够现代的环境中使用之前，请不要删除这些导入。即使您今天没有在代码中使用特定 future import 启用的特性，将其保留在文件中可以防止以后对代码的修改无意中依赖于旧行为。

根据需要使用其他 `from __future__` import 语句。

## 2.21 Type Annotated Code 类型注解代码

您可以使用 [type hints](https://docs.python.org/3/library/typing.html) 注解 Python 代码。在构建时使用类型检查工具（如 [pytype](https://github.com/google/pytype)）对代码进行类型检查。在大多数情况下，如果可行，类型注解放在源文件中。对于第三方或扩展模块，注解可以放在 [stub `.pyi` 文件](https://peps.python.org/pep-0484/#stub-files)中。

### 2.21.1 定义

类型注解（或"type hints"）用于函数或方法参数和返回值：

```python
def func(a: int) -> list[int]:
```

您也可以使用类似的语法声明变量的类型：

```python
a: SomeType = some_func()
```

### 2.21.2 优点

类型注解提高了代码的可读性和可维护性。类型检查器会将许多运行时错误转换为构建时错误，并减少您使用 [Power Features](#power-features) 的能力。

### 2.21.3 缺点

您必须保持类型声明最新。您可能会看到您认为是有效代码的类型错误。使用 [type checker](https://github.com/google/pytype) 可能会减少您使用 [Power Features](#power-features) 的能力。

### 2.21.4 规范

强烈鼓励在更新代码时启用 Python 类型分析。在添加或修改公共 API 时，包括类型注解并在构建系统中通过 pytype 启用检查。由于静态分析对 Python 来说相对较新，我们承认不良副作用（如错误推断的类型）可能会阻止某些项目的采用。在这些情况下，鼓励作者在 BUILD 文件或代码本身中添加带有 TODO 的注释或链接到描述当前阻止类型注解采用的问题的 bug。
