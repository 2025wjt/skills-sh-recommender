#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skills-sh-recommender 验证脚本

功能：
1. 验证 Python 版本
2. 验证技能目录存在
3. 验证核心脚本可访问
4. 验证索引文件已初始化

使用方法：
    python verify.py
"""

import os
import sys
import platform
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


def verify_python_version():
    """验证 Python 版本"""
    print("[CHECK] 检查 Python 版本...")
    if sys.version_info < (3, 8):
        print(
            f"[FAIL] Python 3.8+ required, got {sys.version_info.major}.{sys.version_info.minor}"
        )
        return False
    print(f"[PASS] Python {sys.version_info.major}.{sys.version_info.minor} (>= 3.8)")
    return True


def verify_skill_directory(skill_path):
    """验证技能目录存在"""
    print("\n[CHECK] 检查技能目录...")
    if not skill_path.exists():
        print(f"[FAIL] 技能目录不存在: {skill_path}")
        return False
    print(f"[PASS] 技能目录存在: {skill_path}")
    return True


def verify_core_scripts(skill_path):
    """验证核心脚本可访问"""
    print("\n[CHECK] 检查核心脚本...")

    required_files = [
        "tools/skills.py",
        "tools/cache.py",
        "tools/fetcher.py",
        "tools/parser.py",
        "tools/id_resolver.py",
    ]

    all_exist = True
    for file in required_files:
        file_path = skill_path / file
        if file_path.exists():
            print(f"[PASS] {file}")
        else:
            print(f"[FAIL] {file} (不存在)")
            all_exist = False

    return all_exist


def verify_index_file():
    """验证索引文件已初始化"""
    print("\n[CHECK] 检查索引文件...")

    cache_dir = Path.home() / ".skills-sh"
    l0_file = cache_dir / "l0.jsonl"

    if not cache_dir.exists():
        print(f"[INFO] 缓存目录不存在，将在使用时自动创建")
        print(f"[PASS] 通过 (将在首次运行时初始化)")
        return True

    if not l0_file.exists():
        print(f"[INFO] 索引文件不存在，将在使用时自动创建")
        print(f"[PASS] 通过 (将在首次运行时初始化)")
        return True

    print(f"[PASS] 索引文件已存在: {l0_file}")
    return True


def verify_import():
    """验证模块导入"""
    print("\n[CHECK] 检查模块导入...")

    skill_path = get_skill_base_path()
    tools_path = skill_path / "tools"

    if str(tools_path) not in sys.path:
        sys.path.insert(0, str(tools_path))

    try:
        from cache import load_l0, save_l0
        from fetcher import fetch_sitemap
        from parser import parse_sitemap

        print("[PASS] 模块导入成功")
        return True
    except ImportError as e:
        print(f"[FAIL] 模块导入失败: {e}")
        return False


def run_smoke_test():
    """运行冒烟测试"""
    print("\n[CHECK] 运行冒烟测试...")

    skill_path = get_skill_base_path()
    cli_path = skill_path / "tools" / "skills.py"

    if not cli_path.exists():
        print(f"[FAIL] CLI 脚本不存在: {cli_path}")
        return False

    # 测试 search 命令（不需要网络）
    import subprocess

    result = subprocess.run(
        [sys.executable, str(cli_path), "search", "test"],
        capture_output=True,
        text=True,
        cwd=str(skill_path),
        timeout=30,
    )

    # 检查是否成功执行（可能有结果或明确的无结果消息）
    if result.returncode == 0:
        print("[PASS] CLI 脚本可执行")
        return True
    else:
        # 如果返回码不为 0，检查是否只是没有找到结果
        if "未找到" in result.stdout or "No results" in result.stdout:
            print("[PASS] CLI 脚本可执行（搜索功能正常）")
            return True
        print(f"[FAIL] CLI 脚本执行失败")
        print(f"      stdout: {result.stdout[:200]}")
        print(f"      stderr: {result.stderr[:200]}")
        return False


def main():
    print("=" * 50)
    print("skills-sh-recommender 安装验证")
    print("=" * 50)

    all_passed = True

    # 1. 检查 Python 版本
    if not verify_python_version():
        all_passed = False

    # 2. 获取技能路径
    skill_path = get_skill_base_path()
    print(f"\n[DIR] 技能路径: {skill_path}")

    # 3. 验证技能目录
    if not verify_skill_directory(skill_path):
        all_passed = False

    # 4. 验证核心脚本
    if not verify_core_scripts(skill_path):
        all_passed = False

    # 5. 验证索引文件
    if not verify_index_file():
        all_passed = False

    # 6. 验证模块导入
    if not verify_import():
        all_passed = False

    # 7. 运行冒烟测试
    if not run_smoke_test():
        all_passed = False

    # 输出结果
    print("\n" + "=" * 50)
    if all_passed:
        print("[PASS] 安装验证通过")
        print("=" * 50)
        print("\n[OK] 技能已成功安装！")
        print("\n下一步：")
        print(f"  python {skill_path}/tools/skills.py search <关键词>")
        return 0
    else:
        print("[FAIL] 安装验证失败")
        print("=" * 50)
        print("\n请检查上述错误信息并重新运行安装脚本：")
        print(f"  cd {skill_path}")
        print(f"  python install.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())
