import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

BASELINE_ROOT = Path(__file__).parent.parent
SPEC = importlib.util.spec_from_file_location(
    "check_github_config", BASELINE_ROOT / ".github" / "actions" / "check-github-config" / "check.py"
)
CHECK_GITHUB_CONFIG = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK_GITHUB_CONFIG)


class GitHubConfigTest(unittest.TestCase):
    def setUp(self):
        self.checks = {
            "hasWikiEnabled": False,
            "autoMergeAllowed": True,
        }

    def test_loads_repository_config(self):
        checks = CHECK_GITHUB_CONFIG.load_config(BASELINE_ROOT / "config" / "github.yml")

        self.assertEqual(set(checks), {"hasWikiEnabled", "autoMergeAllowed", "deleteBranchOnMerge"})

    def test_rejects_invalid_repository_config(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml") as config:
            config.write("config:\n  invalid-field: false\n")
            config.flush()

            with self.assertRaisesRegex(ValueError, "must be GraphQL field names"):
                CHECK_GITHUB_CONFIG.load_config(config.name)

    def test_rejects_malformed_yaml(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml") as config:
            config.write("config: [\n")
            config.flush()

            with self.assertRaisesRegex(ValueError, "must be valid YAML"):
                CHECK_GITHUB_CONFIG.load_config(config.name)

    def test_parses_json_skip(self):
        self.assertEqual(CHECK_GITHUB_CONFIG.parse_json_list('["hasWikiEnabled"]'), {"hasWikiEnabled"})

    def test_rejects_invalid_json_skip(self):
        for value in ('"hasWikiEnabled"', "hasWikiEnabled", '["hasWikiEnabled", 1]'):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "JSON array of strings"):
                CHECK_GITHUB_CONFIG.parse_json_list(value)

    def test_rejects_unknown_skip(self):
        with self.assertRaisesRegex(ValueError, "Unknown skipped GitHub config checks: typo"):
            CHECK_GITHUB_CONFIG.evaluate_checks(self.checks, "owner/repo", {"typo"})

    def test_evaluates_checks_and_reuses_api_response(self):
        requests = []

        def request(repository, fields):
            requests.append((repository, fields))
            return {"hasWikiEnabled": False, "autoMergeAllowed": True}

        results = CHECK_GITHUB_CONFIG.evaluate_checks(self.checks, "owner/repo", request=request)

        self.assertEqual([result.status for result in results], ["passed", "passed"])
        self.assertEqual(requests, [("owner/repo", ["hasWikiEnabled", "autoMergeAllowed"])])

    def test_skips_check_without_requesting_it(self):
        results = CHECK_GITHUB_CONFIG.evaluate_checks(
            {"hasWikiEnabled": self.checks["hasWikiEnabled"]},
            "owner/repo",
            {"hasWikiEnabled"},
            request=lambda _repository, _fields: self.fail("skipped check made an API request"),
        )

        self.assertEqual(results[0].status, "skipped")

    def test_aggregates_mismatches(self):
        results = CHECK_GITHUB_CONFIG.evaluate_checks(
            self.checks,
            "owner/repo",
            request=lambda _repository, _fields: {"hasWikiEnabled": True, "autoMergeAllowed": False},
        )

        self.assertEqual(
            [result.name for result in results if result.status == "failed"],
            ["hasWikiEnabled", "autoMergeAllowed"],
        )

    def test_reports_api_failure_for_each_dependent_check(self):
        def request(_repository, _fields):
            raise RuntimeError("API unavailable")

        results = CHECK_GITHUB_CONFIG.evaluate_checks(self.checks, "owner/repo", request=request)

        self.assertEqual([result.status for result in results], ["failed", "failed"])
        self.assertTrue(all("API unavailable" in result.message for result in results))

    def test_formats_expected_values_as_json(self):
        self.assertEqual(CHECK_GITHUB_CONFIG.format_value(False), "false")
        self.assertEqual(json.loads(CHECK_GITHUB_CONFIG.format_value({"enabled": True})), {"enabled": True})

    def test_rejects_repository_without_owner(self):
        with self.assertRaisesRegex(ValueError, "owner/name"):
            CHECK_GITHUB_CONFIG.repository_name("repository")


if __name__ == "__main__":
    unittest.main()
