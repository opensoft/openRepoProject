"""The plan of `project clean --all-safe` and of a named removal (feature 004,
the US1 plan lane: T036 to T040, and the tests T052 adds).

Sources: specs/004-project-clean-all-safe/contracts/project-clean.md
("Argument checks", "Order of a run", "Streams", "Human output", "Plan
envelope" and "Codes"), data-model.md ("Plan" and "Gate"), research.md R4 and
R12, and design.md D18 of openspec/changes/add-project-clean-all-safe/. Expected
human text comes from clean_support's fixtures (rule 8); key lists and parity
values are literals written here (rule 11). Every repository is a disposable
fixture under the test's temporary directory (rule 4); the eligible ones are
made by merged_worktree(), a commit of their own, so that US2's gates keep them
eligible (lead ruling R-56).
"""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import types
import unittest
from unittest import mock

import clean_support

project = clean_support.load_project()
TEXT = clean_support.TEXT_FIXTURES

# A well-formed --expect-plan value: 64 lowercase hexadecimal characters.
DIGEST = "0" * 64
HEX64 = re.compile("[0-9a-f]{64}")
E_ACUTE = chr(0xE9)  # a non-ASCII code point, built so that this file stays ASCII

# The keys of the plan envelope and of its objects, in the contract's order
# (contracts/project-clean.md, "Plan envelope"), written here as literals.
PLAN_KEYS = ["schema_version", "observed_at", "mode", "root", "target_branch", "tracking_freshness",
             "worktrees", "repository", "merge_target", "limits", "budget", "probes", "operations",
             "selected", "excluded", "omitted", "notes", "completeness", "apply_allowed", "refusals",
             "plan_digest"]
REPOSITORY_KEYS = ["root", "common_dir", "dev", "ino", "root_valid_utf8", "common_dir_valid_utf8"]
SELECTED_KEYS = ["path", "path_valid_utf8", "branch", "head", "upstream", "upstream_oid", "ahead", "behind",
                 "dev", "ino", "admin_id", "locked", "present", "dirty", "ignored_files", "remote_present",
                 "merged_into_target", "current", "classification", "operation"]
EXCLUDED_KEYS = ["path", "path_valid_utf8", "branch", "classification", "reason"]
LIMITS = {"worktree_rows": 128, "targets": 16, "ignored_entries": 64, "status_records": 4096,
          "ignored_samples": 8}
BUDGET = {"probe_timeout_seconds": 5, "invocation_timeout_seconds": 60, "reconciliation_reserve_seconds": 10,
          "removal_floor_seconds": 5, "removal_ceiling_seconds": 300, "probe_concurrency": 1}
FRESHNESS = "local refs only; remote information is as of the last fetch; no fetch performed"

# The packet's preview fixture (ideation/brainstorm/project-maintenance-batch-cleanup.md:1052-1130
# at da33d92), the values its digest covers, and that digest (research.md R12;
# lead ruling R-34).
PACKET_REPOSITORY = {"root": "/home/user/projects/Atlas", "common_dir": "/home/user/projects/Atlas/.git",
                     "dev": 66306, "ino": 3407873, "root_valid_utf8": True, "common_dir_valid_utf8": True}
PACKET_MERGE_TARGET = {"name": "main", "source": "origin-head", "sha": "39f33f71eba7ca23d258c75ebcc8b9a0ec9995d9"}
PACKET_SELECTED = ("/home/user/projects/Atlas-worktrees/feature-login", "feature/login",
                   "635e8931ebd09939ab00fb1598598f6e43fdaf41")
PACKET_EXCLUDED = ("/home/user/projects/Atlas-worktrees/feature-report", "feature/report",
                   "fc2afa49af6ee0111f0de91e16b6e651af506f2a")
PACKET_DIGEST = "7495756d199ba217f41ed4d648c241c95608b4f353c46952e9a7f4cddc17f3bc"


def argv_words(record):
    """A counted child's argument vector without its leading -c pins."""
    argv, at = record.argv, 0
    while at + 1 < len(argv) and argv[at] == "-c":
        at += 2
    return argv[at:]


def literal_row(name, *, main=False, valid=True, locked=False, classification="merged-removable",
                registered=True):
    """A lane G WorktreeRow written as a literal (lead ruling R-56): the fields
    the gates read, and its `main`, `raw_path` and `registered` attributes."""
    raw = b"/w/" + name.encode() + (b"" if valid else b"\xff")
    row = project.WorktreeRow(path=project.json_path(raw)[0], branch=name, locked=locked,
                              classification=classification, path_valid_utf8=valid)
    row.raw_path, row.main, row.registered = raw, main, registered
    return row


def literal_plan(mode, target=None):
    """A Plan of mode for the literal rows, P being target in mode single."""
    plan = project.Plan({"root": Path("/w/main")}, types.SimpleNamespace(
        mode=mode, action=None if mode == "report" else "remove"))
    plan.target = target
    return plan


def packet_row(values, **fields):
    """One worktree row of the packet fixture, its fields as the fixture gives them."""
    path, branch, head = values
    row = project.WorktreeRow(
        path=path, present=True, branch=branch, head=head, upstream=f"origin/{branch}", remote_present=True,
        ahead=0, behind=0, dirty=False, ignored_files=0, current=False, merged_into_target=True,
        classification="merged-removable", locked=False, path_valid_utf8=True)
    row.update(fields)
    row.raw_path = path.encode()
    row.removal_args = ["-C", PACKET_REPOSITORY["root"], "worktree", "remove", path]
    return row


def packet_plan():
    """A Plan holding the packet fixture's values, its digest computed."""
    plan = literal_plan("all-safe")
    plan.repository, plan.merge_target = dict(PACKET_REPOSITORY), dict(PACKET_MERGE_TARGET)
    plan.selected = [packet_row(PACKET_SELECTED)]
    plan.excluded = [(packet_row(PACKET_EXCLUDED, dirty=True, ahead=2, merged_into_target=False,
                                 classification="dirty"), "dirty")]
    plan.digest = project.plan_digest(plan)
    return plan


