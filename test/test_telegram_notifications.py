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
            '🆕 owner/repo — PR opened · <a href="https://github.com/owner/repo/pull/42">#42</a> '
            "<b>feat: add notifications</b> · octocat",
        )

    def test_formats_ready_and_reopened_pull_request_actions(self):
        self.assertIn("🆗 owner/repo — PR ready for review", PR_TELEGRAM.format_opened("owner/repo", self.pull_request, "ready_for_review"))
        self.assertIn("🆙 owner/repo — PR reopened", PR_TELEGRAM.format_opened("owner/repo", self.pull_request, "reopened"))

    def test_skips_draft_pull_request(self):
        self.pull_request["isDraft"] = True

        self.assertEqual(PR_TELEGRAM.format_opened("owner/repo", self.pull_request, "opened"), "")

    def test_formats_merged_pull_request(self):
        message = PR_TELEGRAM.format_merged("owner/repo", self.pull_request)

        self.assertEqual(
            message,
            '🔀 owner/repo — PR merged · <a href="https://github.com/owner/repo/pull/42">#42</a> '
            "<b>feat: add notifications</b> · octocat",
        )

    def test_escapes_pull_request_values_for_telegram_html(self):
        self.pull_request["title"] = "fix: escape <markup> & text"
        self.pull_request["author"] = {"login": "bot&name"}

        message = PR_TELEGRAM.format_opened("owner/repo", self.pull_request, "opened")

        self.assertIn("<b>fix: escape &lt;markup&gt; &amp; text</b>", message)
        self.assertIn("bot&amp;name", message)

    def test_open_pull_request_digest_excludes_drafts_and_reports_age(self):
        draft = dict(self.pull_request, number=41, isDraft=True)
        message = PR_TELEGRAM.format_digest(
            "owner/repo",
            [draft, self.pull_request | {"createdAt": "2026-08-10T12:00:00Z"}],
            now=datetime(2026, 8, 12, 12, tzinfo=timezone.utc),
        )

        self.assertIn("1 open PR", message)
        self.assertTrue(message.startswith("🔠 owner/repo"))
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
        self.assertIn('pull/10">#10</a> <b>feat: add notifications</b>', message)
        self.assertNotIn('pull/11">#11</a> <b>feat: add notifications</b>', message)
        self.assertIn('href="https://github.com/owner/repo/pulls">...and 2 more</a>', message)

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
        self.assertIn("more</a>", message)

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

        self.assertIn("#12 Move notifications\nResolution summary.\noctocat ·", message)

    def test_closed_issue_truncates_long_body(self):
        issue = {
            "number": 12,
            "title": "Move notifications",
            "body": "x" * (ISSUE_TELEGRAM.ISSUE_BODY_LIMIT + 10),
            "url": "https://github.com/owner/repo/issues/12",
        }

        message = ISSUE_TELEGRAM.format_closed("owner/repo", issue, "octocat")
        body = message.splitlines()[2]

        self.assertEqual(len(body), ISSUE_TELEGRAM.ISSUE_BODY_LIMIT)
        self.assertTrue(body.endswith("..."))


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
        self.assertEqual(steps[-1]["with"]["parse-mode"], "HTML")

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

    def test_baseline_caller_passes_only_explicit_telegram_secrets(self):
        path = BASELINE_ROOT / ".github" / "workflows" / "notify-telegram-pr.yml"
        content = path.read_text()
        workflow = yaml.safe_load(content)
        secrets = workflow["jobs"]["notify"]["secrets"]

        self.assertEqual(set(secrets), {"TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"})
        self.assertNotIn("secrets: inherit", content)

    def test_internal_actions_separate_formatting_and_delivery(self):
        action_root = BASELINE_ROOT / ".github" / "actions"
        telegram_actions = sorted(path.parent.name for path in action_root.glob("*telegram*/action.yml"))
        pr_action = (action_root / "prepare-telegram-pr-message" / "action.yml").read_text()
        issue_action = (action_root / "prepare-telegram-issue-message" / "action.yml").read_text()
        send_action = (action_root / "send-telegram-message" / "action.yml").read_text()

        self.assertEqual(
            telegram_actions,
            ["prepare-telegram-issue-message", "prepare-telegram-pr-message", "send-telegram-message"],
        )
        self.assertIn('run: python3 "${{ github.action_path }}/prepare.py"', pr_action)
        self.assertIn('run: python3 "${{ github.action_path }}/prepare.py"', issue_action)
        self.assertNotIn("api.telegram.org", pr_action)
        self.assertNotIn("api.telegram.org", issue_action)
        self.assertIn("inputs:\n  message:", send_action)
        self.assertIn("parse-mode:", send_action)
        self.assertIn("parse_mode", send_action)
        self.assertIn("--output /dev/null", send_action)
        self.assertIn("api.telegram.org", send_action)


if __name__ == "__main__":
    unittest.main()
