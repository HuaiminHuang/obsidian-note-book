---
title: Install FUSE
date: 2026-03-15
tags: [obsidian, quick-start]
status: completed
---

# 解决 FUSE 依赖

AppImage 运行时缺少 FUSE 库的错误处理。

## 错误现象

运行 AppImage 时提示：

```
dlopen(): error loading libfuse.so.2

AppImages require FUSE to run.
You might still be able to extract the contents of this AppImage
if you run it with the --appimage-extract option.
```

## 原因分析

较新的 Ubuntu (22.04 / 24.04) 默认安装 **fuse3**，但 AppImage 依赖 **libfuse2**，两者不兼容。

## 解决方案

### 安装 libfuse2

```bash
sudo apt update
sudo apt install libfuse2
```

### 验证安装

```bash
ls /lib/x86_64-linux-gnu/libfuse.so.2
```

如果文件存在，说明安装成功。

### 重新运行

```bash
~/Applications/obsidian/Obsidian-*.AppImage
```

---

> [!tip] 备选方案
> 如果不想安装 FUSE，可以使用 `--appimage-extract` 解压后运行，但不推荐。
