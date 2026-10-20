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

    def test_clean_git_older_than_2_36(self):
        # FR-002, research.md R2; it pins T048 (require_git()). Every clean
        # mode refuses with git-too-old, exit 2, before any repository probe:
        # its only child is `git --version`, and nothing is removed.
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-merged")
        fake = clean_support.install_fake_git(self.base / "fake", "version-2.35.0")
        refusal = TEXT["git_too_old"].format(VERSION="2.35.0")
        modes = (
            ("report", ()),
            ("all-safe preview", ("--all-safe",)),
            ("all-safe apply", ("--all-safe", "--apply", "--yes")),
            ("single remove", ("--apply", "--action", "remove", "--worktree", tree, "--yes")),
            ("push", ("--apply", "--action", "push", "--branch", "001-merged", "--yes")),
            ("delete-branch", ("--apply", "--action", "delete-branch", "--branch", "001-merged", "--yes")),
        )
        for label, extra in modes:
            with self.subTest(mode=label):
                result, records = self.counted("clean", root, *extra, real=fake)
                self.assert_status(result, 2)
                self.assertEqual(result.stderr, "REFUSED: " + refusal + "\n")
                self.assertEqual([command(record) for record in records], [["--version"]])
                self.assertTrue(tree.is_dir(), "nothing was removed")
        for label, extra in (("report", ()), ("all-safe preview", ("--all-safe",)),
                             ("all-safe apply", ("--all-safe", "--apply", "--yes"))):
            with self.subTest(mode=label, output="json"):
                result, records = self.counted("clean", root, *extra, "--json", real=fake)
                self.assert_status(result, 2)
                document = self.assert_one_document(result)
                self.assertEqual([document[key] for key in ("error", "code", "completeness", "apply_allowed")],
                                 [refusal, "git-too-old", "incomplete", False])
                self.assertEqual(document["refusals"], [{"code": "git-too-old", "message": refusal}])
                self.assertEqual([command(record) for record in records], [["--version"]])
        with self.subTest("no git on PATH"):
            env = dict(self.env, PATH=self.path_without_git())
            unavailable = TEXT["git_unavailable"].format(DETAIL=TEXT["git_unavailable_not_found"])
            result = self.run_cli("clean", root, env=env)
            self.assert_status(result, 2)
            self.assertEqual(result.stderr, "REFUSED: " + unavailable + "\n")
            result = self.run_json("clean", root, "--json", env=env)
            self.assert_status(result, 2)
            self.assertEqual([result.document[key] for key in ("error", "code")],
                             [unavailable, "git-unavailable"])
            self.assertTrue(tree.is_dir())

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

    # T115: the evidence model's rows in status, doctor and update.

    def test_status_a_failed_root_status_is_reported(self):
        # FR-050, FR-051: a failed root status probe is a row-level
        # inspection-error, never a refusal with exit 2.
        root = self.repo()
        head = self.git(root, "rev-parse", "HEAD").strip()
        fake_dir = self.base / "fake"
        clean_support.install_fake_git(fake_dir, "status-fails-in", path=root)
        env = self.path_first(fake_dir)
        message = git_message("status", "row_error_probe_failed",
                              DETAIL=TEXT["row_error_probe_failed_exit"].format(N=128))
        errors = [{"code": "probe-failed", "message": message}]
        for name, code in (("status", 0), ("doctor", 1)):
            with self.subTest(command=name):
                result = self.run_json(name, root, "--json", env=env)
                self.assert_status(result, code)
                repository = result.document["repository"]
                self.assertEqual([repository[key] for key in ("present", "branch", "head", "dirty",
                                                              "classification", "errors")],
                                 [True, "main", head, None, "inspection-error", errors])
                self.assertEqual(repository["worktrees"],
                                 [{"path": str(root), "path_valid_utf8": True, "present": True, "head": head,
                                   "branch": "main", "dirty": None, "ignored_files": None, "current": False,
                                   "upstream": None, "ahead": None, "behind": None,
                                   "classification": "inspection-error", "errors": errors}])
                if name == "doctor":
                    self.assertEqual(checks(result.document, "error"),
                                     [{"level": "error", "check": str(root),
                                       "detail": "inspection-error (probe-failed): " + message}])
        result = self.run_cli("status", root, env=env)
        self.assert_status(result, 0)
        self.assertIn("  Git: inspection-error (probe-failed)\n", result.stdout)

    def test_doctor_not_established_is_an_error_none_is_not(self):
        # FR-051, analyze M4: a null that means "none" is no error; a null that
        # means "not established" is.
        with self.subTest("a fresh project with no remote passes"):
            root = self.repo("Fresh")
            result, records = self.counted("doctor", root, "--json")
            self.assert_status(result, 0)
            repository = self.assert_one_document(result)["repository"]
            self.assertEqual([repository[key] for key in ("present", "upstream", "ahead", "behind", "dirty")],
                             [True, None, None, None, False])
            self.assertNotIn("classification", repository)
            self.assertEqual(checks(result.document, "error"), [])
            # Rule 13: the git row names the counting wrapper, the git on PATH.
            self.assertEqual(git_row(result.document),
                             {"level": "ok", "check": "git", "detail": f"{result.wrapper} (git version {real_version()})"})

        with self.subTest("a leg whose status probe fails"):
            root = self.project("Atlas", [("spec", "spec")])
            leg = self.repo("Atlas/spec")
            fake_dir = self.base / "fake"
            fake = clean_support.install_fake_git(fake_dir, "status-fails-in", path=leg)
            result, records = self.counted("doctor", root, "--json", real=fake)
            self.assert_status(result, 1)
            child = self.assert_one_document(result)["children"][0]
            message = git_message("status", "row_error_probe_failed",
                                  DETAIL=TEXT["row_error_probe_failed_exit"].format(N=128))
            self.assertEqual([child[key] for key in ("present", "dirty", "classification", "errors")],
                             [True, None, "inspection-error", [{"code": "probe-failed", "message": message}]])
            self.assertEqual(checks(result.document, "error"),
                             [{"level": "error", "check": str(leg),
                               "detail": "inspection-error (probe-failed): " + message}])

        with self.subTest("a leg whose parent denies search"):
            if hasattr(os, "geteuid") and os.geteuid() == 0:
                self.skipTest("permission fixtures do not bind the superuser (effective uid 0)")
            root = self.project("Locked", [("spec", "locked/spec")])
            (root / ".gitignore").write_text("locked/\n")
            leg = self.repo("Locked/locked/spec")
            (root / "locked").chmod(0o600)
            self.addCleanup((root / "locked").chmod, 0o700)
            result = self.run_json("doctor", root, "--json")
            self.assert_status(result, 1)
            child = result.document["children"][0]
            message = TEXT["row_error_os_error"].format(OPERATION="lstat", STRERROR=os.strerror(errno.EACCES))
            self.assertEqual([child[key] for key in ("path", "present", "dirty", "classification", "errors")],
                             [str(leg), None, None, "inspection-error", [{"code": "os-error", "message": message}]])
            self.assertEqual(checks(result.document, "error"),
                             [{"level": "error", "check": str(leg),
                               "detail": "inspection-error (os-error): " + message}])

    @clean_support.linux_paths
    def test_status_json_paths_carry_their_flags(self):
        # FR-051, analyze M4, lead ruling R-9: `path_valid_utf8` beside every
        # path, `root_valid_utf8` beside every root, and ignored samples as
        # objects, in status and doctor JSON alike.
        holder = self.repo("Family/Family")
        (holder / "family.yaml").write_text("kind: family-manifest\nmembers:\n  - project: Atlas\n"
                                            "  - project: Ghost\n")
        member = self.project("Family/Atlas", [("spec", "spec")])
        self.repo("Family/Atlas/spec")
        (member / ".gitignore").write_text("local.env\nspec/\n")
        self.commit(member)
        feature = self.base / "feature-tree"
        self.git(member, "worktree", "add", "-b", "001-feature", feature)
        (feature / "local.env").write_text("preserve")
        odd = os.fsencode(self.base) + b"/odd-\xff-tree"
        self.git(member, "worktree", "add", "-b", "002-odd", odd)
        for name in ("status", "doctor"):
            with self.subTest(command=name):
                result = self.run_json(name, holder, "--json")
                found = list(walk(result.document))
                paths = [item for item in found if "path" in item]
                roots = [item for item in found if "root" in item]
                self.assertGreaterEqual(len(paths), 6)
                for item in paths:
                    self.assertIsInstance(item.get("path_valid_utf8"), bool, item)
                self.assertEqual([(item["root"], item["root_valid_utf8"]) for item in roots],
                                 [(str(holder), True), (str(member), True)])
                atlas = result.document["children"][0]
                ghost = result.document["children"][1]
                self.assertEqual(ghost, {"role": "member", "path": str(self.base / "Family/Ghost"),
                                         "path_valid_utf8": True, "present": False})
                trees = {Path(tree["path"]).name: tree for tree in atlas["repository"]["worktrees"]}
                self.assertEqual(trees["feature-tree"]["ignored_samples"],
                                 [{"path": "local.env", "path_valid_utf8": True}])
                self.assertEqual(trees["Atlas"]["ignored_samples"],
                                 [{"path": "spec/", "path_valid_utf8": True}])
                self.assertEqual((trees["odd-\\xff-tree"]["path"], trees["odd-\\xff-tree"]["path_valid_utf8"]),
                                 (f"{self.base}/odd-\\xff-tree", False))
                for tree in trees.values():
                    for sample in tree["ignored_samples"]:
                        self.assertEqual(list(sample), ["path", "path_valid_utf8"])

    def test_status_sigterm_during_inspection(self):
        # FR-058, analyze M5, research.md R4. Launcher, its own table (R-29): a
        # 10 s probe budget for status (so the signal, not the budget, stops the
        # probe), a grace of 0.5 s and a reap wait of 0.5 s; every other value
        # real. The ignore-sigterm fake is the root's status probe.
        table = clean_support.timing_table(inspect_budget=10.0, term_grace=0.5, reap_wait=0.5)
        root = self.repo()
        fake_dir = self.base / "fake"
        clean_support.install_fake_git(fake_dir, "ignore-sigterm")
        env = self.path_first(fake_dir)
        events = fake_dir / clean_support.FAKE_EVENTS
        for signum, code in ((signal.SIGTERM, 143), (signal.SIGHUP, 129)):
            with self.subTest(signal=signum.name):
                if events.exists():
                    events.unlink()
                child = subprocess.Popen(clean_support.launched_argv(table, "status", root, "--json"),
                                         cwd=self.base, env=env, stdin=subprocess.DEVNULL,
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                         start_new_session=True)
                try:
                    ready = clean_support.wait_for_event(fake_dir, "ready", timeout=10)
                    self.assertIsNotNone(ready, "the fake status probe started")
                    child.send_signal(signum)
                    out, err = child.communicate(timeout=clean_support.TIMEOUT)
                finally:
                    if child.poll() is None:
                        os.killpg(child.pid, signal.SIGKILL)
                        child.communicate()
                self.assertEqual(child.returncode, code, err)
                self.assertEqual((out, err), ("", CANCELLED + "\n"))
                term = clean_support.wait_for_event(fake_dir, "term", pid=ready["pid"])
                death = clean_support.wait_for_event(fake_dir, "death", pid=ready["pid"])
                self.assertIsNotNone(term, "the probe's group got SIGTERM")
                self.assertIsNotNone(death, "the probe was killed")
                self.assertGreaterEqual(death["t"] - term["t"], 0.9 * table["term_grace"])
                with self.assertRaises(ProcessLookupError):
                    os.killpg(ready["pgid"], 0)

    def test_status_a_deleted_upstream_in_status_and_doctor(self):
        # FR-051, FR-056: an upstream whose remote-tracking ref was deleted keeps
        # its configured short name, with ahead and behind null.
        root = self.repo()
        self.bare_remote()
        self.git(root, "push", "-q", "-u", "origin", "main")
        tree = self.base / "gone-tree"
        self.git(root, "worktree", "add", "-b", "001-gone", tree)
        self.git(tree, "push", "-q", "-u", "origin", "001-gone")
        for branch in ("main", "001-gone"):
            self.git(root, "update-ref", "-d", f"refs/remotes/origin/{branch}")
        for name in ("status", "doctor"):
            with self.subTest(command=name):
                result = self.run_json(name, root, "--json")
                self.assert_status(result, 0)
                repository = result.document["repository"]
                self.assertEqual([repository[key] for key in ("upstream", "ahead", "behind")],
                                 ["origin/main", None, None])
                self.assertNotIn("classification", repository)
                gone = {Path(item["path"]).name: item for item in repository["worktrees"]}["gone-tree"]
                self.assertEqual([gone[key] for key in ("upstream", "ahead", "behind")],
                                 ["origin/001-gone", None, None])
                if name == "doctor":
                    self.assertEqual(checks(result.document, "error"), [])
                result = self.run_json(name, tree, "--json")
                self.assert_status(result, 0)
                self.assertEqual([result.document["repository"][key] for key in ("branch", "upstream", "ahead",
                                                                                 "behind")],
                                 ["001-gone", "origin/001-gone", None, None])

    def test_update_a_leg_s_probe_times_out(self):
        # D-R, FR-052. Launcher, its own table (R-29): status, doctor and update
        # give each Git child the inspect budget, here 1 s, with a grace of
        # 0.5 s and a reap wait of 0.5 s; every other value real. The leg's
        # status probe hangs, so its dirty is null and the update refuses.
        table = clean_support.timing_table(inspect_budget=1.0, term_grace=0.5, reap_wait=0.5)
        root = self.project("Atlas", [("spec", "spec")])
        leg = self.repo("Atlas/spec")
        self.commit(root)  # the manifest, and the leg as a gitlink: a clean root
        shape = self.base / "shape"
        runs = self.recording_script(shape / "update-shape.py")
        fake_dir = self.base / "fake"
        clean_support.install_fake_git(fake_dir, "status-hangs-in", path=leg)
        result = self.run_launched(table, "update", root, "--apply", "--component", "shape",
                                   "--shape-source", shape, "--at", "a" * 40, "--yes",
                                   env=self.path_first(fake_dir))
        self.assert_status(result, 2)
        self.assertEqual(result.stderr, "REFUSED: " + CHILD_WORK.format(PATH=leg) + "\n")
        self.assertFalse(runs.exists(), "the owner tool was never invoked")

    def test_status_a_submodule_checkout_is_reported(self):
        # FR-055, analyze H4, lead ruling R-42: status and doctor report what
        # clean refuses, a submodule's checkout and a linked worktree of a bare
        # repository, and never refuse.
        superproject = self.repo("super")
        sub = self.submodule(superproject)
        self.commit(superproject)
        sub_head = self.git(sub, "rev-parse", "HEAD").strip()
        seed = self.repo("seed")
        seed_head = self.git(seed, "rev-parse", "HEAD").strip()
        bare = self.base / "bare.git"
        self.git(self.base, "init", "-q", "--bare", bare)
        self.git(seed, "push", "-q", bare, "main")
        linked = self.base / "linked"
        self.git(bare, "worktree", "add", "-q", "-b", "001-linked", linked, "main")
        cases = (
            ("submodule", sub, {"present": True, "branch": "main", "head": sub_head, "dirty": False,
                                "upstream": "origin/main", "ahead": 0, "behind": 0}, [str(sub)], 0),
            ("bare", linked, {"present": True, "branch": "001-linked", "head": seed_head, "dirty": False,
                              "upstream": None, "ahead": None, "behind": None}, [str(linked)], 0),
        )
        for label, path, values, trees, doctor_code in cases:
            for name, code in (("status", 0), ("doctor", doctor_code)):
                with self.subTest(case=label, command=name):
                    result = self.run_json(name, path, "--json")
                    self.assert_status(result, code)
                    repository = result.document["repository"]
                    self.assertEqual({key: repository[key] for key in values}, values)
                    self.assertNotIn("classification", repository)
                    self.assertEqual([tree["path"] for tree in repository["worktrees"]], trees)

    # T116: the pinned status configuration, a missing leg, the default report.

    def test_status_the_pinned_status_configuration(self):
        # Rule 1, plan review M14, FR-054: core.untrackedCache and core.fsmonitor
        # true in the GIT_CONFIG_GLOBAL file; every status child carries the two
        # status pins before the seven protocol pins. It pins Phase 2.
        config = self.base / "user.gitconfig"
        config.write_text("[core]\n\tuntrackedCache = true\n\tfsmonitor = true\n")
        root = self.repo()
        tree = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-b", "001-feature", tree)
        env = dict(self.env, GIT_CONFIG_GLOBAL=str(config))
        for name in ("status", "doctor"):
            with self.subTest(command=name):
                result, records = self.counted(name, root, "--json", env=env)
                self.assert_status(result, 0)
                statuses = [record for record in records if subcommand(record) == "status"]
                self.assertEqual(sorted(command(record)[1] for record in statuses), sorted([str(root), str(tree)]))
                for record in statuses:
                    self.assertEqual(split_pins(record)[0], STATUS_PINS + PINS)
                for record in records:
                    self.assertEqual(split_pins(record)[0][-len(PINS):], PINS)

        with self.subTest("every removal child of an apply (pins T056)"):
            self.bare_remote()
            merged = self.merged_worktree("002-merged")
            result, records = self.counted("clean", root, "--all-safe", "--apply", "--yes", env=env)
            self.assert_status(result, 0)
            self.assertFalse(merged.exists())
            removals = [record for record in records if command(record)[2:4] == ["worktree", "remove"]]
            self.assertEqual([command(record)[1:] for record in removals],
                             [[str(root), "worktree", "remove", str(merged)]])
            for record in removals:
                self.assertEqual(split_pins(record)[0],
                                 ["-c", "status.showUntrackedFiles=normal"] + STATUS_PINS + PINS)
            statuses = [record for record in records if subcommand(record) == "status"]
            self.assertTrue(statuses)
            for record in statuses:
                self.assertEqual(split_pins(record)[0], STATUS_PINS + PINS)

    def test_doctor_missing_leg(self):
        # project-command "Inspect and diagnose": a declared leg with no checkout
        # is an actionable failure with a nonzero exit.
        root = self.project("Atlas", [("spec", "spec")])
        leg = root / "spec"
        result = self.run_json("doctor", root, "--json")
        self.assert_status(result, 1)
        self.assertEqual(result.document["children"],
                         [{"role": "spec", "tracking_branch": "main", "path": str(leg),
                           "path_valid_utf8": True, "present": False}])
        self.assertIn({"level": "error", "check": str(leg), "detail": MISSING_CHECKOUT},
                      checks(result.document, "error"))
        result = self.run_cli("doctor", root)
        self.assert_status(result, 1)
        self.assertIn(f"ERROR {leg}: {MISSING_CHECKOUT}\n", result.stdout)

    def test_update_default_report(self):
        # project-command "Explicit maintenance": without --apply, update reports
        # its plan, runs only read-only probes, and installs nothing.
        root = self.repo()
        bin_dir = self.fake_bin()
        workflow = self.recording_tool(bin_dir / "setup-openspeckit")
        shape = self.recording_tool(bin_dir / "openRepoShape")
        tools = self.recording_tool(self.wb / "setup.sh")
        before = self.git(root, "status", "--porcelain", "--ignored")
        for args in ((root, "--json"), (root,), (root, "--component", "workflow", "--json")):
            with self.subTest(args=args[1:]):
                result, records = self.counted("update", *args, env=self.path_first(bin_dir))
                self.assert_status(result, 0)
                if "--json" in args:
                    document = self.assert_one_document(result)
                    self.assertEqual([update["component"] for update in document["updates"]],
                                     ["shape", "workflow", "bench", "tools"])
                    self.assertEqual(document["repository"]["dirty"], False)
                else:
                    self.assertIn("workflow: Refresh through setup-openspeckit --repo PATH\n", result.stdout)
                self.assertTrue(records)
                for record in records:
                    self.assertIn(subcommand(record), READ_ONLY, command(record))
                    self.assertEqual(record.optional_locks, "0", "every child is a read-only probe")
        for record in (workflow, shape, tools):
            self.assertFalse(record.exists(), f"{record.name}: nothing was installed or run")
        self.assertEqual(self.git(root, "status", "--porcelain", "--ignored"), before)


if __name__ == "__main__":
    unittest.main()
