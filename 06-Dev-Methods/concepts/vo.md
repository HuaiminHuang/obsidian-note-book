---
title: VO - 视图对象
tags: [development, vo, view-object]
status: completed
difficulty: intermediate
time_spent: 1h
date: 2026-03-15
updated: 2026-03-15
---

# VO - 视图对象

## 概念

VO (View Object) 也称为 View Model，是一种专门用于向用户展示数据的对象。VO 从 DTO 转换而来，通常用于 API 响应。

**主要作用**：
- 优化前端展示数据
- 过滤敏感信息（如密码）
- 格式化数据（如日期、金额）
- 聚合数据（如计算字段）

## 用法

VO 与 DTO 的区别：
- DTO：用于数据传输，可包含不可见字段
- VO：专门用于前端展示，只包含可见字段
- PO/Entity：对应数据库表结构

## 示例

```python
from pydantic import BaseModel
from datetime import datetime

class UserVO(BaseModel):
    """用户视图对象"""
    id: int
    username: str
    email: str
    created_at: datetime
    is_active: bool

class UserDetailVO(UserVO):
    """用户详情视图对象"""
    posts_count: int
    followers_count: int

class UserSummaryVO(BaseModel):
    """用户摘要视图对象"""
    id: int
    username: str
    avatar_url: str

# 从 Entity 转换为 VO
def user_to_vo(user: User) -> UserVO:
    return UserVO(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at,
        is_active=user.is_active
    )

# 从 DTO 转换为 VO
def dto_to_vo(dto: UserDTO) -> UserVO:
    return UserVO(
        id=dto.id or 0,
        username=dto.username,
        email=dto.email,
        created_at=datetime.now(),
        is_active=True
    )

# API 响应
@app.get("/users/{user_id}", response_model=UserVO)
async def get_user(user_id: int):
    user = db.get(User, user_id)
    # 过滤敏感信息，添加计算字段
    vo = UserDetailVO(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at,
        is_active=user.is_active,
        posts_count=len(user.posts),
        followers_count=0  # 需要计算
    )
    return vo
```

## 相关资源

- [MVVM Pattern](https://en.wikipedia.org/wiki/Model%E2%80%93View%E2%80%93ViewModel)

## 相关笔记

- [[dto]] - 数据传输对象
- [[po]] - 持久化对象
- [[entity]] - 实体对象

---

**创建日期**: 2026-03-15
**最后更新**: 2026-03-15
