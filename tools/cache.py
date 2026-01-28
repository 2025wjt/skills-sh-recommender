# -*- coding: utf-8 -*-
"""缓存读写层"""

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    from .constants import CACHE_DIR, CACHE_TTL_DAYS
except ImportError:
    from constants import CACHE_DIR, CACHE_TTL_DAYS

L0_FILENAME = "l0.jsonl"
L1_DIRNAME = "l1"


def get_cache_dir() -> Path:
    """获取缓存目录"""
    return Path(os.path.expanduser(CACHE_DIR))


def get_l0_path() -> Path:
    """获取 l0 文件路径"""
    return get_cache_dir() / L0_FILENAME


def get_l1_dir() -> Path:
    """获取 l1 目录路径"""
    return get_cache_dir() / L1_DIRNAME


def get_l1_path(skill_id: str) -> Path:
    """获取 l1 缓存文件路径"""
    key = hashlib.sha1(skill_id.encode()).hexdigest()
    dir_path = get_l1_dir() / key[0]
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path / f"{key}.json"


def ensure_cache_dir():
    """确保缓存目录存在"""
    get_cache_dir().mkdir(parents=True, exist_ok=True)
    get_l1_dir().mkdir(parents=True, exist_ok=True)


# === l0 操作 ===


def load_l0() -> List[Dict[str, Any]]:
    """加载 l0 索引"""
    path = get_l0_path()
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def save_l0(records: List[Dict[str, Any]]):
    """保存 l0 索引"""
    ensure_cache_dir()
    path = get_l0_path()
    with open(path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def is_l0_expired() -> bool:
    """检查 l0 是否过期"""
    path = get_l0_path()
    if not path.exists():
        return True
    mtime = path.stat().st_mtime
    age_days = (time.time() - mtime) / 86400
    return age_days > CACHE_TTL_DAYS


def get_l0_expired_at() -> Optional[float]:
    """获取 l0 过期时间戳"""
    path = get_l0_path()
    if not path.exists():
        return None
    mtime = path.stat().st_mtime
    return mtime + CACHE_TTL_DAYS * 86400


# === l1 操作 ===


def load_l1(skill_id: str) -> Optional[Dict[str, Any]]:
    """加载 l1 详情"""
    path = get_l1_path(skill_id)
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_l1(skill_id: str, data: Dict[str, Any]):
    """保存 l1 详情"""
    ensure_cache_dir()
    path = get_l1_path(skill_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def l1_exists(skill_id: str) -> bool:
    """检查 l1 是否存在"""
    return get_l1_path(skill_id).exists()


def list_all_l1_ids() -> List[str]:
    """列出所有 l1 的 ID（用于 l0 损坏恢复）"""
    ids = []
    l1_dir = get_l1_dir()
    if not l1_dir.exists():
        return []
    for hash_dir in l1_dir.iterdir():
        if not hash_dir.is_dir():
            continue
        for f in hash_dir.glob("*.json"):
            ids.append(f.stem)
    return ids


# === 索引搜索 ===


def search_l0(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """在 l0 中全文搜索"""
    records = load_l0()
    query = query.lower()
    scored = []
    for rec in records:
        score = 0
        text = " ".join(
            [
                rec.get("id", ""),
                rec.get("slug", ""),
                rec.get("owner", ""),
                rec.get("repo", ""),
                rec.get("description", ""),
            ]
        ).lower()
        if query in text:
            if rec.get("slug", "").lower() == query:
                score = 100
            elif rec.get("id", "").lower() == query:
                score = 80
            else:
                score = 10
        scored.append((score, rec))

    scored.sort(key=lambda x: -x[0])
    return [rec for sc, rec in scored if sc > 0][:top_k]


def get_l0_by_id(target_id: str) -> Optional[Dict[str, Any]]:
    """根据 ID 精确查找 l0"""
    records = load_l0()
    for rec in records:
        if rec.get("id") == target_id:
            return rec
    return None
