"""Shared helpers of the clean test modules (feature 004, lane B: T009 to T011).

Discovery never collects this file, since it is not test*.py; a test module
imports what it needs by name (`from clean_support import CleanCase, ...`),
because `python3 -m unittest discover -s tests` puts tests/ on sys.path. Nothing
here imports tests/test_project.py or binds ProjectTests, and no module imports
this one with `import *` (tasks.md, "Rules for every new test", rule 3):
loadTestsFromModule would otherwise run the 96 tests again.

load_project() loads `project` under its own module name, `project_clean`,
separate from the `project_cli` that tests/test_project.py loads, so a test
patches the module object it calls.
"""
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "project"
LAUNCHER = ROOT / "tests" / "launch_project.py"
MODULE_NAME = "project_clean"
TIMEOUT = 20  # seconds: run_cli's limit; every test ends inside it (rule 5)


def _which_git():
    found = shutil.which("git")
    return os.path.abspath(found) if found else None


# The real git, resolved once when this module is imported, before any test puts
# a counting wrapper or a fake git first on a PATH (lead ruling R-31). Fixture
# setup calls it by this absolute path, so a wrapper never counts a fixture call.
REAL_GIT = _which_git()

# The seventeen names every Git child of `project` runs without, in the order of
# the Environment requirement (openspec/changes/add-project-clean-all-safe/specs/
# project-command/spec.md:98-110), and the one name read-only probes set. These
# are this harness's own transcription: the counting wrapper records them, and
# CleanCase removes them from the base environment so a child sees only what the
# test sets.
SCRUBBED_NAMES = (
    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_CONFIG", "GIT_CONFIG_PARAMETERS",
    "GIT_CONFIG_COUNT", "GIT_OBJECT_DIRECTORY", "GIT_DIR", "GIT_WORK_TREE",
    "GIT_IMPLICIT_WORK_TREE", "GIT_GRAFT_FILE", "GIT_INDEX_FILE",
    "GIT_NO_REPLACE_OBJECTS", "GIT_REPLACE_REF_BASE", "GIT_PREFIX",
    "GIT_SHALLOW_FILE", "GIT_COMMON_DIR", "GIT_INTERNAL_SUPER_PREFIX",
    "GIT_ALLOW_PROTOCOL",
)
OPTIONAL_LOCKS = "GIT_OPTIONAL_LOCKS"

# The fixed author and committer of every fixture commit (rule 4).
AUTHOR = {
    "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
    "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@example.invalid",
}

_project = None


def load_project():
    """`project` as a module named project_clean, loaded as tests/test_project.py
    loads it (SourceFileLoader, spec_from_loader) and registered in sys.modules
    before exec_module, since a @dataclass under postponed annotations looks its
    module up there while the class is built (lead ruling R-29). Its __name__ is
    not "__main__", so the guard at the end of `project` does not run the CLI.
    Loaded once; every later call returns the same module object."""
    global _project
    if _project is None:
        loader = importlib.machinery.SourceFileLoader(MODULE_NAME, str(CLI))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules[loader.name] = module
        try:
            loader.exec_module(module)
        except BaseException:
            sys.modules.pop(loader.name, None)
            raise
        _project = module
    return _project


def timing_table(factor=None, **values):
    """A whole TIMING table for run_launched(): every real value of `project`'s
    table multiplied by factor (left as it is when factor is None), then each
    named value set as given. An unknown name raises KeyError, as the launcher
    refuses it. Each time-bound test names its own factor or table (lead ruling
    R-29); no one factor serves every test."""
    real = getattr(load_project(), "TIMING", None)
    if not isinstance(real, dict):
        raise AssertionError("project has no TIMING table (region timing, T006)")
    unknown = sorted(set(values) - set(real))
    if unknown:
        raise KeyError(f"timing_table: unknown TIMING keys {unknown}")
    table = {key: value if factor is None else value * factor for key, value in real.items()}
    table.update(values)
    return table


