"""Offline behavioral checks with disposable Git repositories and generators."""
import contextlib
import errno
import importlib.machinery
import importlib.util
import io
import json
import os
from pathlib import Path
import select
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "project"
loader = importlib.machinery.SourceFileLoader("project_cli", str(CLI))
spec = importlib.util.spec_from_loader(loader.name, loader)
module = importlib.util.module_from_spec(spec)
loader.exec_module(module)

# Fixed text of design.md D13, character for character. NAME, ORG, VIS and
# PARENT are the format fields {NAME}, {ORG}, {VIS} and {PARENT}; every other
# character is literal. Begin D13 fixtures.
QUESTION_HEADER = "How should {NAME} be created? Nothing is created until you confirm."
QUESTION_TRIAD = "  1. Triad (default): an assembly root with a spec leg and a code leg, made by openRepoShape. It is preferred, not required: it stays elective and confers nothing."
OBSTACLE_NAME = "     Not possible here: {NAME} cannot be a Triad name; a Triad name is a letter first, then letters and digits only, such as MyApp."
OBSTACLE_OPENREPOSHAPE = "     Not possible here: openRepoShape is not on PATH. Install openRepoShape through workBenches first."
OBSTACLE_PARENT = "     Not possible here: The parent directory {PARENT} does not exist; a Triad is created inside an existing directory."
QUESTION_SINGLE = "  2. Single repository: fully supported, and no reason is asked. single-repository.yaml is the ratified way to record staying single."
QUESTION_PROMPT = "Create it as a Triad? [Y/n or 1/2]:"
ORG_PROMPT = "GitHub organization for the Triad:"
VIS_PROMPT = "Visibility (private, public or internal):"
QUESTION_RETRY = "Answer y or 1 for the Triad, n or 2 for a single repository; Enter takes the Triad."
ORG_RETRY = "An organization name starts with a letter or digit and has only letters, digits and hyphens."
VIS_RETRY = "Type the visibility in full: private, public or internal."
QUESTION_MISSED = "No recognised answer to the Triad question; nothing was created."
QUESTION_ENDED = "No answer to the Triad question (end of input); nothing was created."
OBSTACLES_REFUSAL_START = "A Triad cannot be created here. "
OBSTACLE_LINE_START = "Not possible here: "
OBSTACLES_REFUSAL_END = " Nothing was created."
ORG_MISSED = "Invalid GitHub organization name. Nothing was created."
ORG_ENDED = "No GitHub organization was given (end of input); nothing was created."
VIS_MISSED = "Visibility must be private, public or internal. Nothing was created."
VIS_ENDED = "No visibility was given (end of input); nothing was created."
RESTATED = "Triad {NAME} in organization {ORG}, visibility {VIS}."
RESTATED_PUBLIC = "Triad {NAME} in organization {ORG}, visibility public: anyone can read the repositories."
ADVISORY_PREFERENCE = "warning: {NAME} was created as a single repository. The Triad (an assembly root with a spec leg and a code leg) is preferred, not required: it stays elective and confers nothing."
ADVISORY_CONVERSION = "warning: openRepoShape's adopt-project.py converts a repository in place when a person deciding for this project runs it, and a project that stays single can say so in single-repository.yaml. Nothing here changes."
# End D13 fixtures.

# Fixed text of openspec/changes/fix-parent-obstacle-wording/design.md, D2 (that
# design's numbering, not the D13 block's above), character for character.
# PARENT is the format field {PARENT}; every other character is literal. A
# parent that does not exist keeps OBSTACLE_PARENT above, unchanged.
OBSTACLE_PARENT_NOT_A_DIRECTORY = "     Not possible here: The parent {PARENT} exists but is not a directory; choose a parent that is a directory."


def obstacles_refusal(*obstacle_lines):
    """The D13 known-obstacles refusal composed from formatted obstacle lines, in their order."""
    sentences = [line.split(OBSTACLE_LINE_START, 1)[1] for line in obstacle_lines]
    return OBSTACLES_REFUSAL_START + " ".join(sentences) + OBSTACLES_REFUSAL_END


# Existing text this change keeps, pinned as literals (no test reads history).
REFUSED = "REFUSED: "
CANCELLED = "Cancelled."
NAME_PROMPT = "Project name:"
GENERATOR_PROMPT = "Select a generator number (or specify --bench and --type):"
CONFIRM_PROMPT = "Type yes to run this plan:"
DECLINED = "Cancelled; no command was run."
INVALID_NAME = "Project name must start with a letter or digit and contain letters, digits, _ or -."
PARENT_AND_INTO = "Use either positional parent or --into."
DESTINATION_EXISTS = "Destination already exists: {PATH}"
SHAPE_NEEDS_ORG_AND_VISIBILITY = "Shape creation requires --org and --visibility."
ORG_NEEDS_SHAPE = "--org, --visibility, --family and --elected-by require --shape."
NOT_A_TERMINAL = "{PROMPT} Supply explicit options when stdin is not a terminal."
NOT_CREATED = "Generator returned success but did not create {PATH}"
WORKFLOW_MISSING = "--workflow requires setup-openspeckit on PATH."
NO_GENERATOR = "No matching generator; run project benches."
WORKFLOW_FAILED = "Project created at {PATH}; workflow setup failed."

# The fakes of D14. Each is a script for this interpreter, so it needs nothing
# else on PATH; {python} and {status} are filled in when it is written.
FAKE_SHAPE_PROMPT = "Type yes to continue:"
FAKE_SHAPE_DECLINED = "not confirmed; nothing was created."
FAKE_OPENREPOSHAPE = """#!{python}
import json, os, sys
args = sys.argv[1:]
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "openRepoShape.argv"), "a") as record:
    record.write(json.dumps(args) + "\\n")
sys.stdout.write("Type yes to continue: ")
sys.stdout.flush()
if sys.stdin.readline().strip() == "yes":
    os.makedirs(os.path.join(args[args.index("--into") + 1], args[0]))
    sys.exit({status})
print("not confirmed; nothing was created.")
sys.exit(1)
"""
FAKE_SETUP_OPENSPECKIT = """#!{python}
import sys
marker = " ".join(["FOLLOWUP"] + sys.argv[1:])
print(marker, flush=True)
print(marker, file=sys.stderr, flush=True)
sys.exit({status})
"""
PTY_EOF = "\x04"


