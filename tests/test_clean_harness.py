"""Self-tests of the clean harness in tests/clean_support.py (feature 004, lane B,
T008): the counting wrapper, the fake Gits, the direct registrations, the
pseudo-terminal runner and the text fixtures."""
import errno
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

from clean_support import (
    COUNTED_NAMES, NEXT_STEP_FIXTURES, OPTIONAL_LOCKS, REAL_GIT, SCRUBBED_NAMES,
    TEXT_FIXTURES, TIMEOUT, CleanCase, child_log, fake_events,
    install_counting_git, install_fake_git, load_project, reset_child_log,
    wait_for_event,
)

# The seven protocol pins, as the contract writes them (contracts/project-clean.md,
# "Git children"); a fake must match its command behind them.
PINS = ["-c", "protocol.allow=never", "-c", "protocol.file.allow=never",
        "-c", "protocol.ssh.allow=never", "-c", "protocol.git.allow=never",
        "-c", "protocol.http.allow=never", "-c", "protocol.https.allow=never",
        "-c", "protocol.ext.allow=never"]
STATUS = ["status", "--porcelain=v1", "-z", "--untracked-files=normal", "--ignored=matching"]
LS_FILES = ["ls-files", "-v", "--stage", "-z"]


def script(path, text):
    """An executable sh script at path; returns its path."""
    path = Path(path)
    path.write_text("#!/bin/sh\n" + text)
    path.chmod(0o755)
    return path


def group_gone(pgid):
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return True
    return False


