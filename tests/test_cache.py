# -*- coding: utf-8 -*-
"""tests for cache"""

import json
import os
import tempfile
import time
from pathlib import Path

# 使用临时目录进行测试
TEMPDIR = tempfile.mkdtemp()

# 重写常量指向临时目录
import tools.cache as cache

cache.CACHE_DIR = TEMPDIR


def test_ensure_cache_dir():
    cache.ensure_cache_dir()
    assert Path(cache.get_cache_dir()).exists()
    assert Path(cache.get_l1_dir()).exists()


def test_save_and_load_l0():
    records = [
        {
            "id": "a/b/c",
            "slug": "c",
            "owner": "a",
            "repo": "b",
            "description": "test",
            "url": "https://skills.sh/a/b/c",
        },
    ]
    cache.save_l0(records)
    loaded = cache.load_l0()
    assert len(loaded) == 1
    assert loaded[0]["id"] == "a/b/c"


def test_search_l0():
    cache.save_l0(
        [
            {
                "id": "owner/repo/skill1",
                "slug": "skill1",
                "owner": "owner",
                "repo": "repo",
                "description": "first skill",
            },
            {
                "id": "owner/repo/skill2",
                "slug": "skill2",
                "owner": "owner",
                "repo": "repo",
                "description": "second skill",
            },
        ]
    )
    results = cache.search_l0("first", top_k=5)
    assert len(results) == 1
    assert results[0]["slug"] == "skill1"


def test_search_l0_partial_match():
    cache.save_l0(
        [
            {
                "id": "a/b/c",
                "slug": "test",
                "owner": "a",
                "repo": "b",
                "description": "test description",
            },
        ]
    )
    results = cache.search_l0("test", top_k=5)
    assert len(results) == 1


def test_save_and_load_l1():
    data = {
        "schema_version": 1,
        "fetched_at": "2026-01-28T12:00:00Z",
        "id": "owner/repo/skill",
        "url": "https://skills.sh/owner/repo/skill",
        "title": "Test Skill",
        "description": "English description",
    }
    cache.save_l1("owner/repo/skill", data)
    loaded = cache.load_l1("owner/repo/skill")
    assert loaded is not None
    assert loaded["title"] == "Test Skill"
    assert loaded["schema_version"] == 1


def test_load_l1_not_exists():
    loaded = cache.load_l1("nonexistent/id")
    assert loaded is None


def test_l1_exists():
    cache.save_l1("test/id", {"test": "data"})
    assert cache.l1_exists("test/id") is True
    assert cache.l1_exists("other/id") is False


def test_is_l0_expired_new():
    path = cache.get_l0_path()
    if path.exists():
        os.remove(path)
    assert cache.is_l0_expired() is True


def test_get_l0_by_id():
    cache.save_l0(
        [
            {
                "id": "owner/repo/skill",
                "slug": "skill",
                "owner": "owner",
                "repo": "repo",
                "description": "desc",
            },
        ]
    )
    rec = cache.get_l0_by_id("owner/repo/skill")
    assert rec is not None
    assert rec["slug"] == "skill"

    rec = cache.get_l0_by_id("nonexistent")
    assert rec is None
