---
title: Style Guide 学习问答
tags: [python, style-guide, google, qa]
status: learning
date: 2026-03-29
updated: 2026-03-30
---

# Style Guide 学习问答

学习 Google Python Style Guide 过程中的疑问与解答记录。

---

## pylint vs pylance

**Q**: pylint 和 pylance 都是 Python 的语法静态检查吗？

**A**: 两者定位不同：

| 工具 | 定位 | 侧重 |
|------|------|------|
| **pylint** | 代码静态分析工具 | 代码风格（PEP 8）、潜在 bug、代码坏味道 |
| **pylance** | VS Code 语言服务器（基于 Pyright） | 类型检查、自动补全、代码导航 |

pylint 独立运行，不依赖编辑器；pylance 是编辑器插件，侧重开发体验。

---

## 规范问题 vs 语法问题

**Q**: `Missing class docstring`、`Access to a protected member` 这类提示是规范问题还是语法问题？

**A**: 都是**规范/代码质量**问题，不是语法错误。代码本身能正常运行。

- `Missing class docstring` — 缺少文档字符串（PEP 257 规范）
- `Access to a protected member` — 访问了双下划线 `__` 开头的名称改写成员

双下划线会触发 Python 名称改写（name mangling），`__init_once` 在外部实际变成 `_Config__init_once`，导致跨作用域调用和静态分析都出现识别偏差。

参考：[[01-language-rules-part1]]

---

## 全捕获 except 的正确用法

**Q**: "永远不要使用全捕获 except:" 是什么意思？不是需要 try/except 来捕获异常吗？

**A**: PEP 8 的意思是**不要用空 catch**，而不是不要用 try/except。

```python
# 错误 — 吞掉所有异常，包括 KeyboardInterrupt
except:
    pass

# 错误 — 范围太宽，掩盖真实问题
except Exception:
    pass

# 正确 — 捕获具体异常类型
try:
    value = int(user_input)
except ValueError:
    print("请输入数字")
except KeyError:
    print("键不存在")
```

全捕获会隐藏真实错误，比如变量名拼错这种 bug 也被吞掉，排查非常痛苦。

