#!/usr/bin/env python3
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml
from identify.identify import tags_from_path

BASELINE_ROOT = Path(__file__).parent.parent


def load_hook_defs():
    with open(BASELINE_ROOT / ".pre-commit-hooks.yaml") as f:
        return yaml.safe_load(f)


def repo_files():
    result = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True)
    return [Path(p) for p in result.stdout.splitlines() if p]


def file_tags(path):
    try:
        return tags_from_path(str(path))
    except ValueError:
        return frozenset()


def hook_needed(hook, files):
    if "types" in hook:
        required = set(hook["types"])
        return any(required.issubset(file_tags(f)) for f in files)
    if "files" in hook:
        pattern = re.compile(hook["files"])
        return any(pattern.search(str(f)) for f in files)
    return False


def needed_hooks(hook_defs, files):
    return {h["id"] for h in hook_defs if hook_needed(h, files)}


def load_config():
    try:
        with open(".pre-commit-config.yaml") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("::error::.pre-commit-config.yaml not found — required when pre-commit is in linters.")
        sys.exit(1)


def baseline_configured_hooks(config):
    hooks = next(
        ({h["id"] for h in r["hooks"]} for r in config["repos"] if "rubykatzen/baseline" in r["repo"]),
        None,
    )
    if hooks is None:
        print("::error::No rubykatzen/baseline entry in .pre-commit-config.yaml.")
        sys.exit(1)
    return hooks


def parse_linters():
    return {x.strip() for x in os.environ["LINTERS"].split(",") if x.strip() not in ("", "pre-commit")}


hook_defs = load_hook_defs()
files = repo_files()
config = load_config()
configured = baseline_configured_hooks(config)
linters = parse_linters()
needed = needed_hooks(hook_defs, files)

ok = True

missing = needed - configured
if missing:
    print(f"::error::Hooks needed for repo files but missing from .pre-commit-config.yaml: {sorted(missing)}")
    ok = False

extra = configured - needed
if extra:
    print(f"::notice::Hooks configured but no matching files found: {sorted(extra)}")

if configured != linters:
    print("::error::Linter mismatch between workflow and .pre-commit-config.yaml")
    print(f"  workflow:   {sorted(linters)}")
    print(f"  pre-commit: {sorted(configured)}")
    ok = False

if not ok:
    sys.exit(1)

print(f"In sync: {sorted(configured)}")
