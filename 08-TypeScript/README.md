---
title: TypeScript 学习
tags: [typescript, learning, index]
status: learning
date: 2026-05-25
updated: 2026-05-25
---

# TypeScript 学习

> 从 Python 视角学习 JS/TS，目标：能够审查 ClawX TS 客户端项目的 AI 生成代码。

## 学习路径

JS 基础（与 Python 差异）→ TypeScript 类型系统 → 异步编程 → ClawX 项目审查

## Concepts (`concepts/`)

### JS 基础（与 Python 对比）
- [[js-fundamentals-from-python]] — JS/TS 基础：类型、作用域、Hoisting、类型转换、控制流、命名规范

### TypeScript 类型系统
- [[ts-type-system]] — 类型注解、联合类型、type 别名、interface
- [[ts-as-const]] — `as const` + `typeof` 模式（替代 enum）
- [[ts-utility-types]] — Record、Partial、Pick、Omit
- [[ts-generics]] — 泛型 `<T>`、`keyof`、泛型约束
- [[ts-type-guards]] — 类型守卫 `x is T`、`as` 断言

### 异步编程
- [[ts-async]] — Promise / async-await、与 Python 差异

### 常用语法
- [[ts-common-syntax]] — 箭头函数、`?.`、`??`、`||`、`&&`、解构、map/filter、try/catch、export/import

## ClawX 项目

- ClawX 路径：`/home/h2mzzz/typescript-learn/ClawX/`
- TSConfig：`strict: true`，target ES2022
- 主要模式：`as const` + `typeof`（替代 enum）、`Record` 字典、`Partial` 更新、泛型 API 客户端

## 参考资源

- Airbnb JS Style Guide: `/home/h2mzzz/typescript-learn/javascript/README.md`
- TypeScript 官方文档: https://www.typescriptlang.org/docs/

---

**创建日期**: 2026-05-25
**最后更新**: 2026-05-25
