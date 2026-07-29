"""Pre-publish validation for generated editorial content."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit


FRONTMATTER_RE = re.compile(
    r"\A---\s*\r?\n(?P<frontmatter>.*?)\r?\n---\s*(?:\r?\n|$)",
    re.DOTALL,
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
WORD_RE = re.compile(r"\b[\w'-]+\b")

UNSUPPORTED_CLAIM_PATTERNS = (
    (
        "percentage claim",
        re.compile(r"\b\d+(?:\.\d+)?\s*%", re.IGNORECASE),
    ),
    (
        "untraceable community-data attribution",
        re.compile(r"\baccording to community data\b", re.IGNORECASE),
    ),
    (
        "untraceable corpus-analysis attribution",
        re.compile(r"\bbased on (?:our|an?) analysis of\b", re.IGNORECASE),
    ),
    (
        "unsupported audience-performance metric",
        re.compile(
            r"\b(?:completion|engagement|retention|conversion|click-through)\s+"
            r"(?:rate|rates|score|scores|data|metric|metrics|thread|threads)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "unsupported comparative metric",
        re.compile(
            r"\b\d+(?:\.\d+)?(?:x| times)?\s+(?:higher|lower|more|less)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "unsupported large-corpus claim",
        re.compile(
            r"\b\d[\d,]*\+\s+(?:titles|books|readers|users|ratings|reviews|"
            r"interactions|views|copies|sales)\b",
            re.IGNORECASE,
        ),
    ),
)


def _frontmatter(content: str) -> tuple[str, str] | None:
    match = FRONTMATTER_RE.search(content)
    if not match:
        return None
    return match.group("frontmatter"), content[match.end() :]


def _field(frontmatter: str, name: str) -> str | None:
    match = re.search(
        rf"^{re.escape(name)}:\s*(?P<value>.+?)\s*$",
        frontmatter,
        re.MULTILINE,
    )
    if not match:
        return None
    return match.group("value").strip().strip("\"'")


def _existing_content_slugs(content_dir: Path) -> set[str]:
    if not content_dir.exists():
        return set()
    return {path.stem for path in content_dir.glob("*.md")}


def _internal_links(content: str) -> set[str]:
    links: set[str] = set()
    for target in MARKDOWN_LINK_RE.findall(content):
        target = target.strip()
        if not target.startswith("/"):
            continue
        links.add(urlsplit(target).path)
    return links


def validate_generated_content(
    content: str,
    *,
    content_dir: Path,
    expected_date: str,
    expected_type: str,
    platform_url: str,
    allowed_internal_links: set[str] | frozenset[str] | tuple[str, ...],
    allow_sourced_claims: bool = False,
) -> list[str]:
    """Return blocking issues. An empty list means the draft may be written."""

    issues: list[str] = []
    parsed = _frontmatter(content)
    if not parsed:
        return ["missing or malformed YAML frontmatter"]

    frontmatter, body = parsed
    title = _field(frontmatter, "title")
    description = _field(frontmatter, "description")
    date = _field(frontmatter, "date")
    post_type = _field(frontmatter, "type")

    if not title or title.lower() == "post":
        issues.append("frontmatter title is missing or still a placeholder")
    if not description or description.lower() == "generated post":
        issues.append("frontmatter description is missing or still a placeholder")
    if date != expected_date:
        issues.append(f"frontmatter date must be {expected_date}, got {date!r}")
    if post_type != expected_type:
        issues.append(f"frontmatter type must be {expected_type!r}, got {post_type!r}")

    word_count = len(WORD_RE.findall(body))
    if word_count < 350:
        issues.append(f"body is too short ({word_count} words; minimum 350)")
    if word_count > 1_600:
        issues.append(f"body is too long ({word_count} words; maximum 1600)")
    if re.search(r"(?m)^#\s+", body):
        issues.append("body contains an H1; the title must come from frontmatter")
    if "```" in body:
        issues.append("body contains a fenced code block")
    if re.search(r"\[(?:x|insert|title|book|author)\]", body, re.IGNORECASE):
        issues.append("body contains an unresolved placeholder")

    platform_link_pattern = re.compile(
        rf"\[[^\]]+\]\({re.escape(platform_url.rstrip('/'))}/?\)",
        re.IGNORECASE,
    )
    if not platform_link_pattern.search(body):
        issues.append(f"body must contain a markdown link to {platform_url}")

    claim_patterns = () if allow_sourced_claims else UNSUPPORTED_CLAIM_PATTERNS
    for label, pattern in claim_patterns:
        match = pattern.search(body)
        if match:
            excerpt = re.sub(r"\s+", " ", body[max(0, match.start() - 45) : match.end() + 65])
            issues.append(f"{label}: …{excerpt.strip()}…")

    allowed = {urlsplit(path).path for path in allowed_internal_links}
    existing_slugs = _existing_content_slugs(content_dir)
    for path in sorted(_internal_links(body)):
        if path in allowed:
            continue
        blog_match = re.fullmatch(r"/blog/(?P<slug>[^/]+)/", path)
        if blog_match and blog_match.group("slug") in existing_slugs:
            continue
        issues.append(f"internal link is not a known route: {path}")

    return issues


def retry_guidance(issues: list[str]) -> str:
    bullets = "\n".join(f"- {issue}" for issue in issues)
    return (
        "\n\nThe previous draft failed the pre-publish quality gate. Rewrite the "
        "entire article and correct every issue below. Do not discuss the gate in "
        f"the article.\n{bullets}"
    )
