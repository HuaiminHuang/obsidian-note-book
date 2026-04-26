---
title: OpenCode 代理配置问题排查
date: 2026-04-19
tags: [ai, opencode, troubleshooting, proxy, wsl2, bashrc, profile]
status: completed
related: "[[../overview]]"
---

# OpenCode 代理配置问题排查

## 问题背景

在 WSL2 环境下使用 OpenCode 时，代理配置可能导致插件安装失败。本笔记记录代理配置对 OpenCode 的影响，以及 `.bashrc` 和 `.profile` 重复配置的风险。

## 根因

OpenCode 的后台插件安装器（不是 npm CLI）在处理某些代理环境时存在兼容问题：

- 当环境中存在 `ALL_PROXY=socks5://...` 时，可能触发：
  ```
  fetch() proxy.url must be a non-empty string
  ```
- 这不是"网络不通"或"代理坏了"，而是 **OpenCode 内部的代理解析/适配实现存在 bug**

## 代理环境变量

### 当前配置

**`~/.profile`（第 29-36 行）**：
```bash
# Proxy configuration for WSL to use Windows gateway
GATEWAY=$(ip route | awk '/default/ {print $3}')
export http_proxy="http://$GATEWAY:7890"
export https_proxy="$http_proxy"
export HTTP_PROXY="$http_proxy"
export HTTPS_PROXY="$http_proxy"
# export ALL_PROXY="socks5://$GATEWAY:7890"  # 已注释
export no_proxy="localhost,127.0.0.1"
```

**`~/.bashrc`（第 128-133 行）**：
```bash
# Proxy configuration for WSL to use Windows gateway
GATEWAY=$(ip route | awk '/default/ {print $3}')
export http_proxy="http://$GATEWAY:7890"
export https_proxy="http://$GATEWAY:7890"
export HTTP_PROXY="http://$GATEWAY:7890"
export HTTPS_PROXY="http://$GATEWAY:7890"
```

### 重复配置的风险

`~/.profile` 和 `~/.bashrc` **同时配置了代理**，存在以下风险：

1. **值不一致**：`.profile` 用 `$http_proxy` 引用，`.bashrc` 用 `$GATEWAY` 直接拼接。功能上等价但维护时容易漏改
2. **`no_proxy` 缺失**：`.bashrc` 没有设置 `no_proxy`，某些场景下只 source 了 `.bashrc` 时会丢失
3. **`ALL_PROXY` 幽灵**：注释掉 `.profile` 中的 `ALL_PROXY` 后，**已启动的 shell 仍会保留旧值**。需要新开终端才能生效

### Shell 加载顺序

```
Login Shell:  ~/.profile → source ~/.bashrc
Non-login Shell:  ~/.bashrc only
```

这意味着 `.profile` 中的代理设置会在 login shell 中被加载两次（一次自己、一次被 `.bashrc` 覆盖）。

## 修复措施

### 1. 注释掉 `ALL_PROXY`

`ALL_PROXY` 使用 socks5 协议，是触发 OpenCode 插件安装 bug 的最大嫌疑：

```bash
# ~/.profile 第 35 行
# export ALL_PROXY="socks5://$GATEWAY:7890"
```

### 2. 统一代理配置（建议）

将代理配置统一到**一个文件**中，推荐只保留 `~/.bashrc`：

```bash
# 在 ~/.bashrc 中保留代理配置
GATEWAY=$(ip route | awk '/default/ {print $3}')
export http_proxy="http://$GATEWAY:7890"
export https_proxy="$http_proxy"
export HTTP_PROXY="$http_proxy"
export HTTPS_PROXY="$http_proxy"
export no_proxy="localhost,127.0.0.1"
```

同时在 `~/.profile` 中删除重复的代理配置。

### 3. 修改后必须重启

- 修改 `~/.profile` 或 `~/.bashrc` 后，**当前 shell 不会自动更新环境变量**
- 已运行的 OpenCode 进程会继承旧环境
- 需要**新开终端**或 `source ~/.profile` 后重新启动 `opencode`

## 排查命令

```bash
# 检查当前环境中的代理变量
env | grep -i proxy

# 在干净环境下测试（排除旧 shell 残留）
env -i HOME="$HOME" USER="$USER" SHELL="/bin/bash" \
  PATH="$HOME/.nvm/versions/node/v24.14.0/bin:/usr/bin:/bin" \
  bash -lc 'env | grep -i proxy'

# 检查 OpenCode 插件加载日志
opencode debug agent sisyphus --print-logs --log-level DEBUG
```

## 关键理解

| 问题 | 不是 | 而是 |
|---|---|---|
| `proxy.url must be a non-empty string` | 代理不可用 | OpenCode 的代理解析实现有 bug |
| 注释 `ALL_PROXY` 后仍然失败 | `ALL_PROXY` 不是问题 | 需要新开终端/重启 OpenCode |
| 全局 npm 有包但 OpenCode 找不到 | OpenCode 不识别全局包 | OpenCode 只看自己的缓存目录 |

## 相关笔记

- [[../overview]] - OpenCode 概述与正常安装流程
- [[opencode-omo-install-failure]] - OMO 安装失败完整排查
