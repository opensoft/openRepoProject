"""Lane G of feature 004: the evidence model behind cleanup_report() (T027 to
T033; design D4, D6, D7 and D8; research.md R9; data-model.md, "Repository
identity", "Merge target", "Worktree row", "Worktree identity and
registration", "Branch evidence" and "Classification").

Parity values are literals written into the test (rule 11, research.md R9):
once cleanup_report() reads the evidence model no baseline function remains to
compare against.
"""
import copy
import errno
import json
import os
from pathlib import Path
import shutil
import unittest
from unittest import mock

import clean_support

project = clean_support.load_project()
TEXT = clean_support.TEXT_FIXTURES

# The seven protocol pins and the two status pins, as the contract writes them
# (contracts/project-clean.md, "Git children").
PINS = ["-c", "protocol.allow=never", "-c", "protocol.file.allow=never",
        "-c", "protocol.ssh.allow=never", "-c", "protocol.git.allow=never",
        "-c", "protocol.http.allow=never", "-c", "protocol.https.allow=never",
        "-c", "protocol.ext.allow=never"]
STATUS_PINS = ["-c", "core.untrackedCache=false", "-c", "core.fsmonitor=false"]

# The children of design D6's table, after `-C DIR` (contracts/project-clean.md).
ROW_3 = ["rev-parse", "--path-format=absolute", "--show-toplevel", "--git-common-dir",
         "--show-superproject-working-tree"]
ROW_4 = ["worktree", "list", "--porcelain", "-z"]
ROW_4B = ["config", "--get", "core.worktree"]
ROW_6 = ["for-each-ref", "--format=%(refname)%00%(objectname)%00%(symref)%00%(upstream)"
         "%00%(upstream:short)%00%(upstream:track,nobracket)", "refs/heads", "refs/remotes"]
STATUS = ["status", "--porcelain=v1", "-z", "--untracked-files=normal", "--ignored=matching"]
# discover()'s one child for a path argument, until T107 resolves Git-first.
DISCOVER = ["rev-parse", "--show-toplevel"]
# The baseline's per-row children, which the evidence model replaces (D6).
REPLACED = ("rev-list", "merge-base", "show-ref", "symbolic-ref")

# A worktree row's keys in order (data-model.md, "Worktree row"); `prunable`
# comes after `recommendation`, only on a stale row whose record says so.
ROW_KEYS = ["path", "present", "branch", "head", "upstream", "remote_present", "ahead", "behind",
            "dirty", "ignored_files", "current", "merged_into_target", "classification",
            "recommendation", "locked", "ignored_files_truncated", "ignored_samples",
            "path_valid_utf8", "errors", "notes"]


def split_pins(record):
    """A counted child's argument vector as (its -c pins, the rest from -C on)."""
    argv = record.argv
    at = 0
    while at + 1 < len(argv) and argv[at] == "-c":
        at += 2
    return argv[:at], argv[at:]


def command(record):
    return split_pins(record)[1]


def by_name(report):
    """A report's rows by the last part of their path."""
    return {Path(row["path"]).name: row for row in report["worktrees"]}


def git_message(subcommand, code, **fields):
    """A row error's message for `git SUBCOMMAND`, from the fixtures (rule 8)."""
    operation = TEXT["row_error_git_operation"].format(SUBCOMMAND=subcommand)
    return TEXT[code].format(OPERATION=operation, **fields)

# The ladder's fifteen classes, in its order (FR-007), and the recommendation of
# each, verbatim from cleanup_report() at 961c405 (project:566-616); two
# classes have a second rung with a second text (:580 and :613).
CLASSES = ("stale-worktree", "protected-default", "inspection-error", "dirty",
           "ignored-local-files", "detached", "unpublished", "remote-gone", "review-required",
           "diverged", "remote-ahead", "unpushed", "merged-removable", "merged-current",
           "pushed-unmerged")
RECOMMENDATIONS = {
    "stale-worktree": "Review and prune stale worktree metadata manually.",
    "protected-default": "Keep the default branch; use the repository's normal push or PR process.",
    "inspection-error": "Preserve this worktree; Git could not establish its clean state.",
    "dirty": "Preserve or commit the working changes before cleanup.",
    "ignored-local-files": "Preserve or relocate ignored local files before cleanup.",
    "detached": "Preserve the detached commit or attach it to a named branch before cleanup.",
    "unpublished": "Push or otherwise preserve the branch before removing its worktree.",
    "remote-gone": "Confirm the branch should be republished before removing local work.",
    "review-required": "Remote tracking state could not be established from local refs; preserve it for review.",
    "diverged": "Reconcile the diverged branch through the normal Git workflow before cleanup.",
    "remote-ahead": "Fetch and reconcile the newer remote branch before cleanup.",
    "unpushed": "Use an explicit clean push, then continue through the normal review process.",
    "merged-removable": "This clean, merged, non-current worktree may be removed explicitly.",
    "merged-current": "The branch is merged, but this is the current checkout; switch away before removal.",
    "pushed-unmerged": "Continue through the repository's normal pull-request or merge process.",
}
IGNORED_STATE = "Preserve this worktree; Git could not establish its ignored-file state."
MERGE_STATE = "Merge state could not be established from local refs; preserve it for review."

