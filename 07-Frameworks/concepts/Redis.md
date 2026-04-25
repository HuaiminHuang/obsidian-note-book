---
title: Redis - 内存数据库
tags: [python, framework, database, redis, cache]
date: 2026-03-15
status: learning
difficulty: intermediate
---

# Redis - 内存数据库

## 概念

Redis（Remote Dictionary Server）是一个开源的内存数据库，支持字符串、哈希、列表、集合、有序集合等多种数据结构。Redis 的特点是速度快、支持持久化、丰富的数据类型。

**主要特点**：
- 高性能：基于内存操作，速度快
- 数据类型丰富：字符串、哈希、列表、集合、有序集合
- 支持持久化：RDB 和 AOF 两种持久化方式
- 支持集群：分片和复制功能

## 安装

```bash
# Docker 安装
docker run -d -p 6379:6379 --name redis redis:latest

# 启动 Redis
docker start redis

# 命令行连接
redis-cli
```

## 基本使用

### 1. 安装 Python 客户端

```bash
pip install redis
```

### 2. 连接 Redis

```python
import redis

# 连接 Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# 测试连接
r.ping()
print("Redis 连接成功")
```

### 3. 基本数据操作

```python
# 字符串操作
r.set("name", "Alice")
r.set("age", "25")
value = r.get("name")
print(value)  # b'Alice'

# 哈希操作
r.hset("user:1", "name", "Alice")
r.hset("user:1", "age", "25")
r.hset("user:1", "email", "alice@example.com")
user_data = r.hgetall("user:1")
print(user_data)  # {b'name': b'Alice', b'age': b'25', b'email': b'alice@example.com'}

# 列表操作
r.lpush("tasks", "task1", "task2", "task3")
tasks = r.lrange("tasks", 0, -1)
print(tasks)  # [b'task3', b'task2', b'task1']

# 集合操作
r.sadd("tags", "python", "redis", "database")
tags = r.smembers("tags")
print(tags)  # {b'python', b'redis', b'database'}

# 有序集合操作
r.zadd("leaderboard", {"player1": 100, "player2": 200, "player3": 150})
ranking = r.zrange("leaderboard", 0, -1, withscores=True)
print(ranking)  # [(b'player1', 100.0), (b'player3', 150.0), (b'player2', 200.0)]
```

## 高级功能

### 1. 键过期

```python
# 设置过期时间（秒）
r.setex("session:user:123", 3600, "session_data")

# 设置过期时间（毫秒）
r.psetex("cache:key", 300000, "value")

# 检查剩余时间
ttl = r.ttl("session:user:123")
print(f"剩余时间: {ttl}秒")

# 删除过期键
r.expire("temp:key", 60)
```

### 2. 原子操作

```python
# 自增
count = r.incr("page_views")
print(count)  # 1

count = r.incr("page_views")
print(count)  # 2

# 自减
count = r.decr("inventory")
print(count)  # -1

# 设置值并获取旧值
old_value = r.set("counter", 10)
new_value = r.get("counter")
print(old_value)  # b'None'
print(new_value)  # b'10'
```

### 3. 事务

```python
# 开启事务
pipe = r.pipeline()

pipe.set("key1", "value1")
pipe.set("key2", "value2")
pipe.get("key1")
pipe.get("key2")

# 执行事务
results = pipe.execute()
print(results)  # [True, True, b'value1', b'value2']
```

### 4. 发布订阅

```python
# 发布者
import threading
import time

def publisher():
    r.publish("channel1", "message1")
    r.publish("channel1", "message2")

# 订阅者
def subscriber():
    pubsub = r.pubsub()
    pubsub.subscribe("channel1")

    for message in pubsub.listen():
        print(f"收到消息: {message}")

# 运行
threading.Thread(target=publisher, daemon=True).start()
threading.Thread(target=subscriber, daemon=True).start()
time.sleep(1)
```

## 实际应用

### 1. 缓存实现

```python
import time

def get_cached_data(key, get_data_func, ttl=60):
    """获取缓存数据"""
    # 先从缓存获取
    cached_data = r.get(key)
    if cached_data:
        return cached_data

    # 缓存未命中，从源获取
    data = get_data_func()
    r.setex(key, ttl, data)
    return data

# 使用缓存
def fetch_user_data(user_id):
    # 模拟从数据库获取
    return f"User {user_id} data"

user_data = get_cached_data(f"user:{123}", lambda: fetch_user_data(123), ttl=300)
print(user_data)
```

### 2. 限流实现

```python
def check_rate_limit(user_id, limit=10, window=60):
    """检查限流"""
    key = f"rate_limit:{user_id}"

    # 获取当前计数
    current = r.incr(key)

    # 第一次访问，设置过期时间
    if current == 1:
        r.expire(key, window)

    # 超过限制
    if current > limit:
        return False

    return True

# 使用限流
if check_rate_limit("user:123"):
    print("访问允许")
else:
    print("访问限制")
```

### 3. 会话管理

```python
import json
import secrets

class SessionManager:
    def __init__(self, redis):
        self.redis = redis

    def create_session(self, user_id):
        """创建会话"""
        session_id = secrets.token_urlsafe(32)
        session_data = {
            "user_id": user_id,
            "created_at": time.time()
        }
        self.redis.setex(f"session:{session_id}", 3600, json.dumps(session_data))
        return session_id

    def get_session(self, session_id):
        """获取会话"""
        session_data = self.redis.get(f"session:{session_id}")
        return json.loads(session_data) if session_data else None

    def delete_session(self, session_id):
        """删除会话"""
        self.redis.delete(f"session:{session_id}")

# 使用会话管理器
session_manager = SessionManager(r)
session_id = session_manager.create_session(123)
session = session_manager.get_session(session_id)
print(session)  # {'user_id': 123, 'created_at': ...}
```

## 相关资源

- [Redis 官方文档](https://redis.io/docs/)
- [Redis Python 客户端](https://redis-py.readthedocs.io/)

## 相关笔记

- [[Milvus]] - Milvus 向量数据库
- [[MySQL]] - MySQL 数据库

---

**创建日期**: 2026-03-15
**最后更新**: 2026-03-15
