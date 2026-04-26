---
title: TDD - 测试驱动开发
tags: [development, tdd, test-driven-development]
status: completed
difficulty: advanced
time_spent: 3h
date: 2026-03-15
updated: 2026-03-15
---

# TDD - 测试驱动开发

## 概念

测试驱动开发（Test-Driven Development, TDD）是一种敏捷软件开发方法，要求在编写实际代码之前先编写测试。TDD 的核心流程是：红-绿-重构。

**核心流程**：
1. **红**：编写失败的测试用例
2. **绿**：编写最小代码使测试通过
3. **重构**：优化代码质量

**主要优势**：
- 提高代码质量和可测试性
- 减少Bug数量
- 更好的代码设计
- 增强对代码的信心

## 基础步骤

### 1. 红阶段

编写失败的测试用例，验证业务需求。

```python
import pytest
from app.services.user_service import UserService

def test_register_user_success():
    """测试成功注册用户"""
    user_service = UserService()
    user = user_service.register(
        username="alice",
        email="alice@example.com",
        password="password123"
    )
    assert user.username == "alice"
    assert user.email == "alice@example.com"
```

### 2. 绿阶段

编写最小代码使测试通过。

```python
class UserService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, username: str, email: str, password: str):
        """注册用户"""
        # 检查用户名是否已存在
        if self.db.query(User).filter_by(username=username).first():
            raise ValueError("用户名已存在")

        # 创建用户
        user = User(
            username=username,
            email=email,
            password_hash=self._hash_password(password)
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def _hash_password(self, password: str):
        """密码加密"""
        return f"hash_{password}"
```

### 3. 重构阶段

优化代码质量，确保没有重复代码。

```python
# 重构后
class UserService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, username: str, email: str, password: str):
        """注册用户"""
        self._validate_username(username)
        user = User(
            username=username,
            email=email,
            password_hash=self._hash_password(password)
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def _validate_username(self, username: str):
        """验证用户名"""
        if not username:
            raise ValueError("用户名不能为空")
        if self.db.query(User).filter_by(username=username).first():
            raise ValueError("用户名已存在")

    def _hash_password(self, password: str):
        """密码加密"""
        return f"hash_{password}"

# 运行测试
def test_register_user_success():
    user_service = UserService(db)
    user = user_service.register("alice", "alice@example.com", "password123")
    assert user.username == "alice"
    assert user.email == "alice@example.com"

def test_register_user_duplicate():
    user_service = UserService(db)
    user_service.register("alice", "alice@example.com", "password123")
    with pytest.raises(ValueError) as exc:
        user_service.register("alice", "other@example.com", "password456")
    assert "用户名已存在" in str(exc.value)
```

## TDD 工作流

### 完整示例

```python
# 步骤1：编写测试
def test_calculate_total_amount():
    """测试计算订单总金额"""
    order = Order()
    order.add_item("P-001", 2, 99.99)
    order.add_item("P-002", 1, 199.99)

    total = order.total_amount()
    assert total == 2 * 99.99 + 1 * 199.99  # 399.98

# 步骤2：实现功能
class Order:
    def __init__(self):
        self.items = []

    def add_item(self, product_id: str, quantity: int, unit_price: float):
        """添加订单项"""
        self.items.append(OrderItem(product_id, quantity, unit_price))

    def total_amount(self) -> float:
        """计算总金额"""
        total = 0.0
        for item in self.items:
            total += item.quantity * item.unit_price
        return total

# 步骤3：重构优化
class Order:
    def __init__(self):
        self.items = []

    def add_item(self, product_id: str, quantity: int, unit_price: float):
        """添加订单项"""
        self.items.append(OrderItem(product_id, quantity, unit_price))

    def total_amount(self) -> float:
        """计算总金额"""
        return sum(item.quantity * item.unit_price for item in self.items)
```

## 实用原则

### 1. 测试优先

永远先写测试，再写业务代码。

### 2. 最小实现

实现功能要最小化，只通过测试即可。

### 3. 持续测试

频繁运行测试，及时发现问题。

### 4. 重构优化

在测试通过的基础上不断优化代码。

## TDD 实践建议

```python
# 1. 测试文件命名
# test_user_service.py  - 测试用户服务
# test_order_service.py - 测试订单服务

# 2. 测试命名规范
# test_功能名_场景_预期结果()
def test_register_user_success():
    """成功注册用户"""

def test_register_user_duplicate():
    """重复用户名注册失败"""

# 3. 测试隔离
@pytest.fixture
def user_service():
    """创建测试用的服务实例"""
    db = create_test_db()
    return UserService(db)

def test_register_user(user_service):
    """测试注册用户"""
    user = user_service.register(...)
    assert user.username == "alice"

# 4. 测试覆盖率
# 确保测试覆盖主要场景和边界情况
```

## 相关资源

- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)
- [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

## 相关笔记

- [[ddd]] - 领域驱动设计
- [[bo]] - 业务对象
- [[specs]] - 规范模式

---

**创建日期**: 2026-03-15
**最后更新**: 2026-03-15
