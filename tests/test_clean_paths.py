"""Exact paths and one JSON document per run (feature 004, User Story 8:
T110, T111 and the tests of T112).

Sources: the project-clean delta's requirements "Clean reports every path
exactly or excludes it" and "Clean plans and refusals are versioned JSON"
(openspec/changes/add-project-clean-all-safe/, which governs);
specs/004-project-clean-all-safe/contracts/project-clean.md ("Order of a run",
"Streams", "Human output", "JSON", "Plan envelope", "Extended error object",
"Apply result record" and "Codes") and data-model.md ("Repository identity",
"Worktree row" and "Refusal"); lead rulings R-8, R-9, R-38, R-56 Q-14, R-59
D8, R-60, R-61, R-80 (P-13 and P-14) and R-89 (b).

Every character outside ASCII in a fixture path is built with chr(), and every
byte that is not UTF-8 is written as a bytes escape; the expected escaped forms
are built from BACKSLASH, so this source holds no raw character and no escape
an editor could turn into one. The expected $'...' forms follow the delta as
written: the escapes of U+000A, U+0009, U+0001 and U+202E in lower case, and
the byte 0xFF as its two hexadecimal digits. Whether the command form should
write a non-ASCII code point as its UTF-8 bytes is LQ-8, with Brett Heap (lead
rulings R-61 (a) and R-80, P-14). Expected human text comes from clean_support's
fixtures (rule 8), and the contract's key lists are literals written here (rule
11). Every repository is a disposable fixture under the test's temporary
directory (rule 4).
"""
import contextlib
import io
import json
import os
from pathlib import Path
import re
import signal
import types
import unittest
from unittest import mock

import clean_support

project = clean_support.load_project()
TEXT = clean_support.TEXT_FIXTURES
STEPS = clean_support.NEXT_STEP_FIXTURES

BACKSLASH = chr(92)  # built, so that no edit turns an escape written here into its character
FRESHNESS = "local refs only; remote information is as of the last fetch; no fetch performed"
# The baseline's message of a refused confirmation, kept for `cancelled`
# (contracts/project-clean.md, "Codes"; lead ruling R-68 (a)).
CANCELLED = "Cancelled; no command was run."
ZEROS = "0" * 64  # an --expect-plan value no plan's digest equals
HEX_64 = re.compile("[0-9a-f]{64}")

# The contract's key order of each document (contracts/project-clean.md, "Plan
# envelope", "Extended error object" and "Apply result record").
PLAN_ENVELOPE_KEYS = ["schema_version", "observed_at", "mode", "root", "target_branch", "tracking_freshness",
                      "worktrees", "repository", "merge_target", "limits", "budget", "probes", "operations",
                      "selected", "excluded", "omitted", "notes", "completeness", "apply_allowed", "refusals",
                      "plan_digest"]
EXTENDED_ERROR_KEYS = ["error", "code", "schema_version", "observed_at", "mode", "repository", "merge_target",
                       "completeness", "apply_allowed", "refusals"]
APPLY_RESULT_KEYS = ["schema_version", "observed_at", "repository", "merge_target", "plan_digest", "probes",
                     "operations", "targets", "exit_code", "completeness"]
REPOSITORY_KEYS = ["root", "common_dir", "dev", "ino", "root_valid_utf8", "common_dir_valid_utf8"]

# The eighteen refusal codes (the delta's "Clean plans and refusals are
# versioned JSON"), written here as a literal.
REFUSAL_CODES = ["invalid-arguments", "internal-error", "git-unavailable", "git-too-old",
                 "repository-not-found", "ambiguous-name", "target-not-repository-root",
                 "unsupported-path-bytes", "manifest-invalid", "no-merge-target",
                 "inspection-incomplete", "inspect-cap", "deadline-exceeded",
                 "worktree-not-found", "target-excluded", "plan-digest-mismatch",
                 "confirmation-required", "cancelled"]

