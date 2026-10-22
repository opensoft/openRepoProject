"""The named removal as a one-item batch (feature 004, the US3 single lane:
T069 to T071 and T075).

Sources: the project-clean delta's "Clean can explicitly retire verified
worktrees" (P's completeness) and "Clean bounds its Git work and reports
omitted work" (the caps, the registry read and `omitted`), in
openspec/changes/add-project-clean-all-safe/specs/; specs/004-project-clean-all-safe/
data-model.md ("Plan") and contracts/project-clean.md ("Order of a run" and
the plan notes in "Codes"); lead rulings R-53 P-14 and P-15 and R-67 (b).

Expected human text comes from clean_support's fixtures (rule 8); counts and
key values are literals written here (rule 11). Every repository is a
disposable fixture under the test's temporary directory (rule 4). The eligible
worktrees are made by merged_worktree(), each with a commit of its own; rows
registered directly by register_worktrees() are `unpublished`.

A plan is read without removing anything as `--apply --action remove
--worktree P --json` run without --yes on a standard input that is not a
terminal: the run stops at `confirmation-required`, exit 2, and prints the
plan envelope with its selection, notes and `omitted`. The removals run with
--yes, at a pseudo-terminal, or in process with `ask_removal` patched as T046
patches it (lead ruling R-53 P-14).
"""
import contextlib
import errno
import io
import json
import os
from pathlib import Path
import shutil
import unittest
from unittest import mock

import clean_support

project = clean_support.load_project()
TEXT = clean_support.TEXT_FIXTURES

# The status probe's words after `-C PATH` (design D6), as the contract writes them.
STATUS = ["status", "--porcelain=v1", "-z", "--untracked-files=normal", "--ignored=matching"]
# The hidden-state probe's words after `-C PATH` (gate 10; design D2 and D11).
HIDDEN = ["ls-files", "-v", "--stage", "-z"]


def argv_words(record):
    """A counted child's argument vector without its leading -c pins."""
    argv, at = record.argv, 0
    while at + 1 < len(argv) and argv[at] == "-c":
        at += 2
    return argv[at:]


def status_paths(records):
    """The directory of each status probe in the counting log, in spawn order."""
    return [argv_words(record)[1] for record in records if argv_words(record)[2:] == STATUS]


def worktree_children(records):
    """(subcommand, directory) of each status probe and hidden-state probe in
    the counting log, in spawn order."""
    return [(argv_words(record)[2], argv_words(record)[1]) for record in records
            if argv_words(record)[2:] in (STATUS, HIDDEN)]


def removals(records):
    """The `worktree remove` children in the counting log."""
    return [record for record in records if argv_words(record)[2:4] == ["worktree", "remove"]]


def codes(document):
    return [refusal["code"] for refusal in document["refusals"]]


