---
title: Google Python Style Guide - 风格规则（Main 和类型注解）
date: 2026-03-15
tags: [python, style-guide, google]
source: https://google.github.io/styleguide/pyguide.html
---

# 3.17 Main 主函数

在 Python 中，`pydoc` 和单元测试都要求模块是可导入的。如果文件打算作为可执行文件使用，其主要功能应该在 `main()` 函数中，并且代码应该始终在执行主程序之前检查 `if __name__ == '__main__'`，以便在模块被导入时不执行。

使用 [absl](https://github.com/abseil/abseil-py) 时，使用 `app.run`：

```python
from absl import app
...

def main(argv: Sequence[str]):
    # process non-flag arguments
    ...

if __name__ == '__main__':
    app.run(main)
```

否则，使用：

```python
def main():
    ...

if __name__ == '__main__':
    main()
```

所有顶级代码在模块被导入时都会执行。注意不要调用函数、创建对象或执行其他在文件被 `pydoc` 处理时不应该执行的操作。

# 3.18 Function length 函数长度

偏好小型和专注的函数。

我们认识到长函数有时是合适的，因此对函数长度没有硬性限制。如果函数超过约 40 行，请考虑是否可以在不损害程序结构的情况下拆分它。

即使您的长函数现在完美运行，几个月后修改它的人可能会添加新行为。这可能导致难以发现的错误。保持函数短小简单使其他人更容易阅读和修改您的代码。

您可能会在处理某些代码时发现长而复杂的函数。不要被修改现有代码所吓倒：如果使用此类函数证明很困难，您发现错误难以调试，或者您想在多个不同上下文中使用其中的一部分，请考虑将函数拆分为更小、更易于管理的部分。

# 3.19 Type Annotations 类型注解

## 3.19.1 General Rules 通用规则

- 熟悉 [type hints](https://docs.python.org/3/library/typing.html)。
    
- 通常不需要注解 `self` 或 `cls`。如果需要正确的类型信息，可以使用 [`Self`](https://docs.python.org/3/library/typing.html#typing.Self)，例如：
    
    ```python
    from typing import Self

    class BaseClass:
      @classmethod
      def create(cls) -> Self:
        ...

      def difference(self, other: Self) -> float:
        ...
    ```
    
- 同样，不需要注解 `__init__` 的返回值（其中 `None` 是唯一有效的选项）。
    
- 如果任何其他变量或返回类型不应表达，请使用 `Any`。
    
- 您不需要注解模块中的所有函数。
    
    - 至少注解您的公共 API。
    - 使用判断在安全性和清晰度与灵活性之间取得良好平衡。
    - 注解容易出现类型相关错误的代码（以前的 bug 或复杂性）。
    - 注解难以理解的代码。
    - 从类型角度来看稳定时注解代码。在许多情况下，您可以在不失去太多灵活性的情况下注解成熟代码中的所有函数。

## 3.19.2 Line Breaking 换行

尝试遵循现有的[缩进](#indentation)规则。

注解后，许多函数签名将变成"每个参数一行"。为确保返回类型也有自己的行，可以在最后一个参数后放置逗号。

```python
def my_method(
    self,
    first_var: int,
    second_var: Foo,
    third_var: Bar | None,
) -> int:
  ...
```

始终优先在变量之间断行，而不是在变量名和类型注解之间。但是，如果所有内容都适合在同一行，那就这样做。

```python
def my_method(self, first_var: int) -> int:
  ...
```

如果函数名、最后一个参数和返回类型的组合太长，在新行中缩进 4。使用换行时，优先将每个参数和返回类型放在各自的行上，并将闭合括号与 `def` 对齐：

```python
Yes:
def my_method(
    self,
    other_arg: MyLongType | None,
) -> tuple[MyLongType1, MyLongType1]:
  ...
```

可选地，返回类型可以放在与最后一个参数相同的行上：

```python
Okay:
def my_method(
    self,
    first_var: int,
    second_var: int) -> dict[OtherLongType, MyLongType]:
  ...
```

`pylint` 允许您将闭合括号移到新行并与开放括号对齐，但这不太可读。

```python
No:
def my_method(self,
              other_arg: MyLongType | None,
             ) -> dict[OtherLongType, MyLongType]:
  ...
```

如上例所示，优先不拆分类型。但是，有时它们太长无法放在单行上（尽量保持子类型不拆分）。

```python
def my_method(
    self,
    first_var: tuple[list[MyLongType1],
                     list[MyLongType2]],
    second_var: list[dict[
        MyLongType3, MyLongType4]],
) -> None:
  ...
```

如果单个名称和类型太长，考虑为类型使用[别名](#typing-aliases)。最后的手段是在冒号后断行并缩进 4。

```python
Yes:
def my_function(
    long_variable_name:
        long_module_name.LongTypeName,
) -> None:
  ...
```

```python
No:
def my_function(
    long_variable_name: long_module_name.
        LongTypeName,
) -> None:
  ...
```

## 3.19.3 Forward Declarations 前向声明

如果您需要使用尚未定义的类名（来自同一模块）——例如，如果您需要在该类的声明中使用类名，或者使用代码中稍后定义的类——请使用 `from __future__ import annotations` 或使用类名字符串。

```python
Yes:
from __future__ import annotations

class MyClass:
  def __init__(self, stack: Sequence[MyClass], item: OtherClass) -> None:

class OtherClass:
  ...
```

```python
Yes:
class MyClass:
  def __init__(self, stack: Sequence['MyClass'], item: 'OtherClass') -> None:

class OtherClass:
  ...
```

## 3.19.4 Default Values 默认值

根据 [PEP-008](https://peps.python.org/pep-0008/#other-recommendations)，仅对于同时具有类型注解和默认值的参数，在 `=` 周围使用空格。

```python
Yes:
def func(a: int = 0) -> int:
  ...
```

```python
No:
def func(a:int=0) -> int:
  ...
```

## 3.19.5 NoneType

在 Python 类型系统中，`NoneType` 是"一等"类型，对于类型目的，`None` 是 `NoneType` 的别名。如果参数可以是 `None`，则必须声明！您可以使用 `|` 联合类型表达式（在新的 Python 3.10+ 代码中推荐），或较旧的 `Optional` 和 `Union` 语法。

使用显式的 `X | None` 而不是隐式的。早期版本的类型检查器允许将 `a: str = None` 解释为 `a: str | None = None`，但这不再是首选行为。

```python
Yes:
def modern_or_union(a: str | int | None, b: str | None = None) -> str:
  ...
def union_optional(a: Union[str, int, None], b: Optional[str] = None) -> str:
  ...
```

```python
No:
def nullable_union(a: Union[None, str]) -> str:
  ...
def implicit_optional(a: str = None) -> str:
  ...
```

## 3.19.6 Type Aliases 类型别名

您可以声明复杂类型的别名。别名的名称应该是 CapWord 格式。如果别名仅在此模块中使用，它应该是 \_Private 的。

注意 `: TypeAlias` 注解仅在 3.10+ 版本中支持。

```python
from typing import TypeAlias

_LossAndGradient: TypeAlias = tuple[tf.Tensor, tf.Tensor]
ComplexTFMap: TypeAlias = Mapping[str, _LossAndGradient]
```

## 3.19.7 Ignoring Types 忽略类型

您可以使用特殊注释 `# type: ignore` 在行上禁用类型检查。

`pytype` 有针对特定错误的禁用选项（类似于 lint）：

```python
# pytype: disable=attribute-error
```

## 3.19.8 Typing Variables 类型变量

**Annotated Assignments 注解赋值**

如果内部变量的类型难以或无法推断，请使用注解赋值指定其类型——在变量名和值之间使用冒号和类型（与具有默认值的函数参数相同）：

```python
a: Foo = SomeUndecoratedFunction()
```

**Type Comments 类型注释**

虽然您可能会在代码库中看到它们（在 Python 3.6 之前是必需的），但不要再在行尾添加 `# type: <type name>` 注释：

```python
a = SomeUndecoratedFunction()  # type: Foo
```

## 3.19.9 Tuples vs Lists 元组 vs 列表

类型化列表只能包含单一类型的对象。类型化元组可以具有单个重复类型或具有不同类型的固定数量元素。后者通常用作函数的返回类型。

```python
a: list[int] = [1, 2, 3]
b: tuple[int, ...] = (1, 2, 3)
c: tuple[int, str, float] = (1, "2", 3.5)
```

## 3.19.10 Type variables 类型变量

Python 类型系统有 [generics](https://docs.python.org/3/library/typing.html#generics)。类型变量，如 `TypeVar` 和 `ParamSpec`，是使用它们的常见方式。

示例：

```python
from collections.abc import Callable
from typing import ParamSpec, TypeVar
_P = ParamSpec("_P")
_T = TypeVar("_T")
...
def next(l: list[_T]) -> _T:
  return l.pop()

def print_when_called(f: Callable[_P, _T]) -> Callable[_P, _T]:
  def inner(*args: _P.args, **kwargs: _P.kwargs) -> _T:
    print("Function was called")
    return f(*args, **kwargs)
  return inner
```

`TypeVar` 可以被约束：

```python
AddableType = TypeVar("AddableType", int, float, str)
def add(a: AddableType, b: AddableType) -> AddableType:
  return a + b
```

`typing` 模块中常见的预定义类型变量是 `AnyStr`。将它用于可以是 `bytes` 或 `str` 且必须都是相同类型的多个注解。

```python
from typing import AnyStr
def check_length(x: AnyStr) -> AnyStr:
  if len(x) <= 42:
    return x
  raise ValueError()
```

类型变量必须具有描述性名称，除非它满足以下所有条件：

- 不对外可见
- 不受约束

```python
Yes:
  _T = TypeVar("_T")
  _P = ParamSpec("_P")
  AddableType = TypeVar("AddableType", int, float, str)
  AnyFunction = TypeVar("AnyFunction", bound=Callable)
```

```python
No:
  T = TypeVar("T")
  P = ParamSpec("P")
  _T = TypeVar("_T", int, float, str)
  _F = TypeVar("_F", bound=Callable)
```

## 3.19.11 String types 字符串类型

> 不要在新代码中使用 `typing.Text`。它仅用于 Python 2/3 兼容性。

使用 `str` 表示字符串/文本数据。对于处理二进制数据的代码，使用 `bytes`。

```python
def deals_with_text_data(x: str) -> str:
  ...
def deals_with_binary_data(x: bytes) -> bytes:
  ...
```

如果函数的所有字符串类型始终相同（例如，如果返回类型与上面代码中的参数类型相同），请使用 [AnyStr](#typing-type-var)。

## 3.19.12 Imports For Typing 类型导入

对于 `typing` 或 `collections.abc` 模块中用于支持静态分析和类型检查的符号（包括类型、函数和常量），始终导入符号本身。这使常见注解更简洁，并与世界各地使用的类型实践相匹配。明确允许从 `typing` 和 `collections.abc` 模块在一行上导入多个特定符号。例如：

```python
from collections.abc import Mapping, Sequence
from typing import Any, Generic, cast, TYPE_CHECKING
```

鉴于这种导入方式会将项添加到本地命名空间，`typing` 或 `collections.abc` 中的名称应类似于关键字处理，不应在您的 Python 代码中定义，无论是否类型化。如果类型与模块中的现有名称冲突，请使用 `import x as y` 导入。

```python
from typing import Any as AnyType
```

在注解函数签名时，优先使用抽象容器类型（如 `collections.abc.Sequence`）而不是具体类型（如 `list`）。如果需要使用具体类型（例如，类型化元素的 `tuple`），优先使用内置类型（如 `tuple`）而不是 `typing` 模块中的参数化类型别名（例如，`typing.Tuple`）。

## 3.19.13 Conditional Imports 条件导入

仅在类型检查所需的额外导入必须在运行时避免的例外情况下使用条件导入。不鼓励这种模式；应优先考虑重构代码以允许顶级导入的替代方案。

仅类型注解所需的导入可以放在 `if TYPE_CHECKING:` 块中。

- 条件导入的类型需要作为字符串引用，以便与 Python 3.6 向前兼容，其中注解表达式实际上被评估。
- 只有仅用于类型化的实体应该在这里定义；这包括别名。否则将是运行时错误，因为模块在运行时不会被导入。
- 该块应该在所有正常导入之后。
- 类型导入列表中不应该有空行。
- 像普通导入列表一样排序此列表。

```python
import typing
if typing.TYPE_CHECKING:
  import sketch
def f(x: "sketch.Sketch"): ...
```

## 3.19.14 Circular Dependencies 循环依赖

由类型引起的循环依赖是代码异味。此类代码是重构的良好候选者。虽然技术上可以保持循环依赖，但各种构建系统不会让您这样做，因为每个模块都必须依赖另一个。

用 `Any` 替换创建循环依赖导入的模块。使用有意义的名称设置[别名](#typing-aliases)，并使用此模块的真实类型名称（`Any` 的任何属性都是 `Any`）。别名定义应该与最后一个导入隔开一行。

```python
from typing import Any

some_mod = Any  # some_mod.py 导入此模块。
...

def my_method(self, var: "some_mod.SomeType") -> None:
  ...
```

## 3.19.15 Generics 泛型

在注解时，优先在参数列表中为[泛型](https://docs.python.org/3/library/typing.html#generics)类型指定类型参数；否则，泛型的参数将被假定为 [`Any`](https://docs.python.org/3/library/typing.html#the-any-type)。

```python
# Yes:
def get_names(employee_ids: Sequence[int]) -> Mapping[int, str]:
  ...
```

```python
# No:
# 这被解释为 get_names(employee_ids: Sequence[Any]) -> Mapping[Any, Any]
def get_names(employee_ids: Sequence) -> Mapping:
  ...
```

如果泛型的最佳类型参数是 `Any`，请使其显式，但请记住，在许多情况下 [`TypeVar`](#typing-type-var) 可能更合适：

```python
# No:
def get_names(employee_ids: Sequence[Any]) -> Mapping[Any, str]:
  """Returns a mapping from employee ID to employee name for given IDs."""
```

```python
# Yes:
_T = TypeVar('_T')
def get_names(employee_ids: Sequence[_T]) -> Mapping[_T, str]:
  """Returns a mapping from employee ID to employee name for given IDs."""
```
