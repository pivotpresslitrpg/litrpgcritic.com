import unittest
import sys
from unittest.mock import MagicMock, patch

sys.modules.setdefault("anthropic", MagicMock())
sys.modules.setdefault("requests", MagicMock())

from generate_post import (
    audit_draft_against_sources,
    format_book_list,
    pick_supported_author,
)


class GeneratePostTests(unittest.TestCase):
    def test_book_packet_includes_grounding_fields(self):
        packet = format_book_list([{
            "title": "Verified Book",
            "authors": ["A. Writer"],
            "series_name": "Verified Series",
            "average_rating": 4.5,
            "review_count": 12,
            "genres": ["LitRPG", "Isekai"],
            "published_date": "2026-07-01",
            "description": "A supplied synopsis with a named protagonist.",
        }])
        self.assertIn("Verified Book by A. Writer", packet)
        self.assertIn("genres: LitRPG, Isekai", packet)
        self.assertIn("Description: A supplied synopsis", packet)

    @patch("generate_post._published_entries", return_value=[])
    def test_author_picker_skips_names_without_feed_evidence(self, _entries):
        state = {"author_queue_index": 0}
        author, books = pick_supported_author(
            ["Unsupported Name", "Verified Author"],
            state,
            [{"title": "Book", "authors": ["Verified Author"]}],
        )
        self.assertEqual("Verified Author", author)
        self.assertEqual(1, len(books))
        self.assertEqual(2, state["author_queue_index"])

    @patch("generate_post.call_claude", return_value="PASS")
    def test_source_audit_accepts_explicit_pass(self, _call):
        issue = audit_draft_against_sources(
            "VERIFIED SOURCE PACKET\n- Book by Author",
            "A grounded draft.",
        )
        self.assertIsNone(issue)

    @patch("generate_post.call_claude", return_value="FAIL\n- Wrong protagonist")
    def test_source_audit_blocks_fact_conflict(self, _call):
        issue = audit_draft_against_sources(
            "VERIFIED SOURCE PACKET\n- Book by Author",
            "An ungrounded draft.",
        )
        self.assertIn("Wrong protagonist", issue)


if __name__ == "__main__":
    unittest.main()