class SingleTests(clean_support.CleanCase):

    def snapshot(self, root):
        """What a run that removes nothing leaves unchanged: the registry, every
        ref, and every file of the repository's worktrees with its content (a
        "nothing changed" snapshot of this module's own, rule 3)."""
        registry = self.git(root, "worktree", "list", "--porcelain")
        trees = [Path(line[9:]) for line in registry.splitlines() if line.startswith("worktree ")]
        files = {}
        for tree in trees:
            if not os.access(tree.parent, os.X_OK):
                continue  # an unreadable fixture row: its parent has no search permission
            for directory, names, filenames in os.walk(tree):
                names[:] = [name for name in names if name != ".git"]
                for name in filenames:
                    path = Path(directory) / name
                    if path.name != ".git":
                        files[str(path)] = path.read_bytes()
        return registry, self.git(root, "for-each-ref", "--format=%(refname) %(objectname)"), files

    def counting(self, real=None):
        """The counting wrapper first on PATH, execing real (a fake Git) or the
        real git: the environment to run with and the log, emptied."""
        bin_dir = self.base / "counting-bin"
        log = self.base / "children.log"
        clean_support.install_counting_git(bin_dir, log, real=real or clean_support.REAL_GIT)
        clean_support.reset_child_log(log)
        return self.path_first(bin_dir), log

    def run_counted(self, *args, real=None):
        """`project ARGS...` under the counting wrapper: the run and its children."""
        env, log = self.counting(real)
        result = self.run_cli(*args, env=env)
        return result, clean_support.child_log(log)

    def named_plan(self, root, target, real=None):
        """The plan of `--apply --action remove --worktree TARGET --json`, read
        without removing anything: no --yes on a standard input that is not a
        terminal stops the run at confirmation-required, exit 2, after the plan
        is built and checked. Returns the run, its document and its children."""
        result, records = self.run_counted("clean", root, "--apply", "--action", "remove", "--worktree", target,
                                           "--json", real=real)
        self.assert_status(result, 2)
        result.document = self.load_json(result)
        self.assertEqual((result.document["mode"], codes(result.document)), ("single", ["confirmation-required"]),
                         "\n" + clean_support.transcript(result))
        self.assertEqual(removals(records), [])
        return result, result.document, records

    def assert_named_plan(self, document, target, notes=()):
        """A complete single-mode plan selecting TARGET alone, its notes NOTES."""
        self.assertEqual((document["completeness"], [entry["path"] for entry in document["selected"]],
                          document["notes"]),
                         ("complete", [str(target)], list(notes)))

    def note(self, code, target, **values):
        """A plan note of a single-mode plan naming TARGET (contracts/project-clean.md,
        "Codes"), its message from the fixtures."""
        key = "note_" + code.replace("-", "_")
        return {"code": code, "message": TEXT[key].format(PATH=target, **values)}

    def unreadable_worktree(self, root, branch, parent):
        """A merged linked worktree at PARENT/tree whose parent then loses its
        search permission, so that its lstat fails (`present: null`, an
        `os-error`, `inspection-error`); restored before the cleanup."""
        parent.mkdir()
        tree = self.merged_worktree(branch, path=parent / "tree", root=root)
        parent.chmod(0o600)
        self.addCleanup(parent.chmod, 0o700)
        return tree

    def assert_removed(self, root, tree, branch, head):
        """TREE removed: gone from the registry and from disk, while its
        branch is kept at HEAD, its planned SHA."""
        self.assertNotIn(f"worktree {tree}", self.git(root, "worktree", "list", "--porcelain").splitlines())
        self.assertFalse(os.path.lexists(tree))
        self.assertEqual(self.git(root, "rev-parse", f"refs/heads/{branch}").strip(), head)

    def main_in_process(self, *argv, env=None, **patches):
        """project's main(ARGV) in this process, in env (self.env by default),
        standard input a stand-in terminal whose isatty() is true, as T046's,
        and each named function of project replaced by its stand-in: (status,
        stdout, stderr). main() restores the signal handlers it installs."""
        class Terminal(io.StringIO):
            def isatty(self):
                return True

        out, err = io.StringIO(), io.StringIO()
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.dict(os.environ, self.env if env is None else env, clear=True))
            stack.enter_context(mock.patch.object(project.sys, "stdin", Terminal()))
            for name, stand_in in patches.items():
                stack.enter_context(mock.patch.object(project, name, stand_in))
            stack.enter_context(contextlib.redirect_stdout(out))
            stack.enter_context(contextlib.redirect_stderr(err))
            status = project.main([os.fspath(arg) for arg in argv])
        return status, out.getvalue(), err.getvalue()

    # T069: "Single target equals a one-item batch".

    def test_clean_single_target_equals_a_one_item_batch(self):
        # Two fresh copies of one fixture, used in turn at one path (site/):
        # the main worktree, P (the only eligible row) and a dirty worktree.
        site = self.base / "site"
        root = self.repo("site/repo")
        self.bare_remote(root, "site/remote.git")
        target = self.merged_worktree("001-p", path=site / "p-tree", root=root)
        dirty = self.merged_worktree("002-dirty", path=site / "dirty-tree", root=root)
        (dirty / "uncommitted").write_text("preserve")
        template = self.base / "template"
        shutil.copytree(site, template, symlinks=True)

        def fresh_copy():
            shutil.rmtree(site)
            shutil.copytree(template, site, symlinks=True)
            return os.lstat(target)

        entries = {}
        for mode, words, status in (("single", ("--apply", "--action", "remove", "--worktree", target), 2),
                                    ("all-safe", ("--all-safe",), 0)):
            with self.subTest(mode=mode):
                found = fresh_copy()
                result = self.run_json("clean", root, *words, "--json")
                self.assert_status(result, status)
                document = result.document
                self.assertEqual((document["mode"], document["completeness"]), (mode, "complete"))
                self.assertEqual(len(document["selected"]), 1)
                entry = dict(document["selected"][0])
                self.assertEqual((entry.pop("dev"), entry.pop("ino")), (found.st_dev, found.st_ino))
                entries[mode] = entry
        self.assertEqual(entries["single"], entries["all-safe"], "the same entry for P apart from dev and ino")
        self.assertEqual((entries["single"]["path"], entries["single"]["classification"]),
                         (str(target), "merged-removable"))
        single_words = ("--apply", "--action", "remove", "--worktree", target)
        batch = ("--all-safe", "--apply")

        # Both copies with --yes run the same argument vector by the counting
        # log and end with P removed, its branch kept, and exit 0.
        argvs = {}
        for mode, words in (("single", single_words), ("all-safe", batch)):
            with self.subTest(mode=mode, yes=True):
                fresh_copy()
                head = self.git(target, "rev-parse", "HEAD").strip()
                result, records = self.run_counted("clean", root, *words, "--yes")
                self.assert_status(result, 0)
                [removal] = removals(records)
                argvs[mode] = removal.argv
                self.assertEqual(argv_words(removal), ["-C", str(root), "worktree", "remove", str(target)])
                self.assert_removed(root, target, "001-p", head)
        self.assertEqual(argvs["single"], argvs["all-safe"])

        # P made dirty between confirmation and revalidation (lead ruling R-53
        # P-14): both copies without --yes, ask_removal patched in process to
        # dirty P and answer `yes`; the same stage, reason, exit status 2 and
        # human result text, since both run at one path.
        progress = TEXT["progress_line_reason"].format(STAGE="refused", PATH=target, REASON="state-changed")
        expected = [progress,
                    TEXT["stop_block"].format(PATH=target, REASON="state-changed", K=0, N=1, NOT_ATTEMPTED="none",
                                              ROOT=root),
                    TEXT["branches_kept_line"].format(BRANCHES="001-p"), TEXT["residual_window_line"]]

        def dirty_p(plan, run):
            (target / "late-change").write_text("preserve")
            return "yes"

        outcomes = {}
        for mode, words in (("single", single_words), ("all-safe", batch)):
            for json_output in (False, True):
                with self.subTest(mode=mode, dirtied=True, json=json_output):
                    fresh_copy()
                    asked = mock.Mock(side_effect=dirty_p)
                    status, out, err = self.main_in_process("clean", root, *words,
                                                            *(("--json",) if json_output else ()), ask_removal=asked)
                    self.assertEqual((status, asked.call_count), (2, 1), out + err)
                    human = (err if json_output else out).splitlines()
                    self.assertIn(progress, human)
                    result_text = human[human.index(progress):]
                    self.assertEqual(result_text, expected)
                    if json_output:
                        document = json.loads(out)
                        outcomes[mode, "json"] = [(item["path"], item["stage"], item["reason"])
                                                  for item in document["targets"]] + [document["exit_code"]]
                    else:
                        outcomes[mode, "human"] = (status, result_text)
                    self.assertTrue((target / "late-change").is_file())
        self.assertEqual(outcomes["single", "human"], outcomes["all-safe", "human"])
        self.assertEqual(outcomes["single", "json"], outcomes["all-safe", "json"])
        self.assertEqual(outcomes["single", "json"], [(str(target), "refused", "state-changed"), 2])

        with self.subTest("an unregistered path and a dirty worktree"):
            fresh_copy()
            before = self.snapshot(root)
            nowhere = site / "nowhere"
            for named, code, message, reason in (
                    (nowhere, "worktree-not-found", f"No unique linked worktree found at {nowhere}", None),
                    (dirty, "target-excluded", TEXT["target_excluded_class"].format(CLASS="dirty"), "dirty")):
                words = ("clean", root, "--apply", "--action", "remove", "--worktree", named, "--yes")
                result, records = self.run_counted(*words)
                self.assert_status(result, 2)
                self.assertEqual(result.stderr, f"REFUSED: {message}\n")
                self.assertEqual(removals(records), [])
                document = self.run_json(*words, "--json").document
                refusal = {"code": code, "message": message, "path": str(named), "path_valid_utf8": True}
                if reason is not None:
                    refusal["reason"] = reason
                self.assertEqual((document["refusals"], document["selected"], document["apply_allowed"]),
                                 ([refusal], [], False))
            self.assertEqual(self.snapshot(root), before)

        with self.subTest("another worktree unreadable"):
            if hasattr(os, "geteuid") and os.geteuid() == 0:
                self.skipTest("permission fixtures do not bind the superuser (effective uid 0)")
            fresh_copy()
            self.unreadable_worktree(root, "003-hidden", site / "hidden")
            before = self.snapshot(root)
            # The row's path could not be read, so the remedy names no git
            # worktree prune (#19's round (l); W87 M-1, lead ruling R-307).
            refused = "REFUSED: " + TEXT["plan_incomplete"].format(
                CODE="inspection-incomplete", REMEDY=TEXT["remedy_inspection_incomplete_unread"]) + "\n"
            batch, records = self.run_counted("clean", root, "--all-safe", "--apply", "--yes")
            self.assert_status(batch, 2)
            self.assertEqual(batch.stderr, refused)
            self.assertEqual(removals(records), [])
            self.assertEqual(self.snapshot(root), before)
            # The named removal's plan is complete on P's own evidence, the
            # unreadable row a non-blocking note.
            _, document, _ = self.named_plan(root, target)
            self.assert_named_plan(document, target, [self.note("inspection-incomplete", target, K=1)])
            self.assertEqual(self.snapshot(root), before)
            head = self.git(target, "rev-parse", "HEAD").strip()
            result, records = self.run_counted("clean", root, *single_words, "--yes")
            self.assert_status(result, 0)
            self.assertEqual(len(removals(records)), 1)
            self.assert_removed(root, target, "001-p", head)

    # T070: a named removal beside an inspection error, among seventeen
    # eligible rows, and beyond the row cap.

    def test_clean_a_named_removal_beside_another_row_s_inspection_error(self):
        root = self.repo()
        self.bare_remote()
        target = self.merged_worktree("001-p")
        failing = self.merged_worktree("002-failing")
        fake = clean_support.install_fake_git(self.base / "fake", "status-fails-in", path=failing)
        env = self.path_first(fake.parent)
        before = self.snapshot(root)
        _, document, records = self.named_plan(root, target, real=fake)
        self.assert_named_plan(document, target, [self.note("inspection-incomplete", target, K=1)])
        rows = {row["path"]: row for row in document["worktrees"]}
        self.assertEqual(rows[str(failing)]["classification"], "inspection-error")
        self.assertEqual(status_paths(records)[0], str(target), "P is probed first")
        # The same repository's batch refuses: there the row is not P's.
        batch = self.run_json("clean", root, "--all-safe", "--apply", "--yes", "--json", env=env).document
        self.assertEqual((batch["completeness"], codes(batch)), ("incomplete", ["inspection-incomplete"]))
        self.assertEqual(self.snapshot(root), before)
        # With --yes, P is removed beside the failing row, exit 0.
        head = self.git(target, "rev-parse", "HEAD").strip()
        result, records = self.run_counted("clean", root, "--apply", "--action", "remove", "--worktree", target,
                                           "--yes", "--json", real=fake)
        self.assert_status(result, 0)
        document = self.load_json(result)
        self.assertEqual(([(item["path"], item["stage"], item["reason"]) for item in document["targets"]],
                          document["exit_code"]), ([(str(target), "removed", None)], 0))
        self.assertEqual(status_paths(records)[0], str(target))
        self.assert_removed(root, target, "001-p", head)
        self.assertTrue(failing.is_dir())

    def test_clean_a_named_removal_among_seventeen_eligible_rows(self):
        root = self.repo()
        self.bare_remote()
        trees = [self.merged_worktree(f"{number:03d}-eligible") for number in range(1, 18)]
        target = trees[8]
        before = self.snapshot(root)
        result, document, _ = self.named_plan(root, target)
        self.assert_named_plan(document, target)
        others = [tree for tree in trees if tree != target]
        self.assertEqual(len(others), 16)
        self.assertEqual([(entry["path"], entry["reason"]) for entry in document["excluded"]],
                         sorted([(str(tree), "not-requested") for tree in others] + [(str(root), "main-worktree")]))
        self.assertEqual(document["omitted"], {"count": 0, "exactness": "exact"})
        human = self.run_cli("clean", root, "--apply", "--action", "remove", "--worktree", target)
        self.assert_status(human, 2)
        self.assertIn(TEXT["excluded_group"].format(REASON="not-requested", K=16,
                                                    NEXT_STEP=clean_support.NEXT_STEP_FIXTURES["not-requested"]),
                      human.stdout.splitlines())
        self.assertIn(TEXT["selected_heading"].format(N=1), human.stdout.splitlines())
        self.assertEqual(self.snapshot(root), before)
        # With --yes, P alone is removed, the other sixteen stay, exit 0.
        head = self.git(target, "rev-parse", "HEAD").strip()
        result, records = self.run_counted("clean", root, "--apply", "--action", "remove", "--worktree", target,
                                           "--yes")
        self.assert_status(result, 0)
        self.assertEqual([argv_words(record)[-1] for record in removals(records)], [str(target)])
        self.assertIn(TEXT["success_line"].format(N=1, BRANCHES="009-eligible"), result.stdout.splitlines())
        self.assert_removed(root, target, "009-eligible", head)
        self.assertTrue(all(tree.is_dir() for tree in others))

    def test_clean_a_named_removal_beyond_the_row_cap(self):
        # Lead ruling R-53 P-15: the main worktree, 129 rows registered directly
        # (registered first, while the main worktree's head has an empty tree,
        # so each is clean and `unpublished`), and P, a real merged worktree
        # whose path sorts after every other: 131 entries. P and the first 128
        # entries other than P, the main worktree first, are inspected, and the
        # last two registered rows are not.
        root = self.repo()
        self.bare_remote()
        registered = self.register_worktrees(129, "r")
        target = self.merged_worktree("p", path=self.base / "zz-p")
        self.assertEqual(sorted(map(os.fsencode, registered + [target]))[-1], os.fsencode(target))
        before = self.snapshot(root)
        _, document, records = self.named_plan(root, target)
        self.assert_named_plan(document, target, [self.note("inspect-cap", target, K=2, M=128)])
        self.assertEqual(document["omitted"], {"count": 2, "exactness": "exact"})
        self.assertEqual(document["limits"]["worktree_rows"], 128)
        inspected = [str(root)] + [str(tree) for tree in registered[:127]] + [str(target)]
        self.assertEqual([row["path"] for row in document["worktrees"]], inspected)
        self.assertEqual({row["classification"] for row in document["worktrees"][1:-1]}, {"unpublished"})
        excluded = [entry["path"] for entry in document["excluded"]]
        self.assertEqual(excluded, sorted(inspected[:-1]), "the rows past the cap are neither rows nor excluded")
        paths = status_paths(records)
        self.assertEqual(paths[0], str(target), "P's status probe is the first status child")
        self.assertEqual(paths, [str(target)] + inspected[:-1])
        # The batch of the same repository, past its cap: incomplete with
        # inspect-cap, the main worktree and the 127 smallest paths inspected.
        batch = self.run_json("clean", root, "--all-safe", "--json")
        self.assert_status(batch, 1)
        self.assertEqual((batch.document["completeness"], batch.document["omitted"], codes(batch.document)),
                         ("incomplete", {"count": 3, "exactness": "exact"}, ["inspect-cap"]))
        self.assertEqual([row["path"] for row in batch.document["worktrees"]], inspected[:-1])
        self.assertEqual(self.snapshot(root), before)
        # With --yes, P is probed first and removed, exit 0.
        head = self.git(target, "rev-parse", "HEAD").strip()
        result, records = self.run_counted("clean", root, "--apply", "--action", "remove", "--worktree", target,
                                           "--yes")
        self.assert_status(result, 0)
        self.assertEqual(status_paths(records)[0], str(target))
        self.assertEqual([argv_words(record)[-1] for record in removals(records)], [str(target)])
        self.assert_removed(root, target, "p", head)
        self.assertTrue(all(tree.is_dir() for tree in registered))

    def test_clean_single_target_p_s_own_realpath_unread_keeps_the_cap(self):
        # Lead ruling R-73 (d): when P's own realpath read fails, P's match is
        # undecided and no entry is exempt from the cap, so the rows inspected
        # are the ones --all-safe's cap takes, the main worktree and the 127
        # smallest paths; the counting log has no status probe past the cap,
        # and the run refuses with inspection-incomplete, exit 2, before the
        # question stage, with nothing removed.
        root = self.repo()
        self.bare_remote()
        registered = self.register_worktrees(129, "r")
        target = self.merged_worktree("p", path=self.base / "zz-p")
        before = self.snapshot(root)
        env, log = self.counting()
        real_fs_call, failed = project.fs_call, []

        def fs_call(fn, *args, **kwargs):
            if fn is os.path.realpath and args[0] == os.fsencode(target) and not failed:
                failed.append(args[0])
                raise OSError(errno.EIO, os.strerror(errno.EIO))
            return real_fs_call(fn, *args, **kwargs)

        asked = AssertionError("the run reached the question stage")
        status, out, err = self.main_in_process(
            "clean", root, "--apply", "--action", "remove", "--worktree", target, "--yes", "--json", env=env,
            fs_call=fs_call, confirm_removal=mock.Mock(side_effect=asked),
            apply_removals=mock.Mock(side_effect=asked))
        self.assertEqual((status, failed), (2, [os.fsencode(target)]), err)
        document = json.loads(out)
        inspected = [str(root)] + [str(tree) for tree in registered[:127]]
        self.assertEqual((codes(document), document["selected"], document["completeness"], document["omitted"]),
                         (["inspection-incomplete"], [], "incomplete", {"count": 3, "exactness": "exact"}))
        self.assertEqual(document["notes"], [], "the refusal speaks alone (lead ruling R-93 (e))")
        self.assertEqual([row["path"] for row in document["worktrees"]], inspected)
        self.assertEqual(status_paths(clean_support.child_log(log)), inspected,
                         "no status probe past the cap: none for the last two registered rows or P")
        self.assertEqual(self.snapshot(root), before)

    # T071: "Remove a merged clean worktree".

    def test_clean_remove_a_merged_clean_worktree(self):
        # At a pseudo-terminal: D18's question in the singular, then `yes`. The
        # worktree is removed and its branch kept; only a separate --action
        # delete-branch deletes the branch. It pins T054 and T057.
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-feature")
        head = self.git(tree, "rev-parse", "HEAD").strip()
        result = self.run_pty_steps(
            clean_support.cli_argv("clean", root, "--apply", "--action", "remove", "--worktree", tree),
            steps=[(TEXT["question_one"], "yes")])
        self.assert_status(result, 0)
        lines = result.stdout.splitlines()
        self.assertIn(TEXT["question_one"], lines)
        self.assertNotIn("worktrees, keeping", result.stdout)
        self.assertIn(TEXT["progress_line"].format(STAGE="removed", PATH=tree), lines)
        self.assertIn(TEXT["success_line"].format(N=1, BRANCHES="001-feature"), lines)
        self.assert_removed(root, tree, "001-feature", head)
        deleted = self.run_cli("clean", root, "--apply", "--action", "delete-branch", "--branch", "001-feature",
                               "--yes")
        self.assert_status(deleted, 0)
        self.assertEqual(self.git(root, "branch", "--list", "001-feature"), "")


    # Lead ruling R-72 (c): a rule match_target() has (R-67 (b), R-69 (2)).

    def test_clean_single_target_a_failed_realpath_read_counts_as_a_match(self):
        # The realpath read of another entry, Q, fails once, during P's match
        # only: Q counts as a match, failing closed, so P's match is undecided,
        # plan.target is None and nothing is selected; the run refuses with
        # inspection-incomplete, exit 2, before the question stage (which
        # would raise here), with nothing removed. Q's own row read (a second
        # realpath call) is not failed, so Q's row stays merged-removable.
        root = self.repo()
        self.bare_remote()
        target = self.merged_worktree("001-p")
        other = self.merged_worktree("002-q")
        before = self.snapshot(root)
        real_fs_call, failed = project.fs_call, []

        def fs_call(fn, *args, **kwargs):
            if fn is os.path.realpath and args[0] == os.fsencode(other) and not failed:
                failed.append(args[0])
                raise OSError(errno.EIO, os.strerror(errno.EIO))
            return real_fs_call(fn, *args, **kwargs)

        out, err = io.StringIO(), io.StringIO()
        asked = AssertionError("the run reached the question stage")
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.dict(os.environ, self.env, clear=True))
            stack.enter_context(mock.patch.object(project, "fs_call", fs_call))
            stack.enter_context(mock.patch.object(project, "confirm_removal", side_effect=asked))
            stack.enter_context(mock.patch.object(project, "apply_removals", side_effect=asked))
            stack.enter_context(contextlib.redirect_stdout(out))
            stack.enter_context(contextlib.redirect_stderr(err))
            status = project.main(["clean", str(root), "--apply", "--action", "remove", "--worktree", str(target),
                                   "--yes", "--json"])
        self.assertEqual((status, failed), (2, [os.fsencode(other)]))
        # Under --apply --json the human plan goes to standard error (contract,
        # "Streams"): P is not selected there either, and nothing is asked.
        self.assertNotIn(TEXT["selected_heading"].format(N=1), err.getvalue())
        self.assertNotIn("[yes/N]", err.getvalue())
        document = json.loads(out.getvalue())
        self.assertEqual((document["mode"], codes(document), document["selected"], document["completeness"],
                          document["apply_allowed"]),
                         ("single", ["inspection-incomplete"], [], "incomplete", False))
        rows = {row["path"]: row["classification"] for row in document["worktrees"]}
        self.assertEqual(rows[str(other)], "merged-removable")
        self.assertEqual(sorted((entry["path"], entry["reason"]) for entry in document["excluded"]),
                         [(str(target), "not-requested"), (str(other), "not-requested"),
                          (str(root), "main-worktree")])
        self.assertEqual(self.snapshot(root), before)

    # Lead ruling R-93 (d), lane 3's HIGH-1: design D13 inspects P's row first,
    # "identity, status probe, gates", then the other rows (the delta's "P
    # SHALL be probed first").

    def test_clean_single_target_a_deadline_among_other_rows_leaves_p_decided(self):
        # P (001-p) and another merged worktree whose status probe hangs (the
        # fake `status-hangs-in`, which SIGTERM ends) behind the counting
        # wrapper, run through the launcher with a table that shortens the
        # deadline to 3 s and the reserve to 1 s (R-29): 2 s of work, and the
        # probe budget min(5 s, work remaining), so the hang is cut at the work
        # deadline. P's status probe and P's gates (gate 7's reflog read, gate
        # 9's `modules` lstat and gate 10's `ls-files`) run before any other
        # row is inspected, so P's row is decided and the plan complete beside
        # the non-blocking note `deadline-exceeded`; the floor then makes P
        # `not-attempted` with deadline-exceeded, exit 1 (D19 row 2), and
        # nothing is removed.
        root = self.repo()
        self.bare_remote()
        target = self.merged_worktree("001-p")
        hang = self.merged_worktree("002-hang")
        fake = clean_support.install_fake_git(self.base / "fake", "status-hangs-in", path=hang, lifetime=10)
        env, log = self.counting(real=fake)
        table = clean_support.timing_table(invocation_deadline=3.0, reconciliation_reserve=1.0)
        words = ("clean", root, "--apply", "--action", "remove", "--worktree", target)
        order = [("status", str(target)), ("ls-files", str(target)), ("status", str(root)), ("status", str(hang))]
        progress = TEXT["progress_line_reason"].format(STAGE="not-attempted", PATH=target, REASON="deadline-exceeded")
        stop = TEXT["stop_block"].format(PATH=target, REASON="deadline-exceeded", K=0, N=1, NOT_ATTEMPTED=target,
                                         ROOT=root)
        result_text = [progress, stop, TEXT["branches_kept_line"].format(BRANCHES="001-p"),
                       TEXT["residual_window_line"]]
        before = self.snapshot(root)

        def launched(*extra):
            clean_support.reset_child_log(log)
            result = self.run_launched(table, *words, *extra, env=env)
            return result, clean_support.child_log(log)

        def assert_children(records):
            self.assertEqual(worktree_children(records), order, "P's gate children before the other rows' status")
            self.assertEqual(removals(records), [])

        with self.subTest("human"):
            result, records = launched("--yes")
            self.assert_status(result, 1)
            lines = result.stdout.splitlines()
            self.assertIn(TEXT["selected_heading"].format(N=1), lines)
            self.assertIn(progress, lines, "\n" + clean_support.transcript(result))
            self.assertEqual(lines[lines.index(progress):], result_text)
            self.assertNotIn("REFUSED", result.stdout + result.stderr)
            assert_children(records)

        with self.subTest("json, the plan"):
            # Without --yes on a standard input that is not a terminal the run
            # stops at confirmation-required and prints the plan envelope.
            result, records = launched("--json")
            self.assert_status(result, 2)
            document = self.load_json(result)
            self.assertEqual((codes(document), document["completeness"],
                              sorted((entry["path"], entry["reason"]) for entry in document["excluded"])),
                             (["confirmation-required"], "complete",
                              [(str(hang), "inspection-error"), (str(root), "main-worktree")]))
            self.assert_named_plan(document, target, [self.note("deadline-exceeded", target, K=1)])
            rows = {row["path"]: row for row in document["worktrees"]}
            cut = [{"code": "deadline-exceeded",
                    "message": TEXT["row_error_deadline_exceeded"].format(OPERATION="git status")}]
            self.assertEqual([(rows[str(tree)]["classification"], rows[str(tree)]["errors"]) for tree in (target, hang)],
                             [("merged-removable", []), ("inspection-error", cut)])
            assert_children(records)

        with self.subTest("json, the result"):
            result, records = launched("--yes", "--json")
            self.assert_status(result, 1)
            document = self.load_json(result)
            self.assertEqual([(item["path"], item["stage"], item["reason"], item["reconciliation"])
                              for item in document["targets"]],
                             [(str(target), "not-attempted", "deadline-exceeded", None)])
            self.assertEqual((document["exit_code"], document["operations"]["performed"]), (1, 0))
            lines = result.stderr.splitlines()
            self.assertIn(progress, lines, "\n" + clean_support.transcript(result))
            self.assertEqual(lines[lines.index(progress):], result_text)
            assert_children(records)

        self.assertTrue(target.is_dir())
        self.assertIn(f"worktree {target}", self.git(root, "worktree", "list", "--porcelain").splitlines())
        self.assertEqual(self.snapshot(root), before)

    # Lead ruling R-283: #19 at b3228bb says single mode "SHALL build the same
    # plan with `mode: "single"` ... and share the batch's sequence, refusal
    # codes, stages and exit codes" (pcl:786-792), and a row whose every error
    # is the work deadline's is deadline_stopped(), its plan deadline-exceeded
    # (Brett Heap's ruling "O-1: deadline-exceeded", lead rulings R-263 and
    # R-278). So P's own row cut by the deadline refuses as the one-item batch
    # does, at check_plan()'s step 3.

    def assert_p_s_own_row_cut(self, seam, operation, classification, reason):
        """P's own row cut in process, every other read and child real:
        seam(root, target, name, calls) gives main_in_process()'s stand-ins,
        which answer one read or child of P's planning with a DriverOutcome
        NAME and append to calls. Cut at its budget (`timeout`), the deadline
        not being the limit, the run refuses inspection-incomplete with the
        base remedy; cut by the work deadline (`deadline`), deadline-exceeded
        with the deadline's remedy and no repair remedy. Either way `--worktree
        P` refuses exactly as the one-item batch over the same repository
        does, exit 2, before the question, P's row CLASSIFICATION with the
        cut's error its one error and excluded as REASON; nothing is removed."""
        root = self.repo()
        self.bare_remote()
        target = self.merged_worktree("001-p")
        before = self.snapshot(root)
        asked = AssertionError("the run reached the question stage")
        cuts = (
            ("its budget", "timeout", "no answer within 5 s",
             {"code": "probe-timeout", "message": TEXT["row_error_probe_timeout"].format(OPERATION=operation, S="5")},
             "inspection-incomplete", TEXT["remedy_inspection_incomplete"]),
            ("the work deadline", "deadline", "no time was left to start it",
             {"code": "deadline-exceeded", "message": TEXT["row_error_deadline_exceeded"].format(OPERATION=operation)},
             "deadline-exceeded", TEXT["remedy_deadline_exceeded"]),
        )
        single = ("--apply", "--action", "remove", "--worktree", target, "--yes")
        batch = ("--all-safe", "--apply", "--yes")
        for label, name, detail, error, code, remedy in cuts:
            with self.subTest(f"P's row cut at {label}"):
                calls = []
                patches = dict(seam(root, target, (name, detail), calls),
                               confirm_removal=mock.Mock(side_effect=asked), apply_removals=mock.Mock(side_effect=asked))
                message = TEXT["plan_incomplete"].format(CODE=code, REMEDY=remedy)
                refusals = {}
                for mode, words in (("single", single), ("all-safe", batch)):
                    status, out, err = self.main_in_process("clean", root, *words, "--json", **patches)
                    self.assertEqual(status, 2, out + err)
                    document = json.loads(out)
                    refusals[mode] = document["refusals"]
                    [row] = [row for row in document["worktrees"] if row["path"] == str(target)]
                    self.assertEqual((document["mode"], document["completeness"], document["apply_allowed"],
                                      document["selected"], row["classification"], row["errors"],
                                      {entry["path"]: entry["reason"] for entry in document["excluded"]}),
                                     (mode, "incomplete", False, [], classification, [error],
                                      {str(root): "main-worktree", str(target): reason}))
                self.assertEqual(refusals["single"], [{"code": code, "message": message}])
                self.assertEqual(refusals["single"], refusals["all-safe"], "the one-item batch's refusal")
                status, out, err = self.main_in_process("clean", root, *single, **patches)
                self.assertEqual((status, err), (2, "REFUSED: " + message + "\n"), out)
                self.assertNotIn("[yes/N]", out)
                if name == "deadline":
                    for repair in (TEXT["remedy_inspection_incomplete"], TEXT["remedy_inspection_incomplete_redirect"]):
                        self.assertNotIn(repair, err)
                self.assertEqual(len(calls), 3, "one cut per run")
                self.assertEqual(self.snapshot(root), before, "nothing removed")
        self.assertTrue(target.is_dir())

    def fs_cut(self, picks):
        """A seam for assert_p_s_own_row_cut(): the filesystem call that
        picks(root, target) gives a test of, given its function and
        arguments, answered by the cut's DriverOutcome."""
        def seam(root, target, cut, calls):
            test, real_fs_call = picks(root, target), project.fs_call

            def fs_call(fn, *args, **options):
                if test(fn, args):
                    calls.append(args[0])
                    return project.DriverOutcome(None, cut[0], detail=cut[1])
                return real_fs_call(fn, *args, **options)
            return {"fs_call": fs_call}
        return seam

    def test_clean_single_target_p_s_reflog_read_cut_by_the_deadline(self):
        # Gate 7: the read of P's branch reflog. reflog_gate() leaves the row
        # merged-removable and unprobed, excluded as reflog-unavailable, the
        # read's error its one error (lead ruling R-278).
        def picks(root, target):
            reflog = os.fsencode(self.reflog_file("001-p", root))
            return lambda fn, args: fn is project._read_head and args[:1] == (reflog,)

        self.assert_p_s_own_row_cut(self.fs_cut(picks), "read", "merged-removable", "reflog-unavailable")

    def test_clean_single_target_p_s_admin_listing_cut_by_the_deadline(self):
        # Gate 11: the listing of P's admin directory. _index_undecided()
        # makes the row inspection-error, the listing's error its one error.
        def picks(root, target):
            admin = os.fsencode(self.common_dir(root) / "worktrees" / target.name)
            return lambda fn, args: fn is os.listdir and args == (admin,)

        self.assert_p_s_own_row_cut(self.fs_cut(picks), "listdir", "inspection-error", "inspection-error")

    def test_clean_single_target_p_s_status_probe_cut_by_the_deadline(self):
        # The status probe in P (design D6), a Git child: the row is
        # inspection-error, the probe's error its one error.
        def seam(root, target, cut, calls):
            real_run_bounded = project.run_bounded

            def run_bounded(spec, parser, run):
                kind, args, cwd = spec
                if args[2:] == list(project.STATUS_PROBE) and os.fsencode(args[1]) == bytes(target):
                    calls.append(args[1])
                    return project.DriverOutcome(project.git_argv(kind, args), cut[0], detail=cut[1])
                return real_run_bounded(spec, parser, run)
            return {"run_bounded": run_bounded}

        self.assert_p_s_own_row_cut(seam, "git status", "inspection-error", "inspection-error")

    def test_clean_single_target_p_s_rows_the_deadline_stopped_are_not_counted_for_the_variant(self):
        # Lead ruling R-287 (a), lane 3's W73 L-2: check_plan()'s step 3
        # counts P's rows for the variant remedy as a batch's rows are counted
        # (counted_rows(); 63e4573's rule), so a row of P's that is excluded
        # as registration-mismatch and that the work deadline stopped
        # (deadline_stopped()) does not make the refusal name the unset of
        # core.worktree and core.bare. A copied admin directory makes the
        # registry name P twice: both rows are P's, so P names no single row
        # and step 3 refuses inspection-incomplete, and both are
        # registration-mismatch, read for no registration and probed by no
        # status probe, so inspection-error (the shared registry path; lead
        # rulings R-57 L3 and R-59 D5). In process, every read and child real
        # but one: the working directory's realpath, which worktree_rows()
        # reads once per call and gives to each present row it builds, is
        # answered by a DriverOutcome, so that its error is each row's one
        # error. Cut by the work deadline, P's rows are deadline_stopped() and
        # not counted: the base remedy. With no cut, or cut at its budget, they
        # are counted: the variant. Nothing is removed, and the run stops
        # before the question.
        root = self.repo()
        self.bare_remote()
        target = self.merged_worktree("001-p")
        admin = self.common_dir(root) / "worktrees"
        shutil.copytree(admin / target.name, admin / f"{target.name}-copy")
        listed = self.git(root, "worktree", "list", "--porcelain").splitlines()
        self.assertEqual(listed.count(f"worktree {target}"), 2, "the registry names P twice")
        before = self.snapshot(root)
        asked = AssertionError("the run reached the question stage")
        variant, base = TEXT["remedy_inspection_incomplete_redirect"], TEXT["remedy_inspection_incomplete"]
        cuts = (
            ("no cut", None, [], variant),
            ("its budget", ("timeout", "no answer within 5 s"),
             [{"code": "probe-timeout", "message": TEXT["row_error_probe_timeout"].format(OPERATION="realpath",
                                                                                         S="5")}], variant),
            ("the work deadline", ("deadline", "no time was left to start it"),
             [{"code": "deadline-exceeded",
               "message": TEXT["row_error_deadline_exceeded"].format(OPERATION="realpath")}], base),
        )
        words = ("--apply", "--action", "remove", "--worktree", target, "--yes")
        real_fs_call = project.fs_call
        for label, cut, errors, remedy in cuts:
            with self.subTest(f"the working directory's realpath: {label}"):
                calls = []

                def fs_call(fn, *args, cut=cut, calls=calls, **options):
                    if cut is not None and fn is os.path.realpath and args == (b".",):
                        calls.append(args[0])
                        return project.DriverOutcome(None, cut[0], detail=cut[1])
                    return real_fs_call(fn, *args, **options)

                patches = dict(fs_call=fs_call, confirm_removal=mock.Mock(side_effect=asked),
                               apply_removals=mock.Mock(side_effect=asked))
                message = TEXT["plan_incomplete"].format(CODE="inspection-incomplete", REMEDY=remedy)
                status, out, err = self.main_in_process("clean", root, *words, "--json", **patches)
                self.assertEqual(status, 2, out + err)
                document = json.loads(out)
                rows = [row for row in document["worktrees"] if row["path"] == str(target)]
                self.assertEqual([(row["classification"], row["errors"]) for row in rows],
                                 [("inspection-error", errors)] * 2)
                self.assertEqual(sorted((entry["path"], entry["reason"]) for entry in document["excluded"]),
                                 sorted([(str(root), "main-worktree")] + [(str(target), "registration-mismatch")] * 2))
                self.assertEqual((document["mode"], document["completeness"], document["selected"],
                                  document["refusals"]),
                                 ("single", "incomplete", [], [{"code": "inspection-incomplete", "message": message}]))
                status, out, err = self.main_in_process("clean", root, *words, **patches)
                self.assertEqual((status, err), (2, "REFUSED: " + message + "\n"), out)
                self.assertEqual(len(calls), 0 if cut is None else 4, "one cut per worktree_rows() call")
                self.assertEqual(self.snapshot(root), before, "nothing removed")
        self.assertTrue(target.is_dir())


if __name__ == "__main__":
    unittest.main()
