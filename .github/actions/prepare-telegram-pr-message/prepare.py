#!/usr/bin/env python3
import json
import os
import subprocess
import uuid
from datetime import datetime, timezone

DIGEST_PR_LIMIT = 10
MARKDOWN_V2_SPECIAL_CHARACTERS = frozenset("_*[]()~`>#+-=|{}.!\\")
TELEGRAM_MESSAGE_LIMIT = 4096


def gh_json(*arguments):
    result = subprocess.run(["gh", *arguments], stdout=subprocess.PIPE, text=True, check=True)
    return json.loads(result.stdout)


def author_login(pull_request):
    return (pull_request.get("author") or {}).get("login") or "ghost"


def escape_markdown(value):
    return "".join(f"\\{character}" if character in MARKDOWN_V2_SPECIAL_CHARACTERS else character for character in str(value))


def escape_link_url(value):
    return str(value).replace("\\", "\\\\").replace(")", "\\)")


def pull_request_link(pull_request):
    number = escape_markdown(f"#{pull_request['number']}")
    url = escape_link_url(pull_request["url"])
    return f"[{number}]({url})"


def format_opened(repository, pull_request, event_action):
    if pull_request.get("isDraft"):
        return ""

    events = {
        "ready_for_review": ("🆗", "PR ready"),
        "reopened": ("🆙", "PR reopened"),
    }
    emoji, event = events.get(event_action, ("🆕", "PR opened"))
    return (
        f"{emoji} {escape_markdown(repository)} — {event} · {pull_request_link(pull_request)} "
        f"*{escape_markdown(pull_request['title'])}* · {escape_markdown(author_login(pull_request))}"
    )


def format_merged(repository, pull_request):
    return (
        f"🔀 {escape_markdown(repository)} — PR merged · {pull_request_link(pull_request)} "
        f"*{escape_markdown(pull_request['title'])}* · {escape_markdown(author_login(pull_request))}"
    )


def parse_github_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def format_digest(repository, pull_requests, now=None):
    pull_requests = [pull_request for pull_request in pull_requests if not pull_request.get("isDraft")]
    if not pull_requests:
        return ""

    now = now or datetime.now(timezone.utc)
    count = len(pull_requests)
    header = f"🔠 {escape_markdown(repository)} — {count} open {'PR' if count == 1 else 'PRs'}"
    lines = []
    for pull_request in pull_requests[:DIGEST_PR_LIMIT]:
        age = max(0, (now - parse_github_time(pull_request["createdAt"])).days)
        line = (
            f"{pull_request_link(pull_request)} *{escape_markdown(pull_request['title'])}* · "
            f"{escape_markdown(author_login(pull_request))} · {age}d"
        )
        remaining = len(pull_requests) - len(lines) - 1
        suffix = (
            f"[{escape_markdown(f'...and {remaining} more')}](https://github.com/{escape_link_url(repository)}/pulls)"
            if remaining
            else ""
        )
        candidate = "\n".join((header, *lines, line, suffix)).rstrip()
        if len(candidate) > TELEGRAM_MESSAGE_LIMIT:
            break
        lines.append(line)

    remaining = len(pull_requests) - len(lines)
    if remaining:
        lines.append(f"[{escape_markdown(f'...and {remaining} more')}](https://github.com/{escape_link_url(repository)}/pulls)")

    return "\n".join((header, *lines))


def write_output(message):
    delimiter = f"ghdelim_{uuid.uuid4().hex}"
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        print(f"message<<{delimiter}", file=output)
        print(message, file=output)
        print(delimiter, file=output)


def main():
    repository = os.environ["REPOSITORY"]
    event_name = os.environ["EVENT_NAME"]
    event_action = os.environ.get("EVENT_ACTION") or None
    number = os.environ.get("NUMBER") or None
    merged = os.environ.get("MERGED") == "true"

    if event_name in ("schedule", "workflow_dispatch"):
        pull_requests = gh_json(
            "pr",
            "list",
            "--repo",
            repository,
            "--state",
            "open",
            "--limit",
            "100",
            "--json",
            "number,title,author,isDraft,url,createdAt",
        )
        message = format_digest(repository, pull_requests)
    elif event_name == "pull_request_target" and event_action in ("opened", "ready_for_review", "reopened"):
        pull_request = gh_json(
            "pr",
            "view",
            number,
            "--repo",
            repository,
            "--json",
            "number,title,author,url,isDraft",
        )
        message = format_opened(repository, pull_request, event_action)
    elif event_name == "pull_request_target" and event_action == "closed" and merged:
        pull_request = gh_json(
            "pr",
            "view",
            number,
            "--repo",
            repository,
            "--json",
            "number,title,author,url",
        )
        message = format_merged(repository, pull_request)
    else:
        raise ValueError(f"Unsupported pull request notification event: {event_name}/{event_action}")

    write_output(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
