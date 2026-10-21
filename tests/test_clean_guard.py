"""The internal-error guard of project clean (feature 004, lane H: T034).

Every test runs in process: project's main(), or the guard itself, called with
its standard streams captured, in CleanCase's environment, and the signal
handlers and wakeup descriptor in force before each call checked again after it,
even when it raises (tasks.md, "Rules for every new test", rule 7). Sources:
research.md R6; contracts/project-clean.md, "Streams" and "Extended error
object"; plan review M2, M6 and m12; lead rulings R-38, R-44 and R-45.
"""
import argparse
import contextlib
import io
import json
import os
import re
import signal
import subprocess
import unittest
from unittest import mock

import clean_support

project = clean_support.load_project()

# Where the faults are injected: the frozen stages of T047's pipeline, which
# T047 retargeted from discover and cleanup_report, one line each (analyze H3,
# lead rulings R-42 and R-49). Every stand-in below takes any arguments.
RESOLVING_STAGE = "resolve_clean_target"
PLANNING_STAGE = "build_plan"

REFUSED = "REFUSED: "
CANCELLED = "Cancelled.\n"
BOOM = "RuntimeError: boom"  # the contract's `TYPE: TEXT` for RuntimeError("boom")

# The extended error object's keys, in order, and the keys of the two objects it
# carries (contracts/project-clean.md, "Extended error object" and "Plan
# envelope"), written here as literals.
EXTENDED_ERROR_KEYS = ["error", "code", "schema_version", "observed_at", "mode", "repository",
                       "merge_target", "completeness", "apply_allowed", "refusals"]
REPOSITORY_KEYS = ["root", "common_dir", "dev", "ino", "root_valid_utf8", "common_dir_valid_utf8"]
MERGE_TARGET_KEYS = ["name", "source", "sha"]
OBSERVED_AT = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")

SCOPED_SIGNALS = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)


def raising(exc):
    """A stand-in for a stage that raises exc, whatever it is called with."""
    def stage(*args, **kwargs):
        raise exc
    return stage


def interrupting(signum, seen):
    """A stand-in for a stage during which signum arrives (lane F's note): it
    records signum in the slot of the invocation in force, appends that
    invocation to seen, and raises Interrupted as the driver does."""
    def stage(*args, **kwargs):
        invocation = project.current_invocation()
        seen.append(invocation)
        invocation.record_signal(signum)
        raise project.Interrupted(signum)
    return stage


def signal_state():
    """The handlers of SIGINT, SIGTERM and SIGHUP and the wakeup descriptor in force."""
    handlers = tuple(signal.getsignal(signum) for signum in SCOPED_SIGNALS)
    wakeup = signal.set_wakeup_fd(-1)
    if wakeup != -1:
        signal.set_wakeup_fd(wakeup)
    return handlers, wakeup


