#!/usr/bin/env python3
import json
import os
import subprocess
import uuid
from datetime import datetime, timezone
from html import escape

DIGEST_PR_LIMIT = 10
TELEGRAM_MESSAGE_LIMIT = 4096


def gh_json(*arguments):
    result = subprocess.run(["gh", *arguments], stdout=subprocess.PIPE, text=True, check=True)
    return json.loads(result.stdout)


def author_login(pull_request):
    return (pull_request.get("author") or {}).get("login") or "ghost"


def pull_request_link(pull_request):
    return f'<a href="{escape(pull_request["url"], quote=True)}">#{pull_request["number"]}</a>'


def format_opened(repository, pull_request, event_action):
    if pull_request.get("isDraft"):
        return ""

    events = {
        "ready_for_review": ("🆗", "PR ready for review"),
        "reopened": ("🆙", "PR reopened"),
    }
    emoji, event = events.get(event_action, ("🆕", "PR opened"))
    return (
        f"{emoji} {escape(repository)} — {event} · {pull_request_link(pull_request)} "
        f"<b>{escape(pull_request['title'])}</b> · {escape(author_login(pull_request))}"
    )


def format_merged(repository, pull_request):
    return (
        f"🔀 {escape(repository)} — PR merged · {pull_request_link(pull_request)} "
        f"<b>{escape(pull_request['title'])}</b> · {escape(author_login(pull_request))}"
    )


def parse_github_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def format_digest(repository, pull_requests, now=None):
    pull_requests = [pull_request for pull_request in pull_requests if not pull_request.get("isDraft")]
    if not pull_requests:
        return ""

    now = now or datetime.now(timezone.utc)
    count = len(pull_requests)
    header = f"🔠 {escape(repository)} — {count} open {'PR' if count == 1 else 'PRs'}"
    lines = []
    for pull_request in pull_requests[:DIGEST_PR_LIMIT]:
        age = max(0, (now - parse_github_time(pull_request["createdAt"])).days)
        line = (
            f"{pull_request_link(pull_request)} <b>{escape(pull_request['title'])}</b> · "
            f"{escape(author_login(pull_request))} · {age}d"
        )
        remaining = len(pull_requests) - len(lines) - 1
        suffix = (
            f'<a href="https://github.com/{escape(repository, quote=True)}/pulls">...and {remaining} more</a>'
            if remaining
            else ""
        )
        candidate = "\n".join((header, *lines, line, suffix)).rstrip()
        if len(candidate) > TELEGRAM_MESSAGE_LIMIT:
            break
        lines.append(line)

    remaining = len(pull_requests) - len(lines)
    if remaining:
        lines.append(f'<a href="https://github.com/{escape(repository, quote=True)}/pulls">...and {remaining} more</a>')

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