def _git_version(git):
    """(major, minor) of `git --version`, or None when it cannot be read."""
    if not git:
        return None
    try:
        output = subprocess.run([git, "--version"], capture_output=True, text=True,
                                timeout=TIMEOUT).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    match = re.match(r"git version (\d+)\.(\d+)", output)
    return (int(match.group(1)), int(match.group(2))) if match else None


GIT_VERSION = _git_version(REAL_GIT)

# Skip decorators; each prints its reason (rule 9).
linux_paths = unittest.skipUnless(
    sys.platform.startswith("linux"),
    "non-UTF-8 path fixtures run on Linux only: macOS file systems refuse names "
    "that are not UTF-8 (FR-066)")
not_root = unittest.skipIf(
    hasattr(os, "geteuid") and os.geteuid() == 0,
    "permission fixtures do not bind the superuser (effective uid 0)")
git_236_to_239 = unittest.skipUnless(
    GIT_VERSION is not None and (2, 36) <= GIT_VERSION <= (2, 39),
    "needs the git on PATH to be 2.36 to 2.39, found "
    + (".".join(map(str, GIT_VERSION)) if GIT_VERSION else "none")
    + "; the git-floor job runs it (FR-067)")


def _arg(value):
    """One argument for a child: bytes stay bytes (a non-UTF-8 path), a path
    becomes its string, anything else str()."""
    if isinstance(value, (str, bytes)):
        return value
    if isinstance(value, os.PathLike):
        return os.fspath(value)
    return str(value)


def _text(data):
    if data is None:
        return ""
    if isinstance(data, bytes):
        return data.decode("utf-8", "surrogateescape")
    return data


def transcript(result):
    """A run's command, exit status and both streams, for a failure message."""
    command = " ".join(shlex.quote(os.fsdecode(arg)) for arg in result.args)
    return (f"$ {command}\nexit {result.returncode}\n--- stdout ---\n{_text(result.stdout)}"
            f"\n--- stderr ---\n{_text(result.stderr)}")


