---
title: OpenCode OMO 插件安装失败排查
date: 2026-04-19
tags: [ai, opencode, omo, troubleshooting, proxy, npm]
status: completed
difficulty: advanced
related: "[[../overview]]"
---

# OpenCode OMO 插件安装失败排查

## 问题现象

- `opencode` 启动后 Tab 键只能看到原生 `build` 和 `plan`
- `opencode debug agent sisyphus` 返回 `Agent sisyphus not found`
- 日志中出现：
  ```
  FetchError: request to https://registry.npmjs.org/@opencode-ai%2fplugin failed,
  reason: fetch() proxy.url must be a non-empty string
  ```
  以及：
  ```
  ENOENT: no such file or directory, open
  '/home/h2mzzz/.cache/opencode/packages/oh-my-openagent@latest/node_modules/package.json'
  ```

## 根因分析（三层）

### 第一层：OpenCode 插件缓存安装失败

OpenCode 看到 `plugin: ["oh-my-openagent@latest"]` 后，尝试自行下载插件到缓存目录：

```
~/.cache/opencode/packages/oh-my-openagent@latest/
```

但在下载依赖 `@opencode-ai/plugin` 时失败：
- 错误：`fetch() proxy.url must be a non-empty string`
- 原因：OpenCode 的后台安装器对当前代理环境处理异常

**关键理解**：这**不是** npm CLI 的问题。`npm view oh-my-openagent version` 能正常工作。问题出在 OpenCode 自己的 fetch/代理适配层。

### 第二层：代理环境触发 bug

当前环境中的代理变量：
- `HTTP_PROXY=http://172.31.48.1:7890`
- `HTTPS_PROXY=http://172.31.48.1:7890`
- `http_proxy=http://172.31.48.1:7890`
- `https_proxy=http://172.31.48.1:7890`
- `ALL_PROXY=socks5://172.31.48.1:7890`（后来注释掉）

注释掉 `ALL_PROXY` 后，`proxy.url` 错误消失，但插件安装仍可能需要完全干净的环境才能成功。

### 第三层：Agent 注册需要完整重启

即使插件包成功下载到缓存，agent 注册（`sisyphus`、`prometheus` 等）需要在**完整重启 OpenCode 后**才能生效。在旧 shell 中反复运行 `opencode debug` 不会触发重新注册。

## 完整排查步骤

### Step 1：检查配置文件

```bash
# 确认插件声明存在
cat ~/.config/opencode/opencode.json | grep plugin
# 应该看到: "plugin": ["oh-my-openagent@latest"]

# 确认 OMO 配置文件存在
ls ~/.config/opencode/oh-my-openagent.json
```

### Step 2：检查插件缓存

```bash
ls ~/.cache/opencode/packages/oh-my-openagent@latest/
# 如果只有空目录或不存在 → 安装失败
# 如果有 package.json + node_modules/ → 安装成功
```

### Step 3：查看插件加载日志

```bash
opencode debug agent sisyphus --print-logs --log-level DEBUG
```

关注：
- `loading plugin` → 插件开始加载
- `proxy.url must be a non-empty string` → 代理问题
- `ENOENT ... node_modules/package.json` → 缓存安装失败
- `failed to resolve plugin server entry` → 入口解析失败

### Step 4：检查代理环境

```bash
env | grep -i proxy
```

如果存在 `ALL_PROXY=socks5://...`，这是最可能的触发条件。

### Step 5：验证修复

修改代理配置后，用**全新环境**验证：

```bash
env -i HOME="$HOME" USER="$USER" SHELL="/bin/bash" \
  PATH="$HOME/.nvm/versions/node/v24.14.0/bin:/usr/bin:/bin" \
  bash -lc 'opencode debug agent sisyphus --print-logs --log-level DEBUG'
```

## 解决方案

### 方案 A：修复代理环境（推荐）

1. 编辑 `~/.profile`，注释掉 `ALL_PROXY`：
   ```bash
   # export ALL_PROXY="socks5://$GATEWAY:7890"
   ```

2. 清除 OMO 插件缓存：
   ```bash
   rm -rf ~/.cache/opencode/packages/oh-my-openagent@latest
   ```

3. 新开终端，启动 `opencode`，等待自动重新下载

4. 验证：
   ```bash
   opencode agent list
   opencode debug agent sisyphus
   ```

### 方案 B：`file://` 本地加载（workaround）

如果代理环境无法修复，可以绕过 OpenCode 的下载器：

1. 全局安装：
   ```bash
   npm install -g oh-my-openagent@latest
   ```

2. 修改 `opencode.json`：
   ```json
   {
     "plugin": [
       "file:///home/h2mzzz/.nvm/versions/node/v24.14.0/lib/node_modules/oh-my-openagent/dist/index.js"
     ]
   }
   ```

**注意**：切换 nvm Node 版本后路径可能失效。

### 方案 C：固定目录安装

比方案 B 更稳定，不受 nvm 切版本影响：

```bash
cd ~/.config/opencode
npm install oh-my-openagent@latest
```

```json
{
  "plugin": [
    "file:///home/h2mzzz/.config/opencode/node_modules/oh-my-openagent/dist/index.js"
  ]
}
```

更新时：
```bash
cd ~/.config/opencode && npm install oh-my-openagent@latest
```

## 关键概念区分

| 概念 | 路径 | 说明 |
|---|---|---|
| 系统全局 npm 包 | `~/.nvm/.../lib/node_modules/oh-my-openagent` | `npm install -g` 安装的位置 |
| OpenCode 插件缓存 | `~/.cache/opencode/packages/oh-my-openagent@latest/` | OpenCode 自己管理的位置 |
| 配置目录本地依赖 | `~/.config/opencode/node_modules/@opencode-ai/plugin` | OpenCode 配置目录自己的依赖 |
| OMO 配置文件 | `~/.config/opencode/oh-my-openagent.json` | Agent 模型配置 |

**核心理解**：OpenCode 默认**不会**使用系统全局安装的 npm 包作为插件。它只看自己的缓存目录。`plugin: ["oh-my-openagent@latest"]` 是包名声明，OpenCode 会自己去下载，不会 fallback 到全局 npm。

## 环境信息

- **OpenCode 版本**：1.14.17
- **OMO 版本**：3.17.4
- **Node**：v24.14.0（nvm 管理）
- **OS**：Linux x64（WSL2）
- **订阅**：Z.ai Coding Plan

## 相关笔记

- [[../overview]] - OpenCode 概述与正常安装流程
- [[opencode-proxy-config]] - 代理配置问题排查
