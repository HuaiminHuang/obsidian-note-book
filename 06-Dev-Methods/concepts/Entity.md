---
title: Entity - 实体对象
tags: [development, entity, domain-entity]
status: learning
difficulty: intermediate
time_spent: 1h
created: 2026-03-15
updated: 2026-03-15
---

# Entity - 实体对象

## 概念

Entity (实体) 是领域驱动设计（DDD）中的核心概念，代表业务领域中的重要对象。Entity 具有唯一标识，即使属性值相同，不同的实例也是不同的对象。

**主要特点**：
- 具有唯一标识
- 生命周期独立
- 生命周期中的行为不变
- 与数据库表结构可能不完全对应

## 用法

Entity 与 PO 的区别：
- PO：直接映射数据库表
- Entity：代表业务概念，可能与表结构不同
- 在 DDD 中，Entity 封装业务规则

## 示例

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class OrderItem:
    """订单项实体"""
    product_id: str
    quantity: int
    unit_price: float

@dataclass
class Order:
    """订单实体（DDD 风格）"""
    order_id: str  # 实体标识，不一定是数据库自增 ID
    customer_id: str
    items: List[OrderItem]
    status: str = "pending"
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

    def total_amount(self) -> float:
        """计算订单总金额（业务逻辑）"""
        return sum(item.quantity * item.unit_price for item in self.items)

    def can_cancel(self) -> bool:
        """检查订单是否可取消（业务规则）"""
        # 业务规则：已发货或已完成订单不可取消
        return self.status in ["pending", "confirmed"]

    def cancel(self):
        """取消订单（业务操作）"""
        if not self.can_cancel():
            raise ValueError("订单不可取消")

        self.status = "cancelled"

    def add_item(self, product_id: str, quantity: int, unit_price: float):
        """添加订单项（业务操作）"""
        item = OrderItem(product_id, quantity, unit_price)
        self.items.append(item)

    def remove_item(self, product_id: str):
        """移除订单项"""
        self.items = [item for item in self.items if item.product_id != product_id]

# 使用 Entity
order = Order(
    order_id="ORD-001",
    customer_id="CUST-123",
    items=[
        OrderItem("P-001", 2, 99.99),
        OrderItem("P-002", 1, 199.99)
    ]
)

print(f"订单总金额: ${order.total_amount()}")
print(f"订单状态: {order.status}")
print(f"是否可取消: {order.can_cancel()}")

# 业务操作
try:
    order.cancel()
    print(f"取消后的状态: {order.status}")
except ValueError as e:
    print(f"取消失败: {e}")
```

## Entity 设计模式

### 聚合设计

```python
class Order:
    # 实体
    pass

class OrderItem:
    # 值对象
    pass

class Customer:
    # 聚合根
    pass
```

### 等价性判断

```python
def __eq__(self, other):
    if not isinstance(other, Order):
        return False
    return self.order_id == other.order_id

def __hash__(self):
    return hash(self.order_id)
```

## 相关资源

- [Domain-Driven Design](https://martinfowler.com/tags/domain%20driven%20design.html)
- [Entity Pattern](https://en.wikipedia.org/wiki/Entity_pattern)

## 相关笔记

- [[DDD]] - 领域驱动设计
- [[PO]] - 持久化对象
- [[BO]] - 业务对象
- [[Value Object]] - 值对象

---

**创建日期**: 2026-03-15
**最后更新**: 2026-03-15
