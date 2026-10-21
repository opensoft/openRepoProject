"""Lane G of feature 004: the evidence model behind cleanup_report() (T027 to
T033; design D4, D6, D7 and D8; research.md R9; data-model.md, "Repository
identity", "Merge target", "Worktree row", "Worktree identity and
registration", "Branch evidence" and "Classification").

Parity values are literals written into the test (rule 11, research.md R9):
once cleanup_report() reads the evidence model no baseline function remains to
compare against.
"""
import contextlib
import copy
import errno
import json
import os
from pathlib import Path
import shlex
import shutil
import unittest
from unittest import mock

import clean_support

project = clean_support.load_project()
TEXT = clean_support.TEXT_FIXTURES

# The seven protocol pins and the four status pins, as the contract writes them
# (contracts/project-clean.md, "Git children").
PINS = ["-c", "protocol.allow=never", "-c", "protocol.file.allow=never",
        "-c", "protocol.ssh.allow=never", "-c", "protocol.git.allow=never",
        "-c", "protocol.http.allow=never", "-c", "protocol.https.allow=never",
        "-c", "protocol.ext.allow=never"]
STATUS_PINS = ["-c", "core.untrackedCache=false", "-c", "core.fsmonitor=false",
               "-c", "core.trustctime=true", "-c", "core.checkStat=default"]

# The children of design D6's table, after `-C DIR` (contracts/project-clean.md).
ROW_3 = ["rev-parse", "--path-format=absolute", "--show-toplevel", "--git-common-dir",
         "--show-superproject-working-tree"]
ROW_4 = ["worktree", "list", "--porcelain", "-z"]
ROW_4B = ["config", "--get", "core.worktree"]


def row_4c(common):
    """Row 4c after `-C DIR` (design D6; Brett Heap's ruling LQ-11): the
    extension read from the common directory's own `config` file."""
    return ["config", "--file", os.path.join(str(common), "config"), "--type=bool", "--get",
            "extensions.worktreeConfig"]


