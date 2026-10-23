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

# The nineteen refusal codes (the delta's "Clean plans and refusals are
# versioned JSON"), written here as a literal; relative-config-path is Brett
# Heap's ruling LQ-15 (lead rulings R-102 and R-131 (c)).
REFUSAL_CODES = ["invalid-arguments", "internal-error", "git-unavailable", "git-too-old",
                 "relative-config-path",
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
            self.assertEqual(group, "  unsupported-path-bytes (1): move it to a valid UTF-8 path with git worktree "
                                    "move, or mv it and then git worktree repair NEWPATH")
            # T14 (lane 3's W120 L-1): a plain mv leaves the registry entry stale, so the step names
            # the two moves that mend it; git worktree move refuses a worktree that holds a submodule.
            self.assertIn("git worktree move", project.NEXT_STEPS["unsupported-path-bytes"])
            self.assertIn("git worktree repair NEWPATH", project.NEXT_STEPS["unsupported-path-bytes"])
            self.assertIn(group, human.stdout.splitlines())
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

    @clean_support.linux_paths
    def test_clean_line_feed_paths_where_row_4c_reads_true(self):
        # "Control-character and non-UTF-8 paths" in a repository whose
        # extensions.worktreeConfig is true (lane 3's W70 M-2; lead ruling
        # R-287): LQ-11's work-tree probe prints a linked worktree's own path
        # over two lines where that path holds a line feed, and its output,
        # less the one line feed Git ends it with, is read as one path. Two
        # merged worktrees, nothing redirected: one whose path holds a line
        # feed inside, one whose path ends in one. Both are selected, the probe
        # runs in each at planning and again at its revalidation, both are
        # removed and the rescan proves it, and the counts are the extension's:
        # seven children per revalidation, three for the final rescan, and
        # probes.estimated equal to probes.performed.
        root = self.repo()
        self.bare_remote()
        self.assert_plain_base()
        base = os.fsencode(self.base)
        eligible = []  # (raw path, branch, exact text), in raw path byte order
        for name, branch in (("end-a" + chr(0x0A), "001-end"), ("lf-a" + chr(0x0A) + "b", "002-lf")):
            raw = base + b"/" + name.encode("ascii")
            self.merged_worktree(branch, path=raw)
            eligible.append((raw, branch, os.fsdecode(raw)))
        self.git(root, "config", "extensions.worktreeConfig", "true")
        probe = [b"rev-parse", b"--path-format=absolute", b"--show-toplevel"]
        for _raw, _branch, text in eligible:
            printed = self.git(Path(text), *(word.decode("ascii") for word in probe))
            self.assertEqual(printed, text + chr(0x0A), "Git prints the path and one line feed")
            self.assertGreater(len(printed.split(chr(0x0A))), 2, "over two lines or more")

        preview = self.run_json("clean", root, "--all-safe", "--json")
        self.assert_status(preview, 0)
        document = self.one_document(preview)
        self.assertEqual([(entry["path"], entry["branch"]) for entry in document["selected"]],
                         [(text, branch) for _raw, branch, text in eligible])
        self.assertEqual([entry["reason"] for entry in document["excluded"]], ["main-worktree"],
                         "no registration-mismatch")
        rows = {row["path"]: row for row in document["worktrees"]}
        for _raw, _branch, text in eligible:
            self.assertEqual((rows[text]["errors"], rows[text]["classification"]), ([], "merged-removable"))
        self.assertEqual((document["completeness"], document["refusals"]), ("complete", []))
        planning = document["probes"]["performed"]
        self.assertEqual(document["probes"]["estimated"], planning + 7 * len(eligible) + 3)

        env, log = self.counting()
        applied = self.run_json("clean", root, "--all-safe", "--apply", "--yes", "--json", env=env)
        self.assert_status(applied, 0)
        document = self.one_document(applied)
        self.assertEqual([(target["path"], target["stage"], target["reason"]) for target in document["targets"]],
                         [(text, "removed", None) for _raw, _branch, text in eligible])
        for target in document["targets"]:
            record = target["reconciliation"]
            self.assertEqual((record["registry_entry_present"], record["path_present"], record["reconciled"]),
                             (False, False, True), "the rescan proves it removed")
        revalidations = [target["probes_performed"] for target in document["targets"]]
        self.assertEqual(revalidations, [7] * len(eligible))
        self.assertEqual(document["probes"], {"estimated": planning + sum(revalidations) + 3,
                                              "performed": planning + sum(revalidations) + 3})
        probed = [argv_words(record)[1] for record in clean_support.child_log(log)
                  if argv_words(record)[2:] == probe]
        self.assertEqual(sorted(probed), sorted([raw for raw, _b, _t in eligible] * 2),
                         "the work-tree probe at planning and again at each revalidation")
        registry = self.registry(root)
        for raw, _branch, _text in eligible:
            self.assertFalse(os.path.lexists(raw), raw)
            self.assertNotIn(raw, registry)

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

    # T111: "Apply with JSON prints one document".

    def test_clean_apply_with_json_prints_one_document(self):
        # Pins T057: under --apply --json, standard output holds the one document.
        root = self.repo()
        self.bare_remote()
        trees = [(self.merged_worktree("001-a"), "001-a"), (self.merged_worktree("002-b"), "002-b")]
        plan = [f"Cleanup plan for {root}", TEXT["merge_target_line"].format(NAME="main", SOURCE="main"),
                f"Freshness: {FRESHNESS}", TEXT["selected_heading"].format(N=2)]
        plan += [TEXT["selected_row"].format(PATH=tree, BRANCH=branch) for tree, branch in trees]
        plan += [TEXT["excluded_heading"].format(M=1),
                 TEXT["excluded_group"].format(REASON="main-worktree", K=1, NEXT_STEP=STEPS["main-worktree"]),
                 TEXT["excluded_row"].format(PATH=root, BRANCH="main"), TEXT["residual_window_line"]]

        with self.subTest("stopped before the apply phase by plan-digest-mismatch"):
            stopped = self.run_cli("clean", root, "--all-safe", "--apply", "--yes", "--json", "--expect-plan", ZEROS)
            self.assert_status(stopped, 2)
            document = self.one_document(stopped)
            self.assertEqual(list(document), PLAN_ENVELOPE_KEYS, "only the plan envelope")
            self.assertEqual((document["apply_allowed"], document["refusals"]), (False, [{
                "code": "plan-digest-mismatch",
                "message": TEXT["plan_digest_mismatch"].format(DIGEST=document["plan_digest"], EXPECTED=ZEROS)}]))
            self.assertEqual(stopped.stderr, "\n".join(plan) + "\n", "the human plan alone, no REFUSED: line")
            self.assertTrue(all(tree.is_dir() for tree, _ in trees), "nothing removed")

        with self.subTest("the apply removes two worktrees"):
            applied = self.run_cli("clean", root, "--all-safe", "--apply", "--yes", "--json")
            self.assert_status(applied, 0)
            document = self.one_document(applied)
            self.assertEqual(list(document), APPLY_RESULT_KEYS, "the apply result record alone")
            self.assertEqual([(target["path"], target["stage"], target["reason"]) for target in document["targets"]],
                             [(str(tree), "removed", None) for tree, _ in trees])
            self.assertEqual((document["exit_code"], document["completeness"]), (0, "complete"))
            result = [TEXT["progress_line"].format(STAGE="removed", PATH=tree) for tree, _ in trees]
            result += [TEXT["success_line"].format(N=2, BRANCHES="001-a, 002-b"), TEXT["residual_window_line"]]
            self.assertEqual(applied.stderr, "\n".join(plan + result) + "\n",
                             "the human plan and the progress on standard error")
            self.assertFalse(any(tree.exists() for tree, _ in trees))

    # T111: "The plain report in JSON".

    def test_clean_the_plain_report_in_json(self):
        # Pins T051 (the envelope) and T101 (a complete report exits 0).
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-eligible")
        report = self.run_json("clean", root, "--json")
        self.assert_status(report, 0)
        document = self.one_document(report)
        self.assertEqual(list(document), PLAN_ENVELOPE_KEYS)
        self.assertEqual((document["schema_version"], document["mode"], document["apply_allowed"],
                          document["limits"]["worktree_rows"], document["completeness"], document["refusals"]),
                         (1, "report", False, 256, "complete", []))
        self.assertEqual([entry["path"] for entry in document["selected"]], [str(tree)])
        self.assertIsNotNone(HEX_64.fullmatch(document["plan_digest"]), document["plan_digest"])
        self.assertEqual(report.stderr, "")
        preview = self.run_json("clean", root, "--all-safe", "--json")
        self.assert_status(preview, 0)
        previewed = self.one_document(preview)
        self.assertEqual((previewed["mode"], previewed["limits"]["worktree_rows"]), ("all-safe", 128))
        self.assertEqual(document["plan_digest"], previewed["plan_digest"],
                         "FR-004: the report's digest equals the --all-safe preview's")

    # T111: every path value in JSON carries its flag (lead ruling R-9).

    def test_clean_every_json_path_carries_its_flag(self):
        root = self.repo()
        self.bare_remote()
        self.merged_worktree("001-merged")
        ignored = self.merged_worktree("002-ignored",
                                       setup=lambda tree: (tree / ".gitignore").write_text("local.env\n"))
        (ignored / "local.env").write_text("preserve")
        dirty = self.merged_worktree("003-dirty")
        (dirty / "uncommitted").write_text("preserve")
        failing = self.merged_worktree("004-failing")
        fake = clean_support.install_fake_git(self.base / "fails-bin", "status-fails-in", path=failing)
        failing_env = self.path_first(fake.parent)
        subdirectory = root / "sub"
        subdirectory.mkdir()
        documents = {}
        for label, target, words, env, status in (
                ("report", root, ("--json",), failing_env, 1),
                ("preview", root, ("--all-safe", "--json"), failing_env, 1),
                ("target-excluded", root, ("--apply", "--action", "remove", "--worktree", dirty, "--yes", "--json"),
                 None, 2),
                ("worktree-not-found", root, ("--apply", "--action", "remove", "--worktree", self.base / "nowhere",
                                              "--yes", "--json"), None, 2),
                ("target-not-repository-root", subdirectory, ("--json",), None, 2),
                ("apply", root, ("--all-safe", "--apply", "--yes", "--json"), None, 0)):
            result = self.run_cli("clean", target, *words, env=env)
            self.assert_status(result, status)
            documents[label] = self.one_document(result)

        flagged, samples, repositories = [], [], 0
        for label, document in documents.items():
            for item in objects(document):
                if "path" in item:
                    self.assertIs(item.get("path_valid_utf8"), True, (label, item))
                    flagged.append((label, item["path"]))
                if "path" in item and item.get("ignored_samples") is not None:  # a row; `limits` has a count
                    for sample in item["ignored_samples"]:
                        self.assertEqual(list(sample), ["path", "path_valid_utf8"], (label, sample))
                        samples.append(sample)
                if isinstance(item.get("repository"), dict):
                    self.assertEqual(list(item["repository"]), REPOSITORY_KEYS)
                    self.assertEqual((item["repository"]["root_valid_utf8"],
                                      item["repository"]["common_dir_valid_utf8"]), (True, True), label)
                    repositories += 1
        # The walk reached every kind of object that carries a path.
        self.assertIn({"path": "local.env", "path_valid_utf8": True}, samples)
        self.assertEqual(repositories, 5, "every document but the extended error object")
        for label, kinds in (("report", ("worktrees", "selected", "excluded")), ("apply", ("targets",))):
            for kind in kinds:
                self.assertTrue(documents[label][kind], (label, kind))
        for label in ("target-excluded", "worktree-not-found", "target-not-repository-root"):
            refusal = documents[label]["refusals"][0]
            self.assertEqual((refusal["code"], refusal["path_valid_utf8"]), (label, True))
        self.assertIn(("report", str(failing)), flagged)

    # T111: each refusal code prints its one document (plan review M6).

    def test_clean_each_refusal_prints_its_document(self):
        root = self.repo()
        self.bare_remote()
        merged = self.merged_worktree("001-merged")
        dirty = self.merged_worktree("002-dirty")
        (dirty / "uncommitted").write_text("preserve")
        elsewhere = self.base / "elsewhere"
        elsewhere.mkdir()
        before = self.snapshot(root)
        reached = []

        def in_process(*argv, **options):
            status, out, err = self.main_in_process(*argv, **options)
            return types.SimpleNamespace(returncode=status, stdout=out, stderr=err, args=[os.fspath(a) for a in argv])

        def error_object(result, code, message, mode, path=None, repository=None):
            """Exit 2 and one extended error object (invalid-arguments,
            internal-error and every resolve code)."""
            self.assert_status(result, 2)
            document = self.one_document(result)
            refusal = {"code": code, "message": message}
            if path is not None:
                refusal.update(path=str(path), path_valid_utf8=True)
            self.assertEqual(list(document), EXTENDED_ERROR_KEYS)
            self.assertEqual(document, {
                "error": message, "code": code, "schema_version": 1, "observed_at": document["observed_at"],
                "mode": mode, "repository": repository, "merge_target": None, "completeness": "incomplete",
                "apply_allowed": False, "refusals": [refusal]})
            self.assertNotIn("REFUSED", result.stderr)
            reached.append(code)

        def envelope(result, status, refusal, mode):
            """One plan envelope with `apply_allowed: false` and the refusal in
            `refusals` (the plan, select and confirm codes)."""
            self.assert_status(result, status)
            document = self.one_document(result)
            self.assertEqual(list(document), PLAN_ENVELOPE_KEYS)
            self.assertEqual((document["mode"], document["apply_allowed"], document["refusals"]),
                             (mode, False, [refusal]))
            self.assertNotIn("REFUSED", result.stderr)
            reached.append(refusal["code"])
            return document

        def incomplete(code, remedy):
            return {"code": code, "message": TEXT["plan_incomplete"].format(CODE=code, REMEDY=remedy)}

        with self.subTest("invalid-arguments"):
            result = self.run_cli("clean", root, "--all-safe", "--action", "remove", "--json")
            error_object(result, "invalid-arguments", TEXT["invalid_arguments_all_safe"], "all-safe")
        with self.subTest("internal-error"):
            # An exception injected in process, on the module object main() runs (rule 3).
            result = in_process("clean", root, "--json", build_plan=raising(RuntimeError("boom")))
            error_object(result, "internal-error", TEXT["internal_error"].format(TYPE="RuntimeError", TEXT="boom"),
                         "report")
        with self.subTest("git-unavailable"):
            result = self.run_cli("clean", root, "--json", env=dict(self.env, PATH=self.path_without_git()))
            error_object(result, "git-unavailable",
                         TEXT["git_unavailable"].format(DETAIL=TEXT["git_unavailable_not_found"]), "report")
        with self.subTest("git-too-old"):
            fake = clean_support.install_fake_git(self.base / "old-bin", "version-2.35.0")
            result = self.run_cli("clean", root, "--all-safe", "--json", env=self.path_first(fake.parent))
            error_object(result, "git-too-old", TEXT["git_too_old"].format(VERSION="2.35.0"), "all-safe")
        with self.subTest("relative-config-path"):
            result = self.run_cli("clean", root, "--json", env=dict(self.env, HOME="h"))
            error_object(result, "relative-config-path", TEXT["relative_config_path"].format(NAME="HOME"), "report")
        with self.subTest("repository-not-found"):
            # Inline bare-name fixture (rule 3), as tests/test_clean_resolution.py builds it.
            result = self.run_cli("clean", "Nowhere", "--json", cwd=elsewhere)
            error_object(result, "repository-not-found", f"Directory does not exist: {elsewhere / 'Nowhere'}",
                         "report")
        with self.subTest("ambiguous-name"):
            # Inline bare-name fixture (rule 3), as tests/test_clean_resolution.py
            # builds it: two project directories each holding Atlas, given to
            # main() in process through projects_dirs(), since macOS folds
            # ~/projects and ~/Projects into one directory.
            directories = [self.base / "projects-one", self.base / "projects-two"]
            for directory in directories:
                (directory / "Atlas").mkdir(parents=True)
            result = in_process("clean", "Atlas", "--json", cwd=elsewhere, projects_dirs=lambda: directories)
            error_object(result, "ambiguous-name", "Ambiguous project name; supply a path.", "report")
        with self.subTest("target-not-repository-root"):
            subdirectory = root / "sub"
            subdirectory.mkdir()
            result = self.run_cli("clean", subdirectory, "--json")
            error_object(result, "target-not-repository-root",
                         TEXT["target_not_repository_root"].format(PATH=subdirectory), "report", path=subdirectory)
        with self.subTest("manifest-invalid"):
            wrong = self.repo("wrong-kind")
            (wrong / "project.yaml").write_text("kind: family-manifest\n")
            result = self.run_cli("clean", wrong, "--json")
            error_object(result, "manifest-invalid",
                         f"Unexpected kind in {wrong / 'project.yaml'}; expected project-manifest", "report",
                         repository=self.repository(wrong))
        with self.subTest("no-merge-target"):
            trunk = self.repo("trunk-only", branch="trunk")
            result = self.run_cli("clean", trunk, "--all-safe", "--json")
            error_object(result, "no-merge-target", TEXT["no_merge_target"], "all-safe",
                         repository=self.repository(trunk))
        with self.subTest("inspection-incomplete"):
            fake = clean_support.install_fake_git(self.base / "fails-bin", "status-fails-in", path=dirty)
            result = self.run_cli("clean", root, "--all-safe", "--json", env=self.path_first(fake.parent))
            envelope(result, 1, incomplete("inspection-incomplete", TEXT["remedy_inspection_incomplete"]), "all-safe")
        with self.subTest("inspect-cap"):
            capped = self.repo("capped")
            self.register_worktrees(128, "cap", root=capped)  # 129 rows with the main worktree
            result = self.run_cli("clean", capped, "--all-safe", "--json")
            document = envelope(result, 1, incomplete("inspect-cap", TEXT["remedy_inspect_cap"].format(N=129, M=128)),
                                "all-safe")
            self.assertEqual(document["omitted"], {"count": 1, "exactness": "exact"})
        with self.subTest("deadline-exceeded"):
            # Through the launcher, with a table that shortens the deadline to 3 s
            # and the reserve to 1 s: 2 s of work, so each probe's budget,
            # min(5 s, work remaining), is at most 2 s (rule 5, R-29). The first
            # linked row's status probe hangs (status-hangs-in, US6's T099), the
            # work deadline cuts it, and the row after it is never probed.
            fake = clean_support.install_fake_git(self.base / "hangs-bin", "status-hangs-in", path=merged)
            table = clean_support.timing_table(invocation_deadline=3.0, reconciliation_reserve=1.0)
            result = self.run_launched(table, "clean", root, "--all-safe", "--json", env=self.path_first(fake.parent))
            envelope(result, 1, incomplete("deadline-exceeded", TEXT["remedy_deadline_exceeded"]), "all-safe")
        with self.subTest("worktree-not-found"):
            nowhere = self.base / "nowhere"
            result = self.run_cli("clean", root, "--apply", "--action", "remove", "--worktree", nowhere, "--yes",
                                  "--json")
            envelope(result, 2, {"code": "worktree-not-found", "message": f"No unique linked worktree found at {nowhere}",
                                 "path": str(nowhere), "path_valid_utf8": True}, "single")
        with self.subTest("target-excluded"):
            result = self.run_cli("clean", root, "--apply", "--action", "remove", "--worktree", dirty, "--yes", "--json")
            envelope(result, 2, {"code": "target-excluded", "message": TEXT["target_excluded_class"].format(CLASS="dirty"),
                                 "path": str(dirty), "path_valid_utf8": True, "reason": "dirty"}, "single")
        with self.subTest("plan-digest-mismatch"):
            result = self.run_cli("clean", root, "--all-safe", "--apply", "--yes", "--expect-plan", ZEROS, "--json")
            digest = self.load_json(result)["plan_digest"]
            envelope(result, 2, {"code": "plan-digest-mismatch", "message": TEXT["plan_digest_mismatch"].format(
                DIGEST=digest, EXPECTED=ZEROS)}, "all-safe")
        with self.subTest("confirmation-required"):
            result = self.run_cli("clean", root, "--all-safe", "--apply", "--json")  # standard input a pipe
            envelope(result, 2, {"code": "confirmation-required", "message": TEXT["confirmation_required"]}, "all-safe")
        with self.subTest("cancelled"):
            # Standard input at a terminal, standard output on a pipe (lead
            # ruling R-56 Q-14): the question on standard error, answered `no`.
            argv = clean_support.cli_argv("clean", root, "--all-safe", "--apply", "--json")
            result = self.run_pty_steps(argv, [(TEXT["question_one"], "no")], stdout_pipe=True)
            self.assertIn(TEXT["question_one"], result.stderr.split("\n"))
            envelope(result, 2, {"code": "cancelled", "message": CANCELLED}, "all-safe")

        self.assertEqual(sorted(reached), sorted(code for code in REFUSAL_CODES if code != "unsupported-path-bytes"),
                         "every code but unsupported-path-bytes, its clause below")
        self.assertEqual(self.snapshot(root), before, "nothing changes")

    @clean_support.linux_paths
    def test_clean_each_refusal_prints_its_document_unsupported_path_bytes(self):
        # The one code left needs a root that is not valid UTF-8, which only a
        # Linux file system holds (rule 9); T110's root test asserts the whole object.
        self.assert_plain_base()
        raw = os.fsencode(self.base) + b"/root-a" + NOT_UTF_8 + b"b"
        self.repo_at(raw)
        result = self.run_cli("clean", raw, "--json")
        self.assert_status(result, 2)
        document = self.one_document(result)
        self.assertEqual(list(document), EXTENDED_ERROR_KEYS)
        self.assertEqual((document["code"], document["apply_allowed"], [item["code"] for item in document["refusals"]]),
                         ("unsupported-path-bytes", False, ["unsupported-path-bytes"]))
        self.assertEqual(result.stderr, "")

    # T112's sweep: every refusal that names a path prints it through the
    # escaping printer (FR-041), so that a path holding U+202E, valid UTF-8 and
    # so never refused for its bytes, is escaped in `REFUSED:` (lead ruling
    # R-80, P-12, and the fallback of build_plan() in region plan).

    def test_clean_refusal_messages_print_their_paths_escaped(self):
        self.assert_plain_base()
        rlo = chr(0x202E)
        root = self.repo("rlo-a" + rlo + "b")
        manifest_form = self.dollar(str(self.base), "/rlo-a", BACKSLASH, "u202eb/project.yaml")
        manifest = root / "project.yaml"
        for label, content, message in (
                ("the wrong kind", "kind: family-manifest\n",
                 f"Unexpected kind in {manifest_form}; expected project-manifest"),
                ("not a mapping", "- kind\n- project-manifest\n", f"Expected a mapping in {manifest_form}"),
                ("a parse error", "kind: [unclosed\n", f"Cannot read {manifest_form}: ")):
            with self.subTest(label):
                manifest.write_text(content)
                human = self.run_cli("clean", root)
                self.assert_status(human, 2)
                self.assertTrue(human.stderr.isascii(), human.stderr)
                self.assertTrue(human.stderr.startswith("REFUSED: " + message), human.stderr)
                result = self.run_cli("clean", root, "--all-safe", "--json")
                self.assert_status(result, 2)
                document = self.one_document(result)
                self.assertEqual((document["code"], document["repository"]["root_valid_utf8"]),
                                 ("manifest-invalid", True))
                self.assertTrue(document["error"].startswith(message), document["error"])
        manifest.unlink()
        with self.subTest("built: target-not-repository-root"):
            subdirectory = root / ("sub-a" + rlo + "b")
            subdirectory.mkdir()
            human = self.run_cli("clean", subdirectory)
            form = self.dollar(str(self.base), "/rlo-a", BACKSLASH, "u202eb/sub-a", BACKSLASH, "u202eb")
            self.assertEqual((human.returncode, human.stderr),
                             (2, "REFUSED: " + TEXT["target_not_repository_root"].format(PATH=form) + "\n"))
        with self.subTest("built: worktree-not-found"):
            nowhere = self.base / ("nowhere-a" + rlo + "b")
            human = self.run_cli("clean", root, "--apply", "--action", "remove", "--worktree", nowhere, "--yes")
            form = self.dollar(str(self.base), "/nowhere-a", BACKSLASH, "u202eb")
            self.assertEqual((human.returncode, human.stderr),
                             (2, f"REFUSED: No unique linked worktree found at {form}\n"))
            self.assertTrue(human.stdout.isascii(), human.stdout)
        with self.subTest("build_plan() for a caller that passes no evidence"):
            # Only such a caller reaches the fallback (lead rulings R-71 (b) and
            # R-72 (g)); it runs in process on the module object loaded here.
            with mock.patch.dict(os.environ, self.env, clear=True), project.Invocation("clean") as run:
                run.mode, run.action = "report", None
                with self.assertRaises(project.Refused) as caught:
                    project.build_plan({"root": subdirectory}, run)
            self.assertEqual(str(caught.exception), "Cannot inspect Git repository at " + self.dollar(
                str(self.base), "/rlo-a", BACKSLASH, "u202eb/sub-a", BACKSLASH, "u202eb"))

    # Lead ruling R-92 (c): discover()'s two bare-name messages, `Directory does
    # not exist: PATH` and `No project found at PATH; supply a path or name.`,
    # reach clean as `repository-not-found` and name the user's own argument, so
    # resolve_clean_target() prints the path in each through human_path()
    # (contracts/project-clean.md, "Human output" and "Codes"). The JSON
    # document keeps the one message, escaped alike, in `error` and in the
    # refusal, which has no `path` of its own: the baseline's refusal had none.

    def assert_bare_name_not_found(self, argument, message, cwd):
        """clean ARGUMENT in CWD refuses with `repository-not-found` and MESSAGE,
        in human output and in the extended error object, both ASCII only."""
        human = self.run_cli("clean", argument, cwd=cwd)
        self.assert_status(human, 2)
        self.assertEqual((human.stdout, human.stderr), ("", f"REFUSED: {message}\n"))
        self.assertTrue(human.stderr.isascii(), human.stderr)
        result = self.run_cli("clean", argument, "--json", cwd=cwd)
        self.assert_status(result, 2)
        document = self.one_document(result)
        self.assertTrue(result.stdout.isascii(), result.stdout)
        self.assertEqual(list(document), EXTENDED_ERROR_KEYS)
        self.assertEqual(document, {
            "error": message, "code": "repository-not-found", "schema_version": 1,
            "observed_at": document["observed_at"], "mode": "report", "repository": None, "merge_target": None,
            "completeness": "incomplete", "apply_allowed": False,
            "refusals": [{"code": "repository-not-found", "message": message}]})
        self.assertEqual(result.stderr, "")

    def test_clean_refusal_messages_print_their_paths_escaped_for_a_bare_name_not_found(self):
        self.assert_plain_base()
        rlo = chr(0x202E)
        elsewhere = self.base / "elsewhere"
        elsewhere.mkdir()
        (self.base / ("Plain" + rlo + "dir")).mkdir()  # in the projects directory, holding no project
        before = sorted(path.name for path in self.base.iterdir())
        for label, argument, message in (
                ("a directory that does not exist", "No" + rlo + "where",
                 "Directory does not exist: " + self.dollar(str(elsewhere), "/No", BACKSLASH, "u202ewhere")),
                ("an existing directory with no project", "Plain" + rlo + "dir",
                 "No project found at " + self.dollar(str(self.base), "/Plain", BACKSLASH, "u202edir")
                 + "; supply a path or name.")):
            with self.subTest(label):
                self.assertNotIn(rlo, message)
                self.assert_bare_name_not_found(argument, message, elsewhere)
        with self.subTest("a discover() that codes neither message, as before T118"):
            # In process, since discover() now codes both: the fallback in
            # resolve_clean_target() maps and escapes them alike.
            path = str(elsewhere / ("No" + rlo + "where"))
            form = self.dollar(str(elsewhere), "/No", BACKSLASH, "u202ewhere")
            for raw, message in (
                    (f"Directory does not exist: {path}", f"Directory does not exist: {form}"),
                    (f"No project found at {path}; supply a path or name.",
                     f"No project found at {form}; supply a path or name.")):
                status, out, err = self.main_in_process("clean", "Nowhere", cwd=elsewhere,
                                                        discover=raising(project.Refused(raw)))
                self.assertEqual((status, out, err), (2, "", f"REFUSED: {message}\n"))
        self.assertEqual(sorted(path.name for path in self.base.iterdir()), before, "nothing changes")

    @clean_support.linux_paths
    def test_clean_refusal_messages_print_their_paths_escaped_for_a_bare_name_not_found_not_utf_8(self):
        # The same two messages for a bare name that holds the byte 0xFF, which
        # prints as \xff (rule 9, Linux only).
        self.assert_plain_base()
        elsewhere = self.base / "elsewhere"
        elsewhere.mkdir()
        os.mkdir(os.fsencode(self.base) + b"/Plain" + NOT_UTF_8 + b"dir")
        for label, argument, message in (
                ("a directory that does not exist", b"No" + NOT_UTF_8 + b"where",
                 "Directory does not exist: " + self.dollar(str(elsewhere), "/No", BACKSLASH, "xffwhere")),
                ("an existing directory with no project", b"Plain" + NOT_UTF_8 + b"dir",
                 "No project found at " + self.dollar(str(self.base), "/Plain", BACKSLASH, "xffdir")
                 + "; supply a path or name.")):
            with self.subTest(label):
                self.assert_bare_name_not_found(argument, message, elsewhere)

    # Lead ruling R-89 (b), a fix in region plan carried by this lane.

    def test_clean_the_inspect_cap_remedy_counts_the_entries_that_become_rows(self):
        # N of the inspect-cap remedy counts the registry entries that become
        # rows, as the row cap counts them (contracts/project-clean.md, "Codes";
        # pcl:24; lead ruling R-73 (d)): a bare repository's `bare` entry, and a
        # first entry that is the common directory with no main worktree named,
        # are no rows (D8). Literal evidence, as inspect_repository() shapes it.
        def entry(path, bare=False):
            return {"path": path, "bare": bare}
        linked = [entry(b"/w/%03d" % number) for number in range(129)]
        for label, first, first_is_common_dir, root, rows in (
                ("a bare repository's bare entry", entry(b"/r.git", bare=True), False, None, 129),
                ("the common directory with no main worktree named", entry(b"/r/.git"), True, None, 129),
                ("the common directory with its main worktree named", entry(b"/r/.git"), True, b"/r", 130),
                ("the main worktree", entry(b"/r"), False, b"/r", 130)):
            with self.subTest(label):
                plan = types.SimpleNamespace(mode="all-safe", evidence={
                    "records": [first, *linked], "first_is_common_dir": first_is_common_dir,
                    "identity": {"root": root, "common_dir": b"/r/.git", "dev": 1, "ino": 2}})
                refusal = project.incomplete_refusal(plan, "inspect-cap")
                self.assertEqual((refusal.code, str(refusal)), ("inspect-cap", TEXT["plan_incomplete"].format(
                    CODE="inspect-cap", REMEDY=TEXT["remedy_inspect_cap"].format(N=rows, M=128))))


if __name__ == "__main__":
    unittest.main()
