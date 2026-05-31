---
title: TypeScript Utility Types（Record、Partial、Pick、Omit）
tags: [typescript, utility-types, learning]
status: learning
difficulty: intermediate
date: 2026-05-25
updated: 2026-05-25
---

# TypeScript Utility Types

## 概念

> TS 内置的工具类型，基于已有类型派生出新类型，避免重复定义。

## Record<K, V> — 类型安全的字典

> key 都是 K 类型、value 都是 V 类型的对象。

```ts
// 不用 Record
const icons: { [key: string]: string } = {};

// 用 Record — 更简洁
const icons: Record<string, string> = {};
```

### Python 对比

```python
# Python — 不强制
icons: dict[str, str] = {}
icons[123] = 1     # 运行时才报错

# TS — 编译期报错
const icons: Record<string, string> = {};
icons[123] = 1;    // 编译报错
```

### ClawX 实际使用

```ts
// src/types/channel.ts — 每种通道类型对应一个图标
export const CHANNEL_ICONS: Record<ChannelType, string> = {
  whatsapp: '📱',
  wechat: '💬',
  telegram: '✈️',
  discord: '🎮',
  // 少写任何一个 ChannelType 都编译报错
};
```

## Partial<T> — 所有属性变可选

> 更新操作时，用户可能只改部分字段。

```ts
interface ProviderConfig {
  id: string;
  name: string;
  apiKey: string;
  createdAt: string;
  updatedAt: string;
}

// 更新参数只传要改的部分
function updateProvider(updates: Partial<ProviderConfig>) {}
updateProvider({ name: '新名称' });   // 可以，只改 name
updateProvider({});                    // 可以，空对象也行
```

### 不用 Partial 的话

```ts
function updateProvider(updates: ProviderConfig) {}
updateProvider({ name: '新名称' });   // 报错：缺少 id、apiKey 等
```

### ClawX 实际使用

```ts
// src/stores/providers.ts:52
updateProvider: (
  providerId: string,
  updates: Partial<ProviderConfig>,
  apiKey?: string,
) => Promise<void>;
```

## Pick<T, K> — 只取部分属性

> 从大类型中提取子集。

```ts
interface ChatState {
  messages: [];
  loading: boolean;
  error: string | null;
  sendMessage: () => void;
  loadSessions: () => void;
  // 上百个属性...
}

type SessionRunState = Pick<
  ChatState,
  'sending' | 'activeRunId' | 'streamingText' | 'streamingMessage'
>;
// 只包含 4 个属性，ChatState 里其他属性都不包含
```

### ClawX 实际使用

```ts
// src/stores/chat.ts:86
type SessionRunState = Pick<
  ChatState,
  'sending' | 'activeRunId' | 'pendingFinal'
  | 'lastUserMessageAt' | 'streamingText' | 'streamingMessage'
  | 'streamingTools' | 'pendingToolImages'
>;
```

## Omit<T, K> — 排除某些属性

> Pick 的反操作，排除不要的属性。

```ts
// 添加时不需要传自动生成的字段
addProvider: (
  config: Omit<ProviderConfig, 'createdAt' | 'updatedAt'>,
  apiKey?: string,
) => Promise<void>;

// 调用
store.addProvider({ id: 'prov_001', name: 'OpenAI' });  // 不需要 createdAt
```

### ClawX 实际使用

```ts
// src/stores/providers.ts:50
addProvider: (
  config: Omit<ProviderConfig, 'createdAt' | 'updatedAt'>,
  apiKey?: string,
) => Promise<void>;
```

## 汇总

| 工具类型 | 作用 | Python 类比 |
|---------|------|-------------|
| `Record<K, V>` | key → value 的字典 | `dict[K, V]`（不强制） |
| `Partial<T>` | 所有属性变可选 | `TypedDict(total=False)` |
| `Pick<T, K>` | 只取部分属性 | 无直接等价 |
| `Omit<T, K>` | 排除部分属性 | 无直接等价 |

### 常用场景

- `Record` — 枚举映射、配置表
- `Partial` — 更新操作（PATCH 请求）
- `Pick` — 从大状态中提取子集
- `Omit` — 创建时排除自动生成字段

## 相关笔记

- [[ts-type-system]] — 类型注解、联合类型、interface
- [[ts-generics]] — 泛型 <T>

---

**创建日期**: 2026-05-25
**最后更新**: 2026-05-25
