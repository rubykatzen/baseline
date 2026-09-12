#!/usr/bin/env python3
import json
import os
import subprocess
import uuid

MARKDOWN_V2_SPECIAL_CHARACTERS = frozenset("_*[]()~`>#+-=|{}.!\\")


def gh_json(*arguments):
    result = subprocess.run(["gh", *arguments], stdout=subprocess.PIPE, text=True, check=True)
    return json.loads(result.stdout)


def escape_markdown(value):
    return "".join(f"\\{character}" if character in MARKDOWN_V2_SPECIAL_CHARACTERS else character for character in str(value))


def escape_link_url(value):
    return str(value).replace("\\", "\\\\").replace(")", "\\)")


def format_closed(repository, issue, actor):
    label = escape_markdown(f"issue {issue['number']}")
    link = f"[{label}]({escape_link_url(issue['url'])})"
    parts = [
        f"*{escape_markdown(repository)}*",
        f"{link} closed",
        f"*{escape_markdown(issue['title'])}*",
        escape_markdown(actor),
    ]
    return " • ".join(parts)


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
        "number,title,url",
    )
    write_output(format_closed(repository, issue, actor))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
