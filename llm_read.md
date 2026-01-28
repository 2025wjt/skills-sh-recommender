# skills-sh-recommender 安装指南

> 本文档供大模型（AI Agent）阅读，自动解析并执行安装流程。

## 1. 快速开始

```bash
# 步骤 1：克隆仓库到标准位置
git clone https://github.com/2025wjt/-skill.sh-skill ~/.config/opencode/skills/skills-sh-recommender

# 步骤 2：进入技能目录
cd ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender

# 步骤 3：运行安装脚本
python install.py
```

## 2. 环境要求

| 要求 | 最低版本 | 说明 |
|------|----------|------|
| Python | 3.8+ | 纯标准库，无需 pip 安装 |
| Git | 任意版本 | 用于克隆仓库 |
| 操作系统 | Windows / Linux / macOS | 跨平台兼容 |

## 3. 路径说明

### 3.1 标准安装路径

```
~/.config/opencode/skills/skills-sh-recommender/
```

### 3.2 路径验证命令

```bash
# 验证技能目录存在
ls -la ~/.config/opencode/skills/skills-sh-recommender/

# 验证核心脚本存在
ls -la ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py
```

**预期输出**：如果文件存在则路径正确。

### 3.3 动态路径检测算法

如果安装路径非标准，使用以下 Python 算法自动发现技能目录：

```python
import os
import sys
from pathlib import Path

def find_skill_path() -> str:
    """
    自动发现 skills-sh-recommender 技能目录
    策略优先级：环境变量 > 标准位置 > 软链接 > 目录搜索
    """
    # 策略 1：检查环境变量 SKILL_HOME
    if os.environ.get('SKILL_HOME'):
        path = os.path.join(os.environ['SKILL_HOME'], 'skills-sh-recommender')
        if os.path.exists(path):
            return os.path.abspath(path)
    
    # 策略 2：检查标准位置 ~/.config/opencode/skills/skills-sh-recommender
    home = os.path.expanduser('~')
    standard_path = os.path.join(home, '.config', 'opencode', 'skills', 'skills-sh-recommender')
    if os.path.exists(standard_path):
        return os.path.abspath(standard_path)
    
    # 策略 3：检查软链接 ~/.config/opencode/skills/ 的实际 target
    skills_link = os.path.join(home, '.config', 'opencode', 'skills')
    if os.path.islink(skills_link):
        target = os.readlink(skills_link)
        # 软链接可能指向 .../superpowers/skills/，需要追加 skills-sh-recommender
        path = os.path.join(target, 'skills-sh-recommender')
        if os.path.exists(path):
            return os.path.abspath(path)
        # 也可能是直接链接到 skills-sh-recommender
        if target.endswith('skills-sh-recommender'):
            return os.path.abspath(target)
    
    # 策略 4：从当前文件所在目录向上搜索
    current = Path(__file__).parent.resolve() if '__file__' in dir() else Path.cwd()
    for _ in range(10):  # 最多向上 10 层
        if current.name == 'skills-sh-recommender':
            return str(current)
        parent = current.parent
        if parent == current:  # 已经到达根目录
            break
        current = parent
    
    # 策略 5：搜索父目录下的 skills-sh-recommender
    if '__file__' in dir():
        current = Path(__file__).parent.resolve()
    else:
        current = Path.cwd()
    
    for _ in range(5):
        sibling = current / 'skills-sh-recommender'
        if sibling.exists():
            return str(sibling)
        current = current.parent
    
    raise FileNotFoundError("无法找到 skills-sh-recommender 技能目录")

# 使用示例
try:
    skill_path = find_skill_path()
    cli_path = os.path.join(skill_path, 'tools', 'skills.py')
    print(f"技能路径: {skill_path}")
    print(f"CLI 路径: {cli_path}")
except FileNotFoundError as e:
    print(f"错误: {e}")
    sys.exit(1)
```

## 4. 安装步骤详解

### 4.1 方式一：Git 克隆（推荐）

```bash
# 1. 确保目标目录存在
mkdir -p ~/.config/opencode/skills

# 2. 克隆仓库
git clone https://github.com/2025wjt/-skill.sh-skill ~/.config/opencode/skills/skills-sh-recommender

# 3. 进入技能目录
cd ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender

# 4. 运行安装脚本
python install.py
```

