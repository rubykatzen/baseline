#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

FIELD_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    message: str


def parse_json_list(value):
    try:
        items = json.loads(value)
    except json.JSONDecodeError as error:
        raise ValueError("skip must be a JSON array of strings") from error

    if not isinstance(items, list) or not all(isinstance(item, str) and item for item in items):
        raise ValueError("skip must be a JSON array of strings")

    return set(items)


def load_config(config_path):
    try:
        with open(config_path) as file:
            config = yaml.safe_load(file)
    except yaml.YAMLError as error:
        raise ValueError("github repo config must be valid YAML") from error

    if not isinstance(config, dict):
        raise ValueError("github repo config must be a mapping")

    checks = config.get("checks")
    if not isinstance(checks, dict) or not checks:
        raise ValueError("github repo config must contain a non-empty checks mapping")
    for field in checks:
        if not isinstance(field, str) or not FIELD_PATTERN.fullmatch(field):
            raise ValueError("github repo check names must be GraphQL field names")

    return checks


def github_request(args):
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode:
        message = result.stderr.strip() or result.stdout.strip() or "unknown error"
        raise RuntimeError(message)

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError("GitHub API returned invalid JSON") from error


def repository_name(repository):
    parts = repository.split("/")
    if len(parts) != 2 or not all(parts):
        raise ValueError("repository must use owner/name format")
    return parts


def github_repository(repository, fields):
    owner, name = repository_name(repository)
    selection = " ".join(fields)
    query = (
        "query($owner: String!, $name: String!) { "
        f"repository(owner: $owner, name: $name) {{ {selection} }} "
        "}"
    )
    response = github_request(
        ["api", "graphql", "-f", f"query={query}", "-F", f"owner={owner}", "-F", f"name={name}"]
    )
    try:
        return response["data"]["repository"]
    except (KeyError, TypeError) as error:
        raise RuntimeError("GitHub returned an invalid repository response") from error


def format_value(value):
    return json.dumps(value, separators=(",", ":"), sort_keys=True)


def evaluate_checks(checks, repository, skipped=(), request=github_repository):
    skipped = set(skipped)
    if unknown := skipped - set(checks):
        names = ", ".join(sorted(unknown))
        raise ValueError(f"Unknown skipped GitHub config checks: {names}")

    active_fields = [field for field in checks if field not in skipped]
    payload = None
    request_error = None
    if active_fields:
        try:
            payload = request(repository, active_fields)
        except RuntimeError as error:
            request_error = str(error)

    results = []
    for field, expected in checks.items():
        if field in skipped:
            results.append(CheckResult(field, "skipped", "skipped by workflow input"))
            continue

        if request_error:
            results.append(CheckResult(field, "failed", f"GitHub request failed: {request_error}"))
            continue

        if field not in payload:
            results.append(CheckResult(field, "failed", f"GitHub API response has no {field} field"))
            continue
        actual = payload[field]

        if type(actual) is not type(expected) or actual != expected:
            message = f"expected {format_value(expected)}, got {format_value(actual)}"
            results.append(CheckResult(field, "failed", message))
            continue

        results.append(CheckResult(field, "passed", format_value(actual)))

    return results


def annotation_value(value):
    return str(value).replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def main():
    try:
        checks = load_config(Path(os.environ["CONFIG_PATH"]))
        skipped = parse_json_list(os.environ.get("SKIP", "[]"))
        repository = os.environ["REPOSITORY"]
        results = evaluate_checks(checks, repository, skipped)
    except (KeyError, OSError, ValueError) as error:
        print(f"::error::{annotation_value(error)}")
        return 1

    print(f"GitHub repository config: {repository}")
    for result in results:
        if result.status == "failed":
            title = annotation_value(f"GitHub config: {result.name}")
            message = annotation_value(result.message)
            print(f"::error title={title}::{message}")
        else:
            print(f"{result.status.upper()} {result.name}: {result.message}")

    failed = sum(result.status == "failed" for result in results)
    passed = sum(result.status == "passed" for result in results)
    skipped_count = sum(result.status == "skipped" for result in results)
    print(f"Result: {passed} passed, {failed} failed, {skipped_count} skipped")
    return int(failed > 0)


if __name__ == "__main__":
    sys.exit(main())
