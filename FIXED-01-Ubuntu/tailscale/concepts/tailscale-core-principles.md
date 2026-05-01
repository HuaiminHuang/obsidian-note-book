---
title: Tailscale 核心原理
tags: [ubuntu, tailscale, network, vpn]
status: completed
difficulty: intermediate
time_spent: 1h
date: 2026-05-01
---

# Tailscale 核心原理

## 概念

Tailscale 是一个基于 **WireGuard** 的 **P2P VPN** 服务，它将多台设备组织成一个加密的虚拟局域网。

```mermaid
graph TB
    subgraph Internet[公网]
        COORD[协调服务器]
        DERP[DERP 中继服务器]
    end

    subgraph DeviceA[设备 A 100.124.24.56]
        WG_A[WireGuard 接口]
    end

    subgraph DeviceB[设备 B 100.66.254.74]
        WG_B[WireGuard 接口]
    end

    DeviceA -->|1. 登录认证| COORD
    DeviceB -->|2. 登录认证| COORD
    COORD -->|3. 交换节点信息| DeviceA
    COORD -->|4. 交换节点信息| DeviceB
    DeviceA -->|5. 尝试 P2P 直连| DeviceB
    DeviceA -->|6. P2P 失败则走 DERP 中继| DERP
    DERP -->|7. 转发流量| DeviceB
```

## 核心机制

### 1. WireGuard 加密

- 现代、高效的内核级 VPN 协议
- 每对设备之间建立独立的加密隧道
- 端到端加密，中间节点无法解密

### 2. NAT 穿透

- 自动检测 NAT 类型
- 使用 UDP 打洞技术建立直连
- 如果直连失败，自动回退到 DERP 中继

### 3. MagicDNS

```mermaid
sequenceDiagram
    participant App as 应用程序
    participant ResolvConf as /etc/resolv.conf
    participant TS_DNS as Tailscale DNS (100.100.100.100)
    participant Upstream as 上游 DNS

    Note over ResolvConf: Tailscale 安装后写入 nameserver 100.100.100.100

    App->>ResolvConf: 域名查询
    ResolvConf->>TS_DNS: 转发请求

    alt Tailscale 在线
        TS_DNS->>Upstream: 查询外部域名
        Upstream-->>TS_DNS: 返回结果
        TS_DNS-->>App: 正常解析
    else Tailscale 离线
        TS_DNS-->>ResolvConf: 无响应 / recursion not available
        Note over ResolvConf: 可能 fallback 到其他 DNS
    end
```

### 4. 设备间通信流程

```mermaid
flowchart TD
    A[设备 A] -->|1. 查询对端 IP| COORD[协调服务器]
    COORD -->|2. 返回对端地址信息| A
    A -->|3. 尝试 UDP 打洞| B[设备 B]
    B -->|4. 确认连接| A

    A -.->|5. 打洞失败| DERP[DERP 中继]
    DERP -.->|6. 中继转发| B
```

## 对比传统 VPN

| 特性 | 传统 VPN | Tailscale |
|------|---------|-----------|
| 配置复杂度 | 高（证书、路由表等） | 低（一条命令） |
| 需要公网 IP | 通常需要 | 不需要 |
| 连接方式 | 客户端-服务器 | P2P 直连 |
| 中继 | 不常用 | DERP 自动中继 |
| 加密 | 多种协议 | WireGuard |
| 访问控制 | 手动配置 | ACL 集中管理 |

## 适用场景

- **远程 SSH**：从外网访问家中/公司机器
- **私有服务暴露**：通过 Tailscale Serve/Funnel 暴露本地服务
- **跨设备文件传输**：scp/syncthing over Tailscale
- **远程开发**：VSCode Remote SSH over Tailscale

## 相关笔记

- [[tailscale/concepts/tailscale-ssh-vs-traditional|Tailscale SSH vs 传统 SSH]]
- [[tailscale/troubleshooting/dns-resolv-conf-override|DNS 被 Tailscale 接管]]

---

**创建日期**: 2026-05-01
**最后更新**: 2026-05-01
**版本**: 1.0
