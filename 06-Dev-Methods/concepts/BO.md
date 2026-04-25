---
title: BO - 业务对象
tags: [development, bo, business-object]
status: learning
difficulty: intermediate
time_spent: 1h
created: 2026-03-15
updated: 2026-03-15
---

# BO - 业务对象

## 概念

BO (Business Object) 也称为领域对象或业务实体，是包含业务逻辑的对象。BO 封装了与业务相关的数据和操作，是系统的核心业务逻辑单元。

**主要作用**：
- 封装业务逻辑
- 处理业务规则
- 协调多个 PO/Entity
- 提供业务方法

## 用法

BO 与其他对象的区别：
- PO/Entity：数据存储，无业务逻辑
- BO：包含业务逻辑，处理业务规则
- DTO/VO：仅数据传输，无业务逻辑

## 示例

```python
from sqlalchemy.orm import Session
from typing import List

class UserBO:
    """用户业务对象"""
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str) -> dict:
        """根据用户名获取用户（业务逻辑）"""
        po = self.db.query(UserPO).filter_by(username=username).first()

        if not po:
            raise ValueError("用户不存在")

        # 业务规则：检查用户是否活跃
        if not po.is_active:
            raise ValueError("用户已被禁用")

        # 业务规则：验证用户年龄
        if po.age < 18:
            raise ValueError("用户年龄不足")

        # 转换为 VO 并返回
        return po.to_vo().dict()

    def register_user(self, username: str, password: str, email: str, age: int) -> dict:
        """注册用户（业务逻辑）"""
        # 业务规则：验证用户名是否已存在
        if self.db.query(UserPO).filter_by(username=username).first():
            raise ValueError("用户名已存在")

        # 业务规则：验证邮箱格式
        if not self._is_valid_email(email):
            raise ValueError("邮箱格式不正确")

        # 业务规则：验证年龄范围
        if not 18 <= age <= 100:
            raise ValueError("年龄必须在 18-100 之间")

        # 创建 PO
        po = UserPO(
            username=username,
            email=email,
            password_hash=self._hash_password(password),
            age=age
        )

        # 保存到数据库
        self.db.add(po)
        self.db.commit()
        self.db.refresh(po)

        # 发送欢迎邮件（业务操作）
        self._send_welcome_email(username, email)

        return po.to_vo().dict()

    def _is_valid_email(self, email: str) -> bool:
        """验证邮箱格式"""
        return "@" in email and "." in email

    def _hash_password(self, password: str) -> str:
        """密码加密（简化版）"""
        return f"hash_{password}"

    def _send_welcome_email(self, username: str, email: str):
        """发送欢迎邮件（简化版）"""
        print(f"发送欢迎邮件到 {email}: 欢迎 {username}!")

# 使用 BO
db = Session(bind=engine)
user_bo = UserBO(db)

try:
    # 业务操作
    user_data = user_bo.register_user(
        username="alice",
        password="password123",
        email="alice@example.com",
        age=25
    )
    print(user_data)
except ValueError as e:
    print(f"业务错误: {e}")
finally:
    db.close()
```

## 业务对象设计原则

1. **单一职责**：每个 BO 只负责一个业务领域
2. **封装性**：隐藏内部实现细节
3. **不可变性**：重要业务规则不应被外部修改
4. **事务管理**：BO 负责协调数据库事务

## 相关资源

- [Domain-Driven Design](https://martinfowler.com/tags/domain%20driven%20design.html)
- [Service Layer Pattern](https://en.wikipedia.org/wiki/Service_layer_pattern)

## 相关笔记

- [[DTO]] - 数据传输对象
- [[VO]] - 视图对象
- [[PO]] - 持久化对象
- [[Entity]] - 实体对象
- [[DDD]] - 领域驱动设计

---

**创建日期**: 2026-03-15
**最后更新**: 2026-03-15
