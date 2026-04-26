---
title: DDD - 领域驱动设计
tags: [development, ddd, domain-driven-design]
status: completed
difficulty: advanced
time_spent: 3h
date: 2026-03-15
updated: 2026-03-15
---

# DDD - 领域驱动设计

## 概念

领域驱动设计（Domain-Driven Design, DDD）是一种软件开发方法论，强调以领域模型为核心，解决复杂业务问题。DDD 将软件设计与业务领域紧密结合，提高系统的可维护性和可扩展性。

**核心思想**：
- 基于领域建模
- 建立统一语言
- 划分界限上下文
- 关注核心域、支撑域、通用域

## DDD 四大核心概念

### 1. 领域模型

领域模型是业务概念的抽象，包含业务逻辑和规则。

```python
class Order:
    """订单聚合根"""
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.items = []
        self.status = "pending"

    def add_item(self, product: Product, quantity: int):
        """添加订单项"""
        self.items.append(OrderItem(product, quantity))

    def total_amount(self) -> float:
        """计算总金额"""
        return sum(item.quantity * item.unit_price for item in self.items)

class Product:
    """产品实体"""
    pass

class OrderItem:
    """订单项值对象"""
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
```

### 2. 限界上下文

限界上下文定义了业务领域中一个明确的边界，负责特定的业务领域。

```python
# 订单上下文
class OrderContext:
    """订单限界上下文"""
    def __init__(self):
        self.order_service = OrderService()

# 用户上下文
class UserContext:
    """用户限界上下文"""
    def __init__(self):
        self.user_service = UserService()
```

### 3. 聚合

聚合是一组相关对象的集合，定义了聚合边界和不变性约束。

```python
class Order:
    """订单聚合根"""
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.items = []

    def add_item(self, item: OrderItem):
        """添加订单项（聚合内部操作）"""
        self.items.append(item)

class OrderItem:
    """订单项（聚合内部对象）"""
    pass
```

### 4. 领域服务

领域服务处理跨聚合的业务逻辑。

```python
class OrderService:
    """订单领域服务"""
    def place_order(self, customer_id: str, items: List[OrderItem]) -> Order:
        """创建订单（领域服务方法）"""
        # 业务规则验证
        if not self._validate_items(items):
            raise ValueError("订单项无效")

        # 创建订单
        order = Order(str(uuid.uuid4()))
        order.add_items(items)

        return order

    def _validate_items(self, items: List[OrderItem]) -> bool:
        """验证订单项"""
        # 验证逻辑
        return True
```

## DDD 分层架构

```python
# 1. 用户接口层 (User Interface)
@app.get("/orders/{order_id}")
def get_order(order_id: str):
    """REST API 接口"""
    order = order_service.get_order(order_id)
    return order.to_dto()

# 2. 应用层 (Application)
class OrderService:
    """订单应用服务"""
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
        self.domain_service = OrderDomainService()

    def get_order(self, order_id: str) -> Order:
        """获取订单"""
        return self.order_repository.find(order_id)

# 3. 领域层 (Domain)
class Order:
    """订单聚合根"""
    def __init__(self, order_id: str):
        self.order_id = order_id

    def cancel(self):
        """取消订单（领域方法）"""
        self.status = "cancelled"

# 4. 基础设施层 (Infrastructure)
class OrderRepository:
    """订单仓储（基础设施）"""
    def find(self, order_id: str) -> Order:
        """从数据库查询"""
        # ORM 操作
        pass

    def save(self, order: Order):
        """保存到数据库"""
        pass
```

## DDD 实践原则

### 1. 统一语言

与业务专家建立共同语言，避免技术与业务术语冲突。

```python
class Order:  # 业务术语：订单
    """订单"""
    pass

class OrderItem:  # 业务术语：订单项
    """订单项"""
    pass
```

### 2. 分层关注

- 领域层：核心业务逻辑
- 应用层：流程编排
- 基础设施层：技术实现
- 用户接口层：接口展示

### 3. 优先复杂度而非功能

关注复杂业务场景，而非简单 CRUD。

## 相关资源

- [Domain-Driven Design](https://martinfowler.com/tags/domain%20driven%20design.html)
- [Eric Evans DDD](https://www.domainlanguage.com/ddd/)

## 相关笔记

- [[entity]] - 实体对象
- [[bo]] - 业务对象
- [[specs]] - 规范模式
- [[tdd]] - 测试驱动开发

---

**创建日期**: 2026-03-15
**最后更新**: 2026-03-15
