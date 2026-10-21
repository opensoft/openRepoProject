"""Push and branch deletion: their refusals, path escaping, signals and
children (feature 004, the US3 push lane: T072 to T074, T076 and T077).

Sources: the project-clean delta's "Clean can explicitly push safe feature
branches" in openspec/changes/add-project-clean-all-safe/specs/, and draft PR
#19's scenario "The push child reaches its remote" (LQ-3's assumption);
specs/004-project-clean-all-safe/research.md R1, R4 and R5; data-model.md,
"States of push and delete-branch" and "Exit statuses"; contracts/project-clean.md,
"Streams" and "Git children"; lead rulings R-28, R-53 (P-1, P-5 to P-9, P-19,
P-23), R-74 (c) and R-101 (e), which rules on lane openRepoProject-3's fan-out
read F2: H-1 and H-2, the push vector, and M-1, a signal once the child ran.

Expected human text comes from clean_support's fixtures (rule 8), and the
baseline messages push and delete-branch keep are written here as literals
(rule 11). Every repository is a disposable fixture under the test's
temporary directory, its remote a local bare repository (rule 4). Signals go
only to a `project` child (rule 7), and every pseudo-terminal run makes the
terminal its controlling terminal (rule 14).
"""
import errno
import io
import os
from pathlib import Path
import shlex
import signal
import subprocess
import sys
import time
from unittest import mock

import clean_support

project = clean_support.load_project()
TEXT = clean_support.TEXT_FIXTURES

# The seven protocol pins, transcribed from contracts/project-clean.md, "Git
# children"; every Git child but the push child carries them.
PINS = ["-c", "protocol.allow=never", "-c", "protocol.file.allow=never",
        "-c", "protocol.ssh.allow=never", "-c", "protocol.git.allow=never",
        "-c", "protocol.http.allow=never", "-c", "protocol.https.allow=never",
        "-c", "protocol.ext.allow=never"]

# Baseline texts push and delete-branch keep (project at 961c405, :152-154).
CONFIRM = "Type yes to run this plan:"
CHANGED = "Cleanup state changed after confirmation; no command was run."
JSON_REFUSED = "--json cannot be combined with --apply; use JSON for the read-only plan."
INCOMPLETE = "REFUSED: " + TEXT["plan_incomplete"].format(
    CODE="inspection-incomplete", REMEDY=TEXT["remedy_inspection_incomplete"]) + "\n"
NO_TERMINAL = f"REFUSED: {CONFIRM} Supply explicit options when stdin is not a terminal.\n"

# Lead ruling R-101 (e) 2 (lane 3's M-1): a signal recorded once the push or
# `git branch -d` child has run is reported with git's status, never as
# `Cancelled.`, which the delta pairs with nothing mutated (project-clean
# spec.md:928-930). Region push's own text, written here as a literal.
INTERRUPTED = "Interrupted; {WHAT} had started and was waited for, and git exited with status {STATUS}.\n"

# The hook of the signal tests, installed as pre-push and as
# reference-transaction (T073). It acts only in a run whose environment names
# its log, and once per run (on `committed` for a reference transaction), so
# that fixture commands and the other transactions of one `git branch -d` pass
# through it. It records every SIGINT, SIGTERM or SIGHUP that reaches it and
# waits, at most 15 s, until the test creates the release file; with
# HOOK_KILL set it ends its own git, its parent, with SIGKILL instead.
HOOK = """#!/bin/sh
[ -n "$HOOK_LOG" ] || exit 0
cat > /dev/null
case "$0" in *reference-transaction) [ "$1" = committed ] || exit 0;; esac
[ -e "$HOOK_LOG" ] && exit 0
if [ -n "$HOOK_KILL" ]; then kill -KILL "$PPID"; exit 0; fi
trap 'echo INT >> "$HOOK_LOG"' INT
trap 'echo TERM >> "$HOOK_LOG"' TERM
trap 'echo HUP >> "$HOOK_LOG"' HUP
echo started >> "$HOOK_LOG"
i=0
while [ ! -e "$HOOK_RELEASE" ] && [ "$i" -lt 300 ]; do sleep 0.05; i=$((i + 1)); done
echo done >> "$HOOK_LOG"
"""

# PR #19's pre-push hook (T074): 7 s of sleep, unscaled, past the 5 s a probe
# child gets, recording every signal that reaches it.
SLEEPING_HOOK = """#!/bin/sh
[ -n "$HOOK_LOG" ] || exit 0
cat > /dev/null
trap 'echo INT >> "$HOOK_LOG"' INT
trap 'echo TERM >> "$HOOK_LOG"' TERM
trap 'echo HUP >> "$HOOK_LOG"' HUP
echo started >> "$HOOK_LOG"
sleep 7
echo done >> "$HOOK_LOG"
"""

# Git's credential prompts for the tty-credential fake's https://example.invalid.
PROMPTS = ("Username for 'https://example.invalid': ", "Password for 'https://user@example.invalid': ")


def words(record):
    """A counted child's argument vector after its leading -c pins."""
    argv, at = record.argv, 0
    while at + 1 < len(argv) and argv[at] == "-c":
        at += 2
    return argv[at:]


def pins(record):
    """The -c pins a counted child carries before its own words."""
    return record.argv[:len(record.argv) - len(words(record))]


def pushes(records):
    """The push children in the counting log."""
    return [record for record in records if words(record)[2:3] == ["push"]]


def deletions(records):
    """The `git branch -d` children in the counting log."""
    return [record for record in records if words(record)[2:4] == ["branch", "-d"]]


