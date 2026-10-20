"""US9 of feature 004: status, doctor and update read repositories through the
one evidence model (T114 to T116; FR-050 to FR-053, FR-059; design D16;
research.md R2 and R4; data-model.md, "Root and leg state outside clean";
contracts/project-clean.md, "status, doctor and update").

Each scenario test is named by rule 1: the subcommand the scenario drives, then
its exact title. Values are literals written into the test (rule 11), and the
human text comes from the fixtures of tests/clean_support.py (rule 8), except
the texts that stay outside TEXT: D16's `Git: inspection-error (CODES)` line
(T119), `Cancelled.` (T035) and the baseline refusals of `update`. Fixture
setup calls the real git by its absolute path, so a counting wrapper on the
PATH of the run under test records only that run's children (rule 13).
"""
import errno
import json
import os
from pathlib import Path
import signal
import subprocess
import unittest

import clean_support

TEXT = clean_support.TEXT_FIXTURES

# The seven protocol pins and the two status pins, as the contract writes them
# (contracts/project-clean.md, "Git children").
PINS = ["-c", "protocol.allow=never", "-c", "protocol.file.allow=never",
        "-c", "protocol.ssh.allow=never", "-c", "protocol.git.allow=never",
        "-c", "protocol.http.allow=never", "-c", "protocol.https.allow=never",
        "-c", "protocol.ext.allow=never"]
STATUS_PINS = ["-c", "core.untrackedCache=false", "-c", "core.fsmonitor=false"]

# The status, doctor and update texts this change keeps or adds outside TEXT.
CANCELLED = "Cancelled."
FRESHNESS = "local refs only; no fetch"
STALE = "Review the stale worktree metadata before pruning it manually."
MISSING_CHECKOUT = "Missing checkout; use the estate's bootstrap/siblings command"
CLEAN_TRACKING = "Project updates require a clean tracking checkout; preserve feature work first."
CHILD_WORK = "Child has work to preserve: {PATH}"
NO_IDENTITY = "no GitHub repository identity to match a parked record"

# The command-neutral row texts of git-too-old and git-unavailable (lead ruling
# R-48 (b)), for the 2.35 fake and for no git on PATH.
TOO_OLD = TEXT["inspection_git_too_old"].format(VERSION="2.35.0")
NOT_FOUND = TEXT["inspection_git_unavailable"].format(DETAIL=TEXT["git_unavailable_not_found"])

# The commands status, doctor and update run, all read-only probes (D6).
READ_ONLY = {"--version", "rev-parse", "worktree", "for-each-ref", "status", "remote"}


def real_version():
    """What the real git prints after `git version `, as doctor's git row shows it."""
    output = subprocess.run([clean_support.REAL_GIT, "--version"], capture_output=True, text=True,
                            timeout=clean_support.TIMEOUT).stdout
    return output.splitlines()[0].strip().removeprefix("git version ")


def split_pins(record):
    """A counted child's argument vector as (its -c pins, the rest)."""
    argv = record.argv
    at = 0
    while at + 1 < len(argv) and argv[at] == "-c":
        at += 2
    return argv[:at], argv[at:]


def command(record):
    return split_pins(record)[1]


def subcommand(record):
    """The Git subcommand of a counted child: the word after `-C DIR`, or the
    first argument (`--version`)."""
    rest = command(record)
    return rest[2] if rest[:1] == ["-C"] else rest[0]


def git_message(subcommand_name, code, **fields):
    """A row error's message for `git SUBCOMMAND`, from the fixtures (rule 8)."""
    operation = TEXT["row_error_git_operation"].format(SUBCOMMAND=subcommand_name)
    return TEXT[code].format(OPERATION=operation, **fields)


def checks(document, level=None):
    """doctor's check rows, all of them or those of one level."""
    return [row for row in document["checks"] if level is None or row["level"] == level]


def git_row(document):
    rows = [row for row in document["checks"] if row["check"] == "git"]
    assert len(rows) == 1, rows
    return rows[0]


def walk(value):
    """Every dict nested anywhere in a JSON document, the document included."""
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk(item)


