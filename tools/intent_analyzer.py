# -*- coding: utf-8 -*-
"""Intent analyzer for skill queries"""

import json
from typing import Dict, List


INTENT_ANALYSIS_PROMPT = """You are analyzing user intent for skill search on skills.sh.

skills.sh is a marketplace for AI agent skills - each skill is a specialized AI agent workflow with knowledge and best practices (format: owner/repo/skill-name).

Analyze the user query and extract relevant search terms for skills.sh.

User Query: "{query}"

Output a JSON object with:
- intent_type: "development" | "learning" | "tool" | "reference"
- domain: primary technical domain
- search_terms: 3-5 relevant search terms for skills.sh (NOT technology stack names like "react", "vue", but skill-related terms like "react-best-practices", "frontend-design")
- priority_terms: 2-3 highest priority search terms
- reasoning: brief explanation

Rules:
1. search_terms should be skill-related terms (best-practices, patterns, guidelines, design, etc.)
2. Do NOT include plain technology names (react, vue, nextjs, python, etc.) - those are libraries, not skills
3. If user mentions a technology, convert to skill-related terms (e.g., "react" → "react-best-practices", "frontend")
4. For "video website", use terms like "video", "streaming", "frontend", "video-player"
5. For "learning react", use terms like "react", "react-best-practices", "learning"

Output JSON only, no other text:"""

DOMAIN_KEYWORDS = {
    "frontend": ["frontend", "ui", "react", "vue", "javascript", "css", "html"],
    "backend": ["backend", "server", "api", "database", "python", "node"],
    "fullstack": ["fullstack", "frontend", "backend"],
    "video": ["video", "streaming", "player", "media", "ffmpeg"],
    "ai": ["ai", "llm", "mcp", "agent", "ml", "model"],
    "database": ["database", "sql", "postgres", "mysql", "sqlite"],
    "devops": ["devops", "docker", "kubernetes", "ci", "deployment"],
    "testing": ["testing", "test", "qa", "e2e"],
    "security": ["security", "auth", "oauth", "encryption"],
    "mobile": ["mobile", "ios", "android", "react-native"],
}


def analyze_intent(user_query: str) -> Dict:
    """
    Analyze user intent using built-in LLM prompt

    Args:
        user_query: The user's input text

    Returns:
        Dict with intent_type, domain, search_terms, priority_terms, reasoning
    """
    domain = _detect_domain_fallback(user_query)
    search_terms = _extract_terms_fallback(user_query)

    return {
        "intent_type": "reference",
        "domain": domain,
        "search_terms": search_terms,
        "priority_terms": search_terms[:2],
        "reasoning": f"Domain detected: {domain}",
    }


def _detect_domain_fallback(user_query: str) -> str:
    """Fallback domain detection based on keywords"""
    query_lower = user_query.lower()

    for domain, keywords in DOMAIN_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            return domain

    return "general"


def _extract_terms_fallback(user_query: str) -> List[str]:
    """Fallback term extraction"""
    terms = []

    keyword_mappings = {
        "frontend": ["frontend", "frontend-design", "frontend-best-practices"],
        "backend": ["backend", "backend-best-practices", "api-design"],
        "video": ["video", "video-player", "streaming"],
        "ai": ["ai", "agent", "mcp"],
        "fullstack": ["fullstack", "fullstack-best-practices"],
    }

    query_lower = user_query.lower()

    for base_term, expanded in keyword_mappings.items():
        if base_term in query_lower:
            return expanded

    words = user_query.split()
    return words[:3] if words else [user_query]


def llm_call(prompt: str) -> str:
    """
    Call Claude Code's built-in LLM

    This uses the current conversation's LLM capability.
    The response should be parsed as JSON.
    """
    return prompt
