# skills-sh-recommender Installation Guide

> This document is for AI Agents (Large Language Models) to read and automatically parse and execute the installation process.

## 1. Quick Start

```bash
# Step 1: Clone the repository to the standard location
git clone https://github.com/2025wjt/-skill.sh-skill ~/.config/opencode/skills/skills-sh-recommender

# Step 2: Enter the skill directory
cd ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender

# Step 3: Run the installation script
python install.py
```

## 2. Environment Requirements

| Requirement | Minimum Version | Notes |
|-------------|-----------------|-------|
| Python | 3.8+ | Standard library only, no pip dependencies |
| Git | Any version | For cloning the repository |
| OS | Windows / Linux / macOS | Cross-platform compatible |

## 3. Path Information

### 3.1 Standard Installation Path

```
~/.config/opencode/skills/skills-sh-recommender/
```

### 3.2 Path Verification Commands

```bash
# Verify skill directory exists
ls -la ~/.config/opencode/skills/skills-sh-recommender/

# Verify core script exists
ls -la ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py
```

**Expected Output**: If files exist, the path is correct.

### 3.3 Dynamic Path Detection Algorithm

If the installation path is non-standard, use the following Python algorithm to automatically discover the skill directory:

```python
import os
import sys
from pathlib import Path

def find_skill_path() -> str:
    """
    Automatically discover the skills-sh-recommender skill directory
    Strategy Priority: Environment Variable > Standard Location > Symlink > Directory Search
    """
    # Strategy 1: Check SKILL_HOME environment variable
    if os.environ.get('SKILL_HOME'):
        path = os.path.join(os.environ['SKILL_HOME'], 'skills-sh-recommender')
        if os.path.exists(path):
            return os.path.abspath(path)
    
    # Strategy 2: Check standard location ~/.config/opencode/skills/skills-sh-recommender
    home = os.path.expanduser('~')
    standard_path = os.path.join(home, '.config', 'opencode', 'skills', 'skills-sh-recommender')
    if os.path.exists(standard_path):
        return os.path.abspath(standard_path)
    
    # Strategy 3: Check symlink target of ~/.config/opencode/skills/
    skills_link = os.path.join(home, '.config', 'opencode', 'skills')
    if os.path.islink(skills_link):
        target = os.readlink(skills_link)
        # Symlink may point to .../superpowers/skills/, need to append skills-sh-recommender
        path = os.path.join(target, 'skills-sh-recommender')
        if os.path.exists(path):
            return os.path.abspath(path)
        # May also be a direct link to skills-sh-recommender
        if target.endswith('skills-sh-recommender'):
            return os.path.abspath(target)
    
    # Strategy 4: Search upward from current file location
    current = Path(__file__).parent.resolve() if '__file__' in dir() else Path.cwd()
    for _ in range(10):  # Search up to 10 levels
        if current.name == 'skills-sh-recommender':
            return str(current)
        parent = current.parent
        if parent == current:  # Reached root directory
            break
        current = parent
    
    # Strategy 5: Search for skills-sh-recommender in parent directories
    if '__file__' in dir():
        current = Path(__file__).parent.resolve()
    else:
        current = Path.cwd()
    
    for _ in range(5):
        sibling = current / 'skills-sh-recommender'
        if sibling.exists():
            return str(sibling)
        current = current.parent
    
    raise FileNotFoundError("Cannot find skills-sh-recommender skill directory")

# Usage Example
try:
    skill_path = find_skill_path()
    cli_path = os.path.join(skill_path, 'tools', 'skills.py')
    print(f"Skill Path: {skill_path}")
    print(f"CLI Path: {cli_path}")
except FileNotFoundError as e:
    print(f"Error: {e}")
    sys.exit(1)
```

## 4. Detailed Installation Steps

### 4.1 Method 1: Git Clone (Recommended)

```bash
# 1. Ensure target directory exists
mkdir -p ~/.config/opencode/skills

# 2. Clone the repository
git clone https://github.com/2025wjt/-skill.sh-skill ~/.config/opencode/skills/skills-sh-recommender

# 3. Enter the skill directory
cd ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender

# 4. Run the installation script
python install.py
```