class PushTests(clean_support.CleanCase):

    def counting(self, real=None, env=None):
        """The counting wrapper first on PATH, in front of real (the real Git
        by default); returns the environment and the emptied log."""
        bin_dir, log = self.base / "counting-bin", self.base / "children.log"
        clean_support.install_counting_git(bin_dir, log, real=real or clean_support.REAL_GIT)
        clean_support.reset_child_log(log)
        return self.path_first(bin_dir, env), log

    def unpushed(self, branch, root=None):
        """A linked worktree of branch, published with `push -u origin`, then
        given one commit of its own, so that it is `unpushed`: origin's
        branch lacks a commit the local one holds and holds none it lacks.
        Needs an origin (bare_remote()). Returns the worktree's path."""
        root = self._root(root)
        tree = self._tree(branch, None)
        self.git(root, "worktree", "add", "-q", "-b", branch, tree)
        self.git(tree, "push", "-q", "-u", "origin", branch)
        self.advance(tree)
        return tree

    def advance(self, tree):
        """One more commit in the worktree at tree; returns its SHA."""
        return self.commit(tree, "one more", allow_empty=True)

    def refs(self, path):
        """Every ref of the repository at path with its object, as text."""
        return self.git(path, "for-each-ref", "--format=%(refname) %(objectname)")

    def stray_commit(self, message, root=None):
        """A commit on top of the root's HEAD that no local branch holds, made
        by `commit-tree`, as another clone's commit; returns its SHA."""
        return self.git(self._root(root), "commit-tree", "HEAD^{tree}", "-p", "HEAD", "-m", message).strip()

    def option_branch(self, name, root=None):
        """A clean linked worktree on the branch NAME, which `git branch`
        refuses for an option-like name but `update-ref` and `symbolic-ref`
        make, holding one commit of its own and no upstream (`unpublished`).
        Returns its head."""
        root = self._root(root)
        tree = self.base / "option-tree"
        self.git(root, "worktree", "add", "-q", "--detach", tree)
        self.git(root, "update-ref", "refs/heads/" + name, "HEAD")
        self.git(tree, "symbolic-ref", "HEAD", "refs/heads/" + name)
        return self.advance(tree)

    def push_named(self, root, branch, env):
        """`clean ROOT --apply --action push --branch=BRANCH --yes`, the branch
        in the `=` form, so that a name such as `--force` stays the value."""
        return self.run_cli("clean", root, "--apply", "--action", "push", f"--branch={branch}", "--yes", env=env)

    def pushed_as(self, log, root, *words):
        """The one push child in log, its argument vector `-C ROOT push WORDS`."""
        [push] = pushes(clean_support.child_log(log))
        self.assertEqual(push.argv, ["-C", str(root), "push", *words])

    def test_clean_push_an_unpushed_feature_branch(self):
        root = self.repo()
        remote = self.bare_remote()
        tree = self.unpushed("001-feature")
        env, log = self.counting()
        result = self.run_pty_steps(
            clean_support.cli_argv("clean", root, "--apply", "--action", "push", "--branch", "001-feature"),
            [(CONFIRM, "yes")], controlling_tty=True, env=env)
        self.assert_status(result, 0)
        shown = ("Cleanup action: push branch 001-feature\n"
                 f"Working directory: {root}\n"
                 f"  git -C {root} push -- origin refs/heads/001-feature:refs/heads/001-feature\n")
        # The terminal shows the plan, then the answer echoed; input() writes
        # confirm()'s prompt to standard error at a terminal.
        self.assertEqual(result.stdout, shown + "yes\n", "the exact push plan, then the confirmation")
        self.assertTrue(result.stderr.startswith(CONFIRM + " "), result.stderr)
        [push] = pushes(clean_support.child_log(log))
        self.assertEqual(push.argv, ["-C", str(root), "push", "--", "origin",
                                     "refs/heads/001-feature:refs/heads/001-feature"],
                         "pushed as shown: no pin, no --force, and both refs named in full (R-101 (e) 1)")
        self.assertEqual(self.git(remote, "rev-parse", "refs/heads/001-feature"),
                         self.git(tree, "rev-parse", "HEAD"))

        with self.subTest("a push the remote rejects leaves every local ref as it was"):
            self.advance(tree)
            hook = remote / "hooks" / "pre-receive"
            hook.write_text("#!/bin/sh\necho 'rejected by the fixture' >&2\nexit 1\n")
            hook.chmod(0o755)
            before = (self.refs(root), self.git(tree, "rev-parse", "HEAD"), self.refs(remote))
            result = self.run_cli("clean", root, "--apply", "--action", "push", "--branch", "001-feature",
                                  "--yes", env=env)
            self.assert_status(result, 1)  # git push's own status, passed through
            self.assertIn("pre-receive hook declined", result.stderr)
            self.assertEqual((self.refs(root), self.git(tree, "rev-parse", "HEAD"), self.refs(remote)), before)

    # Lane 3's H-1 (lead ruling R-101 (e) 1): the bare branch name in the
    # refspec let Git read it as a `+` force marker, as an option, or through
    # a configured push mapping. Each test below fails on the vector of
    # c9103ba, and each pushes the named branch to its own ref and nothing
    # else, never forced: `push [-u] -- REMOTE refs/heads/B:DESTINATION`.

    def test_clean_push_an_unpushed_feature_branch_named_plus_x(self):
        # X3: `+x` is a legal branch name, and `push -u origin +x` force-pushed
        # branch x over another clone's commit, x having diverged locally.
        root = self.repo()
        remote = self.bare_remote()
        theirs = self.stray_commit("another clone's x")
        self.git(root, "push", "-q", "origin", f"{theirs}:refs/heads/x")
        self.git(root, "branch", "x", self.stray_commit("the local x"))
        tree = self.base / "plus-x-tree"
        self.git(root, "worktree", "add", "-q", "-b", "+x", tree)
        head = self.advance(tree)
        env, log = self.counting()
        result = self.push_named(root, "+x", env)
        self.assert_status(result, 0)
        self.pushed_as(log, root, "-u", "--", "origin", "refs/heads/+x:refs/heads/+x")
        self.assertEqual(self.git(remote, "rev-parse", "refs/heads/x").strip(), theirs, "origin's x is not forced")
        self.assertEqual(self.git(remote, "rev-parse", "refs/heads/+x").strip(), head)

    def test_clean_push_an_unpushed_feature_branch_named_dash_dash_force(self):
        # X2: `push -u origin --force` read the name as the option and
        # force-pushed main, the default branch, over another clone's commit.
        root = self.repo()
        remote = self.bare_remote()
        self.git(root, "push", "-q", "-u", "origin", "main")
        theirs = self.stray_commit("another clone's main")
        self.git(root, "push", "-q", "origin", f"{theirs}:refs/heads/main")
        head = self.option_branch("--force")
        env, log = self.counting()
        result = self.push_named(root, "--force", env)
        self.assert_status(result, 0)
        self.pushed_as(log, root, "-u", "--", "origin", "refs/heads/--force:refs/heads/--force")
        self.assertEqual(self.git(remote, "rev-parse", "refs/heads/main").strip(), theirs, "origin's main is not forced")
        self.assertEqual(self.git(remote, "rev-parse", "refs/heads/--force").strip(), head)

    def test_clean_push_an_unpushed_feature_branch_named_dash_dash_mirror(self):
        # X1: `push -u origin --mirror` deleted a branch only origin holds and
        # published the repository's remote-tracking refs.
        root = self.repo()
        remote = self.bare_remote()
        self.git(root, "push", "-q", "-u", "origin", "main")
        self.git(root, "push", "-q", "origin", f"{self.stray_commit('only on origin')}:refs/heads/keep1")
        before = self.refs(remote).splitlines()
        head = self.option_branch("--mirror")
        env, log = self.counting()
        result = self.push_named(root, "--mirror", env)
        self.assert_status(result, 0)
        self.pushed_as(log, root, "-u", "--", "origin", "refs/heads/--mirror:refs/heads/--mirror")
        self.assertEqual(sorted(self.refs(remote).splitlines()), sorted([*before, f"refs/heads/--mirror {head}"]),
                         "origin gains the branch alone: nothing deleted, no remote-tracking ref published")

    def test_clean_push_an_unpushed_feature_branch_under_a_forced_push_mapping(self):
        # X6h: with remote.origin.push mapping every branch through a `+`
        # refspec, `push -u origin solo` became `solo -> other/solo (forced
        # update)`; a destination named in full leaves the mapping unused.
        root = self.repo()
        remote = self.bare_remote()
        theirs = self.stray_commit("another clone's other/solo")
        self.git(root, "push", "-q", "origin", f"{theirs}:refs/heads/other/solo")
        self.git(root, "config", "remote.origin.push", "+refs/heads/*:refs/heads/other/*")
        tree = self.base / "solo-tree"
        self.git(root, "worktree", "add", "-q", "-b", "solo", tree)
        head = self.advance(tree)
        env, log = self.counting()
        result = self.push_named(root, "solo", env)
        self.assert_status(result, 0)
        self.pushed_as(log, root, "-u", "--", "origin", "refs/heads/solo:refs/heads/solo")
        self.assertEqual(self.git(remote, "rev-parse", "refs/heads/other/solo").strip(), theirs,
                         "not forced through the mapping")
        self.assertEqual(self.git(remote, "rev-parse", "refs/heads/solo").strip(), head)

    def test_clean_push_an_unpushed_feature_branch_tracking_a_remote_named_a_b(self):
        # Lane 3's H-2, X5 (R-101 (e) 1): the upstream's short name `a/b/feat`
        # was cut at its first `/`, so the push went to remote `a` as
        # `feat:b/feat`. The remote and the destination now come from
        # branch.feat.remote and branch.feat.merge.
        # Since Git 2.51.0 (a5a727c448, "remote: detect collisions in remote
        # names") `git remote add` refuses a name nested under an existing
        # remote's, `a/b` beside `a`, or one that holds an existing remote's.
        # Git still reads, fetches and pushes such remotes when the config
        # names them, so each is written as `remote add` writes it, its url
        # and its default fetch refspec, and X5 runs on every Git.
        root = self.repo()
        self.bare_remote()
        remotes = {"a": self.base / "a.git", "a/b": self.base / "ab.git"}
        for name, path in remotes.items():
            self.git(self.base, "init", "-q", "--bare", path)
            self.git(root, "config", f"remote.{name}.url", path)
            self.git(root, "config", f"remote.{name}.fetch", f"+refs/heads/*:refs/remotes/{name}/*")
        self.assertEqual(sorted(self.git(root, "remote").split()), ["a", "a/b", "origin"])
        tree = self.base / "feat-tree"
        self.git(root, "worktree", "add", "-q", "-b", "feat", tree)
        self.git(tree, "push", "-q", "-u", "a/b", "feat")
        head = self.advance(tree)
        env, log = self.counting()
        result = self.push_named(root, "feat", env)
        self.assert_status(result, 0)
        self.pushed_as(log, root, "--", "a/b", "refs/heads/feat:refs/heads/feat")
        self.assertEqual(self.git(remotes["a/b"], "rev-parse", "refs/heads/feat").strip(), head)
        self.assertEqual(self.refs(remotes["a"]), "", "nothing pushed to remote a")

    def test_clean_push_an_unpushed_feature_branch_with_an_unusable_upstream_refuses(self):
        # R-101 (e) 1: an upstream whose configuration cannot be used runs no
        # push, and refuses as the code already did for an upstream it could
        # not map. This test pins two such forms: a local upstream (remote `.`)
        # named `team/base`, which was pushed to a remote `team`, and a second
        # merge ref, which was ignored, the short name taking the first. A
        # merge outside refs/heads/ is pinned by the test after this one
        # (R-130); a missing remote or merge value is not exercised here
        # (lane 3's W12 L-4).
        root = self.repo()
        remote = self.bare_remote()
        self.git(root, "branch", "team/base")
        local = self.base / "local-tree"
        self.git(root, "worktree", "add", "-q", "--track", "-b", "002-local", local, "team/base")
        self.advance(local)
        self.unpushed("003-two")
        self.git(root, "config", "--add", "branch.003-two.merge", "refs/heads/elsewhere")
        env, log = self.counting()
        for variant, branch, upstream in (("a local upstream", "002-local", "team/base"),
                                          ("two merge refs", "003-two", "origin/003-two")):
            with self.subTest(variant):
                before = (self.refs(root), self.refs(remote))
                clean_support.reset_child_log(log)
                result = self.push_named(root, branch, env)
                self.assert_status(result, 2)
                self.assertEqual(result.stderr, f"REFUSED: Unsupported upstream mapping for {branch}: {upstream}\n")
                self.assertEqual(pushes(clean_support.child_log(log)), [], "no push child")
                self.assertEqual((self.refs(root), self.refs(remote)), before)

    def test_clean_push_an_unpushed_feature_branch_whose_merge_is_outside_refs_heads_refuses(self):
        # Lead ruling R-130 (lane 3's W12 M-5, mutant N3): branch.B.merge must
        # name a branch under refs/heads/, or the push would land outside the
        # branch namespace: a tag, a review ref, or a branch literally named
        # `+refs/heads/feat`. Each upstream still resolves, through a remote `o`
        # whose fetch refspec maps every ref (`+*:refs/remotes/o/*`), so the row
        # is `unpushed` and this guard alone refuses it.
        root = self.repo()
        remote = self.bare_remote()
        self.git(root, "remote", "add", "o", remote)
        self.git(root, "config", "remote.o.fetch", "+*:refs/remotes/o/*")
        tree = self.base / "feat-tree"
        self.git(root, "worktree", "add", "-q", "-b", "feat", tree)
        self.advance(tree)
        env, log = self.counting()
        for merge in ("refs/tags/v1", "refs/for/main", "+refs/heads/feat"):
            with self.subTest(merge=merge):
                self.git(root, "config", "branch.feat.remote", "o")
                self.git(root, "config", "branch.feat.merge", merge)
                self.git(root, "update-ref", "refs/remotes/o/" + merge, "main")
                upstream = "o/" + merge
                self.assertEqual(self.git(root, "for-each-ref", "--format=%(upstream:short)", "refs/heads/feat"),
                                 upstream + "\n")
                before = (self.refs(root), self.refs(remote))
                clean_support.reset_child_log(log)
                result = self.push_named(root, "feat", env)
                self.assert_status(result, 2)
                self.assertEqual((result.stdout, result.stderr),
                                 ("", f"REFUSED: Unsupported upstream mapping for feat: {upstream}\n"))
                self.assertEqual(pushes(clean_support.child_log(log)), [], "no push child")
                self.assertEqual((self.refs(root), self.refs(remote)), before, "nothing pushed")

    def test_clean_push_refuses_a_branch_whose_upstream_was_deleted(self):
        root = self.repo()
        remote = self.bare_remote()
        self.merged_worktree("010-merged")
        self.unpushed("011-unmerged")
        for branch in ("010-merged", "011-unmerged"):
            self.git(root, "push", "-q", "origin", "--delete", branch)
        rows = {row["branch"]: row for row in self.run_json("clean", root, "--json").document["worktrees"]}
        self.assertEqual([(rows[branch]["classification"], rows[branch]["remote_present"])
                          for branch in ("010-merged", "011-unmerged")],
                         [("merged-removable", False), ("remote-gone", False)],
                         "a deleted upstream, on a merged and on an unmerged branch")
        env, log = self.counting()
        for branch, variant in (("010-merged", "merged"), ("011-unmerged", "unmerged")):
            with self.subTest(variant):
                clean_support.reset_child_log(log)
                result = self.run_cli("clean", root, "--apply", "--action", "push", "--branch", branch,
                                      "--yes", env=env)
                self.assert_status(result, 2)
                message = TEXT["push_remote_gone"].format(BRANCH=branch, UPSTREAM="origin/" + branch)
                self.assertEqual((result.stdout, result.stderr), ("", f"REFUSED: {message}\n"))
                self.assertEqual(pushes(clean_support.child_log(log)), [], "no push child")
                self.assertEqual(self.git(remote, "for-each-ref", "refs/heads/" + branch), "")

    # Lead ruling R-130 (lane 3's W12 M-1 to M-4 and L-3): the push's own
    # refusals before its vector is built, inherited from the baseline
    # (project:687-702 at 961c405), each pinned with its text, exit 2 and no
    # push child. With one removed (mutants P1 to P4 and N9), this module
    # stayed green: the push went ahead (P1, P2) or Git's own check failed it
    # with another status (P3, P4, N9).

    def assert_push_refused(self, root, branch, env, log, message, remote):
        """`clean ROOT --apply --action push --branch=BRANCH --yes` refused
        with message before anything is shown: exit 2, no push child, and
        every ref of the repository and of remote as it was."""
        before = (self.refs(root), self.refs(remote))
        clean_support.reset_child_log(log)
        result = self.push_named(root, branch, env)
        self.assert_status(result, 2)
        self.assertEqual((result.stdout, result.stderr), ("", f"REFUSED: {message}\n"))
        self.assertEqual(pushes(clean_support.child_log(log)), [], "no push child")
        self.assertEqual((self.refs(root), self.refs(remote)), before, "nothing pushed")

    def test_clean_push_refuses_the_default_branch(self):
        # P1 (project:5761-5762 at 92daad9): main, the merge target, one commit
        # ahead of its upstream origin/main; P1 pushed it to origin.
        root = self.repo()
        remote = self.bare_remote()
        self.git(root, "push", "-q", "-u", "origin", "main")
        self.advance(root)
        env, log = self.counting()
        self.assert_push_refused(root, "main", env, log,
                                 "The default branch is protected; use its normal repository workflow.", remote)

    def test_clean_push_refuses_a_dirty_worktree(self):
        # P2 (project:5763-5764): an unpublished branch with a commit of its own
        # whose worktree holds a staged and an untracked file, then the same
        # worktree moved away, missing; P2 published the branch from each.
        root = self.repo()
        remote = self.bare_remote()
        tree = self.base / "dirty-tree"
        self.git(root, "worktree", "add", "-q", "-b", "001-dirty", tree)
        self.advance(tree)
        (tree / "staged").write_text("staged")
        self.git(tree, "add", "staged")
        (tree / "untracked").write_text("untracked")
        env, log = self.counting()
        message = "Cannot push 001-dirty; its worktree is dirty, missing, or unreadable."
        with self.subTest("dirty"):
            self.assert_push_refused(root, "001-dirty", env, log, message, remote)
            self.assertEqual(self.git(tree, "status", "--porcelain"), "A  staged\n?? untracked\n", "the work is kept")
        with self.subTest("missing"):
            tree.rename(tree.with_name("dirty-tree.moved"))
            self.assert_push_refused(root, "001-dirty", env, log, message, remote)

    def test_clean_push_refuses_a_detached_worktree(self):
        # P3 (project:5765-5766): `--branch detached` names the detached row;
        # without the refusal Git's own push failed, exit 1.
        root = self.repo()
        remote = self.bare_remote()
        self.git(root, "worktree", "add", "-q", "--detach", self.base / "detached-tree")
        env, log = self.counting()
        self.assert_push_refused(root, "detached", env, log,
                                 "Cannot push a detached worktree; name the branch first.", remote)

    def test_clean_push_refuses_a_branch_to_reconcile(self):
        # P4 (project:5767-5768): a diverged and a remote-ahead branch, each
        # refused before its push; without the refusal Git rejected each as a
        # non-fast-forward, exit 1. No row of the evidence model reaches
        # review-required (classify()'s docstring), so an unpushed row is
        # relabelled review-required in process for the third case.
        root = self.repo()
        remote = self.bare_remote()
        diverged = self.unpushed("001-diverged")
        self.git(diverged, "push", "-q", "origin", "001-diverged")
        self.git(diverged, "reset", "-q", "--hard", "HEAD~1")
        self.commit(diverged, "the local side", allow_empty=True)  # one commit each side
        behind = self.unpushed("002-remote-ahead")
        self.git(behind, "push", "-q", "origin", "002-remote-ahead")
        self.git(behind, "reset", "-q", "--hard", "HEAD~1")  # origin one commit ahead
        self.unpushed("003-review")
        report = self.run_json("clean", root, "--json").document
        rows = {row["branch"]: row["classification"] for row in report["worktrees"]}
        self.assertEqual([rows[branch] for branch in ("001-diverged", "002-remote-ahead", "003-review")],
                         ["diverged", "remote-ahead", "unpushed"])
        env, log = self.counting()
        for branch in ("001-diverged", "002-remote-ahead"):
            with self.subTest(branch):
                self.assert_push_refused(root, branch, env, log,
                                         f"Cannot push {branch}; reconcile its remote state first.", remote)
        with self.subTest("review-required, in process"):
            real = project.classify

            def relabel(row, merge_target):
                found = real(row, merge_target)
                if row.get("branch") == "003-review":
                    return "review-required", project.SECOND_RECOMMENDATIONS["review-required"]
                return found

            before = self.refs(remote)
            out, err = io.StringIO(), io.StringIO()
            with mock.patch.dict(os.environ, self.env, clear=True), \
                    mock.patch.object(project, "classify", relabel), \
                    mock.patch.object(project.sys, "stdout", out), mock.patch.object(project.sys, "stderr", err):
                status = project.main(["clean", str(root), "--apply", "--action", "push", "--branch=003-review",
                                       "--yes"])
            self.assertEqual((status, out.getvalue(), err.getvalue()),
                             (2, "", "REFUSED: Cannot push 003-review; reconcile its remote state first.\n"))
            self.assertEqual(self.refs(remote), before, "nothing pushed")

    def test_clean_push_refuses_to_publish_without_an_origin_remote(self):
        # N9 (project:5781-5782): an unpublished branch, first in a repository
        # with no remote, then with one remote not named origin, never pushed
        # to instead; without the refusal Git's own push to `origin` failed,
        # exit 128.
        root = self.repo()
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-q", "-b", "001-feature", tree)
        self.advance(tree)
        fork = self.base / "fork.git"
        self.git(self.base, "init", "-q", "--bare", fork)
        env, log = self.counting()
        message = "Cannot publish a branch without an origin remote."
        with self.subTest("no remote"):
            self.assertEqual(self.git(root, "remote"), "")
            self.assert_push_refused(root, "001-feature", env, log, message, fork)
        with self.subTest("a remote not named origin"):
            self.git(root, "remote", "add", "fork", fork)
            self.assert_push_refused(root, "001-feature", env, log, message, fork)
        self.assertEqual(self.git(root, "config", "--get-all", "branch.001-feature.remote", check=False), "",
                         "no upstream was set")

    @clean_support.not_root
    def test_clean_push_refuses_an_incomplete_inspection(self):
        root = self.repo()
        remote = self.bare_remote()
        self.unpushed("001-feature")
        pushed = self.git(remote, "rev-parse", "refs/heads/001-feature")
        self.git(root, "branch", "002-merged")  # at the merge target's tip, with no worktree
        broken = self.base / "broken-tree"
        self.git(root, "worktree", "add", "-q", "-b", "003-broken", broken)
        sealed = self.base / "sealed"
        sealed.mkdir()
        self.git(root, "worktree", "add", "-q", "-b", "004-sealed", sealed / "sealed-tree")
        self.addCleanup(os.chmod, sealed, 0o755)
        cases = (("push", "001-feature", pushes), ("delete-branch", "002-merged", deletions))

        fake = clean_support.install_fake_git(self.base / "fake-bin", "status-fails-in", path=broken)
        env, log = self.counting(real=fake)
        for action, branch, children in cases:
            with self.subTest("another row inspection-error", action=action):
                clean_support.reset_child_log(log)
                result = self.run_cli("clean", root, "--apply", "--action", action, "--branch", branch,
                                      "--yes", env=env)
                self.assert_status(result, 2)
                self.assertEqual((result.stdout, result.stderr), ("", INCOMPLETE))
                self.assertEqual(children(clean_support.child_log(log)), [], "no delegate")

        env, log = self.counting()

        def seal(running):
            os.chmod(sealed, 0o600)  # no search permission: the row's lstat fails

        for action, branch, children in cases:
            with self.subTest("a row unreadable after confirmation", action=action):
                clean_support.reset_child_log(log)
                result = self.run_pty_steps(
                    clean_support.cli_argv("clean", root, "--apply", "--action", action, "--branch", branch),
                    [(CONFIRM, seal), ("", "yes")], controlling_tty=True, env=env)
                os.chmod(sealed, 0o755)
                self.assert_status(result, 2)
                self.assertEqual(result.stderr, f"{CONFIRM} {INCOMPLETE}", "refused after confirmation")
                self.assertEqual(children(clean_support.child_log(log)), [], "no delegate")
        self.assertEqual(self.git(remote, "rev-parse", "refs/heads/001-feature"), pushed)
        self.assertNotEqual(self.git(root, "for-each-ref", "refs/heads/002-merged"), "")

    def test_clean_push_refuses_a_change_after_confirmation(self):
        # The baseline's revalidation after confirmation (project:656-666 at
        # 961c405), now through the full re-inspection (T076): a branch's row
        # or head that changed while `Type yes` waited refuses with the
        # baseline message, exit 2, and runs no delegate.
        root = self.repo()
        remote = self.bare_remote()
        tree = self.unpushed("001-feature")
        pushed = self.git(remote, "rev-parse", "refs/heads/001-feature")
        self.git(root, "branch", "002-merged")
        env, log = self.counting()

        def dirty(running):
            (tree / "late-change").write_text("preserve")

        def advance(running):
            self.git(root, "branch", "-f", "002-merged", self.git(tree, "rev-parse", "HEAD").strip())

        for action, branch, change, children in (("push", "001-feature", dirty, pushes),
                                                 ("delete-branch", "002-merged", advance, deletions)):
            with self.subTest(action=action):
                clean_support.reset_child_log(log)
                result = self.run_pty_steps(
                    clean_support.cli_argv("clean", root, "--apply", "--action", action, "--branch", branch),
                    [(CONFIRM, change), ("", "yes")], controlling_tty=True, env=env)
                self.assert_status(result, 2)
                self.assertEqual(result.stderr, f"{CONFIRM} REFUSED: {CHANGED}\n")
                self.assertEqual(children(clean_support.child_log(log)), [], "no delegate")
        self.assertEqual(self.git(remote, "rev-parse", "refs/heads/001-feature"), pushed)
        self.assertNotEqual(self.git(root, "for-each-ref", "refs/heads/002-merged"), "")

    # Lane 3's RB M-1 and W4 M-2 (lead rulings R-107 and R-117): delete-branch's
    # first two refusals, inherited from the baseline (project:727-730 at
    # 961c405), each pinned where the other cannot stand in for it. Without
    # the first, `git branch -d` deleted the merge target, exit 0; without the
    # second, Git's own check refused, exit 1. Both refuse before the plan is
    # shown and run no child after the inspection.

    def test_clean_a_branch_deletion_of_the_default_branch_is_refused(self):
        # The main worktree on a branch cut from main, so that no worktree holds
        # main, the merge target, which is merged into itself and into HEAD.
        root = self.repo()
        self.bare_remote()
        self.git(root, "checkout", "-q", "-b", "001-work")
        self.assertNotIn("branch refs/heads/main", self.git(root, "worktree", "list", "--porcelain"))
        before = self.refs(root)
        env, log = self.counting()
        result = self.run_cli("clean", root, "--apply", "--action", "delete-branch", "--branch", "main", "--yes",
                              env=env)
        self.assert_status(result, 2)
        self.assertEqual((result.stdout, result.stderr),
                         ("", "REFUSED: The default branch is protected and cannot be deleted.\n"))
        self.assertEqual(deletions(clean_support.child_log(log)), [], "no git branch -d")
        self.assertEqual(self.refs(root), before, "main is kept")

    def test_clean_a_branch_deletion_of_a_branch_a_worktree_holds_is_refused(self):
        # Each branch is merged into main, the merge target, so that this refusal
        # alone stands before `git branch -d`: held by a present linked worktree,
        # then by the main worktree, checked out on a branch other than main.
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-merged")
        env, log = self.counting()
        for holder, branch in (("a linked worktree", "001-merged"), ("the main worktree", "002-held")):
            with self.subTest(holder):
                if branch == "002-held":
                    self.git(root, "checkout", "-q", "-b", branch)
                self.assertIn(branch, self.git(root, "branch", "--merged", "main", "--format=%(refname:short)").split())
                before = self.refs(root)
                clean_support.reset_child_log(log)
                result = self.run_cli("clean", root, "--apply", "--action", "delete-branch", "--branch", branch,
                                      "--yes", env=env)
                self.assert_status(result, 2)
                self.assertEqual((result.stdout, result.stderr), (
                    "", "REFUSED: Remove the linked worktree first; branch deletion is a separate action.\n"))
                self.assertEqual(deletions(clean_support.child_log(log)), [], "no git branch -d")
                self.assertEqual(self.refs(root), before, "the branch is kept")
        self.assertTrue((tree / "work-001-merged").is_file(), "the linked worktree is kept")

    def test_clean_push_and_branch_deletion_stay_human_only(self):
        # Pins T048's argument check: no child runs, `git --version` included.
        root = self.repo()
        env, log = self.counting()
        for action in ("push", "delete-branch"):
            with self.subTest(action=action):
                clean_support.reset_child_log(log)
                result = self.run_json("clean", root, "--apply", "--json", "--action", action,
                                       "--branch", "001-feature", "--yes", env=env)
                self.assert_status(result, 2)
                self.assertEqual((result.document["code"], result.document["error"]),
                                 ("invalid-arguments", JSON_REFUSED))
                self.assertEqual(clean_support.child_log(log), [], "no child")

    def test_clean_push_with_standard_output_closed_runs_no_child(self):
        # Lead ruling R-74 (c)(3): the check after printing (R-55) runs after
        # the push plan, so a closed standard output refuses before any child,
        # as `internal-error`, exit 2 (R-55's reading; LQ-7).
        root = self.repo()
        remote = self.bare_remote()
        self.unpushed("001-feature")
        before = self.refs(remote)
        env, log = self.counting()
        read, write = os.pipe()
        os.close(read)
        try:
            result = subprocess.run(
                clean_support.cli_argv("clean", root, "--apply", "--action", "push", "--branch", "001-feature",
                                       "--yes"),
                cwd=self.base, env=env, stdin=subprocess.DEVNULL, stdout=write, stderr=subprocess.PIPE,
                timeout=clean_support.TIMEOUT)
        finally:
            os.close(write)
        broken = TEXT["internal_error"].format(TYPE="BrokenPipeError",
                                               TEXT=f"[Errno {errno.EPIPE}] {os.strerror(errno.EPIPE)}")
        self.assertEqual((result.returncode, result.stderr.decode()), (2, f"REFUSED: {broken}\n"))
        self.assertEqual(pushes(clean_support.child_log(log)), [], "no push child")
        self.assertEqual(self.refs(remote), before)

    def install_hooks(self, text, *names, root=None):
        """Write text as each named hook of the repository, executable."""
        hooks = self.common_dir(root) / "hooks"
        hooks.mkdir(exist_ok=True)
        for name in names:
            (hooks / name).write_text(text)
            (hooks / name).chmod(0o755)

    def run_signalled(self, argv, env, signum):
        """Run argv in a session of its own and, once the hook has started,
        send signum (unless None) to that process alone, wait 0.2 s so that it
        is recorded while the hook still waits, then release the hook. Returns
        the run, its streams as text, and the hook's log."""
        log, release = Path(env["HOOK_LOG"]), Path(env["HOOK_RELEASE"])
        for path in (log, release):
            if path.exists():
                path.unlink()
        child = subprocess.Popen(argv, cwd=self.base, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, start_new_session=True)
        try:
            deadline = time.monotonic() + clean_support.TIMEOUT
            while child.poll() is None and not (log.exists() and "started" in log.read_text()):
                if time.monotonic() > deadline:
                    self.fail(f"the hook did not start within {clean_support.TIMEOUT} s")
                time.sleep(0.01)
            if signum is not None and child.poll() is None:
                os.kill(child.pid, signum)
                time.sleep(0.2)
            release.touch()
            out, err = child.communicate(timeout=clean_support.TIMEOUT)
        finally:
            if child.poll() is None:
                os.killpg(child.pid, signal.SIGKILL)
                child.wait()
        result = subprocess.CompletedProcess(argv, child.returncode, out.decode("utf-8", "surrogateescape"),
                                             err.decode("utf-8", "surrogateescape"))
        return result, log.read_text() if log.exists() else ""

    def test_clean_a_signal_during_the_push_or_branch_deletion(self):
        # Through the launcher with the real table. A signal sent to project
        # alone while the child's hook waits is recorded only: the hook sees
        # none, the child completes, and project exits 128 plus the signal's
        # number (plan review M3; data-model.md, "Exit statuses"), reporting
        # the child's status and never `Cancelled.` (R-101 (e) 2).
        root = self.repo()
        remote = self.bare_remote()
        tree = self.unpushed("001-feature")
        self.install_hooks(HOOK, "pre-push", "reference-transaction")
        env = dict(self.env, HOOK_LOG=str(self.base / "hook.log"), HOOK_RELEASE=str(self.base / "hook.release"))

        def launched(*args):
            return clean_support.launched_argv(None, "clean", root, "--apply", *args, "--yes")

        for signum in (None, signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
            name = "none" if signum is None else signum.name
            expected = 0 if signum is None else 128 + signum
            with self.subTest("push", signal=name):
                head = self.advance(tree)
                result, hook = self.run_signalled(launched("--action", "push", "--branch", "001-feature"), env, signum)
                self.assertEqual(hook, "started\ndone\n", "no signal reached the push or its hook")
                self.assertEqual(self.git(remote, "rev-parse", "refs/heads/001-feature").strip(), head,
                                 "the push was waited for and completed")
                self.assert_status(result, expected)
                self.assertNotIn("Cancelled.", result.stderr, "the push ran")
                self.assertEqual(result.stderr.endswith(INTERRUPTED.format(WHAT="the push", STATUS=0)),
                                 signum is not None, result.stderr)
            with self.subTest("delete-branch", signal=name):
                branch = "002-merged-" + name.lower()
                self.git(root, "branch", branch)
                result, hook = self.run_signalled(launched("--action", "delete-branch", "--branch", branch), env,
                                                  signum)
                self.assertEqual(hook, "started\ndone\n", "no signal reached git branch -d or its hook")
                self.assertEqual(self.git(root, "for-each-ref", "refs/heads/" + branch), "", "the branch is gone")
                self.assertIn(f"Deleted branch {branch} (was ", result.stdout, "the child's own output")
                self.assert_status(result, expected)
                self.assertNotIn("Cancelled.", result.stderr, "git branch -d ran")
                self.assertEqual(result.stderr, INTERRUPTED.format(WHAT="the branch deletion", STATUS=0)
                                 if signum is not None else "")

        with self.subTest("a hook that ends its own git push with SIGKILL"):
            self.advance(tree)
            before = self.refs(remote)
            result = self.run_launched(None, "clean", root, "--apply", "--action", "push", "--branch",
                                       "001-feature", "--yes",
                                       env=dict(env, HOOK_KILL="1", HOOK_LOG=str(self.base / "kill.log")))
            self.assert_status(result, 128 + signal.SIGKILL)
            self.assertEqual(self.refs(remote), before, "nothing pushed")
        with self.subTest("a git branch -d that dies of SIGKILL"):
            fake = self.base / "kill-bin" / "git"
            fake.parent.mkdir()
            fake.write_text('#!/bin/sh\ncase " $* " in *" branch -d "*) kill -KILL $$;; esac\n'
                            f'exec {shlex.quote(clean_support.REAL_GIT)} "$@"\n')
            fake.chmod(0o755)
            self.git(root, "branch", "003-merged-killed")
            result = self.run_launched(None, "clean", root, "--apply", "--action", "delete-branch", "--branch",
                                       "003-merged-killed", "--yes", env=self.path_first(fake.parent))
            self.assert_status(result, 128 + signal.SIGKILL)
            self.assertNotEqual(self.git(root, "for-each-ref", "refs/heads/003-merged-killed"), "")

    def test_clean_a_signal_during_the_push_or_branch_deletion_once_git_has_mutated(self):
        # Lane 3's M-1 (lead ruling R-101 (e) 2): a slow git wrapper first on
        # PATH runs the real push, or `git branch -d`, to its end, so that the
        # ref has moved, and only then waits for the release while the test
        # sends the signal to project alone. Project still waits for the
        # child, reports git's status, exits 128 plus the signal's number, and
        # never prints `Cancelled.`, which the delta pairs with nothing mutated
        # (project-clean spec.md:928-930). Through the launcher, the real table.
        root = self.repo()
        remote = self.bare_remote()
        tree = self.unpushed("001-feature")
        self.git(root, "branch", "002-merged")
        real = shlex.quote(clean_support.REAL_GIT)
        slow = self.base / "slow-bin" / "git"
        slow.parent.mkdir()
        slow.write_text("#!/bin/sh\n"
                        f'case " $* " in *" push "*|*" branch -d "*) ;; *) exec {real} "$@";; esac\n'
                        f'{real} "$@"\nstatus=$?\necho started >> "$HOOK_LOG"\ni=0\n'
                        'while [ ! -e "$HOOK_RELEASE" ] && [ "$i" -lt 300 ]; do sleep 0.05; i=$((i + 1)); done\n'
                        'echo done >> "$HOOK_LOG"\nexit $status\n')
        slow.chmod(0o755)
        env = dict(self.path_first(slow.parent), HOOK_LOG=str(self.base / "slow.log"),
                   HOOK_RELEASE=str(self.base / "slow.release"))

        def launched(*args):
            return clean_support.launched_argv(None, "clean", root, "--apply", *args, "--yes")

        for signum in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
            with self.subTest("push", signal=signum.name):
                head = self.advance(tree)
                result, log = self.run_signalled(launched("--action", "push", "--branch", "001-feature"), env, signum)
                self.assertEqual(log, "started\ndone\n", "the signal came after the push, while git still ran")
                self.assertEqual(self.git(remote, "rev-parse", "refs/heads/001-feature").strip(), head, "pushed")
                self.assert_status(result, 128 + signum)
                self.assertNotIn("Cancelled.", result.stderr)
                self.assertTrue(result.stderr.endswith(INTERRUPTED.format(WHAT="the push", STATUS=0)), result.stderr)
        with self.subTest("delete-branch", signal="SIGTERM"):
            result, log = self.run_signalled(launched("--action", "delete-branch", "--branch", "002-merged"), env,
                                             signal.SIGTERM)
            self.assertEqual(log, "started\ndone\n", "the signal came after the deletion, while git still ran")
            self.assertEqual(self.git(root, "for-each-ref", "refs/heads/002-merged"), "", "the branch is gone")
            self.assertIn("Deleted branch 002-merged (was ", result.stdout, "the child's own output")
            self.assert_status(result, 128 + signal.SIGTERM)
            self.assertEqual(result.stderr, INTERRUPTED.format(WHAT="the branch deletion", STATUS=0))

    def test_clean_push_and_delete_branch_escape_their_paths(self):
        # The root's name holds a tab (Cc) and U+202E (Cf), and so does one
        # branch's U+202E; each is built with chr(), as is the backslash of
        # each expected escape (rule 6). Without a terminal and --yes,
        # confirm() refuses after the plan is shown, so nothing runs.
        backslash = chr(92)
        root = self.repo("re" + chr(9) + "po" + chr(0x202E) + "x")
        self.bare_remote()
        self.unpushed("001-feature")
        reversed_branch = "002-merged" + chr(0x202E)
        for branch in ("002-merged", reversed_branch):
            self.git(root, "branch", branch)
        escaped = f"$'{self.base}/re{backslash}u0009po{backslash}u202ex'"
        shown = f"$'002-merged{backslash}u202e'"
        pinned = " ".join(PINS)
        cases = (("push", "001-feature", "push branch 001-feature",
                  f"git -C {escaped} push -- origin refs/heads/001-feature:refs/heads/001-feature"),
                 ("delete-branch", "002-merged", "delete verified merged local branch 002-merged",
                  f"git {pinned} -C {escaped} branch -d 002-merged"),
                 ("delete-branch", reversed_branch, f"delete verified merged local branch {shown}",
                  f"git {pinned} -C {escaped} branch -d {shown}"))
        for action, branch, what, command in cases:
            with self.subTest(action=action, branch=ascii(branch)):
                result = self.run_cli("clean", root, "--apply", "--action", action, "--branch", branch)
                self.assert_status(result, 2)
                self.assertEqual(result.stdout, f"Cleanup action: {what}\nWorking directory: {escaped}\n  {command}\n")
                self.assertEqual(result.stderr, NO_TERMINAL)
                self.assertFalse({chr(9), chr(0x202E)} & set(result.stdout + result.stderr),
                                 "never the raw code points")

    def run_session(self, argv, env):
        """Run argv in a session of its own, so that its process group is its
        pid, within the 20 s limit. Returns the run, its streams as text, with
        the attribute `pid`."""
        child = subprocess.Popen(argv, cwd=self.base, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, start_new_session=True)
        try:
            out, err = child.communicate(timeout=clean_support.TIMEOUT)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.wait()
            self.fail(f"run passed {clean_support.TIMEOUT} s")
        result = subprocess.CompletedProcess(argv, child.returncode, out.decode("utf-8", "surrogateescape"),
                                             err.decode("utf-8", "surrogateescape"))
        result.pid = child.pid
        return result

    def assert_children(self, records, pid, root, branch, kept=()):
        """The push child alone: the vector shown, no pin, project's process
        group, the seventeen names removed but those kept; every other child:
        the seven pins, its own process group, no scrubbed name. Returns the
        push child's record."""
        [push] = pushes(records)
        self.assertEqual(push.argv, ["-C", str(root), "push", "--", "origin",
                                     f"refs/heads/{branch}:refs/heads/{branch}"], "no pin")
        self.assertEqual((push.ppid, push.pgid), (pid, pid), "project's own process group")
        self.assertEqual(push.names, tuple(kept))
        others = [record for record in records if record is not push]
        self.assertTrue(others)
        for record in others:
            self.assertEqual(pins(record)[-len(PINS):], PINS, record.argv)
            self.assertEqual((record.ppid, record.pgid), (pid, record.pid), "a process group of its own")
            self.assertIn(record.names, ((), ("GIT_OPTIONAL_LOCKS",)), record.argv)
        return push

    def test_clean_the_push_child_reaches_its_remote(self):
        # PR #19's scenario (LQ-3; research.md R1; lead ruling R-28): ROOT the
        # main worktree's absolute path, project in a session of its own with
        # GIT_DIR naming another repository and GIT_CONFIG_PARAMETERS set,
        # here to a pin that would refuse a push to a local path; the sh
        # counting wrapper, and the real table.
        root = self.repo()
        remote = self.bare_remote()
        tree = self.unpushed("020-reach")
        other = self.repo("other")
        env, log = self.counting()
        env.update(GIT_DIR=str(other / ".git"), GIT_CONFIG_PARAMETERS="'protocol.file.allow'='never'")
        argv = clean_support.cli_argv("clean", root, "--apply", "--action", "push", "--branch", "020-reach", "--yes")

        result = self.run_session(argv, env)
        self.assert_status(result, 0)
        self.assert_children(clean_support.child_log(log), result.pid, root, "020-reach")
        self.assertEqual(self.git(remote, "rev-parse", "refs/heads/020-reach"), self.git(tree, "rev-parse", "HEAD"))

        with self.subTest("a pre-push hook that sleeps 7 s; the caller's GIT_ALLOW_PROTOCOL kept"):
            self.install_hooks(SLEEPING_HOOK, "pre-push")
            head = self.advance(tree)
            clean_support.reset_child_log(log)
            hook = self.base / "sleeping-hook.log"
            result = self.run_session(argv, dict(env, GIT_ALLOW_PROTOCOL="file", HOOK_LOG=str(hook)))
            self.assert_status(result, 0)
            self.assertEqual(hook.read_text(), "started\ndone\n", "no signal reached the push or its hook")
            self.assert_children(clean_support.child_log(log), result.pid, root, "020-reach",
                                 kept=("GIT_ALLOW_PROTOCOL",))
            self.assertEqual(self.git(remote, "rev-parse", "refs/heads/020-reach").strip(), head)

        with self.subTest("the caller's GIT_ALLOW_PROTOCOL is honoured (R-28)"):
            self.advance(tree)
            before = self.refs(remote)
            clean_support.reset_child_log(log)
            result = self.run_session(argv, dict(env, GIT_ALLOW_PROTOCOL="ssh"))
            self.assert_status(result, 128)  # git push's own: transport 'file' not allowed
            self.assertIn("transport 'file' not allowed", result.stderr)
            self.assert_children(clean_support.child_log(log), result.pid, root, "020-reach",
                                 kept=("GIT_ALLOW_PROTOCOL",))
            self.assertEqual(self.refs(remote), before)

    def test_clean_the_push_child_reaches_its_remote_at_a_terminal(self):
        # PR #19's scenario at a pseudo-terminal made project's controlling
        # terminal (R-31), with --yes: the tty-credential fake behind the
        # counting wrapper opens /dev/tty and Git prompts there.
        root = self.repo()
        remote = self.bare_remote()
        tree = self.unpushed("021-terminal")
        fake_dir = self.base / "fake-bin"
        env, log = self.counting(real=clean_support.install_fake_git(fake_dir, "tty-credential"))
        argv = clean_support.cli_argv("clean", root, "--apply", "--action", "push", "--branch", "021-terminal",
                                      "--yes")
        result = self.run_pty_steps(argv, list(zip(PROMPTS, ("user", "secret"))), controlling_tty=True, env=env)
        self.assert_status(result, 0)
        [event] = [event for event in clean_support.fake_events(fake_dir) if event["event"] == "tty"]
        [push] = pushes(clean_support.child_log(log))
        self.assertEqual((event["tty"], event["fill_status"], event["username"], event["password"]),
                         ("opened", 0, "user", "secret"), "Git's prompts answered at the terminal")
        self.assertEqual(event["pid"], push.pid)
        self.assertEqual(event["foreground"], event["pgid"], "the push child in the terminal's foreground")
        self.assertEqual((push.pgid, push.ppid), (event["pgid"], event["pgid"]),
                         "its group is project's, which leads the terminal's session")
        self.assertEqual(self.git(remote, "rev-parse", "refs/heads/021-terminal"), self.git(tree, "rev-parse", "HEAD"))

        with self.subTest("^C typed at the username prompt"):
            self.advance(tree)
            before = self.refs(remote)
            result = self.run_pty_steps(argv, [(PROMPTS[0], chr(3))], controlling_tty=True, env=env)
            self.assert_status(result, 130)  # D19's first row: SIGINT was recorded
            # The push child was spawned, so project cannot say nothing was
            # mutated: it reports git's own status, never `Cancelled.` (R-101 (e) 2).
            self.assertNotIn("Cancelled.", result.stderr)
            self.assertTrue(result.stderr.endswith(INTERRUPTED.format(WHAT="the push", STATUS=130)), result.stderr)
            self.assertEqual(self.refs(remote), before, "nothing pushed")

    def test_clean_the_delegate_relay_passes_both_streams_whole(self):
        # Lead ruling R-53 P-1: the `git branch -d` delegate runs on the driver,
        # and RelayParser writes each chunk of its standard output and of its
        # standard error to project's own, whole: here a fake git writes every
        # byte value, about 200 KiB to each stream, then exits 3. In process,
        # with project's streams replaced by buffers.
        fake_dir = self.base / "relay-bin"
        fake_dir.mkdir()
        source = ("import sys\n"
                  "out, err = bytes(range(256)) * 800, bytes(reversed(range(256))) * 700\n"
                  "for at in range(0, len(out), 4096):\n"
                  "    for stream, data in ((sys.stdout.buffer, out), (sys.stderr.buffer, err)):\n"
                  "        stream.write(data[at:at + 4096])\n"
                  "        stream.flush()\n"
                  "sys.exit(3)\n")
        (fake_dir / "git").write_text(f"#!/bin/sh\nexec {shlex.quote(sys.executable)} -c {shlex.quote(source)}\n")
        (fake_dir / "git").chmod(0o755)
        stdout, stderr = io.TextIOWrapper(io.BytesIO()), io.TextIOWrapper(io.BytesIO())
        path = os.pathsep.join([str(fake_dir), os.environ.get("PATH", "")])
        with mock.patch.dict(os.environ, {"PATH": path}), mock.patch.object(project.sys, "stdout", stdout), \
                mock.patch.object(project.sys, "stderr", stderr):
            outcome = project.run_bounded(("delegate", ["-C", str(self.base), "branch", "-d", "relayed"], None),
                                          project.RelayParser(), project.Invocation())
        self.assertEqual((outcome.status, outcome.result), (3, b""))
        self.assertEqual(stdout.buffer.getvalue(), bytes(range(256)) * 800)
        self.assertEqual(stderr.buffer.getvalue(), bytes(reversed(range(256))) * 700)
        self.assertEqual((len(outcome.stderr), outcome.stderr_bytes), (4096, 256 * 700),
                         "the driver still keeps the standard-error head")

    def test_clean_a_branch_deletion_that_cannot_be_spawned(self):
        # Lead ruling R-81 (b): a `git branch -d` delegate that cannot be
        # spawned gives the baseline's refusal, execute()'s `Cannot run git:
        # ...` (project:194-198), which push_or_delete() builds from
        # run_bounded()'s detail, exit 2, and no other child. In process, so
        # that git goes at the moment of deletion: the counting wrapper is the
        # only git on PATH (path_without_git()), the full re-inspection after
        # confirmation runs through it as built, and only then is the wrapper
        # made not executable, or removed. Every spawn attempt is recorded
        # through subprocess.Popen, which all three of project's spawns use.
        root = self.repo()
        self.bare_remote()
        self.git(root, "branch", "002-merged")  # at the merge target's tip, with no worktree
        wrapper = self.base / "counting-bin" / "git"
        delegate = ["git", *PINS, "-C", str(root), "branch", "-d", "002-merged"]
        shown = ("Cleanup action: delete verified merged local branch 002-merged\n"
                 f"Working directory: {root}\n"
                 f"  git {' '.join(PINS)} -C {root} branch -d 002-merged\n")
        for variant, disable, code in (("not executable", lambda: wrapper.chmod(0o644), errno.EACCES),
                                       ("missing", wrapper.unlink, errno.ENOENT)):
            with self.subTest(variant):
                env, log = self.counting(env=dict(self.env, PATH=self.path_without_git()))
                popen, marks = mock.Mock(wraps=subprocess.Popen), []
                out, err = io.StringIO(), io.StringIO()

                def then_unspawnable(*args, reinspect=project.require_unchanged_cleanup_state, disable=disable,
                                     popen=popen, marks=marks):
                    reinspect(*args)
                    disable()
                    marks.append(len(popen.call_args_list))

                with mock.patch.dict(os.environ, env, clear=True), \
                        mock.patch.object(project, "require_unchanged_cleanup_state", then_unspawnable), \
                        mock.patch.object(project.subprocess, "Popen", popen), \
                        mock.patch.object(project.sys, "stdout", out), mock.patch.object(project.sys, "stderr", err):
                    status = project.main(["clean", str(root), "--apply", "--action", "delete-branch",
                                           "--branch", "002-merged", "--yes"])
                self.assertEqual(len(marks), 1, "the re-inspection ran once, as built")
                self.assertEqual(status, 2, err.getvalue())
                self.assertEqual(out.getvalue(), shown, "the plan, and nothing relayed")
                self.assertEqual(err.getvalue(),
                                 f"REFUSED: Cannot run git: [Errno {code}] {os.strerror(code)}: 'git'\n")
                attempts = [call.args[0] for call in popen.call_args_list]
                self.assertEqual(attempts[marks[0]:], [delegate], "after the re-inspection, the delegate alone")
                records = clean_support.child_log(log)
                self.assertEqual(deletions(records), [], "no git branch -d ran")
                self.assertEqual(len(records), marks[0], "every other attempt was a child the wrapper counted")
                self.assertEqual({record.optional_locks for record in records}, {"0"}, "read-only probes only")
                self.assertNotEqual(self.git(root, "for-each-ref", "refs/heads/002-merged"), "", "the branch is kept")
