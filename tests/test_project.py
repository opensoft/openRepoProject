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
        answers = [(QUESTION_PROMPT, ""), (ORG_PROMPT, "example"), (VIS_PROMPT, "private")]
        destination = self.base / "Atlas"
        result = self.run_pty("new", "Atlas", env=env, steps=[*answers, (FAKE_SHAPE_PROMPT, "yes")])
        self.assert_status(result, 0)
        self.assertTrue(destination.is_dir())
        self.assertEqual(self.shape_record(),
                         [["Atlas", "--org", "example", "--visibility", "private", "--into", str(self.base)]])
        self.assert_in_order(result.stdout, RESTATED.format(NAME="Atlas", ORG="example", VIS="private"),
                             f"Create: {destination}", FAKE_SHAPE_PROMPT, f"Created: {destination}")
        self.assertNotIn("warning:", result.stdout + result.stderr)
        declined = self.run_pty("new", "Orion", env=env, steps=[*answers, (FAKE_SHAPE_PROMPT, "no")])
        self.assert_status(declined, 1)
        self.assert_line(declined.stdout, FAKE_SHAPE_DECLINED)
        self.assertFalse((self.base / "Orion").exists())
        self.assertNotIn("Created:", declined.stdout)
        self.assertEqual(self.shape_record()[-1],
                         ["Orion", "--org", "example", "--visibility", "private", "--into", str(self.base)])
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


if __name__ == "__main__":
    unittest.main()
