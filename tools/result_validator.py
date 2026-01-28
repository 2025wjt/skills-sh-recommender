# -*- coding: utf-8 -*-
"""Skill result validator"""

import re
from typing import Dict, List, Tuple


class SkillValidator:
    """Validates if a skill is from skills.sh and has valid format"""

    VALID_SKILL_PATTERN = re.compile(r"^[\w-]+/[\w-]+/[\w-]+$")

    INVALID_PATTERNS = [
        r"^facebook/react$",
        r"^vuejs/vue$",
        r"^angular/angular$",
        r"^nodejs/node$",
        r"^docker/docker$",
        r"^kubernetes/kubernetes$",
        r"^ffmpeg$",
        r"^ffmpeg/ffmpeg$",
        r"^axios$",
        r"^lodash$",
        r"^express$",
        r"^expressjs/express$",
    ]

    INVALID_PATTERN_COMPILED = [re.compile(p) for p in INVALID_PATTERNS]

    SKILLS_SH_BASE_URL = "https://skills.sh"

    def validate(self, skill_id: str, skill_url: str) -> Dict:
        """
        Validate a single skill

        Args:
            skill_id: The skill ID (owner/repo/skill)
            skill_url: The skill URL

        Returns:
            Dict with is_valid and reason
        """
        result = {
            "is_valid": True,
            "reason": "success",
            "skill_id": skill_id,
            "skill_url": skill_url,
        }

        if not skill_id or not skill_url:
            result["is_valid"] = False
            result["reason"] = "Missing ID or URL"
            return result

        if not self.VALID_SKILL_PATTERN.match(skill_id):
            result["is_valid"] = False
            result["reason"] = "Invalid skill ID format"
            return result

        if not self._validate_url(skill_url):
            result["is_valid"] = False
            result["reason"] = "Invalid URL format"
            return result

        if self._is_known_invalid(skill_id):
            result["is_valid"] = False
            result["reason"] = "Known invalid skill (not a skills.sh skill)"
            return result

        return result

    def _validate_url(self, url: str) -> bool:
        """Validate that URL points to skills.sh"""
        if not url:
            return False
        return "skills.sh" in url and url.startswith(self.SKILLS_SH_BASE_URL)

    def _is_known_invalid(self, skill_id: str) -> bool:
        """Check if skill ID is a known invalid pattern"""
        for pattern in self.INVALID_PATTERN_COMPILED:
            if pattern.match(skill_id):
                return True
        return False

    def validate_results(self, results: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """
        Validate a list of search results

        Args:
            results: List of search result dicts

        Returns:
            Tuple of (valid_results, invalid_results)
        """
        valid_results = []
        invalid_results = []

        for result in results:
            skill_id = result.get("id", "")
            skill_url = result.get("url", "")

            validation = self.validate(skill_id, skill_url)

            if validation["is_valid"]:
                valid_results.append(
                    {**result, "validation_reason": validation["reason"]}
                )
            else:
                invalid_results.append(
                    {**result, "validation_reason": validation["reason"]}
                )

        return valid_results, invalid_results


def validate_skill(skill_id: str, skill_url: str) -> Dict:
    """
    Convenience function to validate a skill

    Args:
        skill_id: The skill ID
        skill_url: The skill URL

    Returns:
        Validation result dict
    """
    validator = SkillValidator()
    return validator.validate(skill_id, skill_url)


def validate_results(results: List[Dict]) -> List[Dict]:
    """
    Convenience function to validate results

    Args:
        results: List of search result dicts

    Returns:
        List of valid results
    """
    validator = SkillValidator()
    valid_results, _ = validator.validate_results(results)
    return valid_results
