# OpenCode 自动补全配置

> [!NOTE]
> 正确配置自动补全可以提升命令行使用效率

#opencode #completion #shell配置

---

## 配置步骤

### 1. 查看补全脚本内容（只看，不执行）

```bash
opencode completion --help
```

### 2. 将补全脚本添加到 .bashrc（推荐方式）

```bash
opencode completion >> ~/.bashrc
```

### 3. 重新加载配置

```bash
source ~/.bashrc
```

---

## 常见问题排查

> [!WARNING]
> 如果自动补全不工作，请检查以下内容

### 检查清单

1. **是否已执行 `source ~/.bashrc`**
   - 确保在配置后重新加载了 bash 配置
   - 或者重新打开终端窗口

2. **终端是否支持 bash 补全**
   - 确认使用的是 bash shell
   - 可以通过 `echo $SHELL` 查看当前 shell

3. **opencode 是否已正确安装并配置**
   - 运行 `opencode --version` 确认安装成功
   - 确保 opencode 在 PATH 中

---

## 其他 Shell 支持

### Zsh

```bash
opencode completion >> ~/.zshrc
source ~/.zshrc
```

### Fish

```bash
opencode completion >> ~/.config/fish/completions/opencode.fish
```

---

## 相关链接

- [[CLI 命令速查]]
- [[OpenCode 文档索引]]
