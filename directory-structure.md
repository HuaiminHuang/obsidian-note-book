---
title: 知识库目录结构
tags: [structure, overview]
---

# 知识库目录结构

## 完整目录树

```
ObsidianNote/
├── 01-Daily/                    # 日常学习日记（按时间归档）
│   └── 2026/                    # 按年分组
│       └── 03/                 # 按月分组
│           └── 14-学习Python装饰器.md  # 格式：DD-主题.md
├── 02-Python/                   # Python 学习
│   ├── README.md                # 学习路线图和索引
│   ├── concepts/                # 核心概念知识点
│   ├── code/                    # 代码示例和工具封装
│   └── troubleshooting/         # 问题排查
├── 03-IDE-Tools/                # IDE 和工具
│   ├── README.md                # 工具索引
│   ├── VSCode/                  # VSCode 相关
│   │   ├── plugins.md           # 常用插件
│   │   ├── debugging.md         # 调试技巧
│   │   └── config.md            # 配置选项
│   └── Windsurf/                # Windsurf 相关
├── 04-AI-Tools/                 # AI 工具使用
│   ├── README.md                # AI 工具索引
│   ├── Codeium.md
│   ├── Copilot.md
│   └── Claude.md
├── 05-Algorithms/               # 数据结构和算法
│   ├── README.md                # 算法学习路线图
│   ├── data-structures/         # 数据结构
│   │   ├── array.md
│   │   ├── linked-list.md
│   │   └── tree.md
│   └── algorithms/             # 算法
│       ├── sort.md
│       └── search.md
├── 06-Dev-Methods/              # 开发方法和规范
│   ├── README.md                # 开发方法索引
│   ├── concepts/                # 概念知识
│   │   ├── DTO.md               # 数据传输对象
│   │   ├── VO.md                # 视图对象
│   │   ├── PO.md                # 持久化对象
│   │   ├── BO.md                # 业务对象
│   │   ├── Entity.md            # 实体对象
│   │   ├── Specs.md             # 规范模式
│   │   ├── DDD.md               # 领域驱动设计
│   │   └── TDD.md               # 测试驱动开发
│   ├── code/                    # 代码示例
│   └── troubleshooting/         # 问题排查
├── 07-Frameworks/               # 框架和技术
│   ├── README.md                # 框架技术索引
│   ├── concepts/                # 概念知识
│   │   ├── FastAPI.md           # FastAPI Web 框架
│   │   ├── Flask.md             # Flask Web 框架
│   │   ├── SQLAlchemy.md        # Python ORM 框架
│   │   ├── Milvus.md            # 向量数据库
│   │   ├── Redis.md             # 内存数据库
│   │   └── MySQL.md             # 关系型数据库
│   ├── code/                    # 代码示例
│   └── troubleshooting/         # 问题排查
├── FIXED-01-Ubuntu/             # Linux/Ubuntu 使用指南（固定）
│   ├── README.md                # 使用索引
│   ├── concepts/                # Linux 概念知识
│   ├── code/                    # Linux 代码示例
│   └── troubleshooting/         # 问题排查
├── FIXED-02-Obsidian/           # Obsidian 使用指南（固定）
│   ├── README.md                # 使用索引
│   ├── templates-usage.md       # Templates 插件使用
│   └── quick_start/             # 快速入门资料
│       ├── install.md
│       ├── install-chinese.md
│       ├── install-appimage.md
│       ├── install-fuse.md
│       ├── frontmatter.md
│       ├── tags.md
│       ├── callouts.md
│       ├── embeds.md
│       └── links.md
├── FIXED-03-Todo/               # 待办事项管理（固定）
│   ├── README.md                # 看板视图
│   ├── current/                 # 当前任务
│   ├── backlog/                 # 待办事项池
│   └── done/                    # 已完成归档
├── FIXED-04-Resources/          # 资源收集（固定，始终最后）
│   ├── README.md                # 资源索引
│   ├── docs/                    # 文档链接
│   ├── blogs/                   # 博客文章
│   └── videos/                  # 视频教程
├── tools/                       # opencode 工具配置（目录隔离）
│   ├── skills/
│   ├── agents/
│   └── opencode_tips/
├── templates/                   # 模板库
│   ├── daily-note.md
│   ├── concept-note.md
│   ├── doc-note.md
│   ├── troubleshooting.md
│   └── todo.md
├── index.md                     # 全局索引
├── directory-structure.md       # 目录结构说明
└── .obsidian/                   # Obsidian 配置（已存在）
```

## 目录概览

### 📚 学习内容

- [[01-Daily]] - 日常学习日记（按时间归档）
- [[02-Python]] - Python 高级用法和工具封装
- [[03-IDE-Tools]] - IDE 生态插件和调试技巧（VSCode、Windsurf）
- [[04-AI-Tools]] - AI 辅助编程工具（Codeium、Copilot、Claude）
- [[05-Algorithms]] - 数据结构和算法
- [[06-Dev-Methods]] - 开发方法和规范（DTO、VO、PO、BO、DDD、TDD）
- [[07-Frameworks]] - 框架和技术（FastAPI、Flask、SQLAlchemy、Milvus、Redis、MySQL）

### 🛠️ 工具使用（固定目录）

- [[FIXED-01-Ubuntu]] - Linux/Ubuntu 使用指南
- [[FIXED-02-Obsidian]] - Obsidian 使用指南（模板、快速入门）

### 📝 工作管理（固定目录）

- [[FIXED-03-Todo]] - 待办事项管理

### 🔗 资源收集（固定目录）

- [[FIXED-04-Resources]] - 资源收集（文档、博客、视频）

## 目录顺序规则

1. **学习内容**：01-99（可以扩展）
   - 01-Daily：日常学习日记
   - 02-Python：Python 学习
   - 03-IDE-Tools：IDE 和工具
   - 04-AI-Tools：AI 工具使用
   - 05-Algorithms：数据结构和算法
   - 06-Dev-Methods：开发方法和规范
   - 07-Frameworks：框架和技术
   - ... 新增学习内容使用连续编号

2. **固定目录**：FIXED-01 至 FIXED-99（使用FIXED前缀标记）
   - FIXED-01-Ubuntu：Linux/Ubuntu 使用指南
   - FIXED-02-Obsidian：Obsidian 使用指南
   - FIXED-03-Todo：待办事项管理
   - FIXED-04-Resources：资源收集（始终最后）

3. **特殊目录**：不参与序号排序
   - tools/：opencode 工具配置
   - templates/：模板库
   - .obsidian/：Obsidian 配置

4. **新增规则**：
   - 新学习内容目录直接使用下一个编号（如：08-Database）
   - 固定目录使用FIXED前缀，无需调整编号
   - FIXED-04-Resources 始终保持最后

## 相关文档

- [[docs/knowledge-base-design]] - 知识库结构设计和规则

---

**更新日期**: 2026-03-15