### 4.2 方式二：手动下载安装包

1. 访问 https://github.com/2025wjt/-skill.sh-skill/releases
2. 下载最新版本的源码压缩包
3. 解压到 `~/.config/opencode/skills/skills-sh-recommender/`
4. 进入 `skills-sh-recommender` 子目录
5. 运行 `python install.py`

### 4.3 方式三：OpenCode 生态安装

```bash
opencode skill install 2025wjt/-skill.sh-skill
```

## 5. 正确调用方式

### 5.1 获取技能路径（Python）

```python
import os
import sys

def get_skill_path():
    """获取 skills-sh-recommender 的安装路径"""
    script = '''
import os
from pathlib import Path

def find_skill_path():
    home = os.path.expanduser("~")
    path = os.path.join(home, ".config", "opencode", "skills", "skills-sh-recommender")
    if os.path.exists(path):
        print(os.path.abspath(path))
        return
    
    # 检查软链接
    skills_link = os.path.join(home, ".config", "opencode", "skills")
    if os.path.islink(skills_link):
        target = os.readlink(skills_link)
        path = os.path.join(target, "skills-sh-recommender")
        if os.path.exists(path):
            print(os.path.abspath(path))
            return

find_skill_path()
'''
    import subprocess
    result = subprocess.run(
        [sys.executable, '-c', script],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None
```

### 5.2 执行技能搜索

**通用命令模板**：

```bash
python <技能路径>/tools/skills.py search "<搜索关键词>"
```

**实际示例**：

```bash
# Windows
python "%USERPROFILE%\.config\opencode\skills\skills-sh-recommender\tools\skills.py" search "学生管理"

# Linux/macOS
python ~/.config/opencode/skills/skills-sh-recommender/tools/skills.py search "学生管理"
```

### 5.3 跨平台调用封装

```python
import os
import platform
import subprocess

def run_skill_command(query: str, command: str = "search") -> subprocess.CompletedProcess:
    """
    跨平台调用 skills-sh-recommender CLI
    
    Args:
        query: 搜索关键词
        command: 命令类型 (search/show/update)
    
    Returns:
        subprocess.CompletedProcess 对象
    """
    skill_path = find_skill_path()
    cli_path = os.path.join(skill_path, 'tools', 'skills.py')
    
    cmd = [sys.executable, cli_path, command, query]
    
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

# 使用示例
result = run_skill_command("学生管理", "search")
print(result.stdout)
```

## 6. 常见问题排查

### Q1: ImportError 错误

**错误信息**：
```
ModuleNotFoundError: No module named 'tools.xxx'
```

**原因分析**：
- 当前工作目录不在技能目录下
- Python 导入路径未正确设置

**解决方案**：

```bash
# 方法 1：确保在技能目录下执行
cd ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender
python tools/skills.py search "test"

# 方法 2：使用完整路径调用
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "test"
```

### Q2: 路径不存在错误

**错误信息**：
```
FileNotFoundError: [Errno 2] No such file or directory
```

**解决方案**：

```bash
# 1. 检查路径是否存在
ls -la ~/.config/opencode/skills/

# 2. 如果目录不存在，重新克隆
git clone https://github.com/2025wjt/-skill.sh-skill ~/.config/opencode/skills/skills-sh-recommender

# 3. 检查软链接
ls -la ~/.config/opencode/skills/
# 如果看到 superpowers -> ... 的软链接，使用实际 target 路径
```

### Q3: 权限错误

**错误信息**：
```
PermissionError: [Errno 13] Permission denied
```

**解决方案**（Linux/macOS）：

```bash
chmod +x ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py
```

**解决方案**（Windows）：
以管理员身份运行命令提示符或 PowerShell。

### Q4: 网络超时

**错误信息**：
```
urllib.error.URLError: <urlopen error timed out>
```

**解决方案**：

```bash
# 手动更新索引（增加超时时间）
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py update --index
```

如果网络问题持续，请检查：
- 网络连接是否正常
- 代理设置是否正确
- https://skills.sh 是否可访问

### Q5: Python 版本过低

**错误信息**：
```
SyntaxError: f-string without f
```

**解决方案**：