class StatusDoctorUpdateTests(clean_support.CleanCase):

    def counted(self, *args, real=None, env=None, cwd=None, timing=None):
        """`project ARGS...` with the counting wrapper first on PATH, in front of
        real (REAL_GIT, or a fake), through the launcher when timing is given.
        Returns the run, with its parsed document as `document` (None when it
        printed none) and the wrapper's path as `wrapper`, and the children."""
        bin_dir = self.base / "counting-bin"
        log = self.base / "children.log"
        wrapper = clean_support.install_counting_git(bin_dir, log, real=real or clean_support.REAL_GIT)
        clean_support.reset_child_log(log)
        env = self.path_first(bin_dir, env)
        if timing is None:
            result = self.run_cli(*args, env=env, cwd=cwd)
        else:
            result = self.run_launched(timing, *args, env=env, cwd=cwd)
        try:
            result.document = json.loads(result.stdout)
        except ValueError:
            result.document = None
        result.wrapper = str(wrapper)
        return result, clean_support.child_log(log)

    def fake_bin(self):
        path = self.base / "fake-bin"
        path.mkdir(exist_ok=True)
        return path

    def recording_tool(self, path, status=0):
        """A script at path that appends its argument vector, one JSON line, to
        PATH.runs and exits with status: a fake owner tool or delegate."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        record = str(path) + ".runs"
        path.write_text("#!/bin/sh\n"
                        f"printf '%s\\n' \"$*\" >> '{record}'\n"
                        f"exit {status}\n")
        path.chmod(0o755)
        return Path(record)

    def recording_script(self, path):
        """A Python script at path, as `update --component shape` runs its
        update-shape.py, that appends its arguments, one line, to PATH.runs."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        record = Path(str(path) + ".runs")
        path.write_text("import sys\n"
                        f"with open({str(record)!r}, 'a') as stream:\n"
                        "    stream.write(' '.join(sys.argv[1:]) + '\\n')\n")
        return record

    def assert_one_document(self, result):
        self.assertIsNotNone(result.document, clean_support.transcript(result))
        return result.document

    def project(self, name, legs):
        """A repository self.base/NAME holding a project manifest that declares
        legs, each (role, relative path)."""
        root = self.repo(name)
        lines = "".join(f"  - {{role: {role}, path: {path}}}\n" for role, path in legs)
        (root / "project.yaml").write_text("kind: project-manifest\nlegs:\n" + lines)
        return root

    # T114: Git older than 2.36, no git, and the components that need no Git.

    def test_status_git_older_than_2_36_in_status_and_doctor(self):
        # FR-050, FR-053, research.md R2: the 2.35 fake behind the counting
        # wrapper. A workspace is configured, so handoff() reaches its remote
        # lookup, which must spawn nothing once the version check has failed
        # (plan review M10; lead ruling R-56).
        root = self.project("Atlas", [("spec", "spec")])
        (root / "spec").mkdir()  # a leg directory with no .git
        workspace = self.base / "workspace"
        workspace.mkdir()
        env = dict(self.env, SPECKIT_WORKSPACE_PATH=str(workspace))
        fake = clean_support.install_fake_git(self.base / "fake", "version-2.35.0")
        repository = {"path": str(root), "path_valid_utf8": True, "present": None, "branch": None,
                      "head": None, "dirty": None, "upstream": None, "ahead": None, "behind": None,
                      "tracking_freshness": FRESHNESS, "worktrees": None, "classification": "inspection-error",
                      "errors": [{"code": "git-too-old", "message": TOO_OLD}]}
        leg = {"role": "spec", "tracking_branch": "main", "path": str(root / "spec"),
               "path_valid_utf8": True, "present": False}
        for name, code in (("status", 0), ("doctor", 1)):
            with self.subTest(command=name, output="json"):
                result, records = self.counted(name, root, "--json", real=fake, env=env)
                self.assert_status(result, code)
                document = self.assert_one_document(result)
                self.assertEqual(document["repository"], repository)
                self.assertEqual(document["children"], [leg])
                self.assertEqual(document["handoff"], {"state": NO_IDENTITY})
                self.assertEqual([command(record) for record in records], [["--version"]],
                                 "git --version alone; handoff()'s remote get-url never spawned")
                if name == "doctor":
                    self.assertEqual(git_row(document), {"level": "error", "check": "git",
                                                         "detail": "git-too-old: " + TOO_OLD})
                    self.assertTrue(git_row(document)["detail"].startswith("git-too-old: "))
                    self.assertIn({"level": "error", "check": str(root),
                                   "detail": "inspection-error (git-too-old): " + TOO_OLD}, checks(document))
            with self.subTest(command=name, output="human"):
                result, records = self.counted(name, root, real=fake, env=env)
                self.assert_status(result, code)
                self.assertIn("  Git: inspection-error (git-too-old)\n", result.stdout)
                self.assertNotIn("REFUSED", result.stderr)
                self.assertEqual([command(record) for record in records], [["--version"]])
                if name == "doctor":
                    self.assertIn("ERROR git: git-too-old: " + TOO_OLD + "\n", result.stdout)

        with self.subTest("a directory with no .git needs no version check"):
            # No workspace here: handoff() would otherwise look up the remote of
            # a root that holds no repository, a child git() runs unchecked.
            plain = self.base / "Plain"
            plain.mkdir()
            (plain / "project.yaml").write_text("kind: project-manifest\nlegs: []\n")
            env = self.env
            result, records = self.counted("status", plain, "--json", real=fake, env=env)
            self.assert_status(result, 0)
            self.assertEqual(self.assert_one_document(result)["repository"],
                             {"path": str(plain), "path_valid_utf8": True, "present": False})
            self.assertEqual(records, [], "status never runs the version check by itself")
            result, records = self.counted("doctor", plain, "--json", real=fake, env=env)
            self.assert_status(result, 1)
            self.assertEqual(git_row(self.assert_one_document(result)),
                             {"level": "error", "check": "git", "detail": "git-too-old: " + TOO_OLD})
            self.assertEqual([command(record) for record in records], [["--version"]],
                             "doctor's git row runs the memoized version check itself")

    def test_doctor_no_git_on_path(self):
        # Research.md R2: with no git, discover() finds the root by the nearest
        # .git entry, and doctor reports git-unavailable as an error row.
        root = self.repo()
        env = dict(self.env, PATH=self.path_without_git())
        result = self.run_json("doctor", root, "--json", env=env)
        self.assert_status(result, 1)
        self.assertEqual(git_row(result.document),
                         {"level": "error", "check": "git", "detail": "git-unavailable: " + NOT_FOUND})
        self.assertTrue(git_row(result.document)["detail"].startswith("git-unavailable: "))
        repository = result.document["repository"]
        self.assertEqual((repository["present"], repository["classification"], repository["errors"]),
                         (None, "inspection-error", [{"code": "git-unavailable", "message": NOT_FOUND}]))
        result = self.run_cli("doctor", root, env=env)
        self.assert_status(result, 1)
        self.assertIn("\nERROR git: git-unavailable: " + NOT_FOUND + "\n", result.stdout)
        result = self.run_json("status", root, "--json", env=env)
        self.assert_status(result, 0)
        self.assertEqual(result.document["repository"]["errors"],
                         [{"code": "git-unavailable", "message": NOT_FOUND}])

    def test_update_tools_and_workflow_need_no_git(self):
        # FR-052: the 2.35 fake first on PATH; neither component is refused for
        # Git's version, and each runs its command as before.
        root = self.repo()
        bin_dir = self.fake_bin()
        clean_support.install_fake_git(bin_dir, "version-2.35.0")
        workflow = self.recording_tool(bin_dir / "setup-openspeckit")
        tools = self.recording_tool(self.wb / "setup-script")
        (self.wb / "setup.sh").write_text(f"#!/bin/bash\nexec '{self.wb / 'setup-script'}' \"$@\"\n")
        env = self.path_first(bin_dir)
        result = self.run_cli("update", root, "--apply", "--component", "workflow", "--yes", env=env)
        self.assert_status(result, 0)
        self.assertEqual(workflow.read_text(), f"--repo {root}\n")
        result = self.run_cli("update", root, "--apply", "--component", "tools", "--yes", env=env)
        self.assert_status(result, 0)
        self.assertEqual(tools.read_text(), "\n")
        self.assertNotIn("REFUSED", result.stderr)


if __name__ == "__main__":
    unittest.main()
