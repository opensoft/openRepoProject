"""Push and branch deletion: their refusals, path escaping, signals and
children (feature 004, the US3 push lane: T072 to T074, T076 and T077).

Sources: the project-clean delta's "Clean can explicitly push safe feature
branches" in openspec/changes/add-project-clean-all-safe/specs/, and draft PR
#19's scenario "The push child reaches its remote" (LQ-3's assumption);
specs/004-project-clean-all-safe/research.md R1, R4 and R5; data-model.md,
"States of push and delete-branch" and "Exit statuses"; contracts/project-clean.md,
"Streams" and "Git children"; lead rulings R-28, R-53 (P-1, P-5 to P-9, P-19,
P-23) and R-74 (c).

Expected human text comes from clean_support's fixtures (rule 8), and the
baseline messages push and delete-branch keep are written here as literals
(rule 11). Every repository is a disposable fixture under the test's
temporary directory, its remote a local bare repository (rule 4). Signals go
only to a `project` child (rule 7), and every pseudo-terminal run makes the
terminal its controlling terminal (rule 14).
"""
import errno
import os
import subprocess

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
                 f"  git -C {root} push origin 001-feature:001-feature\n")
        # The terminal shows the plan, then the answer echoed; input() writes
        # confirm()'s prompt to standard error at a terminal.
        self.assertEqual(result.stdout, shown + "yes\n", "the exact push plan, then the confirmation")
        self.assertTrue(result.stderr.startswith(CONFIRM + " "), result.stderr)
        [push] = pushes(clean_support.child_log(log))
        self.assertEqual(push.argv, ["-C", str(root), "push", "origin", "001-feature:001-feature"],
                         "pushed as shown: no pin, and no --force")
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
