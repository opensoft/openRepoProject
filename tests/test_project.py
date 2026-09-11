"""Offline behavioral checks with disposable Git repositories and generators."""
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import shutil
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

    def test_benches_discovers_a_workbench_from_its_own_directory(self):
        previous = self.env.pop("WORKBENCHES_ROOT")
        self.addCleanup(self.env.__setitem__, "WORKBENCHES_ROOT", previous)
        result = self.run_cli("benches", "--json", cwd=self.wb)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)[0]["bench"], "testBench")

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

    def test_invalid_yaml_encoding_is_a_structured_error(self):
        root = self.repo()
        (root / "project.yaml").write_bytes(b"kind: \xff\n")
        result = self.run_cli("status", root, "--json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("error", json.loads(result.stdout))
        self.assertNotIn("Traceback", result.stderr)

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

    def test_human_reports_render_present_project_leg_state(self):
        root = self.repo("Atlas")
        leg = self.repo("Atlas/spec")
        (root / "project.yaml").write_text("kind: project-manifest\nlegs:\n  - {role: spec, path: spec}\n")
        for command in ("status", "doctor"):
            result = self.run_cli(command, root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(f"spec: {leg} — main; dirty=False", result.stdout)

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

    def test_family_name_refuses_ambiguous_default_project_roots(self):
        bases = [self.base / "first-projects", self.base / "second-projects"]
        for base in bases:
            holder = base / "Family/Family"
            holder.mkdir(parents=True)
            (holder / "family.yaml").write_text("kind: family-manifest\nmembers: []\n")
        with patch.object(module, "projects_dirs", return_value=bases):
            with self.assertRaisesRegex(module.Refused, "Ambiguous project name"):
                module.discover("Family")

    def test_registered_claude_git_commands_have_skill_bundles(self):
        registry = json.loads((ROOT / ".specify/extensions/.registry").read_text())
        commands = registry["extensions"]["git"]["registered_commands"]["claude"]
        for command in commands:
            skill = command.replace(".", "-")
            self.assertTrue((ROOT / ".claude/skills" / skill / "SKILL.md").is_file(), command)

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

    def test_handoff_rejects_path_like_remote_identity_before_record_lookup(self):
        root = self.repo()
        self.git(root, "remote", "add", "origin", "git@github.com:../repo")
        config = self.base / "home/.agents"
        config.mkdir(parents=True)
        workspace = self.base / "parked"
        workspace.mkdir()
        (config / "workspace.yaml").write_text(f"repository: example/wip\npath: {workspace}\n")
        (workspace / "sentinel.yaml").write_text("kind: [\n")
        result = self.run_cli("status", root, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["handoff"]["state"],
                         "no GitHub repository identity to match a parked record")

    def test_handoff_rejects_non_github_host_before_record_lookup(self):
        root = self.repo()
        self.git(root, "remote", "add", "origin", "https://evilgithub.com/example/repo.git")
        config = self.base / "home/.agents"
        config.mkdir(parents=True)
        workspace = self.base / "parked"
        workspace.mkdir()
        (config / "workspace.yaml").write_text(f"repository: example/wip\npath: {workspace}\n")
        result = self.run_cli("status", root, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["handoff"]["state"],
                         "no GitHub repository identity to match a parked record")

    def test_doctor_validate_reports_missing_owner_scripts(self):
        root = self.repo()
        (root / "project.yaml").write_text("kind: project-manifest\nlegs: []\n")
        result = self.run_cli("doctor", root, "--validate", "--json")
        self.assertEqual(result.returncode, 1, result.stderr)
        errors = [c for c in json.loads(result.stdout)["checks"] if c["level"] == "error"]
        self.assertEqual({c["check"] for c in errors}, {"validate-manifest.py", "validate-pins.py"})

    def test_profile_reports_filter_unknown_secret_fields(self):
        root = self.repo()
        (root / ".project.json").write_text(json.dumps({
            "schema_version": 1, "bench": "testBench", "type": "test", "token": "do-not-report"}))
        status = self.run_cli("status", root, "--json")
        self.assertEqual(status.returncode, 0, status.stderr)
        self.assertNotIn("token", json.loads(status.stdout)["profile"])
        doctor = self.run_cli("doctor", root, "--json")
        self.assertEqual(doctor.returncode, 0, doctor.stderr)
        self.assertNotIn("token", json.loads(doctor.stdout)["profile"])

    def test_malformed_bench_entries_refuse_without_tracebacks(self):
        root = self.repo()
        (root / ".project.json").write_text(json.dumps({"schema_version": 1, "bench": "testBench", "type": "test"}))
        self.config["benches"]["testBench"] = []
        self.save_config()
        doctor = self.run_cli("doctor", root, "--json")
        self.assertEqual(doctor.returncode, 2)
        self.assertIn("error", json.loads(doctor.stdout))
        update = self.run_cli("update", root, "--apply", "--component", "bench", "--yes")
        self.assertEqual(update.returncode, 2)
        self.assertNotIn("Traceback", update.stderr)

    def test_update_refuses_missing_child_and_retains_shape_owner_prompt(self):
        root = self.repo("Atlas")
        (root / "project.yaml").write_text("kind: project-manifest\nlegs:\n  - {role: spec, path: spec}\n")
        self.commit(root)
        missing = self.run_cli("update", root, "--apply", "--component", "shape", "--yes")
        self.assertEqual(missing.returncode, 2)
        self.assertIn("Child checkout is missing", missing.stderr)
        source = self.base / "shape"
        source.mkdir()
        (source / "update-shape.py").write_text("import sys\nsys.exit(0)\n")
        (root / "spec").mkdir()
        self.git(root / "spec", "init", "-b", "main")
        self.git(root / "spec", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "--allow-empty", "-m", "initial")
        self.commit(root)
        with patch.object(module, "execute", return_value=0) as run:
            code = module.main(["update", str(root), "--apply", "--component", "shape", "--shape-source",
                                str(source), "--at", "a" * 40, "--yes"])
        self.assertEqual(code, 0)
        self.assertEqual(run.call_count, 2)
        self.assertTrue(all("--yes" not in call.args[0] for call in run.call_args_list))

    def test_update_refuses_a_dirty_family_member(self):
        holder = self.repo("Family/Family")
        (holder / "family.yaml").write_text("kind: family-manifest\nmembers:\n  - project: Atlas\n")
        self.commit(holder)
        member = self.repo("Family/Atlas")
        (member / "project.yaml").write_text("kind: project-manifest\nlegs: []\n")
        self.commit(member)
        (member / "preserve").write_text("dirty")
        result = self.run_cli("update", holder, "--apply", "--component", "shape", "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Child has work to preserve", result.stderr)

    def test_doctor_validate_with_a_project_leg_has_structured_output(self):
        root = self.repo("Atlas")
        leg = self.repo("Atlas/spec")
        (root / "project.yaml").write_text("kind: project-manifest\nlegs:\n  - {role: spec, path: spec}\n")
        result = self.run_cli("doctor", root, "--validate", "--json")
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertIn("checks", report)
        self.assertEqual(report["children"][0]["path"], str(leg))

    def test_doctor_repository_health_reports_default_drift_and_worktree_blockers(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        self.git(root, "push", "-u", "origin", "main")
        self.git(remote, "symbolic-ref", "HEAD", "refs/heads/main")
        ignored = self.base / "ignored-tree"
        unpublished = self.base / "unpublished-tree"
        self.git(root, "worktree", "add", "-b", "001-ignored", str(ignored))
        (ignored / ".gitignore").write_text("local.env\n")
        self.commit(ignored)
        (ignored / "local.env").write_text("preserve")
        self.git(root, "worktree", "add", "-b", "002-unpublished", str(unpublished))
        other = self.base / "other"
        subprocess.run(["git", "clone", "--branch", "main", str(remote), str(other)], env=self.env,
                       check=True, text=True, capture_output=True)
        (other / "remote").write_text("remote")
        self.commit(other)
        self.git(other, "push")
        (root / "local").write_text("local")
        self.commit(root)
        self.git(root, "fetch", "origin")
        before = self.git(root, "worktree", "list", "--porcelain")
        result = self.run_cli("doctor", root, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        health = report["repository_health"]
        self.assertEqual(health["state"], "available")
        self.assertEqual(health["target_branch"], "main")
        by_branch = {row["branch"]: row for row in health["worktrees"]}
        self.assertEqual(by_branch["main"]["classification"], "protected-default")
        self.assertEqual(by_branch["main"]["health_status"], "diverged-default")
        self.assertEqual(by_branch["main"]["health_level"], "warning")
        self.assertEqual(by_branch["001-ignored"]["classification"], "ignored-local-files")
        self.assertEqual(by_branch["001-ignored"]["health_level"], "warning")
        self.assertEqual(by_branch["002-unpublished"]["classification"], "unpublished")
        self.assertEqual(by_branch["002-unpublished"]["health_level"], "warning")
        health_check = next(check for check in report["checks"]
                            if check["check"].endswith("repository health"))
        self.assertEqual(health_check["level"], "warning")
        self.assertEqual(before, self.git(root, "worktree", "list", "--porcelain"))
        human = self.run_cli("doctor", root)
        self.assertEqual(human.returncode, 0, human.stderr)
        self.assertIn("Repository health: WARNING", human.stdout)
        self.assertIn("WARNING DIVERGED-DEFAULT", human.stdout)
        self.assertIn("WARNING IGNORED-LOCAL-FILES", human.stdout)

    def test_doctor_reports_unknown_default_as_unavailable_health(self):
        root = self.repo(branch="develop")
        result = self.run_cli("doctor", root, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        health = json.loads(result.stdout)["repository_health"]
        self.assertEqual(health["state"], "unavailable")
        self.assertIn("Cannot determine the default branch", health["error"])
        human = self.run_cli("doctor", root)
        self.assertEqual(human.returncode, 0, human.stderr)
        self.assertIn("Repository health: UNAVAILABLE", human.stdout)

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

    def test_clean_is_read_only_and_classifies_linked_worktrees(self):
        root = self.repo()
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        before = self.git(root, "worktree", "list", "--porcelain")
        result = self.run_cli("clean", root, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["target_branch"], "main")
        self.assertIn("last fetch", report["tracking_freshness"])
        by_branch = {row["branch"]: row for row in report["worktrees"]}
        self.assertEqual(by_branch["main"]["classification"], "protected-default")
        self.assertEqual(by_branch["001-feature"]["classification"], "unpublished")
        self.assertEqual(before, self.git(root, "worktree", "list", "--porcelain"))
        self.assertTrue(tree.is_dir())

    def test_clean_refuses_unmerged_worktree_removal(self):
        root = self.repo()
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        (tree / "work").write_text("preserve")
        self.commit(tree)
        result = self.run_cli("clean", root, "--apply", "--action", "remove",
                              "--worktree", tree, "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unpublished", result.stderr)
        self.assertTrue(tree.is_dir())
        result = self.run_cli("clean", root, "--apply", "--action", "delete-branch",
                              "--branch", "001-feature", "--yes")
        self.assertEqual(result.returncode, 2)
        result = self.run_cli("clean", root, "--apply", "--action", "delete-branch",
                              "--branch", "main", "--yes")
        self.assertEqual(result.returncode, 2)

    def test_clean_retires_merged_worktree_and_local_branch(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        (tree / "work").write_text("done")
        self.commit(tree)
        self.git(tree, "push", "-u", "origin", "001-feature")
        feature_head = self.git(tree, "rev-parse", "HEAD")
        self.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "merge", "--no-ff", "001-feature", "-m", "merge feature")
        result = self.run_cli("clean", root, "--apply", "--action", "remove",
                              "--worktree", tree, "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("branch -d 001-feature", result.stdout)
        self.assertFalse(tree.exists())
        self.assertIsNone(module.git_text(root, "show-ref", "--verify", "--quiet", "refs/heads/001-feature"))
        self.assertEqual(feature_head, self.git(remote, "rev-parse", "refs/heads/001-feature"))

    def test_clean_retires_merged_worktree_with_disposable_python_caches(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        (tree / ".gitignore").write_text("__pycache__/\n*.pyc\n*.pyo\n")
        (tree / "work").write_text("done")
        self.commit(tree)
        self.git(tree, "push", "-u", "origin", "001-feature")
        self.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "merge", "--no-ff", "001-feature", "-m", "merge feature")
        cache = tree / "__pycache__"
        cache.mkdir()
        (cache / "project.cpython-312.pyc").write_bytes(b"cache")
        (tree / "legacy.pyc").write_bytes(b"cache")
        (tree / "optimized.pyo").write_bytes(b"cache")
        report = json.loads(self.run_cli("clean", root, "--json").stdout)
        row = next(item for item in report["worktrees"] if item["branch"] == "001-feature")
        self.assertEqual(row["classification"], "merged-removable")
        self.assertEqual(row["blocking_ignored_paths"], [])
        self.assertEqual(row["disposable_ignored_paths"],
                         ["__pycache__/", "legacy.pyc", "optimized.pyo"])
        result = self.run_cli("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Disposable ignored artifacts to discard", result.stdout)
        self.assertIn("__pycache__", result.stdout)
        self.assertFalse(tree.exists())
        self.assertIsNone(module.git_text(root, "show-ref", "--verify", "--quiet", "refs/heads/001-feature"))

    def test_clean_deletes_a_verified_orphaned_local_branch(self):
        root = self.repo()
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        (tree / "work").write_text("done")
        self.commit(tree)
        self.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "merge", "--no-ff", "001-feature", "-m", "merge feature")
        self.git(root, "worktree", "remove", tree)
        result = self.run_cli("clean", root, "--apply", "--action", "delete-branch",
                              "--branch", "001-feature", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIsNone(module.git_text(root, "show-ref", "--verify", "--quiet", "refs/heads/001-feature"))

    def test_clean_reports_branch_retirement_failure_without_force(self):
        root = self.base / "repo"
        tree = self.base / "feature-tree"
        root.mkdir()
        tree.mkdir()
        report = {"target_branch": "main", "worktrees": [
            {"path": str(root), "branch": "main", "present": True},
            {"path": str(tree), "branch": "001-feature", "current": False,
             "classification": "merged-removable", "head": "a" * 40,
             "disposable_ignored_paths": []},
        ]}
        args = module.argparse.Namespace(target=root, json=False, apply=True, action="remove",
                                         worktree=tree, branch=None, yes=True)
        with patch.object(module, "discover", return_value=root), \
             patch.object(module, "cleanup_report", return_value=report), \
             patch.object(module, "require_unchanged_cleanup_state"), \
             patch.object(module, "branch_still_merged", return_value=True), \
             patch.object(module, "execute", side_effect=[0, 7]) as execute:
            self.assertEqual(module.clean(args), 7)
        commands = [call.args[0] for call in execute.call_args_list]
        self.assertEqual(commands[0][-2:], ["remove", str(tree)])
        self.assertEqual(commands[1][-2:], ["-d", "001-feature"])
        self.assertNotIn("-D", commands[1])

    def test_clean_stops_when_worktree_removal_fails(self):
        root = self.base / "repo"
        tree = self.base / "feature-tree"
        root.mkdir()
        tree.mkdir()
        report = {"target_branch": "main", "worktrees": [
            {"path": str(root), "branch": "main", "present": True},
            {"path": str(tree), "branch": "001-feature", "current": False,
             "classification": "merged-removable", "head": "a" * 40,
             "disposable_ignored_paths": []},
        ]}
        args = module.argparse.Namespace(target=root, json=False, apply=True, action="remove",
                                         worktree=tree, branch=None, yes=True)
        with patch.object(module, "discover", return_value=root), \
             patch.object(module, "cleanup_report", return_value=report), \
             patch.object(module, "require_unchanged_cleanup_state"), \
             patch.object(module, "execute", return_value=9) as execute:
            self.assertEqual(module.clean(args), 9)
        self.assertEqual(execute.call_count, 1)
        self.assertEqual(execute.call_args.args[0][-2:], ["remove", str(tree)])

    def test_clean_stops_when_cache_deletion_fails(self):
        root = self.base / "repo"
        tree = self.base / "feature-tree"
        root.mkdir()
        tree.mkdir()
        report = {"target_branch": "main", "worktrees": [
            {"path": str(root), "branch": "main", "present": True},
            {"path": str(tree), "branch": "001-feature", "current": False,
             "classification": "merged-removable", "head": "a" * 40,
             "disposable_ignored_paths": ["__pycache__/"],
             "blocking_ignored_paths": []},
        ]}
        args = module.argparse.Namespace(target=root, json=False, apply=True, action="remove",
                                         worktree=tree, branch=None, yes=True)
        with patch.object(module, "discover", return_value=root), \
             patch.object(module, "cleanup_report", return_value=report), \
             patch.object(module, "require_unchanged_cleanup_state", return_value=report["worktrees"][1]), \
             patch.object(module, "remove_disposable_ignored_artifacts", side_effect=module.Refused("stop")), \
             patch.object(module, "execute") as execute:
            with self.assertRaisesRegex(module.Refused, "stop"):
                module.clean(args)
        execute.assert_not_called()

    def test_clean_preserves_branch_when_merge_state_changes_after_worktree_removal(self):
        root = self.base / "repo"
        tree = self.base / "feature-tree"
        root.mkdir()
        tree.mkdir()
        report = {"target_branch": "main", "worktrees": [
            {"path": str(root), "branch": "main", "present": True},
            {"path": str(tree), "branch": "001-feature", "current": False,
             "classification": "merged-removable", "head": "a" * 40,
             "disposable_ignored_paths": []},
        ]}
        args = module.argparse.Namespace(target=root, json=False, apply=True, action="remove",
                                         worktree=tree, branch=None, yes=True)
        with patch.object(module, "discover", return_value=root), \
             patch.object(module, "cleanup_report", return_value=report), \
             patch.object(module, "require_unchanged_cleanup_state"), \
             patch.object(module, "branch_still_merged", return_value=False), \
             patch.object(module, "execute", return_value=0) as execute:
            with self.assertRaisesRegex(module.Refused, "local branch was preserved"):
                module.clean(args)
        self.assertEqual(execute.call_count, 1)
        self.assertEqual(execute.call_args.args[0][-2:], ["remove", str(tree)])

    def test_clean_never_removes_the_worktree_containing_the_current_directory(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        (tree / "work").write_text("done")
        self.commit(tree)
        self.git(tree, "push", "-u", "origin", "001-feature")
        self.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "merge", "--no-ff", "001-feature", "-m", "merge feature")
        result = self.run_cli("clean", root, "--apply", "--action", "remove",
                              "--worktree", tree, "--yes", cwd=tree)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Cannot remove the current worktree", result.stderr)
        self.assertTrue(tree.is_dir())

    def test_clean_pushes_explicit_clean_feature_branch_without_force(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        self.git(tree, "push", "-u", "origin", "001-feature")
        (tree / "work").write_text("publish")
        self.commit(tree)
        result = self.run_cli("clean", root, "--apply", "--action", "push",
                              "--branch", "001-feature", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git(tree, "rev-parse", "HEAD"),
                         self.git(root, "rev-parse", "refs/remotes/origin/001-feature"))

    def test_clean_reports_dirty_detached_and_pushed_unmerged_states(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        feature = self.base / "feature-tree"
        detached = self.base / "detached-tree"
        dirty = self.base / "dirty-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(feature))
        self.git(feature, "push", "-u", "origin", "001-feature")
        (feature / "review-work").write_text("review")
        self.commit(feature)
        self.git(feature, "push", "origin", "001-feature")
        self.git(root, "worktree", "add", "--detach", str(detached))
        self.git(root, "worktree", "add", "-b", "001-dirty", str(dirty))
        (dirty / "uncommitted").write_text("preserve")
        report = json.loads(self.run_cli("clean", root, "--json", cwd=feature).stdout)
        by_branch = {row["branch"]: row for row in report["worktrees"]}
        self.assertEqual(by_branch["001-feature"]["classification"], "pushed-unmerged")
        self.assertTrue(by_branch["001-feature"]["current"])
        self.assertEqual(by_branch["detached"]["classification"], "detached")
        self.assertEqual(by_branch["001-dirty"]["classification"], "dirty")

    def test_clean_reports_stale_worktree_metadata(self):
        root = self.repo()
        tree = self.base / "stale-tree"
        self.git(root, "worktree", "add", "-b", "001-stale", str(tree))
        shutil.rmtree(tree)
        report = json.loads(self.run_cli("clean", root, "--json").stdout)
        stale = next(row for row in report["worktrees"] if row["path"] == str(tree))
        self.assertEqual(stale["classification"], "stale-worktree")

    def test_clean_preserves_ignored_files_in_an_otherwise_merged_worktree(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        (tree / ".gitignore").write_text("local.env\n")
        (tree / "work").write_text("done")
        self.commit(tree)
        self.git(tree, "push", "-u", "origin", "001-feature")
        self.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "merge", "--no-ff", "001-feature", "-m", "merge feature")
        ignored = tree / "local.env"
        ignored.write_text("preserve")
        report = json.loads(self.run_cli("clean", root, "--json").stdout)
        row = next(item for item in report["worktrees"] if item["branch"] == "001-feature")
        self.assertEqual(row["classification"], "ignored-local-files")
        self.assertEqual(row["disposable_ignored_paths"], [])
        self.assertEqual(row["blocking_ignored_paths"], ["local.env"])
        result = self.run_cli("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertTrue(ignored.is_file())

    def test_clean_preserves_a_symlink_named_like_a_disposable_cache(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        (tree / ".gitignore").write_text("__pycache__\n")
        (tree / "work").write_text("done")
        self.commit(tree)
        self.git(tree, "push", "-u", "origin", "001-feature")
        self.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "merge", "--no-ff", "001-feature", "-m", "merge feature")
        outside = self.base / "outside"
        outside.mkdir()
        (tree / "__pycache__").symlink_to(outside, target_is_directory=True)
        report = json.loads(self.run_cli("clean", root, "--json").stdout)
        row = next(item for item in report["worktrees"] if item["branch"] == "001-feature")
        self.assertEqual(row["classification"], "ignored-local-files")
        self.assertEqual(row["disposable_ignored_paths"], [])
        self.assertEqual(row["blocking_ignored_paths"], ["__pycache__"])
        result = self.run_cli("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertTrue((tree / "__pycache__").is_symlink())
        self.assertTrue(outside.is_dir())

    def test_clean_revalidates_disposable_cache_paths(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        (tree / ".gitignore").write_text("__pycache__/\nlocal.env\n")
        (tree / "work").write_text("done")
        self.commit(tree)
        self.git(tree, "push", "-u", "origin", "001-feature")
        self.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "merge", "--no-ff", "001-feature", "-m", "merge feature")
        cache = tree / "__pycache__"
        cache.mkdir()
        (cache / "project.cpython-312.pyc").write_bytes(b"cache")
        def change_after_plan(_):
            (tree / "local.env").write_text("preserve")
        args = module.argparse.Namespace(target=str(root), json=False, apply=True, action="remove",
                                         branch=None, worktree=str(tree), yes=True)
        with patch.object(module, "confirm", side_effect=change_after_plan):
            with self.assertRaises(module.Refused):
                module.clean(args)
        self.assertTrue(cache.is_dir())
        self.assertTrue((tree / "local.env").is_file())
        self.assertTrue(tree.is_dir())

    def test_clean_can_retire_when_target_is_the_worktree_being_removed(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        (tree / "work").write_text("done")
        self.commit(tree)
        self.git(tree, "push", "-u", "origin", "001-feature")
        self.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "merge", "--no-ff", "001-feature", "-m", "merge feature")
        result = self.run_cli("clean", tree, "--apply", "--action", "remove", "--worktree", tree, "--yes",
                              cwd=root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(tree.exists())
        self.assertIsNone(module.git_text(root, "show-ref", "--verify", "--quiet", "refs/heads/001-feature"))

    def test_clean_refuses_to_guess_a_nonstandard_default_branch(self):
        root = self.repo(branch="develop")
        result = self.run_cli("clean", root, "--json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Cannot determine the default branch", json.loads(result.stdout)["error"])

    def test_clean_pushes_to_a_differently_named_upstream_branch(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-local", str(tree))
        self.git(tree, "push", "-u", "origin", "001-local:review/remote")
        (tree / "work").write_text("publish")
        self.commit(tree)
        result = self.run_cli("clean", root, "--apply", "--action", "push", "--branch", "001-local", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git(tree, "rev-parse", "HEAD"),
                         self.git(remote, "rev-parse", "refs/heads/review/remote"))

    def test_clean_refuses_diverged_branch_push(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        self.git(tree, "push", "-u", "origin", "001-feature")
        (tree / "local").write_text("local")
        self.commit(tree)
        other = self.base / "other"
        subprocess.run(["git", "clone", "--branch", "001-feature", str(remote), str(other)], env=self.env,
                       check=True, text=True, capture_output=True)
        (other / "remote").write_text("remote")
        self.git(other, "add", ".")
        self.git(other, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "remote")
        self.git(other, "push")
        self.git(tree, "fetch", "origin")
        report = json.loads(self.run_cli("clean", root, "--json").stdout)
        row = next(item for item in report["worktrees"] if item["branch"] == "001-feature")
        self.assertEqual(row["classification"], "diverged")
        result = self.run_cli("clean", root, "--apply", "--action", "push", "--branch", "001-feature", "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertIn("reconcile", result.stderr)

    def test_clean_revalidates_a_worktree_after_confirmation(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        (tree / "work").write_text("done")
        self.commit(tree)
        self.git(tree, "push", "-u", "origin", "001-feature")
        self.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "merge", "--no-ff", "001-feature", "-m", "merge feature")
        def change_after_plan(_):
            (tree / "late-change").write_text("preserve")
        args = module.argparse.Namespace(target=str(root), json=False, apply=True, action="remove",
                                         branch=None, worktree=str(tree), yes=True)
        with patch.object(module, "confirm", side_effect=change_after_plan):
            with self.assertRaises(module.Refused):
                module.clean(args)
        self.assertTrue(tree.is_dir())


if __name__ == "__main__":
    unittest.main()
