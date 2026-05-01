---
title: Tailscale 安装与登录
tags: [ubuntu, tailscale, install, setup, wsl2]
status: completed
difficulty: easy
date: 2026-05-01
---

# Tailscale 安装与登录

## 安装

### WSL2 / Linux
```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

### macOS
```bash
brew install tailscale
```

### Windows
从 [https://tailscale.com/download](https://tailscale.com/download) 下载安装包。

## 登录流程

```mermaid
sequenceDiagram
    participant Terminal as 终端
    participant Tailscale as Tailscale 守护进程
    participant Browser as 浏览器
    participant Auth as 认证服务器

    Terminal->>Tailscale: sudo tailscale up
    Tailscale->>Terminal: 打印认证链接
    Note over Terminal: https://login.tailscale.com/a/xxxxx
    Terminal->>Browser: 打开链接
    Browser->>Auth: 选择 GitHub / Google 登录

    alt 浏览器已登录 GitHub
        Auth->>Browser: 自动授权（OAuth session）
        Browser->>Terminal: 认证成功通知
    else 未登录
        Browser->>Auth: 跳转 GitHub 登录页
        Auth->>Browser: 输入账号密码
        Browser->>Terminal: 认证成功通知
    end

    Tailscale->>Auth: 获取节点身份
    Auth->>Tailscale: 分配 100.x.x.x IP
    Tailscale-->>Terminal: 登录成功
```

## 自动登录 GitHub 的原因

```mermaid
graph LR
    A[执行 tailscale up] --> B[打开认证链接]
    B --> C{浏览器 GitHub session?}
    C -->|有 cookie| D[自动 OAuth 授权]
    C -->|无| E[手动输入 GitHub 账号]
    D --> F[加入 tailnet]
    E --> F
```

> 自动使用 GitHub 登录是因为**浏览器里有 GitHub 的登录 session（cookie）**，与 SSH 密钥无关。

## 登录后的验证

```bash
# 查看本机 IP
tailscale ip -4
# 示例输出: 100.124.24.56

# 查看网络状态
tailscale status
# 示例输出: 100.124.24.56  mk  HuaiminHuang@  linux  -
```

## 登录原则

- **所有设备必须使用同一个账号登录**，才会加入同一个 tailnet
- 不同账号的设备互相不可见（除非配置共享）
- `tailscale up --reset` 可强制重新登录

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 自动登录了错误的账号 | 浏览器里登录了多个 GitHub 账号 | `sudo tailscale logout` 后重新 `up`，手动选择账号 |
| 两台机器互相找不到 | 用了不同的 GitHub 账号登录 | 确保所有设备用**同一个账号** |
| WSL2 重启后 Tailscale 断连 | WSL2 网络栈重启 | 重新 `sudo tailscale up` |

## 相关笔记

- [[tailscale/setup/ssh-connection-setup|SSH 连接配置]]
- [[tailscale/troubleshooting/tailscale-offline-reauth|离线重连]]

---

**创建日期**: 2026-05-01
**最后更新**: 2026-05-01
**版本**: 1.0