参考：[[01-language-rules-part1#2.4 Exceptions 异常]]

---

## finally 的使用场景

**Q**: finally 什么时候使用比较好？

**A**: `finally` 用于**无论是否发生异常都必须执行的清理操作**。

常见场景：关闭文件、关闭数据库连接、释放网络连接、释放锁。

```python
f = open("data.txt")
try:
    content = f.read()
except FileNotFoundError:
    print("文件不存在")
finally:
    f.close()
```

优先使用 `with` 语句（内部就是自动调用 finally）：

```python
with open("data.txt") as f:
    content = f.read()
```

**简单原则**：需要手动释放资源的场景用 `finally`，能用 `with` 的优先用 `with`。

参考：[[01-language-rules-part1#2.4 Exceptions 异常]]

---

## Mutable Global State 可变全局状态

**Q**: 可变全局状态是什么意思？

**A**: 在模块级别定义、且运行时会被修改的变量。

```python
# 可变全局状态（避免）
_db_connection = None
current_user = None

# 模块级常量（推荐，不可变）
MAX_RETRY_COUNT = 3
DB_HOST = "localhost"
```

问题：任何地方都能修改，难以追踪"谁在什么时候改了什么值"。常量定义后不改变，可变全局状态在运行时会被反复修改。

参考：[[01-language-rules-part1#2.5 Mutable Global State 可变全局状态]]

---

## Nested Classes and Functions 嵌套类和函数

**Q**: 这里是尽量减少嵌套吗？类也可以嵌套吗？

**A**: 对，能用模块级的就不要嵌套。

| 场景 | 是否应该嵌套 |
|------|-------------|
| 闭包（捕获外层变量） | 可以 |
| 装饰器 | 可以 |
| 仅仅为了隐藏函数/类 | 不应该，用 `_` 前缀代替 |
| 需要单独测试的函数 | 不应该 |

嵌套类语法合法但日常开发中几乎用不到，常量用 `enum` 即可。

参考：[[01-language-rules-part1#2.6 Nested/Local/Inner Classes and Functions 嵌套局部内部类和函数]]

---

## @classmethod 的作用

**Q**: `@classmethod` 是在做什么？

**A**: 让方法绑定到**类本身**而不是实例，第一个参数 `cls` 就是类。

```python
# 普通方法 — 需要先创建实例
status = Status.SUCCESS
status.label

# classmethod — 直接通过类调用，不需要实例
Status.get_by_label("fail")
```

参考：[[enum-dataclass-pattern]]

---

## 相关笔记

- [[01-language-rules-part1]] - 语言规则（上）
- [[enum-dataclass-pattern]] - Enum 与 dataclass 组合模式
- [[02-Python]] - Python 学习目录

---

## 默认迭代器 in/not in

**Q**: 为什么推荐使用 `in`/`not in` 而非手动循环？

**A**: 原因有四：

1. **可读性** - 更接近自然语言
2. **性能** - dict/set 的 `in` 是 O(1)，list 是 O(n)
3. **Pythonic** - 符合 Python 设计哲学
4. **通用性** - 适用于所有容器类型

```python
# ✅ 推荐
if name in names:
    
# ❌ 不推荐
found = False
for n in names:
    if n == name:
        found = True
```

参考：[[01-language-rules-part1#2.8 Default Iterators and Operators 默认迭代器和操作符]]

---

## 括号使用规则

**Q**: "不要在 return 语句或条件语句中使用括号，除非..." 是什么意思？

**A**: 不要加**多余的括号**，只在两种情况使用：

```python
# ❌ 多余括号
if (x):
    bar()
return (foo)

# ✅ 正常写法
if x:
    bar()
return foo

# ✅ 允许的情况 1：隐式换行
if (very_long_condition and
    another_condition):
    pass

# ✅ 允许的情况 2：明确表示元组
return (spam, beans)
onesie = (foo,)  # 单元素元组
```

参考：[[03-style-rules-formatting#3.3 Parentheses 括号]]

---

## Shebang 行何时需要

**Q**: `#!/usr/bin/env python3` 什么时候需要？

**A**: 只有**直接执行的入口脚本**需要，普通模块不需要。

```python
# ✅ 入口脚本（如 main.py）
#!/usr/bin/env python3
"""主程序入口"""
def main():
    pass

# ✅ 普通模块
"""模块说明 docstring"""
def helper():
    pass
```

| 内容 | 是否需要 |
|------|---------|
| `# -*- coding: utf-8 -*-` | ❌ Python 3 默认 UTF-8 |
| `#!/usr/bin/env python3` | ⚠️ 仅入口脚本 |
| `@Date @Author` 注释块 | ❌ 用 git 管理 |

参考：[[03-style-rules-formatting#3.7 Shebang Line Shebang 行]]

---

## Getter/Setter 使用场景

**Q**: 什么时候需要写 getter/setter？

**A**: **有复杂逻辑或副作用时才需要**，简单读写直接用属性。

```python
# ❌ 没必要 - 只是简单读写
class Bad:
    def __init__(self):
        self._x = 0
    
    def get_x(self):
        return self._x
    
    def set_x(self, value):
        self._x = value

# ✅ 直接公开属性
class Good:
    def __init__(self):
        self.x = 0

# ✅ 有副作用时用 setter 或 @property
class Cache:
    def __init__(self):
        self._data = {}
        self._dirty = False
    
    def set_data(self, key, value):
        self._data[key] = value
        self._dirty = True
```

参考：[[06-style-rules-resources#3.15 Getters and Setters 访问器和设置器]]

---

## isinstance 使用建议

**Q**: `isinstance` 可以经常使用吗？

**A**: **不建议频繁使用**，Python 推崇"鸭子类型"。

```python
# ❌ 过度类型检查
def process(data):
    if isinstance(data, list):
        return data[0]
    elif isinstance(data, dict):
        return list(data.values())[0]

# ✅ 鸭子类型
def process(data):
    return data[0]  # 能用就行
```

**什么时候用？** 类型注解、处理明显不同类型分支、序列化场景。

---

## 前向声明

**Q**: 类型注解中的 `'ClassName'` 字符串是什么意思？

**A**: 让 Python 在解析时不报错，用于**尚未定义的类**。

```python
class Node:
    def __init__(self, next_node: 'Node'):  # Node 还没定义完
        self.next_node = next_node
```

**不需要删除**，写上就保留。推荐用 `from __future__ import annotations` 全局生效。

参考：[[08-style-rules-main-typing#3.19.3 Forward Declarations 前向声明]]

---

## typing 导入方式

**Q**: 为什么推荐 `from typing import xxx`？会污染命名空间吗？

**A**: 这是推荐写法。"污染命名空间"指**不要自己定义同名变量**。

```python
# ✅ 推荐
from typing import Any, cast

# ❌ 不要覆盖
from typing import Any
Any = "oops"  # 覆盖了类型

# ✅ 冲突时用别名
from typing import Query as TypeQuery
```

参考：[[08-style-rules-main-typing#3.19.12 Imports For Typing 类型导入]]

---

## TypeVar vs Any

**Q**: 为什么 `TypeVar` 比 `Any` 更合适？

**A**: `Any` 丢失类型信息，`TypeVar` 保留类型关系。

```python
# ❌ Any - 类型断链
def get_names(ids: Sequence[Any]) -> Mapping[Any, str]:
    ...

# ✅ TypeVar - 输入输出类型关联
_T = TypeVar('_T')
def get_names(ids: Sequence[_T]) -> Mapping[_T, str]:
    ...

# 调用时：ids: Sequence[int] → 返回 Mapping[int, str]
```

- `Any` = "不在乎是什么类型"，关闭类型检查
- `TypeVar` = "记住这个类型，后面还要用"

参考：[[08-style-rules-main-typing#3.19.14 Generic Types 泛型类型]]

---

## 泛型实际作用

**Q**: 泛型有什么实际作用？使用场景是什么？

**A**: 让类型检查器追踪类型关系，提供更准确的类型提示。

**常见场景：**

1. **容器类** - 自定义集合类型
2. **通用函数** - 输入输出类型关联
3. **协议/抽象基类** - 约束行为

```python
_T = TypeVar('_T')

class Box(Generic[_T]):
    def __init__(self, item: _T):
        self.item = item
    
    def get(self) -> _T:
        return self.item

box: Box[int] = Box(42)
reveal_type(box.get())  # 类型检查器知道是 int
```

**重点注意：**
- 泛型是**静态类型检查工具用的**，运行时不生效
- 用 `bound` 限制范围，用 `Generic` 定义泛型类
- 写库/框架用得多，普通业务代码相对少用

参考：[[08-style-rules-main-typing#3.19.14 Generic Types 泛型类型]]

---

## 相关笔记

- [[01-language-rules-part1]] - 语言规则（上）
- [[02-language-rules-part2]] - 语言规则（下）
- [[03-style-rules-formatting]] - 风格规则（格式）
- [[06-style-rules-resources]] - 风格规则（资源）
- [[08-style-rules-main-typing]] - 风格规则（类型）
- [[enum-dataclass-pattern]] - Enum 与 dataclass 组合模式
- [[02-Python]] - Python 学习目录

---

**创建日期**: 2026-03-29
**最后更新**: 2026-03-30