class BatchTests(clean_support.CleanCase):

    def main_in_process(self, *argv, **patches):
        """project's main(ARGV) in this process, in self.env, each named function
        of project replaced by its stand-in: (status, stdout, stderr)."""
        out, err = io.StringIO(), io.StringIO()
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.dict(os.environ, self.env, clear=True))
            for name, stand_in in patches.items():
                stack.enter_context(mock.patch.object(project, name, stand_in))
            stack.enter_context(contextlib.redirect_stdout(out))
            stack.enter_context(contextlib.redirect_stderr(err))
            status = project.main([os.fspath(arg) for arg in argv])
        return status, out.getvalue(), err.getvalue()

    def snapshot(self, root):
        """What a run must leave unchanged: the registry, every ref, and every
        file of the repository's worktrees with its content (a "nothing
        changed" snapshot of this module's own, lead ruling R-56)."""
        registry = self.git(root, "worktree", "list", "--porcelain")
        trees = [Path(line[9:]) for line in registry.splitlines() if line.startswith("worktree ")]
        files = {}
        for tree in trees:
            for directory, names, filenames in os.walk(tree):
                names[:] = [name for name in names if name != ".git"]
                for name in filenames:
                    path = Path(directory) / name
                    if path.name != ".git":
                        files[str(path)] = path.read_bytes()
        return registry, self.git(root, "for-each-ref", "--format=%(refname) %(objectname)"), files

    def plan_header(self, root, name="main", source="main"):
        """The baseline header of a human plan (D18), from the fixtures."""
        return [f"Cleanup plan for {root}", TEXT["merge_target_line"].format(NAME=name, SOURCE=source),
                f"Freshness: {FRESHNESS}"]

    def preview_digest(self, root):
        """The plan_digest of `clean ROOT --all-safe --json`, and its selection."""
        document = self.run_json("clean", root, "--all-safe", "--json").document
        return document["plan_digest"], [entry["path"] for entry in document["selected"]]

    def assert_nothing_asked_or_removed(self, result, records):
        """No question was printed and no `worktree remove` child ran."""
        self.assertNotIn("[yes/N]", result.stdout + result.stderr)
        self.assertEqual([record for record in records if argv_words(record)[2:4] == ["worktree", "remove"]], [])

    def counting(self, env=None):
        """The counting wrapper first on PATH (in front of the real git): returns
        the environment to run with and the log, emptied."""
        bin_dir = self.base / "counting-bin"
        log = self.base / "children.log"
        clean_support.install_counting_git(bin_dir, log)
        clean_support.reset_child_log(log)
        return self.path_first(bin_dir, env), log

    def run_counted(self, *args, cwd=None, env=None):
        """`project ARGS...` under the counting wrapper: the run and its children."""
        env, log = self.counting(env)
        result = self.run_cli(*args, cwd=cwd, env=env)
        return result, clean_support.child_log(log)

    # T036: "The preview says what keeps each row".

    def test_clean_the_preview_says_what_keeps_each_row(self):
        # D18, plan review M8, lead ruling R-57: two rows selected, one excluded
        # as ignored-local-files and two as dirty, beside the main worktree. Each
        # pair is created in the order opposite to raw path byte order, which is
        # also not case-folded order ("Keep-b" < "keep-a" as bytes).
        root = self.repo()
        self.bare_remote()
        keep_a = self.merged_worktree("001-a", path=self.base / "keep-a")
        keep_b = self.merged_worktree("002-b", path=self.base / "Keep-b")
        ignored = self.merged_worktree("003-ignored", path=self.base / "ignored",
                                       setup=lambda tree: (tree / ".gitignore").write_text("local.env\n"))
        (ignored / "local.env").write_text("preserve")
        dirty_a = self.merged_worktree("004-a", path=self.base / "dirty-a")
        dirty_b = self.merged_worktree("005-b", path=self.base / "Dirty-b")
        for tree in (dirty_a, dirty_b):
            (tree / "uncommitted").write_text("preserve")
        before = self.snapshot(root)
        result = self.run_cli("clean", root, "--all-safe")
        self.assert_status(result, 0)
        steps = clean_support.NEXT_STEP_FIXTURES
        expected = self.plan_header(root) + [
            TEXT["selected_heading"].format(N=2),
            TEXT["selected_row"].format(PATH=keep_b, BRANCH="002-b"),
            TEXT["selected_row"].format(PATH=keep_a, BRANCH="001-a"),
            TEXT["excluded_heading"].format(M=4),
            TEXT["excluded_group"].format(REASON="main-worktree", K=1, NEXT_STEP=steps["main-worktree"]),
            TEXT["excluded_row"].format(PATH=root, BRANCH="main"),
            TEXT["excluded_group"].format(REASON="dirty", K=2, NEXT_STEP=steps["dirty"]),
            TEXT["excluded_row"].format(PATH=dirty_b, BRANCH="005-b"),
            TEXT["excluded_row"].format(PATH=dirty_a, BRANCH="004-a"),
            TEXT["excluded_group"].format(REASON="ignored-local-files", K=1,
                                          NEXT_STEP=steps["ignored-local-files"]),
            TEXT["excluded_row"].format(PATH=ignored, BRANCH="003-ignored")
            + TEXT["ignored_suffix"].format(N=1, SAMPLE="local.env"),
            TEXT["residual_window_line"],
        ]
        self.assertEqual((result.stdout, result.stderr), ("\n".join(expected) + "\n", ""))
        self.assertEqual(self.snapshot(root), before, "the registry, the branches and the files are unchanged")

    # T037: "Plan digest mismatch" (its apply clause is T041's, R-56 Q-5).

    def test_clean_plan_digest_mismatch(self):
        root = self.repo()
        self.bare_remote()
        first = self.merged_worktree("001-p1")
        second = self.merged_worktree("002-p2")
        (second / "uncommitted").write_text("preserve")
        digest, selected = self.preview_digest(root)
        self.assertEqual(selected, [str(first)])

        def second_becomes_eligible():
            (second / "uncommitted").unlink()

        def first_advances():
            (second / "uncommitted").write_text("preserve")
            self.assertEqual(self.preview_digest(root), (digest, [str(first)]), "the same plan as the preview")
            (first / "later").write_text("later")
            self.commit(first)
            self.git(first, "push", "origin", "001-p1")
            self.git(root, "merge", "--no-ff", "001-p1", "-m", "merge 001-p1 again")

        for label, change in (("a second merged worktree becomes eligible", second_becomes_eligible),
                              ("P1's branch advances", first_advances)):
            with self.subTest(label):
                change()
                before = self.snapshot(root)
                words = ("clean", root, "--all-safe", "--apply", "--yes", "--expect-plan", digest)
                result, records = self.run_counted(*words, "--json")
                self.assert_status(result, 2)
                document = self.load_json(result)
                fresh = document["plan_digest"]
                self.assertNotEqual(fresh, digest)
                message = TEXT["plan_digest_mismatch"].format(DIGEST=fresh, EXPECTED=digest)
                self.assertEqual((document["apply_allowed"], document["refusals"]),
                                 (False, [{"code": "plan-digest-mismatch", "message": message}]))
                self.assertIn(str(first), [entry["path"] for entry in document["selected"]])
                self.assert_nothing_asked_or_removed(result, records)
                # Human output: the fresh plan, then REFUSED: with its digest.
                result, records = self.run_counted(*words)
                self.assert_status(result, 2)
                self.assertTrue(result.stdout.startswith("\n".join(self.plan_header(root))), result.stdout)
                self.assertIn(TEXT["selected_row"].format(PATH=first, BRANCH="001-p1"), result.stdout.splitlines())
                self.assertEqual(result.stderr, f"REFUSED: {message}\n")
                self.assert_nothing_asked_or_removed(result, records)
                self.assertEqual(self.snapshot(root), before, "nothing changes")

    # T038: "Preview is advisory"; "Paths and empty plans".

    def test_clean_preview_is_advisory(self):
        root = self.repo()
        self.bare_remote()
        first = self.merged_worktree("001-p1")
        digest, selected = self.preview_digest(root)
        self.assertEqual(selected, [str(first)])
        (first / "uncommitted").write_text("preserve")
        before = self.snapshot(root)
        result, records = self.run_counted("clean", root, "--all-safe", "--apply", "--yes")
        self.assert_status(result, 0)
        steps = clean_support.NEXT_STEP_FIXTURES
        self.assertEqual((result.stdout, result.stderr), ("\n".join(self.plan_header(root) + [
            TEXT["excluded_heading"].format(M=2),
            TEXT["excluded_group"].format(REASON="main-worktree", K=1, NEXT_STEP=steps["main-worktree"]),
            TEXT["excluded_row"].format(PATH=root, BRANCH="main"),
            TEXT["excluded_group"].format(REASON="dirty", K=1, NEXT_STEP=steps["dirty"]),
            TEXT["excluded_row"].format(PATH=first, BRANCH="001-p1"),
            TEXT["empty_line"]]) + "\n", ""))
        self.assert_nothing_asked_or_removed(result, records)
        # With --expect-plan naming the preview's digest, the mismatch is refused
        # before the empty selection is reported.
        fresh, selected = self.preview_digest(root)
        self.assertEqual(selected, [])
        result, records = self.run_counted("clean", root, "--all-safe", "--apply", "--yes", "--expect-plan", digest)
        self.assert_status(result, 2)
        self.assertNotIn(TEXT["empty_line"], result.stdout)
        self.assertEqual(result.stderr,
                         "REFUSED: " + TEXT["plan_digest_mismatch"].format(DIGEST=fresh, EXPECTED=digest) + "\n")
        self.assert_nothing_asked_or_removed(result, records)
        self.assertEqual(self.snapshot(root), before)

    def test_clean_paths_and_empty_plans(self):
        steps = clean_support.NEXT_STEP_FIXTURES
        root = self.repo()
        self.bare_remote()
        spaced = self.merged_worktree("001-spaced", path=self.base / "with spaces" / "a tree")
        stale = self.base / "external" / "stale tree"
        self.git(root, "worktree", "add", "-b", "002-stale", stale)
        shutil.rmtree(stale)
        locked = self.merged_worktree("003-locked")
        self.git(root, "worktree", "lock", locked)
        with self.subTest("spaces, a missing external path and a lock"):
            before = self.snapshot(root)
            result = self.run_cli("clean", root, "--all-safe")
            self.assert_status(result, 0)
            self.assertEqual(result.stdout, "\n".join(self.plan_header(root) + [
                TEXT["selected_heading"].format(N=1),
                TEXT["selected_row"].format(PATH=spaced, BRANCH="001-spaced"),
                TEXT["excluded_heading"].format(M=3),
                TEXT["excluded_group"].format(REASON="main-worktree", K=1, NEXT_STEP=steps["main-worktree"]),
                TEXT["excluded_row"].format(PATH=root, BRANCH="main"),
                TEXT["excluded_group"].format(REASON="locked-worktree", K=1, NEXT_STEP=steps["locked-worktree"]),
                TEXT["excluded_row"].format(PATH=locked, BRANCH="003-locked"),
                TEXT["excluded_group"].format(REASON="stale-worktree", K=1,
                                              NEXT_STEP=TEXT["recommendation_stale_worktree"]),
                TEXT["excluded_row"].format(PATH=stale, BRANCH="002-stale"),
                TEXT["residual_window_line"]]) + "\n")
            document = self.run_json("clean", root, "--all-safe", "--json").document
            self.assertEqual([(entry["path"], entry["reason"]) for entry in document["excluded"]],
                             [(str(locked), "locked-worktree"), (str(stale), "stale-worktree"),
                              (str(root), "main-worktree")])
            # The path with spaces is one argument of its removal, exact, and a
            # command prints it shell-quoted (FR-041); in prose it is verbatim.
            [entry] = document["selected"]
            self.assertEqual(entry["operation"]["argv"][-3:], ["worktree", "remove", str(spaced)])
            self.assertEqual(project.human_path(os.fsencode(spaced), command=True), f"'{spaced}'")
            self.assertEqual(self.snapshot(root), before)
        with self.subTest("a complete plan that selects nothing"):
            empty = self.repo("empty-repo")
            self.bare_remote(empty, "empty-remote.git")
            dirty = self.merged_worktree("011-dirty", root=empty)
            (dirty / "uncommitted").write_text("preserve")
            before = self.snapshot(empty)
            expected = "\n".join(self.plan_header(empty) + [
                TEXT["excluded_heading"].format(M=2),
                TEXT["excluded_group"].format(REASON="main-worktree", K=1, NEXT_STEP=steps["main-worktree"]),
                TEXT["excluded_row"].format(PATH=empty, BRANCH="main"),
                TEXT["excluded_group"].format(REASON="dirty", K=1, NEXT_STEP=steps["dirty"]),
                TEXT["excluded_row"].format(PATH=dirty, BRANCH="011-dirty"),
                TEXT["empty_line"]]) + "\n"
            # As a preview, and under --apply without --yes on a standard input
            # that is not a terminal: no question and no confirmation-required.
            for words in (("--all-safe",), ("--all-safe", "--apply")):
                with self.subTest(arguments=words):
                    result, records = self.run_counted("clean", empty, *words)
                    self.assert_status(result, 0)
                    self.assertEqual((result.stdout, result.stderr), (expected, ""))
                    self.assert_nothing_asked_or_removed(result, records)
            self.assertEqual(self.snapshot(empty), before)
        with self.subTest("an incomplete plan that selects nothing"):
            if hasattr(os, "geteuid") and os.geteuid() == 0:
                self.skipTest("permission fixtures do not bind the superuser (effective uid 0)")
            unreadable = self.repo("unreadable-repo")
            hidden = self.base / "hidden"
            hidden.mkdir()
            self.git(unreadable, "worktree", "add", "-b", "021-hidden", hidden / "tree")
            hidden.chmod(0o600)
            self.addCleanup(hidden.chmod, 0o700)
            # The row's path could not be read, so its next step and the
            # remedy name no git worktree prune (#19's round (l); W87 M-1,
            # lead ruling R-307).
            refused = "REFUSED: " + TEXT["plan_incomplete"].format(
                CODE="inspection-incomplete", REMEDY=TEXT["remedy_inspection_incomplete_unread"]) + "\n"
            # The preview exits 1 and, as the plan is refused (FR-024), names the
            # refusal and its remedy too.
            preview = self.run_cli("clean", unreadable, "--all-safe")
            self.assert_status(preview, 1)
            self.assertEqual(preview.stderr, refused)
            self.assertNotIn(TEXT["empty_line"], preview.stdout, "never reported as empty")
            self.assertIn(TEXT["excluded_group"].format(REASON="inspection-error", K=1,
                                                        NEXT_STEP=TEXT["next_step_unread_row"]),
                          preview.stdout.splitlines())
            for words in (("--all-safe", "--apply"), ("--all-safe", "--apply", "--yes")):
                with self.subTest(arguments=words):
                    result, records = self.run_counted("clean", unreadable, *words)
                    self.assert_status(result, 2)
                    self.assertEqual((result.stdout, result.stderr), (preview.stdout, refused))
                    self.assert_nothing_asked_or_removed(result, records)
            document = self.run_json("clean", unreadable, "--all-safe", "--apply", "--json").document
            self.assertEqual((document["completeness"], document["apply_allowed"], document["selected"],
                              [refusal["code"] for refusal in document["refusals"]]),
                             ("incomplete", False, [], ["inspection-incomplete"]))

    # T039: "Invalid argument combinations".

    def test_clean_invalid_argument_combinations(self):
        root = self.repo()
        tree = self.base / "w"
        cases = [
            (("--all-safe", "--action", "remove"), TEXT["invalid_arguments_all_safe"]),
            (("--all-safe", "--branch", "b"), TEXT["invalid_arguments_all_safe"]),
            (("--all-safe", "--worktree", tree), TEXT["invalid_arguments_all_safe"]),
            (("--all-safe", "--apply", "--action", "remove", "--worktree", tree),
             TEXT["invalid_arguments_all_safe"]),
            (("--expect-plan", DIGEST), TEXT["invalid_arguments_expect_plan"]),
            (("--all-safe", "--expect-plan", DIGEST), TEXT["invalid_arguments_expect_plan"]),
            (("--apply", "--expect-plan", DIGEST), TEXT["invalid_arguments_expect_plan"]),
            (("--apply", "--action", "remove", "--worktree", tree, "--expect-plan", DIGEST),
             TEXT["invalid_arguments_expect_plan"]),
            (("--all-safe", "--apply", "--expect-plan", "abc"), TEXT["invalid_arguments_expect_plan_value"]),
            (("--all-safe", "--apply", "--expect-plan", "a" * 63), TEXT["invalid_arguments_expect_plan_value"]),
            (("--all-safe", "--apply", "--expect-plan", "a" * 65), TEXT["invalid_arguments_expect_plan_value"]),
            (("--all-safe", "--apply", "--expect-plan", "A" * 64), TEXT["invalid_arguments_expect_plan_value"]),
            # The baseline's messages, now coded `invalid-arguments`.
            (("--apply",), "--apply requires --action push|remove|delete-branch"),
            (("--apply", "--action", "push"), "Push cleanup requires --branch BRANCH"),
            (("--apply", "--action", "remove"), "Worktree cleanup requires --worktree PATH"),
            (("--apply", "--action", "delete-branch"), "Branch cleanup requires --branch BRANCH"),
        ]
        json_kept = "--json cannot be combined with --apply; use JSON for the read-only plan."
        for extra, message in cases:
            # Under --json, push and delete-branch meet the kept --apply --json row first (below).
            for as_json in (False,) if "push" in extra or "delete-branch" in extra else (False, True):
                with self.subTest(arguments=[os.fspath(arg) for arg in extra], json=as_json):
                    words = (*extra, "--json") if as_json else extra
                    result, records = self.run_counted("clean", root, *words)
                    self.assert_status(result, 2)
                    self.assertEqual(records, [], "no child ran, not even git --version")
                    if as_json:
                        document = self.load_json(result)
                        self.assertEqual((document["code"], document["error"], document["refusals"]),
                                         ("invalid-arguments", message,
                                          [{"code": "invalid-arguments", "message": message}]))
                        self.assertEqual(result.stderr, "")
                    else:
                        self.assertEqual((result.stdout, result.stderr), ("", f"REFUSED: {message}\n"))
        # --apply --json stays refused for push and delete-branch (OQ-10), with
        # the baseline's message, now coded.
        for action in ("push", "delete-branch"):
            with self.subTest(action=action, json=True):
                result, records = self.run_counted("clean", root, "--apply", "--action", action,
                                                   "--branch", "b", "--json")
                self.assert_status(result, 2)
                self.assertEqual(records, [])
                document = self.load_json(result)
                self.assertEqual((document["code"], document["error"]), ("invalid-arguments", json_kept))
        # An argument-parser usage error prints the parser's message, exits 2
        # and prints no JSON document.
        for words in (("--all-safe", "--apply", "--expect-plan"), ("--action", "bogus"), ("--no-such-flag",)):
            with self.subTest(usage=words):
                result, records = self.run_counted("clean", root, *words, "--json")
                self.assert_status(result, 2)
                self.assertEqual((result.stdout, records), ("", []))
                self.assertIn("usage: project", result.stderr)

    def test_clean_invalid_argument_combinations_unrefused_flags(self):
        # Plan review M9: flags no row of the table refuses keep the baseline's
        # handling.
        root = self.repo()
        self.bare_remote()
        merged = self.merged_worktree("001-merged")
        dirty = self.merged_worktree("002-dirty")
        (dirty / "uncommitted").write_text("preserve")
        before = self.git(root, "worktree", "list", "--porcelain")
        # Without --apply, --yes, --action, --branch and --worktree are ignored:
        # the run is a report (or, with --all-safe, a preview), exit 0.
        plain = self.load_json(self.run_cli("clean", root, "--json"))
        for extra in (("--yes",), ("--action", "remove"), ("--action", "push"), ("--branch", "002-dirty"),
                      ("--worktree", merged), ("--action", "remove", "--worktree", merged, "--yes")):
            with self.subTest(ignored=[os.fspath(arg) for arg in extra]):
                result = self.run_cli("clean", root, *extra, "--json")
                self.assert_status(result, 0)
                document = self.load_json(result)
                self.assertEqual(document["target_branch"], "main")
                self.assertEqual([(row["path"], row["classification"]) for row in document["worktrees"]],
                                 [(row["path"], row["classification"]) for row in plain["worktrees"]])
        with self.subTest(ignored=["--all-safe", "--yes"]):
            self.assert_status(self.run_cli("clean", root, "--all-safe", "--yes"), 0)
        # An unused --branch beside --apply --action remove, or --worktree beside
        # --apply --action push, is ignored: the run ends as it does without it.
        pairs = [
            (("--apply", "--action", "remove", "--worktree", dirty, "--yes"), ("--branch", "001-merged")),
            (("--apply", "--action", "push", "--branch", "002-dirty", "--yes"), ("--worktree", merged)),
        ]
        for words, unused in pairs:
            with self.subTest(unused=[os.fspath(arg) for arg in unused]):
                without = self.run_cli("clean", root, *words)
                given = self.run_cli("clean", root, *words, *unused)
                self.assert_status(without, 2)
                self.assertEqual((given.returncode, given.stdout, given.stderr),
                                 (without.returncode, without.stdout, without.stderr))
        self.assertEqual(self.git(root, "worktree", "list", "--porcelain"), before)
        self.assertTrue((dirty / "uncommitted").is_file())

    def test_clean_a_relative_configuration_path_after_the_argument_checks(self):
        # Brett Heap's ruling LQ-15 (lead ruling R-102) in the order of a run
        # (the project-clean delta, "Clean reports local worktree state"):
        # under a relative HOME the argument checks, which start no Git child,
        # still refuse invalid-arguments first; the same run with its
        # arguments made valid then refuses relative-config-path, exit 2,
        # again with no child, before the version check.
        root = self.repo()
        tree = self.base / "w"
        env = dict(self.env, HOME="h")
        relative = TEXT["relative_config_path"].format(NAME="HOME")
        cases = [
            (("--all-safe", "--action", "remove"), TEXT["invalid_arguments_all_safe"], ("--all-safe",)),
            (("--expect-plan", DIGEST), TEXT["invalid_arguments_expect_plan"],
             ("--all-safe", "--apply", "--expect-plan", DIGEST)),
            (("--all-safe", "--apply", "--expect-plan", "abc"), TEXT["invalid_arguments_expect_plan_value"],
             ("--all-safe", "--apply", "--yes")),
            (("--apply", "--action", "remove"), "Worktree cleanup requires --worktree PATH",
             ("--apply", "--action", "remove", "--worktree", tree, "--yes")),
        ]
        for invalid, message, valid in cases:
            for as_json in (False, True):
                label = [os.fspath(arg) for arg in invalid]
                with self.subTest(arguments=label, json=as_json):
                    extra = ("--json",) if as_json else ()
                    first, records = self.run_counted("clean", root, *invalid, *extra, env=env)
                    self.assert_status(first, 2)
                    self.assertEqual(records, [], "no child ran, not even git --version")
                    second, records = self.run_counted("clean", root, *valid, *extra, env=env)
                    self.assert_status(second, 2)
                    self.assertEqual(records, [])
                    if as_json:
                        self.assertEqual([(document["code"], document["error"]) for document in
                                          (self.load_json(first), self.load_json(second))],
                                         [("invalid-arguments", message), ("relative-config-path", relative)])
                    else:
                        self.assertEqual([(result.stdout, result.stderr) for result in (first, second)],
                                         [("", f"REFUSED: {message}\n"), ("", f"REFUSED: {relative}\n")])

    # T040: the first gates, the plan document and the estimates.

    def test_clean_first_gates_in_order(self):
        # FR-020, data-model.md "Gate": gate_rows() on literal rows, with no
        # child and no filesystem call; the first failing gate is the reason.
        main = literal_row("main", main=True, valid=False, locked=True, classification="protected-default")
        rows = {
            "bytes": literal_row("bytes", valid=False, locked=True, classification="dirty"),
            "locked": literal_row("locked", locked=True, classification="dirty"),
            "dirty": literal_row("dirty", classification="dirty"),
            # Lead ruling R-53 P-16: a registration never read passes gate 3 and
            # is excluded at gate 5 by its class, never as registration-mismatch.
            "unread": literal_row("unread", classification="stale-worktree", registered=None),
            "unverified": literal_row("unverified", classification="inspection-error", registered=None),
            "p": literal_row("p"),
            "q": literal_row("q"),
        }
        expected = {"main": "main-worktree", "bytes": "unsupported-path-bytes", "locked": "locked-worktree",
                    "dirty": "dirty", "unread": "stale-worktree", "unverified": "inspection-error"}
        order = [main, rows["q"], rows["unverified"], rows["p"], rows["dirty"], rows["unread"],
                 rows["locked"], rows["bytes"]]

        def outcome(plan, gated=None):
            selected, excluded = project.gate_rows(gated or order, plan, None)
            return ([row["branch"] for row in selected], [(row["branch"], reason) for row, reason in excluded])

        def by_bytes(names):
            return sorted(names, key=lambda name: ({"main": main, **rows}[name]).raw_path)

        with mock.patch.object(project, "run_bounded", side_effect=AssertionError("a Git child ran")), \
                mock.patch.object(project, "fs_call", side_effect=AssertionError("a filesystem call ran")), \
                mock.patch.object(project, "reflog_gate", return_value=None), \
                mock.patch.object(project, "index_gates", return_value=None), \
                mock.patch.object(project, "admin_state_gates", return_value=None):
            for mode in ("all-safe", "report"):
                with self.subTest(mode=mode):
                    self.assertEqual(outcome(literal_plan(mode)),
                                     (["p", "q"], [(name, expected[name]) for name in by_bytes(expected)]))
            with self.subTest("not-requested only in mode single, for a row other than P"):
                single = {**expected, "q": "not-requested"}
                self.assertEqual(outcome(literal_plan("single", rows["p"])),
                                 (["p"], [(name, single[name]) for name in by_bytes(single)]))
                none = {**expected, "p": "not-requested", "q": "not-requested"}
                self.assertEqual(outcome(literal_plan("single")),
                                 ([], [(name, none[name]) for name in by_bytes(none)]), "no single P: none selected")
            # The stubs' slots in the order: gate 3 after gate 2 and before gate 4,
            # gate 7 after gate 6, gate 8 over the rows past gate 7, and gates 9
            # and 10 only for the rows gate 8 takes.
            mismatched = literal_row("mismatched", locked=True, classification="inspection-error", registered=False)
            hidden = literal_row("bytes-mismatched", valid=False, registered=False)
            unstarted = literal_row("r")
            gated = [main, hidden, mismatched, rows["p"], rows["q"], unstarted]
            seen = []

            def reflog(row, plan, run):
                if row is unstarted:
                    row.unprobed = True  # R-67 (a): a read past its budget still names a reason
                    return "reflog-unavailable"
                return "unstarted-branch" if row is rows["q"] else None

            def index(row, plan, run):
                seen.append(row["branch"])
                return "hidden-local-state" if row is rows["p"] else None

            with mock.patch.object(project, "registration_gate",
                                   side_effect=lambda row, plan, run: "registration-mismatch"
                                   if row.registered is False else None), \
                    mock.patch.object(project, "reflog_gate", side_effect=reflog), \
                    mock.patch.object(project, "index_gates", side_effect=index):
                self.assertEqual(outcome(literal_plan("all-safe"), gated), ([], sorted([
                    ("main", "main-worktree"), ("bytes-mismatched", "unsupported-path-bytes"),
                    ("mismatched", "registration-mismatch"), ("p", "hidden-local-state"),
                    ("q", "unstarted-branch"), ("r", "reflog-unavailable")],
                    key=lambda item: b"/w/" + item[0].encode() + (b"\xff" if item[0] == "bytes-mismatched" else b""))))
                self.assertEqual(seen, ["p"])
                seen.clear()
                self.assertEqual(outcome(literal_plan("single", unstarted), gated)[1][-2:],
                                 [("q", "not-requested"), ("r", "reflog-unavailable")])
                # Gate 8 takes the first candidate and defers the rest: the
                # deferred row gets no index gate.
                with mock.patch.object(project, "deferral_gate",
                                       side_effect=lambda candidates, plan: (candidates[:1], candidates[1:])), \
                        mock.patch.object(project, "reflog_gate", return_value=None):
                    seen.clear()
                    self.assertEqual(outcome(literal_plan("report"), [main, rows["p"], rows["q"]]),
                                     ([], [("main", "main-worktree"), ("p", "hidden-local-state"),
                                           ("q", "deferred-target-cap")]))
                    self.assertEqual(seen, ["p"])
        # Gate 3 is pure under R-53 P-16 and passes every row whose registration
        # was not read and found to disagree; gates 7, 9 and 10 read files or
        # run children, so their own lanes' tests pin them (lead ruling R-71).
        # The deferral stub takes every candidate.
        plan = literal_plan("all-safe")
        for row in (main, *rows.values()):
            self.assertEqual([project.registration_gate(row, plan, None)], [None])
        self.assertEqual(project.deferral_gate([rows["p"], rows["q"]], plan), ([rows["p"], rows["q"]], []))

    def test_clean_plan_document_keys(self):
        # Plan review M6, contracts/project-clean.md "Plan envelope".
        root = self.repo()
        self.bare_remote()
        trees = [self.merged_worktree("001-first"), self.merged_worktree("002-second")]
        dirty = self.merged_worktree("003-dirty")
        (dirty / "uncommitted").write_text("preserve")
        common = self.common_dir()
        found = os.lstat(common)
        main_sha = self.git(root, "rev-parse", "main").strip()
        for extra, mode, rows_cap in ((("--all-safe",), "all-safe", 128), ((), "report", 256)):
            with self.subTest(mode=mode):
                result = self.run_cli("clean", root, *extra, "--json")
                self.assert_status(result, 0)
                document = self.load_json(result)
                self.assertEqual(list(document), PLAN_KEYS)
                self.assertEqual((document["schema_version"], document["mode"], document["root"],
                                  document["target_branch"], document["tracking_freshness"]),
                                 (1, mode, str(root), "main", FRESHNESS))
                self.assertEqual(list(document["repository"].items()), list(zip(REPOSITORY_KEYS, (
                    str(root), str(common), found.st_dev, found.st_ino, True, True))))
                self.assertEqual(document["merge_target"], {"name": "main", "source": "main", "sha": main_sha})
                self.assertEqual(document["limits"], {**LIMITS, "worktree_rows": rows_cap})
                self.assertEqual(list(document["limits"]), list(LIMITS))
                self.assertEqual(list(document["budget"].items()), list(BUDGET.items()))
                self.assertEqual((document["omitted"], document["notes"], document["completeness"],
                                  document["apply_allowed"], document["refusals"]),
                                 ({"count": 0, "exactness": "exact"}, [], "complete", mode == "all-safe", []))
                self.assertRegex(document["plan_digest"], HEX64)
                self.assertEqual([entry["path"] for entry in document["selected"]], [str(tree) for tree in trees])
                for entry, tree in zip(document["selected"], trees):
                    branch = tree.name.removesuffix("-tree")
                    stat = os.lstat(tree)
                    self.assertEqual(list(entry), SELECTED_KEYS)
                    self.assertEqual(
                        [entry[key] for key in SELECTED_KEYS[:-1]],
                        [str(tree), True, branch, self.git(tree, "rev-parse", "HEAD").strip(), f"origin/{branch}",
                         self.git(root, "rev-parse", f"refs/remotes/origin/{branch}").strip(), 0, 0,
                         stat.st_dev, stat.st_ino, tree.name, False,
                         True, False, 0, True, True, False, "merged-removable"])
                    self.assertEqual(entry["operation"], {"kind": "worktree-remove", "argv": project.git_argv(
                        "removal", ["-C", str(root), "worktree", "remove", str(tree)])})
                self.assertEqual([list(entry) for entry in document["excluded"]], [EXCLUDED_KEYS] * 2)
                self.assertEqual([tuple(entry.values()) for entry in document["excluded"]], [
                    (str(dirty), True, "003-dirty", "dirty", "dirty"),
                    (str(root), True, "main", "protected-default", "main-worktree")])

    def test_clean_plan_document_bytes(self):
        # Plan review M6: one document, json.dumps(doc, indent=2,
        # ensure_ascii=True) and one newline, its keys in the contract's order;
        # plan notes are {code, message} objects and row notes code strings.
        root = self.repo()
        self.bare_remote()
        accented = self.merged_worktree("001-accented", path=self.base / ("caf" + E_ACUTE + "-tree"))
        gone = self.merged_worktree("002-gone")
        for path in gone.iterdir():
            if path.name != ".git":
                path.unlink()  # every tracked file deleted by hand: a partial removal (D4)
        result = self.run_cli("clean", root, "--all-safe", "--json")
        self.assert_status(result, 0)
        document = self.load_json(result)
        self.assertEqual(result.stdout, json.dumps(document, indent=2, ensure_ascii=True) + "\n")
        self.assertTrue(result.stdout.isascii())
        self.assertEqual(list(document), PLAN_KEYS)
        self.assertEqual([entry["path"] for entry in document["selected"]], [str(accented)])
        rows = {row["path"]: row for row in document["worktrees"]}
        self.assertEqual(rows[str(gone)]["notes"], ["partially-removed"])
        self.assertEqual([row["notes"] for path, row in rows.items() if path != str(gone)], [[], []])
        # The merge target's notes move into the plan's notes (P-13), each a
        # {code, message} object, under a stand-in that names one.
        resolve = project.resolve_merge_target
        note = {"code": "merge-target-conflict",
                "message": TEXT["note_merge_target_conflict"].format(NAME="main", OTHER="develop")}

        def with_note(refs, declared):
            return {**resolve(refs, declared), "notes": [dict(note)]}

        status, out, err = self.main_in_process("clean", root, "--all-safe", "--json",
                                                resolve_merge_target=with_note)
        self.assertEqual((status, err), (0, ""))
        noted = json.loads(out)
        self.assertEqual(out, json.dumps(noted, indent=2, ensure_ascii=True) + "\n")
        self.assertEqual((noted["notes"], noted["merge_target"]), ([note], document["merge_target"]))

    def test_clean_estimates_are_the_apply_upper_bound(self):
        # Plan review M7, research.md R8, lead rulings R-27 and R-56: in every
        # mode, previews and reports included, probes.estimated is F + W + E +
        # 6T + 3 and operations.estimated is T, so that a run's estimate is its
        # counted children plus 6T + 3, six the children of one revalidation in
        # a repository without extensions.worktreeConfig (D7, as LQ-13 amends
        # it; lead ruling R-165). F, W and E come from the counting log: W the
        # status probes, E the hidden-state probes (`ls-files`), never assumed
        # zero, F every other child, the reachability probes among them; no
        # removal runs.
        root = self.repo()
        self.bare_remote()
        target = self.merged_worktree("001-merged")
        self.merged_worktree("002-merged")
        dirty = self.merged_worktree("003-dirty")
        (dirty / "uncommitted").write_text("preserve")
        runs = (("report", ("--json",), 0, 2), ("all-safe", ("--all-safe", "--json"), 0, 2),
                ("single", ("--apply", "--action", "remove", "--worktree", target, "--json"), 2, 1))
        for mode, words, status, targets in runs:
            with self.subTest(mode=mode):
                result, records = self.run_counted("clean", root, *words)
                self.assert_status(result, status)
                document = self.load_json(result)
                self.assertEqual((document["mode"], len(document["selected"])), (mode, targets))
                kinds = [argv_words(record)[2:3] for record in records]
                self.assertEqual([record for record in records if argv_words(record)[2:4] == ["worktree", "remove"]],
                                 [])
                self.assertIn(["--version"], [argv_words(record) for record in records], "F counts row 1")
                status_children, hidden = kinds.count(["status"]), kinds.count(["ls-files"])
                repository_wide = len(records) - status_children - hidden
                self.assertEqual(status_children, 4, "one status probe per present, verified row")
                self.assertEqual(document["probes"], {
                    "estimated": repository_wide + status_children + hidden + 6 * targets + 3,
                    "performed": len(records)})
                self.assertEqual(document["operations"], {"estimated": targets, "performed": 0})

    def test_clean_plan_digest_canonical_text(self):
        # Research.md R12, lead ruling R-34: the packet's own fixture values give
        # its own digest, and the mode, observed_at, excluded and the notes
        # leave it unchanged.
        plan = packet_plan()
        self.assertEqual(project.plan_digest(plan), PACKET_DIGEST)
        for change in ("mode", "excluded", "notes", "flags"):
            with self.subTest(unchanged_by=change):
                varied = packet_plan()
                if change == "mode":
                    varied.mode = "report"
                elif change == "excluded":
                    varied.excluded = []
                elif change == "notes":
                    varied.notes = [{"code": "merge-target-conflict", "message": "m"}]
                else:
                    varied.repository.update(root_valid_utf8=False, common_dir_valid_utf8=False)
                    varied.merge_target["source"] = "manifest"
                self.assertEqual(project.plan_digest(varied), PACKET_DIGEST)
        stamps = iter(("2026-10-07T14:03:12Z", "2026-10-20T18:00:00Z"))
        with mock.patch.object(project, "observed_at", side_effect=lambda: next(stamps)):
            first, second = project.plan_document(packet_plan()), project.plan_document(packet_plan())
        self.assertNotEqual(first["observed_at"], second["observed_at"])
        self.assertEqual((first["plan_digest"], second["plan_digest"]), (PACKET_DIGEST, PACKET_DIGEST))
        # Each covered value changes it: a selected head, the merge target's SHA,
        # the repository's inode, and a selection withheld (null).
        for change in ("head", "sha", "ino", "withheld"):
            with self.subTest(changed=change):
                varied = packet_plan()
                if change == "head":
                    varied.selected[0]["head"] = PACKET_EXCLUDED[2]
                elif change == "sha":
                    varied.merge_target["sha"] = PACKET_SELECTED[2]
                elif change == "ino":
                    varied.repository["ino"] += 1
                else:
                    varied.selected = None
                self.assertNotEqual(project.plan_digest(varied), PACKET_DIGEST)
        # ensure_ascii=False serves the digest's text alone: a non-ASCII branch
        # is hashed as its UTF-8 bytes, never as a \\u escape.
        plan.selected[0]["branch"] = "feature/caf" + E_ACUTE
        text = json.dumps({"merge_target": {"name": "main", "sha": PACKET_MERGE_TARGET["sha"]},
                           "repository": {key: PACKET_REPOSITORY[key] for key in ("root", "common_dir", "dev", "ino")},
                           "selected": [[PACKET_SELECTED[0], "feature/caf" + E_ACUTE, PACKET_SELECTED[2]]]},
                          sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        self.assertIn("caf" + E_ACUTE, text)
        self.assertEqual(project.plan_digest(plan), hashlib.sha256(text.encode("utf-8")).hexdigest())

    # T052: the printed plan.

    def test_clean_a_reader_that_closes_standard_output(self):
        # Lead rulings R-55 and R-59 D2: standard output a pipe whose read end
        # is closed, as tests/test_project.py's test_advisory_with_stderr_on_a_closed_pipe
        # closes one. Before the apply phase the failed write is internal-error,
        # exit 2, nothing mutated, no traceback, and never exit 120.
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-merged")
        before = self.snapshot(root)
        env, log = self.counting()
        for words in (("--all-safe",), ("--all-safe", "--json"), ("--all-safe", "--apply", "--yes")):
            with self.subTest(arguments=words):
                clean_support.reset_child_log(log)
                read_end, write_end = os.pipe()
                os.close(read_end)
                try:
                    result = subprocess.run(clean_support.cli_argv("clean", root, *words), cwd=self.base, env=env,
                                            stdin=subprocess.DEVNULL, stdout=write_end, stderr=subprocess.PIPE,
                                            text=True, timeout=clean_support.TIMEOUT)
                finally:
                    os.close(write_end)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertNotIn("Exception ignored", result.stderr)
                if "--json" in words:
                    self.assertEqual(result.stderr, "", "under --json the error goes to standard output")
                else:
                    self.assertRegex(result.stderr, r"\AREFUSED: BrokenPipeError: [^\n]*\n\Z")
                removals = [record for record in clean_support.child_log(log)
                            if argv_words(record)[2:4] == ["worktree", "remove"]]
                self.assertEqual(removals, [], "the plan failed to print before the apply phase")
                self.assertEqual(self.snapshot(root), before)
                self.assertTrue(tree.is_dir())

    def test_clean_the_preview_says_what_keeps_each_row_single_mode(self):
        # Lead ruling R-59 D8, R-62 (b): --apply --action remove --worktree P,
        # standard input not a terminal and no --yes, beside other eligible rows.
        root = self.repo()
        self.bare_remote()
        target = self.merged_worktree("001-p")
        others = [self.merged_worktree("002-q"), self.merged_worktree("003-r")]
        dirty = self.merged_worktree("004-dirty")
        (dirty / "uncommitted").write_text("preserve")
        before = self.snapshot(root)
        result = self.run_cli("clean", root, "--apply", "--action", "remove", "--worktree", target)
        self.assert_status(result, 2)
        steps = clean_support.NEXT_STEP_FIXTURES
        expected = self.plan_header(root) + [
            TEXT["selected_heading"].format(N=1),
            TEXT["selected_row"].format(PATH=target, BRANCH="001-p"),
            TEXT["excluded_heading"].format(M=4),
            TEXT["excluded_group"].format(REASON="main-worktree", K=1, NEXT_STEP=steps["main-worktree"]),
            TEXT["excluded_row"].format(PATH=root, BRANCH="main"),
            TEXT["excluded_group"].format(REASON="dirty", K=1, NEXT_STEP=steps["dirty"]),
            TEXT["excluded_row"].format(PATH=dirty, BRANCH="004-dirty"),
            TEXT["excluded_group"].format(REASON="not-requested", K=2, NEXT_STEP=steps["not-requested"]),
            TEXT["excluded_row"].format(PATH=others[0], BRANCH="002-q"),
            TEXT["excluded_row"].format(PATH=others[1], BRANCH="003-r"),
            TEXT["residual_window_line"],
        ]
        # T053's confirmation-required refuses, before the baseline question.
        self.assertEqual((result.stdout, result.stderr),
                         ("\n".join(expected) + "\n", "REFUSED: " + TEXT["confirmation_required"] + "\n"))
        self.assertEqual(self.snapshot(root), before, "nothing removed")

    def test_clean_the_preview_says_what_keeps_each_row_single_mode_shared_path(self):
        # Lead rulings R-62 (a) and R-67 (b) as corrected: a P that more than
        # one registry entry names, by raw bytes or by realpath, is P's own
        # evidence incomplete: nothing is selected for it, no
        # worktree-not-found, and the run refuses with inspection-incomplete,
        # exit 2, before any target-excluded; nothing is removed. P's rows are
        # excluded as registration-mismatch, by bytes and by realpath alike, so
        # the remedy is the variant naming the unset (#19's round (h) at
        # b3228bb, design.md D18).
        refused = "REFUSED: " + TEXT["plan_incomplete"].format(
            CODE="inspection-incomplete", REMEDY=TEXT["remedy_inspection_incomplete_redirect"]) + "\n"
        # Raw bytes: a copied admin directory lists the same path twice (lane G's
        # fixture), and both rows are inspection-error (registration-mismatch).
        bytes_root = self.repo("bytes-repo")
        self.bare_remote(bytes_root, "bytes-remote.git")
        shared = self.merged_worktree("001-shared", root=bytes_root)
        admin = self.common_dir(bytes_root) / "worktrees"
        shutil.copytree(admin / shared.name, admin / f"{shared.name}-copy")
        self.assertEqual(self.git(bytes_root, "worktree", "list", "--porcelain").splitlines().count(
            f"worktree {shared}"), 2)
        # Realpath: a second entry naming the same worktree through a symbolic
        # link, which the two-way check passes (R-67 (c), a later evidence fix),
        # in a repository with no inspection-error row, so that P's own match,
        # not another row, is what refuses (check 3 of the single-mode order).
        real_root = self.repo("realpath-repo")
        self.bare_remote(real_root, "realpath-remote.git")
        spelled = self.merged_worktree("002-spelled", root=real_root)
        link = self.base / "link"
        link.symlink_to(self.base)
        admin = self.common_dir(real_root) / "worktrees"
        shutil.copytree(admin / spelled.name, admin / f"{spelled.name}-copy")
        (admin / f"{spelled.name}-copy" / "gitdir").write_text(f"{link / spelled.name / '.git'}\n")
        self.assertIn(f"worktree {link / spelled.name}",
                      self.git(real_root, "worktree", "list", "--porcelain").splitlines())
        report = self.run_json("clean", real_root, "--json").document
        self.assertEqual([row["classification"] for row in report["worktrees"]],
                         ["protected-default", "inspection-error", "inspection-error"])
        for root, target in ((bytes_root, shared), (real_root, spelled), (real_root, link / spelled.name)):
            with self.subTest(worktree=os.fspath(target)):
                before = self.snapshot(root)
                result, records = self.run_counted("clean", root, "--apply", "--action", "remove",
                                                   "--worktree", target, "--yes")
                self.assert_status(result, 2)
                self.assertEqual(result.stderr, refused)
                self.assertNotIn(TEXT["selected_heading"].format(N=1), result.stdout)
                self.assert_nothing_asked_or_removed(result, records)
                document = self.run_json("clean", root, "--apply", "--action", "remove", "--worktree", target,
                                         "--yes", "--json").document
                self.assertEqual(([refusal["code"] for refusal in document["refusals"]], document["selected"],
                                  document["completeness"], document["apply_allowed"]),
                                 (["inspection-incomplete"], [], "incomplete", False))
                self.assertEqual(self.snapshot(root), before)


if __name__ == "__main__":
    unittest.main()
