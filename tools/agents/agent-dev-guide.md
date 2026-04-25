---
description: 迭代改进 subagent 配置的流程指南
mode: subagent
tools:
  read: true
  edit: true
  glob: true
permission:
  edit: allow
---

## Subagent 迭代流程

### 1. 手动测试

```
@explorer 帮我分析 xxx 需求
```

观察：
- 是否理解任务？
- 输出是否结构化？
- 是否遵守权限限制？

### 2. 记录问题

创建测试记录：

```markdown
## 测试: explorer 分析需求

**输入:** 分析用户登录流程
**期望:** 输出计划 + 风险提示
**实际:** [记录实际输出]
**问题:** [发现的问题]
```

### 3. 修改配置

编辑 `~/.config/opencode/agents/explorer.md`：
- 调整 prompt 描述
- 修改 tools 权限
- 优化输出格式

### 4. 验证改进

重新测试相同场景，确认问题已修复

---

## 配置参数调优

| 参数 | 调优方向 |
|------|----------|
| `description` | 更精确描述触发条件 |
| `tools` | 根据实际需要增减 |
| `permission` | 平衡能力与安全 |
| `temperature` | 创造性 vs 确定性 |
| prompt 内容 | 调整行为指导 |

---

## 最佳实践

1. **一次改一个参数** - 便于定位影响
2. **保留版本记录** - 用 git 管理变更
3. **建立测试集** - 标准化测试场景
4. **收集真实反馈** - 使用中发现问题

---

## 迭代记录

### 2026-02-26 迭代

**数据来源**: history/opencode_chat_export_20260224_195953.json

**使用统计**:
| Agent | 会话占比 | Tokens占比 |
|-------|----------|------------|
| build | 66.0% | 91.3% |
| explorer | 12.8% | 2.6% |
| general | 8.5% | 2.5% |
| reviewer | 6.4% | 2.0% |
| plan | 2.1% | 0.1% |

**本次变更**:
1. **executor.md** - 添加 Context 优化提示（减少 tokens 消耗）
2. **explorer.md** - 增加深度分析能力和探索策略
3. **reviewer.md** - 增加审查维度和问题检查清单
4. **plan.md** - 新增规划专用 subagent（原 plan 使用极少但复杂度最高）

**下一步计划**:
- 推广 reviewer 使用率
- 复杂任务引导使用 plan agent
- 监控 tokens 消耗变化
