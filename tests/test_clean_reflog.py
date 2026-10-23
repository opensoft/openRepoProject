"""Gate 7 of `project clean`, `unstarted-branch` or `reflog-unavailable`, read
from the branch's reflog (feature 004, the US2 reflog lane: T059 and T060, for
T066).

Sources: design.md D10 of openspec/changes/add-project-clean-all-safe/ and its
Context table (the reflog lines Git writes), the project-clean delta's gate
list, reflog rule and reflog scenarios, and data-model.md ("Gate" and "Reflog
anchor and movement"); lead rulings R-33, R-53 P-22, R-54 X-1, R-56 Q-6 and
R-67 (a). The decider, reflog_outcome(), is tested on byte literals; the gate
on the same literals written to a file, and on reads that fail; the scenarios
on disposable repositories (rule 4), whose eligible rows are made by
merged_worktree(), a commit of their own (lead ruling R-56). Expected human
text comes from clean_support's fixtures (rule 8).
"""
import ast
import contextlib
import errno
import io
import json
import os
from pathlib import Path
import threading
import types
import unittest
from unittest import mock

import clean_support

project = clean_support.load_project()
TEXT = clean_support.TEXT_FIXTURES
STEPS = clean_support.NEXT_STEP_FIXTURES

# Object names of the byte literals, as Git 2.43 wrote them for D10's Context
# probes when this lane was written.
ZERO = b"0" * 40
TIP = b"b3b09e72f0429adfa3b16c07d5e2a6e16542ea19"  # the merge target's tip when the branch was made
OWN = b"9eb6cd0fab2be84d76ae3e06b3b50979f0790d94"  # the branch's own commit
MAIN = b"c6315905edd7fad8cc435c617c6863c2e08a27d1"  # the merge target's later tip
LATER = b"5f1c0de2a63e1b2bb6a1d7d4b0c0f6f3f0a4e7c1"  # a later commit of the branch's own
IDENT = b"T <t@e.invalid> 1792530262 +0000"
ZERO_256 = b"0" * 64
TIP_256 = b"4c1e3f0b2a9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f"
OWN_256 = b"0f1e2d3c4b5a69788796a5b4c3d2e1f00f1e2d3c4b5a69788796a5b4c3d2e1f0"

# The recommendation texts of the two classes these rows take (project at 961c405).
MERGED_REMOVABLE = "This clean, merged, non-current worktree may be removed explicitly."
INSPECTION_ERROR = "Preserve this worktree; Git could not establish its clean state."

BOUND = 65536  # the read's 64 KiB bound (lead ruling R-33)
DAY = 86400


def entry(old, new, message=None):
    """One reflog line: `<old> <new> <identity> <time> <zone>`, then a tab and
    the message when there is one (D10)."""
    return old + b" " + new + b" " + IDENT + (b"" if message is None else b"\t" + message) + b"\n"


# The entries of D10's Context table, as Git writes them.
CREATED = entry(ZERO, TIP, b"branch: Created from HEAD")  # worktree add -b, branch, checkout -b
COMMIT = entry(TIP, OWN, b"commit: one")
RENAMED = entry(TIP, TIP, b"Branch: renamed refs/heads/x to refs/heads/x2")
RESET = entry(OWN, MAIN, b"branch: Reset to main")  # worktree add -B, branch -f, checkout -B
FETCHED = entry(ZERO, MAIN, b"fetch origin feat:f1: storing head")
FETCHED_QUIET = entry(ZERO, MAIN, b"fetch -q origin feat:f1: storing head")
UPDATE_REF = entry(ZERO, MAIN)  # git update-ref with no -m: no tab, no message
PUSHED = entry(ZERO, MAIN, b"push")  # git push . main:f3


