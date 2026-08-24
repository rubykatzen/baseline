import importlib.util
import os
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import yaml

BASELINE_ROOT = Path(__file__).parent.parent


def load_action_module(name):
    path = BASELINE_ROOT / ".github" / "actions" / name / "prepare.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PR_TELEGRAM = load_action_module("prepare-telegram-pr-message")
ISSUE_TELEGRAM = load_action_module("prepare-telegram-issue-message")
RELEASE_TELEGRAM = load_action_module("prepare-telegram-release-message")


class TelegramPullRequestMessageTest(unittest.TestCase):
    def setUp(self):
        self.pull_request = {
            "number": 42,
            "title": "feat: add notifications",
            "author": {"login": "octocat"},
            "url": "https://github.com/owner/repo/pull/42",
            "isDraft": False,
        }

    def test_formats_opened_pull_request(self):
        message = PR_TELEGRAM.format_opened("owner/repo", self.pull_request, "opened")

        self.assertEqual(
            message,
            "*owner/repo* · [PR 42](https://github.com/owner/repo/pull/42) opened · "
            "*feat: add notifications* · octocat",
        )

    def test_formats_ready_and_reopened_pull_request_actions(self):
        self.assertIn("[PR 42](https://github.com/owner/repo/pull/42) ready", PR_TELEGRAM.format_opened("owner/repo", self.pull_request, "ready_for_review"))
        self.assertIn("[PR 42](https://github.com/owner/repo/pull/42) reopened", PR_TELEGRAM.format_opened("owner/repo", self.pull_request, "reopened"))

    def test_skips_draft_pull_request(self):
        self.pull_request["isDraft"] = True

        self.assertEqual(PR_TELEGRAM.format_opened("owner/repo", self.pull_request, "opened"), "")

    def test_formats_merged_pull_request(self):
        message = PR_TELEGRAM.format_merged("owner/repo", self.pull_request)

        self.assertEqual(
            message,
            "*owner/repo* · [PR 42](https://github.com/owner/repo/pull/42) merged · "
            "*feat: add notifications* · octocat",
        )

    def test_escapes_pull_request_values_for_telegram_markdown(self):
        self.pull_request["title"] = "fix: escape [markup] & text!"
        self.pull_request["author"] = {"login": "dependabot[bot]"}

        message = PR_TELEGRAM.format_opened("owner/repo", self.pull_request, "opened")

        self.assertIn(r"*fix: escape \[markup\] & text\!*", message)
        self.assertIn(r"dependabot\[bot\]", message)

    def test_open_pull_request_digest_excludes_drafts_and_reports_age(self):
        draft = dict(self.pull_request, number=41, isDraft=True)
        message = PR_TELEGRAM.format_digest(
            "owner/repo",
            [draft, self.pull_request | {"createdAt": "2026-08-10T12:00:00Z"}],
            now=datetime(2026, 8, 12, 12, tzinfo=timezone.utc),
        )

        self.assertIn("1 open PR", message)
        self.assertTrue(message.startswith("*owner/repo*"))
        self.assertIn("octocat · 2d", message)
        self.assertNotIn("#41", message)
        self.assertNotIn("more", message)

    def test_open_pull_request_digest_is_empty_without_targets(self):
        self.assertEqual(PR_TELEGRAM.format_digest("owner/repo", []), "")

    def test_open_pull_request_digest_lists_at_most_ten_pull_requests(self):
        pull_requests = [
            self.pull_request
            | {
                "number": number,
                "url": f"https://github.com/owner/repo/pull/{number}",
                "createdAt": "2026-08-10T12:00:00Z",
            }
            for number in range(1, 13)
        ]

        message = PR_TELEGRAM.format_digest("owner/repo", pull_requests)

        self.assertIn("12 open PRs", message)
        self.assertIn("[PR 10](https://github.com/owner/repo/pull/10) *feat: add notifications*", message)
        self.assertNotIn("[PR 11](https://github.com/owner/repo/pull/11) *feat: add notifications*", message)
        self.assertIn(r"[\.\.\.and 2 more](https://github.com/owner/repo/pulls)", message)

    def test_open_pull_request_digest_stays_within_telegram_limit(self):
        pull_requests = [
            self.pull_request
            | {
                "number": number,
                "title": "x" * 1000,
                "createdAt": "2026-08-10T12:00:00Z",
            }
            for number in range(1, 11)
        ]

        message = PR_TELEGRAM.format_digest("owner/repo", pull_requests)

        self.assertLessEqual(len(message), PR_TELEGRAM.TELEGRAM_MESSAGE_LIMIT)
        self.assertIn("more]", message)

    def test_writes_multiline_github_output(self):
        with tempfile.NamedTemporaryFile() as output, patch.dict(os.environ, {"GITHUB_OUTPUT": output.name}):
            PR_TELEGRAM.write_output("first\nsecond")
            value = Path(output.name).read_text()

        self.assertRegex(value, r"^message<<ghdelim_[0-9a-f]+\nfirst\nsecond\nghdelim_[0-9a-f]+\n$")


