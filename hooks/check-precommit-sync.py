#!/usr/bin/env python3
import yaml, sys, os

try:
    with open(".pre-commit-config.yaml") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("::notice::No .pre-commit-config.yaml found — skipping sync check.")
    sys.exit(0)

hooks = next(
    ({h["id"] for h in r["hooks"]} for r in config["repos"] if "rubykatzen/baseline" in r["repo"]),
    None,
)
if hooks is None:
    print("::notice::No rubykatzen/baseline entry in .pre-commit-config.yaml — skipping.")
    sys.exit(0)

linters = {x.strip() for x in os.environ["LINTERS"].split(",") if x.strip() not in ("", "pre-commit")}

if linters != hooks:
    print("::error::Linter mismatch between workflow and .pre-commit-config.yaml")
    print(f"  workflow:   {sorted(linters)}")
    print(f"  pre-commit: {sorted(hooks)}")
    sys.exit(1)

print(f"In sync: {sorted(linters)}")
