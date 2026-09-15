"""Campaign invariants and isolated scheduled-publication rehearsal."""
import copy
import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

import publish_scheduled_post as publisher

ROOT = Path(__file__).resolve().parent.parent
TYPES = {"editorial_review", "manuscript_preview"}


def entries():
    return [p for p in publisher.load_schedule()["posts"] if p["post_type"] in TYPES
            and ("second-look" in p["slug"] or "draft-preview" in p["slug"])]


class SeriesCampaignTests(unittest.TestCase):
    def test_exact_books_dates_and_unique_destinations(self):
        posts = entries()
        self.assertEqual(len(posts), 15)
        self.assertEqual(len({p["slug"] for p in posts}), 15)
        for prefix, count, start in [
            ("apocalypse-breaker-", 5, date(2026, 9, 21)),
            ("resonance-cycle-", 10, date(2026, 9, 23)),
        ]:
            group = sorted((p for p in posts if p["slug"].startswith(prefix)),
                           key=lambda p: p["publish_date"])
            self.assertEqual(len(group), count)
            for i, p in enumerate(group):
                self.assertTrue(p["slug"].startswith(f"{prefix}{i + 1}-"))
                self.assertEqual(p["publish_date"], (start + timedelta(days=14*i)).isoformat())

    def test_disclosures_sources_and_preview_survive_validation(self):
        for p in entries():
            content, manifest, issues = publisher.validate_entry(p)
            self.assertEqual(issues, [], p["slug"])
            self.assertIn('<p class="text-sm leading-relaxed"><small class="text-sm">', content)
            self.assertIn("fictional", content)
            self.assertIn("publisher-affiliated", content)
            self.assertIn("selected manuscript passages", content)
            self.assertIn("## Sources and scope", content)
            self.assertEqual(len(manifest["source_artifacts"][0]["sha256"]), 64)
            self.assertNotIn("file://", content)
            self.assertNotIn("G:\\", content)
            if p["slug"].startswith("apocalypse-breaker-5-"):
                self.assertEqual(p["post_type"], "manuscript_preview")
                self.assertIn("unfinished", content.lower())
                self.assertIn("preview", content.lower())

    def test_publication_rehearsal_does_not_publish_early_or_twice(self):
        schedule = {"version": 1, "posts": copy.deepcopy(entries())}
        for p in schedule["posts"]:
            p["status"] = "scheduled"
            p.pop("published_at", None)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.object(publisher, "CONTENT_DIR", root / "content"), \
                 patch.object(publisher, "SCHEDULE_FILE", root / "schedule.json"), \
                 patch.object(publisher, "_write_github_output"):
                self.assertIsNone(publisher.publish_due(schedule, "2026-09-20", git_push=False))
                self.assertFalse((root / "content").exists())
                for p in sorted(schedule["posts"], key=lambda x: x["publish_date"]):
                    due = publisher.publish_due(schedule, p["publish_date"], git_push=False)
                    self.assertEqual(due["slug"], p["slug"])
                    output = root / "content" / f'{p["publish_date"]}-{p["slug"]}.md'
                    self.assertEqual(output.read_text(encoding="utf-8"),
                                     (ROOT / "scripts" / p["draft"]).read_text(encoding="utf-8"))
                    self.assertIsNone(publisher.publish_due(schedule, p["publish_date"], git_push=False))
                self.assertEqual(len(list((root / "content").glob("*.md"))), 15)
                persisted = json.loads((root / "schedule.json").read_text(encoding="utf-8"))
                self.assertTrue(all(p["status"] == "published" for p in persisted["posts"]))

    def test_deploy_follows_successful_same_repo_content_job(self):
        workflow = (ROOT / ".github/workflows/deploy.yml").read_text(encoding="utf-8")
        self.assertIn("workflow_run:", workflow)
        self.assertIn('workflows: ["Generate Blog Post"]', workflow)
        self.assertIn("types: [completed]", workflow)
        self.assertIn("branches: [main]", workflow)
        self.assertIn("github.event.workflow_run.conclusion == 'success'", workflow)
        self.assertIn("github.event.workflow_run.head_repository.full_name == github.repository", workflow)


if __name__ == "__main__":
    unittest.main()
