---
title: TypeScript 类型系统（类型注解、联合类型、interface）
tags: [typescript, type-system, learning]
status: learning
difficulty: intermediate
date: 2026-05-25
updated: 2026-05-25
---

# TypeScript 类型系统

## 概念

> TS = JS + 静态类型系统。编译期检查类型，编译后生成纯 JS。所有类型注解编译后消失，零运行时开销。

## 基础类型注解

### 原始类型

```ts
const name: string = 'Tom';
const age: number = 25;
const isDone: boolean = true;
const empty: null = null;
const unk: undefined = undefined;
```

### 数组

```ts
const nums: number[] = [1, 2, 3];
const names: Array<string> = ['a', 'b'];  // 等价写法
```

### 对象 — 内联注解

```ts
const user: { name: string; age: number } = {
  name: 'Tom',
  age: 25,
};
```

### 函数

```ts
function add(a: number, b: number): number {
  return a + b;
}

const double = (x: number): number => x * 2;

// 可选参数 ?
function greet(name: string, title?: string): string {
  return title ? `${title} ${name}` : name;
}

// 默认值
function repeat(str: string, times: number = 2): string {
  return str.repeat(times);
}

// 无返回值
function log(msg: string): void {
  console.log(msg);
}

// any — 关闭类型检查，尽量避免
let x: any = 1;
x = 'hello';  // 不报错
```

## 联合类型 |

> 一个变量可以是几种类型之一。

```ts
let id: string | number;
id = 'abc123';   // 可以
id = 42;         // 可以
id = true;       // 报错
```

### 类型收窄（type narrowing）

```ts
function double(x: string | number) {
  if (typeof x === 'number') {
    return x * 2;    // TS 知道 x 是 number
  }
  return x.repeat(2); // TS 知道 x 是 string
}
```

## type 别名

> 给类型起名字，避免重复写。

```ts
type ChannelStatus = 'connected' | 'disconnected' | 'connecting' | 'degraded' | 'error';

function process(status: ChannelStatus) {}
```

### Python 对比

```python
from typing import Literal

ChannelStatus = Literal['connected', 'disconnected', 'connecting', 'degraded', 'error']
```

Python 不强制检查，TS 编译不过就不能运行。

## interface

> 定义一个对象必须包含什么属性、各是什么类型。编译后消失。

```ts
export interface Channel {
  id: string;
  type: ChannelType;
  name: string;
  status: ChannelStatus;
  accountId?: string;   // ? 可选属性
  avatar?: string;
  metadata?: Record<string, unknown>;
}
```

### interface vs type

```ts
// interface — 专门定义对象形状
interface User { name: string; age: number; }

// type — 更通用，联合类型/元组只能用 type
type User = { name: string; age: number; };
type Status = 'on' | 'off';
type Pair = [string, number];
```

### interface 继承

```ts
interface BaseChannel { id: string; name: string; }

interface Channel extends BaseChannel {
  type: ChannelType;
  // 继承了 id 和 name
}
```

### 作用

- **编辑器自动补全**：写 `ch.` 时列出所有属性
- **编译期检查**：传错参数/遗漏属性时报错
- **重构保护**：修改 interface 后所有用到的地方都报错

### Python 对比

```python
from typing import TypedDict

# TS interface → Python TypedDict
class Channel(TypedDict):
    id: str
    name: str
    status: str

# 但 Python 不强制检查（只有 mypy/pyright 会报错）
```

## ClawX 实际使用

```ts
// src/types/channel.ts — 接口定义
export interface Channel {
  id: string;
  type: ChannelType;
  name: string;
  status: ChannelStatus;
  accountId?: string;
  metadata?: Record<string, unknown>;
}

// src/types/channel.ts — type 别名（字符串联合类型）
export type ChannelType =
  | 'whatsapp'
  | 'wechat'
  | 'dingtalk'
  | 'telegram'
  | 'discord';

export type ChannelStatus = 'connected' | 'disconnected' | 'connecting' | 'degraded' | 'error';
```

## 相关笔记

- [[ts-utility-types]] — Record、Partial、Pick、Omit
- [[ts-generics]] — 泛型 <T>
- [[ts-type-guards]] — 类型守卫、as 断言
- [[ts-common-syntax]] — 常用语法速查

---

**创建日期**: 2026-05-25
**最后更新**: 2026-05-25
