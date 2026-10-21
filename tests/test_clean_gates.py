"""The registration and index gates of `project clean` (feature 004, the US2
index lane: T061 to T065, beside T067's gates 3, 9 and 10).

Sources: the project-clean delta of openspec/changes/add-project-clean-all-safe/
(the gate list and the scenarios "Every protected classifier", "Hidden local
state", "Submodules", "A deleted upstream is remote-gone", "A merged worktree
whose upstream was deleted", "Dirty or unmerged work is preserved" and "Pushed
feature branch has an open review path"), the project-clean-review-safety delta
("Cleanup preserves all local work not proven disposable"), and
specs/004-project-clean-all-safe/data-model.md ("Gate", "Worktree identity and
registration") and contracts/project-clean.md ("Git children", "Codes").
Expected human text comes from clean_support's fixtures (rule 8); reasons,
classes and recommendations are literals written here (rule 11). Every
repository is a disposable fixture under the test's temporary directory (rule
4), and a row that must stay eligible is a merged_worktree(), a commit of its
own (lead ruling R-56).
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
STEPS = clean_support.NEXT_STEP_FIXTURES

# The baseline recommendations the scenarios name, written here as literals.
MERGED_REMOVABLE_ADVICE = "This clean, merged, non-current worktree may be removed explicitly."
DIRTY_ADVICE = "Preserve or commit the working changes before cleanup."
REVIEW_ADVICE = "Continue through the repository's normal pull-request or merge process."
INSPECTION_ERROR_ADVICE = "Preserve this worktree; Git could not establish its clean state."


def argv_words(record):
    """A counted child's argument vector without its leading -c pins (a small
    helper of this module's own, tasks.md rule 3)."""
    argv, at = record.argv, 0
    while at + 1 < len(argv) and argv[at] == "-c":
        at += 2
    return argv[at:]


def removals(records):
    """The counted `worktree remove` children."""
    return [record for record in records if argv_words(record)[2:4] == ["worktree", "remove"]]


def by_path(document):
    """The `excluded` entries of a plan envelope as a map from path to reason."""
    return {entry["path"]: entry["reason"] for entry in document["excluded"]}


def row_of(document, path):
    """The `worktrees` row of the plan envelope whose path is path."""
    [row] = [row for row in document["worktrees"] if row["path"] == str(path)]
    return row


