#!/usr/bin/env python3
import os
import re
import uuid

LINKEDIN_POST_LIMIT = 2800
MARKDOWN_HEADING = re.compile(r"^(#{1,6})\s+")
MARKDOWN_LINK = re.compile(r"\[([^]]+)]\([^)]*\)")
MARKDOWN_LIST_ITEM = re.compile(r"^(?:[-+*]|\d+\.)\s+")


def truncate(value, limit):
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


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


def format_published(repository, release, limit=LINKEDIN_POST_LIMIT):
    tag = release["tag"]
    title = f"{repository} {release.get('name') or tag}"
    url = release["url"]
    description = release_description(release.get("body") or "", tag=tag)
    fixed = f"{title}\n\n{url}"
    if not description:
        return truncate(fixed, limit)

    description_limit = limit - len(fixed) - 2
    if description_limit <= 0:
        return truncate(fixed, limit)
    return f"{title}\n\n{truncate(description, description_limit)}\n\n{url}"


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
    write_output(format_published(os.environ["REPOSITORY"], release))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
