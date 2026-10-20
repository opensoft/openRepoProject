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
plan envelope with its selection, notes and `omitted`.
"""
import os
from pathlib import Path
import shutil
import unittest

import clean_support

project = clean_support.load_project()
TEXT = clean_support.TEXT_FIXTURES

# The status probe's words after `-C PATH` (design D6), as the contract writes them.
STATUS = ["status", "--porcelain=v1", "-z", "--untracked-files=normal", "--ignored=matching"]


def argv_words(record):
    """A counted child's argument vector without its leading -c pins."""
    argv, at = record.argv, 0
    while at + 1 < len(argv) and argv[at] == "-c":
        at += 2
    return argv[at:]


def status_paths(records):
    """The directory of each status probe in the counting log, in spawn order."""
    return [argv_words(record)[1] for record in records if argv_words(record)[2:] == STATUS]


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
            refused = "REFUSED: " + TEXT["plan_incomplete"].format(
                CODE="inspection-incomplete", REMEDY=TEXT["remedy_inspection_incomplete"]) + "\n"
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


if __name__ == "__main__":
    unittest.main()
