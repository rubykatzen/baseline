#!/usr/bin/env python3
import os
import uuid

MARKDOWN_V2_SPECIAL_CHARACTERS = frozenset("_*[]()~`>#+-=|{}.!\\")


def escape_markdown(value):
    return "".join(f"\\{character}" if character in MARKDOWN_V2_SPECIAL_CHARACTERS else character for character in str(value))


def escape_link_url(value):
    return str(value).replace("\\", "\\\\").replace(")", "\\)")


def post_url(post_id):
    return f"https://www.linkedin.com/feed/update/{post_id}/"


def format_published(repository, tag, post_id):
    link = f"[LinkedIn post]({escape_link_url(post_url(post_id))})"
    return f"*{escape_markdown(repository)}* • {link} published for {escape_markdown(tag)}"


def format_failed(repository, tag, run_url):
    link = f"[LinkedIn post]({escape_link_url(run_url)})"
    return f"*{escape_markdown(repository)}* • {link} failed for {escape_markdown(tag)}"


def write_output(message):
    delimiter = f"ghdelim_{uuid.uuid4().hex}"
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        print(f"message<<{delimiter}", file=output)
        print(message, file=output)
        print(delimiter, file=output)


def main():
    repository = os.environ["REPOSITORY"]
    tag = os.environ["TAG_NAME"]
    result = os.environ["RESULT"]

    if result == "success":
        message = format_published(repository, tag, os.environ["POST_ID"])
    elif result == "failure":
        message = format_failed(repository, tag, os.environ["RUN_URL"])
    else:
        raise ValueError(f"result must be success or failure, got {result!r}")

    write_output(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
