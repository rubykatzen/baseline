#!/usr/bin/env python3
import json
import os
import re
import uuid

LINKEDIN_POST_LIMIT = 2800
MARKDOWN_HEADING = re.compile(r"^(#{1,6})\s+")
MARKDOWN_LINK = re.compile(r"\[([^]]+)]\([^)]*\)")
MARKDOWN_LIST_ITEM = re.compile(r"^(?:[-+*]|\d+\.)\s+")
LITTLE_RESERVED = frozenset("|{}@[]()<>#\\*_~")


def truncate(value, limit):
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def escape_little_text(value):
    return "".join(f"\\{character}" if character in LITTLE_RESERVED else character for character in value)


def truncate_little_text(value, limit):
    escaped = escape_little_text(value)
    if len(escaped) <= limit:
        return escaped

    available = limit - 3
    result = []
    length = 0
    for character in value:
        token = f"\\{character}" if character in LITTLE_RESERVED else character
        if length + len(token) > available:
            break
        result.append(token)
        length += len(token)
    return "".join(result).rstrip() + "..."


def is_release_heading(value, tag):
    version = re.escape(tag.removeprefix("v"))
    return bool(re.fullmatch(rf"v?{version}(?:\s+\(\d{{4}}-\d{{2}}-\d{{2}}\))?", value))


def release_description(value, tag=""):
    lines = []
    for source_line in value.strip().splitlines():
        source_line = source_line.strip()
        if not source_line:
            if lines and lines[-1]:
                lines.append("")
            continue

        heading = bool(MARKDOWN_HEADING.match(source_line))
        list_item = bool(MARKDOWN_LIST_ITEM.match(source_line))
        line = MARKDOWN_HEADING.sub("", source_line)
        line = MARKDOWN_LIST_ITEM.sub("", line)
        line = MARKDOWN_LINK.sub(r"\1", line)
        if not line or line in ("---", "***"):
            continue
        if heading and not any(lines) and tag and is_release_heading(line, tag):
            continue

        lines.append(f"• {line}" if list_item else line)

    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def format_hashtags(topics):
    hashtags = []
    for topic in topics:
        name = "".join(word.capitalize() for word in re.findall(r"[A-Za-z0-9]+", topic))
        hashtag = f"#{name}" if name else ""
        if hashtag and hashtag not in hashtags:
            hashtags.append(hashtag)
    return " ".join(hashtags)


def format_published(repository, release, repository_description="", topics=None, limit=LINKEDIN_POST_LIMIT):
    tag = release["tag"]
    header = escape_little_text(f"{repository} {release.get('name') or tag}")
    footer = escape_little_text(release["url"])
    hashtags = format_hashtags(topics or [])
    if repository_description:
        header = f"{header}\n\n{escape_little_text(repository_description)}"
    if hashtags:
        footer = f"{footer}\n\n{hashtags}"

    description = release_description(release.get("body") or "", tag=tag)
    fixed = f"{header}\n\n{footer}"
    if not description:
        return truncate(fixed, limit)

    description_limit = limit - len(fixed) - 2
    if description_limit <= 0:
        return truncate(fixed, limit)
    return f"{header}\n\n{truncate_little_text(description, description_limit)}\n\n{footer}"


def write_output(message):
    delimiter = f"ghdelim_{uuid.uuid4().hex}"
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        print(f"message<<{delimiter}", file=output)
        print(message, file=output)
        print(delimiter, file=output)


def main():
    release = {
        "tag": os.environ["TAG_NAME"],
        "name": os.environ.get("RELEASE_NAME") or "",
        "url": os.environ["RELEASE_URL"],
        "body": os.environ.get("RELEASE_BODY") or "",
    }
    topics = json.loads(os.environ.get("REPOSITORY_TOPICS") or "[]")
    if topics is None:
        topics = []
    if not isinstance(topics, list) or not all(isinstance(topic, str) for topic in topics):
        raise ValueError("repository topics must be a JSON array of strings")
    write_output(
        format_published(
            os.environ["REPOSITORY"],
            release,
            repository_description=os.environ.get("REPOSITORY_DESCRIPTION") or "",
            topics=topics,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
