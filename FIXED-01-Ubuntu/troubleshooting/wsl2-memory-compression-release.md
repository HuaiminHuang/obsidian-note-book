---
title: WSL2 Ubuntu内存压缩释放
date: 2026-03-15
tags: [ubuntu, wsl, memory, optimization]
status: active
---

# WSL2 Ubuntu内存压缩释放

## 概述

WSL2虚拟磁盘默认是稀疏文件（Sparse File），只存储实际写入的数据。但压缩释放虚拟磁盘空间可以释放未使用的磁盘空间。

## 问题原因

`Optimize-VHD` 命令会报错"无法将项识别为 cmdlet"，通常是因为：
- 缺少Hyper-V模块
- 虚拟磁盘文件是稀疏文件，与命令要求不兼容

## 方案一：使用 DiskPart 进行压缩

### 步骤

**1. 关闭所有WSL实例**

```powershell
wsl --shutdown
```

**2. 启动 DiskPart 工具**

```powershell
diskpart
```

**3. 执行压缩命令**

在DiskPart环境中执行（注意替换路径）：

```diskpart
# 选择你的WSL虚拟磁盘文件
select vdisk file="C:\Users\hhm18\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu22.04LTS_79rhkp1fndgsc\LocalState\ext4.vhdx"

# 以只读模式附加虚拟磁盘
attach vdisk readonly

# 开始压缩虚拟磁盘
compact vdisk

# 压缩完成后，分离虚拟磁盘
detach vdisk

# 退出 DiskPart
exit
```

**4. 注意事项**

- 如果 `attach vdisk readonly` 第一次报错，直接再执行一次即可
- 压缩过程可能需要几分钟，请耐心等待

## 方案二：使用 WSL 导出/导入（参考）

### 优势

- 能100%成功压缩虚拟磁盘
- 可以把整个Linux系统迁移到其他盘

### 简要步骤

**1. 在WSL内部清零空闲空间**

```bash
# 创建一个用0填充的大文件
dd if=/dev/zero of=~/zero.file bs=1M
# 填充完成后，删除这个文件
rm -f ~/zero.file
```

**2. 导出并重新导入系统**

```powershell
# 在Windows（管理员PowerShell）中执行
wsl --shutdown

# 创建目录
mkdir D:\WSL\Ubuntu22.04_Export

# 导出系统
wsl --export Ubuntu-22.04 D:\WSL\ubuntu22.04.tar

# 注销旧实例
wsl --unregister Ubuntu-22.04

# 重新导入到新位置
wsl --import Ubuntu-22.04 D:\WSL\Ubuntu22.04 D:\WSL\ubuntu22.04.tar --version 2
```

**3. 设置默认用户**

```bash
# 进入新系统
wsl -d Ubuntu-22.04

# 修改默认用户
sudo nano /etc/wsl.conf
# 添加：[user]\ndefault=你的用户名

wsl --shutdown
wsl -d Ubuntu-22.04
```

## 总结

- **推荐使用方法一（DiskPart）**：简单快速，无需额外功能
- **方法二（导出/导入）**：适合需要系统迁移的场景

---

**创建日期**: 2026-03-15
**最后更新**: 2026-03-15
**版本**: 1.0
