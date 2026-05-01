---
title: Ubuntu 使用指南
date: 2026-03-15
updated: 2026-05-01
tags: [ubuntu, linux]
status: completed
---

# Ubuntu 使用指南

## 目录内容

### Tailscale (`tailscale/`)

#### Concepts
- [[tailscale/concepts/tailscale-core-principles|核心原理]] - WireGuard P2P VPN 原理
- [[tailscale/concepts/tailscale-ssh-vs-traditional|Tailscale SSH vs 传统 SSH]] - 认证方式对比

#### Setup
- [[tailscale/setup/install-and-login|安装与登录]] - 安装、认证流程
- [[tailscale/setup/ssh-connection-setup|SSH 连接配置]] - 密码/密钥/VSCode 连接

#### Troubleshooting
- [[tailscale/troubleshooting/dns-resolv-conf-override|DNS 被 Tailscale 接管]] - resolv.conf 覆写
- [[tailscale/troubleshooting/tailscale-offline-reauth|离线重连]] - offline 状态修复
- [[tailscale/troubleshooting/cross-tailnet-connection|跨 Tailnet 连接问题]] - 账号不一致

### Troubleshooting (`troubleshooting/`)
- [[troubleshooting/wsl2-memory-compression-release]] - WSL2 Ubuntu内存压缩释放方案

## 相关资源

- [WSL2 官方文档](https://docs.microsoft.com/windows/wsl/)
- [Tailscale 官方文档](https://tailscale.com/docs/)

---

**创建日期**: 2026-03-15
**最后更新**: 2026-05-01
**版本**: 1.1
