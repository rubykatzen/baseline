#!/usr/bin/env python3
import os
import re
import uuid

RELEASE_DESCRIPTION_LIMIT = 3500
MARKDOWN_V2_SPECIAL_CHARACTERS = frozenset("_*[]()~`>#+-=|{}.!\\")
MARKDOWN_LINK = re.compile(r"\[([^]]+)]\([^)]*\)")
MARKDOWN_HEADING = re.compile(r"^(#{1,6})\s+")
MARKDOWN_LIST_ITEM = re.compile(r"^(?:[-+*]|\d+\.)\s+")


def escape_markdown(value):
    return "".join(f"\\{character}" if character in MARKDOWN_V2_SPECIAL_CHARACTERS else character for character in str(value))


def escape_link_url(value):
    return str(value).replace("\\", "\\\\").replace(")", "\\)")


def truncate(value, limit):
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def is_release_heading(value, tag):
    version = re.escape(tag.removeprefix("v"))
    return bool(re.fullmatch(rf"v?{version}(?:\s+\(\d{{4}}-\d{{2}}-\d{{2}}\))?", value))


def release_description(value, tag="", limit=RELEASE_DESCRIPTION_LIMIT):
    lines = []
    for source_line in value.strip().splitlines():
        source_line = source_line.strip()
        if not source_line:
            continue

        heading = bool(MARKDOWN_HEADING.match(source_line))
        line = MARKDOWN_HEADING.sub("", source_line)
        line = MARKDOWN_LIST_ITEM.sub("", line)
        line = MARKDOWN_LINK.sub(r"\1", line)
        if not line or line in ("---", "***"):
            continue
        if heading and not lines and tag and is_release_heading(line, tag):
            continue

        escaped = escape_markdown(line)
        lines.append(f"_{escaped}_" if heading else f"• {escaped}")

    return truncate("\n".join(lines), limit)


def format_published(repository, release):
    tag = release["tag"]
    label = escape_markdown(f"release {tag}")
    link = f"[{label}]({escape_link_url(release['url'])})"
    parts = [f"*{escape_markdown(repository)}*", f"{link} published"]

    name = release.get("name")
    if name and name != tag:
        parts.append(f"*{escape_markdown(name)}*")

    parts.append(escape_markdown(release.get("actor") or "ghost"))
    message = " • ".join(parts)
    if description := release_description(release.get("body") or "", tag=tag):
        message += f"\n{description}"
    return message


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
        "actor": os.environ.get("ACTOR") or "ghost",
    }
    write_output(format_published(os.environ["REPOSITORY"], release))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
