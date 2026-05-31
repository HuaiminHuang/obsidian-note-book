---
title: as const + typeof 模式（TypeScript）
tags: [typescript, as-const, pattern, learning]
status: learning
difficulty: intermediate
date: 2026-05-25
updated: 2026-05-25
---

# as const + typeof 模式

## 概念

> ClawX 中替代 `enum` 的惯用写法。用于定义常量列表并从中提取类型，实现"一处定义 = 运行时值 + 编译期类型"。

## 用法

### 问题：不加 as const

```ts
const PROVIDER_TYPES = ['anthropic', 'openai', 'google'];
// TS 推断类型为 string[]，失去了每个元素的具体值
```

### 加了 as const

```ts
const PROVIDER_TYPES = ['anthropic', 'openai', 'google'] as const;
// TS 推断类型为 readonly ["anthropic", "openai", "google"]
// 每个元素的具体值保留了
```

### 提取类型

```ts
type ProviderType = (typeof PROVIDER_TYPES)[number];
// 等价于：type ProviderType = 'anthropic' | 'openai' | 'google'

function setProvider(p: ProviderType) { }
setProvider('anthropic');    // 可以
setProvider('deepseek');     // 编译报错
```

## as const vs enum

| 对比 | `enum` | `as const` + `typeof` |
|------|--------|----------------------|
| 编译后 | 生成 JS 对象代码 | 变成普通 const 数组 |
| 类型赋值 | 必须 `Enum.xxx` | 字符串直接传 |
| 数值映射 | 原生支持 | 需要额外映射对象 |
| 分组归属 | 天然分组 | 需要命名 |
| JSDoc 注释 | 每个成员独立注释 | 也可以 |
| 典型场景 | 协议错误码、事件类型 | 字符串列表、通道类型 |
| ClawX 使用量 | 4 个 enum（3 文件） | 75+ 处 as const |

### 什么时候用 enum

```ts
// 需要数值映射 + JSDoc → 用 enum
export enum JsonRpcErrorCode {
  /** Invalid JSON was received */
  PARSE_ERROR = -32700,
  /** The method does not exist */
  METHOD_NOT_FOUND = -32601,
}
```

### 什么时候用 as const

```ts
// 纯字符串列表 → 用 as const
const SUPPORTED_LANGUAGE_CODES = ['en', 'zh', 'ja', 'ru'] as const;
type LanguageCode = (typeof SUPPORTED_LANGUAGE_CODES)[number];
```

## as const 也用于对象

```ts
const ROLE = {
  admin: '管理员',
  user: '用户',
} as const;

// 不加 as const：ROLE.admin 的类型是 string
// 加了 as const：ROLE.admin 的类型是字面量 '管理员'
```

## Python 对比

```python
from typing import Literal

# Python 没有 as const，需要手动同步
LANGUAGES = ['en', 'zh', 'ja']
Language = Literal['en', 'zh', 'ja']  # 需要手动维护一致
```

## ClawX 实际使用

```ts
// shared/language.ts
export const SUPPORTED_LANGUAGE_CODES = ['en', 'zh', 'ja', 'ru'] as const;
export type LanguageCode = (typeof SUPPORTED_LANGUAGE_CODES)[number];

// src/lib/providers.ts
export const PROVIDER_TYPES = [
  'anthropic', 'openai', 'google', 'openrouter',
] as const;
export type ProviderType = (typeof PROVIDER_TYPES)[number];
```

## 相关笔记

- [[ts-type-system]] — 类型注解、联合类型、interface

---

**创建日期**: 2026-05-25
**最后更新**: 2026-05-25
