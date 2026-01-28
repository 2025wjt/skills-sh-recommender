#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skills-sh-recommender 卸载脚本

功能：
1. 删除技能目录
2. 删除缓存文件（可选）
3. 删除软链接（如果存在）

使用方法：
    python uninstall.py
"""

import os
import sys
import shutil
from pathlib import Path


def get_skill_base_path():
    """获取技能的基准路径"""
    current = Path(__file__).parent.resolve()
    if current.name == "skills-sh-recommender":
        return current
    parent = current.parent
    sibling = parent / "skills-sh-recommender"
    if sibling.exists():
        return sibling
    return current


def get_standard_skill_path():
    """获取标准安装路径"""
    home = Path.home()
    return home / ".config" / "opencode" / "skills" / "skills-sh-recommender"


def remove_skill_directory(skill_path, force=False):
    """删除技能目录"""
    print("\n[DELETE] 删除技能目录...")

    if not skill_path.exists():
        print(f"[INFO] 技能目录不存在: {skill_path}")
        return True

    try:
        # 检查是否在标准位置
        standard_path = get_standard_skill_path()
        is_standard_location = skill_path.resolve() == standard_path.resolve()

        if not is_standard_location and not force:
            print(f"[WARN] 技能未安装在标准位置: {skill_path}")
            print(f"       标准位置: {standard_path}")
            response = input("       是否仍要删除? (y/N): ")
            if response.lower() != "y":
                print("[INFO] 已取消删除")
                return False

        # 删除目录
        shutil.rmtree(skill_path)
        print(f"[OK] 已删除: {skill_path}")
        return True
    except Exception as e:
        print(f"[FAIL] 删除失败: {e}")
        return False


def remove_cache_files():
    """删除缓存文件"""
    print("\n[DELETE] 删除缓存文件...")

    cache_dir = Path.home() / ".skills-sh"

    if not cache_dir.exists():
        print("[INFO] 缓存目录不存在")
        return True

    try:
        shutil.rmtree(cache_dir)
        print(f"[OK] 已删除缓存: {cache_dir}")
        return True
    except Exception as e:
        print(f"[WARN] 删除缓存失败: {e}")
        print("[INFO] 您可以手动删除: rm -rf ~/.skills-sh/")
        return True  # 缓存删除失败不影响卸载


def remove_symlink():
    """删除软链接"""
    print("\n[CHECK] 检查软链接...")

    home = Path.home()
    skills_link = home / ".config" / "opencode" / "skills"

    if not skills_link.is_symlink():
        print("[INFO] 不存在软链接")
        return True

    try:
        target = os.readlink(skills_link)
        os.remove(skills_link)
        print(f"[OK] 已删除软链接: {skills_link} -> {target}")
        return True
    except Exception as e:
        print(f"[WARN] 删除软链接失败: {e}")
        return True  # 软链接删除失败不影响卸载


def main():
    print("=" * 50)
    print("skills-sh-recommender 卸载程序")
    print("=" * 50)

    # 确认卸载
    print("\n[WARN] 此操作将删除以下内容：")
    print("   - skills-sh-recommender 技能目录")
    print("   - ~/.skills-sh/ 缓存目录")
    print("   - ~/.config/opencode/skills 软链接（如存在）")

    response = input("\n是否继续卸载? (y/N): ")
    if response.lower() != "y":
        print("\n[INFO] 已取消卸载")
        return 0

    skill_path = get_skill_base_path()
    print(f"\n技能路径: {skill_path}")

    all_passed = True

    # 1. 删除软链接
    if not remove_symlink():
        all_passed = False

    # 2. 删除技能目录
    if not remove_skill_directory(skill_path, force=False):
        all_passed = False

    # 3. 删除缓存文件
    if not remove_cache_files():
        all_passed = False

    # 输出结果
    print("\n" + "=" * 50)
    if all_passed:
        print("[OK] 卸载完成")
        print("=" * 50)
        print("\n[OK] skills-sh-recommender 已成功卸载")
        return 0
    else:
        print("[WARN] 部分操作失败")
        print("=" * 50)
        print("\n请手动检查以下路径：")
        print(f"  - {skill_path}")
        print(f"  - {Path.home() / '.skills-sh'}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
