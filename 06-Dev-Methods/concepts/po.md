---
title: PO - 持久化对象
tags: [development, po, persistent-object]
status: completed
difficulty: intermediate
time_spent: 1h
date: 2026-03-15
updated: 2026-03-15
---

# PO - 持久化对象

## 概念

PO (Persistent Object) 也称为 Data Object 或 Table Data Gateway，是直接映射数据库表的实体对象。PO 包含数据库表结构对应的字段，用于数据持久化操作。

**主要作用**：
- 直接对应数据库表结构
- 与 ORM 框架（如 SQLAlchemy）集成
- 提供数据持久化方法（增删改查）
- 不包含业务逻辑

## 用法

PO 的特点：
- 字段与数据库表一一对应
- 通常包含 ID 作为主键
- 通过 ORM 操作数据库
- 转换为 DTO/VO 用于传输和展示

## 示例

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UserPO(Base):
    """用户持久化对象"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    age = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dto(self) -> UserDTO:
        """转换为 DTO"""
        return UserDTO(
            id=self.id,
            username=self.username,
            email=self.email,
            age=self.age
        )

    def to_vo(self) -> UserVO:
        """转换为 VO"""
        return UserVO(
            id=self.id,
            username=self.username,
            email=self.email,
            created_at=self.created_at,
            is_active=self.is_active
        )

    def update(self, **kwargs):
        """更新字段"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

# 使用 PO 进行数据库操作
# 创建
po = UserPO(
    username="alice",
    email="alice@example.com",
    password_hash="hashed_password",
    age=25
)
db.add(po)
db.commit()

# 查询
po = db.query(UserPO).filter_by(username="alice").first()

# 更新
po.update(age=26)

# 删除
db.delete(po)
db.commit()
```

## 相关资源

- [SQLAlchemy ORM](https://www.sqlalchemy.org/)
- [Active Record Pattern](https://en.wikipedia.org/wiki/Active_record_pattern)

## 相关笔记

- [[dto]] - 数据传输对象
- [[vo]] - 视图对象
- [[entity]] - 实体对象
- [[bo]] - 业务对象

---

**创建日期**: 2026-03-15
**最后更新**: 2026-03-15
