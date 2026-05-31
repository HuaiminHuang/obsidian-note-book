---
title: TypeScript 常用语法速查（箭头函数、可选链、运算符等）
tags: [typescript, syntax, learning]
status: learning
difficulty: beginner
date: 2026-05-25
updated: 2026-05-25
---

# TypeScript 常用语法速查

> 从 Python 视角学习 JS/TS 常用语法，附 ClawX 实际例子。

## 箭头函数

```ts
// 短形式（单表达式，省略 return）
sessions.filter((session) => !session.key.endsWith(':main'))
```
```python
[s for s in sessions if not s.key.endswith(':main')]
```

```ts
// 长形式（多语句，需要 return）
attachedFiles.map((file, i) => {
  const isImage = file.mimeType.startsWith('image/');
  return isImage ? null : file;
})
```
```python
# Python 的列表推导或 lambda
[None if f.mime_type.startswith('image/') else f for i, f in enumerate(attached_files)]
```

## 可选链 ?.

> 安全访问对象深层属性，中间有 null/undefined 返回 undefined 不报错。

```ts
// 没有 ?. — 每层都要判断
if (user && user.profile && user.profile.name) { ... }

// 有 ?.
user?.profile?.avatar ?? 'default.png'
```

```python
# Python — 没有等价，需要 try/except 或 getattr
avatar = getattr(getattr(user, 'profile', None), 'avatar', None) or 'default.png'
```

## 空值合并 ??

> 只在值为 null/undefined 时才用默认值。

```ts
// ?? — 只排除 null/undefined
0 ?? 10          // 0（保留 0）
'' ?? 'default'  // ''（保留空字符串）
null ?? 'x'      // 'x'
undefined ?? 'x' // 'x'

// || — 排除所有假值
0 || 10          // 10（0 被覆盖了！）
```

```python
# Python — 没有 ??，|| 行为近似
x = 0 or 10           # 10 — 但 0 可能是有意义的
x = 0 if 0 is not None else 10  # 0 — 太长
```

## 逻辑运算符 || &&

```ts
// || — 返回第一个真值
'a' || 'b'          // 'a'
'' || 'default'    // 'default'

// && — 返回第一个假值
'a' && 'b'         // 'b'（都真返回最后一个）
'' && 'b'          // ''（遇到假值直接返回）
```

| JS | Python | 说明 |
|----|--------|------|
| `\|\|` | `or` | 第一个真值 |
| `&&` | `and` | 第一个假值 |
| `??` | 无 | 第一个非 null/undefined |

## 模板字符串

```ts
const newKey = `${prefix}:session-${Date.now()}`;
```
```python
new_key = f"{prefix}:session-{int(time.time() * 1000)}"
```

**完全一样，** 只是 JS 用反引号 `` ` ``，Python 用 `f""`。

## 解构赋值

```ts
const { t } = useTranslation('chat');          // 取一个属性
const { currentSessionKey } = get();           // 从 store 取状态
const [first, second] = [1, 2];                // 数组解构
```

```python
# Python
t = use_translation('chat')  # 只能逐个取
first, second = [1, 2]       # 数组解构一样
```

## .map() / .filter() / .reduce()

```ts
arr.map(x => x * 2)              // 映射
arr.filter(x => x > 1)           // 过滤
arr.reduce((acc, x) => acc + x, 0)  // 累积
arr.find(x => x > 1)             // 找第一个
arr.some(x => x > 1)             // 是否有满足的
arr.every(x => x > 1)            // 是否都满足
```

```python
[x * 2 for x in arr]                           # map
[x for x in arr if x > 1]                      # filter
functools.reduce(lambda a, x: a + x, arr, 0)   # reduce
next((x for x in arr if x > 1), None)          # find
any(x > 1 for x in arr)                        # some
all(x > 1 for x in arr)                        # every
```

## for...of 遍历

```ts
for (const message of messages) {
  if (message._attachedFiles?.length) { ... }
}
```
```python
for message in messages:
    if getattr(message, '_attached_files', []) and len(message._attached_files):
        ...
```

## try/catch

```ts
// 不需要错误变量时可以省略 (err)
try {
  const raw = JSON.parse(str);
} catch { /* 忽略解析错误 */ }

// 需要错误信息时
try {
  await invokeApi('channel:list');
} catch (error) {
  console.warn('失败:', error);
}
```
```python
# Python — 不能省略 except 后的异常类型
try:
    raw = json.loads(s)
except Exception:
    pass
```

## export / import

```ts
// 命名导出 — 一个文件可以有多个
export function createHistoryActions(set, get) { ... }
export const useChatStore = create<ChatState>((set, get) => ({...}));

// 默认导出 — 一个文件只能一个
export default Chat;

// 命名导入
import { useChatStore, type RawMessage } from '@/stores/chat';

// 类型专用导入（编译时删除）
import type { ChatGet, ChatSet } from './store-api';
```

```python
# Python — 所有 def/class 都是"命名导出"
# 没有默认导出概念
from stores.chat import use_chat_store, RawMessage
```

| JS/TS | Python | 注意 |
|-------|--------|------|
| `export function` | 不需要关键字 | 所有 def 自动导出 |
| `export default X` | 无概念 | 文件最核心的导出 |
| `import { a } from './x'` | `from x import a` | 一样 |
| `import type { T }` | 无 | TS 独有，编译后消失 |

## .then() / .catch()

```ts
rpc('config.get', {}, 5_000)
  .then((snapshot) => { ... })
  .catch(() => { /* 默认值 */ })
  .finally(() => { /* 清理 */ });
```
```python
# Python 没有 .then() 写法，用 await
try:
    snapshot = await rpc('config.get', {}, 5_000)
except Exception:
    pass
finally:
    ...
```

**现代 TS 代码通常用 `async/await` 代替 `.then()`。**

## ClawX 实际代码汇总

```ts
// 箭头函数 + 链式操作
sessions
  .filter((session) => !session.key.endsWith(':main'))
  .map((session) => [session.key, session.label || ''])

// 可选链 + 空值合并
const key = `${gatewayStatus?.pid ?? 'none'}:${gatewayStatus?.connectedAt ?? 'none'}`;

// 模板字符串
const newKey = `${prefix}:session-${Date.now()}`;

// 解构
const { t } = useTranslation('chat');

// try/catch
try {
  const result = await hostApiFetch(url);
} catch (error) {
  console.warn('失败:', error);
}
```

## 相关笔记

- [[ts-type-system]] — 类型系统基础
- [[ts-async]] — 异步编程 Promise/async-await

---

**创建日期**: 2026-05-25
**最后更新**: 2026-05-25