```bash
# 检查 Python 版本
python --version

# 如果版本低于 3.8，请升级 Python
# Windows: https://www.python.org/downloads/
# macOS: brew install python@3.11
# Linux: sudo apt install python3.11
```

## 7. 验证安装成功

### 7.1 方式一：运行验证脚本

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

### 7.2 方式二：手动验证

```bash
# 1. 检查 Python 版本
python --version
# 预期：Python 3.8+

# 2. 检查目录结构
ls -la ~/.config/opencode/skills/skills-sh-recommender/
# 预期：看到 skills-sh-recommender 子目录

# 3. 检查核心脚本
ls -la ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py
# 预期：文件存在

# 4. 运行测试搜索
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "git"
# 预期：输出搜索结果
```

### 7.3 验证失败处理

如果验证失败，请按以下步骤排查：

1. **检查环境**：
   ```bash
   python --version
   git --version
   ```

2. **检查路径**：
   ```bash
   ls -la ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/
   ```

3. **重新运行安装**：
   ```bash
   cd ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender
   python install.py
   ```

4. **查看错误日志**：
   ```bash
   python install.py 2>&1
   ```

## 8. 使用示例

### 8.1 搜索技能

```bash
# 搜索与学生管理相关的技能
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "学生管理"

# 搜索 Git 相关技能
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "git"

# 搜索测试相关技能
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "测试"
```

### 8.2 查看技能详情

```bash
# 查看指定技能的详细信息
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py show <skill_id>

# 示例
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py show obra/superpowers/using-git-worktrees
```

### 8.3 更新本地索引

```bash
# 更新技能索引（获取最新技能列表）
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py update --index

# 强制刷新指定技能详情
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py update --id <skill_id>
```

## 9. 卸载方法

### 9.1 方式一：运行卸载脚本

```bash
cd ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender
python uninstall.py
```

### 9.2 方式二：手动删除

```bash
# 删除技能目录
rm -rf ~/.config/opencode/skills/skills-sh-recommender

# 删除缓存文件（可选）
rm -rf ~/.skills-sh/
```

## 10. 文件结构说明

```
skills-sh-recommender/
├── llm_read.md                    # 本安装指南（大模型用）
├── llm_read_en.md                 # 安装指南（英文版）
├── install.py                     # 安装脚本
├── verify.py                      # 验证脚本
├── uninstall.py                   # 卸载脚本
├── README.md                      # 用户使用说明（中文）
├── README_EN.md                   # 用户使用说明（英文）
├── .gitignore                     # Git 忽略配置
├── LICENSE                        # 开源许可证
├── SKILL.md                       # 技能定义文件
├── skills-sh-recommender/         # 技能核心目录
│   ├── tools/                     # 核心工具模块
│   │   ├── skills.py              # CLI 入口
│   │   ├── cache.py               # 缓存管理
│   │   ├── fetcher.py             # 网络请求
│   │   ├── parser.py              # HTML 解析
│   │   ├── id_resolver.py         # ID 解析
│   │   ├── smart_search.py        # 智能搜索
│   │   ├── skill_detector.py      # 技能检测
│   │   ├── intent_analyzer.py     # 意图分析
│   │   ├── query_expander.py      # 查询扩展
│   │   ├── result_validator.py    # 结果验证
│   │   ├── constants.py           # 常量定义
│   │   └── __init__.py
│   ├── tests/                     # 测试用例
│   │   ├── test_cache.py
│   │   ├── test_fetcher.py
│   │   ├── test_parser.py
│   │   ├── test_id_resolver.py
│   │   ├── integration/
│   │   │   ├── test_smoke.py
│   │   │   └── test_cli_contract.py
│   │   └── fixtures/
│   └── .pytest_cache/             # pytest 缓存
└── nul                            # Windows 空设备文件
```

## 11. 技术支持

- **GitHub Issues**: https://github.com/2025wjt/-skill.sh-skill/issues
- **仓库地址**: https://github.com/2025wjt/-skill.sh-skill
- **维护者**: @2025wjt
- **文档更新**: https://github.com/2025wjt/-skill.sh-skill/blob/main/skills-sh-recommender/llm_read.md

## 12. 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2026-01-28 | 初始发布 |

## 13. 开源许可

本项目采用 MIT License 开源许可。

---

**祝您使用愉快！** 🎉
