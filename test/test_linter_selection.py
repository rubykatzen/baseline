import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

BASELINE_ROOT = Path(__file__).parent.parent
SPEC = importlib.util.spec_from_file_location(
    "detect_linters", BASELINE_ROOT / "hooks" / "detect-linters.py"
)
DETECT_LINTERS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DETECT_LINTERS)
detect_linters = DETECT_LINTERS.detect_linters
parse_json_list = DETECT_LINTERS.parse_json_list


class LinterSelectionTest(unittest.TestCase):
    def setUp(self):
        self.previous_directory = Path.cwd()
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary_directory.name)
        os.chdir(self.repo)
        subprocess.run(["git", "init", "--quiet"], check=True)

        self.track("app.rb", "puts 'ok'\n")
        self.track("script.py", "print('ok')\n")
        self.track("README.md", "# Test\n")
        self.track(".github/workflows/lint.yml", "name: Test\n")
        self.track(".pre-commit-config.yaml", "repos: []\n")

    def tearDown(self):
        os.chdir(self.previous_directory)
        self.temporary_directory.cleanup()

    def track(self, path, content):
        file = self.repo / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content)
        subprocess.run(["git", "add", path], check=True)

    def test_detects_linters_from_tracked_files(self):
        self.assertEqual(
            detect_linters(BASELINE_ROOT),
            {"actionlint", "pre-commit", "pymarkdown", "rubocop", "ruff", "yamllint"},
        )

    def test_skips_detected_linter(self):
        self.assertNotIn("rubocop", detect_linters(BASELINE_ROOT, {"rubocop"}))

    def test_allows_skipping_non_applicable_linter(self):
        self.assertEqual(detect_linters(BASELINE_ROOT, {"herb"}), detect_linters(BASELINE_ROOT))

    def test_rejects_unknown_skip(self):
        with self.assertRaisesRegex(ValueError, "Unknown skipped linters: typo"):
            detect_linters(BASELINE_ROOT, {"typo"})

    def test_parses_json_skips(self):
        self.assertEqual(parse_json_list('["rubocop", "herb"]'), {"rubocop", "herb"})

    def test_rejects_non_array_skips(self):
        for value in ('"rubocop"', "rubocop", '["rubocop", 1]'):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "JSON array of strings"):
                parse_json_list(value)

    def test_writes_single_json_output(self):
        output = self.repo / "github-output"
        with patch.dict(os.environ, {"SKIP": "[]", "GITHUB_OUTPUT": str(output)}):
            self.assertEqual(DETECT_LINTERS.main(), 0)

        lines = output.read_text().splitlines()
        self.assertEqual(len(lines), 1)
        name, value = lines[0].split("=", 1)
        self.assertEqual(name, "linters")
        self.assertEqual(json.loads(value), sorted(detect_linters(BASELINE_ROOT)))

    def test_ignores_untracked_files(self):
        (self.repo / "script.sh").write_text("#!/bin/sh\n")

        self.assertNotIn("shellcheck", detect_linters(BASELINE_ROOT))


if __name__ == "__main__":
    unittest.main()
