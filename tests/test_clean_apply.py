"""The apply lane of feature 004's User Story 1 (T041 to T046 and T054 to T057):
the removal question, the revalidation, the removal child, the rescan, the
target's stage, the result and its exit status (design D7, D9, D15, D18 and D19;
research.md R3 and R4; data-model.md, "Target stages", "Target result and
reconciliation record" and "Exit statuses"; contracts/project-clean.md, "The
removal question", "Streams", "Apply result record" and "Exit statuses"; lead
rulings R-55 and R-56).

The unit tests call project's functions in process, on literal values or on a
disposable repository, with os.environ replaced by CleanCase's environment and
an Invocation entered; no signal is ever sent to the test process (rule 7).
Expected human text comes from clean_support's fixtures (rule 8), and the
contract's key tuples are written here as literals.
"""
import contextlib
import io
import os
from pathlib import Path
import re
import signal
import time
import types
import unittest
from unittest import mock

import clean_support

project = clean_support.load_project()
TEXT = clean_support.TEXT_FIXTURES

# The contract's key order of the apply result record, a target result and a
# reconciliation record (contracts/project-clean.md, "Apply result record";
# data-model.md, "Target result and reconciliation record").
APPLY_RESULT_KEYS = ["schema_version", "observed_at", "repository", "merge_target", "plan_digest",
                     "probes", "operations", "targets", "exit_code", "completeness"]
TARGET_RESULT_KEYS = ["path", "path_valid_utf8", "branch", "planned_sha", "stage", "reason", "notes",
                      "command", "exit_status", "probes_performed", "reconciliation"]
RECONCILIATION_KEYS = ["registry_entry_present", "path_present", "branch_present", "branch_sha",
                       "reconciled"]
OBSERVED_AT = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")

# The removal child's pins, as the contract writes them ("Git children"): the
# three status pins, then the seven protocol pins, before `-C ROOT`.
PROTOCOL_PINS = ["-c", "protocol.allow=never", "-c", "protocol.file.allow=never",
                 "-c", "protocol.ssh.allow=never", "-c", "protocol.git.allow=never",
                 "-c", "protocol.http.allow=never", "-c", "protocol.https.allow=never",
                 "-c", "protocol.ext.allow=never"]
REMOVAL_PINS = ["-c", "status.showUntrackedFiles=normal", "-c", "core.untrackedCache=false",
                "-c", "core.fsmonitor=false", *PROTOCOL_PINS]
# The rescan's three children after `-C ROOT` (design D6, rows 3, 4 and 6).
ROW_3 = ["rev-parse", "--path-format=absolute", "--show-toplevel", "--git-common-dir",
         "--show-superproject-working-tree"]
ROW_4 = ["worktree", "list", "--porcelain", "-z"]
ROW_6 = ["for-each-ref", "--format=%(refname)%00%(objectname)%00%(symref)%00%(upstream)"
         "%00%(upstream:short)%00%(upstream:track,nobracket)", "refs/heads", "refs/remotes"]

SCOPED_SIGNALS = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)
SHA_A, SHA_B, SHA_C = "a" * 40, "b" * 40, "c" * 40


def strip_pins(argv):
    """A child's argument vector, as the counting wrapper records it (after
    `git`), split into its leading `-c NAME=VALUE` pins and the rest."""
    at = 0
    while at + 1 < len(argv) and argv[at] == "-c":
        at += 2
    return list(argv[:at]), list(argv[at:])


def signal_state():
    """The handlers of SIGINT, SIGTERM and SIGHUP and the wakeup descriptor."""
    handlers = tuple(signal.getsignal(signum) for signum in SCOPED_SIGNALS)
    wakeup = signal.set_wakeup_fd(-1)
    if wakeup != -1:
        signal.set_wakeup_fd(wakeup)
    return handlers, wakeup


def record(registry_entry_present=False, path_present=False, branch_present=True, branch_sha=SHA_A):
    """A reconciliation record, as project builds it (reconciled derived)."""
    return project.reconciliation_record(registry_entry_present, path_present, branch_present, branch_sha)


def target(stage, reason=None, exit_status=None, path=b"/w/a", branch="a", sha=SHA_A, notes=(),
           reconciliation="default", probes_performed=5):
    """A literal target result as the apply phase keeps it (region apply,
    Target): `path` raw bytes, `command` the planned vector. A
    `not-attempted` target has no reconciliation by default; any other the
    record of a clean removal."""
    if reconciliation == "default":
        reconciliation = None if stage == "not-attempted" else record()
    return {"path": path, "branch": branch, "planned_sha": sha, "stage": stage, "reason": reason,
            "notes": list(notes), "command": ["git", *REMOVAL_PINS, "-C", b"/r", "worktree", "remove", path],
            "exit_status": exit_status, "probes_performed": probes_performed,
            "reconciliation": reconciliation}


