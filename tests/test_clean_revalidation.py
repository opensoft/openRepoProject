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
        self.assertEqual(strip_pins(removal.argv)[0][:6], ["-c", "status.showUntrackedFiles=normal",
                                                            "-c", "core.untrackedCache=false",
                                                            "-c", "core.fsmonitor=false"])

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


if __name__ == "__main__":
    unittest.main()
