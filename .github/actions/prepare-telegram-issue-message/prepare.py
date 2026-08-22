#!/usr/bin/env python3
import json
import os
import subprocess
import uuid

ISSUE_BODY_LIMIT = 500
MARKDOWN_V2_SPECIAL_CHARACTERS = frozenset("_*[]()~`>#+-=|{}.!\\")


def gh_json(*arguments):
    result = subprocess.run(["gh", *arguments], stdout=subprocess.PIPE, text=True, check=True)
    return json.loads(result.stdout)


def truncate(value, limit):
    value = " ".join(value.split())
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def escape_markdown(value):
    return "".join(f"\\{character}" if character in MARKDOWN_V2_SPECIAL_CHARACTERS else character for character in str(value))


def escape_link_url(value):
    return str(value).replace("\\", "\\\\").replace(")", "\\)")


def format_closed(repository, issue, actor):
    number = escape_markdown(f"#{issue['number']}")
    link = f"[{number}]({escape_link_url(issue['url'])})"
    parts = [
        escape_markdown(repository),
        "issue closed",
        f"{link} *{escape_markdown(issue['title'])}*",
    ]
    if body := truncate(issue.get("body") or "", ISSUE_BODY_LIMIT):
        parts.append(escape_markdown(body))
    parts.append(escape_markdown(actor))
    return " · ".join(parts)


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
