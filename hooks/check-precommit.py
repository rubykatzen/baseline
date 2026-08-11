#!/usr/bin/env python3
import json
import os
import sys

import yaml


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


def detected_hooks():
    return set(json.loads(os.environ["LINTERS"])) - {"pre-commit"}


configured = configured_hooks()
detected = detected_hooks()

if configured != detected:
    print("::error::Linter mismatch between workflow and .pre-commit-config.yaml")
    print(f"  workflow:   {sorted(detected)}")
    print(f"  pre-commit: {sorted(configured)}")
    sys.exit(1)
print(f"In sync: {sorted(configured)}")
