import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/sync-upstream-skills.py"
spec = importlib.util.spec_from_file_location("sync_skills", SCRIPT)
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name).resolve()
        self.root = root
        self.manifest = root / "upstream/sources.json"
        self.manifest.parent.mkdir()
        self.manifest.write_text(json.dumps({
            "repository": "example/skills", "commit": "a" * 40,
            "license": "upstream/LICENSE",
            "skills": {"skills/example": "skills/example"}, "files": {},
        }), encoding="utf-8")
        for name, value in (("ROOT", root), ("MANIFEST", self.manifest)):
            patcher = patch.object(sync, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def run_sync(self, files=None, commit=None):
        files = files or {"SKILL.md": b"Example\n", "FORMAT.md": b"Format\n"}
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            archive.writestr("repo/LICENSE", "MIT\n")
            archive.writestr("repo/unselected/SKILL.md", "Do not import")
            for name, data in files.items():
                archive.writestr("repo/skills/example/" + name, data)
        with patch.object(sync.urllib.request, "urlopen", return_value=io.BytesIO(buffer.getvalue())):
            sync.sync(commit)

    def test_import_repeat_and_update_removes_obsolete_files(self):
        self.run_sync()
        original = self.manifest.read_bytes()
        self.run_sync()
        self.assertEqual(original, self.manifest.read_bytes())
        self.assertFalse((self.root / "unselected").exists())
        self.run_sync({"SKILL.md": b"Updated\n"}, "b" * 40)
        self.assertFalse((self.root / "skills/example/FORMAT.md").exists())
        self.assertEqual(json.loads(self.manifest.read_text())["commit"], "b" * 40)

    def test_modified_missing_and_extra_files_are_protected(self):
        self.run_sync()
        skill = self.root / "skills/example/SKILL.md"
        for content in (b"Local edits", None):
            with self.subTest(content=content):
                if content is None:
                    skill.unlink()
                else:
                    skill.write_bytes(content)
                with self.assertRaisesRegex(ValueError, "Local change"):
                    self.run_sync()
                skill.write_bytes(b"Example\n")
        extra = skill.parent / "local.md"
        extra.write_text("Local work")
        with self.assertRaisesRegex(ValueError, "Untracked local file"):
            self.run_sync()
        self.assertEqual(extra.read_text(), "Local work")

    def test_crlf_checkout_is_accepted(self):
        self.run_sync()
        skill = self.root / "skills/example/SKILL.md"
        skill.write_bytes(b"Example\r\n")
        self.run_sync()
        self.assertEqual(skill.read_bytes(), b"Example\r\n")

    def test_missing_skill_and_unsafe_archive_fail_before_writes(self):
        for files in ({"FORMAT.md": b"No skill"}, {"../escape": b"bad"}):
            with self.subTest(files=files):
                with self.assertRaises(ValueError):
                    self.run_sync(files)
                self.assertFalse((self.root / "skills").exists())


if __name__ == "__main__":
    unittest.main()
