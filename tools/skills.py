# -*- coding: utf-8 -*-
"""CLI 入口"""

import argparse
import sys
import time
from typing import List

try:
    from .constants import (
        TITLES,
        LABELS,
        MESSAGES,
        DEFAULT_TOP_K,
    )
    from .id_resolver import SkillID
    from .cache import (
        load_l0,
        save_l0,
        is_l0_expired,
        load_l1,
        save_l1,
        search_l0,
        get_l0_by_id,
    )
    from .fetcher import fetch_sitemap, fetch_details
    from .parser import parse_sitemap, parse_skill_details
    from .skill_detector import is_skill_query
    from .smart_search import smart_search
except ImportError:
    from constants import (
        TITLES,
        LABELS,
        MESSAGES,
        DEFAULT_TOP_K,
    )
    from id_resolver import SkillID
    from cache import (
        load_l0,
        save_l0,
        is_l0_expired,
        load_l1,
        save_l1,
        search_l0,
        get_l0_by_id,
    )
    from fetcher import fetch_sitemap, fetch_details
    from parser import parse_sitemap, parse_skill_details
    from skill_detector import is_skill_query
    from smart_search import smart_search


def format_search_results(query: str, results: List[dict]) -> str:
    """Format search results"""
    lines = []
    lines.append(f'## {TITLES["search"]}: "{query}"\n')

    if not results:
        lines.append(MESSAGES["no_results"])
        return "\n".join(lines)

    lines.append(f"Found {len(results)} results:\n")

    for i, rec in enumerate(results, 1):
        title = rec.get("slug") or rec.get("title") or rec.get("id")
        lines.append(f"### {i}. {title}")
        lines.append(f"- **{LABELS['id']}**: `{rec.get('id', '')}`")
        desc = rec.get("description", "")
        if desc:
            lines.append(f"- **{LABELS['description']}**: ")
            lines.append(f"  > {desc}")
        lines.append(f"\n**{LABELS['install']}**:")
        lines.append("```bash")
        lines.append(f"npx skills add {rec.get('id', '')}")
        lines.append("```")
        lines.append(f"\n**{LABELS['install_backup']}**:")
        lines.append("```bash")
        lines.append(f"opencode skill install {rec.get('id', '')}")
        lines.append("```")
        lines.append("")

    lines.append(
        f"\n**{LABELS['count']} {len(results)} {LABELS['results']}**，showing all."
    )
    return "\n".join(lines)


def format_show_result(rec: dict) -> str:
    """Format skill details"""
    lines = []
    lines.append(f"## {TITLES['show']}: {rec.get('id', '')}")
    lines.append("")
    lines.append(f"- **{LABELS['id']}**: `{rec.get('id', '')}`")

    if rec.get("author"):
        lines.append(f"- **{LABELS['author']}**: {rec.get('author')}")

    if rec.get("tags"):
        tags_str = " ".join(f"`{t}`" for t in rec.get("tags", []))
        lines.append(f"- **{LABELS['tags']}**: {tags_str}")

    if rec.get("updated_at"):
        lines.append(f"- **{LABELS['updated_at']}**: {rec.get('updated_at')}")

    if rec.get("url"):
        lines.append(f"- **{LABELS['url']}**: [{rec.get('url')}]({rec.get('url')})")

    lines.append("")
    lines.append(f"### {LABELS['description']}")
    lines.append("")
    desc = rec.get("description", "")
    if desc:
        lines.append(f"> {desc}")
        lines.append("")
        lines.append("（Agent layer is responsible for translating when displaying）")
    else:
        lines.append("_No description_")

    lines.append("")
    lines.append(f"### {LABELS['install']}")
    lines.append("```bash")
    lines.append(f"npx skills add {rec.get('id', '')}")
    lines.append("```")
    lines.append(f"\n**{LABELS['install_backup']}**:")
    lines.append("```bash")
    lines.append(f"opencode skill install {rec.get('id', '')}")
    lines.append("```")

    return "\n".join(lines)


