"""Lane G of feature 004: the evidence model behind cleanup_report() (T027 to
T033; design D4, D6, D7 and D8; research.md R9; data-model.md, "Repository
identity", "Merge target", "Worktree row", "Worktree identity and
registration", "Branch evidence" and "Classification").

Parity values are literals written into the test (rule 11, research.md R9):
once cleanup_report() reads the evidence model no baseline function remains to
compare against.
"""
import os
from pathlib import Path
import shutil
import unittest

import clean_support

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


if __name__ == "__main__":
    unittest.main()