### 4.2 Method 2: Manual Download

1. Visit https://github.com/2025wjt/-skill.sh-skill/releases
2. Download the latest source code archive
3. Extract to `~/.config/opencode/skills/skills-sh-recommender/`
4. Enter the `skills-sh-recommender` subdirectory
5. Run `python install.py`

### 4.3 Method 3: OpenCode Ecosystem Installation

```bash
opencode skill install 2025wjt/-skill.sh-skill
```

## 5. Correct Usage

### 5.1 Get Skill Path (Python)

```python
import os
import sys

def get_skill_path():
    """Get the installation path of skills-sh-recommender"""
    script = '''
import os
from pathlib import Path

def find_skill_path():
    home = os.path.expanduser("~")
    path = os.path.join(home, ".config", "opencode", "skills", "skills-sh-recommender")
    if os.path.exists(path):
        print(os.path.abspath(path))
        return
    
    # Check symlink
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

### 5.2 Execute Skill Search

**General Command Template**:

```bash
python <skill-path>/tools/skills.py search "<search-keyword>"
```

**Real Examples**:

```bash
# Windows
python "%USERPROFILE%\.config\opencode\skills\skills-sh-recommender\tools\skills.py" search "student management"

# Linux/macOS
python ~/.config/opencode/skills/skills-sh-recommender/tools/skills.py search "student management"
```

### 5.3 Cross-Platform Wrapper

```python
import os
import platform
import subprocess

