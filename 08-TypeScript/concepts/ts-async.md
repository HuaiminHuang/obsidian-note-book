---
title: TypeScript 异步编程（Promise / async-await）
tags: [typescript, async, promise, learning]
status: learning
difficulty: intermediate
date: 2026-05-25
updated: 2026-05-25
---

# TypeScript 异步编程

## 概念

> JS 是单线程事件循环（和 Python asyncio 一样）。`Promise` 是异步容器，`async/await` 是语法糖。

## 基础

```ts
async function fetchData(): Promise<string> {
  const result = await someAsyncTask();  // 暂停，不阻塞
  return result;
}
```

### Python 对比

```python
async def fetch_data() -> str:
    result = await some_async_task()
    return result
```

**语法几乎一样：** `async function` ↔ `async def`，`await` ↔ `await`。

## 核心差异

### 1. Promise 是"热的"（eager），协程是"冷的"（lazy）

```js
// JS — 声明时就立即执行
const p = fetch('/api/data');   // 请求已经发出去了！
await p;                        // 等待结果
```

```python
# Python — 声明时什么都不做
c = fetch_data()                 # 还没执行
await c                          # 这里才执行
```

### 2. JS 没有 asyncio.run()

```js
// JS — 顶层 await 可以直接用（模块中）
await fetchData();

// 或者直接调用 async 函数
async function main() { return await fetchData(); }
main();  // 返回 Promise
```

```python
# Python — 需要 asyncio.run
result = asyncio.run(fetch_data())
```

### 3. 错误处理

```js
// JS — try/catch 和 Python 一样
async function load() {
  try {
    const data = await fetchData();
    return data;
  } catch (err) {
    console.error('失败:', err);
    return fallback;
  }
}

// 也可以 .catch() 风格
fetchData()
  .then(data => console.log(data))
  .catch(err => console.error(err));
```

### 4. 并发执行

```js
// JS — Promise.all = Python 的 asyncio.gather
const [users, channels, settings] = await Promise.all([
  fetchUsers(),
  fetchChannels(),
  fetchSettings(),
]);
```

```python
# Python
users, channels, settings = await asyncio.gather(
    fetch_users(),
    fetch_channels(),
    fetch_settings(),
)
```

## 坑点

### 1. 忘了 await — 请求在后台默默跑

```ts
function saveChannel(id: string, data: Partial<Channel>) {
  invokeApi('channel:update', id, data);  // 请求发出去了！
  showSuccessToast();                      // 立刻显示成功，但实际可能失败
}

// ✅ 正确
async function saveChannel(id: string, data: Partial<Channel>) {
  try {
    await invokeApi('channel:update', id, data);
    showSuccessToast();
  } catch {
    showErrorToast();
  }
}
```

### 2. void 关键字 — 故意不等待

```ts
void loadMissingPreviews(enrichedMessages).then((updated) => {
  // void 告诉 TS："我故意不等这个 Promise"
});
```

### 3. 并发失控 — 循环里逐个 await 太慢

```ts
// ❌ 串行 — 太慢
for (const id of ids) {
  const data = await fetchData(id);
}

// ✅ 并发
const results = await Promise.all(ids.map(id => fetchData(id)));

// ✅ 限流（大批量时）
async function batchedFetch<T>(items: T[], batchSize = 5) {
  const results = [];
  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    const batchResults = await Promise.all(batch.map(item => fetchData(item)));
    results.push(...batchResults);
  }
  return results;
}
```

## JS vs Python 异步对比

| 概念 | JS | Python |
|------|-----|--------|
| 异步容器 | `Promise<T>` | `Future[T]` / `Coroutine` |
| 声明异步函数 | `async function` | `async def` |
| 等待 | `await` | `await` |
| 声明即执行 | **是**（Promise eager） | **否**（协程 lazy） |
| 顶层 await | 模块中直接支持 | 需要 `asyncio.run()` |
| 并发等待 | `Promise.all([...])` | `asyncio.gather(...)` |
| 错误处理 | `try/catch` 或 `.catch()` | `try/except` |
| 定时器 | `await new Promise(r => setTimeout(r, ms))` | `await asyncio.sleep(ms)` |
| 限流 | 需要手写 | `asyncio.Semaphore` |

## ClawX 实际使用

```ts
// src/stores/chat/session-actions.ts
async loadSessions() {
  this.loading = true;
  try {
    const sessions = await invokeApi<ChatSession[]>('session:list');
    this.sessions = sessions;
  } catch (err) {
    this.error = err.message;
  } finally {
    this.loading = false;
  }
}

// 并发获取多个资源
const [channels, agents, skills] = await Promise.all([
  invokeApi<Channel[]>('channel:list'),
  invokeApi<Agent[]>('agent:list'),
  invokeApi<Skill[]>('skill:list'),
]);
```

## 相关笔记

- [[ts-generics]] — 泛型（`Promise<T>` 也是泛型）
- [[ts-common-syntax]] — 常用语法（`.then()`、`try/catch`）

---

**创建日期**: 2026-05-25
**最后更新**: 2026-05-25