class TelegramIssueMessageTest(unittest.TestCase):

    def test_closed_issue_includes_body(self):
        issue = {
            "number": 12,
            "title": "Move notifications",
            "body": "Resolution summary.",
            "url": "https://github.com/owner/repo/issues/12",
        }

        message = ISSUE_TELEGRAM.format_closed("owner/repo", issue, "octocat")

        self.assertEqual(
            message,
            "*owner/repo* · [issue 12](https://github.com/owner/repo/issues/12) closed · "
            "*Move notifications* · octocat\nResolution summary\\.",
        )

    def test_closed_issue_truncates_long_body(self):
        issue = {
            "number": 12,
            "title": "Move notifications",
            "body": "x" * (ISSUE_TELEGRAM.ISSUE_BODY_LIMIT + 10),
            "url": "https://github.com/owner/repo/issues/12",
        }

        message = ISSUE_TELEGRAM.format_closed("owner/repo", issue, "octocat")
        body = ISSUE_TELEGRAM.truncate(issue["body"], ISSUE_TELEGRAM.ISSUE_BODY_LIMIT)

        self.assertEqual(len(body), ISSUE_TELEGRAM.ISSUE_BODY_LIMIT)
        self.assertTrue(body.endswith("..."))
        self.assertTrue(message.endswith(r"\.\.\."))

    def test_closed_issue_uses_only_first_body_paragraph(self):
        issue = {
            "number": 12,
            "title": "Fix [alerts]",
            "body": "First line.\nContinued *line*.\n\nIgnored paragraph.",
            "url": "https://github.com/owner/repo/issues/12",
        }

        message = ISSUE_TELEGRAM.format_closed("owner/repo", issue, "dependabot[bot]")

        self.assertIn(r"*Fix \[alerts\]*", message)
        self.assertTrue(message.endswith("dependabot\\[bot\\]\nFirst line\\. Continued \\*line\\*\\."))
        self.assertNotIn("Ignored", message)

    def test_closed_issue_includes_leading_heading_and_first_paragraph(self):
        issue = {
            "number": 12,
            "title": "Move notifications",
            "body": "## Resolution\n\nFirst line.\nContinued line.\n\nIgnored paragraph.",
            "url": "https://github.com/owner/repo/issues/12",
        }

        message = ISSUE_TELEGRAM.format_closed("owner/repo", issue, "octocat")

        self.assertTrue(message.endswith("\nResolution\nFirst line\\. Continued line\\."))
        self.assertNotIn("Ignored", message)


class TelegramReleaseMessageTest(unittest.TestCase):
    def test_formats_release_without_repeating_tag_as_name(self):
        release = {
            "tag": "v1.2.3",
            "name": "v1.2.3",
            "url": "https://github.com/owner/repo/releases/tag/v1.2.3",
            "actor": "octocat",
        }

        message = RELEASE_TELEGRAM.format_published("owner/repo", release)

        self.assertEqual(
            message,
            "*owner/repo* · [release v1\\.2\\.3](https://github.com/owner/repo/releases/tag/v1.2.3) "
            "published · octocat",
        )

    def test_formats_distinct_release_name_and_escapes_markdown(self):
        release = {
            "tag": "v1.2.3",
            "name": "Summer [release]",
            "url": "https://github.com/owner/repo/releases/tag/v1.2.3",
            "actor": "dependabot[bot]",
        }

        message = RELEASE_TELEGRAM.format_published("owner/repo", release)

        self.assertIn(r"*Summer \[release\]*", message)
        self.assertTrue(message.endswith(r"dependabot\[bot\]"))


