#!/usr/bin/env python3
import json
import os
import subprocess
import uuid

ISSUE_BODY_LIMIT = 500


def gh_json(*arguments):
    result = subprocess.run(["gh", *arguments], stdout=subprocess.PIPE, text=True, check=True)
    return json.loads(result.stdout)


def truncate(value, limit):
    value = value.strip()
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def format_closed(repository, issue, actor):
    lines = [
        f"{repository} — issue closed",
        f"#{issue['number']} {issue['title']}",
    ]
    if body := truncate(issue.get("body") or "", ISSUE_BODY_LIMIT):
        lines.append(body)
    lines.append(f"{actor} · {issue['url']}")
    return "\n".join(lines)


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
