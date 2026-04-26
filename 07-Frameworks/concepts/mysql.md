---
title: MySQL - 关系型数据库
tags: [python, framework, database, mysql]
date: 2026-03-15
status: learning
difficulty: intermediate
---

# MySQL - 关系型数据库

## 概念

MySQL 是世界上最流行的开源关系型数据库管理系统，使用 SQL（结构化查询语言）进行数据管理。MySQL 支持多用户、多线程、ACID 事务，适合 Web 应用。

**主要特点**：
- 开源免费：GPL 协议，可自由使用
- 性能优秀：查询优化、索引、缓存
- 可靠性高：ACID 事务、备份恢复
- 可扩展性：支持主从复制、集群

## 安装

```bash
# Docker 安装
docker run -d --name mysql \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=mydb \
  mysql:8.0

# 启动 MySQL
docker start mysql

# 连接
mysql -u root -p
```

## 基本使用

### 1. 安装 Python 客户端

```bash
pip install mysql-connector-python pymysql
```

### 2. 连接数据库

```python
import mysql.connector

# 连接数据库
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="rootpassword",
    database="mydb"
)

# 创建游标
cursor = conn.cursor()

print("MySQL 连接成功")
```

### 3. 创建表

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    age INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

```python
# 执行 SQL
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        age INT DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.commit()
```

### 4. 插入数据

```python
# 单条插入
cursor.execute(
    "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
    ("alice", "alice@example.com", 25)
)
conn.commit()

# 批量插入
users = [
    ("bob", "bob@example.com", 30),
    ("charlie", "charlie@example.com", 28)
]
cursor.executemany(
    "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
    users
)
conn.commit()
```

### 5. 查询数据

```python
# 查询单条
cursor.execute("SELECT * FROM users WHERE id = %s", (1,))
user = cursor.fetchone()
print(user)  # (1, 'alice', 'alice@example.com', 25, datetime(...))

# 查询多条
cursor.execute("SELECT * FROM users WHERE age > 18")
users = cursor.fetchall()
for user in users:
    print(user)

# 查询特定列
cursor.execute("SELECT username, email FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)  # ('alice', 'alice@example.com')

# 使用字典游标
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM users WHERE id = 1")
user = cursor.fetchone()
print(user)  # {'id': 1, 'username': 'alice', 'email': 'alice@example.com', ...}
```

### 6. 更新数据

```python
# 更新数据
cursor.execute(
    "UPDATE users SET age = %s WHERE username = %s",
    (26, "alice")
)
conn.commit()

# 更新多行
cursor.execute(
    "UPDATE users SET age = age + 1 WHERE age < 30"
)
conn.commit()
```

### 7. 删除数据

```python
# 删除数据
cursor.execute("DELETE FROM users WHERE username = 'bob'")
conn.commit()

# 删除多条
cursor.execute("DELETE FROM users WHERE id > 10")
conn.commit()
```

## 高级功能

### 1. 事务

```python
try:
    # 开始事务
    conn.start_transaction()

    # 执行操作
    cursor.execute("INSERT INTO users (username, email, age) VALUES (%s, %s, %s)", ("david", "david@example.com", 35))
    cursor.execute("UPDATE users SET age = age + 1 WHERE username = 'alice'")

    # 提交事务
    conn.commit()
    print("事务提交成功")

except mysql.connector.Error as err:
    # 回滚事务
    conn.rollback()
    print(f"事务回滚: {err}")
```

### 2. 预处理语句（防止 SQL 注入）

```python
# 使用 %s 参数化查询
user_id = input("Enter user ID: ")

# 安全查询
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
user = cursor.fetchone()
```

### 3. 连接池

```python
from mysql.connector import pooling

# 创建连接池
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    host="localhost",
    port=3306,
    user="root",
    password="rootpassword",
    database="mydb"
)

# 从池中获取连接
conn = connection_pool.get_connection()
cursor = conn.cursor()

# 使用连接
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

# 释放连接回池
cursor.close()
conn.close()
```

### 4. 查询优化

```python
# 使用索引
cursor.execute("CREATE INDEX idx_email ON users(email)")

# 使用 LIMIT 分页
page = 1
page_size = 10
offset = (page - 1) * page_size

cursor.execute(
    "SELECT * FROM users LIMIT %s OFFSET %s",
    (page_size, offset)
)
users = cursor.fetchall()

# 使用 WHERE 子句过滤
cursor.execute("SELECT * FROM users WHERE age > 25 AND is_active = 1")
active_users = cursor.fetchall()

# 使用 JOIN 查询
cursor.execute("""
    SELECT users.username, orders.order_id
    FROM users
    JOIN orders ON users.id = orders.user_id
    WHERE users.age > 20
""")
```

## 实际应用

### 1. 用户管理系统

```python
class UserRepository:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor(dictionary=True)

    def create_user(self, username, email, age):
        """创建用户"""
        self.cursor.execute(
            "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
            (username, email, age)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_user(self, user_id):
        """获取用户"""
        self.cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return self.cursor.fetchone()

    def get_users_by_age(self, min_age, max_age):
        """根据年龄范围获取用户"""
        self.cursor.execute(
            "SELECT * FROM users WHERE age BETWEEN %s AND %s",
            (min_age, max_age)
        )
        return self.cursor.fetchall()

    def update_user(self, user_id, **kwargs):
        """更新用户信息"""
        set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        values = list(kwargs.values()) + [user_id]
        self.cursor.execute(
            f"UPDATE users SET {set_clause} WHERE id = %s",
            values
        )
        self.conn.commit()

    def delete_user(self, user_id):
        """删除用户"""
        self.cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        self.conn.commit()

# 使用
repo = UserRepository(conn)
user_id = repo.create_user("alice", "alice@example.com", 25)
user = repo.get_user(user_id)
users = repo.get_users_by_age(20, 30)
```

## 相关资源

- [MySQL 官方文档](https://dev.mysql.com/doc/)
- [MySQL Python 客户端](https://pymysql.readthedocs.io/)

## 相关笔记

- [[sqlalchemy]] - SQLAlchemy ORM 框架
- [[redis]] - Redis 数据库
- [[milvus]] - Milvus 向量数据库

---

**创建日期**: 2026-03-15
**最后更新**: 2026-03-15
