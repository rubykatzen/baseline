#!/usr/bin/env python3
import difflib
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

import yaml


@dataclass(frozen=True)
class Fragment:
    path: str
    content: str


@dataclass(frozen=True)
class FragmentResult:
    name: str
    path: str
    status: str
    message: str
    diff: str = ""


def parse_json_list(value):
    try:
        items = json.loads(value)
    except json.JSONDecodeError as error:
        raise ValueError("skip must be a JSON array of strings") from error

    if not isinstance(items, list) or not all(isinstance(item, str) and item for item in items):
        raise ValueError("skip must be a JSON array of strings")

    return set(items)


def validate_path(value):
    if not isinstance(value, str) or not value:
        raise ValueError("embedder check path must be a non-empty string")

    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or value != path.as_posix():
        raise ValueError(f"embedder check path must be a normalized relative path: {value!r}")
    return value


def load_config(config_path):
    try:
        with open(config_path) as file:
            config = yaml.safe_load(file)
    except yaml.YAMLError as error:
        raise ValueError("embedder config must be valid YAML") from error

    if not isinstance(config, dict):
        raise ValueError("embedder config must be a mapping")

    raw_fragments = config.get("fragments")
    if not isinstance(raw_fragments, dict) or not raw_fragments:
        raise ValueError("embedder config must contain a non-empty fragments mapping")

    fragments = {}
    for name, value in raw_fragments.items():
        if not isinstance(name, str) or not name:
            raise ValueError("embedder fragment names must be non-empty strings")
        if not isinstance(value, dict) or set(value) != {"path", "content"}:
            raise ValueError(f"embedder fragment {name!r} must contain only path and content")

        path = validate_path(value["path"])
        content = value["content"]
        if not isinstance(content, str) or not content:
            raise ValueError(f"embedder fragment {name!r} content must be a non-empty string")
        fragments[name] = Fragment(path=path, content=content)

    return fragments


def read_repository_file(repository_root, path):
    target = Path(repository_root) / path
    try:
        return target.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise RuntimeError("file does not exist") from None
    except (OSError, UnicodeError) as error:
        raise RuntimeError(f"file could not be read: {error}") from error


def current_fragment(actual, expected):
    expected_lines = expected.splitlines(keepends=True)
    if len(expected_lines) < 2:
        return None

    opening = expected_lines[0].rstrip("\r\n")
    closing = expected_lines[-1].rstrip("\r\n")
    actual_lines = actual.splitlines(keepends=True)

    for start, line in enumerate(actual_lines):
        if line.rstrip("\r\n") != opening:
            continue
        for end in range(start + 1, len(actual_lines)):
            if actual_lines[end].rstrip("\r\n") == closing:
                return "".join(actual_lines[start : end + 1])
        return "".join(actual_lines[start:])

    return None


def fragment_diff(name, path, expected, actual):
    current = current_fragment(actual, expected) or ""
    lines = difflib.unified_diff(
        current.splitlines(),
        expected.splitlines(),
        fromfile=f"{path} ({name}, actual)",
        tofile=f"{path} ({name}, expected)",
        lineterm="",
    )
    return "\n".join(lines)


def evaluate_fragments(fragments, repository_root, skipped=(), read=read_repository_file):
    skipped = set(skipped)
    if unknown := skipped - set(fragments):
        names = ", ".join(sorted(unknown))
        raise ValueError(f"Unknown skipped embedder fragments: {names}")

    files = {}
    for name, fragment in fragments.items():
        if name in skipped:
            continue
        if fragment.path in files:
            continue
        try:
            files[fragment.path] = (read(repository_root, fragment.path), None)
        except RuntimeError as error:
            files[fragment.path] = (None, str(error))

    results = []
    for name, fragment in fragments.items():
        if name in skipped:
            results.append(FragmentResult(name, fragment.path, "skipped", "skipped by workflow input"))
            continue

        actual, error = files[fragment.path]
        if error:
            diff = fragment_diff(name, fragment.path, fragment.content, "")
            results.append(FragmentResult(name, fragment.path, "failed", error, diff))
        elif fragment.content not in actual:
            current = current_fragment(actual, fragment.content)
            message = "required fragment is missing" if current is None else "required fragment differs"
            diff = fragment_diff(name, fragment.path, fragment.content, actual)
            results.append(FragmentResult(name, fragment.path, "failed", message, diff))
        else:
            results.append(FragmentResult(name, fragment.path, "passed", "required content found"))

    return results


def annotation_value(value):
    return str(value).replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def print_report(results):
    print("Embedder expectations:")
    for result in results:
        print(f"{result.status.upper()} {result.name} ({result.path}): {result.message}")

    for result in results:
        if not result.diff:
            continue
        print(f"::group::Diff {result.name} ({result.path})")
        print(result.diff)
        print("::endgroup::")


def main():
    try:
        fragments = load_config(Path(os.environ["CONFIG_PATH"]))
        skipped = parse_json_list(os.environ.get("SKIP", "[]"))
        repository_root = Path(os.environ.get("REPOSITORY_ROOT", "."))
        results = evaluate_fragments(fragments, repository_root, skipped)
    except (KeyError, OSError, ValueError) as error:
        print(f"::error::{annotation_value(error)}")
        return 1

    print(f"Embedder config: {len(fragments)} fragments")
    print_report(results)
    for result in results:
        if result.status == "failed":
            title = annotation_value(f"Embedder fragment: {result.name}")
            message = annotation_value(result.message)
            print(f"::error file={result.path},title={title}::{message}")

    failed = sum(result.status == "failed" for result in results)
    passed = sum(result.status == "passed" for result in results)
    skipped_count = sum(result.status == "skipped" for result in results)
    print(f"Result: {passed} passed, {failed} failed, {skipped_count} skipped")
    return int(failed > 0)


if __name__ == "__main__":
    sys.exit(main())
