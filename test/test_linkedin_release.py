import importlib.util
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

BASELINE_ROOT = Path(__file__).parent.parent


def load_action_module(action, module):
    path = BASELINE_ROOT / ".github" / "actions" / action / module
    spec = importlib.util.spec_from_file_location(action, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


PREPARE = load_action_module("prepare-linkedin-release-post", "prepare.py")
SEND = load_action_module("send-linkedin-post", "send.py")


class FakeResponse:
    def __init__(self, body=b"", headers=None, status=200):
        self.body = body
        self.headers = headers or {}
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, _size=-1):
        return self.body


class LinkedInReleasePostTest(unittest.TestCase):
    def setUp(self):
        self.release = {
            "tag": "v0.18.0",
            "name": "v0.18.0",
            "url": "https://github.com/owner/repo/releases/tag/v0.18.0",
            "body": (
                "## [0.18.0](https://github.com/owner/repo/compare/v0.17.0...v0.18.0) (2026-09-01)\n\n"
                "### Features\n\n"
                "* publish releases to LinkedIn "
                "([#193](https://github.com/owner/repo/issues/193))\n\n"
                "Release automation stays deterministic."
            ),
        }

    def test_formats_release_please_body_as_plain_text(self):
        message = PREPARE.format_published("owner/repo", self.release)

        self.assertEqual(
            message,
            "owner/repo v0.18.0\n\n"
            "Features\n\n"
            "• publish releases to LinkedIn (#193)\n\n"
            "Release automation stays deterministic.\n\n"
            "https://github.com/owner/repo/releases/tag/v0.18.0",
        )
        self.assertNotIn("[", message)

    def test_uses_distinct_release_name(self):
        self.release["name"] = "LinkedIn publishing"

        message = PREPARE.format_published("owner/repo", self.release)

        self.assertTrue(message.startswith("owner/repo LinkedIn publishing\n\n"))

    def test_formats_release_without_body(self):
        self.release["body"] = ""

        message = PREPARE.format_published("owner/repo", self.release)

        self.assertEqual(
            message,
            "owner/repo v0.18.0\n\nhttps://github.com/owner/repo/releases/tag/v0.18.0",
        )

    def test_truncates_body_and_preserves_release_url(self):
        self.release["body"] = "x" * 4000

        message = PREPARE.format_published("owner/repo", self.release)

        self.assertEqual(len(message), PREPARE.LINKEDIN_POST_LIMIT)
        self.assertIn("...\n\n", message)
        self.assertTrue(message.endswith(self.release["url"]))

    def test_writes_multiline_github_output(self):
        with tempfile.NamedTemporaryFile() as output, patch.dict(os.environ, {"GITHUB_OUTPUT": output.name}):
            PREPARE.write_output("first\nsecond")
            value = Path(output.name).read_text()

        self.assertRegex(value, r"^message<<ghdelim_[0-9a-f]+\nfirst\nsecond\nghdelim_[0-9a-f]+\n$")


