"""Lane F of feature 004: the child handle, the driver and the runner (T018 to
T021 and T026; design D1 and D2 as lead ruling R-30 amends them; research.md R4,
R5 and R14).

A case that needs a budget, the grace, the reap wait or a signal runs in a child
interpreter that loads `project` as tests/launch_project.py does, through its
prepare(), with the timing table the case names (lead ruling R-29); signals go
only to that child (rule 7). Every timing assertion is a ratio or an ordering,
measured from the child where it says so (R10): the fakes log their own SIGTERM
and death times with time.monotonic(), which every process on the host shares.
"""
import ast
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import textwrap
import threading
import time
from unittest import mock

from clean_support import (
    CLI, REAL_GIT, SCRUBBED_NAMES, TIMEOUT, CleanCase, child_log, fake_events,
    install_counting_git, install_fake_git, load_project, timing_table, transcript,
    wait_for_event,
)

TESTS = Path(__file__).resolve().parent

# The combined status probe of a worktree (design D6), after its -C PATH.
STATUS = ["status", "--porcelain=v1", "-z", "--untracked-files=normal", "--ignored=matching"]

# The seven protocol pins and the five status pins, as the contract writes them
# (contracts/project-clean.md, "Git children").
PINS = ["-c", "protocol.allow=never", "-c", "protocol.file.allow=never",
        "-c", "protocol.ssh.allow=never", "-c", "protocol.git.allow=never",
        "-c", "protocol.http.allow=never", "-c", "protocol.https.allow=never",
        "-c", "protocol.ext.allow=never"]
STATUS_PINS = ["-c", "core.untrackedCache=false", "-c", "core.fsmonitor=false",
               "-c", "core.trustctime=true", "-c", "core.checkStat=default", "-c", "core.ignoreCase=false"]

# The prelude of every child interpreter: project loaded by the launcher's own
# prepare(), its TIMING replaced by the table passed first as --timing=JSON
# (R-29), the case's arguments second, and emit() for the one result line.
PRELUDE = """\
import json, os, signal, sys, threading, time
import launch_project
project, _ = launch_project.prepare(sys.argv[1:2])
ARGS = json.loads(sys.argv[2])
TABLE = project.TIMING


def emit(**fields):
    print("RESULT " + json.dumps(fields), flush=True)


def group_alive(pgid):
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    return True


def status_spec(path):
    return ("status", ["-C", path, "status", "--porcelain=v1", "-z",
                       "--untracked-files=normal", "--ignored=matching"], None)
"""


def group_gone(pgid):
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return True
    return False


def first_event(events, name, pid):
    return next((entry for entry in events if entry["event"] == name and entry["pid"] == pid), None)


def sigint_default():
    """preexec_fn of run_child() when this process ignores SIGINT, as a `&` job
    of a non-interactive shell does: the child interpreter starts with SIGINT
    at SIG_DFL, as a foreground run starts it, since project leaves a signal
    ignored on entry ignored (lead ruling R-101 (b))."""
    signal.signal(signal.SIGINT, signal.SIG_DFL)


