# -*- coding: utf-8 -*-
"""tests for id_resolver"""

import pytest
from tools.id_resolver import SkillID


def test_parse_full_id():
    sid = SkillID.parse("owner/repo/skill")
    assert sid.owner == "owner"
    assert sid.repo == "repo"
    assert sid.skill == "skill"
    assert sid.to_url() == "https://skills.sh/owner/repo/skill"


def test_parse_partial_id_two_parts():
    sid = SkillID.parse("owner/repo")
    assert sid.owner == "owner"
    assert sid.repo == "repo"
    assert sid.skill is None
    assert sid.to_url() == "https://skills.sh/owner/repo"


def test_parse_partial_id_one_part():
    sid = SkillID.parse("owner")
    assert sid.owner == "owner"
    assert sid.repo == ""
    assert sid.skill is None


def test_cache_key_full():
    sid = SkillID.parse("owner/repo/skill")
    assert sid.to_cache_key() == "owner/repo/skill"


def test_cache_key_partial():
    sid = SkillID.parse("owner/repo")
    assert sid.to_cache_key() == "owner/repo"


def test_is_full_id():
    assert SkillID.parse("owner/repo/skill").is_full_id() is True
    assert SkillID.parse("owner/repo").is_full_id() is False


def test_from_url():
    sid = SkillID.from_url("https://skills.sh/owner/repo/skill")
    assert sid.owner == "owner"
    assert sid.repo == "repo"
    assert sid.skill == "skill"


def test_guess_sitemap_urls():
    urls = SkillID.guess_sitemap_urls()
    assert len(urls) == 3
    assert all("skills.sh" in u for u in urls)
    assert "sitemap.xml" in urls[0]


def test_parse_invalid_empty():
    with pytest.raises(ValueError):
        SkillID.parse("")
