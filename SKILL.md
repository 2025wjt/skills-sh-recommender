---
name: skills-sh-recommender
description: Search and recommend skills from skills.sh. Use when user wants to find, explore, or install AI agent skills from the skills.sh marketplace.
---

## When to Use

Use this skill when:
- User asks to "搜索 skills"、"查找 skill"、"推荐一个 skill"
- User wants to explore available skills
- User asks "有什么 skill 可以用"
- User wants to install a specific skill

## How to Use

### Search for Skills

```bash
python tools/skills.py search "<keyword>"
```

Example: `python tools/skills.py search "git"`

Output (Markdown):
```markdown
## Search Results: "git"

Found 5 results:

### 1. obra/superpowers/using-git-worktrees
- **ID**: `obra/superpowers/using-git-worktrees`
- **Description**: > English description...

**Install Command**:
```bash
npx skills add obra/superpowers/using-git-worktrees
```

**OpenCode (Backup)**:
```bash
opencode skill install obra/superpowers/using-git-worktrees
```

Found 5 results, showing all.
```

### Show Skill Details

```bash
python tools/skills.py show "<owner/repo/skill>"
```

Example: `python tools/skills.py show "obra/superpowers/using-git-worktrees"`

### Update Skill Index

```bash
python tools/skills.py update --index
```

Refreshes the local cache of available skills from skills.sh.

## Translation Rules

- **Script text** (titles, labels, messages): English (agent layer will translate to Chinese)
- **IDs, URLs, commands, code blocks**: Keep original
- **Descriptions**: Keep English原文 (agent layer is responsible for translating when displaying)

## Output Display and Translation Rules (Mandatory)

After executing `python tools/skills.py ...` and getting the stdout Markdown:

1) **Do not paste** the script output to users as-is.
2) You **must translate** the natural language content into Chinese (Simplified) before displaying.
3) **Must preserve** (do NOT translate/rewrite):
   - Skill IDs (e.g., `owner/repo/skill`)
   - URLs
   - Commands in backticks (e.g., `npx skills add ...` / `opencode skill install ...`)
   - Code blocks, file paths, cache paths (e.g., `~/.skills-sh/`)
   - Numbers and units (values unchanged)
4) **Keep Markdown structure unchanged**: numbering, hierarchy, field order unchanged.
5) **User can override**: If user explicitly requests "don't translate/keep English", output English原文 (still preserve structure).

> Note: Script field names (like "安装/详情/提示") can remain in Chinese; mainly need to translate English descriptions and titles fetched from skills.sh.

## Output Format

All output is valid Markdown ready for agent consumption:
- Titles start with `## `
- Field labels: `ID`, `Author`, `Tags`, `Description`, `Install Command`
- Commands in fenced code blocks
- ID in backticks: `owner/repo/skill`

## Examples

**User says**: "帮我搜索一下 git 相关的 skill"

**You invoke**: `python tools/skills.py search "git"`

**Then present** the Markdown output to the user (agent should translate descriptions).

**User says**: "我想看看 using-git-worktrees 这个 skill 的详情"

**You invoke**: `python tools/skills.py show "obra/superpowers/using-git-worktrees"`

**User says**: "更新一下 skill 列表"

**You invoke**: `python tools/skills.py update --index`
