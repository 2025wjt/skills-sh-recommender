# -*- coding: utf-8 -*-
"""中文常量表"""

TITLES = {
    "search": "🔍 搜索结果",
    "show": "📦 技能详情",
    "update_index": "🔄 索引更新",
    "update_id": "🔄 强制刷新",
    "not_found": "❓ 未找到",
    "warning": "⚠️ 警告",
    "error": "🚫 错误",
}

LABELS = {
    "id": "标识符",
    "author": "作者",
    "tags": "标签",
    "updated_at": "更新时间",
    "url": "链接",
    "description": "描述",
    "install": "安装命令",
    "install_backup": "备用（OpenCode）",
    "count": "共找到",
    "results": "条结果",
}

MESSAGES = {
    "no_results": "未找到相关技能",
    "fetching_details": "正在获取详情...",
    "index_updated": "索引已更新",
    "index_update_failed": "索引更新失败",
    "cache_refreshed": "缓存已刷新",
    "offline_mode": "离线状态，使用已有缓存",
    "id_not_found": "未找到标识符",
    "try_search": "您是否想搜索：",
    "index_expired": "索引已过期，正在后台刷新...",
    "index_refreshed": "索引已后台刷新",
}

CACHE_TTL_DAYS = 7
CACHE_DIR = "~/.skills-sh"
DEFAULT_TOP_K = 5
MAX_WORKERS = None  # 自动计算
REQUEST_TIMEOUT = 10
MAX_RETRIES = 1
BACKOFF = [0.5, 1.5]
