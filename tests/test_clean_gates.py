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

    def test_clean_submodules_beside_hidden_local_state_with_a_modules_entry(self):
        # Lead ruling R-155 (lane 3's W19 M-3, mutants G9-10b and G9-10c): the
        # `modules` check runs before the hidden-state probe (index_gates()), so
        # a worktree whose admin directory holds a `modules` entry is
        # contains-submodule, never hidden-local-state, though its index holds
        # an entry flagged assume-unchanged. Two worktrees:
        # - 001-left: a submodule added and removed again, which leaves its
        #   repository under the admin directory's `modules` and no gitlink.
        #   Only this shape tells G9-10b apart, since the probe, run first,
        #   still answers contains-submodule for any gitlink it reads.
        # - 002-both: a submodule added, so a gitlink, a .gitmodules entry and a
        #   `modules` entry, with the flagged entry before the gitlink in path
        #   order, so the probe reads both (G9-10c).
        root = self.repo()
        self.bare_remote()

        def added_then_removed(tree):
            self.submodule(tree, "sub-removed")
            self.commit(tree, "add sub-removed")
            self.git(tree, "rm", "-q", "sub-removed")

        left = self.merged_worktree("001-left", path=self.base / "left", setup=added_then_removed)
        # Last: once merged, its gitlink is in the merge target's tree.
        both = self.merged_worktree("002-both", path=self.base / "both",
                                    setup=lambda tree: self.submodule(tree, "zz-sub"))
        admin = self.common_dir(root) / "worktrees"
        for tree, name, gitlink in ((left, "001-left", False), (both, "002-both", True)):
            self.git(tree, "update-index", "--assume-unchanged", "work-" + name)
            self.assertTrue((admin / tree.name / "modules").is_dir(), name)
            parser = project.HiddenStateParser()
            parser.feed(os.fsencode(self.git(tree, "ls-files", "-v", "--stage", "-z")))
            found = parser.finish()
            self.assertEqual((found["gitlink"], found["hidden"]), (gitlink, True), name)
        self.assertEqual(self.git(both, "config", "--file", ".gitmodules", "--get", "submodule.zz-sub.path"),
                         "zz-sub\n")
        before = self.snapshot(root)
        result = self.preview(root)
        self.assert_status(result, 0)
        self.assertEqual((result.document["selected"], by_path(result.document)),
                         ([], {str(root): "main-worktree", str(left): "contains-submodule",
                               str(both): "contains-submodule"}))
        for tree in (left, both):
            self.assertEqual(row_of(result.document, tree)["classification"], "merged-removable", tree)
        self.assertEqual(self.snapshot(root), before, "a preview changes nothing")

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

    # LQ-14 (Brett Heap, 2026-10-21; design D22; lead rulings R-124, R-126 and
    # R-146): the gate `operation-in-progress`, one listing of the row's admin
    # directory. Scenarios "An operation in progress" and "A squash merge that
    # holds an autostash", the eleven markers, and the listing's failures.

    # The combined status probe's words after `-C PATH` (D6, D11).
    STATUS_WORDS = ("status", "--porcelain=v1", "-z", "--untracked-files=normal", "--ignored=matching")
    # The eleven markers of D22, written here as literals (rule 11).
    MARKERS = ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "BISECT_LOG", "BISECT_START", "rebase-apply",
               "rebase-merge", "sequencer", "MERGE_AUTOSTASH", "NOTES_MERGE_PARTIAL", "NOTES_MERGE_REF")

    def admin_dir(self, tree):
        """The administrative directory of the linked worktree at tree."""
        return Path(self.git(tree, "rev-parse", "--path-format=absolute", "--git-dir").rstrip("\n"))

    def side_commits(self, root, branch, *changes):
        """One commit per change ({file: text}) on a new branch BRANCH from
        root's first commit, made in a temporary worktree that is then removed,
        so the branch is no worktree row. Returns the commits' SHAs."""
        first = self.git(root, "rev-list", "--max-parents=0", "HEAD").strip()
        tmp = self.base / ("side-" + branch)
        self.git(root, "worktree", "add", "-q", "-b", branch, tmp, first)
        shas = []
        for change in changes:
            for name, text in change.items():
                (tmp / name).write_text(text)
            shas.append(self.commit(tmp, f"side {len(shas) + 1}"))
        self.git(root, "worktree", "remove", tmp)
        return shas

    def assert_status_clean(self, tree):
        """The combined status probe prints no record for tree."""
        self.assertEqual(self.git(tree, *self.STATUS_WORDS), "", f"{tree} reads clean to the status probe")

    def test_clean_an_operation_in_progress(self):
        root = self.repo()
        self.bare_remote()
        plain = self.merged_worktree("001-plain", path=self.base / "plain")
        branches = {"am": "002-am", "cherry-pick": "003-cherry-pick", "merge": "004-merge", "notes": "005-notes",
                    "bisect": "006-bisect"}
        trees = {name: self.merged_worktree(branch, path=self.base / name) for name, branch in branches.items()}
        # A side branch whose first two commits add each worktree's own file
        # with other content, so that a patch of the first does not apply and a
        # cherry-pick of the second stops at a conflict; a third adds a file of
        # its own.
        add_am, add_pick, third = self.side_commits(root, "side", {"work-002-am": "other\n"},
                                                    {"work-003-cherry-pick": "other\n"}, {"side-file": "side\n"})
        patch = self.base / "add-am.patch"
        patch.write_text(self.git(root, "format-patch", "-1", "--stdout", add_am))
        self.git(trees["am"], "am", patch, check=False)
        self.assertTrue((self.admin_dir(trees["am"]) / "rebase-apply").is_dir(), "the failed am stopped")
        self.git(trees["cherry-pick"], "cherry-pick", add_pick, third, check=False)
        self.git(trees["cherry-pick"], "checkout", "--ours", "work-003-cherry-pick")
        self.git(trees["cherry-pick"], "add", "work-003-cherry-pick")
        self.git(trees["merge"], "merge", "-q", "--no-commit", "-s", "ours", "side")
        notes = trees["notes"]
        self.git(notes, "notes", "add", "-m", "base", "HEAD")
        self.git(notes, "update-ref", "refs/notes/other", "refs/notes/commits")
        self.git(notes, "notes", "add", "-f", "-m", "mine", "HEAD")
        self.git(notes, "notes", "--ref=other", "add", "-f", "-m", "theirs", "HEAD")
        self.git(notes, "notes", "merge", "refs/notes/other", check=False)
        self.git(trees["bisect"], "bisect", "start", "--no-checkout")
        expected = {"am": {"rebase-apply"}, "cherry-pick": {"CHERRY_PICK_HEAD", "sequencer"},
                    "merge": {"MERGE_HEAD"}, "notes": {"NOTES_MERGE_PARTIAL", "NOTES_MERGE_REF"},
                    "bisect": {"BISECT_LOG", "BISECT_START"}}
        for name, tree in trees.items():
            with self.subTest(made_by=name):
                self.assertEqual(set(self.MARKERS) & set(os.listdir(self.admin_dir(tree))), expected[name])
                self.assert_status_clean(tree)
                self.assertEqual(self.git(tree, "branch", "--show-current").strip(), branches[name], "not detached")
        before = self.snapshot(root)
        result = self.preview(root)
        self.assert_status(result, 0)
        document = result.document
        self.assertEqual([entry["path"] for entry in document["selected"]], [str(plain)])
        self.assertEqual(by_path(document), {str(root): "main-worktree",
                                             **{str(tree): "operation-in-progress" for tree in trees.values()}})
        for tree in trees.values():
            self.assertEqual((row_of(document, tree)["classification"], row_of(document, tree)["errors"]),
                             ("merged-removable", []), "the gate excludes without relabelling")
        human = self.run_cli("clean", root, "--all-safe")
        self.assert_status(human, 0)
        lines = human.stdout.splitlines()
        group = lines.index(TEXT["excluded_group"].format(REASON="operation-in-progress", K=5,
                                                          NEXT_STEP=STEPS["operation-in-progress"]))
        ordered = sorted(trees.values(), key=lambda tree: os.fsencode(tree))
        names = {tree: branches[name] for name, tree in trees.items()}
        self.assertEqual(lines[group + 1:group + 6],
                         [TEXT["excluded_row"].format(PATH=tree, BRANCH=names[tree]) for tree in ordered])
        self.assertEqual(self.snapshot(root), before, "a preview changes nothing")
        # The batch removes none of them.
        result, records = self.run_counted("clean", root, "--all-safe", "--apply", "--yes")
        self.assert_status(result, 0)
        self.assertEqual([argv_words(record)[-1] for record in removals(records)], [str(plain)])
        for name, tree in trees.items():
            self.assertTrue(tree.is_dir(), name)
            self.assertEqual(set(self.MARKERS) & set(os.listdir(self.admin_dir(tree))), expected[name])
        # Naming one refuses with target-excluded, reason operation-in-progress.
        message = TEXT["target_excluded_gate"].format(REASON="operation-in-progress",
                                                      NEXT_STEP=STEPS["operation-in-progress"])
        result, records = self.run_counted("clean", root, "--apply", "--action", "remove", "--worktree",
                                           trees["merge"], "--yes")
        self.assert_status(result, 2)
        self.assertEqual(result.stderr, f"REFUSED: {message}\n")
        self.assertEqual(removals(records), [])
        for tree in trees.values():
            with self.subTest(named=str(tree)):
                result = self.run_json("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes",
                                       "--json")
                self.assert_refused_target(result, tree, "operation-in-progress", message)
        # Once each is aborted, each is selected as before; the aborted notes
        # merge leaves its NOTES_MERGE_WORKTREE behind, which is no marker.
        self.git(trees["am"], "am", "--abort")
        self.git(trees["cherry-pick"], "cherry-pick", "--abort")
        self.git(trees["merge"], "merge", "--abort")
        self.git(notes, "notes", "merge", "--abort")
        self.git(trees["bisect"], "bisect", "reset")
        self.assertTrue((self.admin_dir(notes) / "NOTES_MERGE_WORKTREE").exists())
        result = self.preview(root)
        self.assert_status(result, 0)
        self.assertEqual([entry["path"] for entry in result.document["selected"]], [str(tree) for tree in ordered])
        self.assertEqual(by_path(result.document), {str(root): "main-worktree"})

    @clean_support.not_root
    def test_clean_an_operation_in_progress_admin_directory_that_cannot_be_listed(self):
        # The scenario's last clause: read permission removed from the admin
        # directory while its gitdir file stays readable (write and search
        # kept), so that only the listing fails.
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-unlisted", path=self.base / "unlisted")
        admin = self.admin_dir(tree)
        admin.chmod(0o300)
        self.addCleanup(admin.chmod, 0o700)
        self.assertTrue((admin / "gitdir").read_text().strip())
        refused = {"code": "inspection-incomplete", "message": TEXT["plan_incomplete"].format(
            CODE="inspection-incomplete", REMEDY=TEXT["remedy_inspection_incomplete"])}
        error = {"code": "os-error", "message": TEXT["row_error_os_error"].format(
            OPERATION="listdir", STRERROR=os.strerror(errno.EACCES))}
        for words, status in ((("--all-safe", "--json"), 1), (("--all-safe", "--apply", "--yes", "--json"), 2)):
            with self.subTest(words=words):
                result, records = self.run_counted("clean", root, *words)
                self.assert_status(result, status)
                document = self.load_json(result)
                self.assertEqual((document["selected"], by_path(document)),
                                 ([], {str(root): "main-worktree", str(tree): "inspection-error"}))
                row = row_of(document, tree)
                self.assertEqual((row["classification"], row["recommendation"], row["errors"]),
                                 ("inspection-error", INSPECTION_ERROR_ADVICE, [error]))
                self.assertEqual((document["completeness"], document["apply_allowed"], document["refusals"]),
                                 ("incomplete", False, [refused]))
                self.assertEqual(removals(records), [])
        self.assertTrue(tree.is_dir())

    def test_clean_operation_in_progress_markers(self):
        # Each of the eleven markers, of any kind (a file, a directory, a
        # dangling symbolic link), excludes an otherwise eligible row; the
        # entries that are no marker, NOTES_MERGE_WORKTREE and SQUASH_MSG, do not.
        root = self.repo()
        self.bare_remote()
        marked = {}
        for number, marker in enumerate(self.MARKERS, start=1):
            tree = self.merged_worktree(f"{number:03d}-marker", path=self.base / f"m{number:02d}-{marker}")
            place = self.admin_dir(tree) / marker
            kind = ("file", "directory", "symlink")[number % 3]
            if kind == "file":
                place.write_text("planted\n")
            elif kind == "directory":
                place.mkdir()
            else:
                place.symlink_to(self.base / "nowhere")
            marked[str(tree)] = kind
        unmarked = []
        for number, (name, directory) in enumerate((("NOTES_MERGE_WORKTREE", True), ("SQUASH_MSG", False)), start=20):
            tree = self.merged_worktree(f"{number:03d}-unmarked", path=self.base / f"u{number}-{name}")
            place = self.admin_dir(tree) / name
            place.mkdir() if directory else place.write_text("squash\n")
            unmarked.append(tree)
        plain = self.merged_worktree("030-plain", path=self.base / "z-plain")
        result = self.preview(root)
        self.assert_status(result, 0)
        self.assertEqual([entry["path"] for entry in result.document["selected"]],
                         [str(tree) for tree in unmarked] + [str(plain)])
        self.assertEqual(by_path(result.document), {str(root): "main-worktree",
                                                    **{path: "operation-in-progress" for path in marked}})
        self.assertEqual(sorted(set(marked.values())), ["directory", "file", "symlink"])

    def test_clean_operation_in_progress_markers_from_real_operations(self):
        # The markers a revert and both rebase backends leave, made by Git. A
        # revert whose index and tree are put back to the head is excluded as
        # operation-in-progress; a stopped rebase detaches HEAD, so its row is
        # `detached` first, and the listing alone is checked to find it.
        root = self.repo()
        self.bare_remote()
        revert = self.merged_worktree("001-revert", path=self.base / "revert")
        merge_backend = self.merged_worktree("002-rebase-merge", path=self.base / "rebase-merge")
        apply_backend = self.merged_worktree("003-rebase-apply", path=self.base / "rebase-apply")
        [side] = self.side_commits(root, "side", {"work-003-rebase-apply": "other\n"})
        self.git(revert, "revert", "--no-commit", "HEAD")
        self.git(revert, "checkout", "HEAD", "--", ".")
        self.assert_status_clean(revert)
        self.git(merge_backend, "rebase", "--exec", "false", "HEAD~1", check=False)
        self.git(apply_backend, "rebase", "--apply", "side", check=False)
        found = {"revert": "REVERT_HEAD", "merge": "rebase-merge", "apply": "rebase-apply"}
        common = os.fsencode(self.common_dir(root))
        for name, tree in (("revert", revert), ("merge", merge_backend), ("apply", apply_backend)):
            with self.subTest(made_by=name):
                self.assertIn(found[name], os.listdir(self.admin_dir(tree)))
                with project.Invocation("clean") as run:
                    self.assertEqual(project.operation_check(common, os.fsencode(tree.name), run),
                                     ("operation-in-progress", None))
        result = self.preview(root)
        self.assert_status(result, 0)
        reasons = by_path(result.document)
        self.assertEqual((result.document["selected"], reasons[str(revert)], reasons[str(merge_backend)]),
                         ([], "operation-in-progress", "detached"))
        self.assertNotIn(str(apply_backend), [entry["path"] for entry in result.document["selected"]])

    def test_clean_a_squash_merge_that_holds_an_autostash(self):
        version = clean_support.GIT_VERSION
        if version is None or not (version >= (2, 40) or version <= (2, 36)):
            self.skipTest("needs Git 2.40 or later, which keeps the autostash, or Git 2.36, which applies it at "
                          "once; found " + (".".join(map(str, version)) if version else "none"))
        root = self.repo()
        self.bare_remote()
        self.side_commits(root, "side", {"side-file": "side\n"})
        tree = self.merged_worktree("001-squash", path=self.base / "squash")
        (tree / "work-001-squash").write_text("an edit to a tracked file\n")
        self.git(tree, "merge", "-q", "--squash", "--autostash", "-s", "ours", "side")
        held = self.admin_dir(tree) / "MERGE_AUTOSTASH"
        result = self.preview(root)
        self.assert_status(result, 0)
        if version <= (2, 36):
            # Git 2.36.6 applies the autostash at once: the edit is back, dirty.
            self.assertFalse(held.exists())
            self.assertEqual((tree / "work-001-squash").read_text(), "an edit to a tracked file\n")
            self.assertEqual(by_path(result.document), {str(root): "main-worktree", str(tree): "dirty"})
            return
        # Only MERGE_AUTOSTASH holds the edit: no stash entry, no status record.
        self.assertTrue(held.is_file())
        self.assertEqual(self.git(tree, "stash", "list"), "")
        self.assert_status_clean(tree)
        self.assertEqual((result.document["selected"], by_path(result.document)),
                         ([], {str(root): "main-worktree", str(tree): "operation-in-progress"}))
        result, records = self.run_counted("clean", root, "--all-safe", "--apply", "--yes")
        self.assert_status(result, 0)
        self.assertEqual(removals(records), [])
        self.assertTrue(tree.is_dir())
        self.assertTrue(held.is_file(), "the worktree and its MERGE_AUTOSTASH stay")

    def test_clean_operation_in_progress_listing_that_fails(self):
        # R-124: a listing that fails decides nothing. In process, the listing
        # of the row's admin directory made to raise PermissionError, to time
        # out at its budget and to be cut by the work deadline; every other
        # filesystem call runs as it is. The first two leave the plan
        # incomplete with inspection-incomplete, the deadline with
        # deadline-exceeded; the preview exits 1, --apply 2, nothing removed.
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-target", path=self.base / "target")
        admin = os.fsencode(self.common_dir(root) / "worktrees" / tree.name)
        real_fs_call = project.fs_call
        denied = PermissionError(errno.EACCES, os.strerror(errno.EACCES), os.fsdecode(admin))
        cases = (
            ("PermissionError", denied, {"code": "os-error", "message": TEXT["row_error_os_error"].format(
                OPERATION="listdir", STRERROR=os.strerror(errno.EACCES))}, "inspection-incomplete"),
            ("a timeout", project.DriverOutcome(None, "timeout", detail="no answer within 5 s"),
             {"code": "probe-timeout", "message": TEXT["row_error_probe_timeout"].format(OPERATION="listdir", S="5")},
             "inspection-incomplete"),
            ("the work deadline", project.DriverOutcome(None, "deadline", detail="no time was left to start it"),
             {"code": "deadline-exceeded", "message": TEXT["row_error_deadline_exceeded"].format(
                 OPERATION="listdir")}, "deadline-exceeded"),
        )
        remedies = {"inspection-incomplete": TEXT["remedy_inspection_incomplete"],
                    "deadline-exceeded": TEXT["remedy_deadline_exceeded"]}
        for label, answer, error, code in cases:
            with self.subTest(f"the listing meets {label}"):
                calls = []

                def fs_call(fn, *args, answer=answer, calls=calls, **options):
                    if fn is os.listdir and args == (admin,):
                        calls.append(args[0])
                        if isinstance(answer, BaseException):
                            raise answer
                        return answer
                    return real_fs_call(fn, *args, **options)

                refused = {"code": code, "message": TEXT["plan_incomplete"].format(CODE=code, REMEDY=remedies[code])}
                before = self.snapshot(root)
                for words, status in ((("--all-safe", "--json"), 1), (("--all-safe", "--apply", "--yes", "--json"), 2)):
                    out_status, out, err = self.main_in_process("clean", root, *words, fs_call=fs_call)
                    self.assertEqual(out_status, status, out + err)
                    document = json.loads(out)
                    self.assertEqual((document["selected"], by_path(document)),
                                     ([], {str(root): "main-worktree", str(tree): "inspection-error"}))
                    row = row_of(document, tree)
                    self.assertEqual((row["classification"], row["recommendation"], row["errors"]),
                                     ("inspection-error", INSPECTION_ERROR_ADVICE, [error]))
                    self.assertEqual((document["completeness"], document["apply_allowed"], document["refusals"]),
                                     ("incomplete", False, [refused]))
                self.assertEqual(calls, [admin, admin], "one listing per run")
                self.assertEqual(self.snapshot(root), before, "nothing removed")
                self.assertTrue(tree.is_dir())

    # LQ-13 (Brett Heap, 2026-10-21; design D21; lead rulings R-124 and R-146):
    # the last gate, `worktree-only-commits`: one bounded read of the row's
    # logs/HEAD, then one `rev-list` in the worktree. Scenario "A commit held
    # only by the worktree", and the read's and the child's outcomes.

    # The reachability child's first words after `-C WORKTREE` (D21).
    REACHABILITY = ["rev-list", "--max-count=1", "--glob=refs/worktree"]

    def reachability(self, records):
        """The counted reachability children: (directory, the words after -C DIR)."""
        return [(argv_words(record)[1], argv_words(record)[2:]) for record in records
                if argv_words(record)[2:5] == self.REACHABILITY]

    def detached_commit(self, tree, branch, name):
        """A commit made on tree's detached HEAD, then its branch checked out
        again, so that only tree's HEAD reflog holds it. Returns its SHA."""
        self.git(tree, "checkout", "-q", "--detach")
        (tree / name).write_text("work made only here\n")
        sha = self.commit(tree, "detached work")
        self.git(tree, "checkout", "-q", branch)
        return sha

    def test_clean_a_commit_held_only_by_the_worktree(self):
        root = self.repo()
        self.bare_remote()
        plain = self.merged_worktree("001-plain", path=self.base / "plain")
        detached = self.merged_worktree("002-detached", path=self.base / "detached")
        kept = self.merged_worktree("003-kept", path=self.base / "kept")
        amended = self.merged_worktree("004-amended", path=self.base / "amended")
        lost = self.detached_commit(detached, "002-detached", "detached-work")
        # A commit that only refs/worktree/keep holds: made with commit-tree,
        # so that no HEAD reflog names it, and kept by that per-worktree ref.
        held = self.git(kept, "commit-tree", "HEAD^{tree}", "-p", "HEAD", "-m", "kept work").strip()
        self.git(kept, "update-ref", "refs/worktree/keep", held)
        self.assertEqual(self.git(root, "for-each-ref", "refs/worktree"), "", "the main worktree does not see it")
        # A branch committed on, amended and reset back to its merged head: its
        # HEAD reflog names two commits that only its branch's reflog still holds.
        merged = self.git(amended, "rev-parse", "HEAD").strip()
        (amended / "later").write_text("later\n")
        first = self.commit(amended, "later")
        self.git(amended, "commit", "-q", "--amend", "-m", "later, amended")
        self.git(amended, "reset", "-q", "--hard", merged)
        self.assertNotEqual(self.git(amended, "rev-list", "--max-count=1", first, "--not", "--branches", "--tags",
                                     "--remotes"), "", "only the branch's reflog holds the amended commits")
        for tree in (detached, kept, amended):
            self.assertEqual(self.git(tree, *self.STATUS_WORDS), "", tree)
        before = self.snapshot(root)
        result, records = self.run_counted("clean", root, "--all-safe", "--json")
        self.assert_status(result, 0)
        document = self.load_json(result)
        self.assertEqual([entry["path"] for entry in document["selected"]], [str(amended), str(plain)])
        self.assertEqual(by_path(document), {str(root): "main-worktree", str(detached): "worktree-only-commits",
                                             str(kept): "worktree-only-commits"})
        for tree in (detached, kept):
            self.assertEqual((row_of(document, tree)["classification"], row_of(document, tree)["errors"]),
                             ("merged-removable", []), "the gate excludes without relabelling")
        # One child per row past the cap, in its own worktree; the negatives
        # name the non-zero objects of that row's branch reflog.
        self.assertEqual([directory for directory, _ in self.reachability(records)],
                         [str(amended), str(detached), str(kept), str(plain)])
        [words] = [words for directory, words in self.reachability(records) if directory == str(amended)]
        negatives = words[words.index("--not") + 1:]
        self.assertEqual(negatives[:3], ["--branches", "--tags", "--remotes"])
        self.assertTrue({first, merged} <= set(negatives[3:]), negatives)
        self.assertNotIn("0" * len(merged), negatives, "never the all-zeros object")
        human = self.run_cli("clean", root, "--all-safe")
        self.assert_status(human, 0)
        lines = human.stdout.splitlines()
        group = lines.index(TEXT["excluded_group"].format(REASON="worktree-only-commits", K=2,
                                                          NEXT_STEP=STEPS["worktree-only-commits"]))
        self.assertEqual(lines[group + 1:group + 3],
                         [TEXT["excluded_row"].format(PATH=detached, BRANCH="002-detached"),
                          TEXT["excluded_row"].format(PATH=kept, BRANCH="003-kept")])
        self.assertEqual(self.snapshot(root), before, "a preview changes nothing")
        # The batch removes neither; both commits stay reachable from their worktrees.
        result, records = self.run_counted("clean", root, "--all-safe", "--apply", "--yes")
        self.assert_status(result, 0)
        self.assertEqual([argv_words(record)[-1] for record in removals(records)], [str(amended), str(plain)])
        self.assertTrue(detached.is_dir() and kept.is_dir())
        self.assertEqual(self.git(detached, "rev-parse", "HEAD@{1}").strip(), lost)
        self.assertEqual(self.git(kept, "rev-parse", "refs/worktree/keep").strip(), held)
        # Naming either refuses with target-excluded, reason worktree-only-commits.
        message = TEXT["target_excluded_gate"].format(REASON="worktree-only-commits",
                                                      NEXT_STEP=STEPS["worktree-only-commits"])
        for tree in (detached, kept):
            with self.subTest(named=str(tree)):
                result = self.run_json("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes",
                                       "--json")
                self.assert_refused_target(result, tree, "worktree-only-commits", message)
        # Once the first commit is tagged, and a branch is made at the second and
        # its refs/worktree/keep deleted, both are selected as before.
        self.git(root, "tag", "keep-lost", lost)
        self.git(root, "branch", "keep-held", held)
        self.git(kept, "update-ref", "-d", "refs/worktree/keep")
        result = self.preview(root)
        self.assert_status(result, 0)
        self.assertEqual(([entry["path"] for entry in result.document["selected"]], by_path(result.document)),
                         ([str(detached), str(kept)], {str(root): "main-worktree"}))
        # A HEAD reflog naming a commit whose object was deleted: the child exits
        # 128 (`fatal: bad object`), the row is inspection-error and the plan
        # incomplete; the preview exits 1, --apply 2, nothing removed.
        missing = self.merged_worktree("005-missing", path=self.base / "missing")
        gone = self.detached_commit(missing, "005-missing", "gone-work")
        os.unlink(self.common_dir(root) / "objects" / gone[:2] / gone[2:])
        failed = {"code": "probe-failed", "message": TEXT["row_error_probe_failed"].format(
            OPERATION="git rev-list", DETAIL=TEXT["row_error_probe_failed_exit"].format(N=128))}
        refused = {"code": "inspection-incomplete", "message": TEXT["plan_incomplete"].format(
            CODE="inspection-incomplete", REMEDY=TEXT["remedy_inspection_incomplete"])}
        for words, status in ((("--all-safe", "--json"), 1), (("--all-safe", "--apply", "--yes", "--json"), 2)):
            with self.subTest(missing_object=words):
                result, records = self.run_counted("clean", root, *words)
                self.assert_status(result, status)
                document = self.load_json(result)
                self.assertEqual(by_path(document)[str(missing)], "inspection-error")
                row = row_of(document, missing)
                self.assertEqual((row["classification"], row["errors"]), ("inspection-error", [failed]))
                self.assertEqual((document["completeness"], document["refusals"]), ("incomplete", [refused]))
                self.assertEqual(removals(records), [])
        self.assertTrue(all(tree.is_dir() for tree in (detached, kept, missing)))

    def test_clean_worktree_only_commits_reads_and_children_that_fail(self):
        # R-124: only a decided result gives the reason. In process, the read of
        # the row's logs/HEAD made to raise PermissionError, to time out and to
        # be cut by the work deadline, and the reachability child made to exit
        # 128, to time out and to be cut by the deadline: each makes the row
        # inspection-error, the plan incomplete with inspection-incomplete, or
        # with deadline-exceeded for a deadline cut; nothing is removed.
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-target", path=self.base / "target")
        log = os.fsencode(self.common_dir(root) / "worktrees" / tree.name / "logs" / "HEAD")
        real_fs_call, real_run_bounded = project.fs_call, project.run_bounded
        denied = PermissionError(errno.EACCES, os.strerror(errno.EACCES), os.fsdecode(log))

        def read_error(key, **fields):
            return TEXT[key].format(OPERATION="read", **fields)

        def child_error(key, **fields):
            return TEXT[key].format(OPERATION="git rev-list", **fields)

        reads = (
            ("PermissionError", denied, {"code": "os-error", "message": read_error(
                "row_error_os_error", STRERROR=os.strerror(errno.EACCES))}, "inspection-incomplete"),
            ("a timeout", project.DriverOutcome(None, "timeout", detail="no answer within 5 s"),
             {"code": "probe-timeout", "message": read_error("row_error_probe_timeout", S="5")},
             "inspection-incomplete"),
            ("the work deadline", project.DriverOutcome(None, "deadline", detail="no time was left to start it"),
             {"code": "deadline-exceeded", "message": read_error("row_error_deadline_exceeded")}, "deadline-exceeded"),
        )
        children = (
            ("exit 128", dict(name="failed", status=128), {"code": "probe-failed", "message": child_error(
                "row_error_probe_failed", DETAIL=TEXT["row_error_probe_failed_exit"].format(N=128))},
             "inspection-incomplete"),
            ("a timeout", dict(name="timeout"), {"code": "probe-timeout", "message": child_error(
                "row_error_probe_timeout", S="5")}, "inspection-incomplete"),
            ("the work deadline", dict(name="deadline"), {"code": "deadline-exceeded", "message": child_error(
                "row_error_deadline_exceeded")}, "deadline-exceeded"),
        )
        remedies = {"inspection-incomplete": TEXT["remedy_inspection_incomplete"],
                    "deadline-exceeded": TEXT["remedy_deadline_exceeded"]}

        def assert_undecided(stand_ins, error, code, calls):
            refused = {"code": code, "message": TEXT["plan_incomplete"].format(CODE=code, REMEDY=remedies[code])}
            before = self.snapshot(root)
            for words, status in ((("--all-safe", "--json"), 1), (("--all-safe", "--apply", "--yes", "--json"), 2)):
                out_status, out, err = self.main_in_process("clean", root, *words, **stand_ins)
                self.assertEqual(out_status, status, out + err)
                document = json.loads(out)
                self.assertEqual((document["selected"], by_path(document)),
                                 ([], {str(root): "main-worktree", str(tree): "inspection-error"}))
                row = row_of(document, tree)
                self.assertEqual((row["classification"], row["recommendation"], row["errors"]),
                                 ("inspection-error", INSPECTION_ERROR_ADVICE, [error]))
                self.assertEqual((document["completeness"], document["apply_allowed"], document["refusals"]),
                                 ("incomplete", False, [refused]))
            self.assertEqual(len(calls), 2, "one read or child per run")
            self.assertEqual(self.snapshot(root), before, "nothing removed")

        for label, answer, error, code in reads:
            with self.subTest(f"the read of logs/HEAD meets {label}"):
                calls = []

                def fs_call(fn, *args, answer=answer, calls=calls, **options):
                    if fn is project._read_head and args[:1] == (log,):
                        calls.append(args)
                        if isinstance(answer, BaseException):
                            raise answer
                        return answer
                    return real_fs_call(fn, *args, **options)

                assert_undecided({"fs_call": fs_call}, error, code, calls)
        for label, fields, error, code in children:
            with self.subTest(f"the reachability child meets {label}"):
                calls = []

                def run_bounded(spec, parser, run, fields=fields, calls=calls):
                    kind, args, cwd = spec
                    if args[2:5] == self.REACHABILITY:
                        calls.append(args)
                        return project.DriverOutcome(project.git_argv(kind, args), **fields)
                    return real_run_bounded(spec, parser, run)

                assert_undecided({"run_bounded": run_bounded}, error, code, calls)

    def test_clean_worktree_only_commits_decided_by_the_read(self):
        # D21: a logs/HEAD read to its 64 KiB bound, or holding a line that
        # does not parse, decides `worktree-only-commits` with no child run; a
        # missing or empty logs/HEAD gives no candidate, and the child still
        # runs, for refs/worktree, and passes.
        root = self.repo()
        self.bare_remote()
        log_of = {}
        trees = {}
        for name in ("bound", "unparsable", "missing", "empty"):
            tree = self.merged_worktree(f"00{len(trees) + 1}-{name}", path=self.base / name)
            trees[name] = tree
            log_of[name] = self.common_dir(root) / "worktrees" / tree.name / "logs" / "HEAD"
        # Whole, parseable lines past 64 KiB: only the bound decides.
        head = self.git(trees["bound"], "rev-parse", "HEAD").strip()
        pad = f"{head} {head} T <t@e.invalid> 0 +0000\tpad\n".encode()
        size = log_of["bound"].stat().st_size
        log_of["bound"].write_bytes(log_of["bound"].read_bytes() + pad * ((64 * 1024 - size) // len(pad) + 1))
        self.assertGreater(log_of["bound"].stat().st_size, 64 * 1024)
        with log_of["unparsable"].open("ab") as stream:
            stream.write(b"not a reflog line\n")
        log_of["missing"].unlink()
        log_of["empty"].write_bytes(b"")
        result, records = self.run_counted("clean", root, "--all-safe", "--json")
        self.assert_status(result, 0)
        document = self.load_json(result)
        self.assertEqual(by_path(document), {str(root): "main-worktree", str(trees["bound"]): "worktree-only-commits",
                                             str(trees["unparsable"]): "worktree-only-commits"})
        self.assertEqual([entry["path"] for entry in document["selected"]],
                         [str(trees["empty"]), str(trees["missing"])])
        reached = dict(self.reachability(records))
        self.assertEqual(sorted(reached), sorted([str(trees["empty"]), str(trees["missing"])]),
                         "no child where the read decided")
        for name in ("empty", "missing"):
            words = reached[str(trees[name])]
            self.assertEqual(words[3], "--not", "no candidate before the negatives")


if __name__ == "__main__":
    unittest.main()
