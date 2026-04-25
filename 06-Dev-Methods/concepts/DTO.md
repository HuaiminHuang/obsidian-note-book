---
title: DTO - 数据传输对象
tags: [development, dto, data-transfomer]
status: learning
difficulty: intermediate
time_spent: 1h
created: 2026-03-15
updated: 2026-03-15
---

# DTO - 数据传输对象

## 概念

DTO (Data Transfer Object) 是一种设计模式，用于在软件系统不同层之间传输数据。DTO 是一个设计模式，用于在软件系统不同层之间传输数据，不包含业务逻辑，仅用于数据传递。

**主要作用**：
- 在 API 层与前端或外部服务之间传输数据
- 在服务层与数据访问层之间传输数据
- 隐藏内部数据结构，提高安全性
- 减少数据传输量，优化性能

## 用法

DTO 与实体类（Entity）的区别：
- DTO：用于数据传输，不直接映射数据库表
- Entity：对应数据库表，包含业务逻辑
- VO (View Object)：用于前端展示，经过 DTO 转换

## 示例

```python
from pydantic import BaseModel
from typing import Optional

class UserDTO(BaseModel):
    """用户数据传输对象"""
    id: Optional[int] = None
    username: str
    email: str
    age: Optional[int] = None

class CreateUserDTO(UserDTO):
    """创建用户 DTO"""
    password: str

class UpdateUserDTO(BaseModel):
    """更新用户 DTO"""
    username: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

# 使用 DTO
@app.post("/users", response_model=UserDTO)
async def create_user(user: CreateUserDTO):
    # 将 DTO 转换为 Entity 并保存到数据库
    entity = User.from_dto(user)
    db.add(entity)
    db.commit()
    return entity.to_dto()

@app.get("/users/{user_id}", response_model=UserDTO)
async def get_user(user_id: int):
    # 从数据库获取 Entity 并转换为 DTO
    entity = db.get(User, user_id)
    return entity.to_dto()
```

## 相关资源

- [Pydantic 文档](https://docs.pydantic.dev/)
- [DTO Pattern](https://en.wikipedia.org/wiki/Data_transfer_object)

## 相关笔记

- [[VO]] - 视图对象
- [[PO]] - 持久化对象
- [[Entity]] - 实体对象
- [[BO]] - 业务对象

---

**创建日期**: 2026-03-15
**最后更新**: 2026-03-15
