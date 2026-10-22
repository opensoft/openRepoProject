"""Every run is bounded and says what it omits (feature 004, User Story 6:
T096 to T103).

Sources: the project-clean delta's "Clean reports local worktree state" and
"Clean bounds its Git work and reports omitted work", in
openspec/changes/add-project-clean-all-safe/specs/, and its design D9, D12,
D14 and D18; specs/004-project-clean-all-safe/data-model.md ("Plan", "Revalidation
step and probes_performed", "Target stages", "Exit statuses" and "Constants"),
contracts/project-clean.md ("Order of a run", "Human output", "Plan envelope"
and "Codes") and research.md R8, R10 and R11; lead rulings R-26, R-27, R-29,
R-39, R-67 (a), R-69, R-73 (d), R-75 (g), R-78 (b) and (d), R-80 (P-1 to P-3,
P-5, P-6), R-81 (a) and R-82 (d).

Expected human text comes from clean_support's fixtures (rule 8); counts and
key values are literals written here (rule 11). Every repository is a
disposable fixture under the test's temporary directory, its remote a local
bare repository (rule 4). The caps run at their real sizes, rows registered
directly (rule 6). A time-bound test runs project through the launcher with
its own table, named in its body with the probe budget it yields (rule 5,
lead ruling R-29), and asserts orderings, never wall-clock values; each CLI
run ends inside run_cli's 20 s. Signals go only to a `project` child (rule 7).
"""
import contextlib
import errno
import io
import json
import os
from pathlib import Path
import shlex
import shutil
import time
import unittest
from unittest import mock

import clean_support

project = clean_support.load_project()
TEXT = clean_support.TEXT_FIXTURES
STEPS = clean_support.NEXT_STEP_FIXTURES
REAL_GIT = clean_support.REAL_GIT

# The baseline's freshness text, which says remote information may be stale.
FRESHNESS = "local refs only; remote information is as of the last fetch; no fetch performed"
# The status probe's words after `-C PATH` (design D6), as the contract writes them.
STATUS = ["status", "--porcelain=v1", "-z", "--untracked-files=normal", "--ignored=matching"]
# confirm()'s baseline prompt, which push and delete-branch keep.
CONFIRM = "Type yes to run this plan:"
# The commands an audit must never run.
MUTATING = ("fetch", "pull", "commit", "push", "reset", "stash", "merge", "checkout", "switch", "rebase",
            "update-ref", "prune", "gc")
# The real values in force (data-model.md, "Constants"), written as literals.
BUDGET = {"probe_timeout_seconds": 5, "invocation_timeout_seconds": 60, "reconciliation_reserve_seconds": 10,
          "removal_floor_seconds": 5, "removal_ceiling_seconds": 300, "probe_concurrency": 1}
LIMITS = {"targets": 16, "ignored_entries": 64, "status_records": 4096, "ignored_samples": 8}


def argv_words(record):
    """A counted child's argument vector without its leading -c pins."""
    argv, at = record.argv, 0
    while at + 1 < len(argv) and argv[at] == "-c":
        at += 2
    return argv[at:]


def subcommand(record):
    """A counted child's words after its pins and its `-C DIR`, if any."""
    words = argv_words(record)
    return words[2:] if words[:1] == ["-C"] else words


def directory(record):
    """The `-C DIR` a counted child names, or None."""
    words = argv_words(record)
    return words[1] if words[:1] == ["-C"] else None


def is_removal(record):
    return subcommand(record)[:2] == ["worktree", "remove"]


def status_paths(records):
    """The directory of each status probe in the counting log, in spawn order."""
    return [directory(record) for record in records if subcommand(record) == STATUS]


def codes(document):
    return [refusal["code"] for refusal in document["refusals"]]


def refused(code, remedy):
    """The `REFUSED:` line of a plan incomplete with code."""
    return "REFUSED: " + TEXT["plan_incomplete"].format(CODE=code, REMEDY=remedy) + "\n"


def stages(document):
    """(path, stage, reason) of each target of an apply result record."""
    return [(target["path"], target["stage"], target["reason"]) for target in document["targets"]]


def record(registry_entry_present, path_present, branch_present, branch_sha):
    """A reconciliation record, as project builds it (reconciled derived)."""
    return project.reconciliation_record(registry_entry_present, path_present, branch_present, branch_sha)


def wait_line(path):
    return TEXT["wait_line"].format(PATH=shlex.quote(str(path)))


class Terminal(io.StringIO):
    """A standard input that says it is a terminal, as T046's test uses."""

    def isatty(self):
        return True


