---
title: CLI Commands
date: 2026-03-15
tags: [opencode, cli]
status: completed
---

# OpenCode CLI 命令速查

> [!TIP]
> 快速查找常用命令和选项

#opencode #cli #命令行 #速查

---

## 主命令选项

| 选项 | 说明 |
|------|------|
| `-h, --help` | 显示帮助 |
| `-v, --version` | 显示版本 |
| `-c, --continue` | 继续上一次会话 |
| `-s, --session` | 继续指定会话 ID |
| `-m, --model` | 指定模型 (provider/model 格式) |

---

## opencode run 专用选项

### 基础选项

| 选项 | 说明 |
|------|------|
| `-f, --file` | 附加文件到消息 |
| `-c, --continue` | 继续上次会话 |
| `-s, --session` | 继续指定会话 ID |
| `-m, --model` | 指定模型 |
| `--agent` | 指定 agent |

### 输出控制

| 选项 | 说明 |
|------|------|
| `--format` | 输出格式: default 或 json |
| `--thinking` | 显示思考过程 |

### 会话管理

| 选项 | 说明 |
|------|------|
| `--share` | 分享会话 |
| `--title` | 会话标题 |
| `--fork` | 分支会话 |

### 服务器相关

| 选项 | 说明 |
|------|------|
| `--attach` | 附加到运行中的服务器 |
| `--dir` | 工作目录 |
| `--port` | 本地服务器端口 |

### 高级选项

| 选项 | 说明 |
|------|------|
| `--command` | 运行命令 |
| `--variant` | 模型变体 (如 high, max, minimal) |

---

## 常用示例

### 基础用法

```bash
# 直接提问
opencode run "帮我写一个函数"

# 指定模型
opencode run -m zai-coding-plan/glm-5 "优化代码"

# 附加文件
opencode run -f ./agents/plan.md "分析这个文件"

# 继续会话
opencode run -c "继续之前的任务"

# 指定会话 ID
opencode run -s ses_xxx "继续讨论"

# 组合使用
opencode run -f ./file.js -m gpt-4 "审查代码"
```

### 高级用法

```bash
# 指定工作目录
opencode run --dir ./src "重构这个目录"

# 使用思考模式
opencode run --thinking "详细分析这段代码"

# 创建分支会话
opencode run --fork "探索不同的实现方案"

# 共享会话
opencode run --share --title "代码审查" "帮我审查"

# JSON 格式输出
opencode run --format json "列出所有文件"

# 指定 agent
opencode run --agent code-reviewer "审查这段代码"

# 指定模型变体
opencode run --variant max "深度分析这个架构"
```

---

## 快捷命令别名

> [!TIP]
> 可以在 `.bashrc` 或 `.zshrc` 中添加别名简化输入

```bash
# 常用别名示例
alias oc='opencode'
alias ocr='opencode run'
alias occ='opencode run -c'
alias ocf='opencode run -f'
```

---

## 相关链接

- [[自动补全配置]]
- [[OpenCode 文档索引]]
- [[命令行最佳实践]]
