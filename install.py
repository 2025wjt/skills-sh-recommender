#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skills-sh-recommender 安装脚本

功能：
1. 检测环境（Python 版本、OS 类型）
2. 验证路径结构
3. 初始化索引缓存
4. 生成环境变量配置

使用方法：
    python install.py
"""

import os
import sys
import json
import platform
from pathlib import Path


def get_skill_base_path():
    """获取技能的基准路径（skills-sh-recommender 目录）"""
    current = Path(__file__).parent.resolve()
    # 如果当前目录就是 skills-sh-recommender，直接返回
    if current.name == "skills-sh-recommender":
        return current
    # 否则查找父目录中的 skills-sh-recommender
    parent = current.parent
    sibling = parent / "skills-sh-recommender"
    if sibling.exists():
        return sibling
    return current


def check_python_version():
    """检查 Python 版本"""
    if sys.version_info < (3, 8):
        print(
            f"[X] Python 3.8+ required, got {sys.version_info.major}.{sys.version_info.minor}"
        )
        return False
    print(
        f"[OK] Python 版本检查通过 ({sys.version_info.major}.{sys.version_info.minor})"
    )
    return True


def check_core_files(skill_path):
    """检查核心文件是否存在"""
    required_files = [
        "tools/skills.py",
        "tools/cache.py",
        "tools/fetcher.py",
        "tools/parser.py",
        "tools/id_resolver.py",
        "tools/smart_search.py",
        "tools/skill_detector.py",
        "tools/intent_analyzer.py",
        "tools/query_expander.py",
        "tools/result_validator.py",
        "tools/constants.py",
    ]

    missing_files = []
    for file in required_files:
        if not (skill_path / file).exists():
            missing_files.append(file)

    if missing_files:
        print("[X] 缺少核心文件：")
        for f in missing_files:
            print(f"   - {f}")
        return False

    print("[OK] 核心文件检查通过")
    return True


def init_cache():
    """初始化缓存目录"""
    cache_dir = Path.home() / ".skills-sh"
    cache_dir.mkdir(parents=True, exist_ok=True)

    # 创建初始索引文件
    l0_file = cache_dir / "l0.jsonl"
    if not l0_file.exists():
        l0_file.write_text("")
        print(f"[OK] 创建索引文件: {l0_file}")
    else:
        print(f"[OK] 索引文件已存在: {l0_file}")

    return str(cache_dir)


def create_symlink_if_needed():
    """在标准位置创建软链接（如果需要）"""
    home = Path.home()
    standard_path = home / ".config" / "opencode" / "skills" / "skills-sh-recommender"
    skills_link = home / ".config" / "opencode" / "skills"

    skill_path = get_skill_base_path()

    # 如果技能已经在标准位置，无需创建软链接
    try:
        if standard_path.resolve() == skill_path.resolve():
            print("[OK] 技能已在标准位置，无需创建软链接")
            return True
    except Exception:
        pass

    # 检查标准位置是否存在
    if standard_path.exists() or skills_link.exists():
        print("[INFO] 标准位置已存在文件，跳过软链接创建")
        return True

    try:
        # 确保父目录存在
        skills_link.parent.mkdir(parents=True, exist_ok=True)

        # 创建软链接
        # 注意：这里我们创建从 skills 到 skills-sh-recommender 的软链接
        # 这样 ~/.config/opencode/skills/ 会指向 ~/.config/opencode/skills/skills-sh-recommender
        if platform.system() == "Windows":
            # Windows 使用 mklink 命令
            import subprocess

            result = subprocess.run(
                ["mklink", "/D", str(skills_link), str(skill_path)],
                shell=True,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0 and "already exists" not in result.stderr:
                print(f"[WARN] 无法创建软链接 (Windows): {result.stderr}")
        else:
            # Linux/macOS 使用 os.symlink
            if skills_link.is_symlink() or skills_link.exists():
                print("[WARN] 目标路径已存在，跳过软链接创建")
            else:
                os.symlink(skill_path, skills_link)
                print(f"[OK] 创建软链接: {skills_link} -> {skill_path}")
    except Exception as e:
        print(f"[WARN] 创建软链接失败: {e}")
        print("   这不影响技能使用，但建议手动创建软链接以保持兼容性")

    return True


def print_usage_info(skill_path):
    """打印使用信息"""
    print("\n" + "=" * 50)
    print("安装完成！")
    print("=" * 50)
    print(f"\n技能路径: {skill_path}")
    print(f"\n使用方式：")
    print(f"  # 搜索技能")
    print(f"  python {skill_path}/tools/skills.py search <关键词>")
    print(f"\n  # 查看技能详情")
    print(f"  python {skill_path}/tools/skills.py show <skill_id>")
    print(f"\n  # 更新索引")
    print(f"  python {skill_path}/tools/skills.py update --index")
    print(f"\n验证安装：")
    print(f"  python {skill_path}/verify.py")


def main():
    print("=" * 50)
    print("skills-sh-recommender 安装程序")
    print("=" * 50)
    print()

    # 1. 获取技能路径
    skill_path = get_skill_base_path()
    print(f"技能目录: {skill_path}")

    # 2. 检查 Python 版本
    if not check_python_version():
        sys.exit(1)

    # 3. 检查核心文件
    if not check_core_files(skill_path):
        print("\n[X] 缺少必要的文件，请确保完整克隆了仓库")
        sys.exit(1)

    # 4. 初始化缓存
    print()
    cache_dir = init_cache()
    print(f"缓存目录: {cache_dir}")

    # 5. 创建软链接（可选）
    print()
    create_symlink_if_needed()

    # 6. 打印使用信息
    print_usage_info(skill_path)


if __name__ == "__main__":
    main()
