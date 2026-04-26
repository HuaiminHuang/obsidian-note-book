---
title: VSCode 终端快捷键与设置
tags: [ide/vscode, ide/settings, ide/terminal]
status: completed
difficulty: easy
time_spent: 30min
created: 2026-04-26
updated: 2026-04-26
---

# VSCode 终端快捷键与设置

## 背景

PowerShell PSReadLine 模块提供了方便的终端导航快捷键（如 `Ctrl+Alt+U` 翻上半页），但在 VSCode 内置终端中无效。

**原因**：VSCode 和已安装的扩展会优先拦截键盘事件，快捷键在到达终端进程前已被消费。

### 被拦截的快捷键

| 操作 | 快捷键 | VSCode 默认占用 |
|------|--------|----------------|
| 上半页 | `Ctrl+Alt+U` | 可能被扩展拦截 |
| 下半页 | `Ctrl+Alt+D` | 可能被扩展拦截 |
| 上一行 | `Ctrl+Alt+Y` | 可能被扩展拦截 |
| 下一行 | `Ctrl+Alt+E` | 可能被扩展拦截 |
| 翻上页 | `Ctrl+Alt+B` | 可能被扩展拦截 |
| 翻下页 | `Ctrl+Alt+F` | 可能被扩展拦截 |
| 回到最顶 | `Ctrl+G` | Go to Line（默认） |
| 跳到最后 | `Ctrl+Alt+G` | 可能被扩展拦截 |

## 解决方案

通过 `keybindings.json` 中的 `workbench.action.terminal.sendSequence` 命令，配合 `when: terminalFocus` 条件，在终端聚焦时将快捷键对应的控制序列直接发送给终端进程。

```jsonc
// .config/Code/User/keybindings.json 或 VSCode 设置 → 键盘快捷键 → 右上角 {} 按钮

// PSReadLine 导航快捷键 —— 仅在终端聚焦时生效
{
    "key": "ctrl+g",
    "command": "workbench.action.terminal.sendSequence",
    "when": "terminalFocus",
    "args": { "text": "\u0007" }
},
{
    "key": "ctrl+alt+u",
    "command": "workbench.action.terminal.sendSequence",
    "when": "terminalFocus",
    "args": { "text": "\u001b\u0015" }
},
{
    "key": "ctrl+alt+d",
    "command": "workbench.action.terminal.sendSequence",
    "when": "terminalFocus",
    "args": { "text": "\u001b\u0004" }
},
{
    "key": "ctrl+alt+y",
    "command": "workbench.action.terminal.sendSequence",
    "when": "terminalFocus",
    "args": { "text": "\u001b\u0019" }
},
{
    "key": "ctrl+alt+e",
    "command": "workbench.action.terminal.sendSequence",
    "when": "terminalFocus",
    "args": { "text": "\u001b\u0005" }
},
{
    "key": "ctrl+alt+b",
    "command": "workbench.action.terminal.sendSequence",
    "when": "terminalFocus",
    "args": { "text": "\u001b\u0002" }
},
{
    "key": "ctrl+alt+f",
    "command": "workbench.action.terminal.sendSequence",
    "when": "terminalFocus",
    "args": { "text": "\u001b\u0006" }
},
{
    "key": "ctrl+alt+g",
    "command": "workbench.action.terminal.sendSequence",
    "when": "terminalFocus",
    "args": { "text": "\u001b\u0007" }
}
```

### 原理说明

- `when: terminalFocus` — 只在终端获得焦点时生效，编辑器/其他面板中保持原有行为
- `sendSequence` — 将转义序列直接写入终端，PSReadLine 识别后执行对应操作

## settings.json 终端相关配置

```jsonc
// .config/Code/User/settings.json

// === 终端外观 ===
"terminal.integrated.fontSize": 16,
"terminal.integrated.fontWeight": "normal",
"terminal.integrated.fontWeightBold": "bold",
"terminal.integrated.initialHint": false,     // 关闭"Select a profile..." 提示

// === 终端滚动 ===
"terminal.integrated.mouseWheelScrollSensitivity": 2,  // 滚轮灵敏度
"terminal.integrated.fastScrollSensitivity": 5,          // 快速滚动灵敏度
"terminal.integrated.scrollback": 5000,                  // 回滚缓冲区行数
"terminal.integrated.mouseWheelZoom": true,              // 滚轮缩放

// === 代理环境变量推送到终端 ===
"terminal.integrated.env.windows": {
    "HTTP_PROXY": "http://127.0.0.1:7890",
    "HTTPS_PROXY": "http://127.0.0.1:7890"
},

// === 默认终端 ===
"terminal.external.windowsExec": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
```

### 代理推送说明

在 `settings.json` 中配置 `terminal.integrated.env.windows` 可以将代理环境变量自动注入到所有新建终端会话中，避免每次手动 `$env:HTTP_PROXY=...`。

## 括号引导线配置

```jsonc
// settings.json

// 启用彩色括号
"editor.bracketPairColorization.enabled": true,

// 括号对引导线
"editor.guides.bracketPairs": "active",          // "active"（当前高亮）/ true（始终显示）/ false
"editor.guides.bracketPairsHorizontal": "active",

// 缩进引导线
"editor.guides.indentation": true,
"editor.guides.highlightActiveIndentation": true,

// 自定义括号颜色（可选）
"workbench.colorCustomizations": {
    "editorBracketHighlight.foreground1": "#FFD700",
    "editorBracketHighlight.foreground2": "#DA70D6",
    "editorBracketHighlight.foreground3": "#179fff",
    "editorBracketHighlight.foreground4": "#ff0000",
    "editorBracketHighlight.foreground5": "#00ff00",
    "editorBracketHighlight.foreground6": "#ff8c00",

    "editorBracketPairGuide.background1": "#FFD70050",
    "editorBracketPairGuide.background2": "#DA70D650",
    "editorBracketPairGuide.background3": "#179fff50",

    "editorBracketPairGuide.activeBackground1": "#FFD700",
    "editorBracketPairGuide.activeBackground2": "#DA70D6",
    "editorBracketPairGuide.activeBackground3": "#179fff"
}
```

## 相关笔记

- [[../Windsurf/windsurf-codeium-download-issue]] - Windsurf 插件下载问题

---

**创建日期**: 2026-04-26
**最后更新**: 2026-04-26