def run_skill_command(query: str, command: str = "search") -> subprocess.CompletedProcess:
    """
    Cross-platform call to skills-sh-recommender CLI
    
    Args:
        query: Search keyword
        command: Command type (search/show/update)
    
    Returns:
        subprocess.CompletedProcess object
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

# Usage Example
result = run_skill_command("student management", "search")
print(result.stdout)
```

## 6. Troubleshooting

### Q1: ImportError

**Error Message**:
```
ModuleNotFoundError: No module named 'tools.xxx'
```

**Cause Analysis**:
- Current working directory is not the skill directory
- Python import path is not set correctly

**Solutions**:

```bash
# Method 1: Ensure you're in the skill directory
cd ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender
python tools/skills.py search "test"

# Method 2: Use full path
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "test"
```

### Q2: Path Not Found Error

**Error Message**:
```
FileNotFoundError: [Errno 2] No such file or directory
```

**Solutions**:

```bash
# 1. Check if path exists
ls -la ~/.config/opencode/skills/

# 2. If directory doesn't exist, re-clone
git clone https://github.com/2025wjt/-skill.sh-skill ~/.config/opencode/skills/skills-sh-recommender

# 3. Check symlink
ls -la ~/.config/opencode/skills/
# If you see superpowers -> ... symlink, use the actual target path
```

### Q3: Permission Error

**Error Message**:
```
PermissionError: [Errno 13] Permission denied
```

**Solutions** (Linux/macOS):

```bash
chmod +x ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py
```

**Solutions** (Windows):
Run Command Prompt or PowerShell as Administrator.

### Q4: Network Timeout

**Error Message**:
```
urllib.error.URLError: <urlopen error timed out>
```

**Solutions**:

```bash
# Manually update index (increase timeout)
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py update --index
```

If network issues persist, check:
- Is network connection working?
- Are proxy settings correct?
- Is https://skills.sh accessible?

### Q5: Python Version Too Old

**Error Message**:
```
SyntaxError: f-string without f
```

**Solutions**:

```bash
# Check Python version
python --version

# If version is below 3.8, please upgrade Python
# Windows: https://www.python.org/downloads/
# macOS: brew install python@3.11
# Linux: sudo apt install python3.11
```

## 7. Verify Installation

### 7.1 Method 1: Run Verification Script

```bash
cd ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender
python verify.py
```

**Expected Output**:
```
========================================
skills-sh-recommender Installation Verification
========================================
✅ Python version check passed (3.13.5)
✅ Skill directory exists
✅ Core scripts accessible
✅ Index file initialized
✅ Installation verification passed

🎉 Installation successful!
```

### 7.2 Method 2: Manual Verification

```bash
# 1. Check Python version
python --version
# Expected: Python 3.8+

# 2. Check directory structure
ls -la ~/.config/opencode/skills/skills-sh-recommender/
# Expected: see skills-sh-recommender subdirectory

# 3. Check core script
ls -la ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py
# Expected: file exists

# 4. Run test search
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "git"
# Expected: search results output
```

### 7.3 Verification Failure Handling

If verification fails, follow these steps:

1. **Check environment**:
   ```bash
   python --version
   git --version
   ```

2. **Check path**:
   ```bash
   ls -la ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/
   ```

3. **Re-run installation**:
   ```bash
   cd ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender
   python install.py
   ```

4. **View error log**:
   ```bash
   python install.py 2>&1
   ```

## 8. Usage Examples

### 8.1 Search Skills

```bash
# Search for student management related skills
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "student management"

# Search for git related skills
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "git"

# Search for testing related skills
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "testing"
```

### 8.2 Show Skill Details

```bash
# Show detailed information for a specific skill
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py show <skill_id>

# Example
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py show obra/superpowers/using-git-worktrees
```

### 8.3 Update Local Index

```bash
# Update skill index (get latest skill list)
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py update --index

# Force refresh specific skill details
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py update --id <skill_id>
```

## 9. Uninstall

### 9.1 Method 1: Run Uninstall Script

```bash
cd ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender
python uninstall.py
```

### 9.2 Method 2: Manual Delete

```bash
# Delete skill directory
rm -rf ~/.config/opencode/skills/skills-sh-recommender

# Delete cache files (optional)
rm -rf ~/.skills-sh/
```

## 10. File Structure

```
skills-sh-recommender/
├── llm_read.md                    # This installation guide (for AI agents)
├── llm_read_en.md                 # Installation guide (English)
├── install.py                     # Installation script
├── verify.py                      # Verification script
├── uninstall.py                   # Uninstall script
├── README.md                      # User guide (Chinese)
├── README_EN.md                   # User guide (English)
├── .gitignore                     # Git ignore configuration
├── LICENSE                        # Open source license
├── SKILL.md                       # Skill definition file
├── skills-sh-recommender/         # Skill core directory
│   ├── tools/                     # Core tool modules
│   │   ├── skills.py              # CLI entry point
│   │   ├── cache.py               # Cache management
│   │   ├── fetcher.py             # Network requests
│   │   ├── parser.py              # HTML parsing
│   │   ├── id_resolver.py         # ID resolution
│   │   ├── smart_search.py        # Smart search
│   │   ├── skill_detector.py      # Skill detection
│   │   ├── intent_analyzer.py     # Intent analysis
│   │   ├── query_expander.py      # Query expansion
│   │   ├── result_validator.py    # Result validation
│   │   ├── constants.py           # Constants
│   │   └── __init__.py
│   ├── tests/                     # Test cases
│   │   ├── test_cache.py
│   │   ├── test_fetcher.py
│   │   ├── test_parser.py
│   │   ├── test_id_resolver.py
│   │   ├── integration/
│   │   │   ├── test_smoke.py
│   │   │   └── test_cli_contract.py
│   │   └── fixtures/
│   └── .pytest_cache/             # pytest cache
└── nul                            # Windows null device file
```

## 11. Support

- **GitHub Issues**: https://github.com/2025wjt/-skill.sh-skill/issues
- **Repository**: https://github.com/2025wjt/-skill.sh-skill
- **Maintainer**: @2025wjt
- **Documentation**: https://github.com/2025wjt/-skill.sh-skill/blob/main/skills-sh-recommender/llm_read_en.md

## 12. Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2026-01-28 | Initial release |

## 13. License

This project is licensed under the MIT License.

---

**Enjoy using it!** 🎉
