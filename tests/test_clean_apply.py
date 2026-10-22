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
The command-line tests (T041 to T044, Q-5's two moved clauses and R-59 D2's
apply side) run `project clean` as a child, under the counting wrapper where
they count children, at a pseudo-terminal where they answer the question.
Expected human text comes from clean_support's fixtures (rule 8), and the
contract's key tuples are written here as literals.
"""
import contextlib
import io
import json
import os
from pathlib import Path
import re
import shlex
import signal
import subprocess
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
# five status pins, then the seven protocol pins, before `-C ROOT`.
PROTOCOL_PINS = ["-c", "protocol.allow=never", "-c", "protocol.file.allow=never",
                 "-c", "protocol.ssh.allow=never", "-c", "protocol.git.allow=never",
                 "-c", "protocol.http.allow=never", "-c", "protocol.https.allow=never",
                 "-c", "protocol.ext.allow=never"]
REMOVAL_PINS = ["-c", "status.showUntrackedFiles=normal", "-c", "core.untrackedCache=false",
                "-c", "core.fsmonitor=false", "-c", "core.trustctime=true", "-c", "core.checkStat=default",
                *PROTOCOL_PINS]
# The rescan's three children after `-C ROOT` (design D6, rows 3, 4 and 6).
ROW_3 = ["rev-parse", "--path-format=absolute", "--show-toplevel", "--git-common-dir",
         "--show-superproject-working-tree"]
ROW_4 = ["worktree", "list", "--porcelain", "-z"]
ROW_6 = ["for-each-ref", "--format=%(refname)%00%(objectname)%00%(symref)%00%(upstream)"
         "%00%(upstream:short)%00%(upstream:track,nobracket)", "refs/heads", "refs/remotes"]

SCOPED_SIGNALS = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)
SHA_A, SHA_B, SHA_C = "a" * 40, "b" * 40, "c" * 40
FRESHNESS = "local refs only; remote information is as of the last fetch; no fetch performed"
# The baseline's message of a refused confirmation, kept for `cancelled`
# (contracts/project-clean.md, "Codes"; lead ruling R-68 (a)).
CANCELLED = "Cancelled; no command was run."


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


def removals(records):
    """The counted `worktree remove` children, in the order they started."""
    return [record for record in records if subcommand(record)[:2] == ["worktree", "remove"]]


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

    # The command-line tests' fixtures and helpers (inline fixtures, lead
    # ruling R-56).

    def remote_ahead_worktree(self, branch):
        """A merged, clean worktree whose upstream holds one commit more than
        its branch: a second commit pushed, then the branch reset to the first,
        so `behind` is 1 and `ahead` 0 (class `remote-ahead`)."""
        tree = self.merged_worktree(branch)
        (tree / "later").write_text("later")
        self.commit(tree)
        self.git(tree, "push", "origin", branch)
        self.git(tree, "reset", "-q", "--hard", "HEAD~1")
        return tree

    def unmerged_worktree(self, branch):
        """A clean worktree whose branch has a commit of its own, published and
        never merged (class `pushed-unmerged`)."""
        tree = self._tree(branch, None)
        self.git(self.root, "worktree", "add", "-b", branch, tree)
        (tree / ("work-" + branch)).write_text("review")
        self.commit(tree)
        self.git(tree, "push", "-u", "origin", branch)
        return tree

    def counting(self, env=None):
        """The counting wrapper first on PATH, in front of the real git: the
        environment to run with and the log, emptied."""
        bin_dir, log = self.base / "counting-bin", self.base / "children.log"
        clean_support.install_counting_git(bin_dir, log)
        clean_support.reset_child_log(log)
        return self.path_first(bin_dir, env), log

    def branches(self, root):
        """Every local branch with its object, as one text."""
        return self.git(root, "for-each-ref", "--format=%(refname) %(objectname)", "refs/heads")

    def plan_lines(self, root, selected, excluded=()):
        """D18's printed plan of an --all-safe run: the baseline header, the
        selected rows (path, branch), the excluded groups (reason, [(path,
        branch)]) with the main worktree's first, and the residual-window line."""
        steps = clean_support.NEXT_STEP_FIXTURES
        groups = [("main-worktree", [(root, "main")]), *excluded]
        lines = [f"Cleanup plan for {root}", TEXT["merge_target_line"].format(NAME="main", SOURCE="main"),
                 f"Freshness: {FRESHNESS}", TEXT["selected_heading"].format(N=len(selected))]
        lines += [TEXT["selected_row"].format(PATH=path, BRANCH=branch) for path, branch in selected]
        lines.append(TEXT["excluded_heading"].format(M=sum(len(rows) for _, rows in groups)))
        for reason, rows in groups:
            lines.append(TEXT["excluded_group"].format(REASON=reason, K=len(rows), NEXT_STEP=steps[reason]))
            lines += [TEXT["excluded_row"].format(PATH=path, BRANCH=branch) for path, branch in rows]
        return lines + [TEXT["residual_window_line"]]

    def result_lines(self, selected):
        """The result of a batch that removed every selected (path, branch):
        one progress line each, the success line and the residual-window line."""
        lines = [TEXT["progress_line"].format(STAGE="removed", PATH=path) for path, _ in selected]
        return lines + [TEXT["success_line"].format(N=len(selected), BRANCHES=", ".join(b for _, b in selected)),
                        TEXT["residual_window_line"]]

    # T045: D19's exit table and the apply result record.

    def test_clean_apply_exit_table(self):
        # D19's rows in order (lead ruling R-56 Q-8): the signal row first, since
        # it needs the slot; then 1; then Git's own status; then 2; then 0.
        removed = target("removed", path=b"/w/a")
        later = target("not-attempted", "batch-stopped", path=b"/w/c", branch="c")
        cases = [
            # 130, 143 or 129: the first signal decides, whatever the targets say.
            ("SIGINT over a clean batch", [removed], signal.SIGINT, 130),
            ("SIGTERM over an unknown target", [target("unknown", "unconfirmed-removal"), later],
             signal.SIGTERM, 143),
            ("SIGHUP over a failed target", [target("failed", "git-refused", 128), later], signal.SIGHUP, 129),
            ("SIGINT stopping the batch", [removed, target("not-attempted", "interrupted", path=b"/w/b"),
                                           target("not-attempted", "interrupted", path=b"/w/c")],
             signal.SIGINT, 130),
            # 1: the deadline after the apply phase began, an unknown target, a ceiling.
            ("deadline", [removed, target("not-attempted", "deadline-exceeded", path=b"/w/b")], None, 1),
            ("unknown", [removed, target("unknown", "unconfirmed-removal", 0, path=b"/w/b"), later], None, 1),
            ("unknown before a failed status", [target("unknown", "reconciliation-incomplete", 0),
                                                target("failed", "git-failed", 255, path=b"/w/b")], None, 1),
            ("ceiling, removed", [target("removed", "removal-ceiling", 137), later], None, 1),
            ("ceiling, unknown", [target("unknown", "removal-ceiling", 137, notes=["partially-removed"]), later],
             None, 1),
            # Git's own status, passed through even when it is one of project's.
            ("git-refused", [removed, target("failed", "git-refused", 128, path=b"/w/b"), later], None, 128),
            ("git-failed", [target("failed", "git-failed", 255, notes=["orphaned-directory"]), later], None, 255),
            ("git-failed 1", [target("failed", "git-failed", 1), later], None, 1),
            ("git-failed 2", [target("failed", "git-failed", 2), later], None, 2),
            ("git-failed by a signal", [target("failed", "git-failed", 137), later], None, 137),
            ("Git's status before a refusal", [target("failed", "git-failed", 3),
                                               target("refused", "state-changed", path=b"/w/b")], None, 3),
            # 2: a refused target, a branch-after-removal reason, spawn-error.
            ("refused", [removed, target("refused", "state-changed", path=b"/w/b"), later], None, 2),
            ("identity-changed", [target("refused", "identity-changed"), later], None, 2),
            ("branch advanced", [target("removed", "branch-advanced-after-removal"), later], None, 2),
            ("branch missing", [target("removed", "branch-missing-after-removal"), later], None, 2),
            ("spawn-error", [target("failed", "spawn-error"), later], None, 2),
            # 0: every target removed with reason null, or nothing eligible.
            ("clean batch", [removed, target("removed", path=b"/w/b"), target("removed", path=b"/w/c")], None, 0),
            ("nothing eligible", [], None, 0),
        ]
        for name, targets, signum, expected in cases:
            with self.subTest(name):
                self.assertEqual(project.apply_exit_status(targets, signum), expected)
        # A list no row matches, which the apply phase never builds, fails closed.
        self.assertEqual(project.apply_exit_status([target("pending")], None), 2)

    def test_clean_result_document_keys(self):
        # Plan review M12: exit_status is null unless a child was spawned and
        # reaped, Git's own status when it exited, and 128 plus the signal
        # number when a signal ended it, whoever sent it: 137 at the ceiling.
        outcome = project.DriverOutcome
        statuses = [
            (outcome(["git"], "complete", status=0), 0),
            (outcome(["git"], "failed", status=128), 128),
            (outcome(["git"], "failed", status=255), 255),
            (outcome(["git"], "failed", status=-signal.SIGINT), 130),
            (outcome(["git"], "failed", status=-signal.SIGTERM), 143),
            (outcome(["git"], "timeout", status=-signal.SIGKILL), 137),
            (outcome(["git"], "failed", detail="cannot run git: [Errno 2] No such file"), None),
            (outcome(["git"], "timeout", detail="the child did not end after SIGKILL"), None),
        ]
        for given, expected in statuses:
            with self.subTest(outcome=given):
                self.assertEqual(project.removal_exit_status(given), expected)

        orphaned = record(registry_entry_present=False, path_present=True)
        targets = [
            target("removed", exit_status=0, path=b"/w/a"),
            target("failed", "git-failed", 255, path=b"/w/b", branch="b", sha=SHA_B, notes=["orphaned-directory"],
                   reconciliation=orphaned),
            target("not-attempted", "batch-stopped", path=b"/w/c\xff", branch="c", sha=SHA_C, probes_performed=0,
                   reconciliation=record()),
        ]
        repository = {"root": "/r", "common_dir": "/r/.git", "dev": 1, "ino": 2, "root_valid_utf8": True,
                      "common_dir_valid_utf8": True}
        merge_target = {"name": "main", "source": "main", "sha": SHA_A}
        context = {"repository": repository, "merge_target": merge_target, "plan_digest": "d" * 64,
                   "probes": {"estimated": 30, "performed": 21}, "operations": {"estimated": 3, "performed": 2}}
        document = project.result_document(targets, 255, **context)
        self.assertEqual(list(document), APPLY_RESULT_KEYS)
        self.assertEqual(document["schema_version"], 1)
        self.assertRegex(document["observed_at"], OBSERVED_AT)
        for key, value in context.items():
            self.assertEqual(document[key], value, key)
        self.assertEqual(document["exit_code"], 255)
        self.assertEqual(document["completeness"], "complete")
        written = json.loads(json.dumps(document, indent=2, ensure_ascii=True))
        self.assertEqual(written, document)
        first, failed, skipped = document["targets"]
        for entry in document["targets"]:
            self.assertEqual(list(entry), TARGET_RESULT_KEYS)
        self.assertEqual(first["path"], "/w/a")
        self.assertIs(first["path_valid_utf8"], True)
        self.assertEqual(first["command"], ["git", *REMOVAL_PINS, "-C", "/r", "worktree", "remove", "/w/a"])
        self.assertEqual(first["exit_status"], 0)
        self.assertEqual(list(first["reconciliation"]), RECONCILIATION_KEYS)
        self.assertEqual(first["reconciliation"], {"registry_entry_present": False, "path_present": False,
                                                   "branch_present": True, "branch_sha": SHA_A, "reconciled": True})
        self.assertEqual((failed["stage"], failed["reason"], failed["exit_status"], failed["notes"]),
                         ("failed", "git-failed", 255, ["orphaned-directory"]))
        self.assertTrue(failed["reconciliation"]["path_present"])
        # A not-attempted target: no reconciliation, no exit status, its path
        # escaped with its flag beside it (FR-041).
        self.assertIsNone(skipped["reconciliation"])
        self.assertIsNone(skipped["exit_status"])
        self.assertEqual((skipped["path"], skipped["path_valid_utf8"]), ("/w/c\\xff", False))
        self.assertEqual(skipped["command"][-1], "/w/c\\xff")

        # Every removed, refused, failed or unknown target carries an object;
        # one that read nothing has every field null and is not reconciled.
        cases = [target("refused", "state-changed", reconciliation=record(True, True, True, SHA_A)),
                 target("unknown", "unconfirmed-removal", 0, reconciliation=record(True, None, True, SHA_A)),
                 target("unknown", "internal-error", reconciliation=None)]
        document = project.result_document(cases, 1, **context)
        refused, unconfirmed, internal = document["targets"]
        self.assertIs(refused["reconciliation"]["reconciled"], True)
        self.assertIs(unconfirmed["reconciliation"]["reconciled"], False)
        self.assertEqual(internal["reconciliation"], dict.fromkeys(RECONCILIATION_KEYS[:-1], None)
                         | {"reconciled": False})
        self.assertEqual(document["completeness"], "incomplete")
        self.assertEqual(project.result_document([], 0, **context)["completeness"], "complete")

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

            question = types.SimpleNamespace(selected=[1])
            with mock.patch.object(project, "input", ended, create=True), self.assertRaises(EOFError):
                project.ask_removal(question, run)
            first = run.now()  # the clock runs again
            time.sleep(0.01)
            self.assertGreater(run.now(), first)

        # A signal already in the slot raises before the question is written.
        with self.in_process(command="clean") as run:
            run.human = io.StringIO()
            run.record_signal(signal.SIGTERM)
            question = types.SimpleNamespace(selected=[1])
            with mock.patch.object(project, "input", side_effect=self.failureException("input() was called"),
                                   create=True), self.assertRaises(project.Terminated):
                project.ask_removal(question, run)
            self.assertEqual(run.human.getvalue(), "")

    def test_clean_ask_removal_never_reads_after_a_failed_write(self):
        # Lead ruling R-55: a question that could not be written is not
        # answered; the failed write is recorded for the check after it.
        with self.in_process() as run:
            run.human = RaisingStream()
            with mock.patch.object(project, "input", side_effect=self.failureException("input() was called"),
                                   create=True):
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
                    # Rows 3, 4, 6 and 7 again, never the memo, and the target's
                    # status, hidden-state and reachability probes (D7, LQ-13).
                    self.assertEqual(entry["probes_performed"], 6)
            self.assertEqual(self.snapshot(root, trees.values()), before)

    def test_clean_revalidate_refuses_a_changed_target_with_state_changed(self):
        """It also asserts identity-changed, for a removed registry entry and another identity (R-77(1))."""
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
                "001-dirty-tree": ("state-changed", record(True, True, None, None)),
                "002-locked-tree": ("state-changed", record(True, True, None, None)),
                "003-gone-tree": ("identity-changed", record(False, False, None, None)),
            }
            for name, reconciliation in expected.items():
                with self.subTest(name):
                    self.assertEqual(project.revalidate(plan, entries[name], run),
                                     reconciliation)
            self.assertTrue((trees["001-dirty"] / "late-change").is_file())

            # Another repository identity: the listings are not this repository's,
            # so only the path's own lstat is read.
            entry = entries["004-identity-tree"]
            moved = dict(plan.evidence, identity=dict(plan.evidence["identity"], ino=-1))
            with mock.patch.object(plan, "evidence", moved):
                self.assertEqual(project.revalidate(plan, entry, run),
                                 ("identity-changed", record(None, True, None, None)))
            self.assertIsNone(project.revalidate(plan, entry, run))

            # The merge target advances: every target differs.
            self.git(root, "commit", "-q", "--allow-empty", "-m", "advance the merge target")
            self.assertEqual(project.revalidate(plan, entry, run),
                             ("state-changed", record(True, True, True, heads["004-identity"])))

    def test_clean_revalidate_records_a_refused_path_after_the_work_deadline(self):
        # Lead ruling R-101 (d), apply review F3: a difference found just as the
        # work deadline passes still records the planned path's presence, since
        # that one lstat runs with the reserve's budget (data-model.md, "Target
        # result and reconciliation record"). In process, on the Invocation's
        # own clock under `clean` (the real table), in phase `apply`: the lock
        # makes step 3 differ before the target's own lstat, and the stand-in
        # moves the work deadline 1 s into the past as the difference returns,
        # the reserve ending reconciliation_reserve (10 s) after it. So the
        # work left is below 0, the reserve left about 9 s, and the lstat's
        # budget min(5 s, 9 s); under the per-child budget it would be 0.
        root, trees = self.merged_repository("001-a")
        tree = trees["001-a"]
        with self.in_process(command="clean") as run:
            plan = self.plan_of(root, run, [tree])
            entry = project.make_target(plan, plan.selected[0])
            self.git(root, "worktree", "lock", tree)
            real = project.revalidation_difference

            def at_the_work_deadline(*args):
                reason = real(*args)
                run.work_end = run.now() - 1
                run.reserve_end = run.work_end + project.TIMING["reconciliation_reserve"]
                return reason

            run.phase = "apply"
            with mock.patch.object(project, "revalidation_difference", at_the_work_deadline):
                refused = project.revalidate(plan, entry, run)
            self.assertLess(run.work_remaining(), 0)
            self.assertGreater(run.reserve_remaining(), 0)
        self.assertEqual(refused, ("state-changed", record(True, True, None, None)))
        self.assertIs(refused[1]["reconciled"], False)  # the branch was not read back
        self.assertTrue(tree.is_dir())

    # T056: the removal child, the rescan and the stage.

    def test_clean_run_removal_spawns_the_planned_vector_from_the_command_directory(self):
        root, trees = self.merged_repository("001-a")
        tree = trees["001-a"]
        planned = self.head(tree)
        bin_dir, log = self.base / "counting-bin", self.base / "children.log"
        clean_support.install_counting_git(bin_dir, log)
        with self.in_process(self.path_first(bin_dir)) as run:
            plan = self.plan_of(root, run, [tree])
            entry = project.make_target(plan, plan.selected[0])
            self.assertEqual(entry["command"], ["git", *REMOVAL_PINS, "-C", os.fsencode(root), "worktree", "remove",
                                                os.fsencode(tree)])
            probes = run.probes
            clean_support.reset_child_log(log)
            outcome = project.run_removal(entry, run)
            self.assertEqual((outcome.name, outcome.status, entry["exit_status"]), ("complete", 0, 0))
            self.assertEqual((run.operations, run.probes), (1, probes))
            reconciliation = project.rescan(entry, run)
            self.assertEqual(run.probes, probes + 3)
        removal, *rescans = clean_support.child_log(log)
        pins, rest = strip_pins(removal.argv)
        self.assertEqual(pins, REMOVAL_PINS)
        self.assertEqual(rest, ["-C", str(root), "worktree", "remove", str(tree)])
        self.assertNotIn("--force", removal.argv)
        self.assertEqual(removal.cwd, str(root))  # the command directory (design D9)
        self.assertEqual(removal.pgid, removal.pid)  # a process group of its own (D2)
        self.assertEqual(removal.names, ())  # scrubbed, and no GIT_OPTIONAL_LOCKS (R-48 (a))
        # The rescan: rows 3, 4 and 6 in the command directory, read-only probes.
        self.assertEqual([strip_pins(child.argv) for child in rescans],
                         [(PROTOCOL_PINS, ["-C", str(root), *ROW_3]), (PROTOCOL_PINS, ["-C", str(root), *ROW_4]),
                          (PROTOCOL_PINS, ["-C", str(root), *ROW_6])])
        self.assertTrue(all(child.optional_locks == "0" for child in rescans))
        self.assertEqual(reconciliation, record(False, False, True, planned))
        self.assertEqual(project.decide_stage(entry, outcome, reconciliation), ("removed", None, []))
        self.assertFalse(tree.exists())
        self.assertEqual(self.head(root, "refs/heads/001-a"), planned)  # every branch is kept

    def test_clean_run_removal_decides_what_git_did(self):
        root, trees = self.merged_repository("001-noop", "002-refused", "003-failed", "004-killed", "005-spawn")
        bin_dir = self.base / "fake-bin"
        # Each fake exits as Git might without removing anything; the rescan
        # finds the entry, the path and the branch at its planned SHA.
        cases = {
            "001-noop": ("remove-noop", {}, ("complete", 0), ("unknown", "unconfirmed-removal", [])),
            "002-refused": ("remove-exit", {"status": 128}, ("failed", 128), ("failed", "git-refused", [])),
            "003-failed": ("remove-exit", {"status": 255}, ("failed", 255), ("failed", "git-failed", [])),
        }
        with self.in_process() as run:
            plan = self.plan_of(root, run, trees.values())
            entries = {Path(os.fsdecode(row.raw_path)).name: project.make_target(plan, row) for row in plan.selected}
        for name, (kind, options, (outcome_name, status), stage) in cases.items():
            with self.subTest(name):
                fake_dir = bin_dir / name
                clean_support.install_fake_git(fake_dir, kind, **options)
                entry = entries[name + "-tree"]
                with self.in_process(self.path_first(fake_dir)) as run:
                    outcome = project.run_removal(entry, run)
                    reconciliation = project.rescan(entry, run)
                self.assertEqual((outcome.name, outcome.status, entry["exit_status"]), (outcome_name, status, status))
                self.assertEqual(reconciliation, record(True, True, True, self.head(trees[name])))
                self.assertEqual(project.decide_stage(entry, outcome, reconciliation), stage)
                self.assertTrue(trees[name].is_dir())

        # A removal child killed by a signal, whoever sent it, exited on its own:
        # `failed`, its exit status 128 plus the signal number (D15, M12).
        killer = self.base / "killer-bin"
        killer.mkdir()
        script = killer / "git"
        script.write_text('#!/bin/sh\ncase " $* " in *" worktree remove "*) kill -9 $$;; esac\n'
                          f'exec {shlex.quote(clean_support.REAL_GIT)} "$@"\n')
        script.chmod(0o755)
        entry = entries["004-killed-tree"]
        with self.in_process(self.path_first(killer)) as run:
            outcome = project.run_removal(entry, run)
            reconciliation = project.rescan(entry, run)
        self.assertEqual((outcome.name, outcome.status, entry["exit_status"]), ("failed", -9, 137))
        self.assertEqual(project.decide_stage(entry, outcome, reconciliation), ("failed", "git-failed", []))

        # No git to spawn: `failed` with `spawn-error`, no exit status, and no
        # removal counted, since no child ran.
        empty = self.base / "empty-bin"
        empty.mkdir()
        entry = entries["005-spawn-tree"]
        with self.in_process(dict(self.env, PATH=str(empty))) as run:
            outcome = project.run_removal(entry, run)
            self.assertEqual(run.operations, 0)
        self.assertEqual((outcome.name, outcome.status, entry["exit_status"]), ("failed", None, None))
        self.assertEqual(project.decide_stage(entry, outcome, record(True, True, True, SHA_A)),
                         ("failed", "spawn-error", []))
        self.assertTrue(trees["005-spawn"].is_dir())

    def test_clean_rescan_reestablishes_the_repository_identity_first(self):
        root, trees = self.merged_repository("001-a")
        tree = trees["001-a"]
        with self.in_process() as run:
            plan = self.plan_of(root, run, [tree])
            entry = project.make_target(plan, plan.selected[0])
            self.assertEqual(project.rescan(entry, run), record(True, True, True, self.head(tree)))
            for key, value in (("dev", -1), ("ino", -1), ("common_dir", b"/elsewhere/.git"), ("root", b"/elsewhere")):
                with self.subTest(key):
                    entry.identity = dict(plan.evidence["identity"], **{key: value})
                    unknown = project.rescan(entry, run)
                    self.assertEqual(unknown, record(None, None, None, None))
                    self.assertIs(unknown["reconciled"], False)
            # The branch deleted after the removal: present false, its SHA null.
            entry.identity = plan.evidence["identity"]
            self.git(root, "worktree", "remove", tree)
            self.git(root, "branch", "-D", "001-a")
            self.assertEqual(project.rescan(entry, run), record(False, False, False, None))

    def test_clean_rescan_reads_the_git_file_where_the_entry_and_the_path_remain(self):
        # Lane 3's W52 F-1 (Brett Heap's ruling "F-1: prune-then-delete", lead
        # ruling R-263): where the registry entry and the path are both shown
        # present, the rescan ends with one lstat of the target's `.git`
        # through fs_call(), no Git child, kept on the target as
        # git_file_present and in no record. The `.git` file present and gone
        # (a kill part way through `git worktree remove` leaves it gone), the
        # lstat cut at its budget or interrupted by a second SIGINT (None, the
        # record as the other reads made it), and the entry or the path gone
        # (no read, None). git_file_read says whether the read was made, so
        # that a read that failed or was cut is told from one not reached
        # (#19's round (i) at 1a4785e; W73 M-1, lead ruling R-284). No
        # recursive delete: the `.git` file and the admin directory are
        # renamed aside and back.
        root, trees = self.merged_repository("001-a")
        tree = trees["001-a"]
        planned = self.head(tree)
        dotgit = os.fsencode(tree / ".git")
        admin = Path(self.git(tree, "rev-parse", "--path-format=absolute", "--git-dir").strip())
        real_fs_call = project.fs_call

        def rescan(answer=None):
            """The rescan in a fresh Invocation, every lstat recorded and the
            `.git` lstat answered by answer when given: (record, lstats, the
            children it ran)."""
            lstats = []

            def fs_call(fn, *args, **options):
                if fn is os.lstat:
                    lstats.append(args[0])
                    if answer is not None and args[0] == dotgit:
                        if isinstance(answer, BaseException):
                            raise answer
                        return answer
                return real_fs_call(fn, *args, **options)

            with self.in_process() as run:
                entry.identity = plan.evidence["identity"]
                before = run.probes
                with mock.patch.object(project, "fs_call", fs_call):
                    found = project.rescan(entry, run)
                return found, lstats, run.probes - before

        with self.in_process() as run:
            plan = self.plan_of(root, run, [tree])
            entry = project.make_target(plan, plan.selected[0])
        self.assertEqual((entry.git_file_present, entry.git_file_read), (None, False))
        kept = record(True, True, True, planned)
        for label, answer, expected in [
                ("present", None, True),
                ("cut at its budget", project.DriverOutcome(None, "timeout", detail="cut here"), None),
                ("a second SIGINT", project.Interrupted(signal.SIGINT), None)]:
            with self.subTest(f"the .git file read: {label}"):
                found, lstats, children = rescan(answer)
                self.assertEqual((found, type(found)), (kept, dict))
                self.assertIs(entry.git_file_present, expected)
                self.assertIs(entry.git_file_read, True, "the read was made (W73 M-1, R-284)")
                self.assertEqual(lstats[-1], dotgit, "the .git lstat comes last")
                self.assertEqual(children, 3, "rows 3, 4 and 6 only: no Git child reads the .git file")
        aside = self.base / "dotgit-aside"
        with self.subTest("the .git file gone, the entry and the path kept"):
            os.rename(tree / ".git", aside)
            try:
                found, lstats, children = rescan()
            finally:
                os.rename(aside, tree / ".git")
            self.assertEqual((found, entry.git_file_present, entry.git_file_read, lstats[-1], children),
                             (kept, False, True, dotgit, 3))
        with self.subTest("the registry entry gone, the path kept"):
            moved = admin.parent.parent / "admin-aside"
            os.rename(admin, moved)
            try:
                found, lstats, children = rescan()
            finally:
                os.rename(moved, admin)
            self.assertEqual((found, entry.git_file_present, entry.git_file_read),
                             (record(False, True, True, planned), None, False))
            self.assertNotIn(dotgit, lstats, "no .git read without the entry")
        with self.subTest("the path gone, the entry kept"):
            moved = self.base / "tree-aside"
            os.rename(tree, moved)
            try:
                found, lstats, children = rescan()
            finally:
                os.rename(moved, tree)
            self.assertEqual((found, entry.git_file_present, entry.git_file_read),
                             (record(True, False, True, planned), None, False))
            self.assertNotIn(dotgit, lstats, "no .git read without the path")
        with self.subTest("a directory above the target denies search: the path lstat fails"):
            # Lane 3's W90 M-1 (lead ruling R-329; #19's ceiling scenario,
            # "as when a directory above it denies search"): the target's own
            # lstat fails with EACCES, so the path is null, no `.git` read is
            # made or could be, and the `.git` counts as unread: the
            # ceiling's note for the record this rescan leaves is the third
            # one, which advises no prune, whatever the entry shows; plain
            # `git worktree prune` would delete the live worktree's admin
            # directory. The mode is restored in a cleanup that tolerates a
            # missing path.
            if hasattr(os, "geteuid") and os.geteuid() == 0:
                self.skipTest("permission fixtures do not bind the superuser (effective uid 0)")
            parent = self.base / "par"
            parent.mkdir()
            unread = self.merged_worktree("002-par", path=parent / "wt", root=root)
            planned_unread = self.head(unread)
            with self.in_process() as run:
                plan_unread = self.plan_of(root, run, [unread])
                held = project.make_target(plan_unread, plan_unread.selected[0])
            mode = parent.stat().st_mode & 0o7777

            def searchable_again():
                with contextlib.suppress(FileNotFoundError):
                    parent.chmod(mode)

            self.addCleanup(searchable_again)
            parent.chmod(0o000)
            try:
                with self.in_process() as run:
                    found = project.rescan(held, run)
            finally:
                searchable_again()
            self.assertEqual((found, type(found)), (record(True, None, True, planned_unread),
                                                    project.UnfinishedRescan))
            self.assertIs(found["reconciled"], False)
            self.assertIsNone(held.git_file_present, "no value for the `.git`")
            held["reconciliation"] = found  # as apply_removals() keeps it
            killed = project.DriverOutcome(["git"], "timeout", status=-signal.SIGKILL)
            self.assertEqual(project.decide_stage(held, killed, found),
                             ("unknown", "removal-ceiling", ["partially-removed"]))
            self.assertEqual(project.partial_removal_text(held), "partial_removal_note_unread",
                             "the third note: no prune advice where the path could not be read")
        found, _, _ = rescan()
        self.assertEqual((found, entry.git_file_present), (kept, True), "the fixture is restored")

    def test_clean_decide_stage_on_literal_outcomes(self):
        outcome = project.DriverOutcome
        gone, kept = record(False, False, True, SHA_A), record(True, True, True, SHA_A)
        cases = [
            (outcome(["git"], "complete", status=0), gone, ("removed", None, [])),
            (outcome(["git"], "complete", status=0), kept, ("unknown", "unconfirmed-removal", [])),
            (outcome(["git"], "complete", status=0), record(False, True, True, SHA_A),
             ("unknown", "unconfirmed-removal", [])),
            (outcome(["git"], "complete", status=0), record(None, None, None, None),
             ("unknown", "unconfirmed-removal", [])),
            (outcome(["git"], "failed", status=128), kept, ("failed", "git-refused", [])),
            (outcome(["git"], "failed", status=1), kept, ("failed", "git-failed", [])),
            (outcome(["git"], "failed", status=255), record(False, True, True, SHA_A), ("failed", "git-failed", [])),
            (outcome(["git"], "failed", status=-signal.SIGTERM), gone, ("failed", "git-failed", [])),
            (outcome(["git"], "failed", detail="cannot run git"), kept, ("failed", "spawn-error", [])),
            # Cut at the ceiling, or its exit not observed: the rescan decides (D9).
            (outcome(["git"], "timeout", status=-signal.SIGKILL), gone, ("removed", "removal-ceiling", [])),
            (outcome(["git"], "timeout", status=-signal.SIGKILL), kept,
             ("unknown", "removal-ceiling", ["partially-removed"])),
            (outcome(["git"], "timeout"), record(False, True, True, SHA_A),
             ("unknown", "removal-ceiling", ["partially-removed"])),
            (outcome(["git"], "timeout"), record(None, None, None, None), ("unknown", "removal-ceiling", [])),
        ]
        stages = project.STAGE_REASONS
        for given, reconciliation, expected in cases:
            with self.subTest(outcome=given, reconciliation=reconciliation):
                decided = project.decide_stage(target("pending"), given, reconciliation)
                self.assertEqual(decided, expected)
                self.assertIn(decided[1], stages[decided[0]])

    # T057's printers.

    def test_clean_print_result_prints_the_success_line_or_the_stop_block(self):
        plan = types.SimpleNamespace(root=Path("/r oot"))
        removed = [target("removed", path=b"/w/a", branch="a"), target("removed", path=b"/w/b", branch="b"),
                   target("removed", path=b"/w/c", branch="c")]
        stopped = [removed[0], target("refused", "state-changed", path=b"/w/b", branch="b"),
                   target("not-attempted", "batch-stopped", path=b"/w/c", branch="c")]
        last = [removed[0], removed[1], target("failed", "git-refused", 128, path=b"/w/c", branch="c")]
        kept = TEXT["branches_kept_line"].format(BRANCHES="a, b, c")
        residual = TEXT["residual_window_line"]
        cases = [
            (removed, ["  removed /w/a", "  removed /w/b", "  removed /w/c",
                       TEXT["success_line"].format(N=3, BRANCHES="a, b, c"), residual]),
            (stopped, ["  removed /w/a", "  refused /w/b (state-changed)", "  not-attempted /w/c (batch-stopped)",
                       TEXT["stop_block"].format(PATH="/w/b", REASON="state-changed", K=1, N=3,
                                                 NOT_ATTEMPTED="/w/c", ROOT="'/r oot'"), kept, residual]),
            # The stop at the last target leaves nothing not attempted (D18 leaves
            # that list's empty form open; project writes `none`).
            (last, ["  removed /w/a", "  removed /w/b", "  failed /w/c (git-refused)",
                    TEXT["stop_block"].format(PATH="/w/c", REASON="git-refused", K=2, N=3,
                                              NOT_ATTEMPTED="none", ROOT="'/r oot'"), kept, residual]),
        ]
        for targets, lines in cases:
            with self.subTest(stages=[entry["stage"] for entry in targets]):
                run = types.SimpleNamespace(human=io.StringIO(), write_error=None)
                for entry in targets:
                    project.print_progress(entry, run)
                project.print_result(plan, targets, run)
                self.assertEqual(run.human.getvalue(), "\n".join(lines) + "\n")
        self.assertEqual(TEXT["success_line"].format(N=3, BRANCHES="a, b, c"), "Removed 3; branches kept: a, b, c.")

        # Paths and branches print escaped (FR-041), the root in its command form.
        odd = [target("unknown", "unconfirmed-removal", path=b"/w/a\x1bb", branch="a" + chr(0x202E) + "b")]
        run = types.SimpleNamespace(human=io.StringIO(), write_error=None)
        project.print_progress(odd[0], run)
        project.print_result(types.SimpleNamespace(root=b"/r\nx"), odd, run)
        self.assertEqual(run.human.getvalue().splitlines()[:3], [
            "  unknown $'/w/a\\u001bb' (unconfirmed-removal)",
            TEXT["stop_block"].format(PATH="$'/w/a\\u001bb'", REASON="unconfirmed-removal", K=0, N=1,
                                      NOT_ATTEMPTED="none", ROOT="$'/r\\u000ax'"),
            TEXT["branches_kept_line"].format(BRANCHES="$'a\\u202eb'")])

        # Every line goes through say(): a failed write is recorded, never raised.
        run = types.SimpleNamespace(human=RaisingStream(), write_error=None)
        project.print_progress(stopped[1], run)
        project.print_result(plan, stopped, run)
        self.assertIsInstance(run.write_error, BrokenPipeError)

    # T041: "Stable order and preserved work", and the apply clauses of "Plan
    # digest mismatch" and "Paths and empty plans" (lead ruling R-56 Q-5).

    def test_clean_stable_order_and_preserved_work(self):
        root = self.repo()
        self.bare_remote()
        # Three eligible worktrees, created in an order other than raw path byte
        # order, their names differing by more than case ("Alpha" < "mid" <
        # "zeta" as bytes).
        eligible = {"001-zeta": self.merged_worktree("001-zeta", path=self.base / "zeta"),
                    "002-alpha": self.merged_worktree("002-alpha", path=self.base / "Alpha"),
                    "003-mid": self.merged_worktree("003-mid", path=self.base / "mid")}
        current = self.merged_worktree("004-current")
        dirty = [self.merged_worktree("005-dirty"), self.merged_worktree("006-dirty")]
        for tree in dirty:
            (tree / "uncommitted").write_text("preserve")
        locked = self.merged_worktree("007-locked")
        self.git(root, "worktree", "lock", locked)
        ahead = self.remote_ahead_worktree("008-ahead")
        unmerged = self.unmerged_worktree("009-unmerged")
        kept = {current: "merged-current", dirty[0]: "dirty", dirty[1]: "dirty", locked: "locked-worktree",
                ahead: "remote-ahead", unmerged: "pushed-unmerged", root: "main-worktree"}
        # The run's working directory is a linked worktree, the current one.
        preview = self.run_json("clean", root, "--all-safe", "--json", cwd=current).document
        self.assertEqual({entry["path"]: entry["reason"] for entry in preview["excluded"]},
                         {str(tree): reason for tree, reason in kept.items()})
        order = sorted(eligible.items(), key=lambda item: os.fsencode(item[1]))
        self.assertEqual([entry["path"] for entry in preview["selected"]], [str(tree) for _, tree in order])
        branches = self.branches(root)

        env, log = self.counting()
        result = self.run_cli("clean", root, "--all-safe", "--apply", "--yes", cwd=current, env=env)
        self.assert_status(result, 0)
        records = clean_support.child_log(log)
        # Removed in raw path order, each by its own child.
        self.assertEqual([subcommand(record)[2:] for record in removals(records)],
                         [[str(tree)] for _, tree in order])
        registry = self.git(root, "worktree", "list", "--porcelain").splitlines()
        for name, tree in eligible.items():
            self.assertFalse(tree.exists(), name)
            self.assertNotIn(f"worktree {tree}", registry)
        for tree in kept:
            self.assertTrue(tree.is_dir(), tree)
            self.assertIn(f"worktree {tree}", registry)
        self.assertEqual(self.branches(root), branches, "every branch is kept at its head")
        self.assertTrue((dirty[0] / "uncommitted").is_file())
        # The result names every retained branch, in canonical order.
        self.assertEqual(result.stdout.splitlines()[-2:], [
            TEXT["success_line"].format(N=3, BRANCHES="002-alpha, 003-mid, 001-zeta"), TEXT["residual_window_line"]])
        # Nothing pushed, fetched, forced, deleted, pruned, repaired, locked or unlocked.
        for record in records:
            words = subcommand(record)
            with self.subTest(argv=record.argv):
                self.assertNotIn("--force", record.argv)
                self.assertNotIn(words[:1], (["push"], ["fetch"]))
                self.assertFalse(words[:1] == ["branch"] and {"-d", "-D", "--delete"} & set(words))
                self.assertFalse(words[:1] == ["remote"] and {"remove", "rm", "prune", "set-url"} & set(words))
                self.assertNotIn(words[:2], (["worktree", "prune"], ["worktree", "repair"], ["worktree", "lock"],
                                             ["worktree", "unlock"]))

    def test_clean_stable_order_and_preserved_work_target_not_checked_out(self):
        root = self.repo()
        self.bare_remote()
        trees = [self.merged_worktree("001-a"), self.merged_worktree("002-b")]
        # The main worktree moves to another branch: the merge-target branch is
        # checked out nowhere, and every removal still names the command
        # directory (design D9).
        self.git(root, "checkout", "-q", "-b", "003-elsewhere")
        self.assertNotIn("branch refs/heads/main", self.git(root, "worktree", "list", "--porcelain"))
        branches = self.branches(root)
        env, log = self.counting()
        result = self.run_cli("clean", root, "--all-safe", "--apply", "--yes", env=env)
        self.assert_status(result, 0)
        children = removals(clean_support.child_log(log))
        self.assertEqual([strip_pins(record.argv)[1] for record in children],
                         [["-C", str(root), "worktree", "remove", str(tree)] for tree in trees])
        self.assertEqual([record.cwd for record in children], [str(root)] * 2)
        self.assertFalse(any(tree.exists() for tree in trees))
        self.assertEqual(self.branches(root), branches)

    def test_clean_plan_digest_mismatch_unchanged_digest_applies(self):
        root = self.repo()
        self.bare_remote()
        first = self.merged_worktree("001-p1")
        second = self.merged_worktree("002-p2")
        (second / "uncommitted").write_text("preserve")
        preview = self.run_json("clean", root, "--all-safe", "--json").document
        digest = preview["plan_digest"]
        self.assertEqual([entry["path"] for entry in preview["selected"]], [str(first)])
        # Only the excluded row changes: P2 gains a commit and stays dirty.
        (second / "later").write_text("later")
        self.git(second, "add", "later")
        self.git(second, "commit", "-q", "-m", "later")
        again = self.run_json("clean", root, "--all-safe", "--json").document
        heads = [{row["path"]: row["head"] for row in document["worktrees"]} for document in (preview, again)]
        self.assertNotEqual(heads[0][str(second)], heads[1][str(second)])
        self.assertEqual([entry["path"] for entry in again["excluded"] if entry["reason"] == "dirty"], [str(second)])
        self.assertEqual(again["plan_digest"], digest, "the digest covers only what is selected")
        result = self.run_cli("clean", root, "--all-safe", "--apply", "--yes", "--expect-plan", digest)
        self.assert_status(result, 0)
        self.assertFalse(first.exists())
        self.assertTrue((second / "uncommitted").is_file())
        self.assertEqual(self.head(root, "refs/heads/001-p1"), heads[0][str(first)])

    def test_clean_paths_and_empty_plans_paths_with_spaces_are_removed(self):
        root = self.repo()
        self.bare_remote()
        spaced = [self.merged_worktree("001-spaced", path=self.base / "with spaces" / "a tree"),
                  self.merged_worktree("002-spaced", path=self.base / "with spaces" / "b  tree")]
        branches = self.branches(root)
        env, log = self.counting()
        result = self.run_cli("clean", root, "--all-safe", "--apply", "--yes", env=env)
        self.assert_status(result, 0)
        # Each path is one exact argument of its removal, and prints verbatim in
        # prose (FR-041).
        self.assertEqual([subcommand(record)[2:] for record in removals(clean_support.child_log(log))],
                         [[str(tree)] for tree in spaced])
        selected = [(spaced[0], "001-spaced"), (spaced[1], "002-spaced")]
        self.assertEqual(result.stdout.splitlines()[-4:], self.result_lines(selected))
        self.assertFalse(any(tree.exists() for tree in spaced))
        self.assertEqual(self.branches(root), branches)

    # T042: "Every branch remains after a batch".

    def test_clean_every_branch_remains_after_a_batch(self):
        root = self.repo()
        self.bare_remote()
        trees = {"001-a": self.merged_worktree("001-a"), "002-b": self.merged_worktree("002-b")}
        preview = self.run_json("clean", root, "--all-safe", "--json").document
        planned = {entry["branch"]: entry["head"] for entry in preview["selected"]}
        self.assertEqual(sorted(planned), sorted(trees))
        result = self.run_cli("clean", root, "--all-safe", "--apply", "--yes")
        self.assert_status(result, 0)
        for branch, head in planned.items():
            with self.subTest(branch=branch):
                self.assertEqual(self.head(root, f"refs/heads/{branch}"), head)
                self.assertFalse(trees[branch].exists())
        selected = [(trees["001-a"], "001-a"), (trees["002-b"], "002-b")]
        self.assertEqual((result.stdout, result.stderr),
                         ("\n".join(self.plan_lines(root, selected) + self.result_lines(selected)) + "\n", ""))
        self.assertEqual(TEXT["success_line"].format(N=2, BRANCHES="001-a, 002-b"),
                         "Removed 2; branches kept: 001-a, 002-b.")

    # T043: "Only yes confirms".

    def test_clean_only_yes_confirms(self):
        root = self.repo()
        self.bare_remote()
        trees = [self.merged_worktree(f"00{number}-t") for number in range(1, 8)]
        question = TEXT["question"].format(N=7)
        self.assertEqual(question, "Remove 7 worktrees, keeping 7 branches? [yes/N]")
        before = self.snapshot(root, trees)
        argv = clean_support.cli_argv("clean", root, "--all-safe", "--apply")
        # Only `yes`, its surrounding whitespace stripped, accepts: `YES` and
        # `Yes` are cancelled like `y` (plan review C1; lead ruling R-101 (c)).
        for answer in ("y", "", "no", "YES", "Yes"):
            with self.subTest(answer=answer):
                result = self.run_pty_steps(argv, [(question, answer)])
                self.assert_status(result, 2)
                self.assertIn(question, result.stdout.splitlines())
                self.assertEqual(result.stderr, f"REFUSED: {CANCELLED}\n")
                self.assertNotIn(TEXT["progress_line"].format(STAGE="removed", PATH=trees[0]), result.stdout)
                self.assertEqual(self.snapshot(root, trees), before, "nothing removed")

        # Under --json, with standard input at the terminal and standard output
        # on a pipe (R-56 Q-14): the question on standard error, and standard
        # output one document, the plan envelope refused as `cancelled`.
        result = self.run_pty_steps([*argv, "--json"], [(question, "no")], stdout_pipe=True)
        self.assert_status(result, 2)
        self.assertIn(question, result.stderr.splitlines())
        self.assertNotIn(question, result.stdout)
        document = self.load_json(result)
        self.assertEqual((document["apply_allowed"], document["refusals"]),
                         (False, [{"code": "cancelled", "message": CANCELLED}]))
        self.assertEqual([entry["path"] for entry in document["selected"]], [str(tree) for tree in trees])
        self.assertNotIn("REFUSED", result.stderr)
        self.assertEqual(self.snapshot(root, trees), before, "nothing removed")

        # The singular form for one, and ` yes ` begins the apply phase.
        one = self.repo("one-repo")
        self.bare_remote(one, "one-remote.git")
        tree = self.merged_worktree("011-one", root=one)
        self.assertEqual(TEXT["question_one"], "Remove 1 worktree, keeping 1 branch? [yes/N]")
        result = self.run_pty_steps(clean_support.cli_argv("clean", one, "--all-safe", "--apply"),
                                    [(TEXT["question_one"], " yes ")])
        self.assert_status(result, 0)
        lines = result.stdout.splitlines()
        self.assertIn(TEXT["question_one"], lines)
        self.assertEqual(lines[-3:], self.result_lines([(tree, "011-one")]))
        self.assertFalse(tree.exists())
        self.assertEqual(self.head(one, "refs/heads/011-one"), self.head(one, "011-one"))

    def test_clean_only_yes_confirms_an_undecodable_answer(self):
        # Lead ruling R-101 (c), plan review F1: an answer standard input cannot
        # decode is not `yes`, so it is cancelled like any other: exit 2, the
        # human refusal, and under --json the plan envelope refused as
        # `cancelled`, never internal-error's error object. Standard input
        # decodes strictly here, as Python's does under a UTF-8 locale other
        # than C, through PYTHONIOENCODING=utf-8:strict; the answer is the byte
        # 0xE9 and a newline, as a Latin-1 terminal sends it.
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-a")
        before = self.snapshot(root, [tree])
        env = dict(self.env, PYTHONIOENCODING="utf-8:strict")
        argv = clean_support.cli_argv("clean", root, "--all-safe", "--apply")
        answer = [(TEXT["question_one"], b"\xe9\n")]
        result = self.run_pty_steps(argv, answer, env=env)
        self.assert_status(result, 2)
        self.assertEqual(result.stderr, f"REFUSED: {CANCELLED}\n")
        self.assertEqual(self.snapshot(root, [tree]), before, "nothing removed")
        result = self.run_pty_steps([*argv, "--json"], answer, env=env, stdout_pipe=True)
        self.assert_status(result, 2)
        self.assertIn(TEXT["question_one"], result.stderr.splitlines())
        self.assertNotIn("REFUSED", result.stderr)
        document = self.load_json(result)
        self.assertNotIn("code", document, "a plan envelope, not an error object")
        self.assertEqual((document["apply_allowed"], document["refusals"]),
                         (False, [{"code": "cancelled", "message": CANCELLED}]))
        self.assertEqual([entry["path"] for entry in document["selected"]], [str(tree)])
        self.assertEqual(self.snapshot(root, [tree]), before, "nothing removed")

    # T044: "A noninteractive batch needs --yes".

    def test_clean_a_noninteractive_batch_needs_yes(self):
        root = self.repo()
        self.bare_remote()
        trees = [self.merged_worktree("001-a"), self.merged_worktree("002-b")]
        before = self.snapshot(root, trees)
        env, log = self.counting()
        # Standard input not a terminal (run_cli's is an empty pipe), no --yes.
        result = self.run_cli("clean", root, "--all-safe", "--apply", env=env)
        self.assert_status(result, 2)
        selected = [(trees[0], "001-a"), (trees[1], "002-b")]
        self.assertEqual((result.stdout, result.stderr), ("\n".join(self.plan_lines(root, selected)) + "\n",
                                                          "REFUSED: " + TEXT["confirmation_required"] + "\n"))
        self.assertEqual(removals(clean_support.child_log(log)), [])
        self.assertEqual(self.snapshot(root, trees), before)
        # Under --json: the plan envelope with that refusal, and no question.
        result = self.run_json("clean", root, "--all-safe", "--apply", "--json", env=env)
        self.assert_status(result, 2)
        self.assertEqual((result.document["apply_allowed"], result.document["refusals"]),
                         (False, [{"code": "confirmation-required", "message": TEXT["confirmation_required"]}]))
        self.assertEqual(result.stderr, "\n".join(self.plan_lines(root, selected)) + "\n")
        self.assertEqual(self.snapshot(root, trees), before)
        # With --yes the fresh plan's selection is removed with no question.
        clean_support.reset_child_log(log)
        result = self.run_cli("clean", root, "--all-safe", "--apply", "--yes", env=env)
        self.assert_status(result, 0)
        self.assertNotIn("[yes/N]", result.stdout + result.stderr)
        self.assertEqual(len(removals(clean_support.child_log(log))), 2)
        self.assertFalse(any(tree.exists() for tree in trees))

    # T057's apply side of the closed reader (lead rulings R-55 and R-59 D2).

    def test_clean_a_reader_that_closes_standard_output_under_apply_json(self):
        # --all-safe --apply --yes --json with standard output a pipe whose read
        # end is closed: the plan and the progress go to standard error, the
        # removals proceed, the failed write of the result record is
        # best-effort, and the run exits by D19, 0 when every target is removed,
        # with no traceback and never 120.
        root = self.repo()
        self.bare_remote()
        trees = [self.merged_worktree("001-a"), self.merged_worktree("002-b")]
        branches = self.branches(root)
        env, log = self.counting()
        read_end, write_end = os.pipe()
        os.close(read_end)
        try:
            result = subprocess.run(clean_support.cli_argv("clean", root, "--all-safe", "--apply", "--yes", "--json"),
                                    cwd=self.base, env=env, stdin=subprocess.DEVNULL, stdout=write_end,
                                    stderr=subprocess.PIPE, text=True, timeout=clean_support.TIMEOUT)
        finally:
            os.close(write_end)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertNotIn("Exception ignored", result.stderr)
        selected = [(trees[0], "001-a"), (trees[1], "002-b")]
        self.assertEqual(result.stderr, "\n".join(self.plan_lines(root, selected) + self.result_lines(selected)) + "\n")
        self.assertEqual(len(removals(clean_support.child_log(log))), 2)
        self.assertFalse(any(tree.exists() for tree in trees))
        self.assertEqual(self.branches(root), branches)


if __name__ == "__main__":
    unittest.main()
