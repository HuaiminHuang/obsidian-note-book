---
title: JS/TS 基础 — 从 Python 视角学习
tags: [typescript, javascript, python, learning]
status: learning
difficulty: intermediate
date: 2026-05-25
updated: 2026-05-25
---

# JS/TS 基础 — 从 Python 视角学习

> 基于 Airbnb JavaScript Style Guide，以 Python 开发者视角整理的核心知识点。

## 参考来源

- Airbnb JS Style Guide: `/home/h2mzzz/typescript-learn/javascript/README.md`
- ClawX 项目: `/home/h2mzzz/typescript-learn/ClawX/`

---

## 1. 类型系统

### 原始类型（值复制）

`string`, `number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`

```js
const foo = 1;
let bar = foo;    // 值复制，互不影响
bar = 9;
// foo=1, bar=9
```

### 复杂类型（引用复制）

`object`, `array`, `function`

```js
const foo = [1, 2];
const bar = foo;    // 引用复制，指向同一个地址
bar[0] = 9;
// foo=[9,2], bar=[9,2]  — 改了 bar，foo 也变了
```

### JS number 的坑

- JS 只有 `number`（IEEE 754 双精度浮点），没有 int/float 区分
- 超过 `2^53-1` 精度丢失，需要 `BigInt`
- Python 类比: Python 有 `int`（无限精度）和 `float`

### typeof 检查类型

```js
typeof 'hello'       // 'string'
typeof 42            // 'number'
typeof null          // 'object' — JS 历史 bug
typeof []            // 'object' — 数组也是 object
typeof function(){}  // 'function'

Array.isArray([1])   // true  — 检查数组的正确方式
```

Python 对比: `type(x)` 返回 `<class 'int'>` 等

### 类型转换

| 目标 | 推荐写法 | 避免写法 |
|------|---------|---------|
| 字符串 | `String(x)` | `x + ''`, `new String(x)` |
| 数字 | `Number(x)`, `parseInt(x, 10)` | `+x`, `x >> 0` |
| 布尔 | `!!x`, `Boolean(x)` | `new Boolean(x)` |

---

## 2. 变量声明

### 规则: 默认 `const`，需要重赋值用 `let`，永远不用 `var`

```js
const a = 1;      // 默认用 const
let count = 0;    // 需要改的用 let
// var — 永远不用
```

### const 锁引用不锁内容

```js
const arr = [1, 2];
arr[0] = 9;       // 可以，改的是内容不是引用
arr.push(3);      // 可以

arr = [4, 5];     // TypeError — 不能改引用
```

Python 类比: Python 没有 const，但行为类似引用复制（list/dict 赋值后改一个另一个也变）

### 作用域

| | `var` | `let`/`const` |
|--|-------|---------------|
| 作用域 | 函数级 | 块级 `{}` |
| 类比 Python | 和 Python 一致 | 比 Python 更严格 |

```js
{
  let a = 1;
  var b = 1;
}
console.log(a);  // ReferenceError
console.log(b);  // 1 — var 泄漏到外面
```

---

## 3. Hoisting（变量提升）

> Python 没有这个概念。

JS 引擎执行前会把 `var` 和 `function` 声明"提升"到作用域顶部。

| 声明方式 | 提升行为 | 声明前使用 |
|---------|---------|-----------|
| `var x = 5` | 声明提升，赋值不提升 | `undefined`（不报错，更危险） |
| `let x = 5` | 不提升（TDZ 暂时性死区） | `ReferenceError` |
| `const x = 5` | 不提升（TDZ） | `ReferenceError` |
| `function foo(){}` | 整体提升 | 可正常调用 |
| `var foo = function(){}` | 只提升变量名 | `TypeError` |

```js
console.log(x);    // undefined — var 声明被提升了
var x = 5;

console.log(y);    // ReferenceError — let/const 不提升
let y = 5;
```

---

## 4. 比较运算符

### 核心规则: 永远用 `===`，不用 `==`

```js
// == 隐式类型转换，结果离谱
0 == false         // true
'' == false        // true
'1' == 1           // true
null == undefined  // true

// === 严格比较
0 === false         // false
'' === false        // false
'1' === 1           // false
null === undefined  // false
```

Python 的 `==` 等价于 JS 的 `===`，不会做这种隐式转换。

### 真假值（falsy values）

| JS falsy | 说明 |
|----------|------|
| `0`, `-0`, `NaN` | 数字 |
| `''` | 空字符串 |
| `null`, `undefined` | 空值 |
| `false` | 布尔 |

**重要区别: JS 的空数组 `[]` 和空对象 `{}` 是 truthy！**

```js
if ([]) { }    // true  — JS
if ({}) { }    // true  — JS

bool([])       # False — Python
bool({})       # False — Python
```

---

## 5. 对象操作

### 创建对象: 用字面量 `{}`

```js
const item = {};            // good
const item = new Object();  // bad
```

### 计算属性名 `[expr]`

```js
const role = 'admin';
const user = { [`${role}_level`]: 5 };  // { admin_level: 5 }
```

Python 没有这个语法，只能 `d[key] = value` 分两步。

### 方法简写

