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


if __name__ == "__main__":
    unittest.main()
