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
        # number (plan review M3; data-model.md, "Exit statuses").
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
                self.assertEqual(result.stderr.endswith("Cancelled.\n"), signum is not None, result.stderr)
            with self.subTest("delete-branch", signal=name):
                branch = "002-merged-" + name.lower()
                self.git(root, "branch", branch)
                result, hook = self.run_signalled(launched("--action", "delete-branch", "--branch", branch), env,
                                                  signum)
                self.assertEqual(hook, "started\ndone\n", "no signal reached git branch -d or its hook")
                self.assertEqual(self.git(root, "for-each-ref", "refs/heads/" + branch), "", "the branch is gone")
                self.assertIn(f"Deleted branch {branch} (was ", result.stdout, "the child's own output")
                self.assert_status(result, expected)
                self.assertEqual(result.stderr.endswith("Cancelled.\n"), signum is not None, result.stderr)

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
                  f"git -C {escaped} push origin 001-feature:001-feature"),
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
        self.assertEqual(push.argv, ["-C", str(root), "push", "origin", f"{branch}:{branch}"], "no pin")
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
            self.assertTrue(result.stderr.endswith("Cancelled.\n"), result.stderr)
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