# The four eligible worktrees of "Control-character and non-UTF-8 paths": the
# name its path starts with, its branch, the code point its path holds, and
# the letters after the backslash of the escape the $'...' form writes for it.
SPECIAL = (
    ("lf", "001-lf", chr(0x0A), "u000a"),
    ("tab", "002-tab", chr(0x09), "u0009"),
    ("soh", "003-soh", chr(0x01), "u0001"),
    ("rlo", "004-rlo", chr(0x202E), "u202e"),
)
NOT_UTF_8 = b"\xff"  # the byte of the fifth worktree's path and of the non-UTF-8 root

SCOPED_SIGNALS = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)


def signal_state():
    """The handlers of SIGINT, SIGTERM and SIGHUP and the wakeup descriptor in force."""
    handlers = tuple(signal.getsignal(signum) for signum in SCOPED_SIGNALS)
    wakeup = signal.set_wakeup_fd(-1)
    if wakeup != -1:
        signal.set_wakeup_fd(wakeup)
    return handlers, wakeup


def argv_words(record):
    """A counted child's argument vector as raw bytes, after its leading
    `-c NAME=VALUE` pins: `-C DIR` and the subcommand's words."""
    argv, at = record.argv_bytes, 0
    while at + 1 < len(argv) and argv[at] == b"-c":
        at += 2
    return list(argv[at:])


def is_removal(record):
    return argv_words(record)[2:4] == [b"worktree", b"remove"]


def probes_a_row(record):
    """Whether a counted child probes a worktree row: a status or hidden-state
    probe."""
    return argv_words(record)[2:3] in ([b"status"], [b"ls-files"])


def objects(value):
    """Every JSON object (dict) in value, value itself first, depth first."""
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from objects(item)
    elif isinstance(value, list):
        for item in value:
            yield from objects(item)


def raising(exc):
    """A stand-in for a stage that raises exc, whatever it is called with."""
    def stage(*args, **kwargs):
        raise exc
    return stage


@contextlib.contextmanager
def working_directory(path):
    """chdir for an in-process run, restored after (contextlib.chdir is 3.11+)."""
    before = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(before)