class RunnerTests(CleanCase):
    def setUp(self):
        super().setUp()
        self.project = load_project()
        # Whatever a case leaves live in the shared module is stopped, so that
        # LIVE_PROBES is empty for the next module's comparisons.
        self.addCleanup(self.project.kill_live_probes)

    # Helpers.

    def run_child(self, table, body, env=None, **args):
        """Run body after PRELUDE in a child interpreter with table as its TIMING;
        returns the fields of its one RESULT line and the run."""
        argv = [sys.executable, "-c", PRELUDE + textwrap.dedent(body),
                "--timing=" + json.dumps(table), json.dumps(args)]
        env = dict(self.env if env is None else env)
        env["PYTHONPATH"] = str(TESTS)
        reset = sigint_default if signal.getsignal(signal.SIGINT) == signal.SIG_IGN else None
        try:
            result = subprocess.run(argv, cwd=self.base, env=env, capture_output=True, text=True,
                                    timeout=TIMEOUT, preexec_fn=reset)
        except subprocess.TimeoutExpired as exc:
            self.fail(f"child interpreter passed {TIMEOUT} s\n{exc.stdout}\n{exc.stderr}")
        lines = [line for line in result.stdout.splitlines() if line.startswith("RESULT ")]
        if result.returncode != 0 or len(lines) != 1:
            self.fail("child interpreter failed\n" + transcript(result))
        return json.loads(lines[0][len("RESULT "):]), result

    def worktree(self, dirty=True):
        """A repository with one commit, an untracked file when dirty, and an
        ignored file; the real git builds it."""
        repo = self.repo()
        (repo / ".gitignore").write_text("*.log\n")
        self.commit(repo)
        (repo / "kept.log").write_text("ignored")
        if dirty:
            (repo / "new.txt").write_text("untracked")
        return repo

    def fake_dir(self, kind, **options):
        directory = self.base / f"fake-{kind}"
        install_fake_git(directory, kind, **options)
        return directory

    def env_with(self, bin_dir=None, **extra):
        env = self.path_first(bin_dir) if bin_dir is not None else dict(self.env)
        env.update(extra)
        return env

    def in_process_env(self, bin_dir=None, **extra):
        """This process's environment replaced by self.env, bin_dir first on PATH,
        for in-process children (restored on exit)."""
        return mock.patch.dict(os.environ, self.env_with(bin_dir, **extra), clear=True)

    def stop(self, handle):
        """Drive a handle to its end, as a driver would."""
        handle.terminate_group()
        while not handle.advance(time.monotonic()):
            time.sleep(0.01)
        handle.close()

    def blocked_fds(self, proc, deadline):
        """The sorted descriptor names of the process whose /proc directory is
        proc, listed while it is blocked: state S, with the same context-switch
        counts in its status before and after the listing, so that it did not
        run while it was listed; and two such listings in a row agree (lead
        ruling R-81 (c)). A process still starting, its dynamic loader or
        setlocale holding fd 3 open, is running (R) or in a disk read (D),
        never asleep (S), though `comm` already names the new program."""
        def blocked_state():
            fields = dict(line.split(":", 1) for line in (proc / "status").read_text().splitlines())
            return (fields["State"].split()[0], fields["voluntary_ctxt_switches"].strip(),
                    fields["nonvoluntary_ctxt_switches"].strip())
        last = None
        while True:
            before = blocked_state()
            fds = sorted(os.listdir(proc / "fd"))
            after = blocked_state()
            if before[0] == "S" and before == after:
                if fds == last:
                    return fds
                last = fds
            else:
                last = None
            self.assertLess(time.monotonic(), deadline, f"the child never blocked: {after}, fds {fds}")
            time.sleep(0.01)

    # T018.

    def test_clean_child_handle_runs_in_its_own_group(self):
        project = self.project
        repo = self.worktree()
        fake = self.fake_dir("status-hangs-in", path=str(repo), lifetime=15)
        log = self.base / "children.log"
        bin_dir = self.base / "bin"
        install_counting_git(bin_dir, log, real=fake / "git")
        caller = {name: str(self.base / "elsewhere") for name in SCRUBBED_NAMES}
        inherited_r, inherited_w = os.pipe()
        os.set_inheritable(inherited_r, True)
        self.addCleanup(os.close, inherited_r)
        self.addCleanup(os.close, inherited_w)
        expected_locks = {"probe": "0", "status": "0", "hidden": "0", "removal": None, "delegate": None}
        with self.in_process_env(bin_dir, **caller):
            for kind, locks in expected_locks.items():
                with self.subTest(kind=kind):
                    handle = project.ChildHandle.start(project.git_argv(kind, ["-C", str(repo), "status"]),
                                                       None, kind)
                    self.addCleanup(lambda handle=handle: None if handle.finished else self.stop(handle))
                    deadline = time.monotonic() + TIMEOUT / 2
                    while not [r for r in child_log(log) if r.pid == handle.pid]:
                        self.assertLess(time.monotonic(), deadline, "the wrapper never recorded the child")
                        time.sleep(0.01)
                    record = next(r for r in child_log(log) if r.pid == handle.pid)
                    # Its own session and process group, a child of this process.
                    self.assertEqual((record.pgid, record.ppid), (handle.pid, os.getpid()))
                    self.assertEqual(os.getsid(handle.pid), handle.pid)
                    self.assertEqual(os.getpgid(handle.pid), handle.pid)
                    # git_env(kind): none of the thirty-one names, and GIT_OPTIONAL_LOCKS=0
                    # for the read-only kinds only.
                    self.assertEqual([n for n in record.names if n in SCRUBBED_NAMES], [])
                    self.assertEqual(record.optional_locks, locks)
                    self.assertEqual(record.argv, project.git_argv(kind, ["-C", str(repo), "status"])[1:])
                    self.assertIs(handle in project.LIVE_PROBES, locks is not None)
                    proc = Path(f"/proc/{handle.pid}")
                    if proc.is_dir():  # Linux; macOS, where no CI job runs, has no /proc (R-35)
                        # Standard input from /dev/null, and only the three standard
                        # descriptors once the fake has exec'd sleep (close_fds): the
                        # inheritable pipe of this process is not among them. `comm`
                        # reads `sleep` from the exec on, while sleep's own start-up
                        # still opens and closes files at fd 3, so the descriptors
                        # are listed once sleep is blocked in its sleep (R-81 (c)).
                        while (proc / "comm").read_text().strip() != "sleep":
                            self.assertLess(time.monotonic(), deadline, "the fake never reached sleep")
                            time.sleep(0.01)
                        fds = self.blocked_fds(proc, deadline)
                        self.assertEqual(os.readlink(proc / "fd" / "0"), os.devnull)
                        self.assertEqual(fds, ["0", "1", "2"])
                    self.stop(handle)
                    self.assertEqual(handle.state, "reaped")
                    self.assertNotIn(handle, project.LIVE_PROBES)
                    self.assertTrue(group_gone(handle.pid))
        self.assertEqual(len(child_log(log)), len(expected_locks))

    def test_clean_driver_outcomes(self):
        project = self.project
        repo = self.worktree()
        status = ["-C", str(repo), *STATUS]
        # Each outcome's row error (plan review M17).
        self.assertEqual(project.OUTCOME_ERRORS, {
            "complete": None, "complete-at-bound": None, "failed": "probe-failed",
            "timeout": "probe-timeout", "deadline": "deadline-exceeded"})

        with self.in_process_env():
            run = project.Invocation("status")
            # complete: a real status probe, its records parsed.
            outcome = project.run_bounded(("status", status, None), project.StatusParser(), run)
            self.assertEqual((outcome.name, outcome.error, outcome.status), ("complete", None, 0))
            self.assertEqual((outcome.result["dirty"], outcome.result["ignored_files"]), (True, 1))
            # failed: a nonzero exit, with the head of standard error.
            missing = self.base / "missing"
            outcome = project.run_bounded(("probe", ["-C", str(missing), "status"], None), None, run)
            self.assertEqual((outcome.name, outcome.error, outcome.status), ("failed", "probe-failed", 128))
            self.assertTrue(outcome.stderr.startswith(b"fatal:"), outcome.stderr)
            # failed: a truncated last record (ParseError from finish()), exit 0.
            outcome = project.run_bounded(("probe", ["-C", str(repo), "rev-parse", "HEAD"], None),
                                          project.StatusParser(), run)
            self.assertEqual((outcome.name, outcome.error, outcome.status), ("failed", "probe-failed", 0))
            self.assertIn("truncated", outcome.detail)
            # failed: a malformed record, exit 0.
            outcome = project.run_bounded(("probe", ["-C", str(repo), "for-each-ref"], None),
                                          project.RefParser(), run)
            self.assertEqual((outcome.name, outcome.error), ("failed", "probe-failed"))
            self.assertIsNone(outcome.result)
            self.assertEqual(run.probes, 4)
        # failed: no git to spawn.
        with self.in_process_env(PATH=self.path_without_git()):
            outcome = project.run_bounded(("probe", ["--version"], None), None, run)
            self.assertEqual((outcome.name, outcome.error, outcome.status), ("failed", "probe-failed", None))
            self.assertEqual(run.probes, 4, "a child never spawned is not counted")
        # complete-at-bound on the ignored-5000 fake, its child stopped by SIGTERM.
        with self.in_process_env(self.fake_dir("ignored-5000")):
            outcome = project.run_bounded(("status", status, None), project.StatusParser(), run)
            self.assertEqual((outcome.name, outcome.error), ("complete-at-bound", None))
            self.assertEqual((outcome.result["ignored_files"], outcome.result["ignored_files_truncated"]),
                             (64, True))
            self.assertEqual(outcome.status, -signal.SIGTERM, "the child was stopped at the bound")
            self.assertTrue(group_gone(outcome.pid))
        self.assertEqual(self.project.LIVE_PROBES, set())

        # timeout on the ignore-sigterm fake. Table: the real one with the 15 s
        # inspect budget at 1 s (the probe budget it yields here, outside clean),
        # the grace at 0.5 s and the reap wait at 2 s.
        grace = 0.5
        table = timing_table(inspect_budget=1, term_grace=grace, reap_wait=2)
        fake = self.fake_dir("ignore-sigterm", lifetime=15)
        fields, _ = self.run_child(table, """
            run = project.Invocation("status")
            outcome = project.run_bounded(status_spec(ARGS["repo"]), project.StatusParser(), run)
            emit(name=outcome.name, error=outcome.error, status=outcome.status, pid=outcome.pid,
                 budget=run.child_budget("probe")[0], live=len(project.LIVE_PROBES))
        """, env=self.env_with(fake), repo=str(repo))
        self.assertEqual(fields["budget"], 1.0)
        self.assertEqual((fields["name"], fields["error"]), ("timeout", "probe-timeout"))
        self.assertEqual((fields["status"], fields["live"]), (-signal.SIGKILL, 0), "reaped, out of the registry")
        pid = fields["pid"]
        death = wait_for_event(fake, "death", pid)
        term = first_event(fake_events(fake), "term", pid)
        self.assertIsNotNone(term, "the child got SIGTERM")
        self.assertIsNotNone(death, "the child died")
        self.assertGreaterEqual(death["t"] - term["t"], 0.9 * grace, "SIGKILL came at least 0.9 graces after SIGTERM")
        self.assertTrue(group_gone(pid), "no process of its group remains")

        # An abandoned handle: a child whose exit is never observed (as one stuck in
        # the kernel) is abandoned at its reap deadline, records probe-timeout, stays
        # registered, is never polled again, and is killed again on exit; the
        # driver's outcome for it is timeout with no exit status. Table: the 15 s
        # inspect budget at 0.5 s (the probe budget here), grace 0.2 s, reap wait
        # 0.3 s.
        fields, _ = self.run_child(timing_table(inspect_budget=0.5, term_grace=0.2, reap_wait=0.3), """
            polls = []
            real_start = project.ChildHandle.start.__func__

            def start(cls, argv, cwd, kind):
                handle = real_start(cls, argv, cwd, kind)
                handle.real_poll = handle.process.poll
                handle.process.poll = lambda: polls.append(1)
                handle.process.wait = lambda timeout=None: time.sleep(timeout or 0)
                return handle

            project.ChildHandle.start = classmethod(start)
            spec = ("status", ["-C", ARGS["repo"], "status"], None)
            handle = project.ChildHandle.start(project.git_argv(*spec[:2]), None, "status")
            handle.terminate_group()
            while not handle.advance(time.monotonic()):
                time.sleep(0.01)
            seen = len(polls)
            handle.reap()
            handle.advance(time.monotonic() + 10)
            again = len(polls) - seen
            registered = handle in project.LIVE_PROBES
            kills = []
            real_killpg = os.killpg
            os.killpg = lambda pgid, signum: (kills.append((pgid, int(signum))), real_killpg(pgid, signum))
            project.kill_live_probes()
            os.killpg = real_killpg
            outcome = project.run_bounded(status_spec(ARGS["repo"]), project.StatusParser(),
                                          project.Invocation("status"))
            emit(state=handle.state, error=handle.error, registered=registered, again=again,
                 kills=[k for k in kills if k[0] == handle.pid], pid=handle.pid,
                 outcome=[outcome.name, outcome.error, outcome.status])
        """, env=self.env_with(self.fake_dir("status-hangs-in", path=str(repo), lifetime=15)),
            repo=str(repo))
        self.assertEqual((fields["state"], fields["error"], fields["registered"]),
                         ("abandoned", "probe-timeout", True))
        self.assertEqual(fields["again"], 0, "never polled again once abandoned")
        self.assertEqual(fields["kills"], [[fields["pid"], int(signal.SIGKILL)]], "killed again on exit")
        self.assertEqual(fields["outcome"], ["timeout", "probe-timeout", None])

        # deadline: under clean, the work deadline is the limit. Table: deadline
        # 1.5 s and reserve 0.5 s, so 1 s of work; the probe budget stays 5 s, and the
        # first child's budget is the work left, about 1 s. A second child finds no
        # time left and is never spawned.
        table = timing_table(invocation_deadline=1.5, reconciliation_reserve=0.5, term_grace=0.3)
        fields, _ = self.run_child(table, """
            run = project.Invocation("clean")
            budget, limit = run.child_budget("probe")
            first = project.run_bounded(status_spec(ARGS["repo"]), project.StatusParser(), run)
            second = project.run_bounded(status_spec(ARGS["repo"]), project.StatusParser(), run)
            emit(budget=budget, limit=limit, probe_budget=TABLE["probe_budget"],
                 first=[first.name, first.error, first.pid is not None],
                 second=[second.name, second.error, second.pid], probes=run.probes)
        """, env=self.env_with(self.fake_dir("status-hangs-in", path=str(repo), lifetime=15)),
            repo=str(repo))
        self.assertEqual((fields["limit"], fields["probe_budget"]), ("deadline", 5.0))
        self.assertLess(fields["budget"], 0.25 * fields["probe_budget"])
        self.assertEqual(fields["first"], ["deadline", "deadline-exceeded", True])
        self.assertEqual(fields["second"], ["deadline", "deadline-exceeded", None])
        self.assertEqual(fields["probes"], 1)

        # interrupted: the signal-parent-in fake sends a signal to its parent, the
        # child interpreter, then runs the real status. While planning the driver
        # stops the child and raises Interrupted, for each of the three signals; in
        # the apply phase the child runs on; while reconciling the first signal is
        # only recorded and a second SIGINT interrupts. Table: the real one.
        for number in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            with self.subTest(signal=number.name):
                fake = self.fake_dir("signal-parent-in", path=str(repo), signal=number.name)
                fields, _ = self.run_child(timing_table(), """
                    results = {}
                    for phase in ("planning", "apply", "reconciling"):
                        with project.signal_scope() as scope:
                            run = scope.invocation
                            run.phase = phase
                            try:
                                outcome = project.run_bounded(status_spec(ARGS["repo"]),
                                                              project.StatusParser(), run)
                                results[phase] = [outcome.name, run.signal]
                            except project.Interrupted as exc:
                                results[phase] = ["interrupted", exc.signum, run.signal]
                            if phase == "reconciling":
                                try:
                                    project.run_bounded(status_spec(ARGS["repo"]), project.StatusParser(), run)
                                    results["second"] = ["returned", run.second_interrupt]
                                except project.Interrupted as exc:
                                    results["second"] = ["interrupted", exc.signum, run.second_interrupt]
                            if phase == "planning":
                                probes = run.probes
                                try:
                                    project.run_bounded(status_spec(ARGS["repo"]), project.StatusParser(), run)
                                    results["after"] = "returned"
                                except project.Interrupted:
                                    results["after"] = ["interrupted", run.probes - probes]
                    emit(results=results, live=len(project.LIVE_PROBES))
                """, env=self.env_with(fake), repo=str(repo))
                results = fields["results"]
                self.assertEqual(results["planning"], ["interrupted", number, number])
                self.assertEqual(results["after"], ["interrupted", 0], "a set slot spawns nothing more")
                self.assertEqual(results["apply"], ["complete", number])
                self.assertEqual(results["reconciling"], ["complete", number])
                expected = (["interrupted", number, True] if number == signal.SIGINT else ["returned", False])
                self.assertEqual(results["second"], expected)
                self.assertEqual(fields["live"], 0)

    def test_clean_termination_never_blocks(self):
        # Table: grace 0.6 s and reap wait 1 s; no probe budget is used here.
        grace = 0.6
        table = timing_table(term_grace=grace, reap_wait=1)
        fake = self.fake_dir("ignore-sigterm", lifetime=15)
        repo = self.worktree()
        fields, _ = self.run_child(table, """
            def ready(pid):
                end = time.monotonic() + 10
                while time.monotonic() < end:
                    with open(ARGS["events"], "a+") as events:
                        events.seek(0)
                        if any(json.loads(line).get("event") == "ready" and json.loads(line)["pid"] == pid
                               for line in events.read().splitlines() if line):
                            return True
                    time.sleep(0.01)
                return False

            spec = status_spec(ARGS["repo"])
            handle = project.ChildHandle.start(project.git_argv(*spec[:2]), None, "status")
            assert ready(handle.pid)
            start = time.monotonic()
            handle.terminate_group()
            returned = time.monotonic() - start
            state = handle.state
            # No advance() for 1.5 graces: nothing sends SIGKILL in the meantime.
            time.sleep(1.5 * TABLE["term_grace"])
            alive = group_alive(handle.pid) and handle.state == "terminating"
            states = []
            while not handle.advance(time.monotonic()):
                states.append(handle.state)
                time.sleep(0.01)
            states.append(handle.state)

            # Three at once through kill_live_probes(): their graces run side by side.
            others = [project.ChildHandle.start(project.git_argv(*spec[:2]), None, "status")
                      for _ in range(3)]
            assert all(ready(other.pid) for other in others)
            start = time.monotonic()
            project.kill_live_probes()
            together = time.monotonic() - start
            emit(returned=returned, state=state, alive=alive, states=states, pid=handle.pid,
                 others=[other.pid for other in others], other_states=[o.state for o in others],
                 together=together, live=len(project.LIVE_PROBES))
        """, env=self.env_with(fake), repo=str(repo), events=str(fake / "fake-events.jsonl"))
        self.assertLess(fields["returned"], grace / 10, "terminate_group() returns at once")
        self.assertEqual(fields["state"], "terminating")
        self.assertTrue(fields["alive"], "SIGKILL waits for advance()")
        # The first advance() past the grace sends SIGKILL (and may already reap);
        # the reap is observed only through advance().
        self.assertIn(fields["states"][0], ("killing", "reaped"))
        self.assertEqual(fields["states"][-1], "reaped")
        pid = fields["pid"]
        death = wait_for_event(fake, "death", pid)
        term = first_event(fake_events(fake), "term", pid)
        self.assertGreaterEqual(death["t"] - term["t"], 1.4 * grace, "killed only once advance() ran")
        # kill_live_probes(): each child killed at least 0.9 graces after its own
        # SIGTERM, the three side by side: the whole stop well under two graces,
        # where graces stacked one per handle would take three.
        self.assertEqual(fields["other_states"], ["reaped"] * 3)
        self.assertEqual(fields["live"], 0)
        self.assertLess(fields["together"], 2 * grace)
        for other in fields["others"]:
            death = wait_for_event(fake, "death", other)
            term = first_event(fake_events(fake), "term", other)
            self.assertGreaterEqual(death["t"] - term["t"], 0.9 * grace)
            self.assertTrue(group_gone(other))

    def test_clean_a_flooding_child_never_times_out(self):
        # More than the 64 KiB a pipe holds goes to standard error before any
        # record: drained while standard output is read, the probe completes. The
        # real table (5 s and 15 s budgets) applies; the run takes far less.
        project = self.project
        repo = self.worktree()
        with self.in_process_env():
            plain = project.run_bounded(("status", ["-C", str(repo), *STATUS], None),
                                        project.StatusParser(), project.Invocation("status"))
        for kib in (70, 1024):
            with self.subTest(kib=kib), self.in_process_env(self.fake_dir("flood-stderr", kib=kib)):
                outcome = project.run_bounded(("status", ["-C", str(repo), *STATUS], None),
                                              project.StatusParser(), project.Invocation("clean"))
                self.assertEqual((outcome.name, outcome.error, outcome.status), ("complete", None, 0))
                self.assertEqual(outcome.result, plain.result)
                self.assertEqual(outcome.stderr, b"E" * 4096, "a head of exactly 4,096 bytes")
                self.assertEqual(outcome.stderr_bytes, kib * 1024, "and the rest counted")

    def test_clean_reaping_uses_popen_only(self):
        # Lead ruling R-40: by `ast` over project, no raw reaper by name or
        # attribute anywhere (os.waitid, the fourth, is held to the same rule);
        # reaping goes through Popen.poll() and Popen.wait(timeout) (R14). A
        # runtime patch of os.waitpid cannot show it, since Popen calls it.
        tree = ast.parse(CLI.read_text(encoding="utf-8"), str(CLI))
        banned = {"waitpid", "wait3", "wait4", "waitid"}
        found = sorted({(node.lineno, getattr(node, "id", None) or getattr(node, "attr", None)
                         or getattr(node, "name", None))
                        for node in ast.walk(tree)
                        if (isinstance(node, ast.Name) and node.id in banned)
                        or (isinstance(node, ast.Attribute) and node.attr in banned)
                        or (isinstance(node, ast.alias) and node.name.split(".")[-1] in banned)})
        self.assertEqual(found, [], "project never reaps behind Popen's back")
        handle = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "ChildHandle")
        calls = {node.func.attr for node in ast.walk(handle)
                 if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}
        self.assertIn("poll", calls)

    # T019.

    def test_clean_signal_scopes(self):
        project = self.project
        self.assertTrue(issubclass(project.Interrupted, BaseException))
        self.assertTrue(issubclass(project.Terminated, BaseException))
        self.assertFalse(issubclass(project.Interrupted, Exception))
        self.assertFalse(issubclass(project.Terminated, Exception))
        # Table: grace 0.3 s and reap wait 1 s, for the probes a scope stops.
        fake = self.fake_dir("ignore-sigterm", lifetime=15)
        repo = self.worktree()
        fields, result = self.run_child(timing_table(term_grace=0.3, reap_wait=1), """
            SIGNALS = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)

            def handlers():
                return [signal.getsignal(number) for number in SIGNALS]

            def wakeup():
                fd = signal.set_wakeup_fd(-1)
                signal.set_wakeup_fd(fd, warn_on_full_buffer=False)
                return fd

            start = (handlers(), wakeup())
            out = {}
            with project.signal_scope() as scope:
                fd = wakeup()
                out["installed"] = all(callable(h) and h not in start[0] for h in handlers())
                out["wakeup"] = [fd != start[1], not os.get_blocking(fd), not os.get_blocking(scope.wake)]
                out["bound"] = project.current_invocation() is scope.invocation
                for number in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
                    os.kill(os.getpid(), number)
                    time.sleep(0.01)
                out["slot"] = [scope.invocation.signal, scope.invocation.second_interrupt]
                out["woken"] = len(os.read(scope.wake, 64)) > 0
                with project.default_signals():
                    out["default"] = (handlers(), wakeup()) == start
                out["default_back"] = handlers() != start[0] and wakeup() == fd
            out["restored"] = (handlers(), wakeup()) == start
            # A full wakeup pipe: with warn_on_full_buffer=False a signal leaves
            # standard error quiet. The scope's own write end is filled (its
            # private _pipe), since reading the descriptor back would reset the flag.
            with project.signal_scope() as scope:
                for size in (4096, 1):
                    try:
                        while True:
                            os.write(scope._pipe[1], b"x" * size)
                    except BlockingIOError:
                        pass
                os.kill(os.getpid(), signal.SIGTERM)
                time.sleep(0.05)
            with project.signal_scope():
                inside = handlers()
                with project.raising_signals():
                    out["raising_installed"] = all(h not in inside and h not in start[0] for h in handlers())
                out["raising_back"] = handlers() == inside

            for error in (ValueError("boom"), KeyboardInterrupt(), SystemExit(3)):
                try:
                    with project.signal_scope():
                        handles = [project.ChildHandle.start(project.git_argv(*status_spec(ARGS["repo"])[:2]),
                                                             None, "status") for _ in range(2)]
                        time.sleep(0.3)
                        raise error
                except BaseException:
                    pass
                out[type(error).__name__] = [(handlers(), wakeup()) == start,
                                             [h.state for h in handles],
                                             [group_alive(h.pid) for h in handles],
                                             len(project.LIVE_PROBES)]

            for number in SIGNALS:
                with project.Invocation() as run:
                    try:
                        with project.raising_signals():
                            os.kill(os.getpid(), number)
                            time.sleep(5)
                        got = ["none"]
                    except KeyboardInterrupt:
                        got = ["KeyboardInterrupt"]
                    except project.Terminated as exc:
                        got = ["Terminated", exc.signum]
                    out["raise_" + signal.Signals(number).name] = got + [run.signal,
                                                                          handlers() == start[0]]
            with project.Invocation() as run:
                run.record_signal(signal.SIGHUP)
                try:
                    with project.raising_signals():
                        got = ["entered"]
                except project.Terminated as exc:
                    got = ["Terminated", exc.signum]
                out["raise_preset"] = got + [handlers() == start[0]]

            # A signal ignored on entry stays ignored in every scope, which
            # neither records it nor restores anything for it, while the other
            # two get the scope's handlers (lead ruling R-101 (b)).
            for number in (signal.SIGHUP, signal.SIGINT):
                entry = signal.signal(number, signal.SIG_IGN)
                ignored = []
                with project.signal_scope() as scope:
                    ignored.append(signal.getsignal(number))
                    others = all(callable(signal.getsignal(other)) for other in SIGNALS if other != number)
                    os.kill(os.getpid(), number)
                    time.sleep(0.01)
                    with project.raising_signals():
                        ignored.append(signal.getsignal(number))
                        os.kill(os.getpid(), number)
                        time.sleep(0.01)
                    with project.default_signals():
                        ignored.append(signal.getsignal(number))
                    ignored.append(signal.getsignal(number))
                    slot = scope.invocation.signal
                ignored.append(signal.getsignal(number))
                signal.signal(number, entry)
                out["ignored_" + signal.Signals(number).name] = [
                    [handler == signal.SIG_IGN for handler in ignored], others, slot]
            emit(**out)
        """, env=self.env_with(fake), repo=str(repo))
        self.assertTrue(fields["installed"], "record-only handlers for SIGINT, SIGTERM and SIGHUP")
        self.assertEqual(fields["wakeup"], [True, True, True], "a non-blocking wakeup descriptor")
        self.assertTrue(fields["bound"])
        self.assertEqual(fields["slot"], [signal.SIGTERM, False], "only the first signal is kept")
        self.assertTrue(fields["woken"])
        self.assertNotIn("wakeup", result.stderr, "warn_on_full_buffer=False")
        self.assertTrue(fields["default"], "default_signals() restores what the process started with")
        self.assertTrue(fields["default_back"])
        self.assertTrue(fields["raising_installed"])
        self.assertTrue(fields["raising_back"], "raising_signals() restores the record-only handlers")
        self.assertTrue(fields["restored"])
        for name in ("ValueError", "KeyboardInterrupt", "SystemExit"):
            with self.subTest(exception=name):
                self.assertEqual(fields[name], [True, ["reaped", "reaped"], [False, False], 0],
                                 "handlers restored and every live probe group killed and reaped")
        self.assertEqual(fields["raise_SIGINT"], ["KeyboardInterrupt", signal.SIGINT, True])
        self.assertEqual(fields["raise_SIGTERM"], ["Terminated", signal.SIGTERM, signal.SIGTERM, True])
        self.assertEqual(fields["raise_SIGHUP"], ["Terminated", signal.SIGHUP, signal.SIGHUP, True])
        self.assertEqual(fields["raise_preset"], ["Terminated", signal.SIGHUP, True], "lead ruling R-47")
        for name in ("SIGHUP", "SIGINT"):
            with self.subTest(ignored_on_entry=name):
                self.assertEqual(fields["ignored_" + name], [[True] * 5, True, None],
                                 "ignored in signal_scope, raising_signals, default_signals and after; "
                                 "the other two installed; nothing recorded (lead ruling R-101 (b))")

    # T020.

    def test_clean_filesystem_calls_are_bounded(self):
        project = self.project
        path = self.base / "present"
        path.write_text("x")
        self.assertEqual(project.fs_call(os.lstat, path, budget=5), os.lstat(path))
        with self.assertRaises(FileNotFoundError):
            project.fs_call(os.lstat, self.base / "absent", budget=5)
        blocker = threading.Event()
        self.addCleanup(blocker.set)
        for run, budget, name in ((project.Invocation("status"), 0.2, "timeout"),
                                  (project.Invocation("clean"), None, "deadline")):
            with self.subTest(outcome=name), run:
                if budget is None:
                    run.work_end = time.monotonic() + 0.2  # the work deadline is the limit
                before = {thread.ident for thread in threading.enumerate()}
                start = time.monotonic()
                outcome = project.fs_call(blocker.wait, budget=budget)
                elapsed = time.monotonic() - start
                self.assertIsInstance(outcome, project.DriverOutcome)
                self.assertEqual(outcome.name, name)
                self.assertEqual(outcome.error, project.OUTCOME_ERRORS[name])
                self.assertGreaterEqual(elapsed, 0.9 * 0.2)
                self.assertLess(elapsed, 0.2 + 2)
                stuck = [thread for thread in threading.enumerate() if thread.ident not in before]
                self.assertEqual(len(stuck), 1, "the call's thread stays blocked")
                self.assertTrue(stuck[0].daemon and stuck[0].is_alive())
        self.assertEqual(project.Invocation("status").child_budget("probe"), (15, "timeout"))
        # Never a concurrent.futures pool.
        tree = ast.parse(CLI.read_text(encoding="utf-8"))
        names = {alias.name for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))
                 for alias in node.names} | {node.module for node in ast.walk(tree)
                                             if isinstance(node, ast.ImportFrom)}
        self.assertFalse({name for name in names if name and name.startswith("concurrent")})
        self.assertNotIn("ThreadPoolExecutor", {node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)})

    def test_clean_git_version_check(self):
        fakes = {
            "apple": 'echo "git version 2.39.3 (Apple Git-146)"',
            "exit": "exit 3",
            "hang": "exec sleep 15",
            "garbage": "echo hello",
        }
        dirs = {}
        for name, action in fakes.items():
            directory = self.base / f"version-{name}"
            directory.mkdir()
            git = directory / "git"
            git.write_text(f'#!/bin/sh\ncase " $* " in *" --version "*) {action};; esac\nexec "{REAL_GIT}" "$@"\n')
            git.chmod(0o755)
            dirs[name] = str(directory)
        dirs["old"] = str(self.fake_dir("version-2.35.0"))
        log = self.base / "version.log"
        install_counting_git(self.base / "counting", log)
        dirs["real"] = str(self.base / "counting")
        # Table: the 15 s budget outside clean at 0.5 s, so the hanging fake times
        # out; grace 0.2 s.
        fields, _ = self.run_child(timing_table(inspect_budget=0.5, term_grace=0.2), """
            out = {}
            base = os.environ["PATH"]
            for name, directory in ARGS["dirs"].items():
                os.environ["PATH"] = directory + os.pathsep + base
                run = project.Invocation("status")
                result = project.git_version(run)
                again = project.git_version(run)
                out[name] = [result.code, result.version, result.text, result.detail,
                             again is result, run.probes]
            os.environ["PATH"] = ARGS["none"]
            run = project.Invocation()
            result = project.git_version(run)
            out["none"] = [result.code, result.version, result.text, result.detail, True, run.probes]
            os.environ["PATH"] = ARGS["dirs"]["real"] + os.pathsep + base
            project.git_version(project.Invocation())
            emit(**out)
        """, dirs=dirs, none=self.path_without_git())
        real = subprocess.run([REAL_GIT, "--version"], capture_output=True, text=True).stdout.strip()
        text = real[len("git version "):]
        numbers = [int(part) for part in text.split(" ")[0].split(".")[:3]]
        self.assertEqual(fields["real"], [None, numbers + [0] * (3 - len(numbers)), text, None, True, 1])
        self.assertEqual(fields["apple"], [None, [2, 39, 3], "2.39.3 (Apple Git-146)", None, True, 1])
        self.assertEqual(fields["old"], ["git-too-old", [2, 35, 0], "2.35.0", None, True, 1])
        self.assertEqual(fields["none"], ["git-unavailable", None, None, "not found", True, 0])
        self.assertEqual(fields["exit"], ["git-unavailable", None, None, "exit 3", True, 1])
        self.assertEqual(fields["hang"], ["git-unavailable", None, None, "timed out", True, 1])
        self.assertEqual(fields["garbage"], ["git-unavailable", None, None, "unparseable version", True, 1])
        # One child per invocation, scrubbed and pinned: two checks in one
        # invocation and one in another make two children.
        records = child_log(log)
        self.assertEqual(len(records), 2)
        for record in records:
            self.assertEqual(record.argv, [*PINS, "--version"])
            self.assertEqual(record.optional_locks, "0")

    def test_clean_invocation_holds_the_per_run_state(self):
        project = self.project
        table = project.TIMING
        clean, other = project.Invocation("clean"), project.Invocation("status")
        # The per-child budget: 5 s under clean, 15 s otherwise, and outside any
        # invocation (plan review M10).
        self.assertEqual(clean.child_budget("probe"), (table["probe_budget"], "timeout"))
        self.assertEqual(other.child_budget("status"), (table["inspect_budget"], "timeout"))
        self.assertEqual(project.current_invocation().child_budget("probe"), (table["inspect_budget"], "timeout"))
        self.assertEqual(clean.child_budget("removal"), (None, "timeout"))
        self.assertEqual(clean.child_budget("delegate"), (None, "timeout"))
        # The clock: under clean, work ends at the deadline less the reserve.
        self.assertAlmostEqual(clean.work_end - clean.started,
                               table["invocation_deadline"] - table["reconciliation_reserve"], places=6)
        self.assertAlmostEqual(clean.reserve_end - clean.started, table["invocation_deadline"], places=6)
        self.assertEqual((other.work_end, other.reserve_end, other.work_remaining()), (None, None, None))
        # Paused while a question waits: the clock stands still and both
        # deadlines move later by the time waited.
        work_end, reserve_end = clean.work_end, clean.reserve_end
        clean.pause()
        held = clean.now()
        time.sleep(0.2)
        self.assertEqual(clean.now(), held)
        clean.resume()
        self.assertGreaterEqual(clean.work_end - work_end, 0.9 * 0.2)
        self.assertAlmostEqual(clean.work_end - work_end, clean.reserve_end - reserve_end, places=6)
        # While reconciling, the reserve is the limit.
        clean.phase = "reconciling"
        clean.reserve_end = clean.now() + 1
        budget, limit = clean.child_budget("probe")
        self.assertEqual(limit, "deadline")
        self.assertLessEqual(budget, 1)
        # TIMING is read when an invocation is made, not at import (R-29).
        with mock.patch.object(project, "TIMING", {**table, "invocation_deadline": 7, "reconciliation_reserve": 2}):
            late = project.Invocation("clean")
        self.assertAlmostEqual(late.work_end - late.started, 5, places=6)
        # The counters: a removal in operations, every other child in probes.
        repo = self.worktree()
        with self.in_process_env():
            for kind in ("probe", "status", "hidden", "delegate", "removal"):
                outcome = project.run_bounded((kind, ["-C", str(repo), "status"], None), None, other)
                self.assertEqual(outcome.name, "complete", outcome)
            # The memos: the version check's result, and the common-directory memos.
            version = project.git_version(other)
            other.common_dirs["key"] = "evidence"
        self.assertEqual((other.probes, other.operations), (5, 1))
        self.assertIs(other.version, version)
        # Nothing carries from one invocation to the next.
        fresh = project.Invocation("status")
        self.assertEqual((fresh.probes, fresh.operations, fresh.version, fresh.common_dirs, fresh.signal,
                          fresh.phase), (0, 0, None, {}, None, "planning"))
        with other:
            self.assertIs(project.current_invocation(), other)
            with fresh:
                self.assertIs(project.current_invocation(), fresh)
            self.assertIs(project.current_invocation(), other)
        outside = project.current_invocation()
        self.assertIsNot(outside, other)
        self.assertIsNot(outside, project.current_invocation(), "a fresh default at each call")
        self.assertEqual((outside.version, outside.probes, outside.common_dirs), (None, 0, {}))

    # T021.

    def test_clean_git_and_git_text_run_through_the_driver(self):
        project = self.project
        repo = self.worktree()
        other = self.repo("other", branch="elsewhere")
        log = self.base / "git.log"
        bin_dir = self.base / "counting"
        install_counting_git(bin_dir, log)
        # A caller's Git environment naming another repository is ignored.
        caller = {"GIT_DIR": str(other / ".git"), "GIT_WORK_TREE": str(other),
                  "GIT_INDEX_FILE": str(other / ".git" / "index")}
        spawned = []
        real_start = project.ChildHandle.start.__func__

        def start(cls, argv, cwd, kind):
            handle = real_start(cls, argv, cwd, kind)
            wakeup = signal.set_wakeup_fd(-1)
            signal.set_wakeup_fd(wakeup)
            spawned.append((handle, [signal.getsignal(number) for number in project.SCOPED_SIGNALS], wakeup))
            return handle

        before = ([signal.getsignal(number) for number in project.SCOPED_SIGNALS], signal.set_wakeup_fd(-1))
        signal.set_wakeup_fd(before[1])
        with self.in_process_env(bin_dir, **caller), \
                mock.patch.object(project.ChildHandle, "start", classmethod(start)):
            # Outside a subcommand: what they return today (tests/test_project.py:878
            # reads git_text() in process), one probe each with the 15 s budget, and
            # no signal handler installed.
            top = project.git(repo, "rev-parse", "--show-toplevel")
            self.assertIsInstance(top, subprocess.CompletedProcess)
            self.assertEqual((top.returncode, top.stdout, top.stderr), (0, f"{repo}\n", ""))
            self.assertEqual(project.git_text(repo, "symbolic-ref", "--short", "HEAD"), "main")
            self.assertIsNone(project.git_text(repo, "show-ref", "--verify", "--quiet", "refs/heads/none"))
            missing = project.git(self.base / "missing", "status")
            self.assertEqual(missing.returncode, 128)
            self.assertIn("fatal:", missing.stderr)
            self.assertEqual(len(spawned), 4)
            for handle, handlers, wakeup in spawned:
                self.assertAlmostEqual(handle.budget_end - handle.started, project.TIMING["inspect_budget"], places=6)
                self.assertEqual((handlers, wakeup), before, "no handler installed")
                self.assertEqual(handle.state, "reaped")
            # Inside an invocation each child is counted.
            with project.Invocation("status") as run:
                project.git_text(repo, "rev-parse", "HEAD")
                project.git(repo, "status", "--porcelain")
            self.assertEqual(run.probes, 2)
        records = child_log(log)
        self.assertEqual(len(records), 6)
        for record, args in zip(records, (
                ["-C", str(repo), "rev-parse", "--show-toplevel"],
                ["-C", str(repo), "symbolic-ref", "--short", "HEAD"],
                ["-C", str(repo), "show-ref", "--verify", "--quiet", "refs/heads/none"],
                ["-C", str(self.base / "missing"), "status"],
                ["-C", str(repo), "rev-parse", "HEAD"],
                ["-C", str(repo), "status", "--porcelain"])):
            # Scrubbed, pinned and in a process group of its own.
            self.assertEqual(record.argv, [*PINS, *args])
            self.assertEqual([name for name in record.names if name in SCRUBBED_NAMES], [])
            self.assertEqual(record.optional_locks, "0")
            self.assertEqual((record.ppid, record.pgid), (os.getpid(), record.pid))

        # Once the invocation's version check has failed, nothing is spawned:
        # git() returns a failed CompletedProcess and git_text() None.
        old_log = self.base / "old.log"
        old_bin = self.base / "counting-old"
        install_counting_git(old_bin, old_log, real=self.fake_dir("version-2.35.0") / "git")
        with self.in_process_env(old_bin), project.Invocation("status") as run:
            self.assertEqual(project.git_version(run).code, "git-too-old")
            self.assertEqual(len(child_log(old_log)), 1)
            refused = project.git(repo, "rev-parse", "HEAD")
            self.assertIsInstance(refused, subprocess.CompletedProcess)
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn("older than 2.36", refused.stderr)
            self.assertIsNone(project.git_text(repo, "rev-parse", "HEAD"))
            self.assertEqual((len(child_log(old_log)), run.probes), (1, 1), "no child after a failed check")

    # T026.

    def test_clean_two_handles_share_scrub_termination_and_parsers(self):
        # SC-004, SC-012, FR-062, N2 and lead ruling R-30, with the spike's table:
        # probe budget 1 s, grace 0.4 s (reap wait 2 s, tick 0.1 s). Three handles
        # start at once and the test's own selector loop drives them, calling
        # advance() on every tick, as feature 005's overview will: a status probe of
        # a real worktree, the ignore-sigterm fake, and a second ignore-sigterm fake
        # whose budget falls due 0.35 s later, on a later tick.
        grace = 0.4
        table = timing_table(probe_budget=1, term_grace=grace)
        repo = self.worktree()
        other = self.repo("other", branch="elsewhere")
        fake = self.fake_dir("ignore-sigterm", lifetime=15)
        real_log, fake_log = self.base / "real.log", self.base / "fake.log"
        real_git = install_counting_git(self.base / "counting-real", real_log)
        fake_git = install_counting_git(self.base / "counting-fake", fake_log, real=fake / "git")
        caller = {"GIT_DIR": str(other / ".git"), "GIT_INDEX_FILE": str(other / ".git" / "index"),
                  "GIT_CONFIG_PARAMETERS": "'core.bare'='true'"}
        fields, _ = self.run_child(table, """
            import selectors
            args = ["-C", ARGS["repo"], "status", "--porcelain=v1", "-z",
                    "--untracked-files=normal", "--ignored=matching"]
            handles, parsers = [], []
            selector = selectors.DefaultSelector()
            for index, git in enumerate((ARGS["real"], ARGS["fake"], ARGS["fake"])):
                argv = project.git_argv("status", args)
                handle = project.ChildHandle.start([git, *argv[1:]], None, "status")
                handle.budget_end = handle.started + TABLE["probe_budget"] + (0.35 if index == 2 else 0)
                handles.append(handle)
                parsers.append(project.StatusParser())
                for stream in (handle.process.stdout, handle.process.stderr):
                    selector.register(stream.fileno(), selectors.EVENT_READ,
                                      (index, stream is handle.process.stdout))
            open_streams = [2, 2, 2]
            terminated = {}
            while not all(handle.finished for handle in handles):
                now = time.monotonic()
                for index, handle in enumerate(handles):
                    if handle.state == "running":
                        if open_streams[index] == 0 and handle.reap() is not None:
                            continue
                        if now >= handle.budget_end:
                            handle.terminate_group()
                            terminated[index] = time.monotonic()
                    else:
                        handle.advance(now)
                dues = [handle.due() for handle in handles if not handle.finished and handle.due() is not None]
                timeout = max(0.0, min([TABLE["selector_tick"], *(due - time.monotonic() for due in dues)]))
                for key, _ in selector.select(timeout):
                    index, is_out = key.data
                    try:
                        chunk = os.read(key.fd, 65536)
                    except BlockingIOError:
                        continue
                    if not chunk:
                        selector.unregister(key.fd)
                        open_streams[index] -= 1
                    elif is_out:
                        parsers[index].feed(chunk)
                    else:
                        handles[index].keep_stderr(chunk)
            for handle in handles:
                handle.close()
            first = parsers[0].finish()
            one_wide = project.run_bounded(status_spec(ARGS["repo"]), project.StatusParser(),
                                           project.Invocation("status"))
            emit(pids=[handle.pid for handle in handles], states=[handle.state for handle in handles],
                 status=[handle.process.returncode for handle in handles],
                 terminated=sorted(terminated), same=first == one_wide.result,
                 first=[first["dirty"], first["ignored_files"], [os.fsdecode(s) for s in first["ignored_samples"]]],
                 one_wide_name=one_wide.name, live=len(project.LIVE_PROBES))
        """, env=self.env_with(**caller), repo=str(repo), real=str(real_git), fake=str(fake_git))
        self.assertEqual(fields["states"], ["reaped"] * 3)
        self.assertEqual(fields["status"], [0, -signal.SIGKILL, -signal.SIGKILL])
        self.assertEqual(fields["terminated"], [1, 2], "only the slow ones were stopped")
        self.assertEqual(fields["live"], 0)
        # The same parser gives the first one's records as the one-wide driver does.
        self.assertEqual(fields["one_wide_name"], "complete")
        self.assertTrue(fields["same"])
        self.assertEqual(fields["first"], [True, 1, ["kept.log"]])
        # All three scrubbed and pinned, each in a group of its own.
        records = child_log(real_log)[:1] + child_log(fake_log)
        self.assertEqual(len(records), 3)
        for record in records:
            self.assertEqual(record.argv, [*STATUS_PINS, *PINS, "-C", str(repo), *STATUS])
            self.assertEqual([name for name in record.names if name in SCRUBBED_NAMES], [])
            self.assertEqual(record.optional_locks, "0")
            self.assertEqual(record.pgid, record.pid)
        # Each slow one got SIGKILL 0.9 to 1.5 graces after its own SIGTERM,
        # measured from the child, its group gone; the second's SIGTERM came on a
        # later tick, and its grace did not wait on the first's.
        terms = []
        for pid in fields["pids"][1:]:
            death = wait_for_event(fake, "death", pid)
            term = first_event(fake_events(fake), "term", pid)
            self.assertIsNotNone(term)
            self.assertIsNotNone(death)
            gap = (death["t"] - term["t"]) / grace
            self.assertGreaterEqual(gap, 0.9)
            self.assertLess(gap, 1.5, "a blocking termination per handle measured 1.79 to 2.08")
            self.assertTrue(group_gone(pid))
            terms.append(term["t"])
        self.assertGreaterEqual(terms[1] - terms[0], 0.2)
