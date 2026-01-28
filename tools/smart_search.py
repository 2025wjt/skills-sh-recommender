# -*- coding: utf-8 -*-
"""Smart search orchestrator for skills"""

import json
import sys
from typing import Dict, List, Optional

try:
    from .cache import search_l0, is_l0_expired
    from .skill_detector import is_skill_query
    from .intent_analyzer import analyze_intent
    from .query_expander import expand_search_terms, create_search_queries
    from .result_validator import validate_results
    from .constants import TITLES, LABELS, MESSAGES, DEFAULT_TOP_K
except ImportError:
    from cache import search_l0, is_l0_expired
    from skill_detector import is_skill_query
    from intent_analyzer import analyze_intent
    from query_expander import expand_search_terms, create_search_queries
    from result_validator import validate_results
    from constants import TITLES, LABELS, MESSAGES, DEFAULT_TOP_K


def smart_search(user_query: str, top_k: int = 5) -> str:
    """
    Main smart search orchestration

    Args:
        user_query: The user's input query
        top_k: Maximum number of results to return

    Returns:
        Formatted Markdown output (English, for agent translation)
    """
    lines = []

    lines.append(f'## {TITLES["search"]}: "{user_query}"')
    lines.append("")

    intent = analyze_intent(user_query)

    expanded = expand_search_terms(
        intent.get("search_terms", [user_query]), intent.get("domain", "general")
    )

    queries = create_search_queries(expanded)

    if is_l0_expired():
        print(MESSAGES["index_expired"], file=sys.stderr)

    all_results = []
    results_count = {}

    for query in queries[:5]:
        results = search_l0(query, top_k=top_k)
        results_count[query] = len(results)
        all_results.extend(results)

    valid_results, invalid_results = validate_results(all_results)

    unique_results = _deduplicate_by_id(valid_results)

    ranked_results = _rank_results(unique_results, intent)

    if not ranked_results:
        lines.append(MESSAGES["no_results"])
        lines.append("")
        lines.append(
            f"**Suggestion**: Try searching with different keywords like: {', '.join(expanded.get('core_terms', []))}"
        )
        return "\n".join(lines)

    lines.append(f"Found {len(ranked_results)} related skills:\n")

    for i, rec in enumerate(ranked_results[:top_k], 1):
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
        f"\n**{LABELS['count']} {len(ranked_results)} {LABELS['results']}**，已显示全部。"
    )

    if intent.get("reasoning"):
        lines.append("")
        lines.append(f"**Note**: {intent['reasoning']}")

    return "\n".join(lines)


def _deduplicate_by_id(results: List[Dict]) -> List[Dict]:
    """Remove duplicate results by skill ID"""
    seen = set()
    unique = []
    for rec in results:
        skill_id = rec.get("id", "")
        if skill_id and skill_id not in seen:
            seen.add(skill_id)
            unique.append(rec)
    return unique


def _rank_results(results: List[Dict], intent: Dict) -> List[Dict]:
    """Rank results based on intent and priority"""
    priority_terms = set(t.lower() for t in intent.get("priority_terms", []))
    core_terms = set(t.lower() for t in intent.get("search_terms", []))

    scored = []
    for rec in results:
        score = 0
        text = " ".join(
            [
                rec.get("id", ""),
                rec.get("slug", ""),
                rec.get("description", ""),
            ]
        ).lower()

        for term in priority_terms:
            if term in text:
                score += 10
                if term in rec.get("slug", "").lower():
                    score += 5

        for term in core_terms:
            if term in text:
                score += 3

        scored.append((score, rec))

    scored.sort(key=lambda x: -x[0])

    return [rec for _, rec in scored]


def run_smart_search(args) -> Optional[str]:
    """
    Run smart search from command line arguments

    Args:
        args: Parsed command line arguments

    Returns:
        Formatted output string or None
    """
    user_query = args.query
    top_k = getattr(args, "top_k", DEFAULT_TOP_K)

    is_triggered, keywords = is_skill_query(user_query)

    if not is_triggered:
        return None

    return smart_search(user_query, top_k=top_k)
