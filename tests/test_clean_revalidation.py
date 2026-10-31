"""The revalidation lane of feature 004's User Story 4 (T079 to T085): a change
after the plan stops the removal (design D7; the project-clean-review-safety
delta, "Cleanup revalidates destructive actions" and "Cleanup states a narrow
guarantee and its residual window"; data-model.md, "Revalidation step and
probes_performed", "Target result and reconciliation record" and "Target
stages"; research.md R16; lead rulings R-22, R-41, R-68, R-76 and R-77).

Most tests run project's main() in process for `clean ROOT --all-safe --apply
--json`, with standard input a terminal and ask_removal() patched as T046
patches it, so that a change made "at the question" lands after the plan is
shown and before the first revalidation (lead ruling R-76); main() restores
the signal handlers it installs, and no signal is sent to the test process
(rule 7). A change between revalidation and removal, or between Git's removal
and the rescan, is made by the counting wrapper's pre- or post-remove hook,
which calls the real git by its absolute path. Expected human text comes from
clean_support's fixtures (rule 8).
"""
import contextlib
import errno
import io
import json
import os
from pathlib import Path
import shlex
import shutil
import signal
import subprocess
import time
import types
import unittest
from unittest import mock

import clean_support

project = clean_support.load_project()
TEXT = clean_support.TEXT_FIXTURES
REAL_GIT = clean_support.REAL_GIT

RECONCILIATION_KEYS = ["registry_entry_present", "path_present", "branch_present", "branch_sha",
                       "reconciled"]
SCOPED_SIGNALS = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)
NAMES = ("001-p", "002-q", "003-r", "004-s", "005-t")


def strip_pins(argv):
    """A child's argument vector, as the counting wrapper records it (after
    `git`), split into its leading `-c NAME=VALUE` pins and the rest."""
    at = 0
    while at + 1 < len(argv) and argv[at] == "-c":
        at += 2
    return list(argv[:at]), list(argv[at:])


def subcommand(record):
    """A counted child's words after its pins and its `-C DIR`, if any."""
    words = strip_pins(record.argv)[1]
    return words[2:] if words[:1] == ["-C"] else words


def directory(record):
    """The `-C DIR` a counted child names, or None."""
    words = strip_pins(record.argv)[1]
    return words[1] if words[:1] == ["-C"] else None


def is_removal(record):
    return subcommand(record)[:2] == ["worktree", "remove"]


def signal_state():
    """The handlers of SIGINT, SIGTERM and SIGHUP and the wakeup descriptor."""
    handlers = tuple(signal.getsignal(signum) for signum in SCOPED_SIGNALS)
    wakeup = signal.set_wakeup_fd(-1)
    if wakeup != -1:
        signal.set_wakeup_fd(wakeup)
    return handlers, wakeup


def record(registry_entry_present, path_present, branch_present, branch_sha):
    """A reconciliation record, as project builds it (reconciled derived)."""
    return project.reconciliation_record(registry_entry_present, path_present, branch_present, branch_sha)


def when_target(path, *commands):
    """sh text for a counting-wrapper hook that runs commands only when the
    worktree being removed ($target) is path."""
    return f"if [ \"$target\" = {shlex.quote(os.fsdecode(path))} ]; then\n" + "\n".join(commands) + "\nfi"


def sh_git(*args):
    """One real-git command line for a hook, by absolute path (lead ruling R-31)."""
    return " ".join(shlex.quote(os.fsdecode(arg)) for arg in (REAL_GIT, *args))


class Terminal(io.StringIO):
    """A standard input that says it is a terminal, as T046's test uses."""

    def isatty(self):
        return True