class LinkedInSenderTest(unittest.TestCase):
    def test_resolves_person_urn_from_userinfo(self):
        requests = []

        def opener(request):
            requests.append(request)
            return FakeResponse(json.dumps({"sub": "member123"}).encode())

        person_urn = SEND.person_urn("secret-token", opener=opener)

        self.assertEqual(person_urn, "urn:li:person:member123")
        self.assertEqual(requests[0].full_url, SEND.USERINFO_URL)
        self.assertEqual(requests[0].get_header("Authorization"), "Bearer secret-token")

    def test_publishes_public_text_post(self):
        requests = []

        def opener(request):
            requests.append(request)
            return FakeResponse(headers={"x-restli-id": "urn:li:share:123"}, status=201)

        post_id = SEND.publish_post(
            "secret-token",
            "urn:li:person:member123",
            "Release text",
            opener=opener,
        )

        request = requests[0]
        payload = json.loads(request.data)
        self.assertEqual(post_id, "urn:li:share:123")
        self.assertEqual(request.full_url, SEND.POSTS_URL)
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.get_header("Linkedin-version"), SEND.LINKEDIN_API_VERSION)
        self.assertEqual(request.get_header("X-restli-protocol-version"), "2.0.0")
        self.assertEqual(payload["author"], "urn:li:person:member123")
        self.assertEqual(payload["commentary"], "Release text")
        self.assertEqual(payload["visibility"], "PUBLIC")
        self.assertEqual(payload["distribution"]["feedDistribution"], "MAIN_FEED")
        self.assertEqual(payload["lifecycleState"], "PUBLISHED")

    def test_rejects_create_response_without_post_id(self):
        with self.assertRaisesRegex(ValueError, "x-restli-id"):
            SEND.publish_post(
                "secret-token",
                "urn:li:person:member123",
                "Release text",
                opener=lambda _request: FakeResponse(status=201),
            )

    def test_requires_created_status(self):
        with self.assertRaisesRegex(ValueError, "expected 201"):
            SEND.publish_post(
                "secret-token",
                "urn:li:person:member123",
                "Release text",
                opener=lambda _request: FakeResponse(headers={"x-restli-id": "urn:li:share:123"}),
            )

    def test_writes_post_id_to_output_and_summary(self):
        with tempfile.NamedTemporaryFile() as output, tempfile.NamedTemporaryFile() as summary:
            with patch.dict(
                os.environ,
                {"GITHUB_OUTPUT": output.name, "GITHUB_STEP_SUMMARY": summary.name},
            ):
                SEND.write_output("urn:li:share:123")
                SEND.write_summary("urn:li:share:123")
            output_value = Path(output.name).read_text()
            summary_value = Path(summary.name).read_text()

        self.assertEqual(output_value, "post-id=urn:li:share:123\n")
        self.assertEqual(summary_value, "LinkedIn post published: `urn:li:share:123`\n")

    def test_http_error_diagnostic_does_not_include_token(self):
        error = __import__("urllib.error").error.HTTPError(
            SEND.POSTS_URL,
            401,
            "Unauthorized",
            {},
            io.BytesIO(b'{"message":"Expired token"}'),
        )

        try:
            detail = SEND.error_detail(error)
        finally:
            error.close()

        self.assertEqual(detail, 'LinkedIn API request failed with HTTP 401: {"message":"Expired token"}')


class LinkedInWorkflowTest(unittest.TestCase):
    def load_workflow(self, name):
        with open(BASELINE_ROOT / ".github" / "workflows" / name) as workflow:
            return yaml.safe_load(workflow)

    def test_shared_workflow_publishes_stable_releases(self):
        workflow = self.load_workflow("publish-linkedin-release-shared.yml")
        workflow_call = workflow[True]["workflow_call"]
        job = workflow["jobs"]["publish"]

        self.assertEqual(set(workflow_call["secrets"]), {"linkedin-access-token"})
        self.assertNotIn("inputs", workflow_call)
        self.assertEqual(workflow_call["outputs"]["post-id"]["value"], "${{ jobs.publish.outputs.post-id }}")
        self.assertIn("github.event_name == 'release'", job["if"])
        self.assertIn("github.event.release.prerelease == false", job["if"])
        self.assertEqual(job["permissions"], {})
        self.assertEqual(job["outputs"]["post-id"], "${{ steps.send.outputs.post-id }}")
        self.assertEqual(
            [step["uses"] for step in job["steps"]],
            [
                "$/.github/actions/prepare-linkedin-release-post",
                "$/.github/actions/send-linkedin-post",
            ],
        )

    def test_baseline_caller_passes_token_explicitly(self):
        path = BASELINE_ROOT / ".github" / "workflows" / "publish-linkedin-release.yml"
        content = path.read_text()
        workflow = yaml.safe_load(content)
        job = workflow["jobs"]["publish"]

        self.assertIn("release:\n    types: [published]", content)
        self.assertEqual(job["uses"], "./.github/workflows/publish-linkedin-release-shared.yml")
        self.assertEqual(
            job["secrets"],
            {"linkedin-access-token": "${{ secrets.LINKEDIN_ACCESS_TOKEN }}"},
        )
        self.assertNotIn("secrets: inherit", content)

    def test_actions_keep_formatting_and_delivery_separate(self):
        action_root = BASELINE_ROOT / ".github" / "actions"
        prepare_action = (action_root / "prepare-linkedin-release-post" / "action.yml").read_text()
        send_action = (action_root / "send-linkedin-post" / "action.yml").read_text()
        send_script = (action_root / "send-linkedin-post" / "send.py").read_text()

        self.assertIn('run: python3 "${{ github.action_path }}/prepare.py"', prepare_action)
        self.assertNotIn("api.linkedin.com", prepare_action)
        self.assertIn('run: python3 "${{ github.action_path }}/send.py"', send_action)
        self.assertIn("LINKEDIN_ACCESS_TOKEN", send_action)
        self.assertIn('LINKEDIN_API_VERSION = "202608"', send_script)
        self.assertNotIn("requests", send_script)


if __name__ == "__main__":
    unittest.main()