class ProjectTests(unittest.TestCase):
    def setUp(self):
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
        self.env = {**os.environ, "WORKBENCHES_ROOT": str(self.wb),
                    "HOME": str(self.base / "home"), "SPECKIT_WORKSPACE_PATH": "",
                    "PROJECTS_DIR": str(self.base), "GIT_CONFIG_NOSYSTEM": "1",
                    "GIT_CONFIG_GLOBAL": os.devnull}

    def save_config(self):
        (self.wb / "config/bench-config.json").write_text(json.dumps(self.config))

    def run_cli(self, *args, cwd=None):
        return subprocess.run([sys.executable, str(CLI), *map(str, args)],
                              cwd=cwd or self.base, env=self.env, input="", text=True,
                              capture_output=True, timeout=20)

    pty_timeout = 20  # seconds; a pty run that exceeds it fails with its transcript

    def fake_bin(self):
        """The temporary bin directory that holds the fakes (D14)."""
        path = self.base / "bin"
        path.mkdir(exist_ok=True)
        return path

    def question_env(self, ci):
        """The environment of a question or advisory test (D14): self.env with CI set to the
        given string or removed (None), without GH_TOKEN, GITHUB_TOKEN or any OPENREPOSHAPE_*
        variable, and with PATH the fake bin directory plus the directories of bash, git and
        this interpreter, so no openRepoShape or setup-openspeckit installed here is found."""
        env = {key: value for key, value in self.env.items()
               if key not in ("CI", "GH_TOKEN", "GITHUB_TOKEN") and not key.startswith("OPENREPOSHAPE_")}
        if ci is not None:
            env["CI"] = ci
        directories = [str(self.fake_bin())]
        for tool in (shutil.which("bash"), shutil.which("git"), sys.executable):
            self.assertTrue(tool, "bash, git and this interpreter must be found to build PATH")
            directory = str(Path(tool).parent)
            if directory not in directories:
                directories.append(directory)
        env["PATH"] = os.pathsep.join(directories)
        return env

    def write_fake(self, tool, template, status):
        path = self.fake_bin() / tool
        path.write_text(template.format(python=sys.executable, status=status))
        path.chmod(0o755)
        return path

    def write_fake_openreposhape(self, status=0):
        """The fake openRepoShape: records its argv beside itself, prints FAKE_SHAPE_PROMPT,
        reads one line, and on yes creates <--into>/<name> and exits with status; otherwise
        prints FAKE_SHAPE_DECLINED and exits 1."""
        return self.write_fake("openRepoShape", FAKE_OPENREPOSHAPE, status)

    def write_fake_setup_openspeckit(self, status=0):
        """The fake setup-openspeckit: a FOLLOWUP marker line carrying its arguments on stdout
        and on stderr, then exits with status."""
        return self.write_fake("setup-openspeckit", FAKE_SETUP_OPENSPECKIT, status)

    def shape_record(self):
        """The argv lists the fake openRepoShape recorded, or None when it never ran."""
        record = self.fake_bin() / "openRepoShape.argv"
        if not record.exists():
            return None
        return [json.loads(line) for line in record.read_text().splitlines()]

    def assert_fake_on_path(self, env, tool):
        self.assertEqual(shutil.which(tool, path=env["PATH"]), str(self.fake_bin() / tool),
                         f"PATH must resolve {tool} to the fake")

    def assert_absent_from_path(self, env, tool):
        self.assertIsNone(shutil.which(tool, path=env["PATH"]), f"PATH must resolve no {tool}")

    def shape_env(self, ci, status=0):
        """question_env(ci) with the fake openRepoShape written and asserted on PATH."""
        env = self.question_env(ci)
        self.write_fake_openreposhape(status)
        self.assert_fake_on_path(env, "openRepoShape")
        return env

    def run_pty(self, *args, env, steps=(), timeout=None):
        """Run project with stdin and stdout on one pseudo-terminal and stderr on a pipe (D14).

        steps is a sequence of (expected, action). Each action is taken only once its expected
        text has appeared on either stream, past the previous match on that stream: a line of
        text is written with a newline, PTY_EOF is written alone, and signal.SIGINT is sent
        with send_signal and repeated until the child exits. The child starts in a new session,
        so the pty is never a controlling terminal. Returns a CompletedProcess whose stdout is
        the pty transcript (echoed input included) and stderr the pipe, both with \\r\\n read as
        \\n; its seen attribute holds, for each step, both transcripts as they stood when the
        action was taken.
        """
        argv = [sys.executable, str(CLI), *map(str, args)]
        limit = timeout or self.pty_timeout
        deadline = time.monotonic() + limit
        master, slave = os.openpty()
        try:
            child = subprocess.Popen(argv, cwd=self.base, env=env, stdin=slave, stdout=slave,
                                     stderr=subprocess.PIPE, start_new_session=True)
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
            return f"$ project {shlex.join(argv[2:])}\n--- pty ---\n{text(master)}\n--- stderr ---\n{text(error)}"

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
                    if action is signal.SIGINT:
                        child.send_signal(signal.SIGINT)
                        interrupted = time.monotonic()
                    else:
                        with contextlib.suppress(OSError):
                            os.write(master, (action if action == PTY_EOF else action + "\n").encode())
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
            self.fail(f"project exited before the step waiting for {pending[0][0]!r}\n{transcript()}")
        result = subprocess.CompletedProcess(argv, child.returncode, text(master), text(error))
        result.seen = seen
        return result

    @contextlib.contextmanager
    def inproc_terminal(self, ci, stdin_tty=True, stdout_tty=True):
        """In-process streams and environment for module.main() (D14): the whole environment
        replaced by question_env(ci), stdout and stderr redirected to StringIO, then the isatty
        of sys.stdin and of sys.stdout patched independently. Yields (stdout, stderr)."""
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.dict(os.environ, self.question_env(ci), clear=True))
            stack.enter_context(contextlib.redirect_stdout(stdout))
            stack.enter_context(contextlib.redirect_stderr(stderr))
            stack.enter_context(patch.object(sys, "stdin", io.StringIO()))
            stack.enter_context(patch.object(sys.stdin, "isatty", return_value=stdin_tty))
            stack.enter_context(patch.object(sys.stdout, "isatty", return_value=stdout_tty))
            yield stdout, stderr

    def run_inproc(self, *args, ci, answers=(), stdin_tty=True, stdout_tty=True):
        """module.main(args) in process with builtins.input patched to the scripted answers;
        an answer that is an exception (EOFError, KeyboardInterrupt) is raised instead.
        Returns a CompletedProcess with the captured streams and a prompts attribute."""
        script = list(answers)
        prompts = []

        def scripted_input(prompt=""):
            prompts.append(prompt)
            if not script:
                raise AssertionError(f"Unscripted prompt: {prompt!r}")
            answer = script.pop(0)
            if isinstance(answer, BaseException) or (isinstance(answer, type) and issubclass(answer, BaseException)):
                raise answer
            return answer

        with self.inproc_terminal(ci, stdin_tty, stdout_tty) as (stdout, stderr), \
                patch("builtins.input", scripted_input):
            code = module.main([str(arg) for arg in args])
        self.assertEqual(script, [], "Scripted answers left unused")
        result = subprocess.CompletedProcess(args, code, stdout.getvalue(), stderr.getvalue())
        result.prompts = prompts
        return result

    def assert_status(self, result, code):
        self.assertEqual(result.returncode, code, f"\n--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}")

    def assert_line(self, transcript, line):
        """line is a whole line of the transcript."""
        self.assertIn(line, transcript.split("\n"), f"missing line {line!r} in:\n{transcript}")

    def assert_line_ends(self, transcript, text):
        """Some line of the transcript ends with text. A report on stderr can follow a prompt on
        the same line, since the prompt's stream is not fixed and its answer echoes on the pty."""
        self.assertTrue(any(line.endswith(text) for line in transcript.split("\n")),
                        f"no line ends with {text!r} in:\n{transcript}")

    def assert_in_order(self, transcript, *texts):
        """Each text appears in the transcript after the one before it."""
        position = -1
        for text in texts:
            found = transcript.find(text, position + 1)
            self.assertGreater(found, position, f"{text!r} not found after the previous text in:\n{transcript}")
            position = found

    def assert_not_asked(self, result):
        """No line of the creation question and no question prompt on either stream."""
        combined = result.stdout + result.stderr
        for text in (QUESTION_HEADER.split("{NAME}")[0], QUESTION_TRIAD, QUESTION_SINGLE, QUESTION_PROMPT):
            self.assertNotIn(text, combined)

    def assert_question(self, transcript, name, *obstacles):
        """The question's lines in order and consecutive: the header for name, entry 1, the given
        obstacle lines (already formatted), entry 2."""
        lines = transcript.split("\n")
        header = QUESTION_HEADER.format(NAME=name)
        self.assertIn(header, lines, f"missing question header in:\n{transcript}")
        start = lines.index(header)
        self.assertEqual(lines[start + 1:start + 3 + len(obstacles)], [QUESTION_TRIAD, *obstacles, QUESTION_SINGLE])

    def obstacle_env(self, fake):
        """question_env(None) with the fake openRepoShape on PATH (asserted), or with none on
        PATH (asserted) when fake is false."""
        if fake:
            return self.shape_env(ci=None)
        (self.fake_bin() / "openRepoShape").unlink(missing_ok=True)
        env = self.question_env(None)
        self.assert_absent_from_path(env, "openRepoShape")
        return env

    def known_obstacle_cases(self):
        """Each known obstacle alone, then all three: label to (name, whether the fake
        openRepoShape is on PATH, extra arguments, the formatted obstacle lines in D13 order)."""
        absent = self.base / "absent parent"
        name_line = OBSTACLE_NAME.format(NAME="my-app")
        parent_line = OBSTACLE_PARENT.format(PARENT=absent)
        # A parent that exists but is not a directory, given as a regular file and as a symbolic link
        # to it, both named by the file; a dangling symbolic link, named by its target with the
        # missing-parent line; and the file with the other two obstacles, the parent line last
        # (fix-parent-obstacle-wording design D3).
        parent_file, file_link, dangling_link, dangling_target = self.parent_fixtures()
        file_line = OBSTACLE_PARENT_NOT_A_DIRECTORY.format(PARENT=parent_file)
        return {"name": ("my-app", True, (), [name_line]),
                "openRepoShape": ("MyApp", False, (), [OBSTACLE_OPENREPOSHAPE]),
                "parent": ("MyApp", True, ("--into", absent), [parent_line]),
                "all three": ("my-app", False, ("--into", absent), [name_line, OBSTACLE_OPENREPOSHAPE, parent_line]),
                "file parent": ("MyApp", True, ("--into", parent_file), [file_line]),
                "link to the file parent": ("MyApp", True, ("--into", file_link), [file_line]),
                "dangling link parent": ("MyApp", True, ("--into", dangling_link),
                                         [OBSTACLE_PARENT.format(PARENT=dangling_target)]),
                "all three with the file parent": ("my-app", False, ("--into", parent_file),
                                                   [name_line, OBSTACLE_OPENREPOSHAPE, file_line])}

    parent_file_content = "A regular file where a parent directory is expected.\n"

    def parent_file_fixture(self, path):
        """A regular file at path holding parent_file_content: a parent that exists but is not a
        directory (fix-parent-obstacle-wording design D3)."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.parent_file_content)
        return path

    def parent_fixtures(self):
        """The parent fixtures of fix-parent-obstacle-wording design D3, under self.base: a regular
        file, a symbolic link to it, and a dangling symbolic link. Returns (the file, the link to
        it, the dangling link, the dangling link's target); the file and the target are the paths
        new() resolves those links to, since self.base is already resolved."""
        parent_file = self.parent_file_fixture(self.base / "file parent")
        file_link = self.base / "link to file parent"
        file_link.symlink_to(parent_file)
        dangling_target = self.base / "absent link target"
        dangling_link = self.base / "dangling link parent"
        dangling_link.symlink_to(dangling_target)
        return parent_file, file_link, dangling_link, dangling_target

    def assert_parent_file_unchanged(self, path, before):
        """Nothing was created under self.base since the before snapshot, and path is still a
        regular file holding parent_file_content (fix-parent-obstacle-wording design D3, N2)."""
        self.assertEqual(sorted(self.base.rglob("*")), before)
        self.assertTrue(path.is_file() and not path.is_symlink(), f"{path} is no longer a regular file")
        self.assertEqual(path.read_text(), self.parent_file_content)

    def run_cli_streams(self, *args, stdin="", stderr=subprocess.PIPE, prefix=()):
        """Like run_cli, with the stdin text and the stderr target chosen by the test (a pipe,
        subprocess.STDOUT, a descriptor or a file) and an optional command prefix, such as a
        shell that closes stderr before it runs project."""
        return subprocess.run([*prefix, sys.executable, str(CLI), *map(str, args)],
                              cwd=self.base, env=self.env, input=stdin, text=True,
                              stdout=subprocess.PIPE, stderr=stderr, timeout=20)

    def creation_stdout(self, name, parent=None):
        """The pinned stdout of a test-generator creation of name in parent (PROJECTS_DIR by
        default) that is confirmed and not asked: the plan, then Created: and Next:."""
        parent = parent or self.base
        destination = parent / name
        return (f"Create: {destination}\n  " + shlex.join(["bash", str(self.generator), name, str(parent)])
                + f"\nCreated: {destination}\nNext: project doctor {shlex.quote(str(destination))}\n")

    def advisory(self, name):
        """The two creation advisory lines for name, from the D13 fixtures."""
        return [ADVISORY_PREFERENCE.format(NAME=name), ADVISORY_CONVERSION]

    def assert_created(self, destination, parent=None):
        """destination holds exactly the test generator's file and the pinned .project.json."""
        parent = parent or destination.parent
        self.assertEqual(sorted(path.name for path in destination.iterdir()), [".project.json", "arguments"])
        self.assertEqual((destination / "arguments").read_text(), f"{destination.name}\n{parent}\n")
        self.assertEqual((destination / ".project.json").read_text(),
                         json.dumps({"schema_version": 1, "bench": "testBench", "type": "test"}, indent=2) + "\n")

    def assert_advised_run_unharmed(self, result, name):
        """A --type test --yes creation whose stderr could not take the advisory: exit 0, the
        pinned stdout with no warning: in it, and the repository created."""
        self.assert_status(result, 0)
        self.assertEqual(result.stdout, self.creation_stdout(name))
        self.assertNotIn("warning:", result.stdout)
        self.assert_created(self.base / name)

    def repo(self, name="repo", branch="main"):
        path = self.base / name
        path.mkdir(parents=True, exist_ok=True)
        self.git(path, "init", "-b", branch)
        self.git(path, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "--allow-empty", "-m", "initial")
        return path

    def git(self, path, *args):
        result = subprocess.run(["git", "-C", str(path), *args], env=self.env,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def commit(self, path):
        self.git(path, "add", ".")
        self.git(path, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "-m", "fixture")

    def test_benches_excludes_updaters_and_reports_missing(self):
        result = self.run_cli("benches", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = json.loads(result.stdout)
        self.assertEqual([r["type"] for r in rows], ["test", "missing"])
        self.assertTrue(rows[0]["available"])
        self.assertFalse(rows[1]["available"])

    def test_benches_discovers_a_workbench_from_its_own_directory(self):
        previous = self.env.pop("WORKBENCHES_ROOT")
        self.addCleanup(self.env.__setitem__, "WORKBENCHES_ROOT", previous)
        result = self.run_cli("benches", "--json", cwd=self.wb)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)[0]["bench"], "testBench")

    def test_new_preserves_paths_with_spaces_and_writes_profile(self):
        parent = self.base / "new parent"
        result = self.run_cli("new", "MyApp", parent, "--type", "test", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((parent / "MyApp/arguments").read_text().splitlines(), ["MyApp", str(parent)])
        profile = json.loads((parent / "MyApp/.project.json").read_text())
        self.assertEqual(profile["bench"], "testBench")

    def test_dry_run_creates_no_parent(self):
        parent = self.base / "absent"
        result = self.run_cli("new", "App", parent, "--type", "test", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(parent.exists())

    def test_existing_destination_and_noninteractive_confirmation_refuse(self):
        target = self.base / "App"
        target.mkdir()
        result = self.run_cli("new", "App", "--type", "test", "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(list(target.iterdir()), [])
        result = self.run_cli("new", "Another", "--type", "test")
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.base / "Another").exists())

    def test_generator_failure_propagates_and_no_workflow_follows(self):
        self.generator.write_text("#!/bin/bash\nexit 17\n")
        result = self.run_cli("new", "App", "--type", "test", "--yes")
        self.assertEqual(result.returncode, 17, result.stderr)
        self.assertFalse((self.base / "App/.project.json").exists())

    def test_success_without_project_is_failure(self):
        self.generator.write_text("#!/bin/bash\nexit 0\n")
        self.assertEqual(self.run_cli("new", "App", "--type", "test", "--yes").returncode, 2)

    def test_registry_paths_cannot_escape_or_follow_outside_symlink(self):
        self.config["benches"]["testBench"]["path"] = "../outside"
        self.save_config()
        self.assertEqual(self.run_cli("benches").returncode, 2)
        self.config["benches"]["testBench"]["path"] = "link"
        (self.wb / "link").symlink_to(self.base)
        self.save_config()
        self.assertEqual(self.run_cli("benches").returncode, 2)

    def test_keyword_selection_is_case_insensitive_and_ambiguous_refuses(self):
        result = self.run_cli("new", "App", "--description", "PYTHON app", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.config["benches"]["testBench"]["project_scripts"].append(
            {"name": "second", "script": "scripts/new-test.sh"})
        self.save_config()
        self.assertEqual(self.run_cli("new", "App", "--description", "python", "--dry-run").returncode, 2)

    def test_invalid_json_and_manifest_are_structured_errors(self):
        (self.wb / "config/bench-config.json").write_text("[")
        result = self.run_cli("benches", "--json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("error", json.loads(result.stdout))
        root = self.repo()
        (root / "project.yaml").write_text("kind: [")
        result = self.run_cli("status", root, "--json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("error", json.loads(result.stdout))

    def test_invalid_yaml_encoding_is_a_structured_error(self):
        root = self.repo()
        (root / "project.yaml").write_bytes(b"kind: \xff\n")
        result = self.run_cli("status", root, "--json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("error", json.loads(result.stdout))
        self.assertNotIn("Traceback", result.stderr)

    def test_status_from_nested_path_and_feature_worktree_is_read_only(self):
        root = self.repo()
        child = root / "nested"
        child.mkdir()
        (root / "dirty").write_text("preserve")
        before = self.git(root, "status", "--porcelain")
        result = self.run_cli("status", "--json", cwd=child)
        report = json.loads(result.stdout)
        self.assertEqual(report["root"], str(root))
        self.assertTrue(report["repository"]["dirty"])
        self.assertEqual(before, self.git(root, "status", "--porcelain"))
        tree = self.base / "feature"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        report = json.loads(self.run_cli("status", tree, "--json").stdout)
        self.assertEqual(report["repository"]["branch"], "001-feature")
        self.assertEqual(len(report["repository"]["worktrees"]), 2)

    def test_shape_skips_assembly_dot_and_reports_missing_legs(self):
        root = self.repo("Atlas")
        (root / "project.yaml").write_text('kind: project-manifest\ntracking_branch: develop\nlegs:\n'
            '  - {role: assembly, path: "."}\n  - {role: spec, path: spec}\n  - {role: code, path: code}\n')
        (root / "spec").mkdir()  # Must not confuse parent Git with a leg checkout.
        result = self.run_cli("doctor", root, "--json")
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(len(report["children"]), 2)
        self.assertFalse(report["children"][0]["present"])
        self.assertEqual(report["children"][0]["tracking_branch"], "develop")

    def test_human_reports_render_present_project_leg_state(self):
        root = self.repo("Atlas")
        leg = self.repo("Atlas/spec")
        (root / "project.yaml").write_text("kind: project-manifest\nlegs:\n  - {role: spec, path: spec}\n")
        for command in ("status", "doctor"):
            result = self.run_cli(command, root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(f"spec: {leg} — main; dirty=False", result.stdout)

    def test_family_name_prefers_holder_and_inspects_working_sibling(self):
        root = self.repo("Family/Family")
        (root / "family.yaml").write_text("kind: family-manifest\nmembers:\n  - project: Atlas\n    path: members/Atlas\n")
        member = self.repo("Family/Atlas")
        (member / "project.yaml").write_text("kind: project-manifest\nlegs: []\n")
        result = self.run_cli("status", "Family", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["root"], str(root))
        self.assertEqual(report["children"][0]["root"], str(member))

    def test_family_name_refuses_ambiguous_default_project_roots(self):
        bases = [self.base / "first-projects", self.base / "second-projects"]
        for base in bases:
            holder = base / "Family/Family"
            holder.mkdir(parents=True)
            (holder / "family.yaml").write_text("kind: family-manifest\nmembers: []\n")
        with patch.object(module, "projects_dirs", return_value=bases):
            with self.assertRaisesRegex(module.Refused, "Ambiguous project name"):
                module.discover("Family")

    def test_registered_claude_git_commands_have_skill_bundles(self):
        registry = json.loads((ROOT / ".specify/extensions/.registry").read_text())
        commands = registry["extensions"]["git"]["registered_commands"]["claude"]
        for command in commands:
            skill = command.replace(".", "-")
            self.assertTrue((ROOT / ".claude/skills" / skill / "SKILL.md").is_file(), command)

    def test_update_default_and_dry_run_do_not_execute(self):
        root = self.repo()
        result = self.run_cli("update", root, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)["updates"]), 4)
        result = self.run_cli("update", root, "--apply", "--component", "workflow", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("setup-openspeckit", result.stdout)
        self.assertFalse((root / ".specify").exists())

    def test_update_refuses_dirty_and_feature_branch(self):
        root = self.repo()
        (root / "dirty").write_text("preserve")
        result = self.run_cli("update", root, "--apply", "--component", "bench", "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertIn("clean tracking", result.stderr)
        self.commit(root)
        self.git(root, "switch", "-c", "001-feature")
        self.assertEqual(self.run_cli("update", root, "--apply", "--component", "bench", "--yes").returncode, 2)

    def test_shape_plan_keeps_owner_confirmation(self):
        with patch.object(module.shutil, "which", return_value="/bin/tool"), patch.object(module, "execute", return_value=19) as run:
            code = module.main(["new", "Atlas", "--shape", "--org", "example", "--visibility", "private",
                                "--into", str(self.base), "--yes"])
        self.assertEqual(code, 19)
        self.assertNotIn("--yes", run.call_args.args[0])
        self.assertIn("openRepoShape", run.call_args.args[0])

    def test_exact_bench_updater_receives_only_selected_root(self):
        root = self.repo()
        (root / ".project.json").write_text(json.dumps({"schema_version": 1, "bench": "testBench", "type": "test"}))
        self.commit(root)
        updater = self.generator.parent / "update-test.sh"
        updater.write_text('#!/bin/bash\nprintf "%s" "$1"\nexit 23\n')
        result = self.run_cli("update", root, "--apply", "--component", "bench", "--yes")
        self.assertEqual(result.returncode, 23, result.stderr)
        self.assertTrue(result.stdout.endswith(str(root)))

    def test_handoff_reads_matching_record_without_changing_it(self):
        root = self.repo()
        self.git(root, "remote", "add", "origin", "git@github.com:example/Atlas.git")
        config = self.base / "home/.agents"
        config.mkdir(parents=True)
        workspace = self.base / "parked"
        records = workspace / "workspaces/example"
        records.mkdir(parents=True)
        (config / "workspace.yaml").write_text(f"repository: example/wip\npath: {workspace}\n")
        record = records / "atlas.yaml"
        content = "kind: workspace-manifest\nprojects:\n  - repository: example/Atlas\n    parked_at: 2026-09-10T18:42:11Z\n    active_feature: 001-demo\n    features: [{branch: 001-demo}]\n"
        record.write_text(content)
        result = self.run_cli("status", root, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        handoff = json.loads(result.stdout)["handoff"]
        self.assertEqual(handoff["state"], "recorded")
        self.assertEqual(handoff["records"][0]["features"], 1)
        self.assertEqual(record.read_text(), content)

    def test_handoff_rejects_path_like_remote_identity_before_record_lookup(self):
        root = self.repo()
        self.git(root, "remote", "add", "origin", "git@github.com:../repo")
        config = self.base / "home/.agents"
        config.mkdir(parents=True)
        workspace = self.base / "parked"
        workspace.mkdir()
        (config / "workspace.yaml").write_text(f"repository: example/wip\npath: {workspace}\n")
        (workspace / "sentinel.yaml").write_text("kind: [\n")
        result = self.run_cli("status", root, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["handoff"]["state"],
                         "no GitHub repository identity to match a parked record")

    def test_handoff_rejects_non_github_host_before_record_lookup(self):
        root = self.repo()
        self.git(root, "remote", "add", "origin", "https://evilgithub.com/example/repo.git")
        config = self.base / "home/.agents"
        config.mkdir(parents=True)
        workspace = self.base / "parked"
        workspace.mkdir()
        (config / "workspace.yaml").write_text(f"repository: example/wip\npath: {workspace}\n")
        result = self.run_cli("status", root, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["handoff"]["state"],
                         "no GitHub repository identity to match a parked record")

    def test_doctor_validate_reports_missing_owner_scripts(self):
        root = self.repo()
        (root / "project.yaml").write_text("kind: project-manifest\nlegs: []\n")
        result = self.run_cli("doctor", root, "--validate", "--json")
        self.assertEqual(result.returncode, 1, result.stderr)
        errors = [c for c in json.loads(result.stdout)["checks"] if c["level"] == "error"]
        self.assertEqual({c["check"] for c in errors}, {"validate-manifest.py", "validate-pins.py"})

    def test_profile_reports_filter_unknown_secret_fields(self):
        root = self.repo()
        (root / ".project.json").write_text(json.dumps({
            "schema_version": 1, "bench": "testBench", "type": "test", "token": "do-not-report"}))
        status = self.run_cli("status", root, "--json")
        self.assertEqual(status.returncode, 0, status.stderr)
        self.assertNotIn("token", json.loads(status.stdout)["profile"])
        doctor = self.run_cli("doctor", root, "--json")
        self.assertEqual(doctor.returncode, 0, doctor.stderr)
        self.assertNotIn("token", json.loads(doctor.stdout)["profile"])

    def test_malformed_bench_entries_refuse_without_tracebacks(self):
        root = self.repo()
        (root / ".project.json").write_text(json.dumps({"schema_version": 1, "bench": "testBench", "type": "test"}))
        self.config["benches"]["testBench"] = []
        self.save_config()
        doctor = self.run_cli("doctor", root, "--json")
        self.assertEqual(doctor.returncode, 2)
        self.assertIn("error", json.loads(doctor.stdout))
        update = self.run_cli("update", root, "--apply", "--component", "bench", "--yes")
        self.assertEqual(update.returncode, 2)
        self.assertNotIn("Traceback", update.stderr)

    def test_update_refuses_missing_child_and_retains_shape_owner_prompt(self):
        root = self.repo("Atlas")
        (root / "project.yaml").write_text("kind: project-manifest\nlegs:\n  - {role: spec, path: spec}\n")
        self.commit(root)
        missing = self.run_cli("update", root, "--apply", "--component", "shape", "--yes")
        self.assertEqual(missing.returncode, 2)
        self.assertIn("Child checkout is missing", missing.stderr)
        source = self.base / "shape"
        source.mkdir()
        (source / "update-shape.py").write_text("import sys\nsys.exit(0)\n")
        (root / "spec").mkdir()
        self.git(root / "spec", "init", "-b", "main")
        self.git(root / "spec", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "--allow-empty", "-m", "initial")
        self.commit(root)
        with patch.object(module, "execute", return_value=0) as run:
            code = module.main(["update", str(root), "--apply", "--component", "shape", "--shape-source",
                                str(source), "--at", "a" * 40, "--yes"])
        self.assertEqual(code, 0)
        self.assertEqual(run.call_count, 2)
        self.assertTrue(all("--yes" not in call.args[0] for call in run.call_args_list))

    def test_update_refuses_a_dirty_family_member(self):
        holder = self.repo("Family/Family")
        (holder / "family.yaml").write_text("kind: family-manifest\nmembers:\n  - project: Atlas\n")
        self.commit(holder)
        member = self.repo("Family/Atlas")
        (member / "project.yaml").write_text("kind: project-manifest\nlegs: []\n")
        self.commit(member)
        (member / "preserve").write_text("dirty")
        result = self.run_cli("update", holder, "--apply", "--component", "shape", "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Child has work to preserve", result.stderr)

    def test_doctor_validate_with_a_project_leg_has_structured_output(self):
        root = self.repo("Atlas")
        leg = self.repo("Atlas/spec")
        (root / "project.yaml").write_text("kind: project-manifest\nlegs:\n  - {role: spec, path: spec}\n")
        result = self.run_cli("doctor", root, "--validate", "--json")
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertIn("checks", report)
        self.assertEqual(report["children"][0]["path"], str(leg))

    def test_shape_update_runs_check_then_apply_and_propagates_failure(self):
        root = self.repo()
        (root / "project.yaml").write_text("kind: project-manifest\nlegs: []\n")
        self.commit(root)
        source = self.base / "shape"
        source.mkdir()
        (source / "update-shape.py").write_text("import sys\nprint(sys.argv[1])\nsys.exit(1 if sys.argv[1] == 'check' else 9)\n")
        result = self.run_cli("update", root, "--apply", "--component", "shape", "--shape-source", source,
                              "--at", "a" * 40, "--yes")
        self.assertEqual(result.returncode, 9, result.stderr)
        self.assertTrue(result.stdout.endswith("check\napply\n"), result.stdout)

    def test_clean_is_read_only_and_classifies_linked_worktrees(self):
        root = self.repo()
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        before = self.git(root, "worktree", "list", "--porcelain")
        result = self.run_cli("clean", root, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["target_branch"], "main")
        self.assertIn("last fetch", report["tracking_freshness"])
        by_branch = {row["branch"]: row for row in report["worktrees"]}
        self.assertEqual(by_branch["main"]["classification"], "protected-default")
        self.assertEqual(by_branch["001-feature"]["classification"], "unpublished")
        self.assertEqual(before, self.git(root, "worktree", "list", "--porcelain"))
        self.assertTrue(tree.is_dir())

    def test_clean_refuses_unmerged_worktree_removal(self):
        root = self.repo()
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        (tree / "work").write_text("preserve")
        self.commit(tree)
        result = self.run_cli("clean", root, "--apply", "--action", "remove",
                              "--worktree", tree, "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unpublished", result.stderr)
        self.assertTrue(tree.is_dir())
        result = self.run_cli("clean", root, "--apply", "--action", "delete-branch",
                              "--branch", "001-feature", "--yes")
        self.assertEqual(result.returncode, 2)
        result = self.run_cli("clean", root, "--apply", "--action", "delete-branch",
                              "--branch", "main", "--yes")
        self.assertEqual(result.returncode, 2)

    def test_clean_removes_only_merged_worktree_and_keeps_branch(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        (tree / "work").write_text("done")
        self.commit(tree)
        self.git(tree, "push", "-u", "origin", "001-feature")
        self.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "merge", "--no-ff", "001-feature", "-m", "merge feature")
        result = self.run_cli("clean", root, "--apply", "--action", "remove",
                              "--worktree", tree, "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(tree.exists())
        self.assertEqual(self.git(root, "show-ref", "--verify", "--quiet", "refs/heads/001-feature"), "")
        result = self.run_cli("clean", root, "--apply", "--action", "delete-branch",
                              "--branch", "001-feature", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIsNone(module.git_text(root, "show-ref", "--verify", "--quiet", "refs/heads/001-feature"))

    def test_clean_never_removes_the_worktree_containing_the_current_directory(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        (tree / "work").write_text("done")
        self.commit(tree)
        self.git(tree, "push", "-u", "origin", "001-feature")
        self.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "merge", "--no-ff", "001-feature", "-m", "merge feature")
        result = self.run_cli("clean", root, "--apply", "--action", "remove",
                              "--worktree", tree, "--yes", cwd=tree)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Cannot remove the current worktree", result.stderr)
        self.assertTrue(tree.is_dir())

    def test_clean_pushes_explicit_clean_feature_branch_without_force(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        self.git(tree, "push", "-u", "origin", "001-feature")
        (tree / "work").write_text("publish")
        self.commit(tree)
        result = self.run_cli("clean", root, "--apply", "--action", "push",
                              "--branch", "001-feature", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git(tree, "rev-parse", "HEAD"),
                         self.git(root, "rev-parse", "refs/remotes/origin/001-feature"))

    def test_clean_reports_dirty_detached_and_pushed_unmerged_states(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        feature = self.base / "feature-tree"
        detached = self.base / "detached-tree"
        dirty = self.base / "dirty-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(feature))
        self.git(feature, "push", "-u", "origin", "001-feature")
        (feature / "review-work").write_text("review")
        self.commit(feature)
        self.git(feature, "push", "origin", "001-feature")
        self.git(root, "worktree", "add", "--detach", str(detached))
        self.git(root, "worktree", "add", "-b", "001-dirty", str(dirty))
        (dirty / "uncommitted").write_text("preserve")
        report = json.loads(self.run_cli("clean", root, "--json", cwd=feature).stdout)
        by_branch = {row["branch"]: row for row in report["worktrees"]}
        self.assertEqual(by_branch["001-feature"]["classification"], "pushed-unmerged")
        self.assertTrue(by_branch["001-feature"]["current"])
        self.assertEqual(by_branch["detached"]["classification"], "detached")
        self.assertEqual(by_branch["001-dirty"]["classification"], "dirty")

    def test_clean_reports_stale_worktree_metadata(self):
        root = self.repo()
        tree = self.base / "stale-tree"
        self.git(root, "worktree", "add", "-b", "001-stale", str(tree))
        shutil.rmtree(tree)
        report = json.loads(self.run_cli("clean", root, "--json").stdout)
        stale = next(row for row in report["worktrees"] if row["path"] == str(tree))
        self.assertEqual(stale["classification"], "stale-worktree")

    def test_clean_preserves_ignored_files_in_an_otherwise_merged_worktree(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        (tree / ".gitignore").write_text("local.env\n")
        (tree / "work").write_text("done")
        self.commit(tree)
        self.git(tree, "push", "-u", "origin", "001-feature")
        self.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "merge", "--no-ff", "001-feature", "-m", "merge feature")
        ignored = tree / "local.env"
        ignored.write_text("preserve")
        report = json.loads(self.run_cli("clean", root, "--json").stdout)
        row = next(item for item in report["worktrees"] if item["branch"] == "001-feature")
        self.assertEqual(row["classification"], "ignored-local-files")
        result = self.run_cli("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertTrue(ignored.is_file())

    def test_clean_refuses_to_guess_a_nonstandard_default_branch(self):
        root = self.repo(branch="develop")
        result = self.run_cli("clean", root, "--json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Cannot determine the default branch", json.loads(result.stdout)["error"])

    def test_clean_pushes_to_a_differently_named_upstream_branch(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-local", str(tree))
        self.git(tree, "push", "-u", "origin", "001-local:review/remote")
        (tree / "work").write_text("publish")
        self.commit(tree)
        result = self.run_cli("clean", root, "--apply", "--action", "push", "--branch", "001-local", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git(tree, "rev-parse", "HEAD"),
                         self.git(remote, "rev-parse", "refs/heads/review/remote"))

    def test_clean_refuses_diverged_branch_push(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        self.git(tree, "push", "-u", "origin", "001-feature")
        (tree / "local").write_text("local")
        self.commit(tree)
        other = self.base / "other"
        subprocess.run(["git", "clone", "--branch", "001-feature", str(remote), str(other)], env=self.env,
                       check=True, text=True, capture_output=True)
        (other / "remote").write_text("remote")
        self.git(other, "add", ".")
        self.git(other, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "remote")
        self.git(other, "push")
        self.git(tree, "fetch", "origin")
        report = json.loads(self.run_cli("clean", root, "--json").stdout)
        row = next(item for item in report["worktrees"] if item["branch"] == "001-feature")
        self.assertEqual(row["classification"], "diverged")
        result = self.run_cli("clean", root, "--apply", "--action", "push", "--branch", "001-feature", "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertIn("reconcile", result.stderr)

    def test_clean_revalidates_a_worktree_after_confirmation(self):
        root = self.repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], env=self.env, check=True,
                       text=True, capture_output=True)
        self.git(root, "remote", "add", "origin", remote)
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", str(tree))
        (tree / "work").write_text("done")
        self.commit(tree)
        self.git(tree, "push", "-u", "origin", "001-feature")
        self.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "merge", "--no-ff", "001-feature", "-m", "merge feature")
        def change_after_plan(_):
            (tree / "late-change").write_text("preserve")
        args = module.argparse.Namespace(target=str(root), json=False, apply=True, action="remove",
                                         branch=None, worktree=str(tree), yes=True)
        with patch.object(module, "confirm", side_effect=change_after_plan):
            with self.assertRaises(module.Refused):
                module.clean(args)
        self.assertTrue(tree.is_dir())

    def test_inproc_person_at_terminal_rule(self):
        for ci in (None, "", "0", "false", "no", " FALSE ", " No "):
            with self.subTest(CI=ci), self.inproc_terminal(ci):
                self.assertIs(module.person_at_terminal(), True)
        for ci in ("true", "1", "yes", "anything"):
            with self.subTest(CI=ci), self.inproc_terminal(ci):
                self.assertIs(module.person_at_terminal(), False)
        for stdin_tty, stdout_tty in ((False, True), (True, False), (False, False)):
            with self.subTest(stdin_tty=stdin_tty, stdout_tty=stdout_tty), \
                    self.inproc_terminal(None, stdin_tty, stdout_tty):
                self.assertIs(module.person_at_terminal(), False)
        for stream in ("stdin", "stdout"):
            with self.subTest(stream=stream, value=None), self.inproc_terminal(None), \
                    patch.object(sys, stream, None):
                self.assertIs(module.person_at_terminal(), False)
            with self.subTest(stream=stream, value="no isatty"), self.inproc_terminal(None), \
                    patch.object(sys, stream, object()):
                self.assertIs(module.person_at_terminal(), False)
            for error in (OSError, ValueError, AttributeError):
                with self.subTest(stream=stream, error=error.__name__), self.inproc_terminal(None), \
                        patch.object(getattr(sys, stream), "isatty", side_effect=error):
                    self.assertIs(module.person_at_terminal(), False)

    def test_pty_question_is_asked_once_the_name_is_known(self):
        self.config["benches"]["testBench"]["project_scripts"].append(
            {"name": "second", "script": "scripts/new-test.sh"})
        self.save_config()
        env = self.shape_env(ci=None)
        into = self.base / "into parent"
        into.mkdir()
        positional = self.base / "positional parent"
        positional.mkdir()
        header = QUESTION_HEADER.format(NAME="MyApp")
        cases = {"name given": ("MyApp",), "name typed": (), "--into": ("MyApp", "--into", into),
                 "positional parent": ("MyApp", positional), "--workbenches": ("MyApp", "--workbenches", self.wb)}
        for label, extra in cases.items():
            with self.subTest(label):
                steps = [(NAME_PROMPT, "MyApp")] if not extra else []
                steps += [(QUESTION_PROMPT, "2"), (GENERATOR_PROMPT, PTY_EOF)]
                result = self.run_pty("new", *extra, env=env, steps=steps)
                self.assert_status(result, 130)
                self.assert_line_ends(result.stderr, CANCELLED)
                if not extra:
                    self.assertNotIn(header, result.seen[0])
                self.assert_line(result.stdout, header)
                self.assert_in_order(result.stdout, header, "1. testBench:test", "2. testBench:second")
                combined = result.stdout + result.stderr
                self.assertNotIn("Create:", combined)
                self.assertNotIn(CONFIRM_PROMPT, combined)
                self.assertNotIn(ORG_PROMPT, combined)
                self.assertFalse((self.base / "MyApp").exists())

    def test_pty_question_entries(self):
        env = self.shape_env(ci=None)
        result = self.run_pty("new", "MyApp", env=env, steps=[(QUESTION_PROMPT, "2"), (CONFIRM_PROMPT, "yes")])
        self.assert_status(result, 0)
        lines = result.stdout.split("\n")
        start = lines.index(QUESTION_HEADER.format(NAME="MyApp"))
        self.assertEqual(lines[start + 1], QUESTION_TRIAD)
        self.assertEqual(lines[start + 2], QUESTION_SINGLE)
        self.assertNotIn(OBSTACLE_LINE_START, result.stdout)
        self.assertIn("(default)", QUESTION_TRIAD)
        for term in ("preferred, not required", "elective", "confers nothing"):
            self.assertIn(term, QUESTION_TRIAD)
        self.assertIn("single-repository.yaml", QUESTION_SINGLE)
        self.assertTrue((self.base / "MyApp/.project.json").is_file())
        self.assertEqual(list(self.base.rglob("single-repository.yaml")), [])

    def test_pty_single_answers_take_the_bench_path(self):
        env = self.shape_env(ci=None)
        for number, answer in enumerate(("2", "n", "no", "N", " No "), 1):
            name = f"Single{number}"
            destination = self.base / name
            with self.subTest(answer=answer):
                result = self.run_pty("new", name, env=env,
                                      steps=[(QUESTION_PROMPT, answer), (CONFIRM_PROMPT, "yes")])
                self.assert_status(result, 0)
                self.assert_in_order(result.stdout, QUESTION_HEADER.format(NAME=name), f"Create: {destination}",
                                     f"Created: {destination}")
                self.assert_line(result.stdout, "  " + shlex.join(["bash", str(self.generator), name, str(self.base)]))
                self.assertTrue(destination.is_dir())
                profile = json.loads((destination / ".project.json").read_text())
                self.assertEqual((profile["bench"], profile["type"]), ("testBench", "test"))
                self.assertNotIn(ORG_PROMPT, result.stdout + result.stderr)
                self.assertNotIn("warning:", result.stdout + result.stderr)
        self.assertIsNone(self.shape_record())

    def test_pty_single_answer_is_not_a_confirmation(self):
        env = self.shape_env(ci=None)
        result = self.run_pty("new", "MyApp", env=env, steps=[(QUESTION_PROMPT, "2"), (CONFIRM_PROMPT, "no")])
        self.assert_status(result, 2)
        self.assert_line_ends(result.stderr, REFUSED + DECLINED)
        self.assertFalse((self.base / "MyApp").exists())

    def test_pty_one_unrecognised_answer_is_asked_again(self):
        env = self.shape_env(ci=None)
        cases = (("3", "2", "AgainOne", (), [(CONFIRM_PROMPT, "yes")], True),
                 ("maybe", "n", "AgainTwo", ("--dry-run",), [], False))
        for first, second, name, flags, rest, created in cases:
            destination = self.base / name
            with self.subTest(first=first, second=second):
                result = self.run_pty("new", name, *flags, env=env,
                                      steps=[(QUESTION_PROMPT, first), (QUESTION_PROMPT, second), *rest])
                self.assert_status(result, 0)
                self.assertEqual((result.stdout + result.stderr).count(QUESTION_PROMPT), 2)
                self.assertEqual(result.stdout.split("\n").count(QUESTION_RETRY), 1)
                self.assert_in_order(result.stdout, QUESTION_HEADER.format(NAME=name), QUESTION_RETRY,
                                     f"Create: {destination}")
                self.assert_line(result.stdout, "  " + shlex.join(["bash", str(self.generator), name, str(self.base)]))
                self.assertEqual(destination.is_dir(), created)
                self.assertNotIn(ORG_PROMPT, result.stdout + result.stderr)

    def test_pty_two_unrecognised_answers_refuse(self):
        env = self.shape_env(ci=None)
        result = self.run_pty("new", "MyApp", env=env, steps=[(QUESTION_PROMPT, "3"), (QUESTION_PROMPT, "maybe")])
        self.assert_status(result, 2)
        self.assert_line_ends(result.stderr, REFUSED + QUESTION_MISSED)
        self.assertEqual(result.stdout.split("\n").count(QUESTION_RETRY), 1)
        self.assertNotIn("Create:", result.stdout)
        self.assertFalse((self.base / "MyApp").exists())
        self.assertIsNone(self.shape_record())

    def test_pty_end_of_input_at_the_question_refuses(self):
        env = self.shape_env(ci=None)
        result = self.run_pty("new", "MyApp", env=env, steps=[(QUESTION_PROMPT, PTY_EOF)])
        self.assert_status(result, 2)
        self.assert_line_ends(result.stderr, REFUSED + QUESTION_ENDED)
        self.assertNotIn(CANCELLED, result.stderr)
        self.assertFalse((self.base / "MyApp").exists())
        self.assertIsNone(self.shape_record())

    def test_pty_interrupt_at_the_question_cancels(self):
        env = self.shape_env(ci=None)
        result = self.run_pty("new", "MyApp", env=env, steps=[(QUESTION_PROMPT, signal.SIGINT)])
        self.assert_status(result, 130)
        self.assert_line_ends(result.stderr, CANCELLED)
        self.assertFalse((self.base / "MyApp").exists())
        self.assertIsNone(self.shape_record())

    def test_pty_end_of_input_at_existing_prompts_is_unchanged(self):
        env = self.shape_env(ci=None)
        cases = {"Project name": ((), [(NAME_PROMPT, PTY_EOF)]),
                 "Type yes": (("MyApp",), [(QUESTION_PROMPT, "2"), (CONFIRM_PROMPT, PTY_EOF)])}
        for label, (extra, steps) in cases.items():
            with self.subTest(label):
                result = self.run_pty("new", *extra, env=env, steps=steps)
                self.assert_status(result, 130)
                self.assert_line_ends(result.stderr, CANCELLED)
                self.assertFalse((self.base / "MyApp").exists())

    def test_pty_dry_run_single_answer_prints_the_generator_plan(self):
        env = self.shape_env(ci=None)
        parent = self.base / "new parent"
        result = self.run_pty("new", "MyApp", "--into", parent, "--dry-run", env=env,
                              steps=[(QUESTION_PROMPT, "2")])
        self.assert_status(result, 0)
        self.assert_in_order(result.stdout, QUESTION_HEADER.format(NAME="MyApp"), f"Create: {parent / 'MyApp'}")
        self.assert_line(result.stdout, f"Create: {parent / 'MyApp'}")
        self.assert_line(result.stdout, "  " + shlex.join(["bash", str(self.generator), "MyApp", str(parent)]))
        self.assertNotIn(CONFIRM_PROMPT, result.stdout + result.stderr)
        self.assertFalse(parent.exists())
        self.assertNotIn("warning:", result.stdout + result.stderr)

    def test_pty_refusals_before_a_path_come_first(self):
        env = self.shape_env(ci=None)
        existing = self.base / "Existing"
        existing.mkdir()
        other = self.base / "other parent"
        other.mkdir()
        cases = {"invalid name": (("bad name",), INVALID_NAME),
                 "positional parent with --into": (("MyApp", other, "--into", other), PARENT_AND_INTO),
                 "existing destination": (("Existing",), DESTINATION_EXISTS.format(PATH=existing))}
        for label, (extra, refusal) in cases.items():
            with self.subTest(label):
                result = self.run_pty("new", *extra, env=env)
                self.assert_status(result, 2)
                self.assert_line_ends(result.stderr, REFUSED + refusal)
                self.assert_not_asked(result)
                self.assertNotIn("Create:", result.stdout)
        self.assertEqual(list(existing.iterdir()), [])
        self.assertFalse((other / "MyApp").exists())
        self.assertIsNone(self.shape_record())

    def test_pty_answers_that_take_the_triad(self):
        env = self.shape_env(ci=None)
        for answer in ("", "1", "y", "yes", "Y", " YES "):
            with self.subTest(answer=answer):
                result = self.run_pty("new", "Atlas", env=env, steps=[(QUESTION_PROMPT, answer), (ORG_PROMPT, PTY_EOF)])
                self.assert_status(result, 2)
                self.assert_line_ends(result.stderr, REFUSED + ORG_ENDED)
                combined = result.stdout + result.stderr
                self.assertNotIn(GENERATOR_PROMPT, combined)
                self.assertNotIn(CONFIRM_PROMPT, combined)
                self.assertNotIn("Create:", result.stdout)
                self.assertFalse((self.base / "Atlas").exists())
        self.assertIsNone(self.shape_record())

    def test_pty_organization_then_visibility(self):
        env = self.shape_env(ci=None)
        result = self.run_pty("new", "Atlas", env=env, steps=[(QUESTION_PROMPT, ""), (ORG_PROMPT, "-bad"),
                                                              (ORG_PROMPT, "example"), (VIS_PROMPT, PTY_EOF)])
        self.assert_status(result, 2)
        self.assertNotIn(VIS_PROMPT, result.seen[1])
        self.assertNotIn(VIS_PROMPT, result.seen[2])
        self.assertEqual(result.stdout.split("\n").count(ORG_RETRY), 1)
        combined = result.stdout + result.stderr
        self.assertEqual(combined.count(ORG_PROMPT), 2)
        self.assertEqual(combined.count(VIS_PROMPT), 1)
        self.assert_line_ends(result.stderr, REFUSED + VIS_ENDED)
        self.assertIsNone(self.shape_record())

    def test_pty_visibility_is_a_full_word(self):
        env = self.shape_env(ci=None)
        for typed, word, restated in (("PUBLIC", "public", RESTATED_PUBLIC), (" private ", "private", RESTATED)):
            with self.subTest(accepted=typed):
                result = self.run_pty("new", "Atlas", env=env, steps=[
                    (QUESTION_PROMPT, ""), (ORG_PROMPT, "example"), (VIS_PROMPT, typed), (FAKE_SHAPE_PROMPT, "no")])
                self.assert_status(result, 1)
                self.assert_line(result.stdout, restated.format(NAME="Atlas", ORG="example", VIS=word))
                argv = self.shape_record()[-1]
                self.assertEqual(argv[argv.index("--visibility") + 1], word)
        for typed in ("1", "2", "3", ""):
            with self.subTest(rejected=typed):
                result = self.run_pty("new", "Atlas", env=env, steps=[
                    (QUESTION_PROMPT, ""), (ORG_PROMPT, "example"), (VIS_PROMPT, typed), (VIS_PROMPT, PTY_EOF)])
                self.assert_status(result, 2)
                self.assertEqual(result.stdout.split("\n").count(VIS_RETRY), 1)
                self.assert_line_ends(result.stderr, REFUSED + VIS_ENDED)
        self.assertEqual(len(self.shape_record()), 2)

    def test_pty_two_misses_at_organization_or_visibility_refuse(self):
        env = self.shape_env(ci=None)
        cases = {"organization": ([(ORG_PROMPT, ""), (ORG_PROMPT, "-x")], ORG_RETRY, ORG_MISSED),
                 "visibility": ([(ORG_PROMPT, "example"), (VIS_PROMPT, "1"), (VIS_PROMPT, "")], VIS_RETRY, VIS_MISSED)}
        for label, (steps, retry, refusal) in cases.items():
            with self.subTest(label):
                result = self.run_pty("new", "Atlas", env=env, steps=[(QUESTION_PROMPT, ""), *steps])
                self.assert_status(result, 2)
                self.assertEqual(result.stdout.split("\n").count(retry), 1)
                self.assert_line_ends(result.stderr, REFUSED + refusal)
                self.assertNotIn("Create:", result.stdout)
                self.assertFalse((self.base / "Atlas").exists())
                if label == "organization":
                    self.assertNotIn(VIS_PROMPT, result.stdout + result.stderr)
        self.assertIsNone(self.shape_record())

    def test_pty_end_of_input_at_organization_or_visibility_refuses(self):
        env = self.shape_env(ci=None)
        cases = {"organization": ([(ORG_PROMPT, PTY_EOF)], ORG_ENDED),
                 "visibility": ([(ORG_PROMPT, "example"), (VIS_PROMPT, PTY_EOF)], VIS_ENDED)}
        for label, (steps, refusal) in cases.items():
            with self.subTest(label):
                result = self.run_pty("new", "Atlas", env=env, steps=[(QUESTION_PROMPT, ""), *steps])
                self.assert_status(result, 2)
                self.assert_line_ends(result.stderr, REFUSED + refusal)
                self.assertNotIn(CANCELLED, result.stderr)
                self.assertFalse((self.base / "Atlas").exists())
        self.assertIsNone(self.shape_record())

    def test_pty_interrupt_at_organization_or_visibility_cancels(self):
        env = self.shape_env(ci=None)
        cases = {"organization": [(ORG_PROMPT, signal.SIGINT)],
                 "visibility": [(ORG_PROMPT, "example"), (VIS_PROMPT, signal.SIGINT)]}
        for label, steps in cases.items():
            with self.subTest(label):
                result = self.run_pty("new", "Atlas", env=env, steps=[(QUESTION_PROMPT, ""), *steps])
                self.assert_status(result, 130)
                self.assert_line_ends(result.stderr, CANCELLED)
                self.assertFalse((self.base / "Atlas").exists())
        self.assertIsNone(self.shape_record())

    def test_pty_restating_line_precedes_the_plan(self):
        env = self.shape_env(ci=None)
        destination = self.base / "Atlas"
        for word, restated in (("private", RESTATED), ("public", RESTATED_PUBLIC)):
            with self.subTest(word):
                result = self.run_pty("new", "Atlas", env=env, steps=[
                    (QUESTION_PROMPT, ""), (ORG_PROMPT, "example"), (VIS_PROMPT, word), (FAKE_SHAPE_PROMPT, "no")])
                self.assert_status(result, 1)
                line = restated.format(NAME="Atlas", ORG="example", VIS=word)
                self.assert_line(result.stdout, line)
                self.assertEqual(result.stdout.count(line), 1)
                self.assertNotIn(line, result.seen[2])
                self.assert_in_order(result.stdout, line, f"Create: {destination}", FAKE_SHAPE_PROMPT)
                self.assertFalse(destination.exists())

    def test_pty_triad_delegates_without_yes_and_keeps_its_confirmation(self):
        env = self.shape_env(ci=None)
        answers = [(QUESTION_PROMPT, ""), (ORG_PROMPT, " Example-Org "), (VIS_PROMPT, "private")]
        destination = self.base / "Atlas"
        result = self.run_pty("new", "Atlas", env=env, steps=[*answers, (FAKE_SHAPE_PROMPT, "yes")])
        self.assert_status(result, 0)
        self.assertTrue(destination.is_dir())
        self.assertEqual(self.shape_record(),
                         [["Atlas", "--org", "Example-Org", "--visibility", "private", "--into", str(self.base)]])
        self.assert_in_order(result.stdout, RESTATED.format(NAME="Atlas", ORG="Example-Org", VIS="private"),
                             f"Create: {destination}", FAKE_SHAPE_PROMPT, f"Created: {destination}")
        self.assertNotIn("warning:", result.stdout + result.stderr)
        declined = self.run_pty("new", "Orion", env=env, steps=[*answers, (FAKE_SHAPE_PROMPT, "no")])
        self.assert_status(declined, 1)
        self.assert_line(declined.stdout, FAKE_SHAPE_DECLINED)
        self.assertFalse((self.base / "Orion").exists())
        self.assertNotIn("Created:", declined.stdout)
        self.assertEqual(self.shape_record()[-1],
                         ["Orion", "--org", "Example-Org", "--visibility", "private", "--into", str(self.base)])
        self.assertNotIn("warning:", declined.stdout + declined.stderr)
        self.assertTrue(all("--yes" not in argv for argv in self.shape_record()))

    def test_pty_openreposhape_refusal_passes_through(self):
        env = self.shape_env(ci=None, status=5)
        result = self.run_pty("new", "Atlas", env=env, steps=[
            (QUESTION_PROMPT, ""), (ORG_PROMPT, "example"), (VIS_PROMPT, "private"), (FAKE_SHAPE_PROMPT, "yes")])
        self.assert_status(result, 5)
        self.assertEqual(len(self.shape_record()), 1)
        self.assertNotIn("Created:", result.stdout)

    def test_pty_dry_run_triad_answer_prints_the_openreposhape_plan(self):
        env = self.shape_env(ci=None)
        before = sorted(self.base.rglob("*"))
        result = self.run_pty("new", "Atlas", "--dry-run", env=env, steps=[
            (QUESTION_PROMPT, ""), (ORG_PROMPT, "example"), (VIS_PROMPT, "private")])
        self.assert_status(result, 0)
        destination = self.base / "Atlas"
        command = "  " + shlex.join(["openRepoShape", "Atlas", "--org", "example", "--visibility", "private",
                                     "--into", str(self.base)])
        self.assert_line(result.stdout, command)
        self.assert_in_order(result.stdout, RESTATED.format(NAME="Atlas", ORG="example", VIS="private"),
                             f"Create: {destination}", command)
        self.assertNotIn(FAKE_SHAPE_PROMPT, result.stdout + result.stderr)
        self.assertIsNone(self.shape_record())
        self.assertEqual(sorted(self.base.rglob("*")), before)
        self.assertNotIn("warning:", result.stdout + result.stderr)

    def test_pty_name_outside_the_assembly_form_is_named(self):
        env = self.shape_env(ci=None)
        result = self.run_pty("new", "my-app", env=env, steps=[(QUESTION_PROMPT, PTY_EOF)])
        self.assert_status(result, 2)
        self.assert_question(result.stdout, "my-app", OBSTACLE_NAME.format(NAME="my-app"))
        self.assertEqual(result.stdout.count(OBSTACLE_LINE_START), 1)
        self.assertIn("(default)", QUESTION_TRIAD)
        self.assert_line_ends(result.stderr, REFUSED + QUESTION_ENDED)
        self.assertFalse((self.base / "my-app").exists())

    def test_pty_missing_openreposhape_is_named(self):
        env = self.question_env(None)
        self.assert_absent_from_path(env, "openRepoShape")
        result = self.run_pty("new", "MyApp", env=env, steps=[(QUESTION_PROMPT, PTY_EOF)])
        self.assert_status(result, 2)
        self.assert_question(result.stdout, "MyApp", OBSTACLE_OPENREPOSHAPE)
        self.assertEqual(result.stdout.count(OBSTACLE_LINE_START), 1)
        self.assertFalse((self.base / "MyApp").exists())

    def test_pty_missing_parent_is_named_without_into(self):
        env = self.shape_env(ci=None)
        absent_projects = self.base / "absent projects"
        absent_into = self.base / "absent into"
        default_env = {key: value for key, value in env.items() if key != "PROJECTS_DIR"}
        default_projects = Path(default_env["HOME"]) / "projects"
        cases = {"PROJECTS_DIR": ({**env, "PROJECTS_DIR": str(absent_projects)}, (), absent_projects),
                 "default ~/projects": (default_env, (), default_projects),
                 "--into": (env, ("--into", absent_into), absent_into)}
        for label, (case_env, extra, parent) in cases.items():
            with self.subTest(label):
                result = self.run_pty("new", "MyApp", *extra, env=case_env, steps=[(QUESTION_PROMPT, PTY_EOF)])
                self.assert_status(result, 2)
                self.assert_question(result.stdout, "MyApp", OBSTACLE_PARENT.format(PARENT=parent))
                lines = result.stdout.split("\n")
                start = lines.index(QUESTION_HEADER.format(NAME="MyApp"))
                question = lines[start:lines.index(QUESTION_SINGLE, start) + 1]
                self.assertTrue(all("--into" not in line for line in question), question)
                self.assertFalse(parent.exists())
        # A parent that exists but is not a directory, by each route (fix-parent-obstacle-wording
        # design D3): named by the resolved file, with no question line containing --into.
        parent_file = self.parent_file_fixture(self.base / "file parent")
        default_file = self.parent_file_fixture(default_projects)
        file_cases = {"--into": (env, ("--into", parent_file), parent_file),
                      "positional parent": (env, (parent_file,), parent_file),
                      "PROJECTS_DIR": ({**env, "PROJECTS_DIR": str(parent_file)}, (), parent_file),
                      "default ~/projects": (default_env, (), default_file)}
        for label, (case_env, extra, parent) in file_cases.items():
            with self.subTest("file parent", route=label):
                before = sorted(self.base.rglob("*"))
                result = self.run_pty("new", "MyApp", *extra, env=case_env, steps=[(QUESTION_PROMPT, PTY_EOF)])
                self.assert_status(result, 2)
                self.assert_question(result.stdout, "MyApp", OBSTACLE_PARENT_NOT_A_DIRECTORY.format(PARENT=parent))
                lines = result.stdout.split("\n")
                start = lines.index(QUESTION_HEADER.format(NAME="MyApp"))
                question = lines[start:lines.index(QUESTION_SINGLE, start) + 1]
                self.assertTrue(all("--into" not in line for line in question), question)
                self.assert_parent_file_unchanged(parent, before)

    def test_pty_triad_answer_with_an_obstacle_refuses(self):
        for label, (name, fake, extra, obstacles) in self.known_obstacle_cases().items():
            with self.subTest(label):
                env = self.obstacle_env(fake)
                parent = Path(extra[1]) if extra else self.base
                # A parent that exists but is not a directory (fix-parent-obstacle-wording design D3).
                file_parent = parent.exists() and not parent.is_dir()
                before = sorted(self.base.rglob("*")) if file_parent else None
                result = self.run_pty("new", name, *extra, env=env, steps=[(QUESTION_PROMPT, "")])
                self.assert_status(result, 2)
                self.assert_question(result.stdout, name, *obstacles)
                self.assert_line_ends(result.stderr, REFUSED + obstacles_refusal(*obstacles))
                self.assertNotIn(ORG_PROMPT, result.stdout + result.stderr)
                self.assertNotIn("Create:", result.stdout)
                self.assertFalse((parent / name).exists())
                self.assertIsNone(self.shape_record())
                if file_parent:
                    self.assert_parent_file_unchanged(parent.resolve(), before)

    def test_inproc_triad_obstacle_runs_nothing(self):
        def forbidden(what):
            return AssertionError(f"{what} was called on a Triad answer with a known obstacle")
        for label, (name, fake, extra, obstacles) in self.known_obstacle_cases().items():
            with self.subTest(label):
                self.obstacle_env(fake)
                parent = Path(extra[1]) if extra else self.base
                # A parent that exists but is not a directory (fix-parent-obstacle-wording design D3).
                file_parent = parent.exists() and not parent.is_dir()
                before = sorted(self.base.rglob("*")) if file_parent else None
                with patch.object(module, "execute", side_effect=forbidden("execute")), \
                        patch("subprocess.run", side_effect=forbidden("subprocess.run")), \
                        patch("subprocess.Popen", side_effect=forbidden("subprocess.Popen")), \
                        patch("socket.socket", side_effect=forbidden("socket.socket")):
                    result = self.run_inproc("new", name, *extra, ci=None, answers=[""])
                self.assert_status(result, 2)
                self.assertEqual(result.prompts, [QUESTION_PROMPT + " "])
                self.assertEqual(result.stdout, "\n".join([QUESTION_HEADER.format(NAME=name), QUESTION_TRIAD,
                                                           *obstacles, QUESTION_SINGLE]) + "\n")
                self.assertEqual(result.stderr, REFUSED + obstacles_refusal(*obstacles) + "\n")
                self.assertFalse((parent / name).exists())
                self.assertIsNone(self.shape_record())
                if file_parent:
                    self.assert_parent_file_unchanged(parent.resolve(), before)

    def test_pty_dry_run_with_an_obstacle_refuses(self):
        env = self.shape_env(ci=None)
        absent = self.base / "absent parent"
        cases = {"name": (("my-app",), [OBSTACLE_NAME.format(NAME="my-app")]),
                 "parent": (("MyApp", "--into", absent), [OBSTACLE_PARENT.format(PARENT=absent)])}
        # A file, a symbolic link to it and a dangling symbolic link, each by --into
        # (fix-parent-obstacle-wording design D3): the loop's assertions apply to them as they stand,
        # and after the loop the file is still a regular file with its content (N2).
        parent_file, file_link, dangling_link, dangling_target = self.parent_fixtures()
        file_line = OBSTACLE_PARENT_NOT_A_DIRECTORY.format(PARENT=parent_file)
        cases.update({"file parent": (("MyApp", "--into", parent_file), [file_line]),
                      "link to the file parent": (("MyApp", "--into", file_link), [file_line]),
                      "dangling link parent": (("MyApp", "--into", dangling_link),
                                               [OBSTACLE_PARENT.format(PARENT=dangling_target)])})
        fixtures_before = sorted(self.base.rglob("*"))
        for label, (extra, obstacles) in cases.items():
            with self.subTest(label):
                before = sorted(self.base.rglob("*"))
                result = self.run_pty("new", *extra, "--dry-run", env=env, steps=[(QUESTION_PROMPT, "")])
                self.assert_status(result, 2)
                self.assert_line_ends(result.stderr, REFUSED + obstacles_refusal(*obstacles))
                self.assertNotIn(ORG_PROMPT, result.stdout + result.stderr)
                self.assertNotIn("Create:", result.stdout)
                self.assertEqual(sorted(self.base.rglob("*")), before)
                self.assertIsNone(self.shape_record())
        self.assert_parent_file_unchanged(parent_file, fixtures_before)

    def test_pty_single_answer_is_unaffected_by_obstacles(self):
        env = self.obstacle_env(fake=False)
        parent = self.base / "absent parent"
        destination = parent / "my-app"
        result = self.run_pty("new", "my-app", "--into", parent, env=env,
                              steps=[(QUESTION_PROMPT, "2"), (CONFIRM_PROMPT, "yes")])
        self.assert_status(result, 0)
        self.assert_question(result.stdout, "my-app", OBSTACLE_NAME.format(NAME="my-app"), OBSTACLE_OPENREPOSHAPE,
                             OBSTACLE_PARENT.format(PARENT=parent))
        plan = [f"Create: {destination}", "  " + shlex.join(["bash", str(self.generator), "my-app", str(parent)]),
                f"Created: {destination}", f"Next: project doctor {shlex.quote(str(destination))}"]
        for line in plan:
            self.assert_line(result.stdout, line)
        self.assert_in_order(result.stdout, QUESTION_SINGLE, *plan)
        self.assertEqual(sorted(path.name for path in destination.iterdir()), [".project.json", "arguments"])
        self.assertEqual((destination / "arguments").read_text().splitlines(), ["my-app", str(parent)])
        self.assertEqual(json.loads((destination / ".project.json").read_text()),
                         {"schema_version": 1, "bench": "testBench", "type": "test"})
        combined = result.stdout + result.stderr
        for text in (ORG_PROMPT, REFUSED, "warning:"):
            self.assertNotIn(text, combined)

    def test_pty_single_answer_with_a_file_parent_ends_as_the_flag_chosen_path(self):
        # fix-parent-obstacle-wording design D3: with a parent that exists but is not a directory,
        # the single-repository answer ends as the same name and parent end with the generator
        # chosen by flag (--type test, not asked): the same exit status, the same stdout from
        # Create: on and the same REFUSED: line; the advisory is left out of the comparison.
        env = self.shape_env(ci=None)
        parent_file = self.parent_file_fixture(self.base / "file parent")
        before = sorted(self.base.rglob("*"))
        asked = self.run_pty("new", "MyApp", "--into", parent_file, env=env,
                             steps=[(QUESTION_PROMPT, "2"), (CONFIRM_PROMPT, "yes")])
        baseline = self.run_pty("new", "MyApp", "--into", parent_file, "--type", "test", env=env,
                                steps=[(CONFIRM_PROMPT, "yes")])
        self.assert_question(asked.stdout, "MyApp", OBSTACLE_PARENT_NOT_A_DIRECTORY.format(PARENT=parent_file))
        self.assert_not_asked(baseline)
        self.assert_status(asked, baseline.returncode)
        for result in (asked, baseline):
            self.assertIn("Create:", result.stdout)
        self.assertEqual(asked.stdout[asked.stdout.index("Create:"):],
                         baseline.stdout[baseline.stdout.index("Create:"):])
        # A prompt can precede the report on its stderr line (see assert_line_ends), so each line is
        # compared from REFUSED: on.
        refused = [[line[line.index(REFUSED):] for line in result.stderr.split("\n") if REFUSED in line]
                   for result in (asked, baseline)]
        self.assertEqual(len(refused[0]), 1, asked.stderr)
        self.assertEqual(refused[0], refused[1])
        self.assertNotIn("warning:", asked.stdout + asked.stderr)
        self.assertIsNone(self.shape_record())
        self.assert_parent_file_unchanged(parent_file, before)

    def test_pty_symbolic_link_to_a_directory_names_no_obstacle(self):
        # fix-parent-obstacle-wording design D3: a symbolic link to a directory is a parent, and the
        # question names no obstacle, as in test_pty_no_known_obstacle_names_none.
        env = self.shape_env(ci=None)
        target = self.base / "linked directory"
        target.mkdir()
        link = self.base / "link to directory parent"
        link.symlink_to(target, target_is_directory=True)
        result = self.run_pty("new", "MyApp", "--into", link, env=env,
                              steps=[(QUESTION_PROMPT, ""), (ORG_PROMPT, PTY_EOF)])
        self.assert_status(result, 2)
        self.assert_question(result.stdout, "MyApp")
        self.assertNotIn(OBSTACLE_LINE_START, result.stdout + result.stderr)
        self.assert_line_ends(result.stderr, REFUSED + ORG_ENDED)
        self.assertIsNone(self.shape_record())
        self.assertEqual(list(target.iterdir()), [])

    def test_pty_no_known_obstacle_names_none(self):
        env = self.shape_env(ci=None)
        result = self.run_pty("new", "MyApp", env=env, steps=[(QUESTION_PROMPT, ""), (ORG_PROMPT, PTY_EOF)])
        self.assert_status(result, 2)
        self.assert_question(result.stdout, "MyApp")
        self.assertNotIn(OBSTACLE_LINE_START, result.stdout + result.stderr)
        self.assert_line_ends(result.stderr, REFUSED + ORG_ENDED)
        self.assertIsNone(self.shape_record())

    def test_pty_choosing_flags_skip_the_question(self):
        env = self.shape_env(ci=None)
        destination = self.base / "MyApp"
        plan = [f"Create: {destination}", "  " + shlex.join(["bash", str(self.generator), "MyApp", str(self.base)])]
        declined = [(CONFIRM_PROMPT, "no")]
        cases = {"--shape": (("--shape",), [], 2, SHAPE_NEEDS_ORG_AND_VISIBILITY),
                 "--org": (("--org", "example"), [], 2, ORG_NEEDS_SHAPE),
                 "--visibility": (("--visibility", "private"), [], 2, ORG_NEEDS_SHAPE),
                 "--family": (("--family", "Products"), [], 2, ORG_NEEDS_SHAPE),
                 "--elected-by": (("--elected-by", "alice"), [], 2, ORG_NEEDS_SHAPE),
                 "--bench": (("--bench", "testBench"), declined, 2, DECLINED),
                 "--type": (("--type", "test"), declined, 2, DECLINED),
                 "--description": (("--description", "python"), declined, 2, DECLINED),
                 '--description ""': (("--description", ""), declined, 2, DECLINED),
                 "--yes": (("--yes",), [], 0, None)}
        for label, (flags, steps, status, refusal) in cases.items():
            with self.subTest(label):
                result = self.run_pty("new", "MyApp", *flags, env=env, steps=steps)
                self.assert_status(result, status)
                self.assert_not_asked(result)
                if refusal is None:
                    for line in [*plan, f"Created: {destination}"]:
                        self.assert_line(result.stdout, line)
                    self.assert_created(destination)
                    shutil.rmtree(destination)
                    continue
                self.assert_line_ends(result.stderr, REFUSED + refusal)
                if steps:
                    for line in plan:
                        self.assert_line(result.stdout, line)
                else:
                    self.assertNotIn("Create:", result.stdout)
                self.assertFalse(destination.exists())
        self.assertIsNone(self.shape_record())

    def test_pty_shape_chosen_by_flag_keeps_openreposhape_confirmation(self):
        env = self.shape_env(ci=None)
        shape = ("--shape", "--org", "example", "--visibility", "private")
        preview = self.base / "Lyra"
        result = self.run_pty("new", "Lyra", *shape, "--dry-run", env=env)
        self.assert_status(result, 0)
        self.assert_not_asked(result)
        self.assert_line(result.stdout, f"Create: {preview}")
        self.assert_line(result.stdout, "  " + shlex.join(["openRepoShape", "Lyra", "--org", "example", "--visibility",
                                                           "private", "--into", str(self.base)]))
        self.assertIsNone(self.shape_record())
        self.assertFalse(preview.exists())
        self.assertNotIn("warning:", result.stdout + result.stderr)
        for name, extra in (("Atlas", ()), ("Orion", ("--yes",))):
            destination = self.base / name
            with self.subTest(name=name, flags=" ".join(shape + extra)):
                result = self.run_pty("new", name, *shape, *extra, env=env, steps=[(FAKE_SHAPE_PROMPT, "yes")])
                self.assert_status(result, 0)
                self.assert_not_asked(result)
                self.assertTrue(destination.is_dir())
                self.assertEqual(self.shape_record()[-1],
                                 [name, "--org", "example", "--visibility", "private", "--into", str(self.base)])
                self.assert_in_order(result.stdout, f"Create: {destination}", FAKE_SHAPE_PROMPT, f"Created: {destination}")
                self.assertNotIn("warning:", result.stdout + result.stderr)
        with self.subTest(name="my-app", flags=" ".join(shape)):
            result = self.run_pty("new", "my-app", *shape, env=env, steps=[(FAKE_SHAPE_PROMPT, "no")])
            self.assert_status(result, 1)
            self.assert_not_asked(result)
            self.assertNotIn(OBSTACLE_LINE_START, result.stdout + result.stderr)
            self.assertEqual(self.shape_record()[-1],
                             ["my-app", "--org", "example", "--visibility", "private", "--into", str(self.base)])
            self.assert_line(result.stdout, FAKE_SHAPE_DECLINED)
            self.assertFalse((self.base / "my-app").exists())
            self.assertNotIn("warning:", result.stdout + result.stderr)
        self.assertEqual(len(self.shape_record()), 3)
        self.assertTrue(all("--yes" not in argv for argv in self.shape_record()))

    def test_new_without_a_terminal_is_not_asked(self):
        self.env = self.question_env(None)
        destination = self.base / "MyApp"
        result = self.run_cli("new", "MyApp")
        self.assert_status(result, 2)
        self.assert_not_asked(result)
        self.assertEqual(result.stdout, f"Create: {destination}\n  "
                         + shlex.join(["bash", str(self.generator), "MyApp", str(self.base)]) + "\n")
        self.assertEqual(result.stderr, REFUSED + NOT_A_TERMINAL.format(PROMPT=CONFIRM_PROMPT) + "\n")
        self.assertFalse(destination.exists())

    def test_inproc_stdout_not_a_terminal_is_not_asked(self):
        result = self.run_inproc("new", "MyApp", ci=None, answers=["yes"], stdin_tty=True, stdout_tty=False)
        self.assert_status(result, 0)
        self.assert_not_asked(result)
        self.assertEqual(result.prompts, [CONFIRM_PROMPT + " "])
        self.assertEqual(result.stdout, self.creation_stdout("MyApp"))
        self.assertEqual(result.stderr, "\n".join(self.advisory("MyApp")) + "\n")
        self.assert_created(self.base / "MyApp")

    def test_pty_ci_decides_the_question(self):
        for ci in ("true", "1", "yes", " TRUE "):
            with self.subTest(CI=ci):
                result = self.run_pty("new", "MyApp", env=self.question_env(ci), steps=[(CONFIRM_PROMPT, "no")])
                self.assert_status(result, 2)
                self.assert_not_asked(result)
                self.assert_line_ends(result.stderr, REFUSED + DECLINED)
        for ci in ("", "0", "false", "no", " FALSE ", " No "):
            with self.subTest(CI=ci):
                result = self.run_pty("new", "MyApp", env=self.question_env(ci), steps=[(QUESTION_PROMPT, PTY_EOF)])
                self.assert_status(result, 2)
                self.assert_line(result.stdout, QUESTION_HEADER.format(NAME="MyApp"))
                self.assert_line_ends(result.stderr, REFUSED + QUESTION_ENDED)
        self.assertFalse((self.base / "MyApp").exists())

    def test_advisory_after_a_flag_chosen_single_repository(self):
        self.env = self.question_env("true")
        destination = self.base / "Flagged"
        result = self.run_cli("new", "Flagged", "--type", "test", "--yes")
        self.assert_status(result, 0)
        self.assertEqual(result.stdout, self.creation_stdout("Flagged"))
        self.assertEqual(result.stderr, "\n".join(self.advisory("Flagged")) + "\n")
        self.assert_created(destination)
        self.assertFalse((destination / ".git").exists())

    def test_pty_advisory_where_ci_is_true(self):
        destination = self.base / "CiApp"
        result = self.run_pty("new", "CiApp", env=self.question_env("true"), steps=[(CONFIRM_PROMPT, "yes")])
        self.assert_status(result, 0)
        self.assert_not_asked(result)
        first, second = self.advisory("CiApp")
        self.assertNotIn("warning:", result.seen[0])
        self.assert_line_ends(result.stderr, first)
        self.assert_line(result.stderr, second)
        self.assert_in_order(result.stderr, first, second)
        self.assertNotIn("warning:", result.stdout)
        self.assert_line(result.stdout, f"Created: {destination}")
        self.assert_created(destination)

    def test_advisory_content(self):
        for line in (ADVISORY_PREFERENCE, ADVISORY_CONVERSION):
            self.assertTrue(line.startswith("warning:"), line)
            self.assertTrue(line.isascii(), line)
        for term in ("preferred, not required", "elective", "confers nothing"):
            self.assertIn(term, ADVISORY_PREFERENCE)
        for term in ("adopt-project.py", "a person deciding for this project", "single-repository.yaml",
                     "Nothing here changes"):
            self.assertIn(term, ADVISORY_CONVERSION)
        self.env = self.question_env("true")
        result = self.run_cli("new", "Flagged", "--type", "test", "--yes")
        self.assert_status(result, 0)
        self.assertTrue(result.stderr.isascii())
        self.assertEqual(result.stderr.splitlines(), self.advisory("Flagged"))

    def test_advisory_silent_cases(self):
        self.env = self.shape_env(ci=None)
        with self.subTest("--dry-run"):
            result = self.run_cli("new", "Dry", "--type", "test", "--dry-run")
            self.assert_status(result, 0)
            self.assertEqual(result.stdout, f"Create: {self.base / 'Dry'}\n  "
                             + shlex.join(["bash", str(self.generator), "Dry", str(self.base)]) + "\n")
            self.assertEqual(result.stderr, "")
        with self.subTest("--shape through the fake"):
            result = self.run_cli_streams("new", "Shaped", "--shape", "--org", "example", "--visibility", "private",
                                          stdin="yes\n")
            self.assert_status(result, 0)
            self.assertTrue((self.base / "Shaped").is_dir())
            self.assertEqual(self.shape_record(),
                             [["Shaped", "--org", "example", "--visibility", "private", "--into", str(self.base)]])
            self.assertNotIn("warning:", result.stdout + result.stderr)
        with self.subTest("generator exits 17"):
            self.generator.write_text("#!/bin/bash\nexit 17\n")
            result = self.run_cli("new", "Failed", "--type", "test", "--yes")
            self.assert_status(result, 17)
            self.assertNotIn("warning:", result.stdout + result.stderr)
            self.assertFalse((self.base / "Failed").exists())
        with self.subTest("generator creates nothing"):
            self.generator.write_text("#!/bin/bash\nexit 0\n")
            result = self.run_cli("new", "Empty", "--type", "test", "--yes")
            self.assert_status(result, 2)
            self.assertEqual(result.stderr, REFUSED + NOT_CREATED.format(PATH=self.base / "Empty") + "\n")
            self.assertNotIn("warning:", result.stdout)

    def test_advisory_with_stderr_closed(self):
        self.env = self.question_env(None)
        result = self.run_cli_streams("new", "Closed", "--type", "test", "--yes",
                                      prefix=("/bin/sh", "-c", 'exec "$@" 2>&-', "sh"))
        self.assert_advised_run_unharmed(result, "Closed")

    def test_advisory_with_stderr_on_dev_full(self):
        if not os.path.exists("/dev/full"):
            self.skipTest("/dev/full does not exist here; the closed-pipe test covers the guard")
        self.env = self.question_env(None)
        with open("/dev/full", "w") as full:
            result = self.run_cli_streams("new", "Full", "--type", "test", "--yes", stderr=full)
        self.assert_advised_run_unharmed(result, "Full")

    def test_advisory_with_stderr_on_a_closed_pipe(self):
        self.env = self.question_env(None)
        read_end, write_end = os.pipe()
        os.close(read_end)
        try:
            result = self.run_cli_streams("new", "Broken", "--type", "test", "--yes", stderr=write_end)
        finally:
            os.close(write_end)
        self.assert_advised_run_unharmed(result, "Broken")

    def test_advisory_is_never_a_report_input(self):
        self.env = self.question_env(None)
        parents = {"advised": self.base / "advised", "asked": self.base / "asked"}
        for parent in parents.values():
            parent.mkdir()
        advised = self.run_cli("new", "Same", "--into", parents["advised"], "--type", "test", "--yes")
        self.assert_status(advised, 0)
        self.assertEqual(advised.stderr, "\n".join(self.advisory("Same")) + "\n")
        asked = self.run_pty("new", "Same", "--into", parents["asked"], env=self.env,
                             steps=[(QUESTION_PROMPT, "2"), (CONFIRM_PROMPT, "yes")])
        self.assert_status(asked, 0)
        self.assertNotIn("warning:", asked.stdout + asked.stderr)
        roots = {label: parent / "Same" for label, parent in parents.items()}
        for label, root in roots.items():
            with self.subTest(files=label):
                self.assert_created(root)
        for command in (("status",), ("status", "--json"), ("doctor",), ("doctor", "--json")):
            with self.subTest(report=" ".join(command)):
                reports = []
                for root in roots.values():
                    result = self.run_cli(command[0], root, *command[1:])
                    reports.append((result.returncode, result.stdout.replace(str(root), "ROOT"),
                                    result.stderr.replace(str(root), "ROOT")))
                self.assertEqual(reports[0], reports[1])
                for text in ("adopt-project.py", "single-repository.yaml", "preferred, not required"):
                    self.assertNotIn(text, reports[0][1] + reports[0][2])

    def test_pty_workspace_name_is_not_asked_or_advised(self):
        destination = self.base / "alice-wip"
        result = self.run_pty("new", "alice-wip", env=self.question_env(None), steps=[(CONFIRM_PROMPT, "yes")])
        self.assert_status(result, 0)
        self.assert_not_asked(result)
        plan = self.creation_stdout("alice-wip").splitlines()
        for line in plan:
            self.assert_line(result.stdout, line)
        self.assert_in_order(result.stdout, *plan)
        self.assertNotIn("warning:", result.stdout + result.stderr)
        self.assert_created(destination)

    def test_workspace_name_by_flag_gives_no_advisory(self):
        self.env = self.question_env(None)
        result = self.run_cli("new", "alice-wip", "--type", "test", "--yes")
        self.assert_status(result, 0)
        self.assertEqual(result.stdout, self.creation_stdout("alice-wip"))
        self.assertEqual(result.stderr, "")
        self.assert_created(self.base / "alice-wip")

    def test_workflow_advisory_precedes_the_follow_up(self):
        self.env = self.question_env(None)
        self.write_fake_setup_openspeckit()
        self.assert_fake_on_path(self.env, "setup-openspeckit")
        destination = self.base / "Flow"
        result = self.run_cli_streams("new", "Flow", "--type", "test", "--yes", "--workflow", stderr=subprocess.STDOUT)
        self.assert_status(result, 0)
        merged = result.stdout
        first, second = self.advisory("Flow")
        marker = f"FOLLOWUP --repo {destination}"
        for line in (first, second, marker):
            self.assert_line(merged, line)
        self.assertEqual(merged.split("\n").count(marker), 2)
        self.assert_in_order(merged, first, second, marker)
        self.assertLess(merged.index(second), merged.index(marker))
        self.assert_created(destination)

    def test_workflow_follow_up_failure_keeps_the_advisory(self):
        self.env = self.question_env(None)
        for status in (3, 130):
            with self.subTest(status=status):
                self.write_fake_setup_openspeckit(status)
                self.assert_fake_on_path(self.env, "setup-openspeckit")
                name = f"Flow{status}"
                destination = self.base / name
                result = self.run_cli("new", name, "--type", "test", "--yes", "--workflow")
                self.assert_status(result, status)
                self.assertEqual(result.stderr, "\n".join([*self.advisory(name), f"FOLLOWUP --repo {destination}",
                                                           WORKFLOW_FAILED.format(PATH=destination)]) + "\n")
                self.assertNotIn("warning:", result.stdout)
                self.assertNotIn("Created:", result.stdout)
                self.assert_created(destination)

    def test_pty_single_answer_with_workflow_adds_no_advisory(self):
        env = self.question_env(None)
        self.write_fake_setup_openspeckit()
        self.assert_fake_on_path(env, "setup-openspeckit")
        destination = self.base / "Flow3"
        result = self.run_pty("new", "Flow3", "--workflow", env=env, steps=[(QUESTION_PROMPT, "2"), (CONFIRM_PROMPT, "yes")])
        self.assert_status(result, 0)
        marker = f"FOLLOWUP --repo {destination}"
        self.assert_line(result.stdout, "  " + shlex.join(["setup-openspeckit", "--repo", str(destination)]))
        self.assert_line(result.stdout, marker)
        self.assert_line_ends(result.stderr, marker)
        self.assert_in_order(result.stdout, QUESTION_HEADER.format(NAME="Flow3"), f"Create: {destination}", marker,
                             f"Created: {destination}")
        self.assertNotIn("warning:", result.stdout + result.stderr)
        self.assert_created(destination)

    def test_workflow_workspace_name_gives_no_advisory(self):
        self.env = self.question_env(None)
        self.write_fake_setup_openspeckit()
        self.assert_fake_on_path(self.env, "setup-openspeckit")
        destination = self.base / "bob-wip"
        result = self.run_cli("new", "bob-wip", "--type", "test", "--yes", "--workflow")
        self.assert_status(result, 0)
        marker = f"FOLLOWUP --repo {destination}"
        self.assert_line(result.stdout, marker)
        self.assertEqual(result.stderr, marker + "\n")
        self.assertNotIn("warning:", result.stdout + result.stderr)
        self.assert_created(destination)

    def test_pty_workflow_prerequisite_is_refused_before_the_question(self):
        env = self.question_env(None)
        self.assert_absent_from_path(env, "setup-openspeckit")
        result = self.run_pty("new", "Flow4", "--workflow", env=env)
        self.assert_status(result, 2)
        self.assert_line_ends(result.stderr, REFUSED + WORKFLOW_MISSING)
        self.assert_not_asked(result)
        self.assertNotIn("Create:", result.stdout)
        self.assertFalse((self.base / "Flow4").exists())

    def test_workflow_refusal_order_unchanged_when_not_asked(self):
        self.env = self.question_env(None)
        self.assert_absent_from_path(self.env, "setup-openspeckit")
        result = self.run_cli("new", "Flow5", "--type", "nope", "--workflow")
        self.assert_status(result, 2)
        self.assertEqual(result.stderr, REFUSED + NO_GENERATOR + "\n")
        self.assertEqual(result.stdout, "")
        self.assertFalse((self.base / "Flow5").exists())


if __name__ == "__main__":
    unittest.main()
