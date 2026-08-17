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
COLOR_PATTERN = re.compile(r"^[0-9A-Fa-f]{6}$")
LABELS_CHECK = "labels"


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

    repository_config = config.get("config")
    if not isinstance(repository_config, dict) or not repository_config:
        raise ValueError("github repo config must contain a non-empty config mapping")
    for field in repository_config:
        if not isinstance(field, str) or not FIELD_PATTERN.fullmatch(field):
            raise ValueError("github repo check names must be GraphQL field names")

    labels = config.get("labels")
    if not isinstance(labels, dict):
        raise ValueError("github repo config must contain a labels mapping")
    required = validate_label_group(labels.get("required"), "required")
    optional = validate_label_group(labels.get("optional", {}), "optional", allow_empty=True)
    if duplicate := set(required) & set(optional):
        names = ", ".join(sorted(duplicate))
        raise ValueError(f"GitHub labels cannot be both required and optional: {names}")

    checks = dict(repository_config)
    checks[LABELS_CHECK] = {"required": required, "optional": optional}
    return checks


def validate_label_group(group, name, allow_empty=False):
    if not isinstance(group, dict) or (not group and not allow_empty):
        raise ValueError(f"GitHub {name} labels must be a{' non-empty' if not allow_empty else ''} mapping")

    validated = {}
    for label, settings in group.items():
        if not isinstance(label, str) or not label:
            raise ValueError(f"GitHub {name} label names must be non-empty strings")
        if not isinstance(settings, dict) or set(settings) != {"color", "description"}:
            raise ValueError(f"GitHub label {label} must contain only color and description")
        color = settings["color"]
        if not isinstance(color, str) or not COLOR_PATTERN.fullmatch(color):
            raise ValueError(f"GitHub label {label} color must be a six-digit hex value")
        description = settings["description"]
        if not isinstance(description, str) or not description:
            raise ValueError(f"GitHub label {label} description must be a non-empty string")
        validated[label] = {"color": color.lower(), "description": description}
    return validated


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


def github_labels(repository):
    repository_name(repository)
    response = github_request(
        ["api", "--paginate", "--slurp", f"repos/{repository}/labels?per_page=100"]
    )
    try:
        return [label for page in response for label in page]
    except TypeError as error:
        raise RuntimeError("GitHub returned an invalid labels response") from error


def format_value(value):
    return json.dumps(value, separators=(",", ":"), sort_keys=True)


def evaluate_label_check(policy, repository, request=github_labels):
    try:
        labels = request(repository)
        actual = {
            label["name"]: {
                "color": label["color"].lower(),
                "description": label.get("description") or "",
            }
            for label in labels
        }
    except (KeyError, TypeError, RuntimeError) as error:
        return CheckResult(LABELS_CHECK, "failed", f"GitHub request failed: {error}")

    required = policy["required"]
    optional = policy["optional"]
    allowed = {**required, **optional}
    problems = []
    if missing := set(required) - set(actual):
        problems.append(f"missing: {', '.join(sorted(missing))}")
    if unexpected := set(actual) - set(allowed):
        problems.append(f"unexpected: {', '.join(sorted(unexpected))}")
    incorrect_colors = [
        f"{name} expected #{allowed[name]['color']}, got #{actual[name]['color']}"
        for name in sorted(set(actual) & set(allowed))
        if actual[name]["color"] != allowed[name]["color"]
    ]
    if incorrect_colors:
        problems.append(f"incorrect colors: {'; '.join(incorrect_colors)}")
    incorrect_descriptions = [
        f"{name} expected {format_value(allowed[name]['description'])}, "
        f"got {format_value(actual[name]['description'])}"
        for name in sorted(set(actual) & set(allowed))
        if actual[name]["description"] != allowed[name]["description"]
    ]
    if incorrect_descriptions:
        problems.append(f"incorrect descriptions: {'; '.join(incorrect_descriptions)}")

    if problems:
        return CheckResult(LABELS_CHECK, "failed", "; ".join(problems))
    return CheckResult(LABELS_CHECK, "passed", f"{len(actual)} labels match policy")


def evaluate_checks(
    checks,
    repository,
    skipped=(),
    request=github_repository,
    labels_request=github_labels,
):
    skipped = set(skipped)
    if unknown := skipped - set(checks):
        names = ", ".join(sorted(unknown))
        raise ValueError(f"Unknown skipped GitHub config checks: {names}")

    active_fields = [field for field in checks if field != LABELS_CHECK and field not in skipped]
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

        if field == LABELS_CHECK:
            results.append(evaluate_label_check(expected, repository, labels_request))
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
