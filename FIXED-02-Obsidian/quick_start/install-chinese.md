# 配置中文环境

为 Obsidian 配置完整的中文支持。

## 检查当前 locale

```bash
locale
```

如果显示 `C.UTF-8`，说明不是完整中文环境。

## 安装步骤

### 1. 安装中文语言包

```bash
sudo apt update
sudo apt install language-pack-zh-hans
```

### 2. 设置系统语言

```bash
sudo update-locale LANG=zh_CN.UTF-8
```

### 3. 安装中文字体

```bash
sudo apt install fonts-noto-cjk
```

### 4. 重启生效

重启终端或重新登录系统。

### 5. Obsidian 设置

启动 Obsidian → 设置 → 关于 → 语言 → 选择 **简体中文** → 重启 Obsidian

---

## 验证

系统 locale 应显示：

```
LANG=zh_CN.UTF-8
```

完成后：

- Obsidian 界面中文
- Markdown 中文正常显示
- 脚本写入中文不乱码

---

> [!note] 相关
> 配置完成后可返回 [[install|安装指南]] 开始使用。
