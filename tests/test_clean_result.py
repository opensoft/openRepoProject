"""The removal lane of feature 004's User Story 5 (T087 to T090): every removal
ends in a reconcilable record (design D9, D15, D18 and D19; the project-clean
delta, "Clean can explicitly retire verified worktrees" and "Clean records a
reconcilable result for every removal target"; data-model.md, "Signal slot",
"Target result and reconciliation record" and "Target stages"; research.md R4
and R6; lead rulings R-29, R-44, R-68, R-76, R-82, R-83 and R-93).

The command-line tests run `project clean` as a child through
tests/launch_project.py, each with the TIMING table it names (R-29): signals go
to that child alone, never to the test process or to a Git child (rule 7). The
in-process tests run project's main() with os.environ replaced and both
streams captured; main() must leave the signal handlers and the wakeup
descriptor as it found them. The fakes this module needs and clean_support
lacks are written here (rule 3; lead ruling R-83, P-14): a removal fake that
records every signal it receives, the ceiling child, a slow removal that marks
its end, and the sender that signals project once a removal is in flight.
Expected human text comes from clean_support's fixtures (rule 8).
"""
import contextlib
import errno
import io
import json
import os
from pathlib import Path
import shlex
import signal
import subprocess
import sys
import threading
import time
import types
import unittest
from unittest import mock

import clean_support

project = clean_support.load_project()
TEXT = clean_support.TEXT_FIXTURES
REAL_GIT = clean_support.REAL_GIT
TIMEOUT = clean_support.TIMEOUT

RECONCILIATION_KEYS = ["registry_entry_present", "path_present", "branch_present", "branch_sha",
                       "reconciled"]
SCOPED_SIGNALS = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)
NAMES = ("001-p", "002-q", "003-r")
CANCELLED = "Cancelled."

# The removal child's pins, as the contract writes them ("Git children"): the
# three status pins, then the seven protocol pins, before `-C ROOT`.
REMOVAL_PINS = ["-c", "status.showUntrackedFiles=normal", "-c", "core.untrackedCache=false",
                "-c", "core.fsmonitor=false", "-c", "protocol.allow=never", "-c", "protocol.file.allow=never",
                "-c", "protocol.ssh.allow=never", "-c", "protocol.git.allow=never",
                "-c", "protocol.http.allow=never", "-c", "protocol.https.allow=never",
                "-c", "protocol.ext.allow=never"]


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


NULL_RECORD = dict.fromkeys(RECONCILIATION_KEYS[:-1]) | {"reconciled": False}


def quoted(path):
    """path as a command prints it: human_path(path, command=True), which for
    the plain paths of these fixtures is shlex.quote() (contracts/project-clean.md,
    "Human output"; lead ruling R-83, P-2)."""
    return shlex.quote(os.fsdecode(path))


def wait_line(path):
    return TEXT["wait_line"].format(PATH=quoted(path))


