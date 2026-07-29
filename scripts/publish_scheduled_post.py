#!/usr/bin/env python3
"""Publish due, source-locked editorial posts before the normal generator runs."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from content_guard import FRONTMATTER_RE, validate_generated_content
from site_config import CONFIG


SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
SCHEDULE_FILE = SCRIPT_DIR / "scheduled_posts.json"
CONTENT_DIR = REPO_ROOT / CONFIG["content_dir"]
NUMBER_RE = re.compile(r"(?<![\w])(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?(?![\w])")
MARKDOWN_URL_RE = re.compile(r"\]\([^)]+\)")
SAFE_SLUG_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def load_schedule() -> dict:
    return json.loads(SCHEDULE_FILE.read_text(encoding="utf-8"))


def _script_path(relative_path: str) -> Path:
    path = (SCRIPT_DIR / relative_path).resolve()
    if not path.is_relative_to(SCRIPT_DIR.resolve()):
        raise ValueError(f"scheduled path escapes scripts directory: {relative_path}")
    return path


def _body(content: str) -> str:
    match = FRONTMATTER_RE.search(content)
    return content[match.end() :] if match else content


def validate_scheduled_content(
    content: str,
    entry: dict,
    manifest: dict,
    *,
    content_dir: Path = CONTENT_DIR,
) -> list[str]:
    """Validate editorial structure plus the frozen claim manifest."""

    issues = validate_generated_content(
        content,
        content_dir=content_dir,
        expected_date=entry["publish_date"],
        expected_type=entry["post_type"],
        platform_url=CONFIG["platform_url"],
        allowed_internal_links=CONFIG["allowed_internal_links"],
        allow_sourced_claims=True,
    )
    body = _body(content)
    claim_text = re.sub(r"(?m)^date:\s*.+$", "", content)
    claim_text_without_urls = MARKDOWN_URL_RE.sub("]()", claim_text)
    allowed_numbers = set(manifest.get("allowed_numbers", []))
    unexpected_numbers = sorted(set(NUMBER_RE.findall(claim_text_without_urls)) - allowed_numbers)
    if unexpected_numbers:
        issues.append(
            "numbers absent from the frozen claim manifest: "
            + ", ".join(unexpected_numbers)
        )

    body_lower = body.lower()
    for phrase in manifest.get("required_phrases", []):
        if phrase.lower() not in body_lower:
            issues.append(f"required claim qualifier is missing: {phrase!r}")
    for phrase in manifest.get("forbidden_phrases", []):
        if phrase.lower() in body_lower:
            issues.append(f"forbidden claim language is present: {phrase!r}")
    for link in manifest.get("required_links", []):
        if f"]({link})" not in body:
            issues.append(f"required source link is missing: {link}")

    artifacts = manifest.get("source_artifacts", [])
    if not artifacts:
        issues.append("claim manifest has no source artifacts")
    for artifact in artifacts:
        if not re.fullmatch(r"[A-Fa-f0-9]{64}", artifact.get("sha256", "")):
            issues.append(f"source artifact has an invalid SHA-256: {artifact.get('label')!r}")
    return issues


def select_due_post(schedule: dict, today: str) -> dict | None:
    due = [
        entry
        for entry in schedule.get("posts", [])
        if entry.get("status") == "scheduled" and entry.get("publish_date", "") <= today
    ]
    return min(due, key=lambda entry: (entry["publish_date"], entry["slug"])) if due else None


def validate_entry(entry: dict) -> tuple[str, dict, list[str]]:
    slug = entry.get("slug", "")
    if not SAFE_SLUG_RE.fullmatch(slug):
        return "", {}, [f"invalid slug: {slug!r}"]
    draft_path = _script_path(entry["draft"])
    manifest_path = _script_path(entry["manifest"])
    if not draft_path.exists():
        return "", {}, [f"scheduled draft does not exist: {entry['draft']}"]
    if not manifest_path.exists():
        return "", {}, [f"claim manifest does not exist: {entry['manifest']}"]
    content = draft_path.read_text(encoding="utf-8")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return content, manifest, validate_scheduled_content(content, entry, manifest)


def check_all(schedule: dict) -> list[str]:
    issues: list[str] = []
    for entry in schedule.get("posts", []):
        _, _, entry_issues = validate_entry(entry)
        issues.extend(f"{entry.get('slug', '<missing slug>')}: {issue}" for issue in entry_issues)
    return issues


def _write_github_output(published: bool, slug: str = "") -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return
    with Path(output_path).open("a", encoding="utf-8") as output:
        output.write(f"published={'true' if published else 'false'}\n")
        output.write(f"slug={slug}\n")


def _git_commit_and_push(destination: Path, entry: dict) -> None:
    subprocess.run(
        ["git", "config", "user.name", "github-actions[bot]"],
        check=True,
        cwd=REPO_ROOT,
    )
    subprocess.run(
        ["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"],
        check=True,
        cwd=REPO_ROOT,
    )
    subprocess.run(
        ["git", "add", str(destination), str(SCHEDULE_FILE)],
        check=True,
        cwd=REPO_ROOT,
    )
    subprocess.run(
        ["git", "commit", "-m", f"Publish scheduled research: {entry['slug']}"],
        check=True,
        cwd=REPO_ROOT,
    )
    subprocess.run(["git", "push"], check=True, cwd=REPO_ROOT)


def publish_due(schedule: dict, today: str, *, git_push: bool) -> dict | None:
    entry = select_due_post(schedule, today)
    if not entry:
        _write_github_output(False)
        return None

    content, _, issues = validate_entry(entry)
    if issues:
        raise ValueError("\n".join(issues))

    destination = CONTENT_DIR / f"{entry['publish_date']}-{entry['slug']}.md"
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.read_text(encoding="utf-8") != content:
        raise ValueError(f"destination exists with different content: {destination}")
    destination.write_text(content, encoding="utf-8")

    entry["status"] = "published"
    entry["published_at"] = today
    SCHEDULE_FILE.write_text(json.dumps(schedule, indent=2) + "\n", encoding="utf-8")
    if git_push:
        _git_commit_and_push(destination, entry)
    _write_github_output(True, entry["slug"])
    return entry


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="UTC publication date override (YYYY-MM-DD)")
    parser.add_argument("--check-all", action="store_true")
    parser.add_argument("--git-push", action="store_true")
    args = parser.parse_args()

    schedule = load_schedule()
    if args.check_all:
        issues = check_all(schedule)
        if issues:
            raise SystemExit("\n".join(issues))
        print(f"Validated {len(schedule.get('posts', []))} scheduled posts.")
        return

    today = args.date or datetime.now(timezone.utc).date().isoformat()
    published = publish_due(schedule, today, git_push=args.git_push)
    print(
        f"Published scheduled post: {published['slug']}"
        if published
        else f"No scheduled post due on {today}."
    )


if __name__ == "__main__":
    main()