class TelegramWorkflowTest(unittest.TestCase):
    def load_workflow(self, name):
        with open(BASELINE_ROOT / ".github" / "workflows" / name) as workflow:
            return yaml.safe_load(workflow)

    def test_pr_workflow_prepares_and_sends_supported_events(self):
        workflow = self.load_workflow("notify-telegram-pr-shared.yml")
        job = workflow["jobs"]["notify"]
        steps = job["steps"]

        self.assertEqual(set(workflow["jobs"]), {"notify"})
        self.assertIn("pull_request_target", job["if"])
        self.assertIn("merged == true", job["if"])
        self.assertIn("schedule", job["if"])
        self.assertEqual(
            [step["uses"] for step in steps],
            [
                "$/.github/actions/prepare-telegram-pr-message",
                "$/.github/actions/send-telegram-message",
            ],
        )
        self.assertEqual(steps[-1]["with"]["parse-mode"], "MarkdownV2")

    def test_issue_workflow_only_sends_closed_issue_notification(self):
        workflow = self.load_workflow("notify-telegram-issue-shared.yml")
        job = workflow["jobs"]["notify-closed"]

        self.assertIn("github.event_name == 'issues'", job["if"])
        self.assertIn("github.event.action == 'closed'", job["if"])
        self.assertEqual(job["permissions"], {"issues": "read"})
        self.assertEqual(
            [step["uses"] for step in job["steps"]],
            [
                "$/.github/actions/prepare-telegram-issue-message",
                "$/.github/actions/send-telegram-message",
            ],
        )
        self.assertEqual(job["steps"][-1]["with"]["parse-mode"], "MarkdownV2")

    def test_release_workflow_only_sends_published_release_notification(self):
        workflow = self.load_workflow("notify-telegram-release-shared.yml")
        job = workflow["jobs"]["notify"]

        self.assertIn("github.event_name == 'release'", job["if"])
        self.assertIn("github.event.action == 'published'", job["if"])
        self.assertEqual(job["permissions"], {})
        self.assertEqual(
            [step["uses"] for step in job["steps"]],
            [
                "$/.github/actions/prepare-telegram-release-message",
                "$/.github/actions/send-telegram-message",
            ],
        )
        self.assertEqual(job["steps"][-1]["with"]["parse-mode"], "MarkdownV2")

    def test_baseline_callers_pass_only_explicit_telegram_secrets(self):
        for name in ("notify-telegram-pr.yml", "notify-telegram-release.yml"):
            path = BASELINE_ROOT / ".github" / "workflows" / name
            content = path.read_text()
            workflow = yaml.safe_load(content)
            secrets = workflow["jobs"]["notify"]["secrets"]

            with self.subTest(name=name):
                self.assertEqual(set(secrets), {"TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"})
                self.assertNotIn("secrets: inherit", content)

    def test_baseline_release_caller_uses_published_event(self):
        content = (BASELINE_ROOT / ".github" / "workflows" / "notify-telegram-release.yml").read_text()

        self.assertIn("release:\n    types: [published]", content)
        self.assertIn("uses: ./.github/workflows/notify-telegram-release-shared.yml", content)

    def test_internal_actions_separate_formatting_and_delivery(self):
        action_root = BASELINE_ROOT / ".github" / "actions"
        telegram_actions = sorted(path.parent.name for path in action_root.glob("*telegram*/action.yml"))
        pr_action = (action_root / "prepare-telegram-pr-message" / "action.yml").read_text()
        issue_action = (action_root / "prepare-telegram-issue-message" / "action.yml").read_text()
        release_action = (action_root / "prepare-telegram-release-message" / "action.yml").read_text()
        send_action = (action_root / "send-telegram-message" / "action.yml").read_text()

        self.assertEqual(
            telegram_actions,
            [
                "prepare-telegram-issue-message",
                "prepare-telegram-pr-message",
                "prepare-telegram-release-message",
                "send-telegram-message",
            ],
        )
        self.assertIn('run: python3 "${{ github.action_path }}/prepare.py"', pr_action)
        self.assertIn('run: python3 "${{ github.action_path }}/prepare.py"', issue_action)
        self.assertIn('run: python3 "${{ github.action_path }}/prepare.py"', release_action)
        self.assertNotIn("api.telegram.org", pr_action)
        self.assertNotIn("api.telegram.org", issue_action)
        self.assertNotIn("api.telegram.org", release_action)
        self.assertIn("inputs:\n  message:", send_action)
        self.assertIn("parse-mode:", send_action)
        self.assertIn("parse_mode", send_action)
        self.assertIn("--output /dev/null", send_action)
        self.assertIn("api.telegram.org", send_action)


if __name__ == "__main__":
    unittest.main()
