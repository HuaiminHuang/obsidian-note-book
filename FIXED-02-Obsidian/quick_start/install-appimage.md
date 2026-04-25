# AppImage 安装

下载并配置 Obsidian AppImage 版本。

## 下载

官网地址：https://obsidian.md

选择 **Linux - AppImage** 版本下载。

下载后文件名类似：

```
Obsidian-1.x.x.AppImage
```

默认保存在 `~/Downloads` 目录。

## 赋予执行权限

```bash
cd ~/Downloads
chmod +x Obsidian-*.AppImage
```

## 直接运行测试

```bash
./Obsidian-*.AppImage
```

---

## 长期使用规范

建议整理到专用目录：

```bash
mkdir -p ~/Applications/obsidian
mv ~/Downloads/Obsidian-*.AppImage ~/Applications/obsidian/
chmod +x ~/Applications/obsidian/Obsidian-*.AppImage
```

### 以后运行

```bash
~/Applications/obsidian/Obsidian-*.AppImage
```

---

> [!warning] 可能遇到的问题
> 如果运行时报错 `error loading libfuse.so.2`，请查看 [[install-fuse|解决 FUSE 依赖]]。