# A clean, pushed, unmerged row of branch `f`: the ladder's last rung.
BASE_ROW = {
    "path": "/w/f", "present": True, "branch": "f", "head": "a" * 40, "upstream": "origin/f",
    "remote_present": True, "ahead": 0, "behind": 0, "dirty": False, "ignored_files": 0,
    "current": False, "merged_into_target": False, "errors": [],
}

# The fields T027 compares per row, in this order (research.md R9).
PARITY_FIELDS = ("classification", "dirty", "upstream", "ahead", "behind",
                 "merged_into_target", "remote_present", "current")

# Per row, named by its directory: the literal values of PARITY_FIELDS. A key
# the baseline reader leaves out of a row reads as None, as for the stale row.
PARITY = {
    "repo": ("protected-default", False, None, None, None, True, None, False),
    "unpublished-tree": ("unpublished", False, None, None, None, True, None, False),
    "pushed-tree": ("pushed-unmerged", False, "origin/002-pushed", 0, 0, False, True, False),
    "unpushed-tree": ("unpushed", False, "origin/003-unpushed", 1, 0, False, True, False),
    "behind-tree": ("remote-ahead", False, "origin/004-behind", 0, 1, False, True, False),
    "diverged-tree": ("diverged", False, "origin/005-diverged", 1, 1, False, True, False),
    "dirty-tree": ("dirty", True, None, None, None, True, None, False),
    "007-ignored-tree": ("ignored-local-files", False, "origin/007-ignored", 0, 0, True, True, False),
    "detached-tree": ("detached", False, None, None, None, None, None, False),
    "stale-tree": ("stale-worktree", None, None, None, None, None, None, None),
    "010-merged-tree": ("merged-removable", False, "origin/010-merged", 0, 0, True, True, False),
    "011-current-tree": ("merged-current", False, "origin/011-current", 0, 0, True, True, True),
}

# The baseline keys of a worktree row and the exact types each may hold.
NONE = type(None)
BASELINE_TYPES = {
    "path": (str,), "present": (bool, NONE), "branch": (str,), "head": (str,),
    "upstream": (str, NONE), "remote_present": (bool, NONE), "ahead": (int, NONE),
    "behind": (int, NONE), "dirty": (bool, NONE), "ignored_files": (int, NONE),
    "current": (bool, NONE), "merged_into_target": (bool, NONE), "classification": (str,),
    "recommendation": (str,), "prunable": (bool,),
}
# The baseline keys every row carries, the stale row's included.
ALWAYS = ("path", "present", "branch", "head", "merged_into_target", "remote_present",
          "classification", "recommendation")


