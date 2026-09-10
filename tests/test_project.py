"""Offline behavioral checks with disposable Git repositories and generators."""
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "project"
loader = importlib.machinery.SourceFileLoader("project_cli", str(CLI))
spec = importlib.util.spec_from_loader(loader.name, loader)
module = importlib.util.module_from_spec(spec)
loader.exec_module(module)


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.wb = self.base / "work benches"
        (self.wb / "config").mkdir(parents=True)
        scripts = self.wb / "devBenches/testBench/scripts"
        scripts.mkdir(parents=True)
        self.generator = scripts / "new-test.sh"
        self.generator.write_text('#!/bin/bash\nmkdir -p "$2/$1"\nprintf "%s\\n" "$1" "$2" > "$2/$1/arguments"\n')
        self.config = {"benches": {"testBench": {"path": "devBenches/testBench",
            "ai_keywords": ["python"], "project_scripts": [
                {"name": "test", "script": "scripts/new-test.sh"},
                {"name": "update-test", "script": "scripts/update-test.sh"},
                {"name": "missing", "script": "scripts/missing.sh"}]}}}
        self.save_config()
        self.env = {**os.environ, "WORKBENCHES_ROOT": str(self.wb),
                    "HOME": str(self.base / "home"), "SPECKIT_WORKSPACE_PATH": "",
                    "PROJECTS_DIR": str(self.base), "GIT_CONFIG_NOSYSTEM": "1",
                    "GIT_CONFIG_GLOBAL": os.devnull}

    def save_config(self):
        (self.wb / "config/bench-config.json").write_text(json.dumps(self.config))

    def run_cli(self, *args, cwd=None):
        return subprocess.run([sys.executable, str(CLI), *map(str, args)],
                              cwd=cwd or self.base, env=self.env, input="", text=True,
                              capture_output=True, timeout=20)

    def repo(self, name="repo", branch="main"):
        path = self.base / name
        path.mkdir(parents=True, exist_ok=True)
        self.git(path, "init", "-b", branch)
        self.git(path, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "--allow-empty", "-m", "initial")
        return path

    def git(self, path, *args):
        result = subprocess.run(["git", "-C", str(path), *args], env=self.env,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def commit(self, path):
        self.git(path, "add", ".")
        self.git(path, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "-m", "fixture")

    def test_benches_excludes_updaters_and_reports_missing(self):
        result = self.run_cli("benches", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = json.loads(result.stdout)
        self.assertEqual([r["type"] for r in rows], ["test", "missing"])
        self.assertTrue(rows[0]["available"])
        self.assertFalse(rows[1]["available"])

    def test_new_preserves_paths_with_spaces_and_writes_profile(self):
        parent = self.base / "new parent"
        result = self.run_cli("new", "MyApp", parent, "--type", "test", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((parent / "MyApp/arguments").read_text().splitlines(), ["MyApp", str(parent)])
        profile = json.loads((parent / "MyApp/.project.json").read_text())
        self.assertEqual(profile["bench"], "testBench")

    def test_dry_run_creates_no_parent(self):
        parent = self.base / "absent"
        result = self.run_cli("new", "App", parent, "--type", "test", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(parent.exists())

    def test_existing_destination_and_noninteractive_confirmation_refuse(self):
        target = self.base / "App"
        target.mkdir()
        result = self.run_cli("new", "App", "--type", "test", "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(list(target.iterdir()), [])
        result = self.run_cli("new", "Another", "--type", "test")
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.base / "Another").exists())

    def test_generator_failure_propagates_and_no_workflow_follows(self):
        self.generator.write_text("#!/bin/bash\nexit 17\n")
        result = self.run_cli("new", "App", "--type", "test", "--yes")
        self.assertEqual(result.returncode, 17, result.stderr)
        self.assertFalse((self.base / "App/.project.json").exists())

    def test_success_without_project_is_failure(self):
        self.generator.write_text("#!/bin/bash\nexit 0\n")
        self.assertEqual(self.run_cli("new", "App", "--type", "test", "--yes").returncode, 2)

    def test_registry_paths_cannot_escape_or_follow_outside_symlink(self):
        self.config["benches"]["testBench"]["path"] = "../outside"
        self.save_config()
        self.assertEqual(self.run_cli("benches").returncode, 2)
        self.config["benches"]["testBench"]["path"] = "link"
        (self.wb / "link").symlink_to(self.base)
        self.save_config()
        self.assertEqual(self.run_cli("benches").returncode, 2)

    def test_keyword_selection_is_case_insensitive_and_ambiguous_refuses(self):
        result = self.run_cli("new", "App", "--description", "PYTHON app", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.config["benches"]["testBench"]["project_scripts"].append(
            {"name": "second", "script": "scripts/new-test.sh"})
        self.save_config()
        self.assertEqual(self.run_cli("new", "App", "--description", "python", "--dry-run").returncode, 2)

    def test_invalid_json_and_manifest_are_structured_errors(self):
        (self.wb / "config/bench-config.json").write_text("[")
        result = self.run_cli("benches", "--json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("error", json.loads(result.stdout))
        root = self.repo()
        (root / "project.yaml").write_text("kind: [")
        result = self.run_cli("status", root, "--json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("error", json.loads(result.stdout))

    def test_status_from_nested_path_and_feature_worktree_is_read_only(self):
        root = self.repo()
        child = root / "nested"
        child.mkdir()
        (root / "dirty").write_text("preserve")
        before = self.git(root, "status", "--porcelain")
        result = self.run_cli("status", "--json", cwd=child)
        report = json.loads(result.stdout)
        self.assertEqual(report["root"], str(root))
        self.assertTrue(report["repository"]["dirty"])
        self.assertEqual(before, self.git(root, "status", "--porcelain"))
        tree = self.base / "feature"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        report = json.loads(self.run_cli("status", tree, "--json").stdout)
        self.assertEqual(report["repository"]["branch"], "001-feature")
        self.assertEqual(len(report["repository"]["worktrees"]), 2)

    def test_shape_skips_assembly_dot_and_reports_missing_legs(self):
        root = self.repo("Atlas")
        (root / "project.yaml").write_text('kind: project-manifest\ntracking_branch: develop\nlegs:\n'
            '  - {role: assembly, path: "."}\n  - {role: spec, path: spec}\n  - {role: code, path: code}\n')
        (root / "spec").mkdir()  # Must not confuse parent Git with a leg checkout.
        result = self.run_cli("doctor", root, "--json")
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(len(report["children"]), 2)
        self.assertFalse(report["children"][0]["present"])
        self.assertEqual(report["children"][0]["tracking_branch"], "develop")

    def test_family_name_prefers_holder_and_inspects_working_sibling(self):
        root = self.repo("Family/Family")
        (root / "family.yaml").write_text("kind: family-manifest\nmembers:\n  - project: Atlas\n    path: members/Atlas\n")
        member = self.repo("Family/Atlas")
        (member / "project.yaml").write_text("kind: project-manifest\nlegs: []\n")
        result = self.run_cli("status", "Family", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["root"], str(root))
        self.assertEqual(report["children"][0]["root"], str(member))

    def test_update_default_and_dry_run_do_not_execute(self):
        root = self.repo()
        result = self.run_cli("update", root, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)["updates"]), 4)
        result = self.run_cli("update", root, "--apply", "--component", "workflow", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("setup-openspeckit", result.stdout)
        self.assertFalse((root / ".specify").exists())

    def test_update_refuses_dirty_and_feature_branch(self):
        root = self.repo()
        (root / "dirty").write_text("preserve")
        result = self.run_cli("update", root, "--apply", "--component", "bench", "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertIn("clean tracking", result.stderr)
        self.commit(root)
        self.git(root, "switch", "-c", "001-feature")
        self.assertEqual(self.run_cli("update", root, "--apply", "--component", "bench", "--yes").returncode, 2)

    def test_shape_plan_keeps_owner_confirmation(self):
        with patch.object(module.shutil, "which", return_value="/bin/tool"), patch.object(module, "execute", return_value=19) as run:
            code = module.main(["new", "Atlas", "--shape", "--org", "example", "--visibility", "private",
                                "--into", str(self.base), "--yes"])
        self.assertEqual(code, 19)
        self.assertNotIn("--yes", run.call_args.args[0])
        self.assertIn("openRepoShape", run.call_args.args[0])

    def test_exact_bench_updater_receives_only_selected_root(self):
        root = self.repo()
        (root / ".project.json").write_text(json.dumps({"schema_version": 1, "bench": "testBench", "type": "test"}))
        self.commit(root)
        updater = self.generator.parent / "update-test.sh"
        updater.write_text('#!/bin/bash\nprintf "%s" "$1"\nexit 23\n')
        result = self.run_cli("update", root, "--apply", "--component", "bench", "--yes")
        self.assertEqual(result.returncode, 23, result.stderr)
        self.assertTrue(result.stdout.endswith(str(root)))

    def test_handoff_reads_matching_record_without_changing_it(self):
        root = self.repo()
        self.git(root, "remote", "add", "origin", "git@github.com:example/Atlas.git")
        config = self.base / "home/.agents"
        config.mkdir(parents=True)
        workspace = self.base / "parked"
        records = workspace / "workspaces/example"
        records.mkdir(parents=True)
        (config / "workspace.yaml").write_text(f"repository: example/wip\npath: {workspace}\n")
        record = records / "atlas.yaml"
        content = "kind: workspace-manifest\nprojects:\n  - repository: example/Atlas\n    parked_at: 2026-09-10T18:42:11Z\n    active_feature: 001-demo\n    features: [{branch: 001-demo}]\n"
        record.write_text(content)
        result = self.run_cli("status", root, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        handoff = json.loads(result.stdout)["handoff"]
        self.assertEqual(handoff["state"], "recorded")
        self.assertEqual(handoff["records"][0]["features"], 1)
        self.assertEqual(record.read_text(), content)

    def test_doctor_validate_reports_missing_owner_scripts(self):
        root = self.repo()
        (root / "project.yaml").write_text("kind: project-manifest\nlegs: []\n")
        result = self.run_cli("doctor", root, "--validate", "--json")
        self.assertEqual(result.returncode, 1, result.stderr)
        errors = [c for c in json.loads(result.stdout)["checks"] if c["level"] == "error"]
        self.assertEqual({c["check"] for c in errors}, {"validate-manifest.py", "validate-pins.py"})

    def test_shape_update_runs_check_then_apply_and_propagates_failure(self):
        root = self.repo()
        (root / "project.yaml").write_text("kind: project-manifest\nlegs: []\n")
        self.commit(root)
        source = self.base / "shape"
        source.mkdir()
        (source / "update-shape.py").write_text("import sys\nprint(sys.argv[1])\nsys.exit(1 if sys.argv[1] == 'check' else 9)\n")
        result = self.run_cli("update", root, "--apply", "--component", "shape", "--shape-source", source,
                              "--at", "a" * 40, "--yes")
        self.assertEqual(result.returncode, 9, result.stderr)
        self.assertTrue(result.stdout.endswith("check\napply\n"), result.stdout)


if __name__ == "__main__":
    unittest.main()
