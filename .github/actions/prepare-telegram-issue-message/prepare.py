#!/usr/bin/env python3
import json
import os
import re
import subprocess
import uuid

ISSUE_BODY_LIMIT = 500
MARKDOWN_V2_SPECIAL_CHARACTERS = frozenset("_*[]()~`>#+-=|{}.!\\")


def gh_json(*arguments):
    result = subprocess.run(["gh", *arguments], stdout=subprocess.PIPE, text=True, check=True)
    return json.loads(result.stdout)


def truncate(value, limit):
    value = value.strip()
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def escape_markdown(value):
    return "".join(f"\\{character}" if character in MARKDOWN_V2_SPECIAL_CHARACTERS else character for character in str(value))


def escape_link_url(value):
    return str(value).replace("\\", "\\\\").replace(")", "\\)")


def body_excerpt(value, limit=ISSUE_BODY_LIMIT):
    lines = value.strip().splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        return ""

    heading = re.fullmatch(r"\s{0,3}#{1,6}\s+(.+?)\s*#*\s*", lines[0])
    if heading:
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines.pop(0)
        paragraph = []
        for line in lines:
            if not line.strip():
                break
            paragraph.append(line.strip())
        parts = [heading.group(1), " ".join(paragraph)]
        return truncate("\n".join(part for part in parts if part), limit)

    paragraph = []
    for line in lines:
        if not line.strip():
            break
        paragraph.append(line.strip())
    return truncate(" ".join(paragraph), limit)


def format_closed(repository, issue, actor):
    label = escape_markdown(f"issue {issue['number']}")
    link = f"[{label}]({escape_link_url(issue['url'])})"
    parts = [
        f"*{escape_markdown(repository)}*",
        f"{link} closed",
        f"*{escape_markdown(issue['title'])}*",
        escape_markdown(actor),
    ]
    message = " • ".join(parts)
    if excerpt := body_excerpt(issue.get("body") or ""):
        message += f"\n{escape_markdown(excerpt)}"
    return message


def write_output(message):
    delimiter = f"ghdelim_{uuid.uuid4().hex}"
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        print(f"message<<{delimiter}", file=output)
        print(message, file=output)
        print(delimiter, file=output)


def main():
    repository = os.environ["REPOSITORY"]
    number = os.environ["NUMBER"]
    actor = os.environ["ACTOR"]
    issue = gh_json(
        "issue",
        "view",
        number,
        "--repo",
        repository,
        "--json",
        "number,title,url,body",
    )
    write_output(format_closed(repository, issue, actor))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