```js
const obj = {
  double(n) { return n * 2; },       // good
  // double: function(n) { ... }     // bad
};
```

### 属性值简写

```js
const name = 'Tom';
const person = { name };   // 等价于 { name: name }
```

### 展开运算符 `...`

```js
// 合并（后者覆盖前者）
const merged = { ...defaults, ...userConfig };

// 排除属性
const { theme, ...rest } = config;   // rest = 剩余属性

// 浅拷贝
const copy = { ...original };
const arrCopy = [...items];
```

Python 类比: `{**defaults, **user_config}`, `[*items]`

### 检查属性是否存在

```js
// 安全方式
Object.hasOwn(obj, 'key');

// 不安全 — 对象可能自己定义了 hasOwnProperty 属性
obj.hasOwnProperty('key');
```

Python: `'key' in dict`

---

## 6. 数组操作

```js
const arr = [1, 2, 3];

arr.push(4);              // 末尾添加（Python: list.append()）
[...arr]                  // 浅拷贝
arr.map(x => x * 2)       // 映射（Python: [x*2 for x in arr]）
arr.filter(x => x > 1)    // 过滤（Python: [x for x in arr if x > 1]）
arr.reduce((acc, x) => acc + x, 0)  // 累加（Python: sum(arr)）
arr.find(x => x > 1)      // 找第一个（Python: next((x for x in arr if x > 1), None)）
arr.includes(2)            // 是否包含（Python: 2 in arr）
```

### 浅拷贝 vs 深拷贝

```js
const original = [[1, 2], [3, 4]];
const shallow = [...original];         // 浅拷贝，内层还是引用
const deep = structuredClone(original); // 深拷贝，完全独立

// Python: import copy; copy.deepcopy()
```

### 检查引用是否相同

```js
a === b   // true 表示同一个引用
```

---

## 7. 逻辑运算符

### `||` 逻辑或 — 返回第一个真值

```js
"hello" || null      // "hello"
null || "default"    // "default" — 常用于默认值
0 || 10              // 10 — 0 是 falsy
```

Python: `x or y` 行为类似

### `&&` 逻辑与 — 返回第一个假值

```js
"hello" && null      // null
null && "hello"      // null
1 && 2               // 2
```

Python: `x and y` 行为类似

### `??` 空值合并 — 只有 null/undefined 才触发

```js
0 ?? 10              // 0  — 保留 0
'' ?? 'default'      // '' — 保留空字符串
null ?? 'default'    // 'default'
undefined ?? 'default' // 'default'
```

Python 没有 `??` 等价物。`??` 比 `||` 更精确，不会误杀 0、''、false。

### `?.` 可选链 — 安全访问属性

```js
response.data?.user?.profile?.avatar           // 不会报错
response.data?.user?.profile?.avatar ?? 'default.png'  // 配合默认值
```

Python 没有等价语法，需要 try/except 或 `dict.get()` 链。

---

## 8. 控制流

### switch vs if-else

```js
// switch — 需要 break，否则穿透
switch (status) {
  case 200: { handle(); break; }
  case 404: { notFound(); break; }
  default:  { unknown(); }
}

// 对象映射 — 更安全的替代方案
const handlers = {
  200: () => handle(),
  404: () => notFound(),
};
handlers[status]?.() ?? defaultHandler();
```

Python: `if-elif-else`，3.10+ 有 `match-case`

### for...of（最常用遍历）

```js
for (const item of array) { }
```

Python: `for item in array:`

---

## 9. 语法糖对照表

| JS | Python | 用途 |
|----|--------|------|
| `` `${x}` `` | `f"{x}"` | 字符串插值 |
| `...arr` | `*arr` | 展开/剩余 |
| `{...a, ...b}` | `{**a, **b}` | 合并对象/字典 |
| `(x) => x * 2` | `lambda x: x * 2` | 简短函数 |
| `[a, ...rest]` | `a, *rest` | 解构 |
| `const { name } = obj` | 无直接等价 | 对象解构 |
| `?.` | 无 | 可选链（JS 独有） |
| `??` | 无 | 空值合并（JS 独有） |
| `!!x` | `bool(x)` | 转布尔 |

---

## 10. 命名规范对照

| 东西 | JS | Python |
|------|-----|--------|
| 变量/函数 | `camelCase` | `snake_case` |
| 类 | `PascalCase` | `PascalCase` |
| 常量 | `UPPER_SNAKE_CASE` | `UPPER_SNAKE_CASE` |
| 文件名 | `camelCase` 或 `kebab-case` | `snake_case` |

---

## 11. 风格规范速查

| 规则 | JS | Python |
|------|-----|--------|
| 缩进 | 2 空格 | 4 空格 |
| 分号 | 必须 | 不需要 |
| 引号 | 单引号 `'` | 单引号或双引号 |
| 行末逗号 | 多行时加 | 不加 |
| `if` 花括号 | 必须 `{}` | 用缩进 |

---

## 相关笔记

- [[ts-type-system]] - TypeScript 类型系统（待创建）
- [[ts-async]] - 异步编程 Promise/async-await（待创建）
- [[ts-project-structure]] - Node.js 项目结构（待创建）

---

**创建日期**: 2026-05-25
**最后更新**: 2026-05-25
