# skills-sh-recommender

[![GitHub Repo](https://img.shields.io/badge/GitHub-2025wjt%2F--skill.sh-skill-blue)](https://github.com/2025wjt/-skill.sh-skill)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 简介

`skills-sh-recommender` 是一个用于搜索和管理 [skills.sh](https://skills.sh/) 技能市场的命令行工具。它可以帮助你：

- 🔍 搜索与特定关键词相关的 AI 技能
- 📦 查看技能的详细信息
- 🔄 管理本地技能索引缓存
- 🤖 自动化技能发现和安装流程

## 功能特性

- **智能搜索**：支持关键词搜索，自动匹配技能名称、描述和标签
- **详细展示**：查看技能的 ID、作者、更新时间和安装命令
- **索引管理**：本地缓存技能列表，支持增量更新
- **跨平台**：支持 Windows、Linux、macOS
- **零依赖**：纯 Python 标准库，无需 pip 安装

## 安装

### 方式一：Git 克隆（推荐）

```bash
# 克隆到标准位置
git clone https://github.com/2025wjt/-skill.sh-skill ~/.config/opencode/skills/skills-sh-recommender

# 进入技能目录
cd ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender

# 运行安装脚本
python install.py
```

### 方式二：手动安装

1. 下载源码压缩包：https://github.com/2025wjt/-skill.sh-skill/releases
2. 解压到 `~/.config/opencode/skills/skills-sh-recommender/`
3. 进入 `skills-sh-recommender` 目录
4. 运行 `python install.py`

### 方式三：OpenCode 生态

```bash
opencode skill install 2025wjt/-skill.sh-skill
```

## 使用方法

### 搜索技能

```bash
# 搜索与 Git 相关的技能
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "git"

# 搜索与测试相关的技能
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "测试"

# 搜索与学生管理相关的技能
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "学生管理"
```

### 查看技能详情

```bash
# 查看指定技能的详细信息
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py show obra/superpowers/using-git-worktrees
```

### 更新本地索引

```bash
# 更新技能索引
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py update --index

# 强制刷新指定技能详情
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py update --id obra/superpowers/using-git-worktrees
```

## 验证安装

安装完成后，运行验证脚本确认安装成功：

```bash
cd ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender
python verify.py
```

**预期输出**：

```
========================================
skills-sh-recommender 安装验证
========================================
✅ Python 版本检查通过 (3.13.5)
✅ 技能目录存在
✅ 核心脚本可访问
✅ 索引文件已初始化
✅ 安装验证通过

🎉 安装成功！
```

## 卸载

```bash
cd ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender
python uninstall.py
```

或手动删除：

```bash
rm -rf ~/.config/opencode/skills/skills-sh-recommender
rm -rf ~/.skills-sh/
```

## 文件结构

```
skills-sh-recommender/
├── llm_read.md              # 安装指南（大模型用）
├── llm_read_en.md           # 安装指南（英文版）
├── install.py               # 安装脚本
├── verify.py                # 验证脚本
├── uninstall.py             # 卸载脚本
├── README.md                # 本说明文档
├── README_EN.md             # 说明文档（英文版）
├── .gitignore               # Git 忽略配置
├── LICENSE                  # 开源许可证
├── SKILL.md                 # 技能定义
├── skills-sh-recommender/   # 技能核心目录
│   ├── tools/               # 核心工具
│   ├── tests/               # 测试用例
│   └── .pytest_cache/       # pytest 缓存
└── nul                      # Windows 空设备文件
```

## 常见问题

### Q1: ImportError 错误

**问题**：运行命令时出现 `ModuleNotFoundError`

**解决**：确保在技能目录下执行，或使用完整路径：

```bash
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "test"
```

### Q2: 权限错误

**问题**：Permission denied

**解决**（Linux/macOS）：

```bash
chmod +x ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py
```

### Q3: 网络超时

**问题**：请求超时

**解决**：检查网络连接，或稍后重试

### Q4: Python 版本过低

**问题**：SyntaxError

**解决**：升级到 Python 3.8+

## 技术支持

- **GitHub Issues**: https://github.com/2025wjt/-skill.sh-skill/issues
- **仓库地址**: https://github.com/2025wjt/-skill.sh-skill
- **维护者**: @2025wjt

## 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2026-01-28 | 初始发布 |

## 开源许可

本项目采用 MIT License 开源许可。

---

**使用愉快！** 🎉
