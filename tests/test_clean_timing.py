"""Lane A of feature 004: the timing table and its launcher (T005).

research.md R10 and lead rulings R-26 and R-29: every time constant of `project`
lives in one module-level table, TIMING, read when its reader is called; tests
replace it through tests/launch_project.py, never through an environment
variable, a flag or a file that `project` reads (FR-066).
"""
import ast
import contextlib
import json
import os
import re
import signal
import subprocess
import sys
import time
import unittest
from unittest.mock import patch

from clean_support import (CLI, LAUNCHER, TIMEOUT, CleanCase, child_log, install_counting_git,
                           install_fake_git, load_project, timing_table, transcript)
import launch_project

# T005's table as literals (R10; data-model.md "Constants"), in seconds.
REAL_TIMING = {"invocation_deadline": 60, "reconciliation_reserve": 10, "probe_budget": 5,
               "removal_floor": 5, "removal_ceiling": 300, "inspect_budget": 15,
               "term_grace": 2, "reap_wait": 2, "selector_tick": 0.1}

# Parameter names that would hold a timing value: T005's five words, any name ending
# in one of them after an underscore, and the table's own keys (plan review M16).
TIMING_WORDS = ("grace", "budget", "timeout", "tick", "wait")

# Calls that change a dict in place.
MUTATORS = {"update", "setdefault", "pop", "popitem", "clear", "__setitem__", "__delitem__",
            "__ior__"}

# Constants compared between a launched module and a plain load; anything else
# (a lock, a slot object) compares by identity and is left out.
PLAIN_DATA = (dict, list, tuple, set, frozenset, str, bytes, int, float, bool, type(None), re.Pattern)

# The status child's lifetime under the status-hangs-in fake: it sleeps until it is
# cut, ending by itself after 10 s.
STATUS_LIFETIME = 10


def project_tree():
    source = CLI.read_text(encoding="utf-8")
    return source, ast.parse(source, str(CLI))


def is_timing(node):
    return isinstance(node, ast.Name) and node.id == "TIMING"


def is_number(node, numbers=frozenset()):
    """True for a numeric literal, arithmetic on numeric literals, or a module-level
    name bound to one (a derived constant)."""
    if isinstance(node, ast.Constant):
        return isinstance(node.value, (int, float, complex)) and not isinstance(node.value, bool)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        return is_number(node.operand, numbers)
    if isinstance(node, ast.BinOp):
        return is_number(node.left, numbers) and is_number(node.right, numbers)
    return isinstance(node, ast.Name) and node.id in numbers


def timing_reads(node, where, found):
    """Append (where, line) for every read of TIMING under node; where says when the
    read is evaluated: "function" inside a function body, else "module", "class
    attribute", "default argument", "decorator" or "annotation"."""
    if isinstance(node, ast.Name):
        if node.id == "TIMING" and isinstance(node.ctx, ast.Load):
            found.append((where, node.lineno))
        return
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
        arguments = node.args
        for default in (*arguments.defaults, *arguments.kw_defaults):
            if default is not None:
                timing_reads(default, "default argument", found)
        for argument in (*arguments.posonlyargs, *arguments.args, *arguments.kwonlyargs,
                         arguments.vararg, arguments.kwarg):
            if argument is not None and argument.annotation is not None:
                timing_reads(argument.annotation, "annotation", found)
        if isinstance(node, ast.Lambda):
            timing_reads(node.body, "function", found)
            return
        for decorator in node.decorator_list:
            timing_reads(decorator, "decorator", found)
        if node.returns is not None:
            timing_reads(node.returns, "annotation", found)
        for statement in node.body:
            timing_reads(statement, "function", found)
        return
    if isinstance(node, ast.ClassDef):
        for part in (*node.decorator_list, *node.bases, *node.keywords):
            timing_reads(part, where, found)
        for statement in node.body:
            timing_reads(statement, "class attribute", found)
        return
    for child in ast.iter_child_nodes(node):
        timing_reads(child, where, found)


