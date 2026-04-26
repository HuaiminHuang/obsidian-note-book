---
title: SQLAlchemy - Python ORM 框架
tags: [python, framework, orm, sqlalchemy]
date: 2026-03-15
status: learning
difficulty: advanced
---

# SQLAlchemy - Python ORM 框架

## 概念

SQLAlchemy 是 Python 最流行的 ORM（对象关系映射）框架，提供了一整套功能，包括数据建模、SQL 生成、数据库迁移等。

**主要特点**：
- 成熟稳定：10+ 年成熟框架
- 灵活性高：支持 SQL 和 ORM 混用
- 功能全面：连接池、迁移工具、事件系统
- 文档丰富：完善的文档和教程

## 安装

```bash
pip install sqlalchemy
```

## 基本使用

### 1. 创建数据库连接

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建引擎
engine = create_engine("sqlite:///test.db", echo=True)

# 创建基类
Base = declarative_base()

# 创建会话工厂
SessionLocal = sessionmaker(bind=engine)
```

### 2. 定义模型

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer, default=0)
    created_at = Column(Integer, default=0)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
```

### 3. 创建表

```python
# 创建所有表
Base.metadata.create_all(engine)
```

### 4. 增删改查

```python
# 创建会话
session = SessionLocal()

# 创建用户
user = User(username="alice", email="alice@example.com", age=25)
session.add(user)
session.commit()

# 查询用户
user = session.query(User).filter_by(username="alice").first()
print(user)  # <User(id=1, username='alice')>

# 更新用户
user.age = 26
session.commit()

# 删除用户
session.delete(user)
session.commit()
```

## 高级功能

### 1. 关系映射

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    # 一对多关系
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(Text)

    # 外键
    user_id = Column(Integer, ForeignKey("users.id"))

    # 关系
    author = relationship("User", back_populates="posts")

# 使用关系
user = session.query(User).first()
for post in user.posts:
    print(post.title)
```

### 2. 查询操作

```python
# 简单查询
users = session.query(User).all()

# 按条件查询
users = session.query(User).filter(User.age > 18).all()

# 排序
users = session.query(User).order_by(User.username).all()

# 限制结果
users = session.query(User).limit(10).all()

# 聚合函数
count = session.query(User).count()
average_age = session.query(User.age).aggregate(func.avg(User.age))

# 组合条件
users = session.query(User).filter(
    User.age > 18,
    User.username.like("a%")
).all()
```

### 3. 多对多关系

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    # 多对多关系
    posts = relationship("Post", secondary="user_posts", back_populates="users")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    users = relationship("User", secondary="user_posts", back_populates="posts")

# 中间表
class UserPost(Base):
    __tablename__ = "user_posts"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
```

### 4. 链式查询

```python
# 链式查询
user = session.query(User) \
    .filter(User.id == 1) \
    .first()

# 链式过滤和排序
users = session.query(User) \
    .filter(User.age > 18) \
    .filter(User.is_active == True) \
    .order_by(User.username) \
    .limit(10) \
    .all()
```

### 5. 数据库迁移

```python
from flask_migrate import Migrate
from app import app, db

# 集成到 Flask 应用
migrate = Migrate(app, db)

# 迁移命令
# flask db init
# flask db migrate -m "description"
# flask db upgrade
```

## 最佳实践

### 1. Session 管理

```python
from contextlib import contextmanager

@contextmanager
def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# 使用
with get_db() as db:
    user = db.query(User).first()
```

### 2. 模型继承

```python
class BaseUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(100))

class AdminUser(BaseUser):
    __tablename__ = "admin_users"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    permissions = Column(String(200))
```

## 相关资源

- [SQLAlchemy 官方文档](https://www.sqlalchemy.org/)
- [SQLAlchemy 2.0 文档](https://docs.sqlalchemy.org/en/20/)

## 相关笔记

- [[fastapi]] - FastAPI Web 框架
- [[flask]] - Flask Web 框架

---

**创建日期**: 2026-03-15
**最后更新**: 2026-03-15
