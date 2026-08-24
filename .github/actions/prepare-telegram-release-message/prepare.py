#!/usr/bin/env python3
import os
import re
import uuid

RELEASE_DESCRIPTION_LIMIT = 3500
MARKDOWN_V2_SPECIAL_CHARACTERS = frozenset("_*[]()~`>#+-=|{}.!\\")
MARKDOWN_LINK = re.compile(r"\[([^]]+)]\([^)]*\)")


def escape_markdown(value):
    return "".join(f"\\{character}" if character in MARKDOWN_V2_SPECIAL_CHARACTERS else character for character in str(value))


def escape_link_url(value):
    return str(value).replace("\\", "\\\\").replace(")", "\\)")


def truncate(value, limit):
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def release_description(value, limit=RELEASE_DESCRIPTION_LIMIT):
    lines = []
    for source_line in value.strip().splitlines():
        line = re.sub(r"^#{1,6}\s+", "", source_line.strip())
        line = re.sub(r"^(?:[-+*]|\d+\.)\s+", "", line)
        line = MARKDOWN_LINK.sub(r"\1", line)
        if line or (lines and lines[-1]):
            lines.append(line)

    return truncate("\n".join(lines).strip(), limit)


def format_published(repository, release):
    tag = release["tag"]
    label = escape_markdown(f"release {tag}")
    link = f"[{label}]({escape_link_url(release['url'])})"
    parts = [f"*{escape_markdown(repository)}*", f"{link} published"]

    name = release.get("name")
    if name and name != tag:
        parts.append(f"*{escape_markdown(name)}*")

    parts.append(escape_markdown(release.get("actor") or "ghost"))
    message = " · ".join(parts)
    if description := release_description(release.get("body") or ""):
        message += f"\n{escape_markdown(description)}"
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
