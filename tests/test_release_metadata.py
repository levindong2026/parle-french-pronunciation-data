import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_BASE = (
    "https://github.com/levindong2026/parle-french-pronunciation-data/"
    "releases/download/v2026.08.27/"
)

TEACHING_ASSETS = {
    "french-sound-chart-teacher-reference": {
        "filename": "french-sound-chart-teacher-reference.pdf",
        "bytes": 53712,
        "hash": "sha256:cb46d629984e169ee356ad416470802460d33d0fac05a91e4d5f2732acd6bf20",
    },
    "parle-french-sound-chart-open-teaching-pack": {
        "filename": "parle-french-sound-chart-open-teaching-pack.zip",
        "bytes": 445935,
        "hash": "sha256:1d9f22ed19ef84d2dfa2c00414846d07fab401e66221464b13e36ba9cbba2e7b",
    },
    "parle-french-u-y-learner-worksheet": {
        "filename": "parle-french-u-y-learner-worksheet.pdf",
        "bytes": 31156,
        "hash": "sha256:04069eeb620e90035c9c558b21641b47ec631dfcb43ef97dfe9c99ac51266c44",
    },
    "parle-french-u-y-answer-key": {
        "filename": "parle-french-u-y-answer-key.pdf",
        "bytes": 28520,
        "hash": "sha256:cfb5530eabcf98666a3534ba0ebfe3eb15b89fe8dd42468d119651c391ac154e",
    },
}


class ReleaseMetadataTests(unittest.TestCase):
    def test_english_and_french_readmes_discover_the_open_teaching_assets(self):
        for filename in ("README.md", "README.fr.md"):
            text = (ROOT / filename).read_text(encoding="utf-8")
            for asset in TEACHING_ASSETS.values():
                self.assertIn(RELEASE_BASE + asset["filename"], text, filename)
            self.assertIn("https://getparle.app/french-pronunciation-teaching-resources/", text)
            self.assertIn("https://getparle.app/ressources-pedagogiques-prononciation-francaise/", text)

    def test_machine_readable_metadata_describes_every_teaching_asset(self):
        package = json.loads((ROOT / "datapackage.json").read_text(encoding="utf-8"))
        resources = {item["name"]: item for item in package["resources"]}
        for name, expected in TEACHING_ASSETS.items():
            self.assertIn(name, resources)
            resource = resources[name]
            self.assertEqual(resource["path"], RELEASE_BASE + expected["filename"])
            self.assertEqual(resource["bytes"], expected["bytes"])
            self.assertEqual(resource["hash"], expected["hash"])

        citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        self.assertIn("open teaching pack", citation.lower())
        self.assertIn('version: "v2026.08.27"', citation)

    def test_checksum_manifest_covers_the_five_sound_chart_teaching_files(self):
        manifest = (ROOT / "v2026.08.27-SHA256SUMS.txt").read_text(encoding="utf-8")
        rows = {
            filename: digest
            for digest, filename in (line.split("  ", 1) for line in manifest.splitlines())
        }
        self.assertEqual(len(rows), 5)
        for expected in TEACHING_ASSETS.values():
            self.assertEqual(rows[expected["filename"]], expected["hash"].removeprefix("sha256:"))


if __name__ == "__main__":
    unittest.main()
