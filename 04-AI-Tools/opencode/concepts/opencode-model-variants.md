---
title: OpenCode 模型变体机制（Model Variants）
date: 2026-04-24
tags: [ai/opencode, ai/model-variants, reasoning]
status: completed
difficulty: intermediate
---

# OpenCode 模型变体机制

## 概念

OpenCode 的 Model Variants（模型变体）机制允许同一模型以不同的推理配置运行。变体本质上是模型参数的预设组合，通过 `ctrl+t` 键快速切换。

## DeepSeek V4 Flash 变体

DeepSeek V4 Flash 内置 4 个变体，控制 **reasoning effort（推理努力度）**：

| 变体 | 参数值 | 推理深度 | 速度 | 适用场景 |
|------|--------|---------|------|---------|
| `low` | reasoningEffort: "low" | 浅推理 | 最快 | 简单问答、格式化 |
| `medium` | reasoningEffort: "medium" | 中等 | 适中 | 日常编码（默认） |
| `high` | reasoningEffort: "high" | 深推理 | 较慢 | 复杂逻辑、Bug 修复 |
| `max` | reasoningEffort: "max" | 最深 | 最慢 | 架构设计、代码审查 |

变体选择存储位置：`~/.local/state/opencode/model.json`

```json
{
  "variant": {
    "deepseek/deepseek-v4-flash": "max"
  }
}
```

## 切换方式

1. **TUI 快捷键** - 在对话界面按 `ctrl+t` 循环切换
2. **配置文件** - 在 `opencode.json` 中配置自定义变体
3. **状态文件** - 直接编辑 `~/.local/state/opencode/model.json`

## 自定义变体

可在 `opencode.json` 中覆盖或添加变体：

```json
{
  "provider": {
    "deepseek": {
      "models": {
        "deepseek-v4-flash": {
          "variants": {
            "max": { "reasoningEffort": "max" },
            "high": { "reasoningEffort": "high" }
          }
        }
      }
    }
  }
}
```

## 变体实现原理

变体由 `transform.ts` 中的 `variants()` 函数生成。对于 DeepSeek V4 模型：

```typescript
// @openrouter/ai-sdk-provider 和 @ai-sdk/openai-compatible
// 会为 deepseek-v4 添加 "max" 变体
case "@ai-sdk/openai-compatible":
  const efforts = ["low", "medium", "high"]
  if (model.api.id.includes("deepseek-v4")) {
    efforts.push("max")
  }
  return Object.fromEntries(efforts.map((e) => [e, { reasoningEffort: e }]))
```

## 其他模型的变体

| 提供商 | 变体示例 | 含义 |
|--------|---------|------|
| Anthropic (Claude) | high, max | thinking budget 控制 |
| OpenAI (GPT) | none, minimal, low, medium, high, xhigh | reasoning effort |
| Google (Gemini) | low, high | thinking budget |
| DeepSeek V4 | low, medium, high, max | reasoning effort |

## 输出 Token 限制

所有模型受全局输出限制保护：

```typescript
export const OUTPUT_TOKEN_MAX = 32_000  // 可环境变量覆盖
```

实际输出 = min(模型声明上限, 32,000)

---

**创建日期**: 2026-04-24
**最后更新**: 2026-04-24
