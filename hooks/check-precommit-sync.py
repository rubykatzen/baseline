#!/usr/bin/env python3
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml
from identify.identify import tags_from_path

BASELINE_ROOT = Path(__file__).parent.parent


def repo_files():
    out = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout
    return [Path(p) for p in out.splitlines() if p]


def file_tags(path):
    try:
        return tags_from_path(str(path))
    except ValueError:
        return frozenset()


def needed_hooks(files):
    with open(BASELINE_ROOT / ".pre-commit-hooks.yaml") as f:
        hook_defs = yaml.safe_load(f)
    return {
        h["id"] for h in hook_defs
        if ("types" in h and any(set(h["types"]).issubset(file_tags(f)) for f in files))
        or ("files" in h and any(re.search(h["files"], str(f)) for f in files))
    }


def configured_hooks():
    try:
        with open(".pre-commit-config.yaml") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print("::error::.pre-commit-config.yaml not found — required when pre-commit is in linters.")
        sys.exit(1)
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


files = repo_files()
configured = configured_hooks()
linters = parse_linters()
needed = needed_hooks(files)

ok = True
if missing := needed - configured:
    print(f"::error::Hooks needed for repo files but missing from .pre-commit-config.yaml: {sorted(missing)}")
    ok = False
if extra := configured - needed:
    print(f"::error::Hooks configured but no matching files found: {sorted(extra)}")
    ok = False
if configured != linters:
    print("::error::Linter mismatch between workflow and .pre-commit-config.yaml")
    print(f"  workflow:   {sorted(linters)}")
    print(f"  pre-commit: {sorted(configured)}")
    ok = False
if not ok:
    sys.exit(1)
print(f"In sync: {sorted(configured)}")
