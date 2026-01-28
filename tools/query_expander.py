# -*- coding: utf-8 -*-
"""Query expander for skill search"""

from typing import Dict, List


DOMAIN_SKILL_TERMS = {
    "frontend": [
        "frontend",
        "frontend-design",
        "frontend-best-practices",
        "react",
        "react-best-practices",
        "ui-design",
        "css",
        "javascript",
        "typescript",
        "component",
        "state-management",
    ],
    "backend": [
        "backend",
        "backend-best-practices",
        "api",
        "api-design",
        "server",
        "database",
        "sql",
        "python",
        "node",
    ],
    "fullstack": [
        "fullstack",
        "fullstack-best-practices",
        "fullstack-patterns",
        "frontend",
        "backend",
    ],
    "video": [
        "video",
        "video-player",
        "streaming",
        "media",
        "video-processing",
        "audio",
        "transcode",
    ],
    "ai": [
        "ai",
        "llm",
        "mcp",
        "agent",
        "agent-skills",
        "machine-learning",
        "model",
        "rag",
        "vector",
    ],
    "database": [
        "database",
        "sql",
        "postgres",
        "mysql",
        "sqlite",
        "orm",
        "query",
        "schema",
        "migration",
    ],
    "devops": [
        "devops",
        "docker",
        "kubernetes",
        "ci-cd",
        "deployment",
        "infrastructure",
        "cloud",
    ],
    "testing": [
        "testing",
        "test",
        "e2e",
        "unit-test",
        "integration",
        "qa",
        "test-automation",
    ],
    "security": [
        "security",
        "auth",
        "authentication",
        "authorization",
        "oauth",
        "encryption",
        "compliance",
    ],
    "mobile": [
        "mobile",
        "ios",
        "android",
        "react-native",
        "flutter",
        "app-development",
    ],
    "general": [
        "best-practices",
        "patterns",
        "guidelines",
        "architecture",
        "design-patterns",
        "code-quality",
    ],
}


def expand_search_terms(
    search_terms: List[str], domain: str = "general"
) -> Dict[str, object]:
    """
    Expand search terms based on domain

    Args:
        search_terms: Original search terms from intent analysis
        domain: Detected technical domain

    Returns:
        Dict with core_terms and extended_terms
    """
    core_terms = list(set(search_terms))

    extended_terms = list(core_terms)

    domain_terms = DOMAIN_SKILL_TERMS.get(domain, DOMAIN_SKILL_TERMS["general"])
    general_terms = DOMAIN_SKILL_TERMS["general"]

    for term in core_terms:
        term_lower = term.lower()

        if term_lower in DOMAIN_SKILL_TERMS:
            extended_terms.extend(DOMAIN_SKILL_TERMS[term_lower])
        else:
            for d, terms in DOMAIN_SKILL_TERMS.items():
                if d != "general":
                    if any(t in term_lower or term_lower in t for t in terms[:5]):
                        extended_terms.extend(terms)
                        break
            else:
                extended_terms.extend(general_terms)

    extended_terms.extend(domain_terms[:3])

    unique_terms = []
    seen = set()
    for term in extended_terms:
        term_lower = term.lower()
        if term_lower not in seen:
            seen.add(term_lower)
            unique_terms.append(term)

    return {
        "core_terms": core_terms,
        "extended_terms": unique_terms[:10],
        "domain": domain,
    }


def create_search_queries(terms: Dict[str, List[str]]) -> List[str]:
    """
    Create multiple search queries from expanded terms

    Args:
        terms: Dict with core_terms and extended_terms

    Returns:
        List of search query strings
    """
    queries = []

    for term in terms.get("core_terms", []):
        if len(term) > 3:
            queries.append(term)

    for term in terms.get("extended_terms", [])[:5]:
        if term not in queries:
            queries.append(term)

    return queries


def prioritize_terms(
    results_count: Dict[str, int], terms: Dict[str, List[str]]
) -> List[str]:
    """
    Prioritize terms based on search results count

    Args:
        results_count: Dict mapping term to result count
        terms: Dict with core_terms and extended_terms

    Returns:
        Prioritized list of terms
    """
    all_terms = terms.get("extended_terms", [])

    scored = []
    for term in all_terms:
        count = results_count.get(term, 0)
        if term in terms.get("core_terms", []):
            score = count * 1.5
        else:
            score = count
        scored.append((score, term))

    scored.sort(key=lambda x: -x[0])

    return [term for _, term in scored]
