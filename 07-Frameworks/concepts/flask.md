---
title: Flask - 轻量级 Web 框架
tags: [python, framework, flask, web]
date: 2026-03-15
status: learning
difficulty: intermediate
---

# Flask - 轻量级 Web 框架

## 概念

Flask 是一个轻量级 Python Web 框架，被称为"微框架"。它灵活、简单、可扩展，适合小型项目和学习。

**主要特点**：
- 轻量级：核心简单，易于学习
- 灵活：选择你的扩展和工具
- 可扩展：丰富的扩展生态
- 易于测试：测试友好

## 快速开始

### 安装

```bash
pip install flask
```

### 基本示例

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify({"users": ["Alice", "Bob"]})

if __name__ == "__main__":
    app.run(debug=True)
```

### 运行服务

```bash
python app.py

# 访问
http://localhost:5000
http://localhost:5000/api/users
```

## 核心功能

### 1. 路由和端点

```python
@app.route("/users/<int:user_id>")
def get_user(user_id):
    return f"User ID: {user_id}"

@app.route("/api/items", methods=["POST"])
def create_item():
    data = request.get_json()
    return {"name": data.get("name"), "price": data.get("price")}
```

### 2. 请求方法

```python
@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        return "GET users"
    elif request.method == "POST":
        return "POST users"
```

### 3. 路由参数

```python
@app.route("/users/<username>")
def show_user_profile(username):
    return f"User: {username}"

@app.route("/users/<int:user_id>/posts/<int:post_id>")
def show_user_post(user_id, post_id):
    return f"User {user_id}, Post {post_id}"
```

### 4. 请求验证

```python
from flask import request

@app.route("/api/items", methods=["POST"])
def create_item():
    data = request.get_json()

    # 简单验证
    if not data or "name" not in data:
        return {"error": "Missing name"}, 400

    return {"name": data["name"], "price": data.get("price", 0)}
```

### 5. 响应格式

```python
from flask import jsonify

@app.route("/api/items")
def get_items():
    items = [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"}
    ]
    return jsonify(items)
```

### 6. 错误处理

```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500
```

### 7. 配置

```python
app = Flask(__name__)

# 加载配置
app.config["SECRET_KEY"] = "your-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 使用配置
@app.route("/config")
def show_config():
    return app.config["SECRET_KEY"]
```

### 8. 模板渲染

```python
from flask import render_template

@app.route("/users/<username>")
def user_profile(username):
    return render_template("user.html", name=username)
```

## Flask-RESTful 扩展

```python
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class UserResource(Resource):
    def get(self, user_id):
        return {"id": user_id, "name": "Alice"}

    def post(self):
        return {"message": "Created user"}, 201

class UserListResource(Resource):
    def get(self):
        return {"users": []}

api.add_resource(UserListResource, "/api/users")
api.add_resource(UserResource, "/api/users/<int:user_id>")

if __name__ == "__main__":
    app.run(debug=True)
```

## 实际应用

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# 配置
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 初始化扩展
db = SQLAlchemy(app)
ma = Marshmallow(app)

# 数据模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def to_dict(self):
        return {"id": self.id, "username": self.username}

# 序列化器
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "email")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# 路由
@app.route("/api/users/<int:user_id>")
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user))

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User(username=data["username"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

## 相关资源

- [Flask 官方文档](https://flask.palletsprojects.com/)
- [Flask-RESTful 文档](https://flask-restful.readthedocs.io/)

## 相关笔记

- [[fastapi]] - FastAPI Web 框架
- [[sqlalchemy]] - Python ORM

---

**创建日期**: 2026-03-15
**最后更新**: 2026-03-15