class BoundsTests(clean_support.CleanCase):

    # Helpers of this module's own (rule 3).

    def counting(self, hooks=None, real=None, name="counting-bin"):
        """The counting wrapper first on PATH, in front of real (the real git
        by default), with hooks on `worktree remove`: the environment and the
        emptied log."""
        bin_dir, log = self.base / name, self.base / (name + ".log")
        if bin_dir.exists():
            shutil.rmtree(bin_dir)
        clean_support.install_counting_git(bin_dir, log, real=real or REAL_GIT, hooks=hooks)
        clean_support.reset_child_log(log)
        return self.path_first(bin_dir), log

    def snapshot(self, root):
        """What a run that removes nothing leaves unchanged: the registry, every
        ref, and the names and contents of the files of each readable worktree."""
        registry = self.git(root, "worktree", "list", "--porcelain")
        trees = [Path(line[9:]) for line in registry.splitlines() if line.startswith("worktree ")]
        files = {}
        for tree in trees:
            if not os.access(tree.parent, os.X_OK) or not tree.is_dir():
                continue
            for folder, names, filenames in os.walk(tree):
                names[:] = [name for name in names if name != ".git"]
                for name in filenames:
                    path = Path(folder) / name
                    if path.name != ".git":
                        files[str(path)] = path.read_bytes()
        return registry, self.git(root, "for-each-ref", "--format=%(refname) %(objectname)"), files

    def batch(self, case, names):
        """A repository at BASE/CASE/repo with an origin at BASE/CASE/remote.git
        and one merged, clean, published worktree per name at
        BASE/CASE/trees/NAME, in canonical order: (root, trees)."""
        root = self._init_repo(self.base / case / "repo", "main")
        self.bare_remote(root, name=f"{case}/remote.git")
        trees = [self.merged_worktree(name, path=self.base / case / "trees" / name, root=root) for name in names]
        return root, trees

    def head(self, path, ref="HEAD"):
        return self.git(path, "rev-parse", ref).strip()

    def unpushed(self, branch, root=None):
        """A linked worktree of branch, published with `push -u origin`, then
        given one commit of its own: `unpushed`."""
        root = self._root(root)
        tree = self._tree(branch, None)
        self.git(root, "worktree", "add", "-q", "-b", branch, tree)
        self.git(tree, "push", "-q", "-u", "origin", branch)
        self.commit(tree, "one more", allow_empty=True)
        return tree

    def main_in_process(self, *argv, env=None, at_question=None, **patches):
        """project's main(ARGV) in this process: os.environ replaced by env
        (self.env by default), standard input a terminal, ask_removal()
        patched to call at_question() and answer `yes` (as T046 patches it),
        and each named function of project replaced by its stand-in. Returns
        the status, standard output and standard error."""
        def ask(plan, run):
            if at_question is not None:
                at_question()
            return "yes"

        out, err = io.StringIO(), io.StringIO()
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.dict(os.environ, self.env if env is None else env, clear=True))
            stack.enter_context(mock.patch.object(project.sys, "stdin", Terminal()))
            stack.enter_context(mock.patch.object(project, "ask_removal", ask))
            for name, stand_in in patches.items():
                stack.enter_context(mock.patch.object(project, name, stand_in))
            stack.enter_context(contextlib.redirect_stdout(out))
            stack.enter_context(contextlib.redirect_stderr(err))
            status = project.main([os.fsdecode(arg) for arg in argv])
        return status, out.getvalue(), err.getvalue()

    def timed(self, run, *args, **options):
        """run(*args, **options), with the seconds it took as `elapsed`."""
        start = time.monotonic()
        result = run(*args, **options)
        result.elapsed = time.monotonic() - start
        return result

    # T096: "Audit a repository with a feature worktree"; "The plain report
    # exits by completeness"; "An unreadable worktree is one row"; "A failed
    # status probe on the merge-target checkout"; "A failed status in the
    # repository root".

    def test_clean_audit_a_repository_with_a_feature_worktree(self):
        # Pins T052: plain `project clean` reports the main worktree and each
        # linked one, says remote information may be stale, and runs no
        # mutating command.
        root = self.repo()
        self.bare_remote()
        feature = self.base / "feature-tree"
        self.git(root, "worktree", "add", "-q", "-b", "001-feature", feature)
        (feature / "work").write_text("in progress")
        self.commit(feature)
        merged = self.merged_worktree("002-merged")
        before = self.snapshot(root)
        env, log = self.counting()
        result = self.run_cli("clean", root, env=env)
        self.assert_status(result, 0)
        lines = result.stdout.splitlines()
        self.assertEqual(lines[:3], [f"Cleanup plan for {root}", TEXT["merge_target_line"].format(NAME="main",
                                                                                                  SOURCE="main"),
                                     f"Freshness: {FRESHNESS}"])
        rows = [line for line in lines if line.split(": ", 1)[0].replace("-", "").isupper()]
        self.assertEqual([line.split(" dirty=", 1)[0] for line in rows],
                         [f"PROTECTED-DEFAULT: {root} [main]", f"MERGED-REMOVABLE: {merged} [002-merged]",
                          f"UNPUBLISHED: {feature} [001-feature]"], result.stdout)
        records = clean_support.child_log(log)
        self.assertTrue(records)
        for child in records:
            with self.subTest(argv=child.argv):
                words = subcommand(child)
                self.assertNotIn(words[0], MUTATING)
                self.assertNotEqual(words[:2], ["worktree", "remove"])
                self.assertNotEqual(words[:2], ["branch", "-d"])
        document = self.run_json("clean", root, "--json").document
        self.assertEqual((document["mode"], document["tracking_freshness"]), ("report", FRESHNESS))
        self.assertEqual([row["path"] for row in document["worktrees"]], [str(root), str(merged), str(feature)])
        self.assertEqual(self.snapshot(root), before, "nothing fetched, committed, pushed, reset, stashed or removed")

    def test_clean_the_plain_report_exits_by_completeness(self):
        # Rows registered directly (R11); the row counts include the main
        # worktree (lead ruling R-73 (d)): 200 rows are the main worktree and
        # 199 registered, 257 the main worktree and 256.
        root = self.repo()
        self.register_worktrees(199, "r")
        with self.subTest(rows=200):
            result = self.run_json("clean", root, "--json")
            self.assert_status(result, 0)
            document = result.document
            note = {"code": "inspect-cap", "message": TEXT["note_inspect_cap_report"].format(N=200, M=128),
                    "rows": 200}
            self.assertEqual((document["mode"], document["completeness"], document["selected"], document["omitted"],
                              document["notes"], codes(document), document["limits"]["worktree_rows"]),
                             ("report", "complete", None, {"count": 0, "exactness": "exact"}, [note], [], 256))
            self.assertEqual(len(document["worktrees"]), 200)
            human = self.run_cli("clean", root)
            self.assert_status(human, 0)
            self.assertEqual(human.stdout.splitlines()[2:5], [f"Freshness: {FRESHNESS}",
                                                              TEXT["completeness_line_complete"],
                                                              TEXT["selection_line_above_cap"]])
            self.assertEqual(human.stderr, "")
            # --all-safe on the same repository: incomplete with inspect-cap.
            batch = self.run_json("clean", root, "--all-safe", "--json")
            self.assert_status(batch, 1)
            self.assertEqual((batch.document["completeness"], codes(batch.document), batch.document["omitted"]),
                             ("incomplete", ["inspect-cap"], {"count": 72, "exactness": "exact"}))
        self.register_worktrees(57, "s")
        with self.subTest(rows=257):
            result = self.run_json("clean", root, "--json")
            self.assert_status(result, 1)
            document = result.document
            note = {"code": "inspect-cap", "message": TEXT["note_inspect_cap_report"].format(N=257, M=128),
                    "rows": 257}
            self.assertEqual((document["completeness"], codes(document), document["omitted"], document["selected"],
                              document["notes"], document["apply_allowed"]),
                             ("incomplete", ["inspect-cap"], {"count": 1, "exactness": "exact"}, None, [note], False))
            self.assertEqual(len(document["worktrees"]), 256)
            human = self.run_cli("clean", root)
            self.assert_status(human, 1)
            self.assertEqual(human.stdout.splitlines()[3:5], [
                TEXT["completeness_line_incomplete"].format(CODES="inspect-cap"), TEXT["selection_line_above_cap"]])
            self.assertEqual(human.stderr, refused("inspect-cap", TEXT["remedy_inspect_cap"].format(N=257, M=256)))

    @clean_support.not_root
    def test_clean_an_unreadable_worktree_is_one_row(self):
        root = self.repo()
        self.bare_remote()
        merged = self.merged_worktree("001-merged")
        hidden = self.base / "hidden"
        hidden.mkdir()
        tree = self.merged_worktree("002-hidden", path=hidden / "tree")
        hidden.chmod(0o600)
        self.addCleanup(hidden.chmod, 0o700)
        result = self.run_json("clean", root, "--json")
        self.assert_status(result, 1)
        document = result.document
        rows = {row["path"]: row for row in document["worktrees"]}
        error = {"code": "os-error", "message": TEXT["row_error_os_error"].format(
            OPERATION="lstat", STRERROR=os.strerror(errno.EACCES))}
        self.assertEqual([rows[str(tree)][key] for key in ("present", "errors", "classification", "dirty")],
                         [None, [error], "inspection-error", None])
        self.assertEqual({path: row["classification"] for path, row in rows.items() if path != str(tree)},
                         {str(root): "protected-default", str(merged): "merged-removable"}, "every other row")
        self.assertEqual((document["completeness"], codes(document)), ("incomplete", ["inspection-incomplete"]))
        human = self.run_cli("clean", root)
        self.assert_status(human, 1)
        self.assertEqual(human.stdout.splitlines()[3:5], [
            TEXT["completeness_line_incomplete"].format(CODES="inspection-incomplete"),
            TEXT["selection_line"].format(N=1)])
        self.assertEqual(human.stderr, refused("inspection-incomplete", TEXT["remedy_inspection_incomplete"]))

    def test_clean_a_failed_status_probe_on_the_merge_target_checkout(self):
        # The main worktree on a branch of its own, and the merge target, main,
        # checked out in a linked worktree.
        root = self.repo()
        self.git(root, "checkout", "-q", "-b", "work")
        checkout = self.base / "main-tree"
        self.git(root, "worktree", "add", "-q", checkout, "main")
        plain = {row["path"]: row["classification"] for row in self.run_json("clean", root, "--json").document[
            "worktrees"]}
        self.assertEqual(plain[str(checkout)], "protected-default")
        failed = {"code": "probe-failed", "message": TEXT["row_error_probe_failed"].format(
            OPERATION="git status", DETAIL=TEXT["row_error_probe_failed_exit"].format(N=128))}
        # status-hangs-in under the launcher: table probe_budget 1 s (R-29),
        # the rest real, so the probe budget is min(1 s, work remaining).
        table = clean_support.timing_table(probe_budget=1.0)
        timeout = {"code": "probe-timeout", "message": TEXT["row_error_probe_timeout"].format(
            OPERATION="git status", S="1")}
        for kind, timing, error in (("status-fails-in", None, failed), ("status-hangs-in", table, timeout)):
            with self.subTest(kind):
                fake = clean_support.install_fake_git(self.base / kind, kind, path=checkout)
                result = self.run_json("clean", root, "--json", timing=timing, env=self.path_first(fake.parent))
                self.assert_status(result, 1)
                document = result.document
                row = next(row for row in document["worktrees"] if row["path"] == str(checkout))
                self.assertEqual([row[key] for key in ("classification", "dirty", "errors")],
                                 ["inspection-error", None, [error]], "never protected-default")
                self.assertEqual((document["completeness"], codes(document)), ("incomplete", ["inspection-incomplete"]))

    def test_clean_a_failed_status_in_the_repository_root(self):
        root = self.repo()
        self.bare_remote()
        merged = self.merged_worktree("001-merged")
        fake = clean_support.install_fake_git(self.base / "fake", "status-fails-in", path=root)
        env = self.path_first(fake.parent)
        result = self.run_json("clean", root, "--json", env=env)
        self.assert_status(result, 1)
        document = result.document
        rows = {row["path"]: row for row in document["worktrees"]}
        self.assertEqual([rows[str(root)][key] for key in ("classification", "dirty")], ["inspection-error", None])
        self.assertEqual(rows[str(merged)]["classification"], "merged-removable")
        self.assertEqual((document["completeness"], codes(document)), ("incomplete", ["inspection-incomplete"]))
        human = self.run_cli("clean", root, env=env)
        self.assert_status(human, 1)
        self.assertEqual(human.stdout.splitlines()[3],
                         TEXT["completeness_line_incomplete"].format(CODES="inspection-incomplete"))

    # T097: "Row cap and planning failures"; "Twenty rows pass every gate
    # before deferred-target-cap"; "Ignored-file bound".

    def test_clean_row_cap_and_planning_failures(self):
        with self.subTest("129 rows"):
            # The main worktree and 128 registered rows.
            root = self.repo()
            registered = self.register_worktrees(128, "r")
            inspected = [str(root)] + [str(tree) for tree in registered[:127]]
            before = self.snapshot(root)
            env, log = self.counting()
            preview = self.run_json("clean", root, "--all-safe", "--json", env=env)
            self.assert_status(preview, 1)
            document = preview.document
            self.assertEqual((document["completeness"], codes(document), document["omitted"]),
                             ("incomplete", ["inspect-cap"], {"count": 1, "exactness": "exact"}))
            self.assertEqual([row["path"] for row in document["worktrees"]], inspected)
            self.assertEqual(status_paths(clean_support.child_log(log)), inspected,
                             "the status children: the main worktree and the 127 smallest paths")
            message = refused("inspect-cap", TEXT["remedy_inspect_cap"].format(N=129, M=128))
            human = self.run_cli("clean", root, "--all-safe")
            self.assert_status(human, 1)
            self.assertEqual(human.stderr, message)
            clean_support.reset_child_log(log)
            applied = self.run_cli("clean", root, "--all-safe", "--apply", "--yes", env=env)
            self.assert_status(applied, 2)
            self.assertEqual(applied.stderr, message)
            self.assertEqual([child for child in clean_support.child_log(log) if is_removal(child)], [])
            self.assertEqual(self.snapshot(root), before)

        with self.subTest("a status probe times out"):
            # status-hangs-in under the launcher: table probe_budget 1 s (R-29),
            # the rest real.
            root, (slow, other) = self.batch("timeout", ["001-slow", "002-other"])
            fake = clean_support.install_fake_git(self.base / "timeout-bin", "status-hangs-in", path=slow)
            table = clean_support.timing_table(probe_budget=1.0)
            result = self.run_json("clean", root, "--all-safe", "--json", timing=table, env=self.path_first(fake.parent))
            self.assert_status(result, 1)
            document = result.document
            row = next(row for row in document["worktrees"] if row["path"] == str(slow))
            self.assertEqual((row["classification"], row["errors"]), ("inspection-error", [{
                "code": "probe-timeout",
                "message": TEXT["row_error_probe_timeout"].format(OPERATION="git status", S="1")}]))
            self.assertIn({"path": str(slow), "path_valid_utf8": True, "branch": "001-slow",
                           "classification": "inspection-error", "reason": "inspection-error"}, document["excluded"])
            self.assertEqual((document["completeness"], codes(document)), ("incomplete", ["inspection-incomplete"]))
            self.assertEqual([entry["path"] for entry in document["selected"]], [str(other)])

        with self.subTest("the work deadline passes during planning"):
            # The first linked row's status probe hangs, under a table that
            # shortens the deadline to 3 s and the reserve to 1 s: 2 s of work,
            # and the probe budget min(5 s, work remaining), so that probe is
            # cut at the work deadline and every later row's is not started.
            root, trees = self.batch("deadline", ["001-hang", "002-later", "003-last"])
            fake = clean_support.install_fake_git(self.base / "deadline-bin", "status-hangs-in", path=trees[0])
            env = self.path_first(fake.parent)
            table = clean_support.timing_table(invocation_deadline=3.0, reconciliation_reserve=1.0)
            before = self.snapshot(root)
            result = self.timed(self.run_json, "clean", root, "--all-safe", "--json", timing=table, env=env)
            self.assert_status(result, 1)
            document = result.document
            cut = [{"code": "deadline-exceeded",
                    "message": TEXT["row_error_deadline_exceeded"].format(OPERATION="git status")}]
            rows = {row["path"]: row for row in document["worktrees"]}
            self.assertEqual(rows[str(root)]["classification"], "protected-default")
            for tree in trees:
                self.assertEqual((rows[str(tree)]["classification"], rows[str(tree)]["errors"]),
                                 ("inspection-error", cut), tree)
            self.assertEqual(sorted((entry["path"], entry["reason"]) for entry in document["excluded"]),
                             sorted([(str(root), "main-worktree")] + [(str(tree), "inspection-error") for tree in trees]))
            self.assertEqual((document["completeness"], codes(document)), ("incomplete", ["deadline-exceeded"]),
                             f"elapsed {result.elapsed:.1f} s")
            applied = self.timed(self.run_launched, table, "clean", root, "--all-safe", "--apply", "--yes", env=env)
            self.assert_status(applied, 2)
            self.assertEqual(applied.stderr, refused("deadline-exceeded", TEXT["remedy_deadline_exceeded"]),
                             f"elapsed {applied.elapsed:.1f} s")
            self.assertEqual(self.snapshot(root), before)

    def test_clean_row_cap_and_planning_failures_an_unreadable_realpath_in_single_mode(self):
        # Lead ruling R-78 (b): 129 rows registered directly and P, a merged
        # worktree whose path sorts last; the realpath read of one other entry
        # fails during P's match. P's match is then undecided, no entry is
        # exempt from the cap, and the plan inspects at most 128 rows, the
        # main worktree and the 127 smallest paths (lead ruling R-73 (d)); it
        # refuses with inspection-incomplete, exit 2, and P stays.
        root = self.repo()
        self.bare_remote()
        registered = self.register_worktrees(129, "r")
        target = self.merged_worktree("p", path=self.base / "zz-p")
        self.assertEqual(sorted(map(os.fsencode, registered + [target]))[-1], os.fsencode(target))
        other = os.fsencode(registered[5])
        original, failed = project._bounded_realpath, []

        def bounded(path):
            if path == other:
                failed.append(path)
                return None
            return original(path)

        asked = AssertionError("the run reached the question stage")
        status, out, err = self.main_in_process(
            "clean", root, "--apply", "--action", "remove", "--worktree", target, "--yes", "--json",
            _bounded_realpath=bounded, confirm_removal=mock.Mock(side_effect=asked),
            apply_removals=mock.Mock(side_effect=asked))
        self.assertEqual((status, failed), (2, [other]), err)
        document = json.loads(out)
        inspected = [str(root)] + [str(tree) for tree in registered[:127]]
        self.assertEqual([row["path"] for row in document["worktrees"]], inspected, "at most 128 rows")
        self.assertEqual((codes(document), document["selected"], document["completeness"]),
                         (["inspection-incomplete"], [], "incomplete"))
        self.assertTrue(target.is_dir())

    def test_clean_twenty_rows_pass_every_gate_before_deferred_target_cap(self):
        root, trees = self.batch("twenty", [f"{number:03d}-row" for number in range(1, 21)])
        shown = shlex.quote(str(root))
        preview = self.run_cli("clean", root, "--all-safe")
        self.assert_status(preview, 0)
        lines = preview.stdout.splitlines()
        at = lines.index(TEXT["deferral_line"].format(K=4, ROOT=shown))
        self.assertEqual(lines[at + 1:at + 5], [TEXT["excluded_row"].format(PATH=tree, BRANCH=tree.name)
                                                for tree in trees[16:]])
        self.assertIn(TEXT["selected_heading"].format(N=16), lines)
        drain = TEXT["non_drain_line"].split("{REASONS}")[0]
        self.assertEqual([line for line in lines if line.startswith(drain)], [], "no drain line")
        document = self.run_json("clean", root, "--all-safe", "--json").document
        self.assertEqual((document["completeness"], document["apply_allowed"], codes(document)), ("complete", True, []))
        self.assertEqual([entry["path"] for entry in document["selected"]], [str(tree) for tree in trees[:16]])
        self.assertEqual([(entry["path"], entry["reason"]) for entry in document["excluded"]
                          if entry["reason"] != "main-worktree"],
                         [(str(tree), "deferred-target-cap") for tree in trees[16:]])
        result = self.run_json("clean", root, "--all-safe", "--apply", "--yes", "--json")
        self.assert_status(result, 0)
        self.assertEqual(stages(result.document), [(str(tree), "removed", None) for tree in trees[:16]])
        self.assertEqual([tree.exists() for tree in trees], [False] * 16 + [True] * 4)
        again = self.run_json("clean", root, "--all-safe", "--apply", "--yes", "--json")
        self.assert_status(again, 0)
        self.assertEqual(stages(again.document), [(str(tree), "removed", None) for tree in trees[16:]])
        self.assertFalse(any(tree.exists() for tree in trees))

        with self.subTest("seventeen rows holding gitlinks"):
            # Its own repository: a worktree added after a gitlink is merged
            # holds that gitlink too.
            held_root = self._init_repo(self.base / "gitlinks" / "repo", "main")
            self.bare_remote(held_root, name="gitlinks/remote.git")
            held = [self.merged_worktree(f"{number:03d}-held", path=self.base / "gitlinks" / "trees" / f"{number:03d}-held",
                                         root=held_root,
                                         setup=lambda tree, number=number: self.gitlink(tree, f"vendored-{number:03d}"))
                    for number in range(1, 18)]
            preview = self.run_cli("clean", held_root, "--all-safe")
            self.assert_status(preview, 0)
            lines = preview.stdout.splitlines()
            self.assertIn(TEXT["excluded_group"].format(REASON="contains-submodule", K=16,
                                                        NEXT_STEP=STEPS["contains-submodule"]), lines)
            at = lines.index(TEXT["deferral_line"].format(K=1, ROOT=shlex.quote(str(held_root))))
            # R-146 (W21 L-f): REASONS is contains-submodule alone, so the line
            # reads as it did before REASONS was added, with lane 3's W59 G-4
            # clause, since Git removes these 16 only with --force.
            line = TEXT["non_drain_line"].format(REASONS="contains-submodule")
            self.assertEqual(line, "  these deferred rows will not drain while the 16 rows ahead of them are "
                                   "contains-submodule; review those worktrees, then remove them yourself "
                                   "(--force for any that holds a submodule)")
            self.assertEqual(lines[at + 1:at + 3], [line, TEXT["excluded_row"].format(PATH=held[16],
                                                                                      BRANCH=held[16].name)])
            document = self.run_json("clean", held_root, "--all-safe", "--json").document
            self.assertEqual((document["completeness"], document["selected"]), ("complete", []))
            self.assertEqual([(entry["path"], entry["reason"]) for entry in document["excluded"]
                              if entry["reason"] != "main-worktree"],
                             [(str(tree), "contains-submodule") for tree in held[:16]]
                             + [(str(held[16]), "deferred-target-cap")])

    def test_clean_deferred_rows_that_will_not_drain_name_the_gates_after_the_cap(self):
        # Design D12 and D18 as R-146 (W21 L-f) amends them: when every one of
        # the 16 rows taken past the cap is excluded by a gate after it, the
        # drain line names their reasons, each once, in gate order, joined by
        # ", ". Seventeen rows: the first sixteen split between
        # hidden-local-state, operation-in-progress and worktree-only-commits,
        # the seventeenth deferred.
        root, trees = self.batch("mixed", [f"{number:03d}-row" for number in range(1, 18)])
        common = Path(self.git(root, "rev-parse", "--path-format=absolute", "--git-common-dir").strip())
        expected = {}
        for number, tree in enumerate(trees[:16]):
            if number % 3 == 0:
                self.git(tree, "update-index", "--assume-unchanged", f"work-{tree.name}")
                expected[str(tree)] = "hidden-local-state"
            elif number % 3 == 1:
                (common / "worktrees" / tree.name / "MERGE_HEAD").write_text(self.head(root) + "\n")
                expected[str(tree)] = "operation-in-progress"
            else:
                held = self.git(tree, "commit-tree", "HEAD^{tree}", "-p", "HEAD", "-m", "kept").strip()
                self.git(tree, "update-ref", "refs/worktree/keep", held)
                expected[str(tree)] = "worktree-only-commits"
        preview = self.run_cli("clean", root, "--all-safe")
        self.assert_status(preview, 0)
        lines = preview.stdout.splitlines()
        at = lines.index(TEXT["deferral_line"].format(K=1, ROOT=shlex.quote(str(root))))
        self.assertEqual(lines[at + 1:at + 3], [
            TEXT["non_drain_line"].format(REASONS="hidden-local-state, operation-in-progress, worktree-only-commits"),
            TEXT["excluded_row"].format(PATH=trees[16], BRANCH=trees[16].name)])
        document = self.run_json("clean", root, "--all-safe", "--json").document
        self.assertEqual((document["completeness"], document["selected"]), ("complete", []))
        self.assertEqual({entry["path"]: entry["reason"] for entry in document["excluded"]
                          if entry["reason"] != "main-worktree"},
                         {**expected, str(trees[16]): "deferred-target-cap"})

    def test_clean_ignored_file_bound(self):
        # Pins the parsers and the evidence model of Phase 2.
        root = self.repo()
        self.bare_remote()

        def ignore(tree):
            (tree / ".gitignore").write_text("*.ignored\n")

        seventy = self.merged_worktree("001-seventy", setup=ignore)
        exact = self.merged_worktree("002-exact", setup=ignore)
        untracked = self.merged_worktree("003-untracked")
        for tree, count in ((seventy, 70), (exact, 64)):
            for number in range(count):
                (tree / f"{number:03d}.ignored").write_text("")
        for number in range(4097):
            (untracked / f"untracked-{number:04d}").write_text("")
        result = self.run_json("clean", root, "--all-safe", "--json")
        self.assert_status(result, 0)
        document = result.document
        rows = {row["path"]: row for row in document["worktrees"]}
        excluded = {entry["path"]: entry["reason"] for entry in document["excluded"]}
        keys = ("ignored_files", "ignored_files_truncated", "classification")
        self.assertEqual([rows[str(seventy)][key] for key in keys], [64, True, "ignored-local-files"])
        self.assertEqual(len(rows[str(seventy)]["ignored_samples"]), 8)
        self.assertEqual([rows[str(exact)][key] for key in keys], [64, False, "ignored-local-files"])
        self.assertEqual([rows[str(untracked)][key] for key in keys + ("dirty",)], [None, True, "dirty", True])
        self.assertEqual((excluded[str(seventy)], excluded[str(exact)], excluded[str(untracked)]),
                         ("ignored-local-files", "ignored-local-files", "dirty"))
        self.assertEqual(document["completeness"], "complete")

    # T098: "Bounded revalidation work"; "Deadline expiry mid-batch"; "Push
    # refuses an incomplete inspection", its deadline clause; the budget in
    # force (lead ruling R-39).

    def test_clean_bounded_revalidation_work(self):
        # Five rows: the main worktree, three selected targets and a merged
        # worktree made dirty, not selected; --all-safe --apply --yes under
        # the counting wrapper and the real table (R-29). The plan's estimate
        # gives the boundary in the log: planning's children are
        # probes.estimated - 6T - 3 (research.md R8; D7 and D14 as LQ-13
        # amends them).
        root, trees = self.batch("bounded", ["001-a", "002-b", "003-c"])
        dirty = self.merged_worktree("004-dirty", path=self.base / "bounded" / "trees" / "004-dirty", root=root)
        (dirty / "uncommitted").write_text("keep")
        self.assert_bounded_revalidation(root, trees, per_target=6, row_probes=("status", "ls-files", "rev-list"))

    def test_clean_bounded_revalidation_work_where_row_4c_reads_true(self):
        # The same five rows in a repository whose `extensions.worktreeConfig`
        # is true (LQ-11): each target's revalidation adds its effective-work-tree
        # probe, seven children in all (the project-clean delta's "at most six
        # Git children, seven where the plan read the repository's
        # extensions.worktreeConfig as true"), and the estimate counts seven.
        root, trees = self.batch("bounded-4c", ["001-a", "002-b", "003-c"])
        dirty = self.merged_worktree("004-dirty", path=self.base / "bounded-4c" / "trees" / "004-dirty", root=root)
        (dirty / "uncommitted").write_text("keep")
        self.git(root, "config", "extensions.worktreeConfig", "true")
        self.assert_bounded_revalidation(root, trees, per_target=7,
                                         row_probes=("rev-parse", "status", "ls-files", "rev-list"))

    def assert_bounded_revalidation(self, root, trees, per_target, row_probes):
        """--all-safe --apply --yes --json over trees, three selected targets:
        every revalidation spawns per_target children, the repository's three
        (rescan-shared after the first) and then row_probes in the target, the
        final rescan three, and probes.estimated equals probes.performed."""
        env, log = self.counting()
        result = self.run_json("clean", root, "--all-safe", "--apply", "--yes", "--json", env=env)
        self.assert_status(result, 0)
        document = result.document
        self.assertEqual(stages(document), [(str(tree), "removed", None) for tree in trees])
        records = clean_support.child_log(log)
        probes, operations, targets = document["probes"], document["operations"], len(trees)
        planning = probes["estimated"] - per_target * targets - 3
        planned, after = records[:planning], records[planning:]
        self.assertFalse(any(map(is_removal, planned)))
        self.assertEqual(subcommand(planned[-1])[:1], ["rev-list"], "planning ends with the reachability probes")
        # F + W + E + 6T + 3 (plan review M7): W the status probes, E the
        # hidden-state probes, F every other planning child, the reachability
        # probes among them.
        kinds = [subcommand(child)[:1] for child in planned]
        self.assertEqual((kinds.count(["status"]), kinds.count(["ls-files"]), kinds.count(["rev-list"])), (5, 3, 3))
        at = [index for index, child in enumerate(after) if is_removal(child)]
        self.assertEqual(len(at), 3, "three removals run")
        segments = [after[:at[0]], after[at[0] + 1:at[1]], after[at[1] + 1:at[2]], after[at[2] + 1:]]
        words = [[subcommand(child)[0] for child in segment] for segment in segments]
        for segment in words[:3]:
            self.assertEqual(segment, ["rev-parse", "worktree", "for-each-ref", *row_probes])
        self.assertEqual(words[3], ["rev-parse", "worktree", "for-each-ref"], "the final rescan spawns three")
        performed = [target["probes_performed"] for target in document["targets"]]
        self.assertEqual(performed, [per_target] * 3, f"at most {per_target} children per revalidation")
        # After confirmation: no merged-set listing and no status probe of a
        # worktree not selected.
        self.assertFalse(any(any(word.startswith("--merged") for word in subcommand(child)) for child in after))
        self.assertEqual(set(status_paths(after)), {str(tree) for tree in trees})
        # Every status, ls-files and rev-list child, and every effective-work-tree
        # probe, names its own worktree; every other child after resolution,
        # the removals included, the command directory.
        rows = {row["path"] for row in json.loads(self.run_cli("clean", root, "--json").stdout)["worktrees"]}
        rows |= {str(tree) for tree in trees}
        for child in records:
            with self.subTest(argv=child.argv):
                if argv_words(child) == ["--version"]:
                    continue
                if subcommand(child)[0] in ("status", "ls-files", "rev-list") or subcommand(child) == [
                        "rev-parse", "--path-format=absolute", "--show-toplevel"]:
                    self.assertIn(directory(child), rows)
                else:
                    self.assertEqual(directory(child), str(root))
        # The counts (lead ruling R-27): probes every child but the removals,
        # operations the removals; the record's probes.performed is the
        # planning's count, each target's probes_performed and the final
        # rescan (data-model.md, "Revalidation step and probes_performed"),
        # and the estimate is its upper bound, met here.
        removals = [child for child in records if is_removal(child)]
        self.assertEqual(probes["performed"], len(records) - len(removals))
        self.assertEqual(operations, {"estimated": 3, "performed": len(removals)})
        self.assertEqual(probes["performed"], planning + sum(performed) + len(segments[3]))
        self.assertEqual(probes["estimated"], planning + per_target * targets + 3)
        self.assertEqual(probes["performed"], probes["estimated"])

    def test_clean_deadline_expiry_mid_batch(self):
        # Through the launcher with tables that shorten the deadline, the
        # reserve and the floor (R-29); the probe budget is min(5 s, work
        # remaining), or of the reserve remaining while reconciling. A removal
        # is slowed by the counting wrapper's pre-hook for one target alone,
        # which records any signal that reaches it.
        def slow(log, name, seconds):
            return {"pre": f'case "$target" in */{name}) echo start >> {shlex.quote(str(log))}; '
                           f"trap 'echo TERM >> {shlex.quote(str(log))}' TERM; "
                           f"trap 'echo INT >> {shlex.quote(str(log))}' INT; "
                           f"trap 'echo HUP >> {shlex.quote(str(log))}' HUP; "
                           f"sleep {seconds}; echo done >> {shlex.quote(str(log))};; esac"}

        names = ["001-p", "002-q", "003-r"]
        with self.subTest("the second removal outlives the work deadline"):
            # Table: deadline 4 s, reserve 1 s (3 s of work), floor 0.5 s. The
            # second removal sleeps 4 s, so it ends past the work deadline and
            # past the planned end of the reserve, which then counts from its
            # exit.
            root, trees = self.batch("outlives", names)
            planned = {tree: self.head(tree) for tree in trees}
            hook = self.base / "outlives.hook"
            env, log = self.counting(slow(hook, names[1], 4), name="outlives-bin")
            table = clean_support.timing_table(invocation_deadline=4.0, reconciliation_reserve=1.0, removal_floor=0.5)
            result = self.timed(self.run_json, "clean", root, "--all-safe", "--apply", "--yes", "--json",
                                timing=table, env=env)
            self.assert_status(result, 1)
            document = result.document
            self.assertEqual(stages(document), [(str(trees[0]), "removed", None), (str(trees[1]), "removed", None),
                                                (str(trees[2]), "not-attempted", "deadline-exceeded")],
                             f"elapsed {result.elapsed:.1f} s\n{result.stderr}")
            second, third = document["targets"][1:]
            self.assertEqual(second["reconciliation"], record(False, False, True, planned[trees[1]]))
            self.assertEqual((third["reconciliation"], third["exit_status"], third["probes_performed"]), (None, None, 0))
            self.assertEqual(hook.read_text(), "start\ndone\n", "the removal was not signalled and was waited for")
            self.assertEqual(result.stderr.splitlines().count(wait_line(trees[1])), 1, result.stderr)
            self.assertEqual(len([child for child in clean_support.child_log(log) if is_removal(child)]), 2)
            self.assertEqual([tree.exists() for tree in trees], [False, False, True])
            self.assertEqual(self.head(root, "refs/heads/" + names[1]), planned[trees[1]], "the branch is kept")

        with self.subTest("the first removal leaves less than the floor"):
            # Table: deadline 6 s, reserve 1 s (5 s of work), floor 3 s. The
            # first removal sleeps 3 s, so less than 3 s of work remains when it
            # ends: no second removal child.
            root, trees = self.batch("floor-first", names)
            hook = self.base / "floor-first.hook"
            env, log = self.counting(slow(hook, names[0], 3), name="floor-first-bin")
            table = clean_support.timing_table(invocation_deadline=6.0, reconciliation_reserve=1.0, removal_floor=3.0)
            result = self.timed(self.run_json, "clean", root, "--all-safe", "--apply", "--yes", "--json",
                                timing=table, env=env)
            self.assert_status(result, 1)
            document = result.document
            self.assertEqual(stages(document), [(str(trees[0]), "removed", None)] + [
                (str(tree), "not-attempted", "deadline-exceeded") for tree in trees[1:]],
                f"elapsed {result.elapsed:.1f} s\n{result.stderr}")
            for target in document["targets"][1:]:
                self.assertEqual((target["reconciliation"], target["exit_status"], target["probes_performed"]),
                                 (None, None, 0))
            self.assertEqual(len([child for child in clean_support.child_log(log) if is_removal(child)]), 1,
                             "no second child")
            self.assertEqual([tree.exists() for tree in trees], [False, True, True])

        with self.subTest("the second passes revalidation with less than the floor left"):
            # Table: deadline 6 s, reserve 1 s (5 s of work), floor 3 s, the
            # probe budget min(5 s, work remaining). Once the first removal has
            # run, the second target's status probe sleeps 3 s before it runs:
            # its revalidation starts with more than 3 s of work left and passes,
            # and less than 3 s is left at the seam before its spawn.
            root, trees = self.batch("floor-seam", names)
            fake_dir = self.base / "floor-seam-fake"
            fake_dir.mkdir()
            marker = fake_dir / "removed.marker"
            script = (f"#!/bin/sh\nreal={shlex.quote(REAL_GIT)}\nmarker={shlex.quote(str(marker))}\n"
                      'case " $* " in *" worktree remove "*) "$real" "$@"; status=$?; : > "$marker"; '
                      "exit $status;; esac\n"
                      'if [ -e "$marker" ]; then prev=\n'
                      '  for a in "$@"; do\n'
                      f'    if [ "x$prev" = "x-C" ] && [ "x$a" = x{shlex.quote(str(trees[1]))} ]; then\n'
                      '      case " $* " in *" status "*) sleep 3;; esac\n'
                      "    fi\n"
                      "    prev=$a\n"
                      "  done\n"
                      'fi\nexec "$real" "$@"\n')
            (fake_dir / "git").write_text(script)
            (fake_dir / "git").chmod(0o755)
            env, log = self.counting(real=fake_dir / "git", name="floor-seam-bin")
            table = clean_support.timing_table(invocation_deadline=6.0, reconciliation_reserve=1.0, removal_floor=3.0)
            result = self.timed(self.run_json, "clean", root, "--all-safe", "--apply", "--yes", "--json",
                                timing=table, env=env)
            self.assert_status(result, 1)
            document = result.document
            self.assertEqual(stages(document), [(str(trees[0]), "removed", None)] + [
                (str(tree), "not-attempted", "deadline-exceeded") for tree in trees[1:]],
                f"elapsed {result.elapsed:.1f} s\n{result.stderr}")
            second, third = document["targets"][1:]
            self.assertEqual((second["reconciliation"], second["exit_status"], second["probes_performed"]),
                             (None, None, 6), "revalidated, its six children (D7, LQ-13), never spawned")
            self.assertEqual((third["reconciliation"], third["exit_status"], third["probes_performed"]), (None, None, 0))
            self.assertEqual(len([child for child in clean_support.child_log(log) if is_removal(child)]), 1,
                             "no second child")
            self.assertEqual([tree.exists() for tree in trees], [False, True, True])

    def test_clean_deadline_expiry_mid_batch_a_rescan_read_cut_at_the_deadline(self):
        # Lead ruling R-82 (d): a real deadline cut, end to end through the
        # CLI. Table: deadline 3 s, reserve 1 s (2 s of work), floor 0.5 s,
        # the probe budget min(5 s, work or reserve remaining). The removal
        # sleeps 3 s in the counting wrapper's pre-hook, so it ends past the
        # planned end of the reserve; the reserve then counts from its exit
        # (T099), the rescan's identity probe runs, and its registry listing,
        # which the slow-after-remove fake makes hang, is cut at the reserve's
        # end: the record is unfinished, the target unknown.
        root, (tree,) = self.batch("rescan-cut", ["001-p"])
        planned = self.head(tree)
        fake = clean_support.install_fake_git(self.base / "rescan-cut-fake", "slow-after-remove", lifetime=30)
        env, log = self.counting({"pre": "sleep 3"}, real=fake, name="rescan-cut-bin")
        table = clean_support.timing_table(invocation_deadline=3.0, reconciliation_reserve=1.0, removal_floor=0.5)
        result = self.timed(self.run_json, "clean", root, "--all-safe", "--apply", "--yes", "--json",
                            timing=table, env=env)
        self.assert_status(result, 1)
        [target] = result.document["targets"]
        self.assertEqual((target["stage"], target["reason"], target["exit_status"]),
                         ("unknown", "reconciliation-incomplete", 0), f"elapsed {result.elapsed:.1f} s")
        self.assertEqual(target["reconciliation"], record(None, None, None, None))
        records = clean_support.child_log(log)
        at = next(index for index, child in enumerate(records) if is_removal(child))
        self.assertEqual([subcommand(child)[0] for child in records[at + 1:]], ["rev-parse", "worktree"],
                         "the identity probe, then the registry listing cut; no ref listing")
        self.assertEqual(result.stderr.splitlines().count(wait_line(tree)), 1, result.stderr)
        self.assertFalse(tree.exists())
        self.assertEqual(self.head(root, "refs/heads/001-p"), planned, "the branch is kept")

    def test_clean_deadline_expiry_mid_batch_a_revalidation_read_cut_at_the_deadline(self):
        # Lead ruling R-80, P-2 (interim row 7's closure; lane 3's
        # reval-deadline-cut and LOW-2, lead ruling R-93 (e)): a revalidation
        # read the work deadline cuts is no difference. Table: deadline 8 s,
        # reserve 2 s (6 s of work), probe budget 30 s and grace 1 s, so each
        # probe's budget is min(30 s, work remaining) and the work deadline is
        # the limit. The ls-files-stuck-again-in fake, behind the counting
        # wrapper, lets planning's hidden-state probe of the first target run;
        # the revalidation's ignores SIGTERM and sleeps, is cut at the work
        # deadline and killed after the grace. Both targets are then
        # not-attempted with deadline-exceeded and no reconciliation, nothing
        # is removed, and the exit status is 1 (D19, row 2).
        root, trees = self.batch("reval-deadline-cut", ["001-p", "002-q"])
        before = self.snapshot(root)
        fake = clean_support.install_fake_git(self.base / "reval-deadline-cut-fake", "ls-files-stuck-again-in",
                                              path=trees[0], lifetime=30)
        env, log = self.counting(real=fake, name="reval-deadline-cut-bin")
        table = clean_support.timing_table(invocation_deadline=8.0, reconciliation_reserve=2.0, probe_budget=30.0,
                                           term_grace=1.0)
        result = self.timed(self.run_json, "clean", root, "--all-safe", "--apply", "--yes", "--json",
                            timing=table, env=env)
        self.assert_status(result, 1)
        document = result.document
        self.assertEqual(stages(document), [(str(tree), "not-attempted", "deadline-exceeded") for tree in trees],
                         f"elapsed {result.elapsed:.1f} s\n{result.stderr}")
        first, second = document["targets"]
        # The first target's revalidation ran five of its six children (D7, as
        # LQ-13 amends it), the hidden-state probe last and cut; the second was
        # never revalidated.
        self.assertEqual((first["reconciliation"], first["exit_status"], first["probes_performed"]), (None, None, 5))
        self.assertEqual((second["reconciliation"], second["exit_status"], second["probes_performed"]),
                         (None, None, 0))
        self.assertEqual(document["exit_code"], 1)
        records = clean_support.child_log(log)
        self.assertEqual([directory(child) for child in records if subcommand(child)[:1] == ["ls-files"]].count(
            str(trees[0])), 2, "planning's hidden-state probe of the first target, then the revalidation's")
        self.assertEqual((subcommand(records[-1])[:1], directory(records[-1])), (["ls-files"], str(trees[0])),
                         "the cut read is the run's last child: no removal, no rescan")
        self.assertFalse(any(map(is_removal, records)))
        self.assertEqual(self.snapshot(root), before, "nothing removed")

    def test_clean_deadline_expiry_mid_batch_a_revalidation_read_cut_at_its_probe_budget(self):
        # The contrast (lead ruling R-80, P-2; lane 3's reval-budget-cut; R-93
        # (e)): the same stuck hidden-state probe, cut by a 1 s probe budget,
        # the rest of the table real (work deadline 50 s, grace 2 s), so the
        # budget is the limit and the read times out. A timeout stays a
        # difference (T084; the project-clean-review-safety delta, rs:92-93),
        # state-changed as for every revalidation child that decides nothing
        # (the lead's R-195): the first target is refused with it, its record from
        # its revalidation's reads, the second is not-attempted with
        # batch-stopped, nothing is removed, and the exit status is 2.
        root, trees = self.batch("reval-budget-cut", ["001-p", "002-q"])
        planned = self.head(trees[0])
        before = self.snapshot(root)
        fake = clean_support.install_fake_git(self.base / "reval-budget-cut-fake", "ls-files-stuck-again-in",
                                              path=trees[0], lifetime=30)
        env, log = self.counting(real=fake, name="reval-budget-cut-bin")
        table = clean_support.timing_table(probe_budget=1.0)
        result = self.timed(self.run_json, "clean", root, "--all-safe", "--apply", "--yes", "--json",
                            timing=table, env=env)
        self.assert_status(result, 2)
        document = result.document
        self.assertEqual(stages(document), [(str(trees[0]), "refused", "state-changed"),
                                            (str(trees[1]), "not-attempted", "batch-stopped")],
                         f"elapsed {result.elapsed:.1f} s\n{result.stderr}")
        first, second = document["targets"]
        self.assertEqual((first["reconciliation"], first["exit_status"], first["probes_performed"]),
                         (record(True, True, True, planned), None, 5))
        self.assertEqual((second["reconciliation"], second["probes_performed"]), (None, 0))
        self.assertEqual(document["exit_code"], 2)
        records = clean_support.child_log(log)
        self.assertEqual((subcommand(records[-1])[:1], directory(records[-1])), (["ls-files"], str(trees[0])))
        self.assertFalse(any(map(is_removal, records)))
        self.assertEqual(self.snapshot(root), before, "nothing removed")

    def test_clean_push_refuses_an_incomplete_inspection_deadline(self):
        # At a pseudo-terminal made project's controlling terminal (rule 14),
        # through the launcher. status-hangs-in stands first on PATH, behind
        # the counting wrapper, naming a path no child names, so every child
        # passes through; at `Type yes` it is reinstalled naming the push's
        # worktree, so the full re-inspection's status probe of that row
        # hangs into the work deadline (lead ruling R-80, P-1).
        root = self.repo()
        remote = self.bare_remote()
        tree = self.unpushed("001-feature")
        self.git(root, "worktree", "add", "-q", "-b", "002-other", self.base / "002-other-tree")
        pushed = self.head(remote, "refs/heads/001-feature")
        fake_dir = self.base / "fake-bin"
        nowhere = self.base / "nowhere"
        clean_support.install_fake_git(fake_dir, "status-hangs-in", path=nowhere)
        env, log = self.counting(real=fake_dir / "git")

        def pushes():
            return [child for child in clean_support.child_log(log) if subcommand(child)[:1] == ["push"]]

        def hang(running):
            clean_support.install_fake_git(fake_dir, "status-hangs-in", path=tree)

        # Table: deadline 6 s, reserve 1 s (5 s of work); the probe budget
        # min(5 s, work remaining).
        table = clean_support.timing_table(invocation_deadline=6.0, reconciliation_reserve=1.0)
        argv = clean_support.launched_argv(table, "clean", root, "--apply", "--action", "push", "--branch",
                                           "001-feature")
        result = self.timed(self.run_pty_steps, argv, [(CONFIRM, hang), ("", "yes")], controlling_tty=True, env=env)
        self.assert_status(result, 2)
        self.assertEqual(result.stderr, f"{CONFIRM} " + refused("deadline-exceeded", TEXT["remedy_deadline_exceeded"]),
                         f"elapsed {result.elapsed:.1f} s")
        self.assertEqual(pushes(), [], "no push child")
        self.assertEqual(self.head(remote, "refs/heads/001-feature"), pushed)

        with self.subTest("yes answered after the deadline: the clock was paused at the question"):
            # Table: deadline 3 s, reserve 1 s (2 s of work); the answer comes
            # 3.5 s after the question, past the whole deadline.
            clean_support.install_fake_git(fake_dir, "status-hangs-in", path=nowhere)
            clean_support.reset_child_log(log)
            table = clean_support.timing_table(invocation_deadline=3.0, reconciliation_reserve=1.0)
            argv = clean_support.launched_argv(table, "clean", root, "--apply", "--action", "push", "--branch",
                                               "001-feature")
            result = self.run_pty_steps(argv, [(CONFIRM, lambda running: time.sleep(3.5)), ("", "yes")],
                                        controlling_tty=True, env=env)
            self.assert_status(result, 0)
            self.assertEqual(len(pushes()), 1)
            self.assertEqual(self.head(remote, "refs/heads/001-feature"), self.head(tree))

    def test_clean_budget_reports_the_values_in_force(self):
        # It pins T049 and T051 (lead ruling R-39): unscaled, the real values;
        # under the launcher, the values of the test's own table.
        root = self.repo()
        self.bare_remote()
        target = self.merged_worktree("001-merged")
        for words, cap in (((), 256), (("--all-safe",), 128),
                           (("--apply", "--action", "remove", "--worktree", target), 128)):
            with self.subTest(arguments=[os.fsdecode(word) for word in words]):
                document = self.run_json("clean", root, *words, "--json").document
                self.assertEqual(list(document["budget"].items()), list(BUDGET.items()))
                self.assertEqual(document["limits"], {"worktree_rows": cap, **LIMITS})
        table = clean_support.timing_table(probe_budget=7, invocation_deadline=90, reconciliation_reserve=11,
                                           removal_floor=6, removal_ceiling=301)
        document = self.run_json("clean", root, "--all-safe", "--json", timing=table).document
        self.assertEqual(document["budget"], {
            "probe_timeout_seconds": 7, "invocation_timeout_seconds": 90, "reconciliation_reserve_seconds": 11,
            "removal_floor_seconds": 6, "removal_ceiling_seconds": 301, "probe_concurrency": 1})
        self.assertEqual(document["limits"], {"worktree_rows": 128, **LIMITS})

    # Lead ruling R-81 (a): "Admin registration changed", a twin made after
    # planning.

    def test_clean_admin_registration_changed_a_twin_made_after_planning(self):
        # At the question, a second registry entry is made for a selected
        # target, naming it through a symbolic link to the directory that holds
        # it: a copy of its admin directory whose `gitdir` names that spelling.
        # Both entries pass the two-way check with one admin id (lead ruling
        # R-67 (c)); the fresh registry read at revalidation shows another
        # present entry with the target's realpath, so the first target is
        # refused with identity-changed and nothing is removed, the twin of the
        # second target found by the first target's preflight (lead ruling
        # R-41).
        for at in (0, 1):
            with self.subTest(twin_of=at):
                case = f"twin-{at}"
                root, trees = self.batch(case, ["001-p", "002-q"])
                link = self.base / case / "linked-trees"

                def twin(root=root, tree=trees[at], link=link):
                    admin = self.common_dir(root) / "worktrees"
                    shutil.copytree(admin / tree.name, admin / f"{tree.name}-twin")
                    link.symlink_to(tree.parent)
                    (admin / f"{tree.name}-twin" / "gitdir").write_text(f"{link / tree.name / '.git'}\n")

                status, out, err = self.main_in_process("clean", root, "--all-safe", "--apply", "--json",
                                                        at_question=twin)
                self.assertIn(f"worktree {link / trees[at].name}",
                              self.git(root, "worktree", "list", "--porcelain").splitlines())
                document = json.loads(out)
                self.assertEqual(stages(document), [(str(trees[0]), "refused", "identity-changed"),
                                                    (str(trees[1]), "not-attempted", "batch-stopped")], err)
                self.assertEqual((status, document["exit_code"]), (2, 2))
                self.assertTrue(all(tree.is_dir() for tree in trees), "nothing removed")

    @clean_support.not_root
    def test_clean_admin_registration_changed_a_twin_spelled_through_an_unsearchable_directory(self):
        # Lead ruling R-93 (e), LOW-3 (lane 3's twin-unreadable). At the
        # question, a twin of the second target is registered as the test above
        # registers one, but spelled through a directory that is then made mode
        # 000, so that the twin's lstat fails with EACCES and its realpath and
        # admin id cannot be read. A value that cannot be re-read is a
        # difference (the project-clean-review-safety delta, rs:92-93), as
        # planning fails closed on an unread realpath (R-78 (b)): the target is
        # refused with state-changed, since a read that decided nothing is
        # state-changed whatever its step (the lead's R-208, #19 at 9267303),
        # exit 2, and nothing is removed. Under
        # --all-safe the first target's preflight reads the fresh registry
        # listing (R-41), so the first target is the one refused and the
        # second is not attempted; with --worktree naming the second target,
        # it is refused itself.
        for mode in ("all-safe", "single"):
            with self.subTest(mode):
                case = f"twin-unsearchable-{mode}"
                root, trees = self.batch(case, ["001-p", "002-q"])
                planned = {tree: self.head(tree) for tree in trees}
                locked = self.base / case / "locked"
                spelled = locked / "in" / trees[1].name

                def twin(root=root, tree=trees[1], locked=locked, spelled=spelled):
                    admin = self.common_dir(root) / "worktrees"
                    shutil.copytree(admin / tree.name, admin / f"{tree.name}-twin")
                    locked.mkdir()
                    (locked / "in").symlink_to(tree.parent)
                    (admin / f"{tree.name}-twin" / "gitdir").write_text(f"{spelled / '.git'}\n")
                    locked.chmod(0o000)
                    self.addCleanup(locked.chmod, 0o700)

                words = ("--all-safe",) if mode == "all-safe" else ("--action", "remove", "--worktree", trees[1])
                status, out, err = self.main_in_process("clean", root, *words, "--apply", "--json", at_question=twin)
                with self.assertRaises(PermissionError):
                    os.lstat(spelled)
                registry = self.git(root, "worktree", "list", "--porcelain").splitlines()
                self.assertIn(f"worktree {spelled}", registry)
                document = json.loads(out)
                refused_tree = trees[0] if mode == "all-safe" else trees[1]
                expected = [(str(refused_tree), "refused", "state-changed")]
                if mode == "all-safe":
                    expected.append((str(trees[1]), "not-attempted", "batch-stopped"))
                self.assertEqual(stages(document), expected, err)
                self.assertEqual(document["targets"][0]["reconciliation"],
                                 record(True, True, True, planned[refused_tree]))
                self.assertEqual((status, document["exit_code"]), (2, 2))
                self.assertTrue(all(tree.is_dir() for tree in trees), "nothing removed")
                self.assertTrue(all(f"worktree {tree}" in registry for tree in trees))

        # The realpath half: a twin spelled through a searchable symbolic link,
        # as the test above spells it, whose realpath read is made to fail in
        # this process (a realpath that is not strict raises only in a race or
        # at its budget). EACCES, or a read cut at its probe budget, refuses as
        # above; ENOENT is absence (R-36), so the twin is compared by neither
        # and both targets are removed.
        def realpath_error(number):
            return {"code": "os-error", "message": TEXT["row_error_os_error"].format(
                OPERATION="realpath", STRERROR=os.strerror(number))}

        timeout = {"code": "probe-timeout", "message": TEXT["row_error_probe_timeout"].format(
            OPERATION="realpath", S="5")}
        cases = [("EACCES", realpath_error(errno.EACCES), errno.EACCES), ("timeout", timeout, None),
                 ("ENOENT", realpath_error(errno.ENOENT), errno.ENOENT)]
        for name, error, number in cases:
            with self.subTest(realpath=name):
                case = f"twin-realpath-{name.lower()}"
                root, trees = self.batch(case, ["001-p", "002-q"])
                link = self.base / case / "linked-trees"
                original = project._realpath

                def realpath(path, spelled=os.fsencode(link / trees[1].name), error=error, number=number):
                    if path == spelled:
                        raise project.EvidenceError(error, number)
                    return original(path)

                def twin(root=root, tree=trees[1], link=link):
                    admin = self.common_dir(root) / "worktrees"
                    shutil.copytree(admin / tree.name, admin / f"{tree.name}-twin")
                    link.symlink_to(tree.parent)
                    (admin / f"{tree.name}-twin" / "gitdir").write_text(f"{link / tree.name / '.git'}\n")

                status, out, err = self.main_in_process("clean", root, "--all-safe", "--apply", "--json",
                                                        at_question=twin, _realpath=realpath)
                document = json.loads(out)
                if number == errno.ENOENT:
                    self.assertEqual(stages(document), [(str(tree), "removed", None) for tree in trees], err)
                    self.assertEqual((status, document["exit_code"]), (0, 0))
                    continue
                self.assertEqual(stages(document), [(str(trees[0]), "refused", "state-changed"),
                                                    (str(trees[1]), "not-attempted", "batch-stopped")], err)
                self.assertEqual((status, document["exit_code"]), (2, 2))
                self.assertTrue(all(tree.is_dir() for tree in trees), "nothing removed")

        # The boundary, in single mode with P the first target: another
        # worktree whose lstat already failed while planning is null in the
        # plan and null again (rs:89-92), the plan's non-blocking
        # inspection-error that does not refuse P (pcl:258-262), so P is
        # removed; the same worktree made unsearchable at the question can no
        # longer be re-read, so P is refused with state-changed (R-208).
        for when in ("before-planning", "at-the-question"):
            with self.subTest(another_worktree_unsearchable=when):
                root, trees = self.batch(f"other-unsearchable-{when}", ["001-p", "002-q"])
                holder = self.base / f"other-unsearchable-{when}" / "other"
                holder.mkdir()
                self.merged_worktree("003-r", path=holder / "003-r", root=root)
                self.addCleanup(holder.chmod, 0o700)

                def unsearchable(holder=holder):
                    holder.chmod(0o000)

                if when == "before-planning":
                    unsearchable()
                status, out, err = self.main_in_process(
                    "clean", root, "--action", "remove", "--worktree", trees[0], "--apply", "--json",
                    at_question=unsearchable if when == "at-the-question" else None)
                document = json.loads(out)
                if when == "before-planning":
                    self.assertEqual(stages(document), [(str(trees[0]), "removed", None)], err)
                    self.assertEqual((status, document["exit_code"]), (0, 0))
                    self.assertFalse(trees[0].exists())
                    continue
                self.assertEqual(stages(document), [(str(trees[0]), "refused", "state-changed")], err)
                self.assertEqual((status, document["exit_code"]), (2, 2))
                self.assertTrue(all(tree.is_dir() for tree in trees), "nothing removed")


if __name__ == "__main__":
    unittest.main()
