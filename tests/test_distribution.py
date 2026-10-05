import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
from register_codex import install_skill, register

spec = importlib.util.spec_from_file_location("build_release", ROOT / "scripts" / "build_release.py")
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ConfigurationTests(unittest.TestCase):
    def test_preserve_config_and_idempotence(self):
        with tempfile.TemporaryDirectory() as folder:
            config = Path(folder) / "config.toml"
            original = 'model = "user-selected-model"\n[mcp_servers.existing]\ncommand = "keep-this"\n'
            config.write_text(original, encoding="utf-8")
            python = Path(folder) / "python.exe"
            self.assertEqual(register(config, python), "added")
            first = config.read_text(encoding="utf-8")
            self.assertTrue(first.startswith(original))
            self.assertEqual(tomllib.loads(first)["mcp_servers"]["existing"]["command"], "keep-this")
            self.assertEqual(register(config, python), "already-configured")
            self.assertEqual(config.read_text(encoding="utf-8"), first)

    def test_collision_is_non_destructive(self):
        with tempfile.TemporaryDirectory() as folder:
            config = Path(folder) / "config.toml"
            original = '[mcp_servers.garmin_cn_coach]\ncommand = "some-other-install"\n'
            config.write_text(original, encoding="utf-8")
            with self.assertRaises(RuntimeError):
                register(config, Path(folder) / "python.exe")
            self.assertEqual(config.read_text(encoding="utf-8"), original)

    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder) / "codex"
            self.assertEqual(register(home / "config.toml", Path(folder) / "python.exe", True), "dry-run-ok")
            self.assertEqual(install_skill(home, True), "dry-run-ok")
            self.assertFalse(home.exists())

    def test_skill_does_not_overwrite_existing_work(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            target = home / "skills" / "garmin-cn-running-coach"
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text("my existing instructions", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                install_skill(home)
            self.assertEqual((target / "SKILL.md").read_text(), "my existing instructions")


class ReleaseTests(unittest.TestCase):
    def test_private_and_runtime_files_are_excluded(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in release.ROOT_FILES:
                (root / name).write_text("public", encoding="utf-8")
            for relative in ("private/tokens/garmin_tokens.json", ".venv/installed.py", "data/training.json", ".git/config"):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("synthetic private content", encoding="utf-8")
            names = {p.relative_to(root).as_posix() for p in release.public_files(root)}
            self.assertEqual(names, release.ROOT_FILES)

    def test_profile_must_not_enter_public_config(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in release.ROOT_FILES:
                (root / name).write_text("public", encoding="utf-8")
            (root / "config").mkdir()
            (root / "config" / "athlete-profile.json").write_text("{}", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                release.public_files(root)

    def test_cn_tool_allowlist_is_read_only(self):
        tools = json.loads((ROOT / "config" / "tools.json").read_text())["enabled_tools"]
        self.assertEqual(len(tools), 34)
        self.assertTrue(all(name.startswith("get_") for name in tools))
        self.assertFalse(any(word in name for name in tools for word in ("delete", "upload", "create", "set_")))


if __name__ == "__main__":
    unittest.main()
