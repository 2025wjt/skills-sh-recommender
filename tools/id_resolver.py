# -*- coding: utf-8 -*-
"""ID 解析与 URL 构造"""

import re
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

BASE_URL = "https://skills.sh"


@dataclass
class SkillID:
    owner: str
    repo: str
    skill: Optional[str] = None

    @classmethod
    def parse(cls, raw: str) -> "SkillID":
        """解析用户输入为 SkillID

        规则：
        - 3段: owner/repo/skill
        - 2段: owner/repo
        - 1段: owner 或 skill 模糊匹配
        """
        parts = raw.strip().split("/")
        parts = [p for p in parts if p]

        if len(parts) == 3:
            return cls(owner=parts[0], repo=parts[1], skill=parts[2])
        elif len(parts) == 2:
            return cls(owner=parts[0], repo=parts[1], skill=None)
        elif len(parts) == 1:
            return cls(owner=parts[0], repo="", skill=None)
        else:
            raise ValueError(f"无效的 ID 格式: {raw}")

    def to_url(self) -> str:
        """构造 skill 页面 URL"""
        if self.skill:
            return f"{BASE_URL}/{self.owner}/{self.repo}/{self.skill}"
        elif self.repo:
            return f"{BASE_URL}/{self.owner}/{self.repo}"
        else:
            return f"{BASE_URL}/{self.owner}"

    def is_full_id(self) -> bool:
        """是否为完整 ID (owner/repo/skill)"""
        return bool(self.skill)

    def to_cache_key(self) -> str:
        """生成缓存 key"""
        if self.skill:
            return f"{self.owner}/{self.repo}/{self.skill}"
        elif self.repo:
            return f"{self.owner}/{self.repo}"
        else:
            return self.owner

    @staticmethod
    def from_url(url: str) -> "SkillID":
        """从 URL 反解析（用于 sitemap 解析）"""
        pattern = r"skills\.sh/([^/]+)/([^/]+)(?:/([^/]+))?"
        match = re.search(pattern, url)
        if match:
            return SkillID(
                owner=match.group(1), repo=match.group(2), skill=match.group(3)
            )
        raise ValueError(f"无法解析 URL: {url}")

    @staticmethod
    def guess_sitemap_urls() -> list:
        """候选 sitemap 地址"""
        return [
            f"{BASE_URL}/sitemap.xml",
            f"{BASE_URL}/sitemap_index.xml",
            f"{BASE_URL}/sitemap/skills.xml",
        ]