class TimingTests(CleanCase):
    def test_clean_timing_table_holds_every_time_constant(self):
        project = load_project()
        self.assertEqual(project.TIMING, REAL_TIMING)
        for key, value in project.TIMING.items():
            self.assertTrue(isinstance(value, (int, float)) and not isinstance(value, bool),
                            f"TIMING[{key!r}] is {value!r}, not a number")

        source, tree = project_tree()
        lines = source.splitlines()
        opened = [number for number, line in enumerate(lines, 1) if line == "# region timing"]
        closed = [number for number, line in enumerate(lines, 1) if line == "# endregion timing"]
        self.assertEqual((len(opened), len(closed)), (1, 1), "region timing must be marked once")
        inside = [node for node in tree.body if opened[0] < node.lineno <= closed[0]
                  or opened[0] <= node.end_lineno < closed[0]]
        self.assertEqual(len(inside), 1, "region timing holds one statement, the TIMING table")
        assignment = inside[0]
        self.assertTrue(opened[0] < assignment.lineno and assignment.end_lineno < closed[0])
        self.assertIsInstance(assignment, ast.Assign)
        self.assertEqual(len(assignment.targets), 1)
        self.assertTrue(is_timing(assignment.targets[0]), "the region assigns TIMING")
        table = assignment.value
        self.assertIsInstance(table, ast.Dict, "TIMING is one dict display")
        self.assertNotIn(None, table.keys, "no ** unpacking feeds TIMING")
        for key, value in zip(table.keys, table.values):
            self.assertTrue(isinstance(key, ast.Constant) and isinstance(key.value, str),
                            f"line {key.lineno}: a TIMING key is a string literal")
            self.assertTrue(isinstance(value, ast.Constant) and isinstance(value.value, (int, float))
                            and not isinstance(value.value, bool),
                            f"line {value.lineno}: TIMING[{getattr(key, 'value', key)!r}] is a numeric literal")
        self.assertEqual(ast.literal_eval(table), REAL_TIMING)

        # Nothing anywhere else in project rebinds, shadows or changes the table, so no
        # environment variable, flag or file can feed it.
        writes = []
        for node in ast.walk(tree):
            if node is assignment.targets[0]:
                continue
            if isinstance(node, ast.Name) and node.id == "TIMING" and not isinstance(node.ctx, ast.Load):
                writes.append((node.lineno, "TIMING rebound or deleted"))
            elif isinstance(node, (ast.Global, ast.Nonlocal)) and "TIMING" in node.names:
                writes.append((node.lineno, "TIMING declared global or nonlocal"))
            elif isinstance(node, ast.alias) and "TIMING" in (node.name, node.asname):
                writes.append((node.lineno, "TIMING imported"))
            elif isinstance(node, ast.arg) and node.arg == "TIMING":
                writes.append((node.lineno, "TIMING shadowed by a parameter"))
            elif isinstance(node, ast.ExceptHandler) and node.name == "TIMING":
                writes.append((node.lineno, "TIMING shadowed by an except clause"))
            elif isinstance(node, ast.Subscript) and is_timing(node.value) and not isinstance(node.ctx, ast.Load):
                writes.append((node.lineno, "an entry of TIMING assigned or deleted"))
            elif isinstance(node, ast.Attribute) and is_timing(node.value) and node.attr in MUTATORS:
                writes.append((node.lineno, f"TIMING.{node.attr} called"))
        self.assertEqual(writes, [], "only region timing sets TIMING")

    def test_clean_timing_is_read_at_call_time(self):
        _, tree = project_tree()
        found = []
        for statement in tree.body:
            timing_reads(statement, "module", found)
        self.assertEqual([(line, where) for where, line in found if where != "function"], [],
                         "TIMING is read only inside function bodies (lead ruling R-29)")

        numbers = {target.id for statement in tree.body if isinstance(statement, ast.Assign)
                   and is_number(statement.value) for target in statement.targets
                   if isinstance(target, ast.Name)}
        held = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                continue
            arguments = node.args
            positional = (*arguments.posonlyargs, *arguments.args)
            pairs = list(zip(positional[len(positional) - len(arguments.defaults):], arguments.defaults))
            pairs += [pair for pair in zip(arguments.kwonlyargs, arguments.kw_defaults) if pair[1] is not None]
            for argument, default in pairs:
                name = argument.arg
                timed = (name in TIMING_WORDS or name in REAL_TIMING
                         or any(name.endswith("_" + word) for word in TIMING_WORDS))
                if timed and is_number(default, numbers):
                    held.append((default.lineno, getattr(node, "name", "lambda"), name))
        self.assertEqual(held, [], "no default argument holds a timing value (plan review M16)")

    def test_clean_launcher_replaces_the_table(self):
        fresh = load_project()
        argv, path = list(sys.argv), list(sys.path)

        # Imported as a module: exactly the named keys change, as floats.
        overrides = {"term_grace": 0.25, "probe_budget": 1}
        with patch.dict(sys.modules):
            module, rest = launch_project.prepare(["--timing=" + json.dumps(overrides), "status", "--json"])
            self.assertIs(sys.modules["project_cli"], module, "registered before it executes")
        self.assertEqual(module.__name__, "project_cli")
        self.assertEqual(rest, ["status", "--json"])
        self.assertEqual(module.TIMING, {**REAL_TIMING, "term_grace": 0.25, "probe_budget": 1.0})
        self.assertEqual({key: type(module.TIMING[key]) for key in overrides},
                         {key: float for key in overrides})
        # Every other constant is left alone, LIMITS among them once T004 adds it.
        constants = sorted(name for name, value in vars(fresh).items()
                           if name.isupper() and name != "TIMING" and isinstance(value, PLAIN_DATA))
        self.assertTrue(constants)
        for name in constants:
            self.assertEqual(getattr(module, name), getattr(fresh, name), name)
        self.assertEqual(fresh.TIMING, REAL_TIMING, "the shared project_clean module is untouched")

        # An unknown key exits nonzero, naming it and only it.
        with patch.dict(sys.modules), self.assertRaises(SystemExit) as caught:
            launch_project.prepare(['--timing={"term_grace": 1, "no_such_key": 1}', "status"])
        self.assertIsInstance(caught.exception.code, str, "sys.exit(message) exits 1")
        self.assertIn("no_such_key", caught.exception.code)
        self.assertNotIn("term_grace", caught.exception.code)

        # Without --timing first, the real table stands.
        for arguments in (["status"], ["status", '--timing={"term_grace": 1}']):
            with self.subTest(arguments=arguments), patch.dict(sys.modules):
                plain, rest = launch_project.prepare(arguments)
                self.assertEqual(plain.TIMING, REAL_TIMING)
                self.assertEqual(rest, arguments)
        self.assertEqual((sys.argv, sys.path), (argv, path), "prepare() changes neither")

        # Run as a script: --help prints project's usage and exits 0, with or without a table.
        expected = self.run_cli("--help")
        self.assert_status(expected, 0)
        self.assertTrue(expected.stdout.startswith("usage: project "), transcript(expected))
        for table in (None, timing_table(term_grace=0.5)):
            with self.subTest(table=table):
                launched = self.run_launched(table, "--help")
                self.assertEqual((launched.returncode, launched.stdout, launched.stderr),
                                 (expected.returncode, expected.stdout, expected.stderr), transcript(launched))
        refused = self.run_launched({"no_such_key": 1}, "status")
        self.assert_status(refused, 1)
        self.assertEqual(refused.stdout, "", transcript(refused))
        self.assertIn("no_such_key", refused.stderr, transcript(refused))

    def test_clean_launcher_replaces_the_table_keeps_project_s_streams_and_exit_status(self):
        repo = self.repo()
        statuses = set()
        for arguments in (("status", repo, "--json"), ("clean", repo), ("clean", "--no-such-flag"),
                          ("status", self.base / "missing")):
            with self.subTest(arguments=arguments):
                plain = self.run_cli(*arguments)
                launched = self.run_launched(None, *arguments)
                self.assertEqual((launched.returncode, launched.stdout, launched.stderr),
                                 (plain.returncode, plain.stdout, plain.stderr),
                                 f"\n{transcript(plain)}\n{transcript(launched)}")
                statuses.add(plain.returncode)
        self.assertTrue({0, 2} <= statuses, statuses)

    def interrupted_status(self, repo, launcher, signum, label):
        """`project status REPO`, run as python3 project or through the launcher in a new
        session, with the counting wrapper first on PATH over the status-hangs-in fake:
        the status child in REPO sleeps until it is cut, ending by itself after 10 s, and
        every other command, the version check and the pins included, is the real git's.
        Once the wrapper has recorded the status child, project's process group is read
        while project runs, and signum goes to project's pid alone. Returns project's pid,
        the status child's pid and its parent's pid (from the wrapper's first `status`
        record) with project's process group, and project's exit status and streams."""
        bin_dir = self.base / f"bin-{label}"
        log = self.base / f"children-{label}.log"
        fake = install_fake_git(self.base / f"fake-{label}", "status-hangs-in", path=repo,
                                lifetime=STATUS_LIFETIME)
        install_counting_git(bin_dir, log, real=fake)
        argv = [sys.executable, str(LAUNCHER if launcher else CLI), "status", str(repo)]
        child = subprocess.Popen(argv, cwd=self.base, env=self.path_first(bin_dir),
                                 stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, start_new_session=True)
        try:
            deadline = time.monotonic() + TIMEOUT / 2
            while True:
                status = [record for record in child_log(log) if "status" in record.argv]
                if status:
                    break
                if child.poll() is not None or time.monotonic() > deadline:
                    child.kill()
                    out, err = child.communicate()
                    self.fail(f"{label}: the status child never started\n"
                              f"exit {child.returncode}\n--- stdout ---\n{out.decode()}\n"
                              f"--- stderr ---\n{err.decode()}")
                time.sleep(0.02)
            fields = [status[0].pid, status[0].ppid, os.getpgid(child.pid)]
            os.kill(child.pid, signum)
            out, err = child.communicate(timeout=TIMEOUT / 2)
        finally:
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(child.pid, signal.SIGKILL)  # a status child left in project's group
            if child.poll() is None:
                child.wait()
        return child.pid, fields, child.returncode, out.decode(), err.decode()

    def test_clean_launcher_replaces_the_table_runs_project_in_its_own_process(self):
        repo = self.repo()
        for signum in (signal.SIGINT, signal.SIGTERM):
            name = signal.Signals(signum).name
            with self.subTest(signal=name):
                runs = {}
                for label, launcher in (("plain", False), ("launched", True)):
                    pid, (_, parent, group), code, out, err = self.interrupted_status(
                        repo, launcher, signum, f"{label}-{name}")
                    # The status child's parent is the process the test started, and that
                    # process leads its own group: no process stands between them.
                    self.assertEqual((parent, group), (pid, pid), f"{label} {name}")
                    runs[label] = (code, out, err)
                # project's own signal handlers decide the exit status and the streams.
                self.assertEqual(runs["launched"], runs["plain"], name)
                self.assertNotEqual(runs["plain"][0], 0, name)


if __name__ == "__main__":
    unittest.main()