class GatesTests(clean_support.CleanCase):

    # Small helpers of this module's own (tasks.md rule 3).

    def snapshot(self, root):
        """What a run must leave unchanged: the registry, every ref, and every
        file of the repository's worktrees with its content."""
        registry = self.git(root, "worktree", "list", "--porcelain")
        trees = [Path(line[9:]) for line in registry.splitlines() if line.startswith("worktree ")]
        files = {}
        for tree in trees:
            for directory, names, filenames in os.walk(tree):
                names[:] = [name for name in names if name != ".git"]
                for name in filenames:
                    path = Path(directory) / name
                    if path.name != ".git" and not path.is_symlink():
                        files[str(path)] = path.read_bytes()
        return registry, self.git(root, "for-each-ref", "--format=%(refname) %(objectname)"), files

    def counting(self, real=None, env=None):
        """The counting wrapper first on PATH, in front of real (the real git,
        or a fake): the environment to run with and the log, emptied."""
        bin_dir = self.base / "counting-bin"
        log = self.base / "children.log"
        clean_support.install_counting_git(bin_dir, log, real=real or clean_support.REAL_GIT)
        clean_support.reset_child_log(log)
        return self.path_first(bin_dir, env), log

    def run_counted(self, *args, real=None, timing=None, cwd=None):
        """`project ARGS...` under the counting wrapper, through the launcher
        when timing is given: the run and its counted children."""
        env, log = self.counting(real)
        if timing is None:
            result = self.run_cli(*args, env=env, cwd=cwd)
        else:
            result = self.run_launched(timing, *args, env=env, cwd=cwd)
        return result, clean_support.child_log(log)

    def main_in_process(self, *argv, **patches):
        """project's main(ARGV) in this process, in self.env, each named function
        of project replaced by its stand-in: (status, stdout, stderr)."""
        out, err = io.StringIO(), io.StringIO()
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.dict(os.environ, self.env, clear=True))
            for name, stand_in in patches.items():
                stack.enter_context(mock.patch.object(project, name, stand_in))
            stack.enter_context(contextlib.redirect_stdout(out))
            stack.enter_context(contextlib.redirect_stderr(err))
            status = project.main([os.fspath(arg) for arg in argv])
        return status, out.getvalue(), err.getvalue()

    def pushed_worktree(self, branch, path, root=None):
        """`worktree add -b BRANCH PATH`, a commit of its own and `push -u`,
        never merged. Returns the path."""
        root = root or self.root
        self.git(root, "worktree", "add", "-b", branch, path)
        (path / ("work-" + branch)).write_text("work")
        self.commit(path)
        self.git(path, "push", "-q", "-u", "origin", branch)
        return path

    def preview(self, root, *words, cwd=None):
        """`clean ROOT --all-safe --json WORDS...`: the run, its document parsed."""
        return self.run_json("clean", root, "--all-safe", "--json", *words, cwd=cwd)

    def assert_refused_target(self, result, path, reason, message):
        """A single-mode run refused with target-excluded, exit 2."""
        self.assert_status(result, 2)
        self.assertEqual(result.document["refusals"], [
            {"code": "target-excluded", "message": message, "path": str(path), "path_valid_utf8": True,
             "reason": reason}])
        self.assertEqual((result.document["selected"], result.document["apply_allowed"]), ([], False))

    # T061: "Every protected classifier".

    def protected_repository(self):
        """The repository of "Every protected classifier": every protected
        class as a linked worktree, beside the main worktree on the merge
        target and one plain merged, clean, published worktree with a commit of
        its own. Returns its paths by name and the expected reason of each
        excluded path; the non-UTF-8 row is added under linux_paths only."""
        base = self.base
        root = self.repo()
        self.bare_remote()
        trees = {"root": root}
        reasons = {str(root): "main-worktree"}

        def add(name, reason, tree):
            trees[name] = tree
            if reason is not None:
                reasons[str(tree)] = reason

        stale = base / "stale"
        self.git(root, "worktree", "add", "-q", "-b", "001-stale", stale)
        shutil.rmtree(stale)
        add("stale", "stale-worktree", stale)
        detached = base / "detached"
        self.git(root, "worktree", "add", "-q", "--detach", detached)
        add("detached", "detached", detached)
        dirty = self.merged_worktree("003-dirty", path=base / "dirty")
        (dirty / "uncommitted").write_text("preserve")
        add("dirty", "dirty", dirty)
        ignored = self.merged_worktree("004-ignored", path=base / "ignored",
                                       setup=lambda tree: (tree / ".gitignore").write_text("local.env\n"))
        (ignored / "local.env").write_text("preserve")
        add("ignored", "ignored-local-files", ignored)
        unpublished = base / "unpublished"
        self.git(root, "worktree", "add", "-q", "-b", "005-unpublished", unpublished)
        (unpublished / "work").write_text("work")
        self.commit(unpublished)
        add("unpublished", "unpublished", unpublished)
        gone = self.pushed_worktree("006-remote-gone", base / "remote-gone")
        self.git(root, "push", "-q", "origin", "--delete", "006-remote-gone")
        add("remote-gone", "remote-gone", gone)
        diverged = self.pushed_worktree("007-diverged", base / "diverged")
        (diverged / "remote-side").write_text("remote")
        self.commit(diverged)
        self.git(diverged, "push", "-q", "origin", "007-diverged")
        self.git(diverged, "reset", "-q", "--hard", "HEAD~1")
        (diverged / "local-side").write_text("local")
        self.commit(diverged)
        add("diverged", "diverged", diverged)
        behind = self.pushed_worktree("008-remote-ahead", base / "remote-ahead")
        (behind / "remote-side").write_text("remote")
        self.commit(behind)
        self.git(behind, "push", "-q", "origin", "008-remote-ahead")
        self.git(behind, "reset", "-q", "--hard", "HEAD~1")
        add("remote-ahead", "remote-ahead", behind)
        unpushed = self.pushed_worktree("009-unpushed", base / "unpushed")
        (unpushed / "later").write_text("later")
        self.commit(unpushed)
        add("unpushed", "unpushed", unpushed)
        add("pushed-unmerged", "pushed-unmerged", self.pushed_worktree("010-pushed-unmerged",
                                                                       base / "pushed-unmerged"))
        add("current", "merged-current", self.merged_worktree("011-current", path=base / "current"))
        locked = self.merged_worktree("012-locked", path=base / "locked")
        self.git(root, "worktree", "lock", locked)
        add("locked", "locked-worktree", locked)

        @clean_support.linux_paths
        def non_utf_8():
            raw = os.fsencode(base) + b"/non-utf-8-" + bytes([0xFF])
            tree = self.merged_worktree("013-non-utf-8", path=raw)
            trees["non-utf-8"] = tree
            reasons[str(base) + "/non-utf-8-\\xff"] = "unsupported-path-bytes"

        with self.subTest("merged with a non-UTF-8 path, under linux_paths"):
            non_utf_8()
        hidden = self.merged_worktree("014-assume-unchanged", path=base / "assume-unchanged")
        self.git(hidden, "update-index", "--assume-unchanged", "work-014-assume-unchanged")
        (hidden / "work-014-assume-unchanged").write_text("hidden edit")
        add("assume-unchanged", "hidden-local-state", hidden)
        add("plain", None, self.merged_worktree("015-plain", path=base / "plain"))
        # Last: once merged, its gitlink is in the merge target's tree, and a
        # worktree added after it would hold that gitlink too.
        add("submodule", "contains-submodule",
            self.merged_worktree("016-submodule", path=base / "submodule", setup=self.submodule))
        return trees, reasons

    def test_clean_every_protected_classifier(self):
        trees, reasons = self.protected_repository()
        root, current = trees["root"], trees["current"]
        before = self.snapshot(root)
        result = self.preview(root, cwd=current)
        self.assert_status(result, 0)
        document = result.document
        self.assertEqual([entry["path"] for entry in document["selected"]], [str(trees["plain"])])
        self.assertEqual(by_path(document), reasons, "every other row excluded with the gate order's reason")
        self.assertEqual((document["completeness"], document["apply_allowed"], document["refusals"]),
                         ("complete", True, []))
        # The index gates exclude without relabelling: both rows keep their class.
        for name in ("assume-unchanged", "submodule"):
            row = row_of(document, trees[name])
            self.assertEqual((row["classification"], row["errors"]), ("merged-removable", []), name)
        # The human preview groups them under their gates' next steps.
        human = self.run_cli("clean", root, "--all-safe", cwd=current)
        self.assert_status(human, 0)
        lines = human.stdout.splitlines()
        for reason, name in (("contains-submodule", "submodule"), ("hidden-local-state", "assume-unchanged")):
            group = lines.index(TEXT["excluded_group"].format(REASON=reason, K=1, NEXT_STEP=STEPS[reason]))
            branch = self.git(trees[name], "branch", "--show-current").strip()
            self.assertEqual(lines[group + 1], TEXT["excluded_row"].format(PATH=trees[name], BRANCH=branch))
        self.assertEqual(self.snapshot(root), before, "a preview changes nothing")
        # The batch applies: only the plain worktree is removed, exit 0, and
        # every other row stays, its branch included.
        result, records = self.run_counted("clean", root, "--all-safe", "--apply", "--yes", cwd=current)
        self.assert_status(result, 0)
        self.assertEqual([argv_words(record)[-1] for record in removals(records)], [str(trees["plain"])])
        self.assertFalse(trees["plain"].exists())
        self.git(root, "rev-parse", "--verify", "-q", "refs/heads/015-plain")
        for name, tree in trees.items():
            if name not in ("plain", "stale"):
                self.assertTrue(os.path.isdir(tree), name)

    def test_clean_every_protected_classifier_incomplete_copy(self):
        trees, reasons = self.protected_repository()
        root, current = trees["root"], trees["current"]
        plain = str(trees["plain"])
        refused = TEXT["plan_incomplete"].format(CODE="inspection-incomplete",
                                                 REMEDY=TEXT["remedy_inspection_incomplete"])

        def assert_incomplete(added):
            """The copy's plan, with added (path to reason) beside the
            scenario's rows: incomplete, its preview exit 1, and --apply with
            --yes refused with exit 2, nothing removed."""
            before = self.snapshot(root)
            result = self.preview(root, cwd=current)
            self.assert_status(result, 1)
            document = result.document
            self.assertEqual(by_path(document), {**reasons, **added})
            self.assertEqual([entry["path"] for entry in document["selected"]], [plain])
            for path in added:
                self.assertEqual({row["classification"] for row in document["worktrees"] if row["path"] == path},
                                 {"inspection-error"}, path)
            self.assertEqual((document["completeness"], document["apply_allowed"], document["refusals"]),
                             ("incomplete", False, [{"code": "inspection-incomplete", "message": refused}]))
            result, records = self.run_counted("clean", root, "--all-safe", "--apply", "--yes", "--json",
                                               cwd=current)
            self.assert_status(result, 2)
            self.assertEqual(self.load_json(result)["refusals"],
                             [{"code": "inspection-incomplete", "message": refused}])
            self.assertEqual(removals(records), [])
            self.assertEqual(self.snapshot(root), before, "nothing removed")

        @clean_support.not_root
        def unreadable():
            hidden = self.base / "unreadable"
            hidden.mkdir()
            tree = hidden / "tree"
            self.git(root, "worktree", "add", "-q", "-b", "021-unreadable", tree)
            hidden.chmod(0o600)
            try:
                assert_incomplete({str(tree): "inspection-error"})
            finally:
                hidden.chmod(0o700)
                self.git(root, "worktree", "remove", "--force", tree)

        with self.subTest("a copy adding an unreadable worktree"):
            unreadable()
        with self.subTest("a copy adding a broken admin registration"):
            broken = self.merged_worktree("022-broken", path=self.base / "broken")
            gitfile = broken / ".git"
            saved = gitfile.read_bytes()
            missing = self.common_dir(root) / "worktrees" / "missing-admin"
            gitfile.write_text(f"gitdir: {missing}\n")
            try:
                assert_incomplete({str(broken): "registration-mismatch"})
            finally:
                gitfile.write_bytes(saved)
                self.git(root, "worktree", "remove", broken)
        with self.subTest("a copy adding a second registry entry naming a present worktree's path"):
            shared = self.merged_worktree("023-shared", path=self.base / "shared")
            admin = self.common_dir(root) / "worktrees"
            shutil.copytree(admin / shared.name, admin / "shared-copy")
            self.assertEqual(self.git(root, "worktree", "list", "--porcelain").splitlines().count(
                f"worktree {shared}"), 2)
            # Both entries are registration-mismatch (lead rulings R-57 L3 and
            # R-59 D6); the map holds the path once, the document twice.
            assert_incomplete({str(shared): "registration-mismatch"})
            document = self.preview(root, cwd=current).document
            self.assertEqual([entry["reason"] for entry in document["excluded"] if entry["path"] == str(shared)],
                             ["registration-mismatch", "registration-mismatch"])
            # Lead ruling R-62 (a): naming the shared path refuses with
            # inspection-incomplete, exit 2, before any target-excluded; nothing
            # is removed.
            before = self.snapshot(root)
            result, records = self.run_counted("clean", root, "--apply", "--action", "remove", "--worktree", shared,
                                               "--yes", cwd=current)
            self.assert_status(result, 2)
            self.assertEqual(result.stderr, f"REFUSED: {refused}\n")
            self.assertEqual(removals(records), [])
            result = self.run_json("clean", root, "--apply", "--action", "remove", "--worktree", shared, "--yes",
                                   "--json", cwd=current)
            self.assert_status(result, 2)
            self.assertEqual((result.document["refusals"], result.document["selected"]),
                             ([{"code": "inspection-incomplete", "message": refused}], []))
            self.assertEqual(self.snapshot(root), before, "nothing removed")

    # T062: "Hidden local state" (its after-confirmation clause is T083's);
    # "An edit hidden by assume-unchanged survives".

    def test_clean_hidden_local_state(self):
        root = self.repo()
        self.bare_remote()
        plain = self.merged_worktree("001-plain", path=self.base / "plain")
        assumed = self.merged_worktree("002-assumed", path=self.base / "assumed")
        self.git(assumed, "update-index", "--assume-unchanged", "work-002-assumed")
        (assumed / "work-002-assumed").write_text("hidden edit")

        def two_directories(tree):
            for name in ("kept", "sparse"):
                (tree / name).mkdir()
                (tree / name / "file").write_text(name)

        sparse = self.merged_worktree("003-sparse", path=self.base / "sparse", setup=two_directories)
        self.git(sparse, "sparse-checkout", "set", "kept")
        # Each flag is in that worktree's own index; the main worktree's
        # index flags nothing, and neither worktree's status shows a change.
        self.assertIn("h work-002-assumed", self.git(assumed, "ls-files", "-v").splitlines())
        self.assertIn("S sparse/file", self.git(sparse, "ls-files", "-v").splitlines())
        for tree in (root, plain):
            tags = {line[:1] for line in self.git(tree, "ls-files", "-v").splitlines()}
            self.assertEqual(tags, {"H"}, f"no flag in {tree}'s index")
        for tree in (assumed, sparse):
            self.assertEqual(self.git(tree, "status", "--porcelain"), "", tree)
        before = self.snapshot(root)
        result = self.preview(root)
        self.assert_status(result, 0)
        document = result.document
        self.assertEqual([entry["path"] for entry in document["selected"]], [str(plain)])
        self.assertEqual(by_path(document), {str(root): "main-worktree", str(assumed): "hidden-local-state",
                                             str(sparse): "hidden-local-state"})
        human = self.run_cli("clean", root, "--all-safe")
        self.assert_status(human, 0)
        lines = human.stdout.splitlines()
        group = lines.index(TEXT["excluded_group"].format(REASON="hidden-local-state", K=2,
                                                          NEXT_STEP=STEPS["hidden-local-state"]))
        self.assertEqual(lines[group + 1:group + 3],
                         [TEXT["excluded_row"].format(PATH=assumed, BRANCH="002-assumed"),
                          TEXT["excluded_row"].format(PATH=sparse, BRANCH="003-sparse")])
        self.assertEqual(self.snapshot(root), before)
        self.assertEqual((assumed / "work-002-assumed").read_text(), "hidden edit", "the edit survives")
        # The edits survive an apply of the rest.
        result, records = self.run_counted("clean", root, "--all-safe", "--apply", "--yes")
        self.assert_status(result, 0)
        self.assertEqual([argv_words(record)[-1] for record in removals(records)], [str(plain)])
        self.assertFalse(plain.exists())
        self.assertEqual((assumed / "work-002-assumed").read_text(), "hidden edit", "the edit survives the apply")
        self.assertIn("S sparse/file", self.git(sparse, "ls-files", "-v").splitlines())

    def test_clean_an_edit_hidden_by_assume_unchanged_survives(self):
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-assumed", path=self.base / "assumed")
        self.git(tree, "update-index", "--assume-unchanged", "work-001-assumed")
        (tree / "work-001-assumed").write_text("hidden edit")
        self.assertEqual(self.git(tree, "status", "--porcelain"), "", "the edit is hidden from status")
        before = self.snapshot(root)
        message = TEXT["target_excluded_gate"].format(REASON="hidden-local-state", NEXT_STEP=STEPS["hidden-local-state"])
        result, records = self.run_counted("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes")
        self.assert_status(result, 2)
        self.assertEqual(result.stderr, f"REFUSED: {message}\n")
        self.assertEqual(removals(records), [])
        result = self.run_json("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes", "--json")
        self.assert_refused_target(result, tree, "hidden-local-state", message)
        self.assertEqual(self.snapshot(root), before)
        self.assertEqual((tree / "work-001-assumed").read_text(), "hidden edit", "the edit survives")

    def test_clean_index_gate_reads_that_fail(self):
        # Plan review M5, data-model.md "Gate": an index gate whose read cannot
        # finish decides nothing; the row is inspection-error, the plan
        # incomplete with inspection-incomplete, the preview exit 1, --apply
        # exit 2, and nothing is removed.
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-target", path=self.base / "target")
        fake_dir = self.base / "fake"
        refused = {"code": "inspection-incomplete", "message": TEXT["plan_incomplete"].format(
            CODE="inspection-incomplete", REMEDY=TEXT["remedy_inspection_incomplete"])}

        def git_error(key, **fields):
            return TEXT[key].format(OPERATION=TEXT["row_error_git_operation"].format(SUBCOMMAND="ls-files"), **fields)

        def assert_undecided(document, error):
            self.assertEqual((document["selected"], by_path(document)),
                             ([], {str(root): "main-worktree", str(tree): "inspection-error"}))
            row = row_of(document, tree)
            self.assertEqual((row["classification"], row["recommendation"], row["errors"]),
                             ("inspection-error", INSPECTION_ERROR_ADVICE, [error]))
            self.assertEqual((document["completeness"], document["apply_allowed"], document["refusals"]),
                             ("incomplete", False, [refused]))

        failed = {"code": "probe-failed", "message": git_error(
            "row_error_probe_failed", DETAIL=TEXT["row_error_probe_failed_exit"].format(N=128))}
        # The hang runs under the launcher with its own table (R-29): a probe
        # budget of 1 s, every other value real, so the probe budget in force
        # is 1 s and the hidden-state probe is cut there.
        table = clean_support.timing_table(probe_budget=1)
        timed_out = {"code": "probe-timeout", "message": git_error("row_error_probe_timeout", S="1")}
        for kind, timing, error in (("ls-files-fails-in", None, failed), ("ls-files-hangs-in", table, timed_out)):
            with self.subTest(kind):
                shutil.rmtree(fake_dir, ignore_errors=True)
                fake = clean_support.install_fake_git(fake_dir, kind, path=tree)
                before = self.snapshot(root)
                result, records = self.run_counted("clean", root, "--all-safe", "--json", real=fake, timing=timing)
                self.assert_status(result, 1)
                assert_undecided(self.load_json(result), error)
                hidden = [record for record in records if argv_words(record)[2:] == ["ls-files", "-v", "--stage", "-z"]]
                self.assertEqual([argv_words(record)[:2] for record in hidden], [["-C", str(tree)]])
                result, records = self.run_counted("clean", root, "--all-safe", "--apply", "--yes", "--json",
                                                   real=fake, timing=timing)
                self.assert_status(result, 2)
                assert_undecided(self.load_json(result), error)
                self.assertEqual(removals(records), [])
                self.assertEqual(self.snapshot(root), before, "nothing removed")
        # In process: modules_check()'s filesystem call, the lstat of the row's
        # admin `modules` entry, made to raise PermissionError and then to time
        # out; every other filesystem call runs as it is.
        modules = os.fsencode(self.common_dir(root) / "worktrees" / tree.name / "modules")
        real_fs_call = project.fs_call
        denied = PermissionError(errno.EACCES, os.strerror(errno.EACCES), os.fsdecode(modules))
        cut = project.DriverOutcome(None, "timeout", detail="no answer within 5 s")
        os_error = {"code": "os-error", "message": TEXT["row_error_os_error"].format(
            OPERATION="lstat", STRERROR=os.strerror(errno.EACCES))}
        timeout = {"code": "probe-timeout", "message": TEXT["row_error_probe_timeout"].format(OPERATION="lstat", S="5")}
        for label, answer, error in (("PermissionError", denied, os_error), ("a timeout", cut, timeout)):
            with self.subTest(f"modules_check() meets {label}"):
                calls = []

                def fs_call(fn, *args, **options):
                    if fn is os.lstat and args == (modules,):
                        calls.append(args[0])
                        if isinstance(answer, BaseException):
                            raise answer
                        return answer
                    return real_fs_call(fn, *args, **options)

                before = self.snapshot(root)
                status, out, err = self.main_in_process("clean", root, "--all-safe", "--json", fs_call=fs_call)
                self.assertEqual((status, err), (1, ""), out)
                assert_undecided(json.loads(out), error)
                status, out, err = self.main_in_process("clean", root, "--all-safe", "--apply", "--yes", "--json",
                                                        fs_call=fs_call)
                self.assertEqual(status, 2, out + err)
                assert_undecided(json.loads(out), error)
                self.assertEqual(calls, [modules, modules], "one modules check per run")
                self.assertEqual(self.snapshot(root), before, "nothing removed")
                self.assertTrue(tree.is_dir())

    # T063: "Submodules" (its after-confirmation clause is T083's); "A worktree
    # holding a submodule is never offered".

    def test_clean_submodules(self):
        root = self.repo()
        self.bare_remote()
        # The plain row and the modules-only row first: a worktree added after a
        # gitlink reaches the merge target's tree holds that gitlink too.
        plain = self.merged_worktree("001-plain", path=self.base / "plain")

        def added_then_removed(tree):
            self.submodule(tree, "sub-removed")
            self.commit(tree, "add sub-removed")
            self.git(tree, "rm", "-q", "sub-removed")

        left = self.merged_worktree("002-modules-left", path=self.base / "modules-left", setup=added_then_removed)
        populated = self.merged_worktree("003-populated", path=self.base / "populated",
                                         setup=lambda tree: self.submodule(tree, "sub-populated"))
        deinitialized = self.merged_worktree("004-deinitialized", path=self.base / "deinitialized",
                                             setup=lambda tree: self.submodule(tree, "sub-deinitialized"))
        self.git(deinitialized, "submodule", "deinit", "-q", "-f", "sub-deinitialized")
        never = self.merged_worktree("005-never-initialized", path=self.base / "never-initialized",
                                     setup=lambda tree: self.gitlink(tree, "vendored"))
        # What each holds: the modules-only row no gitlink but its admin
        # directory's `modules` entry; the others a gitlink in their own index.
        admin = self.common_dir(root) / "worktrees"
        self.assertNotIn("160000", self.git(left, "ls-files", "--stage"))
        self.assertTrue((admin / left.name / "modules" / "sub-removed").is_dir())
        self.assertFalse((admin / plain.name / "modules").exists())
        self.assertFalse((deinitialized / "sub-deinitialized" / ".git").exists(), "deinitialized")
        self.assertFalse((admin / never.name / "modules").exists(), "never initialized")
        for tree in (populated, deinitialized, never):
            self.assertIn("160000", self.git(tree, "ls-files", "--stage"), tree)
        before = self.snapshot(root)
        result = self.preview(root)
        self.assert_status(result, 0)
        document = result.document
        self.assertEqual([entry["path"] for entry in document["selected"]], [str(plain)])
        self.assertEqual(by_path(document), {
            str(root): "main-worktree", str(left): "contains-submodule", str(populated): "contains-submodule",
            str(deinitialized): "contains-submodule", str(never): "contains-submodule"})
        self.assertEqual(self.snapshot(root), before)
        # An apply removes only the plain worktree.
        result, records = self.run_counted("clean", root, "--all-safe", "--apply", "--yes")
        self.assert_status(result, 0)
        self.assertEqual([argv_words(record)[-1] for record in removals(records)], [str(plain)])
        self.assertFalse(plain.exists())
        for tree in (left, populated, deinitialized, never):
            self.assertTrue(tree.is_dir(), tree)

    def test_clean_submodules_beside_hidden_local_state(self):
        # Lane 3's W4 M-3 (lead ruling R-117): one worktree whose own index holds
        # both a gitlink and an entry flagged assume-unchanged is excluded by gate
        # 9, contains-submodule, never by gate 10, hidden-local-state, in the gate
        # order (pcl:577-583): the hidden-state probe decides the gitlink first.
        # HiddenStateParser stops at the first gitlink, so the flagged entry is
        # put before it in path order, `work-001-both` before `zz-vendored`.
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-both", path=self.base / "both",
                                    setup=lambda tree: self.gitlink(tree, "zz-vendored"))
        self.git(tree, "update-index", "--assume-unchanged", "work-001-both")
        self.assertEqual([(line[:1], line.split()[1], line.split("\t")[1])
                          for line in self.git(tree, "ls-files", "-v", "--stage").splitlines()],
                         [("h", "100644", "work-001-both"), ("H", "160000", "zz-vendored")])
        self.assertFalse((self.common_dir(root) / "worktrees" / tree.name / "modules").exists())
        # The probe's parser reads both: the flag, then the gitlink, its bound.
        parser = project.HiddenStateParser()
        parser.feed(os.fsencode(self.git(tree, "ls-files", "-v", "--stage", "-z")))
        self.assertEqual(parser.finish(), {"gitlink": True, "hidden": True, "entries": 1})
        before = self.snapshot(root)
        result = self.preview(root)
        self.assert_status(result, 0)
        self.assertEqual((result.document["selected"], by_path(result.document)),
                         ([], {str(root): "main-worktree", str(tree): "contains-submodule"}))
        self.assertEqual(row_of(result.document, tree)["classification"], "merged-removable")
        message = TEXT["target_excluded_gate"].format(REASON="contains-submodule", NEXT_STEP=STEPS["contains-submodule"])
        result, records = self.run_counted("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes")
        self.assert_status(result, 2)
        self.assertEqual(result.stderr, f"REFUSED: {message}\n")
        self.assertEqual(removals(records), [])
        result = self.run_json("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes", "--json")
        self.assert_refused_target(result, tree, "contains-submodule", message)
        self.assertEqual(self.snapshot(root), before, "nothing removed")

    def test_clean_a_worktree_holding_a_submodule_is_never_offered(self):
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-populated", path=self.base / "populated", setup=self.submodule)
        self.assertTrue((tree / "sub" / ".git").exists(), "the submodule is populated")
        before = self.snapshot(root)
        message = TEXT["target_excluded_gate"].format(REASON="contains-submodule", NEXT_STEP=STEPS["contains-submodule"])
        result, records = self.run_counted("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes")
        self.assert_status(result, 2)
        self.assertEqual(result.stderr, f"REFUSED: {message}\n")
        self.assertEqual(removals(records), [], "the counting log holds no worktree remove")
        result = self.run_json("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes", "--json")
        self.assert_refused_target(result, tree, "contains-submodule", message)
        self.assertEqual(self.snapshot(root), before)

    # T064: "A merged worktree whose upstream was deleted"; "A deleted upstream
    # is remote-gone". They pin T032, T049 and T057.

    def test_clean_a_merged_worktree_whose_upstream_was_deleted(self):
        root = self.repo()
        self.bare_remote()
        merged = self.merged_worktree("001-merged", path=self.base / "merged")
        unmerged = self.pushed_worktree("002-unmerged", self.base / "unmerged")
        for branch in ("001-merged", "002-unmerged"):
            self.git(root, "push", "-q", "origin", "--delete", branch)
            self.assertEqual(self.git(root, "for-each-ref", f"refs/remotes/origin/{branch}"), "")
            self.assertEqual(self.git(root, "config", f"branch.{branch}.merge").strip(), f"refs/heads/{branch}")
        report = self.run_json("clean", root, "--json").document
        expected = {"001-merged": ("merged-removable", MERGED_REMOVABLE_ADVICE),
                    "002-unmerged": ("remote-gone", "Confirm the branch should be republished before removing local work.")}
        for tree, branch in ((merged, "001-merged"), (unmerged, "002-unmerged")):
            row = row_of(report, tree)
            self.assertEqual((row["classification"], row["recommendation"]), expected[branch])
            self.assertEqual((row["upstream"], row["remote_present"], row["ahead"], row["behind"]),
                             (f"origin/{branch}", False, None, None))
        before = self.snapshot(root)
        result = self.preview(root)
        self.assert_status(result, 0)
        self.assertEqual([entry["path"] for entry in result.document["selected"]], [str(merged)])
        self.assertEqual(by_path(result.document), {str(root): "main-worktree", str(unmerged): "remote-gone"})
        [entry] = result.document["selected"]
        self.assertEqual((entry["upstream"], entry["upstream_oid"], entry["remote_present"]),
                         ("origin/001-merged", None, False))
        self.assertEqual(self.snapshot(root), before)
        # Naming the unmerged one refuses with its class; it is preserved.
        result = self.run_json("clean", root, "--apply", "--action", "remove", "--worktree", unmerged, "--yes",
                               "--json")
        self.assert_refused_target(result, unmerged, "remote-gone",
                                   TEXT["target_excluded_class"].format(CLASS="remote-gone"))
        self.assertEqual(self.snapshot(root), before, "the unmerged one is preserved")
        # --worktree naming the merged one with --yes removes it and keeps its branch.
        head = self.git(merged, "rev-parse", "HEAD").strip()
        result, records = self.run_counted("clean", root, "--apply", "--action", "remove", "--worktree", merged,
                                           "--yes")
        self.assert_status(result, 0)
        self.assertEqual([argv_words(record)[-1] for record in removals(records)], [str(merged)])
        self.assertFalse(merged.exists())
        self.assertEqual(self.git(root, "rev-parse", "refs/heads/001-merged").strip(), head, "the branch is kept")
        self.assertTrue(unmerged.is_dir(), "the unmerged one is preserved")

    def test_clean_a_deleted_upstream_is_remote_gone(self):
        root = self.repo()
        self.bare_remote()
        gone = self.pushed_worktree("001-gone", self.base / "gone")
        self.git(root, "push", "-q", "origin", "--delete", "001-gone")
        unpublished = self.base / "unpublished"
        self.git(root, "worktree", "add", "-q", "-b", "002-unpublished", unpublished)
        (unpublished / "work").write_text("work")
        self.commit(unpublished)
        report = self.run_json("clean", root, "--json").document
        self.assertEqual([(row["path"], row["classification"], row["upstream"]) for row in report["worktrees"]],
                         [(str(root), "protected-default", None), (str(gone), "remote-gone", "origin/001-gone"),
                          (str(unpublished), "unpublished", None)])
        before = self.snapshot(root)
        result = self.preview(root)
        self.assert_status(result, 0)
        self.assertEqual((result.document["selected"], by_path(result.document)),
                         ([], {str(root): "main-worktree", str(gone): "remote-gone", str(unpublished): "unpublished"}))
        # Both are preserved: an apply of the fresh plan has nothing to remove.
        result, records = self.run_counted("clean", root, "--all-safe", "--apply", "--yes")
        self.assert_status(result, 0)
        self.assertEqual(result.stdout.splitlines()[-1], TEXT["empty_line"])
        self.assertEqual(removals(records), [])
        self.assertEqual(self.snapshot(root), before)

    # T065: "Dirty or unmerged work is preserved"; "A merged worktree has
    # ignored local files"; "Default branch cannot be established locally";
    # "Pushed feature branch has an open review path"; "The main worktree and
    # a locked worktree". They pin T050 and T053.

    def test_clean_dirty_or_unmerged_work_is_preserved(self):
        root = self.repo()
        self.bare_remote()
        dirty = self.merged_worktree("001-dirty", path=self.base / "dirty")
        (dirty / "uncommitted").write_text("preserve")
        unmerged = self.pushed_worktree("002-unmerged", self.base / "unmerged")
        before = self.snapshot(root)
        report = self.run_cli("clean", root)
        self.assert_status(report, 0)
        lines = report.stdout.splitlines()
        for tree, branch, label, advice in ((dirty, "001-dirty", "DIRTY", DIRTY_ADVICE),
                                            (unmerged, "002-unmerged", "PUSHED-UNMERGED", REVIEW_ADVICE)):
            [at] = [index for index, line in enumerate(lines) if line.startswith(f"{label}: {tree} [{branch}] ")]
            self.assertEqual(lines[at + 1], f"  {advice}")
        self.assertNotIn("worktree remove", report.stdout, "no destructive action is proposed")
        result = self.preview(root)
        self.assertEqual((result.document["selected"], by_path(result.document)),
                         ([], {str(root): "main-worktree", str(dirty): "dirty", str(unmerged): "pushed-unmerged"}))
        result, records = self.run_counted("clean", root, "--all-safe", "--apply", "--yes")
        self.assert_status(result, 0)
        self.assertEqual(result.stdout.splitlines()[-1], TEXT["empty_line"])
        self.assertEqual(removals(records), [])
        for tree, reason in ((dirty, "dirty"), (unmerged, "pushed-unmerged")):
            result = self.run_json("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes",
                                   "--json")
            self.assert_refused_target(result, tree, reason, TEXT["target_excluded_class"].format(CLASS=reason))
        self.assertEqual(self.snapshot(root), before)

    def test_clean_a_merged_worktree_has_ignored_local_files(self):
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-ignored", path=self.base / "ignored",
                                    setup=lambda tree: (tree / ".gitignore").write_text("local.env\n"))
        (tree / "local.env").write_text("preserve")
        before = self.snapshot(root)
        result = self.preview(root)
        self.assertEqual((result.document["selected"], by_path(result.document)),
                         ([], {str(root): "main-worktree", str(tree): "ignored-local-files"}))
        self.assertEqual(row_of(result.document, tree)["ignored_files"], 1)
        result, records = self.run_counted("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes")
        self.assert_status(result, 2)
        message = TEXT["target_excluded_class"].format(CLASS="ignored-local-files")
        self.assertEqual(result.stderr, f"REFUSED: {message}\n")
        self.assertEqual(removals(records), [])
        result = self.run_json("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes", "--json")
        self.assert_refused_target(result, tree, "ignored-local-files", message)
        self.assertEqual(self.snapshot(root), before)
        self.assertEqual((tree / "local.env").read_text(), "preserve")

    def test_clean_default_branch_cannot_be_established_locally(self):
        # No manifest tracking_branch, no origin/HEAD, neither main nor master;
        # the current branch, trunk, is never taken as the merge target.
        root = self.repo(branch="trunk")
        tree = self.base / "feature"
        self.git(root, "worktree", "add", "-q", "-b", "001-feature", tree)
        before = self.snapshot(root)
        for words in ((), ("--all-safe",), ("--all-safe", "--apply", "--yes"),
                      ("--apply", "--action", "remove", "--worktree", tree, "--yes")):
            with self.subTest(arguments=words):
                result, records = self.run_counted("clean", root, *words)
                self.assert_status(result, 2)
                self.assertEqual((result.stdout, result.stderr), ("", f"REFUSED: {TEXT['no_merge_target']}\n"))
                self.assertEqual(removals(records), [])
                result = self.run_json("clean", root, *words, "--json")
                self.assert_status(result, 2)
                self.assertEqual((result.document["code"], result.document["error"], result.document["merge_target"]),
                                 ("no-merge-target", TEXT["no_merge_target"], None))
        self.assertEqual(self.snapshot(root), before)

    def test_clean_pushed_feature_branch_has_an_open_review_path(self):
        root = self.repo()
        self.bare_remote()
        tree = self.pushed_worktree("001-feature", self.base / "feature")
        head = self.git(tree, "rev-parse", "HEAD").strip()
        report = self.run_cli("clean", root)
        self.assert_status(report, 0)
        lines = report.stdout.splitlines()
        at = lines.index(f"PUSHED-UNMERGED: {tree} [001-feature] dirty=False; upstream=origin/001-feature; "
                         "ahead=0, behind=0; merged=False")
        self.assertEqual(lines[at + 1], f"  {REVIEW_ADVICE}")
        result, records = self.run_counted("clean", root, "--all-safe", "--apply", "--yes")
        self.assert_status(result, 0)
        self.assertEqual(removals(records), [])
        self.assertTrue(tree.is_dir(), "the worktree remains")
        self.assertEqual(self.git(root, "rev-parse", "refs/heads/001-feature").strip(), head, "the branch remains")

    def test_clean_the_main_worktree_and_a_locked_worktree(self):
        root = self.repo()
        self.bare_remote()
        locked = self.merged_worktree("001-locked", path=self.base / "locked")
        self.git(root, "worktree", "lock", locked)
        before = self.snapshot(root)
        cases = ((root, "main-worktree", TEXT["target_excluded_class"].format(CLASS="protected-default")),
                 (locked, "locked-worktree", TEXT["target_excluded_gate"].format(
                     REASON="locked-worktree", NEXT_STEP=STEPS["locked-worktree"])))
        for tree, reason, message in cases:
            with self.subTest(reason):
                result, records = self.run_counted("clean", root, "--apply", "--action", "remove", "--worktree",
                                                   tree, "--yes")
                self.assert_status(result, 2)
                self.assertEqual(result.stderr, f"REFUSED: {message}\n")
                self.assertEqual(removals(records), [])
                result = self.run_json("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes",
                                       "--json")
                self.assert_refused_target(result, tree, reason, message)
        self.assertEqual(self.snapshot(root), before, "nothing removed")


if __name__ == "__main__":
    unittest.main()