class RevalidationTests(clean_support.CleanCase):

    # Fixtures: one repository per case, its worktrees merged, clean and
    # published, each with a commit of its own (merged_worktree()).

    def batch(self, case, count=2, holder=None, trees_dir=None, setup=None):
        """A repository at BASE/CASE/repo (or BASE/CASE/HOLDER/repo) with an
        origin at BASE/CASE/remote.git and count eligible worktrees at
        BASE/CASE/trees/NAME (or TREES_DIR/NAME) on branches NAME, in canonical
        order (raw path bytes); setup(tree), when given, runs in each before its
        commit (merged_worktree(setup=...)). Returns (root, trees)."""
        top = self.base / case
        root = self._init_repo((top / holder if holder else top) / "repo", "main")
        self.bare_remote(root, name=f"{case}/remote.git")
        place = top / "trees" if trees_dir is None else trees_dir
        trees = [self.merged_worktree(name, path=place / name, root=root, setup=setup) for name in NAMES[:count]]
        return root, trees

    def head(self, path, ref="HEAD"):
        return self.git(path, "rev-parse", ref).strip()

    def branches(self, root):
        """Every local branch with its object, as one text."""
        return self.git(root, "for-each-ref", "--format=%(refname) %(objectname)", "refs/heads")

    def snapshot(self, root, trees):
        """What a run that removes nothing leaves as it found it: the
        registry, every local branch with its object, and the files of each
        tree (its `.git` file aside)."""
        files = {}
        for tree in trees:
            tree = Path(tree)
            files[str(tree)] = sorted(str(path.relative_to(tree)) for path in tree.rglob("*")
                                      if path.name != ".git") if tree.exists() else None
        return self.git(root, "worktree", "list", "--porcelain"), self.branches(root), files

    def registered(self, root):
        """The registry's worktree paths, in its order."""
        return [line for line in self.git(root, "worktree", "list", "--porcelain").splitlines()
                if line.startswith("worktree ")]

    def counting(self, hooks=None, env=None):
        """The counting wrapper first on PATH, with hooks: (env, log)."""
        bin_dir, log = self.base / "counting-bin", self.base / "children.log"
        if bin_dir.exists():
            shutil.rmtree(bin_dir)
        clean_support.install_counting_git(bin_dir, log, hooks=hooks)
        clean_support.reset_child_log(log)
        return self.path_first(bin_dir, env), log

    def apply(self, root, at_question=None, env=None, log=None):
        """project.main(["clean", ROOT, "--all-safe", "--apply", "--json"]) in
        process: os.environ replaced by env (self.env by default), standard
        input a terminal, and ask_removal() patched to call at_question(), then
        answer `yes` (as T046 patches it). When log is given, it is emptied at
        the question, so that it holds only the children after confirmation.
        Returns the exit status, the one JSON document, standard error and the
        number of questions asked."""
        asked = []

        def ask(plan, run):
            asked.append(len(plan.selected))
            if log is not None:
                clean_support.reset_child_log(log)
            if at_question is not None:
                at_question()
            return "yes"

        out, err = io.StringIO(), io.StringIO()
        before = signal_state()
        with mock.patch.dict(os.environ, self.env if env is None else env, clear=True), \
                mock.patch.object(project.sys, "stdin", Terminal()), \
                mock.patch.object(project, "ask_removal", ask), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            status = project.main(["clean", str(root), "--all-safe", "--apply", "--json"])
        self.assertEqual(signal_state(), before, "main() left the signal handlers changed")
        try:
            document = json.loads(out.getvalue())
        except ValueError as exc:
            self.fail(f"standard output is not one JSON document: {exc}\n{out.getvalue()}\n{err.getvalue()}")
        return types.SimpleNamespace(status=status, document=document, stderr=err.getvalue(), asked=asked)

    def stages(self, result):
        """(path, stage, reason) of each target of the apply result record."""
        return [(target["path"], target["stage"], target["reason"]) for target in result.document["targets"]]

    def assert_stopped_at_first(self, result, trees, reason, exit_status=2):
        """The first target refused with reason, every later one
        `not-attempted` with `batch-stopped` and no reconciliation, and the
        exit status."""
        expected = [(str(trees[0]), "refused", reason)]
        expected += [(str(tree), "not-attempted", "batch-stopped") for tree in trees[1:]]
        self.assertEqual(self.stages(result), expected, result.stderr)
        for target in result.document["targets"][1:]:
            self.assertIsNone(target["reconciliation"])
            self.assertEqual(target["probes_performed"], 0)
        self.assertEqual((result.status, result.document["exit_code"]), (exit_status, exit_status))

    # T079: "Worktree changes while confirmation is pending", "New worktree
    # and pre-removal changes" and "Changed later target".

    def test_clean_worktree_changes_while_confirmation_is_pending(self):
        root, trees = self.batch("pending")
        before = self.snapshot(root, trees)

        def dirty():
            (trees[0] / "late-change").write_text("preserve")

        result = self.apply(root, dirty)
        self.assertEqual(result.asked, [2])
        self.assert_stopped_at_first(result, trees, "state-changed")
        self.assertTrue((trees[0] / "late-change").is_file(), "the worktree is preserved")
        registry, branches, files = self.snapshot(root, trees)
        self.assertEqual((registry, branches), before[:2], "nothing removed")
        self.assertEqual(files[str(trees[1])], before[2][str(trees[1])])

        # The same at a real question, at a pseudo-terminal: the change is
        # made while the question waits, then `yes` is typed.
        root, trees = self.batch("pending-pty")
        question = TEXT["question"].format(N=2)
        result = self.run_pty_steps(
            clean_support.cli_argv("clean", root, "--all-safe", "--apply"),
            [(question, lambda child: (trees[0] / "late-change").write_text("preserve")), ("", "yes")])
        self.assert_status(result, 2)
        lines = result.stdout.splitlines()
        self.assertIn(TEXT["progress_line_reason"].format(STAGE="refused", PATH=trees[0], REASON="state-changed"),
                      lines)
        self.assertIn(TEXT["progress_line_reason"].format(STAGE="not-attempted", PATH=trees[1],
                                                          REASON="batch-stopped"), lines)
        self.assertTrue(all(tree.is_dir() for tree in trees))
        self.assertTrue((trees[0] / "late-change").is_file())

    def test_clean_new_worktree_and_pre_removal_changes(self):
        # A linked worktree registered at the question is not selected: the
        # confirmed plan's two targets are removed, and nothing else.
        root, trees = self.batch("new")
        late = self.merged_worktree("000-late", path=self.base / "new" / "trees" / "000-late", root=root)
        self.git(root, "worktree", "remove", late)  # eligible again once re-added; sorts first
        result = self.apply(root, lambda: self.git(root, "worktree", "add", late, "000-late"))
        self.assertEqual(self.stages(result), [(str(tree), "removed", None) for tree in trees])
        self.assertEqual(result.status, 0, result.stderr)
        self.assertTrue(late.is_dir())
        self.assertIn(f"worktree {late}", self.git(root, "worktree", "list", "--porcelain"))

        # Each change below, made at the question on a fresh pair of targets,
        # is found before the first removal: the first target is refused with
        # the matching reason, the second is not attempted, nothing is
        # mutated, and the exit status is 2 (research.md R16, lead ruling
        # R-41). The merge-target SHA, the second target's branch tip,
        # upstream object and lock, and its filesystem identity and
        # registration (apply review F1; lead ruling R-101 (d)), are the
        # first target's preflight; the first target's ignored-file state and
        # classification are its own.
        def merge_target_moves(root, trees):
            self.git(root, "commit", "-q", "--allow-empty", "-m", "the merge target moves")

        def second_branch_moves(root, trees):
            self.commit(trees[1], "the second target's branch moves", allow_empty=True)

        def second_upstream_moves(root, trees):
            self.git(root, "update-ref", "refs/remotes/origin/002-q", self.head(root, "main"))

        def second_locked(root, trees):
            self.git(root, "worktree", "lock", trees[1])

        def second_directory_copied(root, trees):
            # Moved aside and copied back with its `.git` file: its
            # registration still holds both ways, and only its `dev` and `ino`
            # differ from the plan's.
            aside = trees[1].with_name(trees[1].name + ".aside")
            trees[1].rename(aside)
            shutil.copytree(aside, trees[1], symlinks=True)

        def second_dotgit_rewritten(root, trees):
            # Its `.git` file names the first target's admin directory, so its
            # two-way registration no longer holds.
            common = Path(self.git(root, "rev-parse", "--path-format=absolute", "--git-common-dir").strip())
            (trees[1] / ".git").write_text(f"gitdir: {common / 'worktrees' / '001-p'}\n")

        def first_ignored_file(root, trees):
            exclude = Path(self.git(root, "rev-parse", "--path-format=absolute", "--git-common-dir").strip())
            (exclude / "info").mkdir(exist_ok=True)
            with open(exclude / "info" / "exclude", "a") as stream:
                stream.write("*.log\n")
            (trees[0] / "build.log").write_text("ignored")

        def first_classification(root, trees):
            (trees[0] / "work-001-p").write_text("edited")  # a tracked edit: class `dirty`

        cases = [
            ("merge-target-sha", merge_target_moves, "state-changed", False),
            ("second-branch-tip", second_branch_moves, "branch-changed", True),
            ("second-upstream-object", second_upstream_moves, "state-changed", True),
            ("second-lock", second_locked, "state-changed", True),
            ("second-directory-copied", second_directory_copied, "identity-changed", True),
            ("second-dotgit-rewritten", second_dotgit_rewritten, "identity-changed", True),
            ("first-ignored-file", first_ignored_file, "state-changed", False),
            ("first-classification", first_classification, "state-changed", False),
        ]
        for case, change, reason, on_second in cases:
            with self.subTest(case):
                root, trees = self.batch(case)
                result = self.apply(root, lambda: change(root, trees))
                self.assert_stopped_at_first(result, trees, reason)
                self.assertTrue(all(tree.is_dir() for tree in trees), "nothing removed")
                registry = self.git(root, "worktree", "list", "--porcelain")
                self.assertTrue(all(f"worktree {tree}" in registry for tree in trees))
                if on_second:
                    # Found by the first target's preflight, so the first is
                    # the refused one, though nothing about it changed.
                    first = result.document["targets"][0]
                    self.assertTrue(first["reconciliation"]["registry_entry_present"])
                    self.assertIsNone(first["exit_status"])

    def test_clean_changed_later_target(self):
        root, trees = self.batch("later", count=3)
        planned = {name: self.head(root, f"refs/heads/{name}") for name in NAMES[:3]}
        # The post-remove hook of target 1 makes target 2 dirty, after target 1
        # passed its revalidation and Git removed it.
        env, log = self.counting({"post": when_target(trees[0], f": > {shlex.quote(str(trees[1] / 'late'))}")})
        result = self.apply(root, env=env)
        self.assertEqual(self.stages(result), [(str(trees[0]), "removed", None),
                                               (str(trees[1]), "refused", "state-changed"),
                                               (str(trees[2]), "not-attempted", "batch-stopped")])
        self.assertEqual(result.status, 2, result.stderr)
        first, second, third = result.document["targets"]
        self.assertEqual(first["reconciliation"], record(False, False, True, planned["001-p"]))
        self.assertEqual(second["reconciliation"], record(True, True, True, planned["002-q"]))
        self.assertIsNone(third["reconciliation"])
        self.assertEqual(sum(map(is_removal, clean_support.child_log(log))), 1)
        self.assertFalse(trees[0].exists())
        self.assertTrue(trees[1].is_dir() and (trees[1] / "late").is_file() and trees[2].is_dir())
        # Every branch is retained at its planned head, and the result says so.
        self.assertEqual({name: self.head(root, f"refs/heads/{name}") for name in planned}, planned)
        lines = result.stderr.splitlines()
        self.assertIn(TEXT["stop_block"].format(PATH=trees[1], REASON="state-changed", K=1, N=3,
                                                NOT_ATTEMPTED=trees[2], ROOT=root), lines)
        self.assertIn(TEXT["branches_kept_line"].format(BRANCHES="001-p, 002-q, 003-r"), lines)

    # T080: "Target directory replaced", "Admin registration changed" and
    # "Parent directory swapped".

    def assert_identity_changed_and_nothing_removed(self, result, trees, log):
        """The first target refused with identity-changed, the later ones not
        attempted, exit 2, and no removal child spawned."""
        self.assert_stopped_at_first(result, trees, "identity-changed")
        self.assertEqual([record for record in clean_support.child_log(log) if is_removal(record)], [])

    def test_clean_target_directory_replaced(self):
        # At the question the first target P is moved aside and, in turn, a
        # new directory, a symbolic link to the moved original, or a copy of
        # it (lane 3's E3, lead ruling R-76) is put at P. The copy carries
        # P's `.git` file, so its registration still holds both ways; only
        # P's recorded `dev` and `ino` tell it apart.
        def new_directory(tree):
            tree.rename(tree.with_name(tree.name + ".aside"))
            tree.mkdir()

        def symlink(tree):
            aside = tree.with_name(tree.name + ".aside")
            tree.rename(aside)
            tree.symlink_to(aside, target_is_directory=True)

        def copy(tree):
            aside = tree.with_name(tree.name + ".aside")
            tree.rename(aside)
            shutil.copytree(aside, tree, symlinks=True)

        for case, change in (("new-directory", new_directory), ("symlink", symlink), ("copy", copy)):
            with self.subTest(case):
                root, trees = self.batch(case)
                env, log = self.counting()
                result = self.apply(root, lambda: change(trees[0]), env=env, log=log)
                self.assert_identity_changed_and_nothing_removed(result, trees, log)
                aside = trees[0].with_name(trees[0].name + ".aside")
                self.assertTrue((aside / "work-001-p").is_file(), "the moved original is untouched")
                self.assertTrue(os.path.lexists(trees[0]), "what was put at P is untouched")
                self.assertTrue(trees[1].is_dir())
                if case == "copy":
                    self.assertTrue((trees[0] / "work-001-p").is_file(), "the copy is not removed")

    def test_clean_admin_registration_changed(self):
        # The first target's `.git` file rewritten to name the second target's
        # admin directory; then, in a second run, its admin `gitdir` file
        # changed to name another existing directory, whose `.git` names
        # nothing back. Each refuses with identity-changed after confirmation,
        # and a fresh plan reports the row as registration-mismatch with
        # classification inspection-error, and is incomplete.
        def admin_dir(root, name):
            common = Path(self.git(root, "rev-parse", "--path-format=absolute", "--git-common-dir").strip())
            return common / "worktrees" / name

        def rewrite_dotgit(root, trees):
            (trees[0] / ".git").write_text(f"gitdir: {admin_dir(root, '002-q')}\n")
            return trees[0]

        def rewrite_admin_gitdir(root, trees):
            elsewhere = trees[0].with_name("elsewhere")
            elsewhere.mkdir()
            (admin_dir(root, "001-p") / "gitdir").write_text(f"{elsewhere / '.git'}\n")
            return elsewhere

        for case, change in (("dotgit", rewrite_dotgit), ("admin-gitdir", rewrite_admin_gitdir)):
            with self.subTest(case):
                root, trees = self.batch(case)
                env, log = self.counting()
                changed = []
                result = self.apply(root, lambda: changed.append(change(root, trees)), env=env, log=log)
                self.assert_identity_changed_and_nothing_removed(result, trees, log)
                self.assertTrue(all((tree / f"work-{tree.name}").is_file() for tree in trees))
                fresh = self.run_json("clean", root, "--all-safe", "--json")
                self.assert_status(fresh, 1)
                document = fresh.document
                self.assertEqual(document["completeness"], "incomplete")
                row = next(row for row in document["worktrees"] if row["path"] == str(changed[0]))
                self.assertEqual(row["classification"], "inspection-error")
                self.assertIn({"path": str(changed[0]), "path_valid_utf8": True, "branch": "001-p",
                               "classification": "inspection-error", "reason": "registration-mismatch"},
                              document["excluded"])

    def test_clean_parent_directory_swapped(self):
        # The directory holding both targets is replaced at the question by a
        # symbolic link to a copy of it: each target's realpath now names the
        # copy, whose `dev` and `ino` differ from the plan's.
        holder = self.base / "swapped" / "holder"
        root, trees = self.batch("swapped", trees_dir=holder)
        env, log = self.counting()

        def swap():
            copy = holder.with_name("holder.copy")
            shutil.copytree(holder, copy, symlinks=True)
            holder.rename(holder.with_name("holder.orig"))
            holder.symlink_to(copy, target_is_directory=True)

        result = self.apply(root, swap, env=env, log=log)
        self.assertNotEqual(os.path.realpath(trees[0]), str(trees[0]))
        self.assert_identity_changed_and_nothing_removed(result, trees, log)
        for name in ("holder.orig", "holder.copy"):
            for tree in trees:
                self.assertTrue((holder.with_name(name) / tree.name / f"work-{tree.name}").is_file(), (name, tree))

    # T081: "State changes before revalidation", "Branch advances before
    # removal" and "Deleted upstream reappears before revalidation".

    def manifest(self, root, tracking_branch=None, text=None):
        """Write root's project.yaml: a project manifest, with tracking_branch
        when given, or text as it is."""
        if text is None:
            text = "kind: project-manifest\n"
            if tracking_branch is not None:
                text += f"tracking_branch: {tracking_branch}\n"
        (Path(root) / "project.yaml").write_text(text)

    def test_clean_state_changes_before_revalidation(self):
        def common_dir(root):
            return Path(self.git(root, "rev-parse", "--path-format=absolute", "--git-common-dir").strip())

        def ignored_file(root, trees):
            (common_dir(root) / "info").mkdir(exist_ok=True)
            with open(common_dir(root) / "info" / "exclude", "a") as stream:
                stream.write("*.log\n")
            (trees[0] / "build.log").write_text("ignored")

        def merge_target_commit(root, trees):
            self.git(root, "commit", "-q", "--allow-empty", "-m", "the merge target gains a commit")

        def through_manifest(root):
            # The plan resolves the merge target from the manifest; `release`
            # is another existing branch.
            self.git(root, "branch", "release")
            self.manifest(root, "main")

        def through_origin_head(root):
            # No manifest: the plan resolves the merge target through
            # origin/HEAD, which names main; `release` exists locally and at
            # origin, and the narrowed ref listing names neither.
            self.git(root, "branch", "release")
            self.git(root, "push", "-q", "origin", "main", "release")
            self.git(root, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")

        cases = [
            ("ignored-file", None, ignored_file, "main"),
            ("merge-target-commit", None, merge_target_commit, "main"),
            ("manifest-edited", through_manifest, lambda root, trees: self.manifest(root, "release"), "manifest"),
            ("manifest-unparseable", through_manifest,
             lambda root, trees: self.manifest(root, text="kind: project-manifest\ntracking_branch: [main\n"),
             "manifest"),
            # A manifest that can no longer be read differs even where the plan
            # read no candidate from it, no manifest or one without the key,
            # which as_candidate() reads as none, as it reads the unreadable
            # value (lane 3's W41, its unmutated manifest arm).
            ("manifest-unparseable-where-the-plan-read-none", None,
             lambda root, trees: self.manifest(root, text="kind: project-manifest\ntracking_branch: [main\n"),
             "main"),
            ("manifest-unparseable-where-the-plan-read-no-key", lambda root: self.manifest(root),
             lambda root, trees: self.manifest(root, text="kind: project-manifest\ntracking_branch: [main\n"),
             "main"),
            # Lead ruling R-77: the manifest's tracking_branch is compared as
            # written, so a spelling that resolves the same still differs.
            ("manifest-spelled-with-its-remote", through_manifest,
             lambda root, trees: self.manifest(root, "origin/main"), "manifest"),
            ("origin-head-plan-gains-manifest", through_origin_head,
             lambda root, trees: self.manifest(root, "release"), "origin-head"),
            ("origin-head-repointed", through_origin_head,
             lambda root, trees: self.git(root, "symbolic-ref", "refs/remotes/origin/HEAD",
                                          "refs/remotes/origin/release"), "origin-head"),
        ]
        for case, setup, change, source in cases:
            with self.subTest(case):
                root, trees = self.batch(case)
                if setup is not None:
                    setup(root)
                preview = self.run_json("clean", root, "--all-safe", "--json").document
                self.assertEqual((preview["merge_target"]["name"], preview["merge_target"]["source"]),
                                 ("main", source))
                self.assertEqual(len(preview["selected"]), 2)
                before = self.registered(root)
                result = self.apply(root, lambda: change(root, trees))
                self.assert_stopped_at_first(result, trees, "state-changed")
                self.assertEqual(self.registered(root), before, "nothing removed")
                self.assertTrue(all(tree.is_dir() for tree in trees))

    def test_clean_state_changes_before_revalidation_a_tracking_branch_that_is_not_a_string(self):
        # Lead ruling R-101 (d), apply review F2: YAML's `.nan` loads as a float
        # that never equals itself, and planning reads a value that is not a
        # string as no candidate (resolve_merge_target()), so the merge target
        # is main. Revalidation compares the manifest's value the same way:
        # left as it was, it is no difference, and both targets are removed.
        # An edit to or from a string still differs, as written (R-77).
        cases = [
            ("nan-left-unchanged", ".nan", None, "main", None),
            ("nan-edited-to-a-string", ".nan", "release", "main", "state-changed"),
            ("a-string-edited-to-nan", "main", ".nan", "manifest", "state-changed"),
        ]
        for case, planned, edited, source, reason in cases:
            with self.subTest(case):
                root, trees = self.batch(case)
                self.git(root, "branch", "release")
                self.manifest(root, planned)
                preview = self.run_json("clean", root, "--all-safe", "--json").document
                self.assertEqual((preview["merge_target"]["name"], preview["merge_target"]["source"]),
                                 ("main", source))
                self.assertEqual(len(preview["selected"]), 2)
                before = self.registered(root)
                result = self.apply(root, None if edited is None else lambda: self.manifest(root, edited))
                if reason is None:
                    self.assertEqual(self.stages(result), [(str(tree), "removed", None) for tree in trees],
                                     result.stderr)
                    self.assertEqual((result.status, result.document["exit_code"]), (0, 0))
                    self.assertFalse(any(tree.exists() for tree in trees))
                else:
                    self.assert_stopped_at_first(result, trees, reason)
                    self.assertEqual(self.registered(root), before, "nothing removed")
                    self.assertTrue(all(tree.is_dir() for tree in trees))

    def test_clean_branch_advances_before_removal(self):
        root, trees = self.batch("advances")
        planned = self.head(trees[0])
        moved = []
        result = self.apply(root, lambda: moved.append(self.commit(trees[0], "advance", allow_empty=True)))
        self.assert_stopped_at_first(result, trees, "branch-changed")
        self.assertNotEqual(moved[0], planned)
        first = result.document["targets"][0]
        self.assertEqual(first["planned_sha"], planned)
        # Plan review M13: the registry entry from the registry listing, the
        # branch and its new SHA from the ref listing, the path from an lstat.
        self.assertEqual(first["reconciliation"], record(True, True, True, moved[0]))
        self.assertIs(first["reconciliation"]["reconciled"], True)
        self.assertEqual(self.head(root, "refs/heads/001-p"), moved[0], "the branch is kept at the new commit")
        self.assertTrue(all(tree.is_dir() for tree in trees))
        self.assertIn(TEXT["stop_block"].format(PATH=trees[0], REASON="branch-changed", K=0, N=2,
                                                NOT_ATTEMPTED=trees[1], ROOT=root), result.stderr.splitlines())

    def test_clean_deleted_upstream_reappears_before_revalidation(self):
        def deleted_upstreams(case):
            # P and Q, each on a branch whose upstream's remote-tracking ref is
            # deleted locally (the remote keeps the branch): `upstream` is
            # recorded with `upstream_oid`, `ahead` and `behind` null.
            root, trees = self.batch(case)
            for name in NAMES[:2]:
                self.git(root, "update-ref", "-d", f"refs/remotes/origin/{name}")
            preview = self.run_json("clean", root, "--all-safe", "--json").document
            self.assertEqual([(entry["upstream"], entry["upstream_oid"], entry["ahead"], entry["behind"],
                               entry["remote_present"]) for entry in preview["selected"]],
                             [(f"origin/{name}", None, None, None, False) for name in NAMES[:2]])
            return root, trees

        def fetch(name):
            return ("fetch", "-q", "origin", f"refs/heads/{name}:refs/remotes/origin/{name}")

        # P's upstream recreated at the question: P differs from its plan.
        root, trees = deleted_upstreams("p-reappears")
        before = self.snapshot(root, trees)
        result = self.apply(root, lambda: self.git(root, *fetch("001-p")))
        self.assert_stopped_at_first(result, trees, "state-changed")
        self.assertEqual(self.snapshot(root, trees)[0], before[0], "nothing removed")

        # Q's recreated after P's removal child exits 0 and before its rescan:
        # P, null in the plan and null again, is removed; Q is refused.
        root, trees = deleted_upstreams("q-reappears")
        env, log = self.counting({"post": when_target(trees[0], sh_git("-C", root, *fetch("002-q")))})
        result = self.apply(root, env=env)
        self.assertEqual(self.stages(result), [(str(trees[0]), "removed", None),
                                               (str(trees[1]), "refused", "state-changed")])
        self.assertEqual((result.status, result.document["exit_code"]), (2, 2))
        self.assertFalse(trees[0].exists())
        self.assertTrue(trees[1].is_dir())
        self.assertEqual(sum(map(is_removal, clean_support.child_log(log))), 1)

    # T082: "Untracked file under status.showUntrackedFiles=no", "Git's own
    # check runs on the pinned configuration" and "Ignored file in the
    # residual window". They pin T056 and T057: a change after the last
    # revalidation is Git's own check's, or the residual window's.

    def assert_git_refused_first(self, result, trees, late):
        """Git refused the first target's removal with 128: `failed`,
        `git-refused`, its reconciliation showing the entry and the path
        present, the late file kept, later targets not attempted, exit 128."""
        self.assertEqual(self.stages(result), [(str(trees[0]), "failed", "git-refused")]
                         + [(str(tree), "not-attempted", "batch-stopped") for tree in trees[1:]])
        first = result.document["targets"][0]
        self.assertEqual(first["exit_status"], 128)
        self.assertEqual((first["reconciliation"]["registry_entry_present"], first["reconciliation"]["path_present"]),
                         (True, True))
        self.assertIs(first["reconciliation"]["reconciled"], True)
        self.assertTrue(late.is_file(), "the file survives")
        self.assertEqual((result.status, result.document["exit_code"]), (128, 128))

    def test_clean_untracked_file_under_status_showuntrackedfiles_no(self):
        config = self.base / "global-gitconfig"
        config.write_text("[status]\n\tshowUntrackedFiles = no\n")
        self.env["GIT_CONFIG_GLOBAL"] = str(config)
        root, trees = self.batch("untracked-no")
        late = trees[0] / "untracked-late"
        env, log = self.counting({"pre": when_target(trees[0], f": > {shlex.quote(str(late))}")})
        result = self.apply(root, env=env)
        self.assert_git_refused_first(result, trees, late)
        removal = [record for record in clean_support.child_log(log) if is_removal(record)]
        self.assertEqual(len(removal), 1)
        self.assertEqual(strip_pins(removal[0].argv)[0][:2], ["-c", "status.showUntrackedFiles=normal"])

    def test_clean_git_s_own_check_runs_on_the_pinned_configuration(self):
        root, trees = self.batch("pinned")
        self.git(root, "config", "core.untrackedCache", "true")
        self.git(root, "config", "core.checkStat", "minimal")
        self.git(trees[0], "status")  # an index-writing status: the untracked cache is filled
        late = trees[0] / "created-late"
        env, log = self.counting({"pre": when_target(trees[0], f": > {shlex.quote(str(late))}")})
        result = self.apply(root, env=env)
        self.assert_git_refused_first(result, trees, late)
        [removal] = [record for record in clean_support.child_log(log) if is_removal(record)]
        self.assertEqual(strip_pins(removal.argv)[0][:12], ["-c", "status.showUntrackedFiles=normal",
                                                             "-c", "core.untrackedCache=false",
                                                             "-c", "core.fsmonitor=false",
                                                             "-c", "core.trustctime=true", "-c", "core.checkStat=default",
                                                             "-c", "core.ignoreCase=false"])

    def test_clean_ignored_file_in_the_residual_window(self):
        root, trees = self.batch("residual")
        common = Path(self.git(root, "rev-parse", "--path-format=absolute", "--git-common-dir").strip())
        (common / "info").mkdir(exist_ok=True)
        (common / "info" / "exclude").write_text("*.log\n")
        late = trees[0] / "late.log"
        env, log = self.counting({"pre": when_target(trees[0], f": > {shlex.quote(str(late))}")})
        result = self.apply(root, env=env)
        self.assertEqual(self.stages(result), [(str(tree), "removed", None) for tree in trees])
        self.assertEqual((result.status, result.document["exit_code"]), (0, 0))
        self.assertFalse(late.exists(), "the ignored file went with the worktree")
        self.assertFalse(trees[0].exists())
        # The confirmation (the printed plan) and the result each carry the
        # residual-window line, once.
        lines = result.stderr.splitlines()
        self.assertEqual(lines.count(TEXT["residual_window_line"]), 2)
        self.assertLess(lines.index(TEXT["residual_window_line"]),
                        lines.index(TEXT["progress_line"].format(STAGE="removed", PATH=trees[0])))
        self.assertEqual(lines[-1], TEXT["residual_window_line"])

    # T083: "Branch advances after removal", "Repository replaced mid-batch",
    # and the after-confirmation clauses of "Hidden local state" and
    # "Submodules" (spec.md, US4 scenario 2).

    def test_clean_branch_advances_after_removal(self):
        # The post-remove hook advances the first target's branch to a new
        # commit, after Git removed the worktree and before the rescan.
        root, trees = self.batch("advanced-after")
        planned = self.head(root, "refs/heads/001-p")
        tree_object = self.head(root, "001-p^{tree}")
        moved = self.git(root, "commit-tree", tree_object, "-p", planned, "-m", "after removal").strip()
        env, log = self.counting({"post": when_target(trees[0], sh_git("-C", root, "update-ref",
                                                                        "refs/heads/001-p", moved))})
        result = self.apply(root, env=env)
        self.assertEqual(self.stages(result), [(str(trees[0]), "removed", "branch-advanced-after-removal"),
                                               (str(trees[1]), "not-attempted", "batch-stopped")])
        first = result.document["targets"][0]
        self.assertEqual(first["reconciliation"], record(False, False, True, moved))
        self.assertNotEqual(first["reconciliation"]["branch_sha"], first["planned_sha"])
        self.assertEqual((result.status, result.document["exit_code"]), (2, 2))
        self.assertEqual(self.head(root, "refs/heads/001-p"), moved)
        self.git(root, "merge-base", "--is-ancestor", planned, moved)  # no commit lost
        self.assertTrue(trees[1].is_dir())
        self.assertEqual(sum(map(is_removal, clean_support.child_log(log))), 1)
        self.assertIn(TEXT["stop_block"].format(PATH=trees[0], REASON="branch-advanced-after-removal", K=1, N=2,
                                                NOT_ATTEMPTED=trees[1], ROOT=root), result.stderr.splitlines())

        # The hook deletes the branch instead.
        root, trees = self.batch("missing-after")
        env, log = self.counting({"post": when_target(trees[0], sh_git("-C", root, "update-ref", "-d",
                                                                        "refs/heads/001-p"))})
        result = self.apply(root, env=env)
        self.assertEqual(self.stages(result), [(str(trees[0]), "removed", "branch-missing-after-removal"),
                                               (str(trees[1]), "not-attempted", "batch-stopped")])
        self.assertEqual(result.document["targets"][0]["reconciliation"], record(False, False, False, None))
        self.assertEqual((result.status, result.document["exit_code"]), (2, 2))

    def test_clean_repository_replaced_mid_batch(self):
        # Three targets outside the directory that holds the root. After the
        # first target's removal child exits 0 and before its rescan, the
        # post-remove hook renames the root and moves another clone into its
        # path; in a second run it replaces the root's parent by a symbolic
        # link to a copy. The rescan's identity probe finds another repository.
        def replace_by_clone(case, root):
            other = self.base / case / "other-clone"
            self.git(self.base, "clone", "-q", root, other)
            return (f"mv {shlex.quote(str(root))} {shlex.quote(str(root) + '.renamed')}"
                    f" && mv {shlex.quote(str(other))} {shlex.quote(str(root))}")

        def replace_parent(case, root):
            holder = shlex.quote(str(root.parent))
            return (f"cp -a {holder} {holder}.copy && mv {holder} {holder}.orig"
                    f" && ln -s {holder}.copy {holder}")

        for case, replacement in (("clone", replace_by_clone), ("parent", replace_parent)):
            with self.subTest(case):
                root, trees = self.batch(case, count=3, holder="holder")
                command = replacement(case, root)
                env, log = self.counting({"post": when_target(trees[0], command)})
                result = self.apply(root, env=env)
                self.assertEqual(self.stages(result), [(str(trees[0]), "unknown", "unconfirmed-removal"),
                                                       (str(trees[1]), "not-attempted", "batch-stopped"),
                                                       (str(trees[2]), "not-attempted", "batch-stopped")])
                first = result.document["targets"][0]
                self.assertEqual(first["reconciliation"], dict.fromkeys(RECONCILIATION_KEYS[:-1]) | {"reconciled": False})
                self.assertEqual(first["exit_status"], 0)
                self.assertEqual((result.status, result.document["exit_code"]), (1, 1))
                self.assertEqual(result.document["completeness"], "incomplete")
                self.assertEqual(sum(map(is_removal, clean_support.child_log(log))), 1)
                self.assertTrue(trees[1].is_dir() and trees[2].is_dir())

        # The same replacement at the question: the first target is refused
        # with identity-changed, and nothing is removed.
        root, trees = self.batch("clone-at-question", count=3, holder="holder")
        command = replace_by_clone("clone-at-question", root)
        env, log = self.counting()
        result = self.apply(root, lambda: self.assertEqual(os.system(command), 0), env=env, log=log)
        self.assert_identity_changed_and_nothing_removed(result, trees, log)
        self.assertTrue(all((tree / f"work-{tree.name}").is_file() for tree in trees))

    def test_clean_hidden_local_state_after_confirmation(self):
        # Lane 3's E3 (lead ruling R-76): an edit hidden by assume-unchanged,
        # set at the question, and in a second run by skip-worktree. Git's own
        # check would not see either; the hidden-state probe does.
        for case, flag in (("assume-unchanged", "--assume-unchanged"), ("skip-worktree", "--skip-worktree")):
            with self.subTest(case):
                root, trees = self.batch(case)
                edited = trees[0] / "work-001-p"

                def hide():
                    edited.write_text("an edit hidden from status\n")
                    self.git(trees[0], "update-index", flag, "work-001-p")

                result = self.apply(root, hide)
                self.assert_stopped_at_first(result, trees, "hidden-local-state")
                self.assertEqual(edited.read_text(), "an edit hidden from status\n", "the edit survives")
                self.assertTrue(trees[1].is_dir())

    def test_clean_submodules_after_confirmation(self):
        # A `modules` directory created in the first target's admin directory at
        # the question.
        root, trees = self.batch("modules")
        common = Path(self.git(root, "rev-parse", "--path-format=absolute", "--git-common-dir").strip())
        env, log = self.counting()
        result = self.apply(root, lambda: (common / "worktrees" / "001-p" / "modules").mkdir(), env=env, log=log)
        self.assert_stopped_at_first(result, trees, "contains-submodule")
        self.assertEqual([record for record in clean_support.child_log(log) if is_removal(record)], [])
        self.assertTrue(all(tree.is_dir() for tree in trees))

    def test_clean_a_nested_repository_made_after_the_plan(self):
        # Brett Heap's Q2 (2) (lead R-380), R-397: #19's "A nested repository made after the plan", through --apply.
        def tracked(tree):
            (tree / "tools").mkdir(exist_ok=True)
            (tree / "tools" / "run.sh").write_text("tracked\n")

        root, trees = self.batch("nested", setup=tracked)
        nested = trees[0] / "tools"
        env, log = self.counting()
        result = self.apply(root, lambda: self.git(nested, "init", "-q"), env=env, log=log)
        self.assert_stopped_at_first(result, trees, "contains-submodule")
        self.assertEqual([record for record in clean_support.child_log(log) if is_removal(record)], [])
        self.assertTrue((nested / ".git").is_dir(), "the nested repository is kept")
        self.assertTrue((nested / "run.sh").is_file())
        self.assertTrue(all(tree.is_dir() for tree in trees))

    # LQ-14 and LQ-13 at revalidation (design D21 and D22; lead rulings R-124,
    # R-127 and R-146): "An operation started after the plan", "A check that
    # fails at revalidation", and the reads that fail or are cut there.

    def admin(self, tree):
        """The administrative directory of the linked worktree at tree."""
        return Path(self.git(tree, "rev-parse", "--path-format=absolute", "--git-dir").rstrip("\n"))

    def assert_nothing_removed(self, root, trees, before, log):
        self.assertEqual([record for record in clean_support.child_log(log) if is_removal(record)], [])
        self.assertEqual(self.snapshot(root, trees)[:2], before[:2], "nothing removed")
        self.assertTrue(all(tree.is_dir() for tree in trees))

    def test_clean_an_operation_started_after_the_plan(self):
        root, trees = self.batch("bisect")
        before = self.snapshot(root, trees)
        env, log = self.counting()
        result = self.apply(root, lambda: self.git(trees[0], "bisect", "start", "--no-checkout"), env=env, log=log)
        self.assert_stopped_at_first(result, trees, "operation-in-progress")
        self.assert_nothing_removed(root, trees, before, log)
        self.assertTrue((self.admin(trees[0]) / "BISECT_LOG").is_file(), "the bisect is kept")

    @clean_support.not_root
    def test_clean_a_check_that_fails_at_revalidation(self):
        with self.subTest("the admin directory can no longer be listed"):
            root, trees = self.batch("unlisted")
            admin = self.admin(trees[0])
            self.addCleanup(admin.chmod, 0o700)
            before = self.snapshot(root, trees)
            env, log = self.counting()
            result = self.apply(root, lambda: admin.chmod(0o300), env=env, log=log)
            self.assert_stopped_at_first(result, trees, "state-changed")
            admin.chmod(0o700)
            self.assert_nothing_removed(root, trees, before, log)
        with self.subTest("P's .git file loses its read permission (R-208)"):
            root, trees = self.batch("unreadable-dotgit")
            dotgit = trees[0] / ".git"
            self.addCleanup(dotgit.chmod, 0o644)
            before = self.snapshot(root, trees)
            env, log = self.counting()
            result = self.apply(root, lambda: dotgit.chmod(0o000), env=env, log=log)
            self.assert_stopped_at_first(result, trees, "state-changed")
            dotgit.chmod(0o644)
            self.assert_nothing_removed(root, trees, before, log)
        with self.subTest("P's .git file is gone: an absent path decides identity-changed"):
            root, trees = self.batch("missing-dotgit")
            dotgit = trees[0] / ".git"
            saved = dotgit.read_bytes()
            self.addCleanup(lambda: dotgit.exists() or dotgit.write_bytes(saved))
            before = self.snapshot(root, trees)
            env, log = self.counting()
            result = self.apply(root, dotgit.unlink, env=env, log=log)
            self.assert_stopped_at_first(result, trees, "identity-changed")
            dotgit.write_bytes(saved)
            self.assert_nothing_removed(root, trees, before, log)
        with self.subTest("a logs/HEAD line names an object the repository does not hold"):
            root, trees = self.batch("bad-object")
            head = self.head(trees[0])
            absent = "1" * len(head)
            self.assertEqual(self.git(root, "cat-file", "--batch-check", input=absent + "\n").split(),
                             [absent, "missing"])
            entry = f"{head} {absent} {clean_support.REFLOG_IDENT} 0 +0000\tplanted\n"
            before = self.snapshot(root, trees)
            env, log = self.counting()

            def plant():
                with (self.admin(trees[0]) / "logs" / "HEAD").open("a") as stream:
                    stream.write(entry)

            result = self.apply(root, plant, env=env, log=log)
            self.assert_stopped_at_first(result, trees, "state-changed")
            self.assert_nothing_removed(root, trees, before, log)
            reachability = [record for record in clean_support.child_log(log)
                            if subcommand(record)[:3] == ["rev-list", "--max-count=1", "--glob=refs/worktree"]]
            self.assertEqual([directory(record) for record in reachability], [str(trees[0])])
            self.assertIn(absent, subcommand(reachability[0]))

    def test_clean_a_worktree_only_commit_made_after_the_plan(self):
        for case in ("head-reflog", "refs-worktree"):
            with self.subTest(case):
                root, trees = self.batch(case)
                branch = self.git(trees[0], "branch", "--show-current").strip()

                def commit_only_there(tree=trees[0], branch=branch, case=case):
                    if case == "head-reflog":
                        self.git(tree, "checkout", "-q", "--detach")
                        (tree / "late-work").write_text("made after the plan\n")
                        self.commit(tree, "late work")
                        self.git(tree, "checkout", "-q", branch)
                    else:
                        held = self.git(tree, "commit-tree", "HEAD^{tree}", "-p", "HEAD", "-m", "late").strip()
                        self.git(tree, "update-ref", "refs/worktree/keep", held)

                before = self.snapshot(root, trees)
                env, log = self.counting()
                result = self.apply(root, commit_only_there, env=env, log=log)
                self.assert_stopped_at_first(result, trees, "worktree-only-commits")
                self.assert_nothing_removed(root, trees, before, log)
                self.assertEqual(self.git(trees[0], "branch", "--show-current").strip(), branch)

    def test_clean_a_work_tree_probe_that_decides_nothing_at_revalidation(self):
        # The lead's R-171 (#19 at 4485678, "Cleanup revalidates destructive
        # actions" and D7): where the plan read extensions.worktreeConfig as
        # true, only a decided different effective work tree is
        # identity-changed (lane E's test of a work tree redirected after the
        # plan pins it). In process, after the question, P's work-tree probe
        # made to exit 128, to time out, to print nothing, to print only a
        # line feed, and to print P's own path with no line feed after it,
        # each state-changed; and cut by the work deadline, which is no
        # difference (P not-attempted with deadline-exceeded, exit 1). Its
        # output, less the one line feed Git ends it with, is one path, which
        # may hold line feeds (lead ruling R-287; lane 3's W70 M-2), so two
        # lines are one other path, a decided different work tree:
        # identity-changed. A line feed alone names no path, so it decides
        # nothing, like empty output (lead ruling R-291; lane 3's W90 L-1).
        probe = ["rev-parse", "--path-format=absolute", "--show-toplevel"]
        lf = chr(0x0A).encode("ascii")
        cases = (("exits 128", dict(name="failed", status=128), ("refused", "state-changed"), 2),
                 ("times out", dict(name="timeout"), ("refused", "state-changed"), 2),
                 ("prints nothing", dict(name="complete", status=0, result=lambda target: b""),
                  ("refused", "state-changed"), 2),
                 ("prints only a line feed", dict(name="complete", status=0, result=lambda target: lf),
                  ("refused", "state-changed"), 2),
                 ("prints P's path with no line feed", dict(name="complete", status=0, result=lambda target: target),
                  ("refused", "state-changed"), 2),
                 ("prints two lines, one other path",
                  dict(name="complete", status=0, result=lambda target: b"/a" + lf + b"/b" + lf),
                  ("refused", "identity-changed"), 2),
                 ("is cut by the deadline", dict(name="deadline"), ("not-attempted", "deadline-exceeded"), 1))
        for number, (label, fields, expected, status) in enumerate(cases):
            with self.subTest(f"the work-tree probe {label}"):
                root, trees = self.batch(f"work-tree-{number}")
                if callable(fields.get("result")):  # the output, from P's own path
                    fields = {**fields, "result": fields["result"](bytes(trees[0]))}
                self.git(root, "config", "extensions.worktreeConfig", "true")
                before = self.snapshot(root, trees)
                asked, calls, real_run_bounded = [], [], project.run_bounded

                def run_bounded(spec, parser, run, fields=fields, asked=asked, calls=calls, target=bytes(trees[0])):
                    kind, args, cwd = spec
                    if asked and args[2:] == probe and args[1] == target:
                        calls.append(args[1])
                        return project.DriverOutcome(project.git_argv(kind, args), **fields)
                    return real_run_bounded(spec, parser, run)

                env, log = self.counting()
                with mock.patch.object(project, "run_bounded", run_bounded):
                    result = self.apply(root, lambda: asked.append(True), env=env, log=log)
                self.assertEqual(len(calls), 1, "one work-tree probe at P's revalidation")
                self.assertEqual(self.stages(result)[0], (str(trees[0]), *expected), result.stderr)
                self.assertEqual([stage for _, stage, _ in self.stages(result)[1:]], ["not-attempted"])
                self.assertEqual((result.status, result.document["exit_code"]), (status, status))
                self.assert_nothing_removed(root, trees, before, log)

    def test_clean_a_redirected_work_tree_beside_a_later_check_s_difference(self):
        # The lead's R-198: the review-safety delta orders the target's
        # identity, its `modules` check and its operation-in-progress listing,
        # by filesystem reads, before its effective-work-tree probe, stopping at
        # the first difference. A work tree redirected after the plan (lane E's
        # decoy in P's config.worktree) beside a `modules` entry made at the
        # same time is contains-submodule, and beside a marker
        # operation-in-progress, and no work-tree probe runs at P's
        # revalidation. The redirection alone stays identity-changed (lane E's
        # test of a work tree redirected after the plan).
        probe = ["rev-parse", "--path-format=absolute", "--show-toplevel"]
        for case, entry, reason in (("modules", "modules", "contains-submodule"),
                                    ("marker", "MERGE_HEAD", "operation-in-progress")):
            with self.subTest(case):
                root, trees = self.batch("redirected-" + case)
                self.git(root, "config", "extensions.worktreeConfig", "true")
                decoy = self.base / ("decoy-" + case)
                decoy.mkdir()
                for name in self.git(trees[0], "ls-files", "-z").split("\0"):
                    if name:
                        shutil.copy2(trees[0] / name, decoy / name)
                admin = self.admin(trees[0])

                def redirect_and_mark(admin=admin, decoy=decoy, entry=entry):
                    self.git(trees[0], "config", "--file", admin / "config.worktree", "core.worktree", decoy)
                    if entry == "modules":
                        (admin / entry).mkdir()
                    else:
                        (admin / entry).write_text(self.head(root) + "\n")

                before = self.snapshot(root, trees)
                env, log = self.counting()
                result = self.apply(root, redirect_and_mark, env=env, log=log)
                self.assertEqual(self.git(trees[0], *probe).strip(), str(decoy), "P's work tree is redirected")
                self.assert_stopped_at_first(result, trees, reason)
                records = clean_support.child_log(log)
                self.assertEqual([record for record in records if subcommand(record) == probe], [],
                                 "the work-tree probe's child is skipped")
                self.assertEqual(result.document["targets"][0]["probes_performed"], 3,
                                 "the identity probe, the registry listing and the ref listing only")
                self.assert_nothing_removed(root, trees, before, log)

    # The lead's R-208 (#19 at 9267303, "Cleanup revalidates destructive
    # actions"): every filesystem call of the revalidation that fails, or runs
    # past its own budget while the deadline is not the limit, is
    # state-changed, whatever its step; ENOENT and ENOTDIR are no failure, and
    # decide that the path is absent, which keeps the step's reason.

    def refused_by_a_read(self, case, place, fn, answer, expected, extra=None):
        """--all-safe --apply over two selected targets P and Q, in process,
        the first filesystem call fn(place(root, trees), ...) after the
        question answered by answer (an exception it raises, or a
        DriverOutcome); the first target's stage and reason are expected, Q
        not-attempted, nothing removed. extra(root) adds rows first."""
        root, trees = self.batch(case)
        if extra is not None:
            extra(root)
        path = place(root, trees)
        before = self.snapshot(root, trees)
        asked, calls, real_fs_call = [], [], project.fs_call

        def fs_call(call, *args, **options):
            if asked and not calls and call is fn and args[:1] == (path,):
                calls.append(path)
                if isinstance(answer, BaseException):
                    raise answer
                return answer
            return real_fs_call(call, *args, **options)

        env, log = self.counting()
        with mock.patch.object(project, "fs_call", fs_call):
            result = self.apply(root, lambda: asked.append(True), env=env, log=log)
        self.assertEqual(calls, [path], "the read was reached at P's revalidation")
        self.assertEqual(self.stages(result)[0], (str(trees[0]), *expected), result.stderr)
        self.assertEqual([stage for _, stage, _ in self.stages(result)[1:]], ["not-attempted"])
        self.assertEqual(result.status, 2)
        self.assert_nothing_removed(root, trees, before, log)

    def denied(self, path):
        return PermissionError(errno.EACCES, os.strerror(errno.EACCES), os.fsdecode(path))

    def timed_out(self):
        return project.DriverOutcome(None, "timeout", detail="no answer within 5 s")

    def missing(self, path):
        return FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), os.fsdecode(path))

    def test_clean_identity_reads_that_fail_at_revalidation(self):
        # Step 1: the lstat of the common directory, after the identity probe.
        def common(root, trees):
            return os.fsencode(os.path.realpath(root / ".git"))

        for label, answer, expected in (
                ("EACCES", self.denied(b"x"), ("refused", "state-changed")),
                ("a timeout", self.timed_out(), ("refused", "state-changed")),
                ("ENOENT, an absent path", self.missing(b"x"), ("refused", "identity-changed"))):
            with self.subTest(label):
                self.refused_by_a_read("identity-" + label.split()[0].strip(","), common, os.lstat, answer,
                                       expected)

    def test_clean_a_target_lstat_that_fails_at_revalidation(self):
        # Step 5: the lstat of the target's path.
        def target(root, trees):
            return bytes(trees[0])

        for label, answer, expected in (
                ("EACCES", self.denied(b"x"), ("refused", "state-changed")),
                ("a timeout", self.timed_out(), ("refused", "state-changed")),
                ("ENOENT, an absent path", self.missing(b"x"), ("refused", "identity-changed"))):
            with self.subTest(label):
                self.refused_by_a_read("lstat-" + label.split()[0].strip(","), target, os.lstat, answer, expected)

    def test_clean_a_twin_read_that_fails_at_revalidation(self):
        # Step 5's twin check reads every registry entry: an unselected dirty
        # row whose lstat fails there.
        def add_dirty(root):
            tree = self.merged_worktree("009-z", path=root.parent / "trees" / "009-z", root=root)
            (tree / "uncommitted").write_text("keep")

        def dirty(root, trees):
            return bytes(root.parent / "trees" / "009-z")

        for label, answer in (("EACCES", self.denied(b"x")), ("a timeout", self.timed_out())):
            with self.subTest(label):
                self.refused_by_a_read("twin-" + label.split()[0], dirty, os.lstat, answer,
                                       ("refused", "state-changed"), extra=add_dirty)

    def test_clean_a_modules_check_that_fails_at_revalidation(self):
        # Step 5's modules check: the lstat of `<admin>/modules`.
        def modules(root, trees):
            return os.fsencode(self.admin(trees[0]) / "modules")

        for label, answer in (("EACCES", self.denied(b"x")), ("a timeout", self.timed_out())):
            with self.subTest(label):
                self.refused_by_a_read("modules-" + label.split()[0], modules, os.lstat, answer,
                                       ("refused", "state-changed"))

    def test_clean_an_admin_directory_gone_at_its_listing(self):
        # Step 5's listing (D22) finding no admin directory decides that the
        # target's registration is gone: identity-changed, not a failed read.
        def admin(root, trees):
            return os.fsencode(self.admin(trees[0]))

        self.refused_by_a_read("listing-gone", admin, os.listdir, self.missing(b"x"), ("refused", "identity-changed"))

    def test_clean_a_dot_git_file_gone_between_its_lstat_and_its_read(self):
        # Step 5's registration reads (verify_registration()): _gitfile()
        # decides ENOENT and ENOTDIR at its lstat of P's `.git`, but not at its
        # read of that file, made once the lstat found a regular file. A `.git`
        # removed between the two, or P replaced by a file, raises them there,
        # and revalidation_difference() decides them as absence (project:5763):
        # identity-changed, as an absent `.git` is (the lead's R-208). The race
        # is made in process: that read raises the error. Lane 3's W41 L-4 took
        # the clause for dead; this pins it.
        def dotgit(root, trees):
            return os.path.join(bytes(trees[0]), b".git")

        not_a_directory = NotADirectoryError(errno.ENOTDIR, os.strerror(errno.ENOTDIR), "x")
        for label, answer in (("ENOENT", self.missing(b"x")), ("ENOTDIR", not_a_directory)):
            with self.subTest(label):
                self.refused_by_a_read("dotgit-read-" + label, dotgit, project._read_head, answer,
                                       ("refused", "identity-changed"))

    # The lead's R-195 (#19 at 4485678, "Cleanup revalidates destructive
    # actions"): every Git child of the revalidation that fails, or runs past
    # its own budget while the deadline is not the limit, is state-changed,
    # whatever its step; a child gives its step's own reason only for a value
    # it decided.

    def assert_child_that_decides_nothing(self, case, words, in_target):
        """P's first revalidation child whose words after `-C DIR` (DIR the
        command directory, or P where in_target) begin with words made, after
        the question, to exit 128 and to time out: each refuses P with
        state-changed, Q is not-attempted, exit 2, nothing removed."""
        for label, fields in (("exits 128", dict(name="failed", status=128)), ("times out", dict(name="timeout"))):
            with self.subTest(f"{case} {label}"):
                root, trees = self.batch(f"{case}-{fields['name']}")
                directory_bytes = bytes(trees[0]) if in_target else os.fsencode(root)
                before = self.snapshot(root, trees)
                asked, calls, real_run_bounded = [], [], project.run_bounded

                def run_bounded(spec, parser, run, fields=fields, asked=asked, calls=calls, at=directory_bytes):
                    kind, args, cwd = spec
                    if asked and not calls and args[2:2 + len(words)] == words and os.fsencode(args[1]) == at:
                        calls.append(args)
                        return project.DriverOutcome(project.git_argv(kind, args), **fields)
                    return real_run_bounded(spec, parser, run)

                env, log = self.counting()
                with mock.patch.object(project, "run_bounded", run_bounded):
                    result = self.apply(root, lambda: asked.append(True), env=env, log=log)
                self.assertEqual(len(calls), 1, "the child was reached at P's revalidation")
                self.assert_stopped_at_first(result, trees, "state-changed")
                self.assert_nothing_removed(root, trees, before, log)

    def test_clean_an_identity_probe_that_decides_nothing_at_revalidation(self):
        # Step 1: identity-changed only for a decided different identity
        # ("Repository replaced mid-batch" pins it).
        self.assert_child_that_decides_nothing(
            "identity", ["rev-parse", "--path-format=absolute", *project.IDENTITY_OPTIONS], in_target=False)

    def test_clean_a_registry_listing_that_decides_nothing_at_revalidation(self):
        # Step 3: identity-changed only for a missing or doubled entry.
        self.assert_child_that_decides_nothing("registry", ["worktree", "list", "--porcelain", "-z"], in_target=False)

    def test_clean_a_ref_listing_that_decides_nothing_at_revalidation(self):
        # Step 4, the narrowed ref listing (lane 3's W41 M-2): branch-changed
        # only for a decided different branch or head ("Branch advances before
        # removal" pins it), state-changed for a decided different upstream or
        # merge target, and state-changed for a listing that decided nothing.
        self.assert_child_that_decides_nothing("refs", ["for-each-ref"], in_target=False)

    def test_clean_a_hidden_state_probe_that_decides_nothing_at_revalidation(self):
        # Step 7: hidden-local-state only for a decided flagged entry ("Hidden
        # local state", its after-confirmation clause, pins it).
        self.assert_child_that_decides_nothing("hidden", list(project.HIDDEN_STATE_PROBE), in_target=True)

    def test_clean_worktree_only_commits_check_cut_at_revalidation(self):
        # In process, after the question: the read of P's logs/HEAD made to
        # time out, and the reachability child made to exit 128 and to time
        # out, each a value that cannot be re-read (state-changed); the child
        # cut by the work deadline, which is no difference (P not-attempted
        # with deadline-exceeded, exit 1).
        cases = (("a read that times out", "read", dict(name="timeout"), ("refused", "state-changed"), 2),
                 ("a child that exits 128", "child", dict(name="failed", status=128), ("refused", "state-changed"), 2),
                 ("a child that times out", "child", dict(name="timeout"), ("refused", "state-changed"), 2),
                 ("a child cut by the deadline", "child", dict(name="deadline"),
                  ("not-attempted", "deadline-exceeded"), 1))
        for label, where, fields, expected, status in cases:
            with self.subTest(label):
                root, trees = self.batch("cut-" + label.split()[1] + "-" + fields["name"])
                log_path = os.fsencode(self.admin(trees[0]) / "logs" / "HEAD")
                before = self.snapshot(root, trees)
                asked, calls = [], []
                real_fs_call, real_run_bounded = project.fs_call, project.run_bounded

                def fs_call(fn, *args, where=where, fields=fields, asked=asked, calls=calls, **options):
                    if where == "read" and asked and fn is project._read_head and args[:1] == (log_path,):
                        calls.append(args[0])
                        return project.DriverOutcome(None, fields["name"], detail="cut here")
                    return real_fs_call(fn, *args, **options)

                def run_bounded(spec, parser, run, where=where, fields=fields, asked=asked, calls=calls):
                    kind, args, cwd = spec
                    if (where == "child" and asked and args[2:5] == ["rev-list", "--max-count=1", "--glob=refs/worktree"]
                            and args[1] == bytes(trees[0])):
                        calls.append(args[1])
                        return project.DriverOutcome(project.git_argv(kind, args), **fields)
                    return real_run_bounded(spec, parser, run)

                env, log = self.counting()
                with mock.patch.object(project, "fs_call", fs_call), \
                        mock.patch.object(project, "run_bounded", run_bounded):
                    result = self.apply(root, lambda: asked.append(True), env=env, log=log)
                self.assertEqual(len(calls), 1, "one read or child at P's revalidation")
                self.assertEqual(self.stages(result)[0], (str(trees[0]), *expected), result.stderr)
                self.assertEqual([stage for _, stage, _ in self.stages(result)[1:]], ["not-attempted"])
                self.assertEqual((result.status, result.document["exit_code"]), (status, status))
                self.assert_nothing_removed(root, trees, before, log)

    def test_clean_operation_in_progress_listing_cut_at_revalidation(self):
        # In process: the listing of P's admin directory, after the question,
        # made to time out at its budget, which is a value that cannot be
        # re-read (state-changed), and to be cut by the work deadline, which
        # is no difference (P not-attempted with deadline-exceeded, exit 1).
        for label, name, expected, status in (
                ("a timeout", "timeout", ("refused", "state-changed"), 2),
                ("the work deadline", "deadline", ("not-attempted", "deadline-exceeded"), 1)):
            with self.subTest(label):
                root, trees = self.batch("listing-" + name)
                admin = os.fsencode(self.admin(trees[0]))
                before = self.snapshot(root, trees)
                asked, calls, real_fs_call = [], [], project.fs_call

                def fs_call(fn, *args, name=name, asked=asked, calls=calls, **options):
                    if asked and fn is os.listdir and args == (admin,):
                        calls.append(args[0])
                        return project.DriverOutcome(None, name, detail="cut here")
                    return real_fs_call(fn, *args, **options)

                env, log = self.counting()
                with mock.patch.object(project, "fs_call", fs_call):
                    result = self.apply(root, lambda: asked.append(True), env=env, log=log)
                self.assertEqual(calls, [admin], "one listing at P's revalidation")
                self.assertEqual(self.stages(result)[0], (str(trees[0]), *expected), result.stderr)
                self.assertEqual([stage for _, stage, _ in self.stages(result)[1:]], ["not-attempted"])
                self.assertEqual((result.status, result.document["exit_code"]), (status, status))
                self.assert_nothing_removed(root, trees, before, log)

    # T099 (lead ruling R-80, P-2; #19 at 9267303, "Cleanup revalidates
    # destructive actions"): a revalidation read that the work deadline cuts is
    # no difference, whatever its step; P and every later target are
    # not-attempted, P with deadline-exceeded, and the exit status is 1. Lane
    # 3's W41 M-1: one test per read whose deadline arm no test reached, each
    # cutting that read of P's revalidation as the listing's test above cuts
    # the listing.

    def assert_cut_at_the_work_deadline(self, case, fs=None, child=None, spend=False, extra=None, fails=False):
        """--all-safe --apply over two selected targets P and Q, in process: the
        first read after the question that fs or child picks is cut at the work
        deadline, a DriverOutcome `deadline` returned in its place. fs(root,
        trees) gives a test of a filesystem call, given its function and
        arguments; child(root, trees) a test of a Git child, given its words
        after `git` (`-C DIR` first). With spend, the work deadline is also
        made to pass at the cut (Invocation.work_end), as a real cut leaves it,
        for a step that reads work_spent() and not the read's code. With fails,
        the picked read is not cut but fails with a non-cut error (a Git child
        exits 128; a filesystem call gives `probe-failed`), so that only
        work_spent() makes it a deadline-exceeded and not a state-changed.
        extra(root) adds rows first. P is not-attempted with deadline-exceeded,
        Q not-attempted, exit 1, and nothing is removed."""
        root, trees = self.batch(case)
        if extra is not None:
            extra(root)
        picks_fs = fs(root, trees) if fs is not None else None
        picks_child = child(root, trees) if child is not None else None
        before = self.snapshot(root, trees)
        asked, calls = [], []
        real_fs_call, real_run_bounded = project.fs_call, project.run_bounded

        def cut(run, read):
            calls.append(read)
            if spend:
                run.work_end = run.now()

        def outcome(argv):
            if fails:
                return project.DriverOutcome(argv, "failed", status=128, stderr=b"fatal: cut here", stderr_bytes=15)
            return project.DriverOutcome(argv, "deadline", detail="cut here")

        def fs_call(fn, *args, **options):
            if asked and not calls and picks_fs is not None and picks_fs(fn, args):
                cut(project.current_invocation(), args[:1])
                return outcome(None)
            return real_fs_call(fn, *args, **options)

        def run_bounded(spec, parser, run):
            kind, args, cwd = spec
            if asked and not calls and picks_child is not None and picks_child(args):
                cut(run, args)
                return outcome(project.git_argv(kind, args))
            return real_run_bounded(spec, parser, run)

        env, log = self.counting()
        with mock.patch.object(project, "fs_call", fs_call), mock.patch.object(project, "run_bounded", run_bounded):
            result = self.apply(root, lambda: asked.append(True), env=env, log=log)
        self.assertEqual(len(calls), 1, "the read was reached at P's revalidation")
        self.assertEqual(self.stages(result)[0], (str(trees[0]), "not-attempted", "deadline-exceeded"), result.stderr)
        self.assertEqual([stage for _, stage, _ in self.stages(result)[1:]], ["not-attempted"])
        self.assertEqual((result.status, result.document["exit_code"]), (1, 1))
        self.assert_nothing_removed(root, trees, before, log)

    def at_root(self, words):
        """A child test: words after `-C ROOT`, the command directory."""
        return lambda root, trees: lambda args: os.fsencode(args[1]) == os.fsencode(root) and args[2:] == words

    def lstat_of(self, place):
        """A filesystem-call test: the lstat of place(root, trees)."""
        def picks(root, trees):
            path = place(root, trees)
            return lambda fn, args: fn is os.lstat and args[:1] == (path,)
        return picks

    def test_clean_an_identity_probe_cut_at_revalidation(self):
        # Step 1, the identity probe (project:5677-5678).
        self.assert_cut_at_the_work_deadline(
            "identity-cut", child=self.at_root(["rev-parse", "--path-format=absolute", *project.IDENTITY_OPTIONS]))

    def test_clean_an_identity_probe_that_fails_with_no_work_time_left_at_revalidation(self):
        # Step 1's first disjunct (project:5721, work_spent(run) or
        # any(map(read_cut, read_errors))): the identity probe fails with
        # `probe-failed`, which read_cut() does not read as a cut, as the work
        # deadline passes (the lead's R-195, R-208; lane 3's W41 LOW-3). Only
        # work_spent() then makes it deadline-exceeded; without it the same
        # failed probe is state-changed (the next arm) and P is refused.
        self.assert_cut_at_the_work_deadline(
            "identity-fails-spent",
            child=self.at_root(["rev-parse", "--path-format=absolute", *project.IDENTITY_OPTIONS]),
            spend=True, fails=True)

    def test_clean_a_manifest_re_read_cut_at_revalidation(self):
        # Step 2, the manifest's re-read (project:5687-5688), one bounded call
        # whose cut reread_manifest() keeps no code for: the step reads that no
        # work time is left (work_spent()), so the cut spends it, as a real
        # cut does.
        def manifest(root, trees):
            return lambda fn, args: (getattr(fn, "__qualname__", "") == "declared_tracking_branch.<locals>.examine"
                                     and os.path.basename(args[0]) == "project.yaml")

        self.assert_cut_at_the_work_deadline("manifest-cut", fs=manifest, spend=True)

    def test_clean_a_registry_listing_cut_at_revalidation(self):
        # Step 3, the registry listing (project:5700-5701).
        self.assert_cut_at_the_work_deadline(
            "registry-cut", child=self.at_root(["worktree", "list", "--porcelain", "-z"]))

    def test_clean_a_ref_listing_cut_at_revalidation(self):
        # Step 4, the narrowed ref listing (project:5723-5724).
        def refs(root, trees):
            return lambda args: os.fsencode(args[1]) == os.fsencode(root) and args[2:3] == ["for-each-ref"]

        self.assert_cut_at_the_work_deadline("refs-cut", child=refs)

    def test_clean_a_target_lstat_cut_at_revalidation(self):
        # Step 5, the lstat of the target's path (project:5750-5751).
        self.assert_cut_at_the_work_deadline("lstat-cut", fs=self.lstat_of(lambda root, trees: bytes(trees[0])))

    def test_clean_a_registration_read_cut_at_revalidation(self):
        # Step 5, the first registration read (verify_registration(),
        # project:5759-5760): _gitfile()'s lstat of P's `.git`.
        self.assert_cut_at_the_work_deadline(
            "registration-cut", fs=self.lstat_of(lambda root, trees: os.path.join(bytes(trees[0]), b".git")))

    def test_clean_a_twin_read_cut_at_revalidation(self):
        # Step 5's twin check (registry_twin(), project:5566-5567): the lstat of
        # an unselected dirty row, which only that check reads.
        def add_dirty(root):
            tree = self.merged_worktree("009-z", path=root.parent / "trees" / "009-z", root=root)
            (tree / "uncommitted").write_text("keep")

        self.assert_cut_at_the_work_deadline(
            "twin-cut", fs=self.lstat_of(lambda root, trees: bytes(root.parent / "trees" / "009-z")), extra=add_dirty)

    def test_clean_a_modules_check_cut_at_revalidation(self):
        # Step 5's modules check (project:5775-5776): the lstat of
        # `<admin>/modules`.
        self.assert_cut_at_the_work_deadline(
            "modules-cut", fs=self.lstat_of(lambda root, trees: os.fsencode(self.admin(trees[0]) / "modules")))

    def test_clean_a_status_probe_cut_at_revalidation(self):
        # Step 6, the status probe in the target (project:5809-5810).
        def status(root, trees):
            return lambda args: os.fsencode(args[1]) == bytes(trees[0]) and args[2:] == list(project.STATUS_PROBE)

        self.assert_cut_at_the_work_deadline("status-cut", child=status)

    # D7's bound, by the counting wrapper (lead rulings R-68 (d) and R-73 (f)).

    def test_clean_revalidation_spawns_at_most_six_children(self):
        # Five rows: the main worktree, three selected targets, and a merged
        # worktree made dirty, which is not selected. The log is emptied at the
        # question, so it holds exactly the children after confirmation.
        root, trees = self.batch("bound", count=3)
        dirty = self.merged_worktree("004-s", path=self.base / "bound" / "trees" / "004-s", root=root)
        (dirty / "uncommitted").write_text("keep")
        env, log = self.counting()
        result = self.apply(root, env=env, log=log)
        self.assertEqual(self.stages(result), [(str(tree), "removed", None) for tree in trees])
        self.assertEqual(result.status, 0, result.stderr)
        records = clean_support.child_log(log)
        at = [index for index, child in enumerate(records) if is_removal(child)]
        self.assertEqual(len(at), 3)
        segments = [records[:at[0]], records[at[0] + 1:at[1]], records[at[1] + 1:at[2]], records[at[2] + 1:]]
        words = [[subcommand(child)[0] for child in segment] for segment in segments]
        # The first revalidation: the identity probe, the registry listing, one
        # narrowed ref listing, the status probe, the hidden-state probe and
        # the reachability probe of worktree-only-commits (D21, LQ-13).
        self.assertEqual(words[0], ["rev-parse", "worktree", "for-each-ref", "status", "ls-files", "rev-list"])
        narrowed = subcommand(segments[0][2])
        self.assertEqual(narrowed[2:], ["refs/heads/main", "refs/heads/master", "refs/remotes/origin/HEAD",
                                        "refs/heads/001-p", "refs/remotes/origin/001-p",
                                        "refs/heads/002-q", "refs/remotes/origin/002-q",
                                        "refs/heads/003-r", "refs/remotes/origin/003-r"])
        # T085: after a plain `removed`, the rescan's three repository children
        # are the next target's steps 1 to 4, so each later target spawns only
        # its status, hidden-state and reachability probes, and counts six; the
        # rescan after the last target is the final rescan, three.
        rescan = ["rev-parse", "worktree", "for-each-ref"]
        self.assertEqual(words[1], rescan + ["status", "ls-files", "rev-list"])
        self.assertEqual(words[2], rescan + ["status", "ls-files", "rev-list"])
        self.assertEqual(words[3], rescan, "the final rescan spawns three")
        self.assertEqual([target["probes_performed"] for target in result.document["targets"]], [6, 6, 6])
        self.assertEqual(len([child for child in records if not is_removal(child)]), 6 * 3 + 3)
        # No merged-set listing, and no status probe of a row not selected; each
        # status, ls-files and rev-list child names its own target, every other
        # child the command directory.
        after = [child for child in records if not is_removal(child)]
        self.assertFalse(any(any(word.startswith("--merged") for word in subcommand(child)) for child in after))
        targets_of = {str(tree) for tree in trees}
        for child in after:
            with self.subTest(argv=child.argv):
                if subcommand(child)[0] in ("status", "ls-files", "rev-list"):
                    self.assertIn(directory(child), targets_of)
                else:
                    self.assertEqual(directory(child), str(root))
        for child in records:
            if is_removal(child):
                self.assertEqual(directory(child), str(root))
        # The record counts every child once: probes the planning's and these.
        probes, operations = result.document["probes"], result.document["operations"]
        planning = probes["estimated"] - 6 * 3 - 3
        self.assertEqual(probes["performed"], planning + len(after))
        self.assertEqual(probes["performed"], probes["estimated"], "performed no longer exceeds estimated")
        self.assertEqual(operations, {"estimated": 3, "performed": 3})

    # T085: the rescan and the stage (lead rulings R-76 (a) and R-78 (e);
    # lane 3's H-1 and E1).

    def after_remove_git(self, bin_dir, words=(), text=":", post=None):
        """bin_dir/git: the real git, except that `worktree remove` runs post,
        sh text, after the real removal when given, and that once a removal
        has run every later child whose argument vector holds one of words (a
        word or words, matched with spaces around them) runs text, sh text,
        instead. Returns the environment with it first on PATH."""
        marker = Path(bin_dir) / "removed.marker"
        test = " || ".join(f'case " $* " in *" {word} "*) true;; *) false;; esac' for word in words) or "false"
        script = (f"#!/bin/sh\nreal={shlex.quote(REAL_GIT)}\nmarker={shlex.quote(str(marker))}\n"
                  'case " $* " in *" worktree remove "*)\n'
                  f'  "$real" "$@"; status=$?; {post or ":"}; : > "$marker"; exit $status;;\nesac\n'
                  f'if [ -e "$marker" ] && {{ {test}; }}; then\n{text}\nfi\nexec "$real" "$@"\n')
        Path(bin_dir).mkdir(parents=True, exist_ok=True)
        path = Path(bin_dir) / "git"
        path.write_text(script)
        path.chmod(0o755)
        return self.path_first(bin_dir)

    def test_clean_decide_stage_removed_needs_reconciled(self):
        # FR-034, pcl:891-895: `removed` needs the entry and the path gone AND
        # the record reconciled; BA:723-730: exit 0 with that evidence but a
        # branch not read back is `unknown` with `reconciliation-incomplete`.
        outcome = project.DriverOutcome
        exited, ceiling = outcome(["git"], "complete", status=0), outcome(["git"], "timeout", status=-9)
        target = {"planned_sha": "a" * 40}

        def unfinished(*values):
            return project.UnfinishedRescan(record(*values))

        gone_unread = record(False, False, None, None)
        self.assertIs(gone_unread["reconciled"], False)
        cases = [
            (exited, gone_unread, ("unknown", "reconciliation-incomplete", [])),
            (ceiling, gone_unread, ("unknown", "removal-ceiling", [])),
            # Lead ruling R-78 (e), second amendment: a rescan read that failed or
            # was cut marks the record (UnfinishedRescan), and a marked record
            # is reconciliation-incomplete: a failed registry listing, lstat or
            # ref listing, or an identity that could not be read.
            (exited, unfinished(None, False, True, "a" * 40), ("unknown", "reconciliation-incomplete", [])),
            (exited, unfinished(False, None, True, "a" * 40), ("unknown", "reconciliation-incomplete", [])),
            (exited, unfinished(True, True, None, None), ("unknown", "reconciliation-incomplete", [])),
            (exited, unfinished(None, None, None, None), ("unknown", "reconciliation-incomplete", [])),
            (ceiling, unfinished(None, None, None, None), ("unknown", "removal-ceiling", [])),
            # Unmarked: the reads gave values showing the removal not done, or
            # the identity found lost or another one (every field null).
            (exited, record(None, None, None, None), ("unknown", "unconfirmed-removal", [])),
            (exited, record(True, True, True, "a" * 40), ("unknown", "unconfirmed-removal", [])),
            # A repository replaced or lost at the ceiling (LOW, pinned as built).
            (ceiling, record(None, None, None, None), ("unknown", "removal-ceiling", [])),
            # The branch race after removal (T085; rs:210-214).
            (exited, record(False, False, True, "a" * 40), ("removed", None, [])),
            (exited, record(False, False, True, "b" * 40), ("removed", "branch-advanced-after-removal", [])),
            (exited, record(False, False, False, None), ("removed", "branch-missing-after-removal", [])),
            (ceiling, record(False, False, True, "b" * 40), ("removed", "removal-ceiling", [])),
        ]
        for given, reconciliation, expected in cases:
            with self.subTest(outcome=given.name, reconciliation=reconciliation,
                              marked=isinstance(reconciliation, project.UnfinishedRescan)):
                decided = project.decide_stage(target, given, reconciliation)
                self.assertEqual(decided, expected)
                self.assertIn(decided[1], project.STAGE_REASONS[decided[0]])
        # The mark is the record's class alone: it compares and is written as
        # the plain record, so it never reaches a document.
        marked = unfinished(None, None, None, None)
        self.assertEqual(marked, record(None, None, None, None))
        self.assertEqual(json.dumps(marked, indent=2), json.dumps(record(None, None, None, None), indent=2))
        documents = [project.target_document(dict(
            path=b"/w/a", branch="a", planned_sha="a" * 40, stage="unknown", reason="reconciliation-incomplete",
            notes=[], command=["git"], exit_status=0, probes_performed=5, reconciliation=value))
            for value in (marked, record(None, None, None, None))]
        self.assertEqual(*(json.dumps(document, indent=2) for document in documents))
        self.assertIs(type(documents[0]["reconciliation"]), dict)

    def test_clean_a_failed_rescan_ref_listing_is_not_removed(self):
        # Lane 3's E1 (lead ruling R-76 (a)): every for-each-ref fails once the
        # removal has run, so the rescan cannot read the branch back.
        root, (tree,) = self.batch("ref-listing", count=1)
        planned = self.head(tree)
        env = self.after_remove_git(self.base / "refs-fail-bin", ["for-each-ref"],
                                    'echo "fatal: fake for-each-ref failure" >&2; exit 1')
        result = self.run_json("clean", root, "--all-safe", "--apply", "--yes", "--json", env=env)
        self.assert_status(result, 1)
        [target] = result.document["targets"]
        self.assertEqual((target["stage"], target["reason"], target["exit_status"]),
                         ("unknown", "reconciliation-incomplete", 0))
        self.assertEqual(target["reconciliation"], record(False, False, None, None))
        self.assertIs(target["reconciliation"]["reconciled"], False)
        self.assertEqual((result.document["exit_code"], result.document["completeness"]), (1, "incomplete"))
        self.assertFalse(tree.exists())
        self.assertEqual(self.head(root, "refs/heads/001-p"), planned, "the branch is kept")

    def test_clean_rescan_marks_every_failed_read(self):
        # Lead ruling R-78 (e), second amendment. The root moved away after the
        # removal: the identity is found lost, the reads that ran gave values,
        # and the target is unconfirmed-removal.
        root, (tree,) = self.batch("lost", count=1)
        env, log = self.counting({"post": when_target(tree, f"mv {shlex.quote(str(root))} "
                                                          f"{shlex.quote(str(root) + '.away')}")})
        result = self.apply(root, env=env)
        [target] = result.document["targets"]
        self.assertEqual((target["stage"], target["reason"]), ("unknown", "unconfirmed-removal"))
        self.assertEqual(target["reconciliation"], record(None, None, None, None))
        self.assertEqual((result.status, result.document["exit_code"]), (1, 1))

        # Each rescan read failing alone after the removal child exits 0, then
        # the registry listing, the ref listing and the lstat together after an
        # established identity: the target is reconciliation-incomplete, exit 1.
        # A Git child is killed by SIGKILL (`kill -9 $$` in a fake git); the
        # lstat fails with EACCES once the directory holding the target is made
        # unsearchable.
        kill = "kill -9 $$"
        cases = [
            ("identity probe", ["rev-parse"], False, lambda sha: (None, None, None, None)),
            ("registry listing", ["worktree list"], False, lambda sha: (None, False, True, sha)),
            ("ref listing", ["for-each-ref"], False, lambda sha: (False, False, None, None)),
            ("lstat", [], True, lambda sha: (False, None, True, sha)),
            ("all but the identity", ["worktree list", "for-each-ref"], True, lambda sha: (None, None, None, None)),
        ]
        for case, words, unsearchable, values in cases:
            with self.subTest(case):
                if unsearchable and hasattr(os, "geteuid") and os.geteuid() == 0:
                    self.skipTest("permission fixtures do not bind the superuser (effective uid 0)")
                root, (tree,) = self.batch(case.replace(" ", "-"), count=1)
                planned = self.head(tree)
                holder = tree.parent
                post = f"chmod 000 {shlex.quote(str(holder))}" if unsearchable else None
                if unsearchable:
                    self.addCleanup(os.chmod, holder, 0o755)
                env = self.after_remove_git(self.base / f"{case.replace(' ', '-')}-bin", words, kill, post)
                result = self.apply(root, env=env)
                if unsearchable:
                    os.chmod(holder, 0o755)
                [target] = result.document["targets"]
                self.assertEqual((target["stage"], target["reason"], target["exit_status"]),
                                 ("unknown", "reconciliation-incomplete", 0))
                self.assertEqual(target["reconciliation"], record(*values(planned)))
                self.assertIs(target["reconciliation"]["reconciled"], False)
                self.assertEqual((result.status, result.document["exit_code"]), (1, 1))
                self.assertFalse(tree.exists())
                self.assertEqual(self.head(root, "refs/heads/001-p"), planned)

    # Lead ruling R-93 (e), LOW-1: during the apply phase the first signal
    # stops scheduling, "so that no further probe or removal starts" (the
    # project-clean delta, pcl:931-933), a revalidation's own children
    # included.

    def run_signalled(self, argv, env, ready, signum):
        """Run argv, project through the launcher, in a session of its own with
        both streams on pipes; poll ready() until it holds, then send signum to
        project alone (rule 7) and wait for it to exit. Returns the
        CompletedProcess, its streams as text and its one JSON document as
        `document`. Each stream holds far less than a pipe's buffer, so both
        are read once project has exited."""
        child = subprocess.Popen(argv, cwd=self.base, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, start_new_session=True)
        deadline = time.monotonic() + clean_support.TIMEOUT
        problem = None
        try:
            while problem is None and not ready():
                if child.poll() is not None:
                    problem = f"project exited before {signal.Signals(signum).name} was sent"
                elif time.monotonic() > deadline:
                    problem = f"the step sending {signal.Signals(signum).name} was not ready in {clean_support.TIMEOUT} s"
                else:
                    time.sleep(0.01)
            if problem is None:
                os.kill(child.pid, signum)
                try:
                    child.wait(max(0.1, deadline - time.monotonic()))
                except subprocess.TimeoutExpired:
                    problem = f"project did not exit within {clean_support.TIMEOUT} s"
        finally:
            if child.poll() is None:
                with contextlib.suppress(OSError):
                    os.killpg(child.pid, signal.SIGKILL)
            out, err = child.communicate()
        result = subprocess.CompletedProcess(argv, child.returncode, out.decode("utf-8", "surrogateescape"),
                                             err.decode("utf-8", "surrogateescape"))
        if problem:
            self.fail(f"{problem}\n{clean_support.transcript(result)}")
        result.document = self.load_json(result)
        return result

    def test_clean_a_signal_during_a_removal_sigint_during_a_revalidation(self):
        # Lane 3's sig-reval-INT. Two targets, through the launcher with the
        # real table (probe budget 5 s, work deadline 50 s), so that only the
        # signal acts. The status-slow-again-in fake, behind the counting
        # wrapper, sleeps 2 s before the first target's second status probe:
        # planning's runs as it is, the revalidation's is slowed. Once the
        # wrapper has recorded that probe, SIGINT goes to project alone. The
        # probe runs to its end, since phase `apply` stops no child, and the
        # revalidation then reads the slot before its next child: no Git child
        # starts after the signal, neither the hidden-state probe nor a
        # removal. The first target ends as the seam before the spawn ended it
        # before this fix, `not-attempted` with `interrupted`, and so does the
        # second; nothing is removed, and the exit status is 130.
        root, trees = self.batch("signal-revalidation")
        before = self.snapshot(root, trees)
        fake = clean_support.install_fake_git(self.base / "slow-status-bin", "status-slow-again-in", path=trees[0],
                                              seconds=2)
        bin_dir, log = self.base / "signal-counting-bin", self.base / "signal-children.log"
        clean_support.install_counting_git(bin_dir, log, real=fake)
        clean_support.reset_child_log(log)
        at_signal = []

        def slowed():
            records = clean_support.child_log(log)
            if [directory(child) for child in records if subcommand(child)[:1] == ["status"]].count(
                    str(trees[0])) < 2:
                return False
            at_signal[:] = records
            return True

        argv = clean_support.launched_argv(clean_support.timing_table(), "clean", root, "--all-safe", "--apply",
                                           "--yes", "--json")
        result = self.run_signalled(argv, self.path_first(bin_dir), slowed, signal.SIGINT)
        self.assert_status(result, 130)
        # The log at the end is the log as it stood when SIGINT was sent, the
        # slowed status probe its last child: no child started after the
        # signal.
        records = clean_support.child_log(log)
        self.assertEqual((subcommand(at_signal[-1])[:1], directory(at_signal[-1])), (["status"], str(trees[0])))
        self.assertEqual([subcommand(child) for child in records[len(at_signal):]], [],
                         "children started after SIGINT")
        self.assertEqual(records, at_signal)
        self.assertEqual([subcommand(child)[0] for child in records[-5:]],
                         ["rev-list", "rev-parse", "worktree", "for-each-ref", "status"],
                         "planning's last reachability probe (D21, LQ-13), then the revalidation's four children")
        self.assertFalse(any(map(is_removal, records)))
        self.assertEqual(self.stages(result), [(str(tree), "not-attempted", "interrupted") for tree in trees],
                         result.stderr)
        first, second = result.document["targets"]
        # The first target's revalidation spawned four children and stopped
        # before its hidden-state probe; the second was never revalidated.
        self.assertEqual((first["reconciliation"], first["exit_status"], first["probes_performed"]), (None, None, 4))
        self.assertEqual((second["reconciliation"], second["exit_status"], second["probes_performed"]),
                         (None, None, 0))
        self.assertEqual(result.document["exit_code"], 130)
        self.assertEqual(self.snapshot(root, trees), before, "nothing removed")


if __name__ == "__main__":
    unittest.main()
