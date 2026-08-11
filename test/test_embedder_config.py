import importlib.util
import tempfile
import unittest
from pathlib import Path

BASELINE_ROOT = Path(__file__).parent.parent
SPEC = importlib.util.spec_from_file_location(
    "check_embedder", BASELINE_ROOT / ".github" / "actions" / "check-embedder" / "check.py"
)
CHECK_EMBEDDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK_EMBEDDER)


class EmbedderConfigTest(unittest.TestCase):
    def setUp(self):
        self.fragments = {
            "heading": CHECK_EMBEDDER.Fragment(path="AGENTS.md", content="# Agents\n"),
            "rule": CHECK_EMBEDDER.Fragment(path="AGENTS.md", content="Required rule\n"),
        }

    def test_loads_embedder_config(self):
        fragments = CHECK_EMBEDDER.load_config(BASELINE_ROOT / "config" / "embedder.yml")

        self.assertEqual(
            set(fragments),
            {"message-prefix", "embedded-fragment-policy", "embedded-fragments", "dependabot"},
        )
        self.assertEqual(fragments["message-prefix"].path, "AGENTS.md")
        self.assertEqual(fragments["embedded-fragment-policy"].path, "AGENTS.md")

    def test_rejects_invalid_config(self):
        invalid_configs = (
            "fragments: []\n",
            "fragments:\n  example:\n    path: /AGENTS.md\n    content: required\n",
            "fragments:\n  example:\n    path: AGENTS.md\n",
            "fragments:\n  example:\n    path: AGENTS.md\n    content: ''\n",
        )
        for value in invalid_configs:
            with self.subTest(value=value), tempfile.NamedTemporaryFile(
                mode="w", suffix=".yml"
            ) as config:
                config.write(value)
                config.flush()

                with self.assertRaises(ValueError):
                    CHECK_EMBEDDER.load_config(config.name)

    def test_rejects_malformed_yaml(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml") as config:
            config.write("fragments: [\n")
            config.flush()

            with self.assertRaisesRegex(ValueError, "must be valid YAML"):
                CHECK_EMBEDDER.load_config(config.name)

    def test_parses_json_skip(self):
        self.assertEqual(CHECK_EMBEDDER.parse_json_list('["heading"]'), {"heading"})

    def test_rejects_invalid_json_skip(self):
        for value in ('"heading"', "heading", '["heading", 1]'):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "JSON array of strings"):
                CHECK_EMBEDDER.parse_json_list(value)

    def test_rejects_unknown_skip(self):
        with self.assertRaisesRegex(ValueError, "Unknown skipped embedder fragments: typo"):
            CHECK_EMBEDDER.evaluate_fragments(self.fragments, ".", {"typo"})

    def test_multiple_fragments_can_target_one_file_and_reuse_read(self):
        reads = []

        def read(root, path):
            reads.append((root, path))
            return "# Agents\n\nRequired rule\n"

        results = CHECK_EMBEDDER.evaluate_fragments(self.fragments, "/repo", read=read)

        self.assertEqual([result.status for result in results], ["passed", "passed"])
        self.assertEqual(reads, [("/repo", "AGENTS.md")])

    def test_reports_each_missing_fragment(self):
        results = CHECK_EMBEDDER.evaluate_fragments(
            self.fragments, ".", read=lambda _root, _path: "unrelated\n"
        )

        self.assertEqual(
            [result.name for result in results if result.status == "failed"],
            ["heading", "rule"],
        )

    def test_reports_missing_file(self):
        def read(_root, _path):
            raise RuntimeError("file does not exist")

        results = CHECK_EMBEDDER.evaluate_fragments(self.fragments, ".", read=read)

        self.assertTrue(all(result.status == "failed" for result in results))
        self.assertTrue(all(result.message == "file does not exist" for result in results))

    def test_skips_named_fragment(self):
        results = CHECK_EMBEDDER.evaluate_fragments(
            self.fragments,
            ".",
            {"rule"},
            read=lambda _root, _path: "# Agents\n",
        )

        self.assertEqual([result.status for result in results], ["passed", "skipped"])

    def test_skipping_all_fragments_does_not_read_target(self):
        results = CHECK_EMBEDDER.evaluate_fragments(
            {"heading": self.fragments["heading"]},
            ".",
            {"heading"},
            read=lambda _root, _path: self.fail("skipped check read its target"),
        )

        self.assertEqual(results[0].status, "skipped")


if __name__ == "__main__":
    unittest.main()
