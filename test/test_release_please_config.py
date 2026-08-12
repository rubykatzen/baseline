import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent


class ReleasePleaseConfigTest(unittest.TestCase):
    def test_manifest_matches_packaged_version(self):
        manifest = self.load_json(".release-please-manifest.json")
        version_file = (ROOT / "lib/baseline/version.rb").read_text()
        gemfile_lock = (ROOT / "Gemfile.lock").read_text()
        version = re.search(r'VERSION = "([^"]+)"', version_file).group(1)

        self.assertEqual(manifest, {".": version})
        self.assertIn(f"rubykatzen-baseline ({version})", gemfile_lock)

    def test_extra_files_have_version_annotations(self):
        config = self.load_json("release-please-config.json")
        version = self.load_json(".release-please-manifest.json")["."]
        package = config["packages"]["."]

        self.assertEqual(config["release-type"], "ruby")
        self.assertFalse(config["include-component-in-tag"])
        self.assertEqual(package["package-name"], "rubykatzen-baseline")
        self.assertEqual(package["version-file"], "lib/baseline/version.rb")

        for extra_file in package["extra-files"]:
            self.assertEqual(extra_file["type"], "generic")
            content = (ROOT / extra_file["path"]).read_text()
            self.assertIn(f"v{version} # x-release-please-version", content)

    def load_json(self, path):
        return json.loads((ROOT / path).read_text())


if __name__ == "__main__":
    unittest.main()