def cmd_search(args):
    """search command with smart detection"""
    query = args.query
    top_k = getattr(args, "top_k", DEFAULT_TOP_K)

    is_triggered, keywords = is_skill_query(query)

    if is_triggered:
        output = smart_search(query, top_k=top_k)
        print(output)
    else:
        if is_l0_expired():
            print(MESSAGES["index_expired"], file=sys.stderr)

        results = search_l0(query, top_k=top_k)
        output = format_search_results(query, results)
        print(output)


def cmd_show(args):
    """show 命令"""
    raw_id = args.id
    try:
        skill_id = SkillID.parse(raw_id)
        cache_key = skill_id.to_cache_key()
    except ValueError as e:
        print(f"## {TITLES['error']}: {e}")
        return

    data = load_l1(cache_key)
    if not data:
        print(MESSAGES["fetching_details"], file=sys.stderr)
        url = skill_id.to_url()
        raw_data, err = fetch_details(url)
        if err:
            print(f"## {TITLES['error']}: {err}")
            return
        raw = raw_data.get("raw", "") if isinstance(raw_data, dict) else raw_data
        detail = parse_skill_details(raw)
        data = {
            "schema_version": 1,
            "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "id": cache_key,
            "url": url,
            **detail,
        }
        save_l1(cache_key, data)

    output = format_show_result(data)
    print(output)


def cmd_update(args):
    """update command"""
    if args.index:
        print(MESSAGES["index_updated"], file=sys.stderr)
        xml, err = fetch_sitemap()
        if err:
            print(
                f"## {TITLES['warning']}: {MESSAGES['index_update_failed']}",
                file=sys.stderr,
            )
            print(f"Error: {err}", file=sys.stderr)
            return

        urls = parse_sitemap(xml)
        records = []
        for url in urls:
            record = {
                "id": SkillID.from_url(url).to_cache_key(),
                "url": url,
                "description": "",
                "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            records.append(record)

        save_l0(records)
        print(f"## {TITLES['update_index']}")
        print(f"\n{MESSAGES['index_updated']}, total {len(records)} skills indexed.")
        print(f"\nLast updated: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

    elif args.id:
        raw_id = args.id
        try:
            skill_id = SkillID.parse(raw_id)
            cache_key = skill_id.to_cache_key()
        except ValueError as e:
            print(f"## {TITLES['error']}: {e}")
            return

        url = skill_id.to_url()
        raw, err = fetch_details(url)
        if err:
            print(f"## {TITLES['error']}: {err}")
            return

        detail = parse_skill_details(raw)
        data = {
            "schema_version": 1,
            "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "id": cache_key,
            "url": url,
            **detail,
        }
        save_l1(cache_key, data)
        print(f"## {TITLES['update_id']}")
        print(f"\n{MESSAGES['cache_refreshed']} {cache_key}.")


def main():
    """CLI entry point"""
    import sys

    if sys.platform == "win32":
        import io

        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace"
        )
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer, encoding="utf-8", errors="replace"
        )

    parser = argparse.ArgumentParser(
        description="skills.sh skill search and management tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_search = subparsers.add_parser("search", help="Search for skills")
    parser_search.add_argument("query", help="Search keyword")
    parser_search.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        help=f"Number of results (default: {DEFAULT_TOP_K})",
    )

    parser_show = subparsers.add_parser("show", help="Show skill details")
    parser_show.add_argument("id", help="Skill ID (owner/repo/skill)")

    parser_update = subparsers.add_parser("update", help="Update cache")
    group = parser_update.add_mutually_exclusive_group(required=True)
    group.add_argument("--index", action="store_true", help="Refresh index")
    group.add_argument("--id", metavar="ID", help="Force refresh a skill detail")

    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(1)

    try:
        if args.command == "search":
            cmd_search(args)
        elif args.command == "show":
            cmd_show(args)
        elif args.command == "update":
            cmd_update(args)
        else:
            parser.print_help()
    except Exception as e:
        print(f"## {TITLES['error']}: {str(e)}", file=sys.stdout)
        sys.exit(1)


if __name__ == "__main__":
    main()