# A linked worktree's effective-work-tree probe after `-C WORKTREE` (D7, LQ-11).
WORK_TREE_PROBE = ["rev-parse", "--path-format=absolute", "--show-toplevel"]
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
        """counted() for `clean ARGS... --json`, which prints one document and exits by
        its completeness: 0 when complete, 1 otherwise (R-88; pcl:40-43)."""
        result, records = self.counted("clean", *args, "--json", **options)
        self.assert_status(result, 0 if (result.document or {}).get("completeness") == "complete" else 1)
        self.assertIsNotNone(result.document, clean_support.transcript(result))
        return result, records

    def assert_pinned(self, records):
        """Every child carries the seven protocol pins, a status child the two
        status pins before them, and every one GIT_OPTIONAL_LOCKS=0 (D11, FR-054)."""
        for record in records:
            pins, rest = split_pins(record)
            with self.subTest(child=rest[:4]):
                self.assertEqual(pins, STATUS_PINS + PINS if rest[2:3] in (["status"], ["ls-files"]) else PINS)
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
        self.assertIs(rows["stale-tree"]["present"], False)
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
        # The one rev-list is gate 12's reachability probe (D21, LQ-13), which a
        # report runs as any plan does, in the one row that reaches it.
        reachability = [c for c in commands if c[2:5] == ["rev-list", "--max-count=1", "--glob=refs/worktree"]]
        self.assertEqual([c[1] for c in reachability], [str(merged)])
        self.assertEqual([c for c in commands if c[2:3] and c[2] in REPLACED and c not in reachability], [],
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

    def test_clean_evidence_a_bare_repository_s_registry_listing_runs_where_the_argument_resolves(self):
        """The project-command delta, pc:124-133 (lead ruling R-75 (j)): the
        identity probe and the registry listing run in the directory the
        argument resolves to, row 4 there because the main worktree is not
        yet known; root being null for a bare repository, the repository-wide
        probes after them run in its common directory. A bare repository is
        reached through a linked worktree, since row 3 fails in its own
        directory, and `clean` then refuses it, before any status probe."""
        source = self.repo("source")
        bare = self.base / "bare.git"
        self.git(self.base, "clone", "-q", "--bare", source, bare)
        tree = self.base / "bare-tree"
        self.git(bare, "worktree", "add", "-q", tree, "main")
        head = self.git(bare, "rev-parse", "refs/heads/main").strip()
        common = os.path.realpath(bare)
        result, records = self.counted("clean", tree)
        self.assert_status(result, 2)
        self.assertEqual((result.stdout, result.stderr),
                         ("", "REFUSED: " + TEXT["target_not_repository_root"].format(PATH=tree) + "\n"))
        self.assertEqual([command(record)[1:] for record in records if command(record)[:1] == ["-C"]],
                         [[str(tree), *ROW_3], [str(tree), *ROW_4], [common, *row_4c(common)], [common, *ROW_6],
                          [common, "for-each-ref", f"--merged={head}", "--format=%(refname)", "refs/heads"]],
                         "rows 3 and 4 where the argument resolves; rows 4c, 6 and 7 in the common directory")
        self.assertEqual(self.status_dirs(records), [])
        self.assert_pinned(records)

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

        with self.subTest("two present entries with one realpath and one admin id (lead ruling R-67 (c))"):
            # A copied admin directory whose `gitdir` file names the worktree
            # through a symbolic link: the registry lists one worktree under two
            # spellings, and the two-way check alone passes both, with one admin
            # id, since both read one `.git` file. Both are registration-mismatch,
            # as two entries naming one path are.
            twin_root = self.repo("twin-repo")
            self.bare_remote(twin_root, "twin-remote.git")
            spelled = self.merged_worktree("021-spelled", root=twin_root)
            control = self.merged_worktree("022-control", root=twin_root)
            link = self.base / "twin-link"
            link.symlink_to(self.base)
            admin = self.common_dir(twin_root) / "worktrees"
            shutil.copytree(admin / spelled.name, admin / f"{spelled.name}-copy")
            (admin / f"{spelled.name}-copy" / "gitdir").write_text(f"{link / spelled.name / '.git'}\n")
            spellings = sorted([str(spelled), str(link / spelled.name)])
            result, records = self.report(twin_root)
            listed = {row["path"]: row for row in result.document["worktrees"]}
            for path in spellings:
                with self.subTest(path=path):
                    row = listed[path]
                    self.assertEqual((row["present"], row["dirty"], row["errors"], row["classification"]),
                                     (True, None, [], "inspection-error"))
                    self.assertNotIn("prunable", row)
            self.assertEqual(listed[str(control)]["classification"], "merged-removable")
            self.assertEqual(self.status_dirs(records), sorted(map(str, (twin_root, control))),
                             "no status probe under either spelling")
            # In process: verify_registration() alone passes both spellings with
            # one admin id, and worktree_rows() makes both `registered` false,
            # building every row or the two twins together, as match_target()
            # builds P's rows.
            with mock.patch.dict(os.environ, self.env, clear=True):
                run = project.Invocation()
                repo = project.inspect_repository(os.fsencode(twin_root), run)
                common = repo["identity"]["common_dir"]
                verdicts = [project.verify_registration(os.fsencode(path), common, False) for path in spellings]
                every = project.worktree_rows(repo, run)
                twins = [record for record in repo["records"] if os.fsdecode(record["path"]) in spellings]
                together = project.worktree_rows(repo, run, records=twins)
            self.assertEqual(verdicts, [(True, os.fsencode(spelled.name))] * 2)
            for label, rows in (("every row", every), ("the twins together", together)):
                with self.subTest(label):
                    self.assertEqual(sorted((os.fsdecode(row.raw_path), row.registered, row.admin_id, row.status)
                                            for row in rows if os.fsdecode(row.raw_path) in spellings),
                                     [(path, False, None, None) for path in spellings])

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
        # With refs/heads/HEAD present, Git 2.43.0 warns "refname 'HEAD' is
        # ambiguous." on standard error in every worktree's status probe, the
        # main worktree's included, so no row's state is established there
        # (status_warned(); lane 3's US2 M-1, lead ruling R-101 (e)).
        warned = {"code": "probe-failed", "message": git_message(
            "status", "row_error_probe_failed", DETAIL=TEXT["row_error_probe_failed_unparseable"])}
        row = rows[tree.name]
        self.assertEqual([row[key] for key in ("branch", "upstream", "remote_present", "ahead", "behind", "errors",
                                               "classification", "recommendation")],
                         ["HEAD", None, None, None, None, [warned, error], "inspection-error",
                          RECOMMENDATIONS["inspection-error"]])
        self.assertEqual((row["present"], row["dirty"], row["merged_into_target"]), (True, None, True),
                         "the status probe ran and row 7 still reads it")
        self.assertIn(str(tree), self.status_dirs(records))
        self.assertEqual([(rows[name]["upstream"], rows[name]["errors"], rows[name]["classification"])
                          for name in ("repo", merged.name)],
                         [("origin/main", [warned], "inspection-error"),
                          ("origin/001-merged", [warned], "inspection-error")])

    # Lead ruling R-54 X-1: each evidence step's pure decider, on literal inputs,
    # with every Git child and filesystem call failing the test.

    def no_io(self):
        stack = contextlib.ExitStack()
        for owner, name in ((project, "run_bounded"), (project, "fs_call"), (os, "lstat"), (os, "stat"),
                            (os.path, "realpath")):
            stack.enter_context(mock.patch.object(owner, name, side_effect=AssertionError(f"{name} ran")))
        return stack

    def assert_decides(self, decider, cases):
        """Each case (label, args, kwargs, expected): the answer, the same again,
        and the inputs unchanged (an exception compared by its type, args and
        attributes, since exceptions compare by identity)."""
        def snapshot(value):
            if isinstance(value, BaseException):
                return (type(value), value.args, getattr(value, "errno", None), snapshot(getattr(value, "error", None)))
            if isinstance(value, dict):
                return {key: snapshot(item) for key, item in value.items()}
            if isinstance(value, (list, tuple)):
                return [snapshot(item) for item in value]
            return value

        with self.no_io():
            for label, args, kwargs, expected in cases:
                with self.subTest(label):
                    before = snapshot((args, kwargs))
                    self.assertEqual(decider(*args, **kwargs), expected)
                    self.assertEqual(decider(*args, **kwargs), expected, "the same inputs, the same answer")
                    self.assertEqual(snapshot((args, kwargs)), before, "the decider changes nothing")

    def test_clean_presence_from_lstat_decides_on_literal_results(self):
        # R-36: ENOENT and ENOTDIR are `present: false`; any other failure is
        # null with its row error, an OSError's built as `os-error` for lstat.
        found = os.stat_result((0o40755, 7, 3, 1, 0, 0, 4096, 0, 0, 0))
        denied = {"code": "os-error", "message": TEXT["row_error_os_error"].format(
            OPERATION="lstat", STRERROR=os.strerror(errno.EACCES))}
        cut = {"code": "probe-timeout", "message": TEXT["row_error_probe_timeout"].format(OPERATION="lstat", S="5")}
        self.assert_decides(project.presence_from_lstat, [
            ("a value", (found,), {}, (True, None)),
            ("ENOENT", (FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT)),), {}, (False, None)),
            ("ENOTDIR", (NotADirectoryError(errno.ENOTDIR, os.strerror(errno.ENOTDIR)),), {}, (False, None)),
            ("EACCES", (PermissionError(errno.EACCES, os.strerror(errno.EACCES)),), {}, (None, denied)),
            ("ENOENT through fs_call", (project.EvidenceError(denied, errno.ENOENT),), {}, (False, None)),
            ("ENOTDIR through fs_call", (project.EvidenceError(denied, errno.ENOTDIR),), {}, (False, None)),
            ("EACCES through fs_call", (project.EvidenceError(denied, errno.EACCES),), {}, (None, denied)),
            ("cut at its budget", (project.EvidenceError(cut),), {}, (None, cut)),
        ])

    def test_clean_registration_verdict_decides_on_literal_realpaths(self):
        # D7, FR-055; R-57 L3 and R-59 D5: the two-way check over realpaths
        # already read, a shared registry path disagreeing whatever was read.
        common, worktrees, admin, dotgit = b"/r/.git", b"/r/.git/worktrees", b"/r/.git/worktrees/wt", b"/w/wt/.git"
        holds = {"worktrees": worktrees, "back": dotgit, "dotgit": dotgit, "commondir": common}
        self.assert_decides(project.registration_verdict, [
            ("main, .git the common directory", (True, common, None), {"dotgit": common}, (True, None)),
            ("main, a gitfile naming it", (True, common, common), {}, (True, None)),
            ("main, a gitfile naming another", (True, common, b"/x/.git"), {}, (False, None)),
            ("main, .git another directory", (True, common, None), {"dotgit": b"/w/.git"}, (False, None)),
            ("linked, both ways", (False, common, admin), holds, (True, b"wt")),
            ("linked, no gitfile", (False, common, None), {}, (False, None)),
            ("linked, an admin directory outside worktrees/", (False, common, b"/x/worktrees/wt"),
             {"worktrees": worktrees}, (False, None)),
            ("linked, its gitdir file missing or empty", (False, common, admin), {"worktrees": worktrees},
             (False, None)),
            ("linked, its gitdir file naming another .git", (False, common, admin),
             dict(holds, back=b"/w/other/.git"), (False, None)),
            # R-125: Git takes the worktree's common directory from its commondir.
            ("linked, its commondir naming another repository", (False, common, admin),
             dict(holds, commondir=b"/x/.git"), (False, None)),
            ("linked, no commondir file: its admin directory", (False, common, admin), dict(holds, commondir=admin),
             (False, None)),
            ("linked, its commondir not read", (False, common, admin), dict(holds, commondir=None), (False, None)),
            ("linked, a shared path", (False, common, admin), dict(holds, shared=True), (False, None)),
            ("main, a shared path", (True, common, common), {"shared": True}, (False, None)),
            ("a shared path, nothing read", (False, common, None), {"shared": True}, (False, None)),
        ])
        self.assert_decides(project.shared_paths, [
            ("one path listed three times", ([{"path": b"/a"}, {"path": b"/b"}, {"path": b"/a"}, {"path": b"/a"}],),
             {}, frozenset({b"/a"})),
            ("distinct paths", ([{"path": b"/a"}, {"path": b"/b"}],), {}, frozenset()),
            ("no entry", ([],), {}, frozenset()),
        ])

        # R-67 (c): among the reads of the rows built together, present rows
        # with one realpath, or one admin id, are registration-mismatch too.
        def read(tree, admin_id=None, registered=True, present=True):
            return {"present": present, "tree": tree, "registered": registered, "admin_id": admin_id}

        self.assert_decides(project.shared_identities, [
            ("one realpath under two spellings",
             ([read(b"/w/a", b"a"), read(b"/w/b", b"b"), read(b"/w/a", b"a")],), {}, frozenset({0, 2})),
            ("one admin id, two realpaths", ([read(b"/w/a", b"x"), read(b"/w/b", b"x")],), {}, frozenset({0, 1})),
            ("one realpath, one registration that disagreed",
             ([read(b"/w/a", b"a"), read(b"/w/a", registered=False)],), {}, frozenset({0, 1})),
            ("a row not present is compared by neither (L2)",
             ([read(b"/w/a", b"a"), read(b"/w/a", b"a", registered=None, present=False)],), {}, frozenset()),
            ("a row whose presence is unknown",
             ([read(b"/w/a", b"a"), read(b"/w/a", b"a", registered=None, present=None)],), {}, frozenset()),
            ("realpaths not read", ([read(None, registered=None), read(None, registered=None)],), {}, frozenset()),
            ("null admin ids: the main worktree and disagreeing registrations",
             ([read(b"/r"), read(b"/w/a", registered=False), read(b"/w/b", registered=False)],), {}, frozenset()),
            ("distinct realpaths and admin ids", ([read(b"/w/a", b"a"), read(b"/w/b", b"b")],), {}, frozenset()),
            ("no read", ([],), {}, frozenset()),
        ])
        self.assert_decides(project.gitdir_line, [
            ("a relative value", (b"gitdir: ../x\n",), {}, b"../x"),
            ("an absolute value and CRLF", (b"gitdir: /a/b\r\n",), {}, b"/a/b"),
            ("no value", (b"gitdir: \n",), {}, None),
            ("not a gitdir line", (b"ref: refs/heads/main\n",), {}, None),
            ("empty", (b"",), {}, None),
        ])

    def test_clean_main_worktree_decision_decides_on_literal_values(self):
        # D8, FR-055; R-36, R-42, R-51 (a): bare, missing, the first record's
        # realpath, then core.worktree, then a candidate toplevel's gitfile.
        common = b"/r/.git"
        checkout, gitfile_main, bare = ({"path": b"/r", "bare": False}, {"path": common, "bare": False},
                                        {"path": b"/r.git", "bare": True})

        def identity(present, realpath):
            return {"common_dir": common, "first_present": present, "first_realpath": realpath}

        layout = identity(True, common)
        self.assert_decides(project.main_worktree_decision, [
            ("no record", (identity(None, None), [], None, {}), {}, (None, "missing")),
            ("a bare first record", (identity(None, None), [bare, checkout], None, {}), {}, (None, "bare")),
            ("a first record not present", (identity(False, None), [checkout], None, {}), {}, (None, "missing")),
            ("its presence unknown", (identity(None, None), [checkout], None, {}), {}, (None, "unreadable")),
            ("its realpath not read", (identity(True, None), [checkout], None, {}), {}, (None, "unreadable")),
            ("an ordinary main worktree", (identity(True, b"/r"), [checkout], None, {b"/r": None}), {},
             (b"/r", None)),
            ("gitfile layout: core.worktree first", (layout, [gitfile_main], b"/checkout", {b"/top": common}), {},
             (b"/checkout", None)),
            ("gitfile layout: the first candidate naming it",
             (layout, [gitfile_main], None, {b"/a": b"/x/.git", b"/top": common, b"/b": common}), {},
             (b"/top", None)),
            ("gitfile layout: no candidate names it", (layout, [gitfile_main], None, {b"/top": None}), {},
             (None, "unnamed")),
            ("gitfile layout: no candidate", (layout, [gitfile_main], None, {}), {}, (None, "unnamed")),
        ])

    def test_clean_row_evidence_assembles_a_row_from_literal_reads(self):
        # D6, D7, FR-006, FR-042; R-61 (b): the row, its classification and its
        # notes from a registry record, the row's reads, row 6 and row 7.
        def record(branch=b"refs/heads/f", prunable=False):
            return {"path": b"/w/f", "head": "a" * 40, "branch": branch, "bare": False, "detached": branch is None,
                    "locked": False, "locked_reason": None, "prunable": prunable, "prunable_reason": None}

        def ref(name, upstream=None, present=None, ahead=None, behind=None, oid="a" * 40):
            short = upstream and upstream.removeprefix(b"refs/remotes/")
            return {"refname": name, "objectname": oid, "symref": None, "upstream": upstream,
                    "upstream_short": short, "remote_present": present, "ahead": ahead, "behind": behind}

        parser = project.StatusParser()
        parser.feed(b"")
        clean = parser.finish()
        refs = {b"refs/heads/f": ref(b"refs/heads/f", b"refs/remotes/origin/f", True, 0, 0),
                b"refs/remotes/origin/f": ref(b"refs/remotes/origin/f", oid="b" * 40),
                b"refs/heads/g": ref(b"refs/heads/g", b"refs/remotes/origin/g", False),
                b"refs/heads/HEAD": ref(b"refs/heads/HEAD", b"refs/remotes/origin/main", True, 0, 0),
                b"refs/heads/main": ref(b"refs/heads/main", b"refs/remotes/origin/main", True, 0, 0)}
        merged = frozenset({b"refs/heads/f", b"refs/heads/g", b"refs/heads/HEAD", b"refs/heads/main"})
        failed = {"code": "probe-failed", "message": "m"}
        head_error = {"code": "probe-failed", "message": git_message(
            "for-each-ref", "row_error_probe_failed", DETAIL=TEXT["row_error_probe_failed_unparseable"])}

        def read(**change):
            return {"present": True, "dev": 1, "ino": 2, "active": b"/elsewhere", "tree": b"/w/f",
                    "registered": True, "admin_id": b"f", "status": clean, "errors": [], **change}

        stale = read(present=False, dev=None, ino=None, tree=None, registered=None, admin_id=None, status=None)
        cases = [
            # label, record, raw, main, read, merged set, expected fields
            ("merged, not current", record(), b"/w/f", False, read(), merged,
             {"upstream": "origin/f", "remote_present": True, "ahead": 0, "behind": 0, "dirty": False,
              "ignored_files": 0, "current": False, "merged_into_target": True,
              "classification": "merged-removable", "errors": [], "notes": []}),
            ("inside the row", record(), b"/w/f", False, read(active=b"/w/f/sub"), merged,
             {"current": True, "classification": "merged-current"}),
            ("the row itself", record(), b"/w/f", False, read(active=b"/w/f"), merged, {"current": True}),
            ("a sibling sharing a prefix", record(), b"/w/f", False, read(active=b"/w/foo"), merged,
             {"current": False}),
            ("the root holds every directory", record(), b"/w/f", False, read(tree=b"/"), merged,
             {"current": True}),
            ("the working directory unread", record(), b"/w/f", False, read(active=None, errors=[failed]), merged,
             {"current": None, "errors": [failed], "classification": "inspection-error"}),
            ("a deleted upstream, merged", record(b"refs/heads/g"), b"/w/f", False, read(), merged,
             {"upstream": "origin/g", "remote_present": False, "ahead": None, "behind": None,
              "classification": "merged-removable"}),
            ("a branch named HEAD", record(b"refs/heads/HEAD"), b"/w/f", False, read(errors=[failed]), merged,
             {"branch": "HEAD", "upstream": None, "remote_present": None, "ahead": None, "behind": None,
              "merged_into_target": True, "errors": [failed, head_error], "classification": "inspection-error"}),
            ("stale", record(prunable=True), b"/w/f", False, stale, merged,
             {"present": False, "upstream": None, "merged_into_target": None, "current": None, "dirty": None,
              "classification": "stale-worktree", "prunable": True}),
            ("registration disagrees", record(), b"/w/f", False,
             read(registered=False, admin_id=None, status=None), merged,
             {"dirty": None, "errors": [], "classification": "inspection-error"}),
            ("row 7 not run", record(), b"/w/f", False, read(), None,
             {"merged_into_target": None, "classification": "review-required"}),
            ("detached", record(None), b"/w/f", False, read(), merged,
             {"branch": "detached", "upstream": None, "merged_into_target": None, "classification": "detached"}),
            ("the main worktree on the target", record(b"refs/heads/main"), b"/r", True, read(tree=b"/r"), merged,
             {"path": "/r", "classification": "protected-default"}),
            ("a path not valid UTF-8", record(), b"/w/\xff", False, read(), merged,
             {"path": "/w/\\xff", "path_valid_utf8": False}),
        ]
        with self.no_io():
            for label, entry, raw, main, reads, merged_set, expected in cases:
                with self.subTest(label):
                    before = copy.deepcopy((entry, reads, refs))
                    row = project.row_evidence(entry, raw, main, reads, refs, merged_set, "main")
                    self.assertIsInstance(row, project.WorktreeRow)
                    keys = ROW_KEYS[:14] + (["prunable"] if "prunable" in expected else []) + ROW_KEYS[14:]
                    self.assertEqual(list(row), keys)
                    self.assertEqual({key: row[key] for key in expected}, expected)
                    self.assertEqual(row["recommendation"], project.classify(row, "main")[1])
                    self.assertEqual([getattr(row, name) for name in ("raw_path", "main", "dev", "ino", "registered",
                                                                      "admin_id", "status")],
                                     [raw, main, reads["dev"], reads["ino"], reads["registered"],
                                      reads["admin_id"], reads["status"]])
                    self.assertIsNot(row["errors"], reads["errors"])
                    self.assertEqual((entry, reads, refs), before, "row_evidence() changes nothing")
                    self.assertEqual(project.row_evidence(entry, raw, main, reads, refs, merged_set, "main"), row)
            first = project.row_evidence(record(), b"/w/f", False, read(), refs, merged, "main")
            gone = project.row_evidence(record(b"refs/heads/g"), b"/w/f", False, read(), refs, merged, "main")
        self.assertEqual((first.upstream_oid, gone.upstream_oid), ("b" * 40, None))

    def test_clean_evidence_memo_by_device_and_inode_and_the_row_5_switch(self):
        # R-54 X-1: inspect_repository() memoizes by the common directory's
        # (dev, ino), so another directory of the repository runs only row 3;
        # repeat_identity_at_root=False runs no row 5 and is memoized apart.
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-merged")
        found = os.lstat(self.common_dir())

        def identity_dirs(spy):
            dirs = [os.fsdecode(call.args[0][1][1]) for call in spy.call_args_list
                    if call.args[0][1][2:3] == ["rev-parse"]]
            spy.reset_mock()
            return dirs

        with mock.patch.dict(os.environ, self.env, clear=True), \
                mock.patch.object(project, "run_bounded", wraps=project.run_bounded) as spy:
            run = project.Invocation()
            from_tree = project.inspect_repository(os.fsencode(tree), run)
            with_row_5 = identity_dirs(spy)
            from_root = project.inspect_repository(os.fsencode(root), run)
            children = len(spy.call_args_list)
            memo_dirs = identity_dirs(spy)
            other = project.Invocation()
            without = project.inspect_repository(os.fsencode(tree), other, repeat_identity_at_root=False)
            without_row_5 = identity_dirs(spy)
            default = project.inspect_repository(os.fsencode(tree), other)
            again = identity_dirs(spy)
        self.assertEqual(list(run.common_dirs), [(found.st_dev, found.st_ino)])
        self.assertIs(from_root, from_tree)
        self.assertEqual((children, memo_dirs), (1, [str(root)]), "a memo hit runs only row 3")
        self.assertEqual(with_row_5, [str(tree), str(root)], "row 3 in the worktree, row 5 at the root")
        self.assertEqual(without_row_5, [str(tree)], "no row 5")
        self.assertEqual(without["identity"]["root"], os.fsencode(root))
        self.assertIsNot(default, without, "the two are memoized apart")
        self.assertEqual(again, [str(tree), str(root)])
        self.assertEqual(len(other.common_dirs), 2)
        self.assertIn((found.st_dev, found.st_ino), other.common_dirs)

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

    def fake_script(self, name, body):
        """An sh script self.base/fake-NAME/git that runs body, then execs the real
        git with its arguments: a fake to stand behind the counting wrapper."""
        path = self.base / f"fake-{name}" / "git"
        path.parent.mkdir()
        path.write_text(f"#!/bin/sh\n{body}\nexec {shlex.quote(clean_support.REAL_GIT)} \"$@\"\n")
        path.chmod(0o755)
        return path

    def test_clean_evidence_verifies_each_identity_immediately_before_its_status_probe(self):
        # The project-command delta, pc:124-126: a worktree probe runs "only
        # after that worktree's identity has been verified immediately before";
        # lane 3's env H-1, lead ruling R-101 (e) and (j). R-67 (c)'s twins are
        # still decided from every row's first read before any probe; each other
        # row's lstat, realpath and registration are read again just before its
        # own probe, and a row whose identity changed gets none.
        root = self.repo()
        self.bare_remote()
        first = self.merged_worktree("001-first")
        swapped = self.merged_worktree("002-swapped")

        with self.subTest("each row's identity is read after the previous row's probe"):
            events = []
            real_fs_call, real_status_probe = project.fs_call, project.status_probe

            def fs_call(fn, *args, **kwargs):
                # A bounded filesystem call on the row's own path: its lstat
                # in the first read, its whole identity in the second.
                if args and isinstance(args[0], (bytes, str)):
                    events.append(("read", os.fsencode(args[0])))
                return real_fs_call(fn, *args, **kwargs)

            def status_probe(path, run):
                events.append(("status", path))
                return real_status_probe(path, run)

            with mock.patch.dict(os.environ, self.env, clear=True):
                run = project.Invocation()
                repo = project.inspect_repository(os.fsencode(root), run)
                with mock.patch.object(project, "fs_call", fs_call), \
                        mock.patch.object(project, "status_probe", status_probe):
                    rows = project.worktree_rows(repo, run)
            probes = [at for at, event in enumerate(events) if event[0] == "status"]
            self.assertEqual([events[at][1] for at in probes], [row.raw_path for row in rows],
                             "every row probed, in the registry's order")
            for before, at in zip([-1, *probes], probes):
                with self.subTest(row=os.fsdecode(events[at][1])):
                    self.assertIn(("read", events[at][1]), events[before + 1:at],
                                  "its identity is read again after the previous row's probe")

        with self.subTest("a worktree swapped after its first read"):
            # A dirty worktree: once every row's identity is read, the first
            # status child (the main worktree's) moves it aside and puts at its
            # path a copy without the uncommitted file, so its `.git` file and
            # registration still hold and only its device and inode differ.
            (swapped / "uncommitted").write_text("preserve")
            decoy = self.base / "decoy"
            shutil.copytree(swapped, decoy, symlinks=True)
            (decoy / "uncommitted").unlink()
            aside = self.base / "aside"
            marker = self.base / "swapped.marker"
            quoted = {name: shlex.quote(str(path)) for name, path in
                      (("tree", swapped), ("decoy", decoy), ("aside", aside), ("marker", marker))}
            fake = self.fake_script("swap", (
                'case " $* " in *" status "*)\n'
                f'  if [ ! -e {quoted["marker"]} ]; then : > {quoted["marker"]}; '
                f'mv {quoted["tree"]} {quoted["aside"]} && mv {quoted["decoy"]} {quoted["tree"]}; fi;;\nesac'))
            result, records = self.report(root, "--all-safe", real=fake)
            self.assertTrue(marker.exists(), "the swap ran")
            rows = by_name(result.document)
            self.assertEqual([rows[swapped.name][key] for key in ("present", "dirty", "errors", "classification")],
                             [True, None, [], "inspection-error"])
            self.assertEqual(rows[first.name]["classification"], "merged-removable")
            self.assertEqual([entry["path"] for entry in result.document["selected"]], [str(first)])
            self.assertEqual((result.document["completeness"], result.document["refusals"][0]["code"]),
                             ("incomplete", "inspection-incomplete"))
            self.assertEqual(self.status_dirs(records), sorted(map(str, (root, first))),
                             "no status probe at the swapped path")
            self.assertTrue((aside / "uncommitted").exists(), "nothing was removed")

    def decoy_of(self, tree):
        """self.base/decoy: a plain directory holding a copy of each file the
        worktree at tree tracks, and nothing else, so that it reads clean."""
        decoy = self.base / "decoy"
        decoy.mkdir()
        for name in self.git(tree, "ls-files", "-z").split("\0"):
            if name:
                shutil.copy2(tree / name, decoy / name)
        return decoy

    def assert_kept_unprobed(self, root, tree, decoy, *, selected):
        """The preview of `clean ROOT --all-safe`: tree is registration-mismatch
        and inspection-error, no status probe runs in tree or in decoy, only
        selected is selected and the plan is incomplete; then the apply
        refuses with exit 2 and removes nothing."""
        result, records = self.report(root, "--all-safe")
        row = by_name(result.document)[tree.name]
        self.assertEqual([row[key] for key in ("present", "dirty", "errors", "classification")],
                         [True, None, [], "inspection-error"])
        self.assertEqual({entry["path"]: entry["reason"] for entry in result.document["excluded"]}[str(tree)],
                         "registration-mismatch")
        self.assertEqual([entry["path"] for entry in result.document["selected"]], [str(path) for path in selected])
        self.assertEqual((result.document["completeness"], result.document["refusals"][0]["code"]),
                         ("incomplete", "inspection-incomplete"))
        self.assertFalse({str(tree), str(decoy)} & set(self.status_dirs(records)), "no status probe in W or D")
        applied = self.run_cli("clean", root, "--all-safe", "--apply", "--yes")
        self.assert_status(applied, 2)
        self.assertTrue((tree / "local.env").exists(), "W and its ignored file survive")
        for path in selected:
            self.assertTrue(path.exists(), "nothing was removed")
        return records

    def test_clean_a_linked_worktree_whose_work_tree_is_redirected(self):
        # The project-command delta as amended at addd346 (Brett Heap's ruling
        # LQ-11, R-102 (b)); lane 5's RB e7. With extensions.worktreeConfig set,
        # a core.worktree in W's config.worktree made every probe read the decoy
        # D, while Git's removal deleted W with its ignored local.env. Row 4c
        # reads the extension; where it is true, each linked row's effective
        # work tree is read before its status probe.
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-redirected", setup=lambda t: (t / ".gitignore").write_text("*.env\n"))
        plain = self.merged_worktree("002-plain")
        (tree / "local.env").write_text("SECRET=keep-me\n")
        decoy = self.decoy_of(tree)
        self.git(root, "config", "extensions.worktreeConfig", "true")
        config = self.common_dir() / "worktrees" / tree.name / "config.worktree"
        self.git(root, "config", "--file", config, "core.worktree", decoy)
        self.assertEqual(self.git(tree, "rev-parse", "--show-toplevel").strip(), str(decoy), "Git reads D for W")

        records = self.assert_kept_unprobed(root, tree, decoy, selected=[plain])
        commands = [command(record) for record in records]
        self.assertEqual(sorted(c[1] for c in commands if c[2:] == WORK_TREE_PROBE), sorted(map(str, (tree, plain))),
                         "one effective-work-tree probe per linked row")
        self.assertEqual([c[1:] for c in commands if c[2:3] == ["config"]],
                         [[str(root), *row_4c(self.common_dir())]], "row 4c once, in the command directory")
        single = self.run_cli("clean", root, "--apply", "--action", "remove", "--worktree", tree, "--yes")
        self.assert_status(single, 2)
        self.assertTrue((tree / "local.env").exists())
        document = self.run_json("status", root, "--json").document
        entry = {Path(item["path"]).name: item for item in document["repository"]["worktrees"]}[tree.name]
        self.assertEqual((entry["dirty"], entry["classification"]), (None, "inspection-error"))

        with self.subTest("core.bare=true in W's config.worktree"):
            config.write_text("[core]\n\tbare = true\n")
            self.assert_kept_unprobed(root, tree, decoy, selected=[plain])

        with self.subTest("the extension set and neither setting: W's work tree is its path"):
            config.unlink()
            (tree / "local.env").rename(self.base / "local.env")
            result, records = self.report(root, "--all-safe")
            self.assertEqual([entry["path"] for entry in result.document["selected"]], sorted(map(str, (tree, plain))))
            self.assertIn(str(tree), [command(record)[1] for record in records
                                      if command(record)[2:] == WORK_TREE_PROBE])

        with self.subTest("without the extension: no effective-work-tree probe"):
            self.git(root, "config", "--unset", "extensions.worktreeConfig")
            result, records = self.report(root, "--all-safe")
            self.assertEqual([command(record)[1] for record in records if command(record)[2:3] == ["rev-parse"]
                              and command(record)[1] in (str(tree), str(plain))], [])
            self.assertEqual(len(result.document["selected"]), 2)

    def test_clean_a_linked_worktree_whose_work_tree_is_redirected_after_the_plan(self):
        # The review-safety delta as amended at addd346: where the plan's row 4c
        # read true, revalidation reads the target's effective work tree in its
        # identity step, and a difference is identity-changed. A fake git plants
        # the decoy, and an ignored file in W, at the second registry listing,
        # revalidation's, after the plan selected W.
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-late", setup=lambda t: (t / ".gitignore").write_text("*.env\n"))
        decoy = self.decoy_of(tree)
        self.git(root, "config", "extensions.worktreeConfig", "true")
        config = self.common_dir() / "worktrees" / tree.name / "config.worktree"
        count = self.base / "listings"
        quoted = {name: shlex.quote(str(path)) for name, path in
                  (("count", count), ("config", config), ("decoy", decoy), ("env", tree / "local.env"),
                   ("git", clean_support.REAL_GIT))}
        fake = self.fake_script("late", (
            'case " $* " in *" worktree list "*)\n'
            f'  n=$(( $(cat {quoted["count"]} 2>/dev/null || echo 0) + 1 )); echo "$n" > {quoted["count"]}\n'
            f'  if [ "$n" = 2 ]; then {quoted["git"]} config --file {quoted["config"]} core.worktree {quoted["decoy"]}; '
            f"printf 'SECRET=keep-me\\n' > {quoted['env']}; fi;;\nesac"))
        result, records = self.counted("clean", root, "--all-safe", "--apply", "--yes", "--json", real=fake)
        self.assert_status(result, 2)
        self.assertEqual(count.read_text().strip(), "2", "planned, then revalidated")
        [target] = result.document["targets"]
        self.assertEqual((target["path"], target["stage"], target["reason"]),
                         (str(tree), "refused", "identity-changed"))
        self.assertEqual([command(record)[1] for record in records if command(record)[2:] == WORK_TREE_PROBE],
                         [str(tree), str(tree)], "read in planning and again in revalidation")
        self.assertTrue((tree / "local.env").exists(), "W and its ignored file survive")
        self.assertIn(tree.name, self.git(root, "worktree", "list", "--porcelain"))

    def test_clean_a_commondir_that_names_another_repository(self):
        # The project-command delta as amended at 93f3194 (lead ruling R-125;
        # lane 3's W9 M2): Git takes a linked worktree's common directory, and
        # so the config that row 4c reads, from its admin `commondir` file. A
        # planted commondir naming a shared clone X that sets the extension,
        # beside a config.worktree decoy, left row 4c reading R's config unset
        # while Git in W read D. The two-way registration now requires the
        # commondir to name <common_dir>.
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-moved", setup=lambda t: (t / ".gitignore").write_text("*.env\n"))
        (tree / "local.env").write_text("SECRET=keep-me\n")
        decoy = self.decoy_of(tree)
        shared = self.base / "shared-clone"
        self.git(self.base, "clone", "-q", "--shared", root, shared)
        self.git(shared, "branch", "001-moved", "origin/001-moved")
        self.git(shared, "config", "extensions.worktreeConfig", "true")
        admin = self.common_dir() / "worktrees" / tree.name
        self.git(root, "config", "--file", admin / "config.worktree", "core.worktree", decoy)
        written = (admin / "commondir").read_text()
        (admin / "commondir").write_text(f"{shared / '.git'}\n")
        self.assertEqual(self.git(tree, "rev-parse", "--show-toplevel").strip(), str(decoy), "Git reads D for W")

        self.assert_kept_unprobed(root, tree, decoy, selected=[])

        with self.subTest("the commondir as `git worktree add` wrote it"):
            (admin / "commondir").write_text(written)
            self.assertEqual(written.strip(), "../..")
            result, records = self.report(root, "--all-safe")
            row = by_name(result.document)[tree.name]
            self.assertEqual((row["errors"], row["classification"]), ([], "ignored-local-files"),
                             "W's registration agrees as before, and its ignored file keeps it")
            self.assertIn(str(tree), self.status_dirs(records))

    def test_clean_evidence_a_failed_ref_listing_establishes_no_branch_evidence(self):
        # Plan review F3; pcl:121-125 ("A row whose evidence could not be
        # established ... SHALL be classified inspection-error directly,
        # whatever its branch") and pcl:1129-1130 ("Null SHALL mean unknown or
        # not established"). Row 6 fails, so no branch's upstream is read: each
        # present row on a branch carries row 6's error, never `unpublished`
        # with a null upstream that would mean "none configured"; a detached
        # row needs no ref.
        root = self.repo()
        self.bare_remote()
        merged = self.merged_worktree("001-merged")
        detached = self.add("detached", "--detach")
        fake = self.fake_script("row-6", (
            'case " $* " in *" refs/remotes "*) echo "fatal: ref listing failed (fake)" >&2; exit 128;; esac'))
        result, records = self.report(root, real=fake)
        rows = by_name(result.document)
        error = {"code": "probe-failed", "message": git_message(
            "for-each-ref", "row_error_probe_failed", DETAIL=TEXT["row_error_probe_failed_exit"].format(N=128))}
        for name in ("repo", merged.name):
            with self.subTest(row=name):
                self.assertEqual([rows[name][key] for key in ("upstream", "remote_present", "dirty", "errors",
                                                              "classification")],
                                 [None, None, False, [error], "inspection-error"])
        self.assertEqual([rows[detached.name][key] for key in ("branch", "errors", "classification")],
                         ["detached", [], "detached"])
        self.assertEqual((result.document["completeness"], result.document["refusals"][0]["code"]),
                         ("incomplete", "inspection-incomplete"))
        self.assertEqual(self.status_dirs(records), sorted(map(str, (root, merged, detached))),
                         "the status probes still run")

    @clean_support.not_root
    def test_clean_evidence_a_status_probe_that_warns_establishes_nothing(self):
        # Lane 3's US2 M-1, lead ruling R-101 (e); pcl:121-125: a row whose
        # evidence could not be established is inspection-error. Git exits 0
        # from a status it could not finish, printing `warning: could not open
        # directory 'secret/': Permission denied` and no record of the files it
        # could not read, so the row's state is not established. Before this
        # rule the row was selected, and the removal failed with exit 255 and
        # left a broken worktree.
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("001-unreadable")
        control = self.merged_worktree("002-control")
        secret = tree / "secret"
        secret.mkdir()
        (secret / "kept.txt").write_text("preserve")
        secret.chmod(0o300)
        self.addCleanup(secret.chmod, 0o700)
        warned = {"code": "probe-failed", "message": git_message(
            "status", "row_error_probe_failed", DETAIL=TEXT["row_error_probe_failed_unparseable"])}
        result, records = self.report(root, "--all-safe")
        row = by_name(result.document)[tree.name]
        self.assertEqual([row[key] for key in ("present", "dirty", "ignored_files", "errors", "classification")],
                         [True, None, None, [warned], "inspection-error"])
        self.assertIn(str(tree), self.status_dirs(records), "its probe ran")
        self.assertEqual([entry["path"] for entry in result.document["selected"]], [str(control)])
        self.assertEqual((result.document["completeness"], result.document["refusals"][0]["code"]),
                         ("incomplete", "inspection-incomplete"))
        applied = self.run_cli("clean", root, "--all-safe", "--apply", "--yes")
        self.assert_status(applied, 2)
        self.assertTrue(tree.exists() and control.exists(), "nothing was removed")
        self.assertIn(tree.name, self.git(root, "worktree", "list", "--porcelain"))

        with self.subTest("status reports the row as not established"):
            document = self.run_json("status", root, "--json").document
            entry = {Path(item["path"]).name: item for item in document["repository"]["worktrees"]}[tree.name]
            self.assertEqual([entry[key] for key in ("dirty", "classification", "errors")],
                             [None, "inspection-error", [warned]])

        with self.subTest("the rule, on literal outcomes"):
            def outcome(stderr, counted=None):
                return project.DriverOutcome(["git"], "complete", stderr=stderr,
                                             stderr_bytes=len(stderr) if counted is None else counted)

            for label, value, expected in (
                    ("nothing", outcome(b""), False),
                    ("advice lines", outcome(b"hint: Use 'git x'.\nhint:\nhint: to do y.\n"), False),
                    ("Git's warning", outcome(b"warning: could not open directory 'secret/': Permission denied\n"),
                     True),
                    ("a translated warning", outcome(b"Warnung: could not open directory 'secret/'\n"), True),
                    ("an error line", outcome(b"error: x\n"), True),
                    ("advice, then a warning", outcome(b"hint: a\nwarning: b\n"), True),
                    ("a line with no line end", outcome(b"E" * 10), True),
                    ("advice past the head kept", outcome(b"hint: a\n", counted=5000), True)):
                with self.subTest(label):
                    self.assertIs(project.status_warned(value), expected)

    # T030: the evidence model's scenarios (rule 1: test_status_, plan review M14).

    def test_status_a_git_that_floods_standard_error(self):
        # The probe completes with its records, no probe-timeout, its standard
        # error capped. A status probe whose standard error holds anything but
        # Git's advice lines has not established the row's state (lane 3's US2
        # M-1, lead ruling R-101 (e); status_warned()), so the row reads
        # inspection-error with `dirty` null, as a failed probe's does.
        root = self.repo()
        fake_dir = self.base / "fake"
        fake = clean_support.install_fake_git(fake_dir, "flood-stderr", kib=70)
        result, records = self.report(root, real=fake)
        row = by_name(result.document)["repo"]
        warned = {"code": "probe-failed", "message": git_message(
            "status", "row_error_probe_failed", DETAIL=TEXT["row_error_probe_failed_unparseable"])}
        self.assertEqual((row["errors"], row["dirty"], row["classification"]), ([warned], None, "inspection-error"))
        self.assertEqual(self.status_dirs(records), [str(root)])
        self.assertNotIn("EEEE", result.stderr, "the child's standard error is read, never passed on")
        # The standard error kept is capped at 4 KiB, and every byte counted.
        with mock.patch.dict(os.environ, self.path_first(fake_dir), clear=True):
            outcome, error = project.status_probe(os.fsencode(root), project.Invocation())
        self.assertEqual(error, warned)
        self.assertEqual((outcome.name, len(outcome.stderr), outcome.stderr_bytes),
                         ("complete", 4096, 70 * 1024))
        self.assertIs(outcome.result["dirty"], False, "the records were read")

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
        self.assertEqual({**steered.document, "observed_at": None}, {**plain.document, "observed_at": None})
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
