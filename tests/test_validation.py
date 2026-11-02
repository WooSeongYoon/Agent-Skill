import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from common import read_document
from render_agents import check
from validate import validate


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT.parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "source"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def test_repository_is_valid(self):
        self.assertEqual(validate(self.root), [])

    def test_broken_reference_is_detected(self):
        file = self.root / "skills/qt-desktop/SKILL.md"
        with file.open("a", encoding="utf-8") as stream:
            stream.write("\n[Missing](references/does-not-exist.md)\n")
        self.assertTrue(any("Broken local link" in error for error in validate(self.root)))

    def test_duplicate_metadata_is_rejected(self):
        file = self.root / "agents/code-reviewer.md"
        file.write_text('---\nname: "one"\nname: "two"\n---\nbody\n', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            read_document(file)

    def test_stale_native_agent_is_detected(self):
        file = self.root / "adapters/codex/agents/code-reviewer.toml"
        file.write_text('name = "wrong"\n', encoding="utf-8")
        self.assertIn("adapters/codex/agents/code-reviewer.toml", check(self.root))

    def test_profile_referencing_missing_skill_is_detected(self):
        file = self.root / "harness.json"
        data = json.loads(file.read_text())
        data["profiles"]["python"].append("missing-skill")
        file.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(any("Manifest/skills mismatch" in error for error in validate(self.root)))

    def test_evaluation_unknown_skill_is_detected(self):
        file = self.root / "evals/cases.json"
        data = json.loads(file.read_text())
        data[0]["expected_skills"].append("invented-skill")
        file.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(any("Invalid evaluation case" in error for error in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
