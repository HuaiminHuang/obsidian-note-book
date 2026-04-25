---
title: OpenCode 概述与 Oh My OpenAgent 配置
date: 2026-04-19
tags: [ai, opencode, omo, plugin, zai-coding-plan]
status: completed
aliases: [OpenCode, OMO, Oh My OpenAgent]
related: "[[opencode/troubleshooting/opencode-omo-install-failure]]"
---

# OpenCode 概述

OpenCode 是一个终端 AI 编码工具（TUI），支持通过插件扩展功能。

- 官方文档：https://opencode.ai/docs
- 配置文件：`~/.config/opencode/opencode.json`
- 插件缓存：`~/.cache/opencode/packages/`

## Oh My OpenAgent (OMO)

Oh My OpenAgent 是 OpenCode 的核心增强插件，提供：

- **多 Agent 编排**：Sisyphus（主编排）、Oracle（架构/调试）、Explore（快速搜索）、Librarian（文档检索）等
- **并行 Background Agent**：同时启动多个专家 agent
- **Hash-Anchored Edit Tool**：基于内容哈希的安全编辑
- **内置 MCP**：Exa（网页搜索）、Context7（官方文档）、Grep.app（GitHub 搜索）
- **Ralph Loop**：自引用循环直到任务完成

- 仓库：https://github.com/code-yeongyu/oh-my-openagent
- 包名：`oh-my-openagent`（插件入口）/ `oh-my-opencode`（CLI/发布名）
- 当前版本：`3.17.4`

## 正常安装流程

### 1. 确认 OpenCode 版本

```bash
opencode --version  # 需要 >= 1.0.150
```

### 2. 运行 OMO 安装器

根据你的订阅选择对应参数：

```bash
bunx oh-my-opencode install --no-tui \
  --claude=<yes|no|max20> \
  --openai=<yes|no> \
  --gemini=<yes|no> \
  --copilot=<yes|no> \
  --opencode-zen=<yes|no> \
  --zai-coding-plan=<yes|no> \
  --opencode-go=<yes|no> \
  --kimi-for-coding=<yes|no> \
  --vercel-ai-gateway=<yes|no>
```

安装器会：
1. 在 `opencode.json` 的 `plugin` 数组中注册 `"oh-my-openagent@latest"`
2. 生成 `~/.config/opencode/oh-my-openagent.json` 配置文件
3. 根据订阅配置各 agent 的模型分配

### 3. 验证

```bash
bunx oh-my-opencode doctor
opencode agent list
opencode debug agent sisyphus
```

### 4. 重启 OpenCode

修改代理环境变量或插件配置后，**必须重启 OpenCode** 才能生效。

## 核心配置文件

### `opencode.json`

主配置文件，关键部分：

```json
{
  "model": "zai-coding-plan/glm-5.1",
  "small_model": "zai-coding-plan/glm-5",
  "provider": { ... },
  "mcp": { ... },
  "plugin": ["oh-my-openagent@latest"]
}
```

### `oh-my-openagent.json`

OMO 插件配置，定义各 agent 和 category 的模型分配：

```json
{
  "agents": {
    "sisyphus": { "model": "zai-coding-plan/glm-5" },
    "oracle": { "model": "zai-coding-plan/glm-5.1" },
    "explore": { "model": "minimax/MiniMax-M2.7" }
  },
  "categories": {
    "visual-engineering": { "model": "zai-coding-plan/glm-5" },
    "quick": { "model": "minimax/MiniMax-M2.7" }
  }
}
```

## 模型分配原则

| 任务类型 | 推荐模型 | 来源 |
|---|---|---|
| 高智能（Oracle、Prometheus、Momus） | `zai-coding-plan/glm-5.1` | Z.ai Coding Plan |
| 均衡任务（Sisyphus、Metis、Deep） | `zai-coding-plan/glm-5` | Z.ai Coding Plan |
| 速度优先（Explore、Atlas、Quick） | `minimax/MiniMax-M2.7` | MiniMax (Z.ai) |
| 视觉任务（Multimodal-Looker） | `zai-coding-plan/glm-4.6v` | Z.ai Coding Plan |
| 文档检索（Librarian） | `zai-coding-plan/glm-4.7` | Z.ai Coding Plan |

## 插件安装机制

OpenCode 的插件安装是**独立的两步过程**：

1. **下载/缓存**：OpenCode 根据插件声明自行下载到缓存目录
   - 缓存路径：`~/.cache/opencode/packages/oh-my-openagent@latest/`
   - 这一步**不依赖**系统 npm 全局安装
2. **运行时加载**：从缓存目录解析入口并加载插件，注册 agent

## 相关笔记

- [[opencode/troubleshooting/opencode-omo-install-failure]] - OMO 安装失败完整排查
- [[opencode/troubleshooting/opencode-proxy-config]] - 代理配置问题排查
- [[llama.cpp/concepts/opencode-model-variants]] - OpenCode 模型变体机制（DeepSeek V4 reasoning effort）
