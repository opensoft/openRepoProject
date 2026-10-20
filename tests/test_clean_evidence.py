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

    # T029: the evidence model's probes, registration, presence and row fields.

    def test_clean_evidence_probes_once_per_common_directory(self):
        # D6, FR-055, FR-056: rows 3, 4, 6 and 7 once each, row 4b only in a
        # gitfile layout, and one combined status probe per present, verified row,
        # inside that worktree; every child pinned (D11).
        root = self.repo()
        self.bare_remote()
        merged = self.merged_worktree("001-merged")
        unstarted = self.unstarted_worktree("002-unstarted")
        stale = self.add("stale", "-b", "003-stale")
        shutil.rmtree(stale)
        main_head = self.git(root, "rev-parse", "HEAD").strip()
        result, records = self.report(root)
        commands = [command(record) for record in records]
        self.assertEqual([c[1] for c in commands if c[2:] == ROW_3], [str(root)])
        self.assertEqual([c[1] for c in commands if c[2:] == ROW_4], [str(root)])
        self.assertEqual([c for c in commands if c[2:] == ROW_4B], [])
        self.assertEqual([c[1] for c in commands if c[2:] == ROW_6], [str(root)])
        merged_set = [c for c in commands if c[2:3] == ["for-each-ref"] and c[2:] != ROW_6]
        self.assertEqual(merged_set, [["-C", str(root), "for-each-ref", f"--merged={main_head}",
                                       "--format=%(refname)", "refs/heads"]])
        self.assertEqual(self.status_dirs(records), sorted(map(str, (root, merged, unstarted))),
                         "one status probe per present, verified row; none for the stale row")
        self.assertEqual([c[2:] for c in commands if c[2:3] == ["rev-parse"] and c[2:] != DISCOVER], [ROW_3])
        self.assertEqual([c for c in commands if c[2:3] and c[2] in REPLACED], [],
                         "no per-row rev-parse, rev-list, merge-base, show-ref or symbolic-ref")
        self.assert_pinned(records)
        rows = by_name(result.document)
        self.assertEqual(rows["001-merged-tree"]["classification"], "merged-removable")

        with self.subTest("a gitfile layout: row 4b, and the git directory is no row"):
            checkout = self.base / "checkout"
            gitdir = self.base / "checkout.git"
            self.git(self.base, "init", "-q", "-b", "main", "--separate-git-dir", gitdir, checkout)
            self.git(checkout, "commit", "-q", "--allow-empty", "-m", "initial")
            result, records = self.report(checkout)
            commands = [command(record) for record in records]
            for row in (ROW_3, ROW_4, ROW_4B, ROW_6):
                self.assertEqual([c[1] for c in commands if c[2:] == row], [str(checkout)], row)
            self.assertEqual(self.status_dirs(records), [str(checkout)])
            self.assertEqual([(row["path"], row["classification"]) for row in result.document["worktrees"]],
                             [(str(checkout), "protected-default")])
            self.assert_pinned(records)

        with self.subTest("a path holding a line feed: row 3 again, one option per child"):
            feed = self.repo("line\nfeed")
            result, records = self.report(feed)
            identity = [c[2:] for c in map(command, records)
                        if c[2:3] == ["rev-parse"] and c[2:] != DISCOVER]
            self.assertEqual(identity, [ROW_3] + [["rev-parse", "--path-format=absolute", option]
                                                  for option in ROW_3[2:]])
            self.assertEqual([(row["path"], row["classification"]) for row in result.document["worktrees"]],
                             [(str(feed), "protected-default")])

    def test_clean_evidence_checks_registration_both_ways(self):
        # D7, FR-055: `<path>/.git` names `<common_dir>/worktrees/<id>`, whose
        # `gitdir` file names `<path>/.git`; a row whose registration disagrees
        # gets no status probe and is inspection-error.
        root = self.repo()
        self.bare_remote()
        rewritten = self.merged_worktree("001-rewritten")
        other = self.merged_worktree("002-other")
        moved = self.merged_worktree("003-moved")
        common = self.common_dir()
        # A rewritten `.git` file: it names another worktree's admin directory,
        # whose `gitdir` file names that worktree, not this one.
        (rewritten / ".git").write_text(f"gitdir: {common / 'worktrees' / other.name}\n")
        # A changed admin `gitdir` file: the registry now names a directory with
        # no `.git` file of its own.
        elsewhere = self.base / "elsewhere"
        elsewhere.mkdir()
        (common / "worktrees" / moved.name / "gitdir").write_text(f"{elsewhere / '.git'}\n")
        result, records = self.report(root)
        rows = by_name(result.document)
        self.assertNotIn(moved.name, rows)
        for name in (rewritten.name, elsewhere.name):
            with self.subTest(row=name):
                row = rows[name]
                self.assertEqual((row["present"], row["dirty"], row["errors"], row["classification"]),
                                 (True, None, [], "inspection-error"))
                self.assertNotIn("prunable", row, "prunable only on a stale row (M11)")
        self.assertEqual(rows[other.name]["classification"], "merged-removable")
        self.assertEqual(self.status_dirs(records), sorted(map(str, (root, other))))

        with self.subTest("two registry entries naming one path (lead rulings R-57 L2 and L3, R-59 D5)"):
            # A copied admin directory: the registry then lists one path twice,
            # and the two-way check alone passes both entries.
            shared_root = self.repo("shared-repo")
            self.bare_remote(shared_root, "shared-remote.git")
            shared = self.merged_worktree("011-shared", root=shared_root)
            gone = self.merged_worktree("012-gone", root=shared_root)
            control = self.merged_worktree("013-control", root=shared_root)
            admin = self.common_dir(shared_root) / "worktrees"
            for tree in (shared, gone):
                shutil.copytree(admin / tree.name, admin / f"{tree.name}-copy")
            shutil.rmtree(gone)
            result, records = self.report(shared_root)
            listed = result.document["worktrees"]
            self.assertEqual([row["path"] for row in listed].count(str(shared)), 2)
            for row in (row for row in listed if row["path"] == str(shared)):
                self.assertEqual((row["present"], row["dirty"], row["errors"], row["classification"]),
                                 (True, None, [], "inspection-error"))
                self.assertNotIn("prunable", row)
            # L2 first: a path not present is stale, with no duplicate check.
            self.assertEqual([(row["present"], row["classification"], row.get("prunable"), row["errors"])
                              for row in listed if row["path"] == str(gone)],
                             [(False, "stale-worktree", True, [])] * 2)
            self.assertEqual(by_name(result.document)[control.name]["classification"], "merged-removable")
            self.assertEqual(self.status_dirs(records), sorted(map(str, (shared_root, control))),
                             "no status probe in the shared path")
            # In process: `registered` is false (gate 3), and the duplicate check
            # covers the whole registry when rows are built for one entry alone.
            with mock.patch.dict(os.environ, self.env, clear=True):
                run = project.Invocation()
                repo = project.inspect_repository(os.fsencode(shared_root), run)
                every = project.worktree_rows(repo, run)
                twins = [record for record in repo["records"] if record["path"] == os.fsencode(shared)]
                alone = project.worktree_rows(repo, run, records=twins[1:])
            self.assertEqual([(row.registered, row.admin_id) for row in every if row.raw_path == os.fsencode(shared)],
                             [(False, None)] * 2)
            self.assertEqual([row.registered for row in every if row.raw_path == os.fsencode(gone)], [None] * 2)
            self.assertEqual([(row.raw_path, row.registered, row["classification"]) for row in alone],
                             [(os.fsencode(shared), False, "inspection-error")])

    def test_clean_evidence_a_branch_named_head_takes_no_upstream(self):
        # Lead ruling R-61 (b): for refs/heads/HEAD, `git for-each-ref` prints
        # the upstream of the branch HEAD names where it runs (Git 2.43.0 credits
        # this branch with origin/main), so the row's upstream, remote_present,
        # ahead and behind are null, and it is inspection-error with one
        # probe-failed error, whatever Git prints. The branch is made by
        # update-ref and checked out by symbolic-ref in a worktree detached at
        # its commit, plumbing every Git of the floor job accepts.
        root = self.repo()
        self.bare_remote()
        merged = self.merged_worktree("001-merged")
        self.git(root, "push", "-u", "origin", "main")
        tip = self.git(root, "rev-parse", "HEAD").strip()
        self.git(root, "update-ref", "refs/heads/HEAD", tip)
        tree = self.add("head", "--detach")
        self.git(tree, "symbolic-ref", "HEAD", "refs/heads/HEAD")
        self.assertIn(b"\0branch refs/heads/HEAD\0",
                      os.fsencode(self.git(root, "worktree", "list", "--porcelain", "-z")))
        result, records = self.report(root)
        rows = by_name(result.document)
        error = {"code": "probe-failed", "message": git_message(
            "for-each-ref", "row_error_probe_failed", DETAIL=TEXT["row_error_probe_failed_unparseable"])}
        row = rows[tree.name]
        self.assertEqual([row[key] for key in ("branch", "upstream", "remote_present", "ahead", "behind", "errors",
                                               "classification", "recommendation")],
                         ["HEAD", None, None, None, None, [error], "inspection-error",
                          RECOMMENDATIONS["inspection-error"]])
        self.assertEqual((row["present"], row["dirty"], row["merged_into_target"]), (True, False, True),
                         "the status probe and row 7 still read it")
        self.assertIn(str(tree), self.status_dirs(records))
        self.assertEqual([(rows[name]["upstream"], rows[name]["errors"], rows[name]["classification"])
                          for name in ("repo", merged.name)],
                         [("origin/main", [], "protected-default"), ("origin/001-merged", [], "merged-removable")])

    def test_clean_evidence_reads_presence(self):
        # Lead ruling R-36, FR-055: an lstat failing with ENOENT, or with ENOTDIR
        # where the parent of a registered path became a regular file, is
        # `present: false`.
        root = self.repo()
        missing = self.add("missing", "-b", "001-missing")
        shutil.rmtree(missing)
        parent = self.base / "parent"
        parent.mkdir()
        self.git(root, "worktree", "add", "-b", "002-parent", parent / "tree")
        shutil.rmtree(parent)
        parent.write_text("now a regular file")
        with self.assertRaises(NotADirectoryError):
            os.lstat(parent / "tree")
        result, records = self.report(root)
        rows = {row["path"]: row for row in result.document["worktrees"]}
        for path in (missing, parent / "tree"):
            with self.subTest(path=path.name):
                row = rows[str(path)]
                self.assertEqual((row["present"], row["classification"], row.get("prunable"), row["errors"]),
                                 (False, "stale-worktree", True, []))
                self.assertEqual([row[key] for key in ("dirty", "ignored_files", "current", "upstream")],
                                 [None] * 4)
        self.assertEqual(self.status_dirs(records), [str(root)])

    @clean_support.not_root
    def test_clean_evidence_reads_presence_without_search_permission(self):
        # R-36: any other lstat failure is `present: null`, an os-error and
        # inspection-error, with no probe.
        root = self.repo()
        locked = self.base / "locked"
        locked.mkdir()
        tree = locked / "tree"
        self.git(root, "worktree", "add", "-b", "001-locked", tree)
        locked.chmod(0o600)
        self.addCleanup(locked.chmod, 0o700)
        result, records = self.report(root)
        row = {row["path"]: row for row in result.document["worktrees"]}[str(tree)]
        message = TEXT["row_error_os_error"].format(OPERATION="lstat", STRERROR=os.strerror(errno.EACCES))
        self.assertEqual((row["present"], row["errors"], row["classification"], row["dirty"]),
                         (None, [{"code": "os-error", "message": message}], "inspection-error", None))
        self.assertNotIn("prunable", row, "Git calls it prunable, but the row is not stale (M11)")
        self.assertEqual(self.status_dirs(records), [str(root)])

    def test_clean_evidence_row_fields(self):
        # Plan review M6 and m11; FR-042, FR-043, FR-056: the six added fields
        # on every row, row errors as objects, and a deleted upstream.
        root = self.repo()
        self.bare_remote()
        ignored = self.merged_worktree(
            "001-ignored", setup=lambda tree: (tree / ".gitignore").write_text("local.env\n"))
        (ignored / "local.env").write_text("preserve")
        gone = self.add("gone", "-b", "002-gone")
        (gone / "gone").write_text("gone")
        self.commit(gone)
        self.git(gone, "push", "-u", "origin", "002-gone")
        self.git(gone, "push", "origin", "--delete", "002-gone")
        self.add("locked", "--lock", "-b", "003-locked")
        failing = self.add("failing", "-b", "004-failing")
        fake = clean_support.install_fake_git(self.base / "fake", "status-fails-in", path=failing)
        stale = self.add("stale", "-b", "005-stale")
        shutil.rmtree(stale)
        result, records = self.report(root, real=fake)
        rows = by_name(result.document)
        for name, row in rows.items():
            with self.subTest(row=name):
                keys = ROW_KEYS[:14] + (["prunable"] if name == "stale-tree" else []) + ROW_KEYS[14:]
                self.assertEqual(list(row), keys)
                self.assertIs(row["locked"], name == "locked-tree")
                self.assertIs(row["path_valid_utf8"], True)
                self.assertEqual(row["notes"], [])
                for error in row["errors"]:
                    self.assertEqual(list(error), ["code", "message"])
        self.assertEqual([rows["001-ignored-tree"][key] for key in
                          ("ignored_files", "ignored_files_truncated", "ignored_samples", "classification")],
                         [1, False, [{"path": "local.env", "path_valid_utf8": True}], "ignored-local-files"])
        self.assertEqual([rows["gone-tree"][key] for key in
                          ("upstream", "remote_present", "ahead", "behind", "classification")],
                         ["origin/002-gone", False, None, None, "remote-gone"])
        message = git_message("status", "row_error_probe_failed",
                              DETAIL=TEXT["row_error_probe_failed_exit"].format(N=128))
        self.assertEqual([rows["failing-tree"][key] for key in
                          ("errors", "dirty", "ignored_files", "ignored_files_truncated", "ignored_samples",
                           "classification")],
                         [[{"code": "probe-failed", "message": message}], None, None, None, None,
                          "inspection-error"])
        self.assertEqual([rows["stale-tree"][key] for key in
                          ("ignored_files_truncated", "ignored_samples", "errors")], [None, None, []])
        self.assertEqual(rows["repo"]["ignored_samples"], [])

    def test_clean_evidence_rows_for_chosen_records_in_the_given_order(self):
        # Lead ruling R-53 (d): worktree_rows(repo, run, records) builds rows
        # only for the registry records given, in the order given, the first
        # registry entry staying the main worktree; None means the whole
        # registry. In process, in the fixture's environment.
        root = self.repo()
        self.bare_remote()
        merged = self.merged_worktree("001-merged")
        second = self.add("second", "-b", "002-second")
        third = self.add("third", "-b", "003-third")
        with mock.patch.dict(os.environ, self.env, clear=True):
            run = project.Invocation()
            repo = project.inspect_repository(os.fsencode(root), run)
            registry = repo["records"]
            record = {entry["path"]: entry for entry in registry}
            every = project.worktree_rows(repo, run)
            order = [os.fsencode(path) for path in (third, root, merged)]
            with mock.patch.object(project, "run_bounded", wraps=project.run_bounded) as spy:
                chosen = project.worktree_rows(repo, run, records=[record[path] for path in order])
            self.assertEqual(project.worktree_rows(repo, run, records=None), every)
            self.assertEqual(project.worktree_rows(repo, run, records=list(registry)), every)
            self.assertEqual(project.worktree_rows(repo, run, records=[]), [])
            copy_of_first = project.worktree_rows(repo, run, records=[dict(record[os.fsencode(root)])])
            with self.assertRaises(ValueError):
                project.worktree_rows(repo, run, records=[dict(registry[1], path=b"/not/registered")])
        self.assertEqual([row.raw_path for row in every],
                         [os.fsencode(path) for path in (root, merged, second, third)])
        self.assertEqual([row.raw_path for row in chosen], order)
        self.assertEqual([row.main for row in chosen], [False, True, False])
        self.assertEqual([row["classification"] for row in chosen],
                         ["unpublished", "protected-default", "merged-removable"])
        rows = {row.raw_path: row for row in every}
        for row in chosen:
            with self.subTest(row=row["path"]):
                self.assertEqual(row, rows[row.raw_path])
                self.assertEqual([getattr(row, name) for name in ("registered", "admin_id", "dev", "ino")],
                                 [getattr(rows[row.raw_path], name) for name in ("registered", "admin_id", "dev",
                                                                                 "ino")])
        self.assertEqual([call.args[0][0] for call in spy.call_args_list], ["status"] * 3,
                         "one status probe per chosen row and no repository-wide child")
        self.assertEqual([os.fsencode(call.args[0][1][1]) for call in spy.call_args_list], order)
        self.assertEqual([(row.main, row["classification"]) for row in copy_of_first],
                         [(True, "protected-default")])

    # T030: the evidence model's scenarios (rule 1: test_status_, plan review M14).

    def test_status_a_git_that_floods_standard_error(self):
        root = self.repo()
        fake_dir = self.base / "fake"
        fake = clean_support.install_fake_git(fake_dir, "flood-stderr", kib=70)
        result, records = self.report(root, real=fake)
        row = by_name(result.document)["repo"]
        self.assertEqual((row["errors"], row["dirty"], row["classification"]), ([], False, "protected-default"))
        self.assertEqual(self.status_dirs(records), [str(root)])
        self.assertNotIn("EEEE", result.stderr, "the child's standard error is read, never passed on")
        # The standard error kept is capped at 4 KiB, and every byte counted.
        with mock.patch.dict(os.environ, self.path_first(fake_dir), clear=True):
            outcome, error = project.status_probe(os.fsencode(root), project.Invocation())
        self.assertIsNone(error)
        self.assertEqual((outcome.name, len(outcome.stderr), outcome.stderr_bytes),
                         ("complete", 4096, 70 * 1024))
        self.assertIs(outcome.result["dirty"], False)

    def test_status_a_git_that_ignores_sigterm(self):
        # Launcher, its own table (R-29): a probe budget of 1 s, a grace of 0.5 s
        # and a reap wait of 0.5 s; every other value real.
        table = clean_support.timing_table(probe_budget=1.0, term_grace=0.5, reap_wait=0.5)
        root = self.repo()
        fake_dir = self.base / "fake"
        fake = clean_support.install_fake_git(fake_dir, "ignore-sigterm")
        result, records = self.report(root, real=fake, timing=table)
        row = by_name(result.document)["repo"]
        self.assertEqual(row["errors"], [{"code": "probe-timeout",
                                          "message": git_message("status", "row_error_probe_timeout", S="1")}])
        self.assertEqual((row["dirty"], row["classification"]), (None, "inspection-error"))
        ready = clean_support.wait_for_event(fake_dir, "ready")
        self.assertIsNotNone(ready, "the fake status probe started")
        term = clean_support.wait_for_event(fake_dir, "term", pid=ready["pid"])
        death = clean_support.wait_for_event(fake_dir, "death", pid=ready["pid"])
        self.assertIsNotNone(term)
        self.assertIsNotNone(death)
        self.assertGreaterEqual(death["t"] - term["t"], 0.9 * table["term_grace"],
                                "SIGKILL came at least 0.9 of the grace after SIGTERM, measured from the child")
        with self.assertRaises(ProcessLookupError):
            os.killpg(ready["pgid"], 0)

    def test_status_five_thousand_ignored_records(self):
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-merged")
        fake = clean_support.install_fake_git(self.base / "fake", "ignored-5000")
        result, records = self.report(root, real=fake)
        rows = by_name(result.document)
        samples = [{"path": f"ignored-{number:05d}", "path_valid_utf8": True} for number in range(8)]
        for name, classification in (("repo", "protected-default"), (tree.name, "ignored-local-files")):
            with self.subTest(row=name):
                row = rows[name]
                self.assertEqual([row[key] for key in ("ignored_files", "ignored_files_truncated",
                                                       "ignored_samples", "dirty", "errors", "classification")],
                                 [64, True, samples, False, [], classification])
        self.assertEqual(self.status_dirs(records), sorted(map(str, (root, tree))))

    def test_status_user_status_configuration(self):
        config = self.base / "user.gitconfig"
        config.write_text("[status]\n\tshowUntrackedFiles = no\n")
        root = self.repo()
        self.bare_remote()
        merged = self.merged_worktree("001-merged")
        untracked = self.merged_worktree("002-untracked")
        (untracked / "new").write_text("untracked")
        result, records = self.report(root, env=dict(self.env, GIT_CONFIG_GLOBAL=str(config)))
        rows = by_name(result.document)
        self.assertEqual([(rows[tree.name]["classification"], rows[tree.name]["errors"])
                          for tree in (merged, untracked)],
                         [("merged-removable", []), ("dirty", [])])
        self.assertEqual(self.status_dirs(records), sorted(map(str, (root, merged, untracked))))

    def test_status_a_caller_s_git_environment_is_ignored(self):
        root = self.repo()
        self.bare_remote()
        merged = self.merged_worktree("001-merged")
        dirty = self.add("dirty", "-b", "002-dirty")
        (dirty / "uncommitted").write_text("preserve")
        other = self.repo("other")
        (other / "other").write_text("other")
        self.commit(other)
        (other / "untracked").write_text("other")
        plain, _ = self.report(root)
        steering = {"GIT_DIR": str(other / ".git"), "GIT_WORK_TREE": str(other),
                    "GIT_INDEX_FILE": str(other / ".git" / "index")}
        steered, records = self.report(root, env=dict(self.env, **steering))
        self.assertEqual(steered.document, plain.document)
        self.assertEqual([by_name(steered.document)[name]["classification"]
                          for name in ("repo", merged.name, dirty.name)],
                         ["protected-default", "merged-removable", "dirty"])
        self.assertEqual(self.status_dirs(records), sorted(map(str, (root, merged, dirty))))
        self.assert_pinned(records)

    @clean_support.git_236_to_239
    def test_status_the_sixteenth_scrubbed_name_on_git_2_36(self):
        root = self.repo()
        self.bare_remote()
        merged = self.merged_worktree("001-merged")
        result, records = self.report(root, env=dict(self.env, GIT_INTERNAL_SUPER_PREFIX="sub/"))
        rows = by_name(result.document)
        self.assertEqual([rows[name]["classification"] for name in ("repo", merged.name)],
                         ["protected-default", "merged-removable"])
        self.assert_pinned(records)

    def test_status_a_lazy_fetch_in_a_partial_clone_is_refused_locally(self):
        source = self.repo("source")
        (source / "tracked").write_text("needs a tree object")
        self.commit(source)
        self.git(source, "config", "uploadpack.allowFilter", "true")
        clone = self.base / "clone"
        self.git(self.base, "clone", "-q", "--no-checkout", "--filter=tree:0", f"file://{source}", clone)
        ran = self.base / "uploadpack.log"
        script = self.base / "uploadpack.sh"
        script.write_text(f"#!/bin/sh\necho ran >> '{ran}'\nexec '{clean_support.REAL_GIT}' upload-pack \"$@\"\n")
        script.chmod(0o755)
        self.git(clone, "config", "remote.origin.uploadpack", script)
        message = git_message("status", "row_error_probe_failed",
                              DETAIL=TEXT["row_error_probe_failed_exit"].format(N=128))
        for label, env in (("pinned", self.env), ("allowed by the caller and the clone",
                                                  dict(self.env, GIT_ALLOW_PROTOCOL="file"))):
            with self.subTest(label):
                if env is not self.env:
                    self.git(clone, "config", "protocol.file.allow", "always")
                result, records = self.report(clone, env=env)
                row = by_name(result.document)["clone"]
                self.assertEqual((row["errors"], row["dirty"], row["classification"]),
                                 ([{"code": "probe-failed", "message": message}], None, "inspection-error"))
                self.assertEqual(self.status_dirs(records), [str(clone)])
                self.assert_pinned(records)
                self.assertFalse(ran.exists(), "the upload-pack script never ran")


if __name__ == "__main__":
    unittest.main()
