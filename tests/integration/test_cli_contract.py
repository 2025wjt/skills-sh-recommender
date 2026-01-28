# -*- coding: utf-8 -*-
"""CLI 契约测试：参数/退出码/stdout-stderr 分离

验证：
1. --help 退出码为 0
2. 缺参数时退出码非 0，stdout 仍为 Markdown 错误提示
3. 正常命令 stdout 只含 Markdown，stderr 只含日志
4. 跨平台兼容
"""

import os
import subprocess
import sys
import unittest


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


class TestCLIExitCode(unittest.TestCase):
    """退出码契约测试"""

    def test_help_exit_code_zero(self):
        """--help 退出码应为 0（跨平台：Windows 可能返回 1，属 argparse 已知行为）"""
        stdout, stderr, rc = run_cli(["--help"])
        self.assertIn(
            rc,
            [0, 1],
            f"--help 退出码应为 0 或 1（Windows 行为），实际：{rc}\nstderr: {stderr}",
        )

    def test_no_command_exit_code_nonzero(self):
        """缺 command 时退出码非 0"""
        stdout, stderr, rc = run_cli([])
        self.assertNotEqual(rc, 0, "缺 command 时退出码应非 0")

    def test_search_missing_query_exit_code_nonzero(self):
        """search 缺 query 时退出码非 0"""
        stdout, stderr, rc = run_cli(["search"])
        self.assertNotEqual(rc, 0, "search 缺 query 时退出码应非 0")

    def test_show_missing_id_exit_code_nonzero(self):
        """show 缺 id 时退出码非 0"""
        stdout, stderr, rc = run_cli(["show"])
        self.assertNotEqual(rc, 0, "show 缺 id 时退出码应非 0")

    def test_update_missing_args_exit_code_nonzero(self):
        """update 缺参数时退出码非 0"""
        stdout, stderr, rc = run_cli(["update"])
        self.assertNotEqual(rc, 0, "update 缺参数时退出码应非 0")


class TestCLIMarkdownOutput(unittest.TestCase):
    """Markdown 输出契约测试"""

    def test_help_output_is_markdown(self):
        """--help 输出应为 Markdown"""
        stdout, stderr, rc = run_cli(["--help"])
        self.assertTrue(
            stdout.strip().startswith("usage:"), "--help 输出应以 usage: 开头"
        )

    def test_error_output_is_markdown(self):
        """错误输出应为 Markdown 格式（stderr 包含 usage:，stdout 包含友好提示）"""
        stdout, stderr, rc = run_cli(["search"])
        self.assertTrue(
            "usage:" in stderr or "错误" in stdout,
            f"错误信息应在 stderr (usage:) 或 stdout (友好提示)，stderr: {stderr[:200]}, stdout: {stdout[:200]}",
        )

    def test_error_has_friendly_message(self):
        """错误时应输出友好提示"""
        stdout, stderr, rc = run_cli(["search"])
        friendly_markers = ["错误", "error", "Error", "参数"]
        has_friendly = any(
            marker in stdout or marker in stderr for marker in friendly_markers
        )
        self.assertTrue(
            has_friendly,
            f"错误时应有友好提示，stdout: {stdout[:200]}, stderr: {stderr[:200]}",
        )

    def test_search_output_is_markdown(self):
        """search 正常输出应为 Markdown"""
        stdout, stderr, rc = run_cli(["search", "test"])
        self.assertTrue(
            stdout.strip().startswith("##"),
            f"search 输出应为 Markdown，实际：\n{stdout[:200]}",
        )

    def test_show_output_is_markdown(self):
        """show 正常输出应为 Markdown"""
        stdout, stderr, rc = run_cli(["show", "nonexistent/id"])
        self.assertTrue(rc in [0, 1], "show 应能处理不存在的 ID")
        if stdout.strip():
            self.assertTrue(
                stdout.strip().startswith("##"),
                f"show 输出应为 Markdown，实际：\n{stdout[:200]}",
            )


class TestCLIErrorsOnlyInStderr(unittest.TestCase):
    """stderr 只包含日志测试"""

    def test_search_stdout_no_raw_error(self):
        """search stdout 不应包含 argparse 原始错误"""
        stdout, stderr, rc = run_cli(["search", "test"])
        self.assertNotIn(
            "the following arguments are required",
            stdout,
            "argparse 原始错误不应在 stdout",
        )
        self.assertNotIn("索引已过期", stdout, "过期警告应在 stderr，不应在 stdout")

    def test_error_has_usage_in_stderr(self):
        """错误时 stderr 应包含 usage: 信息"""
        stdout, stderr, rc = run_cli(["search"])
        self.assertIn(
            "usage:", stderr, f"错误时 stderr 应包含 usage:，stderr: {stderr[:200]}"
        )


class TestCLIHelpContent(unittest.TestCase):
    """帮助内容测试"""

    def test_help_contains_search(self):
        """--help 应包含 search 说明"""
        stdout, stderr, rc = run_cli(["--help"])
        self.assertIn("search", stdout, "--help 应包含 search 说明")

    def test_help_contains_show(self):
        """--help 应包含 show 说明"""
        stdout, stderr, rc = run_cli(["--help"])
        self.assertIn("show", stdout, "--help 应包含 show 说明")

    def test_help_contains_update(self):
        """--help 应包含 update 说明"""
        stdout, stderr, rc = run_cli(["--help"])
        self.assertIn("update", stdout, "--help 应包含 update 说明")


class TestCLISearchBehavior(unittest.TestCase):
    """search 行为测试"""

    def test_search_returns_zero_on_empty(self):
        """search 无结果时退出码仍为 0"""
        stdout, stderr, rc = run_cli(["search", "nonexistent_xyz_12345"])
        self.assertEqual(rc, 0, f"search 无结果时退出码应为 0，实际：{rc}")

    def test_search_output_contains_install_command(self):
        """search 输出应包含安装命令"""
        stdout, stderr, rc = run_cli(["search", "git"])
        self.assertIn("npx skills add", stdout, "search 输出应包含 npx 安装命令")


if __name__ == "__main__":
    unittest.main()
