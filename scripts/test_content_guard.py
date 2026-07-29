import tempfile
import unittest
from pathlib import Path

from content_guard import validate_generated_content


class ContentGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.content_dir = Path(self.temp_dir.name)
        (self.content_dir / "what-is-litrpg.md").write_text("---\ntitle: Existing\n---\n")

    def tearDown(self):
        self.temp_dir.cleanup()

    def draft(self, body: str, *, date: str = "2026-07-28", post_type: str = "guide", title: str = "A Useful Guide") -> str:
        return f"""---
title: "{title}"
description: "A specific description for readers."
date: "{date}"
type: "{post_type}"
author: "Editorial"
tags: ["guide"]
featured: false
---

{body}
"""

    def validate(self, content: str) -> list[str]:
        return validate_generated_content(
            content,
            content_dir=self.content_dir,
            expected_date="2026-07-28",
            expected_type="guide",
            platform_url="https://example.com",
            allowed_internal_links={"/blog/", "/new-releases/"},
        )

    def test_accepts_supported_well_formed_draft(self):
        body = (
            "[Example](https://example.com) offers a useful catalog. "
            "[Read more](/blog/what-is-litrpg/). "
            + "Readers can compare clear editorial recommendations. " * 70
        )
        self.assertEqual([], self.validate(self.draft(body)))
    def test_rejects_exact_duplicate_title(self):
        body = "[Example](https://example.com). " + "Useful editorial context. " * 180
        issues = self.validate(self.draft(body, title="Existing"))
        self.assertTrue(any("title duplicates existing post" in issue for issue in issues))

    def test_rejects_near_duplicate_evergreen_title(self):
        (self.content_dir / "dungeon-core.md").write_text(
            "---\ntitle: What Is Dungeon Core Fiction? A Complete Guide\ntype: guide\n---\n"
        )
        body = "[Example](https://example.com). " + "Useful editorial context. " * 180
        issues = self.validate(
            self.draft(body, title="Dungeon Core Fiction: The Complete Reader Guide")
        )
        self.assertTrue(any("title is too similar to existing post" in issue for issue in issues))


    def test_rejects_unsupported_metrics(self):
        body = (
            "[Example](https://example.com) is useful. "
            "According to community data, completion rates are 41% higher. "
            + "Readers can compare clear editorial recommendations. " * 70
        )
        issues = self.validate(self.draft(body))
        self.assertTrue(any("percentage claim" in issue for issue in issues))
        self.assertTrue(any("community-data attribution" in issue for issue in issues))
        self.assertTrue(any("audience-performance metric" in issue for issue in issues))

    def test_rejects_unknown_internal_route(self):
        body = (
            "[Example](https://example.com) is useful. "
            "[Missing](/blog/not-a-real-post/). "
            + "Readers can compare clear editorial recommendations. " * 70
        )
        issues = self.validate(self.draft(body))
        self.assertIn("internal link is not a known route: /blog/not-a-real-post/", issues)

    def test_rejects_wrong_frontmatter_contract(self):
        body = "[Example](https://example.com). " + "Useful editorial context. " * 180
        issues = self.validate(self.draft(body, date="2026-07-27", post_type="news"))
        self.assertTrue(any("frontmatter date" in issue for issue in issues))
        self.assertTrue(any("frontmatter type" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
