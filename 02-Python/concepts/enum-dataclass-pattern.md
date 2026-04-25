---
title: Enum与dataclass组合模式
tags: [python, python/advanced, python/enum, python/dataclass]
status: completed
difficulty: intermediate
created: 2026-03-29
updated: 2026-03-29
---

# Enum与dataclass组合模式

## 概念

`Enum` 的每个成员只能绑定一个值。当需要为枚举成员携带**多个元数据**时，用 `@dataclass` 定义容器类，让 Enum 成员绑定容器实例。

优势：
- 结构化元数据，类型安全
- 通过 `@property` 简化访问
- 通过 `@classmethod` 支持反向查找

## 用法

### 定义容器 + 枚举

```python
from dataclasses import dataclass
from enum import Enum


@dataclass
class StatusContainer:
    label: str
    description: str


class Status(Enum):
    SUCCESS = StatusContainer("success", "操作成功")
    FAIL = StatusContainer("fail", "操作失败")
    UNKNOWN = StatusContainer("unknown", "未知状态")

    @property
    def label(self) -> str:
        return self.value.label

    @property
    def desc(self) -> str:
        return self.value.description

    @classmethod
    def get_by_label(cls, label: str) -> "Status":
        for item in cls:
            if item.label == label:
                return item
        raise ValueError(f"{label} is not a valid {cls.__name__}")
```

### 使用方式

```python
status = Status.SUCCESS
print(status.label)    # "success"
print(status.desc)     # "操作成功"

found = Status.get_by_label("fail")
print(found)           # Status.FAIL
```

## 示例

适用于需要为枚举成员绑定多个属性的场景，如工作流状态、回调状态码等业务定义。

## 要点说明

### 容器方案对比

| 方案 | 优点 | 缺点 |
|------|------|------|
| `@dataclass` 容器 | 类型安全、可扩展、IDE 友好 | 需要额外定义一个类 |
| `tuple` 值 | 简洁 | 只能用索引访问，可读性差 |
| `dict` 值 | 灵活 | 无类型提示，容易拼错 key |

### 设计要点

1. 容器类命名约定：`{EnumName}Container`
2. `@property` 代理：将 `self.value.xxx` 简化为 `self.xxx`
3. 反向查找：通过 `@classmethod` 提供 `get_by_label()` 等查找能力
4. 异常处理：查找失败抛出 `ValueError`，与内置 Enum 行为一致

## 相关资源

- [PEP 557 - Data Classes](https://peps.python.org/pep-0557/)
- [Python 官方文档 - enum](https://docs.python.org/3/library/enum.html)
- [Python 官方文档 - dataclasses](https://docs.python.org/3/library/dataclasses.html)

## 相关笔记

- [[装饰器]] - 理解 @dataclass 和 @property 装饰器
- [[闭包]] - 理解 Python 类的属性访问机制

---

**创建日期**: 2026-03-29
**最后更新**: 2026-03-29
