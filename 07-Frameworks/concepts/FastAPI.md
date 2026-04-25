---
title: FastAPI - 现代高性能 Web 框架
tags: [python, framework, fastapi, web]
date: 2026-03-15
status: learning
difficulty: intermediate
---

# FastAPI - 现代高性能 Web 框架

## 概念

FastAPI 是一个现代、快速的 Web 框架，用于构建 API。它使用 Python 类型提示，自动生成文档，支持异步编程，性能接近 NodeJS 和 Go。

**主要优势**：
- 基于标准：Python 类型提示
- 自动文档：OpenAPI 和 Swagger UI
- 异步支持：高性能异步编程
- 数据验证：Pydantic
- 类型安全：编译时检查

## 快速开始

### 安装

```bash
pip install fastapi uvicorn
```

### 基本示例

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    email: str

@app.post("/users/")
async def create_user(user: User):
    return {"username": user.username, "email": user.email}

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 运行和文档

```bash
# 运行服务
uvicorn main:app --reload

# 访问文档
http://localhost:8000/docs
http://localhost:8000/redoc
```

## 核心功能

### 1. 路由和端点

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### 2. 请求体验证

```python
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}
```

### 3. 查询参数

```python
@app.get("/users/")
async def read_users(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

### 4. 响应模型

```python
from typing import List

@app.get("/users/", response_model=List[User])
async def read_users():
    return users
```

### 5. 中间件

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 6. 数据库集成

```python
from sqlalchemy.orm import Session

@app.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### 7. 异步编程

```python
import asyncio

@app.get("/items/")
async def read_items():
    # 模拟异步操作
    result = await asyncio.sleep(1)
    return {"result": result}
```

## 实际应用

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

app = FastAPI(title="用户管理系统")

# 依赖注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@app.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 创建用户
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

## 相关资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Pydantic 文档](https://docs.pydantic.dev/)

## 相关笔记

- [[Flask]] - Flask Web 框架
- [[SQLAlchemy]] - Python ORM

---

**创建日期**: 2026-03-15
**最后更新**: 2026-03-15
