---
title: Install
date: 2026-03-15
tags: [obsidian, quick-start]
status: completed
---

# Obsidian 安装指南

在 Linux (Ubuntu) 上安装 Obsidian 的完整流程。

## 安装方式对比

| 方式 | 优点 | 缺点 |
|------|------|------|
| AppImage | 干净、可控、无权限限制 | 需要手动管理 |
| Snap | 自动更新 | 权限受限 |
| Flatpak | 沙盒隔离 | 配置复杂 |

> [!tip] 推荐
> AppImage 方式最适合配合 AI 插件和本地代码仓库使用。

## 安装步骤

1. [[install-appimage|下载并安装 AppImage]]
2. [[install-fuse|解决 FUSE 依赖]]（如遇到错误）
3. [[install-chinese|配置中文环境]]（可选）

## 运行

```bash
~/Applications/obsidian/Obsidian-*.AppImage
```

## GUI 界面

Linux 版本拥有与 Windows 完全一致的图形界面：

- 文件侧栏
- Markdown 实时预览
- 插件系统
- 主题定制
- 多窗口支持

---

> [!info] 为什么选择 AppImage
> - 不受 snap 权限限制
> - 可自由访问代码仓库目录
> - 插件加载更稳定
> - 适合作为 Vault 管理代码项目
