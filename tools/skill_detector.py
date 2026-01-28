# -*- coding: utf-8 -*-
"""Skill query trigger detector"""

import re
from typing import Tuple, List


class SkillTriggerDetector:
    """Detects if user is explicitly asking about skills"""

    SKILL_TRIGGERS = [
        "skill",
        "skills",
        "技能",
        "有什么 skill",
        "有什么 skills",
        "有哪些 skill",
        "有哪些 skills",
        "推荐 skill",
        "推荐 skills",
        "推荐一个 skill",
        "查找 skill",
        "搜索 skill",
        "找 skill",
        "帮我找 skill",
        "帮我搜 skill",
        "有没有 skill",
        "有没有 skills",
        "想要 skill",
        "想要 skills",
        "需要 skill",
        "需要 skills",
        "求推荐",
        "求推荐 skill",
        "有什么好的 skill",
    ]

    INQUIRY_PATTERNS = [
        r"什么|哪些|有没有|能否|可以.*吗",
        r"推荐|查找|搜索|找|需要.*skill",
        r"有没有|是否存在|能.*么",
    ]

    def is_skill_query(self, user_input: str) -> Tuple[bool, List[str]]:
        """
        Detect if user is explicitly asking about skills

        Args:
            user_input: The user's input text

        Returns:
            Tuple of (is_skill_query, extracted_keywords)
        """
        input_lower = user_input.lower()

        has_skill_keyword = any(kw.lower() in input_lower for kw in self.SKILL_TRIGGERS)

        is_inquiry = any(re.search(p, input_lower) for p in self.INQUIRY_PATTERNS)

        is_triggered = has_skill_keyword and is_inquiry

        keywords = self._extract_keywords(user_input)

        return is_triggered, keywords

    def _extract_keywords(self, user_input: str) -> List[str]:
        """Extract technical keywords from user input"""
        keywords = []

        words_to_remove = [
            "skill",
            "skills",
            "有什么",
            "有哪些",
            "推荐",
            "查找",
            "搜索",
            "帮我",
            "一个",
            "好的",
            "需要",
            "想要",
            "有没有",
            "求推荐",
            "请问",
            "我想",
            "我要",
        ]

        words = re.split(r"[\s,，、]+", user_input)

        for word in words:
            word_lower = word.lower().strip()
            if word_lower and word_lower not in words_to_remove:
                if len(word_lower) > 1:
                    keywords.append(word)

        return keywords


def is_skill_query(user_input: str) -> Tuple[bool, List[str]]:
    """
    Convenience function to detect skill query

    Args:
        user_input: The user's input text

    Returns:
        Tuple of (is_skill_query, extracted_keywords)
    """
    detector = SkillTriggerDetector()
    return detector.is_skill_query(user_input)
