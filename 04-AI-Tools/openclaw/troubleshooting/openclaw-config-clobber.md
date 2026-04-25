---
title: OpenClaw 配置文件被覆盖问题
date: 2026-04-26
tags: [ai/openclaw, troubleshooting, ai/config]
status: completed
priority: high
environment: OpenClaw 2026.4.23, Ubuntu, systemd
---

# OpenClaw 配置文件被覆盖问题

## 问题描述

编辑 `~/.openclaw/openclaw.json` 后，OpenClaw gateway 启动或重启时会覆盖配置文件，导致自定义配置丢失。

## 现象

- 出现多个 `.clobbered` 文件，例如 `openclaw.json.clobbered.2026-04-25T11-24-21-136Z`
- 自定义字段（如 `memorySearch`）被删除或重置为默认值
- 配置备份文件出现：`.bak`、`.bak.1`-`.bak.4`、`.last-good`

## 根本原因

OpenClaw gateway 启动时会将运行时配置写回 `openclaw.json`，覆盖整个文件。运行时配置可能不包含用户自定义的字段，导致这些字段被删除。

## 解决方案

### 步骤 1：停止 gateway

```bash
openclaw gateway stop
```

### 步骤 2：编辑配置文件

```bash
# 备份当前配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.manual

# 编辑配置
vim ~/.openclaw/openclaw.json
```

### 步骤 3：验证 JSON 格式

```bash
python3 -c "import json; json.load(open('$HOME/.openclaw/openclaw.json'))"
```

### 步骤 4：验证配置有效性

```bash
openclaw config validate
```

### 步骤 5：启动 gateway

```bash
openclaw gateway start
```

## 验证步骤

```bash
openclaw config validate    # 验证配置
openclaw memory status      # 检查记忆系统
openclaw wiki status        # 检查 wiki
```

## 预防措施

- **始终在 gateway 停止时编辑配置**，避免写入冲突
- **编辑前手动备份**：`cp openclaw.json openclaw.json.bak.manual`
- **编辑后验证**：先验证 JSON 格式，再运行 `openclaw config validate`

## 相关笔记

- [[concepts/memory-system-overview]]
