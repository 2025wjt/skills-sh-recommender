# -*- coding: utf-8 -*-
"""网络请求与重试"""

import json
import time
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

try:
    from .constants import (
        REQUEST_TIMEOUT,
        MAX_RETRIES,
        BACKOFF,
    )
except ImportError:
    from constants import (
        REQUEST_TIMEOUT,
        MAX_RETRIES,
        BACKOFF,
    )

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}


def fetch_url(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = REQUEST_TIMEOUT,
    max_retries: int = MAX_RETRIES,
    backoff: List[float] = BACKOFF,
) -> Tuple[Optional[str], Optional[str]]:
    """
    获取 URL 内容

    Returns:
        (content, error_msg)
    """
    req_headers = {**DEFAULT_HEADERS, **(headers or {})}

    for attempt in range(max_retries + 1):
        try:
            req = urllib.request.Request(url, headers=req_headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                content = resp.read().decode("utf-8")
                return content, None
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                wait_time = backoff[min(attempt, len(backoff) - 1)]
                time.sleep(wait_time)
                continue
            return None, f"HTTP {e.code}: {e.reason}"
        except urllib.error.URLError as e:
            if attempt < max_retries:
                wait_time = backoff[min(attempt, len(backoff) - 1)]
                time.sleep(wait_time)
                continue
            return None, f"网络错误: {e.reason}"
        except Exception as e:
            return None, f"未知错误: {str(e)}"

    return None, "超出重试次数"


def fetch_json(url: str) -> Tuple[Optional[Dict], Optional[str]]:
    """获取 JSON 内容"""
    content, err = fetch_url(url)
    if err:
        return None, err
    try:
        data = json.loads(content)
        return data, None
    except json.JSONDecodeError as e:
        return None, f"JSON 解析错误: {e}"


def fetch_sitemap() -> Tuple[Optional[str], Optional[str]]:
    """获取 sitemap（尝试多个候选地址）"""
    try:
        from .id_resolver import SkillID
    except ImportError:
        from id_resolver import SkillID

    urls = SkillID.guess_sitemap_urls()
    for url in urls:
        content, err = fetch_url(url)
        if err:
            continue
        if content and content.strip().startswith("<?xml"):
            return content, None
        try:
            if content:
                data = json.loads(content)
                return json.dumps(data), None
        except json.JSONDecodeError:
            continue
    return None, "无法获取 sitemap"


def fetch_details(url: str) -> Tuple[Optional[Dict], Optional[str]]:
    """获取 skill 详情页"""
    content, err = fetch_url(url)
    if err:
        return None, err
    return {"raw": content}, None
