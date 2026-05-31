---
title: TypeScript 泛型 + keyof
tags: [typescript, generics, keyof, learning]
status: learning
difficulty: intermediate
date: 2026-05-25
updated: 2026-05-25
---

# TypeScript 泛型 + keyof

## 概念

> 泛型让函数/接口可以适用于任何类型，同时保留类型信息。相当于"类型参数化"。

## 基础用法

### 不用泛型 — 丢失类型或重复定义

```ts
// 用 any — 丢失类型检查
function identity(value: any): any {
  return value;
}
identity('hello').toFixed();  // 运行时才炸

// 不用 any — 每类型写一遍
function identityNum(value: number): number { return value; }
function identityStr(value: string): string { return value; }
```

### 用泛型

```ts
function identity<T>(value: T): T {
  return value;
}

const a = identity('hello');  // T 推断为 string
const b = identity(42);       // T 推断为 number
a.toFixed();                  // 编译报错
```

### Python 对比

```python
from typing import TypeVar

T = TypeVar('T')

def identity(value: T) -> T:   # 写法几乎一样
    return value
```

## 泛型接口

```ts
interface GatewayRpcResponse<T = unknown> {
  success: boolean;
  result?: T;
  error?: string;
}

// 使用
const res: GatewayRpcResponse<Channel[]> = {
  success: true,
  result: [{ id: 'ch_001' }],
};
```

`T = unknown` 表示默认类型，不传类型参数时不会报错。

## 泛型函数

```ts
export async function invokeApi<T>(
  channel: string,
  ...args: unknown[]
): Promise<T> {
  // ...
}

// 调用时指定 T，返回值自动获得类型
const channels = await invokeApi<Channel[]>('channel:list');
// channels 的类型是 Channel[]
```

## ClawX 实际使用

```ts
// src/lib/api-client.ts — 核心 API 调用函数
export async function invokeApi<T>(
  channel: string,
  ...args: unknown[]
): Promise<T> {
  const response = await ipc.invoke(channel, ...args);
  return response as T;
}

// src/types/gateway.ts — 泛型接口
export interface GatewayRpcResponse<T = unknown> {
  success: boolean;
  result?: T;
  error?: string;
}
```

## keyof + 泛型约束

### keyof：取所有 key 组成联合类型

```ts
interface Channel {
  id: string;
  name: string;
  status: string;
}

type ChannelKey = keyof Channel;
// 等价于：'id' | 'name' | 'status'
```

### K extends keyof T：限定 key 必须在范围内

```ts
async function getSetting<K extends keyof AppSettings>(
  key: K
): Promise<AppSettings[K]> {
  const store = await getSettingsStore();
  return store.get(key);
}

// 调用时
getSetting('theme');      // 返回值类型是 string
getSetting('fontSize');   // 返回值类型是 number
getSetting('notExist');   // 编译报错！
```

### ClawX 实际使用

```ts
// electron/utils/store.ts:130
export async function getSetting<K extends keyof AppSettings>(
  key: K
): Promise<AppSettings[K]> {
  const store = await getSettingsStore();
  return store.get(key);
}

export async function setSetting<K extends keyof AppSettings>(
  key: K,
  value: AppSettings[K]
): Promise<void> {
  const store = await getSettingsStore();
  store.set(key, value);
}
```

## 相关笔记

- [[ts-type-system]] — 类型注解、联合类型、interface
- [[ts-utility-types]] — Record、Partial、Pick、Omit
- [[ts-async]] — 异步编程 Promise/async-await

---

**创建日期**: 2026-05-25
**最后更新**: 2026-05-25
