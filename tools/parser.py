# -*- coding: utf-8 -*-
"""HTML/JSON 解析"""

import json
import re
from typing import Any, Dict, List, Optional


def parse_sitemap(xml_content: str) -> List[str]:
    """解析 sitemap XML，提取所有 skill URL"""
    urls = []
    pattern = r"<loc>([^<]+)</loc>"
    for match in re.finditer(pattern, xml_content):
        url = match.group(1).strip()
        if "skills.sh" in url:
            urls.append(url)
    return urls


def parse_next_data(html: str) -> Optional[Dict]:
    """尝试解析 __NEXT_DATA__ JSON"""
    pattern = r'<script[^>]*id="__NEXT_DATA__"[^>]*>([^<]+)</script>'
    match = re.search(pattern, html)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
    return None


def extract_from_next_data(data: Dict) -> Optional[Dict]:
    """从 __NEXT_DATA__ 中提取 skill 信息"""
    try:
        props = data.get("props", {})
        page_props = props.get("pageProps", {})
        for key in ("skill", "data", "result", "skillInfo"):
            if key in page_props:
                return page_props[key]
        return None
    except Exception:
        return None


def extract_meta_content(html: str, property: str) -> Optional[str]:
    """从 meta 标签提取内容"""
    pattern = rf'<meta[^>]*(?:property|name)="{property}"[^>]*content="([^"]*)"'
    match = re.search(pattern, html)
    if match:
        return match.group(1)
    return None


def extract_title(html: str) -> Optional[str]:
    """从 title 标签提取内容"""
    pattern = r"<title>([^<]+)</title>"
    match = re.search(pattern, html)
    if match:
        return match.group(1).strip()
    return None


def parse_skill_from_html(html: str) -> Dict[str, Any]:
    """兜底解析：从 HTML 中提取 skill 信息"""
    result = {
        "title": None,
        "description": None,
        "author": None,
        "tags": [],
    }

    title = extract_meta_content(html, "og:title")
    if not title:
        title = extract_title(html)
    result["title"] = title

    desc = extract_meta_content(html, "og:description")
    if not desc:
        desc = extract_meta_content(html, "description")
    result["description"] = desc

    keywords = extract_meta_content(html, "keywords")
    if keywords:
        result["tags"] = [t.strip() for t in keywords.split(",") if t.strip()]

    return result


def parse_skill_details(raw: str) -> Dict[str, Any]:
    """综合解析 skill 详情"""
    next_data = parse_next_data(raw)
    if next_data:
        data = extract_from_next_data(next_data)
        if data:
            return data

    return parse_skill_from_html(raw)


def build_l0_record(url: str, detail: Optional[Dict] = None) -> Dict:
    """从 URL 构建 l0 记录"""
    try:
        from .id_resolver import SkillID
    except ImportError:
        from id_resolver import SkillID

    skill_id = SkillID.from_url(url)

    record = {
        "id": skill_id.to_cache_key(),
        "owner": skill_id.owner,
        "repo": skill_id.repo,
        "slug": skill_id.skill or "",
        "url": url,
        "description": "",
        "updated_at": "",
    }

    if detail:
        record["title"] = detail.get("title", "")
        record["description"] = detail.get("description", "")
        record["tags"] = detail.get("tags", [])
        record["author"] = detail.get("author", "")

    return record
