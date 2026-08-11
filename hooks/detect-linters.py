#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml
from identify.identify import tags_from_path

BASELINE_ROOT = Path(__file__).parent.parent
PRE_COMMIT_LINTER = "pre-commit"


def parse_json_list(value):
    try:
        items = json.loads(value)
    except json.JSONDecodeError as error:
        raise ValueError("exclude must be a JSON array of strings") from error

    if not isinstance(items, list) or not all(isinstance(item, str) and item for item in items):
        raise ValueError("exclude must be a JSON array of strings")

    return set(items)


def repo_files():
    result = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True)
    return [Path(path) for path in result.stdout.splitlines() if path]


def file_tags(path):
    try:
        return tags_from_path(str(path))
    except ValueError:
        return frozenset()


def hook_applies(hook, files):
    required_types = set(hook.get("types", ()))
    pattern = re.compile(hook["files"]) if "files" in hook else None
    if not required_types and pattern is None:
        return False

    for path in files:
        if required_types and not required_types.issubset(file_tags(path)):
            continue
        if pattern and not pattern.search(str(path)):
            continue
        return True

    return False


def load_hook_definitions(baseline_root):
    with open(Path(baseline_root) / ".pre-commit-hooks.yaml") as file:
        return yaml.safe_load(file)


def detect_linters(baseline_root, excluded=()):
    hook_definitions = load_hook_definitions(baseline_root)
    supported = {hook["id"] for hook in hook_definitions} | {PRE_COMMIT_LINTER}
    excluded = set(excluded)

    if unknown := excluded - supported:
        names = ", ".join(sorted(unknown))
        raise ValueError(f"Unknown excluded linters: {names}")

    files = repo_files()
    selected = {hook["id"] for hook in hook_definitions if hook_applies(hook, files)}
    if Path(".pre-commit-config.yaml").is_file():
        selected.add(PRE_COMMIT_LINTER)

    return selected - excluded


def main():
    try:
        excluded = parse_json_list(os.environ.get("EXCLUDE", "[]"))
        linters = sorted(detect_linters(BASELINE_ROOT, excluded))
    except ValueError as error:
        print(f"::error::{error}")
        return 1

    value = json.dumps(linters, separators=(",", ":"))
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        print(f"linters={','.join(linters)}", file=output)
        print(f"linters-json={value}", file=output)

    print(f"Detected linters: {', '.join(linters) or 'none'}")
    print(f"Excluded linters: {', '.join(sorted(excluded)) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
