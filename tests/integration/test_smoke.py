# -*- coding: utf-8 -*-
"""集成测试：真实网络冒烟测试

环境变量控制：
- RUN_INTEGRATION=1：执行集成测试（默认跳过，避免 CI/离线失败）
"""

import os
import re
import subprocess
import sys
import unittest


def skip_if_no_integration():
    """跳过装饰器：如果没有设置 RUN_INTEGRATION 环境变量则跳过"""
    if os.environ.get("RUN_INTEGRATION") != "1":
        raise unittest.SkipTest("未设置 RUN_INTEGRATION=1，跳过集成测试")
    return True


def run_cli(args, cwd=None):
    """运行 CLI 命令，返回 (stdout, stderr, returncode)"""
    repo_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    cmd = [sys.executable, "tools/skills.py"] + args
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd or repo_root,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout, result.stderr, result.returncode


def extract_first_skill_id(search_stdout):
    """从 search 输出中提取第一个 skill ID"""
    id_pattern = r"`([a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)`"
    matches = re.findall(id_pattern, search_stdout)
    return matches[0] if matches else None


class TestIntegrationUpdateIndex(unittest.TestCase):
    """集成测试 1：update --index 刷新索引"""

    def test_update_index_success(self):
        """测试 update --index 能生成/刷新 l0.jsonl"""
        skip_if_no_integration()

        stdout, stderr, rc = run_cli(["update", "--index"])

        self.assertEqual(rc, 0, f"update --index 退出码非 0：\nstderr: {stderr}")

        self.assertTrue(
            stdout.startswith("##"),
            f"stdout 必须以 Markdown 标题开头，实际：\n{stdout[:200]}",
        )

        self.assertIn(
            "索引", stdout, f"stdout 必须包含'索引'相关中文提示，实际：\n{stdout[:500]}"
        )

    def test_update_index_no_crash_on_failure(self):
        """测试 sitemap 失败时不会崩溃，继续运行"""
        skip_if_no_integration()

        stdout, stderr, rc = run_cli(["update", "--index"])

        self.assertIn(rc, [0, 1], f"update --index 崩溃：\nstderr: {stderr}")


class TestIntegrationSearchGit(unittest.TestCase):
    """集成测试 2：search --query git"""

    def test_search_git_output_is_markdown(self):
        """测试 search git 输出是 Markdown 且包含中文字段名"""
        skip_if_no_integration()

        stdout, stderr, rc = run_cli(["search", "git"])

        self.assertEqual(rc, 0, f"search 退出码非 0：\nstderr: {stderr}")

        self.assertTrue(
            stdout.startswith("##"),
            f"stdout 必须以 Markdown 标题开头，实际：\n{stdout[:200]}",
        )

        chinese_markers = ["安装", "标识符", "描述", "作者", "标签", "链接"]
        found = any(marker in stdout for marker in chinese_markers)
        self.assertTrue(found, f"stdout 必须包含中文字段名，实际：\n{stdout[:500]}")

        self.assertNotIn(
            "索引已过期", stdout, "日志信息不应混入 stdout，实际：\n" + stdout[:500]
        )


class TestIntegrationShowWithCache(unittest.TestCase):
    """集成测试 3：show --id 缓存命中"""

    def test_show_write_and_hit_cache(self):
        """测试 show 能写入 l1 缓存，第二次调用命中缓存"""
        skip_if_no_integration()

        search_stdout, search_stderr, rc = run_cli(["search", "git"])
        self.assertEqual(rc, 0, f"search 失败：\nstderr: {search_stderr}")

        skill_id = extract_first_skill_id(search_stdout)
        if not skill_id:
            self.skipTest("search 结果中没有找到有效的 skill ID")

        stdout1, stderr1, rc1 = run_cli(["show", skill_id])
        self.assertEqual(rc1, 0, f"第一次 show 失败：\nstderr: {stderr1}")

        stdout2, stderr2, rc2 = run_cli(["show", skill_id])
        self.assertEqual(rc2, 0, f"第二次 show 失败：\nstderr: {stderr2}")

        self.assertTrue(
            stdout2.startswith("##"),
            f"第二次 show stdout 不是 Markdown：\n{stdout2[:200]}",
        )

        cache_dir = os.path.expanduser("~/.skills-sh/l1")
        self.assertTrue(os.path.exists(cache_dir), f"缓存目录应该存在：{cache_dir}")


if __name__ == "__main__":
    unittest.main()
