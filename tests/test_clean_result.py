"""The removal lane of feature 004's User Story 5 (T087 to T090): every removal
ends in a reconcilable record (design D9, D15, D18 and D19; the project-clean
delta, "Clean can explicitly retire verified worktrees" and "Clean records a
reconcilable result for every removal target"; data-model.md, "Signal slot",
"Target result and reconciliation record" and "Target stages"; research.md R4
and R6; lead rulings R-29, R-44, R-68, R-76, R-82 and R-83).

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

    def run_signalled(self, argv, env, steps):
        """Run argv, project through the launcher, in a session of its own with
        both streams on pipes read as they fill; for each (ready, signum) of
        steps in turn, poll ready() until it holds, then send signum to project
        alone (rule 7). Returns a CompletedProcess with text streams, its
        document parsed when standard output holds one."""
        child = subprocess.Popen(argv, cwd=self.base, env=env, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
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
        # exit 130 with nothing removed.
        root, trees = self.batch("question", count=2)
        before = self.snapshot(root, trees)
        argv = clean_support.launched_argv(table, "clean", root, "--all-safe", "--apply")
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


if __name__ == "__main__":
    unittest.main()
