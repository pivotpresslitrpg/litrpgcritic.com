import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import publish_scheduled_post as scheduler
from publish_scheduled_post import (
    check_all,
    load_schedule,
    select_due_post,
    validate_entry,
)


class ScheduledPostTests(unittest.TestCase):
    def test_all_scheduled_drafts_pass_claim_and_content_guards(self):
        self.assertEqual(check_all(load_schedule()), [])

    def test_due_selection_uses_earliest_scheduled_post(self):
        schedule = {
            "posts": [
                {"publish_date": "2026-08-10", "slug": "later", "status": "scheduled"},
                {"publish_date": "2026-08-03", "slug": "first", "status": "scheduled"},
                {"publish_date": "2026-08-01", "slug": "done", "status": "published"},
            ]
        }
        first = select_due_post(schedule, "2026-08-03")
        self.assertIsNotNone(first)
        self.assertEqual(first["publish_date"], "2026-08-03")
        self.assertIsNone(select_due_post(schedule, "2026-08-02"))

    def test_unmanifested_number_is_blocked(self):
        entry = load_schedule()["posts"][0]
        content, manifest, issues = validate_entry(entry)
        self.assertEqual(issues, [])
        from publish_scheduled_post import validate_scheduled_content

        issues = validate_scheduled_content(
            content + "\nAn unsupported figure: 999.\n",
            entry,
            manifest,
        )
        self.assertTrue(any("999" in issue for issue in issues))

    def test_publish_due_writes_content_and_advances_state(self):
        schedule = copy.deepcopy(load_schedule())
        first = schedule["posts"][0]
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            temp_schedule = temp_root / "scheduled_posts.json"
            temp_content = temp_root / "content"
            temp_schedule.write_text(json.dumps(schedule), encoding="utf-8")
            with (
                patch.object(scheduler, "SCHEDULE_FILE", temp_schedule),
                patch.object(scheduler, "CONTENT_DIR", temp_content),
                patch.dict(scheduler.os.environ, {"GITHUB_OUTPUT": ""}),
            ):
                published = scheduler.publish_due(
                    schedule,
                    first["publish_date"],
                    git_push=False,
                )

            self.assertEqual(published["slug"], first["slug"])
            destination = temp_content / f"{first['publish_date']}-{first['slug']}.md"
            self.assertTrue(destination.exists())
            persisted = json.loads(temp_schedule.read_text(encoding="utf-8"))
            self.assertEqual(persisted["posts"][0]["status"], "published")


if __name__ == "__main__":
    unittest.main()
