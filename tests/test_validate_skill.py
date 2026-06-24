import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_skill  # type: ignore


class ValidateSkillTests(unittest.TestCase):
    def test_repository_validation_passes(self) -> None:
        report = validate_skill.validate_repository(REPO_ROOT)
        failed = [result for result in report.results if not result.passed]
        self.assertEqual([], failed, msg=report.render())

    def test_placeholder_skill_validator_path_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_copy = Path(temp_dir) / "repo"
            shutil.copytree(REPO_ROOT, repo_copy)

            skill_path = repo_copy / "skills" / "reasonix-orchestrator" / "SKILL.md"
            skill_text = skill_path.read_text(encoding="utf-8")
            skill_text = skill_text.replace(
                "python scripts/validate_skill.py --repo-root .",
                "python -X utf8 <path-to-skill-creator>/quick_validate.py skills/reasonix-orchestrator",
            )
            skill_path.write_text(skill_text, encoding="utf-8")

            report = validate_skill.validate_repository(repo_copy)
            failures = {result.name: result.message for result in report.results if not result.passed}
            self.assertIn("docs-no-placeholder-validator-path", failures)

    def test_manifest_missing_required_field_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_copy = Path(temp_dir) / "repo"
            shutil.copytree(REPO_ROOT, repo_copy)

            manifest_path = repo_copy / ".codex-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            del manifest["interface"]["defaultPrompt"]
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            report = validate_skill.validate_repository(repo_copy)
            failures = {result.name: result.message for result in report.results if not result.passed}
            self.assertIn("manifest-required-fields", failures)


if __name__ == "__main__":
    unittest.main()