def write_script(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    path.chmod(0o755)
    return path


def signal_recording_git(bin_dir, log, slow=None, seconds=1.0, status=None):
    """bin_dir/git, the removal fake that records signals (lead ruling R-83,
    P-14; remove-slow records none). On `worktree remove` it traps SIGINT,
    SIGTERM and SIGHUP, appending `signal NAME TARGET` to log for each one it
    receives, and appends `ready TARGET`. For the worktree slow it then sleeps
    seconds; with status given it then exits status without removing.
    Otherwise it runs the real removal as its own child, appends `exited
    TARGET STATUS` and exits with Git's status. Every other command execs the
    real git."""
    ending = (f'echo "exited $target {int(status)}" >> "$log"; exit {int(status)}' if status is not None
              else ":")
    return write_script(Path(bin_dir) / "git", f"""#!/bin/sh
real={shlex.quote(REAL_GIT)}
log={shlex.quote(str(log))}
slow={shlex.quote(os.fsdecode(slow or ""))}
case " $* " in
*" worktree remove "*)
  target=; prev=
  for a in "$@"; do [ "x$prev" = "xremove" ] && target=$a; prev=$a; done
  trap 'echo "signal INT $target" >> "$log"' INT
  trap 'echo "signal TERM $target" >> "$log"' TERM
  trap 'echo "signal HUP $target" >> "$log"' HUP
  echo "ready $target" >> "$log"
  if [ "x$target" = "x$slow" ]; then
    sleep {float(seconds)}
    {ending}
  fi
  "$real" "$@"
  code=$?
  echo "exited $target $code" >> "$log"
  exit $code;;
esac
exec "$real" "$@"
""")


def log_lines(log):
    path = Path(log)
    return path.read_text().splitlines() if path.exists() else []


# The ceiling child (T089; rule 3): Python behind an sh prelude, so that it can
# log. It logs `term` at each SIGTERM and survives it, and a helper in its own
# session, which a kill of the child's group spares, logs its `death` when the
# last write end of a pipe closes. In mode `remove-first` it runs the real
# removal first and logs `removed` with Git's status; then it logs `ready` with
# its process group and sleeps past any ceiling, so that only SIGKILL ends it.
CEILING_CHILD = r'''
import json, os, signal, subprocess, sys, time

EVENTS, MODE, REAL, ARGV = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]


def log(**fields):
    fields.setdefault("pid", os.getpid())
    fields.setdefault("t", time.monotonic())
    fd = os.open(EVENTS, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        os.write(fd, (json.dumps(fields) + "\n").encode())
    finally:
        os.close(fd)


signal.signal(signal.SIGTERM, lambda signum, frame: log(event="term"))
child = os.getpid()
read_end, write_end = os.pipe()
ack_read, ack_write = os.pipe()
if os.fork() == 0:
    os.setsid()
    os.write(ack_write, b"x")
    null = os.open(os.devnull, os.O_RDWR)
    for fd in (0, 1, 2):
        os.dup2(null, fd)
    os.close(write_end)
    os.read(read_end, 1)
    log(event="death", pid=child)
    os._exit(0)
os.read(ack_read, 1)
for fd in (ack_read, ack_write, read_end):
    os.close(fd)
if MODE == "remove-first":
    log(event="removed", status=subprocess.run([REAL, *ARGV]).returncode)
log(event="ready", pgid=os.getpgrp())
while True:
    time.sleep(3600)
'''


def ceiling_git(bin_dir, mode):
    """bin_dir/git: on `worktree remove`, the ceiling child in mode (`hang`,
    or `remove-first`), its events in bin_dir/ceiling-events.jsonl; every
    other command the real git. Returns the events file."""
    events = Path(bin_dir) / "ceiling-events.jsonl"
    write_script(Path(bin_dir) / "git", f"""#!/bin/sh
case " $* " in *" worktree remove "*)
  exec {shlex.quote(sys.executable)} -I -S -c {shlex.quote(CEILING_CHILD)} {shlex.quote(str(events))} {mode} \
{shlex.quote(REAL_GIT)} "$@";;
esac
exec {shlex.quote(REAL_GIT)} "$@"
""")
    return events


def events_of(path):
    path = Path(path)
    return [json.loads(line) for line in path.read_bytes().split(b"\n")[:-1] if line] if path.exists() else []


def json_documents(text):
    """Every JSON document text holds, in order, read with raw_decode, so that
    a second document is counted where one json.loads() would fail."""
    decoder, documents, at = json.JSONDecoder(), [], 0
    while True:
        while at < len(text) and text[at].isspace():
            at += 1
        if at == len(text):
            return documents
        document, at = decoder.raw_decode(text, at)
        documents.append(document)


# project leaves a signal ignored when it starts ignored (lead ruling R-101
# (b)), and a `&` job of a non-interactive shell starts with SIGINT ignored.
# So a child that a test sends SIGINT gets SIGINT back at SIG_DFL, as a
# foreground run starts it, when this process ignores SIGINT; otherwise it runs
# as it always has.


def sigint_ignored():
    return signal.getsignal(signal.SIGINT) == signal.SIG_IGN


def sigint_default():
    """preexec_fn: SIGINT at SIG_DFL in the child, before it execs."""
    signal.signal(signal.SIGINT, signal.SIG_DFL)


# An exec shim for a child spawned by a helper that takes no preexec_fn: it
# sets SIGINT to SIG_DFL, then execs the command in its own place.
SIGINT_DEFAULT_SHIM = ("import os, signal, sys; signal.signal(signal.SIGINT, signal.SIG_DFL); "
                       "os.execv(sys.argv[1], sys.argv[1:])")


def sigint_default_argv(argv):
    """argv, or argv behind SIGINT_DEFAULT_SHIM when this process ignores SIGINT."""
    return [sys.executable, "-I", "-S", "-c", SIGINT_DEFAULT_SHIM, *argv] if sigint_ignored() else argv


def sh_git(*args):
    """One real-git command line for a hook, by absolute path (lead ruling R-31)."""
    return " ".join(shlex.quote(os.fsdecode(arg)) for arg in (REAL_GIT, *args))


def when_target(path, *commands):
    """sh text for a counting-wrapper hook that runs commands only when the
    worktree being removed ($target) is path."""
    return f"if [ \"$target\" = {shlex.quote(os.fsdecode(path))} ]; then\n" + "\n".join(commands) + "\nfi"


def replaced_by_a_file(directory):
    """sh text for a counting-wrapper hook that moves directory aside, to
    DIRECTORY.moved, and puts an empty file at its path, so that an lstat of
    any path under it fails with ENOTDIR (lead ruling R-93 (a))."""
    path = os.fsdecode(directory)
    return f"mv {shlex.quote(path)} {shlex.quote(path + '.moved')} && : > {shlex.quote(path)}"


class ResultTests(clean_support.CleanCase):

    # Fixtures: one repository per case, its worktrees merged, clean and
    # published, each with a commit of its own (merged_worktree()).

    def batch(self, case, count=3, own_parent=False, setup=None):
        """A repository at BASE/CASE/repo with an origin at BASE/CASE/remote.git
        and count eligible worktrees on branches NAMES[:count], at
        BASE/CASE/trees/NAME, or BASE/CASE/trees/NAME-parent/NAME when
        own_parent is true, in canonical order (raw path bytes). setup(name,
        tree) runs before each worktree's own commit. Returns (root, trees)."""
        top = self.base / case
        root = self._init_repo(top / "repo", "main")
        self.bare_remote(root, name=f"{case}/remote.git")
        trees = []
        for name in NAMES[:count]:
            place = top / "trees" / (name + "-parent") / name if own_parent else top / "trees" / name
            trees.append(self.merged_worktree(name, path=place, root=root,
                                              setup=None if setup is None else lambda tree, n=name: setup(n, tree)))
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

    def stages(self, document):
        """(path, stage, reason) of each target of an apply result record."""
        return [(target["path"], target["stage"], target["reason"]) for target in document["targets"]]

    def counting(self, case, hooks=None, real=REAL_GIT):
        """The counting wrapper first on PATH in front of real, with hooks:
        (env, log), the log emptied."""
        bin_dir, log = self.base / case / "counting-bin", self.base / case / "children.log"
        clean_support.install_counting_git(bin_dir, log, real=real, hooks=hooks)
        clean_support.reset_child_log(log)
        return self.path_first(bin_dir), log

    def run_signalled(self, argv, env, steps, preexec_fn=None):
        """Run argv, project through the launcher, in a session of its own with
        both streams on pipes read as they fill; for each (ready, signum) of
        steps in turn, poll ready() until it holds, then send signum to project
        alone (rule 7). preexec_fn, a test's own, runs in the child before it
        execs; without one, the child gets SIGINT at SIG_DFL when this process
        ignores SIGINT (sigint_default()). Returns a CompletedProcess with text
        streams, its document parsed when standard output holds one."""
        if preexec_fn is None and sigint_ignored():
            preexec_fn = sigint_default
        child = subprocess.Popen(argv, cwd=self.base, env=env, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True,
                                 preexec_fn=preexec_fn)
        streams = {"out": [], "err": []}
        readers = [threading.Thread(target=lambda key=key, stream=stream: streams[key].append(stream.read()),
                                    daemon=True)
                   for key, stream in (("out", child.stdout), ("err", child.stderr))]
        for reader in readers:
            reader.start()
        deadline = time.monotonic() + TIMEOUT
        problem = None
        try:
            for ready, signum in steps:
                while not ready():
                    if child.poll() is not None:
                        problem = f"project exited before the step sending {signal.Signals(signum).name}"
                        break
                    if time.monotonic() > deadline:
                        problem = f"no step sending {signal.Signals(signum).name} became ready in {TIMEOUT} s"
                        break
                    time.sleep(0.01)
                if problem:
                    break
                os.kill(child.pid, signum)
            if problem is None:
                try:
                    child.wait(max(0.1, deadline - time.monotonic()))
                except subprocess.TimeoutExpired:
                    problem = f"project did not exit within {TIMEOUT} s"
        finally:
            if child.poll() is None:
                with contextlib.suppress(OSError):
                    os.killpg(child.pid, signal.SIGKILL)
                child.wait()
            for reader in readers:
                reader.join(TIMEOUT)
            child.stdout.close()
            child.stderr.close()
        text = {key: b"".join(chunks).decode("utf-8", "surrogateescape") for key, chunks in streams.items()}
        result = subprocess.CompletedProcess(argv, child.returncode, text["out"], text["err"])
        if problem:
            self.fail(f"{problem}\n{clean_support.transcript(result)}")
        try:
            result.document = json.loads(result.stdout)
        except ValueError:
            result.document = None
        return result

    def main_in_process(self, argv, env=None, patches=()):
        """project.main(argv) in this process: os.environ replaced by env
        (self.env by default), both streams captured, and each (owner, name,
        value) of patches set for the call. The handlers of SIGINT, SIGTERM and
        SIGHUP and the wakeup descriptor must be as they were after it, even
        when it raises (rule 7). Returns the status and both streams, and,
        under --json, the one JSON document of standard output when it holds
        one."""
        out, err = io.StringIO(), io.StringIO()
        before = signal_state()
        try:
            with contextlib.ExitStack() as stack:
                stack.enter_context(mock.patch.dict(os.environ, self.env if env is None else env, clear=True))
                for owner, name, value in patches:
                    stack.enter_context(mock.patch.object(owner, name, value))
                stack.enter_context(contextlib.redirect_stdout(out))
                stack.enter_context(contextlib.redirect_stderr(err))
                status = project.main([os.fsdecode(arg) for arg in argv])
        finally:
            self.assertEqual(signal_state(), before, "main() left the signal handlers changed")
        result = types.SimpleNamespace(status=status, stdout=out.getvalue(), stderr=err.getvalue(), document=None)
        if "--json" in argv and result.stdout:
            try:
                result.document = json.loads(result.stdout)
            except ValueError as exc:
                self.fail(f"standard output is not one JSON document: {exc}\n{result.stdout}\n{result.stderr}")
        return result

    # T087: "A signal during a removal" and "SIGTERM before the apply phase".

    def test_clean_a_signal_during_a_removal(self):
        # Through the launcher with the real table (probe budget 5 s, work
        # deadline 50 s, ceiling 300 s): no budget, deadline or ceiling is
        # reached, so only the signal acts. The second of three removals sleeps
        # 1.5 s in the signal-recording fake; once it has written `ready`, the
        # signal goes to project alone. The child is not signalled and is
        # waited for; the third target is never revalidated or spawned
        # (pcl:931-935, FR-036; lane 3's E2, M-1). The wait line prints once
        # (D18; lead ruling R-83, P-2).
        table = clean_support.timing_table()
        cases = [("SIGINT", signal.SIGINT, 130, None), ("SIGTERM", signal.SIGTERM, 143, None),
                 ("SIGHUP", signal.SIGHUP, 129, None), ("SIGINT, Git fails", signal.SIGINT, 130, 1)]
        for name, signum, expected, status in cases:
            with self.subTest(name):
                case = name.replace(", ", "-").replace(" ", "-").lower()
                root, trees = self.batch(case)
                planned = {tree: self.head(tree) for tree in trees}
                bin_dir, log = self.base / case / "fake-bin", self.base / case / "signals.log"
                signal_recording_git(bin_dir, log, slow=trees[1], seconds=1.5, status=status)
                result = self.run_signalled(
                    clean_support.launched_argv(table, "clean", root, "--all-safe", "--apply", "--yes", "--json"),
                    self.path_first(bin_dir), [(lambda: f"ready {trees[1]}" in log_lines(log), signum)])
                self.assert_status(result, expected)
                document = result.document
                self.assertIsNotNone(document, clean_support.transcript(result))
                second = ("removed", None) if status is None else ("failed", "git-failed")
                self.assertEqual(self.stages(document), [(str(trees[0]), "removed", None),
                                                         (str(trees[1]), *second),
                                                         (str(trees[2]), "not-attempted", "interrupted")])
                first, middle, last = document["targets"]
                if status is None:
                    self.assertEqual(middle["reconciliation"], record(False, False, True, planned[trees[1]]))
                    self.assertFalse(trees[1].exists())
                else:
                    self.assertEqual((middle["exit_status"], middle["reconciliation"]),
                                     (status, record(True, True, True, planned[trees[1]])))
                    self.assertTrue(trees[1].is_dir())
                self.assertEqual((last["reconciliation"], last["exit_status"], last["probes_performed"]),
                                 (None, None, 0))
                self.assertTrue(trees[2].is_dir())
                self.assertEqual(document["exit_code"], expected)
                # The fake recorded no signal; the second child ran to its end;
                # the third was never spawned.
                lines = log_lines(log)
                self.assertEqual([line for line in lines if line.startswith("signal ")], [], lines)
                self.assertEqual([line for line in lines if line.startswith("ready ")],
                                 [f"ready {trees[0]}", f"ready {trees[1]}"])
                self.assertIn(f"exited {trees[1]} {0 if status is None else status}", lines)
                # The wait line once on the human stream, standard error under
                # --apply --json, naming the removal in flight.
                self.assertEqual(result.stderr.splitlines().count(wait_line(trees[1])), 1, result.stderr)
                self.assertEqual(sum(line.startswith("Waiting for git worktree remove ")
                                     for line in result.stderr.splitlines()), 1)
                self.assertEqual(self.head(root, "refs/heads/" + NAMES[1]), planned[trees[1]])

        # At a pseudo-terminal: SIGINT at the question, and end of input there,
        # exit 130 with nothing removed. run_pty_steps() takes no preexec_fn, so
        # the shim gives the child SIGINT at SIG_DFL when this process ignores it.
        root, trees = self.batch("question", count=2)
        before = self.snapshot(root, trees)
        argv = sigint_default_argv(clean_support.launched_argv(table, "clean", root, "--all-safe", "--apply"))
        question = TEXT["question"].format(N=2)
        for name, action in (("SIGINT", signal.SIGINT), ("end of input", clean_support.PTY_EOF)):
            with self.subTest(at_the_question=name):
                result = self.run_pty_steps(argv, [(question, action)])
                self.assert_status(result, 130)
                self.assertIn(CANCELLED, result.stderr.splitlines())
                self.assertEqual(self.snapshot(root, trees), before, "nothing removed")

    def test_clean_sigterm_before_the_apply_phase(self):
        # The ignore-sigterm fake's status probe is running during planning
        # when SIGTERM reaches project. Table: the grace and the reap wait
        # shortened to 0.5 s, the probe budget whole (5 s), so the probe is
        # still running when the signal arrives (R-29). Pins T047 and T035.
        table = clean_support.timing_table(term_grace=0.5, reap_wait=0.5)
        grace = table["term_grace"]
        root, trees = self.batch("sigterm-planning", count=2)
        before = self.snapshot(root, trees)
        fake = self.base / "ignore-sigterm-bin"
        clean_support.install_fake_git(fake, "ignore-sigterm", lifetime=30)
        result = self.run_signalled(
            clean_support.launched_argv(table, "clean", root, "--all-safe", "--apply", "--yes", "--json"),
            self.path_first(fake), [(lambda: any(event["event"] == "ready" for event in clean_support.fake_events(fake)),
                                     signal.SIGTERM)])
        self.assert_status(result, 143)
        self.assertEqual(result.stdout, "", "no JSON document")
        self.assertEqual(result.stderr.splitlines(), [CANCELLED])
        ready = clean_support.wait_for_event(fake, "ready")
        term = clean_support.wait_for_event(fake, "term", ready["pid"])
        death = clean_support.wait_for_event(fake, "death", ready["pid"])
        self.assertIsNotNone(term, clean_support.fake_events(fake))
        self.assertIsNotNone(death, clean_support.fake_events(fake))
        # SIGKILL at least 0.9 of the grace after the SIGTERM, measured from the
        # child, and no process of its group remains.
        self.assertGreaterEqual(death["t"] - term["t"], 0.9 * grace)
        with self.assertRaises(ProcessLookupError):
            os.killpg(ready["pgid"], 0)
        self.assertEqual(self.snapshot(root, trees), before, "nothing mutated")

    def test_clean_sigterm_before_the_apply_phase_after_the_last_probe(self):
        # The signal-parent-in fake sends SIGTERM, and in turn SIGHUP, to
        # project from the status probe of the last row, which then completes:
        # with --yes, and at a pseudo-terminal before the question. Plan review
        # M1; it pins T047. The real table.
        table = clean_support.timing_table()
        for name, signum, expected in (("TERM", signal.SIGTERM, 143), ("HUP", signal.SIGHUP, 129)):
            root, trees = self.batch(f"after-last-{name.lower()}", count=2)
            before = self.snapshot(root, trees)
            fake = self.base / f"signal-parent-{name.lower()}-bin"
            clean_support.install_fake_git(fake, "signal-parent-in", path=trees[-1], signal=name)
            env = self.path_first(fake)
            with self.subTest(signal=name, run="--yes"):
                result = self.run_launched(table, "clean", root, "--all-safe", "--apply", "--yes", "--json", env=env)
                self.assert_status(result, expected)
                self.assertEqual(result.stdout, "", "no JSON document")
                self.assertEqual(result.stderr.splitlines(), [CANCELLED])
                self.assertEqual(self.snapshot(root, trees), before, "nothing removed")
            with self.subTest(signal=name, run="terminal"):
                argv = clean_support.launched_argv(table, "clean", root, "--all-safe", "--apply")
                result = self.run_pty_steps(argv, env=env)
                self.assert_status(result, expected)
                self.assertNotIn("[yes/N]", result.stdout + result.stderr, "no question asked")
                self.assertIn(CANCELLED, result.stderr.splitlines())
                self.assertEqual(self.snapshot(root, trees), before, "nothing removed")

    def test_clean_sigterm_before_the_apply_phase_while_the_plan_is_written(self):
        # In process: print_plan() records the signal in the slot as it returns
        # (research.md R4, lead ruling R-34). A report and an --all-safe preview
        # each exit 143, 129 and 130 with `Cancelled.` on standard error, and
        # nothing is mutated. Pins T047. No signal is sent (rule 7).
        root, trees = self.batch("while-written", count=2)
        before = self.snapshot(root, trees)
        original = project.print_plan
        for mode in ([], ["--all-safe"]):
            for signum, expected in ((signal.SIGTERM, 143), (signal.SIGHUP, 129), (signal.SIGINT, 130)):
                with self.subTest(mode=mode, signal=signal.Signals(signum).name):
                    def print_plan(plan, run, signum=signum):
                        original(plan, run)
                        run.record_signal(signum)

                    result = self.main_in_process(["clean", root, *mode], patches=[(project, "print_plan", print_plan)])
                    self.assertEqual(result.status, expected, result.stderr)
                    self.assertEqual(result.stderr.splitlines(), [CANCELLED])
                    self.assertIn(f"Cleanup plan for {root}", result.stdout)
                    self.assertEqual(self.snapshot(root, trees), before, "nothing mutated")

    def test_clean_a_second_sigint_abandons_reconciliation(self):
        # The slow-after-remove fake behind the counting wrapper, whose
        # pre-remove hook sleeps 1 s, so the removal is in flight for the first
        # SIGINT. Once the removal has run, the rescan's registry listing (row
        # 4) sleeps; the second SIGINT, sent once that child is recorded,
        # arrives in phase `reconciling` and abandons the remaining rescans
        # (plan review M17, FR-036, D15; lead ruling R-83, P-3 and P-6). The
        # real table.
        table = clean_support.timing_table()
        root, trees = self.batch("second-sigint", count=2)
        planned = self.head(root, "refs/heads/" + NAMES[0])
        fake = clean_support.install_fake_git(self.base / "slow-after-remove-bin", "slow-after-remove", lifetime=30)
        env, log = self.counting("second-sigint", hooks={"pre": "sleep 1"}, real=fake)

        def after_removal():
            records = clean_support.child_log(log)
            at = next((index for index, child in enumerate(records) if is_removal(child)), None)
            return [] if at is None else records[at + 1:]

        result = self.run_signalled(
            clean_support.launched_argv(table, "clean", root, "--all-safe", "--apply", "--yes", "--json"), env,
            [(lambda: any(map(is_removal, clean_support.child_log(log))), signal.SIGINT),
             (lambda: any(subcommand(child)[:2] == ["worktree", "list"] for child in after_removal()),
              signal.SIGINT)])
        self.assert_status(result, 130)
        document = result.document
        self.assertIsNotNone(document, clean_support.transcript(result))
        self.assertEqual(self.stages(document), [(str(trees[0]), "unknown", "reconciliation-incomplete"),
                                                 (str(trees[1]), "not-attempted", "interrupted")])
        first, second = document["targets"]
        # The identity was re-established; the registry listing was abandoned,
        # and no later read ran: every field not read is null.
        self.assertEqual((first["exit_status"], first["reconciliation"]), (0, NULL_RECORD))
        self.assertIsNone(second["reconciliation"])
        self.assertEqual(document["exit_code"], 130)
        rescan = after_removal()
        self.assertEqual([subcommand(child)[:2] for child in rescan],
                         [["rev-parse", "--path-format=absolute"], ["worktree", "list"]])
        # The running group was terminated and reaped.
        with self.assertRaises(ProcessLookupError):
            os.killpg(rescan[-1].pgid, 0)
        self.assertFalse(trees[0].exists())
        self.assertTrue(trees[1].is_dir())
        self.assertEqual(self.head(root, "refs/heads/" + NAMES[0]), planned, "the branch is kept")
        # The record is printed: the stop block on the human stream, and the
        # wait line once, at the first SIGINT.
        self.assertIn(TEXT["stop_block"].format(PATH=trees[0], REASON="reconciliation-incomplete", K=0, N=2,
                                                NOT_ATTEMPTED=trees[1], ROOT=quoted(root)),
                      result.stderr.splitlines())
        self.assertEqual(result.stderr.splitlines().count(wait_line(trees[0])), 1, result.stderr)

    # T088: "Exit 0 without evidence", "Git leaves an orphaned directory" and
    # "Git refuses the removal".

    def test_clean_exit_0_without_evidence(self):
        # The remove-noop fake exits 0 and removes nothing; the rescan finds the
        # entry, the path and the branch at its planned SHA. Pins T056.
        root, trees = self.batch("noop", count=2)
        planned = [self.head(tree) for tree in trees]
        fake = self.base / "remove-noop-bin"
        clean_support.install_fake_git(fake, "remove-noop")
        result = self.run_json("clean", root, "--all-safe", "--apply", "--yes", "--json", env=self.path_first(fake))
        self.assert_status(result, 1)
        document = result.document
        self.assertEqual(self.stages(document), [(str(trees[0]), "unknown", "unconfirmed-removal"),
                                                 (str(trees[1]), "not-attempted", "batch-stopped")])
        first, second = document["targets"]
        self.assertEqual((first["exit_status"], first["notes"]), (0, []))
        self.assertEqual(first["reconciliation"], record(True, True, True, planned[0]))
        self.assertEqual((second["reconciliation"], second["exit_status"]), (None, None))
        self.assertEqual(document["exit_code"], 1)
        self.assertTrue(all(tree.is_dir() for tree in trees))

    @clean_support.not_root
    def test_clean_git_leaves_an_orphaned_directory(self):
        # The first target holds a tracked file in a subdirectory made
        # unwritable after the merge. Git deletes the admin directory, cannot
        # delete the tree and exits 255 (checked on Git 2.43.0). The note goes
        # on the target after decide_stage() (lead ruling R-83, P-5).
        def setup(name, tree):
            if name == NAMES[0]:
                (tree / "kept").mkdir()
                (tree / "kept" / "file").write_text("held")

        root, trees = self.batch("orphaned", count=2, setup=setup)
        held = trees[0] / "kept"
        held.chmod(0o555)
        self.addCleanup(held.chmod, 0o755)
        planned = [self.head(tree) for tree in trees]
        branches = self.branches(root)
        result = self.run_json("clean", root, "--all-safe", "--apply", "--yes", "--json")
        self.assert_status(result, 255)
        document = result.document
        self.assertEqual(self.stages(document), [(str(trees[0]), "failed", "git-failed"),
                                                 (str(trees[1]), "not-attempted", "batch-stopped")])
        first, second = document["targets"]
        self.assertEqual((first["exit_status"], first["notes"]), (255, ["orphaned-directory"]))
        # Entry gone, path present, the retained branch with its SHA.
        self.assertEqual(first["reconciliation"], record(False, True, True, planned[0]))
        self.assertEqual((second["reconciliation"], second["notes"]), (None, []))
        self.assertEqual(document["exit_code"], 255)
        self.assertEqual(self.branches(root), branches, "every branch is kept")
        # Nothing deletes the directory, and no later plan lists it.
        self.assertTrue((held / "file").is_file())
        preview = self.run_json("clean", root, "--all-safe", "--json").document
        self.assertNotIn(str(trees[0]), [row["path"] for row in preview["worktrees"]])
        self.assertEqual([entry["path"] for entry in preview["selected"]], [str(trees[1])])
        self.assertTrue((held / "file").is_file())

    def test_clean_git_refuses_the_removal(self):
        # The pre-remove hook locks the first target after its revalidation, so
        # Git refuses with 128 (checked on Git 2.43.0).
        root, trees = self.batch("git-refuses", count=2)
        planned = [self.head(tree) for tree in trees]
        env, log = self.counting("git-refuses", hooks={"pre": when_target(
            trees[0], sh_git("-C", root, "worktree", "lock", trees[0]))})
        result = self.run_json("clean", root, "--all-safe", "--apply", "--yes", "--json", env=env)
        self.assert_status(result, 128)
        document = result.document
        self.assertEqual(self.stages(document), [(str(trees[0]), "failed", "git-refused"),
                                                 (str(trees[1]), "not-attempted", "batch-stopped")])
        first, second = document["targets"]
        self.assertEqual(first["command"], ["git", *REMOVAL_PINS, "-C", str(root), "worktree", "remove",
                                            str(trees[0])])
        self.assertEqual((first["exit_status"], first["notes"]), (128, []))
        self.assertEqual(first["reconciliation"], record(True, True, True, planned[0]))
        self.assertIsNone(second["reconciliation"])
        self.assertEqual(document["exit_code"], 128)
        self.assertEqual(sum(map(is_removal, clean_support.child_log(log))), 1)
        self.assertTrue(all(tree.is_dir() for tree in trees))
        # Every retained branch is reported, after the stop block.
        lines = result.stderr.splitlines()
        stop = TEXT["stop_block"].format(PATH=trees[0], REASON="git-refused", K=0, N=2, NOT_ATTEMPTED=trees[1],
                                         ROOT=quoted(root))
        self.assertIn(stop, lines)
        self.assertEqual(lines[lines.index(stop) + 1], TEXT["branches_kept_line"].format(BRANCHES=", ".join(NAMES[:2])))

    # T089: "A removal past the hard ceiling", "Unreadable path after removal"
    # and "Exception after the apply phase begins".

    def test_clean_a_removal_past_the_hard_ceiling(self):
        # Through the launcher with a table that shortens the ceiling to 1.5 s,
        # the grace and the reap wait to 0.5 s each, and leaves the probe budget
        # whole, 5 s (R-29). The ceiling child survives SIGTERM: at the ceiling
        # its group gets SIGTERM, then SIGKILL after the grace, and it is reaped
        # with exit_status 137 (plan review M12, lead ruling R-68 (b)). The
        # rescan then decides (D9; pcl:252-256, :910-926): the child that never
        # removed is unknown with removal-ceiling and the note
        # partially-removed; the one that removed first is removed with
        # removal-ceiling. Later targets are not-attempted; exit 1. Lane 3's
        # E4 a end to end (lead ruling R-82 (d)).
        table = clean_support.timing_table(removal_ceiling=1.5, term_grace=0.5, reap_wait=0.5)
        grace = table["term_grace"]
        for mode in ("hang", "remove-first"):
            with self.subTest(mode):
                root, trees = self.batch(f"ceiling-{mode}", count=2)
                planned = [self.head(tree) for tree in trees]
                bin_dir = self.base / f"ceiling-{mode}-bin"
                events = ceiling_git(bin_dir, mode)
                result = self.run_json("clean", root, "--all-safe", "--apply", "--yes", "--json", timing=table,
                                       env=self.path_first(bin_dir))
                self.assert_status(result, 1)
                document = result.document
                first, second = document["targets"]
                logged = events_of(events)
                ready = next(event for event in logged if event["event"] == "ready")
                term = next((event for event in logged if event["event"] == "term"), None)
                deadline = time.monotonic() + TIMEOUT
                while not any(event["event"] == "death" for event in logged) and time.monotonic() < deadline:
                    time.sleep(0.01)
                    logged = events_of(events)
                death = next((event for event in logged if event["event"] == "death"), None)
                self.assertIsNotNone(term, logged)
                self.assertIsNotNone(death, logged)
                self.assertGreaterEqual(death["t"] - term["t"], 0.9 * grace)
                with self.assertRaises(ProcessLookupError):
                    os.killpg(ready["pgid"], 0)
                self.assertEqual(first["exit_status"], 137)
                if mode == "hang":
                    self.assertEqual((first["stage"], first["reason"], first["notes"]),
                                     ("unknown", "removal-ceiling", ["partially-removed"]))
                    self.assertEqual(first["reconciliation"], record(True, True, True, planned[0]))
                    self.assertTrue(trees[0].is_dir())
                else:
                    self.assertEqual([event["status"] for event in logged if event["event"] == "removed"], [0])
                    self.assertEqual((first["stage"], first["reason"], first["notes"]),
                                     ("removed", "removal-ceiling", []))
                    self.assertEqual(first["reconciliation"], record(False, False, True, planned[0]))
                    self.assertFalse(trees[0].exists())
                self.assertEqual((second["stage"], second["reason"], second["reconciliation"]),
                                 ("not-attempted", "batch-stopped", None))
                self.assertTrue(trees[1].is_dir())
                self.assertEqual(document["exit_code"], 1)
                self.assertEqual(self.head(root, "refs/heads/" + NAMES[0]), planned[0], "the branch is kept")
                # Neither a signal nor the deadline came: no wait line.
                self.assertNotIn("Waiting for git worktree remove", result.stderr)
                # T094's recovery text on the partially-removed target, once,
                # first in the result, before the stop block (pcl:925-926; lead
                # rulings R-79 P-11 and R-83 P-2); none once both are gone.
                lines = result.stderr.splitlines()
                note = TEXT["partial_removal_note"].format(PATH=quoted(trees[0]))
                stop = TEXT["stop_block"].format(PATH=trees[0], REASON="removal-ceiling",
                                                 K=0 if mode == "hang" else 1, N=2, NOT_ATTEMPTED=trees[1],
                                                 ROOT=quoted(root))
                self.assertIn(stop, lines)
                if mode == "hang":
                    self.assertEqual(lines.count(note), 1, result.stderr)
                    self.assertLess(lines.index(note), lines.index(stop))
                    self.assertEqual(note, "Probable partial removal: inspect, then git worktree remove --force "
                                           f"{quoted(trees[0])} by hand.")
                else:
                    self.assertNotIn(note, lines)
                    self.assertFalse(any(line.startswith("Probable partial removal:") for line in lines))

    @clean_support.not_root
    def test_clean_unreadable_path_after_removal(self):
        # Each target under a parent directory of its own: CleanCase's base also
        # holds the repository, so an unsearchable base would lose the identity
        # (unconfirmed-removal) instead. After Git exits 0, the post-remove hook
        # removes search permission from the first target's parent, so the
        # rescan's lstat fails with EACCES (pcl:1012-1018).
        root, trees = self.batch("unreadable", count=2, own_parent=True)
        parent = trees[0].parent
        self.addCleanup(os.chmod, parent, 0o755)
        planned = [self.head(tree) for tree in trees]
        env, log = self.counting("unreadable", hooks={"post": when_target(
            trees[0], f"chmod 000 {shlex.quote(str(parent))}")})
        result = self.run_json("clean", root, "--all-safe", "--apply", "--yes", "--json", env=env)
        os.chmod(parent, 0o755)
        self.assert_status(result, 1)
        document = result.document
        self.assertEqual(self.stages(document), [(str(trees[0]), "unknown", "reconciliation-incomplete"),
                                                 (str(trees[1]), "not-attempted", "batch-stopped")])
        first = document["targets"][0]
        self.assertEqual((first["exit_status"], first["notes"]), (0, []))
        self.assertEqual(first["reconciliation"], record(False, None, True, planned[0]))
        self.assertIs(first["reconciliation"]["reconciled"], False)
        self.assertEqual((document["exit_code"], document["completeness"]), (1, "incomplete"))
        self.assertFalse(trees[0].exists())
        # The record is printed: the stop block on the human stream.
        self.assertIn(TEXT["stop_block"].format(PATH=trees[0], REASON="reconciliation-incomplete", K=0, N=2,
                                                NOT_ATTEMPTED=trees[1], ROOT=quoted(root)),
                      result.stderr.splitlines())

    def test_clean_exception_after_the_apply_phase_begins(self):
        # In process, `--all-safe --apply --yes --json` on two targets, a fault
        # injected in turn: into the first target's rescan; into the first
        # removal once its child has started (ChildHandle.due(), which
        # run_bounded() calls after the spawn, raises once for the removal
        # handle, so that the driver waits for the child before the exception
        # goes on; the child is a 1 s removal that logs its end); into the
        # driver's setup once that removal child has started (the selector,
        # which fails once with EMFILE: the child is waited for all the same;
        # the runner review's EMFILE candidate, lead ruling R-101 (b)); and
        # into the final rescan, the second target's. The target being handled is
        # unknown with internal-error and its fields not established null,
        # later targets not-attempted, the record printed, exit 1; and 143 when
        # the fault also records SIGTERM in the slot (plan review M2;
        # pcl:938-941; research.md R6; lead ruling R-83, P-7). No signal is
        # sent (rule 7).
        original_rescan, original_due, original_progress = project.rescan, project.ChildHandle.due, project.print_progress
        original_start, original_selector = project.ChildHandle.start, project.selectors.DefaultSelector
        for fault in ("rescan", "removal", "selector", "final rescan"):
            for signum in (None, signal.SIGTERM):
                with self.subTest(fault=fault, signal=signum and signal.Signals(signum).name):
                    case = f"fault-{fault.replace(' ', '-')}-{'sigterm' if signum else 'plain'}"
                    root, trees = self.batch(case, count=2)
                    planned = [self.head(tree) for tree in trees]
                    env, log = self.env, None
                    calls, seen = [], []

                    def inject(message, signum=signum):
                        if signum is not None:
                            project.current_invocation().record_signal(signum)
                        raise RuntimeError(message)

                    def rescan(target, run, fault=fault):
                        calls.append(target["path"])
                        if fault == "rescan" or len(calls) == 2:
                            inject(f"fault in the {fault}")
                        return original_rescan(target, run)

                    def due(handle):
                        if handle.kind == "removal" and not calls:
                            calls.append(handle.pid)
                            inject("fault once the removal child has started")
                        return original_due(handle)

                    def start(argv, cwd, kind):
                        handle = original_start(argv, cwd, kind)
                        if kind == "removal" and not calls:
                            calls.append(handle.pid)
                        return handle

                    def selector(*args, signum=signum, **kwargs):
                        if len(calls) == 1:  # the removal child has just started
                            calls.append("selector")
                            if signum is not None:
                                project.current_invocation().record_signal(signum)
                            raise OSError(errno.EMFILE, os.strerror(errno.EMFILE))
                        return original_selector(*args, **kwargs)

                    def print_progress(target, run, log=None):
                        seen.append((target["path"], log_lines(log) if log else []))
                        original_progress(target, run)

                    if fault in ("removal", "selector"):
                        bin_dir, log = self.base / case / "slow-bin", self.base / case / "removal.log"
                        signal_recording_git(bin_dir, log, slow=trees[0], seconds=1.0)
                        env = self.path_first(bin_dir)
                        patches = ([(project.ChildHandle, "due", due)] if fault == "removal" else
                                   [(project.ChildHandle, "start", staticmethod(start)),
                                    (project.selectors, "DefaultSelector", selector)])
                    else:
                        patches = [(project, "rescan", rescan)]
                    patches.append((project, "print_progress", lambda target, run, log=log: print_progress(
                        target, run, log)))
                    result = self.main_in_process(["clean", root, "--all-safe", "--apply", "--yes", "--json"],
                                                  env=env, patches=patches)
                    expected = 1 if signum is None else 143
                    self.assertEqual(result.status, expected, result.stderr)
                    document = result.document
                    self.assertIsNotNone(document, result.stderr)
                    later = "batch-stopped" if signum is None else "interrupted"
                    if fault == "final rescan":
                        self.assertEqual(self.stages(document), [(str(trees[0]), "removed", None),
                                                                 (str(trees[1]), "unknown", "internal-error")])
                        handled, stop = document["targets"][1], (trees[1], 1, "none")
                    else:
                        self.assertEqual(self.stages(document), [(str(trees[0]), "unknown", "internal-error"),
                                                                 (str(trees[1]), "not-attempted", later)])
                        handled, stop = document["targets"][0], (trees[0], 0, trees[1])
                        self.assertIsNone(document["targets"][1]["reconciliation"])
                        self.assertTrue(trees[1].is_dir())
                    self.assertEqual(handled["reconciliation"], NULL_RECORD)
                    self.assertEqual(handled["notes"], [])
                    # The rescan faults follow an exit 0; the removal and selector
                    # faults leave the child's status unobserved.
                    self.assertEqual(handled["exit_status"], None if fault in ("removal", "selector") else 0)
                    self.assertEqual(document["exit_code"], expected)
                    self.assertEqual(document["completeness"], "incomplete")
                    path, removed, not_attempted = stop
                    self.assertIn(TEXT["stop_block"].format(PATH=path, REASON="internal-error", K=removed, N=2,
                                                            NOT_ATTEMPTED=not_attempted, ROOT=quoted(root)),
                                  result.stderr.splitlines())
                    if fault in ("removal", "selector"):
                        # The child was waited for: it had run to its end, the
                        # real removal included, before the target was decided.
                        self.assertEqual(seen[0][0], os.fsencode(trees[0]))  # a Target holds raw bytes
                        self.assertIn(f"exited {trees[0]} 0", seen[0][1])
                        self.assertFalse(trees[0].exists())
                    self.assertEqual(self.head(root, "refs/heads/" + NAMES[0]), planned[0], "the branch is kept")

    # What the rescan reads after a removal that exited 0 (T085, T093; lead
    # rulings R-82 (d), R-93 (a) and R-78 (e), second amendment).

    def test_clean_a_parent_replaced_by_a_file_after_removal(self):
        # Lead ruling R-93 (a), which corrects R-82 (d): an lstat that fails
        # with ENOTDIR, a parent no longer a directory, is evidence of
        # absence, as ENOENT is (R-36; data-model.md, "Target result and
        # reconciliation record"). Between Git's exit 0 and the rescan, the
        # post-remove hook:
        # - moves the target's own parent aside and puts a file at its path:
        #   path_present is false, the record reconciled, and the target
        #   `removed`, so the batch goes on, exit 0;
        # - does the same to the parent of the repository root, which holds
        #   the repository alone: the identity probe fails and the root's
        #   lstat gives ENOTDIR, so the identity is lost and the record, every
        #   field null, is left unmarked, `unknown` with `unconfirmed-removal`,
        #   exit 1 (R-78 (e); rescan(), _identity_gone());
        # - in the contrast, an lstat that cannot tell, makes the target's
        #   parent mode 000: EACCES, path_present null and a marked record,
        #   `unknown` with `reconciliation-incomplete`, exit 1 (pcl:1012-1018;
        #   test_clean_unreadable_path_after_removal pins that case in full).
        # Lane 3's runs enotdir-path-parent and enotdir-root-parent gave the
        # first two outcomes.
        for case in ("own parent", "root parent", "unsearchable parent"):
            with self.subTest(case):
                if case == "unsearchable parent" and hasattr(os, "geteuid") and os.geteuid() == 0:
                    self.skipTest("permission fixtures do not bind the superuser (effective uid 0)")
                name = "after-exit-0-" + case.replace(" ", "-")
                if case == "root parent":
                    top = self.base / name
                    root = self._init_repo(top / "parent" / "repo", "main")
                    self.bare_remote(root, name=f"{name}/remote.git")
                    trees = [self.merged_worktree(branch, path=top / "trees" / branch, root=root)
                             for branch in NAMES[:2]]
                    changed = root.parent
                else:
                    root, trees = self.batch(name, count=2, own_parent=True)
                    changed = trees[0].parent
                planned = [self.head(tree) for tree in trees]
                aside = Path(str(changed) + ".moved")
                if case == "unsearchable parent":
                    self.addCleanup(os.chmod, changed, 0o755)
                    action = f"chmod 000 {shlex.quote(str(changed))}"
                else:
                    action = replaced_by_a_file(changed)
                env, log = self.counting(name, hooks={"post": when_target(trees[0], action)})
                result = self.run_json("clean", root, "--all-safe", "--apply", "--yes", "--json", env=env)
                if case == "unsearchable parent":
                    os.chmod(changed, 0o755)
                else:
                    self.assertTrue(changed.is_file() and aside.is_dir(), "the hook replaced the parent")
                document = result.document
                first = document["targets"][0]
                if case == "own parent":
                    self.assert_status(result, 0)
                    self.assertEqual(self.stages(document), [(str(trees[0]), "removed", None),
                                                             (str(trees[1]), "removed", None)])
                    self.assertEqual(first["reconciliation"], record(False, False, True, planned[0]))
                    self.assertEqual((document["exit_code"], document["completeness"]), (0, "complete"))
                elif case == "root parent":
                    self.assert_status(result, 1)
                    self.assertEqual(self.stages(document), [(str(trees[0]), "unknown", "unconfirmed-removal"),
                                                             (str(trees[1]), "not-attempted", "batch-stopped")])
                    self.assertEqual(first["reconciliation"], NULL_RECORD)
                    self.assertEqual((document["exit_code"], document["completeness"]), (1, "incomplete"))
                    # The identity probe failed, and the rescan read nothing more.
                    records = clean_support.child_log(log)
                    at = next(index for index, child in enumerate(records) if is_removal(child))
                    self.assertEqual([subcommand(child)[:2] for child in records[at + 1:]],
                                     [["rev-parse", "--path-format=absolute"]])
                    root = aside / "repo"
                    self.assertTrue(trees[1].is_dir())
                else:
                    self.assert_status(result, 1)
                    self.assertEqual(self.stages(document),
                                     [(str(trees[0]), "unknown", "reconciliation-incomplete"),
                                      (str(trees[1]), "not-attempted", "batch-stopped")])
                    self.assertEqual(first["reconciliation"], record(False, None, True, planned[0]))
                    self.assertEqual((document["exit_code"], document["completeness"]), (1, "incomplete"))
                    self.assertTrue(trees[1].is_dir())
                self.assertEqual((first["exit_status"], first["notes"]), (0, []))
                self.assertFalse(os.path.lexists(trees[0]), "Git removed the worktree")
                self.assertEqual(self.head(root, "refs/heads/" + NAMES[0]), planned[0], "the branch is kept")

    def test_clean_a_rescan_identity_probe_cut_before_it_answers(self):
        # Lead rulings R-82 (d) and R-78 (e), second amendment: the rescan's
        # identity probe, cut at its budget before it answers while the
        # planned root and common directory are still there by lstat, marks
        # the record, so the target is `unknown` with
        # `reconciliation-incomplete`, every field null, exit 1, and the
        # rescan reads nothing more. The same all-null record left unmarked,
        # an identity lost, stays `unconfirmed-removal`: the root parent case
        # of test_clean_a_parent_replaced_by_a_file_after_removal. A fake
        # behind the counting wrapper sleeps on `rev-parse` once the
        # post-remove hook has left its marker. Through the launcher with the
        # probe budget 1 s and the grace and the reap wait 0.5 s each (R-29),
        # so the cut comes at 1 s, inside the 10 s reserve.
        table = clean_support.timing_table(probe_budget=1.0, term_grace=0.5, reap_wait=0.5)
        root, trees = self.batch("cut-identity", count=2)
        planned = [self.head(tree) for tree in trees]
        marker = self.base / "cut-identity" / "removed.marker"
        fake = write_script(self.base / "cut-identity" / "fake-bin" / "git", (
            "#!/bin/sh\n"
            f"case \" $* \" in *\" rev-parse \"*) [ -e {quoted(marker)} ] && exec sleep 30;; esac\n"
            f"exec {quoted(REAL_GIT)} \"$@\"\n"))
        env, log = self.counting("cut-identity", hooks={"post": when_target(trees[0], f": > {quoted(marker)}")},
                                 real=fake)
        result = self.run_json("clean", root, "--all-safe", "--apply", "--yes", "--json", timing=table, env=env)
        self.assert_status(result, 1)
        document = result.document
        self.assertEqual(self.stages(document), [(str(trees[0]), "unknown", "reconciliation-incomplete"),
                                                 (str(trees[1]), "not-attempted", "batch-stopped")])
        first = document["targets"][0]
        self.assertEqual((first["exit_status"], first["reconciliation"], first["notes"]), (0, NULL_RECORD, []))
        self.assertEqual((document["exit_code"], document["completeness"]), (1, "incomplete"))
        # After the removal, the identity probe alone, cut, its group
        # terminated and reaped.
        records = clean_support.child_log(log)
        at = next(index for index, child in enumerate(records) if is_removal(child))
        rescan = records[at + 1:]
        self.assertEqual([subcommand(child)[:2] for child in rescan], [["rev-parse", "--path-format=absolute"]])
        with self.assertRaises(ProcessLookupError):
            os.killpg(rescan[0].pgid, 0)
        self.assertTrue(marker.is_file())
        self.assertTrue((root / ".git").is_dir(), "the root and its common directory are still there")
        self.assertFalse(trees[0].exists())
        self.assertTrue(trees[1].is_dir())
        self.assertEqual(self.head(root, "refs/heads/" + NAMES[0]), planned[0], "the branch is kept")

    # T090: decide_stage()'s stage and reason table.

    def test_clean_stage_and_reason_table(self):
        # data-model.md, "Target stages", as literals; project's table equals it.
        stages = {
            "removed": (None, "branch-advanced-after-removal", "branch-missing-after-removal", "removal-ceiling"),
            "refused": ("identity-changed", "branch-changed", "state-changed", "contains-submodule",
                        "hidden-local-state"),
            "failed": ("git-refused", "git-failed", "spawn-error"),
            "unknown": ("unconfirmed-removal", "reconciliation-incomplete", "internal-error", "removal-ceiling"),
            "not-attempted": ("batch-stopped", "interrupted", "deadline-exceeded"),
        }
        self.assertEqual(project.STAGE_REASONS, stages)
        # decide_stage() decides a spawned target only, with the signature T056
        # gave it (lead ruling R-68 (c)). The refused and not-attempted pairs
        # are revalidate()'s and apply_removals()'s, and unknown with
        # internal-error is apply_removals()' handling of an exception (lead
        # ruling R-83, P-7), so these ten pairs are every one it can reach.
        spawned = {("removed", None), ("removed", "branch-advanced-after-removal"),
                   ("removed", "branch-missing-after-removal"), ("removed", "removal-ceiling"),
                   ("failed", "git-refused"), ("failed", "git-failed"), ("failed", "spawn-error"),
                   ("unknown", "unconfirmed-removal"), ("unknown", "reconciliation-incomplete"),
                   ("unknown", "removal-ceiling")}
        sha, other = "a" * 40, "b" * 40
        target = {"planned_sha": sha}
        outcome = project.DriverOutcome
        exited = outcome(["git"], "complete", status=0)
        killed = outcome(["git"], "timeout", status=-signal.SIGKILL)  # outlived SIGTERM at the ceiling: 137
        termed = outcome(["git"], "timeout", status=-signal.SIGTERM)  # ended by SIGTERM at the ceiling: 143
        unobserved = outcome(["git"], "timeout", detail="the child did not end after SIGKILL")
        gone, kept = record(False, False, True, sha), record(True, True, True, sha)

        def unfinished(*values):
            return project.UnfinishedRescan(record(*values))

        cases = [
            # Exit 0: the rescan proves the removal, or the target is unknown.
            (exited, gone, ("removed", None, [])),
            (exited, record(False, False, True, other), ("removed", "branch-advanced-after-removal", [])),
            (exited, record(False, False, False, None), ("removed", "branch-missing-after-removal", [])),
            (exited, kept, ("unknown", "unconfirmed-removal", [])),
            (exited, record(False, True, True, sha), ("unknown", "unconfirmed-removal", [])),
            (exited, record(None, None, None, None), ("unknown", "unconfirmed-removal", [])),
            (exited, record(False, False, None, None), ("unknown", "reconciliation-incomplete", [])),
            (exited, unfinished(None, False, True, sha), ("unknown", "reconciliation-incomplete", [])),
            (exited, unfinished(False, None, True, sha), ("unknown", "reconciliation-incomplete", [])),
            (exited, unfinished(None, None, None, None), ("unknown", "reconciliation-incomplete", [])),
            # Exited nonzero on its own, a signal death included: failed, Git's status.
            (outcome(["git"], "failed", status=128), kept, ("failed", "git-refused", [])),
            (outcome(["git"], "failed", status=1), kept, ("failed", "git-failed", [])),
            (outcome(["git"], "failed", status=255), record(False, True, True, sha), ("failed", "git-failed", [])),
            (outcome(["git"], "failed", status=-signal.SIGTERM), gone, ("failed", "git-failed", [])),
            # Never spawned.
            (outcome(["git"], "failed", detail="cannot run git: [Errno 2] No such file"), kept,
             ("failed", "spawn-error", [])),
            # Cut at the ceiling, or its exit not observed: the rescan decides.
            (killed, gone, ("removed", "removal-ceiling", [])),
            (termed, record(False, False, True, other), ("removed", "removal-ceiling", [])),
            (unobserved, gone, ("removed", "removal-ceiling", [])),
            (killed, kept, ("unknown", "removal-ceiling", ["partially-removed"])),
            (termed, record(False, True, True, sha), ("unknown", "removal-ceiling", ["partially-removed"])),
            (unobserved, record(True, False, True, sha), ("unknown", "removal-ceiling", ["partially-removed"])),
            (killed, record(False, False, None, None), ("unknown", "removal-ceiling", [])),
            (killed, unfinished(None, None, None, None), ("unknown", "removal-ceiling", [])),
        ]
        reached = set()
        for given, reconciliation, expected in cases:
            with self.subTest(outcome=given, reconciliation=reconciliation,
                              marked=isinstance(reconciliation, project.UnfinishedRescan)):
                decided = project.decide_stage(target, given, reconciliation)
                self.assertEqual(decided, expected)
                self.assertIn(decided[1], stages[decided[0]])
                # orphaned-directory is never decide_stage()'s (lead ruling R-83, P-5).
                self.assertLessEqual(set(decided[2]), {"partially-removed"})
                reached.add(decided[:2])
        self.assertEqual(reached, spawned)

        # A child that exits nonzero on its own is failed whatever the slot
        # holds; only a child killed at the ceiling, or whose exit was not
        # observed, is decided by the rescan (D15; pcl:910-915).
        for signum in (None, signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            with self.subTest(slot=signum and signal.Signals(signum).name), project.Invocation("clean") as run:
                if signum is not None:
                    run.record_signal(signum)
                for status in (1, 128, 255, -signal.SIGINT, -signal.SIGTERM, -signal.SIGHUP, -signal.SIGKILL):
                    given = outcome(["git"], "failed", status=status)
                    reason = "git-refused" if status == 128 else "git-failed"
                    for reconciliation in (gone, kept, unfinished(None, None, None, None)):
                        self.assertEqual(project.decide_stage(target, given, reconciliation), ("failed", reason, []))
                for given in (killed, termed, unobserved):
                    self.assertNotEqual(project.decide_stage(target, given, gone),
                                        project.decide_stage(target, given, kept))

    # Lead ruling R-101 (b): the runner review's F1 and F2.

    def run_with_failing_stderr(self, argv, failure):
        """Run argv with standard input empty, standard output on a pipe, and
        standard error failing: on /dev/full for ENOSPC, or for EPIPE on a pipe
        whose read end is closed before the child starts. Returns the exit
        status and standard output as text."""
        if failure == "ENOSPC":
            if not os.path.exists("/dev/full"):
                self.skipTest("no /dev/full on this host")
            stderr = os.open("/dev/full", os.O_WRONLY)
        else:
            read_end, stderr = os.pipe()
            os.close(read_end)
        try:
            child = subprocess.Popen(argv, cwd=self.base, env=self.env, stdin=subprocess.DEVNULL,
                                     stdout=subprocess.PIPE, stderr=stderr, start_new_session=True)
        finally:
            os.close(stderr)
        try:
            out, _ = child.communicate(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            with contextlib.suppress(OSError):
                os.killpg(child.pid, signal.SIGKILL)
            child.communicate()
            self.fail(f"project did not end within {TIMEOUT} s")
        return child.returncode, out.decode("utf-8", "surrogateescape")

    def test_clean_apply_with_json_prints_one_document_when_standard_error_fails(self):
        # Runner review F1 (lead ruling R-101 (b)): under --apply --json the
        # human plan goes to standard error. When that write fails before the
        # apply phase, with ENOSPC (/dev/full) or with EPIPE (a reader that
        # closed), the run ends as `internal-error`, exit 2 (lead ruling R-55),
        # and standard output holds exactly one document, the extended error
        # object, with no plan envelope before it (pcl:1133-1135); nothing is
        # removed. Two stops before the apply phase: the question a run
        # without --yes needs (confirmation-required), and the scenario's own,
        # a stale --expect-plan (plan-digest-mismatch).
        root, trees = self.batch("stderr-fails", count=2)
        before = self.snapshot(root, trees)
        stops = (("confirmation-required", ()), ("plan-digest-mismatch", ("--yes", "--expect-plan", "0" * 64)))
        for failure, number in (("ENOSPC", errno.ENOSPC), ("EPIPE", errno.EPIPE)):
            for stop, extra in stops:
                with self.subTest(failure=failure, stop=stop):
                    argv = clean_support.cli_argv("clean", root, "--all-safe", "--apply", "--json", *extra)
                    status, out = self.run_with_failing_stderr(argv, failure)
                    documents = json_documents(out)
                    self.assertEqual(len(documents), 1, f"exit {status}, standard output:\n{out}")
                    [document] = documents
                    self.assertEqual(status, 2, out)
                    self.assertEqual(list(document)[:2], ["error", "code"], "the extended error object")
                    self.assertEqual((document["code"], [refusal["code"] for refusal in document["refusals"]]),
                                     ("internal-error", ["internal-error"]))
                    self.assertIn(f"[Errno {number}]", document["error"], "the failed write's own error")
                    self.assertEqual(self.snapshot(root, trees), before, "nothing removed")

    def test_clean_a_signal_during_a_removal_ignored_on_entry_stays_ignored(self):
        # Runner review F2 (lead ruling R-101 (b)): a signal whose disposition
        # is SIG_IGN when project starts, as nohup leaves SIGHUP and a `&` job
        # of a non-interactive shell leaves SIGINT, stays ignored, as by
        # convention and in the baseline; FR-036 reaches only a signal the
        # caller did not ignore. The scenario's run, as
        # test_clean_a_signal_during_a_removal makes it, with the signal set to
        # SIG_IGN in the child before it execs (a preexec_fn of the test's
        # own) and sent to project alone once the second removal is in
        # flight: no target is interrupted, all three
        # are removed, the record's exit_code is 0 and the run exits 0, with
        # no wait line and no `Cancelled.`. The real table.
        table = clean_support.timing_table()
        for signum in (signal.SIGHUP, signal.SIGINT):
            name = signal.Signals(signum).name
            with self.subTest(signal=name):
                case = f"ignored-{name.lower()}"
                root, trees = self.batch(case)
                bin_dir, log = self.base / case / "fake-bin", self.base / case / "signals.log"
                signal_recording_git(bin_dir, log, slow=trees[1], seconds=1.5)

                def ignore(signum=signum):
                    signal.signal(signum, signal.SIG_IGN)

                result = self.run_signalled(
                    clean_support.launched_argv(table, "clean", root, "--all-safe", "--apply", "--yes", "--json"),
                    self.path_first(bin_dir), [(lambda: f"ready {trees[1]}" in log_lines(log), signum)],
                    preexec_fn=ignore)
                self.assert_status(result, 0)
                document = result.document
                self.assertIsNotNone(document, clean_support.transcript(result))
                self.assertEqual(self.stages(document), [(str(tree), "removed", None) for tree in trees])
                self.assertEqual(document["exit_code"], 0)
                self.assertFalse(any(tree.exists() for tree in trees))
                self.assertNotIn(CANCELLED, result.stderr.splitlines())
                self.assertNotIn("Waiting for git worktree remove", result.stderr)
                # The signal went while the second removal ran, and every
                # removal then ran to its end.
                lines = log_lines(log)
                self.assertEqual([line for line in lines if line.startswith("ready ")],
                                 [f"ready {tree}" for tree in trees])
                self.assertEqual([line for line in lines if line.startswith("exited ")],
                                 [f"exited {tree} 0" for tree in trees])


if __name__ == "__main__":
    unittest.main()