class GuardTests(clean_support.CleanCase):

    def setUp(self):
        super().setUp()
        self.repo()

    @contextlib.contextmanager
    def in_process(self, **stages):
        """os.environ replaced by self.env and each named function of project by
        its stand-in, for the block's span; on leaving, even by an exception, the
        signal handlers and wakeup descriptor must be those in force before."""
        before = signal_state()
        try:
            with contextlib.ExitStack() as stack:
                stack.enter_context(mock.patch.dict(os.environ, self.env, clear=True))
                for name, stage in stages.items():
                    stack.enter_context(mock.patch.object(project, name, stage))
                yield
        finally:
            self.assertEqual(signal_state(), before,
                             "the call left the signal handlers or the wakeup descriptor changed")

    def call_main(self, *argv, **stages):
        """project's main(argv) in process (in_process()); returns its status, its
        standard output and its standard error. What main() raises propagates."""
        out, err = io.StringIO(), io.StringIO()
        with self.in_process(**stages), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            status = project.main([os.fspath(arg) for arg in argv])
        return status, out.getvalue(), err.getvalue()

    def error_document(self, out):
        """Standard output as one extended error object (rule 10), written as
        write_document() writes it: indent 2, ASCII only, one newline (R-38)."""
        document = json.loads(out)
        self.assertEqual(out, json.dumps(document, indent=2, ensure_ascii=True) + "\n")
        self.assertEqual(list(document), EXTENDED_ERROR_KEYS)
        self.assertRegex(document["observed_at"], OBSERVED_AT)
        self.assertEqual(len(document["observed_at"]), len("2026-10-19T23:00:00Z"))
        return document

    def test_clean_an_unexpected_exception_is_an_internal_error(self):
        # research.md R6; plan review M6, m12: resolving and planning both refuse.
        for stage in (RESOLVING_STAGE, PLANNING_STAGE):
            with self.subTest(stage=stage, json=False):
                result = self.call_main("clean", self.root, **{stage: raising(RuntimeError("boom"))})
                self.assertEqual(result, (2, "", REFUSED + BOOM + "\n"))
            with self.subTest(stage=stage, json=True):
                status, out, err = self.call_main("clean", self.root, "--json",
                                                  **{stage: raising(RuntimeError("boom"))})
                self.assertEqual((status, err), (2, ""))
                document = self.error_document(out)
                self.assertEqual(document, {
                    "error": BOOM, "code": "internal-error", "schema_version": 1,
                    "observed_at": document["observed_at"], "mode": "report",
                    "repository": None, "merge_target": None, "completeness": "incomplete",
                    "apply_allowed": False,
                    "refusals": [{"code": "internal-error", "message": BOOM}],
                })

    def test_clean_the_guard_passes_refusals_and_signals_unchanged(self):
        # Plan review M2: the guard re-raises each of these, the same object.
        args = project.parser().parse_args(["clean", os.fspath(self.root)])
        for stage in (RESOLVING_STAGE, PLANNING_STAGE):
            for raised in (project.Refused("kept", code="no-merge-target"),
                           project.Interrupted(signal.SIGTERM), project.Terminated(signal.SIGHUP),
                           KeyboardInterrupt(), EOFError()):
                with self.subTest(stage=stage, raised=type(raised).__name__):
                    with self.in_process(**{stage: raising(raised)}), project.Invocation("clean"), \
                            self.assertRaises(type(raised)) as caught:
                        project.run_clean(args)
                    self.assertIs(caught.exception, raised)

    def test_clean_a_refusal_keeps_its_code_and_message(self):
        message = clean_support.TEXT_FIXTURES["no_merge_target"]
        refusal = project.Refused(message, code="no-merge-target")
        self.assertEqual(str(refusal), message)  # its message alone, the code never in it
        result = self.call_main("clean", self.root, **{PLANNING_STAGE: raising(refusal)})
        self.assertEqual(result, (2, "", REFUSED + message + "\n"))
        status, out, err = self.call_main("clean", self.root, "--json", **{PLANNING_STAGE: raising(refusal)})
        self.assertEqual((status, err), (2, ""))
        document = self.error_document(out)
        self.assertEqual((document["error"], document["code"], document["mode"]),
                         (message, "no-merge-target", "report"))
        self.assertEqual(document["refusals"], [{"code": "no-merge-target", "message": message}])

    def test_clean_cancelled_at_keyboard_interrupt_and_end_of_input(self):
        # Both pass the guard and keep main()'s Cancelled. and 130, with no document.
        for raised in (KeyboardInterrupt, EOFError):
            for extra in ((), ("--json",)):
                with self.subTest(raised=raised.__name__, arguments=extra):
                    result = self.call_main("clean", self.root, *extra, **{PLANNING_STAGE: raising(raised())})
                    self.assertEqual(result, (130, "", CANCELLED))

    def test_clean_a_signal_while_planning_exits_by_its_number(self):
        # FR-036: Interrupted with the signal in the slot exits 128 plus its
        # number, with Cancelled. and no document, never internal-error.
        for signum, status in ((signal.SIGTERM, 143), (signal.SIGHUP, 129), (signal.SIGINT, 130)):
            for extra in ((), ("--json",)):
                with self.subTest(signal=signum.name, arguments=extra):
                    seen = []
                    result = self.call_main("clean", self.root, *extra,
                                            **{PLANNING_STAGE: interrupting(signum, seen)})
                    self.assertEqual(result, (status, "", CANCELLED))
                    [invocation] = seen
                    self.assertEqual((invocation.command, invocation.signal), ("clean", signum))
        # Terminated, raised by raising_signals() for SIGTERM and SIGHUP, the same.
        for signum, status in ((signal.SIGTERM, 143), (signal.SIGHUP, 129)):
            with self.subTest(terminated=signum.name):
                result = self.call_main("clean", self.root, "--json",
                                        **{PLANNING_STAGE: raising(project.Terminated(signum))})
                self.assertEqual(result, (status, "", CANCELLED))

        # An Interrupted that names no signal exits by the slot's, else as SIGINT.
        def unnamed(*args, **kwargs):
            project.current_invocation().record_signal(signal.SIGHUP)
            raise project.Interrupted()
        self.assertEqual(self.call_main("clean", self.root, **{PLANNING_STAGE: unnamed}), (129, "", CANCELLED))
        self.assertEqual(self.call_main("clean", self.root, **{PLANNING_STAGE: raising(project.Interrupted())}),
                         (130, "", CANCELLED))

    def test_clean_the_guard_ends_where_the_apply_phase_begins(self):
        # R6: after the apply phase begins the guard converts nothing; the apply
        # phase decides that target itself (T093).
        def applying(*args, **kwargs):
            project.current_invocation().phase = "apply"
            raise RuntimeError("boom")
        with self.assertRaises(RuntimeError) as caught:
            self.call_main("clean", self.root, **{PLANNING_STAGE: applying})
        self.assertEqual(str(caught.exception), "boom")

    def test_clean_the_guard_is_clean_s_alone(self):
        # R6: status keeps its handling; a RuntimeError in snapshot() is not caught.
        seen = []

        def snapshot(*args, **kwargs):
            seen.append(project.current_invocation())
            raise RuntimeError("boom")
        with self.assertRaises(RuntimeError) as caught:
            self.call_main("status", self.root, snapshot=snapshot)
        self.assertEqual(str(caught.exception), "boom")
        [invocation] = seen
        self.assertEqual(invocation.command, "status")
        self.assertIsNot(project.current_invocation(), invocation)

    def test_clean_main_enters_a_fresh_invocation_for_each_call(self):
        # Lead ruling R-44 (1): main()'s one wiring line, an Invocation per call,
        # named by the subcommand and left when main() returns.
        seen = []

        def stage(*args, **kwargs):
            seen.append(project.current_invocation())
            raise project.Refused("stop", code="no-merge-target")
        for _ in range(2):
            self.assertEqual(self.call_main("clean", self.root, **{PLANNING_STAGE: stage})[0], 2)
        first, second = seen
        self.assertIsNot(first, second)
        for invocation in seen:
            self.assertEqual((invocation.command, invocation.phase, invocation.signal), ("clean", "planning", None))
        self.assertIsNot(project.current_invocation(), first)
        self.assertIsNot(project.current_invocation(), second)

    def test_clean_refusal_objects_and_the_extended_error_object(self):
        # data-model.md, "Refusal": {code, message, path?, path_valid_utf8?,
        # reason?}, the flag beside a path exactly when there is one.
        undecodable = b"/w/" + bytes([0xFF])
        refusal = project.Refused("excluded", code="target-excluded", path=undecodable, reason="dirty")
        self.assertEqual(str(refusal), "excluded")
        self.assertEqual(list(refusal.as_object().items()), [
            ("code", "target-excluded"), ("message", "excluded"),
            ("path", "/w/" + chr(92) + "xff"), ("path_valid_utf8", False), ("reason", "dirty")])
        self.assertEqual(project.Refused("plain", code="cancelled").as_object(),
                         {"code": "cancelled", "message": "plain"})
        self.assertEqual(project.Refused("named", code="unsupported-path-bytes", path="/w/ok").as_object(),
                         {"code": "unsupported-path-bytes", "message": "named", "path": "/w/ok",
                          "path_valid_utf8": True})
        # The context fills `repository` and `merge_target`, each in its key order.
        repository = {"ino": 2, "dev": 1, "common_dir_valid_utf8": True, "common_dir": "/r/.git",
                      "root_valid_utf8": True, "root": "/r"}
        merge_target = {"sha": "a" * 40, "source": "manifest", "name": "main"}
        manifest = project.Refused("Manifest /r/project.yaml is larger than 1 MiB.", code="manifest-invalid",
                                   context={"repository": repository, "merge_target": merge_target})
        args = project.parser().parse_args(["clean", "/r", "--json"])
        document = project.error_document(manifest, args)
        self.assertEqual(list(document), EXTENDED_ERROR_KEYS)
        self.assertEqual(list(document["repository"].items()), [(key, repository[key]) for key in REPOSITORY_KEYS])
        self.assertEqual(list(document["merge_target"].items()),
                         [(key, merge_target[key]) for key in MERGE_TARGET_KEYS])
        self.assertEqual(document["refusals"], [manifest.as_object()])
        # A context that names only the repository leaves `merge_target` null.
        early = project.Refused("early", code="no-merge-target", context={"repository": repository})
        self.assertIsNone(project.error_document(early, args)["merge_target"])

    def test_clean_mode_of_the_arguments(self):
        # data-model.md, "Plan": report, single and all-safe, read with getattr.
        cases = (
            (argparse.Namespace(), "report"),
            (project.parser().parse_args(["clean", "/r", "--json"]), "report"),
            (project.parser().parse_args(["clean", "/r", "--action", "remove", "--worktree", "/w"]), "report"),
            (project.parser().parse_args(["clean", "/r", "--apply", "--action", "remove", "--worktree", "/w"]),
             "single"),
            (argparse.Namespace(all_safe=True), "all-safe"),
            (argparse.Namespace(all_safe=True, apply=True, json=True), "all-safe"),
        )
        for args, mode in cases:
            with self.subTest(args=vars(args)):
                self.assertEqual(project.clean_mode(args), mode)

    def test_clean_write_document_is_the_one_writer(self):
        # R-38: ensure_ascii stays True, so a Cf code point is written escaped.
        mark = chr(0x202E)
        document = {"error": "x" + mark, "code": None, "refusals": [{"code": "cancelled", "message": "m"}]}
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            project.write_document(document)
        self.assertEqual(out.getvalue(), json.dumps(document, indent=2, ensure_ascii=True) + "\n")
        self.assertTrue(out.getvalue().isascii())
        self.assertEqual(json.loads(out.getvalue()), document)

    def test_clean_sighup_on_a_closed_terminal_exits_129(self):
        # R-54 X-3, lead ruling R-55 (T047): project runs with standard input and
        # standard error on a pseudo-terminal whose master side is closed before
        # it writes anything, so a write there fails with EIO. The
        # `signal-parent-in` fake then sends SIGHUP to project, its parent, from
        # the linked worktree's status probe, while it plans. main() writes
        # `Cancelled.` best-effort: the run exits 129. An uncaught exception would
        # exit 1, and a line left unflushed at exit would print `Exception ignored
        # ...` and exit 120; neither can show on the hung-up terminal, so the
        # status is the evidence. The signal goes to the child only (rule 7);
        # without a controlling terminal, closing the master signals nothing.
        tree = self.base / "feature-tree"
        self.git(self.root, "worktree", "add", "-q", "-b", "001-feature", tree)
        bin_dir = self.base / "bin"
        clean_support.install_fake_git(bin_dir, "signal-parent-in", path=tree, signal="HUP")
        master, slave = os.openpty()
        try:
            child = subprocess.Popen(clean_support.cli_argv("clean", self.root), cwd=self.base,
                                     env=self.path_first(bin_dir), stdin=slave, stdout=subprocess.PIPE,
                                     stderr=slave, start_new_session=True)
        finally:
            os.close(slave)
            os.close(master)
        try:
            out, _ = child.communicate(timeout=clean_support.TIMEOUT)
        except subprocess.TimeoutExpired:
            with contextlib.suppress(OSError):
                os.killpg(child.pid, signal.SIGKILL)
            child.communicate()
            self.fail(f"project did not end within {clean_support.TIMEOUT} s")
        self.assertEqual((child.returncode, out), (129, b""))


if __name__ == "__main__":
    unittest.main()
