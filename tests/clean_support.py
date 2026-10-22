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
import collections
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

# The thirty-one names every Git child of `project` runs without, in the order of
# specs/004-project-clean-all-safe/contracts/project-clean.md, "Git children"
# (:562-570), and the one name read-only probes set. This is the harness's own
# literal transcription, never imported from project's GIT_SCRUB (lead ruling
# R-42); test_clean_counting_wrapper_records_and_execs asserts the two equal, in
# order. The counting wrapper records these names, and CleanCase removes them
# from the base environment so a child sees only what the test sets.
SCRUBBED_NAMES = (
    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_CONFIG", "GIT_CONFIG_PARAMETERS",
    "GIT_CONFIG_COUNT", "GIT_OBJECT_DIRECTORY", "GIT_DIR", "GIT_WORK_TREE",
    "GIT_IMPLICIT_WORK_TREE", "GIT_GRAFT_FILE", "GIT_INDEX_FILE",
    "GIT_NO_REPLACE_OBJECTS", "GIT_REPLACE_REF_BASE", "GIT_PREFIX",
    "GIT_SHALLOW_FILE", "GIT_COMMON_DIR", "GIT_INTERNAL_SUPER_PREFIX",
    "GIT_ALLOW_PROTOCOL",
    # The fourteen trace names of Brett Heap's ruling Q9 B (PR #19).
    "GIT_TRACE", "GIT_TRACE_BARE", "GIT_TRACE_CURL", "GIT_TRACE_CURL_NO_DATA",
    "GIT_TRACE_FSMONITOR", "GIT_TRACE_PACKET", "GIT_TRACE_PACKFILE",
    "GIT_TRACE_PACK_ACCESS", "GIT_TRACE_PERFORMANCE", "GIT_TRACE_REDACT",
    "GIT_TRACE_REFS", "GIT_TRACE_SETUP", "GIT_TRACE_SHALLOW",
    "GIT_TRACE_WORKING_TREE_ENCODING",
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


# The counting wrapper (T011; plan review M4; lead rulings R-29 and R-31).


def _sh_quote(value):
    """value (str, bytes or a path) as one single-quoted sh word, as bytes."""
    data = value if isinstance(value, bytes) else os.fsencode(value)
    return b"'" + data.replace(b"'", b"'\\''") + b"'"


def _write_script(path, text):
    path = Path(os.fsdecode(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text)
    path.chmod(0o755)
    return path


COUNTED_NAMES = (*SCRUBBED_NAMES, OPTIONAL_LOCKS)  # in this order in each record

_WRAPPER = b"""#!/bin/sh
# Counting git wrapper (tests/clean_support.py): one record per child, written
# by one printf before Git runs; fields NUL-terminated: pid, parent pid,
# process group, working directory, the counted names set, the value of
# GIT_OPTIONAL_LOCKS, the argument count, each argument, then "end".
log=@LOG@
real=@REAL@
if [ -r @PROC@/$$/stat ]; then
  read -r s < @PROC@/$$/stat
  s=${s##*) }; s=${s#* }; s=${s#* }; pgid=${s%% *}
else
  pgid=$(ps -o pgid= -p $$); pgid=${pgid##* }
fi
cwd=$(pwd -P; printf x); cwd=${cwd%x}; cwd=${cwd%?}
names=
@NAMES@
printf '%s\\0' "$$" "$PPID" "$pgid" "$cwd" "${names# }" "${GIT_OPTIONAL_LOCKS-}" "$#" "$@" end >> "$log"
@HOOKS@
exec "$real" "$@"
"""

_HOOKS = b"""case " $* " in
*" worktree remove "*)
  target=; prev=
  for a in "$@"; do [ "x$prev" = "xremove" ] && target=$a; prev=$a; done
  status=
  ( @PRE@
  )
  "$real" "$@"
  status=$?
  ( @POST@
  )
  exit $status;;
esac
"""


def install_counting_git(bin_dir, log, real=REAL_GIT, hooks=None, proc="/proc"):
    """Write bin_dir/git, a POSIX sh counting wrapper after the harness spike's
    SH_WRAPPER (plan review M4, lead ruling R-29), and return its path. Before
    Git runs it appends to log, with one printf, one record for the child, its
    fields NUL-terminated and the record ended by an argument count and a final
    `end` field: the pid, the parent pid, the process group (from
    /proc/$$/stat, else `ps -o pgid= -p $$`), the working directory (`pwd -P`),
    which of the thirty-one scrubbed names and GIT_OPTIONAL_LOCKS are set (each
    tested as ${NAME+x}), GIT_OPTIONAL_LOCKS's value, and the argument vector.
    With no hook it then execs real by absolute path, so the record's pid and
    process group are Git's own. hooks, a dict with "pre" and/or "post", applies
    to `worktree remove` only: the wrapper runs the pre-hook, real as its child
    and the post-hook, then exits with Git's status (128 plus N when Git died
    of signal N, as sh reports it). Each hook is sh text run in a subshell with
    Git's arguments as "$@", the worktree being removed as $target and, for the
    post-hook, Git's status as $status; its output goes to the child's streams,
    and a hook that needs Git calls REAL_GIT, since PATH still holds this
    wrapper. real may be a fake (install_fake_git). proc is the procfs root: a
    test passes a missing directory to take the ps branch."""
    names = b"\n".join(b'[ -n "${%s+x}" ] && names="$names %s"' % (n.encode(), n.encode())
                       for n in COUNTED_NAMES)
    hook_text = b""
    if hooks:
        unknown = sorted(set(hooks) - {"pre", "post"})
        if unknown:
            raise KeyError(f"install_counting_git: unknown hooks {unknown}")
        hook_text = (_HOOKS.replace(b"@PRE@", os.fsencode(hooks.get("pre") or ":"))
                     .replace(b"@POST@", os.fsencode(hooks.get("post") or ":")))
    text = (_WRAPPER.replace(b"@LOG@", _sh_quote(log)).replace(b"@REAL@", _sh_quote(real))
            .replace(b"@PROC@", _sh_quote(proc)).replace(b"@NAMES@", names)
            .replace(b"@HOOKS@", hook_text))
    Path(os.fsdecode(log)).touch()
    return _write_script(Path(os.fsdecode(bin_dir)) / "git", text)


ChildRecord = collections.namedtuple(
    "ChildRecord", "pid ppid pgid cwd names optional_locks argv argv_bytes")
ChildRecord.__doc__ = """One counting-wrapper record: pid, ppid and pgid as ints; cwd as str
(os.fsencode gives back its bytes); names, the counted names that were set,
in COUNTED_NAMES order; optional_locks, GIT_OPTIONAL_LOCKS's value or None
when unset; argv as str (surrogateescape) and argv_bytes as raw bytes."""


def child_log(log):
    """The records of log in the order the children started (the order of their
    appends), complete records only (lead ruling R-31): a trailing record still
    being written is left out. A record cut short in the middle of the log means
    two writers interleaved, and fails loudly."""
    data = Path(os.fsdecode(log)).read_bytes()
    fields = data.split(b"\0")[:-1]  # the last piece is after the final NUL
    records, at = [], 0
    while at < len(fields):
        if at + 7 > len(fields):
            break
        pid, ppid, pgid, cwd, names, locks, count = fields[at:at + 7]
        end = at + 7 + int(count)
        if end >= len(fields):
            break
        if fields[end] != b"end":
            raise AssertionError(f"child_log: malformed record at field {at} of {log}")
        names = tuple(names.decode().split())
        argv = fields[at + 7:end]
        records.append(ChildRecord(
            int(pid), int(ppid), int(pgid), os.fsdecode(cwd), names,
            locks.decode() if OPTIONAL_LOCKS in names else None,
            [os.fsdecode(arg) for arg in argv], argv))
        at = end + 1
    return records


def reset_child_log(log):
    """Empty the log, so that only the command under test is counted."""
    Path(os.fsdecode(log)).write_bytes(b"")


# The fake Gits (T011; plan review M21; harness spike item 3). Each is an sh
# script at bin_dir/git that acts on the commands of its kind and execs real for
# every other; it can stand behind the counting wrapper as its real. A command is
# matched by its words anywhere in the argument vector, since the seven protocol
# pins come first. Events of the Python-backed fakes go to bin_dir/fake-events.jsonl.

FAKE_EVENTS = "fake-events.jsonl"

_FAKE_HEAD = b"""#!/bin/sh
# Fake git (tests/clean_support.py), kind @KIND@.
real=@REAL@
python=@PYTHON@
events=@EVENTS@
in_dir() {
  want=$1; shift; prev=
  for a in "$@"; do
    if [ "x$prev" = "x-C" ] && [ "x$a" = "x$want" ]; then return 0; fi
    prev=$a
  done
  return 1
}
"""

_FAKE_PY_PRELUDE = r'''
import json, os, signal, sys, time


def log(**fields):
    fields.setdefault("pid", os.getpid())
    fields.setdefault("t", time.monotonic())
    data = (json.dumps(fields) + "\n").encode()
    fd = os.open(EVENTS, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        os.write(fd, data)
    finally:
        os.close(fd)


def death_watch():
    """A helper in its own session, so a kill of the fake's group spares it, that
    logs the fake's death: the pipe's last write end closes when the fake dies.
    It confirms its setsid() before the fake goes on (harness spike, item 3)."""
    fake = os.getpid()
    r, w = os.pipe()
    ack_r, ack_w = os.pipe()
    if os.fork() == 0:
        os.setsid()
        os.write(ack_w, b"x")
        null = os.open(os.devnull, os.O_RDWR)
        for fd in (0, 1, 2):
            os.dup2(null, fd)
        os.close(w)
        os.read(r, 1)
        log(event="death", pid=fake)
        os._exit(0)
    os.read(ack_r, 1)
    for fd in (ack_r, ack_w, r):
        os.close(fd)
    return w
'''

_IGNORE_SIGTERM = _FAKE_PY_PRELUDE + r'''
EVENTS, LIFETIME = sys.argv[1], float(sys.argv[2])
watch = death_watch()
signal.signal(signal.SIGTERM, lambda signum, frame: log(event="term"))
start = time.monotonic()
log(event="ready", pgid=os.getpgrp(), sid=os.getsid(0), ppid=os.getppid(),
    sigterm_was_ignored=True)
while time.monotonic() - start < LIFETIME:
    time.sleep(max(0.0, LIFETIME - (time.monotonic() - start)))
log(event="lifetime-ended")
'''

_TTY_CREDENTIAL = _FAKE_PY_PRELUDE + r'''
import subprocess
REAL, EVENTS, ARGV = sys.argv[1], sys.argv[2], sys.argv[3:]
try:
    fd = os.open("/dev/tty", os.O_RDWR)
    foreground = os.tcgetpgrp(fd)
    os.close(fd)
    tty, error = "opened", None
except OSError as exc:
    tty, error, foreground = "failed", exc.errno, None
env = {key: value for key, value in os.environ.items()
       if key not in ("GIT_ASKPASS", "SSH_ASKPASS", "GIT_TERMINAL_PROMPT")}
fill = subprocess.run([REAL, "-c", "credential.helper=", "-c", "core.askPass=", "credential", "fill"],
                      input=b"protocol=https\nhost=example.invalid\n\n", capture_output=True, env=env)
answers = dict(line.split("=", 1) for line in fill.stdout.decode("utf-8", "replace").splitlines() if "=" in line)
log(event="tty", tty=tty, errno=error, foreground=foreground, pgid=os.getpgrp(),
    fill_status=fill.returncode, username=answers.get("username"), password=answers.get("password"),
    fill_stderr=fill.stderr.decode("utf-8", "replace").strip())
os.execv(REAL, [REAL, *ARGV])
'''

FAKE_KINDS = (
    "flood-stderr", "ignore-sigterm", "ignored-5000", "version-2.35.0", "remove-noop",
    "remove-slow", "remove-exit", "status-fails-in", "status-hangs-in",
    "ls-files-fails-in", "ls-files-hangs-in", "signal-parent-in", "slow-after-remove",
    "tty-credential", "status-slow-again-in", "ls-files-stuck-again-in",
)


def install_fake_git(bin_dir, kind, real=REAL_GIT, **options):
    """Write the fake Git of kind at bin_dir/git and return its path. Every
    command the kind does not act on is passed to real by exec. The kinds and
    their options (defaults in brackets):

    flood-stderr [kib=70]: on `status`, kib KiB of "E" on standard error, then
      the real status.
    ignore-sigterm [lifetime=30]: on `status`, ignores TERM from its first
      instruction, logs `ready` (its pgid, sid and ppid), `term` at each SIGTERM
      and `death` from a helper in its own session, and sleeps until lifetime
      seconds have passed, past any budget. Python behind an sh prelude.
    ignored-5000 [count=5000]: on `status`, count NUL-terminated `!! NAME`
      records, exit 0.
    version-2.35.0: prints `git version 2.35.0` when --version stands anywhere
      in the argument vector, behind the seven pins included.
    remove-noop: on `worktree remove`, exits 0 without removing.
    remove-slow [seconds=3]: on `worktree remove`, sleeps, then removes for real.
    remove-exit [status=1]: on `worktree remove`, exits status.
    status-fails-in, ls-files-fails-in (path) [status=128]: on `status` or
      `ls-files` with -C path, prints a fatal line on standard error and exits
      status.
    status-hangs-in, ls-files-hangs-in (path) [lifetime=30]: the same command
      sleeps lifetime seconds instead (TERM ends it).
    signal-parent-in (path) [signal="TERM"]: on `status` with -C path, sends the
      signal to its parent, project, then runs the real status.
    slow-after-remove [lifetime=30]: once a `worktree remove` has run, every
      `worktree list` and `for-each-ref` sleeps lifetime seconds.
    tty-credential: on `push`, opens /dev/tty, runs the real `git credential
      fill` for https://example.invalid so that Git prompts there (no helper,
      no askpass), logs `tty` (whether /dev/tty opened, its errno, the
      terminal's foreground group, its own group, the answers read), then runs
      the real push. Python behind an sh prelude.
    status-slow-again-in (path) [seconds=2]: on `status` with -C path, the
      first runs as it is and leaves bin_dir/status-slow-again.marker; each
      later one sleeps seconds, then runs the real status. So planning's
      status probe of path is not slowed and a revalidation's is (lead ruling
      R-93 (e), LOW-1). Installing the kind removes a marker left before.
    ls-files-stuck-again-in (path) [lifetime=30]: on `ls-files` with -C path,
      the first runs as it is and leaves bin_dir/ls-files-stuck-again.marker;
      each later one ignores TERM and sleeps lifetime seconds instead, so
      that only SIGKILL ends it sooner. So planning's hidden-state probe of
      path runs and a revalidation's is cut at its budget or the deadline
      (lead ruling R-93 (e), LOW-2). Installing the kind removes a marker
      left before.

    No fake relies on signal.sigtimedwait, which macOS lacks."""
    if kind not in FAKE_KINDS:
        raise KeyError(f"install_fake_git: unknown kind {kind!r}")
    bin_dir = Path(os.fsdecode(bin_dir))
    events = bin_dir / FAKE_EVENTS
    allowed = {"flood-stderr": {"kib"}, "ignore-sigterm": {"lifetime"}, "ignored-5000": {"count"},
               "remove-slow": {"seconds"}, "remove-exit": {"status"},
               "status-fails-in": {"path", "status"}, "ls-files-fails-in": {"path", "status"},
               "status-hangs-in": {"path", "lifetime"}, "ls-files-hangs-in": {"path", "lifetime"},
               "signal-parent-in": {"path", "signal"}, "slow-after-remove": {"lifetime"},
               "status-slow-again-in": {"path", "seconds"}, "ls-files-stuck-again-in": {"path", "lifetime"}}
    unknown = sorted(set(options) - allowed.get(kind, set()))
    if unknown:
        raise KeyError(f"install_fake_git: {kind} takes no option {unknown}")
    if kind.endswith("-in") and "path" not in options:
        raise KeyError(f"install_fake_git: {kind} needs path")
    path = _sh_quote(options["path"]) if "path" in options else b""
    lifetime = str(float(options.get("lifetime", 30))).encode()
    if kind == "flood-stderr":
        body = (b'case " $* " in *" status "*)\n'
                b"  dd if=/dev/zero bs=1024 count=%d 2>/dev/null | tr '\\000' E >&2;;\nesac\n"
                % int(options.get("kib", 70)))
    elif kind == "ignore-sigterm":
        body = (b'case " $* " in *" status "*)\n'
                b"  trap '' TERM\n"
                b'  exec "$python" -I -S -c %s "$events" %s;;\nesac\n'
                % (_sh_quote(_IGNORE_SIGTERM), lifetime))
    elif kind == "ignored-5000":
        body = (b'case " $* " in *" status "*)\n'
                b"  i=0\n"
                b"  while [ $i -lt %d ]; do printf '!! ignored-%%05d\\0' \"$i\"; i=$((i + 1)); done\n"
                b"  exit 0;;\nesac\n" % int(options.get("count", 5000)))
    elif kind == "version-2.35.0":
        body = b'case " $* " in *" --version "*) echo "git version 2.35.0"; exit 0;; esac\n'
    elif kind == "remove-noop":
        body = b'case " $* " in *" worktree remove "*) exit 0;; esac\n'
    elif kind == "remove-slow":
        body = (b'case " $* " in *" worktree remove "*) sleep %s; exec "$real" "$@";; esac\n'
                % str(float(options.get("seconds", 3))).encode())
    elif kind == "remove-exit":
        body = (b'case " $* " in *" worktree remove "*) exit %d;; esac\n'
                % int(options.get("status", 1)))
    elif kind in ("status-fails-in", "ls-files-fails-in"):
        word = kind.split("-fails-in")[0].encode()
        body = (b'if in_dir %s "$@"; then case " $* " in *" %s "*)\n'
                b'  echo "fatal: %s failed (fake %s)" >&2; exit %d;;\nesac; fi\n'
                % (path, word, word, kind.encode(), int(options.get("status", 128))))
    elif kind in ("status-hangs-in", "ls-files-hangs-in"):
        word = kind.split("-hangs-in")[0].encode()
        body = (b'if in_dir %s "$@"; then case " $* " in *" %s "*) exec sleep %s;; esac; fi\n'
                % (path, word, lifetime))
    elif kind == "signal-parent-in":
        name = str(options.get("signal", "TERM")).upper().replace("SIG", "", 1).encode()
        body = (b'if in_dir %s "$@"; then case " $* " in *" status "*) kill -s %s "$PPID";; esac; fi\n'
                % (path, name))
    elif kind == "slow-after-remove":
        body = (b"marker=%s\n"
                b'case " $* " in\n'
                b'*" worktree remove "*) "$real" "$@"; status=$?; : > "$marker"; exit $status;;\n'
                b'*" worktree list "*|*" for-each-ref "*) [ -e "$marker" ] && exec sleep %s;;\nesac\n'
                % (_sh_quote(bin_dir / "slow-after-remove.marker"), lifetime))
    elif kind == "status-slow-again-in":
        marker = bin_dir / "status-slow-again.marker"
        marker.unlink(missing_ok=True)
        body = (b"marker=%s\n"
                b'if in_dir %s "$@"; then case " $* " in *" status "*)\n'
                b'  if [ -e "$marker" ]; then sleep %s; else : > "$marker"; fi;;\nesac; fi\n'
                % (_sh_quote(marker), path, str(float(options.get("seconds", 2))).encode()))
    elif kind == "ls-files-stuck-again-in":
        marker = bin_dir / "ls-files-stuck-again.marker"
        marker.unlink(missing_ok=True)
        body = (b"marker=%s\n"
                b'if in_dir %s "$@"; then case " $* " in *" ls-files "*)\n'
                b'  if [ -e "$marker" ]; then trap \'\' TERM; exec sleep %s; fi\n'
                b'  : > "$marker";;\nesac; fi\n'
                % (_sh_quote(marker), path, lifetime))
    else:  # tty-credential
        body = (b'case " $* " in *" push "*)\n'
                b'  exec "$python" -I -S -c %s "$real" "$events" "$@";;\nesac\n'
                % _sh_quote(_TTY_CREDENTIAL))
    head = (_FAKE_HEAD.replace(b"@KIND@", kind.encode()).replace(b"@REAL@", _sh_quote(real))
            .replace(b"@PYTHON@", _sh_quote(sys.executable)).replace(b"@EVENTS@", _sh_quote(events)))
    return _write_script(bin_dir / "git", head + body + b'exec "$real" "$@"\n')


def fake_events(bin_dir):
    """The events the Python-backed fakes logged in bin_dir, complete lines only."""
    path = Path(os.fsdecode(bin_dir)) / FAKE_EVENTS
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_bytes().split(b"\n")[:-1] if line]


def wait_for_event(bin_dir, event, pid=None, timeout=TIMEOUT):
    """The first event named event (of pid, when given), polled until it is
    logged, or None after timeout seconds: the death helper logs on its own
    time, possibly after project has exited."""
    deadline = time.monotonic() + timeout
    while True:
        for entry in fake_events(bin_dir):
            if entry["event"] == event and (pid is None or entry["pid"] == pid):
                return entry
        if time.monotonic() > deadline:
            return None
        time.sleep(0.01)


# The D18 and D14 literals (T011; plan review M8), character for character from
# openspec/changes/add-project-clean-all-safe/design.md D14 (:624-628) and D18
# (:732-780), the lines specs/004-project-clean-all-safe/contracts/project-clean.md
# fixes beyond D18 (:156-180), and three baseline texts kept (project at
# 961c405, :551, :716, :718). This is the tests' own transcription, keyed as
# TEXT and NEXT_STEPS of project are; test_clean_text_fixtures_equal_the_contract_table
# checks the two against each other (rule 8). Each placeholder is a str.format
# field named as the docs spell it ({ROOT}, {PATH}, {BRANCH}, {N}, {K}, {M},
# {REASON}, ...), except three that stand for a phrase or a list: {NEXT_STEP}
# for NEXT STEP, {BRANCHES} for B1, B2 and {NOT_ATTEMPTED} for P1, P2. Every
# other character is literal; [yes/N] is literal text. `question_one` is D18's
# question "in the singular for one", used only for one, so it holds the
# literal 1 and no placeholder (lead ruling R-43).
TEXT_FIXTURES = {
    # D14: the report.
    "completeness_line_complete": "Report: complete",
    "completeness_line_incomplete": "Report: incomplete ({CODES})",
    "selection_line": "--all-safe would select {N}",
    "selection_line_above_cap": "--all-safe would be incomplete (inspect-cap)",
    # D18: the preview.
    "merge_target_line": "Merge target: {NAME} ({SOURCE})",
    "selected_heading": "Selected ({N}):",
    "selected_row": "  remove {PATH} [{BRANCH}]",
    "excluded_heading": "Excluded ({M}):",
    "excluded_group": "  {REASON} ({K}): {NEXT_STEP}",
    "excluded_row": "    {PATH} [{BRANCH}]",
    "ignored_suffix": ": {N} ignored; first: {SAMPLE}",
    "ignored_suffix_truncated": ": at least {N} ignored; first: {SAMPLE}",
    "deferral_line": "  deferred-target-cap ({K}): this run removes up to 16; run again: project clean {ROOT} --all-safe --apply",
    "non_drain_line": "  these deferred rows will not drain while the 16 rows ahead of them are {REASONS}; review those worktrees, then remove them yourself",
    "residual_window_line": "Not protected: ignored files created, index flags set, operations started or worktree-only commits made after the last check, and any change after Git's own check.",
    "empty_line": "No eligible worktrees",
    # D18: the question, the wait, the result.
    "question": "Remove {N} worktrees, keeping {N} branches? [yes/N]",
    "question_one": "Remove 1 worktree, keeping 1 branch? [yes/N]",
    "wait_line": "Waiting for git worktree remove {PATH} to finish; a started removal is never interrupted (at most 300 s).",
    "success_line": "Removed {N}; branches kept: {BRANCHES}.",
    "stop_block": "Stopped at {PATH} ({REASON}). Removed {K} of {N}. Not attempted: {NOT_ATTEMPTED}. Next: project clean {ROOT} --all-safe",
    "partial_removal_note": "Probable partial removal: inspect, then git worktree remove --force {PATH} by hand.",
    # D18: refusal messages and remedies.
    "target_excluded_gate": "Worktree is excluded: {REASON}; {NEXT_STEP}",
    "remedy_inspection_incomplete": "repair or remove the inspection-error rows first: git worktree repair, git worktree prune, or remove the row by hand after review",
    "remedy_inspect_cap": "{N} rows exceed the row cap of {M}; remove worktrees explicitly, or prune stale entries by hand",
    "remedy_deadline_exceeded": "the run ran out of time; remove worktrees explicitly or re-run",
    # The contract, beyond D18.
    "progress_line": "  {STAGE} {PATH}",
    "progress_line_reason": "  {STAGE} {PATH} ({REASON})",
    "branches_kept_line": "Branches kept: {BRANCHES}.",
    "branches_not_confirmed": "Branches not confirmed: {BRANCHES}.",
    "invalid_arguments_all_safe": "--all-safe cannot be combined with --action, --branch or --worktree.",
    "invalid_arguments_expect_plan": "--expect-plan requires --all-safe and --apply.",
    "invalid_arguments_expect_plan_value": "--expect-plan takes 64 lowercase hexadecimal characters.",
    "internal_error": "{TYPE}: {TEXT}",
    "git_unavailable": "Git is unavailable ({DETAIL}); clean needs Git 2.36 or later.",
    "git_unavailable_not_found": "not found",
    "git_unavailable_exit": "exit {N}",
    "git_unavailable_timed_out": "timed out",
    "git_unavailable_unparseable_version": "unparseable version",
    "git_too_old": "Git {VERSION} is older than 2.36; clean needs Git 2.36 or later.",
    "inspection_git_too_old": "Git {VERSION} is older than 2.36; repository inspection needs Git 2.36 or later.",
    "inspection_git_unavailable": "Git is unavailable ({DETAIL}); repository inspection needs Git 2.36 or later.",
    # D18's relative-config-path line, one per failing variable (Brett Heap's ruling LQ-15).
    "relative_config_path": "{NAME} is set to a path that does not begin with /; make it absolute or unset it.",
    "target_not_repository_root": "Not the main worktree of a repository: {PATH}; pass the repository root.",
    "unsupported_path_bytes": "The repository path is not valid UTF-8: {PATH}",
    "manifest_invalid_size": "Manifest {PATH} is larger than 1 MiB.",
    "plan_incomplete": "The plan is incomplete ({CODE}): {REMEDY}.",
    "plan_digest_mismatch": "The fresh plan's digest {DIGEST} differs from --expect-plan {EXPECTED}; nothing was changed.",
    # The plan notes (contracts/project-clean.md, "Codes"; lead ruling R-45 (4); T051).
    "note_merge_target_conflict": "The manifest names {NAME} and origin/HEAD names {OTHER}; {NAME} is the merge target.",
    "note_inspection_incomplete": "{K} other rows are inspection-error or were left unprobed; they do not block {PATH}.",
    "note_inspect_cap": "{K} rows past the row cap of {M} were not inspected; they do not block {PATH}.",
    "note_deadline_exceeded": "{K} rows were stopped at the work deadline; they do not block {PATH}.",
    "note_inspect_cap_report": "{N} rows exceed the --all-safe row cap of {M}; --all-safe would be incomplete (inspect-cap).",
    "confirmation_required": "Standard input is not a terminal; pass --yes to apply this plan.",
    "push_remote_gone": "Cannot push {BRANCH}; its upstream {UPSTREAM} was deleted (remote-gone); review it before it is republished.",
    # Baseline texts kept (project at 961c405).
    "target_excluded_current": "Cannot remove the current worktree.",
    "target_excluded_class": "Worktree is {CLASS}; only clean merged worktrees may be removed.",
    "no_merge_target": "Cannot determine the default branch from the manifest, origin/HEAD, main, or master.",
    # The row errors (contracts/project-clean.md, "Codes"; lead ruling R-45 (4)).
    "row_error_os_error": "{OPERATION} failed: {STRERROR}",
    "row_error_probe_failed": "{OPERATION} failed: {DETAIL}",
    "row_error_probe_failed_exit": "exit {N}",
    "row_error_probe_failed_signal": "signal {N}",
    "row_error_probe_failed_cannot_spawn": "cannot spawn ({STRERROR})",
    "row_error_probe_failed_unparseable": "unparseable output",
    "row_error_probe_timeout": "{OPERATION} timed out after {S} s",
    "row_error_deadline_exceeded": "{OPERATION} stopped at the work deadline",
    "row_error_git_operation": "git {SUBCOMMAND}",
}

# D18's next step by reason (design.md:756-765); every other class keeps its
# baseline recommendation.
NEXT_STEP_FIXTURES = {
    "dirty": "commit or preserve the changes",
    "ignored-local-files": "move or delete the ignored files by hand",
    "unstarted-branch": "no commit was made on this branch here since it was created; review, then git worktree remove yourself",
    "reflog-unavailable": "the branch's reflog is missing, expired or undecidable; review, then git worktree remove yourself",
    "contains-submodule": "review, then remove the worktree yourself",
    "hidden-local-state": "review, then remove the worktree yourself",
    "operation-in-progress": "a git am, merge, notes merge, cherry-pick, revert, rebase or bisect is, or may be, in progress there; finish or abort it (a squash merge that holds an autostash ends only with git commit, --allow-empty where nothing is staged), then run again",
    "worktree-only-commits": "a commit is, or may be, held only by this worktree's HEAD reflog or refs/worktree; keep it on a branch or tag, or review, then git worktree remove yourself",
    "registration-mismatch": "review, then git worktree repair or git worktree prune, or remove the row by hand",
    "inspection-error": "review, then git worktree repair or git worktree prune, or remove the row by hand",
    "locked-worktree": "unlock it yourself if it should go",
    # The contract's next steps for the three reasons D18 gives none
    # (contracts/project-clean.md :160-168; lead rulings R-57 H1 and R-62 (b)).
    "main-worktree": "never removed by project clean",
    "unsupported-path-bytes": "rename the path to valid UTF-8",
    "not-requested": "name it with --worktree to plan its removal",
}


class CleanCase(unittest.TestCase):
    """The base of the clean test classes. It has no test methods, so a module
    that binds it runs nothing extra. setUp builds what ProjectTests.setUp
    builds (tests/test_project.py:117-136): a resolved temporary base, a fake
    workBenches with the test generator, and self.env with WORKBENCHES_ROOT,
    HOME, PROJECTS_DIR, GIT_CONFIG_NOSYSTEM=1 and GIT_CONFIG_GLOBAL=os.devnull;
    plus a fixed author and committer, and none of the thirty-one scrubbed names
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
               "GIT_CONFIG_GLOBAL": os.devnull, "NO_COLOR": "1", **AUTHOR}
        for name in (*SCRUBBED_NAMES, OPTIONAL_LOCKS, "FORCE_COLOR", "PYTHON_COLORS"):
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

    def path_first(self, bin_dir, env=None):
        """A copy of env (self.env by default) with bin_dir first on PATH, for a
        counting wrapper or a fake Git."""
        env = dict(self.env if env is None else env)
        env["PATH"] = os.pathsep.join([os.fsdecode(bin_dir), env.get("PATH", "")])
        return env

    def path_without_git(self, env=None):
        """A PATH under which no `git` is found: one new directory holding a
        symbolic link to the first executable of every other name on env's PATH
        (self.env's by default), so every other tool stays where `project` looks
        for it."""
        env = self.env if env is None else env
        farm = self.base / "path-without-git"
        farm.mkdir(exist_ok=True)
        for directory in env.get("PATH", "").split(os.pathsep):
            if not directory or not os.path.isdir(directory):
                continue
            try:
                entries = list(os.scandir(directory))
            except OSError:
                continue  # an unreadable PATH directory offers nothing
            for entry in entries:
                link = farm / entry.name
                if entry.name == "git" or os.path.lexists(link):
                    continue
                try:
                    runnable = entry.is_file() and os.access(entry.path, os.X_OK)
                except OSError:
                    continue  # an entry this user cannot stat cannot be run either
                if runnable:
                    link.symlink_to(os.path.join(os.path.abspath(directory), entry.name))
        path = str(farm)
        self.assertIsNone(shutil.which("git", path=path), "path_without_git() still finds git")
        return path

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
        a file committed as the branch's own commit, `push -u origin BRANCH`, then
        `merge --no-ff BRANCH` into root's checked-out branch, the merge target.
        The file is `work-BRANCH` ("/" read as "-"), not the recipe's `work`, so
        that every branch has a commit of its own and two never conflict. setup(tree), when given, runs before that commit, so what it
        stages (a gitlink, a submodule) is committed and merged too. Needs an
        origin (bare_remote()). Returns the worktree's path."""
        root = self._root(root)
        tree = self._tree(branch, path)
        self.git(root, "worktree", "add", "-b", branch, tree)
        (tree / ("work-" + branch.replace("/", "-"))).write_text("done")
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
                      timeout=None, stdout_pipe=False):
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

        stdout_pipe=True puts stdout on a pipe of its own while stdin stays on the
        pseudo-terminal (lead ruling R-56 Q-14), as `project ... | jq` at a terminal
        runs; steps then match on all three streams, the run's stdout is that
        pipe's text, and its pty attribute the pty transcript (the echoed input).

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
                                     stdout=subprocess.PIPE if stdout_pipe else slave,
                                     stderr=subprocess.PIPE, start_new_session=True,
                                     preexec_fn=_take_controlling_terminal if controlling_tty else None)
        except BaseException:
            os.close(master)
            raise
        finally:
            os.close(slave)
        error = child.stderr.fileno()
        output = child.stdout.fileno() if stdout_pipe else None
        streams = [master, error] + ([output] if stdout_pipe else [])
        received = {fd: bytearray() for fd in streams}
        cursor = {fd: 0 for fd in streams}
        reading = list(streams)
        pending = list(steps)
        seen = []
        interrupted = exited = None

        def text(fd):
            return bytes(received[fd]).replace(b"\r\n", b"\n").decode("utf-8", "replace")

        def transcript():
            command = " ".join(shlex.quote(os.fsdecode(arg)) for arg in argv)
            piped = f"\n--- stdout ---\n{text(output)}" if stdout_pipe else ""
            return f"$ {command}\n--- pty ---\n{text(master)}{piped}\n--- stderr ---\n{text(error)}"

        def locate(expected):
            for fd in streams:
                found = text(fd).find(expected, cursor[fd])
                if found >= 0:
                    cursor[fd] = found + len(expected)
                    return True
            return False

        try:
            while True:
                if pending and locate(pending[0][0]):
                    action = pending.pop(0)[1]
                    seen.append("".join(text(fd) for fd in streams))
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
            if stdout_pipe:
                child.stdout.close()
            if child.poll() is None:
                with contextlib.suppress(OSError):
                    os.killpg(child.pid, signal.SIGKILL)
                child.wait()
        if pending:
            self.fail(f"the child exited before the step waiting for {pending[0][0]!r}\n{transcript()}")
        result = subprocess.CompletedProcess(argv, child.returncode, text(output if stdout_pipe else master),
                                             text(error))
        result.seen = seen
        if stdout_pipe:
            result.pty = text(master)
        return result