class CleanHarnessTests(CleanCase):
    def run_argv(self, argv, env=None, cwd=None, **kwargs):
        return subprocess.run([os.fsdecode(a) if isinstance(a, Path) else a for a in argv],
                              env=self.env if env is None else env,
                              cwd=self.base if cwd is None else cwd,
                              capture_output=True, timeout=TIMEOUT, **kwargs)

    def spawn(self, argv, env=None):
        """A child in its own session, its streams discarded; killed at cleanup."""
        child = subprocess.Popen([os.fsdecode(a) for a in argv], env=self.env if env is None else env,
                                 cwd=self.base, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL, start_new_session=True)

        def stop():
            if child.poll() is None:
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                child.wait()
        self.addCleanup(stop)
        return child

    def assert_hangs(self, child):
        """child is still running half a second after it started, and TERM to its
        group then ends it."""
        with self.assertRaises(subprocess.TimeoutExpired):
            child.wait(timeout=0.5)
        os.killpg(child.pid, signal.SIGTERM)
        self.assertEqual(child.wait(timeout=TIMEOUT), -signal.SIGTERM)

    def fixture(self):
        """A root with a local origin and five merged, published worktrees."""
        root = self.repo()
        self.bare_remote()
        trees = [self.merged_worktree(f"00{number}-tree") for number in range(1, 6)]
        return root, trees

    def test_clean_counting_wrapper_records_and_execs(self):
        bin_dir, log = self.base / "bin", self.base / "children.log"
        snapshots = self.base / "snapshots"
        snapshots.mkdir()
        # The real git behind a stand-in that, as it starts, copies the log under
        # its own pid, then execs Git: a record in the copy was written before Git.
        stand_in = script(self.base / "stand-in-git",
                          f'cp "{log}" "{snapshots}/$$"\nexec "{REAL_GIT}" "$@"\n')
        wrapper = install_counting_git(bin_dir, log, real=stand_in)
        self.assertEqual(wrapper, bin_dir / "git")
        odd = [b"", b"two words", b"caf\xe9 \xff", b"%s %d \\0 \\n", b"'single' \"double\"",
               b"line\nbreak", b"-C", b"--version"]
        work = self.base / "work dir"
        work.mkdir()
        (self.base / "via link").symlink_to(work)
        cwd = self.base / "via link"

        with self.subTest("raw argument bytes, working directory, exec: Git's own pid"):
            child = subprocess.Popen([os.fsdecode(wrapper), "rev-parse", "--sq-quote", *odd],
                                     env=self.env, cwd=cwd, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, start_new_session=True)
            out, err = child.communicate(timeout=TIMEOUT)
            direct = self.run_argv([REAL_GIT, "rev-parse", "--sq-quote", *odd], cwd=cwd)
            self.assertEqual((child.returncode, out, err),
                             (direct.returncode, direct.stdout, direct.stderr))
            [record] = child_log(log)
            self.assertEqual(record.argv_bytes, [b"rev-parse", b"--sq-quote", *odd])
            self.assertEqual(record.argv, [os.fsdecode(a) for a in record.argv_bytes])
            self.assertEqual(record.cwd, os.path.realpath(cwd))
            self.assertEqual(record.pid, child.pid)  # wrapper, stand-in and Git: one pid
            self.assertEqual(record.pgid, child.pid)  # its own session's group
            self.assertEqual(record.ppid, os.getpid())
            self.assertEqual(record.names, ())
            self.assertIsNone(record.optional_locks)
            copy = child_log(snapshots / str(child.pid))
            self.assertEqual(copy, [record], "the record was complete before Git started")

        with self.subTest("exit status and both streams are the real git's"):
            reset_child_log(log)
            for args in (["rev-parse", "--show-toplevel"], ["--version"], ["no-such-command"]):
                wrapped = self.run_argv([wrapper, *args])
                direct = self.run_argv([REAL_GIT, *args])
                self.assertEqual((wrapped.returncode, wrapped.stdout, wrapped.stderr),
                                 (direct.returncode, direct.stdout, direct.stderr), args)
            self.assertEqual([r.argv for r in child_log(log)],
                             [["rev-parse", "--show-toplevel"], ["--version"], ["no-such-command"]])
            self.assertTrue(all(r.pgid == os.getpgrp() for r in child_log(log)))

        stub = script(self.base / "stub-git", "exit 0\n")
        counting = install_counting_git(self.base / "bin-stub", self.base / "stub.log", real=stub)
        with self.subTest("which counted names are set, the empty value included"):
            every = {name: "" if name == "GIT_DIR" else "/nonexistent" for name in SCRUBBED_NAMES}
            for env_names, expected in (
                    ({**every, OPTIONAL_LOCKS: "0"}, COUNTED_NAMES),
                    ({"GIT_ALLOW_PROTOCOL": "file", "GIT_DIR": ""}, ("GIT_DIR", "GIT_ALLOW_PROTOCOL")),
                    ({}, ())):
                reset_child_log(self.base / "stub.log")
                result = self.run_argv([counting, "status"], env={**self.env, **env_names})
                self.assertEqual(result.returncode, 0)
                [record] = child_log(self.base / "stub.log")
                self.assertEqual(record.names, expected)
                self.assertEqual(record.optional_locks, "0" if OPTIONAL_LOCKS in env_names else None)
            self.assertEqual(COUNTED_NAMES, (*SCRUBBED_NAMES, OPTIONAL_LOCKS))
            # Two transcriptions of the contract's list guard each other (R-42).
            self.assertEqual(SCRUBBED_NAMES, tuple(load_project().GIT_SCRUB))
            self.assertEqual(len(set(SCRUBBED_NAMES)), 17)

        with self.subTest("the process group without /proc, from ps"):
            no_proc = install_counting_git(self.base / "bin-ps", self.base / "ps.log", real=stub,
                                           proc=self.base / "no-proc")
            child = subprocess.Popen([os.fsdecode(no_proc), "status"], env=self.env,
                                     start_new_session=True)
            self.assertEqual(child.wait(timeout=TIMEOUT), 0)
            self.run_argv([no_proc, "status"])
            first, second = child_log(self.base / "ps.log")
            self.assertEqual((first.pid, first.pgid), (child.pid, child.pid))
            self.assertEqual(second.pgid, os.getpgrp())

        with self.subTest("hooks: worktree remove runs pre-hook, Git as a child, post-hook"):
            root = self.repo()
            self.bare_remote()
            clean_tree = self.merged_worktree("001-clean")
            dirty_tree = self.merged_worktree("002-dirty")
            (dirty_tree / "work").write_text("changed")
            order = self.base / "order"
            observer = script(self.base / "observer-git",
                              f'echo "git $PPID" >> "{order}"\nexec "{REAL_GIT}" "$@"\n')
            hooked = install_counting_git(
                self.base / "bin-hooks", self.base / "hooks.log", real=observer,
                hooks={"pre": f'echo "pre $target" >> "{order}"',
                       "post": f'echo "post $status" >> "{order}"'})
            for tree, status in ((clean_tree, 0), (dirty_tree, 128)):
                order.write_text("")
                reset_child_log(self.base / "hooks.log")
                result = self.run_argv([hooked, *PINS, "-C", root, "worktree", "remove", tree])
                self.assertEqual(result.returncode, status, result.stderr)
                [record] = child_log(self.base / "hooks.log")
                self.assertEqual(order.read_text().splitlines(),
                                 [f"pre {tree}", f"git {record.pid}", f"post {status}"])
                self.assertEqual(tree.exists(), status != 0)
            self.assertIn(b"fatal:", result.stderr)  # Git's own refusal reaches the caller
            order.write_text("")
            listed = self.run_argv([hooked, "-C", root, "worktree", "list"])
            self.assertEqual(listed.returncode, 0)
            self.assertEqual(order.read_text().splitlines(), [f"git {os.getpid()}"],
                             "no hook outside worktree remove, and Git is exec'd")

        with self.subTest("a record still being written is never parsed"):
            data = (self.base / "hooks.log").read_bytes() + log.read_bytes()
            whole = self.base / "whole.log"
            whole.write_bytes(data)
            records = child_log(whole)
            ends, at = [], 0
            for record in records:
                at += sum(len(field) + 1 for field in (
                    str(record.pid).encode(), str(record.ppid).encode(), str(record.pgid).encode(),
                    os.fsencode(record.cwd), " ".join(record.names).encode(),
                    (record.optional_locks or "").encode(), str(len(record.argv_bytes)).encode(),
                    *record.argv_bytes, b"end"))
                ends.append(at)
            self.assertEqual(ends[-1], len(data))
            cut = self.base / "cut.log"
            for size in range(len(data) + 1):
                cut.write_bytes(data[:size])
                complete = sum(1 for end in ends if end <= size)
                self.assertEqual(child_log(cut), records[:complete], size)
            cut.write_bytes(data[:ends[0] - 4] + b"xxx\0" + data[ends[0]:])
            with self.assertRaises(AssertionError):
                child_log(cut)

    def test_clean_fake_gits_behave_as_named(self):
        root, (tree1, tree2, tree3, tree4, tree5) = self.fixture()
        (tree1 / "untracked.txt").write_text("so that a real status prints a record")
        status_of = self.run_argv([REAL_GIT, "-C", tree1, *STATUS])
        self.assertEqual(status_of.stdout, b"?? untracked.txt\0")

        def fake(kind, **options):
            bin_dir = self.base / f"fake-{kind}-{len(list(self.base.glob('fake-*')))}"
            return bin_dir, install_fake_git(bin_dir, kind, **options)

        with self.subTest("version-2.35.0, behind the seven pins and the counting wrapper"):
            _, git = fake("version-2.35.0")
            for argv in ([git, *PINS, "--version"], [git, "--version"]):
                result = self.run_argv(argv)
                self.assertEqual((result.returncode, result.stdout), (0, b"git version 2.35.0\n"))
            log = self.base / "version.log"
            wrapper = install_counting_git(self.base / "bin-version", log, real=git)
            result = self.run_argv([wrapper, *PINS, "--version"])
            self.assertEqual(result.stdout, b"git version 2.35.0\n")
            self.assertEqual(child_log(log)[0].argv, [*PINS, "--version"])
            self.assertEqual(self.run_argv([git, "-C", tree1, *STATUS]).stdout, status_of.stdout)

        with self.subTest("flood-stderr: 70 KiB on standard error, then a real status"):
            _, git = fake("flood-stderr")
            result = self.run_argv([git, *PINS, "-C", tree1, *STATUS])
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stderr, b"E" * (70 * 1024))
            self.assertEqual(result.stdout, status_of.stdout)

        with self.subTest("ignored-5000: 5,000 NUL-terminated !! records"):
            _, git = fake("ignored-5000")
            result = self.run_argv([git, *PINS, "-C", tree1, *STATUS])
            self.assertEqual(result.returncode, 0)
            records = result.stdout.split(b"\0")
            self.assertEqual(records[-1], b"")
            self.assertEqual(len(records) - 1, 5000)
            self.assertTrue(all(r.startswith(b"!! ") for r in records[:-1]))

        with self.subTest("ignore-sigterm: survives TERM, logs its group, dies by KILL"):
            bin_dir, git = fake("ignore-sigterm", lifetime=TIMEOUT)
            child = self.spawn([git, *PINS, "-C", tree1, *STATUS])
            ready = wait_for_event(bin_dir, "ready", child.pid)
            self.assertIsNotNone(ready, fake_events(bin_dir))
            self.assertEqual((ready["pgid"], ready["sid"]), (child.pid, child.pid))
            os.killpg(child.pid, signal.SIGTERM)
            self.assertIsNotNone(wait_for_event(bin_dir, "term", child.pid))
            self.assertIsNone(child.poll(), "TERM must not end it")
            os.killpg(child.pid, signal.SIGKILL)
            self.assertEqual(child.wait(timeout=TIMEOUT), -signal.SIGKILL)
            death = wait_for_event(bin_dir, "death", child.pid)
            self.assertIsNotNone(death, "the death helper outlived the group kill")
            self.assertGreaterEqual(death["t"], wait_for_event(bin_dir, "term", child.pid)["t"])
            self.assertTrue(group_gone(child.pid))
            bin_dir, git = fake("ignore-sigterm", lifetime=0.2)
            child = self.spawn([git, "-C", tree1, *STATUS])
            self.assertEqual(child.wait(timeout=TIMEOUT), 0, "its lifetime is capped")
            self.assertIsNotNone(wait_for_event(bin_dir, "lifetime-ended", child.pid))
            self.assertIsNotNone(wait_for_event(bin_dir, "death", child.pid))
            self.assertEqual(self.run_argv([git, "-C", tree1, *LS_FILES]).returncode, 0)

        with self.subTest("remove-noop, remove-exit and remove-slow"):
            _, noop = fake("remove-noop")
            _, exit5 = fake("remove-exit", status=5)
            _, slow = fake("remove-slow", seconds=0.2)
            listed = self.run_argv([REAL_GIT, "-C", root, "worktree", "list", "--porcelain"]).stdout
            for git, status in ((noop, 0), (exit5, 5)):
                result = self.run_argv([git, *PINS, "-C", root, "worktree", "remove", tree2])
                self.assertEqual(result.returncode, status)
                self.assertTrue(tree2.is_dir())
                self.assertIn(os.fsencode(tree2), listed)
            start = time.monotonic()
            result = self.run_argv([slow, *PINS, "-C", root, "worktree", "remove", tree2])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertGreaterEqual(time.monotonic() - start, 0.2)
            self.assertFalse(tree2.exists())

        for word, rest in (("status", STATUS), ("ls-files", LS_FILES)):
            with self.subTest(f"{word}-fails-in and {word}-hangs-in one worktree path"):
                _, fails = fake(f"{word}-fails-in", path=tree1)
                result = self.run_argv([fails, *PINS, "-C", tree1, *rest])
                self.assertEqual(result.returncode, 128)
                self.assertIn(b"fatal:", result.stderr)
                self.assertEqual(self.run_argv([fails, *PINS, "-C", tree3, *rest]).returncode, 0)
                _, hangs = fake(f"{word}-hangs-in", path=tree1, lifetime=TIMEOUT)
                self.assertEqual(self.run_argv([hangs, *PINS, "-C", tree3, *rest]).returncode, 0)
                self.assert_hangs(self.spawn([hangs, *PINS, "-C", tree1, *rest]))

        with self.subTest("signal-parent-in: the status probe of one path signals project"):
            # The parent stands for project: it records the signals it receives.
            parent = ("import json, signal, subprocess, sys\n"
                      "got = []\n"
                      "for s in (signal.SIGTERM, signal.SIGHUP):\n"
                      "    signal.signal(s, lambda number, frame: got.append(number))\n"
                      "run = subprocess.run(sys.argv[1:], capture_output=True)\n"
                      "print(json.dumps([got, run.returncode, run.stdout.hex()]))\n")
            for name, number in (("TERM", signal.SIGTERM), ("SIGHUP", signal.SIGHUP)):
                _, git = fake("signal-parent-in", path=tree1, signal=name)
                for tree, expected in ((tree1, [int(number)]), (tree3, [])):
                    real = self.run_argv([REAL_GIT, "-C", tree, *STATUS]).stdout
                    result = self.run_argv([sys.executable, "-c", parent, os.fsdecode(git), *PINS,
                                            "-C", os.fsdecode(tree), *STATUS])
                    self.assertEqual(json.loads(result.stdout), [expected, 0, real.hex()],
                                     "the parent got the signal, then the real status ran")

        with self.subTest("slow-after-remove: listings sleep once a removal has run"):
            _, git = fake("slow-after-remove", lifetime=TIMEOUT)
            registry = [git, *PINS, "-C", root, "worktree", "list", "--porcelain", "-z"]
            refs = [git, *PINS, "-C", root, "for-each-ref", "--format=%(refname)", "refs/heads"]
            self.assertEqual(self.run_argv(registry).returncode, 0)
            self.assertEqual(self.run_argv(refs).returncode, 0)
            result = self.run_argv([git, *PINS, "-C", root, "worktree", "remove", tree4])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(tree4.exists())
            self.assert_hangs(self.spawn(registry))
            self.assert_hangs(self.spawn(refs))
            self.assertEqual(self.run_argv([git, "-C", tree1, *STATUS]).returncode, 0)

        with self.subTest("tty-credential: Git prompts at the controlling terminal"):
            bin_dir, git = fake("tty-credential")
            remote = self.base / "remote.git"
            for branch, controlling in (("006-tty", True), ("007-no-tty", False)):
                self.git(tree5, "checkout", "-q", "-b", branch)
                steps = [("Username for 'https://example.invalid': ", "user"),
                         ("Password for 'https://user@example.invalid': ", "secret")] if controlling else []
                before = len(fake_events(bin_dir))
                result = self.run_pty_steps([git, "-C", tree5, "push", "-u", "origin", branch],
                                            steps, controlling_tty=controlling)
                self.assert_status(result, 0)
                [event] = [e for e in fake_events(bin_dir)[before:] if e["event"] == "tty"]
                if controlling:
                    self.assertEqual(event["tty"], "opened")
                    self.assertEqual(event["foreground"], event["pgid"])
                    self.assertEqual((event["fill_status"], event["username"], event["password"]),
                                     (0, "user", "secret"))
                else:
                    self.assertEqual((event["tty"], event["errno"]), ("failed", errno.ENXIO))
                    self.assertNotEqual(event["fill_status"], 0)
                self.assertEqual(self.git(remote, "rev-parse", f"refs/heads/{branch}"),
                                 self.git(tree5, "rev-parse", "HEAD"))

    def test_clean_register_worktrees_writes_valid_rows(self):
        root = self.repo()
        head = self.git(root, "rev-parse", "HEAD").strip()
        trees = self.register_worktrees(257, "row-")
        self.assertEqual(len(trees), 257)
        listing = self.git(root, "worktree", "list", "--porcelain", "-z")
        records = [record.split("\0") for record in listing.split("\0\0") if record]
        self.assertEqual(len(records), 258)
        self.assertEqual(records[0][0], f"worktree {root}")
        rows = {}
        for fields in records[1:]:
            path = fields[0][len("worktree "):]
            rows[path] = fields[1:]
        self.assertEqual(set(rows), {str(tree) for tree in trees})
        for tree in trees:
            self.assertEqual(rows[str(tree)], [f"HEAD {head}", f"branch refs/heads/{tree.name}"],
                             "neither detached, locked nor prunable")
        refs = self.git(root, "for-each-ref", "--format=%(refname) %(objectname)", "refs/heads")
        self.assertEqual(sorted(refs.splitlines()),
                         sorted([f"refs/heads/main {head}"] +
                                [f"refs/heads/{tree.name} {head}" for tree in trees]))
        self.assertEqual(self.git(trees[128], "status", "--porcelain"), "")
        self.assertEqual(self.git(trees[256], "rev-parse", "--show-toplevel").strip(), str(trees[256]))

    def test_clean_pty_runner_gives_a_controlling_terminal(self):
        # A command whose own child, in its process group, opens /dev/tty.
        child = ("import os\n"
                 "try:\n"
                 "    os.close(os.open('/dev/tty', os.O_RDWR)); state = 'opened'\n"
                 "except OSError as exc:\n"
                 "    state = 'errno=%d' % exc.errno\n"
                 "print('CHILD', os.getpgrp(), state, flush=True)\n")
        parent = ("import os, subprocess, sys\n"
                  "print('PARENT', os.getpid(), os.getpgrp(), flush=True)\n"
                  "print('reply?', flush=True)\n"
                  "print('REPLY', sys.stdin.readline().strip(), flush=True)\n"
                  f"subprocess.run([sys.executable, '-c', {child!r}])\n")
        seen = {}
        for controlling in (True, False):
            with self.subTest(controlling_tty=controlling):
                result = self.run_pty_steps([sys.executable, "-c", parent], [("reply?", "ok")],
                                            controlling_tty=controlling)
                self.assert_status(result, 0)
                words = {line.split()[0]: line.split()[1:] for line in result.stdout.splitlines()
                         if line.startswith(("PARENT", "CHILD", "REPLY"))}
                pid, pgid = words["PARENT"]
                self.assertEqual(pid, pgid, "the command leads its own session's group")
                self.assertEqual(words["CHILD"][0], pgid, "the child is in its process group")
                self.assertEqual(words["REPLY"], ["ok"])
                seen[controlling] = words["CHILD"][1]
        self.assertEqual(seen, {True: "opened", False: f"errno={errno.ENXIO}"})

        sleeper = [sys.executable, "-c", "import time\nprint('waiting', flush=True)\ntime.sleep(30)\n"]
        for action in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
            with self.subTest(signal=action.name):
                result = self.run_pty_steps(sleeper, [("waiting", action)])
                self.assertEqual(result.returncode, -action)
        with self.subTest("^C typed at the controlling terminal reaches its foreground group"):
            result = self.run_pty_steps(sleeper, [("waiting", "\x03")], controlling_tty=True)
            self.assertEqual(result.returncode, -signal.SIGINT)
        with self.subTest("a callable step runs while the command waits"):
            calls = []
            result = self.run_pty_steps([sys.executable, "-c", parent],
                                        [("reply?", lambda running: calls.append(running.poll())),
                                         ("", "later")])
            self.assertEqual(calls, [None])
            self.assertIn("REPLY later", result.stdout)

    def test_clean_text_fixtures_equal_the_contract_table(self):
        # Two transcriptions of design.md D14 and D18 and the contract's lines
        # beyond D18 checked against each other (rule 8): clean_support's fixtures
        # and project's TEXT and NEXT_STEPS, key by key, so a failure names its key.
        project = load_project()
        for name, fixtures, table in (("TEXT", TEXT_FIXTURES, project.TEXT),
                                      ("NEXT_STEPS", NEXT_STEP_FIXTURES, project.NEXT_STEPS)):
            self.assertEqual((sorted(set(fixtures) - set(table)), sorted(set(table) - set(fixtures))),
                             ([], []), f"keys only in the fixtures, keys only in {name}")
            for key, line in fixtures.items():
                with self.subTest(table=name, key=key):
                    self.assertEqual(line, table[key])
                    self.assertTrue(line.isascii(), "all new text is ASCII (D18)")
