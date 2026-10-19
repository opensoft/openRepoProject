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
import contextlib
import errno
import fcntl
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import re
import select
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import termios
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "project"
LAUNCHER = ROOT / "tests" / "launch_project.py"
MODULE_NAME = "project_clean"
TIMEOUT = 20  # seconds: run_cli's limit; every test ends inside it (rule 5)
PTY_EOF = "\x04"  # written alone to the pseudo-terminal: end of input at a prompt


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
REFLOG_IDENT = "Test <test@example.invalid>"  # the identity of a reflog entry written here

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


def cli_argv(*args):
    """The command `python3 project ARGS...`."""
    return [sys.executable, str(CLI), *map(_arg, args)]


def launched_argv(timing, *args):
    """The command that runs project's main() through tests/launch_project.py, the
    table first as --timing=JSON (T007's interface; lead ruling R-29), or with the
    real table when timing is None."""
    prefix = [] if timing is None else [
        "--timing=" + json.dumps(timing, separators=(",", ":"), sort_keys=True)]
    return [sys.executable, str(LAUNCHER), *prefix, *map(_arg, args)]


def _take_controlling_terminal():
    """preexec_fn of run_pty_steps(controlling_tty=True): runs in the child after
    start_new_session's setsid(), and makes the pseudo-terminal on its standard
    input the new session's controlling terminal (lead ruling R-31). The test's
    own; project never uses a preexec_fn (C4)."""
    fcntl.ioctl(0, termios.TIOCSCTTY, 0)


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
        self.root = None  # the first repository repo() makes; the builders' default

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
        return self._run(cli_argv(*args), cwd, env, input)

    def run_launched(self, timing, *args, cwd=None, env=None, input=""):
        """As run_cli, through tests/launch_project.py, which runs project's main() in
        its own process with TIMING replaced by the given table, passed first as
        --timing=JSON (lead ruling R-29); timing None runs the real table. Build the
        table with timing_table(factor, **values) and record in the test the factor
        or values it names and the probe budget they yield (plan review U1)."""
        return self._run(launched_argv(timing, *args), cwd, env, input)

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

    # Fixture builders (T010). Each calls REAL_GIT by absolute path, so a counting
    # wrapper on the PATH of the run under test never records a fixture call.

    def _root(self, root):
        root = self.root if root is None else root
        self.assertIsNotNone(root, "no repository: call repo() first or pass root")
        return Path(os.fsdecode(root))

    def _tree(self, branch, path):
        if path is None:
            return self.base / (branch.replace("/", "-") + "-tree")
        return Path(os.fsdecode(path))  # bytes too: os.fsencode() gives them back

    def _init_repo(self, path, branch):
        path.mkdir(parents=True, exist_ok=True)
        self.git(path, "init", "-q", "-b", branch)
        self.git(path, "commit", "-q", "--allow-empty", "-m", "initial")
        return path

    def repo(self, name="repo", branch="main"):
        """A repository at self.base/name on branch with one empty commit, as
        ProjectTests.repo makes it. The first one becomes self.root, the default
        repository of the other builders."""
        path = self._init_repo(self.base / name, branch)
        if self.root is None:
            self.root = path
        return path

    def bare_remote(self, root=None, name="remote.git"):
        """A local bare repository at self.base/name, added to root (self.root by
        default) as origin; no network is ever involved (rule 4)."""
        remote = self.base / name
        self.git(self.base, "init", "-q", "--bare", remote)
        self.git(self._root(root), "remote", "add", "origin", remote)
        return remote

    def merged_worktree(self, branch, path=None, root=None, setup=None):
        """tests/test_project.py:857's recipe, copied: `worktree add -b BRANCH PATH`,
        a file `work` committed as the branch's own commit, `push -u origin BRANCH`,
        then `merge --no-ff BRANCH` into root's checked-out branch, the merge
        target. setup(tree), when given, runs before that commit, so what it
        stages (a gitlink, a submodule) is committed and merged too. Needs an
        origin (bare_remote()). Returns the worktree's path."""
        root = self._root(root)
        tree = self._tree(branch, path)
        self.git(root, "worktree", "add", "-b", branch, tree)
        (tree / "work").write_text("done")
        if setup is not None:
            setup(tree)
        self.commit(tree)
        self.git(tree, "push", "-u", "origin", branch)
        self.git(root, "merge", "--no-ff", branch, "-m", f"merge {branch}")
        return tree

    def unstarted_worktree(self, branch, path=None, root=None, publish=True):
        """`worktree add -b BRANCH PATH` at root's head with no commit of its own,
        then, when publish is true, `push -u origin BRANCH`. Returns the path."""
        root = self._root(root)
        tree = self._tree(branch, path)
        self.git(root, "worktree", "add", "-b", branch, tree)
        if publish:
            self.git(tree, "push", "-u", "origin", branch)
        return tree

    def register_worktrees(self, count, prefix, root=None):
        """count linked worktrees registered directly (research.md R11): for each
        name PREFIX000, PREFIX001, ... an admin directory under the common
        directory's worktrees/ holding gitdir, commondir and HEAD (a branch of that
        name), and a directory self.base/NAME holding the .git file; then every
        branch is created at root's head by one `update-ref --stdin` child. No
        checkout and no index are written, so a row is clean only while root's
        head has an empty tree, as repo()'s first commit has. prefix is a plain
        file name. Returns the worktree paths in order."""
        root = self._root(root)
        common = self.common_dir(root)
        head = self.git(root, "rev-parse", "HEAD").strip()
        width = max(3, len(str(count - 1)))
        trees, commands = [], []
        for number in range(count):
            name = f"{prefix}{number:0{width}d}"
            tree = self.base / name
            admin = common / "worktrees" / name
            admin.mkdir(parents=True)
            tree.mkdir()
            (admin / "gitdir").write_text(f"{tree / '.git'}\n")
            (admin / "commondir").write_text("../..\n")
            (admin / "HEAD").write_text(f"ref: refs/heads/{name}\n")
            (tree / ".git").write_text(f"gitdir: {admin}\n")
            commands.append(f"create refs/heads/{name} {head}\n")
            trees.append(tree)
        if commands:
            self.git(root, "update-ref", "--stdin", input="".join(commands))
        return trees

    # Reflog surgery (D10): the branch's reflog under the common directory.

    def common_dir(self, root=None):
        return Path(self.git(self._root(root), "rev-parse", "--path-format=absolute",
                             "--git-common-dir").rstrip("\n"))

    def reflog_file(self, branch, root=None):
        return self.common_dir(root) / "logs" / "refs" / "heads" / branch

    def delete_reflog(self, branch, root=None):
        self.reflog_file(branch, root).unlink()

    def empty_reflog(self, branch, root=None):
        self.reflog_file(branch, root).write_bytes(b"")

    def write_reflog(self, branch, entries, root=None):
        """Replace the branch's reflog with entries, each (old, new, when, message)
        or raw bytes: when is a Unix time (None: now), so an entry can be written
        backdated, and a message of None writes no tab. Returns the bytes written."""
        lines = []
        for entry in entries:
            if isinstance(entry, bytes):
                lines.append(entry)
                continue
            old, new, when, message = entry
            stamp = int(time.time()) if when is None else int(when)
            line = f"{old} {new} {REFLOG_IDENT} {stamp} +0000"
            if message is not None:
                line += "\t" + message
            lines.append((line + "\n").encode())
        data = b"".join(lines)
        path = self.reflog_file(branch, root)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return data

    def backdate_reflog(self, branch, seconds, root=None):
        """Move every entry of the branch's reflog seconds into the past, so that
        `git reflog expire --expire=...` can drop them. Returns the new bytes."""
        path = self.reflog_file(branch, root)
        lines = []
        for line in path.read_bytes().splitlines(keepends=True):
            head, tab, message = line.partition(b"\t")
            ending = b"" if tab else head[len(head.rstrip(b"\n")):]
            prefix, stamp, zone = head.rstrip(b"\n").rsplit(b" ", 2)
            moved = str(int(stamp) - int(seconds)).encode()
            lines.append(prefix + b" " + moved + b" " + zone + ending + tab + message)
        data = b"".join(lines)
        path.write_bytes(data)
        return data

    def pad_reflog(self, branch, size=64 * 1024 + 1, root=None):
        """Grow the branch's reflog to exactly size bytes (by default one past 64
        KiB) by putting no-op entries before the existing ones: old and new both
        the branch's head (equal, so no movement) and a message `pad...` (no
        anchor), so the last entry and every anchor and movement stay as they
        were. Returns the new bytes."""
        root = self._root(root)
        path = self.reflog_file(branch, root)
        data = path.read_bytes()
        head = self.git(root, "rev-parse", f"refs/heads/{branch}").strip()
        first = data.split(b"\n", 1)[0].partition(b"\t")[0].rsplit(b" ", 2)
        stamp = first[1].decode() if len(first) == 3 else str(int(time.time()))

        def filler(length):
            return f"{head} {head} {REFLOG_IDENT} {stamp} +0000\t{('pad' + '.' * length)[:length]}\n".encode()

        bare = len(filler(0))
        full = bare + 200
        gap = size - len(data)
        count, rest = divmod(gap, full)
        if gap < 0 or (count == 0 and 0 < rest < bare + 3):
            raise ValueError(f"pad_reflog: cannot grow {len(data)} bytes to exactly {size}")
        pads = [filler(200)] * count
        if rest >= bare + 3:
            pads.append(filler(rest - bare))
        elif rest:
            pads.pop()
            split = rest + full - 2 * bare
            pads += [filler(split // 2), filler(split - split // 2)]
        data = b"".join(pads) + data
        assert len(data) == size, (len(data), size)
        path.write_bytes(data)
        return data

    def gitlink(self, tree, name="vendored", sha=None):
        """Stage a gitlink (mode 160000) named name in the index of the worktree at
        tree, over an empty directory, with no submodule behind it; sha defaults
        to that worktree's head. Pass it as merged_worktree(setup=...) to commit
        it. Returns name."""
        tree = Path(os.fsdecode(tree))
        (tree / name).mkdir(exist_ok=True)
        sha = sha or self.git(tree, "rev-parse", "HEAD").strip()
        self.git(tree, "update-index", "--add", "--cacheinfo", f"160000,{sha},{name}")
        return name

    def submodule(self, tree, name="sub", source=None):
        """The test's own `submodule add` of a local repository (source, or a new
        one at self.base/NAME-source) as name in the worktree at tree, passing
        `-c protocol.file.allow=always`; Git puts its repository under modules/ in
        that worktree's admin directory. Staged, not committed: pass it as
        merged_worktree(setup=...) to commit it. Returns the submodule's path."""
        tree = Path(os.fsdecode(tree))
        if source is None:
            source = self._init_repo(self.base / f"{name}-source", "main")
        self.git(tree, "-c", "protocol.file.allow=always", "submodule", "add", "-q", source, name)
        return tree / name

    # The pseudo-terminal runner (T010): tests/test_project.py:210-307 copied and
    # extended.

    pty_timeout = TIMEOUT  # seconds; a pty run that exceeds it fails with its transcript

    def run_pty_steps(self, argv, steps=(), controlling_tty=False, env=None, cwd=None,
                      timeout=None):
        """Run argv (cli_argv(...) or launched_argv(...)) with stdin and stdout on one
        pseudo-terminal and stderr on a pipe, in a new session.

        steps is a sequence of (expected, action). Each action is taken only once
        its expected text has appeared on either stream past the previous match on
        that stream ("" matches at once): a str is written with a newline, except
        that one control character (PTY_EOF, or "\\x03" typed as ^C) is written
        alone; bytes are written as they are; signal.SIGINT is sent to the child
        and repeated each second until it exits, as run_pty does; any other signal
        (SIGTERM, SIGHUP, SIGKILL) is sent to the child once; and a callable is
        called with the running child (a Popen), for instance to change the
        repository while the question waits. Signals go to the child only, never to
        the test process (rule 7).

        controlling_tty=True makes the pseudo-terminal the new session's controlling
        terminal (TIOCSCTTY after setsid, through a preexec_fn of the test's own;
        lead ruling R-31), so a child of project in its process group can open
        /dev/tty; without it that open fails with ENXIO.

        Returns a CompletedProcess whose stdout is the pty transcript (echoed input
        included) and stderr the pipe, both with \\r\\n read as \\n; its seen
        attribute holds, for each step, both transcripts as they stood when the
        action was taken."""
        argv = [_arg(arg) for arg in argv]
        limit = timeout or self.pty_timeout
        deadline = time.monotonic() + limit
        master, slave = os.openpty()
        try:
            child = subprocess.Popen(argv, cwd=self.base if cwd is None else cwd,
                                     env=self.env if env is None else env, stdin=slave,
                                     stdout=slave, stderr=subprocess.PIPE, start_new_session=True,
                                     preexec_fn=_take_controlling_terminal if controlling_tty else None)
        except BaseException:
            os.close(master)
            raise
        finally:
            os.close(slave)
        error = child.stderr.fileno()
        received = {master: bytearray(), error: bytearray()}
        cursor = {master: 0, error: 0}
        reading = [master, error]
        pending = list(steps)
        seen = []
        interrupted = exited = None

        def text(fd):
            return bytes(received[fd]).replace(b"\r\n", b"\n").decode("utf-8", "replace")

        def transcript():
            command = " ".join(shlex.quote(os.fsdecode(arg)) for arg in argv)
            return f"$ {command}\n--- pty ---\n{text(master)}\n--- stderr ---\n{text(error)}"

        def locate(expected):
            for fd in (master, error):
                found = text(fd).find(expected, cursor[fd])
                if found >= 0:
                    cursor[fd] = found + len(expected)
                    return True
            return False

        try:
            while True:
                if pending and locate(pending[0][0]):
                    action = pending.pop(0)[1]
                    seen.append(text(master) + text(error))
                    if isinstance(action, signal.Signals):
                        with contextlib.suppress(ProcessLookupError):
                            child.send_signal(action)
                        if action == signal.SIGINT:
                            interrupted = time.monotonic()
                    elif callable(action):
                        action(child)
                    else:
                        if isinstance(action, bytes):
                            data = action
                        elif len(action) == 1 and ord(action) < 32:
                            data = action.encode()
                        else:
                            data = (action + "\n").encode()
                        with contextlib.suppress(OSError):
                            os.write(master, data)
                    continue
                now = time.monotonic()
                if child.poll() is not None:
                    exited = exited or now
                    if not reading or now - exited > 2:
                        break
                elif interrupted is not None and now - interrupted >= 1:
                    child.send_signal(signal.SIGINT)
                    interrupted = now
                if now > deadline:
                    with contextlib.suppress(OSError):
                        os.killpg(child.pid, signal.SIGKILL)
                    child.wait()
                    waiting = repr(pending[0][0]) if pending else "the end of output"
                    self.fail(f"pty run timed out after {limit}s waiting for {waiting}\n{transcript()}")
                if not reading:
                    time.sleep(0.05)
                    continue
                for fd in select.select(reading, [], [], 0.05)[0]:
                    try:
                        chunk = os.read(fd, 65536)
                    except OSError as exc:
                        if exc.errno != errno.EIO:
                            raise
                        chunk = b""
                    if chunk:
                        received[fd] += chunk
                    else:
                        reading.remove(fd)
        finally:
            os.close(master)
            child.stderr.close()
            if child.poll() is None:
                with contextlib.suppress(OSError):
                    os.killpg(child.pid, signal.SIGKILL)
                child.wait()
        if pending:
            self.fail(f"the child exited before the step waiting for {pending[0][0]!r}\n{transcript()}")
        result = subprocess.CompletedProcess(argv, child.returncode, text(master), text(error))
        result.seen = seen
        return result
