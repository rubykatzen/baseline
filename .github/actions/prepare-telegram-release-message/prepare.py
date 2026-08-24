#!/usr/bin/env python3
import os
import uuid

MARKDOWN_V2_SPECIAL_CHARACTERS = frozenset("_*[]()~`>#+-=|{}.!\\")


def escape_markdown(value):
    return "".join(f"\\{character}" if character in MARKDOWN_V2_SPECIAL_CHARACTERS else character for character in str(value))


def escape_link_url(value):
    return str(value).replace("\\", "\\\\").replace(")", "\\)")


def format_published(repository, release):
    tag = release["tag"]
    label = escape_markdown(f"release {tag}")
    link = f"[{label}]({escape_link_url(release['url'])})"
    parts = [f"*{escape_markdown(repository)}*", f"{link} published"]

    name = release.get("name")
    if name and name != tag:
        parts.append(f"*{escape_markdown(name)}*")

    parts.append(escape_markdown(release.get("actor") or "ghost"))
    return " · ".join(parts)


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
        "actor": os.environ.get("ACTOR") or "ghost",
    }
    write_output(format_published(os.environ["REPOSITORY"], release))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
