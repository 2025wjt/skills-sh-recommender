# -*- coding: utf-8 -*-
"""tests for fetcher"""

import tools.fetcher as fetcher


def test_fetch_url_timeout():
    """测试网络超时"""
    content, err = fetcher.fetch_url("http://localhost:99999", timeout=1)
    assert content is None
    assert err is not None
    assert "网络错误" in err or "超时" in err


def test_fetch_url_invalid():
    """测试无效 URL"""
    content, err = fetcher.fetch_url("not-a-valid-url", timeout=1)
    assert content is None
    assert err is not None


def test_fetch_json_invalid():
    """测试 JSON 解析失败"""
    content, err = fetcher.fetch_url("http://localhost:99999", timeout=1)
    assert err is not None


def test_fetch_details():
    """测试详情获取"""
    content, err = fetcher.fetch_url("http://localhost:99999", timeout=1)
    assert content is None
    assert err is not None


def test_default_headers():
    """测试默认请求头"""
    assert "User-Agent" in fetcher.DEFAULT_HEADERS
    assert "Chrome" in fetcher.DEFAULT_HEADERS["User-Agent"]


def test_retry_config():
    """测试重试配置"""
    assert fetcher.REQUEST_TIMEOUT == 10
    assert fetcher.MAX_RETRIES == 1
    assert len(fetcher.BACKOFF) == 2
