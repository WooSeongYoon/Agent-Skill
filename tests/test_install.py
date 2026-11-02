import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from install import apply_plan, build_plan, digest, inspect_plan, safe_path


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT.parent)
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.target = self.base / "project"

    def plan(self, profiles=None, tools=None, **options):
        return build_plan(ROOT, profiles or ["qt"], tools or ["codex", "claude"], **options)

    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts/install.py"), "--target", str(self.target), *arguments],
            capture_output=True, text=True, encoding="utf-8", cwd=ROOT,
        )

    def test_preview_does_not_create_target(self):
        result = self.run_cli("--profiles", "qt")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Preview only", result.stdout)
        self.assertFalse(self.target.exists())

    def test_apply_cli_produces_project_scoped_files(self):
        result = self.run_cli("--profiles", "python", "--tools", "codex", "--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.target / "AGENTS.md").is_file())
        self.assertTrue((self.target / ".agents/skills/python-engineering/SKILL.md").is_file())
        self.assertFalse((self.target / ".claude").exists())

    def test_qt_profile_includes_python_but_not_ml_or_web(self):
        names = set(self.plan())
        self.assertIn(".agents/skills/python-engineering/SKILL.md", names)
        self.assertIn(".claude/skills/qt-desktop/SKILL.md", names)
        self.assertFalse(any("deep-learning" in name or "web-development" in name for name in names))

    def test_profiles_deduplicate_shared_python_dependency(self):
        plan = self.plan(["qt", "ml", "python"])
        self.assertEqual(sum(name.endswith("python-engineering/SKILL.md") for name in plan), 2)

    def test_unknown_profile_fails_without_writes(self):
        result = self.run_cli("--profiles", "unknown", "--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unknown profiles", result.stderr)
        self.assertFalse(self.target.exists())

    def test_empty_selection_is_rejected(self):
        with self.assertRaises(ValueError):
            build_plan(ROOT, [], ["codex"])
        with self.assertRaises(ValueError):
            build_plan(ROOT, ["python"], [])

    def test_apply_is_idempotent_and_preserves_timestamps(self):
        plan = self.plan()
        self.assertEqual(apply_plan(self.target, plan), len(plan))
        timestamps = {name: (self.target / name).stat().st_mtime_ns for name in plan}
        self.assertEqual(apply_plan(self.target, plan), 0)
        self.assertEqual(timestamps, {name: (self.target / name).stat().st_mtime_ns for name in plan})

    def test_conflict_aborts_entire_plan(self):
        self.target.mkdir()
        file = self.target / "AGENTS.md"
        file.write_text("User instructions", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "nothing written"):
            apply_plan(self.target, self.plan())
        self.assertEqual(file.read_text(), "User instructions")
        self.assertEqual(list(self.target.iterdir()), [file])

    def test_skip_instructions_keeps_existing_policies(self):
        self.target.mkdir()
        for name in ("AGENTS.md", "CLAUDE.md"):
            (self.target / name).write_text("Existing policy", encoding="utf-8")
        apply_plan(self.target, self.plan(skip_instructions=True))
        self.assertEqual((self.target / "AGENTS.md").read_text(), "Existing policy")
        self.assertEqual((self.target / "CLAUDE.md").read_text(), "Existing policy")
        self.assertTrue((self.target / ".harness/instructions.md").exists())

    def test_user_edited_project_facts_are_not_overwritten(self):
        plan = self.plan()
        apply_plan(self.target, plan)
        file = self.target / ".harness/project.json"
        file.write_text('{"custom": true}\n', encoding="utf-8")
        with self.assertRaises(ValueError):
            apply_plan(self.target, plan)
        self.assertEqual(json.loads(file.read_text()), {"custom": True})

    def test_manifest_hashes_match_written_files(self):
        plan = self.plan(["full"], with_agents=True)
        apply_plan(self.target, plan)
        manifest = json.loads((self.target / ".harness/installed.json").read_text())
        for name, expected in manifest["files"].items():
            self.assertEqual(digest((self.target / name).read_bytes()), expected, name)

    def test_native_agents_are_optional_and_parse(self):
        self.assertFalse(any("/agents/" in name and name.endswith(".toml") for name in self.plan()))
        plan = self.plan(with_agents=True)
        native = [content for name, content in plan.items() if name.startswith(".codex/agents/")]
        self.assertEqual(len(native), 3)
        for content in native:
            self.assertIn("developer_instructions", tomllib.loads(content.decode()))
        self.assertEqual(sum(name.startswith(".claude/agents/") for name in plan), 3)

    def test_target_file_is_rejected(self):
        self.target.write_text("keep", encoding="utf-8")
        with self.assertRaises(ValueError):
            apply_plan(self.target, self.plan())
        self.assertEqual(self.target.read_text(), "keep")

    def test_parent_file_is_rejected_before_any_write(self):
        self.target.mkdir()
        (self.target / ".agents").write_text("keep", encoding="utf-8")
        with self.assertRaises(ValueError):
            apply_plan(self.target, self.plan())
        self.assertEqual(len(list(self.target.iterdir())), 1)

    def make_link(self, link, target, directory=False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except OSError as error:
            self.skipTest(f"Symbolic links unavailable: {error}")

    def test_linked_target_is_rejected(self):
        outside = self.base / "outside"
        outside.mkdir()
        self.make_link(self.target, outside, directory=True)
        with self.assertRaises(ValueError):
            apply_plan(self.target, self.plan())
        self.assertEqual(list(outside.iterdir()), [])

    def test_linked_parent_is_rejected(self):
        outside = self.base / "outside"
        outside.mkdir()
        linked = self.base / "linked"
        self.make_link(linked, outside, directory=True)
        with self.assertRaises(ValueError):
            apply_plan(linked / "child", self.plan())
        self.assertEqual(list(outside.iterdir()), [])

    def test_broken_destination_link_is_rejected(self):
        self.target.mkdir()
        self.make_link(self.target / "AGENTS.md", self.base / "missing")
        with self.assertRaises(ValueError):
            apply_plan(self.target, self.plan())
        self.assertFalse((self.base / "missing").exists())

    def test_linked_destination_directory_is_rejected(self):
        self.target.mkdir()
        outside = self.base / "outside"
        outside.mkdir()
        self.make_link(self.target / ".agents", outside, directory=True)
        with self.assertRaises(ValueError):
            apply_plan(self.target, self.plan())
        self.assertEqual(list(outside.iterdir()), [])

    def test_path_traversal_and_platform_paths_are_rejected(self):
        for relative in ("../escape", "/absolute", "C:/escape", "a/../../escape", "a\\escape", "./file"):
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                safe_path(self.target, relative)

    def test_linked_source_is_rejected(self):
        source = self.base / "source"
        shutil.copytree(ROOT / "skills", source / "skills")
        shutil.copyfile(ROOT / "harness.json", source / "harness.json")
        file = source / "skills/python-engineering/SKILL.md"
        file.unlink()
        self.make_link(file, ROOT / "skills/python-engineering/SKILL.md")
        with self.assertRaisesRegex(ValueError, "Linked"):
            build_plan(source, ["python"], ["codex"])

    def test_unconfigured_commands_are_explicit(self):
        project = json.loads(self.plan()[".harness/project.json"])
        self.assertTrue(all(value == [] for value in project["commands"].values()))
        self.assertIsNone(project["facts"]["qt_binding"])

    def test_claude_only_install_does_not_create_codex_files(self):
        plan = self.plan(tools=["claude"], with_agents=True)
        self.assertIn("CLAUDE.md", plan)
        self.assertFalse(any(name.startswith((".agents/", ".codex/")) for name in plan))


if __name__ == "__main__":
    unittest.main()
