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
import io
import json
import os
from pathlib import Path
import shlex
import shutil
import signal
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

    def batch(self, case, count=2, holder=None, trees_dir=None):
        """A repository at BASE/CASE/repo (or BASE/CASE/HOLDER/repo) with an
        origin at BASE/CASE/remote.git and count eligible worktrees at
        BASE/CASE/trees/NAME (or TREES_DIR/NAME) on branches NAME, in canonical
        order (raw path bytes). Returns (root, trees)."""
        top = self.base / case
        root = self._init_repo((top / holder if holder else top) / "repo", "main")
        self.bare_remote(root, name=f"{case}/remote.git")
        place = top / "trees" if trees_dir is None else trees_dir
        trees = [self.merged_worktree(name, path=place / name, root=root) for name in NAMES[:count]]
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
        # upstream object and lock are the first target's preflight; the
        # first target's ignored-file state and classification are its own.
        def merge_target_moves(root, trees):
            self.git(root, "commit", "-q", "--allow-empty", "-m", "the merge target moves")

        def second_branch_moves(root, trees):
            self.commit(trees[1], "the second target's branch moves", allow_empty=True)

        def second_upstream_moves(root, trees):
            self.git(root, "update-ref", "refs/remotes/origin/002-q", self.head(root, "main"))

        def second_locked(root, trees):
            self.git(root, "worktree", "lock", trees[1])

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
                    self.assertEqual(first["reconciliation"]["registry_entry_present"], True)
                    self.assertEqual(first["exit_status"], None)

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


if __name__ == "__main__":
    unittest.main()