class PathsTests(clean_support.CleanCase):

    # Helpers of this module's own (rule 3's exceptions).

    def counting(self, name="counting-bin", real=None):
        """The counting wrapper first on PATH: (env, log), the log emptied."""
        bin_dir, log = self.base / name, self.base / (name + ".log")
        clean_support.install_counting_git(bin_dir, log, **({} if real is None else {"real": real}))
        clean_support.reset_child_log(log)
        return self.path_first(bin_dir), log

    def one_document(self, result):
        """Standard output as exactly one JSON document (rule 10), written as
        write_document() writes it: indent 2, ASCII only, one newline (R-38)."""
        document = self.load_json(result)
        self.assertEqual(result.stdout, json.dumps(document, indent=2, ensure_ascii=True) + "\n",
                         clean_support.transcript(result))
        self.assertEqual(document["schema_version"], 1)
        return document

    def assert_plain_base(self):
        """The temporary base prints verbatim inside a $'...' form: ASCII, no
        quote, no backslash, no control character."""
        text = str(self.base)
        self.assertTrue(text.isascii() and text.isprintable(), text)
        self.assertNotIn("'", text)
        self.assertNotIn(BACKSLASH, text)

    def dollar(self, *parts):
        """The $'...' form, from its parts as the test writes them."""
        return "$'" + "".join(parts) + "'"

    def repo_at(self, raw, branch="main"):
        """A repository at the raw path, bytes, with one empty commit (REAL_GIT)."""
        path = Path(os.fsdecode(raw))
        path.mkdir(parents=True)
        self.git(path, "init", "-q", "-b", branch)
        self.git(path, "commit", "-q", "--allow-empty", "-m", "initial")
        return path

    def registry(self, root):
        """The raw paths of root's registry, as `worktree list --porcelain -z` lists them."""
        listing = os.fsencode(self.git(root, "worktree", "list", "--porcelain", "-z"))
        return [field[len(b"worktree "):] for field in listing.split(b"\0") if field.startswith(b"worktree ")]

    def snapshot(self, root):
        """What a refused run must leave unchanged: the registry, every ref,
        and whether each registered path exists."""
        registry = self.registry(root)
        return (registry, self.git(root, "for-each-ref", "--format=%(refname) %(objectname)"),
                [os.path.lexists(path) for path in registry])

    def repository(self, root, common_dir=None):
        """The envelope's `repository` for root, its identity read here: `dev`
        and `ino` by os.lstat of the common directory."""
        common = Path(common_dir) if common_dir is not None else Path(root) / ".git"
        found = os.lstat(common)
        return {"root": str(root), "common_dir": str(common), "dev": found.st_dev, "ino": found.st_ino,
                "root_valid_utf8": True, "common_dir_valid_utf8": True}

    def main_in_process(self, *argv, cwd=None, **patches):
        """project's main(ARGV) in this process, in self.env and cwd (self.base
        by default), each named function of project replaced by its stand-in:
        (status, stdout, stderr). The signal handlers and the wakeup descriptor
        in force before must be in force after (rule 7)."""
        out, err = io.StringIO(), io.StringIO()
        before = signal_state()
        try:
            with contextlib.ExitStack() as stack:
                stack.enter_context(mock.patch.dict(os.environ, self.env, clear=True))
                stack.enter_context(working_directory(self.base if cwd is None else cwd))
                for name, stand_in in patches.items():
                    stack.enter_context(mock.patch.object(project, name, stand_in))
                stack.enter_context(contextlib.redirect_stdout(out))
                stack.enter_context(contextlib.redirect_stderr(err))
                status = project.main([os.fspath(arg) for arg in argv])
        finally:
            self.assertEqual(signal_state(), before, "main() left the signal handlers or wakeup descriptor changed")
        return status, out.getvalue(), err.getvalue()

    # T110: "Control-character and non-UTF-8 paths".

    @clean_support.linux_paths
    def test_clean_control_character_and_non_utf_8_paths(self):
        root = self.repo()
        self.bare_remote()
        self.assert_plain_base()
        base = os.fsencode(self.base)
        eligible = []  # (raw path, branch, its $'...' form, its exact text)
        for name, branch, char, escape in SPECIAL:
            text = str(self.base) + "/" + name + "-a" + char + "b"
            raw = base + b"/" + (name + "-a" + char + "b").encode("utf-8")
            self.assertEqual(os.fsdecode(raw), text)
            self.merged_worktree(branch, path=raw)
            eligible.append((raw, branch, self.dollar(str(self.base), "/", name, "-a", BACKSLASH, escape, "b"), text))
        eligible.sort()  # raw path byte order: lf, rlo, soh, tab
        bad = base + b"/ff-a" + NOT_UTF_8 + b"b"
        self.merged_worktree("005-ff", path=bad)
        bad_form = self.dollar(str(self.base), "/ff-a", BACKSLASH, "xff", "b")
        bad_text = str(self.base) + "/ff-a" + BACKSLASH + "xffb"  # json_path()'s text: \xHH for the byte
        bad_entry = {"path": bad_text, "path_valid_utf8": False, "branch": "005-ff",
                     "classification": "merged-removable", "reason": "unsupported-path-bytes"}

        with self.subTest("the preview, --json"):
            preview = self.run_json("clean", root, "--all-safe", "--json")
            self.assert_status(preview, 0)
            document = self.one_document(preview)
            self.assertTrue(preview.stdout.isascii(), "every code point to escape is a JSON escape, never raw")
            self.assertEqual([(entry["path"], entry["path_valid_utf8"], entry["branch"])
                              for entry in document["selected"]],
                             [(text, True, branch) for _raw, branch, _form, text in eligible])
            for _raw, _branch, _form, text in eligible:
                # Exact JSON strings: json.dumps' escape of each code point.
                self.assertIn('"path": ' + json.dumps(text) + ",", preview.stdout)
            rows = {row["path"]: row for row in document["worktrees"]}
            self.assertEqual((rows[bad_text]["path_valid_utf8"], rows[bad_text]["classification"]),
                             (False, "merged-removable"), "otherwise eligible")
            self.assertIn(bad_entry, document["excluded"])
            self.assertEqual([entry["reason"] for entry in document["excluded"]],
                             ["unsupported-path-bytes", "main-worktree"], "by raw path bytes: ff- before repo")
            self.assertIn('"path": ' + json.dumps(bad_text) + ",", preview.stdout)  # each backslash doubled

        with self.subTest("the preview, human"):
            human = self.run_cli("clean", root, "--all-safe")
            self.assert_status(human, 0)
            group = TEXT["excluded_group"].format(REASON="unsupported-path-bytes", K=1,
                                                  NEXT_STEP=STEPS["unsupported-path-bytes"])
            self.assertEqual(group, "  unsupported-path-bytes (1): rename the path to valid UTF-8")
            expected = [f"Cleanup plan for {root}", TEXT["merge_target_line"].format(NAME="main", SOURCE="main"),
                        f"Freshness: {FRESHNESS}", TEXT["selected_heading"].format(N=4)]
            expected += [TEXT["selected_row"].format(PATH=form, BRANCH=branch) for _raw, branch, form, _ in eligible]
            expected += [TEXT["excluded_heading"].format(M=2),
                         TEXT["excluded_group"].format(REASON="main-worktree", K=1, NEXT_STEP=STEPS["main-worktree"]),
                         TEXT["excluded_row"].format(PATH=root, BRANCH="main"),
                         group,
                         TEXT["excluded_row"].format(PATH=bad_form, BRANCH="005-ff"),
                         TEXT["residual_window_line"]]
            self.assertEqual((human.stdout, human.stderr), ("\n".join(expected) + "\n", ""))

        with self.subTest("the apply, --json, under the counting wrapper"):
            env, log = self.counting()
            applied = self.run_json("clean", root, "--all-safe", "--apply", "--yes", "--json", env=env)
            self.assert_status(applied, 0)
            document = self.one_document(applied)
            self.assertEqual(list(document), APPLY_RESULT_KEYS)
            self.assertEqual([(target["path"], target["path_valid_utf8"], target["branch"], target["stage"],
                               target["reason"]) for target in document["targets"]],
                             [(text, True, branch, "removed", None) for _raw, branch, _form, text in eligible])
            for target in document["targets"]:
                record = target["reconciliation"]
                self.assertEqual((record["registry_entry_present"], record["path_present"], record["reconciled"]),
                                 (False, False, True), "the rescan proves it removed")
            self.assertEqual(document["exit_code"], 0)
            # The human plan and the progress, on standard error, print each
            # path in the $'...' form.
            lines = applied.stderr.split("\n")
            for _raw, branch, form, _text in eligible:
                self.assertIn(TEXT["selected_row"].format(PATH=form, BRANCH=branch), lines)
                self.assertIn(TEXT["progress_line"].format(STAGE="removed", PATH=form), lines)
            self.assertIn(TEXT["excluded_row"].format(PATH=bad_form, BRANCH="005-ff"), lines)
            # Git receives each raw path as one argument, and the fifth in no
            # removal at all.
            removals = [argv_words(record) for record in clean_support.child_log(log) if is_removal(record)]
            self.assertEqual([words[4:] for words in removals], [[raw] for raw, _b, _f, _t in eligible])
            self.assertEqual([words for words in removals if any(NOT_UTF_8 in word for word in words)], [])

        with self.subTest("afterwards"):
            registry = self.registry(root)
            for raw, _branch, _form, _text in eligible:
                self.assertFalse(os.path.lexists(raw), raw)
                self.assertNotIn(raw, registry)
            self.assertTrue(os.path.isdir(bad), "the fifth is still present")
            self.assertIn(bad, registry)

    # T110: "Non-UTF-8 repository root".

    @clean_support.linux_paths
    def test_clean_non_utf_8_repository_root(self):
        self.assert_plain_base()
        raw = os.fsencode(self.base) + b"/root-a" + NOT_UTF_8 + b"b"
        root = self.repo_at(raw)
        self.bare_remote(root=root)
        linked = self.merged_worktree("001-merged", root=root)
        form = self.dollar(str(self.base), "/root-a", BACKSLASH, "xff", "b")
        message = TEXT["unsupported_path_bytes"].format(PATH=form)
        refusal = {"code": "unsupported-path-bytes", "message": message,
                   "path": str(self.base) + "/root-a" + BACKSLASH + "xffb", "path_valid_utf8": False}
        before = self.snapshot(root)
        env, log = self.counting()
        for words, mode in (((), "report"), (("--all-safe",), "all-safe"), (("--all-safe", "--apply", "--yes"),
                                                                             "all-safe")):
            with self.subTest(words=words):
                human = self.run_cli("clean", raw, *words, env=env)
                self.assert_status(human, 2)
                self.assertEqual((human.stdout, human.stderr), ("", f"REFUSED: {message}\n"))
                result = self.run_cli("clean", raw, *words, "--json", env=env)
                self.assert_status(result, 2)
                document = self.one_document(result)
                self.assertEqual(list(document), EXTENDED_ERROR_KEYS, "no plan: the extended error object")
                self.assertEqual(document, {
                    "error": message, "code": "unsupported-path-bytes", "schema_version": 1,
                    "observed_at": document["observed_at"], "mode": mode, "repository": None,
                    "merge_target": None, "completeness": "incomplete", "apply_allowed": False,
                    "refusals": [refusal]})
                self.assertEqual(result.stderr, "")
        records = clean_support.child_log(log)
        self.assertTrue(records, "the runs went through the counting wrapper")
        self.assertEqual([argv_words(record) for record in records if probes_a_row(record) or is_removal(record)],
                         [], "no status child: no row is probed before the refusal, and nothing is removed")
        self.assertEqual(self.snapshot(root), before, "nothing changes")
        self.assertTrue(linked.is_dir())

    @clean_support.linux_paths
    def test_clean_non_utf_8_repository_root_common_directory(self):
        # Lead ruling R-80, P-13: a valid root whose common directory is not
        # valid UTF-8 refuses too, naming the common directory.
        self.assert_plain_base()
        gitdir = os.fsencode(self.base) + b"/gitdir-a" + NOT_UTF_8 + b"b.git"
        checkout = self.base / "checkout"
        self.git(self.base, "init", "-q", "-b", "main", "--separate-git-dir", Path(os.fsdecode(gitdir)), checkout)
        self.git(checkout, "commit", "-q", "--allow-empty", "-m", "initial")
        form = self.dollar(str(self.base), "/gitdir-a", BACKSLASH, "xff", "b.git")
        message = TEXT["unsupported_path_bytes"].format(PATH=form)
        before = self.snapshot(checkout)
        env, log = self.counting()
        result = self.run_cli("clean", checkout, "--all-safe", "--json", env=env)
        self.assert_status(result, 2)
        document = self.one_document(result)
        self.assertEqual((document["code"], document["error"], document["repository"], document["refusals"]),
                         ("unsupported-path-bytes", message, None, [{
                             "code": "unsupported-path-bytes", "message": message,
                             "path": str(self.base) + "/gitdir-a" + BACKSLASH + "xffb.git",
                             "path_valid_utf8": False}]))
        human = self.run_cli("clean", checkout, "--all-safe", "--apply", "--yes", env=env)
        self.assertEqual((human.returncode, human.stdout, human.stderr), (2, "", f"REFUSED: {message}\n"))
        self.assertEqual([record for record in clean_support.child_log(log) if probes_a_row(record)], [])
        self.assertEqual(self.snapshot(checkout), before)


if __name__ == "__main__":
    unittest.main()
