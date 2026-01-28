# skills-sh-recommender

[![GitHub Repo](https://img.shields.io/badge/GitHub-2025wjt%2F--skill.sh-skill-blue)](https://github.com/2025wjt/-skill.sh-skill)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## Introduction

`skills-sh-recommender` is a command-line tool for searching and managing AI skills from [skills.sh](https://skills.sh/). It helps you:

- 🔍 Search for AI skills related to specific keywords
- 📦 View detailed skill information
- 🔄 Manage local skill index cache
- 🤖 Automate skill discovery and installation

## Features

- **Smart Search**: Keyword search with automatic matching of skill names, descriptions, and tags
- **Detailed View**: View skill ID, author, update time, and installation commands
- **Index Management**: Local cache of skill list with incremental updates
- **Cross-Platform**: Supports Windows, Linux, macOS
- **Zero Dependencies**: Pure Python standard library, no pip installation required

## Installation

### Method 1: Git Clone (Recommended)

```bash
# Clone to standard location
git clone https://github.com/2025wjt/-skill.sh-skill ~/.config/opencode/skills/skills-sh-recommender

# Enter the skill directory
cd ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender

# Run the installation script
python install.py
```

### Method 2: Manual Installation

1. Download the source archive: https://github.com/2025wjt/-skill.sh-skill/releases
2. Extract to `~/.config/opencode/skills/skills-sh-recommender/`
3. Enter the `skills-sh-recommender` directory
4. Run `python install.py`

### Method 3: OpenCode Ecosystem

```bash
opencode skill install 2025wjt/-skill.sh-skill
```

## Usage

### Search Skills

```bash
# Search for git-related skills
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "git"

# Search for testing-related skills
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "testing"

# Search for student management related skills
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "student management"
```

### Show Skill Details

```bash
# Show detailed information for a specific skill
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py show obra/superpowers/using-git-worktrees
```

### Update Local Index

```bash
# Update skill index
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py update --index

# Force refresh a specific skill detail
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py update --id obra/superpowers/using-git-worktrees
```

## Verify Installation

After installation, run the verification script to confirm successful installation:

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

## Uninstall

```bash
cd ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender
python uninstall.py
```

Or manually delete:

```bash
rm -rf ~/.config/opencode/skills/skills-sh-recommender
rm -rf ~/.skills-sh/
```

## File Structure

```
skills-sh-recommender/
├── llm_read.md              # Installation guide (for AI agents)
├── llm_read_en.md           # Installation guide (English)
├── install.py               # Installation script
├── verify.py                # Verification script
├── uninstall.py             # Uninstall script
├── README.md                # This documentation (Chinese)
├── README_EN.md             # Documentation (English)
├── .gitignore               # Git ignore configuration
├── LICENSE                  # Open source license
├── SKILL.md                 # Skill definition
├── skills-sh-recommender/   # Skill core directory
│   ├── tools/               # Core tools
│   ├── tests/               # Test cases
│   └── .pytest_cache/       # pytest cache
└── nul                      # Windows null device file
```

## Troubleshooting

### Q1: ImportError

**Problem**: `ModuleNotFoundError` when running commands

**Solution**: Ensure you're in the skill directory or use the full path:

```bash
python ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py search "test"
```

### Q2: Permission Error

**Problem**: Permission denied

**Solution** (Linux/macOS):

```bash
chmod +x ~/.config/opencode/skills/skills-sh-recommender/skills-sh-recommender/tools/skills.py
```

### Q3: Network Timeout

**Problem**: Request timeout

**Solution**: Check network connection or retry later

### Q4: Python Version Too Old

**Problem**: SyntaxError

**Solution**: Upgrade to Python 3.8+

## Support

- **GitHub Issues**: https://github.com/2025wjt/-skill.sh-skill/issues
- **Repository**: https://github.com/2025wjt/-skill.sh-skill
- **Maintainer**: @2025wjt

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2026-01-28 | Initial release |

## License

This project is licensed under the MIT License.

---

**Enjoy using it!** 🎉