class RaisingStream(io.StringIO):
    """A human stream whose writes fail as a closed pipe's do."""

    def write(self, text):
        raise BrokenPipeError(32, "Broken pipe")


class ApplyTests(clean_support.CleanCase):

    @contextlib.contextmanager
    def in_process(self, env=None, command=None):
        """os.environ replaced by env (self.env by default) and a fresh
        Invocation entered for the block's span; yields the Invocation. The
        signal handlers and wakeup descriptor must be as they were after it."""
        before = signal_state()
        try:
            with mock.patch.dict(os.environ, self.env if env is None else env, clear=True), \
                    project.Invocation(command) as run:
                yield run
        finally:
            self.assertEqual(signal_state(), before, "the call left the signal handlers changed")

    # Fixtures: eligible worktrees, each a commit of its own (merged_worktree(),
    # lead ruling R-56), and the plan the in-process tests act on.

    def merged_repository(self, *branches):
        """A repository with an origin and one merged, clean, published
        worktree per branch; returns (root, {branch: path})."""
        root = self.repo()
        self.bare_remote()
        return root, {branch: self.merged_worktree(branch) for branch in branches}

    def plan_of(self, root, run, trees):
        """The Plan of root that T049 builds, as far as the apply phase reads it
        (region dispatcher, Plan): the evidence, the rows, the merge target and
        trees selected in canonical order, each eligible and given its removal
        arguments, ["-C", ROOT, "worktree", "remove", PATH] with PATH the
        registry's raw bytes (design D9)."""
        evidence = project.inspect_repository(os.fsencode(root), run)
        rows = project.worktree_rows(evidence, run)
        plan = project.Plan({"root": root}, types.SimpleNamespace(mode="all-safe", action="remove"))
        plan.evidence, plan.rows = evidence, rows
        plan.merge_target = {key: evidence["merge_target"][key] for key in ("name", "source", "sha")}
        by_path = {row.raw_path: row for row in rows}
        plan.selected = [by_path[os.fsencode(tree)] for tree in sorted(map(os.fsencode, trees))]
        for row in plan.selected:
            self.assertEqual(row["classification"], "merged-removable", row)
            row.removal_args = ["-C", os.fsencode(root), "worktree", "remove", row.raw_path]
        plan.digest = "0" * 64
        return plan

    def snapshot(self, root, trees=()):
        """What a run that removes nothing leaves as it found it: the registry,
        every ref with its object, and the files of each tree (its `.git` file
        aside)."""
        files = {}
        for tree in trees:
            tree = Path(tree)
            files[str(tree)] = sorted(str(path.relative_to(tree)) for path in tree.rglob("*")
                                      if path.name != ".git") if tree.exists() else None
        return (self.git(root, "worktree", "list", "--porcelain"),
                self.git(root, "for-each-ref", "--format=%(refname) %(objectname)"), files)

    def head(self, path, ref="HEAD"):
        return self.git(path, "rev-parse", ref).strip()

    # T054: the removal question.

    def test_clean_ask_removal_writes_the_question_and_reads_one_line(self):
        # Research.md R3: the question is written by project to the human
        # stream and flushed, then one line is read by input() with no prompt,
        # so standard output carries nothing under --apply --json.
        for count, question in ((7, TEXT["question"].format(N=7)), (1, TEXT["question_one"])):
            with self.subTest(count=count), self.in_process() as run:
                run.human, out = io.StringIO(), io.StringIO()
                calls = []

                def answer(*args):
                    calls.append((args, run.human.getvalue()))
                    return " yes "

                plan = types.SimpleNamespace(selected=[object()] * count)
                with mock.patch.object(project, "input", answer, create=True), contextlib.redirect_stdout(out):
                    line = project.ask_removal(plan, run)
                self.assertEqual(line, " yes ")  # as read; confirm_removal() strips it
                self.assertEqual(calls, [((), question + "\n")])
                self.assertEqual(run.human.getvalue(), question + "\n")
                self.assertEqual(out.getvalue(), "")
        self.assertEqual(TEXT["question"].format(N=7), "Remove 7 worktrees, keeping 7 branches? [yes/N]")

    def test_clean_ask_removal_runs_under_raising_signals_with_the_clock_paused(self):
        # D1, D15 and research.md R4: the question alone runs under raising
        # handlers; FR-031: the time at the question is not counted.
        before = signal_state()
        with self.in_process(command="clean") as run:
            run.human = io.StringIO()
            seen = {}

            def answer():
                seen["handlers"] = {signum: signal.getsignal(signum) for signum in SCOPED_SIGNALS}
                first = run.now()
                time.sleep(0.05)
                seen["still"] = run.now() == first
                return "no"

            work_end = run.work_end
            with mock.patch.object(project, "input", answer, create=True):
                self.assertEqual(project.ask_removal(types.SimpleNamespace(selected=[1, 2]), run), "no")
            self.assertTrue(seen["still"], "the clock ran while the question waited")
            self.assertGreaterEqual(run.work_end - work_end, 0.05)
            self.assertEqual(signal_state(), before)
            # The handlers in force at the question record the signal and raise.
            with self.assertRaises(KeyboardInterrupt):
                seen["handlers"][signal.SIGINT](signal.SIGINT, None)
            self.assertEqual(run.signal, signal.SIGINT)
            for signum in (signal.SIGTERM, signal.SIGHUP):
                with self.assertRaises(project.Terminated):
                    seen["handlers"][signum](signum, None)

        # End of input passes to main(), which prints `Cancelled.` and exits 130;
        # the handlers and the clock are restored on the way out.
        with self.in_process(command="clean") as run:
            run.human = io.StringIO()

            def ended():
                raise EOFError

            with mock.patch.object(project, "input", ended, create=True), self.assertRaises(EOFError):
                project.ask_removal(types.SimpleNamespace(selected=[1]), run)
            first = run.now()  # the clock runs again
            time.sleep(0.01)
            self.assertGreater(run.now(), first)

        # A signal already in the slot raises before the question is written.
        with self.in_process(command="clean") as run:
            run.human = io.StringIO()
            run.record_signal(signal.SIGTERM)
            with mock.patch.object(project, "input", lambda: self.fail("input() was called"), create=True), \
                    self.assertRaises(project.Terminated):
                project.ask_removal(types.SimpleNamespace(selected=[1]), run)
            self.assertEqual(run.human.getvalue(), "")

    def test_clean_ask_removal_never_reads_after_a_failed_write(self):
        # Lead ruling R-55: a question that could not be written is not
        # answered; the failed write is recorded for the check after it.
        with self.in_process() as run:
            run.human = RaisingStream()
            with mock.patch.object(project, "input", lambda: self.fail("input() was called"), create=True):
                self.assertEqual(project.ask_removal(types.SimpleNamespace(selected=[1]), run), "")
            self.assertIsInstance(run.write_error, BrokenPipeError)

    # T055: revalidation reads afresh.

    def test_clean_revalidate_passes_an_unchanged_target(self):
        root, trees = self.merged_repository("001-a", "002-b")
        with self.in_process() as run:
            plan = self.plan_of(root, run, trees.values())
            before = self.snapshot(root, trees.values())
            for row in plan.selected:
                with self.subTest(path=row["path"]):
                    entry = project.make_target(plan, row)
                    self.assertIsNone(project.revalidate(plan, entry, run))
                    # Rows 3, 4, 6 and 7 again, never the memo, and the target's status.
                    self.assertEqual(entry["probes_performed"], 5)
            self.assertEqual(self.snapshot(root, trees.values()), before)

    def test_clean_revalidate_refuses_a_changed_target_with_state_changed(self):
        # Lead ruling R-56 Q-13: the memo would hand back the planned evidence,
        # so each change below is seen only by a fresh read.
        names = ("001-dirty", "002-locked", "003-gone", "004-identity")
        root, trees = self.merged_repository(*names)
        with self.in_process() as run:
            plan = self.plan_of(root, run, trees.values())
            entries = {Path(os.fsdecode(row.raw_path)).name: project.make_target(plan, row)
                       for row in plan.selected}
            heads = {name: self.head(trees[name]) for name in names}

            (trees["001-dirty"] / "late-change").write_text("preserve")
            self.git(root, "worktree", "lock", trees["002-locked"])
            self.git(root, "worktree", "remove", trees["003-gone"])
            expected = {
                "001-dirty-tree": record(True, True, True, heads["001-dirty"]),
                "002-locked-tree": record(True, True, True, heads["002-locked"]),
                "003-gone-tree": record(False, False, True, heads["003-gone"]),
            }
            for name, reconciliation in expected.items():
                with self.subTest(name):
                    self.assertEqual(project.revalidate(plan, entries[name], run),
                                     ("state-changed", reconciliation))
            self.assertTrue((trees["001-dirty"] / "late-change").is_file())

            # Another repository identity: the listings are not this repository's,
            # so only the path's own lstat is read.
            entry = entries["004-identity-tree"]
            moved = dict(plan.evidence, identity=dict(plan.evidence["identity"], ino=-1))
            with mock.patch.object(plan, "evidence", moved):
                self.assertEqual(project.revalidate(plan, entry, run),
                                 ("state-changed", record(None, True, None, None)))
            self.assertIsNone(project.revalidate(plan, entry, run))

            # The merge target advances: every target differs.
            self.git(root, "commit", "-q", "--allow-empty", "-m", "advance the merge target")
            self.assertEqual(project.revalidate(plan, entry, run),
                             ("state-changed", record(True, True, True, heads["004-identity"])))


if __name__ == "__main__":
    unittest.main()
