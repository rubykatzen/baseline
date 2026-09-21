import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import yaml

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
            "deleteBranchOnMerge": True,
        }

    def test_loads_repository_config(self):
        checks = CHECK_GITHUB_CONFIG.load_config(BASELINE_ROOT / "config" / "github.yml")

        self.assertEqual(
            set(checks),
            {
                "hasWikiEnabled",
                "deleteBranchOnMerge",
                "mergeCommitAllowed",
                "rebaseMergeAllowed",
                "squashMergeAllowed",
                "squashMergeCommitMessage",
                "squashMergeCommitTitle",
                "labels",
                "types",
            },
        )
        self.assertIn("deps", checks["labels"]["required"])
        self.assertIn("autorelease: pending", checks["labels"]["optional"])
        self.assertEqual(
            checks["labels"]["required"]["deps"]["description"],
            "Pull requests that update a dependency file",
        )
        self.assertIn("Task", checks["types"]["required"])
        self.assertIn("Epic", checks["types"]["optional"])
        self.assertEqual(checks["types"]["required"]["Task"]["color"], "BLUE")

    def test_shared_workflow_grants_permissions_for_repository_and_label_checks(self):
        with open(BASELINE_ROOT / ".github" / "workflows" / "github-shared.yml") as workflow_file:
            workflow = yaml.safe_load(workflow_file)

        permissions = workflow["jobs"]["github-config-check"]["permissions"]

        self.assertEqual(permissions, {"contents": "read", "issues": "read"})

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

    def test_rejects_missing_issues_mapping(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml") as config:
            config.write("config:\n  hasWikiEnabled: false\n")
            config.flush()

            with self.assertRaisesRegex(ValueError, "must contain an issues mapping"):
                CHECK_GITHUB_CONFIG.load_config(config.name)

    def test_rejects_invalid_label_color(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml") as config:
            config.write(
                "config:\n  hasWikiEnabled: false\n"
                "issues:\n  labels:\n    required:\n      deps:\n"
                "        color: blue\n        description: Dependency updates\n"
            )
            config.flush()

            with self.assertRaisesRegex(ValueError, "six-digit hex"):
                CHECK_GITHUB_CONFIG.load_config(config.name)

    def test_rejects_missing_label_description(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml") as config:
            config.write(
                "config:\n  hasWikiEnabled: false\n"
                "issues:\n  labels:\n    required:\n      deps:\n        color: 0366d6\n"
            )
            config.flush()

            with self.assertRaisesRegex(ValueError, "color and description"):
                CHECK_GITHUB_CONFIG.load_config(config.name)

    def test_rejects_missing_types_mapping(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml") as config:
            config.write(
                "config:\n  hasWikiEnabled: false\n"
                "issues:\n  labels:\n    required:\n      deps:\n"
                "        color: 0366d6\n        description: Dependency updates\n"
            )
            config.flush()

            with self.assertRaisesRegex(ValueError, "must contain an issues.types mapping"):
                CHECK_GITHUB_CONFIG.load_config(config.name)

    def test_rejects_invalid_type_color(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml") as config:
            config.write(
                "config:\n  hasWikiEnabled: false\n"
                "issues:\n"
                "  labels:\n    required:\n      deps:\n"
                "        color: 0366d6\n        description: Dependency updates\n"
                "  types:\n    required:\n      Task:\n"
                "        color: blue\n        description: A specific piece of work\n"
            )
            config.flush()

            with self.assertRaisesRegex(ValueError, "one of"):
                CHECK_GITHUB_CONFIG.load_config(config.name)

    def test_rejects_missing_type_description(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml") as config:
            config.write(
                "config:\n  hasWikiEnabled: false\n"
                "issues:\n"
                "  labels:\n    required:\n      deps:\n"
                "        color: 0366d6\n        description: Dependency updates\n"
                "  types:\n    required:\n      Task:\n        color: BLUE\n"
            )
            config.flush()

            with self.assertRaisesRegex(ValueError, "color and description"):
                CHECK_GITHUB_CONFIG.load_config(config.name)

    def test_rejects_type_that_is_both_required_and_optional(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml") as config:
            config.write(
                "config:\n  hasWikiEnabled: false\n"
                "issues:\n"
                "  labels:\n    required:\n      deps:\n"
                "        color: 0366d6\n        description: Dependency updates\n"
                "  types:\n"
                "    required:\n      Task:\n        color: BLUE\n        description: A specific piece of work\n"
                "    optional:\n      Task:\n        color: BLUE\n        description: A specific piece of work\n"
            )
            config.flush()

            with self.assertRaisesRegex(ValueError, "cannot be both required and optional"):
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
            return {"hasWikiEnabled": False, "deleteBranchOnMerge": True}

        results = CHECK_GITHUB_CONFIG.evaluate_checks(self.checks, "owner/repo", request=request)

        self.assertEqual([result.status for result in results], ["passed", "passed"])
        self.assertEqual(requests, [("owner/repo", ["hasWikiEnabled", "deleteBranchOnMerge"])])

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
            request=lambda _repository, _fields: {"hasWikiEnabled": True, "deleteBranchOnMerge": False},
        )

        self.assertEqual(
            [result.name for result in results if result.status == "failed"],
            ["hasWikiEnabled", "deleteBranchOnMerge"],
        )

    def test_reports_api_failure_for_each_dependent_check(self):
        def request(_repository, _fields):
            raise RuntimeError("API unavailable")

        results = CHECK_GITHUB_CONFIG.evaluate_checks(self.checks, "owner/repo", request=request)

        self.assertEqual([result.status for result in results], ["failed", "failed"])
        self.assertTrue(all("API unavailable" in result.message for result in results))

    def test_label_policy_accepts_required_and_present_optional_labels(self):
        policy = {
            "required": {
                "deps": {"color": "0366d6", "description": "Dependency updates"}
            },
            "optional": {
                "autorelease: pending": {"color": "fbca04", "description": "Pending release"}
            },
        }
        result = CHECK_GITHUB_CONFIG.evaluate_label_check(
            policy,
            "owner/repo",
            request=lambda _repository: [
                {"name": "deps", "color": "0366D6", "description": "Dependency updates"},
                {"name": "autorelease: pending", "color": "fbca04", "description": "Pending release"},
            ],
        )

        self.assertEqual(result.status, "passed")

    def test_label_policy_accepts_absent_optional_labels(self):
        policy = {
            "required": {
                "deps": {"color": "0366d6", "description": "Dependency updates"}
            },
            "optional": {
                "autorelease: pending": {"color": "fbca04", "description": "Pending release"}
            },
        }
        result = CHECK_GITHUB_CONFIG.evaluate_label_check(
            policy,
            "owner/repo",
            request=lambda _repository: [
                {"name": "deps", "color": "0366d6", "description": "Dependency updates"}
            ],
        )

        self.assertEqual(result.status, "passed")

    def test_label_policy_reports_all_differences(self):
        policy = {
            "required": {
                "deps": {"color": "0366d6", "description": "Dependency updates"},
                "size: S": {"color": "bfd4f2", "description": "Less than an hour"},
            },
            "optional": {
                "autorelease: pending": {"color": "fbca04", "description": "Pending release"}
            },
        }
        result = CHECK_GITHUB_CONFIG.evaluate_label_check(
            policy,
            "owner/repo",
            request=lambda _repository: [
                {"name": "deps", "color": "ffffff", "description": None},
                {"name": "bug", "color": "d73a4a", "description": "Something is broken"},
            ],
        )

        self.assertEqual(result.status, "failed")
        self.assertIn("missing: size: S", result.message)
        self.assertIn("unexpected: bug", result.message)
        self.assertIn("deps expected #0366d6, got #ffffff", result.message)
        self.assertIn('deps expected "Dependency updates", got ""', result.message)

    def test_skips_label_policy_without_requesting_labels(self):
        results = CHECK_GITHUB_CONFIG.evaluate_checks(
            {"labels": {"required": {}, "optional": {}}},
            "owner/repo",
            {"labels"},
            request=lambda _repository, _fields: {},
            labels_request=lambda _repository: self.fail("skipped check made an API request"),
        )

        self.assertEqual(results[0].status, "skipped")

    def test_type_policy_accepts_required_and_present_optional_types(self):
        policy = {
            "required": {"Task": {"color": "BLUE", "description": "A specific piece of work"}},
            "optional": {"Epic": {"color": "PURPLE", "description": "A goal split into sub-issues"}},
        }
        result = CHECK_GITHUB_CONFIG.evaluate_type_check(
            policy,
            "owner/repo",
            request=lambda _repository: [
                {"name": "Task", "color": "BLUE", "description": "A specific piece of work", "isEnabled": True},
                {
                    "name": "Epic",
                    "color": "PURPLE",
                    "description": "A goal split into sub-issues",
                    "isEnabled": True,
                },
            ],
        )

        self.assertEqual(result.status, "passed")

    def test_type_policy_accepts_absent_optional_types(self):
        policy = {
            "required": {"Task": {"color": "BLUE", "description": "A specific piece of work"}},
            "optional": {"Epic": {"color": "PURPLE", "description": "A goal split into sub-issues"}},
        }
        result = CHECK_GITHUB_CONFIG.evaluate_type_check(
            policy,
            "owner/repo",
            request=lambda _repository: [
                {"name": "Task", "color": "BLUE", "description": "A specific piece of work", "isEnabled": True}
            ],
        )

        self.assertEqual(result.status, "passed")

    def test_type_policy_ignores_disabled_types(self):
        policy = {
            "required": {"Task": {"color": "BLUE", "description": "A specific piece of work"}},
            "optional": {},
        }
        result = CHECK_GITHUB_CONFIG.evaluate_type_check(
            policy,
            "owner/repo",
            request=lambda _repository: [
                {"name": "Task", "color": "BLUE", "description": "A specific piece of work", "isEnabled": True},
                {"name": "Idea", "color": "ORANGE", "description": "A product idea", "isEnabled": False},
            ],
        )

        self.assertEqual(result.status, "passed")

    def test_type_policy_reports_all_differences(self):
        policy = {
            "required": {
                "Task": {"color": "BLUE", "description": "A specific piece of work"},
                "Bug": {"color": "RED", "description": "An unexpected problem or behavior"},
            },
            "optional": {"Epic": {"color": "PURPLE", "description": "A goal split into sub-issues"}},
        }
        result = CHECK_GITHUB_CONFIG.evaluate_type_check(
            policy,
            "owner/repo",
            request=lambda _repository: [
                {"name": "Task", "color": "GREEN", "description": None, "isEnabled": True},
                {"name": "Research", "color": "GREEN", "description": "An inquiry", "isEnabled": True},
            ],
        )

        self.assertEqual(result.status, "failed")
        self.assertIn("missing: Bug", result.message)
        self.assertNotIn("unexpected", result.message)
        self.assertIn("Task expected BLUE, got GREEN", result.message)
        self.assertIn('Task expected "A specific piece of work", got ""', result.message)

    def test_type_policy_ignores_types_outside_the_policy(self):
        policy = {
            "required": {"Task": {"color": "BLUE", "description": "A specific piece of work"}},
            "optional": {},
        }
        result = CHECK_GITHUB_CONFIG.evaluate_type_check(
            policy,
            "owner/repo",
            request=lambda _repository: [
                {"name": "Task", "color": "BLUE", "description": "A specific piece of work", "isEnabled": True},
                {"name": "Book", "color": "YELLOW", "description": "A book to read", "isEnabled": True},
                {"name": "Guitar", "color": "YELLOW", "description": "A song to learn", "isEnabled": True},
            ],
        )

        self.assertEqual(result.status, "passed")

    def test_skips_type_policy_without_requesting_types(self):
        results = CHECK_GITHUB_CONFIG.evaluate_checks(
            {"types": {"required": {}, "optional": {}}},
            "owner/repo",
            {"types"},
            request=lambda _repository, _fields: {},
            types_request=lambda _repository: self.fail("skipped check made an API request"),
        )

        self.assertEqual(results[0].status, "skipped")

    def test_formats_expected_values_as_json(self):
        self.assertEqual(CHECK_GITHUB_CONFIG.format_value(False), "false")
        self.assertEqual(json.loads(CHECK_GITHUB_CONFIG.format_value({"enabled": True})), {"enabled": True})

    def test_rejects_repository_without_owner(self):
        with self.assertRaisesRegex(ValueError, "owner/name"):
            CHECK_GITHUB_CONFIG.repository_name("repository")


if __name__ == "__main__":
    unittest.main()