class EvidenceTests(clean_support.CleanCase):

    def counted(self, *args, real=None, env=None, cwd=None, timing=None):
        """`project ARGS...` with the counting wrapper first on PATH, in front of
        real (REAL_GIT, or a fake), through the launcher when timing is given.
        Returns the run, its parsed document as `document` when it printed one,
        and the counted children."""
        bin_dir = self.base / "counting-bin"
        log = self.base / "children.log"
        clean_support.install_counting_git(bin_dir, log, real=real or clean_support.REAL_GIT)
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
        return result, clean_support.child_log(log)

    def report(self, *args, **options):
        """counted() for `clean ARGS... --json`, which must exit 0 with one document."""
        result, records = self.counted("clean", *args, "--json", **options)
        self.assert_status(result, 0)
        self.assertIsNotNone(result.document, clean_support.transcript(result))
        return result, records

    def assert_pinned(self, records):
        """Every child carries the seven protocol pins, a status child the two
        status pins before them, and every one GIT_OPTIONAL_LOCKS=0 (D11, FR-054)."""
        for record in records:
            pins, rest = split_pins(record)
            with self.subTest(child=rest[:4]):
                self.assertEqual(pins, STATUS_PINS + PINS if rest[2:3] == ["status"] else PINS)
                self.assertEqual(record.optional_locks, "0")
                self.assertEqual(record.names, ("GIT_OPTIONAL_LOCKS",), "only the probes' own name is set")

    def status_dirs(self, records):
        return sorted(command(record)[1] for record in records if command(record)[2:] == STATUS)

    def add(self, name, *options):
        """`worktree add OPTIONS PATH` from the root, PATH self.base/NAME-tree."""
        tree = self.base / f"{name}-tree"
        self.git(self.root, "worktree", "add", *options, tree)
        return tree

    def remote_tracking(self, tree, branch, parent):
        """A commit made only on refs/remotes/origin/BRANCH, a child of parent, as
        if the remote had moved on and been fetched."""
        commit = self.git(tree, "commit-tree", f"{parent}^{{tree}}", "-p", parent, "-m", "remote").strip()
        self.git(tree, "update-ref", f"refs/remotes/origin/{branch}", commit)

    def test_clean_evidence_parity_with_the_baseline_reader(self):
        # R9, FR-061: one fixture per class the baseline reader reaches; the
        # literal values pass on the baseline reader and on the evidence model.
        root = self.repo()
        self.bare_remote()
        self.add("unpublished", "-b", "001-unpublished")
        pushed = self.add("pushed", "-b", "002-pushed")
        (pushed / "pushed").write_text("pushed")
        self.commit(pushed)
        self.git(pushed, "push", "-u", "origin", "002-pushed")
        unpushed = self.add("unpushed", "-b", "003-unpushed")
        self.git(unpushed, "push", "-u", "origin", "003-unpushed")
        (unpushed / "unpushed").write_text("unpushed")
        self.commit(unpushed)
        behind = self.add("behind", "-b", "004-behind")
        (behind / "behind").write_text("behind")
        head = self.commit(behind)
        self.git(behind, "push", "-u", "origin", "004-behind")
        self.remote_tracking(behind, "004-behind", head)
        diverged = self.add("diverged", "-b", "005-diverged")
        (diverged / "diverged").write_text("diverged")
        head = self.commit(diverged)
        self.git(diverged, "push", "-u", "origin", "005-diverged")
        (diverged / "local").write_text("local")
        self.commit(diverged)
        self.remote_tracking(diverged, "005-diverged", head)
        dirty = self.add("dirty", "-b", "006-dirty")
        (dirty / "uncommitted").write_text("preserve")
        ignored = self.merged_worktree(
            "007-ignored", setup=lambda tree: (tree / ".gitignore").write_text("local.env\n"))
        (ignored / "local.env").write_text("preserve")
        self.add("detached", "--detach")
        stale = self.add("stale", "-b", "009-stale")
        shutil.rmtree(stale)
        self.merged_worktree("010-merged")
        current = self.merged_worktree("011-current")

        result = self.run_cli("clean", root, "--json", cwd=current)
        self.assert_status(result, 0)
        report = self.load_json(result)
        self.assertEqual((report["root"], report["target_branch"]), (str(root), "main"))
        rows = {Path(row["path"]).name: row for row in report["worktrees"]}
        self.assertEqual(sorted(rows), sorted(PARITY))
        for name, expected in PARITY.items():
            row = rows[name]
            with self.subTest(row=name):
                actual = tuple(row.get(field) for field in PARITY_FIELDS)
                self.assertEqual(actual, expected)
                self.assertEqual([type(value) for value in actual], [type(value) for value in expected])
                for key in ALWAYS:
                    self.assertIn(key, row)
                for key, types in BASELINE_TYPES.items():
                    if key in row:
                        self.assertIn(type(row[key]), types, key)
                # Plan review M11: prunable only on the stale row, where the record says so.
                if name == "stale-tree":
                    self.assertIs(row.get("prunable"), True)
                else:
                    self.assertNotIn("prunable", row)
        self.assertEqual(rows["detached-tree"]["branch"], "detached")
        self.assertEqual(rows["stale-tree"]["present"], False)
        self.assertEqual(rows["011-current-tree"]["path"], os.fspath(current))

    def test_clean_ladder_is_a_pure_function(self):
        # FR-007, D6, OQ-28: classify(row, merge_target) on literal rows, with no
        # Git child and no filesystem call.
        unestablished = "an unestablished row, whatever its branch (D-A)"
        cases = [
            ("stale", {"present": False}, "stale-worktree", None),
            ("the merge target's checkout", {"branch": "main"}, "protected-default", None),
            (unestablished, {"branch": "main", "present": None}, "inspection-error", None),
            (unestablished, {"branch": "main", "dirty": None}, "inspection-error", None),
            (unestablished, {"branch": "main", "errors": [{"code": "probe-timeout", "message": "m"}]},
             "inspection-error", None),
            ("dirty", {"dirty": True}, "dirty", None),
            ("ignored files", {"ignored_files": 3}, "ignored-local-files", None),
            ("ignored state unknown", {"ignored_files": None}, "inspection-error", IGNORED_STATE),
            ("detached", {"branch": "detached", "upstream": None, "remote_present": None,
                          "ahead": None, "behind": None, "merged_into_target": None}, "detached", None),
            ("no upstream", {"upstream": None, "remote_present": None, "ahead": None, "behind": None},
             "unpublished", None),
            ("upstream deleted, unmerged", {"remote_present": False, "ahead": None, "behind": None},
             "remote-gone", None),
            ("upstream deleted, merge unknown", {"remote_present": False, "ahead": None, "behind": None,
                                                 "merged_into_target": None}, "remote-gone", None),
            # The one reorder (Brett Heap, open question 1): ancestry before remote-gone.
            ("upstream deleted, merged", {"remote_present": False, "ahead": None, "behind": None,
                                          "merged_into_target": True}, "merged-removable", None),
            ("upstream deleted, merged, current", {"remote_present": False, "ahead": None, "behind": None,
                                                   "merged_into_target": True, "current": True},
             "merged-current", None),
            # review-required comes only from rows the evidence model never builds:
            # an upstream that exists with no counts, or a branch with no merge answer.
            ("counts unknown", {"ahead": None}, "review-required", None),
            ("merge unknown", {"merged_into_target": None}, "review-required", MERGE_STATE),
            ("diverged", {"ahead": 1, "behind": 2}, "diverged", None),
            ("behind", {"behind": 2}, "remote-ahead", None),
            ("ahead", {"ahead": 3}, "unpushed", None),
            ("merged", {"merged_into_target": True}, "merged-removable", None),
            ("merged, current", {"merged_into_target": True, "current": True}, "merged-current", None),
            ("pushed, unmerged", {}, "pushed-unmerged", None),
        ]
        reached = set()
        with mock.patch.object(project, "run_bounded", side_effect=AssertionError("a Git child ran")), \
                mock.patch.object(project, "fs_call", side_effect=AssertionError("a filesystem call ran")):
            for label, change, expected, text in cases:
                with self.subTest(label, change=change):
                    row = {**BASE_ROW, **change}
                    before = copy.deepcopy(row)
                    result = project.classify(row, "main")
                    self.assertEqual(result, (expected, text or RECOMMENDATIONS[expected]))
                    self.assertEqual(project.classify(row, "main"), result, "the same row, the same answer")
                    self.assertEqual(row, before, "classify() changes nothing")
                    reached.add(expected)
        self.assertEqual(sorted(reached), sorted(CLASSES))
        self.assertEqual(project.RECOMMENDATIONS, RECOMMENDATIONS)

    def test_clean_partial_removal_note_rules(self):
        # D4, FR-009: after the ladder and apart from it, judged on the records read.
        def status(stream):
            parser = project.StatusParser()
            parser.feed(stream)
            return parser.finish()

        dirty = {**BASE_ROW, "dirty": True}
        deletions = status(b" D a\0 D sub/b\0")
        note = ["partially-removed"]
        self.assertEqual(project.partial_removal_note(dirty, deletions, False), note)
        self.assertEqual(project.partial_removal_note(dirty, status(b" D a\0!! kept.env\0"), False), note,
                         "ignored records leave the flag alone")
        self.assertEqual(project.partial_removal_note(dirty, status(b" D a\0?? new\0"), False), [],
                         "one deletion and one untracked file")
        self.assertEqual(project.partial_removal_note(dirty, status(b" D a\0 M b\0"), False), [])
        self.assertEqual(project.partial_removal_note(dirty, status(b"D  a\0"), False), [],
                         "a deletion staged in the index is not one in the working tree")
        self.assertEqual(project.partial_removal_note(dirty, deletions, True), [], "never the main worktree")
        self.assertEqual(project.partial_removal_note(dirty, None, False), [],
                         "no status result: absent, unverified or failed")
        for change in ({"present": False}, {"present": None}, {"dirty": False}, {"dirty": None}):
            with self.subTest(change=change):
                self.assertEqual(project.partial_removal_note({**dirty, **change}, deletions, False), [])
        # A stream stopped at its bound: the 4,097th record is never read.
        bounded = status(b" D x\0" * 4096 + b"?? late\0")
        self.assertEqual((bounded["records"], bounded["ignored_files_truncated"]), (4096, True))
        self.assertEqual(project.partial_removal_note(dirty, bounded, False), note)

        # The same rules on a report: tracked files deleted by hand (D4's second test).
        root = self.repo()
        self.bare_remote()
        gone = self.merged_worktree("001-gone")
        mixed = self.merged_worktree("002-mixed")
        for tree in (gone, mixed):
            for path in tree.iterdir():
                if path.name != ".git":
                    path.unlink()
        (mixed / "untracked").write_text("new")
        for path in root.iterdir():
            if path.name != ".git":
                path.unlink()
        result = self.run_cli("clean", root, "--json")
        self.assert_status(result, 0)
        rows = {Path(row["path"]).name: row for row in self.load_json(result)["worktrees"]}
        self.assertEqual([(rows[name]["classification"], rows[name]["notes"])
                          for name in ("repo", "001-gone-tree", "002-mixed-tree")],
                         [("protected-default", []), ("dirty", note), ("dirty", [])])


if __name__ == "__main__":
    unittest.main()