def padded(tail, size, head=TIP):
    """tail behind no-op entries (old and new both head, so no movement, and a
    `pad` message, so no anchor) making exactly size bytes."""
    bare = len(entry(head, head, b"pad"))
    gap, chunks = size - len(tail), []
    while gap >= 1000 + bare:
        chunks.append(1000)
        gap -= 1000
    chunks += [gap // 2, gap - gap // 2] if gap > 1000 else [gap] if gap else []
    if any(chunk < bare for chunk in chunks):
        raise ValueError(f"padded: cannot make {size} bytes")
    data = b"".join(entry(head, head, b"pad" + b"." * (chunk - bare)) for chunk in chunks) + tail
    assert len(data) == size, (len(data), size)
    return data


# (label, reflog bytes, head, outcome): D10's outcome for each entry of its
# Context, and for the lines that cannot decide (lead ruling R-53 P-22).
DECIDER_CASES = [
    ("worktree add -b, no commit", CREATED, TIP, "unstarted-branch"),
    ("worktree add -b, then a commit", CREATED + COMMIT, OWN, None),
    ("worktree add -b, then a rename with equal objects", CREATED + RENAMED, TIP, "unstarted-branch"),
    ("a commit, then a rename", CREATED + COMMIT + entry(OWN, OWN, b"Branch: renamed refs/heads/y to refs/heads/z"),
     OWN, None),
    ("branch: Reset to over commits of its own", CREATED + COMMIT + RESET, MAIN, "unstarted-branch"),
    ("branch: Reset to, then a commit", CREATED + COMMIT + RESET + entry(MAIN, LATER, b"commit: two"), LATER, None),
    ("fetch origin feat:f1: storing head", FETCHED, MAIN, "unstarted-branch"),
    ("fetch -q origin feat:f1: storing head", FETCHED_QUIET, MAIN, "unstarted-branch"),
    ("update-ref with no message", UPDATE_REF, MAIN, "unstarted-branch"),
    ("push", PUSHED, MAIN, "unstarted-branch"),
    ("a creation, then a commit, then a later creation", CREATED + COMMIT + PUSHED, MAIN, "unstarted-branch"),
    ("an all-zeros old object is never a movement, whatever its message",
     entry(ZERO, MAIN, b"commit: no anchor message"), MAIN, "unstarted-branch"),
    ("the anchor expired, a movement survives", COMMIT, OWN, None),
    ("the anchor expired, a movement and a rename survive", COMMIT + entry(OWN, OWN, b"Branch: renamed"), OWN, None),
    ("only a rename survives", RENAMED, TIP, "reflog-unavailable"),
    ("an entry to the all-zeros object is no movement", entry(TIP, ZERO, b"x") + RENAMED, TIP,
     "reflog-unavailable"),
    ("an anchor whose new object is not the head, no movement after it",
     CREATED + entry(OWN, OWN, b"Branch: renamed"), OWN, "reflog-unavailable"),
    ("the last entry's new object is not the head", CREATED, OWN, "reflog-unavailable"),
    ("the last entry's new object is not the head, a movement before it", CREATED + COMMIT, TIP,
     "reflog-unavailable"),
    ("SHA-256 objects, no commit", entry(ZERO_256, TIP_256, b"branch: Created from HEAD"), TIP_256,
     "unstarted-branch"),
    ("SHA-256 objects, then a commit", entry(ZERO_256, TIP_256, b"branch: Created from HEAD")
     + entry(TIP_256, OWN_256, b"commit: one"), OWN_256, None),
    ("a head given as text", CREATED + COMMIT, OWN.decode(), None),
    ("no head", CREATED, None, "reflog-unavailable"),
    ("empty", b"", TIP, "reflog-unavailable"),
    ("a line that is not <old> <new> ...", b"not a reflog line\n", TIP, "reflog-unavailable"),
    ("a good entry, then a line that is not one", CREATED + b"garbage\n" + COMMIT, OWN, "reflog-unavailable"),
    ("a truncated last line", CREATED + COMMIT[:50], OWN, "reflog-unavailable"),
    ("a last line with no line feed", CREATED + COMMIT[:-1], OWN, "reflog-unavailable"),
    ("an empty line", CREATED + b"\n" + COMMIT, OWN, "reflog-unavailable"),
    ("objects in upper case", CREATED.upper(), TIP.upper(), "reflog-unavailable"),
    ("old and new objects of different lengths", entry(TIP, OWN_256, b"commit: one"), OWN_256,
     "reflog-unavailable"),
    ("objects of another length than the head", CREATED, TIP_256, "reflog-unavailable"),
    ("no identity, time or zone", ZERO + b" " + TIP + b"\n", TIP, "reflog-unavailable"),
    ("65,535 bytes are decided by their entries", padded(CREATED + COMMIT, BOUND - 1), OWN, None),
    ("65,535 bytes, unstarted", padded(CREATED, BOUND - 1), TIP, "unstarted-branch"),
    ("65,536 bytes reach the bound", padded(CREATED + COMMIT, BOUND), OWN, "reflog-unavailable"),
]


class ReflogTests(clean_support.CleanCase):

    # In-process fixtures: a common directory of its own, one row and its plan.

    def gate_fixture(self, branch="feature/x", head=TIP):
        """A common directory with logs/refs/heads/ under self.base, a
        merged-removable WorktreeRow on branch at head, and an all-safe Plan
        whose evidence names that common directory."""
        common = self.base / "common.git"
        (common / "logs" / "refs" / "heads").mkdir(parents=True, exist_ok=True)
        row = project.WorktreeRow(path="/w/x", present=True, branch=branch,
                                  head=None if head is None else head.decode(),
                                  classification="merged-removable", recommendation=MERGED_REMOVABLE,
                                  locked=False, path_valid_utf8=True, errors=[])
        row.raw_path, row.main, row.registered = b"/w/x", False, True
        plan = project.Plan({"root": Path("/w/main")}, types.SimpleNamespace(mode="all-safe", action=None))
        plan.evidence = {"identity": {"common_dir": os.fsencode(common)}, "errors": []}
        plan.rows = [row]
        return common, row, plan

    def reflog_at(self, common, branch="feature/x"):
        return common / "logs" / "refs" / "heads" / branch

    def write_at(self, common, data, branch="feature/x"):
        path = self.reflog_at(common, branch)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def gate(self, row, plan, run=None):
        """reflog_gate(row, plan, run) in an Invocation of its own (or run's),
        with no Git child allowed."""
        with mock.patch.object(project, "run_bounded", side_effect=AssertionError("a Git child ran")):
            if run is not None:
                return project.reflog_gate(row, plan, run)
            with project.Invocation() as own:
                return project.reflog_gate(row, plan, own)

    def assert_row(self, row, plan, classification, errors, unprobed, completeness):
        self.assertEqual((row["classification"], row["errors"], row.unprobed, project.plan_completeness(plan)),
                         (classification, errors, unprobed, completeness))

    def stuck_read(self):
        """A stand-in for _read_head that blocks until the test ends, so that
        fs_call() abandons it at its budget."""
        release = threading.Event()
        self.addCleanup(release.set)

        def stuck(path, limit):
            release.wait(clean_support.TIMEOUT)
            raise OSError(errno.EIO, os.strerror(errno.EIO))
        return stuck

    # T059: the gate's outcomes.

    def test_clean_reflog_gate_outcomes(self):
        # D10 and data-model.md "Reflog anchor and movement", first on the pure
        # decider (lead ruling R-54 X-1), then through reflog_gate() with each
        # literal as the branch's reflog file.
        with mock.patch.object(project, "fs_call", side_effect=AssertionError("the decider read a file")), \
                mock.patch.object(project, "run_bounded", side_effect=AssertionError("a Git child ran")):
            for label, data, head, expected in DECIDER_CASES:
                with self.subTest("reflog_outcome", case=label):
                    self.assertEqual(project.reflog_outcome(data, head), expected)
        for label, data, head, expected in DECIDER_CASES:
            if head is None or isinstance(head, str):
                continue
            with self.subTest("reflog_gate", case=label):
                common, row, plan = self.gate_fixture(head=head)
                self.write_at(common, data)
                self.assertEqual(self.gate(row, plan), expected)
                # A decided reflog is complete evidence: the row keeps its class.
                self.assert_row(row, plan, "merged-removable", [], False, [])

        # The read: one fs_call() of at most 65,536 bytes of
        # logs/refs/heads/<branch> under the common directory, each `/` of the
        # branch a directory level (R-33, R-56 Q-6).
        common, row, plan = self.gate_fixture(head=OWN)
        path = self.write_at(common, padded(CREATED + COMMIT, 4 * BOUND, head=OWN))
        reads, real_fs_call = [], project.fs_call

        def counted(fn, *args, **kwargs):
            reads.append((fn, args, kwargs))
            return real_fs_call(fn, *args, **kwargs)
        with mock.patch.object(project, "fs_call", side_effect=counted):
            self.assertEqual(self.gate(row, plan), "reflog-unavailable", "a file of 262,144 bytes")
        self.assertEqual(reads, [(project._read_head, (os.fsencode(path), BOUND), {})])

        # ENOENT, ENOTDIR, 0 bytes and the bound reached: reflog-unavailable,
        # the row complete; 65,535 bytes decided by their entries.
        for label, prepare, head, expected in [
            ("ENOENT: no reflog", lambda common: None, TIP, "reflog-unavailable"),
            ("ENOTDIR: logs/refs/heads/feature is a file",
             lambda common: self.write_at(common, CREATED, branch="feature"), TIP, "reflog-unavailable"),
            ("0 bytes", lambda common: self.write_at(common, b""), TIP, "reflog-unavailable"),
            ("65,536 bytes", lambda common: self.write_at(common, padded(CREATED + COMMIT, BOUND)), OWN,
             "reflog-unavailable"),
            ("65,537 bytes", lambda common: self.write_at(common, padded(CREATED + COMMIT, BOUND + 1)), OWN,
             "reflog-unavailable"),
            ("65,535 bytes, a movement", lambda common: self.write_at(common, padded(CREATED + COMMIT, BOUND - 1)),
             OWN, None),
            ("65,535 bytes, no movement", lambda common: self.write_at(common, padded(CREATED, BOUND - 1)), TIP,
             "unstarted-branch"),
        ]:
            with self.subTest(case=label):
                self.temp_common_reset()
                common, row, plan = self.gate_fixture(head=head)
                prepare(common)
                self.assertEqual(self.gate(row, plan), expected)
                self.assert_row(row, plan, "merged-removable", [], False, [])

        # Any other OSError: the row is inspection-error with an os-error for
        # OPERATION read, and the plan incomplete (M5).
        def denied(path, limit):
            raise PermissionError(errno.EACCES, os.strerror(errno.EACCES))
        for label, prepare, read_head, number in [
            ("EISDIR: a directory at the reflog's path",
             lambda common: self.reflog_at(common).mkdir(parents=True), project._read_head, errno.EISDIR),
            ("EACCES", lambda common: self.write_at(common, CREATED), denied, errno.EACCES),
        ]:
            with self.subTest(case=label):
                self.temp_common_reset()
                common, row, plan = self.gate_fixture()
                prepare(common)
                with mock.patch.object(project, "_read_head", read_head):
                    self.assertEqual(self.gate(row, plan), "inspection-error")
                error = {"code": "os-error",
                         "message": TEXT["row_error_os_error"].format(OPERATION="read", STRERROR=os.strerror(number))}
                self.assert_row(row, plan, "inspection-error", [error], False, ["inspection-incomplete"])
                self.assertEqual(row["recommendation"], INSPECTION_ERROR)

        # A read not finished within the filesystem budget, the deadline not
        # being the limit: reflog-unavailable, the row left unprobed with its
        # probe-timeout, its class kept, and the plan incomplete with
        # inspection-incomplete (R-67 (a)). The budget is the 15 s of an
        # invocation with no deadline, set to 0.3 s in TIMING here. A read the
        # work deadline cuts, 0.3 s of work left under clean's deadline, leaves
        # the row the same, reflog-unavailable and unprobed with its class
        # kept, its error deadline-exceeded, and the plan incomplete with
        # deadline-exceeded, not inspection-incomplete, the row
        # deadline_stopped() (#19's round (h) at b3228bb, pcl:713-718 and
        # design D10; Brett Heap's ruling "O-1: deadline-exceeded", lead
        # rulings R-263 and R-278).
        with self.subTest(case="timeout"):
            self.temp_common_reset()
            common, row, plan = self.gate_fixture()
            self.write_at(common, CREATED)
            with mock.patch.dict(project.TIMING, {"inspect_budget": 0.3}), \
                    mock.patch.object(project, "_read_head", self.stuck_read()):
                self.assertEqual(self.gate(row, plan), "reflog-unavailable")
            cut = {"code": "probe-timeout",
                   "message": TEXT["row_error_probe_timeout"].format(OPERATION="read", S="0.3")}
            self.assert_row(row, plan, "merged-removable", [cut], True, ["inspection-incomplete"])
            self.assertEqual(row["recommendation"], MERGED_REMOVABLE)
            self.assertFalse(project.deadline_stopped(row))
        with self.subTest(case="deadline"):
            self.temp_common_reset()
            common, row, plan = self.gate_fixture()
            self.write_at(common, CREATED)
            with project.Invocation("clean") as run, \
                    mock.patch.object(project, "_read_head", self.stuck_read()):
                run.work_end = run.now() + 0.3
                self.assertEqual(self.gate(row, plan, run), "reflog-unavailable")
            cut = {"code": "deadline-exceeded",
                   "message": TEXT["row_error_deadline_exceeded"].format(OPERATION="read")}
            self.assert_row(row, plan, "merged-removable", [cut], True, ["deadline-exceeded"])
            self.assertEqual(row["recommendation"], MERGED_REMOVABLE)
            self.assertTrue(project.deadline_stopped(row))
            self.assertEqual(project.incomplete_refusal(plan, "deadline-exceeded").as_object(),
                             {"code": "deadline-exceeded", "message": TEXT["plan_incomplete"].format(
                                 CODE="deadline-exceeded", REMEDY=TEXT["remedy_deadline_exceeded"])})
        with self.subTest(case="an unprobed row keeps a reason"):
            self.temp_common_reset()
            common, row, plan = self.gate_fixture()
            self.write_at(common, CREATED)
            with mock.patch.dict(project.TIMING, {"inspect_budget": 0.3}), \
                    mock.patch.object(project, "_read_head", self.stuck_read()), \
                    project.Invocation() as run:
                selected, excluded = project.gate_rows([row], plan, run)
            self.assertEqual((selected, excluded), ([], [(row, "reflog-unavailable")]))
            self.assertTrue(row.unprobed)

    def temp_common_reset(self):
        """Remove the in-process fixture's common directory, so that a subtest
        starts from logs/refs/heads/ alone."""
        common = self.base / "common.git"
        if common.exists():
            for directory, names, files in os.walk(common, topdown=False):
                for name in files:
                    os.unlink(os.path.join(directory, name))
                for name in names:
                    os.rmdir(os.path.join(directory, name))
            os.rmdir(common)

    def test_clean_reflog_gate_outcomes_in_a_run(self):
        # The two read failures end to end: a directory at the reflog's path
        # (EISDIR, another OSError) and a FIFO there, whose open never returns,
        # so that fs_call() abandons the read at its budget. That run goes
        # through the launcher with the real table but probe_budget 1 (rule 5),
        # so every child and filesystem call gets min(1 s, work left).
        root = self.repo()
        self.bare_remote()
        control = self.merged_worktree("001-control")
        broken = self.merged_worktree("002-broken")
        reflog = self.reflog_file("002-broken")
        refused = "REFUSED: " + TEXT["plan_incomplete"].format(
            CODE="inspection-incomplete", REMEDY=TEXT["remedy_inspection_incomplete"]) + "\n"
        table = clean_support.timing_table(probe_budget=1)
        for label, prepare, timing, classification, reason, error in [
            ("EISDIR", reflog.mkdir, None, "inspection-error", "inspection-error",
             {"code": "os-error",
              "message": TEXT["row_error_os_error"].format(OPERATION="read", STRERROR=os.strerror(errno.EISDIR))}),
            ("FIFO", lambda: os.mkfifo(reflog), table, "merged-removable", "reflog-unavailable",
             {"code": "probe-timeout", "message": TEXT["row_error_probe_timeout"].format(OPERATION="read", S="1")}),
        ]:
            with self.subTest(case=label):
                if reflog.is_dir():
                    reflog.rmdir()
                else:
                    reflog.unlink()
                prepare()
                result = self.run_json("clean", root, "--all-safe", "--json", timing=timing, launched=True)
                self.assert_status(result, 1)
                plan = result.document
                rows = {row["path"]: row for row in plan["worktrees"]}
                self.assertEqual((rows[str(broken)]["classification"], rows[str(broken)]["errors"]),
                                 (classification, [error]))
                self.assertEqual(([entry["path"] for entry in plan["selected"]], plan["completeness"],
                                  plan["apply_allowed"], [refusal["code"] for refusal in plan["refusals"]]),
                                 ([str(control)], "incomplete", False, ["inspection-incomplete"]))
                self.assertEqual({entry["path"]: entry["reason"] for entry in plan["excluded"]},
                                 {str(root): "main-worktree", str(broken): reason})
                result = self.run_launched(timing, "clean", root, "--all-safe", "--apply", "--yes")
                self.assert_status(result, 2)
                self.assertEqual(result.stderr, refused)
                self.assertNotIn("[yes/N]", result.stdout)
                self.assertTrue(control.is_dir() and broken.is_dir(), "nothing removed")

    def main_in_process(self, *argv, fs_call=None):
        """project's main(ARGV) in this process, in self.env, fs_call replaced
        by its stand-in: (status, stdout, stderr). A small helper of this
        module's own (tasks.md rule 3), as test_clean_gates.py has one."""
        out, err = io.StringIO(), io.StringIO()
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.dict(os.environ, self.env, clear=True))
            stack.enter_context(mock.patch.object(project, "fs_call", fs_call))
            stack.enter_context(contextlib.redirect_stdout(out))
            stack.enter_context(contextlib.redirect_stderr(err))
            status = project.main([os.fspath(arg) for arg in argv])
        return status, out.getvalue(), err.getvalue()

    def test_clean_a_reflog_read_cut_by_the_deadline_against_its_budget(self):
        # #19's round (h) at b3228bb (pcl:713-718, design D10; Brett Heap's
        # ruling "O-1: deadline-exceeded", lead rulings R-263 and R-278). In
        # process, the read of one row's branch reflog made to time out at its
        # budget, the deadline not being the limit, and to be cut by the work
        # deadline; every other filesystem call runs as it is. Either cut
        # leaves the row as gate 7 leaves an unfinished read: excluded as
        # `reflog-unavailable`, its unprobed marker set (read off the row
        # reflog_gate() returned for, since no document writes the marker),
        # its class and recommendation kept, the read's error its one error,
        # and in the preview's `reflog-unavailable` group, never the
        # `inspection-error` one. The budget's cut makes the plan incomplete
        # with inspection-incomplete, whose remedy is the repair one; the
        # deadline's with deadline-exceeded alone, whose refusal prints the
        # deadline's remedy and never the repair one. The preview exits 1,
        # --apply 2, nothing removed.
        root = self.repo()
        self.bare_remote()
        control = self.merged_worktree("001-control")
        cut = self.merged_worktree("002-cut")
        reflog = os.fsencode(self.reflog_file("002-cut"))
        real_fs_call, real_gate = project.fs_call, project.reflog_gate
        excluded = [
            TEXT["excluded_heading"].format(M=2),
            TEXT["excluded_group"].format(REASON="main-worktree", K=1, NEXT_STEP=STEPS["main-worktree"]),
            TEXT["excluded_row"].format(PATH=root, BRANCH="main"),
            TEXT["excluded_group"].format(REASON="reflog-unavailable", K=1, NEXT_STEP=STEPS["reflog-unavailable"]),
            TEXT["excluded_row"].format(PATH=cut, BRANCH="002-cut"),
        ]
        cases = (
            ("its budget", project.DriverOutcome(None, "timeout", detail="no answer within 5 s"),
             {"code": "probe-timeout", "message": TEXT["row_error_probe_timeout"].format(OPERATION="read", S="5")},
             "inspection-incomplete", TEXT["remedy_inspection_incomplete"], False),
            ("the work deadline", project.DriverOutcome(None, "deadline", detail="no time was left to start it"),
             {"code": "deadline-exceeded", "message": TEXT["row_error_deadline_exceeded"].format(OPERATION="read")},
             "deadline-exceeded", TEXT["remedy_deadline_exceeded"], True),
        )
        for label, answer, error, code, remedy, stopped in cases:
            with self.subTest(f"the reflog read meets {label}"):
                calls, gated = [], []

                def fs_call(fn, *args, answer=answer, calls=calls, **options):
                    if fn is project._read_head and args[:1] == (reflog,):
                        calls.append(args[0])
                        return answer
                    return real_fs_call(fn, *args, **options)

                def reflog_gate(row, plan, run, gated=gated):
                    reason = real_gate(row, plan, run)
                    if row["path"] == str(cut):
                        gated.append((reason, row))
                    return reason

                message = TEXT["plan_incomplete"].format(CODE=code, REMEDY=remedy)
                with mock.patch.object(project, "reflog_gate", reflog_gate):
                    for words, status in ((("--all-safe", "--json"), 1),
                                          (("--all-safe", "--apply", "--yes", "--json"), 2)):
                        out_status, out, err = self.main_in_process("clean", root, *words, fs_call=fs_call)
                        self.assertEqual(out_status, status, out + err)
                        document = json.loads(out)
                        self.assertEqual(([entry["path"] for entry in document["selected"]],
                                          {entry["path"]: entry["reason"] for entry in document["excluded"]}),
                                         ([str(control)], {str(root): "main-worktree", str(cut): "reflog-unavailable"}))
                        [row] = [row for row in document["worktrees"] if row["path"] == str(cut)]
                        self.assertEqual((row["classification"], row["recommendation"], row["errors"]),
                                         ("merged-removable", MERGED_REMOVABLE, [error]))
                        self.assertEqual((document["completeness"], document["apply_allowed"], document["refusals"]),
                                         ("incomplete", False, [{"code": code, "message": message}]))
                    # The human preview: the row in the reflog-unavailable group.
                    out_status, out, err = self.main_in_process("clean", root, "--all-safe", fs_call=fs_call)
                    self.assertEqual((out_status, err), (1, "REFUSED: " + message + "\n"), out)
                    lines = out.splitlines()
                    self.assertIn(excluded[0], lines, out)
                    at = lines.index(excluded[0])
                    self.assertEqual(lines[at:at + len(excluded)], excluded, out)
                    self.assertNotIn(STEPS["inspection-error"], out)
                    out_status, out, err = self.main_in_process("clean", root, "--all-safe", "--apply", "--yes",
                                                                fs_call=fs_call)
                    self.assertEqual((out_status, err), (2, "REFUSED: " + message + "\n"), out)
                    self.assertNotIn("[yes/N]", out)
                if stopped:
                    self.assertNotIn(TEXT["remedy_inspection_incomplete"], err)
                self.assertEqual(calls, [reflog] * 4, "one read per run")
                # The row each run's gate 7 left: unprobed, its class kept, the
                # read's error its one error, and deadline_stopped() for the
                # deadline's cut alone.
                self.assertEqual([(reason, row["classification"], row["errors"], row.unprobed,
                                   project.deadline_stopped(row)) for reason, row in gated],
                                 [("reflog-unavailable", "merged-removable", [error], True, stopped)] * 4)
                self.assertTrue(control.is_dir() and cut.is_dir(), "nothing removed")

    def test_clean_only_gate_7_s_deadline_cut_makes_an_unprobed_row_deadline_stopped(self):
        # The completeness rule's scope (#19's round (h) at b3228bb; lead
        # ruling R-278): deadline_stopped() names an unprobed row whose every
        # error is deadline-exceeded, and it changes no other row's outcome.
        # First, reflog_gate() is the unprobed marker's only setter, so the
        # unprobed arm is gate 7's reflog read alone; a new setter must
        # revisit the rule.
        setters = []
        for statement in ast.parse(clean_support.CLI.read_text()).body:
            name = getattr(statement, "name", "<module>")
            for node in ast.walk(statement):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target] if isinstance(
                    node, (ast.AugAssign, ast.AnnAssign)) else []
                if any(isinstance(target, ast.Attribute) and target.attr == "unprobed"
                       for each in targets for target in ast.walk(each)):
                    setters.append(name)
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "setattr"
                        and any(isinstance(arg, ast.Constant) and arg.value == "unprobed" for arg in node.args)):
                    setters.append(name)
        self.assertEqual(setters, ["reflog_gate"])

        def row(path, classification="merged-removable", errors=(), unprobed=False):
            made = project.WorktreeRow(path=path, present=True, branch=path, head=TIP.decode(),
                                       classification=classification, recommendation=MERGED_REMOVABLE,
                                       locked=False, path_valid_utf8=True, errors=[dict(error) for error in errors])
            made.raw_path, made.main, made.registered, made.unprobed = os.fsencode(path), False, True, unprobed
            return made

        def plan_of(*rows, omitted=0, errors=(), excluded=()):
            plan = project.Plan({"root": Path("/w/main")}, types.SimpleNamespace(mode="all-safe", action=None))
            plan.evidence = {"identity": None, "errors": list(errors)}
            plan.rows, plan.excluded = list(rows), list(excluded)
            plan.omitted = {"count": omitted, "exactness": "exact"}
            return plan

        stopped = {"code": "deadline-exceeded", "message": TEXT["row_error_deadline_exceeded"].format(OPERATION="read")}
        timed_out = {"code": "probe-timeout",
                     "message": TEXT["row_error_probe_timeout"].format(OPERATION="read", S="5")}
        failed = {"code": "os-error", "message": TEXT["row_error_os_error"].format(
            OPERATION="listdir", STRERROR=os.strerror(errno.EACCES))}
        # (label, row, deadline_stopped(row), its plan's codes alone). Only the
        # first changes with the rule; every other row is decided as before.
        cases = [
            ("gate 7's read cut by the deadline", row("/w/a", errors=[stopped], unprobed=True),
             True, ["deadline-exceeded"]),
            ("gate 7's read cut at its budget", row("/w/b", errors=[timed_out], unprobed=True),
             False, ["inspection-incomplete"]),
            ("unprobed with no row error", row("/w/c", unprobed=True), False, ["inspection-incomplete"]),
            ("unprobed, one error of the deadline and one of the budget",
             row("/w/d", errors=[stopped, timed_out], unprobed=True), False, ["inspection-incomplete"]),
            ("inspection-error, every error the deadline's (the status probe, gates 9 to 12)",
             row("/w/e", "inspection-error", [stopped]), True, ["deadline-exceeded"]),
            ("inspection-error, another gate's read cut at its budget",
             row("/w/f", "inspection-error", [timed_out]), False, ["inspection-incomplete"]),
            ("inspection-error, a read that failed", row("/w/g", "inspection-error", [failed]),
             False, ["inspection-incomplete"]),
            ("inspection-error with no row error (registration-mismatch)", row("/w/h", "inspection-error"),
             False, ["inspection-incomplete"]),
            ("a complete row", row("/w/i"), False, []),
            ("a complete row carrying a deadline-exceeded", row("/w/j", errors=[stopped]), False, []),
        ]
        for label, made, expected, codes in cases:
            with self.subTest(case=label):
                self.assertEqual((project.deadline_stopped(made), project.plan_completeness(plan_of(made))),
                                 (expected, codes))
        gate_7_cut, budget_cut = cases[0][1], cases[1][1]
        other_cut = cases[5][1]
        with self.subTest(case="the row cap and the repository-wide probes stay their own codes"):
            self.assertEqual(project.plan_completeness(plan_of(omitted=3)), ["inspect-cap"])
            self.assertEqual(project.plan_completeness(plan_of(gate_7_cut, omitted=3)),
                             ["inspect-cap", "deadline-exceeded"])
            self.assertEqual(project.plan_completeness(plan_of(budget_cut, errors=[stopped])),
                             ["inspection-incomplete", "deadline-exceeded"])
            self.assertEqual(project.plan_completeness(plan_of(gate_7_cut, errors=[timed_out])),
                             ["inspection-incomplete", "deadline-exceeded"])
        with self.subTest(case="beside another row, each counts toward its own code"):
            plan = plan_of(gate_7_cut, other_cut, excluded=[(gate_7_cut, "reflog-unavailable"),
                                                           (other_cut, "inspection-error")])
            self.assertEqual(project.plan_completeness(plan), ["inspection-incomplete", "deadline-exceeded"])
            self.assertEqual([project.incomplete_refusal(plan, code).as_object() for code in
                              project.plan_completeness(plan)],
                             [{"code": "inspection-incomplete", "message": TEXT["plan_incomplete"].format(
                                 CODE="inspection-incomplete", REMEDY=TEXT["remedy_inspection_incomplete"])},
                              {"code": "deadline-exceeded", "message": TEXT["plan_incomplete"].format(
                                  CODE="deadline-exceeded", REMEDY=TEXT["remedy_deadline_exceeded"])}])
        with self.subTest(case="the variant remedy does not count a deadline-stopped row"):
            # 63e4573's counting: incomplete_refusal() counts the rows
            # plan_completeness() counts toward inspection-incomplete, so a
            # deadline-stopped row is not among them. Each pairing below is
            # built by hand to show the count: the variant prints where a
            # counted row is excluded as registration-mismatch, and the base
            # where only the deadline-stopped one is.
            remedy = {}
            for name, marked in (("the gate-7 deadline cut", gate_7_cut),
                                 ("another gate's budget cut", other_cut)):
                plan = plan_of(gate_7_cut, other_cut, excluded=[(marked, "registration-mismatch")])
                remedy[name] = str(project.incomplete_refusal(plan, "inspection-incomplete"))
            self.assertEqual(remedy, {
                "the gate-7 deadline cut": TEXT["plan_incomplete"].format(
                    CODE="inspection-incomplete", REMEDY=TEXT["remedy_inspection_incomplete"]),
                "another gate's budget cut": TEXT["plan_incomplete"].format(
                    CODE="inspection-incomplete", REMEDY=TEXT["remedy_inspection_incomplete_redirect"])})

    # T060: the reflog scenarios.

    def preview(self, root):
        """`clean ROOT --all-safe --json`, complete and exit 0: ({path: reason}
        of the excluded rows, [path] of the selected, the document)."""
        result = self.run_json("clean", root, "--all-safe", "--json")
        self.assert_status(result, 0)
        document = result.document
        self.assertEqual(document["completeness"], "complete", document["refusals"])
        return ({entry["path"]: entry["reason"] for entry in document["excluded"]},
                [entry["path"] for entry in document["selected"]], document)

    def assert_single_refused(self, root, tree, reason):
        """`--apply --action remove --worktree TREE --yes` refuses with
        target-excluded, reason REASON, exit 2, and TREE and its branch stay;
        the same under --json, its refusal object naming TREE."""
        branch = self.git(tree, "symbolic-ref", "--short", "HEAD").strip()
        result = self.run_cli("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes")
        self.assert_status(result, 2)
        self.assertEqual(result.stderr, "REFUSED: " + TEXT["target_excluded_gate"].format(
            REASON=reason, NEXT_STEP=STEPS[reason]) + "\n")
        result = self.run_json("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes", "--json")
        self.assert_status(result, 2)
        self.assertEqual([(refusal["code"], refusal.get("reason"), refusal.get("path"))
                          for refusal in result.document["refusals"]],
                         [("target-excluded", reason, str(tree))])
        self.assertTrue(tree.is_dir(), "the worktree is not removed")
        self.assertEqual(self.git(root, "branch", "--list", branch).strip().lstrip("+* "), branch)

    def reflog_lines(self, branch, root=None):
        return self.reflog_file(branch, root).read_bytes().splitlines()

    def test_clean_a_published_branch_with_no_commit_of_its_own(self):
        root = self.repo()
        self.bare_remote()
        control = self.merged_worktree("001-control")
        tree = self.unstarted_worktree("x")
        lines = self.reflog_lines("x")
        self.assertEqual((len(lines), lines[0][:40]), (1, ZERO), "only the creation entry; push -u adds none")
        excluded, selected, _ = self.preview(root)
        self.assertEqual(selected, [str(control)])
        self.assertEqual(excluded, {str(root): "main-worktree", str(tree): "unstarted-branch"})
        result = self.run_cli("clean", root, "--all-safe")
        self.assert_status(result, 0)
        self.assertIn("\n" + TEXT["excluded_group"].format(REASON="unstarted-branch", K=1,
                                                           NEXT_STEP=STEPS["unstarted-branch"])
                      + "\n" + TEXT["excluded_row"].format(PATH=tree, BRANCH="x") + "\n", result.stdout)
        # Before this change a named removal removed it.
        self.assert_single_refused(root, tree, "unstarted-branch")
        # A rename writes an entry with equal objects: still unstarted.
        self.git(root, "branch", "-m", "x", "y")
        old, new = self.reflog_lines("y")[-1].split(b" ")[:2]
        self.assertEqual(old, new)
        excluded, selected, document = self.preview(root)
        self.assertEqual((selected, excluded[str(tree)]), ([str(control)], "unstarted-branch"))
        self.assertEqual([entry["branch"] for entry in document["excluded"] if entry["path"] == str(tree)], ["y"])

    def test_clean_gate_7_s_step_names_the_checks_of_the_gates_that_did_not_run(self):
        # Brett Heap's Q5, "yes, recommended for Q1-Q9" (lead R-380; lane 2's
        # wave 22 triage T5, sr-classification M-2). Gate 7 precedes gates 9
        # to 12, which do not run for a row it excludes, so its step names
        # their checks: a detached commit that only the HEAD reflog holds,
        # and an assume-unchanged edit, each in a worktree whose branch has
        # no commit of its own, both unstarted-branch. "Review, then git
        # worktree remove yourself", followed literally, deleted either; the
        # checks the step now names show each.
        root = self.repo()
        self.bare_remote()
        self.merged_worktree("001-control")
        held = self.unstarted_worktree("lane-held")
        hidden = self.unstarted_worktree("lane-hidden")
        self.git(held, "checkout", "-q", "--detach")
        (held / "y.txt").write_text("detached work, only copy\n")
        detached = self.commit(held, "detached Y")
        self.git(held, "checkout", "-q", "lane-held")
        self.git(hidden, "update-index", "--assume-unchanged", "work-001-control")
        (hidden / "work-001-control").write_text("an edit Git is told to ignore\n")
        step = STEPS["unstarted-branch"]
        self.assertEqual(step, "no commit was made on this branch here since it was created; its later gates did "
                               "not run, so check git log -g HEAD, git ls-files -v and git status there, then git "
                               "worktree remove yourself (--force if it holds a submodule, once its commits are kept)")
        self.assertEqual(STEPS["reflog-unavailable"],
                         "the branch's reflog is missing, expired or undecidable; " + step.split("; ", 1)[1])
        excluded, _, _ = self.preview(root)
        self.assertEqual({path: excluded[path] for path in (str(held), str(hidden))},
                         {str(held): "unstarted-branch", str(hidden): "unstarted-branch"})
        result = self.run_cli("clean", root, "--all-safe")
        self.assert_status(result, 0)
        self.assertIn(TEXT["excluded_group"].format(REASON="unstarted-branch", K=2, NEXT_STEP=step),
                      result.stdout.splitlines())
        for tree in (held, hidden):
            with self.subTest(tree=tree.name):
                self.assert_single_refused(root, tree, "unstarted-branch")
        # The checks, as the step names them: git log -g HEAD shows the
        # detached commit, and git ls-files -v the flagged entry (h), which
        # git status does not show.
        self.assertIn(detached, self.git(held, "log", "-g", "HEAD", "--format=%H").split())
        self.assertIn("h work-001-control", self.git(hidden, "ls-files", "-v").splitlines())
        self.assertEqual(self.git(hidden, "status", "--porcelain"), "")
        self.assertEqual((held / "y.txt").exists(), False)
        self.assertEqual(self.git(held, "cat-file", "-t", detached).strip(), "commit")
        self.assertEqual((hidden / "work-001-control").read_text(), "an edit Git is told to ignore\n")

    def test_clean_a_fast_forward_merged_branch_at_the_target_s_tip_stays_eligible(self):
        root = self.repo()
        self.bare_remote()
        tree = self.base / "ff-tree"
        self.git(root, "worktree", "add", "-b", "ff", tree)
        (tree / "work-ff").write_text("done")
        head = self.commit(tree)
        self.git(tree, "push", "-u", "origin", "ff")
        self.git(root, "merge", "--ff-only", "ff")
        self.assertEqual(self.git(root, "rev-parse", "main").strip(), head, "the merge target sits at the branch's head")
        lines = self.reflog_lines("ff")
        self.assertEqual([(line[:40] == ZERO, line.split(b"\t", 1)[1].split(b":")[0]) for line in lines],
                         [(True, b"branch"), (False, b"commit")], "its commit follows the creation entry")
        excluded, selected, _ = self.preview(root)
        self.assertEqual((selected, excluded), ([str(tree)], {str(root): "main-worktree"}))
        result = self.run_cli("clean", root, "--all-safe", "--apply", "--yes")
        self.assert_status(result, 0)
        self.assertFalse(tree.exists(), "the worktree is removed")
        self.assertEqual(self.git(root, "rev-parse", "ff").strip(), head, "its branch is kept at its head")
        self.assertNotIn(f"worktree {tree}", self.git(root, "worktree", "list", "--porcelain").splitlines())

    def test_clean_a_branch_reset_to_the_merge_target_s_tip_stays_unstarted(self):
        root = self.repo()
        self.bare_remote()
        control = self.merged_worktree("001-control")
        tree = self.merged_worktree("002-reset")
        self.git(root, "worktree", "remove", tree)
        self.git(root, "worktree", "add", "-B", "002-reset", tree, "main")
        # Publish the reset head, so that the row is neither ahead nor behind its
        # upstream and reaches gate 7; a push writes no entry in the branch's reflog.
        self.git(tree, "push", "origin", "002-reset")
        lines = self.reflog_lines("002-reset")
        self.assertEqual([line.partition(b"\t")[2] for line in lines],
                         [b"branch: Created from HEAD", b"commit: fixture", b"branch: Reset to main"])
        self.assertEqual(lines[-1].split(b" ")[1].decode(), self.git(root, "rev-parse", "main").strip())
        excluded, selected, _ = self.preview(root)
        self.assertEqual(selected, [str(control)])
        self.assertEqual(excluded, {str(root): "main-worktree", str(tree): "unstarted-branch"})

    def test_clean_a_branch_fetched_at_the_merge_target_s_tip_stays_unstarted(self):
        root = self.repo()
        self.bare_remote()
        control = self.merged_worktree("001-control")
        tip = self.git(root, "rev-parse", "main").strip()
        self.git(root, "push", "origin", "main:feat")
        self.git(root, "fetch", "origin", "feat:f1")
        self.git(root, "update-ref", "refs/heads/f2", tip)
        self.git(root, "push", ".", "main:f3")
        trees = {}
        for branch in ("f1", "f2", "f3"):
            self.git(root, "branch", "-u", "origin/feat", branch)
            trees[branch] = self.base / f"{branch}-tree"
            self.git(root, "worktree", "add", trees[branch], branch)
        # Each reflog holds its one creation entry, whose old object is all
        # zeros and whose message does not begin `branch:`; neither `branch -u`
        # nor `worktree add` adds an entry.
        self.assertEqual({branch: [(line[:41], line[41:81], line.partition(b"\t")[1:])
                                   for line in self.reflog_lines(branch)] for branch in trees},
                         {"f1": [(ZERO + b" ", tip.encode(), (b"\t", b"fetch origin feat:f1: storing head"))],
                          "f2": [(ZERO + b" ", tip.encode(), (b"", b""))],
                          "f3": [(ZERO + b" ", tip.encode(), (b"\t", b"push"))]})
        excluded, selected, _ = self.preview(root)
        self.assertEqual(selected, [str(control)])
        self.assertEqual(excluded, {str(root): "main-worktree",
                                    **{str(tree): "unstarted-branch" for tree in trees.values()}})

    def test_clean_a_branch_whose_reflog_is_missing_empty_or_expired(self):
        root = self.repo()
        self.bare_remote()
        # A head that is a strict ancestor of the merge target, with no reflog.
        ancestor = self.merged_worktree("001-ancestor")
        self.delete_reflog("001-ancestor")
        # A 0-byte reflog, as `git reflog expire` leaves one whose every entry expired.
        empty = self.merged_worktree("003-empty")
        self.empty_reflog("003-empty")
        # Created and committed to 100 days ago, renamed now: `git reflog expire`
        # at its defaults (gc.reflogExpire, 90 days) keeps only the rename entry.
        expired = self.merged_worktree("004-old", path=self.base / "004-expired-tree")
        self.backdate_reflog("004-old", 100 * DAY)
        self.git(root, "branch", "-m", "004-old", "004-expired")
        self.git(root, "reflog", "expire", "--all")
        lines = self.reflog_lines("004-expired")
        self.assertEqual(len(lines), 1, lines)
        self.assertEqual(lines[0].split(b" ")[0], lines[0].split(b" ")[1], "only the rename entry survives")
        # A head equal to the merge target's SHA, with no reflog: last, so that
        # no later merge moves the target past it.
        at_tip = self.base / "002-tip-tree"
        self.git(root, "worktree", "add", "-b", "002-tip", at_tip)
        (at_tip / "work-002-tip").write_text("done")
        head = self.commit(at_tip)
        self.git(at_tip, "push", "-u", "origin", "002-tip")
        self.git(root, "merge", "--ff-only", "002-tip")
        self.delete_reflog("002-tip")
        self.assertEqual(self.git(root, "rev-parse", "main").strip(), head)
        self.assertNotEqual(self.git(root, "rev-parse", "001-ancestor").strip(), head)
        self.git(root, "merge-base", "--is-ancestor", "001-ancestor", "main")
        trees = (ancestor, empty, expired, at_tip)
        excluded, selected, document = self.preview(root)
        self.assertEqual(selected, [])
        self.assertEqual(excluded, {str(root): "main-worktree", **{str(tree): "reflog-unavailable" for tree in trees}})
        self.assertEqual({row["path"]: row["classification"] for row in document["worktrees"]},
                         {str(root): "protected-default", **{str(tree): "merged-removable" for tree in trees}})
        # Not removed: with nothing eligible, the apply prints "No eligible
        # worktrees" and exits 0 without asking.
        result = self.run_cli("clean", root, "--all-safe", "--apply", "--yes")
        self.assert_status(result, 0)
        self.assertIn(TEXT["empty_line"] + "\n", result.stdout)
        self.assertTrue(all(tree.is_dir() for tree in trees), "nothing removed")
        # Before this change a named removal removed each of them.
        for tree in trees:
            with self.subTest(worktree=tree.name):
                self.assert_single_refused(root, tree, "reflog-unavailable")


if __name__ == "__main__":
    unittest.main()