class CleanCase(unittest.TestCase):
    """The base of the clean test classes. It has no test methods, so a module
    that binds it runs nothing extra. setUp builds what ProjectTests.setUp
    builds (tests/test_project.py:117-136): a resolved temporary base, a fake
    workBenches with the test generator, and self.env with WORKBENCHES_ROOT,
    HOME, PROJECTS_DIR, GIT_CONFIG_NOSYSTEM=1 and GIT_CONFIG_GLOBAL=os.devnull;
    plus a fixed author and committer, and none of the seventeen scrubbed names
    or GIT_OPTIONAL_LOCKS inherited from the caller."""

    def setUp(self):
        super().setUp()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.wb = self.base / "work benches"
        (self.wb / "config").mkdir(parents=True)
        scripts = self.wb / "devBenches/testBench/scripts"
        scripts.mkdir(parents=True)
        self.generator = scripts / "new-test.sh"
        self.generator.write_text('#!/bin/bash\nmkdir -p "$2/$1"\nprintf "%s\\n" "$1" "$2" > "$2/$1/arguments"\n')
        self.config = {"benches": {"testBench": {"path": "devBenches/testBench",
            "ai_keywords": ["python"], "project_scripts": [
                {"name": "test", "script": "scripts/new-test.sh"},
                {"name": "update-test", "script": "scripts/update-test.sh"},
                {"name": "missing", "script": "scripts/missing.sh"}]}}}
        self.save_config()
        env = {**os.environ, "WORKBENCHES_ROOT": str(self.wb),
               "HOME": str(self.base / "home"), "SPECKIT_WORKSPACE_PATH": "",
               "PROJECTS_DIR": str(self.base), "GIT_CONFIG_NOSYSTEM": "1",
               "GIT_CONFIG_GLOBAL": os.devnull, **AUTHOR}
        for name in (*SCRUBBED_NAMES, OPTIONAL_LOCKS):
            env.pop(name, None)
        self.env = env

    def save_config(self):
        (self.wb / "config/bench-config.json").write_text(json.dumps(self.config))

    def _run(self, argv, cwd, env, input):
        try:
            return subprocess.run(argv, cwd=self.base if cwd is None else cwd,
                                  env=self.env if env is None else env, input=input,
                                  capture_output=True, encoding="utf-8",
                                  errors="surrogateescape", timeout=TIMEOUT)
        except subprocess.TimeoutExpired as exc:
            late = subprocess.CompletedProcess(argv, "killed", exc.stdout, exc.stderr)
            self.fail(f"run passed {TIMEOUT} s\n{transcript(late)}")

    def run_cli(self, *args, cwd=None, env=None, input=""):
        """`python3 project ARGS...` with standard input "" (at its end at once) and
        a 20 s timeout, in self.base and self.env unless cwd or env is given.
        Streams are text, decoded as UTF-8 with surrogateescape."""
        return self._run([sys.executable, str(CLI), *map(_arg, args)], cwd, env, input)

    def run_launched(self, timing, *args, cwd=None, env=None, input=""):
        """As run_cli, through tests/launch_project.py, which runs project's main() in
        its own process with TIMING replaced by the given table, passed first as
        --timing=JSON (lead ruling R-29); timing None runs the real table. Build the
        table with timing_table(factor, **values) and record in the test the factor
        or values it names and the probe budget they yield (plan review U1)."""
        prefix = [] if timing is None else [
            "--timing=" + json.dumps(timing, separators=(",", ":"), sort_keys=True)]
        return self._run([sys.executable, str(LAUNCHER), *prefix, *map(_arg, args)],
                         cwd, env, input)

    def load_json(self, result):
        """Standard output parsed by one json.loads, so it must hold exactly one
        JSON document (rule 10); the test fails with the run's transcript if not."""
        try:
            return json.loads(result.stdout)
        except ValueError as exc:
            self.fail(f"standard output is not exactly one JSON document: {exc}\n{transcript(result)}")

    def run_json(self, *args, timing=None, launched=False, cwd=None, env=None, input=""):
        """run_cli (or run_launched, when timing is given or launched is true) with
        its standard output parsed by load_json(); returns the run with the parsed
        document as its `document` attribute. Name --json among the arguments."""
        if launched or timing is not None:
            result = self.run_launched(timing, *args, cwd=cwd, env=env, input=input)
        else:
            result = self.run_cli(*args, cwd=cwd, env=env, input=input)
        result.document = self.load_json(result)
        return result

    def assert_status(self, result, code):
        self.assertEqual(result.returncode, code, "\n" + transcript(result))

    def git(self, path, *args, env=None, input=None, check=True):
        """The real git (REAL_GIT, by absolute path; lead ruling R-31) run as
        `git -C PATH ARGS...` in self.env; fails the test on a nonzero exit unless
        check is false. Returns standard output as text (surrogateescape, so
        os.fsencode() gives back the bytes)."""
        self.assertIsNotNone(REAL_GIT, "no git was found on PATH when clean_support loaded")
        result = subprocess.run([REAL_GIT, "-C", _arg(path), *map(_arg, args)],
                                env=self.env if env is None else env, input=input,
                                capture_output=True, encoding="utf-8",
                                errors="surrogateescape", timeout=TIMEOUT)
        if check:
            self.assertEqual(result.returncode, 0, "\n" + transcript(result))
        return result.stdout

    def commit(self, path, message="fixture", allow_empty=False):
        """Stage everything in the worktree at path and commit it with the fixed
        author and committer, through REAL_GIT; returns the new commit's SHA."""
        self.git(path, "add", "-A")
        self.git(path, "commit", "-q", *(["--allow-empty"] if allow_empty else []), "-m", message)
        return self.git(path, "rev-parse", "HEAD").strip()
