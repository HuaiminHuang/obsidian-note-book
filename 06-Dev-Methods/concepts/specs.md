---
title: Specs - 规范模式
tags: [development, specs, specification]
status: completed
difficulty: intermediate
time_spent: 1h
date: 2026-03-15
updated: 2026-03-15
---

# Specs - 规范模式

## 概念

Specs (Specification) 是一种设计模式，用于封装业务规则和验证逻辑。它将业务规则表达为可重用、可组合的规范对象。

**主要作用**：
- 封装业务验证规则
- 提供可组合的规则逻辑
- 使验证逻辑可测试
- 避免业务逻辑散落在各处

## 用法

Specs 的优势：
- 业务规则集中管理
- 可以组合多个规范
- 易于测试和维护
- 支持动态条件

## 示例

```python
from abc import ABC, abstractmethod
from typing import Any

class Specification(ABC):
    """规范接口"""
    @abstractmethod
    def is_satisfied_by(self, candidate: Any) -> bool:
        """判断候选对象是否满足规范"""
        pass

class AndSpecification(Specification):
    """与规范组合"""
    def __init__(self, *specs):
        self.specs = specs

    def is_satisfied_by(self, candidate: Any) -> bool:
        return all(spec.is_satisfied_by(candidate) for spec in self.specs)

class OrSpecification(Specification):
    """或规范组合"""
    def __init__(self, *specs):
        self.specs = specs

    def is_satisfied_by(self, candidate: Any) -> bool:
        return any(spec.is_satisfied_by(candidate) for spec in self.specs)

class NotSpecification(Specification):
    """非规范组合"""
    def __init__(self, spec):
        self.spec = spec

    def is_satisfied_by(self, candidate: Any) -> bool:
        return not self.spec.is_satisfied_by(candidate)

# 具体规范示例
class ValidEmailSpecification(Specification):
    """有效邮箱规范"""
    def is_satisfied_by(self, candidate: Any) -> bool:
        if not isinstance(candidate, str):
            return False
        return "@" in candidate and "." in candidate

class MinimumAgeSpecification(Specification):
    """最小年龄规范"""
    def __init__(self, min_age: int):
        self.min_age = min_age

    def is_satisfied_by(self, candidate: Any) -> bool:
        if not hasattr(candidate, "age"):
            return False
        return candidate.age >= self.min_age

class ActiveUserSpecification(Specification):
    """活跃用户规范"""
    def is_satisfied_by(self, candidate: Any) -> bool:
        if not hasattr(candidate, "is_active"):
            return False
        return candidate.is_active

# 使用规范组合
def create_registration_spec():
    """创建注册验证规范"""
    return AndSpecification(
        ValidEmailSpecification(),
        MinimumAgeSpecification(18),
        ActiveUserSpecification()
    )

# 测试规范
user1 = User(age=20, is_active=True)
user2 = User(age=15, is_active=True)
user3 = User(age=20, is_active=False)

spec = create_registration_spec()

print(f"用户1满足规范: {spec.is_satisfied_by(user1)}")  # True
print(f"用户2满足规范: {spec.is_satisfied_by(user2)}")  # False (年龄不足)
print(f"用户3满足规范: {spec.is_satisfied_by(user3)}")  # False (未激活)

# 复杂组合规范
advanced_spec = OrSpecification(
    AndSpecification(ValidEmailSpecification(), MinimumAgeSpecification(18)),
    NotSpecification(ActiveUserSpecification())
)
```

## 实际应用场景

```python
class User:
    def __init__(self, username: str, email: str, age: int, is_active: bool):
        self.username = username
        self.email = email
        self.age = age
        self.is_active = is_active

class UserService:
    def __init__(self):
        self.registration_spec = create_registration_spec()
        self.login_spec = AndSpecification(ValidEmailSpecification(), ActiveUserSpecification())

    def register(self, user: User) -> bool:
        """注册用户"""
        if not self.registration_spec.is_satisfied_by(user):
            raise ValueError("用户不符合注册规范")
        # 保存到数据库
        return True

    def login(self, user: User) -> bool:
        """用户登录"""
        if not self.login_spec.is_satisfied_by(user):
            raise ValueError("用户不符合登录规范")
        # 验证密码等
        return True

# 使用
service = UserService()
try:
    service.register(User("alice", "alice@example.com", 25, True))
    print("注册成功")
except ValueError as e:
    print(f"注册失败: {e}")
```

## 相关资源

- [Specification Pattern](https://martinfowler.com/bliki/SpecificationPattern.html)
- [Domain-Driven Design](https://martinfowler.com/tags/domain%20driven%20design.html)

## 相关笔记

- [[ddd]] - 领域驱动设计
- [[bo]] - 业务对象
- [[tdd]] - 测试驱动开发

---

**创建日期**: 2026-03-15
**最后更新**: 2026-03-15
