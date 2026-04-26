---
title: OpenClaw Exec 安全策略与白名单机制
date: 2026-04-26
tags: [ai/openclaw, ai/security, ai/exec-policy]
status: learning
difficulty: intermediate
time_spent: 2h
created: 2026-04-26
updated: 2026-04-26
---

# OpenClaw Exec 安全策略与白名单机制

## 概念

OpenClaw 的 exec 工具是 AI Agent 执行 Shell 命令的核心能力。为了防止未授权命令执行，OpenClaw 采用**双层策略架构**控制 exec 权限。

### 双层策略

| 层级 | 文件 | 作用 |
|------|------|------|
| Agent 侧（请求方） | `~/.openclaw/openclaw.json` 的 `tools.exec` | 控制 Agent 能**请求**什么 |
| Host 侧（执行方） | `~/.openclaw/exec-approvals.json` | 最终**把关**，作为上限 |

**最终策略 = 两层的交集**（取更严格的那个）。

### 三个安全维度

1. **`security`** — 安全模式
   - `deny`：禁止所有执行
   - `allowlist`：只允许白名单内的命令
   - `full`：允许所有命令

2. **`ask`** — 审批模式
   - `off`：从不询问
   - `on-miss`：白名单未命中时询问用户
   - `always`：每次都询问

3. **`elevated`** — 沙箱逃逸通道（从沙箱环境请求在真实主机执行）

### 白名单匹配机制

白名单使用**大小写不敏感的 glob 匹配**，匹配的是**解析后的可执行文件路径**：

```
~/Projects/**/bin/rg     # 项目目录下任意位置
~/.local/bin/*           # 用户本地 bin 目录
/opt/homebrew/bin/rg     # 精确路径
```

### Safe Bins（内置安全工具）

OpenClaw 内置了一批 safeBins，**无需显式白名单**即可运行：

> `jq`, `cut`, `uniq`, `head`, `tail`, `tr`, `wc`

这些工具被认为安全是因为它们只从 stdin 读取、拒绝文件路径参数、不支持重定向和管道。

### 预设策略

```bash
# 三种预设
openclaw exec-policy preset cautious   # 安全：allowlist + on-miss + deny fallback
openclaw exec-policy preset yolo       # 放开：full + off
openclaw exec-policy preset deny-all   # 锁死：deny
```

## 踩坑记录

### 坑 1：白名单加了命令但还是弹审批

**现象**：已将 `/usr/bin/ls`、`/usr/bin/grep` 等加入白名单，但呆猫执行 `ls -la ...` 或 `head -30 file.txt` 时仍然弹审批。

**根因**：呆猫的命令是通过 shell（`bash -c "..."`）执行的，OpenClaw 解析出的实际可执行路径是 `/usr/bin/bash`，而非白名单里的 `/usr/bin/ls`。所以单独加 `ls`、`grep` 等路径无效——shell exec 场景下，匹配的是 shell 本身。

**解决**：将 `/usr/bin/bash` 和 `/bin/bash` 加入白名单。

### 坑 2：加了 bash 白名单等于没有限制？

**分析**：是的。一旦 bash 进入白名单，任何命令都可以通过 `bash -c "任意命令"` 执行，单独限制 `ls`、`grep` 等变得毫无意义。

**结论**：这是 OpenClaw exec 白名单机制在 shell exec 场景下的设计局限——白名单粒度是**二进制路径级别**，无法按命令参数过滤。

**应对方案**：
- 方案 A：只加 bash + `ask=on-miss` 兜底（当前选择）
- 方案 B：用 Docker 沙箱做真正隔离
- 方案 C：低权限系统账户运行 OpenClaw

### 坑 3：workspace 不等于沙箱

**现象**：配置了 `agents.defaults.workspace`，以为文件访问被限制在 workspace 内。

**事实**：`workspace` 只指定 Agent 的默认工作目录，**不限制文件访问范围**。Agent 可以通过 exec 访问整个文件系统。

### 坑 4：cautious 预设后白名单外的命令处理

**现象**：应用 `cautious` 预设后，白名单外的命令不是直接拒绝，而是弹出审批提示。

**解释**：`cautious` 的 `ask=on-miss` 意味着白名单未命中时**询问用户**，而非直接拒绝。`askFallback=deny` 只在审批超时/失败时才拒绝。这是设计意图，不是 bug。

## 最终配置方案

当前采用**方案 A：放宽 + 审批兜底**。

### 白名单（2 条）

```bash
# 只保留 bash，覆盖所有 shell exec 场景
openclaw approvals allowlist add "/usr/bin/bash"
openclaw approvals allowlist add "/bin/bash"
```

### 生效逻辑

```
命令请求 → 解析为 bash 调用 → 匹配白名单 → 自动放行
命令请求 → 非 bash 调用 → 白名单未命中 → 弹审批(on-miss) → 超时则拒绝(deny)
```

### 查看当前策略

```bash
# 查看生效策略
openclaw exec-policy show

# 查看白名单
openclaw approvals get

# 手动审批（在聊天中）
/approve <id> allow-once
/approve <id> allow-always
/approve <id> deny
```

## 安全建议

### 已知漏洞

- **CVE-2026-32017**：safeBins 的短选项绕过漏洞（如 `sort -o/tmp/poc`），可绕过 safeBins 检查实现任意文件写入。已在新版本修复。
- **CVE-2026-32059**：safeBins 长选项缩写绕过。

### 加固建议

1. **保持版本最新**：定期 `openclaw update`
2. **Docker 沙箱**：生产环境启用 `agents.defaults.sandbox.mode: "all"`
3. **低权限账户**：用专用低权限账户运行 OpenClaw，不使用主账户
4. **网络隔离**：`gateway.bind: "loopback"` 只允许本地访问
5. **工具最小化**：`tools.profile: "coding"` 或 `"messaging"`，不轻易用 `"full"`
6. **deny 优先**：`tools.deny` 始终优先于 `allow`，高危工具直接 deny

### 相关命令速查

```bash
# 查看策略
openclaw exec-policy show

# 应用预设
openclaw exec-policy preset cautious

# 白名单管理
openclaw approvals allowlist add "/usr/bin/bash"
openclaw approvals allowlist remove "/usr/bin/ls"
openclaw approvals get

# 安全审计
openclaw doctor
openclaw security audit --deep

# 配置验证
openclaw config validate
```

## 相关笔记

- [[../troubleshooting/openclaw-config-clobber]] - 配置文件被覆盖问题排查
- [[memory-system-overview]] - 记忆系统总览与配置详解

---

**创建日期**: 2026-04-26
**最后更新**: 2026-04-26
